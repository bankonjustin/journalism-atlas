# nodes169.json changelog

Nov 1, 2026: no changes. The file stays read-only and is unchanged.

## Known drift (nothing reads it; sync after launch)

`nn/build.py` takes position, cohort, group, band and the unverified flag from this file. It takes name, founding year, origin, mechanism, revenue and status from `public-snapshot.json`, which `nn/tools/snapshot.py` builds from the private CSV, the approved recode rows and `snapshot-overrides.csv`. These fields in `nodes169.json` therefore differ from the live ASU embed:

- Mechanism on 18 started-above rows (`INHERITED_SCALE` here, an M-code in the embed), Rogan (`EXCEPTION_PLATFORM_LICENSING` here, M3 in the embed).
- Name and founding year withheld on rows 2, 152 and 153 (Washington Post, Risk.net, Insurance Journal).
- No status flag on 12 rows (the embed carries `acquired`, `closed` or `absorbed`).

`nn/tools/parity_check.py` compares the snapshot, not this file, with the embed.

## Dead exception code (remove after launch)

With Rogan at M3 nothing is coded to `EXCEPTION_PLATFORM_LICENSING`, so these are never rendered but still present:

- `nn/content/copy.md`: `legend.grew_past_exception`, `labels.exception_short`, `labels.exception_1`, `labels.exception_2`, `ann.ways_exception`, `list.no_mechanism`, `list.no_mechanism_note`, and the `exceptions_phrase`, `exception_name` and `exceptions_n` tokens in `nn/build.py`.
- `nn/src/engine.js` (the `trid` hollow-triangle shape and the Exception sector label) and `nn/src/explorer.tpl.html` (`EXC`, `hasExc`, the dashed-triangle legend swatch). The template reads `legend.grew_past_exception` unconditionally, so the strings cannot be deleted until those lines go.

## Edition (figure embeds)

`nodes-networks-v5/edition/tools/build_nodes169.py` now reads `nn/data/snapshot-overrides.csv` (the same file `nn/tools/snapshot.py` reads), so the Rogan and Iowa decisions live in one place. It also drops the Exception wedge and key when no node uses it. `fig-6-kaleidoscope` and the edition `explorer/index.html` under `preview/nodes-and-networks-edition-e852c5c5/` were rebuilt from it on Nov 1, 2026. The edition's own `src/data/nodes169.json` is regenerated; this file is not. Backups: `~/nn5-backup-2026-11-01/` (the edition source before the change, the two replaced repo files, the old edition `nodes169.json`).

Still to consolidate after launch: the pre-existing `MECH-RECODE-PROPOSED.csv` and `MECHANISM-CODING-RESOLVED-2026-10-23.csv` still carry the old Rogan and Iowa codings (both are read-only approval records); the override file wins over both.
