# Deploy Passoff — June 23, 2026

**Session type:** Data deploy (Claude Code)
**Triggered by:** Ryan's June 23 master CSV delivery

---

## What happened

Replaced `assets/data/creators-master.csv` with `atlasmaster_june23.csv` (Ryan's file).

| File | Before | After |
|---|---|---|
| `creators-master.csv` | 1,589 rows | 1,718 rows |
| `creators-data.json` | 1,589 creators | 1,718 creators |
| `bluesky-creators.json` | 384 creators | 543 creators |

Net new creators: **129**. Zero rows removed.

Old master archived as `assets/data/creators-master-backup-20260623.csv`.

---

## Open items for Ryan

**Raquel Willis** — `handle.invalid` in the incoming CSV Bluesky field. Her row deployed normally; the bad handle was skipped by `convert_bluesky.py`. Please supply the correct Bluesky handle when you have it so we can update the master.

**Partner Lists (col 19)** — Still missing from the master schema. The incoming file is 18 columns. Per DATA-OPS-PROTOCOL, this column needs to be re-added at the next Final Clean before sending to Justin. The site is not affected by the missing column, but the schema is out of sync with the documented 19-column standard.

**Private columns sync** — `atlas-private-columns-updated.csv` is at 1,602 rows; master is now 1,718. Gap is 116 rows. Ryan needs to add stub rows for all 129 new creators at next Final Clean.

**Bluesky skips to note:**
- Ken Klippenstein — has a blueskydirectory.com URL in the Bluesky field instead of a handle. Needs a real handle.
- Three duplicate handles flagged (two `@rachelgilmore`, one `@sarahp`/`@anya1anya`) — master has slug collisions. Not blocking but worth a cleanup pass.

---

## Script note

`atlas_groups.py` and `atlas_append.py` still use old comma form `"Science, Health & Environment"`. Justin owns the fix. Do not run group normalization until resolved.

Three scripts mentioned in DATA-OPS-PROTOCOL (`atlas_normalize.py`, `atlas_slug.py`, `atlas_version.py`) do not yet exist in the repo. Protocol is ahead of implementation.
