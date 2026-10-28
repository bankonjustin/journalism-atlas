# V16 Install Notes for James

*Agenda for Justin's walkthrough with James · October 27, 2026 · Written by Claude Code from `V16-FOUNDATION-INSTALL-BRIEF-v1.0.md`*

Everything here is factual and short. The install changed no visible page.

## 1. Installed as written

- `DESIGN-TOKENS-v16.md` and `ATLAS-BRAND-GUIDE-v5.md` in `docs/design/`; your three briefs in `docs/briefs/`.
- Archived with the "Superseded" header line: `DESIGN-TOKENS-v15.md`, `ATLAS-BRAND-GUIDE-v4.md`, `ATLAS-BRAND-GUIDE-v3.md` (was in the repo root) and `pulse_tokens.md` (now `pulse_tokens-2026-10-26.md`), all in `docs/design/archive/`.
- `CLAUDE.md` 2a, 2b, 2c, 2f, 2h. `WORKFLOW.md` 3a–3e. Your Step 4 cleanup: README design section, START-HERE "For James" (moved to `docs/design/archive/START-HERE-v14-items-2026-10-06.md`), the duplicate `james-design-principles` copy, the SESSION-3 handoff marks, both ledger headers.
- `variables.css`: the v16 font block, size variables and fallback faces, exactly as in your Step 5. `--font-ui` and the off-scale size variables are removed. No live page used any of them.
- The brand check, with every original rule, allowlist, exclusion and mode kept.

## 2. Amendments (Justin decided; for your review)

**Design rules in their own file** (`docs/design/CLAUDE-DESIGN-RULES.md`). Your 2d (locked rules), 2e (typography) and 2g (what changes only with a new token version) moved out of `CLAUDE.md` into this file, which is under your review. `CLAUDE.md` points to it from the required-reading table and the top of `## Design System`. Why: it lets you own the design rules without owning all of `CLAUDE.md`, which holds product and build notes. One bullet changed: the protected-files list is the narrowed CODEOWNERS list (item 6).

**B1, 4- and 8-digit hex.** `#rgba` and `#rrggbbaa` are now checked. The base color is compared with the palette: not in it is `color`; in it is `color-alpha`, for your review.

**B2, functional colors (re-scoped Oct 28).** `rgb(`, `rgba(`, `hsl(` and `hsla(` are `color-func`, with this scope: pure white or black (any alpha) is flagged **only as a text color** (`color`, `-webkit-text-fill-color`, `caret-color`, `fill`/`stroke` on SVG or canvas text); in shadows, borders, backgrounds and overlays it is allowed. Any other `rgb`/`hsl` value (for example Acid at 20% alpha) is still flagged wherever it appears, because it can't be mapped to the palette. Fixtures cover both cases. Known gaps: a text color set through a custom property (`--x: rgba(...)` used as `color: var(--x)`) isn't caught; text-versus-shape detection for `fill`/`stroke` is heuristic.

**B3, named colors.** CSS named colors are `color-name` when they are the value of a color property or attribute (CSS properties, SVG `fill`/`stroke`, D3 `.attr`/`.style`, `.style.color`, canvas `fillStyle`/`strokeStyle`). Not flagged: `white`, `black`, `transparent`, `currentColor` and the CSS-wide keywords. Two small additions beyond the brief's list: `.style.background`/`backgroundColor`, and any object's `.fillStyle`/`.strokeStyle`, not only `ctx`.

**B4, hex false positives.** A `#` match is skipped after `href=`, `url(`, `querySelector(`, `querySelectorAll(`, `closest(`, `getElementById(`, and when a `{` follows on the same line (a CSS selector). The selector lookahead also stops at quotes, `<`, `>` and `$`, so `style="color:#f00">{{COUNT}}` is still caught. On today's tree this changed no existing count.

**B5, `--tight`.** Same as the default mode, and also fails when a count is below its baseline or the baseline lists a file that is gone. CI uses it. The default mode, used by `build-dist.sh`, is unchanged.

**B6, `--guard-baseline <ref>`.** CI only. Fails if any baseline count is higher than at `<ref>`, unless `scripts/check_brand.py` itself changed. A missing baseline at the ref passes; a ref git can't find exits 2 instead of passing silently. Caveat: the exception uses `git diff <ref> -- scripts/check_brand.py` (two-dot). If `main` gains a change to `check_brand.py` after a branch started, that branch would also see a difference and be allowed to raise counts. Worth a three-dot comparison later if it matters.

**B7, serif path.** No long-form report page exists in the repo (Nodes and Networks is excluded). `SERIF_ARTICLE_PATHS` stays `("watershed/",)` with a comment to add the report path when the first page is built.

**CODEOWNERS: deferred.** No `.github/CODEOWNERS` file exists yet, because James's GitHub username isn't known. The narrowed list is ready to write when it is: `/docs/design/`, `variables.css`, `check_brand.py`, `brand-check.yml` and CODEOWNERS itself; not the baseline (the guard blocks increases), `build-dist.sh`, `_headers`, `CLAUDE.md`, `WORKFLOW.md` or the rest of `.github/`. Until the file exists, the ruleset's "require review from Code Owners" does nothing, so design-file changes need James's review by agreement, not by GitHub. `brand-check.yml` is kept and still enforces the check and the baseline guard.

## 3. Where the repo differed from your brief

- **Line numbers:** every `CLAUDE.md` anchor matched. `variables.css` 169–176 matched; the size block runs 177 (comment) to 192. Both were replaced in full.
- **Extra edit:** `START-HERE.md` line 32 still cited `BRAND-GUIDE-v4`/`TOKENS-v15` outside "For James", so your acceptance grep would have failed. Rewritten to cite v5/v16 and the archive folder.
- **README:** "Google Fonts" and "Material Icons" appear twice (Libraries and Credits). Libraries now says "Fonts and icons: Inter, Source Code Pro, Merriweather (articles only); Material Symbols Outlined". Credits now name the three families and Material Symbols Outlined.
- **`james-design-principles`:** only `docs/james-design-principles.pdf` was deleted. `_reference/` keeps the `.md` and `.pdf`. There was no root copy.
- **`WORKFLOW.md` last bullet** pointed to a `CLAUDE.md` section that no longer exists; it now points to `CLAUDE-DESIGN-RULES.md`.
- **`variables.css` header comments** still say v15 (not in your Step 5). Left as is.
- **`Atlas-Project-Instructions-v4.md`** came in the handoff zip but no step places it. Not installed in the repo.
- **Build image:** no Cloudflare config in the repo. Cloudflare's docs list Python 2.7 (build image v1), 3.11.5 (v2) and 3.13.3 (v3); `check_brand.py` needs 3.7+. Local Python is 3.9; CI pins 3.12. Because the image in use isn't visible from the repo, `build-dist.sh` skips the check with a loud warning if `python3` 3.7+ is missing, instead of failing the deploy; the required GitHub `brand-check` status still enforces. The first Cloudflare build log should show the check printing `OK`, not the warning.
- **About cluster Phase 1:** already committed in `50251de` and on `main` before the brand-check wiring, so the baseline includes it.
- **Count:** the unmodified check reports 2,307 violations in 59 files on Justin's tree; you recorded 2,308 on the public repo.
- **Git:** your `check_brand.py` was committed to `main` (`c1c5689`) before `dev` was cut. `dev` was created fresh from `main`; an older `origin/dev` from 8 months ago exists and is stale.

## 4. Baseline counts (rewritten Oct 28 after the re-scope)

| | Count |
|---|---|
| Your original rules | 2,310 |
| `color-func` (47 files) | 467 |
| `color-name` | 0 |
| `color-alpha` | 0 |
| **Total, 59 files** | **2,777** |

Original rules: `color` 1,374, `font-size` 410, `font-literal` 272, `font-family` 151, `font-weight` 34, `serif-scope` 29, `pill-radius` 19, `serif-heading` 17, `lime-text` 4. Before the re-scope the baseline was 3,041: 731 `color-func`, 3 `color-name`, and `color` at 1,371. The new rules mostly record existing off-palette usage for your next token version; they are not new problems.

What changed since the first count: `color-func` 731 to 467 (shadows, borders, backgrounds and overlays in white or black are allowed); `color-name` 3 to 0 (the `red` error message and the two `gray` spinners were fixed, see 4a); `color` +3 (the three provisional error hex values in `variables.css`).

### 4a. What the 467 `color-func` hits are, and what else changed Oct 28

- **307** are white or black used as a **text color** (the thing v16 forbids).
- **144** are other colors in non-text properties, mostly Acid or Lime with alpha (`rgba(206,255,0,...)`, `rgba(151,214,0,...)`) used as tints and overlays. If you decide tinted palette colors are allowed too, this drops to 323.
- **16** are other colors used as text color.

**Error roles (PROVISIONAL, for you).** `--color-error` (`#f50000`) stays your value. It is 4.3:1 on white and 3.7:1 on `--color-bg`, below the 4.5:1 text minimum, and `v16` records that you rejected the Material 3 `#b3261e` in May 2026 as "too dull". Four new tokens sit beside it, from the Material 3 baseline, named `*-provisional`: `--color-error-provisional` (light surfaces), `--color-on-error-provisional`, `--color-error-on-dark-provisional`, `--color-on-error-on-dark-provisional`. Contrast: light error text 6.5:1 on white and 5.7:1 on `--color-bg`; dark error text 12.3:1 on black, 11.0:1 on step 7, 7.7:1 on step 6; white on the light error 6.5:1; the dark on-error on the dark error 7.7:1. Use is limited to error messages. The search page's data-load error now reads "Error: the creator data could not be loaded. Check your connection and refresh the page." with `role="alert"`.

**Gray spinner:** the `gray` (`#808080`) border on the spinner in `lab/health-field-finder/funder.html` and `review.html` now uses `--gray-neutral-4` (`#909090`, the closest neutral step), with `#909090` as a fallback because those pages don't load `variables.css`. If those pages are regenerated by the password-protection tool, the edit is lost.

**Provisional rules** are in `CLAUDE-DESIGN-RULES.md` under "Provisional, confirm with James": monospace is for live or versioned data only; Acid means changed recently.

**Burn-down order** for the backlog: `index.html`, `pulse.html`, `city-lab-chicago.html`, then by count. Chicago has no exemption (the check never excluded it). Fixing the backlog over time is approved; each fix regenerates the baseline in the same change.


## 5. Open items for James and Justin

- Do tinted palette colors (Acid or Lime with alpha, 144 hits) get palette roles, or are they allowed? And does the provisional error role (section 4a) stand, change or go?
- The open questions at the end of the Pulse and For Brands brief.
- How we research (About Phase 3): lab notebook with "Trace this number" as the single signature element, approved. Before it is built: does a traced number open in place or in a side panel (especially on mobile at 390px), and is the one motion the draw-down or a plain open? v16 has no motion roles, so a motion needs a token.
- Team DMV's header and footer.
- The TIJA LLC GitHub organization, and the repo going private.
- Your GitHub username, so CODEOWNERS can be written (deferred).
