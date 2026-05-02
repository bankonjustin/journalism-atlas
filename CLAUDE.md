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

**Designer's principles:** James Bareham's 15 web design principles live at `_reference/james-design-principles.md`. Read this before making any structural or layout decisions. Key principles that come up constantly: The Explanation Principle (every module needs a narrative entry point), The Surface Hierarchy Principle (dark = stage, light = workspace), The Placeholder Principle (no empty states in public-facing design), and The Tool Principle (every element must serve the user's task).

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
assets/css/header.css      ← Shared site header + footer wordmark styles (all pages)
assets/css/main.css        ← Primary stylesheet for index.html only
assets/css/animations.css  ← Standalone animation keyframes
```

**Load order in every page `<head>`:**
```html
<link rel="stylesheet" href="assets/css/variables.css">  <!-- FIRST -->
<!-- page inline <style> block (if any) -->
<link rel="stylesheet" href="/assets/css/header.css">    <!-- LAST in <head> — overrides inline nav CSS -->
```

`header.css` uses absolute paths (`/assets/...`) and must be the last stylesheet in `<head>` so it wins cascade over any inline nav styles.

**Shared header component:**
The site header is injected via `assets/js/header.js` — a self-contained script that:
- Inserts the `<nav class="top-nav">` HTML as the first element in `<body>`
- Wires up mobile menu, scroll-shrink, and search navigation
- Injects Hanken Grotesk + Material Symbols fonts if not already loaded

`header.js` is loaded as the **first** `<script>` tag in `<body>` on every page. Do not duplicate nav HTML manually — edit `header.js` to change nav content.

Pages with inline `<style>` blocks (postcard.html, partners/*.html, city-lab-chicago.html, latin-america-lab.html) link variables.css before their inline block, and header.css after it (before `</head>`).

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

## URL Structure

Canonical URLs use **no `.html` extension** (Cloudflare Pages clean URLs):
- Home: `https://journalismatlas.com/`
- Root pages: `https://journalismatlas.com/[stem]` (e.g. `/who-we-are`, `/research`)
- Partner pages: `https://journalismatlas.com/partners/[slug]`

`og:url`, `og:canonical`, and Twitter meta tags must match these clean URLs — no `.html` suffix.

Redirects live in `_redirects` at repo root (Cloudflare Pages format).

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
| `partners/ahp.html` | Anne Helen Petersen picks | 17 | Inline `<style>` |
| `partners/icfj.html` | ICFJ global creator list (LatAm/Africa/MENA) | 21 | Inline `<style>` |
| `partners/news-creator-corps.html` | News Creator Corps curated list | 16 | Inline `<style>` |
| `partners/joon-lee.html` | Joon Lee sports/culture picks | 14 | Inline `<style>` |
| `partners/jessica-stahl.html` | Jessica Stahl climate picks | 22 | Inline `<style>` |
| `partners/knowledge-creators.html` | Knowledge Creators edu-journalism list | 17 | Inline `<style>` |
| `partners/emily-atkin.html` | Emily Atkin climate picks | 11 | Inline `<style>` |
| `partners/natgeo.html` | NatGeo creator cohort | 8 | Inline `<style>` |
| `partners/karen-attiah.html` | Karen Attiah picks | 8 | Inline `<style>` |
| `partners/rahim-jessani.html` | Rahim Jessani / Bottom Up Media picks | 7 | Inline `<style>` |
| `partners/noah-smith.html` | Noah Smith economics picks | 8 | Inline `<style>` |
| `city-lab-chicago.html` | Chicago journalism ecosystem | 245+ | Inline `<style>` + inlined data |
| `latin-america-lab.html` | Latin America & Caribbean creator lab (ICFJ) | — | Inline `<style>` + inlined data |

All pages above have been swept to the design token system (variables.css linked first, slim `:root` alias block, no canonical token redefinitions inline). Design sweep completed April 2026.

### Internal / dev-only pages (not public-facing — skip OG tags, skip in bulk operations)

| File | Notes |
|------|-------|
| `what-we-do.html` | Legacy URL — redirects to `about-this-project.html` via `_redirects` |
| `about-this-project.html` | Canonical "About This Project" page (replaced what-we-do.html) |
| `atlas-portal/index.html` | Internal portal |
| `atlas-portal/google-form-template.html` | Internal template |
| `bluesky-creator-intelligence.html` | Research/dev — not public |
| `bluesky-creator-intelligence-v2/v3/v4/v5.html` | Version history — not public |
| `beat-tech.html`, `beat-climate.html`, `beat-finance.html` | Research pages — not public |
| `chicago-analysis.html`, `chicago-survey.html` | Internal research — not public |
| `knight-brief.html`, `atlas-signal-brief.html` | Internal briefs — not public |
| `index-exploration-V1.html` | Dev experiment — not public |
| `partners/_shell.html` | Partner page template — not public |

### Logo files (assets/images/logos/)

| File | Use |
|------|-----|
| `Journalism_Atlas_wordmark_horizontal_lockup_black.png` | Site header (white background) |
| `Journalism_Atlas_wordmark_horizontal_lockup_white.png` | Footer (black background) |
| `Journalism_Atlas_wordmark_stacked_green_white (3).png` | Hero section on index.html |
| `Journalism_Atlas_logo_acid_green.png` | Icon-only uses |

The `_lockup_` files (no "horizontal" in name) are the old equivalents — prefer the `_horizontal_lockup_` versions going forward.

---

## Out of Scope Until Further Notice

- `ATLAS_VIZ_COLORS` — pending James's color assignments per topic category
- Full postcard card system — pending James's spec
- Additional city lab pages beyond Chicago — same pattern as city-lab-chicago.html when ready
- Mainstream outlet layer in city-lab-chicago (Tracy Baim / Liz feedback — separate session)
- Additional ICFJ region labs (africa-lab, asia-lab, etc.) — same pattern as latin-america-lab.html
