# SmartNews page: build report v1.0

Built Oct 19, 2026 against `SMARTNEWS-PAGE-BRIEF-v1.0.md`. Everything is in the working tree, uncommitted. Nothing pushed.

**The page:** `preview/smartnews-d029dc36/index.html`, which serves at `/preview/smartnews-d029dc36/`. The page is not yet at `partners/smartnews.html` (see "Gate").

## Decisions made on your direction

| Decision | Choice |
|---|---|
| Gate | Same mechanism as Nodes and Networks: unlisted hashed URL under `/preview/`, `noindex, nofollow` meta, `robots.txt` `Disallow: /preview/`. No real access control. |
| Brand guide | `ATLAS-BRAND-GUIDE-v3.md` from `~/Desktop/Downloads/` (identical to the copy in `~/Desktop/atlas-chat-bundle-2026-10/C-reference/`). |
| Form backend | A: Google Apps Script → Google Sheet. Source in `intake-apps-script.gs`. |
| Cohort | Alphabetical by last name. Bernstein, Cillizza and Legum `confirmed`; Fleisher and Palmeri `pending`, so hidden. Newsletter names are `[NEWSLETTER NAME]`; Bernstein also has `[CO-WRITERS?]`. GPBP is not expanded anywhere. |

## Step 0 results

| # | Item | Result |
|---|---|---|
| 1 | Repo and tree | FOUND `~/Documents/GitHub/journalism-atlas/`. **Tree was not clean at start:** `build-dist.sh` (modified, adds `coops-data.json`), `co-ops.html` (modified), `assets/data/coops-data.json` (untracked). Untouched. |
| 2 | CLAUDE.md | Read in full. Conflicts are in the flag list below. |
| 3 | Design tokens v14 | FOUND `DESIGN-TOKENS-v14.md` at the **repo root**, not `docs/design/` (that folder does not exist). `variables.css` implements v14 (acid/lime/olive roles, focus tokens, link tokens). The page uses its tokens only; no token values are inlined. |
| 4 | Brand guide v3 | **NOT in the working tree.** It was added in commit `413e5a8` ("more") and is no longer at HEAD; `LEAVE-OFF-LOG` says it was moved to the repo root. The only copies on disk are the two Desktop copies above. Used the Desktop copy. Separately, `journalism-atlas-private/compute/REPO-VISIBILITY-REPORT-2026-10-11.md` records it as an untracked file in this repo. |
| 5 | James's principles | FOUND `_reference/james-design-principles.md` (and `.pdf`; another PDF copy in `docs/`). |
| 6 | The gate | See "How the existing gate works". |
| 7 | Shell, header, redirects, robots | FOUND `partners/_shell.html`, `assets/js/header.js`, `assets/js/footer.js`, `assets/css/header.css`, `_redirects`, `robots.txt`. NOT FOUND: `_headers`, `sitemap.xml`. |
| 8 | `/partners/smartnews` free | Yes. No file, no redirect. |
| 9 | Prototype | The file in `~/Downloads/files.zip` is byte-identical to `~/Downloads/SmartNews x Atlas_ independent journalists in SmartNews.html`. Copied to `docs/briefs/smartnews/reference/smartnews-pilot-prototype-v2.html`. |
| 10 | SmartNews logo | Extracted from the prototype to `assets/images/partners/smartnews-logo.jpg`, **640 × 148 px**, JPEG, 15.5 KB. Source is SmartNews's own one-pager. Replace if Bernie sends an SVG. |
| 11 | Creator count | Live from `creators-data.json` (2,432 records today). Rendered as "about 2,400" (floor to the nearest 100). No hardcoded number anywhere. |

### How the existing gate works

The Nodes and Networks "gate" is **not a password or any access control.** It is three things:

1. An **unguessable URL:** `/preview/nodes-and-networks-f348eb08/`. Security by obscurity.
2. `<meta name="robots" content="noindex, nofollow">` and `<meta name="referrer" content="no-referrer">` in the page.
3. `robots.txt`: `Disallow: /preview/`.

No Cloudflare Access, no `_headers` rule, no client-side password, no sitemap (there isn't one). Anyone with the URL can read the page. That is acceptable for non-secret pre-launch copy, but Bernie's colleagues can open it if the link is forwarded.

Two small caveats of this pattern (inherited, not introduced): `robots.txt` Disallow stops crawlers from reading the `noindex` meta, so a leaked link that gets linked from elsewhere could still show up as a bare URL. And `build-dist.sh` already publishes `preview/**/index.html`, so the new page deploys with no change to the build script.

## What was built

- Co-brand band (white, both marks unrecolored, equal optical weight: Atlas 30 px / SmartNews 44 px tall at desktop, 19 / 28 px on mobile).
- Dark hero, SmartNews first in the headline. The deck, "who" and the release's cohort paragraph all render from the cohort data.
- "Why are you here?" routing row (four routes, each with a line of context). The "recommend" route opens the form in recommend mode; the "reader" route lands on the app-store slot.
- The release (white, 680 px Merriweather column, sticky sidebar with apply button and media contacts). Bernie's quote comes first.
- "Why SmartNews" (see decision below), founding cohort (dark), three ways in, how it works for creators, Atlas story (dark), form, About and media contacts. Footer comes from the shared `footer.js`.
- Cohort, ways-in cards, routes, terms and form options all render from data constants at the top of the script.
- Form: self and recommend modes, interest multi-select, honeypot, preview mode while `FORM_ENDPOINT` is empty.

### Surface choices (Surface Hierarchy)

Dark: hero, cohort, Atlas story (exactly the three the brief names). Light: everything else. **"Why SmartNews" is light.** It is information-dense (who SmartNews is, how the politics vertical works), which Surface Hierarchy reserves for the workspace. The screenshot of the Independent Voices module is the visual. If James wants it as a stage, the cohort would sit between two dark blocks and the rhythm would suffer.

## Verified

| Check | Result |
|---|---|
| Loads at the preview URL, no console errors | Pass |
| Empty submit | Flags all 8 required groups, focuses the first, shows the error note |
| Recommend mode | Relabels fields, email becomes optional, recommender name and email become required, consent text switches |
| Deep links | Route and track links set the mode and pre-check the interest |
| Preview mode submit | Success state says "Preview page: nothing was sent anywhere." |
| **POST to `FORM_ENDPOINT`** | Tested against a **local listener** (not a deployed Apps Script, which needs your Google account). Body arrived form-encoded with all 17 fields, `source=smartnews-page`, `page_version=smartnews-page-v1.0`. The Apps Script itself is **untested**; run the deploy steps in its header and submit one test row. |
| Cohort hide | Setting Legum to `pending` removed his card and his name from the deck and the cohort paragraph |
| 2× inventory | 10 confirmed entries plus the open seat render in a 4-column grid with no layout change; no horizontal scroll |
| 390 px | `scrollWidth` 390 = viewport. No page element overflows (the only off-screen elements are the site's own mobile menu). Min text 13 px. Logo links raised to 44 px targets. |
| Screenshots | `docs/briefs/smartnews/screenshots/` (390 and 1440). They are downsampled captures from the in-app browser, not full-resolution. |

**Not verified:** keyboard-only pass by hand (focus styles are defined for every control, tab order follows the DOM, but I did not tab through it); a contrast tool run (checked by token value, see flags); a real screen reader; Safari/Firefox.

## Flags: conflicts and calls I made

Per the brief, none of these were reconciled silently.

1. **Gate location vs the brief's file path.** The brief says `partners/smartnews.html`. Using the Nodes and Networks mechanism means the gated build lives under `/preview/`. Ungating is a `git mv` (checklist below). Asset paths are absolute so nothing needs rewriting.
2. **Brand guide v3 is not at HEAD** (Step 0, item 4). It needs to be committed back or its absence recorded; CLAUDE.md does not mention it.
3. **Prototype used Hanken Grotesk.** The brand guide v3 retired it. The page uses Inter and Merriweather per the guide.
4. **Prototype hardcoded colors.** Replaced with `variables.css` tokens. The prototype's acid-as-text and lime-as-border on light surfaces would have violated v14; none carried over.
5. **"Dark mode" screenshots.** The site has no OS dark theme (the dark surfaces are a fixed design choice), so `prefers-color-scheme: dark` changes nothing. Screenshot `1440-09` confirms the page is identical. The brief's "light and dark" check is therefore a single mode.
6. **Brand guide on database size:** "about 2,400–2,500", never an older figure. The page shows "about 2,400" from the live count, floored to the nearest 100. A live count of 2,500+ will read "about 2,500". CLAUDE.md's `.js-creator-count` convention is followed (the class is used), but the page sets its own text because it needs the "about" and the rounding.
7. **Prototype copy I removed because it was not in the brief's established facts:** "one of the largest news apps in the United States", "NEW YORK and WASHINGTON" dateline, "Starting this week", "formerly of CNN and The Washington Post" (Cillizza), "Founder of..." style descriptions as fact. Cohort one-liners are now shown as `[DRAFT: ...]` for each creator to confirm. The Justin quote still says "audiences that rival legacy newsrooms"; it is marked `[DRAFT—JUSTIN TO EDIT]`, but that is a factual claim worth sourcing before Bernie sees it.
8. **Em dashes.** Brand guide: "word—word", no spaces. The dateline and the draft tags follow that. The brief's own `[DRAFT — ...]` spelling was changed to `[DRAFT—...]`.
9. **Recommend-mode consent text** is my wording ("...contact me about this recommendation and future opportunities"). The brief gives one consent sentence for both modes. In recommend mode the person recommended has not consented to anything; the Atlas would contact them through normal outreach. Confirm that is what you want.
10. **Beat list does not map to a single vocab.** The form's beats map to the nine controlled **Groups** (comments in the script list the Topic values each suggests). "Other" and "Journalism Formats" have no clean map, so "Other" is submitted for Ryan to code by hand. Locations are free text.
11. **Platform "Other"** covers other newsletter tools, social platforms and Patreon (not offered separately), so those arrive unmapped.
12. **Validation color.** Error text uses `--color-error` (`#f50000`), a v14 token. At 13 px on white it is about 4.3:1, just under the 4.5:1 AA threshold for small text. Needs James's call (see `REVIEW-NOTES-JAMES.md`).
13. **Header search box** looks squeezed at 390 px in the shared header (an empty rounded field next to the Search button). It is `header.js`/`header.css`, not this page; I did not touch it.
14. **Placeholder Principle vs brackets.** James's principle says no empty states in public design. The brackets and the screenshot slot are preview-only. With `GATED = false` the slot and tags disappear, but **bracketed text does not**; every bracket has to be replaced by hand.
15. **No-JS / failed fetch:** the cohort, routes and tracks need JS (they render from data). Creator count falls back to "thousands". The no-cors POST means a script failure looks like success to the applicant (noted in the Apps Script header).
16. **Cillizza** is flagged on his card in the preview (`[NEEDS CHRIS CILLIZZA PRIOR APPROVAL BEFORE NAMING]`). **He is named in the hero deck, the release paragraph and the cohort. Do not ungate or send to Bernie as final until his prior approval is in hand.** The flag only appears while `GATED = true`; it is not a safeguard once ungated.

## Placeholder list (every bracket on the page)

| Placeholder | Where | Owner |
|---|---|---|
| `[RELEASE DATE]` | Hero kicker, release dateline | Justin / Bernie |
| `[DATELINE]` | Release dateline | Justin / Bernie |
| `[LAUNCH DATE]` | Release paragraph 2 | Justin / Bernie |
| `[DRAFT—BERNIE TO APPROVE]` | Bernie quote (preview tag) | Bernie |
| `[DRAFT—JUSTIN TO EDIT]` | Justin quote (preview tag) | Justin |
| `[PRESS CONTACT]` | Sidebar and About, SmartNews | Bernie |
| `[CONFIRM WITH SMARTNEWS]` | Why SmartNews and About SmartNews boilerplate (twice) | Bernie |
| `[SMARTNEWS TO SUPPLY: reader profile]` | Why SmartNews | Bernie |
| `[SMARTNEWS AUDIENCE FIGURE]` | Why SmartNews | Bernie |
| `[SMARTNEWS TO SUPPLY: how the politics vertical works]` | Why SmartNews | Bernie |
| `[APP STORE LINKS]` | Reader block | Bernie |
| `[SCREENSHOT FROM SMARTNEWS]` | Why SmartNews slot | Bernie |
| `[NEWSLETTER NAME]` | Bernstein; Cillizza (Cheney Road Productions) | Ryan / creators |
| `[CO-WRITERS?]` | Bernstein: is he writing as part of a three-person newsletter, and are co-writers named? | Ryan |
| `[DRAFT: ...]` descriptions | Bernstein, Cillizza, Legum (one line each) | Creators / Justin |
| `[PUBLICATION LINK]` | All three cohort cards | Creators |
| `[NEEDS CHRIS CILLIZZA PRIOR APPROVAL BEFORE NAMING]` | Cillizza card (preview tag) | Justin |
| `[CONFIRM VERIFICATION SENTENCE]` | Atlas story: "a person checks every creator against the Atlas's published standards" | Justin / Liz |
| `[CONFIRM ABOUT-ATLAS BOILERPLATE]` | About the Atlas | Justin |

Not on the page by design: the pilot fee, any posting cadence (Bernstein's monthly floor was cut to 16 because of holidays, so no cadence is promised), the GPBP expansion, any SmartNews audience number.

## Ungate checklist

1. Cillizza's written approval is in hand. Fleisher's and Palmeri's signatures are in hand (or they stay hidden); flip their `status` to `confirmed` in `COHORT` if they should show.
2. Replace every bracket in the list above; search the file for `[`.
3. Decide the URL. Default: `git mv preview/smartnews-d029dc36/index.html partners/smartnews.html`. Alternative: `/smartnews` with a `_redirects` entry.
4. Delete the `<meta name="robots">` and `<meta name="referrer">` lines. Set `const GATED = false`.
5. Set `FORM_ENDPOINT` to the deployed Apps Script URL and submit one real test row.
6. Set `SCREENSHOT_SRC` to the screenshot (upload to `assets/images/partners/`), or leave empty to hide the slot.
7. `robots.txt`: nothing to change (the path leaves `/preview/` when it moves). No sitemap exists; if one is added later, include the page.
8. Link it from where it should live (not linked anywhere today). The Partners index and header nav were not touched.
9. Add `partners/smartnews.html` to the Page Inventory in `CLAUDE.md`.
10. Confirm Cloudflare deploy: the logo is under `assets/images/` (already published); `build-dist.sh` copies `partners/` and `preview/**/index.html` already. No build change needed.
11. Push via GitHub Desktop.

## Recommendation: reusable template?

Yes, worth doing for the next platform partner. Most of this page is already data-driven (cohort, ways in, routes, terms, form options). The pieces that would need to move into a config object are the release copy, the partner's logo and the "Why [partner]" section. Suggest waiting for the second partner before extracting, so the abstraction is built from two real cases. Flagged for James as the Template Principle question.

## Files

- `preview/smartnews-d029dc36/index.html`: the page
- `assets/images/partners/smartnews-logo.jpg`: logo (640 × 148)
- `docs/briefs/smartnews/`: brief, `reference/` prototype, `intake-apps-script.gs`, this report, `REVIEW-NOTES-JAMES.md`, `REVIEW-CHECKLIST-BERNIE.md`, `screenshots/`
- `LEAVE-OFF-LOG.md` and `START-HERE.md`: entries added
