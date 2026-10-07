# V14 residual greens: acid/lime text, icons and thin strokes on light surfaces, against HEAD

*2026-10-06, HEAD `86ab67f`. Report only; nothing applied. Full rows: `V14-RESIDUAL-GREENS-2026-10-06.tsv`.*

## Were 2-i and 2-ii applied?

Yes. From `git log`: **`4a4f7bf` "design tokens" = 2-i** (39 files, 375 role renames) and **`2184a46` "tokens" = 2-ii** (28 files, 108 lines of light-surface fixes); then `3ff9d64` CTA swap, `39855ec` CTA states, `86ab67f` 2b. Verified against the files, not just the messages.

## A correction to my own earlier work

This audit found **8 violations that 2-ii should have caught and did not**. Cause: after 2-i repointed the legacy aliases to the new primitives (`--acid-green: var(--color-acid)`, `--lime-green: var(--color-lime)`, and others), my scanner resolved aliases in one pass in file order, and the primitives are defined *later* in `variables.css` than the aliases. So consumers of the legacy aliases were invisible to the static scan I used for 2-ii. The independent rendered-DOM scan did flag two of them, which is how it surfaced. The resolver now iterates to a fixed point, and the results below are from the corrected scan. 2-ii's own regression check was unaffected (it measured real before/after rendering), but its *coverage* was short by these items. Please treat 2-ii as incomplete until group A below is applied.

## Resolving through `--color-accent` (now acid)
**None.** `--color-accent` has 55 consumers at HEAD; all 55 are fills (backgrounds, gradient), 0 are text, icon or stroke. (The two non-fill ones were fixed with the swap.)

## A. Fixable now, on pages that load variables.css (8)

Rules identical to 2-ii: lime/acid text, icon or thin stroke on a light surface → `--color-accent-on-light`; focus rings and focused-field borders → `--color-focus-on-light`.

| file:line | element | property | old | proposed | surface (how) |
|---|---|---|---|---|---|
| assets/css/main.css:96 | `.nav-search:focus` | border-color | `var(--lime-green)` | `var(--color-focus-on-light)` | light (selector) |
| assets/css/main.css:371 | `.filter-search:focus` | border-color | `var(--lime-green)` | `var(--color-focus-on-light)` | light (selector) |
| assets/css/main.css:836 | `.bubble-mode-btn.active` | border-bottom-color | `var(--lime-green)` | `var(--color-accent-on-light)` | light (selector) |
| assets/css/main.css:1228 | `.legend-item:hover` | border-color | `var(--lime-green)` | `var(--color-accent-on-light)` | light (selector) |
| assets/css/main.css:1330 | `.loading-spinner` | border-top-color | `var(--lime-green)` | `var(--color-accent-on-light)` | light (selector) |
| assets/css/main.css:1977 | `.pack-name-input:focus` | border-color | `var(--lime-green)` | `var(--color-focus-on-light)` | light (selector) |
| submit-thanks.html:134 | `.next-steps li:before` | color | `var(--acid-green)` | `var(--color-accent-on-light)` | light (rendered) |
| updates.html:113 | `.benefits-list li:before` | color | `var(--acid-green)` | `var(--color-accent-on-light)` | light (rendered) |

Visible effect if applied: `main.css` focus borders on the nav search and two filter inputs, an active "bubble mode" tab underline, a legend hover border and the loading spinner arc go from lime to olive; the `✓` / `→` bullets on the Thanks and Updates pages go from acid to olive.

## B. Pages without `variables.css`: held, per your instruction
**Rendered at load, confirmed on a light surface (6 elements, hardcode `#5d7400` if/when you want them fixed):** `atlas-portal/index.html` (a link underline, a callout `border-left`, 4 selected-option borders), `atlas-signal-brief.html` (active tab underline, callout `border-left`), and `mobile.html` (the sunburst chart arcs: chart fill, a data color, not a UI violation). Static rules on these pages: 63 rows (see TSV, group B), across atlas_wire_intelligence.html (16), atlas-portal/index.html (13), atlas_pulse_intelligence.html (9), atlas-signal-brief.html (4), atlas_wire_review.html (4), partners/nj-lab.html (4), partners/njlab.html (4), chicago-analysis.html (3), chicago-survey.html (2), mobile.html (2), beat-climate.html (1), lists.html (1).

## C. Not resolvable from the rendered page (95)

These never exist at load (hover/active/modal states, JS-rendered cards, `@keyframes` frames), or are JS-set, or sit in rules shared across light and dark pages. I could not measure a backdrop, so I have not guessed one. Reasons: surface undetermined (48), role other/JS (34), ambiguous: mixed light+dark (12), stylesheet also loaded by a page without variables.css (1). Pages that are dark throughout (`pulse.html`, `for-brands.html`, most of `index.html`, `city-lab-*`) account for most of these and are probably compliant; the proposed fix for each, **only if it turns out to sit on light**, is in the TSV (group C). The JS-set ones (chart palettes in `search.html`, `main.js` canvas strokes, `index.html` node colors) are listed only, as before.

## Footer dividers: did 2b touch them? No

2b changed four footer **text** colors in `assets/css/header.css` (`.footer-tagline`, `.footer-col-title`, `.footer-copy`, `.footer-legal a`: `color: #bdbdbd` → `#c6c6cd`, now lines 338, 339, 344, 346). The dividers are untouched: `header.css:337` `.footer-col:not(:last-child) { border-right: 1px solid rgba(255,255,255,0.15) }` and `header.css:343` `.footer-bottom { border-top: 1px solid #1f1f1f }`, identical before and after `86ab67f`. No footer rule anywhere has a solid `#c6c6cd` border. (Footer text is 9–10px, below the 13px floor; pre-existing.)
