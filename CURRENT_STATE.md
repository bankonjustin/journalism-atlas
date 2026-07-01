# Pulse — Current State
*Last updated: June 30, 2026 (v4)*

## What's live

### pulse.html — Masthead v4 (shipped Jun 30, 2026)

Three-layer layout:
- **Layer 1 (masthead):** Dark full-bleed (`#111111`). Dateline, hero editorial paragraph with entity links, story stack, stat line, dot-field beat viz, live ticker.
- **Layer 2 (signal panel):** Dark, beat-tabbed. `ALL` tab + up to 5 beat tabs, each with up to 8 stacked cards, scrollable, sparse tabs supplemented from `PULSE_DATA.posts`.
- **Layer 3 (archive):** White workspace surface. `THE FULL DIGEST` header with methodology copy + audience bridge, then `.pulse-split` archive tool.

### Hero paragraph
- Scale: `clamp(22px, 2.8vw, 30px)`, weight 700, line-height 1.4, max-width 760px
- Source: `DIGEST_DATA.masthead.headline_text` (pipeline-generated, 2-3 sentences, 45-70 words)
- Stat line below: `[N] CREATORS · [N] BEATS ACTIVE · [N] POSTS THIS WEEK` (DM Mono, 11px, all-caps)

### Entity highlighting in the lede (3 tiers) — v4: all entities are now `<a>` tags or `<span>`
- **Creator names** → `<a class="lede-creator">`, acid green `#ceff00`, weight 700, links to `/search.html` (new tab). Scans `signal_stories[0–4]` creators. `// TODO-JUSTIN: wire search.html ?q= param` — currently links bare `/search.html`.
- **Beat names** → `<a class="lede-beat">`, white text + lime `#97d600` 2px bottom border, triggers in-page beat filter + archive scroll on click (no new tab). Word-boundary matched.
- **Numbers / stats** → `<span class="lede-stat">`, dotted muted-white underline, no link (context, not navigation).

### Story stack (v4 — replaces "Also this week" line)
- `<div class="masthead-story-stack" id="masthead-story-stack">` — below lede, above stat line
- Renders 3–4 signal stories: `[CREATOR LINK] · [TITLE LINK] [BEAT PILL]`
- Skips creators already named in the lede text (scanned from rendered `textContent`) + `headline_creator` + `supporting_creator`
- Supplements from `PULSE_DATA.posts` (by `signal_score` desc) if fewer than 3 candidates
- Hidden entirely if fewer than 2 signal stories available (Placeholder Principle)
- Beat pills trigger same filter + archive scroll as signal panel tab clicks
- Title truncated at 70 chars with ellipsis
- `// TODO-JUSTIN: wire search.html ?q= param` on creator links (same as lede)

### Signal panel (beat-tabbed)
- Tabs computed dynamically from `signal_stories` beat distribution
- Default active = `DIGEST_DATA.masthead.headline_beat`
- Sparse tabs (< 3 signal stories) supplemented from `PULSE_DATA.posts`, sorted by `signal_score`
- Beat tag clicks filter archive + scroll to it; `e.stopPropagation()` prevents card click interference
- `// TODO-JAMES: signal_reason badge color/treatment review`

### Dateline
`PULSE · VOL. 1 · JUN 21–28, 2026` — 7-day active window, computed from `PULSE_DATA.generated_at`. Vol. number is a `// TODO-JUSTIN` hardcoded constant until automated.

---

## Pipeline state (pulse_digest.py)

**Location:** `/Users/justinbank/Documents/Atlas Spidering/core/pulse_digest.py` (NOT in the repo)

### Current output fields
- `DIGEST_DATA.signal_stories` — top 20 ranked posts (7-factor scoring)
- `DIGEST_DATA.field_summary.text` — kept for backwards compat; now a single headline sentence (≤20 words)
- `DIGEST_DATA.masthead` — structured object:
  - `headline_text` — editorial paragraph from Claude (2–3 sentences, 45–70 words)
  - `headline_beat`, `headline_creator`, `headline_stat` (integer post count)
  - `supporting_creator`, `supporting_beat` (from signal_stories[1])
  - `headline_reason`, `date`

### Pipeline re-run status
**Current.** Last run Jun 30, 2026. Outputs `masthead` object and 20 signal stories. `field_summary.text` kept as fallback but no longer primary. `headline_stat` is a real computed integer (post count for top creator). Paragraph prompt has 70-word ceiling instruction + Python post-trim safety net.

---

## Open flags in code
- `// TODO-JUSTIN: increment VOL. number per edition until automated` — in `renderMasthead()`
- `// TODO-JUSTIN: wire search.html ?q= param` — in `applyLedeHighlights()` and `renderStoryStack()` creator `href` values
- `// TODO-LIZ: confirm archive section copy` — in `.archive-method` paragraph
- `// TODO-JAMES: signal_reason badge color/treatment review` — in signal panel card template

---

## Removed (replaced in Jun 2026 session)
- `.page-header` band
- `.pulse-thesis-band`
- `#signal-band`
- `#field-summary-band`
- `.audience-bridge-v2` (relocated into `.archive-header`)
- `#masthead-supporting` / `.masthead-supporting` (replaced by `#masthead-story-stack`)
