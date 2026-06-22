# Atlas Intelligence System — State Map
**Last updated:** 2026-06-22  
**Author:** Claude Code (session audit)  
**Purpose:** Design document for merging Pulse + Wire into a unified intelligence dashboard.

---

## 1. Pipeline Inventory

### Pulse Pipeline (Weekly — Scheduled Sunday 9am)

**Entry point:** `/Users/justinbank/Documents/Atlas Spidering/core/refresh_pulse.sh`

| Step | Script | Location | Input | Output |
|------|--------|----------|-------|--------|
| 1 — Scrape | `pulse_v2.py` | Spidering/core/ | RSS feeds (1,589 creators) | `rss_pulse_v2_YYYYMMDD.json` (core/) |
| 2 — Update HTML | `update_pulse.py` | Spidering/core/ | `rss_pulse_v2_*.json` | Updates `pulse.html`, `index.html`, `for-brands.html` in journalism-atlas repo |
| 3 — Digest | `pulse_digest.py` | Spidering/core/ | `rss_pulse_v2_*.json` | `pulse_digest_YYYYMMDD.json` (core/), injected into `pulse.html` |
| 4 — Spidering brief | `pulse_spidering_brief.py` | Spidering/core/ | `rss_pulse_v2_*.json` | `sessions/SPIDERING_BRIEF_YYYYMMDD.md`, `beat_activity_log.csv` |

**Output files land in:** `/Users/justinbank/Documents/Atlas Spidering/core/`  
**Public files updated in:** `/Users/justinbank/Documents/GitHub/journalism-atlas/`  
**Steps 3 and 4 are non-fatal** (patched 2026-06-22 with `|| true`) — pipeline continues on digest or brief failure.  
**Step 3 max_tokens:** bumped to 8192 (primary call) and 4096 (verification call) on 2026-06-22.

### Wire Pipeline (Manual — as needed)

**Entry point:** Run scripts directly from `journalism-atlas/` repo root.

| Step | Script | Location | Input | Output |
|------|--------|----------|-------|--------|
| 1 — RSS fetch | `atlas-pulse/pulse_fetch.py` | journalism-atlas/atlas-pulse/ | `atlas_rss_universe.csv` | `atlas-pulse/pulse_output.json` (nested format — LEGACY) |
| 2 — Fetch + merge | `atlas_wire_fetch.py` | journalism-atlas/ | `atlas-pulse/pulse_output.json` + Bluesky API | `wire_queue_raw_YYYY-MM-DD.json` |
| 3 — AI rank | `atlas_wire_rank.py` | journalism-atlas/ | `wire_queue_raw_*.json` | `wire_queue_scored_YYYY-MM-DD.json` |
| 4 — Review | `atlas_wire_intelligence.html` | journalism-atlas/ | `wire_queue_scored_*.json` (file-picker) | `wire_approved_YYYY-MM-DD.json` |
| 5 — Post | `atlas_wire_post.py` | journalism-atlas/ | `wire_approved_*.json` | `wire.json` → injected into `wire.html` (deployed) |

**Note:** `atlas_wire_fetch.py` currently reads the LEGACY nested format from `atlas-pulse/pulse_output.json`. As of this session, it will be updated to read the canonical flat format (`rss_pulse_v2_*.json`) from the Spidering/core/ directory.

### Supporting Scripts

| Script | Purpose |
|--------|---------|
| `bsky_enrichment.py` | Bluesky handle enrichment |
| `convert_bluesky.py` | Converts Bluesky data format |
| `rebuild_bluesky_json.py` | Rebuilds Bluesky creator JSON |

---

## 2. Data Compatibility — Field-by-Field

### Pulse post (`rss_pulse_v2_*.json`) — `posts[]` array

```json
{
  "creator":   "Creator Name",
  "channel":   "Publication/Channel Name",
  "title":     "Post title",
  "url":       "https://...",
  "published": "2026-06-21",
  "summary":   "<p>HTML summary...</p>",
  "topic":     "Politics, Local",
  "geography": "New Jersey - US",
  "platform":  "Website"
}
```

Top-level structure: `{ generated_at, window_days, total_creators, total_rss_resolved, total_posts, active_7d, active_30d, dark_creators, dark_count, beat_activity, recency, cross_signal, cross_signal_count, feed_health, posts[] }`

### Wire scored item (`wire_queue_scored_*.json`) — root array

```json
{
  "id":                    "uuid",
  "source":                "rss" | "bsky",
  "creator_name":          "Creator Name",
  "creator_url":           "https://feed-url...",
  "bluesky_handle":        "handle.bsky.social",
  "beat":                  "Politics",
  "title":                 "Post title",
  "link":                  "https://...",
  "text_snippet":          "Plain text excerpt...",
  "pub_date":              "2026-06-17T00:09:38",
  "score":                 9.1,
  "wire_frame":            "📰 Creator on Beat: One-liner\n→ url\n#AtlasWire",
  "cluster":               "cluster-name",
  "status":                "pending" | "approved" | "killed",
  "score_newsworthiness":  8.5,
  "score_distinctiveness": 9.0,
  "score_atlas_fit":       9.5,
  "score_timeliness":      9.5,
  "cluster_thread_opener": true | false | null
}
```

### Field Mapping Table

| Concept | Pulse field | Wire field | Notes |
|---------|-------------|------------|-------|
| Creator name | `creator` | `creator_name` | Same value |
| Publication | `channel` | — | Pulse-only |
| Beat / topic | `topic` | `beat` | Same semantics; may contain comma-separated values |
| Post URL | `url` | `link` | **Join key** for cross-referencing |
| Title | `title` | `title` | Same |
| Excerpt / body | `summary` | `text_snippet` | Pulse = HTML; Wire = plain text |
| Published date | `published` | `pub_date` | Pulse = date string; Wire = ISO datetime |
| Geography | `geography` | — | Pulse-only |
| Platform | `platform` | — | Pulse-only |
| Source platform | — | `source` | Wire-only ("rss" / "bsky") |
| Bluesky handle | — | `bluesky_handle` | Wire-only |
| Creator feed URL | — | `creator_url` | Wire-only |
| Wire score | — | `score` | Wire-only |
| Sub-scores | — | `score_*` (×4) | Wire-only |
| Wire draft copy | — | `wire_frame` | Wire-only |
| Cluster | — | `cluster` | Wire-only |
| Review status | — | `status` | Wire-only |
| Item ID | — | `id` | Wire-only (UUID) |

### Canonical Schema Decision

The `normalizePost()` function in the intelligence dashboard maps everything to **Pulse field names** as canonical — they represent the larger, richer dataset:

```javascript
// Pulse posts: pass through as-is
// Wire posts: translate to Pulse schema on load
function normalizePost(raw, source) {
  if (source === 'pulse') return { ...raw, _source: 'pulse' };
  return {
    creator:   raw.creator_name,
    channel:   raw.creator_url || '',
    title:     raw.title,
    url:       raw.link,
    published: raw.pub_date,
    summary:   raw.text_snippet,
    topic:     raw.beat,
    geography: '',   // Wire-only items (Bluesky) have no geography
    platform:  raw.source === 'bsky' ? 'Bluesky' : '',
    _source:   'wire',
    _wire:     raw,  // preserve full Wire object for score/copy access
  };
}
```

---

## 3. Gap Analysis

### What needs to change to feed Pulse JSON into the Wire dashboard

1. **`atlas_wire_fetch.py` schema mismatch (blocking)**  
   Currently reads `atlas-pulse/pulse_output.json` with legacy nested schema `{creators: [{posts: [...]}]}`. New canonical format is `rss_pulse_v2_*.json` with flat `{posts: [...]}` schema. Must be updated before `--wire` mode works.

2. **`atlas_wire_intelligence.html` — center panel architecture (significant)**  
   Current: card-per-item layout designed for 25 Wire items. Target: paginated sortable table for 5,680 Pulse posts. The left panel (Signal, Beat breakdown, Creator velocity, Histogram) needs to be re-sourced from Pulse data. The right panel (Wire copy editing, Bluesky preview, approve/kill) stays intact for Wire items.

3. **No `normalizePost()` function (straightforward)**  
   The two schemas need a translation layer so the rest of the dashboard code works on a single field set regardless of data source.

4. **No Pulse data loader (straightforward)**  
   Current tool uses a file picker for Wire JSON only. New tool needs auto-detection via `fetch()` for Pulse JSON, Digest JSON, and Wire JSON — requires serving via `python3 -m http.server` (documented in the HTML).

5. **No pagination (required for performance)**  
   5,680 rows rendered simultaneously freezes the browser. Implement 100 rows/page with prev/next.

### Schema adapter vs. full rebuild

The existing tool's HTML structure (three-panel layout, CSS custom properties, design tokens) is sound and should be preserved. The JavaScript state machine (items array, selectedId, approve/kill, keyboard nav) applies to Wire items and should be preserved. The center panel rendering function (`renderQueue` / `qCard`) needs to become a table renderer. The left panel functions (`buildSignal`, `buildBeatBreakdown`, `buildCreatorVelocity`) need to be refactored to work with Pulse corpus data rather than Wire queue items.

**Verdict: Extend, not rebuild.** Preserve ~60% of the existing code. Replace center panel rendering and left panel data sources.

### What the Wire queue is missing that Pulse provides

- Geography (regional filter by state/city)
- Platform breakdown (Newsletter vs. Video vs. Podcast vs. Website)
- Full 30-day corpus context (Wire queue is a 25-item curated slice; Pulse has full picture)
- Creator channel names
- Dark/silent creator tracking

---

## 4. Cadence Feasibility

### Current state
- Pulse: Weekly Sunday ~9am (scheduled task, automated)
- Wire: Manual (no schedule) — last run June 17, 2026

### Proposed cadence
| Mode | Frequency | Command | Duration | Cost |
|------|-----------|---------|----------|------|
| Full | Sunday 9am | `./refresh_pulse.sh` | ~45 min | ~$0.20 |
| Wire | Tue + Thu 9am | `./refresh_pulse.sh --wire` | ~15 min | ~$0.15 |

### Wire mode sequence
```
1. pulse_v2.py --days 1        → rss_pulse_v2_YYYYMMDD.json (1-day window, ~10 min)
2. atlas_wire_fetch.py         → wire_queue_raw_YYYY-MM-DD.json (RSS + Bluesky merge)
3. atlas_wire_rank.py          → wire_queue_scored_YYYY-MM-DD.json (AI scoring, ~3 min)
```

Wire mode does NOT run `update_pulse.py` (no site update), `pulse_digest.py`, or `pulse_spidering_brief.py`.

### Dependencies and risks
- `atlas_wire_fetch.py` must be updated to read new Pulse format before Wire mode works
- `atlas_wire_rank.py` is currently capped at 20 items (`MAX_ITEMS_TO_SCORE = 20`) — may want to increase once rate limits are confirmed
- Wire mode from a 1-day Pulse window will have fewer posts than a manual Wire run using the full 24h window (Wire fetch also queries Bluesky directly, which adds items not in Pulse RSS)
- Full mode on Sunday still generates the fresh 30-day Pulse JSON that the intelligence dashboard uses for corpus view

### Scheduled task configuration
Two new scheduled tasks needed (Tue + Thu 9am), matching the format of the existing Sunday task. Instruction blocks written in Task 3b.

---

## 5. Baseline Stats

| Date | Creators | RSS-resolved | Posts (30d) | Active 7d | Dark 30d | Notes |
|------|----------|-------------|-------------|-----------|----------|-------|
| 2026-04-22 | — | 464 | 807 | — | — | HIGH tier only (legacy pipeline) |
| 2026-05-28 | 1,453 | 883 | 2,299 | — | — | v2.0 pipeline launch |
| 2026-06-05 | 1,589 | 890 | 2,367 | — | — | Local posts broke |
| 2026-06-14 | — | — | — | — | — | Run completed, stats not logged |
| 2026-06-21 | 1,589 | 902 | 5,680 | 545 | 226 | Token fix applied; `\|\| true` patch on Steps 3–4 |
