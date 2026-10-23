# V15 Discovery Report

*Read-only pass, Oct 22, 2026. Repo `~/Documents/GitHub/journalism-atlas/`, branch `main`, HEAD `b1827fb`. Inputs: `DESIGN-TOKENS-v15.md` (684 lines) and `ATLAS-BRAND-GUIDE-v4.md` (304 lines), both read from `~/Downloads/` (the ` (1)` copies are byte-identical).*

Companion files: `V15-SCOPE-BUCKETS.md`, `V15-JAMES-QUESTIONS-DRAFT.md`, `inventory/*.csv`, `inventory/c_samples.md`, `screenshots/baseline/`.

**Method and limits.** Static parse of CSS (files and `<style>` blocks), inline `style=""`, JS and markup, plus two runtime passes in headless Chromium: the baseline screenshots, and a computed-style scan of every public page at 1440px in the rest state (this is the evidence for "green at rest" in Track D). "Surface" in the static CSVs (`light?` / `dark?`) is a guess from nearby rules and class names. Treat it as a hint, not a fact. The runtime scan measures the real background behind each element. I did not hover or click anything, so hover and press states come from the CSS only. All scans exclude `dist/` (git-ignored build output), `_deprecated/`, `data/archive`, `scripts/archive`, `docs/`, `outputs/` and `sessions/`.

---

## One-screen summary

**What we found, in six lines**

1. **The v14 sweep already cleaned the easy things.** Zero live hits for Hanken Grotesk and `#ff9600`. The five retired grays and `#efeff2` survive only in `lab/health-field-finder/*` (internal, 4 lines). Those v15 search-and-replace tasks are essentially done.
2. **"One repoint" will not move most pages.** The page background is hardcoded `#efeff4` on `index.html`, `pulse.html`, `research.html` and the nj-lab pages. Every partner page defines its own `--page-bg: #efeff4` and carries 10–13 hardcoded Cool hexes. Six public pages pin `--light-gray` / `--dark-gray` to Cool hexes in an inline `:root`. **413 chrome hits of Cool hexes on public pages** have to be replaced by role variable in the same commit as the repoint, or pages will show a Neutral gray beside Cool backgrounds. Only 25 Cool hits are graphics. Details in Track B and C.
3. **The hover repoint is safe.** All 67 uses of `--color-hover` are fills, except 3 text/border uses that sit on dark surfaces (where Acid is allowed). **There are no repoint hazards.** The risk is the other direction: 24 hover rules use Lime directly (`#97d600` or `--color-lime`) and will not follow the repoint (Track D).
4. **Source Code Pro is effectively not on the site.** `footer.js` loads it at weight 400 only, for the footer. Every mono label in the site CSS is `DM Mono` (6 files, 132 declarations) or `JetBrains Mono` (3 files, 44 declarations; `header.css` `@import`s it on every page at 400/700). v15's Label and Tag styles need SCP 500 loaded and **338 uppercase rules** (256 on public pages) converted. This is the biggest piece of v15 work.
5. **Green rests on a lot of non-interactive things.** On the 40 public pages, 1,150+ elements rest in Dark Olive without being links (follower counts, channel names, beat tags). 37 pages rest an Acid fill on light (header Search button on every page, `.atlas-footer-btn`, active chips). The Lime pulse dot sits in every page's header. v15 allows only body links and dark eyebrows to rest green.
6. **Beat dots cannot ship data-driven.** Exactly 1 of the 79 topic tags in `creators-data.json` ("Sports") equals an `ATLAS_VIZ_COLORS` key, and 0 of the 9 creator `group` values do. Only the hardcoded homepage cluster cards come close (6 of 9 exact, 3 near).

**Counts** (see `V15-SCOPE-BUCKETS.md`): **GREEN 16 · AMBER 16 · RED 5**, plus 4 non-v15 prerequisites (fonts, broken `variables.css` loads, where the spec files live, the Cloudflare preview check). Recommended Session 1 is in the buckets file's last section.

**Three biggest risks**

1. **Mixed-scale pages.** Repointing in `variables.css` alone makes some pages Neutral and leaves the rest Cool. Ship the repoint and the 413 hex replacements together, and fix the 7 public pages that don't get `variables.css` at all.
2. **Button and tag restyle is a visible redesign, not a token swap.** Buttons stop resting in Acid (37 pages, including the homepage hero CTA on black). 134 pill rules on 30 public pages become 6px rectangles. 488 sub-13px rules on public pages need a decision. Don't ship these on the strength of "v15 says so" without a staging look.
3. **Font plumbing.** Source Code Pro 500 isn't loaded; Inter 500 (93 public rules) and 800 (58 declarations) are still in use; the header nav already overflows below about 1100px and would overflow at 1280px in SCP caps with today's gaps. Fonts should be fixed first, before any label conversion.

**Check yourself:** (a) Cloudflare preview deployments for non-main branches (Track H), and whether a staging site exists at all (v14/v15 say "review on staging" but nothing in the repo describes one); (b) whether `DESIGN-TOKENS-v15.md` and `ATLAS-BRAND-GUIDE-v4.md` should be committed (and where), since CLAUDE.md names a root path; (c) `CURRENT_STATE.md` records an earlier session where the environment auto-committed and auto-pushed, bypassing GitHub Desktop. Worth confirming that can't happen during a fast session.

---

## Step 0: Verification

| # | Item | Result |
|---|---|---|
| 1 | Repo, branch, status | `~/Documents/GitHub/journalism-atlas/`, `main`, working tree **clean** (0 modified, 0 untracked) at the start. After this pass, `git status` shows only `docs/design/` untracked. |
| 2 | Spec files | v15: `~/Downloads/DESIGN-TOKENS-v15.md` (684 lines). Brand v4: `~/Downloads/ATLAS-BRAND-GUIDE-v4.md` (304). Each has a ` (1)` duplicate, byte-identical (checked with `diff`). **Not in the repo.** `docs/design/` did not exist; I created `docs/design/v15-discovery/`. v14: `DESIGN-TOKENS-v14.md` at repo root (562). **Brand v3 is at repo root** (`ATLAS-BRAND-GUIDE-v3.md`, 220), contrary to `START-HERE.md`, which says it's missing. |
| 3 | `variables.css` | Exists, 323 lines. `:root` blocks pasted in Appendix A. |
| 4 | Page counts | 59 HTML pages in scope: **40 public, 19 internal/dev** (CLAUDE.md's inventory plus `build-dist.sh` for what ships). Root-level `*.html`: 31. **Excluded:** `dist/` (59 HTML, git-ignored build output), `_deprecated/` (37), `data/archive/`, `scripts/archive/`, `docs/` (incl. `docs/briefs/smartnews/reference/*.html`), `outputs/`, `sessions/`. `CLAUDE.md` is stale on the inventory (see Track A). |
| 5 | Headless browser and static server | **Available.** Python Playwright (`~/Library/Python/3.9/.../playwright`) with Chromium 1148/1223 cached. A 30-line Python static server (clean URLs and `_redirects` 200 rewrites) served the repo root. Nothing installed. Track I ran. |

**Public pages (40):** `index`, `pulse`, `research`, `for-brands`, `about-this-project`, `who-we-are`, `how-we-did-this`, `advisory`, `contact`, `updates`, `submit`, `submit-thanks`, `search`, `lists`, `mobile`, `wire`, `co-ops`, `city-lab-chicago`, `city-lab-dc-v3`, `latin-america-lab`, `bluesky-creator-intelligence`, `teamdmv/index`, `watershed-preview-uhh7gdyn/index`, `preview/nodes-and-networks-f348eb08/index`, `partners/index`, 13 curator pages, and `partners/nj-lab` + `partners/njlab` (duplicates).
**Internal (19):** `atlas-portal/*` (2), `atlas-signal-brief`, `atlas_pulse_intelligence`, `atlas_wire_intelligence`, `atlas_wire_review`, `beat-climate|finance|tech`, `chicago-analysis`, `chicago-survey`, `index-pre-homepage`, `lab/health-field-finder/*` (2), `partners/_shell`, `partners/_reviewjames` (+copy), `partners/njlab copy`, `preview/smartnews-d029dc36`.

---

## Track A: Docs and references

*Checkpoint: Track A, ~60 files grepped, 36 files reference a spec filename.*

**Who references what** (excluding `_deprecated/`, `dist/`):

| Referrer | `DESIGN-TOKENS` | `BRAND-GUIDE` | `Long-Form-Report-Template` |
|---|---|---|---|
| `CLAUDE.md` (9 mentions), `CLAUDE copy.md` (7, stray duplicate), `WORKFLOW.md` (3), `START-HERE.md` (2), `CURRENT_STATE.md` (5), `CSS_AUDIT.md` (5), `LEAVE-OFF-LOG.md` (3) | v14 | v3 | `START-HERE.md` says it's not in the repo |
| `assets/css/variables.css` (14), `main.css` (17), `header.css` (1), `header.js` (1) | all comments naming `DESIGN-TOKENS-v14.md §` | — | — |
| Page `<style>` comments: `index.html`, `contact.html`, `latin-america-lab.html`, `co-ops.html`, `partners/nj-lab.html`, `njlab.html`, `njlab copy.html`, `preview/smartnews-*` | comments only | — | — |
| `docs/V12…V14-*.md/.tsv` (prior audits), `docs/briefs/smartnews/*` | comments/tables | — | — |

**Programmatic filename lookups: none found.** No script, Routine or build step reads a spec filename. `.claude/agents/` has only `ryan-dataops.md` (no design references). `build-dist.sh` copies `*.html` and `assets/`, and does not copy `.md`, so spec files never ship. **Implication:** renaming to v15 means a text edit of ~100 comment lines plus CLAUDE.md, WORKFLOW.md, START-HERE.md; nothing breaks if a comment is left stale. Don't spend Session 1 on comment churn: update CLAUDE.md, WORKFLOW.md, the `variables.css` header and the `main.css`/`header.*` header comments, and let page comments age out.

The brief's "assumptions to verify" about CLAUDE.md were **mostly wrong in a good way**. CLAUDE.md has already been updated to v14: no "Acid dark-only / Lime light-only" (it's explicitly marked "Not canon"), no "header always black", no Hanken in `header.js`. What *is* stale is below.

### CLAUDE.md conflict list (design section)

Every rule in CLAUDE.md's design content (lines 56–109), v15's position, and a verdict.

| # | CLAUDE.md line | v15 position | Verdict |
|---|---|---|---|
| 1 | L58 "All visual implementation references `DESIGN-TOKENS-v14.md` at the project root as the single source of truth." | v15 replaces v14 "in full". v15 header: "committed to repo as source of truth" (no path). | **STALE** (version, and path undecided) |
| 2 | L22 reading order: `ATLAS-BRAND-GUIDE-v3.md` before user-facing copy; "Hanken Grotesk is retired per this guide" | Brand Guide v4 replaces v3. Hanken retired: v4 §3 and v15 L358. | **STALE** (v3→v4); Hanken claim AGREES |
| 3 | L67 "Acid and Lime on LIGHT surfaces = fill only, with black or step-6 text on top." | Acid: fill only on light (v15 L78). **Lime: "Not used" on light** (L79). | **AGREES** for Acid; **CONFLICTS** for Lime |
| 4 | L68 "On DARK: acid for CTAs and active states, lime for hover and the focus ring." | Acid = hover/press/selected + eyebrows (L70, L476). Lime = **dark focus ring only; "no longer a hover color"** (L71, L19). Buttons no longer rest in Acid. | **CONFLICTS** |
| 5 | L69 Dark Olive = green for text/icons/thin strokes on light; never a fill; not on dark | v15 L72, L80 | **AGREES** (v15 adds underlines, body links, current nav item) |
| 6 | L70 "Focus ring follows the surface: lime on dark, Dark Olive on light" | v15 L40, L157–158 | **AGREES** (note: the unused var `--focus-ring-dark` is Acid, `--focus-ring-light` is Lime; see Track B) |
| 7 | L71 "One acid moment per composition; olive marking the active state counts as that moment." | "The one-acid-moment-per-composition limit is dropped." (L19) | **CONFLICTS** |
| 8 | L72 "Not canon: the older 'acid on dark only / lime on light only' rule." | Not mentioned in v15 | **STALE** (delete; nobody needs the history) |
| 9 | L73 "Primary CTA (v14): acid fill at rest and active, lime on hover, black text throughout…" | "v14's acid-at-rest primary CTA" is replaced: step-6 fill, white text, Acid hover/press (L20, L492–524) | **CONFLICTS** |
| 10 | L74 "Inline links (v14): olive + underlined on light (hover step 8); white + underlined on dark (hover lime)" | Light: same. **Dark hover is Acid** (L31, L187, L531) | **AGREES** (light) / **CONFLICTS** (dark hover) |
| 11 | L75 "In migration: `--color-accent` is still lime (its live look). Do not repoint…" | `variables.css` already has `--color-accent: var(--color-acid)`; `--color-hover` is still Lime. v15: `--color-hover` becomes an alias of Acid (L204) | **STALE** (the live state described no longer exists) |
| 12 | L76 Header white default or black per page; logo must match; nav text follows header; active nav olive on white, acid on black; sub-nav docked; "Pages do not request it yet" | v15 L264–271, L535–543. Adds hover underlined, selected 2px underline offset 8px. | **AGREES**; add the underline states |
| 13 | L77 "Body copy minimum 16px… Micro (11px) for all-caps labels only (weight 500 min, spacing 0.08–0.1em). Never below 13px for any readable content." | Micro is **replaced** by Label (13px) and Tag (12px), SCP 500 caps. Floor 13px; 12px only for SCP tags/badges/meta (L23, L372–373) | **CONFLICTS** |
| 14 | L78 "Material Symbols Outlined only… Filled reserved for active states only" | Filled only for toggle/action icons; nav and section icons stay outlined at every state (L461) | **STALE** (narrower in v15) |
| 15 | L79 "4px base unit — scale to 2xl 48px" | Adds `3xl` 96px (L407–409) | **STALE** (and `variables.css` still has `--space-3xl: 64px`) |
| 16 | L80 "Font weights 400/500/600/700/800 — 500 for Micro labels only; do not introduce 900" | 800 retired; 500 = Source Code Pro labels and tags only (L384–387) | **CONFLICTS** |
| 17 | L81 "Border radius: 6px for cards/buttons/inputs; **9999px** for pills/tags" | One radius, 6px; pills retired (L24, L422–431). (Note: `variables.css` says 100px, CLAUDE.md says 9999px, v14 said 9999px: internal drift) | **CONFLICTS** |
| 18 | L86–90 token architecture: `main.css` "Primary stylesheet for `index.html` only" | `index.html` no longer links `main.css`; only `search.html` and `index-pre-homepage.html` do | **STALE** (not a v15 item) |
| 19 | L105 `header.js` "Injects Inter + Material Symbols fonts" | v15 needs SCP 500 and Merriweather available; Inter 400/600/700 only | **STALE** once fonts change (today it requests Inter 400–800) |
| 20 | L245 "All pages above have been swept to the design token system… no canonical token redefinitions inline" | n/a | **STALE / false today.** 14 pages (11 public) redefine canonical names inline; 7 public pages don't get `variables.css` (Track B) |
| 21 | L222–243 page inventory lists `nj-lab.html` at root and `index-exploration-V1.html` | Actual: `partners/nj-lab.html`, `partners/njlab.html` (+ copy); exploration file is in `_deprecated/` | **STALE** (not a v15 item) |
| 22 | L4 / `WORKFLOW.md` L11 design contact `james@happicamp.com` | v15 L26: `james@journalismatlas.com` | **STALE** |
| 23 | L70/L75 "Non-negotiable rules" don't mention: no color coding by section/content type; instruction-link/eyebrow/tag/button standards; Neutral vs Cool | New in v15 | **GAP** (add) |

**Proposed replacement design section:** see Appendix B (not applied).

**Ambiguities and internal inconsistencies inside v15/v4 themselves** (quoted, not reconciled):

1. **Nav typeface.** v15 L359: Source Code Pro is for "All-caps UI labels: eyebrows, tags, instruction links, footer and **nav labels**, card meta lines." Brand v4 L80 says the same. But the Nav sections (v15 L535–543, v4 L280) specify only color and underline, not typeface. → Q1.
2. **Pulse baseline claim is wrong.** v15 L684: "Up from 11px today." Live `pulse.html:477` `.post-date` is **13px DM Mono, not caps**; the beat tag (`pulse.html:453` `.beat-tag`) is also 13px DM Mono, a 100px pill. v15 L683/L684 says the 12px "matches the beat tag on the same card". Today it doesn't, and 12px SCP caps will look noticeably different from what James compared against.
3. **Spacing table vs live.** v15 L411–420 asks for 48/48/32/24 gaps. Live: `.nav-links { gap: 2.5rem }` (40px), `.nav-logo-search { gap: 2rem }` (32px). `CURRENT_STATE.md` already knew.
4. **Dark-surface primary.** v15 L500: Primary rest on dark is `#303030` fill with `#909090` outline. On the homepage hero (`#000`/`#111`) that makes the page's main CTA the lowest-contrast thing in view. v15 L524 states the visible change but doesn't mention hero context. → Q14.
5. **Charts vs "green means interaction."** v15 L342: "Acid green `#ceff00` is excluded" from the viz palette, but live canvases use Acid and Lime as category colors (Track D/G). → Q8.
6. **Tag padding.** v15 L248: "`4px 8px` (`3px 7px` when outlined, so heights match)". A beat tag has a dot and an outline (L256) but is described as a fill-or-outline tag. Fine, but the dot's 8px height vs 12px×1.2 line height will want checking against "about 20px tall" (L522).
7. **Spec lists `--color-text-on-dark-2` for "covers small all-caps labels"** (L175) while the Footer section says dividers keep their low-opacity treatment (L178). Not a conflict, but there's no equivalent statement for footer *link* color. → Q9.

---

## Track B: Token plumbing

*Checkpoint: Track B, 59 pages + 3 CSS/JS files, 166 canonical custom properties.*

### Current state of `variables.css` vs v15

Single `:root` block (L15–309) plus one `@media (max-width: 768px)` block (L315–323). Full text in Appendix A.

| Group | Variables | v15 |
|---|---|---|
| Neutral scale | `--gray-neutral-1…8` | **KEEP** (already identical to v15 L108–115) |
| Cool scale | `--gray-cool-1…8` | **KEEP** (graphics scale) |
| Green primitives | `--color-acid` `#ceff00`, `--color-lime` `#97d600`, `--color-olive` `#5d7400` | **KEEP** |
| Role (grays) | `--color-bg`, `-text`, `-text-secondary`, `-muted`, `-border`, `-border-hover`, `--color-surface`, `-heading`, `-text-on-dark-2`, `-border-on-dark`, `--color-bg-dark`, `-text-dark`, `-muted-dark` | **CHANGE:** repoint Cool → Neutral |
| Legacy aliases | `--light-gray`, `--dark-gray`, `--color-light-gray`, `--color-dark-gray` (all → Cool), `--medium-gray: #999999` (off-system), `--color-border-dark: #48484f`, `-border-dark-hover: #606068` (off-system) | **CHANGE / RETIRE:** repoint or fold into roles. Not mentioned in v15's migration list |
| Role (green) | `--color-accent` → Acid (already), `--color-hover` → **Lime**, `--color-accent-on-light`, `--color-focus` (Lime), `--color-focus-on-light`, `--color-link`, `--color-link-on-dark` | **CHANGE:** `--color-hover` → `var(--color-acid)` |
| Role (older green) | `--color-accent-hover: #5d7400` (hardcoded), `--color-accent-dark`, `--color-accent-dark-hover` (→ hover), `--canvas-accent` | **CHANGE / RETIRE**, decide during migration |
| Brand-palette aliases | `--color-acid-green`, `--color-lime-green`, `--color-dark-olive`, `--acid-green`, `--lime-green` | KEEP (aliases; v15 silent) |
| **New in v15, missing** | `--color-surface-dark`, `--color-button`, `--color-button-outline`, `--color-button-outline-on-dark`, `--color-button-2-outline` | **ADD** |
| Focus rings | `--focus-ring-light: 2px solid #97d600` (Lime, on "light"), `--focus-ring-dark: 2px solid var(--color-acid)` | Both are the wrong way round vs v15 (olive on light, lime on dark). **Zero uses anywhere** (grep), so a dead-variable fix |
| Fonts | `--font-primary`/`--font-ui` Inter, `--font-mono` Source Code Pro, `--font-editorial` Merriweather | KEEP. `--font-mono` is used in only 4 declarations in the whole site (footer in `header.css`) |
| Type scale | `--text-micro: 11px`, `--lh-micro`, `--ls-micro`, `--weight-extrabold: 800`, `--text-display` comment "800" | **RETIRE** Micro (add Label 13 / Tag 12); retire 800 |
| Radius | `--radius-base: 6px`; `--radius-pill: 100px`; `--radius-modal: 8px`; `--radius-lg: 16px`; legacy `--radius-xs/sm/md` | **CHANGE:** pill retired; modal 8px vs "one radius" is unspecified |
| Spacing | `--space-3xl: 64px` | **CHANGE** to 96px (v15 L407–409) |
| Viz | `--viz-*` legacy (Tier 3 hexes) | KEEP / deprecated per file comment |

### Pages not loading `variables.css`, or loading it broken

| Page | Class | Situation | Distance to join the system |
|---|---|---|---|
| `lists.html` | public | No link. Inline `:root` defines `--acid-green`, **`--lime-green: #d4ff33`**, `--light-gray: #f5f5f5`, `--medium-gray: #e0e0e0` (all off-system) | Medium: link the file, delete the `:root` block, review the visible background change (`#f5f5f5`→`#efefef`) |
| `mobile.html` | public | No link. Inline `:root` pins `--light-gray/--dark-gray` to Cool hexes | Small: link file, delete `:root` |
| `partners/nj-lab.html`, `partners/njlab.html` (+ `njlab copy`) | public ×2 | **Links `assets/css/variables.css` relatively, which resolves to `/partners/assets/css/variables.css` and 404s** (`START-HERE.md` already noted). 43 hardcoded Cool hexes, 25 hardcoded green uses | Small fix (`/assets/css/variables.css`) then ~43 hex swaps. **Two near-identical copies are both live.** Pick one |
| `preview/nodes-and-networks-f348eb08/index.html` | public (unlisted, `robots` disallow) | No `variables.css`, no `header.js`/`header.css`. Own palette (`--bg: #faf9f5`, DM Sans, Libre Baskerville), own `section-nav` and "Jump to cohort" strip. **Generated** by `tools/preview-build`. | Large and a design decision (Q16). Edit the generator, not the HTML |
| `teamdmv/index.html` | public | No header/tokens. Own system (`#F8F5F0`, Playfair Display, DM Sans/DM Mono, radii 12/20px). Playfair is not in the brand | Large; separate design call |
| `watershed-preview-uhh7gdyn/index.html` | public (unlisted) | Own full copy of the tokens (21 canonical redefinitions) in a single line, hardcoded, loads Inter 400/500/700 + Merriweather | Medium: swap the copy for `<link>`; 163 plain olive links to review |
| `atlas-portal/*` (2), `atlas-signal-brief`, `atlas_pulse_intelligence`, `atlas_wire_intelligence`, `atlas_wire_review`, `beat-climate`, `beat-finance`, `beat-tech`, `chicago-analysis`, `chicago-survey`, `lab/health-field-finder/*` (2), `partners/njlab copy` | internal | No usable `variables.css` | 344 of the 434 internal Cool hits are in the three `beat-*` pages. Leave internal pages out of v15 scope unless Justin wants them |

`index-pre-homepage.html` and `partners/_reviewjames*.html` load the file; `partners/_reviewjames*` skip `header.js`.

### Pages with inline `:root` redefining a canonical token

| Page | Redefined | Same as canonical? |
|---|---|---|
| `about-this-project`, `how-we-did-this`, `who-we-are` (public) | `--black --white --acid-green --lime-green --light-gray --dark-gray` | Same values, but **`--light-gray: #efeff4` and `--dark-gray: #303036` are hardcoded**, so they will **not** follow a Cool→Neutral repoint |
| `advisory` | same six | same |
| `mobile` | `--black --white --light-gray --dark-gray --acid-green` | same, same pin |
| `lists` | six + `--medium-gray` | **Different:** `#d4ff33`, `#f5f5f5`, `#e0e0e0` |
| `atlas-portal/index` (internal) | seven | same pin |
| `bluesky-creator-intelligence` (`--white --black`), `city-lab-dc-v3` (`--white`), `chicago-*` (one each) | | harmless |
| `preview/nodes-and-networks…` | `--font-ui: 'DM Sans'` | **Different** (intentional; own chrome) |
| `teamdmv` | `--radius-md: 12px`, `-lg: 20px` | **Different** |
| `watershed-preview…` | 21 | same values, hardcoded |

### The key question: if the gray roles are repointed Cool → Neutral in `variables.css`, which pages change?

Computed per page by counting references to role variables that follow the repoint vs references that don't (hardcoded Cool hex in CSS, inline or JS, or a role alias pinned by an inline `:root`). Full table: `inventory/b_pages_tokens.csv`.

**Pages that change fully** (all gray roles go through role variables, no pin): `contact`, `latin-america-lab`, `submit`, `submit-thanks`, `updates`, and `search` (via `main.css`, 53 role-variable uses, 2 hardcoded in the page). `index-pre-homepage` also, but it's internal.

**Pages that change partly** (this is where mixed scales appear):

| Page | Follows | Doesn't | What stays Cool |
|---|---|---|---|
| `index.html` | 14 | 15 hardcoded | **`body { background: #efeff4 }` (L39)**, cluster card borders, and others |
| `research.html` | 9 | 16 | body background L36 hardcoded |
| `wire.html` | 22 | 18 | body uses `var(--color-bg, #efeff4)` so it follows |
| `for-brands.html` | 9 | 16 | dark page (`#111`); text hexes |
| `about-this-project` | 5 | 11 + pinned alias | `--light-gray/--dark-gray` pinned |
| 13 curator `partners/*` pages | 5 each | 10–12 each + local `--page-bg: #efeff4` | page background and card text |
| `co-ops`, `bluesky-creator-intelligence` | 1 / 6 | 7 / 4 | local `--page-bg: #efeff4` |

**Pages that don't change at all:** `pulse` (0 role-variable uses; `body { background: #efeff4 }` at L27 and `#303036` text hardcoded), `city-lab-chicago` (23 hardcoded Cool hexes, no role vars), `city-lab-dc-v3` (local palette `--light: #efeff4`), `advisory`, `how-we-did-this`, `who-we-are` (alias pinned), `lists`, `mobile`, `partners/nj-lab` + `njlab` (CSS not loaded), `watershed-preview`, `teamdmv`, `nodes-and-networks`.

**Header and footer on every page:** `header.css` uses `var(--gray-cool-*)` directly (not role vars) for the black theme and for the search button's disabled state, and **hardcodes `#c6c6cd` four times** in the footer (`.footer-tagline`, `.footer-col-title`, `.footer-copy`, `.footer-legal a`) plus `#303036` for the search button text. That means the footer on every page stays Cool after a `variables.css`-only repoint. `header.css` also uses `--dark-gray`, `--light-gray` and `--black`, which follow once the aliases are repointed.

**Conclusion.** Of the 40 public pages, a repoint in `variables.css` alone changes **6 fully** (`contact`, `latin-america-lab`, `submit`, `submit-thanks`, `updates`, `search`), **20 partly** (mixed Neutral and Cool), and **13 not at all** (`pulse`, `city-lab-chicago`, `city-lab-dc-v3`, `advisory`, `how-we-did-this`, `who-we-are`, `lists`, `mobile`, both nj-lab copies, `watershed-preview`, `teamdmv`, `nodes-and-networks`); `partners/index` has no gray roles. For the repoint to deliver "the page background warms slightly and nothing else moves" it must travel with (1) repointing the legacy aliases, (2) replacing the 413 Cool hexes in chrome (Track C), (3) removing the inline pins on 6 pages, and (4) linking `variables.css` on `mobile`, `lists` and fixing the nj-lab path. The 25 Cool hits in graphics stay.

---

## Track C: Value searches

*Checkpoint: Track C, 59 pages + 3 assets, all searches run. Per-search detail is in `inventory/c_*.csv`; up to 5 sample lines per file are in `inventory/c_samples.md`.*

### C1. `Hanken`
**0 live hits.** All hits are in `_deprecated/` (10+ files) and `docs/briefs/smartnews/reference/`. `header.js` does not mention Hanken. Nothing to do.

### C2. Cool hexes `#efeff4 #c6c6cd #909097 #5e5e64 #303036 #121218 #efeff2`
**879 hits in 50 files: 854 chrome, 25 graphics.** (Case-insensitive; also matched `rgb()`/`rgba()` forms such as `rgba(239,239,244,.65)` in nj-lab. None of these hexes has a 3-digit shorthand.) By hex: `#303036` 480, `#efeff4` 346, `#c6c6cd` 37, `#5e5e64` 7, `#909097` 5, `#121218` 2, `#efeff2` 2 (lab only).

| By page class | Hits | Files |
|---|---|---|
| Public | 430 (413 chrome, 17 graphics) | 32 |
| Internal | 434 (344 in `beat-climate/finance/tech`) | 16 |
| `header.css` / `variables.css` | 9 / 6 (variables.css = the scale definitions, which stay) | 2 |

Top public files (chrome): `partners/nj-lab` and `njlab` 48 each, `city-lab-chicago` 24, `pulse` 19, `wire` 18, `for-brands` 16, `research` 16, `index` 15, `about-this-project` 13, 13 curator pages 10–13 each, `co-ops` 8.

**Graphics (leave as Cool, 25 hits):** `watershed-preview` inlined SVG fills/strokes (12), nj-lab viz legend/bar labels in `rgba(239,239,244,…)` (4 per copy), `pulse.html` heatmap cell colors (2), `search.html` (1), `atlas-signal-brief` bar fill (internal), `legend-dot` swatches in `beat-*` (internal). The classifier is a heuristic: a selector or JS line mentioning chart/legend/svg/fill/stroke counts as graphics. Spot-check before bulk replace.

### C3. Retired grays `#313131 #6b6b6b #9e9e9e #bdbdbd #a8a8a8` (and `#efeff2`)
**4 hits, 2 files**, both internal and `noindex`: `lab/health-field-finder/funder.html` and `review.html`, `background: #313131` (surface/fill, dark). `#efeff2`: same two files. v15's "none should remain" check is **already passing** for everything that matters.

### C4. `#ff9600`
**0 hits** (also checked `#f90`, `rgb(255,150,0)`).

### C5. `font-weight: 800 / 900 / extrabold`
**58 declarations in 12 files** (33 on 5 public pages: `city-lab-dc-v3` 14, `mobile` 7, `bluesky-creator-intelligence` 5, `teamdmv` 4, `lists` 3; the rest internal: `atlas-signal-brief` 13, `beat-*` 15, `chicago-analysis` 5, `atlas-portal` 2, `smartnews` 2). Plus: one D3 style, **`assets/js/main.js:1873` `.style('font-weight','800')`**; **`assets/js/header.js:40` requests Inter `wght@400;500;600;700;800`** (so every page loads 800); 19 other Google Fonts URLs request 800. There are zero uses of 900. All become **700** (v15 L387 says 700 does the same job). The `--weight-extrabold` and `--text-display` "800" comments in `variables.css` go with it. `font-weight: 800` on Display-type headings is the visible part.

### C6. Inter at weight 500
**132 declarations that resolve to Inter 500 (93 on public pages, 21 files)** vs 29 declarations that are mono 500 (allowed). Breakdown of the Inter ones by role: labels/eyebrows/meta 27, tags/chips/pills/badges 25, buttons/CTAs 16, cards 9, nav 7, other 48. Examples: `.about-subnav-link`, `.hero-stat-label`, `.pill`, `.card-link`, `.filter-chip`, `.card-badge`, `.row-link`, `.mobile-menu-link` (header.css), `.btn-lime`. v15 L384: "500 (medium): Source Code Pro labels and tags only". The header `ensureFont` loads Inter 500 today. → Q5.

### C7. Radius
**755 radius declarations.** On public pages: `6px` already 153; **pill 134 rows on 30 files** (`100px` ×133 overall, `9999px` ×24; no `999px` or `50px` pills found; a few 20–24px); true circles `50%` 53; other values: 2px (22), 8px (18), 12px (17), 3px (16), 4px (15), 10px (4), 1px (4), asymmetric (3), plus 11 uses of a page-local `var(--radius)` and 33 of `var(--r)` that I did not resolve. Biggest pill owners: `city-lab-chicago` 17, `pulse` 14, `index` 12, `for-brands` 8. A `50%` was treated as a circle when the same rule has equal width/height or the selector names an avatar/dot/icon, otherwise flagged `circle?`; none were ambiguous on public pages. `variables.css` `--radius-pill: 100px` is used by 5 places. v15 says one radius for "everything rectangular"; the 2–4px badges, 8–12px cards/inputs and 16px mobile drawers are not addressed beyond that sentence. → AMBER default in buckets.

### C8. Font sizes below 13px
**842 rules/lines in 50 files; 488 CSS rules on 34 public pages.** By size: 11px 254, 12px 252, 10px 107, 9px 102, 8px 9, odd values (12.5, 10.9, 12.8) 17. By typeface and case (CSS rules): Inter/inherited **not caps** ≈ 380 (12px: 214, 11px: 107), Inter/inherited **caps** ≈ 190 (11px: 127), mono caps ≈ 79 (9px: 54, 10px: 25), mono not caps 56. Another 78 SVG/JS chart text sizes (8–12px) are graphics. The 12px SCP exception covers only tags, badges and card meta lines, so **the 214 non-caps Inter 12px rules and everything at 9–11px must either go to 13px or be re-expressed as SCP Tag/Label.** Worst offenders: homepage `.hcn-pill` **8px** JetBrains Mono pills, footer labels 9–10px (`header.css` L338–346), `.nav-soon-badge` 8px, Pulse tickers 9px.

### C9. `text-transform: uppercase` and typed caps
**338 CSS rules (256 on public pages).** Typeface: Inter/inherited 231, **DM Mono 74, JetBrains Mono 26**, other mono 7. Size: 11px 131, 9px 59, 10px 52, 12px 33, 13px 22, em/rem values ~8. Weight: **700 ×117**, 500 ×55, 400 ×36, 600 ×11, 800 ×5, inherited 113. Letter-spacing: 0.1em ×88, 0.08em ×59, 0.14em ×32, 0.12em ×24, 0.15em ×21, 0.06em ×20, 0.04–0.05em ×17. Typed all-caps text in markup is rare (24, mostly acronyms: ICFJ, ATLAS, WRUL). The Label/Tag conversion is a CSS change, not a copy change. No 0.16em/0.14em values survive the v15 0.08–0.12em range, so each rule needs a Label (0.08–0.12) or Tag (0.08) assignment. → AMBER item in buckets, with a mapping default.

### Off-system gray census (context for the "snap to Neutral" item)
Across in-scope files, **128 distinct near-gray hexes outside both scales, 2,004 uses** (top: `#1a1a18` ×288, `#4a4a46` ×228, `#6b6b64` ×170, `#d4d4d8` ×107, `#ddddd8` ×106, `#888888` ×84, `#555555` ×77, `#606068` ×70, `#b0b0b8` ×70, `#666666` ×66). v14 counted ~107 colors / ~1,444 uses. The nodes-and-networks page's warm palette is a large share. This is the v15 "later release" item.

---

## Track D: Green and hover role inventory

*Checkpoint: Track D, 1,246 static references in 58 files, plus 2,993 runtime records on 40 public pages.*

Evidence files: `inventory/d_green_roles.csv` (static, every reference to a green variable, alias, local alias such as `--acid`/`--neon`/`--lime`/`--olive`, or raw `#ceff00`/`#97d600`/`#5d7400` including `rgba()` forms); `inventory/d_green_at_rest_computed.csv` (runtime, rest state, true surface).

### 1. Repoint hazards (if `--color-hover` becomes `#ceff00`)

**None.** `--color-hover` has **67 uses**:
- **64 are `background` / `background-color` fills** (`.btn-acid:hover`, `.atlas-footer-btn:hover`, partner `.card-link:hover` and `.pill.platform:hover`, `.nav-search-btn` uses raw lime, etc.). Fill is the one thing Acid may do on light.
- **3 are text/border and sit on dark surfaces**, where Acid is allowed and wanted: `header.css:162` (`.nav-link:hover` via `--header-fg-hover` in the **unwired black theme** only; on white it resolves to `--black`), `contact.html:76` `.contact-sub a:hover` (dark hero), `pulse.html:170` `.lede-beat:hover` border (`#111` masthead). The static scanner flagged these as "light?"; the runtime/source check shows they're dark.

**The real hazard is the opposite one: hovers that use Lime directly and won't move.** **24 hover/press rules use `#97d600` or `--color-lime`/`--lime-green`**, so after the repoint they'd still hover Lime, against v15's "Lime is no longer a hover color". Public ones: `header.css` `.nav-search-btn:hover` (raw `#97d600`, so **the header search button on every page**), `header.css` `.mobile-menu-link:hover` left border, `main.css` `.breadcrumb-item:hover`, `.sunburst-creator-card:hover`, `.viz-creators-table a:hover`, `partners/nj-lab|njlab` `.cta-primary:hover` (fill and border), `city-lab-chicago` `.beats-toggle-btn:hover`, `watershed-preview` `.dark a:hover` (text). Internal: `atlas-portal`, `atlas-signal-brief`, `beat-climate`, `chicago-survey`. Additional resting uses of Lime outside the focus ring: **45 rest-state rules**, e.g. `.nav-pulse-dot` (6px dot in the header of all 37 pages that load `header.css`; background `#97d600`), `header.css` `.nav-search:focus` border + glow (`--lime-green`, `rgba(151,214,0,.15)`).

**Dependency:** none needed before repointing `--color-hover`; but the 24 Lime hover rules should move to `--color-hover`/`--color-accent` in the same session, or hover is two different greens depending on the page.

### 2. Green at rest (v15 allows only body links on light, olive, underlined; eyebrows on dark, Acid)

Runtime rest-state scan, 40 public pages, 1440px. Unique selectors matter more than element counts (JS-rendered cards repeat).

| What rests green | Where (unique selector → pages) | Elements | v15 |
|---|---|---|---|
| **Acid fill on light**: header Search button | `button.nav-search-btn` → 37 pages | 37 | Primary button: step-6 fill, Acid on hover |
| Acid fill on light: footer-area CTA | `a.atlas-footer-btn` → 14 partner pages | 14 | Primary button |
| Acid fill on light: active filter chips | `button.chip.active` (13), `.filter-pill.active`, `.signal-tab.active`, `.bx-chip--active` | ~17 | Secondary button selected = **black** fill |
| Acid fill on light: bars, dots | `.card-count-dot`, `.beat-map-bar-fill`, `.dist-bar-fill`, `.pi-beat-bar-fill`, `.gmp-bar`, `.featured-dot`, `.pulse-dot-inline` | ~40 | Data bars/status dots in Acid = chart-in-green question (Q8) |
| Acid fill on light: primary CTAs | `.btn-primary` (homepage, research, for-brands, latin-america-lab), `.header-cta`, `.btn-acid`, `.btn-lime`, `.contact-email-btn`, `.cta-primary`, `.form-submit`, `.submit-btn` | 37 pages with an Acid fill somewhere | Rest in gray (v15 L524) |
| **Lime fill on light** | `span.nav-pulse-dot` in header → 37 pages; `.card-badge.badge-verified` (nj-lab ×2); `.ci-platform.cross` (bluesky page, 226) | 300+ | Lime = dark focus ring only |
| **Olive fill** (never a fill) | `span.beat-tag` in Pulse (50), `.creator-chip-count` (10), `.pulse-live-badge` | 61 | Beat tag per v15: dot + outline |
| **Olive text/border on non-links** | `div.creator-channel` (13 curator pages), `div.ci-followers` (bluesky page), `p.org-structure`, `.ticker-card-byline`, `span.n`, `span.ci-platform`; **1,154 elements on 21 pages** | 1,154 | Secondary text step 5 |
| Olive on links that aren't body links | `a.card-link` (partner pages, co-ops: 253 elements), `.ticker-card-link`, `.about-link`, `.partner-col-link`, `.cluster-explore-link` | 457 | Instruction links (step 6 at rest) or buttons |
| Olive text on a link in running text | plain `a` (119 elements; 163 are on `watershed-preview`) | 237 | **Allowed**: matches the body-link rule |
| **Olive on dark** (fails 4.0:1) | `em` ×2, `.pulse-dot`, `.stat-live-dot` | 4 | Acid on dark |
| Acid text on dark | hero/pulse ticker beat labels (116), `p.hero-eyebrow` (16), `.card-country`, `.card-channel` (15 each), `.appearance-role`, `.atlas-attribution-badge` (13), `.hero-stat-num`… | 370 | Eyebrows allowed; stat numbers, ticker items, card-channel and attribution badges are not eyebrows |
| Acid border on dark | `.signal-beat-tag`, `.featured-beat`, `.icfj-badge`, `.opp-card`, `.hero-eyebrow-pill`, `.cta-ghost`, `.spotlight-quote` | 44 | Tags have no color but dots |
| Acid non-fill on **light** (v13 violation today) | `button.filter-pill.active` border, `a.cta-btn.cta-primary` border, `.bx-chip--active`, `.signal-tab.active` | 6 | Wrong today; fix with the button restyle |

Static counts for the same question (`d_green_roles.csv`): 560 rest-state green rows, 105 Lime-outside-focus, 197 flagged "Acid non-fill on light" (**unreliable**: dark pages such as `for-brands` (`body #111`) are mislabeled "light?". Use the runtime CSV for this question).

### 3. Focus
All real focus rings use `--color-focus` (Lime, 24 rules) and `--color-focus-on-light` (olive, 45 rules): **correct and already v15-compliant.** Nav search `:focus` pairs an olive outline with a Lime border and glow: mixed. `START-HERE.md` open item 3 ("v14 says lime; `--focus-ring-dark` is still acid") is moot, because that variable is unused.

### 4. JS/SVG-set greens (charts, canvases)
`index.html` `CLUSTERS` (L1540): Climate & Science = Acid, Local News = Lime; `search.html` `FIELD_GROUP_COLORS` (Power & Politics = Acid, Civic Life = Lime) and `FIELD_PLATFORM_COLORS` (Newsletter - Substack = Acid); more in `city-lab-dc-v3`, `city-lab-chicago`, `for-brands`. **Acid and Lime are used as category colors**, against v15 L342 and v14's viz rule. → Q8. Not touched by any of the colour migration; blocked on Ryan (Track G).

---

## Track E: Component pattern inventory

*Checkpoint: Track E, 3,181 rules matched across 21 component patterns. This is a coverage map, not a visual audit. Raw: `inventory/e_components.csv` (one row per rule, first matching pattern), `inventory/e_arrow_links.csv`.*

| Pattern | Selectors (examples) | Files / pages | Current look | v15 |
|---|---|---|---|---|
| **Primary button** | `.btn`, `.btn-acid`, `.btn-lime`, `.btn-primary`, `.cta-btn`, `.atlas-footer-btn`, `.form-submit`, `.nav-search-btn`, `.contact-email-btn`, `.submit-btn` (307 button-ish selectors) | 37 public pages | Acid (or Lime) fill at rest, 6/8px radius, `#000`/`#303036`/`#111` text, weight 500–700, font-size 12–16px, hover = Lime (or `--color-hover`), **header search button is 12px/700 with 6px 14px padding** | **COVERED** (L492–524). Mismatches: 44px min height, 15px/600, gray rest. Which are "primary" vs "secondary" is a judgment per page |
| **Secondary / filter / beat rows** | `.hcn-pill`, `.beat-pill`, `.recency-btn`, `.chip`, `.filter-chip`, `.beat-chip/.plat-chip`, `.view-btn`, `.pill.platform` | index, pulse, search, city-lab-chicago, partners, co-ops, for-brands | Pills (100px) or 4/6px; `.hcn-pill` is **8px** JetBrains Mono caps; selected = Acid fill with olive border (pulse `.beat-pill.active`, city-lab `.beat-chip.active`) or black (`.view-btn.active`, `.recency-btn.active`) | **COVERED** for style (L507–518): rest outline, selected **black**. AMBER for the Acid-selected ones and 44px on dense rows |
| **Tabs styled as buttons** | `.tab-btn` (city-lab-chicago: underline tab strip, 12px caps 700, active bg `rgba(151,214,0,.08)`), for-brands tablist (9 `aria-selected`), pulse (1) | 3 pages | Underline-style, not button-style | **NOT COVERED** (v15 L507 mentions "tabs shown as buttons" only) |
| **Icon-only and toggle/action** | mobile-menu button/close (`header.css`), drawer close, `.material-symbols-outlined` controls | header + a few pages | Transparent, no hover, no filled state. `CURRENT_STATE.md` L55: save/follow/bookmark **do not exist** on the live site (an "add to pack" lives in `search.html` `renderPackCanvas`) | **NOT COVERED** for hover/press/selected on light surfaces (v15 L461 covers glyph fill only) → Q7 |
| **Instruction links (`… →`)** | `.card-link` (17), `.hero-tertiary-link`, `.featured-view-all`, `.research-link`, `.row-link`, `.audience-bridge-link`, `.pulse-intel-cta`, `.pi-beat-more`, unclassed `<a>` (36) | **124 arrow links in 29 files** | Sentence/title case, **never caps**, Inter 14px/400 olive (`.card-link`, hover Lime fill) or JetBrains Mono 11px (`.hero-tertiary-link`, 0.08em); ending in `→` | **COVERED** (L526–533): SCP 13px caps, 0.08–0.12em. Letter-spacing needs one value (Q11). **Wording differs for the same destination** (below) |
| **Body links** | plain `a` in prose; `--color-link` olive underlined on light | watershed (163), partners (4 each), about, others | Olive underlined on light (v14 migration) where applied; some pages leave default blue/none | **COVERED** (L531). Carry-over from v14; mostly there |
| **Header nav** | `.nav-link` (Inter 15px/400, `letter-spacing .01em`, gap 2.5rem), `.nav-link--pulse` (+6px Lime dot), `.nav-link--partners` + `.nav-soon-badge` (JetBrains Mono 8px caps, 100px pill), `.mobile-menu-link` (Inter 16px/500, 3px left border Lime on hover) | all pages (injected by `header.js`) | Rest `--dark-gray`; hover `--black`; **no current-page state at all** (no `aria-current` is ever set; 0 uses on nav) | **AMBIGUOUS** typeface (L359 vs L535–543). Selected state is COVERED by v15 but has no code to hang on. → Q1 |
| **"Jump to" sub-nav** | nodes-and-networks preview only: `.section-nav` (sticky, `background: var(--bg)` = `#faf9f5`, Inter 13px/600) and `.cohort-strip` ("Jump to cohort") | 1 page; **not on the shared header** | Warm off-system page chrome; has no white/olive treatment | **COVERED** by v15 L270 but the template doc `Atlas-Long-Form-Report-Template-2026-09.md` isn't in the repo and the page is **generated** (`tools/preview-build`) → Q16 |
| **Mobile menu** | `.mobile-menu*` | all pages | White drawer, Inter 16px/500 links, `border-left: 3px` Lime on hover, close icon 26px | **NOT COVERED** (v15 silent on drawer link states; Lime hover border conflicts with "Lime = focus only") |
| **Tags, badges, chips: content type** | `.research-badge`, `.card-badge`, `.pill` (13 files: 100px, 13px/600, cursor default) | partners, research | Pills; text-case/size vary | **COVERED** (L250–258). Content-type labels (Essay, Field Study…) appear in the nodes-and-networks preview and pulse copy only |
| Tags: status | none live (no "CHECKED TODAY / HIRED / BEING TESTED / KEPT SEPARATE" in the current site; `HIRED` only in `_deprecated/`) | 0 | n/a | **COVERED**; nothing to migrate |
| Tags: beat | `.beat-tag` (pulse: olive fill-tint pill, 13px DM Mono), `.featured-beat`, `.signal-beat-tag`, `.story-stack-beat`, `.db-pill.topic` (13px JetBrains caps, outline), `.creator-tag`, `.card-beat-tag` | index, pulse, search, city-lab | Colored text/pills in Acid, olive or monotone; **never a Tier 4 dot** | **COVERED** for style; dots blocked → Q2 |
| Tags: platform (Newsletter, Podcast…) | `.db-pill.platform` (black fill, white text), `.pill.platform` (outline, **hover Lime fill, clickable**), `.platform-tag`, `.ci-platform`, `.plat-instagram` etc. brand-hex fills | index, partners, pulse, city-lab, bluesky | Black fill, outline, or platform-brand color | **NOT COVERED** → Q4 (platform brand colors also run into "no color by content type") |
| **Clickable tags** | `.creator-tag.clickable-tag`, `.creator-meta-item.clickable-tag` (search cards, filter on click; hover Lime), `.pill.platform` (13 partner pages), `a.lede-beat`, `.hcn-pill` (homepage buttons), `.beat-pill` (Pulse buttons), cluster `data-filter-*` | search, partners, index, pulse | Pills that filter on click | **CONFLICTS** (v15 L248: "Tags aren't clickable") → Q3 |
| **Eyebrows / small labels** | `.hero-eyebrow` (**22 pages**: DM Mono 10px caps 0.12em), `.section-eyebrow`, `.eyebrow`, `.about-eyebrow` (olive on light), `.lab-eyebrow`/`.spotlight-eyebrow` (Acid, Inter 11px/700 0.16em), `.contact-eyebrow` (white 40%) | 22+ pages | Mono or Inter caps, 9–11px, spacing 0.1–0.16em; colors vary: step 5-ish gray, white at 30–40% opacity, Acid, olive | **COVERED** (L260–262). Dark-surface step 3 vs Acid → Q10 |
| **Card meta lines** | `.post-date` (13px DM Mono), `.platform-tag` (13px), `.signal-card-meta` (11px), `.card-channel`, `.creator-channel`, `.ci-followers` | pulse, search, partners, bluesky | Mono or Inter, 11–13px, mostly not caps | **COVERED** (L380) but v15's "up from 11px" baseline is wrong for Pulse (Track A #2) |
| **Cards and hover** | `.creator-card` (hover: bg `--color-bg`, border `--color-border-hover`), `.cluster-card` (hover: border `#b0b0b8`), `.research-card`, `.way-card`, `.gallery-card` (hover Acid-tint border on dark), whole-card links via `a.cluster-card` | all card pages | Hover is a background shift or a border change, not green. `main.css` L556 `.creator-card:hover` | **NOT COVERED** (v15 L545–548 lists states only) → Q13 |
| **Inputs** | `.nav-search` (Inter 15px, 8px radius, olive focus outline + Lime border), `.form-input` (16px, 6px radius, `#d4d4d8` border, olive focus border), `.db-filter-select` (13px, **4px radius**), `.beat-search-input` (10px DM Mono, borderless) | header, for-brands, submit, index, pulse | Various radii (4/6/8px) and borders | **NOT COVERED** → Q13 (v15 radius table says input 6px) |
| **Selects / dropdowns** | `.db-filter-select` (4 per homepage), native `<select>`s | index, search | Native element, 13px | **NOT COVERED** |
| **Checkboxes, radios, toggles** | 5 rules; `accent-color` not set | submit, for-brands | Browser default | **NOT COVERED** |
| **Table headers, data tables** | `.creators-table th` (dark `#303036`-ish header, 700, white text, sort arrows in Acid, hover `#424242`), `.viz-creators-table th` | search (+ main.css) | Dark header row, bold sentence case, Acid sort arrows | **NOT COVERED** (L359 says Label is for "eyebrows and instruction links") → Q6 |
| **Footer links and labels** | `.footer-col ul li a` (Inter 13px, `rgba(255,255,255,.55)`, hover `#fff`), `.footer-col-title` / `.footer-copy` / `.footer-legal a` (**9px** `Source Code Pro`→fallback, caps, 0.06–0.14em, hardcoded `#c6c6cd`), `.footer-tagline` (10px) | all pages (injected by `footer.js`) | Mono labels below the floor and loaded at weight 400 only | **AMBIGUOUS** (L359 says footer labels are SCP; links and hover are not specified) → Q9 |
| **Pagination / load more** | `.beat-more-btn` (Pulse: dashed pill, 9px caps), `.view-more`, `.load-more` | pulse, search | Text-style buttons | **NOT COVERED** |
| **Tooltips, modals, drawers** | `.sunburst-creator-card`, drawer in `main.js` (`atlasOpenDrawer`), index hero `#cluster-panel`, D3 hover tooltips (mouseover handlers in 13 files), `.mobile-menu` | index, search, city-labs, bluesky | Dark panels; `--radius-modal: 8px` | **NOT COVERED** (radius for modals/drawers; v15's "one radius" would make it 6px) |
| **Chart interaction** | legend toggles, active segment, hover cards in `index.html`, `search.html`, `city-lab-*.html`, `pulse.html` heatmap (`BEAT_COLORS` uses 14 Tailwind-like hexes `#2563eb #7c3aed #db2777 …`), `main.css` sunburst | 6 pages | Brand-secondary hexes (and Acid/Lime) as categories | **NOT COVERED** and gated on Ryan (Tier 4 migration is a "separate project") |
| **`:visited` and disabled** | `:visited`: **0 rules**. Disabled: 36 files have `:disabled`/`[aria-disabled]` rules (mostly `gray-cool-4/5` on buttons) | | | **COVERED** for buttons (L505); visited not specified |

**Same destination, different wording** (`inventory/e_arrow_links.csv`; all 124 arrow links are sentence/title case): `/pulse` → "Atlas Pulse", "Explore Atlas Pulse", "Explore the full digest", "Full intelligence", "Open full Pulse feed", "See it live", "View Pulse"; `/search` → "Explore the Atlas", "Filter by topic in the full database", "Open in full Atlas database", "Search creators", "View all", "View in Atlas"; `/about-this-project` → "About the Atlas", "How we built this", "Learn how the Atlas works"; `/` → "Explore the Atlas", "View in Atlas", "Visit"; `/` + `search` also share "Explore the full Atlas / database". Unifying wording is a copy decision (it fixes mixed case "on the live homepage" per v15 L680 only if wording is also unified); CSS can only unify case and spacing.

---

## Track F: Font loading

*Checkpoint: Track F, 59 pages, every `fonts.googleapis.com` URL, every `font-family`.*

**Where each family and weight is loaded**

| Mechanism | What |
|---|---|
| `assets/js/header.js` `ensureFont()` (every page) | **Inter `wght@400;500;600;700;800`**; Material Symbols Outlined (`opsz,wght,FILL,GRAD@20..48,400,0,0`) |
| `assets/js/footer.js` (every page) | **Source Code Pro `wght@400`** (footer only, per its own comment) |
| `assets/css/header.css` L1 `@import` (every page) | **JetBrains Mono `wght@400;700`** |
| Page `<head>` link or `@import` (36 pages, 24 public, incl. 13 curator pages) | Inter 400–800 (duplicate of `header.js`), Material Symbols (several different axis ranges) |
| `bluesky-creator-intelligence`, `for-brands`, `search`, `teamdmv` | **DM Mono** 300/400/500 or 400/500 |
| `index` | JetBrains Mono 400/700 (again) |
| `city-lab-dc-v3`, `watershed-preview`, `search`, `index-pre-homepage`, `atlas-portal` | **Merriweather** (various). Not loaded on `research.html` |
| `preview/nodes-and-networks…` | DM Sans, Libre Baskerville |
| `teamdmv` | Playfair Display 400/700/900 |

**Computed `font-family` usage (declarations / files):** Inter 148/48; `monospace` fallback only 178/11; **DM Mono 132/6; JetBrains Mono 44/3**; DM Sans 25/1; Georgia 5; `var(--font-mono)` (Source Code Pro) **4/1**.

**Answers**
- **Inter 400/600/700 on every public page?** Yes via `header.js`, which also loads 500 and 800. Pages that don't run `header.js` (`preview/nodes-and-networks…`, `teamdmv`, `watershed`) don't get Inter from the header: nodes uses DM Sans, teamdmv Inter 400–700 + Playfair, watershed Inter 400/500/700.
- **Source Code Pro 500 available?** **No**, on any page. 400 only, from `footer.js`. The screenshots' loaded-font list shows `Source Code Pro 400` and `JetBrains Mono 400/700`, never 500.
- **Merriweather** is loaded on 3 public pages (`city-lab-dc-v3`, `search`, `watershed-preview`) and absent where v15/v4 expects long-form prose to use it (the report page uses Libre Baskerville).

**What has to change in `header.js`** (not applied): (1) replace the Inter URL with `wght@400;600;700` (**only after** the Inter 500 decision, Q5: 93 public rules use it); (2) add `Source Code Pro:wght@500` (and drop the 400-only load in `footer.js`, or load `wght@400;500`); (3) stop `header.css` importing JetBrains Mono (and then replace the 44 JetBrains and 132 DM Mono declarations); (4) decide whether Merriweather loads site-wide or per page (v15 L360 doesn't say); (5) the nav's 800 reference.

---

## Track G: Beat taxonomy vs `ATLAS_VIZ_COLORS`

*Checkpoint: Track G, 5 hardcoded lists + 2 data-driven vocabularies.*

**Plain answer: v15's colored beat dots cannot ship on a data-driven surface today.** Exactly **1** of the **79** distinct `topic` tags in `assets/data/creators-data.json` ("Sports") equals an `ATLAS_VIZ_COLORS` key (59 of 2,432 creators by first topic). **0 of 9** creator `group` values match a key. The only list that nearly lines up is the hardcoded homepage cluster-card set.

The 9 confirmed keys: Politics & Government · Local News · Technology · Business & Finance · Culture & Arts · Sports · Health · Environment · International.

| List | Where / source | Names | vs keys |
|---|---|---|---|
| Homepage cluster cards (`.cluster-name`) | `index.html` L1177–1352, **hardcoded** | Technology · Politics & Government · Climate & Environment · Local News · Business & Finance · Health & Science · Culture & Media · International · Sports | **6 exact** (Technology, Politics & Government, Local News, Business & Finance, International, Sports); **3 near** (Climate & Environment ≈ Environment, Health & Science ≈ Health, Culture & Media ≈ Culture & Arts) |
| Homepage db filter (`<select>`) | `index.html` L1404–1412, hardcoded | same 9 + "All Topics" | same as above |
| Homepage hero pills (`data-cluster` → display) | `index.html` L586–594, hardcoded; clusters computed by `TOPIC_MAP` (L1483) | Politics, Tech, Culture, Climate, Health, Food, Local, Media, World (cluster ids: Politics, Tech & Business, Culture, Climate & Science, Health, Food & Lifestyle, Local News, Media & Power, World News) | 1 exact (Health), 6 near, **2 none** (Food, Media) |
| Pulse beat pills | `pulse.html` L2278–2297, hardcoded tier 1 (12) + tier 2 (26) | Politics, Tech, Finance/Economics, Culture, Media/Power, Local News, World, Government Accountability, Climate/Environment, Science, Investigative, Health/Wellness · Law/Legal Issues, Food, Sports, Education, … | tier 1: 1 exact (Local News), 7 near, 1 probable (Science), 3 none (Media/Power, Government Accountability, Investigative). Tier 2: 1 exact (Sports); the rest none or probable (Immigration, Crime≈Criminal Justice) |
| Pulse heatmap colors | `pulse.html` L2634 `BEAT_COLORS`, hardcoded, mixes 10 beats and 4 platforms in one map | Tailwind-style hexes (`#2563eb`, `#7c3aed`, `#db2777`, `#ea580c`…) | **None are Tier 4 hexes**; it's a separate color system in live code |
| Search "field" groups | `search.html` L933 `FIELD_GROUP_COLORS`; creator `group` in data | Power & Politics, Money & Work, Science Health & Environment, Culture & Media, Civic Life, Social Issues (+ General News, Journalism Formats, Lifestyle & Personal Life in data) | **0 exact**; colors are brand secondary + Acid/Lime |
| Data-driven topic tags | `creators-data.json` `topic` (comma-separated), **79 distinct**: Politics 382, Local 236, Culture 230, Tech 218, Media/Power 149, Food 120, Travel 119, Health/Wellness 111, Climate/Environment 111, Finance/Economics 107… | | **1 exact** ("Sports") |
| Beat clusters on the Bluesky page | `bluesky-creator-intelligence.html` L550 `CLUSTERS` | own copy of the 9 hero clusters | same as hero pills |

Four different beat vocabularies in live code (long cards, short pills, Pulse pills, data topics) map to the same 9 keys differently. A beat dot needs one canonical mapping `topic → key` (Ryan's) and one display name per key. The 6 exact cluster-card names suggest someone already tried to align to the viz array there. **Recommendation:** treat dots as RED (blocked on Ryan's taxonomy mapping) with one possible early win on the homepage cluster cards if James rules on the 3 near-names (Q2).

---

## Track H: Deploy surface

*Checkpoint: Track H, repo root and docs searched.*

- **No Cloudflare config files**: no `wrangler.toml`, **no `_headers`**, `_redirects` only (67 lines; includes `/postcard`, `/pack`, `/knight-brief` 301s and a few 200 rewrites such as `/wire → /wire.html`).
- `README.md` L186–262 describes Pages build settings ("Build output directory: `/`") and security headers/CSP that **are not implemented**. `build-dist.sh` (copy-only allowlist; Cloudflare runs `sh build-dist.sh`, output `dist/`) is the real build, per `CLAUDE.md`. Treat the README's deploy and header sections as stale.
- **Nothing in the repo says whether preview deployments for non-main branches are on or off**, and no doc describes a "staging" site, even though v14 ("A staging audit found ~107 other colors"), v15 ("Review on staging") and the CSS comments ("open item for James to confirm exact value on staging") assume one. `WORKFLOW.md` L57: "Cloudflare auto-deploys from main branch within ~1 minute." Branches mentioned only in `README.md` L293 (feature branches). No `.github/workflows`.
- **For Justin to check in the Cloudflare dashboard:** Workers & Pages → the Atlas project → Settings → Builds & deployments → **Preview deployments** → are non-production branches deployed (All branches / None / Custom)? If On, a v15 branch gets a `*.pages.dev` URL for review before main. If Off, the only way to review is pushing to `main`, which is live. Also confirm what "staging" means in v14/v15.
- **Related risk:** `CURRENT_STATE.md` L58 records a prior session where the environment auto-committed (`6aa80a0 "update"`) and auto-pushed to `origin/main`, bypassing GitHub Desktop. If Justin is going to move fast and push a lot, confirm that auto-push isn't configured on this machine.
- **Build allowlist implication:** `build-dist.sh` publishes `./*.html`, `partners/`, `lab/`, `teamdmv/`, `watershed-preview-uhh7gdyn/`, `atlas-portal/*.html`, `assets/css|js|images|img`. Any new asset (e.g. `Atlas_logo_lockup_stacked_wht_web.svg`) under `assets/images/logos/` ships automatically.

---

## Track I: Visual baseline

*Checkpoint: Track I, 7 pages × 2 viewports = 14 PNGs, `screenshots/baseline/`.*

Full-page captures at 1440×900 and 390×844 (device scale 1), served from the repo root (not `dist/`) with a local static server. Fonts loaded from Google (network available). Capture log with heights and loaded font list: `screenshots/baseline/_capture-log.json`.

| Page | Files | Notes |
|---|---|---|
| Homepage | `home-1440.png`, `home-390.png` | |
| Pulse | `pulse-*` | |
| Research & Writing | `research-*` | |
| About This Project | `about-this-project-*` | |
| Partner page (`/partners/ahp`) | `partner-ahp-*` | |
| City Lab (`/city-lab-chicago`) | `city-lab-chicago-*` | |
| Long-form report with "Jump to" | `longform-nodes-and-networks-*` | The preview page (`/preview/nodes-and-networks-f348eb08/`) uses its own chrome: DM Sans + Libre Baskerville, `#faf9f5`, **no shared header or footer**, a sticky `.section-nav` and a "Jump to cohort" strip. 30,805px tall at 1440 |
| **Postcard: skipped** | none | `/postcard` is **retired** (July 2026) and 301s to `/` (`_redirects`); the file lives in `_deprecated/`. A screenshot would just be the homepage. Say the word if you want the deprecated file captured anyway |

Sizes: the two long-form PNGs are ~7MB each; the whole folder is ~28MB. Consider whether to commit it, or `.gitignore` the folder and keep it local.

---

## Found along the way (recorded, not fixed)

1. **The desktop header already overflows below ~1100px.** Measured: nav links total 581px at 40px gaps; the nav container overflows at 1100px and below, while the hamburger only appears at ≤768px (`header.css` L350). So 769–1100px is broken today. v15's SCP caps (+49px) would push the overflow up to 1280px unless gaps drop to 32px (+17px; fits at 1280). (Q1 evidence.)
2. **11 internal pages are deployed and indexable**: `build-dist.sh` copies `./*.html`, `atlas-portal/`, `lab/` and `partners/`. These have no `noindex`: `atlas-portal/index`, `google-form-template`, `atlas-signal-brief`, `atlas_pulse_intelligence`, `atlas_wire_intelligence`, `atlas_wire_review`, `beat-climate|finance|tech`, `chicago-analysis`, `chicago-survey`, `partners/_shell`, `partners/njlab copy`, plus `index-pre-homepage`. Only `/preview/` is `Disallow`ed in `robots.txt`. Probably unintended.
3. **`partners/nj-lab.html` and `partners/njlab.html` are duplicates, both public, both with a broken `variables.css` path** (also `njlab copy.html`). `partners/_reviewjames copy.html`, `CLAUDE copy.md`, `PARTNERS copy.md` are stray copies.
4. **`header.css` loads `@import` JetBrains Mono on every page** while `footer.js` loads Source Code Pro and `variables.css` declares Source Code Pro as `--font-mono`. The footer's `font-family: var(--font-mono)` works only after `footer.js` has loaded the 400 weight.
5. **`--focus-ring-light/dark` are dead variables** (0 uses) and inverted relative to v15.
6. **`--space-3xl` is 64px** in `variables.css` but 96px in v15/v11.
7. **`--color-text-header-dark: #000000`** is labelled "Header text always black — mode-invariant" and is a dark-mode alias for black; `--color-border-dark: #48484f` and `-hover: #606068` are off-system (these are why `#606068` ×70 shows in the gray census).
8. **Partner pages**: `body { padding-top: 72px }` leaves a 72px empty band above the sticky header (known; `START-HERE.md`).
9. **Footer still uses `Journalism_Atlas_wordmark_stacked_white.svg`**; `Atlas_logo_lockup_stacked_wht_web.svg` (v15 L573) isn't in `assets/images/logos/`. Header lockups (`..._blk_web.svg`, `..._wht_web.svg`) are present and wired.
10. **`README.md` says `assets/data/creators-master.csv` is the source of truth**, while `CLAUDE.md` says `creators-master.csv` (root). Not a v15 matter.
11. **`CLAUDE.md` ↔ `ATLAS-BRAND-GUIDE-v3.md` has an old database-size rule** ("1,718") while Pulse shows 2,432 and v4 says "about 2,400–2,500". Out of scope.
12. **Pulse `BEAT_COLORS`** (14 Tailwind-like hexes incl. platform names) is a second, unrelated color system.
13. **`atlas-portal/index.html`, `chicago-*.html`** carry their own `:root` with hardcoded `--black/--white` etc. Internal; ignore unless in scope.
14. **`.DS_Store`** tracked-and-modified issue from `START-HERE.md` was not reproduced (`git status` is clean).

---

## Appendix A: `assets/css/variables.css` `:root` blocks (verbatim)

Source: `assets/css/variables.css` as of HEAD `b1827fb`. Block 1 is `:root` (L15–309); block 2 is the 768px override.

```css
:root {

  /* =========================================
     BRAND COLOR PALETTE
     Primary palette from Style Guide 2026
     ========================================= */
  --color-acid-green:  var(--color-acid);   /* Acid: CTA/active. Fill-only on light surfaces (v14 § Greens by Surface) */
  --color-lime-green:  var(--color-lime);   /* Lime: hover/focus. Fill-only on light surfaces (v14) */
  --color-dark-olive:  var(--color-olive);   /* Olive: text, icons, thin strokes on light surfaces (v14) */
  --color-dark-gray:   var(--gray-cool-6);
  --color-light-gray:  var(--gray-cool-2);
  --color-black:       #000000;
  --color-white:       #ffffff;

  /* Legacy aliases — used throughout main.css; migrate over time */
  --black:       #000000;
  --white:       #ffffff;
  --light-gray:  var(--gray-cool-2);
  --dark-gray:   var(--gray-cool-6);
  --medium-gray: #999999;
  --acid-green:  var(--color-acid);   /* Legacy alias of --color-acid. (The old "acid on dark only" rule was never canon; see v14.) */
  --lime-green:  var(--color-lime);


  /* =========================================
     MONOTONE SCALES — v12 (Oct 2026)
     DESIGN-TOKENS-v14.md § Tier 2 — Monotones
     Site uses the Cool scale for semantic roles; don't mix scales on one surface.
     Step 4 is large text / UI / disabled only (3.2:1 on white), never body text.
     ========================================= */
  --gray-neutral-1: #ffffff;
  --gray-neutral-2: #efefef;
  --gray-neutral-3: #c6c6c6;
  --gray-neutral-4: #909090;
  --gray-neutral-5: #5e5e5e;
  --gray-neutral-6: #303030;
  --gray-neutral-7: #121212;
  --gray-neutral-8: #000000;

  --gray-cool-1: #ffffff;
  --gray-cool-2: #efeff4;
  --gray-cool-3: #c6c6cd;
  --gray-cool-4: #909097;
  --gray-cool-5: #5e5e64;
  --gray-cool-6: #303036;
  --gray-cool-7: #121218;
  --gray-cool-8: #000000;

  /* v12 semantic names that do not collide with existing tokens.
     DESIGN-TOKENS-v14.md § Semantic Color Assignments.
     The existing --color-bg / -text / -text-secondary / -muted / -border / -error
     definitions below are re-pointed to these scales in Phase 2a/2b. */
  --color-surface:        var(--gray-cool-1);
  --color-heading:        var(--gray-cool-8);
  --color-text-on-dark-2: var(--gray-cool-3);   /* secondary text on dark surfaces */
  --color-border-on-dark: var(--gray-cool-5);
  /* Green primitives (DESIGN-TOKENS-v14.md § Migrating color variables). Role variables point at these.
     Brand-palette names --color-acid-green / --color-lime-green / --color-dark-olive above are older aliases of the same values. */
  --color-acid:           #ceff00;
  --color-lime:           #97d600;
  --color-olive:          #5d7400;

  /* Role variables (v14). Use by what the element does, not by color:
     at-rest/active fill → --color-accent · hover fill → --color-hover · green text/icons/strokes on LIGHT → --color-accent-on-light
     inline links → --color-link / --color-link-on-dark · focus ring → --color-focus (dark) / --color-focus-on-light (light) */
  --color-hover:          var(--color-lime);    /* hover FILL (fill only on light surfaces) */
  --color-accent-on-light: var(--color-olive);  /* text, icons, thin strokes on light surfaces */
  --color-focus:          var(--color-lime);    /* focus ring on dark surfaces */
  --color-focus-on-light: var(--color-olive);   /* focus ring on light surfaces (lime fails 3:1 on white) */
  --color-link:           var(--color-olive);   /* inline link on light surfaces, underlined; hover step 8 */
  --color-link-on-dark:   #ffffff;              /* inline link on dark surfaces, underlined; hover lime */
  --color-on-error:       #ffffff;
  --color-display-dark:   #ffbc00;              /* dark-mode display accent (v12 Tier 5) */

  /* =========================================
     LIGHT MODE — Semantic Color Assignments
     DESIGN-TOKENS-v14.md § Semantic Color Assignments
     Use these tokens in all light-surface contexts.
     ========================================= */
  --color-bg:             var(--gray-cool-2);   /* Primary page background */
  --color-bg-card:        #ffffff;   /* Card / panel background */
  --color-text:           var(--gray-cool-6);   /* Primary body text */
  --color-text-header:    #000000;   /* Heading text — always black, any mode */
  --color-accent:         var(--color-acid);   /* Primary accent / CTA fill (v14): acid, fill only on light surfaces. Text/icons/strokes on light use --color-accent-on-light. */
  --color-accent-hover:   #5d7400;   /* Hover / active state — dark olive */
  --color-text-secondary: var(--gray-cool-5);   /* Secondary text on light surfaces */
  --color-muted:          var(--gray-cool-4);   /* Muted / disabled text and icons */
  --color-border:         var(--gray-cool-3);   /* Default border */
  --color-border-hover:   var(--gray-cool-5);   /* Border on hover */
  --color-error:          #f50000;   /* Error state — near-pure red */


  /* =========================================
     DARK MODE — Semantic Color Assignments
     Use on dark surfaces: dark footer, dark headers, dark cards
     ========================================= */
  --color-bg-dark:            var(--gray-cool-6);
  --color-bg-card-dark:       #000000;
  --color-text-dark:          var(--gray-cool-2);
  --color-text-header-dark:   #000000;   /* Header text always black — mode-invariant */
  --color-accent-dark:        var(--color-acid);   /* Primary accent / CTA — acid green, dark mode only */
  --color-accent-dark-hover:  var(--color-hover);   /* Hover on dark — lime */
  --color-muted-dark:         var(--gray-cool-3);   /* Secondary text on dark surfaces (step 3: 12.4:1 on black) */
  --color-border-dark:        #48484f;
  --color-border-dark-hover:  #606068;
  --color-error-dark:         #ff4422;


  /* =========================================
     CANVAS — Always-dark surface tokens
     Used in renderCanvas() and postcard canvas only.
     Not the same as dark mode — canvas is always #000000.
     ========================================= */
  --canvas-bg:             #000000;
  --canvas-text-primary:   #ffffff;
  --canvas-text-secondary: rgba(255, 255, 255, 0.55);
  --canvas-text-muted:     rgba(255, 255, 255, 0.4);
  --canvas-accent:         var(--color-acid);
  --canvas-divider:        rgba(255, 255, 255, 0.12);
  --canvas-border:         rgba(255, 255, 255, 0.08);


  /* =========================================
     VISUALIZATION COLORS
     D3 only — never use in UI chrome.
     Category → color assignments are in the JS constant ATLAS_VIZ_COLORS (ATLAS_VIZ_COLORS.md).
     These legacy CSS vars are superseded — do not add new --viz-* properties here.
     Reference: DESIGN-TOKENS-v14.md § D3 Visualization Color Array
     ========================================= */
  --viz-yellow:   #fff700;
  --viz-orange:   #ffaa00;
  --viz-pink:     #ff66ff;
  --viz-magenta:  #ff33cc;
  --viz-cyan:     #00e5ff;
  --viz-gold:     #806600;
  --viz-rust:     #b35100;
  --viz-purple:   #a100a1;
  --viz-berry:    #a1006c;
  --viz-blue:     #005ea3;


  /* =========================================
     TYPOGRAPHY
     DESIGN-TOKENS-v14.md § Typography — v7 May 2026
     Weights: 400 / 500 (Micro only) / 600 (H3) / 700 / 800.
     ========================================= */

  /* Font families */
  --font-primary:   'Inter', sans-serif;
  --font-mono:      'Source Code Pro', monospace;
  --font-editorial: 'Merriweather', serif;   /* reactivated Sept 2026 — DESIGN-TOKENS-v14.md v11 § Font Stack */

  /* Legacy alias */
  --font-ui: 'Inter', sans-serif;

  /* Type scale — v7 (Display 48 / H1 36 / H2 28 / H3 20 / Body 16 / Small 13 / Micro 11) */
  --text-display:  48px;   /* 800 · lh 53px */
  --text-h1:       36px;   /* 700 · lh 44px */
  --text-h2:       28px;   /* 700 · lh 35px */
  --text-h3:       20px;   /* 600 · lh 26px */
  --text-body-lg:  16px;   /* 400 · lh 26px — default reading size */
  --text-body-md:  14px;   /* 400 · lh 22px */
  --text-label:    14px;   /* 400 · lh 20px */
  --text-small:    13px;   /* 400 · lh 20px — floor for all UI text */
  --text-micro:    11px;   /* 500 · lh 15px — all-caps labels only; letter-space 0.08–0.1em */

  /* Legacy aliases */
  --text-title:  20px;   /* maps to H3 */
  --text-body:   16px;
  --text-data:   14px;
  --text-micro-legacy: 12px;   /* pre-v7 micro; do not use for new work */

  /* Line heights (computed from v7 ratios) */
  --lh-display:  53px;   /* 48 × 1.1  */
  --lh-h1:       44px;   /* 36 × 1.2  */
  --lh-h2:       35px;   /* 28 × 1.25 */
  --lh-h3:       26px;   /* 20 × 1.3  */
  --lh-title:    26px;   /* maps to H3 */
  --lh-body-lg:  26px;   /* 16 × 1.6  */
  --lh-body-md:  22px;
  --lh-label:    20px;
  --lh-small:    20px;   /* 13 × 1.5  */
  --lh-micro:    15px;   /* 11 × 1.4  */

  /* Letter spacing */
  --ls-display:  -0.25px;
  --ls-h1:       -0.25px;
  --ls-h2:        0px;
  --ls-h3:        0px;
  --ls-title:     0px;
  --ls-body-lg:   0.15px;
  --ls-body-md:   0.25px;
  --ls-label:     0.1px;
  --ls-small:     0.4px;
  --ls-micro:     0.5px;   /* Micro all-caps: use 0.08–0.1em in implementation */

  /* Font weights — 400 / 500 / 600 / 700 / 800 */
  --weight-regular:   400;
  --weight-medium:    500;   /* Micro labels only */
  --weight-semibold:  600;   /* H3 / card titles */
  --weight-bold:      700;
  --weight-extrabold: 800;


  /* =========================================
     SPACING — 4px base unit
     DESIGN-TOKENS-v14.md § Spacing & Layout
     ========================================= */
  --space-xs:   4px;    /* tight inline spacing, badge padding */
  --space-sm:   8px;
  --space-md:   16px;
  --space-lg:   24px;
  --space-xl:   32px;   /* v7: tightened from 40px */
  --space-2xl:  48px;   /* v7: tightened from 64px */
  --space-3xl:  64px;   /* kept for backward compat — not in v7 scale */

  /* Legacy aliases */
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --spacing-xl: 32px;   /* v7: tightened from 40px */


  /* =========================================
     BORDER RADIUS
     DESIGN-TOKENS-v14.md § Spacing & Layout
     ========================================= */
  --radius-base:  6px;    /* Cards, buttons, inputs */
  --radius-modal: 8px;    /* Modals — slightly softer */
  --radius-pill:  100px;  /* Filter chips, tags — always 100px */
  --radius-full:  50%;    /* Circular avatars */

  /* Legacy aliases */
  --radius-xs: 4px;
  --radius-sm: 6px;
  --radius-md: 8px;
  --radius-lg: 16px;


  /* =========================================
     LAYOUT
     DESIGN-TOKENS-v14.md § Max Content Width
     ========================================= */
  --max-width-layout:    1440px;   /* outer container — all pages */
  --max-width-card-grid: 1200px;   /* card grids — sits inside layout with margin */
  --max-width-text:       680px;   /* editorial/reading contexts — ~70 chars at 16px */


  /* =========================================
     ICON SIZES
     Material Symbols Outlined — opsz must match display size
     DESIGN-TOKENS-v14.md § Iconography
     ========================================= */
  --icon-sm:  20px;   /* opsz=20 — inline, tight contexts, tags */
  --icon-md:  24px;   /* opsz=24 — standard UI: buttons, nav, filters */
  --icon-lg:  40px;   /* opsz=40 — decorative, empty states, hero */


  /* =========================================
     COMPONENT: FOCUS RING
     Required on all interactive elements (accessibility).
     Never remove focus styles.
     ========================================= */
  --focus-ring-light:  2px solid #97d600;
  --focus-ring-dark:   2px solid var(--color-acid);
  --focus-ring-offset: 2px;


  /* =========================================
     Z-INDEX LAYERS
     ========================================= */
  --z-canvas:   1;
  --z-ui:       10;
  --z-overlay:  20;
  --z-sheet:    30;
  --z-modal:    40;


  /* =========================================
     TRANSITIONS
     ========================================= */
  --transition-fast: 150ms ease;
  --transition-base: 300ms ease;
  --transition-slow: 500ms ease;


  /* =========================================
     TOUCH / MOBILE
     ========================================= */
  --touch-target-min:       48px;
  --mobile-edge-margin:     16px;
  --safe-area-inset-top:    env(safe-area-inset-top);
  --safe-area-inset-bottom: env(safe-area-inset-bottom);
}
```

```css
/* =============================================
   MOBILE OVERRIDES — 768px and below
   ============================================= */
@media (max-width: 768px) {
  :root {
    --text-display: 40px;   /* stepped down from 48px desktop */
    --text-h1:      30px;   /* stepped down from 36px desktop */
    --text-h2:      24px;   /* stepped down from 28px desktop */
    --text-h3:      18px;   /* stepped down from 20px desktop */
    /* Body (16px), Small (13px), Micro (11px): same as desktop */
  }
}
```

---

## Appendix B: Proposed replacement for CLAUDE.md's design section (NOT APPLIED)

Replaces lines 56–81 (and the version references on lines 4, 22, 58, 105, 111–118). `-` lines are removed, `+` lines added.

```diff
 ## Design System
 
-All visual implementation references `DESIGN-TOKENS-v14.md` at the project root as the single source of truth. Its CSS implementation lives in `assets/css/variables.css` — the canonical token file, loaded before all other stylesheets.
+All visual implementation references `DESIGN-TOKENS-v15.md` (location: TBD, see "Open: where the spec lives") as the single source of truth. Brand voice and strategy: `ATLAS-BRAND-GUIDE-v4.md`. The CSS implementation of the tokens lives in `assets/css/variables.css`, loaded before all other stylesheets.
 
 **Do not infer or improvise colors, type sizes, spacing, or component states — look them up.**
@@ Non-negotiable rules
-- **Greens by surface (DESIGN-TOKENS-v14.md § Greens by Surface):**
-  - **Acid `#ceff00` and Lime `#97d600` on LIGHT surfaces = fill only** ...
-  - **On DARK surfaces** acid and lime are free within their roles: acid for CTAs and active states ..., lime for hover and the focus ring.
-  - **Dark Olive `#5d7400` on LIGHT surfaces ...
-  - **Focus ring follows the surface:** lime on dark, Dark Olive on light.
-  - One acid moment per composition; olive marking the active state on a light surface counts as that moment.
-  - Not canon: the older "acid on dark only / lime on light only" rule. v13 replaces it.
-  - **Primary CTA (v14):** acid fill at rest and active, lime fill on hover, black text throughout; ...
-  - **Inline links (v14):** olive + underlined on light (hover step 8); white + underlined on dark (hover lime). ...
-  - **In migration:** the site's `--color-accent` is still lime ...
+- **Green means interaction (DESIGN-TOKENS-v15.md § Component States).** Buttons, tags, instruction links and nav rest in monotones. Green appears on hover, press and selected. The only things that rest in green are body links on light surfaces (Dark Olive, underlined) and eyebrows on dark surfaces (Acid allowed).
+  - **Acid `#ceff00`**: hover, press and selected. **Fill only on light surfaces** (black text on top); fills, text, underlines and icons on dark. Never a success signal. No per-composition limit.
+  - **Lime `#97d600`**: keyboard focus ring on dark surfaces only. Not a hover color. Not used on light.
+  - **Dark Olive `#5d7400`**: the green for text, icons, underlines and thin strokes on light surfaces (hover and selected text, current nav item, body links, focus ring). Never a fill. Not used on dark.
+  - **Focus ring follows the surface:** Lime on dark, Dark Olive on light, `2px`, offset `2px`.
+  - **Buttons:** two styles, both 44px, 6px radius, Inter 600 15px, sentence case. Primary: step-6 fill, white text, step-5 outline (step-4 on dark); selected = white. Secondary (filters, repeated options): outline only; selected = black (white on dark). Both turn Acid on hover and press.
+  - **Links:** instruction links are Source Code Pro 500 13px caps ending in ` →` (step 6 → Dark Olive underlined; white → Acid underlined). Body links are Dark Olive underlined on light (hover black), white underlined on dark (hover Acid).
+  - **Tags:** Source Code Pro 500 12px caps, 0.08em, fill or outline never both, never clickable, no hover. Beat tags carry color on an 8px dot from `ATLAS_VIZ_COLORS` only.
+  - **No color coding by section or content type.**
+  - **Migration state:** primitives `--color-acid/-lime/-olive` exist; role variables point at them. `--color-hover` is an alias of Acid. Migrate each use by role.
+- **Gray scales (v15):** the website uses the **Neutral** scale (`--gray-neutral-*`) for every semantic gray role. **Cool** (`--gray-cool-*`) is for graphics only (charts, infographics, illustrations); an embedded graphic is its own surface. Don't mix scales on one surface.
 - **Site header = `#ffffff` (default, matches the live site) or `#000000`** ... [keep; add: hover underlined; selected = Dark Olive (white header) or Acid (black header), 2px underline, offset 8px]
-- **Body copy minimum 16px** — Small (13px) is the floor for all UI text. Micro (11px) for all-caps labels only (weight 500 min, letter-spacing 0.08–0.1em). Never below 13px for any readable content.
+- **Body copy minimum 16px.** Small (13px) is the floor for UI text. All-caps UI labels are Source Code Pro 500: **Label 13px** (eyebrows, instruction links, 0.08–0.12em) and **Tag 12px** (tags, badges, card meta lines, 0.08em). 12px Source Code Pro is the only size allowed below 13px.
-- **Material Symbols Outlined only** — no legacy Material Icons; Filled variant reserved for active states only
+- **Material Symbols Outlined only.** Filled only for active toggle/action icons (save, follow, bookmark). Navigation and section icons stay outlined at every state.
-- **4px base spacing unit** — spacing scale: xs 4px / ... / 2xl 48px
+- **4px base spacing unit**: xs 4 / sm 8 / md 16 / lg 24 / xl 32 / 2xl 48 / 3xl 96.
-- **Font weights: 400 / 500 / 600 / 700 / 800** — 500 for Micro labels only; 600 for H3/card titles; do not introduce 900 or other weights
+- **Font weights: 400 / 500 / 600 / 700.** 500 is for Source Code Pro labels and tags only; 600 for H3/card titles and buttons. 800 and 900 are retired.
-- **Border radius: 6px for cards/buttons/inputs; 9999px for pills/tags**
+- **Border radius: 6px for everything rectangular** (cards, buttons, inputs, tags, badges). Pills are retired. `50%` only for photos, avatars and status dots.
@@
-Load order ... (unchanged)
+Load order ... (unchanged)
-- Injects Inter + Material Symbols fonts if not already loaded
+- Injects Inter (400/600/700), Source Code Pro (500) and Material Symbols if not already loaded   [after the font work lands]
@@ header / contact lines
-*Owner: Justin | Design system: James (james@happicamp.com)*
+*Owner: Justin | Design system: James (james@journalismatlas.com)*
-*Last updated: October 6, 2026 (design tokens now v14)*
+*Last updated: <date> (design tokens now v15; brand guide v4)*
-| `DESIGN-TOKENS-v14.md` | Before any CSS/styling work |
-| `ATLAS-BRAND-GUIDE-v3.md` | Before writing any user-facing copy ... |
+| `DESIGN-TOKENS-v15.md` | Before any CSS/styling work |
+| `ATLAS-BRAND-GUIDE-v4.md` | Before writing any user-facing copy ... |
@@ also fix (not v15, but wrong today)
-- `main.css` ← Primary stylesheet for index.html only
+- `main.css` ← used by `search.html` (and the archived `index-pre-homepage.html`)
-All pages above have been swept to the design token system ... no canonical token redefinitions inline. Design sweep completed April 2026.
+(delete: 14 pages redefine canonical names inline; 7 public pages don't load variables.css; see docs/design/v15-discovery)
-| `nj-lab.html` | ... |
+| `partners/nj-lab.html`, `partners/njlab.html` | NJ lab (two live copies; pick one) |
```

*Open: where the spec lives.* CLAUDE.md, WORKFLOW.md and every comment point to the repo root. v15 says it is "committed to repo". Pick one path (root, as today, or `docs/design/`) and update the one line.

---

## Appendix C: Verification of scanner heuristics

- **Surface (light/dark) in static CSVs** is a heuristic. The runtime CSV is authoritative.
- **Chrome vs graphics** uses selector names and JS context. Spot-checked: `pulse.html` heatmap, `watershed` SVG and nj-lab viz are graphics; `beat-*` `legend-dot` swatches are graphics; everything else is chrome.
- **Hanken and `#ff9600` zero-hit result** was cross-checked with plain `grep -rIil` over the repo (excluding `dist/`, `.git`, `_deprecated/`): zero in site code.
- **Elements per page** in Track D runtime counts repeat for JS-rendered lists (`bluesky-creator-intelligence` renders ~550 creators). Use unique selectors and page counts.
