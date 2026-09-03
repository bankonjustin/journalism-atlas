#!/usr/bin/env python3
"""
atlas_groups.py — Normalize Topic/Category and derive Groups field
===================================================================
Reads creators-master.csv, applies two passes:
  1. Topic/Category normalization — maps legacy/variant topic strings to
     canonical values per SCHEMA-VOCAB.md (June 2026 consolidations)
  2. Groups derivation — maps canonical topics to the 9 Groups buckets
     via TAG_TO_GROUP, writes result to the Groups column

Usage:
    python3 pipeline/atlas_groups.py --dry-run          # preview, no writes
    python3 pipeline/atlas_groups.py                    # apply in-place
    python3 pipeline/atlas_groups.py --output out.csv   # write to new file

Run from the repo root. Snapshots the master before any write.
"""

import argparse
import csv
import sys
from collections import Counter
from pathlib import Path

REPO_ROOT   = Path(__file__).parent.parent
MASTER_CSV  = REPO_ROOT / "assets" / "data" / "creators-master.csv"
VERSIONS_DIR = REPO_ROOT / ".atlas_versions"


# ── Topic/Category normalization map ──────────────────────────────────────────
# Maps raw/legacy topic strings → canonical topic string.
# Order matters for the multi-value case: apply left-to-right per value.

TOPIC_NORMALIZE: dict[str, str] = {
    # Case fixes
    "Day in a life":           "Day in a Life",
    "Legal issues":            "Law/Legal Issues",
    "Media/power":             "Media/Power",
    "media/power":             "Media/Power",
    "Positive news":           "Positive News",
    "Urban planning":          "Urban Planning",
    "energy":                  "Energy",
    "history":                 "History",
    "world":                   "World",
    "Things to do":            "Things to Do",
    "Self Help":               "Self-Help",
    # Consolidations (June 2026)
    "Local News":              "Local",
    "Identity":                "Identity/Belonging",
    "Restaurants":             "Restaurants and bars",
    "Bars":                    "Restaurants and bars",
    "Transit/Transportation":  "Transportation",
    "Aviation":                "Transportation",
    "Technology":              "Tech",
    "Economy":                 "Finance/Economics",
    "Workforce":               "Labor/Workers Rights",
    "Motherhood":              "Parenting",
    "Family":                  "Parenting",
    "Running":                 "Fitness",
    "Sailing":                 "Outdoors",
    "Animals":                 "Science",
    "Coffee":                  "Restaurants and bars",
    "Vintage":                 "Culture",
    "Gossip":                  "Culture",
    "Language":                "Culture",
    "University":              "Education",
    "Socio-Economic":          "Finance/Economics",
    "Civic Issues":            "Local",
    "Politics/Policy":         "Politics",
}

# Topics to strip entirely (remove from the value, keep others)
TOPICS_REMOVE: set[str] = {"Divorce", "Utility", "Estate sales", "Gen-Z"}


# ── TAG_TO_GROUP mapping ───────────────────────────────────────────────────────
# Maps canonical topic → Groups bucket.
# A creator's Groups is the unique set of buckets for all their topics.
# Priority order (used when sorting multiple groups — site treemap renders first):
#   Power & Politics > Social Issues > Civic Life > Science Health & Environment
#   > Money & Work > General News > Culture & Media > Journalism Formats
#   > Lifestyle & Personal Life

TAG_TO_GROUP: dict[str, str] = {
    # Power & Politics
    "Politics":                      "Power & Politics",
    "Government Accountability":     "Power & Politics",
    "Law/Legal Issues":              "Power & Politics",
    "Foreign Policy":                "Power & Politics",
    "National Security":             "Power & Politics",
    "Military":                      "Power & Politics",
    "Policy":                        "Power & Politics",
    # Money & Work
    "Finance/Economics":             "Money & Work",
    "Tech":                          "Money & Work",
    "Business":                      "Money & Work",
    "Personal Finance":              "Money & Work",
    "Real Estate":                   "Money & Work",
    "Careers":                       "Money & Work",
    "Labor/Workers Rights":          "Money & Work",
    # Culture & Media
    "Culture":                       "Culture & Media",
    "Internet Culture":              "Culture & Media",
    "Media/Power":                   "Culture & Media",
    "Entertainment/Hollywood":       "Culture & Media",
    "Music":                         "Culture & Media",
    "Film/Movies":                   "Culture & Media",
    "Books/Writing":                 "Culture & Media",
    "Art":                           "Culture & Media",
    "History":                       "Culture & Media",
    "Comedy":                        "Culture & Media",
    "Design":                        "Culture & Media",
    "Photography":                   "Culture & Media",
    "Games/Gaming":                  "Culture & Media",
    "Architecture":                  "Culture & Media",
    "Museums":                       "Culture & Media",
    # Science Health & Environment
    "Climate/Environment":           "Science Health & Environment",
    "Health/Wellness":               "Science Health & Environment",
    "Science":                       "Science Health & Environment",
    "Energy":                        "Science Health & Environment",
    "Mental Health":                 "Science Health & Environment",
    "Cancer":                        "Science Health & Environment",
    "Weather":                       "Science Health & Environment",
    # Lifestyle & Personal Life
    "Food":                          "Lifestyle & Personal Life",
    "Travel":                        "Lifestyle & Personal Life",
    "Lifestyle":                     "Lifestyle & Personal Life",
    "Fashion":                       "Lifestyle & Personal Life",
    "Fitness":                       "Lifestyle & Personal Life",
    "Parenting":                     "Lifestyle & Personal Life",
    "Home":                          "Lifestyle & Personal Life",
    "Restaurants and bars":          "Lifestyle & Personal Life",
    "Recipes":                       "Lifestyle & Personal Life",
    "Sports":                        "Lifestyle & Personal Life",
    "Outdoors":                      "Lifestyle & Personal Life",
    "Dating/Romance":                "Lifestyle & Personal Life",
    "Things to Do":                  "Lifestyle & Personal Life",
    "Self-Help":                     "Lifestyle & Personal Life",
    # Civic Life
    "Local":                         "Civic Life",
    "Education":                     "Civic Life",
    "Housing":                       "Civic Life",
    "Urban Planning":                "Civic Life",
    "Transportation":                "Civic Life",
    "Crime":                         "Civic Life",
    "Construction":                  "Civic Life",
    "Agriculture":                   "Civic Life",
    # Social Issues
    "LGBTQIA":                       "Social Issues",
    "Identity/Belonging":            "Social Issues",
    "Gender":                        "Social Issues",
    "Immigration":                   "Social Issues",
    "Human Rights":                  "Social Issues",
    "Criminal Justice":              "Social Issues",
    "Faith/Religion":                "Social Issues",
    "Activism":                      "Social Issues",
    "Inequality":                    "Social Issues",
    # General News
    "General News":                  "General News",
    "World":                         "General News",
    "Positive News":                 "General News",
    # Journalism Formats
    "Explanatory":                   "Journalism Formats",
    "Investigative":                 "Journalism Formats",
    "Data Visualization":            "Journalism Formats",
    "Solutions Journalism":          "Journalism Formats",
    "Day in a Life":                 "Journalism Formats",
}

GROUP_PRIORITY = [
    "Power & Politics",
    "Social Issues",
    "Civic Life",
    "Science Health & Environment",
    "Money & Work",
    "General News",
    "Culture & Media",
    "Journalism Formats",
    "Lifestyle & Personal Life",
]


def normalize_topics(raw: str) -> tuple[str, list[str]]:
    """
    Normalize a raw Topic/Category string.
    Returns (normalized_string, list_of_warnings).
    """
    if not raw:
        return "", []

    warnings = []
    parts = [p.strip() for p in raw.split(",") if p.strip()]
    normalized = []

    for part in parts:
        if part in TOPICS_REMOVE:
            warnings.append(f"stripped '{part}'")
            continue
        mapped = TOPIC_NORMALIZE.get(part, part)
        if mapped != part:
            warnings.append(f"'{part}' → '{mapped}'")
        normalized.append(mapped)

    return ", ".join(normalized), warnings


def derive_groups(topic_str: str) -> str:
    """
    Derive comma-separated Groups value from normalized topic string.
    Returns groups in priority order.
    """
    if not topic_str:
        return ""

    topics = [t.strip() for t in topic_str.split(",") if t.strip()]
    groups_seen: set[str] = set()
    unmapped: list[str] = []

    for topic in topics:
        group = TAG_TO_GROUP.get(topic)
        if group:
            groups_seen.add(group)
        else:
            unmapped.append(topic)

    if not groups_seen and not unmapped:
        return ""

    # Sort by priority
    ordered = [g for g in GROUP_PRIORITY if g in groups_seen]
    return ", ".join(ordered)


def snapshot(master_path: Path) -> Path:
    """Save a timestamped snapshot of the master CSV before any write."""
    from datetime import datetime
    VERSIONS_DIR.mkdir(exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    dest = VERSIONS_DIR / f"creators-master_{ts}_pre-groups.csv"
    import shutil
    shutil.copy(master_path, dest)
    return dest


def main():
    parser = argparse.ArgumentParser(description="Normalize Topics and derive Groups in creators-master.csv")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without writing")
    parser.add_argument("--output", type=Path, default=None, help="Write to this path instead of in-place")
    parser.add_argument("--topics-only", action="store_true", help="Only normalize topics, skip groups derivation")
    parser.add_argument("--groups-only", action="store_true", help="Only derive groups from current topics")
    parser.add_argument("--show-changes", action="store_true",
                         help="List every row whose Groups value would change, old vs new (for review before running for real)")
    args = parser.parse_args()

    if not MASTER_CSV.exists():
        print(f"ERROR: {MASTER_CSV} not found", file=sys.stderr)
        sys.exit(1)

    with open(MASTER_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    print(f"Loaded {len(rows)} rows from {MASTER_CSV.name}")

    topic_changes = 0
    group_changes = 0
    unmapped_topics: Counter = Counter()
    all_warnings: list[str] = []
    group_diffs: list[tuple[str, str, str, str]] = []  # (slug, name, old_group, new_group)

    for row in rows:
        slug = row.get("slug", "")
        name = row.get("Creator Name", "")
        original_topic = row.get("Topic/Category", "")
        original_group = row.get("Groups", "")

        # Step 1: normalize topics
        if not args.groups_only:
            normalized_topic, warnings = normalize_topics(original_topic)
            if normalized_topic != original_topic:
                topic_changes += 1
                if warnings:
                    all_warnings.append(f"  {slug}: {'; '.join(warnings)}")
            row["Topic/Category"] = normalized_topic
        else:
            normalized_topic = original_topic

        # Step 2: derive groups
        if not args.topics_only:
            new_group = derive_groups(normalized_topic)

            # Track unmapped topics
            for t in [x.strip() for x in normalized_topic.split(",") if x.strip()]:
                if t not in TAG_TO_GROUP:
                    unmapped_topics[t] += 1

            if new_group != original_group:
                group_changes += 1
                group_diffs.append((slug, name, original_group, new_group))

            row["Groups"] = new_group

    # ── Report ────────────────────────────────────────────────────────────────
    print(f"\nTopic changes:  {topic_changes}")
    print(f"Group changes:  {group_changes}")

    if all_warnings:
        print(f"\nTopic normalizations ({len(all_warnings)}):")
        for w in all_warnings[:20]:
            print(w)
        if len(all_warnings) > 20:
            print(f"  ... and {len(all_warnings) - 20} more")

    if unmapped_topics:
        print(f"\nUnmapped topics (no Group assigned) — {len(unmapped_topics)} distinct:")
        for topic, count in unmapped_topics.most_common(20):
            print(f"  '{topic}' ({count} creators)")
        if len(unmapped_topics) > 20:
            print(f"  ... and {len(unmapped_topics) - 20} more")

    if args.show_changes and group_diffs:
        # Split into two categories: pure additions (derivation adds a bucket
        # the stored value didn't have — usually a real correction) vs. rows
        # that would LOSE a stored bucket derivation can't produce (likely a
        # deliberate editorial addition that would be silently discarded —
        # see runryan/Pipeline-Audit-for-Justin-Aug2026.md #3).
        losses = []
        additions_only = []
        for slug, name, old, new in group_diffs:
            old_set = {g.strip() for g in old.split(",") if g.strip()}
            new_set = {g.strip() for g in new.split(",") if g.strip()}
            if old_set - new_set:
                losses.append((slug, name, old, new))
            else:
                additions_only.append((slug, name, old, new))

        print(f"\n=== GROUPS WOULD CHANGE — {len(group_diffs)} rows ===")
        print(f"  {len(losses)} would LOSE a stored bucket topic-derivation can't reproduce (review these)")
        print(f"  {len(additions_only)} are pure additions/corrections (derivation adds, nothing lost)")

        if losses:
            print(f"\n--- LOSSES ({len(losses)}) — stored Groups value has a bucket the new derivation drops ---")
            for slug, name, old, new in losses:
                print(f"  {name} ({slug}): '{old}' → '{new}'")

        if additions_only:
            print(f"\n--- ADDITIONS ({len(additions_only)}) — derivation adds a bucket, nothing lost ---")
            for slug, name, old, new in additions_only[:20]:
                print(f"  {name} ({slug}): '{old}' → '{new}'")
            if len(additions_only) > 20:
                print(f"  ... and {len(additions_only) - 20} more")

    if args.dry_run:
        print("\n── DRY RUN — no files written ──")
        return

    # ── Write ─────────────────────────────────────────────────────────────────
    snap = snapshot(MASTER_CSV)
    print(f"\nSnapshot saved: {snap.name}")

    out_path = args.output or MASTER_CSV
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Written: {out_path}")
    print(f"\nNext: node convert.js to regenerate creators-data.json")


if __name__ == "__main__":
    main()
