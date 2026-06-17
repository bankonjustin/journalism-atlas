"""
atlas_wire_rank.py
Session 1 of Atlas Wire pipeline.

Takes wire_queue_raw_YYYY-MM-DD.json, calls Claude API to:
  1. Detect thematic clusters across all items (one batch call)
  2. Score each item and draft wire post copy (batched ~20 at a time)

Writes: wire_queue_scored_YYYY-MM-DD.json

Usage:
  python3 atlas_wire_rank.py                    # uses today's raw queue
  python3 atlas_wire_rank.py wire_queue_raw_X.json
  python3 atlas_wire_rank.py --dev              # uses all pulse items regardless of date

Requires:
  ANTHROPIC_API_KEY in environment (or .env file)
"""

import json
import os
import sys
import time
import glob
from datetime import datetime, timezone

import anthropic

# ── Config ────────────────────────────────────────────────────────────────────

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
MODEL = "claude-sonnet-4-6"
BATCH_SIZE = 20
BATCH_DELAY = 1.0  # seconds between scoring batches

WIRE_FRAME_FORMAT = """📰 {creator_name} on {beat}: {one_sentence}
→ {link}
#AtlasWire #IndependentJournalism"""

CLUSTER_THREAD_FORMAT = """📡 {n} independent journalists are covering {topic} today — a thread.
{cluster_summary}
#AtlasWire"""


# ── Load .env if present ──────────────────────────────────────────────────────

def load_dotenv():
    env_path = os.path.join(REPO_ROOT, ".env")
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip())


# ── Find input file ───────────────────────────────────────────────────────────

def find_input_file(argv):
    """Return path to raw queue JSON. Accepts explicit path or finds today's."""
    # Check for explicit file arg
    for arg in argv[1:]:
        if arg.endswith(".json") and os.path.exists(arg):
            return arg
        if arg.endswith(".json"):
            full = os.path.join(REPO_ROOT, arg)
            if os.path.exists(full):
                return full

    # Today's file
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    today_file = os.path.join(REPO_ROOT, f"wire_queue_raw_{today}.json")
    if os.path.exists(today_file):
        return today_file

    # Latest available
    files = sorted(glob.glob(os.path.join(REPO_ROOT, "wire_queue_raw_*.json")))
    if files:
        print(f"  No today's file found. Using most recent: {os.path.basename(files[-1])}")
        return files[-1]

    return None


# ── Dev mode: load from Pulse directly ───────────────────────────────────────

def load_dev_items():
    """Load a sample of Pulse items for testing when no real 24h queue exists."""
    pulse_file = os.path.join(REPO_ROOT, "atlas-pulse", "pulse_output.json")
    bsky_file = os.path.join(REPO_ROOT, "assets", "data", "bluesky-creators.json")

    with open(pulse_file) as f:
        data = json.load(f)
    with open(bsky_file) as f:
        bsky_creators = json.load(f)

    bsky_lookup = {}
    for c in bsky_creators:
        handle = c.get("bsky_handle") or c.get("bluesky_handle")
        if handle:
            bsky_lookup[c.get("name", "").lower().strip()] = handle

    import uuid
    items = []
    for creator in data.get("creators", [])[:60]:  # first 60 creators = ~sample
        name = creator.get("name", "")
        handle = bsky_lookup.get(name.lower().strip())
        for post in creator.get("posts", [])[:1]:  # 1 post per creator
            items.append({
                "id": str(uuid.uuid4()),
                "source": "rss",
                "creator_name": name,
                "creator_url": creator.get("rss_url", ""),
                "bluesky_handle": handle,
                "beat": creator.get("topic", ""),
                "title": post.get("title", ""),
                "link": post.get("url", ""),
                "text_snippet": (post.get("summary", "") or post.get("title", ""))[:280],
                "pub_date": post.get("published", ""),
                "score": None,
                "wire_frame": None,
                "cluster": None,
                "status": "pending",
            })
    print(f"  Dev mode: loaded {len(items)} sample items from Pulse")
    return items


# ── Pass 1: Cluster detection ─────────────────────────────────────────────────

CLUSTER_SCHEMA = {
    "name": "clusters",
    "description": "Thematic clusters found in the item set",
    "input_schema": {
        "type": "object",
        "properties": {
            "clusters": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "cluster_id": {"type": "string"},
                        "cluster_label": {"type": "string", "description": "5 words max"},
                        "cluster_summary": {"type": "string", "description": "One sentence"},
                        "item_ids": {"type": "array", "items": {"type": "string"}},
                    },
                    "required": ["cluster_id", "cluster_label", "cluster_summary", "item_ids"],
                },
            }
        },
        "required": ["clusters"],
    },
}


def detect_clusters(client, items):
    if not items:
        return {}

    item_list = "\n".join(
        f'- ID:{item["id"]} | {item["creator_name"]} | {item["beat"]} | {item["title"] or item["text_snippet"][:120]}'
        for item in items
    )

    prompt = f"""You are an editorial assistant for Atlas Wire, a curated wire service tracking independent journalism.

Here are {len(items)} items published recently by independent journalists in the Atlas database.

Identify thematic clusters — groups of 3 or more items covering the same story, topic, or developing situation. Return only clusters with 3+ items. Items not in any cluster should be omitted.

Items:
{item_list}"""

    response = client.messages.create(
        model=MODEL,
        max_tokens=2000,
        tools=[CLUSTER_SCHEMA],
        tool_choice={"type": "tool", "name": "clusters"},
        messages=[{"role": "user", "content": prompt}],
    )

    for block in response.content:
        if block.type == "tool_use" and block.name == "clusters":
            clusters_data = block.input.get("clusters", [])
            # Build id → cluster_id mapping
            id_to_cluster = {}
            for cl in clusters_data:
                for item_id in cl["item_ids"]:
                    id_to_cluster[item_id] = {
                        "cluster_id": cl["cluster_id"],
                        "cluster_label": cl["cluster_label"],
                        "cluster_summary": cl["cluster_summary"],
                    }
            return id_to_cluster, clusters_data

    return {}, []


# ── Pass 2: Scoring + wire frame drafting ──────────────────────────────────────

SCORE_SCHEMA = {
    "name": "scored_items",
    "description": "Scored and framed wire items",
    "input_schema": {
        "type": "object",
        "properties": {
            "items": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string"},
                        "score": {"type": "number", "description": "1-10 overall editorial score"},
                        "score_newsworthiness": {"type": "number"},
                        "score_distinctiveness": {"type": "number"},
                        "score_atlas_fit": {"type": "number"},
                        "score_timeliness": {"type": "number"},
                        "wire_frame": {"type": "string", "description": "Ready-to-post wire text"},
                    },
                    "required": ["id", "score", "wire_frame"],
                },
            }
        },
        "required": ["items"],
    },
}


def score_batch(client, batch, cluster_map):
    item_list = "\n\n".join(
        f"""Item ID: {item['id']}
Creator: {item['creator_name']} | Beat: {item['beat']}
Title: {item['title']}
Snippet: {item['text_snippet'][:200]}
Link: {item['link']}"""
        for item in batch
    )

    prompt = f"""You are an editorial assistant for Atlas Wire, a curated wire service for independent journalism.

Score each item and draft wire post copy.

SCORING (1-10 each dimension, average for overall score):
- Newsworthiness: Is this timely, consequential, or surprising?
- Distinctiveness: Is this angle covered elsewhere, or is this independent journalism adding something unique?
- Atlas fit: Does this exemplify independent journalism doing meaningful work?
- Timeliness: Is this breaking/fresh, or retrospective?

WIRE FRAME FORMAT (write exactly this, no deviations):
📰 [Creator Name] on [beat]: [one declarative sentence about what the piece covers, max 220 chars, no quotes, no hype, no "explores" or "examines"]
→ [link]
#AtlasWire #IndependentJournalism

Rules for wire frame:
- The sentence should tell you what the journalism found or covers, not describe the piece
- Use the creator's actual name, not their publication
- Keep the beat label short (1-3 words max)
- The link goes on its own line after →

Items to score and frame:
{item_list}"""

    response = client.messages.create(
        model=MODEL,
        max_tokens=4000,
        tools=[SCORE_SCHEMA],
        tool_choice={"type": "tool", "name": "scored_items"},
        messages=[{"role": "user", "content": prompt}],
    )

    for block in response.content:
        if block.type == "tool_use" and block.name == "scored_items":
            return block.input.get("items", [])

    return []


# ── Pass 3: Draft cluster thread openers ──────────────────────────────────────

def draft_cluster_threads(client, clusters_data, items_by_id):
    """For each cluster, draft a thread opener post."""
    if not clusters_data:
        return {}

    cluster_threads = {}
    for cl in clusters_data:
        n = len(cl["item_ids"])
        topic = cl["cluster_label"]
        summary = cl["cluster_summary"]
        thread_text = CLUSTER_THREAD_FORMAT.format(
            n=n,
            topic=topic,
            cluster_summary=summary,
        )
        cluster_threads[cl["cluster_id"]] = thread_text

    return cluster_threads


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    load_dotenv()

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY not set. Add to .env or export in shell.")
        sys.exit(1)

    dev_mode = "--dev" in sys.argv

    # Load items
    if dev_mode:
        print("Atlas Wire — Rank [DEV MODE]")
        items = load_dev_items()
        date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    else:
        print("Atlas Wire — Rank")
        input_file = find_input_file(sys.argv)
        if not input_file:
            print("ERROR: No wire_queue_raw_*.json found. Run atlas_wire_fetch.py first.")
            sys.exit(1)
        print(f"  Input: {os.path.basename(input_file)}")
        with open(input_file) as f:
            items = json.load(f)
        date_str = os.path.basename(input_file).replace("wire_queue_raw_", "").replace(".json", "")

    if not items:
        print("No items to rank. Exiting.")
        sys.exit(0)

    print(f"  Items to rank: {len(items)}")
    out_file = os.path.join(REPO_ROOT, f"wire_queue_scored_{date_str}.json")

    client = anthropic.Anthropic(api_key=api_key)

    # Pass 1: Cluster detection
    print(f"\n[1/3] Detecting clusters across {len(items)} items...")
    cluster_map, clusters_data = detect_clusters(client, items)
    print(f"  Found {len(clusters_data)} clusters covering {len(cluster_map)} items")
    for cl in clusters_data:
        print(f"  · {cl['cluster_label']} ({len(cl['item_ids'])} items)")

    # Pass 2: Score + frame (batched)
    print(f"\n[2/3] Scoring and framing items (batches of {BATCH_SIZE})...")
    batches = [items[i:i+BATCH_SIZE] for i in range(0, len(items), BATCH_SIZE)]
    scored_map = {}

    for i, batch in enumerate(batches):
        print(f"  Batch {i+1}/{len(batches)} ({len(batch)} items)...")
        results = score_batch(client, batch, cluster_map)
        for r in results:
            scored_map[r["id"]] = r
        if i < len(batches) - 1:
            time.sleep(BATCH_DELAY)

    print(f"  Scored {len(scored_map)}/{len(items)} items")

    # Pass 3: Cluster thread drafts
    print(f"\n[3/3] Drafting cluster thread openers...")
    items_by_id = {item["id"]: item for item in items}
    cluster_threads = draft_cluster_threads(client, clusters_data, items_by_id)

    # Merge results back into items
    for item in items:
        scored = scored_map.get(item["id"], {})
        item["score"] = scored.get("score")
        item["score_newsworthiness"] = scored.get("score_newsworthiness")
        item["score_distinctiveness"] = scored.get("score_distinctiveness")
        item["score_atlas_fit"] = scored.get("score_atlas_fit")
        item["score_timeliness"] = scored.get("score_timeliness")
        item["wire_frame"] = scored.get("wire_frame")

        cluster_info = cluster_map.get(item["id"])
        if cluster_info:
            item["cluster"] = cluster_info
            cid = cluster_info["cluster_id"]
            item["cluster_thread_opener"] = cluster_threads.get(cid)
        else:
            item["cluster"] = None
            item["cluster_thread_opener"] = None

    # Sort by score descending
    items.sort(key=lambda x: (x.get("score") or 0), reverse=True)

    # Summary stats
    scored_items = [x for x in items if x.get("score") is not None]
    high_score = [x for x in scored_items if x["score"] >= 7]
    print(f"\n  Scored: {len(scored_items)}/{len(items)}")
    print(f"  Score ≥7 (wire candidates): {len(high_score)}")
    if scored_items:
        avg = sum(x["score"] for x in scored_items) / len(scored_items)
        print(f"  Average score: {avg:.1f}")

    print("\n  Top 5 items:")
    for item in items[:5]:
        print(f"  [{item.get('score', '?'):.1f}] {item['creator_name']} — {item['title'][:60]}")

    with open(out_file, "w") as f:
        json.dump(items, f, indent=2)

    print(f"\n✓ Written: {out_file}")
    print(f"  Open atlas_wire_review.html to approve/kill/edit items.")


if __name__ == "__main__":
    main()
