#!/usr/bin/env python3
"""Build assets/data/lens-index.json, the compact index behind the /for-brands Issue Lens.

Run after every Pulse update (the Pulse pipeline rewrites assets/data/pulse/posts-*.json and
data/pulse-issues.json) and after `node convert.js`, then commit the result:

    python3 scripts/build_lens_index.py

Inputs (all already in the repo):
  assets/data/pulse/posts-YYYY-Wnn.json   per-week pieces (already canonical: one record per URL, co-hosts in `co`,
                                          harvested social/Bluesky posts excluded by the Pulse build)
  data/pulse-issues.json                  latest issue -> the masthead window (week_start..week_end)
  assets/data/creators-data.json          the registry (beat tags, home base)
  assets/data/site-stats.json             verified count and as-of date
  config/lens_featured_issues.json        hand-edited issue chips; each is dropped if under min_pieces matches this week
  for-brands.html                         (rewrites the chip list between the LENS:CHIPS markers)
  pulse.html                              feeds monitored (total_rss_resolved), so the page never types it

Nothing here is model-written. The index holds only what the Lens may show: piece title, link, date, creator
NAME, format, beat tags and a home-base label. No contact details, no follower counts.
"""
import json, re, sys, html, unicodedata, argparse, urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import main_beats   # the shared main-beat list (also read by the Pulse build)

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets/data/lens-index.json"

SOCIAL_HOSTS = {"bsky.app", "x.com", "twitter.com", "instagram.com", "facebook.com", "threads.net", "threads.com",
                "tiktok.com", "linkedin.com", "mastodon.social", "t.me"}   # mirrors pulse_canonical.SOCIAL_HOSTS
VIDEO_HOSTS = {"youtube.com", "youtu.be", "vimeo.com", "twitch.tv", "rumble.com", "noosphere.tv"}
PODCAST_HOSTS = {"podcasts.apple.com", "open.spotify.com", "spotify.com", "megaphone.fm", "simplecast.com", "libsyn.com",
                 "buzzsprout.com", "transistor.fm", "podbean.com", "omny.fm", "acast.com", "art19.com", "anchor.fm",
                 "soundcloud.com", "overcast.fm", "pca.st"}
NEWSLETTER_SUFFIX = ("substack.com", "beehiiv.com", "ghost.io", "buttondown.email", "buttondown.com", "kit.com", "mailchi.mp")
FORMATS = ["newsletter", "video", "podcast", "web"]   # index = code used in the file


def host_of(url):
    h = urllib.parse.urlparse(url or "").netloc.lower()
    return h[4:] if h.startswith("www.") else h


def fmt_code(url, creator_platform):
    """Format from the URL host first; custom-domain newsletters fall back to the creator's platform label."""
    h = host_of(url)
    if h in VIDEO_HOSTS or any(h.endswith("." + x) for x in VIDEO_HOSTS):
        return 1
    if h in PODCAST_HOSTS or any(h.endswith("." + x) for x in PODCAST_HOSTS):
        return 2
    if h.endswith(NEWSLETTER_SUFFIX):
        return 0
    lab = (creator_platform or "").lower()
    if lab.startswith("newsletter"):
        return 0
    if lab.startswith("podcast"):
        return 2
    if lab.startswith("video"):
        return 1
    return 3


def split_tags(raw):
    return [t.strip() for t in (raw or "").split(",") if t.strip()]


def norm(name):
    return re.sub(r"\s+", " ", (name or "").strip().lower())


# ── Title matcher. MUST stay identical to matcher()/tokens() in for-brands.html (the page and the chip gate use one rule). ──
# Whole-word only. Tokens of 3 letters or fewer are case-sensitive ("AI" and "Fed" do not hit "said" or "fed up"); a short
# token typed all lowercase matches its Capitalized or UPPER form, never the lowercase word. Longer tokens match
# case-insensitively, as whole words with an optional plural ("center" finds "centers", never "centered" or "datacenter").
STOP = {"the", "a", "an", "of", "and", "in", "on", "for", "to", "is", "are", "vs"}


def strip_marks(s):
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))


def raw_tokens(q):
    return [t for t in re.split(r"[^A-Za-z0-9]+", strip_marks(q)) if t and t.lower() not in STOP]


def compile_token(t):
    if len(t) <= 3:
        forms = [t] if re.search(r"[A-Z]", t) else [t[:1].upper() + t[1:].lower(), t.upper()]
        forms = list(dict.fromkeys(forms))
        return re.compile(r"(^|[^A-Za-z0-9])(?:" + "|".join(re.escape(f) for f in forms) + r")($|[^A-Za-z0-9])"), False
    base = t.lower()
    if base.endswith("s") and not base.endswith("ss"):
        base = base[:-1]
    return re.compile(r"(^|[^a-z0-9])" + re.escape(base) + r"(?:s|es)?($|[^a-z0-9])"), True


def title_hits(query, titles):
    """Indexes of titles matching every token of the query."""
    toks = [compile_token(t) for t in raw_tokens(query)]
    if not toks:
        return []
    out = []
    for i, title in enumerate(titles):
        nc = strip_marks(title); n = nc.lower()
        if all(rx.search(n if lower else nc) for rx, lower in toks):
            out.append(i)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--dry-run', action='store_true', help='report only; write nothing')
    args = ap.parse_args()
    issues = json.loads((ROOT / "data/pulse-issues.json").read_text())
    latest = issues["issues"][sorted(issues["issues"])[-1]]
    w_from, w_to, through = latest["week_start"], latest["week_end"], latest["data_through"]

    creators = json.loads((ROOT / "assets/data/creators-data.json").read_text())
    stats = json.loads((ROOT / "assets/data/site-stats.json").read_text())
    by_name = {norm(c["name"]): i for i, c in enumerate(creators)}

    # beat tags -> creator ids (exact, comma-split, same rule as Pulse)
    tag_ids = {}
    for i, c in enumerate(creators):
        for t in split_tags(c.get("topic")):
            tag_ids.setdefault(t, []).append(i)
    tags = sorted(tag_ids, key=lambda t: (-len(tag_ids[t]), t))
    tag_ix = {t: i for i, t in enumerate(tags)}

    def place_of(cid, post_geo=None):
        if cid is not None:
            c = creators[cid]
            if c.get("geoCity") and c.get("geoState"):
                return f'{c["geoCity"]}, {c["geoState"]}'
        g = re.sub(r"\s*-\s*US$", "", (post_geo or "").strip())   # "Oregon - US" -> "Oregon"
        if g and not g.lower().startswith("national"):
            return g
        return ""

    posts = []
    for f in sorted((ROOT / "assets/data/pulse").glob("posts-*.json")):
        posts += json.loads(f.read_text())["posts"]

    places, place_ix = [], {}
    cr_names, cr_ix = [], {}

    def creator_ix(name, post_geo=None):
        key = norm(name)
        if key in cr_ix:
            return cr_ix[key]
        cid = by_name.get(key)
        p = place_of(cid, post_geo)
        if p and p not in place_ix:
            place_ix[p] = len(places); places.append(p)
        cr_ix[key] = len(cr_names)
        cr_names.append([name, place_ix.get(p, -1), cid if cid is not None else -1])
        return cr_ix[key]

    seen, pieces, dropped = set(), [], {"social": 0, "outside_window": 0, "no_title_or_url": 0, "dup": 0, "unregistered": 0}
    for p in posts:
        if not (w_from <= p["published"] <= w_to):
            dropped["outside_window"] += 1; continue
        url = p.get("url") or ""
        title = html.unescape((p.get("title") or "").strip())
        if not url or not title or title.lower() == "no title":
            dropped["no_title_or_url"] += 1; continue
        if host_of(url) in SOCIAL_HOSTS:
            dropped["social"] += 1; continue
        if url in seen:
            dropped["dup"] += 1; continue
        seen.add(url)
        names = [p["creator"]] + list(p.get("co") or [])
        cix = [creator_ix(n, p.get("geography") if n == p["creator"] else None) for n in names]
        tg = sorted({tag_ix[t] for t in split_tags(p.get("topic")) if t in tag_ix})
        day = (int(p["published"][8:10]) - int(w_from[8:10])) if p["published"][:7] == w_from[:7] else \
              (int(p["published"][8:10]) + 31 - int(w_from[8:10]))
        pieces.append([title, cix, url, day, fmt_code(url, p.get("platform")), tg])

    pieces.sort(key=lambda x: (-x[3], x[0]))

    # chips: featured issues first (hand-picked, each must clear min_pieces), then the most-covered beats; 8 total
    cfg = json.loads((ROOT / "config/lens_featured_issues.json").read_text())
    min_pieces = int(cfg.get("min_pieces", 5))
    titles = [p[0] for p in pieces]
    chip_labels, featured_log = [], []
    for phrase in cfg.get("issues", []):
        n_hit = len(title_hits(phrase, titles))
        featured_log.append((phrase, n_hit, n_hit >= min_pieces))
        if n_hit >= min_pieces:
            chip_labels.append(phrase)
    # beat chips: the shared main-beat list (scripts/main_beats.py: >= 40 pieces this week, >= 25 registry creators), most-covered first
    main_labels, _pc = main_beats.main_beat_labels(main_beats.load_window_pieces(ROOT, w_from, w_to), main_beats.load_registry_tag_counts(ROOT))
    for t in main_labels:
        if len(chip_labels) >= 8:
            break
        if t.lower() not in [c.lower() for c in chip_labels]:
            chip_labels.append(t)
    chip_labels = chip_labels[:8]

    feeds = None
    m = re.search(r'"total_rss_resolved":\s*(\d+)', (ROOT / "pulse.html").read_text())
    if m:
        feeds = int(m.group(1))

    out = {
        "v": 1, "from": w_from, "to": w_to, "through": through,
        "creators_total": stats["totalCreators"], "as_of": stats["asOf"], "feeds": feeds,
        "formats": FORMATS, "tags": tags, "tag_ids": [tag_ids[t] for t in tags],
        "places": places, "creators": cr_names, "pieces": pieces,
    }
    blob = json.dumps(out, ensure_ascii=False, separators=(",", ":")).encode()
    if not args.dry_run:
        OUT.write_bytes(blob)
    import gzip
    size, gz = len(blob), len(gzip.compress(blob))
    print(f"{'would write' if args.dry_run else 'wrote'} {OUT.relative_to(ROOT)}: {len(pieces)} pieces, {len(cr_names)} creators, {len(tags)} tags, "
          f"{size/1024:.0f} KB raw, {gz/1024:.0f} KB gzip; window {w_from}..{w_to}, data through {through}, feeds {feeds}")
    # Bake this week's chips and the data-through date into for-brands.html (static, so view-source shows them)
    page = ROOT / "for-brands.html"
    html_src = page.read_text()
    items = "\n".join(f'          <li><button type="button" class="chip">{html.escape(c)}</button></li>' for c in chip_labels)
    new_src = re.sub(r"(<!-- LENS:CHIPS -->).*?(<!-- /LENS:CHIPS -->)", lambda m: f"{m.group(1)}\n{items}\n          {m.group(2)}", html_src, flags=re.S)
    new_src = re.sub(r'(<template id="lens-tpl" data-through=")[^"]*(")', lambda m: f"{m.group(1)}{through}{m.group(2)}", new_src)
    if new_src != html_src and not args.dry_run:
        page.write_text(new_src)
    print("chips:", chip_labels)
    for phrase, n_hit, ok in featured_log:
        print(f"  featured {phrase!r}: {n_hit} matching pieces -> {'kept' if ok else 'DROPPED (under ' + str(min_pieces) + ')'}")
    print("dropped:", dropped)
    print("format mix:", {FORMATS[k]: sum(1 for p in pieces if p[4] == k) for k in range(4)})
    print("creators with a place:", sum(1 for c in cr_names if c[1] >= 0), "of", len(cr_names))


if __name__ == "__main__":
    sys.exit(main())
