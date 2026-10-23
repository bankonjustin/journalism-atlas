# V15 Session 2: handoff checkpoint (after C5)

*Written Oct 23, 2026, mid-session, so the work can continue in another environment. Read this, then `docs/design/v15-session-2/` (this folder), the Session 2 brief Justin has, `docs/design/DESIGN-TOKENS-v15.md` § Component States, and `docs/design/v15-discovery/` for the worklists.*

## Where things stand

Branch `main`, **everything below is committed and already pushed** (Justin's GitHub Desktop picked it up; `origin/main` was in sync at 09:21):

| Step | Commit | What |
|---|---|---|
| F1 | `cea8ebd` | `lists.html` links `variables.css` (footer +64px, expected) |
| F2 | (report only) | nj-lab header with the patch is white like other partner pages: `docs/design/v15-session-2/screenshots/f2/F2-compare.png`. Justin decides; patch for nj-lab/njlab is `docs/design/v15-session-1/C4-held-back.patch` (will need hand-applying, line context moved) |
| F3 | `9633dfa` | removed `partners/njlab copy.html` and `index-pre-homepage.html` (nothing linked them) |
| F4 | `89e0ede` | `_shell` noindex rule in `_headers`. **It was overwritten** by whatever builds the Nodes and Networks edition (it rewrites `_headers`), and that overwrite was pushed in `e7b6e2c`. Re-added in the commit that adds this file; it will be clobbered again unless the NN5 build keeps the rule. |
| C1 | `bbe672b` | `assets/css/components.css` linked on 34 public pages |
| C2 | `a1403a1` | global `:focus-visible` rings; `.on-dark` on 69 dark containers + footer; removed `outline:none` from text inputs |
| C3 | `3d15f48` | `--color-hover` = Acid alias (zero hazards found) |
| C4 | `25691b0` | primary buttons (31 content-page buttons + header Search) |
| C5 | in `e7b6e2c` | secondary buttons + `assets/js/components.js` (aria sync). **Justin's "commit" `e7b6e2c` swept C5 in with his NN5 work, so C5 has no clean commit of its own.** It is verified (see below). |

## Done-and-verified facts worth knowing
- Session 2 "before" screenshots: `docs/design/v15-session-2/screenshots/before` (1440 + 390, gitignored; may not exist in a new environment).
- C4: 67 primary buttons match spec at rest and hover on all 40 pages. C5: 258 secondary buttons match spec (rest, selected, hover). A computed-style diff of every element outside the migrated components (`tools/domdiff.py`) shows only animation noise.
- Known, expected: the header grows 3px on every page (44px Search button next to a 41px field). Rows of filter chips are taller and wrap more at 390px: see `C5-wrap-at-390.txt` (tuple = file, container, buttons, rows before, rows after).
- `mobile.html` has its own `<header class="header">` that overlaps the shared header; the header Search button can't be hovered there. Pre-existing.

## What's left (in the brief's order)
- **C5b (DEFAULT, own commit):** outline "ghost" companions beside a primary, treated as Secondary: `.btn-ghost` (research 4, latin), `.btn-ghost-white` (index), `.cta-ghost` (nj-lab, excluded), and `submit-thanks.html` (both buttons: it defines its own `.btn`, so it was *not* linked to components.css; link it and migrate its primary "Explore The Atlas" and secondary "Submit Another" together). Flag as a James open item.
- **C6 links:** body links (scoped prose containers, not global `a`); instruction links to `.link-instruction` (~37 patterns, 124 links, list in `v15-discovery/inventory/e_arrow_links.csv` and `tools/worklist.py` output); arrows typed as text ` →`; report same-destination wording differences; **C6b** footer links (white, Acid + underline on hover; keep typeface/size).
- **C7 header nav:** states per v15; add `aria-current="page"` in `header.js` (none today); typeface stays Inter; no spacing change.
- **C8 report "Jump to":** `preview/nodes-and-networks-f348eb08/index.html` is *generated* by `tools/preview-build` (edit the generator, not the HTML). Restyle its own `.section-nav` / `.cohort-strip` to v15's white header spec; don't move it to the shared header; report what that would take. Note Justin has a newer edition at `preview/nodes-and-networks-edition-e852c5c5/` (his own work, don't touch).
- **C9 remaining green at rest** (re-run the rest-state scan: `v15-session-1/` approach, runtime script lives in `tools/` as `hovercheck.py`/see `v15-discovery` Track D) and **C9b** icon-only/toggle buttons DEFAULT.
- **C10 optional:** header overflow below ~1100px (hamburger breakpoint). Mark "review before push". The 44px Search button makes it slightly worse.
- **Outputs still to write** in this folder: `V15-SESSION-2-REPORT.md`, `REVIEW-SHEET.html`, `JAMES-OPEN-ITEMS.md`, `SESSION-3-HANDOFF.md`; whole-session verification (green-at-rest zero, Lime only as dark focus ring, contrast table, 390px `:active` tap check, full 40-page diff, dead-CSS list by file).

## Decisions and defaults taken so far (for JAMES-OPEN-ITEMS)
1. **Dark surfaces** use a container class `.on-dark` (or `data-surface="dark"`), not guessed container names; custom-property variants with `:where()` so they add no specificity.
2. **Header Search button** is implemented in `header.css` (primary spec with literal fallbacks), not via `.btn` classes, because `header.css` loads on pages without `components.css` (nj-lab, internal pages).
3. **Selected-state ARIA** via one shared observer (`components.js`) rather than editing ~40 page handlers.
4. **UNSURE, left alone:** homepage hero `.hcn-pill` beat pills (colour-matched to the canvas clusters; graphics legend), underline tab strips (`.tab-btn`, `.analysis-tab`), `.beat-more-btn`, `.clear-filters*`, `.carousel-btn`, press/cite chips, ghost buttons (until C5b), `teamdmv` (own red/blue system), nj-lab pages (no components.css; broken `variables.css` link, pending F2).
5. Header Search 27px to 44px and hero button on black going gray are flagged for James (his questions 14 and the dark-primary concern).

## Gotchas
- **Justin is editing the same working tree** (Nodes and Networks edition: `assets/nn5/*`, `preview/nodes-and-networks-edition-*`, `_headers`, `CURRENT_STATE.md`) and GitHub Desktop commits whatever is there. Stage by explicit path only: `tools/stage_mine.sh` allow-lists pages, `assets/css/*.css`, `assets/js/{header,footer,main,components}.js`, `CLAUDE.md`. Never `git add -A`. Never commit `CURRENT_STATE.md`, `_headers`, `assets/nn5`, `preview/nodes-and-networks-edition-*` unless asked.
- Don't edit site files while a screenshot run is in progress (runs read the working tree).
- Page-level CSS beats `components.css` at equal specificity (it loads first). `migrate.py` strips visual declarations from the old rules; check the result per page. JS that assigns `className` or builds `class="x${...}"` strings needs hand edits (done for Pulse, Bluesky, search, wire).
- `tools/` scripts expect the scratchpad paths I used (`/private/tmp/claude-502/.../scratchpad`); edit `REPO`/`SCR` in `atlasscan.py` and `s1shot.py`. Playwright is the Python package with cached Chromium. `search.html` full-page screenshots are unreliable (300,000px tall): compare it with `tools/slices.py`.
- Animated regions (homepage hero canvas, Bluesky map, Research carousel, Pulse dots) always differ between runs; use a before/before2 noise mask (`cmp2.py`).
