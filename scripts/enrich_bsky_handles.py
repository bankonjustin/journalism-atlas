#!/usr/bin/env python3
"""
Bluesky Handle Enrichment — Independent Journalism Atlas
=========================================================
Finds candidate Bluesky handles for Atlas creators not yet in the Bluesky corpus.

Inputs:
  assets/data/creators-master.csv      — full 1,578-creator master
  assets/data/bluesky-creators.json    — 671 already-evaluated creators

Output:
  outputs/bsky_enrichment_candidates_YYYY-MM-DD.csv

The script does NOT write to creators-master.csv, creators-data.json,
or bluesky-creators.json. It produces candidates only. Ryan confirms/rejects.

Usage:
  python3 scripts/enrich_bsky_handles.py
"""

import csv
import json
import os
import re
import time
import urllib.request
import urllib.error
from datetime import date
from collections import defaultdict

# ── PATHS ────────────────────────────────────────────────────────────────────
REPO_ROOT     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MASTER_CSV    = os.path.join(REPO_ROOT, 'assets', 'data', 'creators-master.csv')
BSKY_JSON     = os.path.join(REPO_ROOT, 'assets', 'data', 'bluesky-creators.json')
OUTPUTS_DIR   = os.path.join(REPO_ROOT, 'outputs')
OUTPUT_CSV    = os.path.join(OUTPUTS_DIR, f'bsky_enrichment_candidates_{date.today()}.csv')

BSKY_SEARCH   = 'https://public.api.bsky.app/xrpc/app.bsky.actor.searchActors'
RATE_LIMIT_S  = 0.3   # seconds between API calls
SEARCH_LIMIT  = 5     # results per query
MIN_SCORE     = 3     # minimum score to keep a candidate

# ── TIER DEFINITIONS ─────────────────────────────────────────────────────────
# Multi-value topic fields — check if ANY component matches.
# Platform fields — check if the platform_primary *starts with* the prefix.
# Tier is assigned to the HIGHEST priority (lowest number) matching rule.

TIER1_PLATFORMS = {'newsletter'}
TIER1_TOPICS    = {
    'politics', 'tech', 'climate/environment', 'science',
    'finance/economics', 'general news', 'health/wellness', 'local'
}

TIER2_PLATFORMS = {'website', 'podcast'}
TIER2_TOPICS    = {'culture', 'travel', 'faith/religion'}

# Tier 3 = everything else (video, social, low-signal topics)

def assign_tier(platform_primary: str, topic_field: str) -> int:
    """Return 1, 2, or 3 based on platform + topic signals. Highest priority wins."""
    platform_lower = platform_primary.lower()
    # split multi-value topic on comma, strip whitespace, lowercase
    topics = {t.strip().lower() for t in topic_field.split(',')} if topic_field else set()

    if platform_lower.startswith('newsletter'):
        return 1
    if topics & TIER1_TOPICS:
        return 1

    if platform_lower.startswith(('website', 'podcast')):
        return 2
    if topics & TIER2_TOPICS:
        return 2

    return 3


# ── SEARCH TERM LOGIC ────────────────────────────────────────────────────────
# Generic words that, alone or in short phrases, don't make useful search terms.
GENERIC_WORDS = {
    'the', 'a', 'an', 'daily', 'weekly', 'morning', 'evening', 'report',
    'news', 'newsletter', 'podcast', 'show', 'brief', 'digest', 'update',
    'today', 'post', 'press', 'review', 'dispatch', 'signal', 'note', 'notes',
    'letter', 'letters', 'talk', 'cast', 'wire', 'times', 'journal',
}

def is_generic_channel(channel: str, name: str) -> bool:
    """True if the channel name is too generic to be a useful search term."""
    if not channel:
        return True
    # Identical or very close to the creator's name
    if channel.strip().lower() == name.strip().lower():
        return True
    # Check word overlap with generic set
    words = {w.lower() for w in re.split(r'\W+', channel) if w}
    meaningful = words - GENERIC_WORDS
    return len(meaningful) < 2


def search_terms(name: str, channel: str) -> list[str]:
    """Return ordered list of search terms to try. Deduplicated."""
    terms = [name]
    if channel and not is_generic_channel(channel, name):
        terms.insert(0, channel)
    return list(dict.fromkeys(terms))  # preserve order, deduplicate


# ── SCORING LOGIC ────────────────────────────────────────────────────────────
# Scoring signals (see brief for full table):
#   Display name exact match (case-insensitive)          → 4
#   Display name contains creator name                   → 3
#   Handle contains simplified creator name              → 2
#   Description mentions journalism keywords             → 1
#   Description mentions creator's topic/beat            → 1
#   Follower count > 1,000                               → 1
#   Follower count > 10,000                              → 1 (stacks with above)

JOURNALISM_KEYWORDS = {
    'journalism', 'journalist', 'reporter', 'newsletter', 'writer',
    'editor', 'correspondent', 'columnist', 'podcast', 'author',
}

def simplify(s: str) -> str:
    """Lowercase, remove spaces/hyphens/dots for fuzzy matching."""
    return re.sub(r'[\s\-_.]', '', s.lower())

def score_candidate(actor: dict, creator_name: str, topic_field: str) -> int:
    """Score a Bluesky actor against a creator record. Returns integer score."""
    score = 0
    display  = (actor.get('displayName') or '').strip()
    handle   = (actor.get('handle') or '').lower()
    desc     = (actor.get('description') or '').lower()
    followers = int(actor.get('followersCount') or 0)

    name_lower   = creator_name.lower().strip()
    name_simple  = simplify(creator_name)

    # Display name signals
    if display.lower() == name_lower:
        score += 4
    elif name_lower in display.lower():
        score += 3

    # Handle signal
    if name_simple in simplify(handle):
        score += 2

    # Description — journalism keywords
    if any(kw in desc for kw in JOURNALISM_KEYWORDS):
        score += 1

    # Description — topic beat match
    topics = [t.strip().lower() for t in topic_field.split(',')] if topic_field else []
    topic_words = set()
    for t in topics:
        topic_words.update(re.split(r'[/\s]+', t))
    topic_words -= {'and', 'or', 'the', 'a'}
    if any(tw in desc for tw in topic_words if len(tw) > 3):
        score += 1

    # Follower signals
    if followers > 10000:
        score += 2  # stacks: > 1k (+1) and > 10k (+1)
    elif followers > 1000:
        score += 1

    return score


# ── API ───────────────────────────────────────────────────────────────────────
def search_bsky(query: str) -> list[dict]:
    """Call searchActors and return list of actor dicts. Empty list on error."""
    params = urllib.parse.urlencode({'q': query, 'limit': SEARCH_LIMIT})
    url = f'{BSKY_SEARCH}?{params}'
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'AtlasEnrichBot/1.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
            return data.get('actors', [])
    except Exception:
        return None  # None signals API error vs empty result

import urllib.parse


# ── MAIN ──────────────────────────────────────────────────────────────────────
def main():
    import time as _time
    start_time = _time.time()

    os.makedirs(OUTPUTS_DIR, exist_ok=True)

    # Load already-evaluated slugs
    with open(BSKY_JSON) as f:
        bsky_data = json.load(f)
    evaluated_slugs = {r['slug'] for r in bsky_data}
    print(f'Already evaluated: {len(evaluated_slugs)} creators')

    # Load master CSV, find unevaluated
    with open(MASTER_CSV, newline='', encoding='utf-8-sig') as f:
        master = list(csv.DictReader(f))
    unevaluated = [r for r in master if r['slug'] not in evaluated_slugs]
    print(f'Unevaluated (to search): {len(unevaluated)}')

    # Assign tiers and sort
    for r in unevaluated:
        r['_tier'] = assign_tier(r.get('Platform Primary', ''), r.get('Topic/Category', ''))
    unevaluated.sort(key=lambda r: (r['_tier'], r['Creator Name'].lower()))

    tier_counts = defaultdict(int)
    for r in unevaluated:
        tier_counts[r['_tier']] += 1
    for t in sorted(tier_counts):
        print(f'  Tier {t}: {tier_counts[t]} creators')

    # Output CSV
    COLUMNS = [
        'slug', 'creator_name', 'creator_channel', 'platform_primary', 'topic',
        'tier', 'bsky_handle', 'bsky_display_name', 'bsky_followers',
        'bsky_description', 'match_score', 'match_confidence', 'bsky_profile_url',
        'reviewer_decision', 'notes',
    ]

    rows_out = []
    api_errors = 0
    total = len(unevaluated)

    for idx, creator in enumerate(unevaluated, 1):
        name     = creator['Creator Name']
        channel  = creator.get('Creator Channel', '')
        slug     = creator['slug']
        platform = creator.get('Platform Primary', '')
        topic    = creator.get('Topic/Category', '')
        tier     = creator['_tier']

        print(f'[{idx}/{total}] T{tier} {name}...', end=' ', flush=True)

        terms = search_terms(name, channel)
        all_actors = {}  # handle → actor, deduplicated across queries
        api_failed = False

        for term in terms:
            actors = search_bsky(term)
            time.sleep(RATE_LIMIT_S)
            if actors is None:
                api_failed = True
                break
            for a in actors:
                h = a.get('handle', '')
                if h and h not in all_actors:
                    all_actors[h] = a

        if api_failed:
            api_errors += 1
            print('API_ERROR')
            rows_out.append({
                'slug': slug, 'creator_name': name, 'creator_channel': channel,
                'platform_primary': platform, 'topic': topic, 'tier': tier,
                'bsky_handle': '', 'bsky_display_name': '', 'bsky_followers': '',
                'bsky_description': '', 'match_score': '', 'match_confidence': 'API_ERROR',
                'bsky_profile_url': '', 'reviewer_decision': '', 'notes': '',
            })
            continue

        if not all_actors:
            print('no results')
            rows_out.append({
                'slug': slug, 'creator_name': name, 'creator_channel': channel,
                'platform_primary': platform, 'topic': topic, 'tier': tier,
                'bsky_handle': '', 'bsky_display_name': '', 'bsky_followers': '',
                'bsky_description': '', 'match_score': 0, 'match_confidence': 'NO_MATCH',
                'bsky_profile_url': '', 'reviewer_decision': '', 'notes': '',
            })
            continue

        # Score all candidates
        scored = []
        for actor in all_actors.values():
            s = score_candidate(actor, name, topic)
            if s >= MIN_SCORE:
                scored.append((s, actor))
        scored.sort(key=lambda x: x[0], reverse=True)

        if not scored:
            print('no match')
            rows_out.append({
                'slug': slug, 'creator_name': name, 'creator_channel': channel,
                'platform_primary': platform, 'topic': topic, 'tier': tier,
                'bsky_handle': '', 'bsky_display_name': '', 'bsky_followers': '',
                'bsky_description': '', 'match_score': 0, 'match_confidence': 'NO_MATCH',
                'bsky_profile_url': '', 'reviewer_decision': '', 'notes': '',
            })
            continue

        # Keep top scorer(s) — if tie at top, keep all tied rows
        top_score = scored[0][0]
        top_candidates = [(s, a) for s, a in scored if s == top_score]

        for s, actor in top_candidates:
            followers = int(actor.get('followersCount') or 0)
            handle    = actor.get('handle', '')
            desc_full = (actor.get('description') or '')
            confidence = 'HIGH' if s >= 6 else 'MEDIUM' if s >= 4 else 'LOW'
            print(f'{confidence} @{handle} ({s})')
            rows_out.append({
                'slug': slug,
                'creator_name': name,
                'creator_channel': channel,
                'platform_primary': platform,
                'topic': topic,
                'tier': tier,
                'bsky_handle': handle,
                'bsky_display_name': actor.get('displayName', ''),
                'bsky_followers': followers,
                'bsky_description': desc_full[:120],
                'match_score': s,
                'match_confidence': confidence,
                'bsky_profile_url': f'https://bsky.app/profile/{handle}',
                'reviewer_decision': '',
                'notes': '',
            })

    # Sort output: tier asc, confidence desc (HIGH→MEDIUM→LOW→NO_MATCH), name asc
    CONF_ORDER = {'HIGH': 0, 'MEDIUM': 1, 'LOW': 2, 'NO_MATCH': 3, 'API_ERROR': 4}
    rows_out.sort(key=lambda r: (
        int(r['tier']),
        CONF_ORDER.get(r['match_confidence'], 5),
        r['creator_name'].lower()
    ))

    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows_out)

    elapsed = _time.time() - start_time
    print(f'\n{"─"*60}')
    print(f'Done in {elapsed/60:.1f} min')
    print(f'Output: {OUTPUT_CSV}')
    print(f'Total rows: {len(rows_out)}')
    from collections import Counter
    conf_counts = Counter(r['match_confidence'] for r in rows_out)
    for k, v in sorted(conf_counts.items(), key=lambda x: CONF_ORDER.get(x[0], 5)):
        print(f'  {k}: {v}')
    print(f'API errors: {api_errors}')


if __name__ == '__main__':
    main()
