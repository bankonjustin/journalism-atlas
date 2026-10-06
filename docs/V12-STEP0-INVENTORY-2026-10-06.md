# DESIGN-TOKENS v12 — Step 0 Inventory (read-only)

## Gate A rulings (from Justin, 2026-10-06, verbatim)

1. Header default = WHITE (live state). Build the data-header-theme switch with white as the default and the existing black wordmark. Black-header option stays unwired (no wht asset in repo). Do not create or recolor any SVG.
2. "Jump to" sub-nav: follow v12, match the header via one shared variable (white by default). Report any active/hover state that uses acid green or another color that fails on white; do not invent a replacement.
3. Do NOT redefine --color-accent (stays lime). Add the other v12 variables, including --color-hover. Mark the line "PENDING JAMES — v12 treats lime as hover-only, site uses it as primary accent on light."
4. Olive: do not touch hover uses (--color-accent-hover, search-button hover). For the ~110 other lines, produce a table: file, line, element, role (text/border/fill/hover/other), proposed v12 replacement. Apply nothing until I approve.
5. Tokens file: delete the unversioned DESIGN-TOKENS.md (v11) via git so it shows in the diff, and update every reference (CLAUDE.md, variables.css comments, header comments) to DESIGN-TOKENS-v12.md. I've placed v12 at the repo root.

Fix-ups to the inventory:
- Redo the var() consumer count with grep -rE (no zsh loops): list which variable names hold a retired gray (variables.css and inline :root blocks), then count consumers of each. Where a retired gray lives inside a variable definition, change the definition once rather than every consumer.
- Diff "CLAUDE copy.md" against CLAUDE.md and report. Don't delete it.

Phase 2 split, stop for me to commit after each:
- 2a: variables.css + unambiguous swaps (#313131, #efeff2, #6b6b6b) + the single #ff9600 comment. Dry-run summary first.
- 2b: #bdbdbd, #a8a8a8, #9e9e9e (~30 lines), each with its role and surface noted in the dry-run.
- Phase 3 (header/sub-nav) is its own stop.
- Olive table (item 4) and Phase 4 audit are report-only.

Unmapped grays (#d4d4d8, #b0b0b8, #888, #555, warm family): report only, don't change. Add a proposed nearest-step mapping table with role context for James to approve in a follow-up. The live D3 brand-secondary-as-category findings stay Phase 4 report-only.

---


*Written 2026-10-06. Repo: `~/Documents/GitHub/journalism-atlas`, branch `main`, working tree clean at start. No files were edited except this one. Scope of greps: tracked `*.html *.css *.js *.py *.md`. "Live" = excluding `_deprecated/`, `_reference/`, `outputs/`, `sessions/`, `research/figures/`.*

## 1. Verified vs. assumption

| # | Assumption | Result |
|---|---|---|
| 1 | Repo at `~/Documents/GitHub/journalism-atlas` | **Verified.** Clean tree, `main`. |
| 2 | `variables.css` canonical; `header.js` injects nav | **Verified.** `assets/css/variables.css`, `assets/css/header.css`, `assets/js/header.js`. Note `main.css` also still carries its own copies of `.top-nav` / `.nav-logo` rules (lines 23–72, 1504–1520) and `atlas-portal/index.html` has inline ones. |
| 3 | Tokens doc filename | **Verified, and it's the v11 "merged" file:** unversioned `DESIGN-TOKENS.md` (header says "v11 (merged)", Sept 20 2026). `DESIGN-TOKENS-v12.md` is **not in the repo** (I read it from `~/Downloads`). Also `ATLAS_VIZ_COLORS.md` and a stray `CLAUDE copy.md` / `PARTNERS copy.md` exist. |
| 4 | Inter/Merriweather/Source Code Pro migration landed | **Mostly.** `variables.css` and `header.js` use Inter. `CLAUDE.md:96` still says header.js "Injects Hanken Grotesk". Several pages still reference `JetBrains Mono` (e.g. `index.html:243`). Out of scope here. |
| 5 | White horizontal logo may be missing | **Confirmed missing, and worse:** *no* `Atlas_logo_lockup_*` file exists in the repo at all (neither `_blk_web` nor `_wht_web`, nor the stacked footer one). The live header uses `assets/images/logos/Journalism_Atlas_wordmark_horizontal_lockup_black.svg`. There is a white **PNG** lockup (`..._horizontal_lockup_white.png`) but no white SVG. |
| 6 | Stale CLAUDE.md rules | **Partly.** See §3. "Weights 400/500/700 only" and "8px base spacing" are *already* corrected in CLAUDE.md (it says 4px and 400–800). Still stale: header text always `#000`, acid/lime surface rule (left as-is per brief), v11 file name refs. |

## 2. Findings that contradict the brief — decisions needed

1. **The live header is WHITE, not black.** `header.css:17` `.top-nav { background-color: var(--white) }`, with the *black* wordmark SVG. Phase 3 says "ship black as default (the current look), so no visual change." That would change the look on every page. **Recommend default = white** (`data-header-theme="white"`), which is a no-op on release.
2. **The report "Jump to" sub-nav is black** (`research/nodes-and-networks.html:50–58`, `background: var(--color-black)`, comment says "Black = site header background") while the header above it is white. So today the docked element already mismatches. Under v12 it must follow the header; with a white default it would change from black to white. Needs Justin/James to confirm intended look.
3. **`--color-accent` collision.** Today `--color-accent` = `#97d600` (lime, light-mode CTA), `--color-accent-dark` = `#ceff00`, `--color-accent-hover` = `#5d7400` (olive). v12's variable block defines `--color-accent: #ceff00` and `--color-hover: #97d600`. Applying v12 literally flips every consumer of `var(--color-accent)` from lime to acid on light surfaces, which contradicts "don't alter acid/lime usage." **Proposal:** add v12's `--color-hover`, keep `--color-accent` at its current value until James rules on the acid/lime question, and flag it. Needs a decision.
4. **Dark Olive is a UI hover token today.** `--color-accent-hover: #5d7400` (`variables.css:49`) and `.nav-search-btn:hover` (`header.css:132`) are the hover state for the search button and others. v12 says hover = Lime `#97d600`. Replacing is clear for hover states, but note lime `#97d600` hover over a lime `#97d600` button (`header.css:119`) is a no-op, so the search button needs a decision.
5. **Brand secondary colors are used as data-category colors in live D3 code** (`index.html:1530–1537` beat-cluster colors `#ff66ff #00e5ff #ffaa00 #fff700 #ff33cc`; `search.html:934–936` same set). v12 says brand secondary is never used for data categories. **`ATLAS_VIZ_COLORS` category hexes appear in zero live files** (only in docs and `_deprecated/index-mock-V5.html`), so the "means its category everywhere" rule has nothing to violate yet, but the live charts use the wrong tier. Phase 4 report item, not changed.
6. **`#ff9600` has one hit only**, a code comment (`atlas-portal/index.html:440`) saying it was *replaced*. No live D3 `#ff9600`. `#ffaa00` is already used widely. Phase 2's orange step is effectively a comment edit.
7. **No `data-header-theme` anywhere; header lives in three places** (`header.css`, `main.css` duplicates, `atlas-portal/index.html` inline). `main.css` duplicates will win or lose by load order and must be reconciled in Phase 3.

## 3. CLAUDE.md lines that conflict with v12

| Line | Text (abridged) | Conflict |
|---|---|---|
| 24–25, 57, 104–107 | refers to `DESIGN-TOKENS.md` | should point to `DESIGN-TOKENS-v12.md` |
| 67 | "Header text = always `#000000` regardless of mode or surface color" | header is black or white; nav text follows header |
| 96 | "Injects Hanken Grotesk + Material Symbols" | Inter (typography, already stale vs. v11) |
| 261 | wordmark PNG "Site header (white background)" | header logo is now the SVG pair |
| 65–66 | acid dark-only / lime light-only | **leave, add `⚠ PENDING JAMES` note per brief** |
| 70–71 | 4px spacing; 400–800 weights | already correct |

(`CLAUDE copy.md` differs from `CLAUDE.md`; I did not diff it. Likely a stray duplicate, tell me if you want it compared or ignored.)

## 4. Counts

### Retired grays (hex, case-insensitive, `*.html *.css *.js *.py *.md`)
- **791 lines across 74 files, all areas.** Over your 300 threshold. By area: `partners/` 288 (19 files), repo root 269 (28 files), `_deprecated/` 211 (23 files), `assets/` 18, `atlas-portal/` 5.
- **Live code only (excl. `_deprecated`, `_reference`, `outputs`, `sessions`, `research/figures`): ≈690 lines.** Per color: `#313131` 392 · `#efeff2` 237 · `#bdbdbd` 30 · `#6b6b6b` 6 · `#9e9e9e` 6 · `#a8a8a8` 1.
- `#313131` and `#efeff2` are overwhelmingly (a) the *legacy-alias* definitions and (b) page-level `body`/text colors in inline `<style>` blocks. Those two are near-mechanical (primary text, page bg). `#bdbdbd` (30) is the one that needs role+surface judgment.
- Top live files: `partners/njlab.html` + two identical copies (`njlab copy.html`, `nj-lab.html`) 43 each, `beat-tech.html` 43, `beat-climate.html` 29, `wire.html` 23, `beat-finance.html` 23, `pulse.html` 20, `city-lab-chicago.html` 18, `research.html` 16, `for-brands.html` 16, `index.html` 14, `variables.css` 13, `about-this-project.html` 13, 14 `partners/*.html` at 10–12 each. `header.css` 5 (lines 120, 161, 162, 286–294).
- **rgba forms:** `header.css:161–162` `rgba(49,49,49,…)` (#313131); `partners/nj-lab.html` several `rgba(239,239,242,0.45–0.75)` (#efeff2 on dark). No `rgb()`/`hsl()` hits for the other retired values.
- **`var()` indirection:** `variables.css` defines `--color-dark-gray`, `--color-light-gray`, `--dark-gray`, `--light-gray`, `--medium-gray (#999999)`, `--color-text`, `--color-bg`, `--color-bg-dark (#313131)`, `--color-text-dark (#efeff2)`, `--color-muted-dark (#bdbdbd)`, etc. Fixing the definitions fixes every `var()` consumer in one place; the hardcoded hex lines are the real migration work. **I did not reliably count `var()` consumers** (my loop failed on `zsh` subscript syntax), so the number of pages indirectly affected is not yet known.
- Markdown: `DESIGN-TOKENS.md` 12 (history, expected), `README.md` 2, `CSS_AUDIT.md` 1, `atlas-portal/LOGO_GUIDE.md` 1.

### `#ff9600`: 1 (a comment). `rgb(255,150,0)`: 0.
### `#5d7400` / `rgba(93,116,0,…)`
- **≈110 live lines, 32 live files** (+ `_deprecated`). Heaviest: `index.html` 25 (e.g. `pulse-open-btn` color and border at 249–250), `pulse.html` 19, `city-lab-chicago.html` 14, `research.html` 8, `about-this-project.html` 8, `partners/njlab` ×3 at 3, one each in ~20 partner/other pages.
- **UI vs non-UI split is not done line by line.** Spot check says nearly all are UI (hover states, link/button colors, borders, `variables.css:23,49`, `header.css:132`). Treat as UI unless proven otherwise; the real split needs the Phase 2 dry-run's role column. Replacement is clear for hover (→ `#97d600`) but links/text/borders on light surfaces need a monotone choice per use.

### Unmapped grays (not in either scale, **reported, not to be fixed**)
Top by count (live): `#d4d4d8` 105 (28 files) · `#b0b0b8` 70 · `#606068` 63 (incl. `--color-border-dark-hover`) · `#e0e0e0` 47 (incl. `header.css`, `main.css`) · `#1a1a1a` 38 · `#555555` 29 · `#2a2a2a` 26 · `#111111` 25 · `#f0f0f0` 19 · `#5f6368` 10 · `#fafafa` 9 · `#e4e4e8/e4e4e9` 17 · plus `#ddd #eee #e5e5e5 #1f1f1f` in `header.css` and `#999999` (`--medium-gray`). Three-digit: `#888` 77, `#555` 58, `#666` 51, `#444` 34, `#aaa` 32, `#111` 30, `#999` 22, `#333` 20. Plus warm-gray family in some pages (`#888880 #4a4a46 #ddddd8 #1a1a18 #5f5e5a`, ~115 / 71 / 50 / 31 / 30), which look like a separate off-brand scheme. These are a large unmapped surface: v12 retires six grays but leaves hundreds of other gray values untouched. Worth a James conversation.

### Hardcoded values duplicating tokens
`#ceff00` 226 and `#97d600` 131 occurrences vs. variables existing for both; `#000`/`#fff` shorthand 288 / 267. Per-file detail deferred (large); say if you want it.

## 5. Header inventory
- **Background:** `header.css:17` (white, `.top-nav`), `:30` scrolled shadow, `:18/:31` borders `#ddd`/`#e5e5e5`. Duplicated in `main.css:23–72` and `1504–1520`, and `atlas-portal/index.html:46–90`.
- **Nav text:** `header.css:54` (`--black`), `:104` (`--dark-gray`), `:114`, `:178`, `:237`, `:255`.
- **Search input:** `header.css:82` border `#e0e0e0`, focus `:93–94` lime; button `:119–120` lime bg / `#313131` text, hover olive `:132`.
- **Mobile menu:** `header.css:196–267` (white panel, `#eee` border, active `--light-gray` bg / lime left border).
- **Scroll-shrink:** `.top-nav.scrolled` (`header.css:28`, `:65`, `:316`, `:328`; `header.js:_initScroll`).
- **Logo path:** `header.js:49` (hardcoded `Journalism_Atlas_wordmark_horizontal_lockup_black.svg`).
- **Footer** (not in scope, but shares `header.css`): `:271–295`, black, uses `#bdbdbd` ×4 as secondary text on dark and `#1f1f1f` divider.
- **Docked elements:** `research/nodes-and-networks.html` `.section-nav-wrap` (black, `top: var(--header-h)`; see §2.2). No other sticky bar under the header found in live pages; `research/figures/*` have their own `.tab-nav` (inside embedded figures, excluded).

## 6. Category colors outside charts
`ATLAS_VIZ_COLORS` hexes: **0 in live code.** Only `ATLAS_VIZ_COLORS.md`, `DESIGN-TOKENS.md`, `_deprecated/index-mock-V5.html`. So no non-chart misuse today.

## 7. Brand-secondary use
- Live hits: `search.html` 13, `variables.css` 10 (the legacy `--viz-*` definitions), `index.html` 5, `partners/njlab` ×3 at 4 each, `city-lab-chicago.html` 1, `bluesky-creator-intelligence.html` 1.
- In `index.html` and `search.html` they are the **beat/cluster category colors in D3** (a data-category use, which v12 forbids). `search.html:934–936` has comments admitting some are "too faint on light bg." Not UI states, as far as I saw. Phase 4 item.

## 8. Editorial badges ("HIRED" etc.)
Only data matches (a post title in `atlas-signal-brief.html`, text in `research/nodes-and-networks.html:381`); no "HIRED"-style badge component found in the live CSS. Nothing to report beyond that; a deeper look at `research/nodes-and-networks.html` badges may be worth doing in Phase 4.

## 9. Pages with their own `:root` token blocks
`atlas_pulse_intelligence.html`, `atlas_wire_intelligence.html`, `partners/karen-attiah.html`, `partners/knowledge-creators.html`, `partners/natgeo.html`. (Also pages with inline `<style>` using hardcoded hex without redefining `:root`: most of `partners/*`, `city-lab-chicago.html`, `latin-america-lab.html`, `atlas-portal/index.html`.) `postcard.html` does not exist in this repo.

## 10. Ambiguous roles (to flag, not auto-fix)
- All 30 live `#bdbdbd` lines (border vs. text, light vs. dark surface).
- `#a8a8a8` (`--color-border-hover`): v12 has no hover-border role; probably Cool-4 `#909097` or keep Cool-3, needs a ruling.
- `--color-muted-dark: #bdbdbd` and `--medium-gray: #999999` (the latter isn't a retired hex but is an alias in the same group).
- `--color-bg-dark: #313131` (a *surface*, not text; v12 maps `#313131` to primary text = step 6, but dark surfaces are step 7 `#121218`).
- `--color-text-header-dark: #000000` ("header text always black"), will conflict with a black header.
- `--color-border-dark: #48484f` / `-hover: #606068`: not in either scale.
- Every `#efeff2` used as *text on dark* (e.g. `partners/nj-lab.html` rgba lines) rather than a page background.
- Dark Olive on light-surface links/borders (no direct substitute chosen yet).

## Summary for Gate A
- **Scale:** ~690 retired-gray lines in live code (791 repo-wide). Over your 300 threshold, but ~85% is `#313131`/`#efeff2`, mostly mechanical. Real judgment is on `#bdbdbd` (30) and Dark Olive (~110).
- **Blockers/decisions before Phase 1:** (1) `DESIGN-TOKENS-v12.md` isn't in the repo yet; (2) header default should be **white**, not black; (3) sub-nav intended color; (4) `--color-accent` lime vs. acid semantic collision; (5) white header logo SVG and the `Atlas_logo_lockup_*` file family are all missing; (6) hover-on-search-button once olive is gone.

---

## Fix-ups (2026-10-06, after Gate A)

### Variables that hold a retired gray, with `var()` consumer counts (live files)
Replaces the earlier "not reliably counted" note. Definitions are changed once; consumers follow.

| variable | holds | defined in | consumers | files |
|---|---|---|---|---|
| `--olive` | #313131 | city-lab-dc-v3.html | 86 | 18 |
| `--page-bg` | #efeff2 | 17 pages (bluesky-creator-intelligence, partners/*) | 78 | 18 |
| `--text` | #efeff2 | atlas_pulse_intelligence, atlas_wire_intelligence, atlas_wire_review, chicago-analysis | 55 | 4 |
| `--dark-gray` | #313131 | variables.css + 7 pages (about, advisory, atlas-portal, how-we-did-this, lists, mobile, who-we-are) | 49 | 11 |
| `--light-gray` | #efeff2 | variables.css + 6 pages | 36 | 11 |
| `--dark` | #313131 | chicago-survey, city-lab-dc-v3 | 25 | 3 |
| `--text-primary` | #313131 | bluesky-creator-intelligence | 20 | 2 |
| `--color-border` | #bdbdbd | variables.css | 13 | 2 |
| `--color-bg` | #efeff2 | variables.css | 10 | 3 |
| `--color-muted` | #9e9e9e | variables.css | 5 | 1 |
| `--color-text` | #313131 | variables.css | 5 | 2 |
| `--light` | #efeff2 | chicago-survey, city-lab-dc-v3 | 5 | 1 |
| `--color-text-secondary` | #6b6b6b | variables.css | 3 | 1 |
| `--color-bg-dark`, `--color-border-hover`, `--color-text-dark` | 313131 / a8a8a8 / efeff2 | variables.css | 1 each | 1 each |
| `--color-dark-gray`, `--color-light-gray`, `--color-muted-dark` | — | variables.css | 0 | 0 |
| `--tab-active-text` | #313131 | city-lab-chicago | 0 | 0 |

Notes: **`--olive` in `city-lab-dc-v3.html` is a misnomer: it holds `#313131`** (a dark gray), so it is *not* Dark Olive and the olive table does not include it. The per-page definitions (`--page-bg`, `--text`, `--dark-gray`, …) are each a single line, so they are covered by the 2a dry-run.

### `CLAUDE copy.md` vs `CLAUDE.md`
`CLAUDE copy.md` is an **older snapshot of `CLAUDE.md`** from before the 2026-09-03 private-repo/spidering move. Four differences, all stale-vs-current: the `CURRENT_STATE.md` note (old: "Atlas Spidering/sessions/…"), the `liz-editorial` location, the "External file locations" table (old copy still lists the untracked `~/Documents/Atlas Spidering/` row), and the missing `research/nodes-and-networks.html` page-inventory row. Nothing in it that CLAUDE.md lacks. Left in place, still references `DESIGN-TOKENS.md`, not updated. Safe to delete whenever you want.

### Remaining `DESIGN-TOKENS.md` mentions (history, left as written)
`CURRENT_STATE.md` (4), `CSS_AUDIT.md` (5), `CLAUDE copy.md` (7), and `_deprecated/`.

### Housekeeping
`.DS_Store` shows as modified in `git status`; it is tracked and not mine. Worth untracking separately.
