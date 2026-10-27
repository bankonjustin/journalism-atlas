# About cluster ledger

## Standing rules
- **Dated vs. live numbers (Oct 27).** A dated document keeps the figure it had on its date; the live figure appears next to it, labeled live. Never drop today's number into a sentence about a past version or brief.
- Counts come from build tokens only (`{{CREATOR_COUNT}}`, `{{COUNT_AS_OF}}`, `{{BLUESKY_COUNT}}`).

## Phase 5 redirect table (running)
| Old | New | Note |
|---|---|---|
| /about-this-project | /about | hash router for `#who-we-are`, `#methodology`, `#advisory`, `#research` |
| /how-we-did-this(.html) | /how-we-research | |
| /advisory(.html) | /who-we-are#boards | only if the merge is approved |
| /what-we-do(.html) | /about | retarget the existing rule (today it goes to /about-this-project); keep it single-hop |

## Decisions waiting on Justin (keep current)
0. **Design system (blocks Phase 3).** The brief says Playfair Display / DM Sans / Space Mono and orange for "changed recently." The repo (v15 tokens) and both sister ledgers use Inter / Merriweather / Source Code Pro with Acid as the single "live" color; there is no orange token. The brief says to reuse the Pulse and /for-brands tokens, so I plan on v15 (Space Mono rule becomes Source Code Pro, orange becomes Acid). Confirm, or James approves a departure.
1. "Verified": define once on How we research (recommended) or stop using it.
2. Who We Are headline.
3. Belief line: keep "outside the institution but inside the public interest" (recommended).
4. Merge /advisory into /who-we-are (recommended) or keep.
5. Funders: name them, or soften "we're transparent about who funds our work".
6. Disclosures: which relationships to list.
7. Methodology v2.0: what changes, signed by Justin, Liz, Ryan.
8. Flags: when Build and Connect turn on.
9. Your bio: current or updated.
10. The paper's published URL.
11. **New: reviewer wording.** See finding F3. Rewrite "no single person decides" or change the practice.
12. **New: "one form, same endpoint."** /contact#contribute is an embedded Google Form iframe. There is no endpoint to post to. Embed the same iframe on How we research, or move to a real form (needs a backend).

## Phase 0: Audit (2026-10-27)
Changed: nothing in the site. Created this ledger and `about_screens/phase-0/` (32 PNGs: home, overview, who, method, advisory, research, contact, bluesky at 390/768/1280/1600, full page, from a local copy with count tokens stamped). Nothing committed.

### F1. The brief's §0 is partly stale. Live matches the repo (checked in a real browser, Oct 27).
Already fixed in the Oct 26 "site audit content fixes" commit (bc22315, 4716e97); do not redo:
- Overview count: live "2,415 of them", no 1,718 anywhere in source or live.
- /research: 2,415 via token, "Knight Center" already present.
- Home: no 2,432, no "Two major studies this summer", no "12 institutional partners". The partner strip is "Published with" text links (3), the Overview's is 3 links, no logos.
- Overview/Who We Are "Three journalists"... Who We Are still has it (below).

Still wrong live today:
| String | Where | Count |
|---|---|---|
| "approximately 1,000 creators"; "1,000 creators is a sample" | how-we-did-this.html:219, :309 | 2 |
| "Three journalists who left major newsrooms..." over four people | who-we-are.html:225 | 1 |
| "journalism minus the journalist" | about-this-project.html:585 | 1 |
| "Knight Foundation · Arizona State University · Forthcoming", "1,000+ independent journalists", title "The Economics of Independent Journalism at Scale" | index.html:1126-1127 (live count 2) | 1 card |
| Overview "Two published, one forthcoming" and "Knight Foundation / ASU economics study" | about-this-project.html:711-712 | 2 |
| "June 2026 · Press Forward Chicago" badge | research.html:725 | 1 (a real date for that toolkit; leave) |
| "550+" in meta, OG and Twitter descriptions | bluesky page lines 7, 9, 14 | 3 |
| "500+ creator-journalists" | index.html:1114 | 1 |
| Home research intro still says "Live now: the CNTI report... Forthcoming: the Knight Foundation / Arizona State economics study." | index.html:1072 | 1 |
| Icon ligature words in text (`lock_open` x1, `pause_circle` x2 on home; "close/menu" visible in page text on the Overview) | home, header.js | see F6 |

### F2. Number inventory (whole site, in-scope pages and shared JS)
| Fact | Values found | Truth source |
|---|---|---|
| Creators | tokens `{{CREATOR_COUNT}}` / `{{COUNT_AS_OF}}` on home, Overview, /research, for-brands (2,415, Oct 26, from `assets/data/site-stats.json`, written by `convert.js`); typed "approximately 1,000" on methodology | site-stats.json |
| Bluesky | typed 550+ (meta), 500+ (home); `bluesky-creators.json` has **634** entries | file |
| Feeds | not in site-stats.json. Pulse ledger: 1,747 monitored (Oct 22 data), for-brands earlier said 1,756 | Pulse build; **no shared build variable** |
| Paper N (169 orgs, nine cohorts) | not in any in-scope page; for-brands gates it | typed |
| Topics 79, platforms 33 | site-stats.json | file |
| Liz "160+" Project C; Chicago "100+ names" | typed, Overview/Who We Are | editorial, leave |
| Partners count | no count appears in source now | n/a |

Canonical creator count: the token system is the one. `build-dist.sh` fills it from `site-stats.json`. Proposal for Phase 2: extend `site-stats.json` (written by `convert.js`) with `blueskyCount` (from `bluesky-creators.json`), `feedCount` (from the Pulse build, `update_pulse.py` or `lens-index.json`, which already carries 1,747), and `asOf`. Add matching tokens in `build-dist.sh`. **The token mechanism also covers `<meta>` text already** (home does it).

### F3. Verification data (the Phase 3 signature depends on this)
Exists, in the private repo only (never publish rows, only aggregates):
- `journalism-atlas-private/data/rejections.csv`, 597 rows, 2026-03-18 to 2026-10-26. Fields: `date, slug, creator_name, url, reason_code, reason_description, note, batch, decided_by, status`. Status is `rejected` on all rows.
- Reason codes: not-journalism 193, legacy 160, scope 131, insufficient 49, inactive 37, duplicate 12, other 9, rule-6 3, rule-9 2, unverifiable 1. These match the six named categories plus a few outliers. Many rows are a legacy-sheet import dated per batch, so dates are batch dates.
- `decided_by`: Ryan 538 + "ryan" 11 + "Ryan, Justin" 8 + Justin 1 + agent entries 39 (Claude agents, auto-reject).

Does not exist at any grain I could find:
- Candidates reviewed or approved counts, approval dates (`creators-master.csv` has no date-added column), reviewer votes. The three-reviewer vote files (`HUMAN_REVIEW_VOTE_*.md`) are per batch documents, not a dataset.
- Spidering/candidate pool: `atlas-engine/ryan-lane/candidate-pool-2026-10.csv` (895 rows, 418 net-new) is a discovery pool, not the review queue.

**Consequence:** the funnel can honestly show declines by named category with a date range, not "reviewed -> approved -> declined." To show approvals Justin or Ryan must export a date-added field (or approval log). Declines are 597 against 2,415 live; do not present a rate.

**Claim conflict (decision 11).** The Bluesky page says "Multiple reviewers evaluate independently, no single person decides." DATA-OPS-PROTOCOL says the three-reviewer vote is for edge-case batches; "clean, obvious adds and obvious rejections... single-pass," and a "proposed change" to the review process is documented but not active. About 90% of recorded declines list Ryan alone. The "How we verify" section cannot carry the current wording as-is. Also, the protocol names Ryan, Liz, Justin (and Anna part-time) as reviewers: confirm what may be said publicly.

### F4. Duplication map (which copy is newer)
| Block | Copies | Notes |
|---|---|---|
| Team bios | Overview §Who We Are (:520-560), who-we-are.html | both touched in bc22315; Overview copy is a mirror |
| Criteria (5) and "Who we're looking for" | Overview §How We Built This (:583-640), how-we-did-this.html | methodology is canonical, dated v1.0 2/12/26 |
| Advisory boards | Overview §Advisory (:644-700), advisory.html | advisory.html is canonical |
| Funding statement | Overview :570, who-we-are.html | near-identical; Who We Are adds "Our funding model will evolve" |
| "Published with" strip | Overview, Who We Are, home | 3 links each |
| Research cards | Overview §Publishing, home, /research | Overview and home still say forthcoming |
| Four-step verify process | bluesky page :372-386 only | would move to How we research |
| About subnav markup | duplicated inline in each of 4 pages (~20 lines CSS + HTML each) | Overview uses anchors and scroll-spy, the others use page links |

The Overview is a one-page copy of the other three, plus them.

### F5. Names for the one page
Five: URL "how-we-did-this"; subnav "Methodology"; H1 "The Atlas: Standards & Criteria"; Overview section "How We Built This"; global nav "How it works"; footer "How We Did This"; welcome strip "How we find them." (that is six surfaces, five distinct labels plus the URL.) Global nav in `assets/js/header.js:148,167` and footer `footer.js:41-44`. Nav has no About link on desktop; "About" is only in the mobile menu (-> /about-this-project.html).

### F6. Icon font
`header.js` loads Material Symbols and uses it for `menu`, `close` and one more (lines 126, 151, 160). Live page text includes "close menu", and home has `lock_open`, `pause_circle`. Replacing it in the shared header affects every page; for-brands already dropped the font on its own page. Needs a decision whether the shared header change is in scope (I recommend yes: one SVG pair in header.js).

### Redirects
- Mechanism: Cloudflare Pages `_redirects`, 301s, copied by `build-dist.sh`. Pages are served extensionless (`/who-we-are`) and `.html` variants exist in links. `what-we-do(.html)` already redirects to `/about-this-project`, which must be retargeted to `/about` when that lands (avoid chains).
- Cannot `curl` live (403 to scripted clients); must test in a browser.
- Internal links to old URLs (source, outside `_deprecated`): header.js (4 spots incl. welcome strip), footer.js (3), pulse.html (4 about-this-project), index.html (3: lines 539, 566, 1001 `#who-we-are`), contact.html:128, submit.html:222, mobile.html (3), chicago-survey/chicago-analysis/beat-climate/beat-finance/beat-tech (subnav-style link blocks, 4 each), watershed/index.html (3), watershed/methods/index.html (1), 14 pages in partners/ and co-ops.html (canonical-style `about-this-project` links). Count is 18 files plus 14 partner pages. Not yet checked: Bluesky page and /research for links to `how-we-did-this`; `#methodology`, `#advisory`, `#who-we-are`, `#contribute` anchors need the mapping in Phase 5. Anchors in a 301 are dropped by the server; fragment preservation only works if the destination page's JS or matching ids handle them (browsers do carry the original fragment across a 301 when the Location has none, so `/about-this-project#who-we-are` -> `/about` loses meaning; plan: small hash router on `/about`).
- Watershed essay links "How we did this" externally; keep the old URL redirecting forever.

### Nav
- Global nav (header.js): Pulse, For Brands, Research & Writing, How it works. No About on desktop.
- About subnav exists only on Overview, Who We Are, Methodology, Advisory (copied inline; Overview version scroll-spies anchors). **/research, /contact and the Bluesky page have none.** Contact has no subnav.

### Lighthouse (local, uncompressed server, stamped copy; throttling default; mobile / desktop)
| Page | Perf | A11y | BP | SEO | LCP | CLS |
|---|---|---|---|---|---|---|
| Home | 58 / 85 | 80 / 80 | 96 | 100 | 20.2 s / 2.7 s | 0 / 0.004 |
| Overview | 73 / 86 | 93 / 93 | 96 | 100 | 8.1 s / 1.5 s | 0.068 / 0.189 |
| Who we are | 56 / 89 | 93 / 93 | 96 | 100 | 17.7 s / 2.1 s | 0 / 0.002 |
| Methodology | 96 / 100 | 94 / 95 | 96 | 100 | 2.3 s / 0.6 s | 0.002 / 0.007 |
| Advisory | 73 / 76 | 93 / 93 | 96 | 100 | 34.8 s / 5.8 s | 0.008 / 0.003 |
| Research | 73 / 95 | 89 / 89 | 96 | 100 | 8.0 s / 1.5 s | 0.001 / 0 |
| Contact | 97 / 100 | 91 / 91 | 73 | 100 | 2.3 s / 0.6 s | 0.01 / 0.009 |
| Bluesky | 59 / 99 | 91 / 91 | 96 | 100 | 8.8 s / 0.9 s | 0.031 / 0.063 |
Accessibility fails the 95 bar on every page but the methodology (94-95); performance is below 90 on mobile on all but methodology and contact. Likely LCP causes are the big headshot/team images (Advisory 34.8 s), not yet diagnosed. Home mobile LCP 20 s is also seen in the for-brands Phase 0, uncompressed local server. Contact best-practices 73 is the Google Form iframe. Numbers are indicative; live is behind a bot challenge.

Horizontal scroll at 390: home scrollWidth 439, Bluesky 705 (the off-canvas menu was a false positive on for-brands; unconfirmed here).

### Top five recommendations
1. **Confirm v15 tokens (decision 0) and fix the reviewer wording (decision 11) before Phase 3.** Both change copy and the signature element.
2. **Ship the Phase 1 hotfix as a shorter list than the brief assumes.** Most count and partner fixes are already live. Remaining: methodology "1,000", the home/Overview paper card and "Forthcoming" lines, "Three journalists", Bluesky "550+"/"500+" (634 in the data), home link to `#who-we-are`.
3. **Build the funnel as declines by category only**, with a note on what export (approval log or date-added) would complete it. The data layer should read counts from a committed aggregate, never rows.
4. **Collapse the Overview into `/about` early**, since it duplicates three pages and its retirement removes the most drift. Add the 301s with a small hash router, and fix the `what-we-do` chain.
5. **Fix shared plumbing once:** one subnav component (also on /research and /contact), the icon font in `header.js`, and extending `site-stats.json` with Bluesky and feed counts so the Trace strip has real values.

### Open questions for Justin
- Is the Phase 1 hotfix still wanted before Oct 28 given F1? Which of the remaining strings do you want changed tonight?
- OK to extend `convert.js` and `build-dist.sh` for Bluesky and feed counts?
- Trace strip and the funnel: are rejection aggregates (counts by category and date range, no names) fine to publish?
- Is the 634 Bluesky figure the one to use (it counts all Bluesky accounts in the file, not only "active")?

## Phase 1: hotfix (2026-10-27)
Nothing committed. Screens: `about_screens/phase-1/` (home/Overview paper card before and after Oct 28 with a fixed clock; Bluesky verify block and full page at 390; full pages at 1280). Before shots: `phase-0/`.

### Changed
- `how-we-did-this.html`, `who-we-are.html`, `about-this-project.html`, `index.html`, `bluesky-creator-intelligence.html`
- `assets/js/header.js` (icons), NEW `assets/js/nn-gate.js` (date gate; paper URL is one value, `url`, still empty so the link goes to `/research`)
- `convert.js` (+`blueskyCount`), `assets/data/site-stats.json` (+`blueskyCount`, `blueskyCountLabel`, edited by hand instead of running `convert.js`, so `creators-data.json` is untouched), `build-dist.sh` (+`{{BLUESKY_COUNT}}` token, fails the build if unresolved)

### Strings: before -> after
| Where | Before | After |
|---|---|---|
| Methodology | "This first version represents approximately 1,000 creators from diverse sources:" | "The Atlas lists {{CREATOR_COUNT}} creators as of {{COUNT_AS_OF}}, from diverse sources:" (built: 2,415, October 26, 2026). Note: this sentence described the v1.0 launch list; the sources still apply but it no longer says "first version". Your call if you want it restored. |
| Methodology | "1,000 creators is a sample" | "{{CREATOR_COUNT}} creators, as of {{COUNT_AS_OF}}, is a sample" |
| Who We Are (SOFT) | "Three journalists who left major newsrooms to build the map that didn't exist." | "Three journalists left major newsrooms to build the map that didn't exist. A designer joined to make it legible." |
| Home card | "Knight Foundation · Arizona State University · Forthcoming", "The Economics of Independent Journalism at Scale", "1,000+ independent journalists" | "Nodes and Networks" / "Knight Center for the Future of News, ASU Cronkite School · October 28, 2026" / "A field study of 169 U.S. journalism organizations: how governance, more than platform, beat or geography, predicts how big they get." Footer reads "Publishes October 28" until Oct 28 ET, then "Read the study ->" (-> /research until the URL is set). `?nn=1` previews. |
| Home research intro | headline plus "...Live now: the CNTI report... Forthcoming: the Knight Foundation / Arizona State economics study." | headline only (the paragraph is removed) |
| Overview | "Two published, one forthcoming." + Knight Foundation / ASU line | "Nodes and Networks" with the same SOFT copy and gated link, plus "Also published: the Watershed essay, the CNTI report..., and a Bluesky methodology brief." |
| Bluesky meta/OG/Twitter | "550+ verified independent journalists" | "{{BLUESKY_COUNT}} ..." (built: 634) |
| Home Bluesky card | "How we spidered 500+ creator-journalists" | "How we spidered {{BLUESKY_COUNT}} creator-journalists" (this card is a May brief; 634 is today's count, so "spidered" slightly overstates what the May brief did. Reword if you want.) |
| Bluesky step 02 (SOFT) | "The intake queue" / "Each candidate enters the Atlas Intake Queue. Multiple reviewers evaluate independently, no single person decides." / tags "Multi-reviewer", "Independent" | "Reviewed by hand" / "Every candidate is reviewed by hand against the Atlas criteria." / tags "Human review", "Atlas criteria" |
| Bluesky step 03 (SOFT) | "Approve or reject" / "Reviewers vote. Rejection categories are real and enforced: ..." / tags "Voted", "Named rejection criteria" | "Approve or decline" / "Approve or decline. Every decline is logged with a named reason: legacy, inactive, duplicate, not journalism, out of scope, insufficient presence." / tags "Logged", "Named decline reasons" |
| Bluesky suggest block | "the same multi-reviewer human approval as every other entry" | "the same human review as every other entry" (same overclaim; your list did not include it, fixed for consistency) |

### Data touched
| Number | Value | Source |
|---|---|---|
| Bluesky count | **634** | All 634 rows of `bluesky-creators.json` are in the current registry (`creators-data.json`, 2,415), none appears in `rejections.csv`, and 634 registry creators have a Bluesky account in any platform slot. Now computed in `convert.js` from the registry and written to `site-stats.json`. |
| Creator count | 2,415, October 26, 2026 | unchanged token path |

### Icons
`header.js`: the menu icon and both close icons are inline SVG (`aria-hidden`). Home: pause/play toggle (JS swaps two SVG groups) and the lock icon are inline SVG. Checked in a real browser build: no ligature words in page text on home, Overview, Who We Are, methodology or Bluesky. The Material Symbols font still loads from `header.js` because the search page and `main.css` use it; I left that alone.

### 390px overflow: real, fixed
- Home: scrollWidth 439 at 390. Cause: the "Published with" strip had `white-space: nowrap` on a 489px item. Now wraps; scrollWidth 390.
- Bluesky: scrollWidth 705. The page had one phone rule (stat strip) and nothing for the header, hero (grid `1fr 440px`), four-step row, or padding. Added a phone block at the end of its style sheet. scrollWidth 390 and the page reads as one column (checked on the 390 screenshot).
- Caveat: tested with Chromium mobile emulation, not a physical phone. A few creator-index platform chips still measure a few px past 390 inside clipped containers.

### Not done / differs from your list
- **/what-we-do:** left as is. It already goes straight to `/about-this-project` (one hop). Pointing it at `/about` now would 404 because `/about` does not exist until after Oct 28. Retarget it when `/about` ships (Phase 5).
- **"journalism minus the journalist":** held. Still on the Overview (line 585). Needs your yes; the fix is one sentence.
- Bluesky "The intake queue is always open" (step 01) says "intake queue", though the Intake Queue sheet was retired Sept 17. Not changed.
- Lighthouse: not re-run; baseline against production after you push.

### SOFT blocks added
Who We Are subtitle; Overview and home Nodes and Networks copy; Bluesky steps 02 and 03.

### Open for you
1. Yes or no on retiring "journalism minus the journalist".
2. Paper URL for `nn-gate.js` (`url`).
3. Ryan: confirm the review protocol in writing before the three-reviewer vote goes back in.
4. Methodology line 1: keep the new "lists N as of date" or restore a v1.0-specific sentence.
5. After you push, check in a real phone browser: home and Bluesky at 390 for horizontal pan; view source shows `634` and `2,415` baked into meta text.

## Phase 1 revision: review round (2026-10-27)
Nothing committed. Screens: `about_screens/phase-1/` (`{home,overview,research}-nn-{before,after}.png`; the earlier `*-paper-*.png` are replaced).

### 1. Dated vs. live (before -> after)
- Methodology: "The Atlas lists {{CREATOR_COUNT}} creators as of {{COUNT_AS_OF}}, from diverse sources: ..." -> "When we published version 1.0 in February 2026, the Atlas held about 1,000 creators, drawn from diverse sources: ... and our own networks as Atlas founders. Today it holds {{CREATOR_COUNT}}, as of {{COUNT_AS_OF}}." (built: "Today it holds 2,415, as of October 26, 2026.") "{{CREATOR_COUNT}} creators, as of {{COUNT_AS_OF}}, is a sample" kept as is.
- Home Bluesky card: "How we spidered {{BLUESKY_COUNT}} creator-journalists across the AT Protocol ..." -> "How we spidered 500+ creator-journalists across the AT Protocol ... on Bluesky. The map now holds {{BLUESKY_COUNT}}." (built: 634). The card meta states no count. The Bluesky page's own meta and body describe the live map, so they keep the live token.

### 2. /research entry
New first card in the research grid, `id="nodes-and-networks"` (scroll offset clears the sticky header; verified it lands about 96 px from the top): badge "October 28, 2026 · Knight Center for the Future of News, ASU Cronkite School", headline "Nodes and Networks", the same SOFT body as the home card. Shown before the gate with no link. After Oct 28 it gets a link only once `nn-gate.js` has the paper URL (so it never links to itself). Home and Overview "Read the study" now go to `/research#nodes-and-networks` until the URL is set.

### 3. No-JS check
With JavaScript off, home, Overview and /research show the date line and the description and no link or "Publishes" text, so crawlers and link previews never see a stale or broken state. I removed the "Publishes October 28" placeholder because it would be wrong after launch for no-JS readers. Gate states tested with a fixed clock: before (no link), after (links as above).

### 4. "Journalism minus the journalist"
Still held. The instruction had a blank for this ("Justin: retire / keep"). Still on the Overview line 585.

### 5. Redirect table
Added `/what-we-do -> /about` to the running table at the top.

### Local test note
Used a plain static server, which has no clean URLs, so I tested `/research.html#...`; production serves `/research`.

### Open for you
1. Retire or keep the belief-line sentence on the Overview.
2. Paper URL in `nn-gate.js` (recommend the Knight Center page; your interactive edition can be linked from the /research entry).
3. After you push: real phone check, then I re-run Lighthouse on production URLs as the baseline.

## Phase 1 addendum: belief line (2026-10-27)
Overview (`about-this-project.html`:585): "Our belief: journalism has expanded far beyond institutional boundaries — what we've called "journalism minus the journalist."" -> "Our belief: journalism has expanded far beyond institutional boundaries. It now lives outside the institution but inside the public interest." (Justin's wording.) Decision 3 is resolved: "journalism minus the journalist" retired. Grep of published pages shows no remaining hits.
