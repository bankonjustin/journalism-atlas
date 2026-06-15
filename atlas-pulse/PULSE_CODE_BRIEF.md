# Atlas Pulse — Claude Code Session Brief
## Paste this at the start of every Pulse Code session

*This is the prompt to give Claude Code. Copy everything below the line.*

---

Read `PULSE_OPS_PLAYBOOK.md` before doing anything else. Then run the following steps in order.

---

**STEP 1 — Pre-flight check**
- Confirm `atlas_rss_universe.csv` exists. Report row count.
- Confirm `pulse_fetch.py` exists.
- Check `pulse_run_log.txt` — report the date and stats from the last run.
- Check for the most recent `atlas_pulse_[date].md` — report its date.

**STEP 2 — Fetch**
Run: `python pulse_fetch.py --tiers HIGH,MEDIUM --days 7`

Wait for completion. Report back:
- Feeds attempted / successful / failed
- Posts retrieved
- Platform breakdown
- Top 10 creators by post count

Do NOT proceed until you report these numbers back to me.

**STEP 3 — Failure triage**
Open `pulse_failed_feeds.csv`. Categorize failures:
- Count errors containing `:145408:` → label "Substack paywall (known, skip)"
- Count `SSL` errors → list creator names
- Count `syntax error` at line 2 → list creator names (possible dead feeds)
- Count `text/html is not an XML media type` → list creator names
- Any other error types → list them

Report the breakdown. Flag anything that wasn't present in the previous run's log.

**STEP 4 — Generate digest (Thing 2)**
Run the summarization script to generate today's digest.
Output: `atlas_pulse_[TODAY'S DATE].json` and `atlas_pulse_[TODAY'S DATE].md`

If you're unsure which script to run, check the directory for the summarization script and confirm with me before running.

**STEP 5 — Validate digest**
Open `atlas_pulse_[TODAY'S DATE].json` and confirm:
- `trending_topics` array has 4–6 entries
- Each topic has `example_posts` with at least 2 entries
- `local.top_topics` — is it populated or empty? Report.
- `statistics.total_creators` and `fetchable_creators` — report numbers
- Any example posts with empty `url` fields — count them

**STEP 6 — New voice flagging (for Ryan handoff)**
Scan the `analysis.universal.notable_activity` and `trending_topics` in the digest JSON.
List any creator names cited in post content who do NOT appear as a `name` in `atlas_rss_universe.csv`.
Format as a simple list: Name | Publication/URL if visible | Topic area
Label this section "POTENTIAL NEW ADDITIONS — for Justin review"

Do NOT add anyone to any file. Just generate the list for my review.

**STEP 7 — Archive**
- Confirm `outputs/pulse_output_[DATE].json` was written
- Confirm `pulse_run_log.txt` is current

**STOP HERE.** Report everything back to me. Do not update `pulse.html` or push to Cloudflare until I review the digest and give the go-ahead.
