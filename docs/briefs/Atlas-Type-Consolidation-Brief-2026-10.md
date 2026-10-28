# Atlas Type Consolidation Brief — One Set of Fonts and Sizes Site-Wide

*Developer brief for Claude Code · Owner: James Bareham, Creative Director · For: Justin Bank · October 27, 2026*
*Implements DESIGN-TOKENS-v16.md § Typography (Font Allowlist, Typeface by Role, Monospace by Role, Type Floor, Font Tokens) and § Site Footer. Introduces no new values.*

**Prerequisite:** `Atlas-Foundation-Lock-Brief-2026-10.md` is merged (v16 installed, font and size variables in `variables.css`, brand check in the build).

---

## 1. Summary

journalismatlas.com currently uses five type systems: Inter, Source Code Pro, Merriweather, and the retired DM Mono and JetBrains Mono, at sizes from 8px up. The shared header loads JetBrains Mono on every page for one 8px badge, the footer runs at 9–10px, and five pages add a second footer strip at 9px. About 250 declarations on public pages set text below 12px.

This brief brings every public page onto one system: Inter for text and headings, Source Code Pro for all-caps labels and tags, Merriweather only in editorial articles, and nothing below 12px. It fixes most of the site's small-text accessibility problems in the same pass, because almost all of them are the old mono labels and the footer.

### In scope
- Shared header and footer (`assets/css/header.css`, `assets/js/header.js`)
- The 98 DM Mono / JetBrains Mono declarations on `index.html`, `bluesky-creator-intelligence.html`, `search.html`, `about-this-project.html`, `contact.html`, `partners/index.html` and `teamdmv/index.html`
- Five pages with a duplicate "Powered by" footer strip
- Merriweather outside articles: `city-lab-dc-v3.html` (page body), `search.html`, `atlas-portal/index.html` (font loads), `teamdmv` (Playfair headings)
- Every remaining declaration below 12px on public pages, including `main.css`, `main.js`, partner pages and the partner shell
- Inter 500, and weights 800/900
- `mobile.html`: legacy Material Icons

### Out of scope
- **Pulse and For Brands:** their own brief (`Atlas-Pulse-For-Brands-Brief-2026-10.md`)
- **Nodes and Networks:** excluded by v16
- **Off-system colors:** the next update (the baseline records them)
- **Sizes between scale steps** (14px, 15px outside buttons): above the floor; the next update
- Internal pages (`atlas-signal-brief`, `atlas_*_intelligence`, `atlas_wire_review`, `beat-*`, `chicago-*`): do last, after public pages, in the same way

---

## 2. Recipes

Use these four recipes for every change below. All values come from v16; use the variables, not literal values.

```css
/* Label: all-caps eyebrows, section labels, instruction links, filter/sort labels, graphic headings.
   DESIGN-TOKENS-v16.md § Monospace by Role */
font-family: var(--font-mono); font-weight: 500; font-size: var(--text-label); line-height: 1.4;
text-transform: uppercase; letter-spacing: 0.12em;   /* 0.08em for instruction links and dense labels */

/* Tag: all-caps tags, badges, pills, status, card meta lines, graphic legends */
font-family: var(--font-mono); font-weight: 500; font-size: var(--text-tag); line-height: 1.2;   /* 1.4 for card meta lines */
text-transform: uppercase; letter-spacing: 0.08em;

/* Small: sentence-case text that used a mono font: handles, channels, places, notes, tooltips, timestamps */
font-family: var(--font-primary); font-weight: 400; font-size: var(--text-small); line-height: 1.5;
letter-spacing: normal; text-transform: none;
font-variant-numeric: tabular-nums;   /* only where numbers align in columns */

/* Numeral: bold stats and counts shown large */
font-family: var(--font-heading); font-weight: 700; font-size: var(--text-h2);   /* or --text-h3 / --text-h1 / --text-display */
line-height: 1.1; letter-spacing: normal; font-variant-numeric: tabular-nums;
```

**Tags keep the v15 tag rules** (fill or outline, never both; 6px radius; padding `4px 8px`, or `3px 7px` when outlined; no hover). Beat tags carry color only on an 8px dot. If a "tag" is clickable today, it's a control: make it a secondary button or remove the click. List each one you find for James rather than deciding.

**Text inside graphics** (legends, axis labels, tooltips, canvas and SVG text) follows the same recipes and the 12px floor. In D3 and canvas code, set `font` strings from the recipes (e.g. `ctx.font = '500 12px "Source Code Pro", monospace'`) because CSS variables don't reach canvas; that is the only place a family name may be written outside `variables.css`. Add the file to the brand-check notes if it needs a baseline entry.

**If text no longer fits at the new size,** change the layout: let it wrap, stack the columns, abbreviate the label, or move it behind a disclosure. Never go below the floor, and never tighten letter-spacing outside the recipe range.

---

## 3. Phase A: Shared Header and Footer (every page)

### A1. `assets/css/header.css`

| Line | Selector | Now | v16 |
|---|---|---|---|
| 1 | `@import url(...JetBrains+Mono...)` | Loads JetBrains Mono on every page | **Delete** |
| 225–231 | `.nav-soon-badge` | JetBrains Mono 500, 8px, 0.12em | **Tag** recipe; status tag style on the header's surface |
| 368 | `.footer-tagline` | Source Code Pro, 10px, 0.08em | **Small** recipe, `--color-text-on-dark-2`; text stays "The human infrastructure of trust, mapped." |
| 369 | `.footer-col-title` | Source Code Pro, 9px, 0.14em | **Label** recipe (0.12em), `--color-text-on-dark-2` |
| 376 | `.footer-copy` | Source Code Pro, 9px, 0.06em | **Tag** recipe, `--color-text-on-dark-2` |
| 378 | `.footer-legal a` | Source Code Pro, 9px, 0.06em | **Tag** recipe, `--color-link-on-dark`; hover unchanged (Acid, underlined) |
| 381 (approx.) | `.footer-col ul li a` | 13px, family inherited | Add `font-family: var(--font-primary)` explicitly |

```css
/* Footer type. DESIGN-TOKENS-v16.md § Site Footer */
.footer-tagline   { font-family: var(--font-primary); font-weight: 400; font-size: var(--text-small); line-height: 1.5; color: var(--color-text-on-dark-2); }
.footer-col-title { font-family: var(--font-mono); font-weight: 500; font-size: var(--text-label); line-height: 1.4; text-transform: uppercase; letter-spacing: 0.12em; color: var(--color-text-on-dark-2); margin-bottom: var(--space-md); }
.footer-col ul li a { font-family: var(--font-primary); font-size: var(--text-small); /* color and states unchanged */ }
.footer-copy      { font-family: var(--font-mono); font-weight: 500; font-size: var(--text-tag); line-height: 1.2; text-transform: uppercase; letter-spacing: 0.08em; color: var(--color-text-on-dark-2); }
.footer-legal a   { font-family: var(--font-mono); font-weight: 500; font-size: var(--text-tag); line-height: 1.2; text-transform: uppercase; letter-spacing: 0.08em; color: var(--color-link-on-dark); /* underline and hover unchanged */ }

/* Partners nav badge. DESIGN-TOKENS-v16.md § Tags and Labels */
.nav-soon-badge   { font-family: var(--font-mono); font-weight: 500; font-size: var(--text-tag); line-height: 1.2; text-transform: uppercase; letter-spacing: 0.08em; /* keep its current colors and padding; padding 3px 7px if outlined */ }
```

**Layout checks:**
- **Nav:** the badge grows from 8px to 12px. Check the header at 1440, 1280, 1024 and 390px against the Header Nav Spacing table (v16). "Research & Writing" is the tightest fit; if the nav wraps, use the table's fallback (24px between links) before anything else.
- **Footer:** column titles grow from 9px to 13px and legal links from 9px to 12px. Check that the four-column grid (`13.2% 9.4% 9.4% 9.4%`) still holds titles on one line at 1280 and 1440; if not, let titles wrap rather than shrink. Check that `.footer-legal` links wrap cleanly at 390px and keep 44px touch targets (add vertical padding, not size).
- Follow `footer-redesign-spec.md` for grid, dividers and gutters; only type changes here.

### A2. `assets/js/header.js`
- Lines 62–63: update the comment: Source Code Pro 500 is now in use.
- **Leave the Inter URL as is until Phase E** (it still loads 500 for pages that use it).

### A3. `assets/js/footer.js`
- Line 9: update the comment that mentions JetBrains Mono. No code change.

---

## 4. Phase B: Pages Using DM Mono and JetBrains Mono

For each page: remove DM Mono and JetBrains Mono from its font links and `@import`s, then apply the target below to each selector. Targets map the selector's role to a recipe; where the brief says "Inter 700, 20px," use the Numeral recipe with `--text-h3`.

**Sizes and widths.** About 80 of these 98 declarations grow from 8–11px to 12–13px, roughly 35–45% wider. Check every one at 390, 768 and 1440px.

**Page notes:**
- **`index.html`:** the hero legend pills (`.hcn-pill`) and `.platform-legend` are graphic legends: Tag recipe, 12px floor. The hero stat numerals move from 22px mono to Inter 700 at 20px (H3 size) and from 28px to Inter 700 at 28px (H2 size). `.featured-beat` becomes a beat tag (dot, not fill). The Pulse grid on the homepage already went to one column at ≤480px for 13px labels; check it again.
- **`bluesky-creator-intelligence.html`:** 31 of 32 declarations are 9–10px, and the page already overflows at phone width (705px; Session 3 item 1). **Do this page together with its mobile layout fix,** not separately.
- **`search.html`:** remove `Merriweather` and `DM+Mono` and weight `800` from its Google Fonts link (line 36); `header.js` loads the site fonts.
- **`partners/index.html`:** has no site footer. Add `footer.js` like other pages.
- **`teamdmv/index.html`:** a standalone page (no `variables.css`, `header.js` or `footer.js`). Link `variables.css`; replace its Google Fonts link (Playfair Display, DM Mono, Inter 500) with nothing (or `header.js` if it adopts the shared header); its `--ff-serif` Playfair headings (8 selectors) become Inter at their scale level via `--font-heading`; its rem sizes map as in the table; its three weight-800/900 rules become 700. ⚑ Adopting the shared header and footer would make it consistent with the rest of the site; list it for Justin and James to confirm, since the page has a gate.

#### `index.html` (31)

| Line | Selector | Now | Case | v16 target |
|---|---|---|---|---|
| 74 | `.hero-eyebrow-pill` | 9px | caps | Label 13px caps |
| 90 | `.hcn-pill` | 8px | caps | Tag 12px caps (graphic legend) |
| 99 | `.viz-label` | 9px | caps | Label 13px caps (graphic heading) |
| 132 | `.platform-legend` | 8px | mixed | Tag 12px caps (graphic legend: 12px floor applies) |
| 140 | `.hero-stat-badge-num` | 22px | mixed | Inter 700, 20px, tabular figures (stat numeral at H3 size) |
| 141 | `.hero-stat-badge-lbl` | 13px | caps | Label 13px caps |
| 154 | `.stat-lbl` | 13px | caps | Label 13px caps |
| 172 | `.featured-eyebrow` | 9px | caps | Label 13px caps |
| 191 | `.featured-beat` | 13px | caps | Beat tag: Tag 12px caps + dot (v15 Tags) |
| 208 | `.credentials-text` | 12px | mixed | Inter Small 13px |
| 227 | `.pulse-live-badge` | 9px | caps | Tag 12px caps (status: confirmed) |
| 241 | `.pulse-beat-name` | 9px | caps | Tag 12px caps |
| 242 | `.pulse-beat-count` | 9px | caps | Tag 12px caps |
| 246 | `.pulse-item-creator` | 9px | caps | Inter Small 13px (creator name, per the Pulse card hierarchy) |
| 254 | `.pulse-item-meta` | 9px | mixed | Tag 12px caps (card meta line) |
| 263 | `.intel-thesis-coda` | 11px | caps | Label 13px caps |
| 274 | `.cluster-count-n` | 28px | mixed | Inter 700, 28px, tabular figures (stat numeral at H2 size) |
| 279 | `.fp-label` | 9px | mixed | Tag 12px caps (graphic label) |
| 295 | `.research-badge` | 9px | caps | Tag 12px caps |
| 299 | `.research-partner-chip` | 9px | caps | Tag 12px caps |
| 302 | `.research-card-status` | 9px | caps | Tag 12px caps |
| 313 | `.research-card-source-pill` | 9px | caps | Tag 12px caps |
| 318 | `.partner-label` | 9px | caps | Label 13px caps |
| 331 | `.db-header-note` | 9px | caps | Tag 12px caps |
| 341 | `.db-card-pub` | 13px | mixed | Tag 12px caps (card meta line) |
| 343 | `.db-pill` | 13px | caps | Tag 12px caps |
| 396 | `#cluster-drawer-count` | 11px | mixed | Inter Small 13px, tabular figures |
| 449 | `.drawer-creator-channel` | 11px | mixed | Inter Small 13px |
| 457 | `.drawer-creator-platform-badge` | 9px | caps | Tag 12px caps |
| 461 | `.drawer-creator-geo` | 9px | mixed | Inter Small 13px |
| 471 | `#cluster-drawer-showing` | 10px | mixed | Inter Small 13px |

#### `bluesky-creator-intelligence.html` (32)

| Line | Selector | Now | Case | v16 target |
|---|---|---|---|---|
| 51 | `.badge` | 10px | caps | Tag 12px caps |
| 54 | `.header-right` | 10px | mixed | Inter Small 13px |
| 61 | `.hero-eyebrow` | 10px | caps | Label 13px caps |
| 68 | `.viz-label` | 9px | caps | Label 13px caps (graphic heading) |
| 76 | `#viz-tooltip .tt-handle` | 10px | mixed | Inter Small 13px |
| 77 | `#viz-tooltip .tt-cluster` | 9px | caps | Tag 12px caps |
| 93 | `.stat-label` | 9px | caps | Label 13px caps |
| 94 | `.stat-sub` | 9px | mixed | Inter Small 13px, tabular figures |
| 95 | `.stat-so-what` | 9px | mixed | Inter Small 13px, tabular figures |
| 101 | `.section-num` | 11px | mixed | Label 13px caps |
| 103 | `.section-meta` | 10px | caps | Label 13px caps |
| 113 | `.cluster-count` | 11px | mixed | Inter Small 13px, tabular figures |
| 119 | `.fp-label` | 9px | mixed | Tag 12px caps (graphic label) |
| 124 | `.cc-handle` | 10px | mixed | Inter Small 13px |
| 128 | `.dist-label` | 10px | mixed | Inter Small 13px, tabular figures |
| 131 | `.dist-count` | 10px | mixed | Inter Small 13px, tabular figures |
| 139 | `.method-num` | 9px | caps | Label 13px caps |
| 143 | `.method-tag` | 9px | mixed | Tag 12px caps |
| 148 | `.gap-micro` | 9px | caps | Tag 12px caps |
| 150 | `.gap-sub` | 10px | mixed | Inter Small 13px |
| 151 | `.gap-thin` | 9px | mixed | Inter Small 13px |
| 175 | `.sort-label` | 10px | caps | Label 13px caps |
| 180 | `.filter-label` | 10px | caps | Label 13px caps |
| 184 | `.index-status` | 11px | mixed | Inter Small 13px |
| 198 | `.ci-channel` | 10px | mixed | Inter Small 13px |
| 199 | `.ci-beat` | 9px | caps | Tag 12px caps |
| 200 | `.ci-platform` | 9px | caps | Tag 12px caps |
| 202 | `.ci-bsky` | 10px | mixed | Inter Small 13px |
| 203 | `.ci-followers` | 11px | mixed | Inter Small 13px, tabular figures |
| 207 | `.ci-list-header span` | 9px | caps | Label 13px caps |
| 219 | `.no-results p` | 13px | mixed | Inter Body 16px |
| 220 | `.viz-expand-hint` | 9px | caps | Label 13px caps |

#### `search.html` (10)

| Line | Selector | Now | Case | v16 target |
|---|---|---|---|---|
| 160 | `.search-orientation-action` | 10px | caps | Label 13px caps |
| 206 | `.search-pulse-text` | 11px | mixed | Inter Small 13px |
| 244 | `.pulse-strip-live` | 9px | caps | Tag 12px caps |
| 268 | `.pulse-strip-week` | 9px | mixed | Inter Small 13px |
| 284 | `.pulse-strip-cta` | 10px | caps | Label 13px caps |
| 351 | `.advanced-viz-summary` | 10px | caps | Label 13px caps |
| 371 | `.field-view-note` | 10px | mixed | Inter Small 13px |
| 402 | `.field-tooltip-meta` | 10px | mixed | Inter Small 13px |
| 408 | `.field-tooltip-beat` | 9px | caps | Tag 12px caps |
| 420 | `.field-dim-label` | 10px | caps | Label 13px caps |

#### `about-this-project.html` (5)

| Line | Selector | Now | Case | v16 target |
|---|---|---|---|---|
| 77 | `.about-eyebrow` | 10px | caps | Label 13px caps |
| 133 | `.pillar-number` | 11px | mixed | Label 13px caps |
| 197 | `.team-title` | 12px | caps | Label 13px caps |
| 295 | `.criteria-num` | 14px | mixed | Label 13px caps |
| 377 | `.board-member-org` | 12px | mixed | Inter Small 13px |

#### `contact.html` (2)

| Line | Selector | Now | Case | v16 target |
|---|---|---|---|---|
| 49 | `.contact-eyebrow` | 10px | caps | Label 13px caps |
| 79 | `.contribute-eyebrow` | 10px | caps | Label 13px caps |

#### `partners/index.html` (1)

| Line | Selector | Now | Case | v16 target |
|---|---|---|---|---|
| 41 | `.partners-eyebrow` | 9px | caps | Label 13px caps |

#### `teamdmv/index.html` (11)

| Line | Selector | Now | Case | v16 target |
|---|---|---|---|---|
| 92 | `.hero-eyebrow` | 0.7rem | caps | Label 13px caps |
| 108 | `.section-eyebrow` | 0.68rem | caps | Label 13px caps |
| 128 | `.featured-role` | 0.62rem | caps | Tag 12px caps |
| 155 | `.card-handle` | 0.72rem | mixed | Inter Small 13px |
| 168 | `.commons-group-title` | 0.68rem | caps | Label 13px caps |
| 201 | `.commons-size` | 0.64rem | mixed | Inter Small 13px, tabular figures |
| 258 | `.commons-group-title` | 0.68rem | caps | Label 13px caps |
| 259 | `.commons-group-count` | 0.62rem | mixed | Inter Small 13px, tabular figures |
| 283 | `.sponsor-eyebrow` | 0.68rem | caps | Label 13px caps |
| 308 | `.modal-handle` | 0.8rem | mixed | Inter Small 13px |
| 353 | `#gate-input` | 1rem | mixed | Inter Body 16px 400 (form input) |

---

## 5. Phase C: One Footer and Serif Clean-Up

### C1. Remove the duplicate footer strips
Five pages end with a second footer strip after the standard footer: `<span style="font-family:'DM Mono',monospace;font-size:9px;...;color:rgba(255,255,255,0.22)">Powered by <a ...>Journalism Atlas</a> data</span>` (with inline `onmouseover` color changes).

| File | Line |
|---|---|
| `city-lab-chicago.html` | 557 |
| `city-lab-dc-v3.html` | 1385 |
| `latin-america-lab.html` | 836 |
| `partners/nj-lab.html` | 645 |
| `partners/njlab.html` | 646 |

**Delete the strip and its wrapper `div`** on all five. It duplicates the standard footer, uses the wrong name ("Journalism Atlas"), fails contrast at 22% white and sits at 9px. If a page needs to credit Atlas data, say so in the page body, e.g. a source line in Small text: "Data: The Independent Journalism Atlas."

### C2. Merriweather outside articles
| File | Now | v16 |
|---|---|---|
| `city-lab-dc-v3.html` | Line 22 loads Merriweather; `--ff-body: 'Merriweather'` (line 37) sets the **whole page body** and four other rules in serif | City Labs aren't editorial articles: body and those rules use `--font-primary`. Remove Merriweather and Inter 500 from line 22 (or drop the link; `header.js` loads the fonts). Delete `--ff-body` |
| `search.html` | Loads Merriweather 400 | Remove from the font link (covered in Phase B) |
| `atlas-portal/index.html` | Loads Merriweather 400/700 and Inter 800 | Internal, but creator-facing. Remove Merriweather and 800; any serif rules become `--font-primary`; it has its own header and footer (fine for an internal portal) |

### C3. `mobile.html`
Replace the legacy `Material+Icons` font link (line 24) with Material Symbols Outlined (already loaded by `header.js`) and change `material-icons` classes to `material-symbols-outlined`. Check each icon name exists in Material Symbols.

---

## 6. Phase D: Remaining Text Below 12px

After Phases A–C, run `python3 scripts/check_brand.py --report | grep font-size` and fix every public-page result with the recipes. On October 27 the public pages outside Phases A–C were:

| File | Count | Notes |
|---|---|---|
| `city-lab-chicago.html` | 36 | Mostly 9–11px labels and legends; mono inline strip handled in C1 |
| `city-lab-dc-v3.html` | 17 | |
| `latin-america-lab.html` | 14 | |
| `partners/nj-lab.html`, `partners/njlab.html` | 7 each | |
| `partners/_shell.html` | 2 | **Fix the shell first** (lines 80, 180) so new partner pages are born correct |
| Partner pages built from the shell (`ahp`, `cillizza`, `emily-atkin`, `icfj`, `iij`, `jessica-stahl`, `knowledge-creators`, `news-creator-corps`, `natgeo`, `joon-lee`, `karen-attiah`, `noah-smith`, `rahim-jessani`) | 3–5 each | Same two shell rules on each, plus a few page-specific ones |
| `research.html` | 6 | 11px labels |
| `wire.html` | 4 | |
| `assets/css/main.css` | 4 | Lines 441, 874, 2186, 2220 (shared: check every page that uses each selector) |
| `assets/js/main.js` | 3 | Lines 2189, 2200 (inline styles in JS templates) and 2988 (`ctx.font = '700 11px ...'`: canvas, use the Tag recipe as a font string) |
| `lists.html` | 3 | |
| `mobile.html` | 2 | |
| `co-ops.html` | 1 | |

Most are 11px Inter. Decide by role: all-caps labels become Label or Tag in Source Code Pro (v15 already moved all-caps UI labels to Source Code Pro); sentence-case text becomes Small (13px Inter).

---

## 7. Phase E: Weights and Font Loading

1. **Weights 800/900** on public pages: `teamdmv` (3, Phase B) and `atlas-portal` (1, Phase C) → 700. Internal pages (`atlas-signal-brief` 12, `beat-*` 4 each, `chicago-analysis` 4) → 700 when they're done.
2. **Inter 500.** About 37 files set `font-weight: 500`. For each rule that isn't Source Code Pro: text → 400; emphasis and UI → 600. Review on staging; 500 → 600 is visible on buttons and nav, 500 → 400 on meta text.
3. Then change the Inter request in `header.js` (line 60) to `family=Inter:wght@400;600;700` and remove any page-level Inter links that request 500 or 800.

---

## 8. Process, Review and Baseline

- **Order:** Phase A (one pull request, reviewed alone because it touches every page) → Phase B and C page by page (Bluesky with its mobile fix) → Phase D (fix the partner shell first) → Phase E.
- **Screenshots:** before and after at 390, 768 and 1440px for every page touched, in the same folder pattern as earlier sessions (`docs/design/v16-type/screens/`). James reviews on the staging preview.
- **After each pull request,** regenerate the baseline (`python3 scripts/check_brand.py --write-baseline`) in the same pull request. The counts must go down. CODEOWNERS sends it to James.
- **Don't change colors in this pass,** even where a line you're editing has an off-system color. Note them; the next update handles color. The exception is the C1 strips, which are deleted entirely.
- **List, don't decide:** clickable tags, layouts that can't fit text at the floor without a structural change, and the Team DMV header/footer question.

---

## 9. Acceptance

- `grep -rliE "DM Mono|DM\+Mono|JetBrains|Playfair|Hanken" --include=*.html --include=*.css --include=*.js .` returns only excluded paths (`_deprecated/`, Nodes and Networks).
- `python3 scripts/check_brand.py --report` shows zero `font-family`, `font-literal`, `serif-scope`, `serif-heading` and `font-size` results on public pages, `header.css`, `main.css` and `main.js` (Pulse and For Brands are cleared by their own brief).
- The shared footer shows 13px Label titles, 13px links and tagline, and 12px Tag copyright and legal links on every page; no page shows a second footer strip.
- The header loads Inter 400/600/700, Source Code Pro 500 and Material Symbols only; no page loads another font (Network panel).
- Every page touched passes visual review at 390, 768 and 1440px with no horizontal overflow and no truncated labels.
- James signs off on staging before each merge to `main`.
