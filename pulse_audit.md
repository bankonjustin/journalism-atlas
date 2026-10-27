# Pulse audit (Phase 0, no code changed)
Date: 2026-10-26. Source: `pulse.html` (repo copy matches live: same Oct 22 data, same masthead text, checked in the browser pane). Screens: `pulse_redesign_screens/phase-0/` (36 PNGs: 390/768/1440 x light/dark x default + 4 tab states + folds). Before-shots were taken from a local static server of the repo, because live returns a Cloudflare 403 to scripted clients.

## 1. Stack and data
- **Stack:** one static HTML file, 3,743 lines / 5.4 MB. Vanilla JS, no framework, no build step beyond `build-dist.sh` (copy allowlist, publishes `dist/`). Cloudflare Pages auto-deploy from GitHub main. **Any new route (`/pulse/beat/...`, `/pulse/archive`, feeds, embeds) must be added to `build-dist.sh` or it 404s live.**
- **Data arrival:** NOT fetched. `update_pulse.py` (in `journalism-atlas-private/pipelines/pulse/`) rewrites two inline JSON blocks in `pulse.html`: `#pulse-data` (line 1158, **5.2 MB**) and `#digest-data`. The page has zero `fetch()` calls. All rendering (masthead, stats, tabs, feed) is client-side from that blob.
- **Pipeline:** `pulse_v2.py` (scrape ~2,430 creators, ~10 min) -> `update_pulse.py` (writes pulse.html, index.html, for-brands.html) -> `pulse_digest.py` (Claude digest + a second Claude verification pass) -> brief and mining. Run locally via `spidering/core/refresh_pulse.sh`; Justin commits via GitHub Desktop. A weekly Routine spec exists (`PULSE-ROUTINE-SPEC-2026-10-05.md`) but is not registered.
- **Cadence today:** weekly by hand. Last data: 2026-10-22 (4 days old at audit time).
- **Beat taxonomy:** no `beats.json`. Beats are the creators' free-text `topic` strings from the master CSV; `canonicalizeBeat()` in the page folds them. `beat_activity` has 78 beats; the raw post `topic` field has **446 distinct strings** and 4,751 of 10,671 posts carry comma-joined multi-tags.
- **Creator database:** `assets/data/creators-master.csv` -> `convert.js` -> `creators-data.json` (2,432 in the blob; preflight confirms CSV = JSON). Per CLAUDE.md, never type a creator count: use the `{{CREATOR_COUNT}}` token / `site-stats.json`.
- **Weekly brief:** `pulse_digest_YYYYMMDD.json`, weekly since 2026-09-08 (6 files). It is LLM-generated and verified by a second LLM pass (health report 2026-10-05: 3 of 4 runs that day failed verification before the patch).

**Sample post record** (all 9 fields, all 10,671 posts have all keys):
```
{"creator":"Peter Zeihan","channel":"Zeihan on Geopolitics","title":"The Great Oil Split Has Begun",
 "url":"https://zeihan.com/the-great-oil-split-has-begun/","published":"2026-10-22",
 "summary":"<p>Global oil markets are beginning to fragment... &#8217;...</p>",
 "topic":"World","geography":"National - US","platform":"Website"}
```
Top-level blob keys: generated_at, preflight, window_days (30), total_creators 2,432, total_rss_resolved 1,756, total_posts 10,671, active_7d 984, active_30d 1,245, dark_creators (508), beat_activity (78), recency {24h, 7d, 30d}, cross_signal (**empty list**), feed_health, completeness, posts.

Digest keys: metadata, analysis.universal.trending_topics, statistics (incl. platforms), signal_stories (20; fields title/url/creator/platform/topic/published/signal_score/signal_reason), public_affairs_signals, field_summary, masthead, beat_trends (75 beats: current, baseline, trend, delta_pct).

## 2. What we can compute (and what we cannot)
**Computable now, from the blob:**
- Feeds monitored (1,756 RSS-resolved / 1,848 "confirmed" in feed_health; the two numbers differ, pick one definition), creators, active 7d/30d, dark creators.
- Posts per day for 30 days (Sep 22 to Oct 22), posts per beat (with multi-tag split), per platform, per creator, distinct posting creators (1,239).
- Day-of-week distribution (weekday vs weekend is clearly visible).
- Beat co-occurrence and lift (multi-tags on 45% of posts).
- Creator home geography per post (9,821 of 10,671 have a value; 850 blank; top: National-US 1,525, New York 1,361, DC 1,035, LA 424, Chicago 318). This is the creator's base, not where the story is about.
- Week-over-week beat deltas: `beat_trends` in the digest (current vs baseline), plus 6 weekly digest files for a short history.
- Poly-platform creators: derivable from `secondaryPlatforms` in `creators-data.json` (not in the post blob).

**NOT available:**
- **Time of day.** `published` is date-only (`YYYY-MM-DD`). `pulse_v2.py:1305` truncates it with `strftime("%Y-%m-%d")`; the feeds carry full timestamps, so this is recoverable but needs a pipeline change (Ryan/Justin's lane). **Consequence: the hourly Line (§4.2), the "6-9am" hover, and the day x hour heatmap (§5.5) cannot be built honestly today.** Daily resolution only, until the pipeline stores `published_at`.
- Avatars and post images: none in the data. Monograms only.
- "Converging stories" (several creators on the same story): the digest has `signal_reason: "cross-beat"` and the page's `cross_signal` array is empty. No story-clustering exists. This is new computation (or new LLM work) and needs a method note.
- First-seen date per creator, and posts older than 30 days: not in the blob (archives exist in the private repo: 17 `rss_pulse_v2_*.json` since June 5, but only aggregates verified).
- Story-level geography for the map; a map of creator bases is possible.
- Per-day dedup/backfill check: **daily volume climbs from ~220/day (Sep 22) to 870 (Oct 21)**. Corpus growth (feeds 1,693 -> 1,756, +35 newly discovered) and backfill probably explain part of it. Any "up X%" headline must be checked against fixed-cohort volume before we publish it.
- Inconsistent totals: blob `total_posts` 10,671 vs `recency.30d` 10,743 vs digest `total_posts` 10,743.
- Chicago: `data/chicago-pulse.json` is a 163-item feed from 55 sources (10 failed). The "76 creators / 245 outlets / 39 / 37" figures are not in it; they live in `city-lab-chicago.html` (CLAUDE.md says "245+"). Not verified by me.

## 3. Known issues, verified
| Claim in brief | Result |
|---|---|
| Masthead `PULSE · VOL. 1 · —` and `— feeds monitored` empty in HTML | **Confirmed.** pulse.html:976 and :1000. Filled by JS (`renderMasthead`, :3361). `VOL. 1` is hard-coded in JS with a `TODO-JUSTIN` comment (:975); there is no stored issue counter. |
| Material icon ligature names leak | **Mostly outdated.** All tab icons already have `aria-hidden="true"`. One miss: the search icon (`search`). Text leaks only if the icon font fails or for no-JS/crawlers. Still worth replacing with inline SVG. |
| "Updated weekly" vs "Today's Pulse" | **Confirmed** (:1000, :1052). Feed rows also say "today" for posts dated Oct 22 while the page is 4 days old, so the label is not trustworthy. |
| Audience CTAs above content; brief buried in a tab; City Lab at bottom; "Load 50 more" with no total | Confirmed from source order and screenshots (digest/intel is the default tab, `data-tab="intel"`). |
| Tabs a11y | `role=tablist`/`tab` present, but **no `aria-selected`, no `tabpanel`**, no arrow-key handling checked, no URL state. The tab descriptor for "overlap" says "Geographic distribution", but the tab is the co-occurrence matrix. |
| URL state | `URLSearchParams` appears in the JS but tab clicks do not change the URL; no shareable filters. |
| Meta/SEO | `<title>`, canonical, OG, Twitter present. **No `<meta name=description>`**, no JSON-LD, no `<h1>`, no `<main>` landmark. OG image is a static logo, not data-driven. |
| Motion/theme | No `prefers-reduced-motion` rule; **no `prefers-color-scheme` or dark mode** in pulse.html or variables.css (so "full dark mode" is a new build). Focus rules exist. |
| Responsive | 390/768/1440: no horizontal page scroll, no console errors. |

**Lighthouse (local static server, mobile defaults):** Performance 55, Accessibility 92, Best Practices 100, SEO 92. CLS 0, TBT 0. Fails: color-contrast, `landmark-one-main`, `link-in-text-block`, `meta-description`. The 33 s FCP/LCP is inflated (uncompressed python server + simulated throttle); the real signal is **6.3 MB transferred**, driven by the 5.2 MB inline blob that every visitor downloads, parses and which delays first paint. Cloudflare compression will shrink it but not the parse cost. Re-run against live in a real browser before the "after" comparison.

## 4. Design tokens actually in use (CONFLICT with the brief)
From `assets/css/variables.css`, `CLAUDE.md` and `pulse.html` (v15 token system):
- **Fonts in use:** Inter (UI/body), DM Mono (Pulse's labels, 59 uses; header.css still imports JetBrains Mono), `--font-editorial` Merriweather (reactivated Sept 2026), Source Code Pro 500 is the v15 label face (not yet used on Pulse). **Space Mono, Playfair Display and DM Sans appear nowhere in the repo.**
- **Color:** Neutral grays `#ffffff #efefef #c6c6c6 #909090 #5e5e5e #303030 #121212 #000000`; Acid `#ceff00` (fills on light, anything on dark), Lime `#97d600` (focus on dark), Dark Olive `#5d7400` (text/links/focus on light). Error `#f50000`. Viz: `ATLAS_VIZ_COLORS.md` (9 confirmed categories live-safe; acid excluded from category colors). **No orange brand accent exists**; closest are `--viz-orange #ffaa00` and `--color-display-dark #ffbc00`.
- **Rules that collide with the brief:** green = interaction only; "no color coding by section or content type"; v15 labels are deliberate Source Code Pro caps with a trailing ` →` instruction link (the brief wants both killed); Cool grays for charts only; 6px radius, pills retired; weights 400-700; 4px spacing; body >= 16px; widths 1440/1200/680.
- Current Pulse look: black `#111` masthead, acid highlights, DM Mono 10px labels (below the 12px floor).

## 5. Top five recommendations (priority order)
1. **Resolve brand conflicts before any pixels (Decisions 1-2).** The brief's type (Space Mono/Playfair/DM Sans), orange "live" accent and anti-caps-eyebrow stance contradict v15 and James's signed system. I recommend building the redesign in v15 (Inter, Merriweather for editorial voice, Source Code Pro for the instrument layer, Acid on dark for "live/now") and taking only the ideas: one display voice, one data voice, links that say what they do.
2. **Fix the data/rendering foundation first.** Server-render masthead numbers at build (`update_pulse.py`), stop shipping 5.2 MB inline to render a summary: bake the small summary into HTML and move posts to a separate `assets/data/pulse-posts.json` fetched after paint (add to `build-dist.sh`). This also fixes the no-JS dashes, link previews, and Lighthouse.
3. **Add `published_at` (ISO with time) to the pipeline** (one line at `pulse_v2.py:1305`), starting now so hourly data accrues. Until ~2-4 weeks accumulate, The Line ships at daily resolution and the rhythm heatmap is day-of-week only. Needs your OK because it touches the pipeline.
4. **Establish the issue/cadence model and a stored issue counter** (weekly frozen issue + live feed; archive back-fill from the weekly digests since Sep 8). This unlocks the masthead, archive, RSS and OG-per-issue. Today there is nothing to compute "No. n" from.
5. **Promote the digest to the editorial lead, but honestly.** Provenance line + method link for the LLM synthesis; compute "converging stories" deterministically (or flag it as new work) since `cross_signal` is empty; sanity-check week-over-week claims against the daily-volume ramp (220 -> 870/day) and the 10,671 vs 10,743 mismatch before they appear in a headline.

## 6. Other blockers and questions
- **Form/intake backend:** nothing confirmed. I did not find an endpoint in the repo; per the brief I will not improvise. Need your answer (Decision 3).
- Page is a hand-edited template with data injected by `update_pulse.py`; Phase 1 template edits live in pulse.html and must keep the injection markers (`#pulse-data`, `#digest-data`) intact.
- Working tree already has unrelated changes (`_headers` modified, `preview/nn-launch-kit/explorer-named/` untracked). I won't touch them.
- `pulse_redesign_screens/` and these md files are new untracked files at repo root; `build-dist.sh` default-deny keeps them off the public site.
