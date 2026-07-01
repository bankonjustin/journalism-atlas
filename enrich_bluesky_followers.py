"""
Bluesky follower-count enrichment script.
Reads bluesky-creators.json, fetches live profile data for every handle,
writes bluesky-creators-enriched.json and bluesky_followers_fetch_log.csv.

Does NOT overwrite the source file. Review both outputs before swapping in.

Rate limit note: Bluesky's public API (public.api.bsky.app) is undocumented
on exact limits but community experience suggests ~3 req/s is safe. We use
200ms delay (5 req/s) with exponential backoff on 429 to stay conservative.

Phase 4 CORS note: This script runs server-side, bypassing CORS entirely.
To check browser CORS allowance, inspect response headers below —
Access-Control-Allow-Origin will tell you if the endpoint permits browser fetches.
"""

import json
import csv
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone

INPUT_FILE  = 'assets/data/bluesky-creators.json'
OUTPUT_JSON = 'bluesky-creators-enriched.json'
OUTPUT_CSV  = 'bluesky_followers_fetch_log.csv'

BASE_URL    = 'https://public.api.bsky.app/xrpc/app.bsky.actor.getProfile?actor={handle}'
DELAY_S     = 0.2   # 200ms between requests
MAX_RETRIES = 3

def fetch_profile(handle):
    """
    Returns (data_dict, cors_header) on success, raises on failure.
    cors_header is the Access-Control-Allow-Origin value from the response,
    useful for validating Phase 4 browser-side fetch feasibility.
    """
    url = BASE_URL.format(handle=handle)
    req = urllib.request.Request(url, headers={'User-Agent': 'JournalismAtlas/1.0'})

    delay = 1.0
    for attempt in range(MAX_RETRIES):
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                cors = resp.headers.get('Access-Control-Allow-Origin', 'not-set')
                data = json.loads(resp.read().decode())
                return data, cors
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(delay)
                delay *= 2
                continue
            raise
        except Exception:
            raise
    raise RuntimeError(f'Max retries exceeded for {handle}')


def main():
    with open(INPUT_FILE, encoding='utf-8') as f:
        creators = json.load(f)

    print(f'Loaded {len(creators)} creators from {INPUT_FILE}')

    enriched = []
    log_rows  = []
    cors_sample = None  # capture one header value for Phase 4 note

    total     = len(creators)
    ok_count  = 0
    fail_count = 0

    for i, creator in enumerate(creators):
        handle = (creator.get('bsky_handle') or '').strip()
        name   = creator.get('name', '?')

        if not handle:
            record = dict(creator)
            enriched.append(record)
            log_rows.append({
                'handle': '',
                'name': name,
                'status': 'skipped',
                'followers_count': '',
                'posts_count': '',
                'indexed_at': '',
                'error_reason': 'no handle',
                'fetched_at': '',
            })
            fail_count += 1
            print(f'  [{i+1}/{total}] SKIP  {name} — no handle')
            continue

        try:
            data, cors = fetch_profile(handle)
            if cors_sample is None:
                cors_sample = cors

            followers = data.get('followersCount', 0)
            posts     = data.get('postsCount', 0)
            indexed   = data.get('indexedAt', '')
            fetched   = datetime.now(timezone.utc).isoformat()

            record = dict(creator)
            record['bsky_followers'] = followers
            record['bsky_posts_count'] = posts
            record['bsky_indexed_at']  = indexed
            enriched.append(record)

            log_rows.append({
                'handle': handle,
                'name': name,
                'status': 'ok',
                'followers_count': followers,
                'posts_count': posts,
                'indexed_at': indexed,
                'error_reason': '',
                'fetched_at': fetched,
            })
            ok_count += 1
            print(f'  [{i+1}/{total}] OK    {name} (@{handle}) — {followers:,} followers')

        except urllib.error.HTTPError as e:
            reason = f'HTTP {e.code}: {e.reason}'
            record = dict(creator)
            enriched.append(record)
            log_rows.append({
                'handle': handle,
                'name': name,
                'status': 'failed',
                'followers_count': '',
                'posts_count': '',
                'indexed_at': '',
                'error_reason': reason,
                'fetched_at': datetime.now(timezone.utc).isoformat(),
            })
            fail_count += 1
            print(f'  [{i+1}/{total}] FAIL  {name} (@{handle}) — {reason}')

        except Exception as e:
            reason = str(e)
            record = dict(creator)
            enriched.append(record)
            log_rows.append({
                'handle': handle,
                'name': name,
                'status': 'failed',
                'followers_count': '',
                'posts_count': '',
                'indexed_at': '',
                'error_reason': reason,
                'fetched_at': datetime.now(timezone.utc).isoformat(),
            })
            fail_count += 1
            print(f'  [{i+1}/{total}] FAIL  {name} (@{handle}) — {reason}')

        time.sleep(DELAY_S)

    # Write enriched JSON
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(enriched, f, indent=2, ensure_ascii=False)

    # Write fetch log CSV
    fieldnames = ['handle', 'name', 'status', 'followers_count', 'posts_count',
                  'indexed_at', 'error_reason', 'fetched_at']
    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(log_rows)

    print()
    print('─' * 60)
    print(f'Done. {ok_count} succeeded, {fail_count} failed/skipped.')
    print(f'Enriched JSON → {OUTPUT_JSON}')
    print(f'Fetch log     → {OUTPUT_CSV}')
    print()
    print(f'Phase 4 CORS note: Access-Control-Allow-Origin = {cors_sample!r}')
    print('If that value is "*", the endpoint allows browser fetches without auth.')
    print()
    print('Next step: review the log for failures, spot-check enriched JSON,')
    print('then swap bluesky-creators-enriched.json → assets/data/bluesky-creators.json')
    print('and push via GitHub Desktop.')


if __name__ == '__main__':
    main()
