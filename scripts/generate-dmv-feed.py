#!/usr/bin/env python3
"""
generate-dmv-feed.py
Fetches recent posts from DMV creator RSS feeds and outputs
assets/data/dmv-recent-posts.json for use in city-lab-dc.html.

Run from the repo root:
  python3 scripts/generate-dmv-feed.py

Requires: feedparser, python-dateutil
  pip3 install feedparser python-dateutil
"""

import json
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

try:
    import feedparser
    from dateutil import parser as dateutil_parser
except ImportError:
    print("Missing dependencies. Run: pip3 install feedparser python-dateutil")
    sys.exit(1)

# ── Creator RSS feed definitions ───────────────────────────────
# (creator_name, channel, rss_url, primary_beat, geography)
RSS_FEEDS = [
    ("Martin Austermuhle",  "The 51st",              "https://51st.news/feed",                                    "DC Government",      "Washington, D.C."),
    ("Natalie Delgadillo",  "The 51st",              "https://51st.news/feed",                                    "Housing",            "Washington, D.C."),
    ("Alex Baca",           "Greater Greater Washington", "https://ggwash.org/rss/feed",                          "Housing",            "Washington, D.C."),
    ("Chris Kain",          "The DC Line",           "https://thedcline.org/feed",                                "DC Government",      "Washington, D.C."),
    ("William J. Ford",     "Maryland Matters",      "https://marylandmatters.org/feed",                          "Maryland Legislature","Maryland - US"),
    ("Brandon Jarvis",      "Virginia Scope",        "https://virginiapoliticalnewsletter.substack.com/feed",     "Virginia Legislature","Virginia - US"),
    ("Scott Brodbeck",      "ARLnow",                "https://www.arlnow.com/feed",                               "Northern Virginia",  "Arlington, VA"),
    ("Dan Silverman",       "PoPville",              "https://www.popville.com/feed",                             "DC Government",      "Washington, D.C."),
    ("Len Lazarick",        "MarylandReporter.com",  "https://marylandreporter.com/feed",                         "Maryland Legislature","Maryland - US"),
    ("Ryan Bacic",          "The Fairfax Machine",   "https://fairfaxmachine.substack.com/feed",                  "Northern Virginia",  "Virginia - US"),
    ("Delonte Harrod",      "Context Newsletter",    "https://contextnewsletter.substack.com/feed",               "Suburban Maryland",  "Maryland - US"),
    ("Barry O'Connell",     "The Maryland Wire",     "https://themarylandwire.substack.com/feed",                 "Maryland Legislature","Maryland - US"),
    ("Ellie Ashford",       "Annandale Today",       "https://annandaletoday.com/feed",                           "Northern Virginia",  "Virginia - US"),
    ("Uriah Kiser",         "Potomac Local News",    "https://www.potomaclocal.com/feed",                         "Northern Virginia",  "Virginia - US"),
    ("Alex Tsironis",       "The MoCo Show",         "https://mocoshow.com/feed",                                 "Suburban Maryland",  "Maryland - US"),
    ("Joe Friday",          "DC Crime Facts",        "https://dccrimefacts.substack.com/feed",                    "Criminal Justice",   "Washington, D.C."),
    ("Chris Wadsworth",     "The Burn",              "https://theburn.com/feed",                                  "Northern Virginia",  "Virginia - US"),
]

WINDOW_DAYS = 30
MAX_PER_CREATOR = 5


def strip_html(text):
    """Remove HTML tags and normalize whitespace."""
    text = re.sub(r'<[^>]+>', ' ', text or '')
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def parse_date(entry):
    """Try multiple date fields and return a datetime or None."""
    for field in ['published_parsed', 'updated_parsed']:
        val = getattr(entry, field, None)
        if val:
            try:
                return datetime(*val[:6])
            except Exception:
                pass
    for field in ['published', 'updated']:
        val = entry.get(field, '')
        if val:
            try:
                return dateutil_parser.parse(val)
            except Exception:
                pass
    return None


def fetch_all(window_days=WINDOW_DAYS, max_per=MAX_PER_CREATOR):
    cutoff = datetime.now() - timedelta(days=window_days)
    all_posts = []
    stats = {}

    for creator, channel, url, beat, geo in RSS_FEEDS:
        print(f"  Fetching {creator} ({channel})...", end=' ', flush=True)
        try:
            feed = feedparser.parse(url)
            count = 0
            for entry in feed.entries:
                if count >= max_per:
                    break
                pub = parse_date(entry)
                if pub and pub < cutoff:
                    continue
                summary = strip_html(entry.get('summary', ''))[:250]
                all_posts.append({
                    'creator': creator,
                    'channel': channel,
                    'beat': beat,
                    'geography': geo,
                    'title': (entry.get('title', '') or '')[:150],
                    'url': entry.get('link', ''),
                    'published': pub.strftime('%Y-%m-%d') if pub else None,
                    'published_iso': pub.isoformat() if pub else None,
                    'summary': summary,
                })
                count += 1
            stats[creator] = {'fetched': count, 'feed_size': len(feed.entries), 'error': None}
            print(f"{count} posts")
        except Exception as e:
            stats[creator] = {'fetched': 0, 'feed_size': 0, 'error': str(e)}
            print(f"ERROR: {e}")

    # Sort by published date desc
    all_posts.sort(key=lambda p: p.get('published_iso') or '', reverse=True)
    return all_posts, stats


def main():
    repo_root = Path(__file__).parent.parent
    out_path = repo_root / 'assets' / 'data' / 'dmv-recent-posts.json'

    print(f"Fetching DMV creator feeds (last {WINDOW_DAYS} days)...")
    posts, stats = fetch_all()

    output = {
        'generated': datetime.now().isoformat(),
        'generated_date': datetime.now().strftime('%Y-%m-%d'),
        'window_days': WINDOW_DAYS,
        'total': len(posts),
        'creators_fetched': len([s for s in stats.values() if s['fetched'] > 0]),
        'creators_no_rss': 11,  # Twitter/Instagram/unresolved
        'stats': stats,
        'posts': posts,
    }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\nDone. {len(posts)} posts from {output['creators_fetched']} creators.")
    print(f"Output: {out_path}")

    # Dead feeds
    errors = [(c, s['error']) for c, s in stats.items() if s['error']]
    if errors:
        print(f"\nErrors ({len(errors)}):")
        for c, e in errors:
            print(f"  {c}: {e}")


if __name__ == '__main__':
    main()
