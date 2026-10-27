# Pulse redesign ledger

## Phase 0: Audit (2026-10-26)
**Changed:** nothing in the site. No commits, no pushes.
**Files created:** `pulse_audit.md`, `pulse_redesign_ledger.md`, `pulse_redesign_screens/phase-0/` (36 PNGs: `full-{390,768,1440}-{light,dark}-default.png`, `-tab-{intel,activity,rhythm,overlap}.png`, `fold-*.png`).
**Open issues:** see audit §2, §3, §6. Headline: no time-of-day data; brief's fonts/accent conflict with v15; no dark mode today; no intake backend confirmed; inline 5.2 MB blob.
**Not done / caveats:** Lighthouse ran locally (live is behind a bot challenge); light vs dark screenshots are visually the same because Pulse has no dark styles; Chicago 76/245 figures not verified; story-geography and creator first-seen data not checked.

### Decisions for Justin
1. Fonts: brief says Space Mono / Playfair / DM Sans; repo (v15) says Inter / Merriweather / Source Code Pro (DM Mono on Pulse today). Recommend v15.
2. Orange "live" accent vs v15 (green = interaction, no orange token). Recommend Acid on dark as the single "live" color. Also: kill caps eyebrows and `->` (brief) vs v15 label/instruction-link spec (James).
3. Cadence model (weekly publication + live feed, recommended), intake destination, analytics tool.
4. OK to add `published_at` to `pulse_v2.py` (unlocks hourly Line and heatmap)? Until then daily only.
5. OK to move posts out of the inline blob into a fetched JSON (and add to `build-dist.sh`)?
6. Public creator count: use the generated `{{CREATOR_COUNT}}` token (CLAUDE.md); confirm whether the database figure is public.
7. Converging stories: new computation/LLM step, or leave out until a method exists?
8. Nodes and Networks module: feature flag off by default, wording yours (unchanged from brief).
9. City Lab tallies public? James review after Phase 2? Final voice pass.

---

## Phase 1: fixes, data foundation, re-sequence (2026-10-26/27)
Nothing committed or pushed. Scraper NOT re-run (10 min, hits ~2,400 sites, mutates feed_cache); the page was rebuilt from the existing `rss_pulse_v2_20261022.json`.

### Files touched
Public repo (`journalism-atlas`): `pulse.html` (restructured, see below), `build-dist.sh` (+1 line: copies `assets/data/pulse`), NEW `assets/data/pulse/posts-2026-W39..W43.json`, NEW `data/pulse-issues.json` (issue counter, not published), NEW `pulse_audit.md`, this ledger, `pulse_redesign_screens/`. `index.html` and `for-brands.html` untouched (run used `--pulse-only`). Your pre-existing `_headers` edit and `preview/nn-launch-kit/explorer-named/` are untouched.
Private repo (`journalism-atlas-private/pipelines/pulse/`): `pulse_v2.py` (+`published_at`, +`generated_at_iso`, UTC fix), `update_pulse.py` (new build step, `--pulse-only`), NEW `prototypes/convergence_proto.py`.

### Decision 4: 10,671 vs 10,743, reconciled (not auto-resolved: please confirm)
- **Cause.** Commit `96c265b` (Oct 26, "remove 13 rejected") hand-edited the page blob: it deleted 72 posts from six rejected creators (D.J. Byrnes 24, Kyle Kulinski 15, Michael Shellenberger 14, Briahna Joy Gray 10, Phillip Lewis 5, Dennis Lee 4) and 3 dark creators, and updated `total_posts` to 10,671, but left every other stored aggregate (`recency.30d` 10,743, `active_30d` 1,245, `total_rss_resolved` 1,756, `beat_activity`) and the whole digest computed from the 10,743. The scraper file `rss_pulse_v2_20261022.json` still has all 10,743. So the two numbers were never two measurements; one was a hand-patched copy.
- **What I built.** `update_pulse.py` now derives every number from one filtered list: drop creators not in `creators-data.json` (the registry), then keep only "public posts" (the feed's own rule: not a harvested social post, has a title and URL). Nothing rendered is copied from a stored aggregate.
- **Waterfall:** 10,743 source rows -> 10,671 after registry (72 rows, 6 creators) -> **9,394 canonical public posts** (328 social-platform rows, 932 items the scraper titled "No title", 17 with no URL). Distinct URLs: 8,966 (428 surplus rows share a URL with another creator row, mostly co-hosted shows listed per host). Feeds monitored: 1,756 -> 1,747. Creators with public posts: 1,132 (was 1,245).
- **Why I went further than 10,671:** the masthead said 3,835 "posts" while the feed's "Last 7 days" showed 3,283, because the feed already hid social/untitled rows. One definition now: masthead 3,283, feed 3,283.
- **Still wrong, not fixable here:** the LLM digest text (lede "1,314 posts across 205 creators", trending-topic descriptions, field summary) was written from the 10,743 raw rows including the six rejected creators (Kulinski, Gray, Shellenberger are all Politics). It needs a re-run of `pulse_digest.py` with the filtered data; I did not touch it.
- **Open:** the 932 "No title" items (8.7% of rows) are real feed items the scraper failed to title. A title fallback in `pulse_v2.py` would recover them. Your call.

### Decision 3: the cohort, and how the curve looks under each definition
Window = last complete day (Oct 21; the Oct 22 scrape day is partial) and the 4 seven-day periods before it (Sep 24 to Oct 21). Public-post basis.

| Definition | Feeds | Wk1 (Sep 24-30) | Wk2 | Wk3 | Wk4 (Oct 15-21) | Last wk vs prior |
|---|---|---|---|---|---|---|
| All monitored feeds (raw) | 1,118 posting | 1,472 | 1,768 | 2,204 | 3,283 | **+49%** |
| Cohort A: a post in each of the 4 weeks (your rule) | **494** | 1,158 | 1,250 | 1,219 | 1,243 | **+2%** |
| Sensitivity: a post in first and last week only | 596 | 1,286 | 1,312 | 1,267 | 1,388 | +10% |

**The raw ramp is a measurement artifact.** RSS depth is capped per feed: of 301 feeds with 15+ posts, 126 have their earliest post after Oct 5, and the counts cluster at exactly 15 (68 feeds, the YouTube Atom cap) and 20 (34 feeds). A prolific feed cannot see back to the start of the window, so older days are undercounted and the curve climbs toward today. Cohort A removes this by construction (a post in the oldest week proves the feed reaches that far) and is flat. Recommendation: **keep your rule as is.** Its cost is a bias toward weekly-or-faster publishers (monthly newsletters and "went quiet" feeds cannot be in it), so "up/down X%" means "among consistent publishers", which is what the copy now says. I would add a separate, plainly labeled count of feeds that dropped out/joined rather than loosen the rule.
- Where cohort numbers appear now: masthead sentence ("Among the 494 feeds that published in every one of the last four weeks, volume was up 2%...") and the Beat momentum list (replaces the digest's raw `beat_trends`; beats with under 15 cohort posts the week before are omitted). Daily raw and cohort series are stored in the page summary (`cohort.daily`) for the Phase 2 Line. Raw totals appear only labeled "all monitored feeds".

### Decision 6: convergence prototype (`prototypes/convergence_proto.py`; build is Phase 3)
Week Oct 15-21, 3,283 public posts / 3,092 distinct URLs.
- **Same URL across 2+ creators: 153 groups, but only 5 span different channels.** The rest are one outlet listed under several creators (a three-host newsletter, a three-host YouTube channel, a podcast with three names). That is double counting, not convergence, and it also inflates "posts published" by about 4% (428 rows).
- **Shared outbound link: 0.** Summaries are truncated at 300 chars; only about 6% carry any link and none is shared.
- **Title similarity across distinct channels, domains and URLs: 7 clusters**, about 4 real (White House press secretary x3, No Kings x2, France protests x2, a cross-posted election analysis x2), 3 false (recurring "The Week Ahead" formats; two unrelated "doesn't work" titles).
- **Conclusion:** same-URL and title rules are too sparse to be the "Nuzzel" feature. The honest deterministic route is to **store outbound links from each entry's full content at scrape time** (feedparser `content`), then converge on shared links across distinct channels. I'd start accruing that in `pulse_v2.py` now. Needs your OK; not done.

### Decision 5: scope items
- **`published_at`** (ISO 8601, UTC `+00:00`) and `generated_at_iso` added in `pulse_v2.py`; also fixed a latent bug (tz-aware date strings kept the local wall clock instead of converting to UTC). Tested on a fixture; **no real data has it yet.** Midnight-UTC values likely mean "date only" in the feed. Line stays daily and Rhythm day-of-week until 4 weeks accrue (about Nov 23 if the next run is Oct 26). Note `published` (the date) is the UTC date, not Eastern.
- **Masthead server-rendered** between `<!-- PULSE:MASTHEAD -->` markers by `update_pulse.py`: "Pulse · Vol. 1, No. 7 · Week of Oct 15, 2026 · Data through Thu Oct 22, 2026", an h1, the numbers sentence, feeds monitored. A viewer's clock adds "(5 days ago)", and "the weekly run is overdue" in amber at 8+ days. `<title>`, description and OG/Twitter tags are generated the same way.
- **Issue counter.** `data/pulse-issues.json`: Issue = ISO weeks since seed week 2026-W37 (first weekly digest) + 1, keyed by the week of the last complete day, so a mid-week re-run refreshes the issue instead of burning a number. Oct 22 data = **No. 7**. Seed is yours to change.
- **Blob split.** `pulse.html` 5.40 MB -> **176 KB** (43 KB gzip). Posts in 5 weekly files, 3.2 MB raw / **813 KB gzip** total, fetched in parallel, cached by `?v=` data date. HTML+posts gzip: 1,618 KB -> ~856 KB (-47%). Dropped from the page payload because unused: post `summary` (re-add as a short `excerpt` for the Phase 3 feed) and the 508-row `dark_creators` list (count kept). `build-dist.sh` copies the folder; `sh build-dist.sh` ran clean.
- **Relative dates -> absolute** ("Thu Oct 22"); no build-time "today" remains.
- **Fixes:** h1, `<main>`, meta description, OG tags, instrument tabs with full ARIA (tablist/tab/tabpanel, aria-selected, aria-controls, roving tabindex, arrows/Home/End), signal-story tabs get arrows/roving tabindex, search icon is an inline SVG (no ligature text) and the input has a label, overlap tab renamed "Overlap" with a correct descriptor (it said "Geographic distribution"; also removed the duplicate line). URL state: `?beat=climate-environment,local&recency=7d&q=name&view=rhythm`; old `?beat=Politics` links still work; two beats = posts tagged with both. Verified in Playwright: arrow keys, deep links, two-beat filter, search restore.
- **Caps and arrows removed on Pulse only:** all `text-transform: uppercase` rules in pulse.html, `.link-instruction` overridden inside `<main>` only, ` →` removed from Pulse links, JS caps strings lowercased. Site header's "READ THE ESSAY →" banner and `components.css` are site-wide v15 and untouched (flag: James/you).
- **Re-sequenced:** masthead, (Line slot, Phase 2), What moved (signal stories + weekly brief promoted out of the Intel tab), The feed, The instruments (Activity, Rhythm, Overlap, For teams), City Lab, How Pulse works, Work with us. Audience CTAs moved to the bottom with existing copy (rewrite is Phase 4). "Updated weekly / Today's Pulse" replaced by one cadence statement.
- **Not done (as scoped):** dark mode, reduced motion, The Line, Follow rails, any intake form.

### Before / after (local static server, mobile Lighthouse defaults; real compression not applied)
| | Before | After |
|---|---|---|
| Performance / A11y / Best Practices / SEO | 55 / 92 / 100 / 92 | 53 / 90 / 100 / **100** |
| FCP | 33.0 s | **3.0 s** |
| LCP | 34.4 s | 22.5 s (waits on 3.2 MB uncompressed posts; ~0.8 MB gzipped live) |
| CLS | 0 | 0.004 (needed a reserved masthead height; first try was 0.46) |
| Page weight | 6,346 KiB | 4,052 KiB uncompressed |
| Failing audits | contrast, main landmark, link-in-text-block, meta description | contrast, link-in-text-block, **target-size (new)** |
Screenshots: `pulse_redesign_screens/phase-1/` (390/768/1440 light: full, fold, rhythm and overlap tabs, filtered feed). No horizontal scroll at 360/390/768/1024/1440. Dark not captured: no dark styles until Phase 2.

### Critique of my own screenshots (and the one thing I removed)
The masthead is still a wall: 12px dateline, a 14px "Atlas Pulse" h1 that reads like a caption, then a very large LLM paragraph. That is Phase 2's job. The weekly brief section is dense text with no hierarchy. Removed: the duplicated overlap descriptor line, and the now-meaningless stat-strip hookups.

### Open issues
1. LCP still depends on the posts download because the lede and beat map render after it. Fix: render digest-only parts before posts arrive (small change, Phase 2).
2. Digest prose is stale/raw (see Decision 4). `pulse_digest.py` should be fed the filtered data and cohort numbers.
3. `field_summary` is rendered with the byline "Justin Bank" (pulse.html, renderIntel) although it is machine-written. Not changed (editorial); the new provenance lines state it is machine-generated, which now contradicts the byline.
4. City Lab block still hard-codes "76 / 245 / 39 / 37" (CLAUDE.md: no typed counts); left as is.
5. Two windows exist: masthead "week" = last 7 complete days (Oct 15-21); feed "Last 24h" = Oct 21 only (complete days). They match numerically today (3,283), but "24h" is really "latest day".
6. Accessibility: target-size and contrast failures remain (small DM Mono labels, muted grey text).

### Decisions for Justin (new)
1. Approve the canonical definition (registry filter + public posts = 9,394) and the 932 untitled items: recover via title fallback?
2. Cohort A as primary (494 feeds); add "joined / dropped out" counts?
3. OK to store outbound links per entry in `pulse_v2.py` to enable real convergence?
4. Issue numbering seed (W37 = No. 1) and "Vol. 1".
5. Re-run the digest on filtered data before the next push? (The live lede currently cites rejected creators' volume.)
6. Remove the "Justin Bank" byline from the machine-written summary, or keep with a note?
7. Whether site-wide `link-instruction` caps/arrow (v15) should change to match Pulse (James).

---

## Phase 1b: ship-first items 1-7 (2026-10-27)
Nothing committed or pushed. Scraper not re-run. Digest WAS re-run (3 API calls, the first two blocked by the verification gate, details below).

### What to push
**Public repo (`journalism-atlas`, via GitHub Desktop):** `pulse.html`, `build-dist.sh`, `assets/data/pulse/` (5 files), `data/pulse-issues.json`; optional: `pulse_audit.md`, `pulse_redesign_ledger.md`, `pulse_redesign_screens/` (all stay off the public site, `build-dist.sh` is default-deny). Do not stage `.DS_Store`, `_headers` or `preview/nn-launch-kit/explorer-named/`: not mine.
**Private repo:** `pipelines/pulse/pulse_canonical.py` (new), `pulse_v2.py`, `update_pulse.py`, `pulse_digest.py`, `pulse_digest_20261022.json`, `previous_pulse_beats.json` (now canonical basis; the old raw one is saved as `previous_pulse_beats.rawbasis.json`), `prototypes/`, `atlas_run_log.jsonl`. Unrelated change not mine: `docs/nodes-and-networks-v5/launch-kit/PROOF-SHEET.md`.

### 1. Title fallback: built, but the premise did not hold
All 932 "No title" items are **Bluesky posts** (`bsky.app/profile/.../post/...`), labelled with the creator's primary platform ("Newsletter - Substack", "Website", "Podcast"). They are not articles the scraper failed to title; 1,134 rows in total have a `bsky.app` URL, and 202 of those carried a social label. `derive_title()` (first line of description/content, cleaned, 120 chars, `title_derived: true`) is in `pulse_canonical.py` and used by `pulse_v2.py` for future scrapes and by the build for stored data. Because the feed's existing rule excludes social posts and these are microposts, I kept them out (flag `INCLUDE_SOCIAL_HOST_POSTS = False` in `pulse_canonical.py`). Classification is now by URL host, not by the creator's platform label.
**Canonical counts:** default (Bluesky out) 9,394 feed rows -> **8,966 pieces** (no change from the 8,966 you approved). If you flip the flag: 10,648 rows -> **10,097 pieces** (+1,131, 1,128 with derived titles), and Bluesky text would appear under "Newsletter"/"Podcast" tags in the feed. **Your call; I recommend leaving them out.**

### 2. Pieces = distinct URLs
Headline and every count now come from pieces (one record per canonical URL; co-hosts kept in `co`, tags unioned). Masthead: **886 creators published 3,092 pieces across 75 beats**; "Last 7 days (3,092)" in the feed matches. Creator counts include co-hosts. Cohort volume is still per feed (rows), by design.

### 3. Digest re-run on the canonical list
`pulse_digest.py` and `update_pulse.py` now both call `pulse_canonical.canonical_view()`, so the numbers cannot drift. The digest window is the masthead window (Oct 15-21) and its prompt carries the cohort numbers and says raw week-over-week totals must never be used. Result: no rejected creators in the text; the lede now says Politics "965 posts across 173 independent creators" (counts taken verbatim from the canonical breakdown); Tech "up" and Science "down" match the cohort data (+10%, -18%). Byline is "Atlas Pulse · date · machine-generated"; `metadata.reviewed_by` is `""` by default and the page shows "reviewed by X" only when set; `metadata.provenance` added.
**Two problems found and fixed in the digest script:** (a) run 1 passed verification but the reviser wrote meta-commentary into 2 descriptions ("the creator names cited in the original digest could not be verified"); (b) run 2 failed verification on a JSON error (the known flaky gate) and correctly refused to publish. Added a guard that replaces any description containing such narration with a data-only line, and told the reviser to write final copy only. Run 3 passed with no leaks. The verification pass still only checks trending topics, not the lede or field summary. `previous_pulse_beats.json` was rewritten by this run on the canonical basis.

### 4. Window label and rename
Masthead: "Pulse · Vol. 1, No. 7 · Oct 15-21, 2026 · Data through Thu Oct 22, 2026 (5 days ago)". Issue number stays ISO-week keyed (2026-W43 = No. 7). "Last 24h" is now **Latest day**.

### 5. Cohort copy and joined / dropped
Masthead note: "Among the 494 feeds that published in every one of the last four weeks, volume was up 2% on the week before. This cohort leaves out the highest-volume feeds, which cannot qualify while RSS depth caps hide their older posts; it will include them once archived history is merged. Compared with the three weeks before, **80** feeds published this week after a quiet stretch and **38** that had published every week did not." Joined = posted this week, none in the three before. Dropped = posted each of the three before, none this week. Caveat: "joined" can include a high-volume feed that merely shows only its latest items; I did not remove capped feeds from it (they are not yet flagged; that is item 8-9 work).

### 6. Labels and target size
All DM Mono is gone (59+ uses): labels are `var(--font-mono)` (Source Code Pro) and every font size under 12px is now 12px (checked in the browser: no visible text under 12px, no DM Mono computed). Target-size fixed (post, signal and intel links get a 24px box). Also fixed contrast: secondary text moved off #888/#aaa/#bbb to the v15 secondary gray; dark-surface muted text raised.

### 7. LCP
The lede renders from the digest before the posts download finishes (the post fetch starts immediately and everything post-dependent waits for it).

### Lighthouse (local; "gzip" = a small server that compresses like Cloudflare)
| | Phase 0 | Phase 1 (no gzip) | Now (gzip) |
|---|---|---|---|
| Performance | 55 | 53 | **82** |
| Accessibility | 92 | 90 | **97** (1 contrast item left) |
| SEO / Best practices | 92 / 100 | 100 / 100 | 100 / 100 |
| FCP / LCP | 33.0 s / 34.4 s | 3.0 s / 22.5 s | **1.9 s / 4.4 s** |
| CLS | 0 | 0.004 | 0.089 (lede reflows when web fonts swap in; under the 0.1 line) |
| Transfer | 6,346 KiB | 4,052 KiB (uncompressed) | 1,772 KiB |
LCP is still the lede; the next step (server-rendering the first 50 posts) was on the earlier list and is not needed for this push.
Screenshots (overwritten, same names): `pulse_redesign_screens/phase-1/`. Before/after for James on the caps/arrow change: phase-0 vs phase-1 `fold-*` and `full-*`.

### Not done (waiting for your push, then items 8-12)
Snapshot merge and per-feed cap flags (8), schedule/Routine (9), outbound links (10), `beats.json` (11), City Lab (12). City Lab findings so far, no change made: the page disagrees with itself (meta says 75 creators, body 76; the outlet list has 244 entries though copy says 245; creators are inline JS arrays with no "as of" date), so those figures cannot be read cleanly from a source file yet; the Pulse block is unchanged.


## Phase 1c: next batch A-E (2026-10-27)

**Premise check.** The batch said "Phase 1b pushed". It is not: the public repo's `main` is still `8c2aa6f` (Oct 26) with the redesign uncommitted, and the live site still serves the old page (no "Atlas Pulse" h1, no `PULSE:MASTHEAD` marker; `/assets/data/pulse/posts-2026-W43.json` returns the site's HTML shell with a 200, so the folder is not deployed). So the two-step order below still applies, but step 1 has not happened yet.

### What goes in which push
- **Push 1 (the working tree as it is now):** Phase 1b on Oct 22 data, plus this batch's page changes: Bluesky stat, City Lab counts (page + Pulse block), CLS fix. `build-dist.sh` copies `assets/data/pulse`. Not for the push: `.DS_Store`, `_headers`, `preview/nn-launch-kit/explorer-named/`.
- **Push 2 (data refresh, staged, not applied):** `journalism-atlas-private/pipelines/pulse/staged/2026-10-27/` holds `pulse.html`, `data/pulse-issues.json` and `assets/data/pulse/posts-2026-W39..W44.json`. After push 1 is live, run `staged/2026-10-27/apply.sh` (plain `cp`, no git) and push that separately.

### A. Fresh scrape, rebuild, digest
- Scrape (old code, run before the link change): 2,415 creators, 1,721 / 1,747 feeds fetched (98.5%, gate 95%), 10,578 rows, 0 future-dated. Manifest `run-manifests/pulse_run_manifest_20261027_074316.json`.
- Canonical: 10,578 rows -> 9,311 feed rows -> **8,875 pieces**. Masthead window Oct 20-26: 907 creators, 3,153 pieces, 73 beats. Cohort 500 feeds, WoW +3.8% (raw +48.4%), joined 108, dropped 36.
- **Gate: passed** (exit 0, nothing live touched; staged only). Digest `pulse_digest_20261027.json`.
- `published_at`: 10,567 of 10,578 (99.9%) carry a real time, 11 are midnight-UTC. By platform 99.5-100%. (The date-only caveat in Phase 1 is smaller than feared: real feeds carry times.)
- Issue number: the Oct 27 scrape is **No. 8** (W44) only five days after No. 7. See Decisions.
- The shrinking W39 file (93 posts vs 1,078) is the 30-day window sliding; the merged archive (D) would stop that.

### B. Lede and field summary
- Figures now come from a template: the model writes prose around `{{placeholders}}` (`top_beat`, `top_beat_posts`, `top_beat_creators`, `pieces`, `creators_active`, `window`, `headline_creator_posts`). A draft that types its own number or an unknown placeholder, names a creator removed from the registry, or omits the top story's creator is rejected before filling. A second model call then checks every non-numeric claim. Unparseable checker output counts as a failed check. After two rejected drafts the lede is a fully deterministic sentence.
- The numeral check on the lede is now **fatal** (it was log-only); trending-topic descriptions stay log-only.
- **Result: 6 of 6 model drafts across 3 runs were rejected**, all by the claims check, and the checker was right each time (a story described as Politics that is tagged Energy/Policy; "comparable" scores of 71 vs 66; a story attributed to a beat it is not tagged with). The page therefore ships the deterministic lede: "Politics led the week of Oct 20-26, tagged on 994 pieces from 174 creators. Highest signal: Justin Gerdes, ..." `metadata.lede_source = "template-fallback"`. `reviewed_by` stays empty for you to fill after reading it.
- **Verifier bug found and fixed.** The old trending-topics verifier saw only the first 2,048 characters of its context, so it "could not find" creators who were in the data and deleted them from accurate descriptions (Oct 27 run 1: Brian Beutler, Ben Thompson, Scott Galloway, Nate Silver and about a dozen more, all confirmed present in the window). It now gets the full window creator list. Oct 22's published digest went through the same truncation; its descriptions may have lost real names.
- Known gap: `lede_facts.creators_active` in the Oct 27 digest metadata is 866 (primary creators only); the masthead's 907 counts co-hosts. Not shown anywhere; fixed in code for the next run.

### C. City Lab counts
- Derived by `city_lab_counts.py` from the inline arrays: **75 creators (39 journalism + 36 lifestyle), 245 outlets, 20 anchor institutions.** One number everywhere: meta, hero, tab badge, eco panels, layer buttons, Methodology, and the Pulse block, all stamped from the arrays at build time (`python3 city_lab_counts.py --check` exits 1 on any disagreement). "As of" = date of the last commit touching `city-lab-chicago.html` (now Oct 26, 2026), shown on both pages.
- Where the copy disagreed: creators 75 (meta, hero) vs 76 (tab badge, All button, eco panel) vs 76 (Pulse); lifestyle 36 (page) vs 37 (Pulse); outlets 245 in the copy vs a code comment saying the array has 244 (it has 245; comment removed); the breakdown sentence "75 + 29 + 33 + 107" sums to 244, replaced by the Medill categories computed from the array (128 for-profit, 53 solopreneur, 45 nonprofit, 18 other, 1 collective = 245).
- Not changed, flagged: 77 Flavors of Chicago ("Sara Faddah, Dario Durham") is listed in both layers, so 75 listings are 74 distinct channels. The "29 Tier 1 orgs" and "33 ethnic and community" figures are hand-typed and cannot be derived from the arrays.

### E. CLS
Metric-matched fallback faces (`Inter Fallback` on Arial, per-weight `size-adjust` measured in Chromium: 106.9% / 108.0% / 101.1% / 102.2% for 400 / 500 / 600 / 700, ascent/descent from Inter's metrics; mono fallback on Courier New). Lighthouse CLS **0.089 -> 0.003** (3 runs). Caveat: the fallbacks use `local()` Arial; a device without Arial (stock Android) falls back to its default sans and is not corrected.

### Bluesky stat
New separate line in How Pulse works, not in the pieces count: "73 Atlas creators posted to Bluesky in Oct 15-21 (84 in the last 30 days)". On Oct 27 data: **77 in Oct 20-26 (86 in 30 days)**. Counts creators with a `bsky.app` post, from the Bluesky accounts Pulse monitors; it is not a census (the registry's Bluesky list is larger). Pieces stay 8,875 / 8,966.

### D. Items 8-12
- **8. Snapshot merge** (`snapshot_merge.py`, new file `spidering/core/rss_pulse_merged_20261027.json`, canonical source untouched). 20 snapshots (19 archives plus today's; you said 17, the folder holds 19 `rss_pulse_v2_*` archives, one a 7-day window) = 163,667 rows -> 64,853 unique posts; 316 future-dated rows dropped (a Dec 2026 date in June-Sept files). 294 feeds are capped in the Oct 27 scrape (10+ items and the oldest item 3+ days short of the window start).
  - Cohort window Sep 29-Oct 26: 9,922 posts from the newest file alone, **13,201 merged**.
  - Capped feeds with a post in the oldest week: **84 -> 261 of 294**. Fully covered all 28 days: **140** (48%); all but 3 days: 173 (59%). Mean days covered of 28: 15.2 -> 22.9.
  - **The merged raw weekly curve still ramps, but less, and it is now distorted the other way.** Newest-only weeks: 1,546 / 1,908 / 2,543 / 3,925 (+154%). Merged: 3,697 / 2,144 / 3,019 / 4,341 (+17%). The dip is a coverage hole, not a trend: there are no snapshots between Oct 5 and Oct 22, so 148 capped feeds are blind on Oct 6, tapering to 0 by Oct 22. **A raw Line on merged data must mark Oct 6-21 as partially covered, or use the cohort.** Snapshots at 2-3 day spacing remove the hole (below).
- **9. Schedule.** Cannot register a Routine from Claude Code (the Oct 5 spec says so); not done. Computed instead, over 453 feeds ever capped in the last 8 snapshots: safe interval = items a feed returns / its peak posts per day. Median 13.1 days, p10 4.4, min 2.8 (Monte Oz; Trish Regan and Ryan Belmore 3.3). Lossless share of capped feeds by scrape spacing: 1-3 days 100% (452/453 at 3), 4 days 92%, 5 days 88%, **7 days 80%**, 14 days 49%. Peak rates come from partly covered data, so they are floors and the safe intervals are upper bounds. **Proposal:** scrape only (no digest, no API cost, ~8 min) every other day (Mon/Wed/Fri/Sun, gaps 2/2/2/1 days), keep the digest and the publish weekly. Fallback: Mon + Thu (3 and 4 day gaps, about 92-100%).
- **10. Outbound links.** `pulse_v2.py` now stores `links` per entry (absolute http(s) links from the full summary and content, tracking params and fragments stripped, same-site, share/social/asset links and duplicates dropped, max 15). No UI; the page's post files use a field whitelist and do not carry it. **Not in the Oct 27 data** (that scrape started before the change); the first file with links is the next scrape.
- **11. beats.json** (`build_beats.py` -> `pipelines/pulse/beats.proposed.json`, not read by anything). The "446 raw strings" are comma-joined combinations of **79 tags** (registry 768 combinations, 439 in the Oct 27 posts, 506 across snapshots); every one of them resolves (0 unresolved), including 4 legacy tags that exist only in old snapshots (Automotive, Civic Life, Local News, Social Issues). No beats merged. 34 beats map to one of the nine confirmed ATLAS_VIZ_COLORS categories, 49 are grey (62% of tag mentions carry a category colour). Eight merge candidates are listed for your call, default keep separate.
- **12. City Lab:** done under C.

### Decisions for Justin (this batch)
1. **Push order.** Phase 1b is not live. Push the working tree first; apply staged Oct 27 second. OK?
2. **Lede.** Read the deterministic lede and set `reviewed_by` if it holds. Model prose is rejected 6 of 6 for now; do you want the fully templated sentence structure (no model prose) as the default and the model as an optional second sentence?
3. **Issue numbers.** The Oct 27 scrape becomes No. 8, five days after No. 7. With a 2-day scrape cadence, should only the weekly publish run increment the counter?
4. **Two Politics numbers on one page:** the lede and beat map say 994 (exact tag, a piece counts under every tag); the trending-topic card says 437 (first tag, non-local). Pick one definition for the page.
5. **City Lab:** 75 listings or 74 distinct (77 Flavors in both layers); the hand-typed 29 and 33.
6. **Schedule:** every other day, or Mon + Thu? You register the Routine.
7. **beats.proposed.json:** approve, edit categories, rule on the 8 merge candidates.
8. **Phase 2 gate:** the merged raw curve is not clean (Oct 6-21 hole), so The Line should be the cohort curve with partially covered days visibly marked. Agree?

### Private-repo files for the commit (this batch)
`pulse_canonical.py` (new; Bluesky counts, link extraction), `city_lab_counts.py`, `snapshot_merge.py`, `build_beats.py`, `beats.proposed.json`, `pulse_digest.py`, `pulse_v2.py`, `update_pulse.py`, `pulse_digest_20261027.json`, `previous_pulse_beats.json` (now the Oct 27 baseline: it belongs with push 2; the Oct 22 canonical baseline is saved as `previous_pulse_beats.20261022.json` if push 2 is skipped), `run-manifests/*20261027*`, `staged/2026-10-27/`. `feed_cache.json` also changed from the scrape.


## Phase 1c rulings (Oct 27, from Justin) and what was done

1. Both pushes today: working tree, then `staged/2026-10-27/apply.sh`. The working tree changed after Justin's 08:11 commit (`42b0817`): City Lab now 74 distinct creators, 29/33 removed, a method line on beat counts, `--publish` issue counter. They ride with push 2 (the staged `pulse.html` already contains them; City Lab page and `build-dist.sh` are in the working tree).
2. **Lede:** the templated sentence is the default; one optional model sentence appears only after passing the checks (`metadata.lede_source`: `template` or `template+model`). Oct 27 run: `template+model` passed. The final lede: "Politics led the week of Oct 20-26, tagged on 994 pieces from 187 creators. Highest signal: Justin Gerdes, ... Taylor Justin's "8 Classic Chicago Foods Worth Trying at Least Once" draws on a rare local beat, spotlighting iconic dishes across Chicago's restaurant and food culture scene." **Read it before applying push 2; `reviewed_by` is empty.** (I would trim the last clause; it is the model's gloss on the title, which passed the checker.)
3. **Issue counter:** only `update_pulse.py --publish` opens a new issue number (`refresh_pulse.sh` passes it on the weekly run; `--scrape` mode added for the every-other-day scrape). Fixed Monday-Sunday issue windows start at the next weekly publish, not today. Not built: that needs the merged archive.
4. **Beat counts are any-tag everywhere:** the digest's topic cards now take their counts from the same any-tag figures as the lede and beat map (Politics 994 posts, 187 creators, co-hosts counted) and overwrite the model's numbers deterministically. A method line was added to How Pulse works. The signal-rail tabs and the beat chips on items still use a piece's first tag as a label and for grouping stories; no count depends on it.
5. **City Lab:** 74 distinct creators (the layer buttons stay 39 and 36). The "29 Tier 1" and "33 ethnic and community" figures are removed from the page: no array, field or source file in the repo produces either (Nonprofit/Established is 29 by coincidence only). Both appear nowhere else on the site.
6. **Schedule:** `PULSE-ROUTINE-SPEC-2026-10-27.md` (private repo) has the two Routines for you to register: scrape every other day (`./refresh_pulse.sh --scrape`), publish weekly.
7. `beats.proposed.json` is held for your ruling (the eight candidates are in the chat reply).
8. **Phase 2 hero** (preview only, not in the push tree): `journalism-atlas-private/pipelines/pulse/phase2/pulse.phase2-preview.html` plus `p2_patch.py`; screenshots in `pulse_redesign_screens/phase-2/` (`hero-*`, `line-*`, `fold-*`, `full-*` at 390/768/1440, light and dark). `pulse_tokens.md` lists the tokens.
   - **The Line:** cohort daily curve (500 feeds, Sep 29-Oct 26), 28 days, acid on dark, weekly bands, hatched and dashed "Partly covered" days (cohort feeds whose depth cap hides their older posts: 86% covered on Sep 29, 100% from Oct 5), a "Show the numbers" table, a text alternative on the chart, redraws at 1:1 so labels stay 12px. Caption states the cohort's +3.8% against the raw +48.4% and why. Daily resolution until four weeks of `published_at` exist.
   - **Dark mode:** v15 neutrals via tokens; Lighthouse accessibility 100 with 0 contrast failures in dark (light: 97, one pre-existing item). **Reduced motion:** verified (ticker stops, draw-in off, durations collapse).
   - **Hero changes beyond the brief, for James:** the h1 "Atlas Pulse" is now a real title (was 14px), the lede is set smaller (26px max, weight 600) because it is now two sentences, and the dotted underline on numbers in the lede is gone (every digit used to be underlined).
   - Dark mode below the hero was converted by token mapping and checked by contrast audit, not by eye section by section; James reviews before Phase 3.


## Phase 3: the rebuild (Oct 27, 2026) — supersedes Phase 2 and the launch-fix list
Nothing committed or pushed. Scraper not re-run; the page was rebuilt with `update_pulse.py --pulse-only` from the Oct 27 scrape (No. 8, Oct 20–26: 907 creators, 3,153 pieces). Banner (`header.js`) untouched. /for-brands N&N date flag and the held org count untouched.

### What the page is now (three questions, in order)
1. **The field (hero).** h1 server-rendered: "907 creators in the Atlas published 3,153 pieces this week." (same sentence in `<title>`, OG, Twitter, description). One circle per creator (907), area = their piece count, packed by beat with d3 (the `d3js.org/d3.v7.min.js` copy search.html already loads; `defer`; if it fails the hidden table is shown instead). Clusters are one neutral fill, no beat colours; Acid marks only the hovered or selected cluster. Hover (fine pointer, 120 ms dwell) or click/tap/Enter opens the panel (side panel at 900+, bottom sheet below): creators and pieces (any-tag), top 8 creators, one piece, "See all {beat}" (jumps to Find your corner), "Brief your team on {beat}" (`/for-brands?issue={beat}`). Individual circles name the creator on hover (desktop). One entrance (≤1 s, staggered); none under `prefers-reduced-motion` (verified: 0 pre-states, 0 animations). Hidden table of beats/counts, clusters are `role=button` with `aria-label`. Quiet line: "Counted from 1,747 monitored feeds … How we count" → `#method`.
2. **What mattered.** Five stories from `assets/data/pulse/pulse-picks.json` (keyed to issue 8). Label "Selected automatically this week." when `picked_by` is `auto`, "Picked by the Atlas." when `atlas`; if the file's issue is not the page's issue the page shows the top 5 digest signal stories, one per beat, labelled "Ranked automatically by signal."
3. **Find your corner.** Beat select (28 main beats, then the other tags) + search (creator, channel, title, tags). URL state `?beat=slug[,slug]&q=`; old `?beat=Politics` links resolve; two-beat filter from the Overlap matrix still works (with a "Show one beat only" link). One line under the filter ("Politics: 187 creators, 994 pieces this week."), then "Want Politics every week? Tell us" with one email field. Empty search: "No one in the Atlas published on “q” this week." plus "Suggest someone" (name or link, optional email). Both forms post to the /for-brands Formspree endpoint with `source_page=pulse`, `interest`, `_subject`, `page_url`, honeypot; failure keeps the answer and shows an error. No mailto anywhere. Feed = the issue window, grouped by day, 50 at a time.
Then City Lab (existing block, stamped counts), Work with the Atlas (the three asks in one row; the duplicate "Turn this into a brief" bar is parked), and **How we count** (collapsed `<details id="method">`, opened by any `#method` link): cohort paragraph with joined/dropped, the raw-vs-cohort sentence ("raw volume looks up 48% … do not read that as growth"), feeds and Bluesky lines, the any-tag note, the machine-generation note, then Rhythm, Overlap and For teams (each collapsed, code unchanged).

### Cut from render (code kept)
Lede, story stack, beat map, ticker, signal rail with beat tabs, weekly brief, old feed controls, activity bars, instrument tab bar. They sit in `#pulse-parked` (hidden) so the old functions still have targets; the calls that fill them were removed from the boot. The Line was never in `pulse.html` (it lives in `pipelines/pulse/phase2/`), so it stays there. The Oct 27 lede, its "8 Classic Chicago Foods" clause and `reviewed_by` are no longer rendered.

### Rulings applied, and two places I deviated
- **Shared beats module:** `scripts/main_beats.py`, read by `build_lens_index.py` (chips) and `update_pulse.py` (field). Rule unchanged (≥40 pieces this week, ≥25 registry creators). Result: **28 main beats** (not 9), plus one "Other beats" cluster (95 creators, 45 other tags). Chips are identical to before. No viz-category mapping; `beats.proposed.json` is not used.
- **Counts:** every printed number is any-tag. Verified equal on both pages: Politics 187 creators / 994 pieces, Tech 110 / 368, Local 74 / 306, Finance/Economics 66 / 202 (Lens panel vs Pulse panel vs `field-data`).
- **DEVIATION 1, the caption.** Your text, "in the beat they published most in this week", is not true of this data: beat tags belong to the creator, not the piece, so every tag of a creator has the same piece count and "published most" is always a tie, broken by canonical order (busiest beat first). That is why **Politics has 187 placed and 187 any-tag, not 133**: the 187-vs-133 gap in the brief does not exist under the stated rule. I shipped "Each creator appears once, in the busiest of their beats this week. Co-hosted pieces count for each host." Reverting is one string in `render_field()` (`update_pulse.py`).
- **DEVIATION 2, labels.** Only the clusters big enough for a 12 px label carry one on the field (10 of 29 at 1440, 9 at 768, 6 at 390). The rest are named on hover, tap, focus and in the table. Larger text would overlap the circles.
- **Dark mode:** the whole page follows the viewer's theme (`prefers-color-scheme`, `data-theme` override); hero distinguished by scale. This is the Phase 2 token set brought into `pulse.html` for the first time (it had only existed in the preview). Below-the-fold dark rules are token-mapped, not checked section by section by eye.
- **Live colour = Acid on both pages:** /for-brands `--viz-orange` → `--color-acid` (3 rules: live dot, framing-line figures, convergence lines; all on the dark Lens stage). For James: token doc now has one live colour.
- **h1 = the /for-brands clamp** (36–64 px Merriweather 700, pending James), Merriweather loaded non-blocking with a metric-matched Georgia fallback.

### Picks for No. 8 (auto; `picked_by: "auto"`)
Rules: substantive reporting or analysis; no listicles, roundups, recurring formats or promos; one per creator, two per beat at most; mix of platforms; prefer stories others covered; each "why" from the piece and the data only. I read the five before writing the lines (the video I could only check by its description).
1. **Chris Geidner**, "In rare Sunday arguments, appeals court judges skeptical of DOJ's California election lawsuit". Government Accountability, Substack, Oct 26. *Covers the Ninth Circuit's Sunday arguments in DOJ's California election lawsuit and ties it to the Alaska suit. Adedayo Fashanu, Aaron Parnas and Lisa Remillard also covered the Alaska suit this week.*
2. **Austin Kocher**, "The First ICE Detention Death of Fiscal 2027 Follows the Deadliest Year on Record". Immigration, Substack, Oct 21. *Reports the Oct 17 death in ICE custody of a Mexican national and lawful permanent resident, the first of fiscal 2027; his daughter says staff would not give him his medications. Kate Morrissey also reported an ICE custody death this week.*
3. **Julie Roys**, "Students accuse NC Christian college of using NDAs to hide sexual assaults". Investigative, Website, Oct 20. *Former students of Excel College, an unaccredited Christian college in North Carolina, accuse it of using a non-disparagement agreement in its honor code to keep sexual assaults quiet.*
4. **Maureen Kelleher**, "Following the Money In Chicago School Board District Races". Local, Ghost newsletter, Oct 23. *Sets Chalkbeat and the Illinois Answers Project's spending analysis against its own predictions for Chicago's school board races; District 4A is the most expensive so far, with more than half a million dollars spent.*
5. **James Li**, "AI Agents Are "Hacking Banks" — But That's Not The Real Story". General News, YouTube, Oct 23. *A video on the reports of AI agents accessing U.S. bank accounts; the title argues it is not the real story. Gary Marcus and Rowan Cheung also covered the bank reports this week.*
Mix: 2 Substack, 1 Ghost, 1 website, 1 video. Five beats, five creators. Convergence found by title overlap across creators (rare-word match, then checked by eye); #1, #2 and #5 are in a cluster, #3 and #4 are not.
**Alternates (swap by editing `pulse-picks.json`):**
- **Gary Marcus**, "Breaking news: U.S. banks are taking hits from AI agents" (Tech, Substack). Same story as #5 in text form; passed to get a video in the mix. Swap in if you want text.
- **Nate Silver**, "Fake polls are a real problem" (Explanatory, Substack). Converges with Matt Yglesias and Tim Pool on the fake-poll story. Passed because the opening is a video/podcast plug and I could only verify that part; strong alternate for a Politics slot (none of the five is Politics).
- **Kate Morrissey**, "Another death in ICE custody, Camp East Montana contract extension and a $100 million surveillance plan" (Immigration, Substack). Same story as #2; one per story, and hers is a multi-item roundup.
- **Francine McKenna / Wilbert Geijtenbeek**, "Crowe Global shut down Dutch member firm's email servers…" (Finance/Economics, Substack). Original accounting reporting, but a guest post under McKenna's byline and no one else covered it.
- **Matthew C. Klein**, "U.S. Inflation Not Getting (Much) Worse, or Better, but Consumers are Fine" (Finance/Economics, Substack). Substantive, but paid after the opening, so a why-line would rest on two paragraphs.
Others passed: the Abdul El-Sayed cluster (9 creators; I read none, mostly campaign-moment commentary), Nathan Fielder (4 creators; culture criticism), the Vivek Ramaswamy ad cluster (6; commentary), the Benn Jordan Flock video (only sponsor copy was available to read). Candidates for next week: `pipelines/pulse/pulse-picks.candidates.md` (private; top 15 signal stories; the top two this week are a power-grid story and the Chicago-foods listicle).

### Lighthouse (local, compressing server; mobile defaults; vs the live No. 8 page, same server)
| | Perf | A11y | BP | SEO | FCP | LCP | CLS | TBT | Transfer |
|---|---|---|---|---|---|---|---|---|---|
| No. 8 as live (2 runs) | 94–95 | 97 | 100 | 100 | 1.8–1.9 s | 2.7–2.9 s | 0.001 | 0–10 ms | 1,802 KiB |
| Rebuild (3 runs) | 93–98 | **100** | 100 | 100 | 1.9 s | 1.9–2.9 s | 0.001 | 20–30 ms | 1,968 KiB (d3 included) |
The old contrast failure is gone. One unscored experimental audit (label-content-name-mismatch) flags the cluster buttons: the visible label is "Politics" over "187" while the accessible name is a full sentence; I kept the sentence. A dark-scheme accessibility run also scored 100 but I could not confirm the flag applied; dark was checked by eye and by the screenshots.

### Screenshots, `pulse_redesign_screens/phase-3/`
`hero-{1440,768,390}-{light,dark}.png` (first screen), `panel-…` (Politics cluster open: side panel at 1440, bottom sheet at 768 and 390), `full-…` (full page). No horizontal scroll at 1440 / 768 / 390, no console errors, reduced motion verified, keyboard (Tab to a cluster, Enter, focus moves to the panel heading, Escape closes) verified.

### Checked, and what I did not
Checked: field totals = masthead = Lens totals; forms with fetch stubbed (empty email, failed post keeps the answer and shows an error, success); empty search and suggest; URL state both ways; `#method` opens; Rhythm, Overlap and For teams render; the Overlap matrix routes into Find your corner; `build-dist.sh` ran clean (no `{{` left, `pulse-picks.json` copied, Lens flag `lens: true`); `build_lens_index.py` rebuilt on the same run (3,153 pieces, 907 creators, same chips). **Not done:** a real Formspree submission (I never post to your live inbox; send one test from /pulse after the push and confirm `source_page=pulse` arrives); a real Cloudflare Lighthouse (live is behind a bot challenge); below-the-fold dark mode by eye.

### Findings for the chat session
1. **Beat tags are per creator, not per piece.** So a beat's "top piece" is only as good as the creator's tag: the panel uses the best digest signal story with that beat as its first tag, else the latest non-listicle piece with that first tag from the beat's busiest creator ("Latest from {creator}"). It is labelled that way, but some are weak (Culture's is a site-management post). Per-piece tags, or dropping the piece where no signal story exists, would be better.
2. **28 main beats is a lot of clusters.** The Lens rule gives 28; the brief assumed 9. It reads well at 1440, thinly at 390. A cap (say the top 12 by pieces, the rest into Other) is one constant in `main_beats.py` if you want it.
3. **/for-brands says "journalists", Pulse now says "creators".** Same numbers, two words. Your vocabulary ruling covered Pulse only.
4. **The Lens index shipped stale.** The committed `lens-index.json` was still on an older window; it is rebuilt here (Oct 20–26, data through Oct 27), so it is in the stage list.
5. **d3 is the floating `d3.v7.min.js` from d3js.org** (the copy main.js/search.html already use), not a pinned cdnjs version.
6. The `?recency=` and `?view=` URL parameters no longer do anything.

### Files to stage
**Public repo (`journalism-atlas`, via GitHub Desktop):** `pulse.html`, `for-brands.html` (acid for orange; chip/`data-through` bake), `assets/data/lens-index.json`, `assets/data/pulse/pulse-picks.json` (new), `scripts/main_beats.py` (new; `build_lens_index.py` already committed with the import). Optional, off the public site: `pulse_redesign_ledger.md`, `pulse_redesign_screens/phase-3/`. Not mine, do not stage: `.DS_Store`, `_headers`, `preview/nn-launch-kit/explorer-named/`.
**Private repo:** `pipelines/pulse/update_pulse.py` (h1, field, cohort, head; imports the shared module), `pipelines/pulse/pulse_candidates.py` (new), `pipelines/pulse/pulse-picks.candidates.md` (new), `spidering/core/refresh_pulse.sh` (step 3c).


### Phase 3 pre-push revisions (Oct 27, evening) — these supersede the matching lines above
1. **Beat wording.** Pulse panel: "187 creators who cover Politics published 994 pieces this week." Find your corner uses the same sentence for a beat filter. Lens: "187 creators who cover Politics published 994 pieces, plus 2 more pieces with “Politics” in the title, in the week of Oct 20, 2026." (I kept the dated "in the week of" so the sentence stays true after the week passes; say if you want "this week".) Title queries read "84 pieces from 60 creators with “AI” in the title". Field caption: "Each creator appears once, under the largest of the beats they cover. Beat tags belong to creators, not pieces; co-hosted pieces count for each host." #method says beat tags belong to creators, a count by beat is the creators who cover it and every piece they published, and that every printed number is of that kind. /for-brands: the Lens counts and the Lens note say "creators"; brand copy that uses "journalists" as a noun (hero, ladder, meta descriptions) is unchanged.
2. **Panel.** Top piece removed (module, build and page). It shows the top 8 creators, each name linked to their registry channel link (the creator's most recent piece in the window if the registry has none), then "See all {beat}" and "Brief your team on {beat}".
3. **Field.** The ten main beats with the most creators get labeled clusters, the same ten at 1440, 768 and 390: Politics, Tech, Media/Power, Culture, Local, Finance/Economics, World, Science, Climate/Environment, Food. Everything else is one "63 more beats" cluster (272 creators placed there, because the largest beat they cover is outside the ten). Its panel lists all 63 beats with creator and piece counts; each is a button into Find your corner. Placement tie-break is now "largest by creators" (it was "busiest by pieces"); the caption matches. Every cluster carries a label at every width: hulls grow to fit their label, and a check at all three widths found 11 clusters, no overlaps, none outside the stage, no horizontal scroll. The Lens keeps the shared 28-beat list (`main`); the field's cap is `FIELD_BEATS = 10` in `scripts/main_beats.py`, noted there and in `pulse.html`. The corner's beat select still lists the 28.
4. **d3 pinned** to `https://cdnjs.cloudflare.com/ajax/libs/d3/7.9.0/d3.min.js` with an SRI hash, in `pulse.html`, `search.html` (the page that loads d3 for `main.js`; `main.js` itself has no URL) and `mobile.html`. A repo-wide search of site pages found no other floating script URL (the others are already versioned cdnjs files). Verified: d3 7.9.0 loads on /pulse and /search with no console errors; `build-dist.sh` clean.
Screenshots (replaced): `pulse_redesign_screens/phase-3/panel-1440-dark-politics.png`, `panel-390-light-politics.png`, plus `panel-…-more-beats.png` at both sizes. Files to stage now also include `search.html` and `mobile.html`. Not re-run after these edits: Lighthouse (the page logic changed, markup did not).
