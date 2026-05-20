# Atlas CSS Token Compliance Audit
*Last updated: 2026-05-20*
*Reference: DESIGN-TOKENS.md (James — james@happicamp.com)*

---

## Summary

| Category | Count |
|---|---|
| Violations fixed this session | 37 |
| Flagged for James | 1 |
| Flagged for Justin | 0 |
| Pages confirmed load-order compliant | 22 |
| Pages with load-order violations fixed | 9 |

---

## Violations Fixed This Session

| File | Line | Value | Violation Type | Fix Applied |
|------|------|-------|----------------|-------------|
| `assets/css/main.css` | 2399 | `#CCFF00` | Wrong hex + hardcoded — footer hover link on dark bg should be `var(--color-acid-green)` (`#ceff00`); `#CCFF00` is a different color | Replaced with `var(--color-acid-green)` |
| `for-brands.html` | 136 | `background: #ceff00` on `.compare-th--right` | Acid green on light surface — `.compare-section` has `background: #f5f5f5`. Rule: acid green = dark backgrounds only. | Replaced with `var(--color-lime-green)` and border with `var(--color-dark-olive)` |
| `about-this-project.html` | 31 | Missing | Load order — `variables.css` not linked; page uses `var()` tokens in inline `<style>` | Added `<link rel="stylesheet" href="assets/css/variables.css">` before inline `<style>` |
| `who-we-are.html` | 31, 49 | Missing + system font | Load order + unapproved font — no `variables.css`; body set to `-apple-system` stack | Added `variables.css` link; changed body `font-family` to `var(--font-primary)` |
| `advisory.html` | 31, 50 | Missing + system font | Load order + unapproved font — no `variables.css`; body set to `-apple-system` stack | Added `variables.css` link; changed body `font-family` to `var(--font-primary)` |
| `submit.html` | 31, 50 | Missing + system font | Load order + unapproved font — no `variables.css`; body set to `-apple-system` stack | Added `variables.css` link; changed body `font-family` to `var(--font-primary)` |
| `submit-thanks.html` | 31, 50 | Missing + system font | Load order + unapproved font — no `variables.css`; body set to `-apple-system` stack | Added `variables.css` link; changed body `font-family` to `var(--font-primary)` |
| `how-we-did-this.html` | 31, 49 | Missing + system font | Load order + unapproved font — no `variables.css`; body set to `-apple-system` stack | Added `variables.css` link; changed body `font-family` to `var(--font-primary)` |
| `research.html` | 31, 50 | Missing + system font | Load order + unapproved font — no `variables.css`; body set to `-apple-system` stack | Added `variables.css` link; changed body `font-family` to `var(--font-primary)` |
| `updates.html` | 31, 50 | Missing + system font | Load order + unapproved font — no `variables.css`; body set to `-apple-system` stack | Added `variables.css` link; changed body `font-family` to `var(--font-primary)` |
| `index.html` | 44 | `background: #d8ff33` | `.btn-acid:hover` — unknown hover color, not in DESIGN-TOKENS.md | Replaced with `var(--color-lime-green)` |
| `for-brands.html` | 64, 423 | `background: #d8ff33` | `.btn-primary:hover` and `.bf-submit:hover` — unknown hover color on dark-bg buttons | Replaced with `var(--color-lime-green)` |
| `for-brands.html` | 367 | `background: #a8e800` | `.form-submit:hover` on white `.form-section` — unknown hover color | Replaced with `var(--color-dark-olive)` |
| `nj-lab.html` | 354 | `background: #b8e600` | `.cta-primary:hover` — unknown hover color | Replaced with `var(--color-lime-green)` |
| `city-lab-chicago.html` | 617 | `background: #ceff00` | `.legend-dot` on white body background — acid green on light surface violation | Replaced with `var(--color-lime-green)` |
| `header.css` | 253–261 | `font-family: 'DM Mono', monospace` | Unapproved typeface in shared footer — DM Mono not in DESIGN-TOKENS.md | Replaced with `'JetBrains Mono'`; added `@import` for JetBrains Mono at top of header.css |
| `index.html` | multiple | `font-family: 'DM Mono', monospace` | Unapproved typeface used ~65 times across all monospace contexts | Replaced all instances with `'JetBrains Mono'`; added Google Fonts `<link>` in `<head>` |
| `research.html` | 147, 158, 276, 282, 296, 301, 306, 330, 336 | `font-weight: 600` | 600 not in approved weight set | Replaced all instances with `700` |
| `city-lab-chicago.html` | 1197, 1980, 1981 | `font-weight: 600` | 600 not in approved weight set | Replaced all instances with `700` |
| `index.html` | 484 | `font-weight: 600` | `.drawer-creator-name` — 600 not approved | Replaced with `700` |
| `assets/css/main.css` | multiple | `font-weight: 500` | 500 not in approved weight set — systemic across main.css | Headings/buttons → `700`; labels/metadata/tags/links → `400` (see decisions log below) |
| `index.html` | multiple | `font-weight: 500` | 500 not in approved weight set | Prominent numbers (`.hero-stat-badge-num`, `.cluster-count-n`) → `700`; labels/metadata/names → `400` |
| `partners/cillizza.html` | multiple | `font-weight: 500` | 500 not in approved weight set — all instances are tags/chips/labels/links | Replaced all with `400` |
| `partners/ahp.html` | multiple | `font-weight: 500` | Same pattern | Replaced all with `400` |
| `partners/icfj.html` | multiple | `font-weight: 500` | Same pattern | Replaced all with `400` |
| `partners/news-creator-corps.html` | multiple | `font-weight: 500` | Same pattern | Replaced all with `400` |
| `partners/joon-lee.html` | multiple | `font-weight: 500` | Same pattern | Replaced all with `400` |
| `partners/jessica-stahl.html` | multiple | `font-weight: 500` | Same pattern | Replaced all with `400` |
| `partners/knowledge-creators.html` | multiple | `font-weight: 500` | Same pattern | Replaced all with `400` |
| `partners/emily-atkin.html` | multiple | `font-weight: 500` | Same pattern | Replaced all with `400` |
| `partners/natgeo.html` | multiple | `font-weight: 500` | Same pattern | Replaced all with `400` |
| `partners/karen-attiah.html` | multiple | `font-weight: 500` | Same pattern | Replaced all with `400` |
| `partners/rahim-jessani.html` | multiple | `font-weight: 500` | Same pattern | Replaced all with `400` |
| `partners/noah-smith.html` | multiple | `font-weight: 500` | Same pattern | Replaced all with `400` |
| `advisory.html` | 237 | `font-weight: 500` on `.about-subnav-link` | Nav link — 500 not approved | Replaced with `400` |
| `submit.html` / `submit-thanks.html` / `updates.html` | 34–42 | Inline `:root` block with wrong values (`--lime-green: #d4ff33`, `--light-gray: #f5f5f5`, `--dark-gray: #666666`) | Local `:root` overrides canonical token values with wrong colors, wins cascade over variables.css | Deleted entire `:root { }` block from each page's inline `<style>`; pages now rely fully on variables.css |
| `assets/css/variables.css` | 107, 161 | Comment said `500 (labels/UI)`; weight still listed without deprecation note | Stale comment conflicts with May 2026 DESIGN-TOKENS.md decision removing 500 | Updated comment to reflect 500 is no longer in approved set |

### main.css font-weight decisions log

| Selector | Old | New | Reason |
|---|---|---|---|
| `.filter-accordion-header h3` | 500 | 700 | Heading |
| `.clear-filters-top` | 500 | 700 | Prominent action button |
| `.mobile-filter-toggle` | 500 | 700 | Prominent action button |
| `.share-view-btn` | 500 | 700 | Action button |
| `.atlas-drawer-show-more` | 500 | 700 | Action button |
| `.bubble-mode-btn` | 500 | 700 | Tab action button |
| `.creators-table th` | 500 | 700 | Table heading |
| `.viz-creators-table th` | 500 | 700 | Table heading |
| `.clear-filters` | 500 | 400 | Label |
| `.results-count` | 500 | 400 | Metadata |
| `.view-btn` | 500 | 400 | Small toggle |
| `.creator-tag` | 500 | 400 | Chip/tag |
| `.filter-badge` | 500 | 400 | Count badge chip |
| `.hero-link` | 500 | 400 | Nav link |
| `.bubble-label` | 500 | 400 | SVG viz label |
| `.viz-creators-table a` | 500 | 400 | Link |
| `.legend-item span` | 500 | 400 | Label |
| `.mobile-menu-link` | 500 | 400 | Nav link |
| `.atlas-drawer-select-count` | 500 | 400 | Count metadata |
| `.atlas-drawer-card-tag` | 500 | 400 | Chip/tag |

---

## Flagged for James

These items require James's decision before any code change. Do not fix.

| File | Line | Value | Context | Question |
|------|------|-------|---------|----------|
| `index.html` | 1411–1419 | `'#ff66ff'`, `'#00e5ff'`, `'#ffaa00'`, `'#4db8ff'`, `'#ff33cc'`, `'#ff4422'` | `CLUSTERS` color array used for hero viz bubbles — same role as `ATLAS_VIZ_COLORS` | These colors are not in DESIGN-TOKENS.md. Are these the sanctioned topic-cluster colors? Needs James sign-off per CLAUDE.md § Out of Scope. |

---

## Token-Compliant Informational Notes

**No violations, but worth knowing:**

- `search.html` load order: `variables.css` → `main.css` → `header.css` — correct. `main.css` as page-specific sheet between variables and header is the intended pattern.
- All 12 `partners/*.html` pages: load order is correct — `variables.css` first, inline `<style>`, `header.css` last. `header.js` is first script in `<body>`.
- `city-lab-dc-v3.html`, `latin-america-lab.html`, `nj-lab.html`, `city-lab-chicago.html`: all have correct load order.
- `index.html`, `postcard.html`, `pulse.html`, `for-brands.html`, `contact.html`: correct load order.
- `for-brands.html` line 362: `.form-submit` uses `background: #97d600` (lime green) on white `.form-section` — correct per surface rule.
- `about-this-project.html` line 403: `.governance-box strong { color: #ceff00 }` — element is inside `.governance-box { background: #000 }` — acid green on dark surface, correct.
- `nj-lab.html` lines 253, 330, 352, 356, 357: all acid green usages confirmed on `.section-dark { background: #313131 }` or `.cta-section { background: #313131 }` — correct.
- `pulse.html` lines 74, 83, 1061: all acid green usages confirmed on `.page-header { background: #111111 }` — correct.
- `city-lab-chicago.html` lines 345, 362, 371, 390, 478: acid green on `#111` or `#000` dark surfaces — correct.
- Redundant local `:root` alias blocks on partner pages (redefining `--acid`, `--lime`, `--olive`, etc. with correct values) — these match variables.css values exactly, so they are redundant but not violations. Leave for now unless a dedicated cleanup session is approved.
- `variables.css` `--weight-medium: 500` variable retained for transition period; comment updated to reflect it is no longer in the approved set (May 2026).

---

## Load Order Compliance

| Page | variables.css first | header.css last in head | header.js first in body | Status |
|------|---------------------|------------------------|------------------------|--------|
| `index.html` | ✓ L31 | ✓ L567 | ✓ L570 | PASS |
| `search.html` | ✓ L37 | ✓ L39 | ✓ L42 | PASS |
| `postcard.html` | ✓ L21 | ✓ L1170 | ✓ L1173 | PASS |
| `about-this-project.html` | ✓ (fixed) | ✓ L457 | ✓ L460 | FIXED |
| `who-we-are.html` | ✓ (fixed) | ✓ L204 | ✓ L207 | FIXED |
| `advisory.html` | ✓ (fixed) | ✓ L254 | ✓ L257 | FIXED |
| `contact.html` | ✓ L25 | ✓ L123 | ✓ L126 | PASS |
| `submit.html` | ✓ (fixed) | ✓ L253 | ✓ L256 | FIXED |
| `submit-thanks.html` | ✓ (fixed) | ✓ L205 | ✓ L208 | FIXED |
| `how-we-did-this.html` | ✓ (fixed) | ✓ L187 | ✓ L190 | FIXED |
| `research.html` | ✓ (fixed) | ✓ L248 | ✓ L251 | FIXED |
| `updates.html` | ✓ (fixed) | ✓ L283 | ✓ L286 | FIXED |
| `pulse.html` | ✓ L18 | ✓ L737 | ✓ L740 | PASS |
| `for-brands.html` | ✓ L23 | ✓ L504 | ✓ L508 | PASS |
| `nj-lab.html` | ✓ L19 | ✓ L403 | ✓ L406 | PASS |
| `city-lab-chicago.html` | ✓ L18 | ✓ L538 | ✓ L541 | PASS |
| `city-lab-dc-v3.html` | ✓ L17 | ✓ L805 | ✓ L808 | PASS |
| `latin-america-lab.html` | ✓ L18 | ✓ L676 | ✓ L679 | PASS |
| `partners/cillizza.html` | ✓ L13 | ✓ L277 | ✓ L280 | PASS |
| `partners/ahp.html` | ✓ L13 | ✓ L277 | ✓ L280 | PASS |
| `partners/icfj.html` | ✓ L13 | ✓ L154 | ✓ L157 | PASS |
| `partners/news-creator-corps.html` | ✓ L13 | ✓ L150 | ✓ L153 | PASS |
| `partners/joon-lee.html` | ✓ L13 | ✓ L79 | ✓ L82 | PASS |
| `partners/jessica-stahl.html` | ✓ L13 | ✓ L124 | ✓ L127 | PASS |
| `partners/knowledge-creators.html` | ✓ L13 | ✓ L87 | ✓ L90 | PASS |
| `partners/emily-atkin.html` | ✓ L13 | ✓ L223 | ✓ L226 | PASS |
| `partners/natgeo.html` | ✓ L13 | ✓ L77 | ✓ L80 | PASS |
| `partners/karen-attiah.html` | ✓ L13 | ✓ L77 | ✓ L80 | PASS |
| `partners/rahim-jessani.html` | ✓ L13 | ✓ L130 | ✓ L133 | PASS |
| `partners/noah-smith.html` | ✓ L13 | ✓ L130 | ✓ L133 | PASS |

---

## Files Not In Scope (Internal/Dev-Only — Not Audited)

Per CLAUDE.md internal list: `chicago-analysis.html`, `city-lab-dc2.html`, `bluesky-intelligence.html`, `beat-tech.html`, `beat-climate.html`, `beat-finance.html`, `chicago-survey.html`, `knight-brief.html`, `atlas-signal-brief.html`, `index-exploration-V1.html`, `index-pre-homepage.html`, `partners/_shell.html`, `atlas-portal/`, `field-study-v11.html`, `search-mock-V1.html`. These were excluded from all checks above.
