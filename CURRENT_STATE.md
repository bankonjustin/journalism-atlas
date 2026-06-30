# Pulse — Current State
*Last updated: June 30, 2026*

## What's live

### pulse.html — Masthead v2 (shipped Jun 30, 2026)

Three-layer layout:
- **Layer 1 (masthead):** Dark full-bleed (`#111111`). Dateline, hero lede with entity highlighting, dot-field beat viz, live ticker.
- **Layer 2 (rail):** Dark, 5 signal story cards. `SIGNAL STORIES — THIS WEEK` eyebrow.
- **Layer 3 (archive):** White workspace surface. `THE FULL DIGEST` header with methodology copy + audience bridge, then `.pulse-split` archive tool.

### Entity highlighting in the lede (3 tiers)
- **Creator names** → acid green `#ceff00` (`<span class="lede-creator">`)
- **Beat names** → solid underline (`<span class="lede-beat">`)
- **Numbers / stats** → dotted underline (`<span class="lede-stat">`) — relies on `masthead.headline_stat` integer from pipeline

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
**Pending.** The current `pulse.html` is using `field_summary.text` as fallback because the pipeline has not yet been re-run to produce the new `masthead` object. Run `pulse_digest.py` to generate structured masthead data and unlock: shorter headline, supporting line, and tier-3 number highlighting.

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
