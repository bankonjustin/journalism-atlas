# V15 Session 1 Report: Foundations

*Oct 22, 2026. Eight local commits on `main` (`b1827fb..9e43681`). **Nothing was pushed.** Screenshots are under `docs/design/v15-session-1/screenshots/` (gitignored): `before/` (untouched tree), `before2/` (second run, for the noise mask), `c4/`, `c5/`, `c6/`, `c7/`, `c7b/`, `c8/`.*

## Step 0 and the auto-push check

- **Working tree:** branch `main`, clean apart from untracked `docs/design/` (discovery files).
- **Files present:** `V15-SCOPE-BUCKETS.md` and all 14 baseline screenshots.
- **Playwright and server:** re-shot `partners/ahp` and `about-this-project` at 1440 and compared with the discovery baseline: **0 pixels different**. (The homepage, Pulse and Research baselines differ from my "before" set only where they animate: hero canvas, Pulse, carousel.)
- **Buckets file vs this brief:** the Session 1 items match the commit plan. Differences, none blocking: (1) the buckets' G11 retired weight 800 only; I also found weight **900** (see C8, and a correction to the discovery report below); (2) the brief says 11 internal pages for C3, the discovery text lists 14 as indexable (see C3).
- **Auto-push check: nothing found that can push or deploy.** `.git/hooks/` holds only the `.sample` files; the git config has no hooks, aliases or auto-push settings (only `credential.helper=osxkeychain`); `.claude/` in the repo has only `agents/ryan-dataops.md` and `launch.json`; `~/.claude/settings.json` has two unrelated `python3 pulse_daily_spike.py` permissions and no hooks; no crontab, no LaunchAgent for this repo; no script or workflow in the repo runs `git commit` or `git push`; the one scheduled task (`wire-refresh-gate-w-oct27`) is a report-only Switchboard job. I could not find what caused the past auto-push logged in `CURRENT_STATE.md` (6aa80a0); it isn't configured in anything I can read. I ran no remote git commands.

## Commits

| # | Hash | Message | Files | Pages affected | Visible effect |
|---|---|---|---|---|---|
| C1 | `ab86f21` | v15: repo hygiene | 37 (`.gitignore`, `docs/design/`: 20 new files incl. v15, brand v4, the discovery reports and inventories, plus the v14 move, `WORKFLOW.md`, `START-HERE.md`, `CLAUDE.md`, 12 CSS/JS/HTML comment edits) | none | **none** (comment text only) |
| C2 | `e11330c` | CLAUDE.md design section to v15 | 1 | none | none |
| C3 | `5e22122` | noindex on 11 internal pages | 11 | 11 internal | none |
| C4 | `0de5d63` | link variables.css on mobile.html | 1 (3 more held back) | `mobile` | **none** (pixel-identical at 1440 and 390) |
| C5 | `c092206` | add missing v15 variables | 1 | none | none (verified identical on 2 pages) |
| C6 | `b70fd8a` | load Source Code Pro 500 site-wide | 3 (`header.js`, `footer.js`, `CLAUDE.md`) | 37 of 40 public pages | **none**, with one tiny exception on `city-lab-dc-v3` (below) |
| C7 | `7c00490` | repoint site grays to Neutral scale | 39 | 40 public pages scanned, 37 files changed | Page backgrounds `#efeff4` → `#efefef`; grays shift ≤7 per channel |
| C8 | `9e43681` | retire font weight 800 and 900 | 25 | 4 pages change look | Big headings on 4 pages are slightly lighter |

### C1: repo hygiene
- `.gitignore`: both screenshot folders. (Note: the brief says everything in the repo is served by Cloudflare; actually `build-dist.sh` is an allowlist that doesn't copy `docs/`, so docs would not deploy. The ignore is still right for repo size.)
- `DESIGN-TOKENS-v15.md` and `ATLAS-BRAND-GUIDE-v4.md` copied from Downloads to `docs/design/`; `DESIGN-TOKENS-v14.md` moved with `git mv` to `docs/design/archive/`.
- References repointed (filename text only): `CLAUDE.md`, `WORKFLOW.md`, `START-HERE.md` (the "brand guide missing" item), and comments in `variables.css`, `main.css`, `header.css`, `header.js`, `index`, `contact`, `latin-america-lab`, `co-ops`, `partners/nj-lab`, `njlab`, `njlab copy`, `preview/smartnews`. I verified the diff outside those words is empty.
- **Left as is on purpose:** the history logs `CURRENT_STATE.md`, `CSS_AUDIT.md`, `LEAVE-OFF-LOG.md`, `docs/V12…V14-*`, `docs/briefs/`, `_deprecated/` and `CLAUDE copy.md` (they record what was true at the time); `ATLAS-BRAND-GUIDE-v3.md` stays at the repo root (not in the plan; archive it when convenient); `WORKFLOW.md` still has `james@happicamp.com` (the contact fix was only in CLAUDE.md's section).
- The discovery reports and inventories (3.7MB of CSV/MD, no screenshots) are committed here.

### C2: CLAUDE.md design section
Applied Appendix B, with real text instead of the sketch, plus: a "v15 rollout status" paragraph (so nobody reads the rules as already live), `main.css` and nj-lab inventory fixes, the sentence "all pages swept" replaced, and a corrected `--color-accent` example. Diff:

```diff
diff --git a/CLAUDE.md b/CLAUDE.md
index b636565..7f82f7a 100644
--- a/CLAUDE.md
+++ b/CLAUDE.md
@@ -1,8 +1,8 @@
 # Atlas — Claude Code Session Guide
 
 *Project: Independent Journalism Atlas (journalismatlas.com)*
-*Owner: Justin | Design system: James (james@happicamp.com)*
-*Last updated: October 6, 2026 (design tokens now v14)*
+*Owner: Justin | Design system: James (james@journalismatlas.com)*
+*Last updated: October 22, 2026 (design tokens now v15, brand guide v4; v15 is rolling out in stages, see "v15 rollout status")*
 
 **Read at session start:** This file + `WORKFLOW.md` (decision authority, "done" definition, Chat→Code handoff protocol, deploy process).
 
@@ -55,7 +55,9 @@ A vanilla JS static HTML site. No npm, no React, no bundler. All pages are singl
 
 ## Design System
 
-All visual implementation references `docs/design/DESIGN-TOKENS-v15.md` at the project root as the single source of truth. Its CSS implementation lives in `assets/css/variables.css` — the canonical token file, loaded before all other stylesheets.
+All visual implementation references `docs/design/DESIGN-TOKENS-v15.md` as the single source of truth (v14 is archived in `docs/design/archive/`). Brand voice and strategy: `docs/design/ATLAS-BRAND-GUIDE-v4.md`. The CSS implementation of the tokens lives in `assets/css/variables.css`, the canonical token file, loaded before all other stylesheets.
+
+**v15 rollout status.** v15 is being applied in stages, scoped in `docs/design/v15-discovery/V15-SCOPE-BUCKETS.md`. The rules below describe the target. Until a stage has shipped, live pages can still show the old look (for example Acid-at-rest buttons, pill tags and DM Mono/JetBrains Mono labels). When a rule and a page disagree, the rule wins for new work; don't "fix" old pages outside the stage being worked.
 
 **Do not infer or improvise colors, type sizes, spacing, or component states — look them up.**
 
@@ -63,29 +65,30 @@ All visual implementation references `docs/design/DESIGN-TOKENS-v15.md` at the p
 
 ### Non-negotiable rules (memorize these)
 
-- **Greens by surface (docs/design/DESIGN-TOKENS-v15.md § Greens by Surface):**
-  - **Acid `#ceff00` and Lime `#97d600` on LIGHT surfaces = fill only**, with black or step-6 text on top. Never text, icons or thin strokes on light (1.2:1 and 1.8:1 on white).
-  - **On DARK surfaces** acid and lime are free within their roles: acid for CTAs and active states (text, icons, strokes, fills), lime for hover and the focus ring.
-  - **Dark Olive `#5d7400` on LIGHT surfaces = the green for text, icons and thin strokes** (active nav item, selected icon, link-style CTA, hover *text*, focus ring). Never a fill, button background or hover fill. Not used on dark surfaces (4.0:1 on black).
-  - **Focus ring follows the surface:** lime on dark, Dark Olive on light.
-  - One acid moment per composition; olive marking the active state on a light surface counts as that moment.
-  - Not canon: the older "acid on dark only / lime on light only" rule. v13 replaces it.
-  - **Primary CTA (v14):** acid fill at rest and active, lime fill on hover, black text throughout; focus ring olive on light, lime on dark; disabled step 4 (light) / step 5 fill + step 3 text (dark).
-  - **Inline links (v14):** olive + underlined on light (hover step 8); white + underlined on dark (hover lime). Variables `--color-link` / `--color-link-on-dark`.
-  - **In migration:** the site's `--color-accent` is still lime (its live look). Do not repoint it in place; migrate each use by role to `--color-accent` (fill), `--color-hover` (hover fill), `--color-accent-on-light` (text/icons/strokes on light), `--color-focus*`. Primitives `--color-acid` / `--color-lime` / `--color-olive`. See `docs/V13-GREENS-AUDIT-2026-10-06.md`.
-- **Site header = `#ffffff` (default, matches the live site) or `#000000`** (a per-page choice, v14). Logo must match (`..._blk_web.svg` on white, `..._wht_web.svg` on black); nav text follows the header (step 1 on black; step 6 or 8 on white); active nav is Dark Olive on white, acid on black. Anything docked to the header (the report "Jump to" sub-nav) uses the same background. The black theme is wired: `header.js` switches the logo with `<html data-header-theme="black">` (default white). Pages do not request it yet
-- **Body copy minimum 16px** — Small (13px) is the floor for all UI text. Micro (11px) for all-caps labels only (weight 500 min, letter-spacing 0.08–0.1em). Never below 13px for any readable content.
-- **Material Symbols Outlined only** — no legacy Material Icons; Filled variant reserved for active states only
-- **4px base spacing unit** — spacing scale: xs 4px / sm 8px / md 16px / lg 24px / xl 32px / 2xl 48px
-- **Font weights: 400 / 500 / 600 / 700 / 800** — 500 for Micro labels only; 600 for H3/card titles; do not introduce 900 or other weights
-- **Border radius: 6px for cards/buttons/inputs; 9999px for pills/tags**
+- **Green means interaction (docs/design/DESIGN-TOKENS-v15.md § Component States).** Buttons, tags, instruction links and nav rest in monotones. Green appears on hover, press and selected. The only things that rest in green are body links on light surfaces (Dark Olive, underlined) and eyebrows on dark surfaces (Acid allowed).
+  - **Acid `#ceff00`:** hover, press and selected. **Fill only on light surfaces** (black text on top); fills, text, underlines and icons on dark. Never a success signal. No per-composition limit.
+  - **Lime `#97d600`:** keyboard focus ring on dark surfaces only. Not a hover color. Not used on light.
+  - **Dark Olive `#5d7400`:** the green for text, icons, underlines and thin strokes on light surfaces (hover and selected text, current nav item, body links, focus ring). Never a fill, button background or hover fill. Not used on dark (4.0:1 on black).
+  - **Focus ring follows the surface:** Lime on dark, Dark Olive on light; `2px`, offset `2px`.
+  - **Buttons:** two styles, both 44px, 6px radius, Inter 600 15px, sentence case. Primary: step-6 fill, white text, step-5 outline (step-4 on dark); selected = white. Secondary (filters, repeated options): outline only; selected = black (white on dark). Both turn Acid on hover and press.
+  - **Links:** instruction links are Source Code Pro 500 13px caps ending in ` →` (step 6 → Dark Olive underlined; white → Acid underlined). Body links are Dark Olive underlined on light (hover black) and white underlined on dark (hover Acid). Variables `--color-link` / `--color-link-on-dark`.
+  - **Tags:** Source Code Pro 500 12px caps, 0.08em, fill or outline never both, never clickable, no hover. Beat tags carry color only on an 8px dot from `ATLAS_VIZ_COLORS`.
+  - **No color coding by section or content type.**
+  - **Migration state:** primitives `--color-acid` / `--color-lime` / `--color-olive` exist and role variables point at them. `--color-hover` still resolves to Lime until the green-model stage; v15 makes it an alias of Acid. Migrate each use by role; never repoint `--color-accent` in place without checking its uses.
+- **Gray scales (v15):** the website uses the **Neutral** scale (`--gray-neutral-*`) for every semantic gray role, through the role variables (`--color-bg`, `--color-text`, `--color-text-secondary`, `--color-muted`, `--color-border`, `--color-text-on-dark-2`, `--color-border-on-dark`, `--color-surface`, `--color-surface-dark`, `--color-heading`). Use the role variable, not a hex. **Cool** (`--gray-cool-*`) is for graphics only (charts, infographics, illustrations); an embedded graphic counts as its own surface. Don't mix scales on one surface.
+- **Site header = `#ffffff` (default, matches the live site) or `#000000`** (a per-page choice). Logo must match (`..._blk_web.svg` on white, `..._wht_web.svg` on black); nav text follows the header (step 1 on black; step 6 or 8 on white); hover is underlined; selected (current page) is Dark Olive on white or Acid on black with a 2px underline, offset 8px. Anything docked to the header (the report "Jump to" sub-nav) uses the same background. The black theme is wired: `header.js` switches the logo with `<html data-header-theme="black">` (default white). Pages do not request it yet.
+- **Body copy minimum 16px.** Small (13px) is the floor for UI text. All-caps UI labels are Source Code Pro 500: **Label 13px** (eyebrows, instruction links, 0.08–0.12em) and **Tag 12px** (tags, badges, card meta lines, 0.08em). 12px Source Code Pro is the only size allowed below 13px.
+- **Material Symbols Outlined only.** Filled only for active toggle/action icons (save, follow, bookmark). Navigation and section icons stay outlined at every state.
+- **4px base spacing unit:** xs 4 / sm 8 / md 16 / lg 24 / xl 32 / 2xl 48 / 3xl 96.
+- **Font weights: 400 / 500 / 600 / 700.** 500 is for Source Code Pro labels and tags only; 600 for H3/card titles and buttons. 800 and 900 are retired.
+- **Border radius: 6px for everything rectangular** (cards, buttons, inputs, tags, badges). Pills are retired. `50%` only for photos, avatars and status dots.
 
 ### CSS token architecture
 
 ```
 assets/css/variables.css   ← THE canonical token file (implements docs/design/DESIGN-TOKENS-v15.md)
 assets/css/header.css      ← Shared site header + footer wordmark styles (all pages)
-assets/css/main.css        ← Primary stylesheet for index.html only
+assets/css/main.css        ← Used by search.html (and the archived index-pre-homepage.html)
 assets/css/animations.css  ← Standalone animation keyframes
 ```
 
@@ -113,8 +116,8 @@ Pages with inline `<style>` blocks (partners/*.html, city-lab-chicago.html, lati
 Before writing any CSS or styling-related code, read the relevant section of `docs/design/DESIGN-TOKENS-v15.md`. Reference it explicitly in comments when implementing tokens:
 
 ```css
-/* Primary accent — light mode only. docs/design/DESIGN-TOKENS-v15.md § Semantic Color Assignments */
---color-accent: #97d600;
+/* Interaction fill: hover, press, selected (fill only on light surfaces). docs/design/DESIGN-TOKENS-v15.md § Semantic Color Assignments */
+--color-accent: var(--color-acid);
 ```
 
 ### What requires James's sign-off before implementing
@@ -239,10 +242,10 @@ Four locations now exist. Don't assume file paths from older briefs still hold 
 | `preview/nodes-and-networks-f348eb08/index.html` | Preview of the ASU/Knight paper "Nodes and Networks" (v938). Unlisted, `noindex`, `/preview/` disallowed in `robots.txt`. **Generated. Don't hand-edit it.** Rebuild it with `make -C tools/preview-build preview DOCX=...` (see `tools/preview-build/preview_build_ledger.md`). Figures are inlined SVG from `paper-one-band-dataset/figures_v22/html/`. Replaced `research/nodes-and-networks.html` (retired Oct 15, 2026, now in `_deprecated/`; the old URL 301s here). | — | Inline `<style>` (v16 chrome) |
 | `city-lab-dc-v3.html` | DC/DMV journalism ecosystem — "Who Covers Washington Now" | ~350 | Inline `<style>` + inlined data |
 | `latin-america-lab.html` | Latin America & Caribbean creator lab (ICFJ) | — | Inline `<style>` + inlined data |
-| `nj-lab.html` | NJ State Lab — CCM partnership. 51 creators (CCM NJ Influencer Study), 6 sections, filterable grid, CSS vizzes. | 51 | Inline `<style>` + inlined data |
+| `partners/nj-lab.html` (a near-identical duplicate, `partners/njlab.html`, is also live) | NJ State Lab — CCM partnership. 51 creators (CCM NJ Influencer Study), 6 sections, filterable grid, CSS vizzes. | 51 | Inline `<style>` + inlined data |
 | `bluesky-creator-intelligence.html` | Bluesky Creator Intelligence — AT Protocol ecosystem map. 552+ creators (live from `assets/data/bluesky-creators.json`). Beat cluster map (live-computed), creator index, methodology band, coverage gaps + suggest-a-creator. Canonical URL: `/bluesky-creator-intelligence`. **Nav inclusion: flag for James — not added to header.js this session.** | 552+ (live JSON) | `variables.css` + inline `<style>` + `header.css` |
 
-All pages above have been swept to the design token system (variables.css linked first, slim `:root` alias block, no canonical token redefinitions inline). Design sweep completed April 2026.
+Pages should link `variables.css` first and avoid redefining canonical tokens inline. As of Oct 22, 2026 a few pages still carry an inline `:root` alias block, and some pages (`teamdmv`, `watershed-preview`, the nodes-and-networks preview) have their own palette; see `docs/design/v15-discovery/V15-DISCOVERY-REPORT.md` Track B.
 
 ### Internal / dev-only pages (not public-facing — skip OG tags, skip in bulk operations)
 
@@ -259,7 +262,6 @@ All pages above have been swept to the design token system (variables.css linked
 | `chicago-analysis.html`, `chicago-survey.html` | Internal research — not public |
 | `atlas-signal-brief.html` | Internal brief — not public |
 | `_deprecated/knight-brief.html` | **Retired July 2026** — internal Knight Foundation pitch brief. Not linked from anywhere live; `/knight-brief` and `/knight-brief.html` now redirect to `/`. |
-| `index-exploration-V1.html` | Dev experiment — not public |
 | `index-pre-homepage.html` | Pre-homepage-launch archive — do not delete until homepage is confirmed stable |
 | `partners/_shell.html` | Partner page template — not public |
 
```

*(The `header.js` line and the "Shipped so far" paragraph were added in C6, C7 and C8.)*

### C3: noindex (11 pages)
`atlas-portal/index.html`, `atlas-portal/google-form-template.html`, `atlas-signal-brief.html`, `atlas_pulse_intelligence.html`, `atlas_wire_intelligence.html`, `atlas_wire_review.html`, `beat-climate.html`, `beat-finance.html`, `beat-tech.html`, `chicago-analysis.html`, `chicago-survey.html`. One `<meta name="robots" content="noindex">` line each, after the charset tag; nothing else changed.
**Not done, still indexable (3):** `partners/_shell.html` (the partner template: copying it to a new partner page would carry the tag along, so I left it), `partners/njlab copy.html` (a stray duplicate), `index-pre-homepage.html` ("do not delete until homepage is confirmed stable"). Say the word and I'll add them, except the shell.

### C4: broken `variables.css` loads (**3 of 4 pages held back**)
| Page | Change tried | Before → after | Status |
|---|---|---|---|
| `mobile.html` | add `<link rel="stylesheet" href="/assets/css/variables.css">` before its `<style>` | 1440 and 390: identical | **committed** |
| `lists.html` | add the same link | Page body identical; **footer 288px → 352px tall** (+64px at 1440, +184px at 390). Cause: the shared footer rules in `header.css` use `var(--space-sm/md)`, which were undefined on this page, so footer spacing had collapsed | **held back** (layout shift) |
| `partners/nj-lab.html`, `partners/njlab.html` | `assets/css/variables.css` → `/assets/css/variables.css` | Same footer +64px/+184px, **and the header turns white** (before, `--white` was undefined so the header was transparent over the gray page, with the 72px empty band above it unchanged) | **held back** |

The three held-back changes are saved as `docs/design/v15-session-1/C4-held-back.patch` (apply with `git apply`). I think they are fixes: the pages would look like every other page. I held them back because the brief says not to commit pages that shift in layout. **If you want them,** apply the patch and commit; C7 already handles these three pages either way (they use `var(--role, neutral)` fallbacks, so they're Neutral without the link).
`partners/njlab copy.html` has the same broken link; it's an internal stray copy, not in the plan, left alone.

### C5: missing variables
Added `--color-surface-dark` (step 7), `--color-button` (6), `--color-button-outline` (5), `--color-button-outline-on-dark` (4), `--color-button-2-outline` (6). Every other variable in v15's block already existed, including `--color-focus-on-light`. `--color-accent` and `--color-hover` untouched; none of the new ones is used. (`--space-3xl` is 64px in `variables.css` vs 96px in v15; that's a changed value, not a missing variable, so I left it.)

### C6: Source Code Pro 500
`header.js` adds `family=Source+Code+Pro:wght@500`. **Verified in Chromium: `document.fonts.load('500 13px "Source Code Pro"')` succeeds on 37 of 40 public pages.** The 3 that don't run `header.js` are `preview/nodes-and-networks…`, `teamdmv` and `watershed-preview` (self-contained pages; unchanged).
**One thing I got wrong and fixed before pushing:** my first version made `footer.js` skip its own 400 load (it skips if *any* Source Code Pro link exists), so footer text rendered in the 500 face on all pages. Caught by the pixel check (footer differed on contact, about, pulse); `footer.js`'s check now looks for the 400 request specifically, and those pages are pixel-identical again. The 400 load itself is untouched.
**One tiny remaining side effect:** on `city-lab-dc-v3`, the footer tagline inherits `font-weight: 900` from the page. With only a 400 face it was faux-bold on 400; now it's faux-bold on the 500 face (702 px, slightly heavier). Goes away when that page's footer weight is cleaned up.

### C7: Neutral scale (one commit)
Three parts, in one commit:
1. `variables.css`: 17 role/alias definitions now point at `--gray-neutral-*` (`--color-bg/-text/-text-secondary/-muted/-border/-border-hover/-surface/-heading/-text-on-dark-2/-border-on-dark/-bg-dark/-text-dark/-muted-dark`, `--light-gray`, `--dark-gray`, `--color-light-gray`, `--color-dark-gray`). Both scales remain defined.
2. Cool hexes in page chrome replaced by role variables: **373 role replacements, 19 fallback hexes inside existing `var(--x, #hex)`, 22 hex mentions in comments** (comment text only), across 37 files. Mapping by property: background `#efeff4` → `var(--color-bg)` (including the homepage, Pulse, Research, nj-lab and partner page backgrounds, `--page-bg`, `--light`); text `#303036` → `var(--color-text)`, `#5e5e64` → `--color-text-secondary`, `#c6c6cd` text → `--color-text-on-dark-2`, border `#c6c6cd` → `--color-border`, dark-surface background `#303036` → `--color-bg-dark`. `rgba()` Cool tints use `color-mix(in srgb, var(--role) N%, transparent)`.
   - **Where no role exists** I used the scale variable instead of a hex: `var(--gray-neutral-3/5/7)` in a few spots.
   - **Pages without `variables.css` (lists, nj-lab, njlab) and `header.css`** use `var(--role, <neutral hex>)`, so they go Neutral without needing the file.
   - **Extension to the plan, same concern:** 100 direct `var(--gray-cool-N)` uses in chrome (disabled-button states on ~25 pages, `main.css`, `header.css`'s black theme) were moved to `var(--gray-neutral-N)`, the same step. Otherwise those states would have stayed Cool on a Neutral page.
3. **5 pinned aliases unpinned:** `--light-gray`/`--dark-gray` lines (10 lines) deleted from `about-this-project`, `advisory`, `how-we-did-this`, `who-we-are`, `mobile`. (`lists`' `--dark-gray: #303036` became a `var()` fallback instead, because it has no `variables.css`.)

**Re-run of the Track C Cool-hex search** over the 40 public pages and shared assets (hex and `rgba()` forms): **29 hits remain, 0 chrome:**
- *Graphics, left on purpose (10):* `partners/nj-lab.html` and `njlab.html`, 4 each, L228/241/283/293: `.viz-title`, `.bar-label`, `.stacked-legend-item`, `.legend-pct` (chart labels, `rgba(239,239,244,…)` and `#efeff4`). **These are the ambiguous ones**: CSS-built bar-chart labels on the dark panel; I treated them as graphics. `pulse.html` L2665 and L2668, heatmap cell text color in JS (graphics).
- *Excluded page (19):* `watershed-preview-uhh7gdyn/index.html`: self-contained, defines its own Cool scale and role copies in one line, doesn't load `variables.css`. Needs its own call.
- Not counted: the Cool scale *definitions* in `variables.css` (stay, per v15).

**Before/after, all 40 public pages** (screenshots at 1440 and 390; "max Δ" is the largest per-channel difference outside animated regions; the expected change is ≤7; threshold for a flag was 8):

| Page | 1440 | 390 | Status | Note |
|---|---|---|---|---|
| `about-this-project.html` | max Δ 7, 31.17% px changed | max Δ 7, 18.83% px changed | PASS |  |
| `advisory.html` | max Δ 7, 4.83% px changed | max Δ 7, 6.01% px changed | PASS |  |
| `bluesky-creator-intelligence.html` | max Δ 212, 13.91% px changed *(flag raw)* | max Δ 239, 65.51% px changed *(flag raw)* | PASS (noise) | Animated beat-cluster map differs run to run; outside it nothing changed beyond ≤7. |
| `city-lab-chicago.html` | max Δ 7, 0.79% px changed | max Δ 7, 0.66% px changed | PASS |  |
| `city-lab-dc-v3.html` | max Δ 53, 58.11% px changed *(flag raw)* | max Δ 52, 46.23% px changed *(flag raw)* | PASS (explained) | Gray shift ≤7 everywhere. One real difference: footer tagline (702 px) heavier. That comes from C6 (Source Code Pro 500 is now loaded; the tagline inherits weight 900 from the page, so it is faux-bold on the 500 face instead of the 400 face), not from C7. |
| `co-ops.html` | max Δ 7, 38.96% px changed | max Δ 7, 45.44% px changed | PASS |  |
| `contact.html` | max Δ 7, 0.15% px changed | max Δ 7, 0.14% px changed | PASS |  |
| `for-brands.html` | height/size changed (7332, 1440) -> (7330, 1440) *(flag raw)* | max Δ 7, 10.79% px changed | PASS (noise) | Page height flips between 7330 and 7332 on the untouched tree too (a dynamic element); side-by-side viewport slices old vs new: ≤10. |
| `how-we-did-this.html` | max Δ 7, 0.08% px changed | max Δ 7, 0.07% px changed | PASS |  |
| `index.html` | max Δ 204, 15.09% px changed *(flag raw)* | max Δ 250, 54.37% px changed *(flag raw)* | PASS (noise) | Animated hero canvas. Old-vs-old gives the same noise (36,437 px vs 37,230). |
| `latin-america-lab.html` | max Δ 7, 37.05% px changed | max Δ 7, 24.05% px changed | PASS |  |
| `lists.html` | max Δ 7, 0.27% px changed | max Δ 7, 0.27% px changed | PASS |  |
| `mobile.html` | max Δ 7, 67.26% px changed | max Δ 5, 44.51% px changed | PASS | Page is 577px wide at a 390px viewport (horizontal overflow) before and after. |
| `partners/ahp.html` | max Δ 7, 40.74% px changed | max Δ 7, 23.86% px changed | PASS |  |
| `partners/cillizza.html` | max Δ 7, 38.13% px changed | max Δ 7, 23.26% px changed | PASS |  |
| `partners/emily-atkin.html` | max Δ 7, 40.36% px changed | max Δ 7, 25.82% px changed | PASS |  |
| `partners/icfj.html` | max Δ 7, 37.92% px changed | max Δ 7, 20.46% px changed | PASS |  |
| `partners/iij.html` | max Δ 7, 42.16% px changed | max Δ 7, 24.97% px changed | PASS |  |
| `partners/index.html` | max Δ 6, 0.18% px changed | max Δ 0, 0.0% px changed | PASS |  |
| `partners/jessica-stahl.html` | max Δ 7, 38.46% px changed | max Δ 7, 23.47% px changed | PASS |  |
| `partners/joon-lee.html` | max Δ 7, 37.79% px changed | max Δ 7, 23.54% px changed | PASS |  |
| `partners/karen-attiah.html` | max Δ 7, 38.53% px changed | max Δ 7, 26.61% px changed | PASS |  |
| `partners/knowledge-creators.html` | max Δ 7, 39.65% px changed | max Δ 7, 23.5% px changed | PASS |  |
| `partners/natgeo.html` | max Δ 7, 38.89% px changed | max Δ 7, 26.09% px changed | PASS |  |
| `partners/news-creator-corps.html` | max Δ 7, 37.25% px changed | max Δ 7, 23.33% px changed | PASS |  |
| `partners/nj-lab.html` | max Δ 7, 63.07% px changed | max Δ 7, 58.66% px changed | PASS | Graphics-labelled hexes left Cool (4 chart-label rules). |
| `partners/njlab.html` | max Δ 7, 63.08% px changed | max Δ 7, 58.68% px changed | PASS | Same as nj-lab. |
| `partners/noah-smith.html` | max Δ 7, 38.61% px changed | max Δ 7, 26.96% px changed | PASS |  |
| `partners/rahim-jessani.html` | max Δ 7, 41.08% px changed | max Δ 7, 27.28% px changed | PASS |  |
| `preview/nodes-and-networks-f348eb08/index.html` | max Δ 0, 0.0% px changed | max Δ 0, 0.0% px changed | unchanged | Not touched: own palette. |
| `pulse.html` | max Δ 7, 65.71% px changed | max Δ 43, 71.55% px changed *(flag raw)* | PASS |  |
| `research.html` | max Δ 7, 21.23% px changed | max Δ 255, 41.69% px changed *(flag raw)* | PASS (noise) | 390px: auto-scrolling carousel is offset by 1–2px. Viewport slice old vs new: max 7. |
| `search.html` | max Δ 255, 99.94% px changed *(flag raw)* | max Δ 255, 63.49% px changed *(flag raw)* | PASS (verified another way) | Chromium drops parts of this 300,000px full-page capture (filter text blank). Side-by-side viewport slices of old vs new tree at 1440 and 390: max 7 (a handful of px at 12 and 60). |
| `submit-thanks.html` | max Δ 7, 14.59% px changed | max Δ 7, 16.09% px changed | PASS |  |
| `submit.html` | max Δ 7, 18.33% px changed | max Δ 7, 12.0% px changed | PASS |  |
| `teamdmv/index.html` | max Δ 0, 0.0% px changed | max Δ 0, 0.0% px changed | unchanged | Not touched: no Cool hexes, own system. |
| `updates.html` | max Δ 7, 7.77% px changed | max Δ 7, 9.68% px changed | PASS |  |
| `watershed-preview-uhh7gdyn/index.html` | max Δ 0, 0.0% px changed | max Δ 0, 0.0% px changed | unchanged | Not touched: self-contained page with its own token copy. |
| `who-we-are.html` | max Δ 7, 33.51% px changed | max Δ 7, 39.31% px changed | PASS |  |
| `wire.html` | max Δ 7, 42.57% px changed | max Δ 8, 35.03% px changed | PASS |  |

*Expected change is a max Δ of 7 (e.g. `#c6c6cd` → `#c6c6c6`) and the page background warming; that is what every PASS row shows. No layout shift, lost border or non-gray color change was found.*

### C8: weight 800/900
- 25 declarations → 700: `city-lab-dc-v3` 12, `mobile` 6, `bluesky-creator-intelligence` 5, `lists` 2. Inter requests lose `800` in `header.js` and 22 public pages.
- **Correction to the discovery report:** it said there were zero uses of 900. There are 16 (e.g. `city-lab-dc-v3` ×7, `bluesky` ×2, `teamdmv` ×3, `mobile`, and `main.js:1542`). The report's C5 section needs that fixed; I corrected it in this session's docs commit.
- **Left alone:** `teamdmv` (3 uses of 900 on its own Playfair Display, intentional there), D3 text in `assets/js/main.js` (L1542 `900`, L1873 `800`; graphics), `search.html` keeps the Inter 800 request for that reason, internal pages (25 more declarations in `atlas-signal-brief`, `beat-*`, `chicago-analysis`, `atlas-portal`, `smartnews`).
- Dead `--weight-extrabold` removed from `variables.css`.

| Page | Before → after | Status |
|---|---|---|
| `city-lab-dc-v3` | Hero headline "Who Covers Washington Now" and stat headings lighter (900/800 → 700); height unchanged | pass |
| `mobile` | Headings lighter; unchanged height | pass |
| `bluesky-creator-intelligence` | Headings lighter; 1440 same height; 390: **22px taller in 57,428** (text re-wraps), horizontal overflow 714 → 708px | pass (note) |
| `lists` | Headings lighter; unchanged height | pass |
| the other 36 public pages | no change beyond animation noise (compared with the C7 state) | pass |

## Left alone / found along the way
- **Not done and why:** C4 for `lists`, `nj-lab`, `njlab` (held back, patch saved); `watershed-preview`, `teamdmv`, `nodes-and-networks` (self-contained; SCP 500 not available there); internal pages' Cool hexes (434) and 800/900 (25); D3 text weights; the 8 nj-lab/Pulse graphics hexes; off-system grays.
- **Cosmetic leftovers noticed:** `header.css` still `@import`s JetBrains Mono on every page; `variables.css` `--color-border-dark: #48484f` and `--medium-gray: #999999` are off-system; `--space-3xl` 64 vs 96; `lists` still has its own off-system aliases (`#f5f5f5`, `#e0e0e0`, lime `#d4ff33`).
- **Screenshot tooling notes:** `search.html` full-page capture is unreliable (300,000px tall); I compare it by viewport slices instead. The homepage hero, Bluesky map, Research carousel and Pulse animate, so a pixel diff there always shows noise. Both are documented in the C7 table.
- **The brief's "everything in this repo is served by Cloudflare"** is not how `build-dist.sh` works (allowlist); noted in C1.
