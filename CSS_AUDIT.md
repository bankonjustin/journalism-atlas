# Atlas CSS Token Compliance Audit
*Last updated: 2026-05-19*
*Reference: DESIGN-TOKENS.md (James — james@happicamp.com)*

---

## Summary

| Category | Count |
|---|---|
| Violations fixed this session | 11 |
| Flagged for James | 7 |
| Flagged for Justin | 9 |
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

---

## Flagged for James

These items require James's decision before any code change. Do not fix.

| File | Line | Value | Context | Question |
|------|------|-------|---------|----------|
| `index.html` | 1411–1419 | `'#ff66ff'`, `'#00e5ff'`, `'#ffaa00'`, `'#4db8ff'`, `'#ff33cc'`, `'#ff4422'` | `CLUSTERS` color array used for hero viz bubbles — same role as `ATLAS_VIZ_COLORS` | These colors are not in DESIGN-TOKENS.md. Are these the sanctioned topic-cluster colors? Needs James sign-off per CLAUDE.md § Out of Scope. |
| `index.html` | 44 | `background: #d8ff33` | `.btn-acid:hover` — hover state on acid green button (dark bg) | `#d8ff33` is not in DESIGN-TOKENS.md. Intended as a lighter acid-green hover? Needs James to either confirm or assign a token. |
| `for-brands.html` | 64, 423 | `background: #d8ff33` | `.btn-primary:hover` and `.bf-submit:hover` — hover on dark-bg buttons | Same unknown color as above. Confirm or tokenize. |
| `nj-lab.html` | 354 | `background: #b8e600` | `.cta-primary:hover` | Not in DESIGN-TOKENS.md. Lighter lime-green variant for hover? Needs token or James decision. |
| `city-lab-chicago.html` | 617 | `background: #ceff00` | `.legend-dot` (beat coverage map) on white body background — visualization legend | Visualization legend dot using acid green on a light surface. Is this intentional as a viz data marker (not UI chrome)? Flag because the rule says acid green = dark surfaces only, but this is a data legend. James to confirm whether viz legends are exempt. |
| `header.css` | 253–261 | `font-family: 'DM Mono', monospace` | Shared site footer (`.footer-tagline`, `.footer-col-title`, `.footer-copy`, `.footer-legal a`) | `DM Mono` is not in DESIGN-TOKENS.md. Approved typefaces are Hanken Grotesk, Merriweather, JetBrains Mono. Should footer monospace be migrated to `JetBrains Mono`? James to confirm. |
| `index.html` | multiple | `font-family: 'DM Mono', monospace` | Used ~63 times across eyebrows, data labels, stat strips, cluster cards, pulse section | Same issue — `DM Mono` not in approved font list. Index.html is heavily reliant on it. Needs James design decision before a bulk migration. |

---

## Flagged for Justin

These need your explicit confirmation before changing.

| File | Line | Value | Context | Question |
|------|------|-------|---------|----------|
| `assets/css/main.css` | multiple | `font-weight: 500` | Used ~20 times across `.filter-accordion-header h3`, `.clear-filters`, `.view-btn`, `.results-count`, `.mobile-filter-toggle`, `.creator-tag`, and others. `main.css` is `search.html`'s primary stylesheet. | DESIGN-TOKENS.md (May 2026) removed `500` from approved weights. This is systemic across `main.css`. Confirm before bulk changing to `400` or `700` — some of these labels may need editorial judgment on which weight fits. |
| `partners/*.html` | multiple | `font-weight: 500` | All 12 partner pages use weight 500 extensively (~185 instances total) for labels, chips, sub-headings, card metadata | Same issue. Partner pages share a template pattern with consistent use of 500. Confirm this entire pattern should shift to 400 (regular). Suggest doing a dedicated session sweep. |
| `index.html` | multiple | `font-weight: 500` | ~15 instances across `.hero-stat-badge-num`, `.stat-lbl`, `.featured-pub`, `.cluster-count-n`, `.cluster-creator-name`, `.pulse-beat-name`, etc. | Same. Confirm direction — particularly for numeric/data labels where 500 is visually distinct from 400. |
| `research.html` | 147, 158, 276, 282, 296, 301, 306, 330, 336 | `font-weight: 600` | Publication names, link text, "Coming June 2026" line | `600` is explicitly not approved. Need to confirm: change to `700`? |
| `city-lab-chicago.html` | 1197, 1980, 1981 | `font-weight: 600` | "Tell us →" link, creator name in table cell JS template | Same — `600` not approved. Change to `700`? |
| `submit.html` / `submit-thanks.html` / `updates.html` | 37–40 | `--lime-green: #d4ff33; --light-gray: #f5f5f5; --dark-gray: #666666` | Local `:root` overrides using wrong token values — `#d4ff33` is not lime green, `#f5f5f5` is not the canonical light gray, `#666666` is not dark gray | These pages override the canonical values with wrong colors. Now that `variables.css` is loaded first, the local `:root` block will win on specificity (same selector, later in cascade). Recommend deleting the inline `:root` blocks on these pages and relying fully on `variables.css`. Confirm before touching. |
| `for-brands.html` | 362, 367 | `background: #97d600` / `#a8e800` | `.form-submit` on white `.form-section` — primary button correct; hover `#a8e800` not in DESIGN-TOKENS.md | The hover value `#a8e800` is unknown. Is this intentional, or should it be `var(--color-dark-olive)` (#5d7400)? |
| `advisory.html` | 237 | `font-weight: 500` | `.about-subnav-link` — shared subnav across the about section group | Part of the systemic 500 issue. Specifically: subnav link weight. Likely `400` after the sweep. |
| `index.html` | 484 | `font-weight: 600` | `.drawer-creator-name` on dark drawer overlay | `600` not approved. Should be `700`? Confirm. |

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
- `variables.css` internal note says `--weight-medium: 500` and comment says "500 (labels/UI)" — this conflicts with the May 2026 DESIGN-TOKENS.md decision removing 500. The `variables.css` comment needs updating when the systemic weight-500 sweep is done.

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
