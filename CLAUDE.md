# Atlas — Claude Code Session Guide

*Project: Independent Journalism Atlas (journalismatlas.com)*
*Owner: Justin | Design system: James (james@journalismatlas.com)*
*Last updated: October 22, 2026 (design tokens now v15, brand guide v4; v15 is rolling out in stages, see "v15 rollout status")*

**Read at session start:** This file + `WORKFLOW.md` (decision authority, "done" definition, Chat→Code handoff protocol, deploy process).

---

## Session Behavior

### Tone

- No sycophantic openers ("Great question!", "I'd be happy to help with that!", "Absolutely!")
- No restating the request back before answering
- No hedging on calls already settled by this file, `docs/design/DESIGN-TOKENS-v15.md`, or `james-design-principles.md` — state the answer, cite the rule, move on
- Flag genuine ambiguity once, briefly, then proceed with the most reasonable interpretation rather than stalling

### Required reading order

| File | When |
|------|------|
| `CLAUDE.md` (this file) | Always |
| `docs/design/DESIGN-TOKENS-v15.md` | Before any CSS/styling work |
| `docs/design/ATLAS-BRAND-GUIDE-v4.md` | Before writing any user-facing copy (voice, self-description, em dash style, database-size wording). Hanken Grotesk is retired per this guide. |
| `_reference/james-design-principles.md` | Before any visual/component decision |
| `CURRENT_STATE.md` (this repo) | Always, for site/deploy/subagent state |
| `DATA-OPS-PROTOCOL.md` | Before touching `creators-master.csv`, intake, or any pipeline script |

**Note (added July 7, 2026 — filesystem audit; path updated 2026-09-03):** `CURRENT_STATE.md` in this repo covers site/deploy/subagent state only. Data-pipeline and spidering state lives in a *different* file with the same name, now at `journalism-atlas-private/spidering/00-unsorted/CURRENT_STATE.md` (moved 2026-09-03 from the old untracked `~/Documents/Atlas Spidering/sessions/` location, which no longer exists — see "External file locations" below). Read whichever one matches the task; they are not duplicates of each other.

### Session close-out

- Update `CURRENT_STATE.md` before ending any session that changed data, pipeline state, or in-flight work — even if not explicitly asked
- Note new out-of-scope items or blockers discovered mid-session in `CURRENT_STATE.md`, not just in chat

### Role-scoped subagents

- **`ryan-dataops`** (`.claude/agents/ryan-dataops.md`, this repo) — Ryan's data-ops lane: `creators-master.csv`, `atlas-private-columns.csv`, `DATA-OPS-PROTOCOL.md`. No Bash tool (hard block on running any script, including `atlas_groups.py`/`atlas_append.py`). No git push.
- **`liz-editorial`** (`.claude/agents/liz-editorial.md`, now inside `journalism-atlas-private/spidering/.claude/agents/`, not this repo) — rebuilt July 7, 2026 with full read access (Read/Grep/Glob) across this repo, `journalism-atlas-private`, and (as of 2026-09-03) the now-merged spidering content, all in one repo. No Bash, Write, or Edit tool — read and analyze only. No Shadow Lists or rejection-notes access — both are canonical Google Sheets and no Sheets connector exists in this environment (see `CURRENT_STATE.md`).
- Scoping for these subagents is enforced by their prompt instructions and by which tools are granted (e.g. omitting Bash) — not by a filesystem ACL. Treat the "in scope" file lists as a convention the subagent is instructed to follow, not a hard sandbox.

---

## Project Overview

A vanilla JS static HTML site. No npm, no React, no bundler. All pages are single HTML files deployed to Cloudflare Pages via GitHub auto-deploy. Data lives in `assets/data/` as JSON. The only build step is `build-dist.sh`, a copy-only allowlist that publishes just the site files (see Deploy).

**Stack:** HTML + CSS + Vanilla JS. CSS custom properties for design tokens. No preprocessors. D3 v7 is present for specific visualizations but is not the general rendering approach — most page UI is vanilla JS.

**Deploy:** Push to GitHub → Cloudflare auto-deploys. Justin pushes via GitHub Desktop (not CLI). Cloudflare runs `sh build-dist.sh` and publishes only `dist/`. Anything not listed in `build-dist.sh` (docs, scripts, `pipeline/`, `.md`, `.py`, the master CSV, snapshots, `_deprecated/`) is never public. **If you add a new top-level folder, page type, or fetched data file, add it to `build-dist.sh` or it will 404 live.**

---

## Design System

All visual implementation references `docs/design/DESIGN-TOKENS-v15.md` as the single source of truth (v14 is archived in `docs/design/archive/`). Brand voice and strategy: `docs/design/ATLAS-BRAND-GUIDE-v4.md`. The CSS implementation of the tokens lives in `assets/css/variables.css`, the canonical token file, loaded before all other stylesheets.

**v15 rollout status.** v15 is being applied in stages, scoped in `docs/design/v15-discovery/V15-SCOPE-BUCKETS.md`. The rules below describe the target. Until a stage has shipped, live pages can still show the old look (for example Acid-at-rest buttons, pill tags and DM Mono/JetBrains Mono labels). When a rule and a page disagree, the rule wins for new work; don't "fix" old pages outside the stage being worked.

**Built in Session 2 (Oct 23, 2026; committed locally, not yet pushed; details in `docs/design/v15-session-2/V15-SESSION-2-REPORT.md`):** `assets/css/components.css` (`.btn--primary`, `.btn--secondary`, `.btn-icon`, `.link-instruction`, `.link-body`, global focus rings, `.on-dark` surfaces), `components.js` (selected ARIA), header nav states with `aria-current`, white footer links, report "Jump to" restyle. Buttons now rest gray/outlined and turn Acid on hover; the live site still shows the old look until that push.

**Shipped so far:** Neutral gray scale on the public pages (role variables repointed; Cool hexes in page chrome replaced by role variables; Cool kept in graphics). Weights 800 and 900 retired on the public pages (700 instead; the D3 text in `assets/js/main.js` and the self-contained `teamdmv` page still use them).

**Do not infer or improvise colors, type sizes, spacing, or component states — look them up.**

**Designer's principles:** James Bareham's 15 web design principles live at `_reference/james-design-principles.md`. Read this before making any structural or layout decisions. Key principles that come up constantly: The Explanation Principle (every module needs a narrative entry point), The Surface Hierarchy Principle (dark = stage, light = workspace), The Placeholder Principle (no empty states in public-facing design), and The Tool Principle (every element must serve the user's task).

### Non-negotiable rules (memorize these)

- **Green means interaction (docs/design/DESIGN-TOKENS-v15.md § Component States).** Buttons, tags, instruction links and nav rest in monotones. Green appears on hover, press and selected. The only things that rest in green are body links on light surfaces (Dark Olive, underlined) and eyebrows on dark surfaces (Acid allowed).
  - **Acid `#ceff00`:** hover, press and selected. **Fill only on light surfaces** (black text on top); fills, text, underlines and icons on dark. Never a success signal. No per-composition limit.
  - **Lime `#97d600`:** keyboard focus ring on dark surfaces only. Not a hover color. Not used on light.
  - **Dark Olive `#5d7400`:** the green for text, icons, underlines and thin strokes on light surfaces (hover and selected text, current nav item, body links, focus ring). Never a fill, button background or hover fill. Not used on dark (4.0:1 on black).
  - **Focus ring follows the surface:** Lime on dark, Dark Olive on light; `2px`, offset `2px`.
  - **Buttons:** two styles, both 44px, 6px radius, Inter 600 15px, sentence case. Primary: step-6 fill, white text, step-5 outline (step-4 on dark); selected = white. Secondary (filters, repeated options): outline only; selected = black (white on dark). Both turn Acid on hover and press.
  - **Links:** instruction links are Source Code Pro 500 13px caps ending in ` →` (step 6 → Dark Olive underlined; white → Acid underlined). Body links are Dark Olive underlined on light (hover black) and white underlined on dark (hover Acid). Variables `--color-link` / `--color-link-on-dark`.
  - **Tags:** Source Code Pro 500 12px caps, 0.08em, fill or outline never both, never clickable, no hover. Beat tags carry color only on an 8px dot from `ATLAS_VIZ_COLORS`.
  - **No color coding by section or content type.**
  - **Migration state:** primitives `--color-acid` / `--color-lime` / `--color-olive` exist and role variables point at them. `--color-hover` still resolves to Lime until the green-model stage; v15 makes it an alias of Acid. Migrate each use by role; never repoint `--color-accent` in place without checking its uses.
- **Gray scales (v15):** the website uses the **Neutral** scale (`--gray-neutral-*`) for every semantic gray role, through the role variables (`--color-bg`, `--color-text`, `--color-text-secondary`, `--color-muted`, `--color-border`, `--color-text-on-dark-2`, `--color-border-on-dark`, `--color-surface`, `--color-surface-dark`, `--color-heading`). Use the role variable, not a hex. **Cool** (`--gray-cool-*`) is for graphics only (charts, infographics, illustrations); an embedded graphic counts as its own surface. Don't mix scales on one surface.
- **Site header = `#ffffff` (default, matches the live site) or `#000000`** (a per-page choice). Logo must match (`..._blk_web.svg` on white, `..._wht_web.svg` on black); nav text follows the header (step 1 on black; step 6 or 8 on white); hover is underlined; selected (current page) is Dark Olive on white or Acid on black with a 2px underline, offset 8px. Anything docked to the header (the report "Jump to" sub-nav) uses the same background. The black theme is wired: `header.js` switches the logo with `<html data-header-theme="black">` (default white). Pages do not request it yet.
- **Body copy minimum 16px.** Small (13px) is the floor for UI text. All-caps UI labels are Source Code Pro 500: **Label 13px** (eyebrows, instruction links, 0.08–0.12em) and **Tag 12px** (tags, badges, card meta lines, 0.08em). 12px Source Code Pro is the only size allowed below 13px.
- **Material Symbols Outlined only.** Filled only for active toggle/action icons (save, follow, bookmark). Navigation and section icons stay outlined at every state.
- **4px base spacing unit:** xs 4 / sm 8 / md 16 / lg 24 / xl 32 / 2xl 48 / 3xl 96.
- **Font weights: 400 / 500 / 600 / 700.** 500 is for Source Code Pro labels and tags only; 600 for H3/card titles and buttons. 800 and 900 are retired.
- **Border radius: 6px for everything rectangular** (cards, buttons, inputs, tags, badges). Pills are retired. `50%` only for photos, avatars and status dots.

### CSS token architecture

```
assets/css/variables.css   ← THE canonical token file (implements docs/design/DESIGN-TOKENS-v15.md)
assets/css/header.css      ← Shared site header + footer wordmark styles (all pages)
assets/css/main.css        ← Used by search.html
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
- Injects Inter, Source Code Pro 500 (v15 labels; not used yet) and Material Symbols fonts if not already loaded

`header.js` is loaded as the **first** `<script>` tag in `<body>` on every page. Do not duplicate nav HTML manually — edit `header.js` to change nav content.

Pages with inline `<style>` blocks (partners/*.html, city-lab-chicago.html, latin-america-lab.html) link variables.css before their inline block, and header.css after it (before `</head>`).

### How to use docs/design/DESIGN-TOKENS-v15.md in a session

Before writing any CSS or styling-related code, read the relevant section of `docs/design/DESIGN-TOKENS-v15.md`. Reference it explicitly in comments when implementing tokens:

```css
/* Interaction fill: hover, press, selected (fill only on light surfaces). docs/design/DESIGN-TOKENS-v15.md § Semantic Color Assignments */
--color-accent: var(--color-acid);
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
| `journalism-atlas-private/` (github.com/bankonjustin/journalism-atlas-private) | Editorial/reference docs (`ATLAS-EDITORIAL-STANDARDS`, `REJECTION_GUIDE`, `DATA-ROADMAP`), the live `atlas-private-columns.csv`, dated master-CSV snapshots, Ryan's `runryan/`, and (as of 2026-09-03) `spidering/` — moved in from `~/Documents/Atlas Spidering/`, see below | Git (private) — access: Justin, Ryan, Liz, James |
| `~/Downloads/` | Still holds a large accumulation of briefs, historical Mega-Database files, and design assets going back to January 2026 (categorized, not yet individually triaged — see open item below). A maintained *mirror* of `ATLAS-EDITORIAL-STANDARDS` also lives here (`ATLAS-EDITORIAL-STANDARDS-v1_4.md`) solely for `liz-editorial.md`'s hardcoded path — see `DATA-OPS-PROTOCOL.md` § "Reference doc locations." | Not tracked |

**Corrections to prior claims:** (1) Earlier docs assumed `ATLAS-EDITORIAL-STANDARDS.md` lived in this repo's `_reference/` folder — it never has. (2) As of the July 7 filesystem audit, this doc said the private repo was "proposed, not yet built" — it's since been approved and built; that recommendation is superseded by the row above.

**Still open:** `~/Downloads/` has 150+ Atlas-related files beyond what's been migrated so far, categorized at the bucket level but not individually triaged (Mega-Database, historical briefs, business/legal docs, older private-columns/master-CSV snapshots predating the private repo). A follow-up pass is expected.

`journalism-atlas/spidering/` must stay empty — confirmed empty as of this audit. Nothing spidering-related belongs there; see `journalism-atlas-private/spidering/SPIDERING_ALIGNMENT_GUIDE.md` (path updated 2026-09-03 — spidering is no longer at `~/Documents/Atlas Spidering/`, and that location no longer exists on disk).

---

## Creator Count Convention

**Never type a creator count.** The count and its as-of date are generated, and only from `creators-master.csv`.

- **Source of truth:** `node convert.js` writes `assets/data/creators-data.json` and `assets/data/site-stats.json` (`totalCreators`, `totalCreatorsLabel`, `asOf`, `asOfLabel`). `asOf` is the date the master last changed (last commit touching it, or file mtime while it has uncommitted edits). Re-run `convert.js` after every master change and commit `site-stats.json` with it.
- **Visible UI text:** `<span class="js-creator-count">{{CREATOR_COUNT}}</span>`. The runtime script replaces the span with the live count; the token is the no-JS fallback.
- **Meta/OG/Twitter tags, partner footers, any static prose:** write the token `{{CREATOR_COUNT}}` (and `{{COUNT_AS_OF}}` where a date belongs). `build-dist.sh` fills both from `site-stats.json` in `dist/` only, and fails the build if a token is left unresolved. Do not write rounded forms (`1,700+`, `1,800+`, `2,400+`) and do not paste an exact number. Source files keep the tokens, so local `serve` shows them in meta tags and no-JS text; that is expected.
- **Cluster card counts on index.html:** computed dynamically from `allCreators` by `_updateClusterCards()`; do not hardcode.
- **Pulse snapshots** (`PULSE_SNAPSHOT_*`, `pulse.html` JSON) are regenerated by the Pulse pipeline; never hand-edit them.
- **Rejected slugs:** `convert.js` runs `scripts/check-rejections.js` first and refuses to build if any slug in `journalism-atlas-private/data/rejections.csv` is in the master without a row in `journalism-atlas-private/data/readmits.csv` (`slug,date,decided_by,note`, dated after the rejection). Fix by moving the row to the hold list or adding the re-admit note. Do not bypass with `--skip-rejection-check` unless Justin says so.
- **Old figures (1,718, 1,800+, 2,432 and similar) are history, not rules.** Do not copy them from older docs or earlier pages.

---

## Homepage names come from data

**Status (Oct 26, 2026):** the homepage is temporarily back on its previous hand-typed featured, preview and exemplar cards (`index.html` restored to its pre-`3ed93d8` state), because no creator has `Featured` set yet and those slots would render empty. The Featured column and `convert.js` support stay in place. Once Ryan has set `Featured` values, re-apply the data-driven homepage from that commit and delete this note. Justin chose to keep those cards (option B) with the nine names that are not in the registry removed (Kara Swisher, Greg Sargent, Block Club Chicago, The Oaklandside, Signal Cleveland, Zeynep Tufekci, The Athletic, Richard Deitsch, Matt Levine); the Local News card therefore has no exemplars until Ryan sets `Featured`. Do not add names back by hand.

No creator names are typed on `index.html`. The featured rotation, the database-preview cards and the cluster-card exemplars render from the master's trailing `Featured` column (emitted as `featured` in `creators-data.json`). Ryan sets it: `home` puts a creator in the featured rotation and preview cards; `cluster` lets them appear as an exemplar on their cluster card (3 max per card). Tokens combine with `|` or `,`. With nothing set, those slots are hidden. Do not hand-type names or blurbs into the page, and do not set `Featured` yourself. `atlas_normalize.py` only prints a note for the extra column, but check that any script that rewrites the master keeps it.

---

## Key Constraints

- **Single deployable HTML file** — no bundler or npm, no external dependencies beyond CDNs (the only build step is the `build-dist.sh` copy allowlist)
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
| `partners/iij.html` | Institute for Independent Journalists (IIJ) picks — built Aug 1, 2026. Published and reachable by direct URL; unlinked from nav/`partners/index.html`/`_redirects` pending confirmation of partnership next steps. Not yet documented elsewhere prior to this entry. | 122 | `variables.css` + inline `<style>` |
| `city-lab-chicago.html` | Chicago journalism ecosystem | 245+ | Inline `<style>` + inlined data |
| `preview/nodes-and-networks-f348eb08/index.html` | Preview of the ASU/Knight paper "Nodes and Networks" (v938). Unlisted, `noindex`, `/preview/` disallowed in `robots.txt`. **Generated. Don't hand-edit it.** Rebuild it with `make -C tools/preview-build preview DOCX=...` (see `tools/preview-build/preview_build_ledger.md`). Figures are inlined SVG from `paper-one-band-dataset/figures_v22/html/`. Replaced `research/nodes-and-networks.html` (retired Oct 15, 2026, now in `_deprecated/`; the old URL 301s here). | — | Inline `<style>` (v16 chrome) |
| `city-lab-dc-v3.html` | DC/DMV journalism ecosystem — "Who Covers Washington Now" | ~350 | Inline `<style>` + inlined data |
| `latin-america-lab.html` | Latin America & Caribbean creator lab (ICFJ) | — | Inline `<style>` + inlined data |
| `partners/nj-lab.html` (a near-identical duplicate, `partners/njlab.html`, is also live) | NJ State Lab — CCM partnership. 51 creators (CCM NJ Influencer Study), 6 sections, filterable grid, CSS vizzes. | 51 | Inline `<style>` + inlined data |
| `bluesky-creator-intelligence.html` | Bluesky Creator Intelligence — AT Protocol ecosystem map. 552+ creators (live from `assets/data/bluesky-creators.json`). Beat cluster map (live-computed), creator index, methodology band, coverage gaps + suggest-a-creator. Canonical URL: `/bluesky-creator-intelligence`. **Nav inclusion: flag for James — not added to header.js this session.** | 552+ (live JSON) | `variables.css` + inline `<style>` + `header.css` |

Pages should link `variables.css` first and avoid redefining canonical tokens inline. As of Oct 22, 2026 a few pages still carry an inline `:root` alias block, and some pages (`teamdmv`, `watershed-preview`, the nodes-and-networks preview) have their own palette; see `docs/design/v15-discovery/V15-DISCOVERY-REPORT.md` Track B.

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
| `partners/_shell.html` | Partner page template — not public |

### Logo files (assets/images/logos/)

| File | Use |
|------|-----|
| `Atlas_logo_lockup_horizontal_blk_web.svg` | Site header on a white header (default). Replaced `Journalism_Atlas_wordmark_horizontal_lockup_black.svg` (byte-identical artwork, left in the folder, now unreferenced) |
| `Atlas_logo_lockup_horizontal_wht_web.svg` | Site header on a black header (`data-header-theme="black"`); same geometry, `fill="#fff"` |
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
