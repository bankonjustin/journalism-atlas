#!/usr/bin/env python3
"""The shared "main beats" list and this week's per-beat figures. One module, read by both builds:

  scripts/build_lens_index.py   (the /for-brands Issue Lens: chips)
  journalism-atlas-private/pipelines/pulse/update_pulse.py   (the /pulse field: clusters, panels, hidden table)

Rules (one place, so the two pages cannot disagree):
  * Counting is ANY-TAG and EXACT-TAG: a piece counts under every beat tag it carries (comma-split, no folding).
    Creators include co-hosts, because a co-hosted piece counts for each host.
  * A beat is a MAIN beat when it has at least MIN_PIECES pieces in the issue window and at least MIN_CREATORS creators
    in the registry carrying the tag (the Lens rule, unchanged). Main beats are ordered by pieces this week, then name.
  * Primary beat (used ONLY to place a creator's circle in the field): the tag on most of that creator's pieces this week;
    ties go to the earlier beat in the canonical order (main beats first, in the order above; then other tags by pieces).
    A creator whose primary beat is not a main beat sits in the "Other beats" cluster.
  * Printed figures never use the primary assignment. The field's cluster labels and panels are any-tag.

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


def compute(pieces, tag_creators, w_from, w_to, signal_stories=()):
    """Everything the field needs. `pieces` are already filtered to the window (one record per URL)."""
    main, pc = main_beat_labels(pieces, tag_creators)
    main_ix = {t: i for i, t in enumerate(main)}
    rank = lambda t: (main_ix.get(t, len(main)), -pc.get(t, 0), t)   # canonical order for tie-breaks

    cr_pieces, cr_tagcount = {}, {}
    beat_creators, beat_cr_pieces = {}, {}
    for p in pieces:
        tags = sorted(set(split_tags(p.get("topic"))))
        for name in [p["creator"], *(p.get("co") or [])]:
            cr_pieces[name] = cr_pieces.get(name, 0) + 1
            for t in tags:
                cr_tagcount.setdefault(name, {}).setdefault(t, 0)
                cr_tagcount[name][t] += 1
                beat_creators.setdefault(t, set()).add(name)
                beat_cr_pieces.setdefault(t, {}).setdefault(name, 0)
                beat_cr_pieces[t][name] += 1

    # circles: one per creator, placed by primary beat (layout only)
    circles = []
    for name in sorted(cr_pieces, key=lambda n: (-cr_pieces[n], n)):
        tc = cr_tagcount.get(name) or {}
        prim = min(tc, key=lambda t: (-tc[t], rank(t))) if tc else None
        circles.append({"n": name, "p": cr_pieces[name], "b": main_ix.get(prim, -1)})

    # top piece per beat: highest-scored digest signal story carrying the tag (labelled "signal"), else the most recent piece
    stories = sorted((s for s in signal_stories if w_from <= (s.get("published") or "") <= w_to),
                     key=lambda s: -(s.get("signal_score") or 0))
    beats = []
    for t in main:
        top = [[n, k] for n, k in sorted(beat_cr_pieces[t].items(), key=lambda x: (-x[1], x[0]))[:TOP_CREATORS]]
        s = next((s for s in stories if t in split_tags(s.get("topic"))), None)
        if s:
            tp = {"title": s["title"], "url": s["url"], "creator": s["creator"], "date": s["published"], "basis": "signal"}
        else:
            q = max((p for p in pieces if t in split_tags(p.get("topic"))), key=lambda p: (p["published"], p.get("published_at") or "", p["title"]))
            tp = {"title": q["title"], "url": q["url"], "creator": q["creator"], "date": q["published"], "basis": "latest"}
        beats.append({"label": t, "slug": slug(t), "creators": len(beat_creators[t]), "pieces": pc[t], "top_creators": top, "top_piece": tp})

    others = [c for c in circles if c["b"] == -1]
    other_tags = sorted((t for t in pc if t not in main_ix), key=lambda t: (-pc[t], t))
    return {
        "window": {"from": w_from, "to": w_to},
        "totals": {"creators": len(cr_pieces), "pieces": len(pieces), "beats": len(pc)},
        "min": {"pieces": MIN_PIECES, "creators": MIN_CREATORS},
        "main": main,
        "beats": beats,
        "other": {"creators": len(others), "top_creators": [[c["n"], c["p"]] for c in others[:TOP_CREATORS]],
                  "beats": [[t, pc[t], len(beat_creators[t])] for t in other_tags[:6]], "beat_count": len(other_tags)},
        "circles": circles,
    }


def compute_from_repo(root=ROOT, signal_stories=()):
    latest = load_issue(root)
    w_from, w_to = latest["week_start"], latest["week_end"]
    return compute(load_window_pieces(root, w_from, w_to), load_registry_tag_counts(root), w_from, w_to, signal_stories)


if __name__ == "__main__":
    r = compute_from_repo()
    print(r["window"], r["totals"])
    for b in r["beats"]:
        print(f'  {b["label"]:28s} {b["creators"]:4d} creators {b["pieces"]:5d} pieces')
    print("  other:", r["other"]["creators"], "creators placed;", r["other"]["beat_count"], "other tags")
    print("  placed per main beat:", [sum(1 for c in r["circles"] if c["b"] == i) for i in range(len(r["main"]))])
