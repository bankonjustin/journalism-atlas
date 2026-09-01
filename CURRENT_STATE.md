# Pulse — Current State
*Last updated: August 24, 2026 (hero/header container layout fix)*

## Role-scoped subagents (in progress)

- **Ryan (`ryan-dataops`)** — built, `.claude/agents/ryan-dataops.md` in this repo. Scoped to `creators-master.csv`, `atlas-private-columns.csv`, `DATA-OPS-PROTOCOL.md`. No Bash tool (hard block, not just an instruction) — cannot run `atlas_groups.py`, `atlas_append.py`, or anything else.
  - **Correction (July 8, 2026, repo sweep):** `atlas-private-columns.csv` is no longer at `~/Downloads/`. As of the July 7 private-repo setup it's the live file at `journalism-atlas-private/data/atlas-private-columns.csv` (Ryan edits it there directly; see `DATA-OPS-PROTOCOL.md` and the private repo's `HANDOFF.md`). **`ryan-dataops.md`'s own "In scope" section still says `~/Downloads/atlas-private-columns.csv` — that file itself was not updated when the migration happened and needs a fix**, tracked as a follow-up, not done in this sweep.
- **Liz (`liz-editorial`)** — built, `.claude/agents/liz-editorial.md` in the Atlas Spidering workspace (not this repo).
  - **Correction (July 8, 2026, repo sweep):** the narrow read-only scope described below (two files, `~/Downloads/` mirror) was superseded same-day by a Session 3 rebuild — see `Atlas Spidering/sessions/CURRENT_STATE.md`. Liz now has full read access (Read/Grep/Glob only, still no Bash/Write/Edit) across all three locations: this repo, `journalism-atlas-private/` (including `atlas-private-columns.csv`), and `Atlas Spidering/`. The `~/Downloads/ATLAS-EDITORIAL-STANDARDS-v1_4.md` mirror referenced below is retired (archived to `~/Downloads/_archive_editorial_standards/`) — she now reads the private repo's `docs/ATLAS-EDITORIAL-STANDARDS-vX.Y.md` directly. Original entry preserved below for history.
  - ~~**Read-only**: `~/Downloads/ATLAS-EDITORIAL-STANDARDS-v1_4.md` + the Global Correspondents session note (`Atlas Spidering/sessions/row_bluesky_global_correspondents_clusters_2026-07-02.md`). No Bash/Write/Edit tools.~~ (superseded, see correction above)
  - **Editorial standards doc** — corrects an earlier wrong claim in this file: it does NOT live in this repo's `_reference/` (guessed from the `james-design-principles.md` pattern — checked, wrong). It's in `~/Downloads/`, same pattern as `atlas-private-columns.csv`. Four versions exist there (v1.1, v1.3 ×2, v1.4); Justin chose **v1.4** (touched July 7, the newest). *(Historical — both docs have since moved into `journalism-atlas-private/docs/`.)*
  - **Global Correspondents cluster output has no canonical, updating file** — still just the one-off session note. Liz's subagent is scoped to it as-is; tracked as an open item in `Atlas Spidering/sessions/CURRENT_STATE.md`.
  - **Shadow Lists AND rejection notes — both out of scope, confirmed as one blocker, not two.** Per `DATA-OPS-PROTOCOL.md`, rejection notes are also canonically a Google Sheet, not a local file — so this isn't just a Shadow Lists gap. No Sheets connector exists anywhere (registry search empty; Justin confirmed directly in claude.ai/Claude Code settings, July 7). No local file was invented as a workaround. Revisit `liz-editorial.md`'s tool scope once a Sheets connector path exists.

## Site maintenance

### Hero/header container layout fix (Aug 24, 2026)

James's Aug 2026 layout-fix brief + `DESIGN-TOKENS-v10.md` claimed 5 hero/first-module sections (Home, Pulse, For Brands, Research & Writing, Contact) plus the site header were escaping the locked `full layout` (1440px) container. Verified each against the actual repo (via local preview + computed `getBoundingClientRect()`, not just reading CSS) before touching anything, per the brief's own "confirm before trusting" instructions. Result: most of it was already fixed in an earlier session; only two real bugs found.

**Fixed:**
- `index.html` — `.hero` was a full-bleed, unconstrained `display:grid` (no max-width). The "Verified Creators" stat badge, absolutely positioned inside the right column, rendered flush to the true browser edge. Wrapped both columns in a new `.hero-container { max-width:1440px; margin:0 auto }`; `.hero` itself keeps its full-bleed black background so the dark-stage look is unchanged, just letterbox-free. Moved the `768px` mobile breakpoint's `grid-template-columns: 1fr` override from `.hero` to `.hero-container` to match.
- `contact.html` — `.contact-hero-inner` was `max-width:680px` with no `margin:auto`, i.e. left-aligned at the section's own 40px padding, not the shared container edge. Read fine only because nothing competed for the right side (as the brief itself noted). Changed to `max-width:1440px; margin:0 auto` — now sits at the identical left offset as the header logo and footer at 1920px viewport (both 240px).

**Found already correct, not touched:** Pulse's masthead (`.masthead-inner`), For Brands' hero (`.section-inner`), and both pages' full-bleed ticker/marquee (already have `mask-image` edge fades — the exact "if intentional, fade the edges" treatment the brief asked for). The site header/footer container claim ("logo sits well left of the container edge") was **not reproducible** — `.nav-container` and `.footer-inner` are both already `max-width:1440px; margin:0 auto` and compute to the same 240px/1680px offsets at 1920px viewport. Likely fixed in a prior session; the brief's screenshots may predate that fix.

**Deliberately left alone (flagged, not fixed):**
- `research.html`'s hero uses an intentional 1100px editorial container (not full-bleed, just narrower than 1440px) — doesn't match the "escaping the container" defect, and changing it would be a design call outside this brief's scope. Its "FROM PROJECT C" row is an auto-scrolling marquee with the same edge-fade pattern as Pulse/For Brands, not a static clipped carousel — not a bug.
- Header's *internal* nav spacing (`DESIGN-TOKENS.md` § Header Nav Spacing) does not yet match the suggested 48/48/32/24px gaps — current values are 32px (logo→search) and a uniform 40px between all nav links. This is a pure spacing tweak independent of the container fix and wasn't applied this pass.
- `bluesky-creator-intelligence.html` has the **same unconstrained full-bleed `.hero` grid bug** as index.html did (`display:grid; grid-template-columns:1fr 440px`, no max-width). Not in the brief's named page list, so not fixed — flagging since it's the same regression class.

**Docs:** `DESIGN-TOKENS.md` was *not* overwritten with the supplied `DESIGN-TOKENS-v10.md` — the committed file (self-labeled v8) already contained Aug 1, 2026 entries (footer grid rebuild, SVG logo swap, Source Code Pro scoping) that v10's lineage doesn't have, so overwriting would have deleted real history. Merged v10's actual new content (Container Inner Padding, the Max Content Width implementation note, Header Nav Spacing table) into the existing file instead, plus a version-numbering note flagging the fork to James. `CLAUDE.md`'s "Non-negotiable rules" section (still says font weights 400/500/700, 100px pill radius) is out of sync with `DESIGN-TOKENS.md`/v10 (600/700/800, 9999px) — Justin's own brief flagged this as a separate follow-up, not done here.

Not pushed — changes are local only, per usual (Justin pushes via GitHub Desktop).

### Stale creator-count cleanup + future-proofing (July 7, 2026)

Master crossed from 1,718 → 1,806 rows across several deploy cycles; several site surfaces had hardcoded the older count as text instead of reading it live. Two categories fixed differently, per `CLAUDE.md`'s Creator Count Convention:

- **Bug fixes (JSON-backed pages, should have been dynamic already):**
  - `index.html:1381` — CTA `<h2>` had a bare `1,718 creators` string outside any `.js-creator-count` span (every other instance on the page was already wired correctly). Wrapped it.
  - `research.html` — had **no** `creators-data.json` fetch at all despite two hardcoded `1,718` strings (hero CTA + section subhead). Added the same lightweight fetch snippet used by `for-brands.html`, wrapped both strings in `.js-creator-count`.
  - `wire.html` — `updateFooter()` computed a `creators` variable (distinct creators in *today's wire feed*) but discarded it and hardcoded `'1,500+'` in the footer — badly stale, and the wrong metric anyway (wire-subset vs. site-wide total). Now fetches `creators-data.json` directly and populates both `#footer-count` and a newly-added `.js-creator-count` span in the hero subhead with the true site-wide total.
- **Static milestone bumps (meta/OG/Twitter tags + partner attribution strings — intentionally not dynamic, per convention):** `index.html`, `lists.html`, `mobile.html` meta descriptions, and all `partners/*.html` (+ `_shell.html` template) attribution strings bumped from `1,700+` → `1,800+`.
- **Correction to a prior assumption:** `mobile.html` is NOT retired — it's live and required to fetch `creators-data.json` per `CLAUDE.md`'s Key Constraints. A brief for this session incorrectly assumed otherwise; verified against the file and CLAUDE.md directly before proceeding.
- **New standing tool:** [`pipeline/update_partner_totals.py`](pipeline/update_partner_totals.py) — run this after any deploy that crosses a new hundred-milestone (e.g. 1,806 → 1,900+). Dry-run by default (prints a diff); `--apply` writes. Regex-matches any `N,NNN+ creator-journalists` string across `partners/*.html`, so it doesn't need the old value hardcoded. Partner pages remain fetch-free by design — this script is the substitute for that constraint, not a workaround of it.
- **`convert.js` now also writes `assets/data/site-stats.json`** on every run (`totalCreators`, `topicCount`, `platformCount`, `lastUpdated`) — a canonical source for future stat-strip numbers so new pages don't need to fetch/parse the full `creators-data.json` array or hardcode a count.
- Not touched, flagged only: `atlas-portal/index.html`'s "over 1,000 others" social-share testimonial copy (ambiguous whether literal or evocative), and `how-we-did-this.html`'s "approximately 1,000 creators" (describes the original v1 launch dataset — historical record, not a live count).

### postcard.html retired (July 6, 2026)
- Mothballed, not rebuilt: `postcard.html` had no traffic, only a leftover footer link, and stale creator-count copy (1,006/1,100+ vs. current 1,718).
- Moved to `_deprecated/postcard.html`. `/postcard` and `/postcard.html` now 301 to `/` via `_redirects`.
- **Also removed `functions/postcard.js`** (moved to `_deprecated/functions-postcard.js`) — this Cloudflare Pages Function intercepted every `/postcard` request at the edge to inject OG tags, and Functions take precedence over `_redirects`. Without removing it, the new redirect would never have fired. Verified locally with `wrangler pages dev` (`GET /postcard` → `301 Location: /`) before this was caught — not something the original brief anticipated.
- Removed the two remaining live links: `assets/js/footer.js` (footer nav) and `index.html` cluster-drawer "Build a starter pack →" link + its JS wiring (the latter wasn't in the shared footer, easy to miss).
- Reference for future work: `postcard.html`'s curate-and-share interaction pattern is the intended reference point for the September creator profile card system (per `CLAUDE.md` Out of Scope) — no design/spec work on that system was done in this session.

### pack.html + knight-brief.html also retired (July 6, 2026, same session)
- Justin decided to mothball both once he saw `postcard.html`'s retirement — same pattern applied.
- `pack.html`: a separate, older full creator-database + curate-and-share view, unrelated to `postcard.html` despite similar functionality (self-contained inline JS, own fetch of `creators-data.json`). Never linked from live nav. Its canonical `/pack` URL was already being shadowed by the old `/pack → /postcard` redirect, so it was effectively unreachable via clean URL already. Moved to `_deprecated/pack.html`; `/pack` and `/pack.html` now redirect to `/` directly (old `/pack → /postcard` chain removed).
- `knight-brief.html`: internal Knight Foundation pitch brief, not linked from anywhere live (this resolves the deferred "Postcard Generator" link question from earlier — moot now that the whole page is archived, no content edit needed). Moved to `_deprecated/knight-brief.html`; `/knight-brief` and `/knight-brief.html` now redirect to `/`.
- `main.js`'s `renderPackCanvas`/`packPreviewCanvas` feature — embedded directly in `search.html`, **not** part of `pack.html` — is untouched and still live.
- Not verified against production `wrangler pages dev` this round (no new Functions or Function-vs-redirect conflicts involved, unlike `postcard.html`) — worth a quick post-deploy spot check on `/pack` and `/knight-brief` anyway.

## What's live

### pulse.html — Masthead v6 (shipped Jul 1, 2026)

Three-layer layout:
- **Layer 1 (masthead):** Dark full-bleed (`#111111`). Dateline, hero editorial paragraph with entity links, corpus-first topic cluster stack, beat coverage map, live ticker.
- **Layer 2 (signal panel):** Dark, beat-tabbed. `ALL` tab + up to 5 beat tabs, each with up to 8 stacked cards, scrollable, sparse tabs supplemented from `PULSE_DATA.posts`.
- **Layer 3 (archive):** White workspace surface. `THE FULL DIGEST` header with methodology copy + audience bridge, then `.pulse-split` archive tool.

### Hero paragraph
- Scale: `clamp(22px, 2.8vw, 30px)`, weight 700, line-height 1.4, max-width 760px
- Source: `DIGEST_DATA.masthead.headline_text` (pipeline-generated, 2-3 sentences, 45-70 words)

### Entity highlighting in the lede (3 tiers)
- **Creator names** → `<a class="lede-creator">`, acid green `#ceff00`, weight 700, `/search.html` (new tab). Scans `signal_stories[0–9]` creator + channel. `// TODO-JUSTIN: wire search.html ?q= param`
- **Beat names** → `<a class="lede-beat">`, white + lime 2px border-bottom, triggers in-page beat filter + archive scroll.
- **Numbers** → `<span class="lede-stat">`, dotted underline, no link.

### Corpus-first topic cluster stack (v6)
- `<div class="masthead-story-stack" id="masthead-story-stack">` — below lede, above beat map
- **Algorithm:** Full `PULSE_DATA.posts` corpus (2,691 posts) → group by primary topic → deduplicate to one post per creator (recency sort) → rank by unique creator count → top 8 clusters with min 3 unique creators.
- **Sparse fallback:** if fewer than 4 pass the min-3 floor, show top 6 buckets regardless of creator count.
- **Rendering:** beat pill + `N CREATORS THIS WEEK` (acid green) + name row (max 6 names, `+N more` overflow). No title fragments — names only.
- Lede-featured creators excluded from name rows but **counted** in the total (numbers stay honest).
- Beat pills: `canonicalizeBeat()` normalizes raw topic → canonical archive pill. `no-filter` class on unmatched beats.
- Console log: `[Pulse v6] Corpus clusters: [...]` before render — topic + creator count for each cluster.
- Current week top 8: Politics (117), Tech (72), Climate/Environment (50), Media/Power (37), Finance/Economics (36), Local (35), Health/Wellness (33), Science (28).
- `// TODO-JUSTIN: wire search.html ?q= param` on creator links.

### Beat coverage map (v5, contrast improved v6)
- Top 8 beats from `beat_trends` by post count, proportional bars, labeled and clickable.
- Labels: `rgba(255,255,255,0.70)` (bumped from 0.45). Counts: `rgba(255,255,255,0.55)` (bumped from 0.35).
- `headline_beat` bar gets `is-headline-beat` (55% opacity). `+ N MORE` for overflow.

### Signal panel (beat-tabbed)
- Tabs from `signal_stories` beat distribution. Default = `headline_beat`.
- Sparse tabs supplemented from `PULSE_DATA.posts` by `signal_score`.
- `// TODO-JAMES: signal_reason badge color/treatment review`

### Dateline
`PULSE · VOL. 1 · JUN 21–28, 2026` — 7-day window from `PULSE_DATA.generated_at`.
`// TODO-JUSTIN: increment VOL. number per edition until automated`

---

## Pipeline state (pulse_digest.py)

**Location:** `/Users/justinbank/Documents/Atlas Spidering/core/pulse_digest.py` (NOT in the repo)

### Current output fields
- `DIGEST_DATA.signal_stories` — top 20 ranked posts (cap pending raise to 30 — `// TODO` in py file)
- `DIGEST_DATA.masthead` — `headline_text`, `headline_beat`, `headline_creator`, `headline_stat`, `supporting_creator`, `supporting_beat`, `headline_reason`, `date`

### Pipeline TODO
- Raise `signal_stories` cap: `if len(signal_stories) >= 20:` → `>= 30:` (brief v6 item — not yet applied to py file outside repo)

---

## Open flags in code
- `// TODO-JUSTIN: increment VOL. number per edition until automated` — in `renderMasthead()`
- `// TODO-JUSTIN: wire search.html ?q= param` — in lede creator links + corpus cluster name links
- `// TODO-LIZ: confirm archive section copy` — in `.archive-method` paragraph
- `// TODO-JAMES: signal_reason badge color/treatment review` — in signal panel card template

---

## Removed across sessions
- `.page-header`, `.pulse-thesis-band`, `#signal-band`, `#field-summary-band`
- `.audience-bridge-v2` (relocated into `.archive-header`)
- `#masthead-supporting` (v4 — replaced by story stack)
- `.masthead-stat-line` (v5 — data visible in beat map)
- `.masthead-dot-field` / `renderDotField()` (v5 — replaced by `renderBeatMap()`)
- Signal-story-sourced `renderStoryStack` algorithm (v6 — replaced by corpus-first)
