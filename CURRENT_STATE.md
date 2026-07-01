# Pulse — Current State
*Last updated: July 1, 2026 (v5)*

## What's live

### pulse.html — Masthead v5 (shipped Jul 1, 2026)

Three-layer layout:
- **Layer 1 (masthead):** Dark full-bleed (`#111111`). Dateline, hero editorial paragraph with entity links, co-coverage cluster stack, beat coverage map, live ticker.
- **Layer 2 (signal panel):** Dark, beat-tabbed. `ALL` tab + up to 5 beat tabs, each with up to 8 stacked cards, scrollable, sparse tabs supplemented from `PULSE_DATA.posts`.
- **Layer 3 (archive):** White workspace surface. `THE FULL DIGEST` header with methodology copy + audience bridge, then `.pulse-split` archive tool.

### Hero paragraph
- Scale: `clamp(22px, 2.8vw, 30px)`, weight 700, line-height 1.4, max-width 760px
- Source: `DIGEST_DATA.masthead.headline_text` (pipeline-generated, 2-3 sentences, 45-70 words)

### Entity highlighting in the lede (3 tiers) — creator scan extended to signal_stories[0–9]
- **Creator names** → `<a class="lede-creator">`, acid green `#ceff00`, weight 700, links to `/search.html` (new tab). Scans `signal_stories[0–9]` creator + channel fields. `// TODO-JUSTIN: wire search.html ?q= param`
- **Beat names** → `<a class="lede-beat">`, white + lime `#97d600` 2px bottom border, triggers in-page beat filter + archive scroll on click.
- **Numbers / stats** → `<span class="lede-stat">`, dotted underline, no link.

### Co-coverage cluster stack (v5 — replaces single-line story stack)
- `<div class="masthead-story-stack" id="masthead-story-stack">` — below lede, above beat map
- **Clustering mode** (when ≥4 candidates and ≥1 beat has 2+ stories): groups by primary beat, shows multi-creator clusters with acid-green "N VOICES THIS WEEK" label. Max 3 display items (clusters first, singles fill remaining slots).
- **Cluster visual:** lime left border `rgba(206,255,0,0.2)`, beat pill header, voice count in `#ceff00`, creator lines in acid green (linked), em-dash separator, title linked to story URL.
- **Sparse fallback** (< 4 candidates or no multi-story beats): v4 single-line format.
- Beat pills in cluster headers trigger beat filter + archive scroll; only wired when beat has a canonical pill match.
- Beat normalization: `"Local"` → `"Local News"` (only known discrepancy in current data).
- Skips creators already named in the lede text (textContent scan) + `headline_creator` + `supporting_creator`.
- `// TODO-JUSTIN: wire search.html ?q= param` on creator links.

### Beat coverage map (v5 — replaces dot field)
- `<div class="masthead-beat-map" id="masthead-beat-map">` — below cluster stack, above ticker
- Top 8 beats from `beat_trends` by post count, proportional horizontal bars.
- Label (DM Mono 9px, 45% white) + bar track (8% white) + bar fill (acid green 30% opacity) + count.
- `headline_beat` bar gets `is-headline-beat` class → 55% opacity (brighter). Only fires when headline beat appears in top 8.
- "+ N MORE" label when `beat_trends` has >8 entries.
- Clicking any bar triggers beat filter + archive scroll. Non-canonical beats (no matching pill) get `.no-filter` and no click handler.
- Mobile: label width reduces to 100px, min-width to 140px; flex-wrap handles layout.

### Signal panel (beat-tabbed)
- Tabs computed dynamically from `signal_stories` beat distribution
- Default active = `DIGEST_DATA.masthead.headline_beat`
- Sparse tabs (< 3 signal stories) supplemented from `PULSE_DATA.posts`, sorted by `signal_score`
- Beat tag clicks filter archive + scroll to it; `e.stopPropagation()` prevents card click interference
- `// TODO-JAMES: signal_reason badge color/treatment review`

### Dateline
`PULSE · VOL. 1 · JUN 21–28, 2026` — 7-day active window, computed from `PULSE_DATA.generated_at`.
`// TODO-JUSTIN: increment VOL. number per edition until automated`

---

## Pipeline state (pulse_digest.py)

**Location:** `/Users/justinbank/Documents/Atlas Spidering/core/pulse_digest.py` (NOT in the repo)

### Current output fields
- `DIGEST_DATA.signal_stories` — top 20 ranked posts (7-factor scoring)
- `DIGEST_DATA.field_summary.text` — kept for backwards compat
- `DIGEST_DATA.masthead` — `headline_text`, `headline_beat`, `headline_creator`, `headline_stat`, `supporting_creator`, `supporting_beat`, `headline_reason`, `date`

### Pipeline re-run status
**Current.** Last run Jun 30, 2026. 20 signal stories. Paragraph prompt has 70-word ceiling + Python post-trim safety net.

---

## Open flags in code
- `// TODO-JUSTIN: increment VOL. number per edition until automated` — in `renderMasthead()`
- `// TODO-JUSTIN: wire search.html ?q= param` — in `applyLedeHighlights()`, `renderStoryStack()` creator `href` values
- `// TODO-LIZ: confirm archive section copy` — in `.archive-method` paragraph
- `// TODO-JAMES: signal_reason badge color/treatment review` — in signal panel card template

---

## Removed (replaced across sessions)
- `.page-header` band
- `.pulse-thesis-band`
- `#signal-band`
- `#field-summary-band`
- `.audience-bridge-v2` (relocated into `.archive-header`)
- `#masthead-supporting` / `.masthead-supporting` (replaced by `#masthead-story-stack`)
- `.masthead-stat-line` — removed v5 (data now visible in beat map)
- `.masthead-dot-field` / `renderDotField()` — removed v5 (replaced by `renderBeatMap()`)
