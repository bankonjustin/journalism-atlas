# V13 Greens audit (report only, nothing applied)

*2026-10-06, against DESIGN-TOKENS-v13.md § Greens by Surface. Covers `#ceff00` acid, `#97d600` lime and `#5d7400` olive, as hex, `rgb()`/`rgba()`, and through `var()` (including `--color-accent` and every alias, resolved per file so inline `:root` overrides count). Full row list: `V13-GREENS-AUDIT-2026-10-06.tsv`.*

## How surfaces were determined (and the limits)

- **Static scan** of every tracked `.html/.css/.js` outside `_deprecated`, `_reference`, `outputs`, `sessions` (files named "… copy" are skipped as duplicates): 973 uses, 92 variable definitions.
- **DOM scan**: every page loaded in headless Chromium at 1280px; every element (and `::before`/`::after`) whose computed text, background, border, outline, shadow, underline or SVG fill/stroke is one of the three greens was recorded with the **real backdrop** (ancestors composited down to the first opaque background; luminance < 0.18 = dark). Each static hit is joined to DOM observations by class and color. That gives a measured surface for what renders at load.
- **Not measured:** hover/focus/active/modal/menu states that are not showing at load (their surface is inherited from the same element's load-time observation when one exists), content injected by JS after a click, and mobile layouts. Static hits whose element never rendered are `unobserved` and listed separately; they need a human look. Gradient backdrops are `unknown`. 6 pages timed out waiting for network idle (external fonts/embeds) but were still scanned.
- Violations follow v13: acid or lime as text/icon/stroke on a light surface; focus ring on light; fills with text other than black or step 6; olive on dark.

## Summary

| category | acid | lime | olive |
|---|---|---|---|
| V1 | 36 | 83 | 0 |
| V2 | 5 | 45 | 0 |
| V3 | 5 | 2 | 0 |
| U | 82 | 14 | 0 |
| J | 20 | 7 | 0 |
| OLIVE-ON-DARK | 0 | 0 | 1 |
| OLIVE-FILL | 0 | 0 | 17 |
| OLIVE-KEEP | 0 | 0 | 143 |
| OLIVE-REVIEW | 0 | 0 | 7 |
| OK | 416 | 90 | 0 |

Legend: J = color set in JavaScript · V1 = text/icon/stroke on light · V2 = focus ring on light · V3 = acid/lime fill with non-black/non-step-6 text on top · U = surface unobserved · OLIVE-* are the olive classes (the olive table has the detail) · OK = compliant (dark surface or fill with black/step-6 text).

DOM-only findings (rendered, no static source matched): 183 elements; violations among them: 2 (listed below).

**Where the V1/V2 violations concentrate:** atlas-portal/index.html (13), assets/css/main.css (12), bluesky-creator-intelligence.html (12), pulse.html (10), city-lab-chicago.html (9), for-brands.html (9), about-this-project.html (5), partners/_shell.html (5).

## V2 — focus ring (outline) in lime/acid on a light surface (50)

Includes anything using `--focus-ring-light` (`2px solid #97d600`) and any `outline`/`:focus` rule. Fix: `var(--color-focus-on-light)` (olive).

| file:line | element | property | color | surface | proposed fix |
|---|---|---|---|---|---|
| assets/css/header.css:139 | `.nav-search:focus` :focus | outline | lime via `var:--focus-ring-light` | light | var(--color-focus-on-light) (olive #5d7400) |
| assets/css/header.css:141 | `.nav-search:focus` :focus | border-color | lime via `var:--lime-green` | light | var(--color-focus-on-light) (olive #5d7400) |
| assets/css/header.css:142 | `.nav-search:focus` :focus | box-shadow | lime via `rgba(151, 214, 0, 0.15)` | light | var(--color-focus-on-light) (olive #5d7400) |
| assets/css/main.css:94 | `.nav-search:focus` :focus | outline | lime via `var:--focus-ring-light` | light | var(--color-focus-on-light) (olive #5d7400) |
| assets/css/main.css:96 | `.nav-search:focus` :focus | border-color | lime via `var:--lime-green` | light | var(--color-focus-on-light) (olive #5d7400) |
| assets/css/main.css:97 | `.nav-search:focus` :focus | box-shadow | lime via `rgba(151, 214, 0, 0.15)` | light | var(--color-focus-on-light) (olive #5d7400) |
| assets/css/main.css:369 | `.filter-search:focus` :focus | outline | lime via `var:--focus-ring-light` | light | var(--color-focus-on-light) (olive #5d7400) |
| assets/css/main.css:371 | `.filter-search:focus` :focus | border-color | lime via `var:--lime-green` | light | var(--color-focus-on-light) (olive #5d7400) |
| assets/css/main.css:1972 | `.pack-name-input:focus` :focus | outline | lime via `var:--focus-ring-light` | light | var(--color-focus-on-light) (olive #5d7400) |
| assets/css/main.css:1974 | `.pack-name-input:focus` :focus | border-color | lime via `var:--lime-green` | light | var(--color-focus-on-light) (olive #5d7400) |
| atlas-portal/index.html:226 | `ut[type="file"]:focus, input[type="text"]:focus, input[type=` :focus | border-color | acid via `var:--acid-green` | light | var(--color-focus-on-light) (olive #5d7400) |
| atlas-portal/index.html:227 | `ut[type="file"]:focus, input[type="text"]:focus, input[type=` :focus | box-shadow | acid via `rgba(206, 255, 0, 0.1)` | light | var(--color-focus-on-light) (olive #5d7400) |
| bluesky-creator-intelligence.html:158 | `.search-input:focus` :focus | border-color | lime via `var:--lime` | light | var(--color-focus-on-light) (olive #5d7400) |
| chicago-survey.html:250 | `input:focus, textarea:focus, select:focus` :focus | border-color | acid via `var:--lime` | mixed | var(--color-focus-on-light) (olive #5d7400) |
| chicago-survey.html:251 | `input:focus, textarea:focus, select:focus` :focus | background | acid via `rgba(206,255,0,0.04)` | mixed | var(--color-focus-on-light) (olive #5d7400) |
| chicago-survey.html:252 | `input:focus, textarea:focus, select:focus` :focus | box-shadow | acid via `rgba(206,255,0,0.08)` | mixed | var(--color-focus-on-light) (olive #5d7400) |
| city-lab-chicago.html:234 | `-visible, .plat-chip:focus-visible, .layer-stat-btn:focus-vi` :focus | outline | lime via `#97d600` | light | var(--color-focus-on-light) (olive #5d7400) |
| for-brands.html:277 | `.form-input:focus, .form-textarea:focus` :focus | border-color | lime via `#97d600` | light | var(--color-focus-on-light) (olive #5d7400) |
| for-brands.html:278 | `.form-input:focus, .form-textarea:focus` :focus | box-shadow | lime via `rgba(151,214,0,0.15)` | light | var(--color-focus-on-light) (olive #5d7400) |
| index.html:349 | `.db-filter-input:focus` :focus | border-color | lime via `#97d600` | light | var(--color-focus-on-light) (olive #5d7400) |
| partners/_shell.html:59 | `.site-nav-link:focus-visible` :focus | outline | lime via `var:--lime` | light | var(--color-focus-on-light) (olive #5d7400) |
| partners/_shell.html:151 | `.card-link:focus-visible` :focus | outline | lime via `var:--lime` | light | var(--color-focus-on-light) (olive #5d7400) |
| partners/_shell.html:208 | `.atlas-footer-btn:focus-visible` :focus | outline | lime via `var:--lime` | light | var(--color-focus-on-light) (olive #5d7400) |
| partners/ahp.html:116 | `.chip:focus-visible` :focus | outline | lime via `var:--lime` | light | var(--color-focus-on-light) (olive #5d7400) |
| partners/ahp.html:191 | `.card-link:focus-visible` :focus | outline | lime via `var:--lime` | light | var(--color-focus-on-light) (olive #5d7400) |
| partners/ahp.html:246 | `.atlas-footer-btn:focus-visible` :focus | outline | lime via `var:--lime` | light | var(--color-focus-on-light) (olive #5d7400) |
| partners/cillizza.html:112 | `.chip:focus-visible` :focus | outline | lime via `var:--lime` | light | var(--color-focus-on-light) (olive #5d7400) |
| partners/cillizza.html:179 | `.card-link:focus-visible` :focus | outline | lime via `var:--lime` | light | var(--color-focus-on-light) (olive #5d7400) |
| partners/cillizza.html:238 | `.atlas-footer-btn:focus-visible` :focus | outline | lime via `var:--lime` | light | var(--color-focus-on-light) (olive #5d7400) |
| partners/emily-atkin.html:143 | `.card-link:focus-visible` :focus | outline | lime via `var:--lime` | light | var(--color-focus-on-light) (olive #5d7400) |
| partners/emily-atkin.html:186 | `.atlas-footer-btn:focus-visible` :focus | outline | lime via `var:--lime` | light | var(--color-focus-on-light) (olive #5d7400) |
| partners/icfj.html:70 | `.chip:focus-visible` :focus | outline | lime via `var:--lime` | light | var(--color-focus-on-light) (olive #5d7400) |
| partners/icfj.html:94 | `.card-link:focus-visible` :focus | outline | lime via `var:--lime` | light | var(--color-focus-on-light) (olive #5d7400) |
| partners/icfj.html:124 | `.atlas-footer-btn:focus-visible` :focus | outline | lime via `var:--lime` | light | var(--color-focus-on-light) (olive #5d7400) |
| partners/iij.html:65 | `.chip:focus-visible` :focus | outline | lime via `var:--lime` | light | var(--color-focus-on-light) (olive #5d7400) |
| partners/iij.html:85 | `.card-link:focus-visible` :focus | outline | lime via `var:--lime` | light | var(--color-focus-on-light) (olive #5d7400) |
| partners/iij.html:115 | `.atlas-footer-btn:focus-visible` :focus | outline | lime via `var:--lime` | light | var(--color-focus-on-light) (olive #5d7400) |
| partners/jessica-stahl.html:59 | `.chip:focus-visible` :focus | outline | lime via `var:--lime` | light | var(--color-focus-on-light) (olive #5d7400) |
| partners/jessica-stahl.html:82 | `.card-link:focus-visible` :focus | outline | lime via `var:--lime` | light | var(--color-focus-on-light) (olive #5d7400) |
| partners/jessica-stahl.html:109 | `.atlas-footer-btn:focus-visible` :focus | outline | lime via `var:--lime` | light | var(--color-focus-on-light) (olive #5d7400) |
| partners/knowledge-creators.html:43 | `.chip:focus-visible` :focus | outline | lime via `var:--lime` | light | var(--color-focus-on-light) (olive #5d7400) |
| partners/news-creator-corps.html:66 | `.chip:focus-visible` :focus | outline | lime via `var:--lime` | light | var(--color-focus-on-light) (olive #5d7400) |
| partners/news-creator-corps.html:93 | `.card-link:focus-visible` :focus | outline | lime via `var:--lime` | light | var(--color-focus-on-light) (olive #5d7400) |
| partners/news-creator-corps.html:124 | `.atlas-footer-btn:focus-visible` :focus | outline | lime via `var:--lime` | light | var(--color-focus-on-light) (olive #5d7400) |
| partners/nj-lab.html:365 | `.filter-chip:focus-visible, .cta-btn:focus-visible` :focus | outline | lime via `#97d600` | light | var(--color-focus-on-light) (olive #5d7400) |
| partners/njlab.html:365 | `.filter-chip:focus-visible, .cta-btn:focus-visible` :focus | outline | lime via `#97d600` | light | var(--color-focus-on-light) (olive #5d7400) |
| partners/noah-smith.html:76 | `.card-link:focus-visible` :focus | outline | lime via `var:--lime` | light | var(--color-focus-on-light) (olive #5d7400) |
| partners/noah-smith.html:107 | `.atlas-footer-btn:focus-visible` :focus | outline | lime via `var:--lime` | light | var(--color-focus-on-light) (olive #5d7400) |
| partners/rahim-jessani.html:76 | `.card-link:focus-visible` :focus | outline | lime via `var:--lime` | light | var(--color-focus-on-light) (olive #5d7400) |
| partners/rahim-jessani.html:106 | `.atlas-footer-btn:focus-visible` :focus | outline | lime via `var:--lime` | light | var(--color-focus-on-light) (olive #5d7400) |

## V1 — acid/lime as text, icon or stroke on a light surface (119)

Note: lime via `var(--color-accent)` is the site's primary light-surface accent; every consumer of it that is text/icon/stroke on light lands here. Fills are not here. Fix is olive via `var(--color-accent-on-light)` for text, icons and strokes.

| file:line | element | property | color | surface | proposed fix |
|---|---|---|---|---|---|
| about-this-project.html:68 | `.about-subnav-link--active` | border-bottom-color | lime via `#97d600` | light | var(--color-accent-on-light) (olive #5d7400) (underline/border: same) |
| about-this-project.html:112 | `.about-read-more` | border-bottom | lime via `#97d600` | light | var(--color-accent-on-light) (olive #5d7400) (underline/border: same) |
| about-this-project.html:140 | `.pillar-card` | border-top | lime via `#97d600` | light | var(--color-accent-on-light) (olive #5d7400) (underline/border: same) |
| about-this-project.html:263 | `.funding-box` | border-left | lime via `#97d600` | light | var(--color-accent-on-light) (olive #5d7400) (underline/border: same) |
| about-this-project.html:371 | `.board-title` | border-bottom | lime via `#97d600` | light | var(--color-accent-on-light) (olive #5d7400) (underline/border: same) |
| advisory.html:251 | `.about-subnav-link--active` | border-bottom-color | lime via `#97d600` | light | var(--color-accent-on-light) (olive #5d7400) (underline/border: same) |
| assets/css/header.css:315 | `.mobile-menu-link:hover, .mobile-menu-link:active` :hover | border-left-color | lime via `var:--lime-green` | mixed | var(--color-accent-on-light) (olive #5d7400) (underline/border: same) |
| assets/css/main.css:559 | `.creator-card.selected` .selected | border | lime via `var:--color-accent` | mixed | var(--color-accent-on-light) (olive #5d7400) (underline/border: same) |
| assets/css/main.css:833 | `.bubble-mode-btn.active` .active | border-bottom-color | lime via `var:--lime-green` | light | var(--color-accent-on-light) (olive #5d7400) (underline/border: same) |
| assets/css/main.css:1225 | `.legend-item:hover` :hover | border-color | lime via `var:--lime-green` | light | var(--color-accent-on-light) (olive #5d7400) (underline/border: same) |
| assets/css/main.css:1327 | `.loading-spinner` | border-top-color | lime via `var:--lime-green` | light | var(--color-accent-on-light) (olive #5d7400) (underline/border: same) |
| assets/css/main.css:1430 | `.mobile-menu-link:hover, .mobile-menu-link:active` :hover | border-left-color | lime via `var:--lime-green` | mixed | var(--color-accent-on-light) (olive #5d7400) (underline/border: same) |
| atlas-portal/index.html:258 | `.radio-option:hover` :hover | border-color | lime via `var:--lime-green` | light | var(--color-accent-on-light) (olive #5d7400) (underline/border: same) |
| atlas-portal/index.html:270 | `.radio-option.selected` .selected | border-color | acid via `var:--acid-green` | light | var(--color-accent-on-light) (olive #5d7400) (underline/border: same) |
| atlas-portal/index.html:335 | `.text-color-option:hover` :hover | border-color | lime via `var:--lime-green` | light | var(--color-accent-on-light) (olive #5d7400) (underline/border: same) |
| atlas-portal/index.html:339 | `.text-color-option.selected` .selected | border-color | acid via `var:--acid-green` | light | var(--color-accent-on-light) (olive #5d7400) (underline/border: same) |
| atlas-portal/index.html:369 | `.image-preview` | border | acid via `var:--acid-green` | light | var(--color-accent-on-light) (olive #5d7400) (underline/border: same) |
| atlas-portal/index.html:403 | `.btn:hover` :hover | box-shadow | acid via `rgba(206, 255, 0, 0.3)` | light | var(--color-accent-on-light) (olive #5d7400) (underline/border: same) |
| atlas-portal/index.html:460 | `.disclosure-box` | border-left | acid via `var:--acid-green` | light | var(--color-accent-on-light) (olive #5d7400) (underline/border: same) |
| atlas-portal/index.html:511 | `.message.success` | border | lime via `var:--lime-green` | light | var(--color-accent-on-light) (olive #5d7400) (underline/border: same) |
| atlas-portal/index.html:562 | `.caption-box:hover` :hover | border-color | lime via `var:--lime-green` | light | var(--color-accent-on-light) (olive #5d7400) (underline/border: same) |
| atlas-portal/index.html:608 | `.footer-section a` | border-bottom | acid via `var:--acid-green` | light | var(--color-accent-on-light) (olive #5d7400) (underline/border: same) |
| atlas-portal/index.html:614 | `.footer-section a:hover` :hover | border-bottom-color | lime via `var:--lime-green` | light | var(--color-accent-on-light) (olive #5d7400) (underline/border: same) |
| atlas-signal-brief.html:27 | `.tab-btn.active` .active | border-bottom-color | acid via `#ceff00` | light | var(--color-accent-on-light) (olive #5d7400) (underline/border: same) |
| atlas-signal-brief.html:97 | `.vel-card:hover` :hover | border-color | lime via `#97d600` | light | var(--color-accent-on-light) (olive #5d7400) (underline/border: same) |
| atlas-signal-brief.html:109 | `.callout-box` | border-left | acid via `#ceff00` | light | var(--color-accent-on-light) (olive #5d7400) (underline/border: same) |
| atlas-signal-brief.html:161 | `.poly-card:hover` :hover | border-color | lime via `#97d600` | light | var(--color-accent-on-light) (olive #5d7400) (underline/border: same) |
| beat-climate.html:88 | `.story-card:hover` :hover | border-color | lime via `#97d600` | light | var(--color-accent-on-light) (olive #5d7400) (underline/border: same) |
| bluesky-creator-intelligence.html:52 | `.badge-atlas` | border | lime via `rgba(151,214,0,0.5)` | light | var(--color-accent-on-light) (olive #5d7400) (underline/border: same) |
| bluesky-creator-intelligence.html:64 | `.hero-title .accent` | color | lime via `var:--lime` | light | var(--color-accent-on-light) (olive #5d7400) |
| bluesky-creator-intelligence.html:84 | `.stat-num` | color | lime via `var:--lime` | light | var(--color-accent-on-light) (olive #5d7400) |
| bluesky-creator-intelligence.html:104 | `.cluster-card.active` .active | border-color | lime via `var:--lime` | light | var(--color-accent-on-light) (olive #5d7400) (underline/border: same) |
| bluesky-creator-intelligence.html:104 | `.cluster-card.active` .active | box-shadow | lime via `rgba(151,214,0,0.25)` | light | var(--color-accent-on-light) (olive #5d7400) (underline/border: same) |
| bluesky-creator-intelligence.html:108 | `.cluster-count .n` | color | lime via `var:--lime` | light | var(--color-accent-on-light) (olive #5d7400) |
| bluesky-creator-intelligence.html:172 | `.sort-btn.active` .active | border-color | lime via `var:--lime` | light | var(--color-accent-on-light) (olive #5d7400) (underline/border: same) |
| bluesky-creator-intelligence.html:179 | `.filter-pill:hover` :hover | border-color | lime via `var:--lime` | light | var(--color-accent-on-light) (olive #5d7400) (underline/border: same) |
| bluesky-creator-intelligence.html:180 | `.filter-pill.active` .active | border-color | lime via `var:--lime` | light | var(--color-accent-on-light) (olive #5d7400) (underline/border: same) |
| bluesky-creator-intelligence.html:199 | `.ci-platform.cross` | border-color | lime via `rgba(151,214,0,0.4)` | light | var(--color-accent-on-light) (olive #5d7400) (underline/border: same) |
| bluesky-creator-intelligence.html:201 | `.ci-followers` | color | lime via `var:--lime` | light | var(--color-accent-on-light) (olive #5d7400) |
| chicago-analysis.html:47 | `.nav button:hover` :hover | color | acid via `var:--neon` | mixed | var(--color-accent-on-light) (olive #5d7400) |
| chicago-analysis.html:47 | `.nav button:hover` :hover | border-color | acid via `rgba(206,255,0,0.3)` | mixed | var(--color-accent-on-light) (olive #5d7400) (underline/border: same) |
| chicago-analysis.html:48 | `.nav button.active` .active | border-color | acid via `var:--neon` | mixed | var(--color-accent-on-light) (olive #5d7400) (underline/border: same) |
| city-lab-chicago.html:53 | `.two-layer-note` | border-left | lime via `#97d600` | light | var(--color-accent-on-light) (olive #5d7400) (underline/border: same) |
| city-lab-chicago.html:65 | `.tab-btn.active` .active | border-bottom-color | lime via `#97d600` | light | var(--color-accent-on-light) (olive #5d7400) (underline/border: same) |
| city-lab-chicago.html:169 | `.creator-row-body` | border-left | lime via `#97d600` | light | var(--color-accent-on-light) (olive #5d7400) (underline/border: same) |
| city-lab-chicago.html:172 | `.row-pulse` | color | lime via `#97d600` | light | var(--color-accent-on-light) (olive #5d7400) |
| city-lab-chicago.html:219 | `.pulse-badge-dot` | color | lime via `#97d600` | light | var(--color-accent-on-light) (olive #5d7400) |
| city-lab-chicago.html:223 | `.beat-headline-card:hover` :hover | border-color | lime via `#97d600` | light | var(--color-accent-on-light) (olive #5d7400) (underline/border: same) |
| city-lab-chicago.html:415 | `<div> (inline)` | border-left | lime via `#97d600` | mixed | var(--color-accent-on-light) (olive #5d7400) (underline/border: same) |
| city-lab-chicago.html:571 | `<a> (inline)` | color | acid via `rgba(206,255,0,0.6)` | mixed | var(--color-accent-on-light) (olive #5d7400) |
| city-lab-dc-v3.html:887 | `<div> (inline)` | color | acid via `var:--acid` | mixed | var(--color-accent-on-light) (olive #5d7400) |
| city-lab-dc-v3.html:920 | `<div> (inline)` | border-left | acid via `var:--acid` | mixed | var(--color-accent-on-light) (olive #5d7400) (underline/border: same) |
| city-lab-dc-v3.html:921 | `<div> (inline)` | color | acid via `var:--acid` | mixed | var(--color-accent-on-light) (olive #5d7400) |
| city-lab-dc-v3.html:1410 | `<a> (inline)` | color | acid via `rgba(206,255,0,0.6)` | mixed | var(--color-accent-on-light) (olive #5d7400) |
| for-brands.html:193 | `.trust-cite-view-all` | color | lime via `#97d600` | light | var(--color-accent-on-light) (olive #5d7400) |
| for-brands.html:436 | `.compare-headline-emphasis.is-visible` | color | lime via `#97d600` | light | var(--color-accent-on-light) (olive #5d7400) |
| for-brands.html:445 | `.bx-chip--active` | border-color | acid via `#ceff00` | mixed | var(--color-accent-on-light) (olive #5d7400) (underline/border: same) |
| for-brands.html:445 | `.bx-chip--active` | box-shadow | acid via `rgba(206,255,0,0.25)` | mixed | var(--color-accent-on-light) (olive #5d7400) (underline/border: same) |
| for-brands.html:875 | `<a> (inline)` | color | acid via `rgba(206,255,0,0.5)` | mixed | var(--color-accent-on-light) (olive #5d7400) |
| for-brands.html:875 | `<a> (inline)` | color | acid via `#ceff00` | mixed | var(--color-accent-on-light) (olive #5d7400) |
| for-brands.html:875 | `<a> (inline)` | color | acid via `rgba(206,255,0,0.5)` | mixed | var(--color-accent-on-light) (olive #5d7400) |
| how-we-did-this.html:134 | `.content-section li:before` | color | acid via `var:--acid-green` | light | var(--color-accent-on-light) (olive #5d7400) |
| how-we-did-this.html:184 | `.about-subnav-link--active` | border-bottom-color | lime via `#97d600` | light | var(--color-accent-on-light) (olive #5d7400) (underline/border: same) |
| index.html:308 | `.research-badge` | border | lime via `rgba(151,214,0,0.3)` | light | var(--color-accent-on-light) (olive #5d7400) (underline/border: same) |
| latin-america-lab.html:267 | `.filter-pill.active` .active | border-color | acid via `var:--page-accent` | mixed | var(--color-accent-on-light) (olive #5d7400) (underline/border: same) |
| latin-america-lab.html:896 | `<a> (inline)` | color | acid via `rgba(206,255,0,0.6)` | mixed | var(--color-accent-on-light) (olive #5d7400) |
| lists.html:57 | `.nav-link:hover, .nav-link.active` :hover | color | acid via `var:--acid-green` | light | var(--color-accent-on-light) (olive #5d7400) |
| mobile.html:73 | `.spinner` | border | acid via `rgba(206, 255, 0, 0.3)` | light | var(--color-accent-on-light) (olive #5d7400) (underline/border: same) |
| mobile.html:74 | `.spinner` | border-top-color | acid via `var:--acid-green` | light | var(--color-accent-on-light) (olive #5d7400) (underline/border: same) |
| partners/_shell.html:112 | `.creator-card:hover` :hover | border-color | lime via `var:--lime` | light | var(--color-accent-on-light) (olive #5d7400) (underline/border: same) |
| partners/_shell.html:134 | `.pill.platform:hover` :hover | border-color | lime via `#97d600` | light | var(--color-accent-on-light) (olive #5d7400) (underline/border: same) |
| partners/ahp.html:131 | `.act-label` | color | lime via `var:--lime` | light | var(--color-accent-on-light) (olive #5d7400) |
| partners/ahp.html:174 | `.pill.platform:hover` :hover | border-color | lime via `#97d600` | light | var(--color-accent-on-light) (olive #5d7400) (underline/border: same) |
| partners/cillizza.html:127 | `.act-label` | color | lime via `var:--lime` | light | var(--color-accent-on-light) (olive #5d7400) |
| partners/cillizza.html:164 | `.pill.platform:hover` :hover | border-color | lime via `#97d600` | light | var(--color-accent-on-light) (olive #5d7400) (underline/border: same) |
| partners/emily-atkin.html:102 | `.act-label` | color | lime via `var:--lime` | light | var(--color-accent-on-light) (olive #5d7400) |
| partners/emily-atkin.html:132 | `.pill.platform:hover` :hover | border-color | lime via `#97d600` | light | var(--color-accent-on-light) (olive #5d7400) (underline/border: same) |
| partners/icfj.html:74 | `.act-label` | color | lime via `var:--lime` | light | var(--color-accent-on-light) (olive #5d7400) |
| partners/icfj.html:89 | `.pill.platform:hover` :hover | border-color | lime via `#97d600` | light | var(--color-accent-on-light) (olive #5d7400) (underline/border: same) |
| partners/iij.html:69 | `.act-label` | color | lime via `var:--lime` | light | var(--color-accent-on-light) (olive #5d7400) |
| partners/jessica-stahl.html:63 | `.act-label` | color | lime via `var:--lime` | light | var(--color-accent-on-light) (olive #5d7400) |
| partners/jessica-stahl.html:77 | `.pill.platform:hover` :hover | border-color | lime via `#97d600` | light | var(--color-accent-on-light) (olive #5d7400) (underline/border: same) |
| partners/joon-lee.html:38 | `.act-label` | color | lime via `var:--lime` | light | var(--color-accent-on-light) (olive #5d7400) |
| partners/joon-lee.html:51 | `.pill.platform:hover` :hover | border-color | lime via `#97d600` | light | var(--color-accent-on-light) (olive #5d7400) (underline/border: same) |
| partners/karen-attiah.html:37 | `.act-label` | color | lime via `var:--lime` | light | var(--color-accent-on-light) (olive #5d7400) |
| partners/karen-attiah.html:50 | `.pill.platform:hover` :hover | border-color | lime via `#97d600` | light | var(--color-accent-on-light) (olive #5d7400) (underline/border: same) |
| partners/knowledge-creators.html:46 | `.act-label` | color | lime via `var:--lime` | light | var(--color-accent-on-light) (olive #5d7400) |
| partners/knowledge-creators.html:59 | `.pill.platform:hover` :hover | border-color | lime via `#97d600` | light | var(--color-accent-on-light) (olive #5d7400) (underline/border: same) |
| partners/natgeo.html:37 | `.act-label` | color | lime via `var:--lime` | light | var(--color-accent-on-light) (olive #5d7400) |
| partners/natgeo.html:50 | `.pill.platform:hover` :hover | border-color | lime via `#97d600` | light | var(--color-accent-on-light) (olive #5d7400) (underline/border: same) |
| partners/news-creator-corps.html:71 | `.act-label` | color | lime via `var:--lime` | light | var(--color-accent-on-light) (olive #5d7400) |
| partners/news-creator-corps.html:88 | `.pill.platform:hover` :hover | border-color | lime via `#97d600` | light | var(--color-accent-on-light) (olive #5d7400) (underline/border: same) |
| partners/nj-lab.html:353 | `.cta-primary` | border | acid via `#ceff00` | mixed | var(--color-accent-on-light) (olive #5d7400) (underline/border: same) |
| partners/nj-lab.html:355 | `.cta-primary:hover` :hover | border-color | lime via `var:--color-lime-green` | light | var(--color-accent-on-light) (olive #5d7400) (underline/border: same) |
| partners/nj-lab.html:642 | `<a> (inline)` | color | acid via `rgba(206,255,0,0.6)` | mixed | var(--color-accent-on-light) (olive #5d7400) |
| partners/njlab.html:353 | `.cta-primary` | border | acid via `#ceff00` | mixed | var(--color-accent-on-light) (olive #5d7400) (underline/border: same) |
| partners/njlab.html:355 | `.cta-primary:hover` :hover | border-color | lime via `var:--color-lime-green` | light | var(--color-accent-on-light) (olive #5d7400) (underline/border: same) |
| partners/njlab.html:643 | `<a> (inline)` | color | acid via `rgba(206,255,0,0.6)` | mixed | var(--color-accent-on-light) (olive #5d7400) |
| partners/noah-smith.html:54 | `.act-label` | color | lime via `var:--lime` | light | var(--color-accent-on-light) (olive #5d7400) |
| partners/noah-smith.html:71 | `.pill.platform:hover` :hover | border-color | lime via `#97d600` | light | var(--color-accent-on-light) (olive #5d7400) (underline/border: same) |
| partners/rahim-jessani.html:54 | `.act-label` | color | lime via `var:--lime` | light | var(--color-accent-on-light) (olive #5d7400) |
| partners/rahim-jessani.html:71 | `.pill.platform:hover` :hover | border-color | lime via `#97d600` | light | var(--color-accent-on-light) (olive #5d7400) (underline/border: same) |
| pulse.html:147 | `.audience-bridge-link:hover` :hover | color | lime via `#97d600` | light | var(--color-accent-on-light) (olive #5d7400) |
| pulse.html:227 | `.signal-tab.active` .active | border-color | acid via `#ceff00` | mixed | var(--color-accent-on-light) (olive #5d7400) (underline/border: same) |
| pulse.html:244 | `.archive-header` | border-top | acid via `#ceff00` | light | var(--color-accent-on-light) (olive #5d7400) (underline/border: same) |
| pulse.html:250 | `.archive-method a:hover` :hover | color | lime via `#97d600` | light | var(--color-accent-on-light) (olive #5d7400) |
| pulse.html:409 | `.beat-pill.active` .active | border-color | lime via `#97d600` | light | var(--color-accent-on-light) (olive #5d7400) (underline/border: same) |
| pulse.html:713 | `.analysis-tab.active` .active | border-bottom-color | lime via `#97d600` | light | var(--color-accent-on-light) (olive #5d7400) (underline/border: same) |
| pulse.html:806 | `.beat-more-btn:hover` :hover | border-color | lime via `#97d600` | light | var(--color-accent-on-light) (olive #5d7400) (underline/border: same) |
| pulse.html:962 | `a.intel-post-link:hover` :hover | text-decoration-color | lime via `#97d600` | light | var(--color-accent-on-light) (olive #5d7400) (underline/border: same) |
| pulse.html:983 | `.intel-bullet::before` | color | lime via `#97d600` | light | var(--color-accent-on-light) (olive #5d7400) |
| pulse.html:1043 | `.city-spotlight-card` | border-left | lime via `#97d600` | light | var(--color-accent-on-light) (olive #5d7400) (underline/border: same) |
| research.html:423 | `.pub-card:hover` :hover | border-color | lime via `#97d600` | light | var(--color-accent-on-light) (olive #5d7400) (underline/border: same) |
| research.html:528 | `.press-chip:hover` :hover | border-color | lime via `#97d600` | light | var(--color-accent-on-light) (olive #5d7400) (underline/border: same) |
| research.html:681 | `.btn-acid` | border | lime via `#97d600` | light | var(--color-accent-on-light) (olive #5d7400) (underline/border: same) |
| search.html:495 | `.field-dim-btn.active` .active | border-color | acid via `#ceff00` | light | var(--color-accent-on-light) (olive #5d7400) (underline/border: same) |
| submit-thanks.html:134 | `.next-steps li:before` | color | acid via `var:--acid-green` | light | var(--color-accent-on-light) (olive #5d7400) |
| updates.html:113 | `.benefits-list li:before` | color | acid via `var:--acid-green` | light | var(--color-accent-on-light) (olive #5d7400) |
| who-we-are.html:201 | `.about-subnav-link--active` | border-bottom-color | lime via `#97d600` | light | var(--color-accent-on-light) (olive #5d7400) (underline/border: same) |

## V3 — acid/lime fills whose text is not black or step 6 (7)

Measured from the rendered text color on the fill.

| file:line | element | property | color | surface | proposed fix |
|---|---|---|---|---|---|
| for-brands.html:60 | `.btn-primary` | background | acid via `#ceff00` | dark | set text to #000 or var(--gray-cool-6) |
| for-brands.html:132 | `.compare-th--right` | background | lime via `#97d600` | light | set text to #000 or var(--gray-cool-6) |
| for-brands.html:282 | `.form-submit` | background | lime via `#97d600` | light | set text to #000 or var(--gray-cool-6) |
| for-brands.html:338 | `.bf-submit` | background | acid via `#ceff00` | dark | set text to #000 or var(--gray-cool-6) |
| for-brands.html:445 | `.bx-chip--active` | background | acid via `#ceff00` | mixed | set text to #000 or var(--gray-cool-6) |
| pulse.html:227 | `.signal-tab.active` .active | background | acid via `#ceff00` | mixed | set text to #000 or var(--gray-cool-6) |
| search.html:495 | `.field-dim-btn.active` .active | background | acid via `#ceff00` | light | set text to #000 or var(--gray-cool-6) |

## Olive on a DARK surface (1)

v13: olive is 4.0:1 on black; use acid (active/CTA) or lime (hover/focus) there.

| file:line | element | property | color | surface | proposed fix |
|---|---|---|---|---|---|
| pulse.html:565 | `.pulse-dot-inline` | background | olive via `#5d7400` | dark | acid #ceff00 (active/CTA) or lime #97d600 (hover/focus); olive is 4.0:1 on black |

## DOM-only violations (rendered; no static match) (2)

| page | element | property | color | surface | note |
|---|---|---|---|---|---|
| atlas-portal/index.html | `a` | border-bottom | acid | light | V1/V2 (DOM-only); "journalismatlas.com" |
| mobile.html | `path.sunburst-path` | svg-fill | lime | light | V1/V2 (DOM-only); "" |

## JS-set colors (review) (27)

Colors assigned in script (chart fills, canvas, inline-style builders). Rendered results that matched are already counted above through the DOM scan.

| file:line | element | property | color | surface | proposed fix |
|---|---|---|---|---|---|
| assets/js/main.js:1046 | `(JS/other)` | js | lime via `#97d600` | n/a | .range(['#97d600', '#ceff00', '#e8ff6b']); |
| assets/js/main.js:1046 | `(JS/other)` | js | acid via `#ceff00` | n/a | .range(['#97d600', '#ceff00', '#e8ff6b']); |
| assets/js/main.js:1367 | `(JS/other)` | js | lime via `#97d600` | n/a | return '#97d600'; // Default acid green |
| assets/js/main.js:2982 | `(JS/other)` | strokestyle | acid via `#ceff00` | n/a | ctx.strokeStyle = '#ceff00'; |
| assets/js/main.js:2987 | `(JS/other)` | fillstyle | acid via `#ceff00` | n/a | ctx.fillStyle = '#ceff00'; |
| assets/js/main.js:3005 | `(JS/other)` | strokestyle | acid via `#ceff00` | n/a | ctx.strokeStyle = '#ceff00'; |
| assets/js/main.js:3028 | `(JS/other)` | fillstyle | acid via `rgba(206,255,0,0.65)` | n/a | ctx.fillStyle = 'rgba(206,255,0,0.65)'; |
| assets/js/main.js:3054 | `(JS/other)` | strokestyle | acid via `#ceff00` | n/a | ctx.strokeStyle = '#ceff00'; |
| assets/js/main.js:3084 | `(JS/other)` | js | acid via `#ceff00` | n/a | ctx.fillStyle = Math.random() > 0.5 ? '#ffffff' : '#ceff00'; |
| atlas-portal/script.js:118 | `(JS/other)` | js | acid via `#ceff00` | n/a | const lightBackgrounds = ['#ceff00', '#97d600']; |
| atlas-portal/script.js:118 | `(JS/other)` | js | lime via `#97d600` | n/a | const lightBackgrounds = ['#ceff00', '#97d600']; |
| atlas_pulse_intelligence.html:398 | `(JS/other)` | js | acid via `#ceff00` | n/a | '#ceff00','#ffbb00','#6699ff','#ff9944','#aa88ff', |
| atlas_wire_intelligence.html:420 | `(JS/other)` | js | acid via `#ceff00` | n/a | const BEAT_COLORS = ['#ceff00','#ffbb00','#6699ff','#ff9944','#aa88ff' |
| atlas_wire_intelligence.html:571 | `(JS/other)` | js | acid via `var(--acid)` | n/a | const col = n>=8?'var(--acid)':n>=7?'var(--amber)':'var(--muted)'; |
| atlas_wire_intelligence.html:898 | `(JS/other)` | js | acid via `var(--acid)` | n/a | const scoreColor = score>=8?'var(--acid)':score>=7?'var(--amber)':'var |
| chicago-analysis.html:459 | `(JS/other)` | neon | acid via `#CEFF00` | n/a | const neon = '#CEFF00'; |
| chicago-analysis.html:460 | `(JS/other)` | js | acid via `#CEFF00` | n/a | const colors = ['#CEFF00', '#66ff88', '#66bbff', '#ffaa44', '#bb88ff', |
| for-brands.html:1316 | `(JS/other)` | style | acid via `#ceff00` | n/a | '<p style="color:#ceff00;font-size:15px;margin:16px 0 0;">Got it — we\ |
| index.html:2180 | `(JS/other)` | js | acid via `#ceff00` | n/a | const color = clusters[node.cluster]?.color // '#ceff00'; |
| mobile.html:1119 | `(JS/other)` | js | lime via `#97d600` | n/a | return '#97d600'; /* D3 sunburst only — confirmed not in UI chrome */ |
| pulse.html:2366 | `(JS/other)` | style | acid via `#ceff00` | n/a | Custom intelligence briefs powered by Journalism Atlas data. <span sty |
| search.html:933 | `(JS/other)` | js | acid via `#ceff00` | n/a | "Power & Politics":              "#ceff00",   // acid green — wrong on |
| search.html:937 | `(JS/other)` | js | lime via `#97d600` | n/a | "Civic Life":                    "#97d600",   // lime — correct token  |
| search.html:943 | `(JS/other)` | js | acid via `#ceff00` | n/a | "Newsletter - Substack": "#ceff00", |
| search.html:949 | `(JS/other)` | js | lime via `#97d600` | n/a | "Website":               "#97d600", |
| search.html:964 | `(JS/other)` | js | acid via `#ceff00` | n/a | "National":        "#ceff00", |
| search.html:967 | `(JS/other)` | js | lime via `#97d600` | n/a | "Midwest":         "#97d600", |

## Undetermined — surface not observed (96)

Static hits whose selector matched no element on any scanned page at load (dead CSS, JS-rendered or state-only elements such as a selected card or copied button) and whose role is text, icon or stroke. If any sit on a light surface they are violations.

| file:line | element | property | color | surface | proposed fix |
|---|---|---|---|---|---|
| advisory.html:161 | `.board-section li:before` | color | acid | unobserved | review: if on a light surface, apply V1/V2 fix |
| assets/css/main.css:240 | `.hero-link:hover` | color | acid | unobserved | review: if on a light surface, apply V1/V2 fix |
| assets/css/main.css:241 | `.hero-link:hover` | border-bottom-color | acid | unobserved | review: if on a light surface, apply V1/V2 fix |
| assets/css/main.css:727 | `.creators-table th.sort-asc .sort-icon::after` | color | acid | unobserved | review: if on a light surface, apply V1/V2 fix |
| assets/css/main.css:732 | `.creators-table th.sort-desc .sort-icon::after` | color | acid | unobserved | review: if on a light surface, apply V1/V2 fix |
| assets/css/main.css:1052 | `.sunburst-creator-card:hover` | border-color | lime | unobserved | review: if on a light surface, apply V1/V2 fix |
| assets/css/main.css:1146 | `.viz-creators-table a:hover` | color | lime | unobserved | review: if on a light surface, apply V1/V2 fix |
| assets/css/main.css:1881 | `.share-view-btn.copied` | color | acid | unobserved | review: if on a light surface, apply V1/V2 fix |
| assets/css/main.css:2089 | `.atlas-drawer-card.selectable.selected` | border | lime | unobserved | review: if on a light surface, apply V1/V2 fix |
| assets/css/main.css:2095 | `.atlas-drawer-card.selectable.selected::after` | color | acid | unobserved | review: if on a light surface, apply V1/V2 fix |
| atlas-signal-brief.html:47 | `.stat-accent` | color | acid | unobserved | review: if on a light surface, apply V1/V2 fix |
| atlas_pulse_intelligence.html:49 | `.stat-pill.wire-pill b` | color | acid | unobserved | review: if on a light surface, apply V1/V2 fix |
| atlas_pulse_intelligence.html:58 | `.btn-load.loaded` | border-color | acid | unobserved | review: if on a light surface, apply V1/V2 fix |
| atlas_pulse_intelligence.html:58 | `.btn-load.loaded` | color | acid | unobserved | review: if on a light surface, apply V1/V2 fix |
| atlas_pulse_intelligence.html:85 | `.signal-box` | border-left | acid | unobserved | review: if on a light surface, apply V1/V2 fix |
| atlas_pulse_intelligence.html:87 | `.signal-box em` | color | acid | unobserved | review: if on a light surface, apply V1/V2 fix |
| atlas_pulse_intelligence.html:92 | `.beat-row.active` | outline | acid | unobserved | review: if on a light surface, apply V1/V2 fix |
| atlas_pulse_intelligence.html:103 | `.theme-name` | color | acid | unobserved | review: if on a light surface, apply V1/V2 fix |
| atlas_pulse_intelligence.html:159 | `table.ptbl thead th.sort-on` | color | acid | unobserved | review: if on a light surface, apply V1/V2 fix |
| atlas_pulse_intelligence.html:163 | `table.ptbl tbody tr.sel` | border-left | acid | unobserved | review: if on a light surface, apply V1/V2 fix |
| atlas_pulse_intelligence.html:217 | `.det-link` | color | acid | unobserved | review: if on a light surface, apply V1/V2 fix |
| atlas_pulse_intelligence.html:228 | `.wire-box` | border | acid | unobserved | review: if on a light surface, apply V1/V2 fix |
| atlas_pulse_intelligence.html:230 | `.wire-score-lg` | color | acid | unobserved | review: if on a light surface, apply V1/V2 fix |
| atlas_pulse_intelligence.html:237 | `.wire-copy` | border-left | acid | unobserved | review: if on a light surface, apply V1/V2 fix |
| atlas_wire_intelligence.html:86 | `.signal-box em` | color | acid | unobserved | review: if on a light surface, apply V1/V2 fix |
| atlas_wire_intelligence.html:91 | `.beat-row.active` | outline | acid | unobserved | review: if on a light surface, apply V1/V2 fix |
| atlas_wire_intelligence.html:128 | `.beat-chip` | border | acid | unobserved | review: if on a light surface, apply V1/V2 fix |
| atlas_wire_intelligence.html:129 | `.beat-chip` | color | acid | unobserved | review: if on a light surface, apply V1/V2 fix |
| atlas_wire_intelligence.html:141 | `.q-card.selected` | border-color | acid | unobserved | review: if on a light surface, apply V1/V2 fix |
| atlas_wire_intelligence.html:141 | `.q-card.selected` | box-shadow | acid | unobserved | review: if on a light surface, apply V1/V2 fix |
| atlas_wire_intelligence.html:142 | `.q-card.approved` | border-left | acid | unobserved | review: if on a light surface, apply V1/V2 fix |
| atlas_wire_intelligence.html:143 | `.q-card.approved .score-badge.high` | box-shadow | acid | unobserved | review: if on a light surface, apply V1/V2 fix |
| atlas_wire_intelligence.html:150 | `.score-badge.high` | box-shadow | acid | unobserved | review: if on a light surface, apply V1/V2 fix |
| atlas_wire_intelligence.html:159 | `.creator-link:hover` | color | acid | unobserved | review: if on a light surface, apply V1/V2 fix |
| atlas_wire_intelligence.html:165 | `.q-wire[contenteditable=true]` | border-color | acid | unobserved | review: if on a light surface, apply V1/V2 fix |
| atlas_wire_intelligence.html:182 | `.btn-approve.is-approved` | border | acid | unobserved | review: if on a light surface, apply V1/V2 fix |
| atlas_wire_intelligence.html:182 | `.btn-approve.is-approved` | color | acid | unobserved | review: if on a light surface, apply V1/V2 fix |
| atlas_wire_intelligence.html:241 | `.wire-edit:focus` | outline | acid | unobserved | review: if on a light surface, apply V1/V2 fix |
| atlas_wire_intelligence.html:241 | `.wire-edit:focus` | border-color | acid | unobserved | review: if on a light surface, apply V1/V2 fix |
| atlas_wire_intelligence.html:278 | `.btn-approve-detail.is-approved` | border | acid | unobserved | review: if on a light surface, apply V1/V2 fix |
| atlas_wire_intelligence.html:278 | `.btn-approve-detail.is-approved` | color | acid | unobserved | review: if on a light surface, apply V1/V2 fix |
| atlas_wire_intelligence.html:582 | `(JS/other)` | color | acid | unobserved | review: if on a light surface, apply V1/V2 fix |
| atlas_wire_review.html:63 | `.header-meta .count-green` | color | acid | unobserved | review: if on a light surface, apply V1/V2 fix |
| atlas_wire_review.html:144 | `.card.approved` | border-left | acid | unobserved | review: if on a light surface, apply V1/V2 fix |
| atlas_wire_review.html:146 | `.card.editing` | border | acid | unobserved | review: if on a light surface, apply V1/V2 fix |
| atlas_wire_review.html:161 | `.score-badge.mid` | color | acid | unobserved | review: if on a light surface, apply V1/V2 fix |
| atlas_wire_review.html:170 | `.card-creator a:hover` | color | acid | unobserved | review: if on a light surface, apply V1/V2 fix |
| atlas_wire_review.html:197 | `.wire-frame-edit` | border | acid | unobserved | review: if on a light surface, apply V1/V2 fix |
| bluesky-creator-intelligence.html:160 | `.search-input.arrival` | border-color | lime | unobserved | review: if on a light surface, apply V1/V2 fix |
| bluesky-creator-intelligence.html:161 | `.search-input.arrival` | box-shadow | lime | unobserved | review: if on a light surface, apply V1/V2 fix |
| bluesky-creator-intelligence.html:211 | `0%` | box-shadow | lime | unobserved | review: if on a light surface, apply V1/V2 fix |
| bluesky-creator-intelligence.html:212 | `30%` | box-shadow | lime | unobserved | review: if on a light surface, apply V1/V2 fix |
| bluesky-creator-intelligence.html:213 | `100%` | box-shadow | lime | unobserved | review: if on a light surface, apply V1/V2 fix |
| chicago-analysis.html:350 | `<strong.stats-grid> (inline)` | style | acid | unobserved | review: if on a light surface, apply V1/V2 fix |
| chicago-survey.html:567 | `.redeem-steps .step-num` | color | acid | unobserved | review: if on a light surface, apply V1/V2 fix |
| chicago-survey.html:840 | `<span.error-msg> (inline)` | style | acid | unobserved | review: if on a light surface, apply V1/V2 fix |
| city-lab-chicago.html:129 | `.beats-toggle-btn:hover` | border-color | lime | unobserved | review: if on a light surface, apply V1/V2 fix |
| city-lab-dc-v3.html:923 | `<em.timeline> (inline)` | color | acid | unobserved | review: if on a light surface, apply V1/V2 fix |
| city-lab-dc-v3.html:923 | `<em.timeline> (inline)` | color | acid | unobserved | review: if on a light surface, apply V1/V2 fix |
| for-brands.html:366 | `.atlas-card-link` | color | acid | unobserved | review: if on a light surface, apply V1/V2 fix |
| for-brands.html:367 | `.atlas-card-link:hover` | color | acid | unobserved | review: if on a light surface, apply V1/V2 fix |
| for-brands.html:759 | `<a.pulse-intel-footer> (inline)` | style | acid | unobserved | review: if on a light surface, apply V1/V2 fix |
| for-brands.html:995 | `<a.bf-secondary-path> (inline)` | style | acid | unobserved | review: if on a light surface, apply V1/V2 fix |
| how-we-did-this.html:143 | `.highlight-box` | border-left | acid | unobserved | review: if on a light surface, apply V1/V2 fix |
| index.html:1533 | `(JS/other)` | color | acid | unobserved | review: if on a light surface, apply V1/V2 fix |
| index.html:1535 | `(JS/other)` | color | lime | unobserved | review: if on a light surface, apply V1/V2 fix |
| index.html:1739 | `(JS/other)` | color | acid | unobserved | review: if on a light surface, apply V1/V2 fix |
| index.html:2097 | `(JS/other)` | color | acid | unobserved | review: if on a light surface, apply V1/V2 fix |
| mobile.html:620 | `.sunburst-path.glow` | filter | acid | unobserved | review: if on a light surface, apply V1/V2 fix |
| partners/_shell.html:165 | `.region-nav-link.active` | border-bottom-color | lime | unobserved | review: if on a light surface, apply V1/V2 fix |
| partners/ahp.html:51 | `.pull-quote-mark` | color | acid | unobserved | review: if on a light surface, apply V1/V2 fix |
| partners/cillizza.html:51 | `.pull-quote-mark` | color | acid | unobserved | review: if on a light surface, apply V1/V2 fix |
| partners/emily-atkin.html:50 | `.pull-quote-mark` | color | acid | unobserved | review: if on a light surface, apply V1/V2 fix |
| partners/emily-atkin.html:98 | `.chip:focus-visible` | outline | lime | unobserved | review: if on a light surface, apply V1/V2 fix |
| partners/icfj.html:47 | `.pull-quote-mark` | color | acid | unobserved | review: if on a light surface, apply V1/V2 fix |
| partners/jessica-stahl.html:38 | `.pull-quote-mark` | color | acid | unobserved | review: if on a light surface, apply V1/V2 fix |
| pulse.html:51 | `.live-badge` | color | acid | unobserved | review: if on a light surface, apply V1/V2 fix |
| pulse.html:53 | `.live-badge` | border | acid | unobserved | review: if on a light surface, apply V1/V2 fix |
| pulse.html:123 | `.signal-band-eyebrow` | color | acid | unobserved | review: if on a light surface, apply V1/V2 fix |
| pulse.html:136 | `.field-summary-eyebrow` | color | lime | unobserved | review: if on a light surface, apply V1/V2 fix |
| pulse.html:173 | `.story-stack-creator` | color | acid | unobserved | review: if on a light surface, apply V1/V2 fix |
| pulse.html:177 | `.story-stack-title:hover` | text-decoration-color | acid | unobserved | review: if on a light surface, apply V1/V2 fix |
| pulse.html:182 | `.story-cluster` | border-left | acid | unobserved | review: if on a light surface, apply V1/V2 fix |
| pulse.html:184 | `.story-cluster-voice-count` | color | acid | unobserved | review: if on a light surface, apply V1/V2 fix |
| pulse.html:1025 | `.header-intel-cta` | color | acid | unobserved | review: if on a light surface, apply V1/V2 fix |
| search.html:71 | `.search-orientation-link` | color | acid | unobserved | review: if on a light surface, apply V1/V2 fix |
| search.html:108 | `.sbc-chip--active` | border-color | acid | unobserved | review: if on a light surface, apply V1/V2 fix |
| search.html:160 | `.sfc-chip--active` | border-color | acid | unobserved | review: if on a light surface, apply V1/V2 fix |
| search.html:273 | `.pulse-strip` | border-bottom | acid | unobserved | review: if on a light surface, apply V1/V2 fix |
| search.html:297 | `.pulse-strip-live` | color | acid | unobserved | review: if on a light surface, apply V1/V2 fix |
| search.html:334 | `.pulse-strip-cta` | color | acid | unobserved | review: if on a light surface, apply V1/V2 fix |
| search.html:342 | `.pulse-strip-cta:hover` | color | acid | unobserved | review: if on a light surface, apply V1/V2 fix |
| search.html:468 | `.field-tooltip-beat` | color | acid | unobserved | review: if on a light surface, apply V1/V2 fix |
| who-we-are.html:135 | `.mission-content li:before` | color | acid | unobserved | review: if on a light surface, apply V1/V2 fix |
| who-we-are.html:144 | `.highlight-box` | border-left | acid | unobserved | review: if on a light surface, apply V1/V2 fix |
| wire.html:168 | `.card-creator a:hover` | color | lime | unobserved | review: if on a light surface, apply V1/V2 fix |

## Variable definitions that hold a green

| file:line | variable | holds | note |
|---|---|---|---|
| about-this-project.html:36 | `--acid-green` | acid | --acid-green: #ceff00; |
| about-this-project.html:37 | `--lime-green` | lime | --lime-green: #97d600; |
| advisory.html:37 | `--acid-green` | acid | --acid-green: #ceff00; |
| advisory.html:38 | `--lime-green` | lime | --lime-green: #97d600; |
| assets/css/variables.css:21 | `--color-acid-green` | acid | --color-acid-green:  #ceff00;   /* Dark backgrounds only — see semanti |
| assets/css/variables.css:22 | `--color-lime-green` | lime | --color-lime-green:  #97d600;   /* Light backgrounds only — see semant |
| assets/css/variables.css:23 | `--color-dark-olive` | olive | --color-dark-olive:  #5d7400;   /* Hover / deep accent */ |
| assets/css/variables.css:35 | `--acid-green` | acid | --acid-green:  #ceff00;   /* NOTE: acid green = dark surfaces only per |
| assets/css/variables.css:36 | `--lime-green` | lime | --lime-green:  #97d600; |
| assets/css/variables.css:71 | `--color-hover` | lime | --color-hover:          #97d600;              /* Lime — hover. FILL ON |
| assets/css/variables.css:72 | `--color-accent-on-light` | olive | --color-accent-on-light: #5d7400;             /* Dark Olive — text, ic |
| assets/css/variables.css:73 | `--color-focus` | lime | --color-focus:          #97d600;              /* focus ring on dark su |
| assets/css/variables.css:74 | `--color-focus-on-light` | olive | --color-focus-on-light: #5d7400;              /* focus ring on light s |
| assets/css/variables.css:87 | `--color-accent` | lime | --color-accent:         #97d600;   /* Primary accent / CTA — lime, lig |
| assets/css/variables.css:88 | `--color-accent-hover` | olive | --color-accent-hover:   #5d7400;   /* Hover / active state — dark oliv |
| assets/css/variables.css:104 | `--color-accent-dark` | acid | --color-accent-dark:        #ceff00;   /* Primary accent / CTA — acid  |
| assets/css/variables.css:105 | `--color-accent-dark-hover` | lime | --color-accent-dark-hover:  #97d600;   /* Hover on dark — lime */ |
| assets/css/variables.css:121 | `--canvas-accent` | acid | --canvas-accent:         #ceff00; |
| assets/css/variables.css:268 | `--focus-ring-light` | lime | --focus-ring-light:  2px solid #97d600; |
| assets/css/variables.css:269 | `--focus-ring-dark` | acid | --focus-ring-dark:   2px solid #ceff00; |
| atlas-portal/index.html:30 | `--acid-green` | acid | --acid-green: #ceff00; |
| atlas-portal/index.html:31 | `--lime-green` | lime | --lime-green: #97d600; |
| atlas_pulse_intelligence.html:28 | `--acid` | acid | --acid:#ceff00;--amber:#ffbb00;--red:#ff4422;--blue:#6699ff; |
| atlas_wire_intelligence.html:16 | `--acid` | acid | --acid:#ceff00;--amber:#ffbb00;--red:#ff4422;--blue:#6699ff; |
| atlas_wire_review.html:21 | `--acid` | acid | --acid: #ceff00; |
| bluesky-creator-intelligence.html:30 | `--acid` | acid | --acid: #ceff00; |
| bluesky-creator-intelligence.html:31 | `--lime` | lime | --lime: #97d600; |
| bluesky-creator-intelligence.html:32 | `--olive` | olive | --olive: #5d7400; |
| chicago-analysis.html:11 | `--neon` | acid | --neon: #CEFF00; |
| chicago-survey.html:14 | `--lime` | acid | --lime: #ceff00; |
| chicago-survey.html:15 | `--green` | lime | --green: #97d600; |
| city-lab-chicago.html:25 | `--tab-active-bg` | lime | --tab-active-bg:     #97d600; |
| city-lab-dc-v3.html:27 | `--acid` | acid | --acid: #ceff00; |
| city-lab-dc-v3.html:30 | `--lime` | lime | --lime: #97d600; |
| how-we-did-this.html:37 | `--acid-green` | acid | --acid-green: #ceff00; |
| how-we-did-this.html:38 | `--lime-green` | lime | --lime-green: #97d600; |
| index.html:256 | `--linked` | olive | .pulse-col-header--linked:hover .pulse-beat-count { color: #5d7400; } |
| lists.html:26 | `--acid-green` | acid | --acid-green: #ceff00; |
| mobile.html:39 | `--acid-green` | acid | --acid-green: #ceff00; |
| partners/_reviewjames.html:10 | `--acid` | acid | :root{--acid:#ceff00;--lime:#97d600;--olive:#5d7400;--page-bg:#efeff4; |
| partners/_reviewjames.html:10 | `--lime` | lime | :root{--acid:#ceff00;--lime:#97d600;--olive:#5d7400;--page-bg:#efeff4; |
| partners/_reviewjames.html:10 | `--olive` | olive | :root{--acid:#ceff00;--lime:#97d600;--olive:#5d7400;--page-bg:#efeff4; |
| partners/_shell.html:38 | `--acid` | acid | --acid:    #ceff00;   /* dark surfaces only */ |
| partners/_shell.html:39 | `--lime` | lime | --lime:    #97d600;   /* light surfaces only */ |
| partners/_shell.html:40 | `--olive` | olive | --olive:   #5d7400; |
| partners/ahp.html:18 | `--acid` | acid | --acid:       #ceff00; |
| partners/ahp.html:19 | `--lime` | lime | --lime:       #97d600; |
| partners/ahp.html:20 | `--olive` | olive | --olive:      #5d7400; |
| partners/cillizza.html:18 | `--acid` | acid | --acid:       #ceff00; |
| partners/cillizza.html:19 | `--lime` | lime | --lime:       #97d600; |
| partners/cillizza.html:20 | `--olive` | olive | --olive:      #5d7400; |
| partners/emily-atkin.html:18 | `--acid` | acid | --acid:       #ceff00; |
| partners/emily-atkin.html:19 | `--lime` | lime | --lime:       #97d600; |
| partners/emily-atkin.html:20 | `--olive` | olive | --olive:      #5d7400; |
| partners/icfj.html:18 | `--acid` | acid | --acid:       #ceff00; |
| partners/icfj.html:19 | `--lime` | lime | --lime:       #97d600; |
| partners/icfj.html:20 | `--olive` | olive | --olive:      #5d7400; |
| partners/iij.html:18 | `--acid` | acid | --acid:       #ceff00; |
| partners/iij.html:19 | `--lime` | lime | --lime:       #97d600; |
| partners/iij.html:20 | `--olive` | olive | --olive:      #5d7400; |
| partners/jessica-stahl.html:18 | `--acid` | acid | --acid:       #ceff00; |
| partners/jessica-stahl.html:19 | `--lime` | lime | --lime:       #97d600; |
| partners/jessica-stahl.html:20 | `--olive` | olive | --olive:      #5d7400; |
| partners/joon-lee.html:16 | `--acid` | acid | :root { --acid:#ceff00; --lime:#97d600; --olive:#5d7400; --page-bg:#ef |
| partners/joon-lee.html:16 | `--lime` | lime | :root { --acid:#ceff00; --lime:#97d600; --olive:#5d7400; --page-bg:#ef |
| partners/joon-lee.html:16 | `--olive` | olive | :root { --acid:#ceff00; --lime:#97d600; --olive:#5d7400; --page-bg:#ef |
| partners/karen-attiah.html:16 | `--acid` | acid | :root{--acid:#ceff00;--lime:#97d600;--olive:#5d7400;--page-bg:#efeff4; |
| partners/karen-attiah.html:16 | `--lime` | lime | :root{--acid:#ceff00;--lime:#97d600;--olive:#5d7400;--page-bg:#efeff4; |
| partners/karen-attiah.html:16 | `--olive` | olive | :root{--acid:#ceff00;--lime:#97d600;--olive:#5d7400;--page-bg:#efeff4; |
| partners/knowledge-creators.html:16 | `--acid` | acid | :root{--acid:#ceff00;--lime:#97d600;--olive:#5d7400;--page-bg:#efeff4; |
| partners/knowledge-creators.html:16 | `--lime` | lime | :root{--acid:#ceff00;--lime:#97d600;--olive:#5d7400;--page-bg:#efeff4; |
| partners/knowledge-creators.html:16 | `--olive` | olive | :root{--acid:#ceff00;--lime:#97d600;--olive:#5d7400;--page-bg:#efeff4; |
| partners/natgeo.html:16 | `--acid` | acid | :root{--acid:#ceff00;--lime:#97d600;--olive:#5d7400;--page-bg:#efeff4; |
| partners/natgeo.html:16 | `--lime` | lime | :root{--acid:#ceff00;--lime:#97d600;--olive:#5d7400;--page-bg:#efeff4; |
| partners/natgeo.html:16 | `--olive` | olive | :root{--acid:#ceff00;--lime:#97d600;--olive:#5d7400;--page-bg:#efeff4; |
| partners/news-creator-corps.html:18 | `--acid` | acid | --acid:       #ceff00; |
| partners/news-creator-corps.html:19 | `--lime` | lime | --lime:       #97d600; |
| partners/news-creator-corps.html:20 | `--olive` | olive | --olive:      #5d7400; |
| partners/noah-smith.html:18 | `--acid` | acid | --acid:       #ceff00; |
| partners/noah-smith.html:19 | `--lime` | lime | --lime:       #97d600; |
| partners/noah-smith.html:20 | `--olive` | olive | --olive:      #5d7400; |
| partners/rahim-jessani.html:18 | `--acid` | acid | --acid:       #ceff00; |
| partners/rahim-jessani.html:19 | `--lime` | lime | --lime:       #97d600; |
| partners/rahim-jessani.html:20 | `--olive` | olive | --olive:      #5d7400; |
| who-we-are.html:39 | `--acid-green` | acid | --acid-green: #ceff00; |
| who-we-are.html:40 | `--lime-green` | lime | --lime-green: #97d600; |

## Compliant (counts only)
506 acid/lime uses are compliant (dark surface, or a fill with black/step-6 text). They are in the TSV.
