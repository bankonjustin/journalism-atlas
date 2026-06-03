#!/usr/bin/env python3
"""
atlas_clean.py — Mechanical data cleaning for creators-master.csv
==================================================================
Applies all safe, rule-based fixes from SCHEMA-VOCAB.md:
  1. Platform vocab normalization (TikTok→Video-TikTok, X→Social-Twitter/X, etc.)
  2. URL fixes: http→https, strip query strings/fragments, twitter→x, threads.net→threads.com,
     strip navigational paths (/about, /subscribe, etc.), strip trailing slashes
  3. Geo Country fill for rows with Geography but missing Geo Country/Region

Does NOT touch: slugs, Topics, Groups, editorial fields, or anything requiring judgment.

Usage:
    python3 pipeline/atlas_clean.py --dry-run     # preview + full report
    python3 pipeline/atlas_clean.py               # apply in-place
"""

import argparse
import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from atlas_groups import snapshot

REPO_ROOT  = Path(__file__).parent.parent
MASTER_CSV = REPO_ROOT / "assets" / "data" / "creators-master.csv"

# ── Platform vocab correction map ─────────────────────────────────────────────

PLATFORM_FIXES: dict[str, str] = {
    "TikTok":              "Video - TikTok",
    "Tiktok":              "Video - TikTok",
    "TIkTok":              "Video - TikTok",
    "Social - TikTok":     "Video - TikTok",   # TikTok is video, not social
    "Social - Rumble":     "Video - Rumble",
    "Social- TikTok":      "Video - TikTok",
    "X":                   "Social - Twitter / X",
    "Twitter":             "Social - Twitter / X",
    "Social - X":          "Social - Twitter / X",
    "Social- X":           "Social - Twitter / X",
    "Social - Twitter/X":  "Social - Twitter / X",
    "YouTube":             "Video - YouTube",
    "Video - Youtube":     "Video - YouTube",
    "Video-  YouTube":     "Video - YouTube",
    "LinkedIn":            "Social - LinkedIn",
    "Social - Linkedin":   "Social - LinkedIn",
    "Instagram":           "Social - Instagram",
    "Social- Instagram":   "Social - Instagram",
    "Facebook":            "Social - Facebook",
    "Social- Facebook":    "Social - Facebook",
    "Bluesky":             "Social - BlueSky",
    "BlueSky":             "Social - BlueSky",
    "Blog":                "Website",
    "Website/Blog":        "Website",
    "Substack":            "Newsletter - Substack",
    "Ghost":               "Newsletter - Ghost",
    "Buttondown":          "Newsletter - Buttondown",
    "Newsletter":          "Newsletter - Other",
    "Podcast - Apple":     "Podcast",
    "Podcasts":            "Podcast",
    "Twitch":              "Video - Twitch",
    "Newsletter- Substack": "Newsletter - Substack",
    "Social- X":           "Social - Twitter / X",
}

# Navigational path suffixes to strip from URLs
NAV_PATHS = (
    "/subscribe", "/about", "/about-us", "/about/", "/about-us/",
    "/home", "/feed", "/login", "/account",
)

# Geography → (Geo Country, Geo Region) for mechanical fills
GEO_COUNTRY_MAP: dict[str, tuple[str, str]] = {
    "International":     ("International", "International"),
    "Scotland":          ("GB",            "International"),
    "Switzerland":       ("CH",            "International"),
    "Hungary":           ("HU",            "International"),
    "Austria":           ("AT",            "International"),
    "Lebanon":           ("LB",            "International"),
    "Palestine":         ("Palestine",     "International"),
    "Dubai":             ("AE",            "International"),
    "Portugal":          ("PT",            "International"),
    "South Asia":        ("International", "International"),
    "Iraq":              ("IQ",            "International"),
    "Colombia":          ("CO",            "International"),
    "Ukraine":           ("UA",            "International"),
    "Germany":           ("DE",            "International"),
    "Netherlands":       ("NL",            "International"),
    "France":            ("FR",            "International"),
    "Australia":         ("AU",            "International"),
    "Canada":            ("CA",            "International"),
    "United Kingdom":    ("GB",            "International"),
    "Mexico":            ("MX",            "International"),
    "Brazil":            ("BR",            "International"),
    "Spain":             ("ES",            "International"),
    "Sweden":            ("SE",            "International"),
    "Japan":             ("JP",            "International"),
    "India":             ("IN",            "International"),
    "Israel":            ("IL",            "International"),
    "New Zealand":       ("NZ",            "International"),
    "Nigeria":           ("NG",            "International"),
    "Kenya":             ("KE",            "International"),
    "South Africa":      ("ZA",            "International"),
    "Puerto Rico":       ("US",            "International"),  # US territory
}

# US state abbreviation → Geo Region
STATE_TO_REGION: dict[str, str] = {
    "ME":"Northeast","VT":"Northeast","NH":"Northeast","MA":"Northeast",
    "RI":"Northeast","CT":"Northeast","NY":"Northeast","NJ":"Northeast",
    "PA":"Northeast","DE":"Northeast",
    "OH":"Midwest","IN":"Midwest","IL":"Midwest","MI":"Midwest",
    "WI":"Midwest","MN":"Midwest","IA":"Midwest","MO":"Midwest",
    "ND":"Midwest","SD":"Midwest","NE":"Midwest","KS":"Midwest",
    "MD":"South","VA":"South","WV":"South","NC":"South","SC":"South",
    "GA":"South","FL":"South","KY":"South","TN":"South","AL":"South",
    "MS":"South","AR":"South","LA":"South","OK":"South","TX":"South",
    "MT":"West","ID":"West","WY":"West","CO":"West","NM":"West",
    "AZ":"West","UT":"West","NV":"West","WA":"West","OR":"West",
    "CA":"West","AK":"West","HI":"West",
    "DC":"Mid-Atlantic",
}


# ── URL cleaning ───────────────────────────────────────────────────────────────

def clean_url(url: str) -> tuple[str, list[str]]:
    """
    Apply all SCHEMA-VOCAB URL normalization rules.
    Returns (cleaned_url, list_of_changes_made).
    """
    if not url:
        return url, []

    original = url
    changes = []

    # http → https
    if url.startswith("http://"):
        url = "https://" + url[7:]
        changes.append("http→https")

    # twitter.com → x.com
    if "twitter.com" in url:
        url = url.replace("twitter.com", "x.com")
        changes.append("twitter→x")

    # threads.net → threads.com
    if "threads.net" in url:
        url = url.replace("threads.net", "threads.com")
        changes.append("threads.net→threads.com")

    # Strip query strings (? and everything after, before any #)
    if "?" in url:
        url = url.split("?")[0]
        changes.append("stripped query string")

    # Strip fragments
    if "#" in url:
        url = url.split("#")[0]
        changes.append("stripped fragment")

    # Strip navigational paths
    for nav in NAV_PATHS:
        if url.lower().rstrip("/").endswith(nav.rstrip("/")):
            url = url[:url.lower().rstrip("/").rfind(nav.rstrip("/"))]
            url = url.rstrip("/")
            changes.append(f"stripped {nav}")
            break

    # Strip trailing slash (but not bare domain: https://example.com/)
    if url.endswith("/") and url.count("/") > 3:
        url = url.rstrip("/")
        changes.append("stripped trailing slash")

    return url, changes


# ── Geo fill ───────────────────────────────────────────────────────────────────

def fill_geo_country(row: dict) -> tuple[str, str, list[str]]:
    """
    Return (geo_country, geo_region, changes) if we can fill them.
    Returns current values unchanged if we can't determine confidently.
    """
    current_country = row.get("Geo Country", "").strip()
    current_region  = row.get("Geo Region", "").strip()
    if current_country:
        return current_country, current_region, []  # already set

    geo   = row.get("Geography", "").strip()
    state = row.get("Geo State", "").strip()

    # US with state → fill country + region
    if state and state in STATE_TO_REGION:
        region = STATE_TO_REGION[state]
        if state == "DC":
            return "US", "Mid-Atlantic", ["filled Geo Country=US, Geo Region=Mid-Atlantic"]
        return "US", region, [f"filled Geo Country=US, Geo Region={region}"]

    # National - US
    if geo in ("National - US", "National"):
        return "US", "National", ["filled Geo Country=US, Geo Region=National"]

    # Geography matches our country map
    for key, (country, region) in GEO_COUNTRY_MAP.items():
        if geo == key or geo.startswith(key + ",") or geo.endswith(", " + key):
            return country, region, [f"filled Geo Country={country}, Geo Region={region} from geo='{geo}'"]

    # US city format "City, ST"
    m = re.match(r'^.+,\s+([A-Z]{2})$', geo)
    if m:
        state_code = m.group(1)
        if state_code in STATE_TO_REGION:
            region = STATE_TO_REGION[state_code]
            return "US", region, [f"filled Geo Country=US, Geo Region={region} from geo='{geo}'"]
        if state_code == "DC":
            return "US", "Mid-Atlantic", [f"filled Geo Country=US, Geo Region=Mid-Atlantic from geo='{geo}'"]

    return current_country, current_region, []  # can't determine


# ── Geography format fixes ─────────────────────────────────────────────────────

GEO_FORMAT_FIXES: dict[str, str] = {
    "Oakland. CA":    "Oakland, CA",
    "United States":  "National - US",
    "USA":            "National - US",
    "Washington DC":  "Washington, DC",
    "Washington, D.C.": "Washington, DC",
}


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Mechanical data cleaning for creators-master.csv")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--master", type=Path, default=MASTER_CSV)
    args = parser.parse_args()

    with open(args.master, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    print(f"Loaded {len(rows)} rows")

    url_fields = ["Link Primary", "Platform 2 Link", "Platform 3 Link", "Platform 4 Link"]
    platform_fields = ["Platform Primary", "Platform 2 Name", "Platform 3 Name", "Platform 4 Name"]

    total_platform_fixes = 0
    total_url_fixes = 0
    total_geo_fills = 0
    total_geo_format_fixes = 0
    flagged_unknown_platform: list[tuple] = []
    change_log: list[str] = []

    for row in rows:
        slug = row.get("slug", "")

        # Platform vocab
        for field in platform_fields:
            val = row.get(field, "").strip()
            if not val:
                continue
            fixed = PLATFORM_FIXES.get(val)
            if fixed:
                change_log.append(f"  {slug} [{field}]: '{val}' → '{fixed}'")
                row[field] = fixed
                total_platform_fixes += 1
            elif val and val not in {
                "Newsletter - Substack","Newsletter - Beehiiv","Newsletter - Ghost",
                "Newsletter - Buttondown","Newsletter - Other",
                "Podcast","Website","Patreon","Chat - SMS",
                "Video - YouTube","Video - Instagram","Video - TikTok","Video - Twitch","Video - Rumble",
                "Social - Twitter / X","Social - BlueSky","Social - LinkedIn",
                "Social - Facebook","Social - Instagram","Social - Threads","Social - TikTok",
            }:
                flagged_unknown_platform.append((slug, field, val))

        # URLs
        for field in url_fields:
            url = row.get(field, "").strip()
            if not url:
                continue
            cleaned, changes = clean_url(url)
            if changes:
                change_log.append(f"  {slug} [{field}]: {', '.join(changes)}")
                if len(changes) == 1 and "trailing slash" in changes[0]:
                    pass  # suppress individual trailing-slash log noise
                row[field] = cleaned
                total_url_fixes += 1

        # Geography format
        geo = row.get("Geography", "").strip()
        if geo in GEO_FORMAT_FIXES:
            fixed_geo = GEO_FORMAT_FIXES[geo]
            change_log.append(f"  {slug} [Geography]: '{geo}' → '{fixed_geo}'")
            row["Geography"] = fixed_geo
            total_geo_format_fixes += 1

        # Geo Country fill
        new_country, new_region, geo_changes = fill_geo_country(row)
        if geo_changes:
            for c in geo_changes:
                change_log.append(f"  {slug}: {c}")
            row["Geo Country"] = new_country
            row["Geo Region"]  = new_region
            total_geo_fills += 1

    # ── Summary ───────────────────────────────────────────────────────────────

    trailing_slash_count = sum(1 for l in change_log if "trailing slash" in l)
    other_url_count = total_url_fixes - trailing_slash_count

    print(f"\nChanges:")
    print(f"  Platform vocab fixes:   {total_platform_fixes}")
    print(f"  URL fixes (non-slash):  {other_url_count}")
    print(f"  Trailing slash strips:  {trailing_slash_count}")
    print(f"  Geo Country fills:      {total_geo_fills}")
    print(f"  Geography format fixes: {total_geo_format_fixes}")

    if flagged_unknown_platform:
        print(f"\nFlagged — unknown platform vocab ({len(flagged_unknown_platform)} rows) — REVIEW NEEDED:")
        for slug, field, val in flagged_unknown_platform:
            print(f"  {slug} [{field}]: '{val}'")

    if not args.dry_run:
        # Show non-trivial changes before writing
        notable = [l for l in change_log if "trailing slash" not in l]
        if notable:
            print(f"\nNon-trailing-slash changes ({len(notable)}):")
            for l in notable[:40]:
                print(l)
            if len(notable) > 40:
                print(f"  ... and {len(notable)-40} more")
    else:
        # In dry run, show everything
        notable = [l for l in change_log if "trailing slash" not in l]
        if notable:
            print(f"\nAll non-trailing-slash changes ({len(notable)}):")
            for l in notable[:60]:
                print(l)
            if len(notable) > 60:
                print(f"  ... and {len(notable)-60} more")
        print(f"\n── DRY RUN — no files written ──")
        return

    snap = snapshot(args.master)
    print(f"\nSnapshot: {snap.name}")

    with open(args.master, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Written: {args.master.name}")
    print(f"Next: node convert.js to regenerate creators-data.json")


if __name__ == "__main__":
    main()
