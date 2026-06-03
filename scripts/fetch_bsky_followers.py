#!/usr/bin/env python3
"""
Fetch live Bluesky follower counts for all creators in the inline CREATORS array.
Reads bluesky-intelligence.html, hits the public Bluesky API, writes enriched JSON.
No auth required.
"""
import json, re, time, sys
import urllib.request, urllib.error

# --- Extract CREATORS from HTML ---
with open('/Users/justinbank/Documents/GitHub/journalism-atlas/bluesky-intelligence.html') as f:
    content = f.read()

m = re.search(r'const CREATORS = (\[.*?\]);', content, re.DOTALL)
if not m:
    sys.exit("Could not find CREATORS array in bluesky-intelligence.html")

creators = json.loads(m.group(1))
print(f"Loaded {len(creators)} creators")

# --- Fetch follower counts ---
BASE = "https://public.api.bsky.app/xrpc/app.bsky.actor.getProfile?actor="
results = []
errors = []

for i, c in enumerate(creators):
    handle = c.get('bsky_handle', '').strip()
    if not handle:
        results.append({**c, 'bsky_followers': 0})
        continue

    url = BASE + handle
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'AtlasBot/1.0'})
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read())
            followers = data.get('followersCount', 0)
            results.append({**c, 'bsky_followers': followers})
            if followers > 0:
                print(f"  [{i+1}/{len(creators)}] {c['name']}: {followers:,}")
            else:
                print(f"  [{i+1}/{len(creators)}] {c['name']}: 0")
    except Exception as e:
        print(f"  [{i+1}/{len(creators)}] ERROR {c['name']} ({handle}): {e}")
        errors.append(c['name'])
        results.append({**c})  # keep existing value

    time.sleep(0.15)  # be polite

# --- Write output ---
out_path = '/Users/justinbank/Documents/GitHub/journalism-atlas/assets/data/bluesky-creators.json'
with open(out_path, 'w') as f:
    json.dump(results, f, indent=2)

print(f"\nDone. {len(results)} records written to {out_path}")
print(f"Errors: {len(errors)}")
if errors:
    print("Failed handles:", errors)

# Summary
with_followers = [r for r in results if r.get('bsky_followers', 0) > 0]
print(f"Records with followers > 0: {len(with_followers)}")
top10 = sorted(results, key=lambda x: x.get('bsky_followers') or 0, reverse=True)[:10]
print("\nTop 10 by followers:")
for r in top10:
    print(f"  {r['name']}: {r.get('bsky_followers', 0):,}")
