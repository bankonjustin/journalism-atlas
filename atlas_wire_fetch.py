"""
atlas_wire_fetch.py
Session 1 of Atlas Wire pipeline.

Pulls last 24h of content from:
  1. ~/Documents/Atlas Spidering/core/rss_pulse_v2_*.json  (most recent Pulse fetch)
  2. Bluesky public API             (for creators with bsky_handle in bluesky-creators.json)

Writes: wire_queue_raw_YYYY-MM-DD.json
"""

import json
import uuid
import time
import glob
import os
import sys
from datetime import datetime, timezone, timedelta

import requests

# ── Config ────────────────────────────────────────────────────────────────────

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))

PULSE_SPIDERING_DIR = os.path.expanduser("~/Documents/Atlas Spidering/core")
BSKY_CREATORS_FILE = os.path.join(REPO_ROOT, "assets", "data", "bluesky-creators.json")

BSKY_API_BASE = "https://public.api.bsky.app/xrpc"
WINDOW_HOURS = 24
BSKY_RATE_LIMIT_DELAY = 0.5  # seconds between Bluesky API calls


# ── Helpers ───────────────────────────────────────────────────────────────────

def parse_dt(s):
    """Parse ISO8601 string to UTC-aware datetime. Returns None on failure."""
    if not s:
        return None
    for fmt in ("%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%S%z"):
        try:
            dt = datetime.strptime(s.rstrip("Z") + "+00:00" if "Z" in s else s, fmt.replace("%z", "") + "+00:00")
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt
        except ValueError:
            continue
    # last resort: dateutil if available
    try:
        from dateutil import parser as dp
        return dp.parse(s).astimezone(timezone.utc)
    except Exception:
        return None


def within_window(dt, cutoff):
    if dt is None:
        return False
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt >= cutoff


def make_item(source, creator_name, creator_url, bluesky_handle, beat, title, link, text_snippet, pub_date_str):
    return {
        "id": str(uuid.uuid4()),
        "source": source,
        "creator_name": creator_name,
        "creator_url": creator_url or "",
        "bluesky_handle": bluesky_handle,
        "beat": beat or "",
        "title": title or "",
        "link": link or "",
        "text_snippet": (text_snippet or "")[:280],
        "pub_date": pub_date_str or "",
        "score": None,
        "wire_frame": None,
        "cluster": None,
        "status": "pending",
    }


# ── Step 1: Build name → bluesky_handle lookup ────────────────────────────────

def build_bsky_lookup():
    with open(BSKY_CREATORS_FILE) as f:
        bsky_creators = json.load(f)
    lookup = {}
    for c in bsky_creators:
        handle = c.get("bsky_handle") or c.get("bluesky_handle")
        if not handle:
            continue
        name_key = c.get("name", "").lower().strip()
        channel_key = c.get("channel", "").lower().strip()
        if name_key:
            lookup[name_key] = (handle, c.get("link") or c.get("channel") or "")
        if channel_key and channel_key not in lookup:
            lookup[channel_key] = (handle, c.get("link") or "")
    return lookup


# ── Step 2: Ingest Pulse RSS items ────────────────────────────────────────────

def fetch_pulse_items(cutoff, bsky_lookup):
    pulse_files = sorted(glob.glob(os.path.join(PULSE_SPIDERING_DIR, "rss_pulse_v2_*.json")))
    if not pulse_files:
        print(f"ERROR: No rss_pulse_v2_*.json found in {PULSE_SPIDERING_DIR}")
        sys.exit(1)

    pulse_path = pulse_files[-1]
    print(f"  Loading: {pulse_path}")

    with open(pulse_path, encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, list):
        posts = data
    else:
        posts = data.get("posts", data.get("items", []))

    print(f"  {len(posts)} posts in Pulse file")
    items = []
    skipped_old = 0

    for post in posts:
        creator = post.get("creator", "")
        channel = post.get("channel", "")
        beat = post.get("topic", "")

        name_key = creator.lower().strip()
        channel_key = channel.lower().strip()
        bsky_info = bsky_lookup.get(name_key) or bsky_lookup.get(channel_key)
        bsky_handle = bsky_info[0] if bsky_info else None
        creator_url = bsky_info[1] if bsky_info else ""

        pub_str = post.get("published", "")
        dt = parse_dt(pub_str)
        if not within_window(dt, cutoff):
            skipped_old += 1
            continue

        items.append(make_item(
            source="rss",
            creator_name=creator,
            creator_url=creator_url,
            bluesky_handle=bsky_handle,
            beat=beat,
            title=post.get("title", ""),
            link=post.get("url", ""),
            text_snippet=post.get("summary", "") or post.get("title", ""),
            pub_date_str=pub_str,
        ))

    print(f"  Pulse: {len(items)} items in window, {skipped_old} outside 24h")
    return items


# ── Step 3: Fetch Bluesky posts ───────────────────────────────────────────────

def fetch_bsky_posts(cutoff, bsky_lookup):
    """
    For each unique handle in the lookup, hit getAuthorFeed and pull posts
    from the last 24h. Returns list of wire items.
    """
    # Collect unique handles → (creator_name, creator_url, beat)
    # We may have multiple name keys mapping to the same handle
    handle_to_meta = {}
    with open(BSKY_CREATORS_FILE) as f:
        bsky_creators = json.load(f)
    for c in bsky_creators:
        handle = c.get("bsky_handle") or c.get("bluesky_handle")
        if not handle:
            continue
        if handle not in handle_to_meta:
            handle_to_meta[handle] = {
                "creator_name": c.get("name", ""),
                "creator_url": c.get("link") or c.get("channel") or "",
                "beat": c.get("topic") or c.get("topic_full") or "",
            }

    items = []
    errors = 0
    total_handles = len(handle_to_meta)

    for i, (handle, meta) in enumerate(handle_to_meta.items()):
        if i % 50 == 0:
            print(f"  Bluesky: {i}/{total_handles} handles fetched...")

        url = f"{BSKY_API_BASE}/app.bsky.feed.getAuthorFeed"
        try:
            r = requests.get(url, params={"actor": handle, "limit": 20}, timeout=10)
            if r.status_code == 400:
                # Handle not found / account deactivated — skip silently
                errors += 1
                time.sleep(BSKY_RATE_LIMIT_DELAY)
                continue
            r.raise_for_status()
        except requests.RequestException as e:
            errors += 1
            time.sleep(BSKY_RATE_LIMIT_DELAY)
            continue

        feed = r.json().get("feed", [])
        for entry in feed:
            post = entry.get("post", {})
            record = post.get("record", {})
            indexed_at = post.get("indexedAt") or record.get("createdAt", "")
            dt = parse_dt(indexed_at)
            if not within_window(dt, cutoff):
                continue

            # Skip reposts — only original posts
            if entry.get("reason", {}).get("$type") == "app.bsky.feed.defs#reasonRepost":
                continue

            uri = post.get("uri", "")  # at://did:.../app.bsky.feed.post/rkey
            rkey = uri.split("/")[-1] if uri else ""
            post_url = f"https://bsky.app/profile/{handle}/post/{rkey}" if rkey else ""

            text = record.get("text", "")

            items.append(make_item(
                source="bluesky",
                creator_name=meta["creator_name"],
                creator_url=meta["creator_url"],
                bluesky_handle=handle,
                beat=meta["beat"],
                title=text[:100] + ("…" if len(text) > 100 else ""),
                link=post_url,
                text_snippet=text,
                pub_date_str=indexed_at,
            ))

        time.sleep(BSKY_RATE_LIMIT_DELAY)

    print(f"  Bluesky: done. {len(items)} posts in window. {errors} handles failed/not found.")
    return items


# ── Step 4: Deduplicate by link ───────────────────────────────────────────────

def deduplicate(items):
    seen_links = set()
    out = []
    for item in items:
        link = item["link"]
        if not link or link not in seen_links:
            if link:
                seen_links.add(link)
            out.append(item)
    return out


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(hours=WINDOW_HOURS)
    date_str = now.strftime("%Y-%m-%d")
    out_file = os.path.join(REPO_ROOT, f"wire_queue_raw_{date_str}.json")

    print(f"Atlas Wire — Fetch")
    print(f"Window: {cutoff.strftime('%Y-%m-%d %H:%M')} UTC → now")

    # Check inputs exist
    if not os.path.exists(BSKY_CREATORS_FILE):
        print(f"ERROR: Missing required file: {BSKY_CREATORS_FILE}")
        sys.exit(1)

    print("\n[1/4] Building Bluesky handle lookup...")
    bsky_lookup = build_bsky_lookup()
    print(f"  {len(bsky_lookup)} name/channel keys → handles")

    print("\n[2/4] Ingesting Pulse RSS items...")
    pulse_items = fetch_pulse_items(cutoff, bsky_lookup)

    bsky_flag = "--skip-bluesky" not in sys.argv
    if bsky_flag:
        print("\n[3/4] Fetching Bluesky author feeds...")
        print(f"  (Pass --skip-bluesky to skip this step)")
        bsky_items = fetch_bsky_posts(cutoff, bsky_lookup)
    else:
        print("\n[3/4] Skipping Bluesky fetch (--skip-bluesky)")
        bsky_items = []

    print("\n[4/4] Merging and deduplicating...")
    all_items = pulse_items + bsky_items
    all_items = deduplicate(all_items)
    # Sort by pub_date descending
    all_items.sort(key=lambda x: x.get("pub_date", ""), reverse=True)

    print(f"\n  Total items: {len(all_items)}")
    print(f"  RSS: {sum(1 for x in all_items if x['source']=='rss')}")
    print(f"  Bluesky: {sum(1 for x in all_items if x['source']=='bluesky')}")
    print(f"  Beats: {sorted(set(x['beat'] for x in all_items if x['beat']))}")

    with open(out_file, "w") as f:
        json.dump(all_items, f, indent=2)

    print(f"\n✓ Written: {out_file}")
    print(f"  Run atlas_wire_rank.py next to score and draft wire copy.")


if __name__ == "__main__":
    main()
