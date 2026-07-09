#!/usr/bin/env python3
"""
atlas_normalize.py — Validation/report tool for creators-master.csv
=====================================================================
Flags rows against the documented 19-column schema and controlled
vocabularies (DATA-OPS-PROTOCOL.md / SCHEMA-VOCAB.md). Read-only.
Never adds, deletes, reclassifies, or rewrites any row in the master CSV.

Checks (v1.0 — the 8 known recurring issues):
  1. Bluesky link containing the literal string "handle.invalid"
  2. Bluesky link pointing at a directory/aggregator site (or any URL that
     doesn't match the bsky.app/profile/<handle> shape) instead of a handle
  3. The same Bluesky handle claimed by more than one slug (cross-row only —
     the same handle repeated across two platform slots on ONE row is not
     a conflict and is not flagged)
  4. Platform vocab typos / non-controlled values in Platform Primary or
     Platform 2-4 Name
  5. Groups values using the retired comma form ("Science, Health & Environment")
  6. Partner Lists (column 19) missing from the file entirely (18-column input)
  7. Geo Country not a two-letter ISO code (e.g. "USA" instead of "US")
  8. Duplicate slugs (case-insensitive)

Out of scope for v1.0 (see ATLAS-NORMALIZE-LINTER-BRIEF-v1.0.md):
  - Topic/Category vocabulary check — no confirmed canonical source found
  - Auto-writing corrections (--output) — not implemented yet; ship the
    report, get it reviewed, then add write mode in a follow-up pass

Usage:
    python3 pipeline/atlas_normalize.py --dry-run
    python3 pipeline/atlas_normalize.py --master path/to/other.csv
"""

import argparse
import csv
import re
import sys
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

REPO_ROOT   = Path(__file__).parent.parent
MASTER_CSV  = REPO_ROOT / "assets" / "data" / "creators-master.csv"
REPORT_ROOT = Path.home() / "Documents" / "Atlas Spidering" / "sessions"

EXPECTED_COLUMNS = [
    "Creator Name", "slug", "Creator Channel", "Link Primary",
    "Platform Primary", "Platform 2 Name", "Platform 2 Link",
    "Platform 3 Name", "Platform 3 Link", "Platform 4 Name", "Platform 4 Link",
    "Topic/Category", "Geography", "Groups",
    "Geo City", "Geo State", "Geo Country", "Geo Region",
    "Partner Lists",
]

PLATFORM_VOCAB = {
    "Newsletter - Substack", "Newsletter - Beehiiv", "Newsletter - Ghost",
    "Newsletter - Buttondown", "Newsletter - Other",
    "Podcast", "Website", "Patreon", "Chat - SMS",
    "Video - YouTube", "Video - Instagram", "Video - TikTok", "Video - Twitch", "Video - Rumble",
    "Social - Twitter / X", "Social - BlueSky", "Social - LinkedIn",
    "Social - Facebook", "Social - Instagram", "Social - Threads", "Social - TikTok",
}

# Known typo -> correct form (SCHEMA-VOCAB.md). Report-only: suggest, don't apply.
PLATFORM_TYPO_MAP = {
    "Blog": "Website", "Website/Blog": "Website",
    "Substack": "Newsletter - Substack",
    "Ghost": "Newsletter - Ghost",
    "Buttondown": "Newsletter - Buttondown",
    "Newsletter": "Newsletter - Other",
    "Podcast - Apple": "Podcast", "Podcasts": "Podcast",
    "YouTube": "Video - YouTube", "Video - Youtube": "Video - YouTube",
    "Social - YouTube": "Video - YouTube",
    "TikTok": "Video - TikTok", "Tiktok": "Video - TikTok", "TIkTok": "Video - TikTok",
    "Social - TikTok's": "Video - TikTok",
    "Instagram": "Social - Instagram",
    "Facebook": "Social - Facebook",
    "Twitter": "Social - Twitter / X", "X": "Social - Twitter / X",
    "Social - X": "Social - Twitter / X", "Social - Twitter/X": "Social - Twitter / X",
    "Bluesky": "Social - BlueSky", "BlueSky": "Social - BlueSky", "BllueSky": "Social - BlueSky",
    "Social - Linkedin": "Social - LinkedIn",
    "Twitch": "Video - Twitch",
    "Social - Rumble": "Video - Rumble",
}

NAME_FIELDS = ["Platform Primary", "Platform 2 Name", "Platform 3 Name", "Platform 4 Name"]
LINK_FIELDS = ["Link Primary", "Platform 2 Link", "Platform 3 Link", "Platform 4 Link"]
PLATFORM_PAIRS = list(zip(NAME_FIELDS, LINK_FIELDS))

BSKY_HANDLE_RE = re.compile(r"bsky\.app/profile/([^/?#]+)", re.I)
ISO3_RE = re.compile(r"^[A-Z]{3}$")


def flag(issue, slug, name, field, value, detail):
    return {"issue": issue, "slug": slug or "", "creator": name or "", "field": field or "", "value": value or "", "detail": detail}


# ── Checks ───────────────────────────────────────────────────────────────────

def check_bluesky_handle_invalid(rows):
    flags = []
    for r in rows:
        for nf, lf in PLATFORM_PAIRS:
            if r.get(nf, "").strip() == "Social - BlueSky":
                link = r.get(lf, "").strip()
                if "handle.invalid" in link.lower():
                    flags.append(flag("bluesky_handle_invalid", r.get("slug"), r.get("Creator Name"), lf, link,
                                       "Bluesky link contains the literal string 'handle.invalid'"))
    return flags


def check_bluesky_bad_link(rows):
    flags = []
    for r in rows:
        for nf, lf in PLATFORM_PAIRS:
            if r.get(nf, "").strip() == "Social - BlueSky":
                link = r.get(lf, "").strip()
                if not link:
                    continue
                if "blueskydirectory.com" in link.lower():
                    flags.append(flag("bluesky_directory_url", r.get("slug"), r.get("Creator Name"), lf, link,
                                       "Points at a Bluesky directory/aggregator site, not the creator's own profile"))
                elif not BSKY_HANDLE_RE.search(link):
                    flags.append(flag("bluesky_non_standard_link", r.get("slug"), r.get("Creator Name"), lf, link,
                                       "Doesn't match the expected bsky.app/profile/<handle> format"))
    return flags


def check_bluesky_duplicate_handles(rows):
    handle_to_slugs = defaultdict(set)
    for r in rows:
        row_handles = set()
        for nf, lf in PLATFORM_PAIRS:
            if r.get(nf, "").strip() == "Social - BlueSky":
                m = BSKY_HANDLE_RE.search(r.get(lf, "").strip())
                if m:
                    row_handles.add(m.group(1).lower())
        for h in row_handles:
            handle_to_slugs[h].add(r.get("slug", ""))

    flags = []
    for h, slugs in handle_to_slugs.items():
        if len(slugs) > 1:
            slug_list = ", ".join(sorted(slugs))
            flags.append(flag("bluesky_duplicate_handle", slug_list, None, "Platform Link", h,
                               f"Handle claimed by {len(slugs)} different slugs: {slug_list}"))
    return flags


def check_platform_vocab(rows):
    flags = []
    for r in rows:
        for field in NAME_FIELDS:
            val = r.get(field, "").strip()
            if not val or val in PLATFORM_VOCAB:
                continue
            suggestion = PLATFORM_TYPO_MAP.get(val)
            detail = f"known typo — suggest '{suggestion}'" if suggestion else "not in controlled vocab — needs manual review"
            flags.append(flag("platform_vocab", r.get("slug"), r.get("Creator Name"), field, val, detail))
    return flags


def check_groups_comma_form(rows):
    flags = []
    for r in rows:
        val = r.get("Groups", "")
        if "Science, Health" in val:
            flags.append(flag("groups_comma_form", r.get("slug"), r.get("Creator Name"), "Groups", val,
                               "Uses the retired comma form — should be 'Science Health & Environment' (no comma)"))
    return flags


def check_partner_lists_column(fieldnames):
    if "Partner Lists" not in (fieldnames or []):
        return [flag("schema_missing_column", None, None, "Partner Lists", None,
                      f"Column is missing entirely from this file — found {len(fieldnames or [])} columns, expected 19")]
    return []


def check_geo_country_iso(rows):
    flags = []
    for r in rows:
        val = r.get("Geo Country", "").strip()
        if val and ISO3_RE.match(val):
            flags.append(flag("geo_country_not_iso2", r.get("slug"), r.get("Creator Name"), "Geo Country", val,
                               "Looks like a 3-letter code — schema requires two-letter ISO codes (e.g. 'US' not 'USA')"))
    return flags


def check_duplicate_slugs(rows):
    counts = Counter(r.get("slug", "").strip().lower() for r in rows if r.get("slug", "").strip())
    dupes = {s for s, c in counts.items() if c > 1}
    flags = []
    for r in rows:
        s = r.get("slug", "").strip().lower()
        if s in dupes:
            flags.append(flag("duplicate_slug", r.get("slug"), r.get("Creator Name"), "slug", r.get("slug"),
                               f"slug '{s}' appears {counts[s]} times"))
    return flags


# ── Report ───────────────────────────────────────────────────────────────────

ISSUE_LABELS = [
    ("bluesky_handle_invalid",     "1. Bluesky handle.invalid literal"),
    ("bluesky_directory_url",      "2a. Bluesky link is a directory/aggregator URL"),
    ("bluesky_non_standard_link",  "2b. Bluesky link doesn't match bsky.app/profile/<handle>"),
    ("bluesky_duplicate_handle",   "3. Duplicate Bluesky handle across rows"),
    ("platform_vocab",             "4. Platform vocab typo / non-controlled value"),
    ("groups_comma_form",          "5. Groups comma form"),
    ("schema_missing_column",      "6. Partner Lists column missing"),
    ("geo_country_not_iso2",       "7. Geo Country not two-letter ISO"),
    ("duplicate_slug",             "8. Duplicate slug"),
]


def write_report(master_path, row_count, flags_by_issue, report_dir):
    report_dir.mkdir(parents=True, exist_ok=True)
    report_path = report_dir / "report.md"

    total = sum(len(v) for v in flags_by_issue.values())
    lines = [
        "# Atlas Normalize — Validation Report",
        "",
        f"**Source:** `{master_path}` ({row_count} rows) — read-only, no changes made",
        f"**Date:** {date.today().isoformat()}",
        f"**Total flags:** {total}",
        "",
        "| Issue | Count |",
        "|---|---|",
    ]
    for key, label in ISSUE_LABELS:
        lines.append(f"| {label} | {len(flags_by_issue.get(key, []))} |")
    lines.append("")

    for key, label in ISSUE_LABELS:
        rows = flags_by_issue.get(key, [])
        lines.append(f"## {label} ({len(rows)})")
        lines.append("")
        if not rows:
            lines.append("_None found._")
            lines.append("")
            continue
        lines.append("| slug | creator | field | value | detail |")
        lines.append("|---|---|---|---|---|")
        for f in rows:
            value = (f["value"] or "").replace("|", "\\|")
            lines.append(f"| {f['slug']} | {f['creator']} | {f['field']} | {value} | {f['detail']} |")
        lines.append("")

    report_path.write_text("\n".join(lines), encoding="utf-8")
    return report_path


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Read-only validation report for creators-master.csv. Never writes to the master."
    )
    parser.add_argument("master", type=Path, nargs="?", default=MASTER_CSV,
                         help="Path to the master CSV to validate (default: assets/data/creators-master.csv)")
    parser.add_argument("--dry-run", action="store_true",
                         help="No-op flag — v1.0 is always report-only regardless")
    parser.add_argument("--output", type=Path, default=None,
                         help="Not implemented in v1.0 — reserved for a future corrected-copy write mode")
    args = parser.parse_args()

    if args.output is not None:
        print("ERROR: --output is not implemented in v1.0. This script is report-only for now — "
              "see ATLAS-NORMALIZE-LINTER-BRIEF-v1.0.md.", file=sys.stderr)
        sys.exit(1)

    if not args.master.exists():
        print(f"ERROR: {args.master} not found", file=sys.stderr)
        sys.exit(1)

    with open(args.master, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    print(f"Loaded {len(rows)} rows from {args.master}")
    if fieldnames != EXPECTED_COLUMNS:
        print(f"NOTE: column headers differ from the documented 19-column schema "
              f"({len(fieldnames or [])} columns found).")

    flags_by_issue = {
        "schema_missing_column":     check_partner_lists_column(fieldnames),
        "bluesky_handle_invalid":    check_bluesky_handle_invalid(rows),
        "bluesky_directory_url":     [],
        "bluesky_non_standard_link": [],
        "bluesky_duplicate_handle":  check_bluesky_duplicate_handles(rows),
        "platform_vocab":            check_platform_vocab(rows),
        "groups_comma_form":         check_groups_comma_form(rows),
        "geo_country_not_iso2":      check_geo_country_iso(rows),
        "duplicate_slug":            check_duplicate_slugs(rows),
    }
    bad_links = check_bluesky_bad_link(rows)
    flags_by_issue["bluesky_directory_url"] = [f for f in bad_links if f["issue"] == "bluesky_directory_url"]
    flags_by_issue["bluesky_non_standard_link"] = [f for f in bad_links if f["issue"] == "bluesky_non_standard_link"]

    total = sum(len(v) for v in flags_by_issue.values())
    print(f"\nFlags found: {total}")
    for key, label in ISSUE_LABELS:
        print(f"  {label}: {len(flags_by_issue.get(key, []))}")

    report_dir = REPORT_ROOT / f"normalize_report_{date.today().isoformat().replace('-', '')}"
    report_path = write_report(args.master, len(rows), flags_by_issue, report_dir)
    print(f"\nReport written: {report_path}")
    print("No changes made to the master CSV.")


if __name__ == "__main__":
    main()
