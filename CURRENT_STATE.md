# Pulse — Current State
*Last updated: July 6, 2026 (postcard.html retirement)*

## Site maintenance

### postcard.html retired (July 6, 2026)
- Mothballed, not rebuilt: `postcard.html` had no traffic, only a leftover footer link, and stale creator-count copy (1,006/1,100+ vs. current 1,718).
- Moved to `_deprecated/postcard.html`. `/postcard` and `/postcard.html` now 301 to `/` via `_redirects`.
- **Also removed `functions/postcard.js`** (moved to `_deprecated/functions-postcard.js`) — this Cloudflare Pages Function intercepted every `/postcard` request at the edge to inject OG tags, and Functions take precedence over `_redirects`. Without removing it, the new redirect would never have fired. Verified locally with `wrangler pages dev` (`GET /postcard` → `301 Location: /`) before this was caught — not something the original brief anticipated.
- Removed the two remaining live links: `assets/js/footer.js` (footer nav) and `index.html` cluster-drawer "Build a starter pack →" link + its JS wiring (the latter wasn't in the shared footer, easy to miss).
- Left untouched, unrelated: `pack.html` (a different, still-active creator-curation feature using `main.js`'s `renderPackCanvas`) and its pre-existing `/pack → /postcard` redirect — now a harmless double-hop (`/pack` → `/postcard` → `/`).
- **Open decision, deferred by Justin mid-session:** `knight-brief.html` (internal, non-public pitch doc) still pitches "Postcard Generator" as a live product with a link to `/postcard`. Needs a decision — leave as-is, fix the link to `/`, or remove the pitch section entirely.
- Reference for future work: `postcard.html`'s curate-and-share interaction pattern is the intended reference point for the September creator profile card system (per `CLAUDE.md` Out of Scope) — no design/spec work on that system was done in this session.

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
