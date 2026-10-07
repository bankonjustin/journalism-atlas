# Start here — open decisions

*Updated 2026-10-06 after the autonomous v14 run. Delete an item when it is resolved.*

## For James
1. **Report article links.** `research/nodes-and-networks.html` styles body links with its own blue (`--blue: #185FA5`, underlined). v14 says olive + underlined on light. Skipped: the page is a copy-locked template with its own palette (warm off-system grays, `#faf9f5` background). Switch to olive?
2. **CTA-style links inside sentences** (arrow links, e.g. "Submit here →" in `how-we-did-this.html`, "Switch to Journalism →" in `city-lab-dc-v3.html`) and the beat-name links in the Pulse masthead lede (`a.lede-beat`, white on dark, no underline). Inline-link rule or CTA/tag rule?
3. **Focus ring on dark.** v14 says lime; `--focus-ring-dark` is still acid. Confirm and I will move it.
4. **`#a8a8a8` → step 5.** `--color-border-hover` now jumps from a pale gray to `#5e5e64` (as ruled). Keep, or step 3/4?
5. **Off-system grays** (~107 colors, 1,444 uses, incl. the warm family): by-role proposal in `docs/V12-UNMAPPED-GRAYS-PROPOSAL-2026-10-06.md`.
6. **Charts** use brand-secondary colors as categories; `ATLAS_VIZ_COLORS` migration needs Ryan's taxonomy mapping.
7. **Header search button** is now acid at rest on every page (it was lime). Confirm.
8. Tier 2 contrast column in v14: label it Neutral (the Cool figures are the semantic table's).

## For Justin
- **Logos:** header swap done (blk/wht wired, default white). Still needed: `Atlas_logo_lockup_stacked_wht_web.svg` (the footer still uses `Journalism_Atlas_wordmark_stacked_white.svg`). The old header SVG (`Journalism_Atlas_wordmark_horizontal_lockup_black.svg`) is now unreferenced and can be deleted.
- **Partner pages have a 72px empty band above the header** (`body { padding-top: 72px }`, pre-existing; the nav is sticky now). Remove the padding?
- **22 pages without `variables.css`** (14 hardcode a green). They were skipped everywhere. Fix = link `variables.css` (visible change) or hardcode v14 colors. Includes `partners/nj-lab.html` / `njlab.html`, whose link is a relative path that 404s. Lists: `docs/V14-STEP2I-2026-10-06.md`, `docs/V14-RESIDUAL-GREENS-2026-10-06.md`.
- **~95 static greens could not be measured** (hover/active/JS-rendered/shared rules; listed with proposed fixes, group C of the residual TSV). Mostly on dark pages; probably compliant.
- **27 JS-set greens** (chart palettes, canvas strokes): listed, not changed.
- `Atlas-Long-Form-Report-Template-2026-09.md` is not in this repo; it needs the white sub-nav spec.
- `.DS_Store` is tracked and shows modified every time; untrack it separately.
- Six commits from this run are local; push when ready.
