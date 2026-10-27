#!/usr/bin/env python3
"""The shared "main beats" list and this week's per-beat figures. One module, read by both builds:

  scripts/build_lens_index.py   (the /for-brands Issue Lens: chips)
  journalism-atlas-private/pipelines/pulse/update_pulse.py   (the /pulse field: clusters, panels, hidden table)

Rules (one place, so the two pages cannot disagree):
  * Counting is ANY-TAG and EXACT-TAG: a piece counts under every beat tag it carries (comma-split, no folding).
    Creators include co-hosts, because a co-hosted piece counts for each host.
  * Beat tags belong to CREATORS, not pieces. A beat count is therefore "creators who cover the beat" and "pieces those
    creators published this week"; every piece a creator publishes counts under every beat they cover.
  * A beat is a MAIN beat when it has at least MIN_PIECES pieces in the issue window and at least MIN_CREATORS creators
    in the registry carrying the tag (the Lens rule, unchanged). Main beats are ordered by pieces this week, then name.
    The Lens keeps this whole list (28 beats this week).
  * The FIELD caps its display at FIELD_BEATS (10): the ten main beats with the most creators get their own labeled
    cluster (the same ten at every width); every other beat packs into one "{n} more beats" cluster.
  * Primary beat (used ONLY to place a creator's circle in the field): the largest, by creators, of the beats they cover.
    (Tags are per creator, so "the beat they published most in" is always a tie; the largest beat is the tie-break.)
    A creator whose largest beat is not one of the ten displayed sits in the "more beats" cluster.
  * Printed figures never use the primary assignment. Cluster labels and panels are any-tag creator counts.

compute() is pure (pieces in, dict out). load_window_pieces() reads the committed weekly post files for callers that
have no in-memory list (the Lens build).
"""
import html
import json
import re
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MIN_PIECES = 40
MIN_CREATORS = 25
TOP_CREATORS = 8
FIELD_BEATS = 10   # the field shows this many beats as clusters; the Lens keeps the full main-beat list

SOCIAL_HOSTS = {"bsky.app", "x.com", "twitter.com", "instagram.com", "facebook.com", "threads.net", "threads.com",
                "tiktok.com", "linkedin.com", "mastodon.social", "t.me"}   # mirrors pulse_canonical.SOCIAL_HOSTS


def split_tags(raw):
    return [t.strip() for t in (raw or "").split(",") if t.strip()]


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", str(s).lower()).strip("-")


def _host(url):
    h = urllib.parse.urlparse(url or "").netloc.lower()
    return h[4:] if h.startswith("www.") else h


def load_registry_tag_counts(root=ROOT):
    """Registry creators per exact beat tag (the Lens rule's second condition)."""
    counts = {}
    for c in json.loads((Path(root) / "assets/data/creators-data.json").read_text()):
        for t in set(split_tags(c.get("topic"))):
            counts[t] = counts.get(t, 0) + 1
    return counts


def load_registry_links(root=ROOT):
    """Creator name -> their own channel link from the registry (http/https only)."""
    out = {}
    for c in json.loads((Path(root) / "assets/data/creators-data.json").read_text()):
        l = (c.get("link") or "").strip()
        if c.get("name") and l.startswith(("http://", "https://")):
            out[c["name"]] = l
    return out


def load_issue(root=ROOT):
    issues = json.loads((Path(root) / "data/pulse-issues.json").read_text())
    latest = issues["issues"][sorted(issues["issues"])[-1]]
    return latest


def load_window_pieces(root=ROOT, w_from=None, w_to=None):
    """Pieces in the issue window from the committed weekly files (same filters as the Lens build)."""
    root = Path(root)
    if not w_from:
        latest = load_issue(root)
        w_from, w_to = latest["week_start"], latest["week_end"]
    seen, out = set(), []
    for f in sorted((root / "assets/data/pulse").glob("posts-*.json")):
        for p in json.loads(f.read_text())["posts"]:
            if not (w_from <= p["published"] <= w_to):
                continue
            url = p.get("url") or ""
            title = html.unescape((p.get("title") or "").strip())
            if not url or not title or title.lower() == "no title" or _host(url) in SOCIAL_HOSTS or url in seen:
                continue
            seen.add(url)
            out.append({**p, "title": title})
    return out


def main_beat_labels(pieces, tag_creators):
    """Ordered main-beat labels. `tag_creators` = registry creators per tag (load_registry_tag_counts)."""
    pc = {}
    for p in pieces:
        for t in set(split_tags(p.get("topic"))):
            pc[t] = pc.get(t, 0) + 1
    ok = [t for t in pc if pc[t] >= MIN_PIECES and tag_creators.get(t, 0) >= MIN_CREATORS]
    return sorted(ok, key=lambda t: (-pc[t], t)), pc


def compute(pieces, tag_creators, w_from, w_to, links=None):
    """Everything the field needs. `pieces` are already filtered to the window (one record per URL). `links`: name -> channel URL."""
    links = links or {}
    main, pc = main_beat_labels(pieces, tag_creators)

    cr_pieces, cr_tagcount, cr_latest = {}, {}, {}
    beat_creators, beat_cr_pieces = {}, {}
    for p in pieces:
        tags = sorted(set(split_tags(p.get("topic"))))
        for name in [p["creator"], *(p.get("co") or [])]:
            cr_pieces[name] = cr_pieces.get(name, 0) + 1
            if name not in cr_latest or (p["published"], p.get("published_at") or "") > cr_latest[name][0]:
                cr_latest[name] = ((p["published"], p.get("published_at") or ""), p["url"])
            for t in tags:
                cr_tagcount.setdefault(name, {}).setdefault(t, 0)
                cr_tagcount[name][t] += 1
                beat_creators.setdefault(t, set()).add(name)
                beat_cr_pieces.setdefault(t, {}).setdefault(name, 0)
                beat_cr_pieces[t][name] += 1

    # display beats: the FIELD_BEATS main beats with the most creators (pieces, then name, break ties)
    display = sorted(main, key=lambda t: (-len(beat_creators[t]), -pc[t], t))[:FIELD_BEATS]
    disp_ix = {t: i for i, t in enumerate(display)}
    # canonical order for placing a creator: displayed beats first (largest first), then every other tag by creators
    rank = lambda t: (disp_ix.get(t, FIELD_BEATS), -len(beat_creators.get(t, ())), t)

    circles = []
    for name in sorted(cr_pieces, key=lambda n: (-cr_pieces[n], n)):
        tc = cr_tagcount.get(name) or {}
        prim = min(tc, key=lambda t: (-tc[t], rank(t))) if tc else None   # all tags tie (tags are per creator); rank decides
        circles.append({"n": name, "p": cr_pieces[name], "b": disp_ix.get(prim, -1)})

    link_for = lambda n: links.get(n) or (cr_latest.get(n) or (None, ""))[1]
    beats = []
    for t in display:
        top = [[n, k, link_for(n)] for n, k in sorted(beat_cr_pieces[t].items(), key=lambda x: (-x[1], x[0]))[:TOP_CREATORS]]
        beats.append({"label": t, "slug": slug(t), "creators": len(beat_creators[t]), "pieces": pc[t], "top_creators": top})

    # Every beat not displayed, largest first. Each links to its corner view on the page.
    more_tags = sorted((t for t in pc if t not in disp_ix), key=lambda t: (-len(beat_creators[t]), -pc[t], t))
    placed = sum(1 for c in circles if c["b"] == -1)
    return {
        "window": {"from": w_from, "to": w_to},
        "totals": {"creators": len(cr_pieces), "pieces": len(pieces), "beats": len(pc)},
        "min": {"pieces": MIN_PIECES, "creators": MIN_CREATORS},
        "main": main,
        "beats": beats,
        "more": {"creators": placed, "beat_count": len(more_tags), "beats": [[t, len(beat_creators[t]), pc[t]] for t in more_tags]},
        "circles": circles,
    }


def compute_from_repo(root=ROOT):
    latest = load_issue(root)
    w_from, w_to = latest["week_start"], latest["week_end"]
    return compute(load_window_pieces(root, w_from, w_to), load_registry_tag_counts(root), w_from, w_to, load_registry_links(root))


if __name__ == "__main__":
    r = compute_from_repo()
    print(r["window"], r["totals"], f'{len(r["main"])} main beats (Lens); the field shows {len(r["beats"])} + "{r["more"]["beat_count"]} more beats"')
    for b in r["beats"]:
        print(f'  {b["label"]:28s} {b["creators"]:4d} creators {b["pieces"]:5d} pieces  placed {sum(1 for c in r["circles"] if c["b"] == r["beats"].index(b))}')
    print("  more beats:", r["more"]["creators"], "creators placed")
