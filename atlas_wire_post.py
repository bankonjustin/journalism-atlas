"""
atlas_wire_post.py
Session 2 of Atlas Wire pipeline.

Takes wire_approved_YYYY-MM-DD.json (exported from atlas_wire_review.html),
posts each item to Bluesky, then appends to wire.json for the public site.

Usage:
  python3 atlas_wire_post.py                         # uses today's approved file
  python3 atlas_wire_post.py wire_approved_X.json
  python3 atlas_wire_post.py --dry-run               # print posts, no network calls

Requires (in .env or shell environment):
  BSKY_HANDLE       e.g. journalismatlas.com
  BSKY_APP_PASSWORD e.g. xxxx-xxxx-xxxx-xxxx  (from Settings → App Passwords)
  BSKY_PDS_URL      optional override, defaults to https://bsky.social
"""

import json
import os
import sys
import time
import glob
from datetime import datetime, timezone

import requests

# ── Config ────────────────────────────────────────────────────────────────────

REPO_ROOT       = os.path.dirname(os.path.abspath(__file__))
WIRE_JSON_FILE  = os.path.join(REPO_ROOT, "wire.json")
POST_DELAY      = 4.0   # seconds between posts (Bluesky rate limit courtesy)
WIRE_JSON_CAP   = 500   # max items to keep in wire.json


# ── Load .env ──────────────────────────────────────────────────────────────────

def load_dotenv():
    env_path = os.path.join(REPO_ROOT, ".env")
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip())


# ── Find approved file ─────────────────────────────────────────────────────────

def find_approved_file(argv):
    for arg in argv[1:]:
        if arg.endswith(".json"):
            path = arg if os.path.isabs(arg) else os.path.join(REPO_ROOT, arg)
            if os.path.exists(path):
                return path

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    today_file = os.path.join(REPO_ROOT, f"wire_approved_{today}.json")
    if os.path.exists(today_file):
        return today_file

    files = sorted(glob.glob(os.path.join(REPO_ROOT, "wire_approved_*.json")))
    if files:
        print(f"  No today's file. Using most recent: {os.path.basename(files[-1])}")
        return files[-1]
    return None


# ── Bluesky auth ───────────────────────────────────────────────────────────────

def create_session(pds_url, handle, app_password):
    r = requests.post(
        f"{pds_url}/xrpc/com.atproto.server.createSession",
        json={"identifier": handle, "password": app_password},
        timeout=15,
    )
    if r.status_code != 200:
        raise RuntimeError(f"Auth failed ({r.status_code}): {r.text[:200]}")
    data = r.json()
    return data["accessJwt"], data["did"]


# ── Build post record with link facet ─────────────────────────────────────────

def build_post_record(text, link_url=None):
    """
    Build an app.bsky.feed.post record.
    If link_url provided and present in text, adds a facet for the link.
    Bluesky requires UTF-8 byte offsets for facets — not character offsets.
    """
    record = {
        "$type": "app.bsky.feed.post",
        "text": text,
        "createdAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }

    if link_url and link_url in text:
        text_bytes = text.encode("utf-8")
        url_bytes  = link_url.encode("utf-8")
        start = text_bytes.find(url_bytes)
        if start >= 0:
            end = start + len(url_bytes)
            record["facets"] = [{
                "index": {"byteStart": start, "byteEnd": end},
                "features": [{"$type": "app.bsky.richtext.facet#link", "uri": link_url}],
            }]

    return record


def post_to_bluesky(jwt, did, pds_url, record):
    """Post a record. Returns (uri, cid) on success."""
    r = requests.post(
        f"{pds_url}/xrpc/com.atproto.repo.createRecord",
        headers={"Authorization": f"Bearer {jwt}"},
        json={
            "repo": did,
            "collection": "app.bsky.feed.post",
            "record": record,
        },
        timeout=15,
    )
    if r.status_code != 200:
        raise RuntimeError(f"Post failed ({r.status_code}): {r.text[:300]}")
    data = r.json()
    return data["uri"], data["cid"]


def uri_to_url(uri, handle):
    """Convert at://did:.../app.bsky.feed.post/rkey → https://bsky.app/... URL."""
    rkey = uri.split("/")[-1]
    return f"https://bsky.app/profile/{handle}/post/{rkey}"


# ── wire.json management ──────────────────────────────────────────────────────

def load_wire_json():
    if os.path.exists(WIRE_JSON_FILE):
        with open(WIRE_JSON_FILE) as f:
            data = json.load(f)
        return data.get("items", [])
    return []


def save_wire_json(items):
    items = items[:WIRE_JSON_CAP]  # newest first, trim oldest
    with open(WIRE_JSON_FILE, "w") as f:
        json.dump({"items": items}, f, indent=2)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    load_dotenv()
    dry_run = "--dry-run" in sys.argv

    handle      = os.environ.get("BSKY_HANDLE")
    app_password= os.environ.get("BSKY_APP_PASSWORD")
    pds_url     = os.environ.get("BSKY_PDS_URL", "https://bsky.social").rstrip("/")

    if not dry_run:
        if not handle or not app_password:
            print("ERROR: BSKY_HANDLE and BSKY_APP_PASSWORD must be set in .env or environment.")
            sys.exit(1)

    approved_file = find_approved_file(sys.argv)
    if not approved_file:
        print("ERROR: No wire_approved_*.json found. Export from atlas_wire_review.html first.")
        sys.exit(1)

    print(f"Atlas Wire — Post {'[DRY RUN] ' if dry_run else ''}")
    print(f"  Handle:  {handle or '(not set)'}")
    print(f"  PDS:     {pds_url}")
    print(f"  Input:   {os.path.basename(approved_file)}")

    with open(approved_file) as f:
        approved = json.load(f)

    if not approved:
        print("No approved items. Exiting.")
        sys.exit(0)

    print(f"  Items:   {len(approved)}")

    # Authenticate
    jwt = did = None
    if not dry_run:
        print("\nAuthenticating with Bluesky...")
        try:
            jwt, did = create_session(pds_url, handle, app_password)
            print(f"  ✓ Authenticated as {handle} (DID: {did[:20]}...)")
        except RuntimeError as e:
            print(f"  ERROR: {e}")
            sys.exit(1)

    # Group items by cluster so we can post cluster threads together
    cluster_groups = {}   # cluster_id → list of items
    solo_items = []

    for item in approved:
        cid = item.get("cluster", {}).get("cluster_id") if item.get("cluster") else None
        if cid:
            cluster_groups.setdefault(cid, []).append(item)
        else:
            solo_items.append(item)

    # Build ordered post queue: (item, reply_to_uri, reply_to_cid, is_thread_opener, thread_opener_text)
    post_queue = []

    # Solo items first
    for item in solo_items:
        post_queue.append((item, None, None, False, None))

    # Cluster groups: opener post → reply thread
    for cid, cluster_items in cluster_groups.items():
        opener_text = cluster_items[0].get("cluster_thread_opener")
        if opener_text:
            post_queue.append((cluster_items[0], None, None, True, opener_text))
            for item in cluster_items:
                post_queue.append((item, "__CLUSTER_OPENER__", cid, False, None))
        else:
            for item in cluster_items:
                post_queue.append((item, None, None, False, None))

    print(f"\nPosting {len(approved)} item(s) ({len(cluster_groups)} cluster(s), {len(solo_items)} solo)...\n")

    wire_entries = []
    cluster_opener_refs = {}  # cid → (uri, cid_bsky)
    posted_count = 0
    error_count = 0

    for i, (item, reply_to_uri, reply_cluster_id, is_opener, opener_text) in enumerate(post_queue):
        # Determine text to post
        if is_opener:
            post_text = opener_text
            post_link = None
        else:
            post_text = item.get("wire_frame", "")
            post_link = item.get("link", "")

        if not post_text:
            print(f"  SKIP #{i+1}: {item['creator_name']} — no wire_frame text")
            continue

        # Resolve reply parent
        reply_ref = None
        if reply_to_uri == "__CLUSTER_OPENER__":
            opener_info = cluster_opener_refs.get(reply_cluster_id)
            if opener_info:
                reply_ref = {"root": opener_info, "parent": opener_info}

        record = build_post_record(post_text, post_link)
        if reply_ref:
            record["reply"] = reply_ref

        label = f"[OPENER] {item.get('cluster', {}).get('cluster_label', '')}" if is_opener else \
                f"{item['creator_name']} ({item['beat']})"

        if dry_run:
            print(f"  DRY #{i+1}: {label}")
            print(f"    {post_text[:120].replace(chr(10), ' ')}")
            if reply_ref:
                print(f"    (reply to cluster opener)")
            print()
            post_uri = f"at://dry-run/app.bsky.feed.post/{i:04d}"
            post_cid = f"dry-run-cid-{i:04d}"
        else:
            try:
                post_uri, post_cid = post_to_bluesky(jwt, did, pds_url, record)
                print(f"  ✓ #{i+1}: {label}")
                posted_count += 1
            except RuntimeError as e:
                print(f"  ✗ #{i+1}: {label} — {e}")
                error_count += 1
                time.sleep(POST_DELAY)
                continue

        # Store opener ref for threading
        if is_opener:
            cluster_opener_refs[reply_cluster_id] = {"uri": post_uri, "cid": post_cid}
            time.sleep(POST_DELAY)
            continue

        # Build wire.json entry
        post_url = uri_to_url(post_uri, handle or "journalismatlas.com")
        cluster = item.get("cluster")
        wire_entries.append({
            "date": item.get("pub_date", "")[:10],
            "creator_name": item.get("creator_name", ""),
            "creator_url": item.get("creator_url", ""),
            "beat": item.get("beat", ""),
            "bluesky_handle": item.get("bluesky_handle"),
            "wire_text": post_text,
            "source_link": item.get("link", ""),
            "bsky_post_uri": post_uri,
            "bsky_post_url": post_url,
            "cluster_id": cluster.get("cluster_id") if cluster else None,
            "cluster_label": cluster.get("cluster_label") if cluster else None,
            "published_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        })

        if not dry_run and i < len(post_queue) - 1:
            time.sleep(POST_DELAY)

    # Append to wire.json (newest first)
    existing = load_wire_json()
    combined = wire_entries + existing   # prepend today's
    save_wire_json(combined)

    print(f"\n{'[DRY RUN] ' if dry_run else ''}Summary:")
    print(f"  Posted:   {posted_count if not dry_run else len(wire_entries)}")
    if not dry_run and error_count:
        print(f"  Errors:   {error_count}")
    print(f"  wire.json: {len(combined)} total items ({len(wire_entries)} new)")
    print(f"\n✓ wire.json updated. Deploy to Cloudflare when ready.")
    if not dry_run:
        print(f"  View on Bluesky: https://bsky.app/profile/{handle}")


if __name__ == "__main__":
    main()
