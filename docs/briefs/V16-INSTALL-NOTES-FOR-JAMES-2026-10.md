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

**B2, functional colors.** Every `rgb(`, `rgba(`, `hsl(` and `hsla(` is `color-func`. Values are not mapped to the palette.

**B3, named colors.** CSS named colors are `color-name` when they are the value of a color property or attribute (CSS properties, SVG `fill`/`stroke`, D3 `.attr`/`.style`, `.style.color`, canvas `fillStyle`/`strokeStyle`). Not flagged: `white`, `black`, `transparent`, `currentColor` and the CSS-wide keywords. Two small additions beyond the brief's list: `.style.background`/`backgroundColor`, and any object's `.fillStyle`/`.strokeStyle`, not only `ctx`.

**B4, hex false positives.** A `#` match is skipped after `href=`, `url(`, `querySelector(`, `querySelectorAll(`, `closest(`, `getElementById(`, and when a `{` follows on the same line (a CSS selector). The selector lookahead also stops at quotes, `<`, `>` and `$`, so `style="color:#f00">{{COUNT}}` is still caught. On today's tree this changed no existing count.

**B5, `--tight`.** Same as the default mode, and also fails when a count is below its baseline or the baseline lists a file that is gone. CI uses it. The default mode, used by `build-dist.sh`, is unchanged.

**B6, `--guard-baseline <ref>`.** CI only. Fails if any baseline count is higher than at `<ref>`, unless `scripts/check_brand.py` itself changed. A missing baseline at the ref passes; a ref git can't find exits 2 instead of passing silently. Caveat: the exception uses `git diff <ref> -- scripts/check_brand.py` (two-dot). If `main` gains a change to `check_brand.py` after a branch started, that branch would also see a difference and be allowed to raise counts. Worth a three-dot comparison later if it matters.

**B7, serif path.** No long-form report page exists in the repo (Nodes and Networks is excluded). `SERIF_ARTICLE_PATHS` stays `("watershed/",)` with a comment to add the report path when the first page is built.

**Narrowed CODEOWNERS** (to be written after the baseline). Owned: `/docs/design/`, `variables.css`, `check_brand.py`, `brand-check.yml`, `CODEOWNERS`. Not owned: the baseline file (the guard blocks increases mechanically, so fix-PRs don't wait on you), `build-dist.sh`, `_headers`, `CLAUDE.md`, `WORKFLOW.md`, the rest of `.github/`. Reasons are in Part D of the install brief.

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

## 4. Baseline counts

| | Count |
|---|---|
| Your original rules (unchanged by B1–B4) | 2,307 |
| `color-func` (51 files; 571 of them are `rgb()`/`rgba()` white or black) | 731 |
| `color-name` | 3 |
| `color-alpha` | 0 |
| **Total, 59 files** | **3,041** |

Original rules: `color` 1,371, `font-size` 410, `font-literal` 272, `font-family` 151, `font-weight` 34, `serif-scope` 29, `pill-radius` 19, `serif-heading` 17, `lime-text` 4. The new rules mostly record existing off-palette and off-role usage for your next token version; they are not new problems. The three `color-name` hits: `red` in an inline error message (`assets/js/main.js:425`) and `gray` in two spinner borders (`lab/health-field-finder/funder.html:148` and `review.html:148`). There is no 4- or 8-digit hex on the site today.

### 4a. `color-func` by property: does v16's rule cover only text color?

v16 says (lines 22 and 297) that opacity-based **text** colors such as `rgba(255,255,255,0.3)` are off-system. It says nothing about shadows, borders, overlays or fills. `color-func` as built flags every `rgb(`/`rgba(`/`hsl(`/`hsla(` regardless of property, so most of the 731 are outside what the rule names. Breakdown by the property the value sits in:

| Property | All 731 | Of which white or black |
|---|---|---|
| `color` (text) | 318 | 303 |
| `border`, `outline`, `stroke` | 162 | 125 |
| `background` (incl. gradients) | 148 | 80 |
| `box-shadow`, `text-shadow` | 58 | 42 |
| multi-line value or gradient continuation (no property on the line) | 24 | 10 |
| `fill` | 9 | 4 |
| custom property (`--x: rgba(...)`) | 6 | 4 |
| other (`text-decoration-color`, `scrollbar-color`, `text-decoration`, a `bg` key) | 6 | 3 |
| **Total** | **731** | **571** |

Only the 318 text-color hits (303 white or black) are what v16 clearly forbids. The other 413 are shadows, borders, backgrounds and overlays that v16 neither allows nor forbids; under "undefined means unbuilt" they read as violations, but nobody has said what token an overlay or a shadow should use. Questions for James:

1. Should `color-func` narrow to text color only (the `color` property), with shadows, borders and overlays handled by a new token role in your next version?
2. Or does every `rgba()` stay flagged, and v17 adds roles (overlay, hairline, shadow) so each one has a home?
3. Until you decide, nobody should rewrite shadows or borders to clear the count. The baseline freezes all 731 as they are.

## 5. Open items for James and Justin

- Do `color-alpha` and `color-func` uses get palette roles, or a rule? Only the `color` (text) hits fall under your rule; see the breakdown in section 4a before anyone starts working the 731 down.
- The open questions at the end of the Pulse and For Brands brief.
- How we research (About Phase 3): lab notebook with "Trace this number" as the single signature element, approved. Before it is built: does a traced number open in place or in a side panel (especially on mobile at 390px), and is the one motion the draw-down or a plain open? v16 has no motion roles, so a motion needs a token.
- Team DMV's header and footer.
- The TIJA LLC GitHub organization, and the repo going private.
- Your GitHub username, for CODEOWNERS (still a placeholder).
