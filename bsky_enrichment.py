"""
Bluesky Handle Enrichment — Atlas Creator Pipeline
Searches Bluesky for candidate handles for the ~907 unevaluated creators.
Outputs a CSV for human review. Does NOT write to any master data file.

Scoring logic:
  +4  Display name exact match (case-insensitive)
  +3  Display name contains creator name
  +2  Handle contains creator name (simplified: lowercase, no spaces)
  +1  Bio mentions journalism keywords (journalist/reporter/writer/newsletter)
  +1  Bio mentions creator's topic/beat
  +1  Follower count > 1,000
  +1  Follower count > 10,000 (stacks with above)

Confidence: HIGH >= 6, MEDIUM 4-5, LOW 3, NO_MATCH < 3
"""

import csv
import json
import os
import re
import time
import urllib.request
import urllib.parse
import urllib.error
from datetime import date

# ── Paths ──────────────────────────────────────────────────────────────────────
REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
MASTER_CSV = os.path.join(REPO_ROOT, "assets/data/creators-master.csv")
BSKY_JSON  = os.path.join(REPO_ROOT, "assets/data/bluesky-creators.json")
OUTPUT_DIR = os.path.join(REPO_ROOT, "outputs")
OUTPUT_CSV = os.path.join(OUTPUT_DIR, f"bsky_enrichment_candidates_{date.today()}.csv")

# ── Constants ──────────────────────────────────────────────────────────────────
API_BASE   = "https://public.api.bsky.app/xrpc/app.bsky.actor.searchActors"
SLEEP_SEC  = 0.3
MIN_SCORE  = 3

JOURNALISM_KEYWORDS = {"journalist", "reporter", "writer", "newsletter", "editor",
                       "correspondent", "columnist", "newsroom", "journalism"}

TIER1_PLATFORMS = {"newsletter"}  # partial match
TIER1_TOPICS    = {"politics", "tech", "climate/environment", "science",
                   "finance/economics", "general news", "health/wellness", "local"}

TIER2_PLATFORMS = {"website", "podcast"}
TIER2_TOPICS    = {"culture", "travel", "faith/religion"}

# Generic single-word short channel names — use creator name only for these
GENERIC_WORDS = {
    "newsletter", "podcast", "show", "daily", "weekly", "morning", "evening",
    "report", "news", "update", "brief", "digest", "review", "dispatch",
    "signal", "watch", "wire", "post", "times", "press", "journal",
}


def get_tier(platform_primary: str, topic: str) -> int:
    p = platform_primary.lower()
    t = topic.lower()
    if any(kw in p for kw in TIER1_PLATFORMS) or t in TIER1_TOPICS:
        return 1
    if any(kw in p for kw in TIER2_PLATFORMS) or t in TIER2_TOPICS:
        return 2
    return 3


def is_generic_channel(channel: str) -> bool:
    """True if the channel name is too generic to be a useful search term."""
    if not channel:
        return True
    words = channel.lower().split()
    if len(words) == 1 and (words[0] in GENERIC_WORDS or len(words[0]) <= 5):
        return True
    # Multi-word but all words are generic
    if all(w in GENERIC_WORDS for w in words):
        return True
    return False


def simplify(name: str) -> str:
    """Lowercase, remove punctuation and spaces — used for handle matching."""
    return re.sub(r"[^a-z0-9]", "", name.lower())


def search_bsky(query: str) -> list:
    """Call the public Bluesky search API. Returns list of actor dicts."""
    params = urllib.parse.urlencode({"q": query, "limit": 5})
    url = f"{API_BASE}?{params}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "atlas-enrichment/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            return data.get("actors", [])
    except Exception as e:
        raise RuntimeError(f"API error for '{query}': {e}")


def score_candidate(actor: dict, creator_name: str, topic: str) -> int:
    display = actor.get("displayName", "") or ""
    handle  = actor.get("handle", "") or ""
    bio     = (actor.get("description", "") or "").lower()
    followers = (actor.get("followersCount") or
                 actor.get("viewer", {}).get("followersCount") or 0)
    # Some API responses nest follower count here:
    if not followers:
        followers = actor.get("followersCount", 0) or 0

    score = 0
    name_lower = creator_name.lower()

    # Display name match
    if display.lower() == name_lower:
        score += 4
    elif name_lower in display.lower():
        score += 3

    # Handle match
    if simplify(creator_name) in simplify(handle):
        score += 2

    # Bio — journalism keywords
    if any(kw in bio for kw in JOURNALISM_KEYWORDS):
        score += 1

    # Bio — topic match (use first word of topic as a rough keyword)
    topic_parts = topic.lower().split("/")[0].split()
    if topic_parts:
        topic_kw = topic_parts[0]
        if len(topic_kw) > 3 and topic_kw in bio:
            score += 1

    # Followers
    if followers > 1000:
        score += 1
    if followers > 10000:
        score += 1

    return score


def confidence_label(score: int) -> str:
    if score >= 6:
        return "HIGH"
    if score >= 4:
        return "MEDIUM"
    if score >= 3:
        return "LOW"
    return "NO_MATCH"


def get_followers(actor: dict) -> int:
    return (actor.get("followersCount") or 0)


def load_evaluated_slugs() -> set:
    with open(BSKY_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)
    return {entry["slug"] for entry in data}


def load_unevaluated_creators(evaluated_slugs: set) -> list:
    creators = []
    with open(MASTER_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["slug"] not in evaluated_slugs:
                creators.append(row)
    return creators


def assign_tiers(creators: list) -> list:
    """Add 'tier' key to each creator and sort: tier asc, then name asc."""
    for c in creators:
        c["tier"] = get_tier(c.get("Platform Primary", ""), c.get("Topic/Category", ""))
    return sorted(creators, key=lambda c: (c["tier"], c["Creator Name"].lower()))


def main():
    t_start = time.time()
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("Loading data files...")
    evaluated_slugs = load_evaluated_slugs()
    creators = load_unevaluated_creators(evaluated_slugs)
    creators = assign_tiers(creators)

    total = len(creators)
    tier_counts = {1: 0, 2: 0, 3: 0}
    for c in creators:
        tier_counts[c["tier"]] += 1
    print(f"Found {total} unevaluated creators  —  Tier 1: {tier_counts[1]}, Tier 2: {tier_counts[2]}, Tier 3: {tier_counts[3]}")
    print(f"Output → {OUTPUT_CSV}\n")

    output_rows = []
    api_errors  = 0

    for idx, creator in enumerate(creators, 1):
        name    = creator["Creator Name"]
        channel = creator.get("Creator Channel", "")
        slug    = creator["slug"]
        platform = creator.get("Platform Primary", "")
        topic   = creator.get("Topic/Category", "")
        tier    = creator["tier"]

        print(f"[{idx}/{total}] T{tier} {name}...", end=" ", flush=True)

        # Build search queries
        queries = []
        if channel and not is_generic_channel(channel) and channel.lower() != name.lower():
            queries.append(channel)
        queries.append(name)
        # Deduplicate while preserving order
        seen_q = set()
        deduped = []
        for q in queries:
            if q not in seen_q:
                seen_q.add(q)
                deduped.append(q)
        queries = deduped

        # Fetch results
        all_actors = {}
        error_flag = False
        for q in queries:
            try:
                actors = search_bsky(q)
                for a in actors:
                    h = a.get("handle", "")
                    if h and h not in all_actors:
                        all_actors[h] = a
                time.sleep(SLEEP_SEC)
            except RuntimeError as e:
                print(f"ERROR — {e}")
                api_errors += 1
                error_flag = True
                break

        if error_flag:
            output_rows.append({
                "slug": slug, "creator_name": name, "creator_channel": channel,
                "platform_primary": platform, "topic": topic, "tier": tier,
                "bsky_handle": "", "bsky_display_name": "", "bsky_followers": "",
                "bsky_description": "", "match_score": 0,
                "match_confidence": "API_ERROR",
                "bsky_profile_url": "", "reviewer_decision": "", "notes": "",
            })
            continue

        if not all_actors:
            print("no results")
            output_rows.append({
                "slug": slug, "creator_name": name, "creator_channel": channel,
                "platform_primary": platform, "topic": topic, "tier": tier,
                "bsky_handle": "", "bsky_display_name": "", "bsky_followers": "",
                "bsky_description": "", "match_score": 0,
                "match_confidence": "NO_MATCH",
                "bsky_profile_url": "", "reviewer_decision": "", "notes": "",
            })
            continue

        # Score all candidates
        scored = []
        for h, actor in all_actors.items():
            s = score_candidate(actor, name, topic)
            if s >= MIN_SCORE:
                scored.append((s, actor))

        if not scored:
            print("no match")
            output_rows.append({
                "slug": slug, "creator_name": name, "creator_channel": channel,
                "platform_primary": platform, "topic": topic, "tier": tier,
                "bsky_handle": "", "bsky_display_name": "", "bsky_followers": "",
                "bsky_description": "", "match_score": 0,
                "match_confidence": "NO_MATCH",
                "bsky_profile_url": "", "reviewer_decision": "", "notes": "",
            })
            continue

        # Sort descending by score
        scored.sort(key=lambda x: -x[0])
        top_score = scored[0][0]
        # Keep all candidates with top score (ties)
        top_candidates = [a for s, a in scored if s == top_score]

        for actor in top_candidates:
            h       = actor.get("handle", "")
            display = actor.get("displayName", "") or ""
            bio     = (actor.get("description", "") or "")[:120]
            followers = get_followers(actor)
            conf    = confidence_label(top_score)
            print(f"→ {h} ({conf}, score {top_score})")
            output_rows.append({
                "slug": slug, "creator_name": name, "creator_channel": channel,
                "platform_primary": platform, "topic": topic, "tier": tier,
                "bsky_handle": h, "bsky_display_name": display,
                "bsky_followers": followers,
                "bsky_description": bio,
                "match_score": top_score,
                "match_confidence": conf,
                "bsky_profile_url": f"https://bsky.app/profile/{h}",
                "reviewer_decision": "", "notes": "",
            })

    # ── Sort output: tier asc, confidence desc, creator_name asc ──────────────
    CONF_ORDER = {"HIGH": 0, "MEDIUM": 1, "LOW": 2, "NO_MATCH": 3, "API_ERROR": 4}
    output_rows.sort(key=lambda r: (
        int(r["tier"]),
        CONF_ORDER.get(r["match_confidence"], 5),
        r["creator_name"].lower()
    ))

    # ── Write CSV ──────────────────────────────────────────────────────────────
    fieldnames = [
        "slug", "creator_name", "creator_channel", "platform_primary", "topic",
        "tier", "bsky_handle", "bsky_display_name", "bsky_followers",
        "bsky_description", "match_score", "match_confidence", "bsky_profile_url",
        "reviewer_decision", "notes",
    ]
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_rows)

    elapsed = time.time() - t_start
    match_rows = [r for r in output_rows if r["match_confidence"] not in ("NO_MATCH", "API_ERROR")]
    high   = sum(1 for r in match_rows if r["match_confidence"] == "HIGH")
    medium = sum(1 for r in match_rows if r["match_confidence"] == "MEDIUM")
    low    = sum(1 for r in match_rows if r["match_confidence"] == "LOW")

    print(f"\n{'─'*60}")
    print(f"Done in {elapsed/60:.1f} min  |  {total} creators processed")
    print(f"Matches: {len(match_rows)} total — HIGH: {high}, MEDIUM: {medium}, LOW: {low}")
    print(f"No match: {sum(1 for r in output_rows if r['match_confidence'] == 'NO_MATCH')}")
    print(f"API errors: {api_errors}")
    print(f"Output: {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
