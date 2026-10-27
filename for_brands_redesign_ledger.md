# /for-brands redesign ledger

## Decisions waiting on Justin (keep current)
1. **Design system conflict (new, blocks Phase 2).** The brief says Playfair Display / DM Sans / Space Mono and an orange "live" accent. The repo's tokens (`docs/design/DESIGN-TOKENS-v15.md`, `assets/css/variables.css`) say Inter / Merriweather / Source Code Pro, green = interaction, and have no orange token. Pulse hit the same conflict (Pulse ledger, decisions 1-2) and recommended v15. Pick one: (a) v15 (Merriweather for the argument, Source Code Pro for live data, Acid as the single "live" color), or (b) the brief's fonts and orange, which means a deliberate departure from v15 that James needs to approve.
2. Headline: "Trust moved. Here's the map." or an alternate.
3. Buyer order: corporate affairs, firms, sponsors.
4. Paid service name: "Field Briefs" under Atlas Labs?
5. Standards section: approve commitments and signers.
6. Lab items: which are real enough to show, and with what status.
7. Nav label: "For brands" or change.
8. Team strip: add James Bareham?
9. Prices: show a starting point or not.
10. Hero Lens depth: build at issue level (title matching) or beat level? See data inventory.
11. Nodes and Networks date gate: the paper goes live Oct 28 (tomorrow). Gate with a date check anyway?

## Phase 0: Audit (2026-10-27)
Changed: nothing in the site. Created `for_brands_redesign_ledger.md` and `for_brands_screens/phase-0/` (8 PNGs: full and fold at 390/768/1280/1600, from a local copy with count tokens stamped; live blocks scripted browsers). Nothing committed.

### Source and plumbing
- `for-brands.html`: one 87 KB static file, inline CSS and JS, Inter and DM Mono from Google Fonts, plus the Material Symbols icon font (source of the leaking ligature text: `summarize`, `rss_feed`, `lock_open`, `task_alt`, `info`, `monitor`, `group`, `article`, `handshake`, `search`).
- Shared: `assets/css/variables.css` (tokens), `components.css`, `header.css`, `assets/js/header.js`, `footer.js`. Build: `build-dist.sh` copies top-level `*.html` and `assets/data/pulse/` already, so a new compact Lens index file under `assets/data/` needs a line added to `build-dist.sh`.
- Counts: `{{CREATOR_COUNT}}` / `{{COUNT_AS_OF}}` are stamped at build from `assets/data/site-stats.json`. Current value **2,415, as of October 26, 2026**, with 79 topics and 33 platforms.

### Numbers inventory
| Value | Where | Source | Status |
|---|---|---|---|
| 2,415 verified creators | for-brands (4 token uses), research (2 token uses) | site-stats.json, build-stamped | Source files use tokens. **Live shows 2,415 on both pages**, so the brief's "1,718 on /research" does not reproduce. 1,718 was the June figure; I found none in the current source or on the live page. Nothing to reconcile on this page. |
| 1,756 feeds, 984 active this week, "Updated October 22" | for-brands Pulse block, JS-filled from a snapshot with typed fallback text | Pulse snapshot | Fallback text is hard-coded and was written by `update_pulse.py`. The pulse.html Phase 1b ledger reports 1,747 feeds and 886 creators / 3,092 pieces for the Oct 15-21 week. for-brands has not been rebuilt, so the two pages disagree until it is. |
| "1,756 creator feeds, monitored weekly" | gallery card | typed | Same issue. |
| 238 news-desert counties, 170 papers closed or merged | trust bar | Medill 2026, typed | Needs source link on the number. |
| About 1 in 5 get news from individuals (Sept 2024) | trust bar | CNTI citing Pew, typed | Needs primary link and date check. |
| 82% and 32% | "good news" section | Muck Rack State of Creator Journalism 2025, link goes to netinfluencer.com | Primary Muck Rack report not yet located. Phase 1 task. |
| 80/45/30/25/22% | gallery card | bar widths only | Presentation, not data. Check it carries no meaning. |
| "Follower counts, platform reach, and audience size data are available for every verified creator" | Pulse block | typed | **Conflicts with the brief's rule** and may not be true. Remove or verify. |

### Forms and CTAs
- Forms: 3. (1) brief builder `#brief-form`, (2) "send a question instead" panel inside it (separate JS fetch to Formspree), (3) capture form `#capture-form`, hidden by default. All post to **Formspree `https://formspree.io/f/xzznlvgj`**, the same endpoint. The industry dropdown has 19 options.
- Anchors to keep working: `#build-brief`, `#capture-form`.
- CTAs: about 14 links in the page body. Eight go to `#build-brief` with three different labels ("Tell us what you're tracking", "Tell us what you're tracking →", "Build my brief"); hero has two buttons; Pulse is linked 6 times; Search 3 times.

### Hero data inventory
- Pulse weekly files `assets/data/pulse/posts-2026-W39..W43.json`: fields per post are exactly `creator, channel, title, url, published, topic, geography, platform` (+ `co` on 100 posts). **No excerpt or summary** (dropped in Phase 1 of the Pulse work), **no post-level tags**, no author URL. `topic` is the creator's beat string, copied to every post (346 distinct strings in the Oct 15-21 window, comma-joined). `geography` is the creator's base, filled on 93% of posts. `platform` is the creator's label, not per-post; piece format has to come from the URL host. YouTube alone is 742 of 3,092 pieces.
- Data stops at Oct 22 (stale by 5 days today).
- `creators-data.json` (2,415): topic 100%, platform 100%, geoState 63%, geoCity 59%, geoRegion 91%. Top states: DC 335, NY 322, CA 226, IL 118. 898 have no state.
- Window Oct 15-21: 3,092 distinct pieces.
- Test of title matching on that window (pieces / creators): "AI" 91/74, "election" 44/32, "housing" 13/9, "data center" 7/7, "tariff" 4/4, "Fed" 4/3, "quantum" 1/1, "vaccine" 2/2; "shutdown", "Bitcoin", "ESPN", "insulin" 0.
- **Verdict:** an issue-level Lens is only partly honest. Title-only matching gives real counts on broad topics and very thin or zero counts on specific ones. Many unrelated pieces could match a short word. The empty-state copy fits, but chips must come from topics with enough volume. Beat-level (creator `topic`) is solid for counts, geography and platform mix. Recommended: beat-level result plus issue-level title matches shown as "pieces whose titles mention X", with the true limit stated. Restoring a short `excerpt` per post (the Pulse ledger planned it) would improve matching; that is a pipeline change in the private repo.

### Server surface
No Worker, Pages Function or `functions/` folder (the postcard function was removed earlier). Forms go straight to Formspree. Hidden fields for the Lens query and referrer are possible with Formspree. Anonymized query logging is **not** possible without new infrastructure; flagged, not built.

### Audit of the page itself
- Lighthouse (local copy, stamped tokens, default throttling):
  | | Perf | A11y | Best practices | SEO | FCP | LCP | CLS |
  |---|---|---|---|---|---|---|---|
  | Mobile | 62 | 95 | 100 | 92 | 5.3 s | 18.9 s | 0.005 |
  | Desktop | 85 | 95 | 100 | 92 | 0.6 s | 2.8 s | 0.01 |
  Failing: color-contrast, no `<main>` landmark, and meta description missing. The local server does not compress, so live performance will be better; the live site returns a bot challenge to scripted browsers, so I could not measure it.
- Caps eyebrow over every section, a pill eyebrow with middle dots in the hero, " →" on most links, an auto-scrolling name ticker with 30 hard-typed creator names (conflicts with the rule that names come from data on the homepage, and with the creator-trust test; none verified against the registry).
- Mobile 390: page scrollWidth read 637, caused by the off-canvas mobile menu (probable false positive; to confirm in a real browser).
- Title and OG say "Creator Intelligence for PR & Comms"; OG image is the generic Atlas preview.

### Top five recommendations
1. **Resolve the design-system conflict first** (decision 1). It changes every Phase 2 choice. I recommend v15 tokens with Merriweather carrying the argument and Acid as the single "live" signal.
2. **Build the Lens at beat level with title-matched pieces**, and say so in copy. Plan an `excerpt` field in Pulse for better matching later.
3. **Fix the P0s in Phase 1 as written**, minus the count reconciliation, which is already done in source. Add `<main>`, a meta description, SVG icons, one form, and one CTA label.
4. **Remove the typed ticker and the "audience size data for every creator" line.** Both are risks with the creator audience.
5. **Rebuild the Pulse block from the same snapshot as pulse.html**, and find the primary Muck Rack, CNTI/Pew and Medill links before they appear next to numbers.

### Open questions
- Ship before or after the Oct 28 paper? The date gate is cheap either way.
- OK to add a compact Lens index file and its `build-dist.sh` line in Phase 1/2?

## Phase 1: fixes and the new spine (2026-10-27)
Decisions applied: v15 tokens (Inter body, Merriweather for the argument, Source Code Pro only for live data, Acid as the "live" color), Lens at beat level plus title-matched pieces (Phase 2).
Changed: `for-brands.html` rewritten in place (old copy saved only in git history). Nothing else touched, nothing committed. `research.html` already uses count tokens; no change needed. Not yet added to `build-dist.sh`: nothing new is fetched in Phase 1.
Screens: `for_brands_screens/phase-1/` (full and fold at 390/768/1280/1600, plus `full-1280-gates-open.png` with the gated blocks shown). Before shots: `phase-0/`.

### What Phase 1 did
- **Spine** in the brief's order: hero with Lens, shift (People/Places/Machines), not influencers (five rows, two-column contrast) with the 82%/32% turn directly under it, three relationships plus "what we do" lines and the closing line, the work (ladder), standards, the Atlas underneath, one intake.
- **Lens:** static layout mock, labeled "Layout preview. No data yet." The field and the seven beat chips already work as hand-offs: they fill the intake's issue field and the hidden `lens_query`, then scroll there. `?issue=` also pre-fills. Result panel has no numbers.
- **One intake**, `#build-brief` (and `#capture-form`, an empty anchor inside it) both land on it. Fields per brief section 6. Hidden fields: `lens_query`, `referrer`, `source_page`; honeypot `_gotcha`. Still posts to the same Formspree endpoint.
- **Behavior change to flag:** the old form showed "Brief received" even when the post failed. The new one shows an error and keeps the answers. Please confirm that is what you want.
- **Icons:** the Material Symbols font is no longer loaded by this page; the one icon is an inline SVG with `aria-hidden`. The ligature words I grepped for ("summarize") appear once, as a real word in the hero copy.
- **Removed on purpose:** the 30-name scrolling ticker; the beat explorer with 28 typed creators and typed audience sizes ("200K+ subscribers"); the Pulse intel grid with typed snapshot numbers (1,756 feeds, 984 active, 1,314 posts); the "audience size data for every creator" line; three form variants; 12 of the 14 CTAs. The Pulse and Search gallery cards became two links in the ladder.
- **Meta:** new title and description (with count token), OG and Twitter tags, `<main>` landmark, one h1. OG image is still the generic one until Phase 5.
- **Flags** (`ATLAS_FLAGS` in the page script): `nn` opens on 2026-10-28 (Eastern), `?nn=1` previews it; `standards` and `lab` stay hidden until set to true. Hidden by default, so a no-JS visitor never sees draft blocks.

### Data touched
| Number | Value | Source | Note |
|---|---|---|---|
| Creator count | token, 2,415 today | site-stats.json at build | Hero dek, Method. No typed counts remain. |
| As-of date | token, October 26, 2026 | site-stats.json | Method. |
| 1 in 5 | typed | CNTI citing Pew, Sept 2024 | Link is the CNTI report; primary check in Phase 3. |
| 238 counties, 170 closures | typed | Medill 2026 | Carried from the old page. Link is Medill's site root, not the report; both need verifying in Phase 3. |
| 82%, 32% | typed | Muck Rack 2025 | Still the netinfluencer.com write-up; primary Muck Rack report not yet found. |
| 169 organizations | typed | Nodes and Networks | Date-gated. |

### CTAs: before and after
- Before: about 14 links in the body (8 to `#build-brief` under 3 labels, Pulse 6, Search 3) and 3 forms.
- After: the primary action is "Request my brief". It appears twice: the closing block of the relationships section, and the intake button. The Lens hand-off ("Get the full brief on this issue") is the third. Pulse and Search each appear once, in the ladder. Forms: 1 intake plus the Lens search field (which does not post).

### SOFT blocks (all marked `SOFT` in the HTML)
Headline and alternates; hero dek; chips (to be generated at build in Phase 2); People/Places/Machines copy and the Medill numbers; Machines figure still to add; Field Briefs name; the Lab items (hidden); the whole Standards section (hidden); team strip (James not added); Nodes and Networks link (points at /research until the paper's URL is known).

### Lighthouse (local, uncompressed; Phase 0 in brackets)
| | Perf | A11y | BP | SEO | LCP | CLS |
|---|---|---|---|---|---|---|
| Mobile | 83 (62) | 95 | 100 | 100 (92) | 4.1 s (18.9 s) | 0.098 |
| Desktop | 99 (85) | 96 | 100 | 100 (92) | 0.8 s (2.8 s) | 0.017 |
A11y flagged `aria-required-children` on my comparison list; fixed after this run (removed the table roles); not re-run. Page height at 1280 dropped from 7,663 to 6,751 px. No horizontal scroll at 390/768/1280/1600.

### Deviations to confirm
- Hero headline is `clamp(36px, 5.2vw, 64px)` Merriweather 700; v15's Display is 48px. I went bigger because the brief says the headline is the design. Needs James, or I set it to 48.
- Section claims are 28px mobile / 36px desktop (H2 is 28px in v15).
- Not yet built: Acid "live" markers on light surfaces (no live data exists until Phase 2).

### Open questions for Justin
1. Confirm the error-on-failed-post behavior.
2. Hero size: keep the larger clamp or snap to 48px?
3. The Medill links and the Muck Rack primary report: OK to search for them in Phase 3?
4. Is "Request my brief" the right label for the Lens hand-off too, or keep "Get the full brief on this issue"?

## Phase 1 revision: approved with changes (2026-10-27)
Changed: `for-brands.html` only. Nothing committed. Screens added in `for_brands_screens/phase-1/`: `fold-1280-lens-off.png`, `fold-1280-lens-on.png`, and `hero-{390,1280}-{clamp-36-64,v15-display-48}.png` for James.

1. **Lens behind `ATLAS_FLAGS.lens` (default off).** Its markup sits in a `<template>` and mounts only when the flag or `?lens=1` is on, so it is not in the page's DOM by default. With it off the hero is headline, dek and one "Request my brief" link. Checked: 0 Lens elements and no visible "layout preview" text in the default render. The string "Layout preview" still exists inside the page script (it sets the tag text when the Lens mounts); it never shows to a visitor.
2. **Labels:** the Lens hand-off reads "Request a brief on {issue}" and falls back to "Request my brief" when the field is empty (tested with "Data centers"). All other CTAs read "Request my brief" (hero, end of relationships, intake button: three).
3. **Medill:** restored `https://localnewsinitiative.northwestern.edu/projects/state-of-local-news/2026/report/` (200). Checked against the report text on 2026-10-27: "In 2026, 238 counties are news deserts" and "In the past year, 170 newspapers have closed or merged, at a rate of nearly three a week." Both numbers match the copy. My Phase 1 site-root link was a regression I introduced; fixed.
4. **Muck Rack:** the netinfluencer.com write-up returns 200 and supports both figures. 32%: "Thirty-two percent of creators view PR professionals as 'very important' to their success." 82%: "Eighty-two percent report that at least some portion of their stories originates from PR pitches, although most (45%) say these account for only 1-10% of their published work." Our wording ("some of their stories start with a PR pitch") is accurate, but the write-up's own caveat (mostly 1-10%) is worth keeping in mind for any stronger phrasing. The Muck Rack report page (`muckrack.com/research/state-of-creator-journalism`, linked from that write-up) returns a bot challenge to scripted clients, so I could not machine-check it; the page now links both it and the write-up, and the write-up remains the verified source.
5. **Lighthouse after the role fix and font change (local, uncompressed):**
   | | Perf | A11y | BP | SEO | FCP | LCP | CLS |
   |---|---|---|---|---|---|---|---|
   | Mobile before | 83 | 95 | 100 | 100 | 1.9 s | 4.1 s | 0.098 |
   | Mobile after | **95** | **100** | 100 | 100 | 1.8 s | **2.3 s** | 0.094 |
   | Desktop after | 100 | 100 | 100 | 100 | 0.6 s | 0.6 s | 0.015 |
   **Mobile LCP element:** `p.dek` (the Inter hero paragraph), not the Merriweather headline. Before: 647 ms element render delay, i.e. the paragraph waited on render-blocking CSS, chiefly the Google Fonts stylesheet. Fix: the font stylesheet now loads non-blocking (`preload` + `onload`, with a `<noscript>` fallback; `display=swap` was already set), and Merriweather loads at 700 only. After: 267 ms render delay. Two changes landed together (font loading, and the Lens leaving the default page, which shortens the hero), so I cannot say how much each contributed. CLS 0.094 is under the 0.1 line but close; it comes from the swap from fallback to web fonts.
6. **Kept:** failed-post error state (tested with the Formspree request blocked: error shown, form stays, no confirmation). Standards and Lab flags stay off.
7. **Hero type:** both versions captured for James. Current is a 36-64px range; v15 Display is 48px. Decision stays with James; Justin leans his way.

### SOFT blocks still open
Headline and alternates; hero dek; Places/Machines copy; Machines figure; Field Briefs name; Lab items (hidden); Standards (hidden); team strip; Nodes and Networks link target; Lens (hidden).

### After you push, check in a real browser
View source shows the baked-in count (no `{{CREATOR_COUNT}}`), submit the form and confirm the Formspree email arrives, and check the OG preview in Slack (still the generic image until Phase 5).

## Phase 2: the Issue Lens (2026-10-27)
Changed: `for-brands.html` (Lens markup, styles and script; Lens stays behind `ATLAS_FLAGS.lens`, default **off**; `?lens=1` previews it), NEW `scripts/build_lens_index.py`, NEW `assets/data/lens-index.json`, `build-dist.sh` (+2 lines: copies the index). Nothing committed. `build-dist.sh` already had your Pulse edits; I only added the Lens lines.
Screens: `for_brands_screens/phase-2/`: `lens-{1280,390}-{strong,thin,empty,beat,idle}.png`. Strong = "AI", thin = "data centers", empty = "Bitcoin", beat = "Politics".

### Verdict: beat level plus title-matched pieces, as you chose
Issue-level matching is honest only as "pieces with these words in the title". The index has titles, creator names, links, dates, a format and the creator's beat tags, and nothing else (no excerpt, no post-level tags). So the Lens says which it did. A query that names a beat ("Politics", "Finance", "Housing") matches creators' Atlas beat tags exactly. Anything else matches titles only, and the panel says "Matched on piece titles only". Where a beat query also appears in titles of pieces filed under other beats, the note says how many.

### Index (`assets/data/lens-index.json`)
- Built by `python3 scripts/build_lens_index.py` from `assets/data/pulse/posts-*.json`, `data/pulse-issues.json`, `creators-data.json`, `site-stats.json` and `pulse.html` (feeds). Committed, like the Pulse files, because Cloudflare only runs `build-dist.sh`. **Re-run it after each Pulse update and commit the result**, or the Lens goes stale. Not wired into the private Pulse pipeline yet (your call).
- Contents this run: **3,092 pieces, 886 creators**, window Oct 15 to Oct 21, data through Oct 22, 1,747 feeds, 79 beat tags. This matches the Pulse masthead exactly (886 creators, 3,092 pieces). **480 KB raw, 198 KB gzip.** It loads lazily on first focus or hover of the Lens, or at once if the URL carries `?issue=`; nothing loads when the Lens is off (checked: 0 requests).
- Bluesky and other social hosts are excluded (0 dropped in this window; the Pulse files already omit them; the script filters again). Creator names, outlet links and dates only: no emails, no follower counts.
- Platform mix of pieces: from URL host first (YouTube/Vimeo = video; known podcast hosts = podcast; Substack/Beehiiv/Ghost etc. = newsletter), then the creator's platform label for custom domains, else web. This window: newsletter 1,677, video 794, podcast 50, web 571. The podcast count is low because most podcasts publish on custom domains and are labeled by creator; treat it as a floor.
- Geography: creator home base (registry city + state, falling back to the Pulse geography string), 677 of 886 creators have one. Shown as a ranked list with "62 of 81 have one listed" and the caveat "home base, not story location". Not a map: coverage is 76% and national outlets have none.
- Chips are baked into the page between `<!-- LENS:CHIPS -->` markers by the script: this week's most-covered beats with at least 40 pieces and 25 creators: Politics (965), Tech (353), Local (319), Media/Power (253), Culture (217), Finance/Economics (204), World (189), Government Accountability (147).

### The Lens
- Matching is client-side: whole-word for tokens up to 3 letters, word-prefix with simple plural handling above that, all tokens required.
- Result: framing line (templated), platform mix with counts, the hub creator count, verified creators in the Atlas filed under the beat (beat queries only), three recent headlines linked to the creators' own pages with name and date, ranked places, and "Request a brief on {issue}", which pre-fills the intake.
- Framing: beat queries say "published N pieces on Politics"; title queries say "published N pieces with "AI" in the title", because "on AI" would claim more than the data shows. Counts include co-hosts, so "2 journalists published 1 piece" can occur for a co-hosted show (same rule as Pulse).
- Empty state uses your copy with the live feed count (1,747) and one honest line about matching on beat names and titles.
- URL: `?issue=` reflects the query and re-runs it on load (works for sharing; today it needs `lens=1` until the flag is on).
- Accessibility: labeled field, chips are buttons with `aria-pressed`, results announced through an `aria-live="polite"` status line, the Lens is keyboard-complete (verified: tab to a chip, Enter, URL updates, hand-off fills the intake). Visible focus on dark uses Lime.
- Motion: the only animation on the page. On each new query, thin Acid lines draw from the platform rows into the creator count, about 750 ms with a small stagger, once. Skipped under `prefers-reduced-motion` (verified: 0 lines) and below 900 px (stacked layout).

### Query test (flag on, real index)
| Kind | Query | Result |
|---|---|---|
| beat | Politics | 186 journalists, 965 pieces |
| title | AI | 81 journalists, 91 pieces |
| title | election | 43 journalists, 55 pieces |
| beat | housing | 2 journalists, 6 pieces (thin; the beat is small) |
| title (thin) | tariffs | 4 journalists, 4 pieces |
| title (thin) | data centers | 12 journalists, 13 pieces |
| empty | Bitcoin, Taylor Swift, ESPN, zxqv, NFT marketplace | all return the empty state |
Also checked: Tech, Finance (resolves to Finance/Economics, 204 pieces), quantum (1), insulin (1), shutdown (1).
Weak spots, stated plainly: a short word can match unrelated titles ("Fed" matches the verb); a topic phrased differently in titles will not match; very new topics need a Pulse refresh to appear. Nothing is model-written.

### Token plan (checked against Pulse and v15)
Palette in use (all from `variables.css`, none new): white `#fff`, Neutral gray 2 `#efefef` (light surface band), gray 3 `#c6c6c6`, gray 5 `#5e5e5e` (secondary text), gray 6 `#303030` (body, buttons), gray 7 `#121212` (dark stage), black `#000`; Acid `#ceff00` (the single "live" signal: live dot, counts in the framing line, convergence lines, hover); Lime `#97d600` (focus on dark); Dark Olive `#5d7400` (links, focus on light); error `#f50000`.
Type: Merriweather 700 (hero 36-64px clamp, claims 28/36, stat numerals, framing line 24/28), Inter 400/500/600/700 (16px body, 13-15px small), Source Code Pro 500 only on live data (counts, dates, window) and 12px status tags. Scale: v15 except the hero clamp (see below). Spacing: 4px base (16/24/32/48/64/96 used). Radius 6px; 50% only on dots and avatars. Grid: 1440 container, 32px gutter (16 on mobile), 680px text column, 2- and 3-column grids from 900px.
Pulse's tokens are the same file. Pulse restyles `.link-instruction` locally; /for-brands has no instruction links.
Mono is live data only: the Lens counts, dates and window. The creator count in the hero dek is mono because it comes from the build.

### Open for you
1. **Flip the Lens on?** It is ready for review. To ship it: set `lens: true` in `ATLAS_FLAGS`. Until then `?issue=` links do nothing but pre-fill the intake.
2. **Index freshness:** it is 5 days stale today because Pulse is (data through Oct 22). The panel says so. Should the private Pulse pipeline call `build_lens_index.py` after each run?
3. **Hero size** is still the 36-64px range pending James.
4. **Title-match limits** are in the panel copy; say if you want them softer.
5. An excerpt field in the Pulse files would let issue queries match more than titles.

### Lighthouse (local; "gzip" = a small compressing server)
| | Perf | A11y | LCP | CLS |
|---|---|---|---|---|
| Default (Lens off), gzip | 96, 96 | 100 | 1.8-1.9 s | 0.093 |
| Lens on with `?issue=AI`, gzip | 95, 84 (two runs) | 100 | 2.1 s, 3.9 s | 0.097 |
The LCP element is the hero dek in every run. Lab runs are noisy (one cold default run scored 82). The heading-order warning on the Lens (h3 after h1) was fixed (result headings are h2).
