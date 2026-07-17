# Atlas — Claude Code Session Guide

*Project: Independent Journalism Atlas (journalismatlas.com)*
*Owner: Justin | Design system: James (james@happicamp.com)*
*Last updated: June 23, 2026*

**Read at session start:** This file + `WORKFLOW.md` (decision authority, "done" definition, Chat→Code handoff protocol, deploy process).

---

## Session Behavior

### Tone

- No sycophantic openers ("Great question!", "I'd be happy to help with that!", "Absolutely!")
- No restating the request back before answering
- No hedging on calls already settled by this file, `DESIGN-TOKENS.md`, or `james-design-principles.md` — state the answer, cite the rule, move on
- Flag genuine ambiguity once, briefly, then proceed with the most reasonable interpretation rather than stalling

### Required reading order

| File | When |
|------|------|
| `CLAUDE.md` (this file) | Always |
| `DESIGN-TOKENS.md` | Before any CSS/styling work |
| `_reference/james-design-principles.md` | Before any visual/component decision |
| `CURRENT_STATE.md` (this repo) | Always, for site/deploy/subagent state |
| `DATA-OPS-PROTOCOL.md` | Before touching `creators-master.csv`, intake, or any pipeline script |

**Note (added July 7, 2026 — filesystem audit):** `CURRENT_STATE.md` in this repo covers site/deploy/subagent state only. Data-pipeline and spidering state lives in a *different* file with the same name: `Atlas Spidering/sessions/CURRENT_STATE.md` (a separate, untracked workspace — see "External file locations" below). Read whichever one matches the task; they are not duplicates of each other. A third file, `Atlas Spidering/core/CURRENT_STATE.md`, existed until this session — it was actually a single stale session log misnamed to look like a tracker, and has been archived as `Atlas Spidering/archive/SESSION_LOG_bsky_corpus_anchor_v1_20260626.md`.

### Session close-out

- Update `CURRENT_STATE.md` before ending any session that changed data, pipeline state, or in-flight work — even if not explicitly asked
- Note new out-of-scope items or blockers discovered mid-session in `CURRENT_STATE.md`, not just in chat

### Role-scoped subagents

- **`ryan-dataops`** (`.claude/agents/ryan-dataops.md`, this repo) — Ryan's data-ops lane: `creators-master.csv`, `atlas-private-columns.csv`, `DATA-OPS-PROTOCOL.md`. No Bash tool (hard block on running any script, including `atlas_groups.py`/`atlas_append.py`). No git push.
- **`liz-editorial`** (`.claude/agents/liz-editorial.md`, Atlas Spidering workspace, not this repo) — read-only: editorial standards doc v1.4 + Global Correspondents session note. No Shadow Lists or rejection-notes access — both are canonical Google Sheets and no Sheets connector exists in this environment (see `CURRENT_STATE.md`). Revisit once that's resolved.
- Scoping for these subagents is enforced by their prompt instructions and by which tools are granted (e.g. omitting Bash) — not by a filesystem ACL. Treat the "in scope" file lists as a convention the subagent is instructed to follow, not a hard sandbox.

---

## Project Overview

A vanilla JS static HTML site. No build step, no npm, no React. All pages are single HTML files deployed to Cloudflare Pages via GitHub auto-deploy. Data lives in `assets/data/` as JSON.

**Stack:** HTML + CSS + Vanilla JS. CSS custom properties for design tokens. No preprocessors. D3 v7 is present for specific visualizations but is not the general rendering approach — most page UI is vanilla JS.

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
- **Body copy minimum 16px** — Small (13px) is the floor for all UI text. Micro (11px) for all-caps labels only (weight 500 min, letter-spacing 0.08–0.1em). Never below 13px for any readable content.
- **Material Symbols Outlined only** — no legacy Material Icons; Filled variant reserved for active states only
- **4px base spacing unit** — spacing scale: xs 4px / sm 8px / md 16px / lg 24px / xl 32px / 2xl 48px
- **Font weights: 400 / 500 / 600 / 700 / 800** — 500 for Micro labels only; 600 for H3/card titles; do not introduce 900 or other weights
- **Border radius: 6px for cards/buttons/inputs; 9999px for pills/tags**

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

Pages with inline `<style>` blocks (partners/*.html, city-lab-chicago.html, latin-america-lab.html) link variables.css before their inline block, and header.css after it (before `</head>`).

### How to use DESIGN-TOKENS.md in a session

Before writing any CSS or styling-related code, read the relevant section of `DESIGN-TOKENS.md`. Reference it explicitly in comments when implementing tokens:

```css
/* Primary accent — light mode only. DESIGN-TOKENS.md § Semantic Color Assignments */
--color-accent: #97d600;
```

### What requires James's sign-off before implementing

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

## Data Pipeline

`creators-master.csv` → `node convert.js` → `creators-data.json` (live site reads this).

See `DATA-OPS-PROTOCOL.md` for migration steps, how to add bespoke creators, and how to keep Ryan's master in sync.

---

## External file locations (updated July 7, 2026 — private repo setup)

Four locations now exist. Don't assume file paths from older briefs still hold — this map was verified against disk, not carried forward from memory.

| Location | What lives there | Tracked? |
|---|---|---|
| `journalism-atlas/` (this repo) | Production site, deploy docs, pipeline scripts (`pipeline/`) | Git, deploys to Cloudflare (public) |
| `journalism-atlas-private/` (github.com/bankonjustin/journalism-atlas-private) | Editorial/reference docs (`ATLAS-EDITORIAL-STANDARDS`, `REJECTION_GUIDE`, `DATA-ROADMAP`), the live `atlas-private-columns.csv`, dated master-CSV snapshots | Git (private) — access: Justin, Ryan, Liz, James |
| `~/Documents/Atlas Spidering/` | Spidering scripts/output, pulse pipeline, `SCHEMA-VOCAB.md` | Not in Git — local only |
| `~/Downloads/` | Still holds a large accumulation of briefs, historical Mega-Database files, and design assets going back to January 2026 (categorized, not yet individually triaged — see open item below). A maintained *mirror* of `ATLAS-EDITORIAL-STANDARDS` also lives here (`ATLAS-EDITORIAL-STANDARDS-v1_4.md`) solely for `liz-editorial.md`'s hardcoded path — see `DATA-OPS-PROTOCOL.md` § "Reference doc locations." | Not tracked |

**Corrections to prior claims:** (1) Earlier docs assumed `ATLAS-EDITORIAL-STANDARDS.md` lived in this repo's `_reference/` folder — it never has. (2) As of the July 7 filesystem audit, this doc said the private repo was "proposed, not yet built" — it's since been approved and built; that recommendation is superseded by the row above.

**Still open:** `~/Downloads/` has 150+ Atlas-related files beyond what's been migrated so far, categorized at the bucket level but not individually triaged (Mega-Database, historical briefs, business/legal docs, older private-columns/master-CSV snapshots predating the private repo). A follow-up pass is expected.

`journalism-atlas/spidering/` must stay empty — confirmed empty as of this audit. Nothing spidering-related belongs there; see `Atlas Spidering/SPIDERING_ALIGNMENT_GUIDE.md`.

---

## Creator Count Convention

**Never hardcode a creator count as a bare number.** The canonical count is always derived from `creators-data.json` at runtime.

- **Visible UI text:** Wrap in `<span class="js-creator-count">1,718</span>`. Pages that fetch `creators-data.json` update all `.js-creator-count` spans automatically with the live count.
- **Pages without a JSON fetch:** Add a lightweight fetch snippet (see `about-this-project.html` or `for-brands.html` for the pattern).
- **Meta/OG/Twitter description tags:** Cannot be dynamic (crawlers read before JS runs). Update manually when the count milestone changes. Use rounded `1,700+` form, not the exact number.
- **Partner page attribution strings** ("Curated from X creator-journalists"): Use `1,700+` rounded form. Update when the count crosses the next hundred.
- **Cluster card counts on index.html:** Computed dynamically from `allCreators` by `_updateClusterCards()` after data loads — do not hardcode.

---

## Key Constraints

- **Single deployable HTML file** — no build step, no external dependencies beyond CDNs
- **City Lab pages** — inline all data as JS constants (no fetch). Hard constraint.
- **lists.html, mobile.html, search.html** — fetch() from `assets/data/creators-data.json`. Do NOT convert to inline constants (data is too large).
- **Cloudflare intercepts plain-text email** — encode as HTML entities or use `[at]` notation
- **Git push via GitHub Desktop** — never attempt `git push` from terminal
- **Clean up dead code while working** — remove dead CSS, unused classes, stale placeholder comments as they become irrelevant

---

## Page Inventory

| File | Description | Creator count | CSS approach |
|------|-------------|--------------|--------------|
| `index.html` | Homepage — hero, stat strip, cluster grid | — | `variables.css` + inline `<style>` + `header.css` |
| `search.html` | Full creator database — filters, search, card grid | live JSON, count varies by Final Clean | External: `main.css` |
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
| `city-lab-dc-v3.html` | DC/DMV journalism ecosystem — "Who Covers Washington Now" | ~350 | Inline `<style>` + inlined data |
| `latin-america-lab.html` | Latin America & Caribbean creator lab (ICFJ) | — | Inline `<style>` + inlined data |
| `nj-lab.html` | NJ State Lab — CCM partnership. 51 creators (CCM NJ Influencer Study), 6 sections, filterable grid, CSS vizzes. | 51 | Inline `<style>` + inlined data |
| `bluesky-creator-intelligence.html` | Bluesky Creator Intelligence — AT Protocol ecosystem map. 552+ creators (live from `assets/data/bluesky-creators.json`). Beat cluster map (live-computed), creator index, methodology band, coverage gaps + suggest-a-creator. Canonical URL: `/bluesky-creator-intelligence`. **Nav inclusion: flag for James — not added to header.js this session.** | 552+ (live JSON) | `variables.css` + inline `<style>` + `header.css` |

All pages above have been swept to the design token system (variables.css linked first, slim `:root` alias block, no canonical token redefinitions inline). Design sweep completed April 2026.

### Internal / dev-only pages (not public-facing — skip OG tags, skip in bulk operations)

| File | Notes |
|------|-------|
| `what-we-do.html` | Legacy URL — redirects to `about-this-project.html` via `_redirects` |
| `about-this-project.html` | Canonical "About This Project" page (replaced what-we-do.html) |
| `_deprecated/postcard.html` | **Retired July 2026** — Starter Pack builder. No traffic, stale creator-count copy. `/postcard` now redirects to `/` via `_redirects` (the matching Cloudflare Pages Function that used to intercept `/postcard` was also removed — see `_deprecated/functions-postcard.js` — Functions take precedence over `_redirects`, so it had to go too). Its curate-and-share interaction pattern is a reference point for the planned creator profile card system (see Out of Scope below) — not currently active work. |
| `_deprecated/pack.html` | **Retired July 2026** — separate, older full creator-database + curate-and-share view (its own inline fetch of `creators-data.json`, own postcard-style share feature — unrelated to `main.js`'s `renderPackCanvas`, which is a distinct feature embedded directly in `search.html`). Never linked from live nav; its canonical `/pack` URL was already being shadowed by a stale `/pack → /postcard` redirect. `/pack` and `/pack.html` now redirect to `/`. |
| `atlas-portal/index.html` | Internal portal |
| `atlas-portal/google-form-template.html` | Internal template |
| `bluesky-creator-intelligence-v2/v3/v4/v5.html` | Version history — not public (superseded by current file) |
| `beat-tech.html`, `beat-climate.html`, `beat-finance.html` | Research pages — not public |
| `chicago-analysis.html`, `chicago-survey.html` | Internal research — not public |
| `atlas-signal-brief.html` | Internal brief — not public |
| `_deprecated/knight-brief.html` | **Retired July 2026** — internal Knight Foundation pitch brief. Not linked from anywhere live; `/knight-brief` and `/knight-brief.html` now redirect to `/`. |
| `index-exploration-V1.html` | Dev experiment — not public |
| `index-pre-homepage.html` | Pre-homepage-launch archive — do not delete until homepage is confirmed stable |
| `partners/_shell.html` | Partner page template — not public |

### Logo files (assets/images/logos/)

| File | Use |
|------|-----|
| `Journalism_Atlas_wordmark_horizontal_lockup_black.png` | Site header (white background) |
| `Journalism_Atlas_wordmark_horizontal_lockup_white.png` | Footer (black background) |
| `Journalism_Atlas_wordmark_stacked_green_white (3).png` | Hero section on search.html |
| `Journalism_Atlas_logo_acid_green.png` | Icon-only uses |

The `_lockup_` files (no "horizontal" in name) are the old equivalents — prefer the `_horizontal_lockup_` versions going forward.

---

## Out of Scope Until Further Notice

- Full postcard card system — pending James's spec (see `_deprecated/postcard.html` for the retired reference implementation's curate-and-share interaction pattern)
- Additional city lab pages beyond Chicago — same pattern as city-lab-chicago.html when ready
- Mainstream outlet layer in city-lab-chicago (Tracy Baim / Liz feedback — separate session)
- Additional ICFJ region labs (africa-lab, asia-lab, etc.) — same pattern as latin-america-lab.html
