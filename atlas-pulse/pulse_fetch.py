#!/usr/bin/env python3
"""
pulse_fetch.py — Atlas Pulse feed fetcher (Thing 1)

Reads atlas_rss_universe.csv, fetches RSS feeds, outputs pulse_output.json.
Run from the atlas-pulse/ directory (or anywhere — paths are relative to this file).

Usage:
  python pulse_fetch.py                              # HIGH+MEDIUM, 7-day window
  python pulse_fetch.py --tiers HIGH                 # HIGH only (fastest, most reliable)
  python pulse_fetch.py --tiers HIGH,MEDIUM,PENDING  # include YouTube resolution
  python pulse_fetch.py --days 14 --workers 20       # wider window, more parallelism

Requires:
  pip install feedparser requests beautifulsoup4 python-dateutil
"""

import argparse
import csv
import json
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta
from pathlib import Path

try:
    import feedparser
    import requests
    from bs4 import BeautifulSoup
    from dateutil import parser as dateutil_parser
except ImportError as e:
    print(f"Missing dependency: {e}")
    print("Run: pip install feedparser requests beautifulsoup4 python-dateutil")
    sys.exit(1)

HERE = Path(__file__).parent
CSV_PATH = HERE / "atlas_rss_universe.csv"
YOUTUBE_CACHE_PATH = HERE / "youtube_channel_ids.csv"
OUTPUTS_DIR = HERE / "outputs"


# ── Helpers ───────────────────────────────────────────────────────────────────

def platform_bucket(platform_str):
    p = platform_str.lower()
    if "substack" in p: return "substack"
    if "beehiiv" in p:  return "beehiiv"
    if "ghost" in p:    return "ghost"
    if "youtube" in p:  return "youtube"
    if "podcast" in p:  return "podcast"
    return "website"


def strip_html(text):
    text = re.sub(r"<[^>]+>", " ", text or "")
    return re.sub(r"\s+", " ", text).strip()


def parse_date(entry):
    """Try feedparser's parsed tuple first, fall back to dateutil string parsing."""
    for field in ["published_parsed", "updated_parsed"]:
        val = getattr(entry, field, None)
        if val:
            try:
                return datetime(*val[:6])
            except Exception:
                pass
    for field in ["published", "updated"]:
        val = entry.get(field, "")
        if val:
            try:
                return dateutil_parser.parse(val, ignoretz=True)
            except Exception:
                pass
    return None


# ── Feed fetching ─────────────────────────────────────────────────────────────

def fetch_feed(row, cutoff):
    """
    Fetch one RSS feed and return (creator_dict, None) on success
    or (None, error_dict) on failure.
    """
    rss_url = row["rss_url"]
    try:
        feed = feedparser.parse(
            rss_url,
            request_headers={"User-Agent": "Mozilla/5.0 (compatible; AtlasPulse/1.0)"},
        )

        # bozo=True but no entries = real failure
        if feed.bozo and not feed.entries:
            exc = str(getattr(feed, "bozo_exception", "parse error"))[:100]
            return None, _err(row, f"PARSE_ERROR: {exc}")

        posts = []
        for entry in feed.entries:
            pub = parse_date(entry)
            if pub and pub < cutoff:
                continue
            posts.append({
                "title":     strip_html(entry.get("title", ""))[:200],
                "url":       entry.get("link", ""),
                "published": pub.isoformat() if pub else None,
                "summary":   strip_html(entry.get("summary", ""))[:500],
            })

        return {
            "name":       row["name"],
            "channel":    row["channel"],
            "rss_url":    rss_url,
            "platform":   row["platform"],
            "topic":      row["topic"],
            "geography":  row["geography"],
            "group":      row["group"],
            "post_count": len(posts),
            "posts":      posts,
        }, None

    except Exception as e:
        return None, _err(row, f"ERROR: {str(e)[:100]}")


def _err(row, reason):
    return {
        "name":         row["name"],
        "rss_url":      row.get("rss_url", row.get("link", "")),
        "platform":     row["platform"],
        "error_reason": reason,
    }


# ── YouTube channel ID resolution ─────────────────────────────────────────────

def load_youtube_cache():
    cache = {}
    if YOUTUBE_CACHE_PATH.exists():
        with open(YOUTUBE_CACHE_PATH) as f:
            for r in csv.DictReader(f):
                cache[r["link"]] = r["rss_url"]
    return cache


def save_youtube_cache(cache):
    with open(YOUTUBE_CACHE_PATH, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["link", "rss_url"])
        writer.writeheader()
        for link, rss_url in cache.items():
            writer.writerow({"link": link, "rss_url": rss_url})


def resolve_youtube_channel_id(handle_url):
    """Scrape a YouTube @handle page to extract the channel_id."""
    try:
        r = requests.get(
            handle_url,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=10,
        )
        soup = BeautifulSoup(r.text, "html.parser")

        # Method A: <link rel="canonical" href="...channel/UCxxx...">
        canonical = soup.find("link", rel="canonical")
        if canonical and "channel/" in canonical.get("href", ""):
            cid = canonical["href"].split("channel/")[-1].strip("/")
            return f"https://www.youtube.com/feeds/videos.xml?channel_id={cid}"

        # Method B: og:url meta tag
        og = soup.find("meta", property="og:url")
        if og and "channel/" in og.get("content", ""):
            cid = og["content"].split("channel/")[-1].strip("/")
            return f"https://www.youtube.com/feeds/videos.xml?channel_id={cid}"

    except Exception:
        pass
    return None


def resolve_youtube_feeds(pending_youtube, rows_to_fetch, failed):
    """Resolve channel IDs for all PENDING YouTube rows, updating cache."""
    print(f"Resolving {len(pending_youtube)} YouTube channel IDs...")
    cache = load_youtube_cache()
    resolved = 0

    for row in pending_youtube:
        link = row["link"]
        if link in cache:
            row["rss_url"] = cache[link]
            rows_to_fetch.append(row)
            resolved += 1
            continue

        rss_url = resolve_youtube_channel_id(link)
        if rss_url:
            cache[link] = rss_url
            row["rss_url"] = rss_url
            rows_to_fetch.append(row)
            resolved += 1
            print(f"  ✓ {row['name']}")
        else:
            failed.append(_err(row, "YOUTUBE_UNRESOLVED"))
            print(f"  ✗ {row['name']} ({link})")

        time.sleep(0.5)  # be polite to YouTube

    save_youtube_cache(cache)
    unresolved = len(pending_youtube) - resolved
    print(f"YouTube: {resolved} resolved, {unresolved} failed\n")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(description="Atlas Pulse — RSS feed fetcher")
    ap.add_argument("--days",    type=int, default=7,                  help="Lookback window in days (default: 7)")
    ap.add_argument("--workers", type=int, default=10,                 help="Parallel fetch workers (default: 10)")
    ap.add_argument("--tiers",   default="HIGH,MEDIUM",                help="Comma-separated tiers to run: HIGH,MEDIUM,PENDING (default: HIGH,MEDIUM)")
    ap.add_argument("--output",  default="pulse_output.json",          help="Output file path (default: pulse_output.json)")
    args = ap.parse_args()

    tiers = {t.strip().upper() for t in args.tiers.split(",")}
    cutoff = datetime.now() - timedelta(days=args.days)
    output_path = HERE / args.output
    OUTPUTS_DIR.mkdir(exist_ok=True)

    print(f"\nAtlas Pulse — Feed Fetcher")
    print(f"Tiers: {', '.join(sorted(tiers))} | Window: {args.days} days | Workers: {args.workers}")
    print(f"Cutoff: {cutoff.strftime('%Y-%m-%d')}\n")

    # Load and partition CSV rows
    with open(CSV_PATH) as f:
        all_rows = list(csv.DictReader(f))

    rows_to_fetch = []
    pending_youtube = []
    pending_podcast = []
    failed = []

    for row in all_rows:
        conf = row["confidence"].strip().upper()
        plat = row["platform"].lower()
        if conf in ("HIGH", "MEDIUM") and conf in tiers:
            rows_to_fetch.append(row)
        elif conf == "PENDING" and "PENDING" in tiers:
            if "youtube" in plat:
                pending_youtube.append(row)
            else:
                # Podcasts: flag as skipped
                failed.append(_err(row, "PODCAST_SKIPPED"))
                pending_podcast.append(row)

    print(f"HIGH/MEDIUM feeds queued: {len(rows_to_fetch)}")
    if "PENDING" in tiers:
        print(f"YouTube to resolve:        {len(pending_youtube)}")
        print(f"Podcasts skipped:          {len(pending_podcast)}")
    print()

    # Phase 2: YouTube channel ID resolution
    if pending_youtube:
        resolve_youtube_feeds(pending_youtube, rows_to_fetch, failed)

    # Phase 1: Parallel feed fetch
    print(f"Fetching {len(rows_to_fetch)} feeds with {args.workers} workers...")
    creators = []
    total = len(rows_to_fetch)
    done = 0

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(fetch_feed, row, cutoff): row for row in rows_to_fetch}
        for future in as_completed(futures):
            result, error = future.result()
            done += 1
            if result:
                creators.append(result)
            else:
                failed.append(error)
            if done % 50 == 0 or done == total:
                print(f"  {done}/{total} — {len(creators)} OK, {len(failed)} failed")

    # Sort by post count descending so top producers surface first
    creators.sort(key=lambda c: c["post_count"], reverse=True)

    # Build platform breakdown (post counts, not feed counts)
    platform_breakdown = {k: 0 for k in ("substack", "beehiiv", "ghost", "website", "youtube", "podcast")}
    posts_total = 0
    for c in creators:
        bucket = platform_bucket(c["platform"])
        platform_breakdown[bucket] = platform_breakdown.get(bucket, 0) + c["post_count"]
        posts_total += c["post_count"]

    # ── Write pulse_output.json ───────────────────────────────────────────────
    output = {
        "run_metadata": {
            "generated_at":        datetime.now().isoformat(),
            "days_window":         args.days,
            "feeds_attempted":     len(rows_to_fetch),
            "feeds_successful":    len(creators),
            "feeds_failed":        len(failed),
            "posts_retrieved":     posts_total,
            "platform_breakdown":  platform_breakdown,
        },
        "creators": creators,
    }

    with open(output_path, "w") as f:
        json.dump(output, f, indent=2)

    # Dated archive copy
    dated = OUTPUTS_DIR / f"pulse_output_{datetime.now().strftime('%Y%m%d')}.json"
    with open(dated, "w") as f:
        json.dump(output, f, indent=2)

    # ── Write pulse_run_log.txt ───────────────────────────────────────────────
    log_path = HERE / "pulse_run_log.txt"
    with open(log_path, "w") as f:
        f.write(f"Atlas Pulse run — {datetime.now().isoformat()}\n")
        f.write(f"Tiers: {', '.join(sorted(tiers))} | Days: {args.days} | Workers: {args.workers}\n")
        f.write(f"Feeds attempted:  {len(rows_to_fetch)}\n")
        f.write(f"Feeds successful: {len(creators)}\n")
        f.write(f"Feeds failed:     {len(failed)}\n")
        f.write(f"Posts retrieved:  {posts_total}\n\n")
        f.write("Platform breakdown (post counts):\n")
        for plat, count in platform_breakdown.items():
            f.write(f"  {plat:<12} {count}\n")
        f.write("\nTop creators by post count:\n")
        for c in creators[:25]:
            f.write(f"  {c['name']:<35} {c['channel']:<35} {c['post_count']} posts\n")
        if failed:
            f.write(f"\nFailed feeds ({len(failed)}):\n")
            for err in failed:
                f.write(f"  {err['name']:<35} {err['error_reason']}\n")

    # ── Write pulse_failed_feeds.csv ─────────────────────────────────────────
    failed_path = HERE / "pulse_failed_feeds.csv"
    with open(failed_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "rss_url", "platform", "error_reason"])
        writer.writeheader()
        writer.writerows(failed)

    # ── Summary ───────────────────────────────────────────────────────────────
    print(f"\nDone.")
    print(f"  Feeds:  {len(creators)} successful / {len(failed)} failed")
    print(f"  Posts:  {posts_total} retrieved")
    print(f"  Output: {output_path}")
    print(f"  Log:    {log_path}")
    if failed:
        print(f"  Failed: {failed_path} ({len(failed)} entries)")


if __name__ == "__main__":
    main()
