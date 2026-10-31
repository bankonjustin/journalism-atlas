# MANIFEST: 2026-10 sweep (journalism-atlas)

Archive, don't delete. Moves go to `_archive/2026-10-sweep/`; the only allowed removal is a byte-identical duplicate (sha256 match). Plan: `journalism-atlas-private/ops/CLEANUP-PLAN-2026-10-31.md`. Starting hash `8b65f2b`.

| Row | Original path | New path | Action | Reason | Evidence |
|---|---|---|---|---|---|
| A1 | `PARTNERS copy.md` | (removed) | remove-identical-dup | Same bytes as `PARTNERS.md` | sha256 29237c24bb41f39e9cd994af93b0a88d60b44ec0471c37a16e2dfdbed93a8959 (both) |
| A2 | `partners/_reviewjames copy.html` | `_archive/2026-10-sweep/partners/_reviewjames copy.html` | archive | Differs from `partners/_reviewjames.html` only in older token names (`--acid`, `--olive` vs `--color-acid`, `--color-accent-on-light`); sibling is newer in content | sha256 98f6629d0a76cd7f271c5b10921f82b3a865e06b26f756ccf0311d0667abc13b vs sibling `d7c13baa73f22fc2ef8f15cdfed738bfb358ae905ca555d379e73df61b63726c`; 16-line diff; referenced only in `docs/V12-*` audit files |
