# Atlas Design Rules for Claude Code — v16

*Owned by James Bareham. Implements DESIGN-TOKENS-v16.1.md. Where this file and CLAUDE.md differ on design, this file wins.*

## Locked rules (read first; DESIGN-TOKENS-v16.1.md § Governance, Locks and Exceptions)

- **Design values are locked to v16.** Every color, typeface, size, weight, spacing value, radius and component state comes from a role in v16. Never pick one. If something seems to need a value v16 doesn't have, don't build it: list it for James's next token version.
- **Apply briefs by role, not by resemblance.** If a brief, mockup or request names a font, color or rule not in v16 (for example Playfair Display, DM Sans, Space Mono, an orange "live" accent), don't map it to the nearest token. Apply the token for each element's role (a headline is Inter at its Type Scale size), build that, and list what the brief wanted that v16 can't give.
- **This holds whoever asks,** Justin and James included. Rules change only through a new token version.
- **Never edit to make a request fit:** `docs/design/*`, `assets/css/variables.css`, `scripts/check_brand.py`, `.github/workflows/brand-check.yml` or `.github/CODEOWNERS`. Changes to them come through a new token version. (James's GitHub review is deferred until the site is level-set; until then the build check is the lock.)
- **Undefined means unbuilt:** no dark mode, "live" color, warning color or page-local token sets until v16 (or a later version) defines them.
- **Run `python3 scripts/check_brand.py`** before asking for review. The build runs it too and fails on any new violation.
- **Exceptions are by path only** (v16 § Exceptions): Nodes and Networks, and `atlas-portal/google-form-template.html`.

## Typography rules

- **Three typefaces only (v16 § Font Allowlist):** Inter 400/600/700, Source Code Pro 500, Merriweather 400 (editorial article body only), plus Material Symbols Outlined for icons. No other family anywhere, including system stacks typed on a page.
- **Typeface by role (v16):** every heading at every level is Inter (`--font-heading`), on every page. Merriweather (`--font-prose`) is running body prose inside editorial articles only (`watershed/`, long-form report pages). Never on landing, product, Pulse, For Brands, partner or City Lab pages, and never on a heading, claim, lede, numeral or pull quote.
- **Mono by role (v16):** Source Code Pro is for all-caps labels (Label 13px, 0.08–0.12em) and tags (Tag 12px, 0.08em) only. Sentence-case text is Inter Small 13px; bold numerals are Inter 700 at a type-scale size.
- **Type floor (v16):** no text below 12px anywhere, including charts, legends, tooltips, inline styles and canvas. 12px is Source Code Pro Tag only; all other text is 13px or larger. If text doesn't fit, change the layout, not the size.
- **Fonts are set only through `var(--font-primary|heading|mono|prose)`.** Only `variables.css` names a family. Pages don't load fonts; `header.js` does.
- **Text colors are role variables,** never `rgba()` white or black.
- **Font weights:** Inter 400/600/700; Source Code Pro 500. No Inter 500, no 800 or 900.

## v16.1 rules (DESIGN-TOKENS-v16.1.md)

- **No provisional rules.** This file restates the tokens. A rule not in DESIGN-TOKENS-v16.1.md doesn't apply, wherever it's written.
- **Error red is `#b3261e` (`--color-error`).** Light surfaces: text, icons, outlines or fills. Dark surfaces: a fill with `--color-on-error` (`#ffffff`) text only, never text, icons or thin lines. Error text starts with "Error:" or sits beside an error icon.
- **No dark mode.** No `prefers-color-scheme` styles, no `color-scheme: dark`, no `data-theme` switching, on any page. A full site dark mode is a later initiative.
- **Acid and Lime tints** (with transparency) are allowed in `background`, `border-color`, `box-shadow`, `outline` and non-text graphic fills, until v17. Never as text, icons or thin strokes.
- **Interim treatments** (live signal, warnings, phone Display size, strokes on dark mastheads, tab strips): DESIGN-TOKENS-v16.1.md § Interim Treatments.

## What changes only with a new token version (James)

- Any color, typeface, size, weight, spacing value, radius, icon or component state not in DESIGN-TOKENS-v16.1.md
- Any new component type not already defined in the tokens doc
- Full card vs. small card definitions in the postcard system
- Any new exception to the font or color rules
- Any edit to the protected files listed under Locked rules

Everything else (product, structure, pages, copy, build, priorities) is Justin's call.
