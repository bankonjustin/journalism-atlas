# Start here — open decisions

*Updated 2026-10-06 after the autonomous v14 run. Delete an item when it is resolved.*

Design rules: DESIGN-TOKENS-v16.md. Open design questions for James live in docs/design/v15-session-2/JAMES-OPEN-ITEMS.md.

## For Justin
- **v16 install, to finish (2026-10-27):** walk James through `docs/briefs/V16-INSTALL-NOTES-FOR-JAMES-2026-10.md`; get James's GitHub username into `.github/CODEOWNERS` (placeholder `@JAMES_GITHUB_USERNAME`); do the GitHub and Cloudflare steps in the install brief's Part E; check the first Cloudflare build log shows the brand check printing OK (or a SKIPPED warning, which means Python is missing).
- **Team DMV header and footer:** open decision.
- **TIJA LLC GitHub organization and the repo going private:** see the repo-visibility brief.
- **Logos:** header swap done (blk/wht wired, default white). Still needed: `Atlas_logo_lockup_stacked_wht_web.svg` (the footer still uses `Journalism_Atlas_wordmark_stacked_white.svg`). The old header SVG (`Journalism_Atlas_wordmark_horizontal_lockup_black.svg`) is now unreferenced and can be deleted.
- **Partner pages have a 72px empty band above the header** (`body { padding-top: 72px }`, pre-existing; the nav is sticky now). Remove the padding?
- **22 pages without `variables.css`** (14 hardcode a green). They were skipped everywhere. Fix = link `variables.css` (visible change) or hardcode v14 colors. Includes `partners/nj-lab.html` / `njlab.html`, whose link is a relative path that 404s. Lists: `docs/V14-STEP2I-2026-10-06.md`, `docs/V14-RESIDUAL-GREENS-2026-10-06.md`.
- **~95 static greens could not be measured** (hover/active/JS-rendered/shared rules; listed with proposed fixes, group C of the residual TSV). Mostly on dark pages; probably compliant.
- **27 JS-set greens** (chart palettes, canvas strokes): listed, not changed.
- `Atlas-Long-Form-Report-Template-2026-09.md` is not in this repo; it needs the white sub-nav spec.
- `.DS_Store` is tracked and shows modified every time; untrack it separately.
- Six commits from this run are local; push when ready.

## SmartNews page (added 2026-10-19; see `docs/briefs/smartnews/SMARTNEWS-PAGE-REPORT-v1.0.md`)
- **Form backend:** built for option A (Apps Script → Sheet). Deploy `docs/briefs/smartnews/intake-apps-script.gs`, paste the URL into `FORM_ENDPOINT`, submit one test row. B (Pages Function + D1/KV) and C (Tally/Typeform) were not built.
- **Cohort order and status:** alphabetical. Fleisher's signature and Palmeri's two open questions (do paywalled pieces count toward five a month; what if she falls short) are open, so both are `pending` and hidden. **Cillizza needs prior approval before the page is ungated.**
- **Bernstein's banner:** newsletter name and whether co-writers are named (`[NEWSLETTER NAME]`, `[CO-WRITERS?]`). Ask Ryan. GPBP is not expanded anywhere.
- **Release date, dateline, launch date** are open.
- **URL:** `partners/smartnews` (default on ungate, via `git mv`) vs `/smartnews` with a redirect.
- **Template:** should this become the reusable "partner announcement" template? Recommendation: after the second partner.
- **Brand guide:** resolved. `ATLAS-BRAND-GUIDE-v5.md` and `DESIGN-TOKENS-v16.md` live in `docs/design/`; earlier versions (v3, v4, v14, v15) are in `docs/design/archive/`.
- **Before ungating:** deploy the Apps Script, submit one real test application and confirm the row lands in the Sheet (the form posts with `no-cors` and shows success even when the endpoint is broken).
- **For James:** twelve items in `docs/briefs/smartnews/REVIEW-NOTES-JAMES.md`, including error-text contrast (4.3:1) and the header search field at 390 px.
