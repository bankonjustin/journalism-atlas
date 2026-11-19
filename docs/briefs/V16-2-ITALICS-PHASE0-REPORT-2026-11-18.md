# v16.2 Italics: Phase 0 Report

*Read-only verification, November 18, 2026. Repo: `~/Developer/atlas/journalism-atlas`. This report is the only file written.*

## Verdict (summary)

**Raise with James before saying yes**, on three items. Each is a question or note, not a conflict with a design value. The package itself is clean: no value changed and nothing from v16.1/v5.1 was lost. Details at 0.9.

---

## 0.1 Repo state

- Branch: **`main`** (tracking `origin/main`). Working tree clean (`git status` shows nothing).
- Last three commits on `main`: `539876e Update CURRENT_STATE.md`, `da4b2ef push`, `310d2a8 farhi: round 5 (chain spine, recodes, interim hero, table cleanup)`.
- **Justin must create a branch in GitHub Desktop before Phase 1** so Cloudflare builds a preview.

Package location: the files are loose in `~/Downloads/` (no `v16.2-package/` folder). All six are present there.

## 0.2 Package integrity

Diffed repo `DESIGN-TOKENS-v16.1.md` against `DESIGN-TOKENS-v16.2.md`, and `ATLAS-BRAND-GUIDE-v5.1.md` against `ATLAS-BRAND-GUIDE-v5.2.md`.

**Nothing was removed.** Every line that differs is an addition or a version/reference rewording. Justin's October amendments carried through, because v16.1 and v5.1 in the repo have no lines absent from v16.2/v5.2.

**No color, size, weight, spacing or radius value differs.** The only value-like additions are the `html { font-synthesis: weight; }` line in the font tokens and the new italic weights.

(a) Changes listed in "What changed in v16.2" / v5.2: Inter Italic 400/600/700; Merriweather italic 400 and 700 widened to inline italics; Source Code Pro upright and the `mono-italic` check; `font-synthesis: weight`; partner italics; N&N published path and partner names; editorial style as a canonical file; the version/title/date references.

(b) Changes not listed in the summaries (all small, all in scope):
- Tokens, Font Loading: Merriweather italic 400 is now loaded **always** on editorial pages, "since titles of works use it" (v16.1 said only if the prose used it).
- Tokens, Enforcement: an added sentence that Inter/Merriweather italics pass the `font-family` rule; `.github/CODEOWNERS` list now includes the editorial style.
- Tokens, Accessibility: "Italics never carry meaning on their own"; markup rule (`<cite>` titles, `<em>` emphasis, `<i>` other) and "pages don't add their own `font-style` rules for them."
- Tokens, Typography: an "Italic (v16.2)" line in the component list.
- Guide: a new "Editorial style" subsection (Section 2), a Section 6 line on slides and PDFs, a Section 7 "Editorial" bullet, and a Governance row for copy style.
- Guide Section 7: the N&N line changes from "publication planned for mid-October" to "published at journalismatlas.com/nodes-and-networks/."

## 0.3 Nodes and Networks

**`nodes-and-networks/` does not exist at the repo root.** It is a build output:
- `build-dist.sh` runs `python3 nn/build.py` (from `nn/content/copy.md` and `nn/src/*.tpl.html`) and copies the result into `dist/nodes-and-networks/`. If Python is too old, it falls back to the committed copy at `nn/built/nodes-and-networks/`.
- `dist/` and `nn/_out/` are git-ignored. `nn/built/nodes-and-networks/` is committed (contains `index.html`, `embed/`, `explorer/`, `media/`).

Other paths in the v16.2 Exceptions table:

| Path | Exists |
|---|---|
| `nodes-and-networks/` | **No** (build output only; see above) |
| `preview/nodes-and-networks-*` | Yes (`-edition-e852c5c5`, `-f348eb08`) |
| `preview/nn-launch-kit/` | Yes (also `nn-launch-kit-staging/` per `check_brand.py`) |
| `assets/nn5/` | Yes |
| `nodes-networks-v5/` | **No** in this repo (the memory notes say the builder lives outside the repo) |
| `tools/preview-build/` | Yes (no HTML/CSS/JS files found) |

Fonts and italics by N&N surface:

- **Published landing, embed and explorer (`nn/src`, `nn/built`)**: load `/assets/css/variables.css`, `components.css`, `header.css` and `/assets/js/header.js`. They use `font-family: Inter` and have **no Google Fonts link and no partner face**. `font-synthesis: weight` will reach them. The landing and embed templates contain no italic markup; the explorer has 2 `<i class=...>` swatch elements (not text italics). **The published report is Inter on the Atlas stack, not Inter Tight / Source Serif 4.**
- **`assets/nn5/edition.css`** (used by the `preview/nodes-and-networks-edition-*` pages): `@font-face` for Inter Tight (roman only), Source Serif 4 roman, and **Source Serif 4 Italic (loaded)**. So its `<em>` text keeps a real italic. Inter Tight has no italic loaded.
- **`preview/nodes-and-networks-edition-e852c5c5/index.html`**: 12 `<em>` plus ~15 other italic markers. Whether each sits in Source Serif 4 (italic loaded) or Inter Tight (not loaded) needs a rendered check; **I did not resolve this per element.** It does not load `variables.css`/`header.js` per the grep, so `font-synthesis` only reaches it if its own CSS sets it.
- **`preview/nodes-and-networks-f348eb08/index.html`** (earlier preview): loads Libre Baskerville with italic 400, plus DM Sans (400;500;600;700, no italic) and an embedded `NNFig DM Sans`. It sets `.masthead-sub { font-style: italic }` and `em { font-style: italic }`. The italic Libre Baskerville is loaded; any italic in DM Sans text would be affected.
- Figure JS (`assets/nn5/js/figs/*.js`, `nav.js`) uses `<i>` only as empty swatch/dot elements, not text italics. `kaleido.js` has no text italic in its matched lines.

At-risk N&N italics (italic file not loaded) are therefore **limited to the preview/earlier-preview pages** and need a rendered check. Nothing on the published path is at risk.

## 0.4 Fonts today

`assets/js/header.js`:

```
60: ensureFont('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
61: ensureFont('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,400,0,0');
64: ensureFont('https://fonts.googleapis.com/css2?family=Source+Code+Pro:wght@500&display=swap');
```

**Not as the brief assumed:** Inter is requested at `400;500;600;700`, with 500. The brief replaces it with `ital,wght@0,400;0,600;0,700;1,400;1,600;1,700`, which drops 500. The repo has ~490 `font-weight: 500` declarations (CSS and HTML, excluding dist/deprecated); many are Source Code Pro's weight, but I did not split them from Inter uses.

Merriweather is loaded at page level, not in `header.js`:
- `watershed/index.html:23` and `watershed/methods/index.html:21`: `family=Inter:wght@400;500;700&family=Merriweather:ital,wght@0,400;0,700;1,400`. Both pages also load `header.js`. So Watershed already requests its own Inter (no 600, no italic) and Merriweather (italic 400 only, roman 700).
- Others: `city-lab-dc-v3.html` (italic 400 loaded), `search.html` (400 only), `atlas-portal/index.html` (400;700, no italic).

Watershed bold italic: **none found** (no `<strong><em>`, `<em><strong>`, `<b><i>` or `<i><b>` in `watershed/`). Prose rules are `.prose em{font-style:italic}` and `.prose strong{font-weight:700}`. The Merriweather italic 700 request is not needed. Merriweather `0,700` (roman bold) is present.

## 0.5 Other italics at risk

Live (non-deprecated, non-N&N) pages with italic markup whose own font is not an italic-loaded face:

| Page | Font in play | Note |
|---|---|---|
| `index.html` | JetBrains Mono (mono rules) | italics would turn upright |
| `city-lab-chicago.html`, `bluesky-creator-intelligence.html`, `city-lab-dc-v3.html`, `latin-america-lab.html`, `partners/njlab.html`, `partners/nj-lab.html` | DM Mono (mono rules) | page-level DM Mono has no italic loaded |
| `partners/cillizza.html`, `jessica-stahl.html`, `ahp.html`, `emily-atkin.html`, `icfj.html` | Georgia (system serif) | local Georgia has a real italic, so probably unaffected |

These are all off-allowlist fonts already counted in the baseline. The ones that turn upright are mono, which is the v16.2 intent. `atlas-portal/google-form-template.html` (Roboto) has **no italic markup**, so nothing is at risk there. I did not trace every `<em>` to its computed font, so treat this list as a first pass; the preview check is the real test.

## 0.6 Mono class list

`grep var(--font-mono)` results:
- CSS: `assets/css/research-hub.css:12` `.rh-eyebrow`, `:19` `.rh-meta`; `assets/css/header.css:369` `.footer-tagline`, `:370` `.footer-col-title`, `:377` `.footer-copy`, `:379` `.footer-legal a`.
- HTML (4 files): `for-brands.html:47` `.tag`; `pulse.html` (many): `.signal-band-eyebrow`, `.signal-beat-tag`, `.signal-reason-tag`, `.signal-card-meta`, `.field-summary-draft`, `.audience-bridge-label`, `.masthead-dateline`, `.story-stack-beat.no-filter`, `.beat-map-label`, `.pulse-ticker-item-beat`, `.stat-pill`, `.section-eyebrow`, `.beat-tag`, `.platform-tag`, `.post-date`; plus the other two files in the 4-file list, which I did not itemize.

**No existing rule sets `font-style: italic` or `oblique` together with the mono font.** `assets/css` has no `font-style: italic` at all.

Header.css footer rules use 9px/10px sizes: already baseline violations, not part of this change.

## 0.7 Build check baseline

`python3 scripts/check_brand.py`: **pass. 2,392 violations in 56 files; baseline allows 2,392.** Per-file counts are in `scripts/brand-baseline.json` (largest: `city-lab-chicago.html` 315, `index.html` 304, `bluesky-creator-intelligence.html` 139, `atlas-signal-brief.html` 138, `atlas_wire_intelligence.html` 94, `mobile.html` 78, `assets/css/main.css` 76, `search.html` 76).

How the script works:
- **Exception paths** are a Python tuple `EXCLUDED` (prefix match). It already contains `preview/nodes-and-networks-`, `preview/nn-launch-kit/`, `preview/nn-launch-kit-staging/`, `assets/nn5/`, `nn/`, `nodes-networks-v5/`, `tools/preview-build/`, `dist/`, plus the Google Form mock-up path.
- **`nodes-and-networks/` as a root path is not listed, but it is not needed**: the published copy lives under `dist/` and `nn/built/`, both already excluded. Adding a root `nodes-and-networks/` entry would be harmless and covers a future checked-in copy.
- **Google Fonts parsing:** `GF_FAMILY = [?&]family=([A-Za-z0-9+ ]+)` captures family names only; **axes (`ital`, `wght`) are ignored**. So Inter/Merriweather `ital` requests already pass; the "accept `ital`" half of Step 4.1 needs no code. The "reject `ital` for Source Code Pro" and `mono-italic` rules are **new code** and go next to the font checks in `scan()` (around the `FAMILY_DECL` / `GF_FAMILY` / `FONTFACE` loop) and use `RULEBLOCK` for rule-level detection.
- The docstring and `build-dist.sh` failure message still say v16, not v16.1/v16.2.

## 0.8 Version references

19 files outside the archive match `v16.1` or `v5.1`.

**Current canonical reference, will update:**
- `CLAUDE.md` lines 4, 17, 26, 27, 61, 75, 94, 113, 119, 121, 124
- `WORKFLOW.md` lines 11, 36, 59, 68, 69
- `START-HERE.md` lines 5, 29 (line 29 says v5.1/v16.1 live in `docs/design/`)
- `docs/design/CLAUDE-DESIGN-RULES.md` lines 3, 5, 25, 27, 31, 35 (and the font section at lines 17-23, which needs the Step 1.4 restatement)
- `for-brands.html:28,58,59` and `pulse.html:581` (comments that point at the tokens file)
- `chicago-survey.html:602` comment points at the tokens file (the "v16.1: dark surface" part is historical)

**Historical, leave:**
- `docs/design/DESIGN-TOKENS-v16.1.md` and `ATLAS-BRAND-GUIDE-v5.1.md` themselves (they move to the archive)
- `START-HERE.md:8,10` (v16.1 level-set history), `docs/design/DESIGN-STATE-2026-10-31.md`, "v16.1: replaces `#f50000`" style notes, `for-brands.html:44,46,89` and `pulse.html:598` where "v16.1" describes when a rule began.

**Not found by the brief's grep:** `variables.css` and `check_brand.py` comments reference `v16` (not `v16.1`), so the brief's step does not touch them. `build-dist.sh` also says `DESIGN-TOKENS-v16.md`.

`.md/.js/.py/.html` only: the brief's grep omits `.css` and `.sh`; I included both and found nothing extra beyond the `v16` cases above.

## 0.9 Verdict: Raise with James before saying yes

1. **`header.js` loads Inter 500 today.** The brief's replacement URL has no 500, so every Inter weight-500 rule would fall to a neighbouring weight. v16 already calls Inter 500 off-system, so this may be intended, but it can show as a visible change (acceptance check 7). Ask James whether to drop 500 or keep `0,500;1,500` for now.
2. **Watershed loads its own Inter and Merriweather links** (Inter 400;500;700, no italic, plus `header.js`). The brief covers only the Merriweather request. Ask whether the page-level Inter link should go (header.js now supplies Inter Italic).
3. **`nodes-and-networks/` isn't a repo path, and the published report uses Inter on the Atlas stack,** not Inter Tight / Source Serif 4 as the Exceptions row says. Acceptance check 6 holds in practice, and no code change is needed. James should know the row describes the previews, not the published page.

Smaller notes (no action needed from James): the unlisted (b) items in 0.2; at-risk italics on DM Mono / JetBrains Mono pages (0.5); the preview pages need a rendered check for Inter Tight italics (0.3); `check_brand.py` needs new code for `mono-italic` (0.7).

Phase 1 has not started.
