# Start here — open decisions

*Updated 2026-10-06. Delete an item when it is resolved.*

## For James
1. **Retired-gray `#a8a8a8` as a hover border** (`--color-border-hover`): v14 maps `#a8a8a8` to step 5 on light, a rule written for secondary *text*. Applied to a hover border it darkens a lot (2.3:1 to 6.4:1). Step 5 as written, or step 3/4?
2. **Five `wire.html` text lines use `#9e9e9e`** (timestamp, hashtag, empty and loading states, footer band) and will read step 4 (3.2:1 on white, 2.8:1 on the page background): below 4.5:1 for small text. Move them to step 5 (`--color-text-secondary`)?
3. **Off-system grays** (about 107 colors, 1,444 uses, including the warm family): snap to Cool by role in a later release. A by-role proposal is in `docs/V12-UNMAPPED-GRAYS-PROPOSAL-2026-10-06.md`.
4. **Sub-nav hover/active on white** is specified in v14 (olive underline, olive active); the long-form report template still describes a black sub-nav and must be updated (stop 6).
5. **Charts** use brand-secondary colors as categories; moving to `ATLAS_VIZ_COLORS` needs Ryan's taxonomy mapping (not in this release).

## For Justin
- Logos: add the three `Atlas_logo_lockup_*_web.svg` files to `assets/images/logos/` (they are in `~/Downloads` now). Header logo swap is stop 6.
- `.DS_Store` is tracked and shows modified every time; untrack it separately.
- Duplicate files in the repo that duplicate live pages: `CLAUDE copy.md`, `PARTNERS copy.md`, `partners/njlab copy.html`, `partners/_reviewjames copy.html`.
