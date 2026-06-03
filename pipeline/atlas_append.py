#!/usr/bin/env python3
"""
atlas_append.py — Append new creator rows to creators-master.csv
=================================================================
Validates, deduplicates, and appends new rows from a batch CSV.
Runs atlas_groups normalization on the new rows before appending.

Usage:
    # From repo root:
    python3 pipeline/atlas_append.py new_rows.csv --dry-run
    python3 pipeline/atlas_append.py new_rows.csv

    # Explicit master path:
    python3 pipeline/atlas_append.py new_rows.csv --master path/to/creators-master.csv

What it does:
    1. Loads existing master — dedup index by URL and slug
    2. Loads new rows — validates required fields, normalizes topics/groups
    3. Dedup pass — skips rows already in master (URL-normalized match)
    4. Schema validation — warns on missing fields, bad platform vocab
    5. Snapshots master, appends clean rows, reports
"""

import argparse
import csv
import re
import sys
from pathlib import Path

# Add pipeline dir to path so we can import atlas_groups
sys.path.insert(0, str(Path(__file__).parent))
from atlas_groups import normalize_topics, derive_groups, snapshot

REPO_ROOT  = Path(__file__).parent.parent
MASTER_CSV = REPO_ROOT / "assets" / "data" / "creators-master.csv"

REQUIRED_FIELDS = ["Creator Name", "slug", "Link Primary", "Platform Primary", "Topic/Category"]

VALID_PLATFORMS = {
    "Newsletter - Substack", "Newsletter - Beehiiv", "Newsletter - Ghost",
    "Newsletter - Buttondown", "Newsletter - Other",
    "Podcast", "Website", "Patreon", "Chat - SMS",
    "Video - YouTube", "Video - Instagram", "Video - TikTok", "Video - Twitch", "Video - Rumble",
    "Social - Twitter / X", "Social - BlueSky", "Social - LinkedIn",
    "Social - Facebook", "Social - Instagram", "Social - Threads", "Social - TikTok",
}

MASTER_FIELDNAMES = [
    "Creator Name", "slug", "Creator Channel", "Link Primary",
    "Platform Primary", "Platform 2 Name", "Platform 2 Link",
    "Platform 3 Name", "Platform 3 Link", "Platform 4 Name", "Platform 4 Link",
    "Topic/Category", "Geography", "Groups",
    "Geo City", "Geo State", "Geo Country", "Geo Region",
]


def normalize_url(url: str) -> str:
    url = url.strip().lower().rstrip("/")
    url = re.sub(r"^https?://", "", url)
    url = re.sub(r"^www\.", "", url)
    return url


def load_master(path: Path) -> tuple[list[dict], set[str], set[str]]:
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    urls = {normalize_url(r.get("Link Primary", "")) for r in rows if r.get("Link Primary")}
    slugs = {r.get("slug", "").lower() for r in rows if r.get("slug")}
    return rows, urls, slugs


def load_new_rows(path: Path) -> tuple[list[dict], list[str]]:
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    return rows, []


def validate_row(row: dict, existing_urls: set[str], existing_slugs: set[str]) -> list[str]:
    issues = []
    for field in REQUIRED_FIELDS:
        if not row.get(field, "").strip():
            issues.append(f"missing required field: {field}")

    url = normalize_url(row.get("Link Primary", ""))
    if url and url in existing_urls:
        issues.append(f"DUPLICATE URL: {row.get('Link Primary', '')}")

    slug = row.get("slug", "").lower().strip()
    if slug and slug in existing_slugs:
        issues.append(f"DUPLICATE SLUG: {slug}")

    platform = row.get("Platform Primary", "").strip()
    if platform and platform not in VALID_PLATFORMS:
        issues.append(f"unknown platform: '{platform}' — check SCHEMA-VOCAB.md")

    return issues


def normalize_row_for_master(row: dict) -> dict:
    """Ensure all 18 master fields exist, normalize topics/groups, return clean row."""
    clean = {f: row.get(f, "").strip() for f in MASTER_FIELDNAMES}

    # Normalize Topic/Category
    normalized_topic, _ = normalize_topics(clean["Topic/Category"])
    clean["Topic/Category"] = normalized_topic

    # Derive Groups
    clean["Groups"] = derive_groups(normalized_topic)

    return clean


def main():
    parser = argparse.ArgumentParser(description="Append new creator rows to creators-master.csv")
    parser.add_argument("batch", type=Path, help="CSV file with new rows to append")
    parser.add_argument("--master", type=Path, default=MASTER_CSV)
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    args = parser.parse_args()

    if not args.batch.exists():
        print(f"ERROR: Batch file not found: {args.batch}", file=sys.stderr)
        sys.exit(1)

    if not args.master.exists():
        print(f"ERROR: Master CSV not found: {args.master}", file=sys.stderr)
        sys.exit(1)

    master_rows, existing_urls, existing_slugs = load_master(args.master)
    print(f"Master: {len(master_rows)} rows loaded")

    new_rows_raw, _ = load_new_rows(args.batch)
    print(f"Batch:  {len(new_rows_raw)} rows in file")

    clean_rows: list[dict] = []
    skipped_dup: list[dict] = []
    skipped_err: list[tuple[dict, list[str]]] = []

    for row in new_rows_raw:
        issues = validate_row(row, existing_urls, existing_slugs)

        dup_issues = [i for i in issues if "DUPLICATE" in i]
        other_issues = [i for i in issues if "DUPLICATE" not in i]

        if dup_issues:
            skipped_dup.append((row, dup_issues))
            continue
        if other_issues:
            skipped_err.append((row, other_issues))
            # Still normalize and include with warnings — don't silently drop
            pass

        clean = normalize_row_for_master(row)
        clean_rows.append(clean)
        # Add to dedup index for rest of batch
        url = normalize_url(clean["Link Primary"])
        if url:
            existing_urls.add(url)
        if clean["slug"]:
            existing_slugs.add(clean["slug"].lower())

    print(f"\nResults:")
    print(f"  To append:      {len(clean_rows)}")
    print(f"  Skipped (dup):  {len(skipped_dup)}")
    print(f"  Warnings:       {len(skipped_err)}")

    if skipped_dup:
        print(f"\nDuplicates skipped:")
        for row, issues in skipped_dup[:10]:
            print(f"  {row.get('Creator Name', '?')} — {'; '.join(issues)}")
        if len(skipped_dup) > 10:
            print(f"  ... and {len(skipped_dup) - 10} more")

    if skipped_err:
        print(f"\nRows with warnings (will be appended — review after):")
        for row, issues in skipped_err[:10]:
            print(f"  {row.get('Creator Name', '?')} — {'; '.join(issues)}")

    if args.dry_run:
        print("\n── DRY RUN — no files written ──")
        if clean_rows:
            print(f"\nFirst row preview:")
            for k, v in clean_rows[0].items():
                if v:
                    print(f"  {k}: {v}")
        return

    if not clean_rows:
        print("\nNothing to append.")
        return

    snap = snapshot(args.master)
    print(f"\nSnapshot: {snap.name}")

    with open(args.master, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=MASTER_FIELDNAMES)
        writer.writerows(clean_rows)

    print(f"Appended {len(clean_rows)} rows to {args.master.name}")
    print(f"New total: {len(master_rows) + len(clean_rows)}")
    print(f"\nNext: node convert.js to regenerate creators-data.json")


if __name__ == "__main__":
    main()
