# Atlas Data Ops Protocol

*Owner: Justin + Ryan Kellett*
*Last updated: May 2026*

---

## The pipeline

```
Ryan's master CSV  →  creators-master.csv  →  node convert.js  →  creators-data.json
```

`creators-data.json` is what the live site reads. **Never edit it by hand.**

---

## Adding creators

**Standard adds (most creators):** Ryan adds to his master sheet and delivers a new `atlas-master.csv`. Run the merge + convert flow described below.

**Bespoke adds (partner projects, ICFJ cohorts, etc.):** When creators are sourced outside Ryan's pipeline (partner pages, curator lists, one-off projects):

1. Add them as rows to `creators-master.csv` directly
2. Send the rows to Ryan so he can incorporate them into his master sheet
3. Run `node convert.js` to regenerate the JSON

The key rule: **every creator on the live site must have a row in `creators-master.csv`.** No exceptions. If it's not in the CSV, it won't survive the next migration.

---

## Migration flow (when Ryan delivers a new master)

1. **Audit first.** Before touching anything, diff the new master against the current `creators-master.csv` to find names in the live file that aren't in Ryan's new one. Expected reasons: bespoke adds (partner projects, ICFJ, etc.). If anything unexpected surfaces, stop and confirm before proceeding.

2. **Build the merged file.** Start from Ryan's new master, then append any bespoke rows that aren't already in it. Bespoke rows go at the end.

3. **Validate.** Check: total row count matches expected, no duplicate slugs, no duplicate creator names, no rows missing `Creator Name` or `slug`.

4. **Convert.** Run `node convert.js` from the repo root. Confirm JSON entry count matches CSV row count.

5. **Update CLAUDE.md.** Update the creator count in the Page Inventory table.

6. **Notify Ryan.** Send him any bespoke rows so his master stays in sync.

---

## What NOT to do

- Don't edit `creators-data.json` directly
- Don't add creators to a partner page's inline data without also adding them to `creators-master.csv`
- Don't run `git push` from CLI — Justin pushes via GitHub Desktop
