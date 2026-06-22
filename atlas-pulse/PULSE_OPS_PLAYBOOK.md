# Atlas Pulse — Operations Playbook
## How to Run a Pulse Round (Claude Chat + Claude Code)

*Canonical reference. Update after each session with learnings.*
*Last updated: 2026-06-22*

---

## The Pipeline at a Glance

```
atlas_rss_universe.csv
        ↓
  pulse_fetch.py          (Thing 1 — fetch all RSS feeds)
        ↓
  pulse_output.json       (raw feed data)
  pulse_failed_feeds.csv  (failed feeds for triage)
  pulse_run_log.txt       (summary stats)
        ↓
  [summarization step]    (Thing 2 — Claude AI digest generation)
        ↓
  atlas_pulse_[date].json (structured analysis output)
  atlas_pulse_[date].md   (human-readable digest)
        ↓
  pulse.html              (public display page, reads from JSON)
```

**Other files in the pulse directory:**
- `pulse_clustered.json` — intermediate topic clustering output (pre-digest)
- `youtube_channel_ids.csv` — cache of resolved YouTube channel IDs (don't delete)
- `outputs/` — dated archive of all `pulse_output_YYYYMMDD.json` runs

---

## Baseline Stats (Track These Each Run)

| Date | Creators (total) | Fetchable | Posts | Failed Feeds | Local Posts | Notes |
|------|-----------------|-----------|-------|--------------|-------------|-------|
| 2026-04-22 | — | 464 | 807 | 120 (26%) | — | HIGH tier only |
| 2026-05-28 | 1,453 | 883 | 2,299 | — | 45 | v2.0 pipeline |
| 2026-06-05 | 1,589 | 890 | 2,367 | — | 0 | Local posts broke |
| 2026-06-14 | — | — | — | — | — | Run completed, stats not logged |
| 2026-06-21 | 1,589 | 902 | 5,680 | — | — | Token fix (4096→8192); `\|\| true` patch on steps 3+4; 545 active 7d; 226 silent 30d |

**Healthy run targets:**
- Failure rate: <20% (120/464 = 26% in April — elevated, needs monitoring)
- Posts retrieved: 2,000+ (pipeline at current scale)
- Local posts: >10 (0 on June 5 is a bug/gap to investigate)

---

## Step-by-Step: Running a Pulse Round

### Pre-flight (Claude Chat — do this before opening Claude Code)

1. **Check date of last run** — look at `atlas_pulse_[date].md` filenames. If <7 days since last run, skip unless you need a fresh digest.

2. **Note any known issues from last run** — scan this playbook's Known Issues section below.

3. **Confirm `atlas_rss_universe.csv` is current** — Ryan owns this file. If he's done a data push recently, make sure the latest version is in the pulse directory before running.

4. **Decide run parameters:**
   - Standard: `python pulse_fetch.py` (HIGH+MEDIUM tiers, 7-day window)
   - Fast/debug: `python pulse_fetch.py --tiers HIGH` 
   - Wider: `python pulse_fetch.py --days 14`
   - Full: `python pulse_fetch.py --tiers HIGH,MEDIUM,PENDING` (resolves YouTube, takes longer)

---

### Running in Claude Code

Hand Claude Code this brief verbatim (fill in the date):

```
Run Atlas Pulse for [DATE].

Pre-flight:
1. Read PULSE_OPS_PLAYBOOK.md for current known issues
2. Confirm atlas_rss_universe.csv exists and check its row count
3. Check pulse_run_log.txt from last run for baseline stats

Step 1 — Fetch:
Run: python pulse_fetch.py --tiers HIGH,MEDIUM --days 7
Wait for completion. Report: feeds attempted, successful, failed, posts retrieved.

Step 2 — Triage failures:
Open pulse_failed_feeds.csv. 
- Count feeds with PARSE_ERROR containing ":145408:" — these are likely Substack paywall truncations (known issue, not actionable)
- Count SSL errors — flag any new ones not in previous runs
- Count "syntax error" at line 2 — these may indicate dead/changed feeds, worth spot-checking 3-5
- Report: total failures by error type

Step 3 — Generate digest:
[Run your summarization script / Thing 2 here]
Output: atlas_pulse_[DATE].json and atlas_pulse_[DATE].md

Step 4 — Validate output:
- Confirm atlas_pulse_[DATE].json has trending_topics (expect 4-6)
- Confirm local.top_topics is populated (if 0, flag — this is a known gap)
- Check statistics.total_creators and fetchable_creators match expected scale

Step 5 — Archive:
- Copy pulse_output.json to outputs/pulse_output_[DATE].json if not already done
- Update pulse_run_log.txt is written

Report back: run stats summary, any new failures not seen before, local post count, and whether digest looks clean.
Do NOT push to Cloudflare yet — Claude Chat will review digest first.
```

---

### Post-Run Review (Claude Chat)

After Code reports back:

1. **Read the `.md` digest** — skim for:
   - Artifact language (internal analysis that leaked into public copy)
   - Duplicate entries (same post attributed to two creators — syndication artifact)
   - Empty URLs in example posts (`` link — acceptable but track frequency)
   - Local section populated? (0 local posts = investigate)

2. **Check key metrics against baseline table above** — update the table

3. **Spot-check 2-3 example post URLs** — confirm they resolve

4. **Decision: push to pulse.html or revise?**
   - If clean → brief Code to update pulse.html with new JSON and push
   - If issues → brief Code with specific fixes first

---

## Known Issues (Running Log)

### `:145408` Parse Errors (Substack paywall truncation)
**Status:** Known, not actionable  
**What it is:** Feedparser hits Substack's paywall at byte 145408 and fails XML parsing. Affects ~60-80 creators on each run.  
**Action:** None. These creators are in the universe and will show up when they publish free posts. Do not remove them from `atlas_rss_universe.csv`.  
**First observed:** April 2026 run

### SSL: TLSV1_ALERT_PROTOCOL_VERSION errors
**Status:** Known, intermittent  
**Affected:** Jasmine Enberg, Kaya Yurieff, Tyler Dunne (April 2026)  
**What it is:** Old TLS version on the server side — their feed URLs may need updating or they've migrated platforms  
**Action:** Spot-check these URLs manually. If feed has moved, update `atlas_rss_universe.csv` via Ryan.

### Local Posts = 0 (June 5, 2026)
**Status:** Open — needs investigation  
**What happened:** May 28 had 45 local posts; June 5 had 0. Same pipeline.  
**Possible causes:** (a) Chicago/DC creators genuinely published nothing in the window, (b) the local group filter in the fetch script broke, (c) local creators dropped out of `atlas_rss_universe.csv`  
**Action for next Code session:** `grep -i "local\|chicago\|dc\|washington" atlas_rss_universe.csv | wc -l` — confirm local creators are still in the file and check their `group` field values.

### Charlotte Wilder — Duplicate failure entries
**Status:** Known  
**What it is:** Two separate RSS URLs for same creator, both failing. Harmless but messy in logs.  
**Action:** Note as dedup candidate for Ryan's next `atlas_rss_universe.csv` cleanup pass.

---

## The Two Scripts (What We Know)

### Thing 1: `pulse_fetch.py`
**What it does:** Reads `atlas_rss_universe.csv`, fetches RSS feeds in parallel, outputs raw post data  
**Key args:**
- `--tiers HIGH,MEDIUM,PENDING` — HIGH = confirmed RSS, MEDIUM = working, PENDING = needs YouTube ID resolution
- `--days 7` — lookback window (7 = weekly digest, 14 = biweekly)
- `--workers 10` — parallel fetch threads (increase to 20 for speed if network allows)
- `--output pulse_output.json` — output filename  

**Outputs:**
- `pulse_output.json` — full raw data (large, ~5-15MB)
- `pulse_run_log.txt` — human-readable summary
- `pulse_failed_feeds.csv` — failed feeds for triage
- `youtube_channel_ids.csv` — updated YouTube cache (only if PENDING tier run)
- `outputs/pulse_output_YYYYMMDD.json` — dated archive copy

### Thing 2: Summarization Script
**Status:** Exists, not yet uploaded to this playbook  
**What it does:** Takes `pulse_output.json`, runs Claude AI summarization, outputs structured digest  
**Outputs:** `atlas_pulse_[date].json` + `atlas_pulse_[date].md`  
**TODO:** Get the script filename from the repo and document it here.

### `pulse.html`
**What it does:** Public-facing display page at `/pulse`  
**Data source:** Reads from a JSON file (likely `atlas_pulse_[latest].json` or a symlink)  
**Design:** Governed by James's design system / `DESIGN-TOKENS.md`  
**After each run:** Brief Code to update the JSON reference and push to Cloudflare Pages via GitHub Desktop.

---

## `atlas_rss_universe.csv` — Field Reference

| Field | Values | Notes |
|-------|--------|-------|
| `name` | Creator name | |
| `channel` | Publication/newsletter name | |
| `rss_url` | RSS feed URL | Blank for PENDING YouTube |
| `link` | Canonical creator URL | Used for YouTube ID resolution |
| `platform` | e.g. "Newsletter - Substack" | |
| `topic` | Beat/subject area | |
| `geography` | e.g. "Chicago", "National" | |
| `group` | "local" or "universal" | **Critical for local digest section** |
| `confidence` | HIGH / MEDIUM / PENDING | Controls which tier runs fetch it |

**Ryan owns this file.** No edits without going through Ryan.  
**To request updates:** Compile a list of changes (new RSS URLs, dead feeds, confidence tier changes) and send to Ryan with `#atlas-data` note.

---

## Enrichment (Post-Pulse)

After a successful digest run, enrichment tasks that can be done in the same Code session:

1. **Failed feed audit** — identify feeds that have failed 3+ consecutive runs → candidates for removal or URL update
2. **New creator additions to RSS universe** — if Ryan has pushed new entries to `creators-master.csv`, run `node convert.js` to refresh `creators-data.json`, then cross-reference for any new RSS-eligible creators to add to `atlas_rss_universe.csv`
3. **Platform breakdown tracking** — log the platform breakdown stats to the baseline table above

---

## What Claude Chat Does vs. Claude Code

| Task | Who |
|------|-----|
| Decide run parameters | Chat |
| Write Code brief | Chat |
| Read PULSE_OPS_PLAYBOOK.md | Code (at session start) |
| Run `pulse_fetch.py` | Code |
| Triage `pulse_failed_feeds.csv` | Code (report) + Chat (decisions) |
| Run summarization (Thing 2) | Code |
| Review digest quality | Chat |
| Update `pulse.html` / push | Code |
| Update baseline stats table | Chat (after run) |
| Update Known Issues log | Chat (after run) |
| Request CSV updates | Chat → Ryan |

---

## Cadence

- **Standard:** Weekly (every 7 days, aligned with 7-day fetch window)
- **Chicago static JSON for `/pulse` page:** Same cadence — run script, commit JSON, push
- **Emergency run:** After a major breaking story (e.g., Minnesota ICE raids) — use `--days 3` to narrow window and `--tiers HIGH` for speed

---

## Cadence & Run Modes

| Mode | Frequency | Command | What it produces | Time |
|------|-----------|---------|-----------------|------|
| Full | Sunday 9am (scheduled) | `./refresh_pulse.sh` | Pulse digest, site update (pulse.html, index.html, for-brands.html), spidering brief | ~30 min |
| Wire | Tue + Thu 9am (scheduled) | `./refresh_pulse.sh --wire` | Wire queue scored JSON only — does NOT update site | ~15 min |
| Manual full | As needed | `./refresh_pulse.sh` | Same as Full | ~30 min |
| Manual wire | As needed | `./refresh_pulse.sh --wire` | Same as Wire | ~15 min |

### Scheduled task instructions (for Tue/Thu Wire runs)

Copy this text exactly into each new scheduled task:

**Description:** Atlas Wire queue refresh — build Wire queue from 1-day RSS window

**Instructions:**
Run the Wire queue pipeline:
```
cd "/Users/justinbank/Documents/Atlas Spidering/core"
./refresh_pulse.sh --wire
```

This runs three steps:
- `pulse_v2.py --days 1` — fetches last 24h of RSS posts (~10 min)
- `atlas_wire_fetch.py` — builds raw Wire queue from Pulse output (RSS + Bluesky)
- `atlas_wire_rank.py` — AI-scores and clusters queue items (~$0.15, ~3 min)

Does NOT update the live site. Does NOT run digest or spidering brief.

Report back:
- Items fetched from RSS
- Items added to Wire queue
- Score range (min / max / avg)
- Any errors

Open `atlas_wire_intelligence.html` to review the queue.

---

## Files in the Pulse Directory (What Should Be There)

```
atlas-pulse/
├── pulse_fetch.py              ← Thing 1 (fetch script)
├── [summarization script]      ← Thing 2 (TODO: confirm filename)
├── atlas_rss_universe.csv      ← Feed source (Ryan owns)
├── pulse_output.json           ← Latest raw fetch output
├── pulse_run_log.txt           ← Latest run summary
├── pulse_failed_feeds.csv      ← Latest failures
├── pulse_clustered.json        ← Intermediate clustering output
├── youtube_channel_ids.csv     ← YouTube channel ID cache
├── atlas_pulse_[latest].json   ← Latest structured digest
├── atlas_pulse_[latest].md     ← Latest human-readable digest
├── pulse.html                  ← Public display page
├── PULSE_OPS_PLAYBOOK.md       ← This file
└── outputs/
    └── pulse_output_YYYYMMDD.json  ← Dated archives
```

---

## Open Questions / Next Actions

- [ ] **Confirm Thing 2 script filename** — what is the summarization script called? Document it here.
- [ ] **Investigate local posts = 0** — grep `group` field in `atlas_rss_universe.csv` for local creators before next run
- [ ] **SSL error feeds** — manually check Jasmine Enberg, Kaya Yurieff, Tyler Dunne RSS URLs — have they migrated?
- [ ] **`:145408` error volume** — is this getting worse over time? Track count per run to detect if Substack is changing paywall behavior
- [ ] **`pulse.html` JSON reference** — confirm what JSON filename/path the display page reads from (static reference or dynamic latest?)
- [ ] **Separate Chicago Pulse JSON** — the weekly Chicago static JSON refresh is a distinct task from the main Pulse run. Document that script separately once identified.
