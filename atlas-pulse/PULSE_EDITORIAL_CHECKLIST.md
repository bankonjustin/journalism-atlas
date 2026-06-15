# Atlas Pulse — Post-Run Editorial Checklist
## What to do in Claude Chat after Code reports back

*Run through this after Code gives you the Step 7 report. Takes ~10 minutes.*

---

## 1. Update the Baseline Table

Open `PULSE_OPS_PLAYBOOK.md` and fill in the new row:

| Date | Creators (total) | Fetchable | Posts | Failed Feeds | Local Posts | Notes |
|------|-----------------|-----------|-------|--------------|-------------|-------|

Note anything unusual in the Notes column.

---

## 2. Read the Digest

Open `atlas_pulse_[DATE].md`. Scan for:

**Red flags (fix before publishing):**
- [ ] Artifact language — copy that reads like internal analysis, not editorial ("this represents a significant inflection point for…" is borderline; "per the data pipeline…" is a red flag)
- [ ] Same article attributed to two different creators with identical title/URL — syndication artifact, remove the duplicate
- [ ] Creator name that doesn't match their publication (name/channel mismatch)
- [ ] Empty URLs in example posts — acceptable but note frequency; if >10, flag to investigate

**Yellow flags (note, don't necessarily fix):**
- [ ] Local section empty — note it, don't delay publishing, but log in Known Issues
- [ ] Insights that feel generic / could apply to any week — these are fine to publish but worth noting as a quality signal
- [ ] A topic cluster that's really just one creator's output dominating — worth noting

---

## 3. Review the New Voice List (Step 6 output)

Code will give you a list of names cited in posts who aren't in `atlas_rss_universe.csv`.

For each name, quick gut check:
- **Obvious add** — independent journalist, active, clear beat → put on Ryan handoff list
- **Review** — might be indie, might be staff, need to check → note for manual lookup
- **Skip** — clearly institutional (NYT reporter, AP wire, etc.) → ignore

This is 5 minutes of editorial judgment. Don't overthink it.

---

## 4. Ryan Handoff (if any Obvious Adds)

If you have names to flag, paste this into `#atlas-data` or send directly to Ryan:

```
Hey Ryan — post-pulse new voice candidates from [DATE] run.
These names came up in post citations but aren't in creators-master.csv.
Worth a look when you have a minute.

OBVIOUS ADDS:
- [Name] | [URL if found] | [Beat]

REVIEW:
- [Name] | [URL if found] | [Beat]
```

---

## 5. Push Decision

**If digest looks clean:** Tell Code to update `pulse.html` with the new JSON and push to Cloudflare via GitHub Desktop.

Brief for Code:
```
Digest looks good. Update pulse.html to reference atlas_pulse_[DATE].json 
as the current digest. Commit with message "Pulse update [DATE]" and push.
```

**If digest has red flags:** Fix them first. Brief Code with specific find/replace targets before pushing.

---

## 6. Log Any New Known Issues

If you spotted something new — a pattern of failures, a broken local feed, a script behavior — add it to the Known Issues section of `PULSE_OPS_PLAYBOOK.md` before closing the session.

---

## Done. Session complete.
