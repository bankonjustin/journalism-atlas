#!/usr/bin/env python3
"""Bulk-update the rounded creator-count milestone string across partner pages.

Partner pages intentionally do not fetch creators-data.json (load speed /
portability — see CLAUDE.md). This script is the substitute: run it by hand
after any deploy that crosses a new hundred-milestone (e.g. 1,718 -> 1,806
crosses into the 1,800s).

Usage:
    python3 pipeline/update_partner_totals.py                # dry run, live master count
    python3 pipeline/update_partner_totals.py 1806            # dry run, explicit count
    python3 pipeline/update_partner_totals.py --apply         # write changes
"""

import argparse
import csv
import difflib
import glob
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MASTER_CSV = REPO_ROOT / "assets" / "data" / "creators-master.csv"
PARTNERS_GLOB = str(REPO_ROOT / "partners" / "*.html")

# Matches "1,700+ creator-journalists" and "1,700+ independent creator-journalists"
COUNT_PATTERN = re.compile(r'(\d{1,3}(?:,\d{3})*)\+(\s*(?:independent\s+)?creator-journalists)')


def live_master_count():
    with open(MASTER_CSV, encoding="utf-8-sig") as f:
        return sum(1 for _ in csv.DictReader(f))


def format_milestone(count):
    rounded = (count // 100) * 100
    return f"{rounded:,}+"


def update_content(content, milestone_str):
    new_number = milestone_str[:-1]  # strip trailing "+"
    return COUNT_PATTERN.sub(lambda m: f"{new_number}+{m.group(2)}", content)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("count", nargs="?", type=int, help="Override master row count (default: read creators-master.csv)")
    parser.add_argument("--apply", action="store_true", help="Write changes (default is dry-run)")
    args = parser.parse_args()

    count = args.count if args.count is not None else live_master_count()
    milestone_str = format_milestone(count)

    files = sorted(glob.glob(PARTNERS_GLOB))
    changed = []

    for path in files:
        with open(path, encoding="utf-8") as f:
            original = f.read()
        updated = update_content(original, milestone_str)
        if updated == original:
            continue

        old_values = sorted(set(m.group(1) + "+" for m in COUNT_PATTERN.finditer(original)))
        changed.append((path, old_values))

        if args.apply:
            with open(path, "w", encoding="utf-8") as f:
                f.write(updated)
        else:
            diff = difflib.unified_diff(
                original.splitlines(keepends=True),
                updated.splitlines(keepends=True),
                fromfile=path, tofile=path,
            )
            sys.stdout.writelines(diff)

    print()
    print(f"Master count: {count}  ->  milestone: {milestone_str}")
    print(f"Files scanned: {len(files)}")
    print(f"Files {'changed' if args.apply else 'that would change'}: {len(changed)}")
    for path, old_values in changed:
        print(f"  {path}: {', '.join(old_values)} -> {milestone_str}")

    if not args.apply and changed:
        print("\nDry run only — re-run with --apply to write these changes.")


if __name__ == "__main__":
    main()
