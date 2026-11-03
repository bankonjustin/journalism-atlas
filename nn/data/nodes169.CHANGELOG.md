# nodes169.json changelog

Nov 2, 2026: regenerated from `cohort_reference_expanded_v22.5.csv` so that `nn/tools/snapshot.py`'s name check passes against v22.5. Built with a copy of `nodes-networks-v5/edition/tools/build_nodes169.py` (same code, inputs pointed at v22.5; the copy was first run on the v22 inputs and reproduced the edition's Nov 1 file byte for byte). The RESOLVED csv stays read-only; its Gannett and CNN keys and the Banner's cohort are translated in memory. Differences from the Oct 29 file: names (CNN (Skydance), USA TODAY Co. (formerly Gannett)), Baltimore Banner C1 to C4 (c, ci, g), Rogan M3 (was the Exception coding), Puck status DEAL_ANNOUNCED, and every layout position (the gov and born lenses re-pack with C1 at 17 and C4 at 45; the other lenses re-run with the same seeds). `nn/built/` was not rebuilt, so the deployed fallback still carries the Oct 29 positions.

Nov 1, 2026: no changes. The file stays read-only and is unchanged.

## Known drift (nothing reads it; sync after launch)

`nn/build.py` takes position, cohort, group, band and the unverified flag from this file. It takes name, founding year, origin, mechanism, revenue and status from `public-snapshot.json`, which `nn/tools/snapshot.py` builds from the private CSV, the approved recode rows and `snapshot-overrides.csv`. These fields in `nodes169.json` therefore differ from the live ASU embed:

- Mechanism on 18 started-above rows (`INHERITED_SCALE` here, an M-code in the embed). Rogan now matches (M3).
- Name and founding year withheld on rows 2, 152 and 153 (Washington Post, Risk.net, Insurance Journal).
- Status flags now present on all 11 rows (`deal announced` for Puck); the old gap is closed.

`nn/tools/parity_check.py` compares the snapshot, not this file, with the embed.

## Dead exception code (remove after launch)

With Rogan at M3 nothing is coded to `EXCEPTION_PLATFORM_LICENSING`, so these are never rendered but still present:

- `nn/content/copy.md`: `legend.grew_past_exception`, `labels.exception_short`, `labels.exception_1`, `labels.exception_2`, `ann.ways_exception`, `list.no_mechanism`, `list.no_mechanism_note`, and the `exceptions_phrase`, `exception_name` and `exceptions_n` tokens in `nn/build.py`.
- `nn/src/engine.js` (the `trid` hollow-triangle shape and the Exception sector label) and `nn/src/explorer.tpl.html` (`EXC`, `hasExc`, the dashed-triangle legend swatch). The template reads `legend.grew_past_exception` unconditionally, so the strings cannot be deleted until those lines go.

## Edition (figure embeds)

`nodes-networks-v5/edition/tools/build_nodes169.py` now reads `nn/data/snapshot-overrides.csv` (the same file `nn/tools/snapshot.py` reads), so the Rogan and Iowa decisions live in one place. It also drops the Exception wedge and key when no node uses it. `fig-6-kaleidoscope` and the edition `explorer/index.html` under `preview/nodes-and-networks-edition-e852c5c5/` were rebuilt from it on Nov 1, 2026. The edition's own `src/data/nodes169.json` is regenerated; this file is not. Backups: `~/nn5-backup-2026-11-01/` (the edition source before the change, the two replaced repo files, the old edition `nodes169.json`).

Still to consolidate after launch: the pre-existing `MECH-RECODE-PROPOSED.csv` and `MECHANISM-CODING-RESOLVED-2026-10-23.csv` still carry the old Rogan and Iowa codings (both are read-only approval records); the override file wins over both.
