# Atlas — Claude Code Session Guide

*Project: Independent Journalism Atlas (journalismatlas.com)*
*Owner: Justin | Design system: James (james@happicamp.com)*

---

## Project Overview

A vanilla JS + D3 static HTML site. No build step, no npm, no React. All pages are single HTML files deployed to Cloudflare Pages via GitHub auto-deploy. Data lives in `assets/data/` as JSON.

**Stack:** HTML + CSS + Vanilla JS + D3 v7. CSS custom properties for design tokens. No preprocessors.

**Deploy:** Push to GitHub → Cloudflare auto-deploys. Justin pushes via GitHub Desktop (not CLI).

---

## Design System

All visual implementation references `DESIGN-TOKENS.md` at the project root as the single source of truth. Its CSS implementation lives in `assets/css/variables.css` — the canonical token file, loaded before all other stylesheets.

**Do not infer or improvise colors, type sizes, spacing, or component states — look them up.**

### Non-negotiable rules (memorize these)

- **Acid green `#ceff00` = dark backgrounds only** — never on light/white surfaces
- **Lime green `#97d600` = light backgrounds only** — never on dark surfaces
- **Header text = always `#000000`** regardless of mode or surface color
- **Body Large (16px) is the minimum reading size** — do not go below this for body copy
- **Material Symbols Outlined only** — no legacy Material Icons; Filled variant reserved for active states only
- **8px base spacing unit** — all spacing must be multiples of 8 (xs = 4px is the only exception)
- **Font weights: 400 / 500 / 700 only** — do not introduce 600 or 800
- **Border radius: 6px for cards/buttons/inputs; 100px for pills/tags**

### CSS token architecture

```
assets/css/variables.css   ← THE canonical token file (implements DESIGN-TOKENS.md)
assets/css/main.css        ← Primary stylesheet for index.html
assets/css/animations.css  ← Standalone animation keyframes
```

**Load order in every page `<head>`:**
```html
<link rel="stylesheet" href="assets/css/variables.css">  <!-- FIRST -->
<link rel="stylesheet" href="assets/css/main.css">       <!-- or page-specific CSS -->
```

Pages with inline `<style>` blocks (postcard.html, partners/*.html, city-lab-chicago.html, latin-america-lab.html) also link variables.css before their inline block.

### How to use DESIGN-TOKENS.md in a session

Before writing any CSS or styling-related code, read the relevant section of `DESIGN-TOKENS.md`. Reference it explicitly in comments when implementing tokens:

```css
/* Primary accent — light mode only. DESIGN-TOKENS.md § Semantic Color Assignments */
--color-accent: #97d600;
```

### What requires James's sign-off before implementing

- Visualization color array (`ATLAS_VIZ_COLORS`) — assignments per topic category pending
- Full card vs. small card definitions in the postcard system
- Any new component type not already defined in the tokens doc

---

## Partner Page Naming Convention

All partner pages live in `partners/` subdirectory. Format: `partners/[slug].html` → `/partners/[slug]`.

```
partners/[curator-slug].html

Examples:
  partners/cillizza.html        Chris Cillizza
  partners/ahp.html             Anne Helen Petersen
  partners/icfj.html            ICFJ (institutional)
  partners/grist.html           Grist / Jess Stahl
  partners/chicago-tribune.html (institutional, city-specific)
  partners/dc-lab.html          (DC City Lab partner variant)

Slug rules:
  - Lowercase, hyphen-separated
  - For individuals: last name preferred (cillizza, petersen → ahp)
  - For institutions: org name abbreviated (icfj, grist, npr)
  - For city-specific partners: city + org (dc-dcist, chicago-wbez)
  - Never include version numbers in production filenames
```

Shell template at `partners/_shell.html` (internal, not public-facing). To spin up a new partner page: copy `_shell.html` → `partners/[slug].html`, fill in `PARTNER_CONFIG`, push.

Old root-level partner URLs redirect to new paths via `_redirects` at repo root.

---

## Key Constraints

- **Single deployable HTML file** — no build step, no external dependencies beyond CDNs
- **City Lab pages** — inline all data as JS constants (no fetch). Hard constraint.
- **pack.html, lists.html, mobile.html, index.html** — fetch() from `assets/data/creators-data.json`. Do NOT convert to inline constants (data is too large).
- **Cloudflare intercepts plain-text email** — encode as HTML entities or use `[at]` notation
- **Git push via GitHub Desktop** — never attempt `git push` from terminal
- **Clean up dead code while working** — remove dead CSS, unused classes, stale placeholder comments as they become irrelevant

---

## Page Inventory

| File | Description | Creator count | CSS approach |
|------|-------------|--------------|--------------|
| `index.html` | Main database | ~1,180+ (live JSON) | External: `main.css` |
| `postcard.html` | Starter Pack builder | — | Inline `<style>` |
| `partners/_shell.html` | Partner page shell (template) | — | Inline `<style>` |
| `partners/cillizza.html` | Chris Cillizza curated list | 17 | Inline `<style>` |
| `partners/ahp.html` | Anne Helen Petersen curated list | 9 | Inline `<style>` |
| `partners/icfj.html` | ICFJ global creator list (LatAm/Africa/MENA) | 21 | Inline `<style>` |
| `partners/grist.html` | Grist / Jess Stahl climate list | 19 | Inline `<style>` |
| `city-lab-chicago.html` | Chicago journalism ecosystem | 245+ | Inline `<style>` + inlined data |
| `latin-america-lab.html` | Latin America & Caribbean creator lab (ICFJ) | — | Inline `<style>` + inlined data |

All pages above have been swept to the design token system (variables.css linked first, slim `:root` alias block, no canonical token redefinitions inline). Design sweep completed April 2026.

---

## Out of Scope Until Further Notice

- `ATLAS_VIZ_COLORS` — pending James's color assignments per topic category
- Full postcard card system — pending James's spec
- Additional city lab pages beyond Chicago — same pattern as city-lab-chicago.html when ready
- Mainstream outlet layer in city-lab-chicago (Tracy Baim / Liz feedback — separate session)
- Additional ICFJ region labs (africa-lab, asia-lab, etc.) — same pattern as latin-america-lab.html
