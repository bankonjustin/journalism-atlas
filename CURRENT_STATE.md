# Pulse — Current State
*Last updated: June 30, 2026 (v3.1)*

## What's live

### pulse.html — Masthead v2 (shipped Jun 30, 2026)

Three-layer layout:
- **Layer 1 (masthead):** Dark full-bleed (`#111111`). Dateline, hero editorial paragraph with entity highlighting, stat line, supporting line, dot-field beat viz, live ticker.
- **Layer 2 (signal panel):** Dark, beat-tabbed. `ALL` tab + up to 5 beat tabs, each with up to 8 stacked cards, scrollable, sparse tabs supplemented from `PULSE_DATA.posts`.
- **Layer 3 (archive):** White workspace surface. `THE FULL DIGEST` header with methodology copy + audience bridge, then `.pulse-split` archive tool.

### Hero paragraph
- Scale: `clamp(22px, 2.8vw, 30px)`, weight 700, line-height 1.4, max-width 760px
- Source: `DIGEST_DATA.masthead.headline_text` (pipeline-generated, 2-3 sentences, 45-70 words)
- Stat line below: `[N] CREATORS · [N] BEATS ACTIVE · [N] POSTS THIS WEEK` (DM Mono, 11px, all-caps)
- Supporting line: `Also this week: [creator] surged in [beat].` — hidden when absent

### Entity highlighting in the lede (3 tiers)
- **Creator names** → acid green `#ceff00`, weight 700 — scans `signal_stories[0–4]` creators
- **Beat names** → lime `#97d600` underline, 2px, word-boundary matched (`<span class="lede-beat">`)
- **Numbers / stats** → dotted muted-white underline — digit sequences + `headline_stat` written forms (`<span class="lede-stat">`)

### Signal panel (beat-tabbed)
- Tabs computed dynamically from `signal_stories` beat distribution
- Default active = `DIGEST_DATA.masthead.headline_beat`
- Sparse tabs (< 3 signal stories) supplemented from `PULSE_DATA.posts`, sorted by `signal_score`
- Beat tag clicks filter archive + scroll to it; `e.stopPropagation()` prevents card click interference
- `// TODO-JAMES: signal_reason badge color/treatment review`

### Dateline
`PULSE · VOL. 1 · JUN 21–28, 2026` — 7-day active window, computed from `PULSE_DATA.generated_at`. Vol. number is a `// TODO-JUSTIN` hardcoded constant until automated.

### Supporting line
Renders beneath the headline when `DIGEST_DATA.masthead.supporting_creator` and `supporting_beat` are both present. Hidden entirely when absent (no broken template). Phrasing: `"Also this week: [creator] surged in [beat]."` — `// TODO-LIZ` to confirm copy.

---

## Pipeline state (pulse_digest.py)

**Location:** `/Users/justinbank/Documents/Atlas Spidering/core/pulse_digest.py` (NOT in the repo)

### Current output fields
- `DIGEST_DATA.signal_stories` — top 8 ranked posts (7-factor scoring)
- `DIGEST_DATA.field_summary.text` — kept for backwards compat; now a single headline sentence (≤20 words)
- `DIGEST_DATA.masthead` — **new in this session**:
  - `headline_text` — single sentence from Claude (≤20 words, AP wire style)
  - `headline_beat`, `headline_creator`, `headline_stat` (integer post count)
  - `supporting_creator`, `supporting_beat` (from signal_stories[1])
  - `headline_reason`, `date`

### Pipeline re-run status
**Current.** Last run Jun 30, 2026. Outputs `masthead` object and 20 signal stories. `field_summary.text` kept as fallback but no longer primary. `headline_stat` is a real computed integer (post count for top creator). Paragraph prompt has 70-word ceiling instruction + Python post-trim safety net (fires only if model overshoots).

---

## Open flags in code
- `// TODO-JUSTIN: increment VOL. number per edition until automated` — in `renderMasthead()`
- `// TODO-LIZ: confirm archive section copy` — in `.archive-method` paragraph
- `// TODO-LIZ: confirm phrasing of supporting line` — in `renderMasthead()`

---

## Removed (replaced in Jun 2026 session)
- `.page-header` band
- `.pulse-thesis-band`
- `#signal-band`
- `#field-summary-band`
- `.audience-bridge-v2` (relocated into `.archive-header`)
