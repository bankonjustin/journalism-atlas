# Open rows research (J3 + J5)

Nov 2, 2026. Read-only. Nothing in the dataset or explorer was edited, staged or committed; this file is the only write. Rules were applied as written in the brief, in order, and each row reports the rule that decided it. Evidence tiers: A primary, B two independent secondaries, C single secondary or data-broker estimates (only if every available estimate clears the line by 50%).

Source caveat: several pages returned 403 (Axios, A Media Operator, Similarweb, FreeERISA) and are read through search summaries or snippets. Those are marked "snippet". Scratch notes with more detail: `r-J3a.md`, `r-J3b.md`, `r-J3c.md`, `r-J5.md` (session scratchpad, not in the repo).

## Verdicts at a glance

| Row | Verdict | Rule | Band |
|---|---|---|---|
| J3-a Risk.net | KEEP (tier C), parent relabel is the alternative | 1 | Above $10M |
| J3-b Defense One / GovExec | RELABEL to GovExec | 2 | Above $10M |
| J3-c Insurance Journal | UNRESOLVED | 4 | Unknown |
| J5 Platformer | KEEP (BELOW) | 1 | Below $3.5M |

---

## J3-a Risk.net

**Verdict: KEEP. Rule 1 (qualifying tier C).** Rule 2 gives the same band on tier A evidence and is the alternative if Justin and Andy don't want to rest on tier C.

Evidence:
- **C (brand):** Similarweb puts risk.net at $15-25M revenue, 51-200 employees ([Similarweb](https://www.similarweb.com/company/risk.net), snippet). It is the only brand-level estimate I could find. A repeat search for ZoomInfo, Owler and Growjo turned up profiles for unrelated companies named "Risk" only, so there is no conflicting estimate; the Similarweb floor of $15M meets the 50% test. Strictly, "every available estimate" here means one estimate.
- **A (parent):** Infopro Digital Services Ltd (Companies House 04699701), FY2025 filed accounts, note 3: turnover GBP 45,840,193 (about $58-61M), of which Data & Information Services 22.8M, Events 17.2M, Marketing 4.0M, Training 1.8M; no brand split. Note 7: 216 average employees (95 editorial/production). The strategic report lists Risk.net among eight brands (Risk.net, Central Banking, FX Markets, WatersTechnology, Insurance Post, Insurance Age, Chartis, 1LOD). [Filing history](https://find-and-update.company-information.service.gov.uk/company/04699701/filing-history). The PDFs are scans read visually, not OCR'd.
- **Corroboration only:** Infopro job posts call Risk Global (Risk.net, Central Banking, Chartis, FX Markets, WatersTechnology) "a 300-person organisation" ([job post](https://builtinlondon.uk/job/reporter-risk-net/7900559)); 300 x $150-250K = $45-75M for the whole unit, which cannot isolate Risk.net. The 2017 sale release gave GBP 40M for the four-brand Insight Group (350+ staff) and a Risk.net team of 40 ([Infopro](https://www.infopro-digital.com/news/insight-group-division-dincisive-media-rejoint-infopro-digital-2/)); 40 x $150-250K = $6-10M, which does not clear the line on its own and is a 2017 figure. I read this as inconclusive, and it is the main reason to treat the tier C result with care.
- No Incisive Risk Information Ltd exists in Companies House. Infopro Digital Risk (IP) Ltd (09232733) is an IP-holding company that did not trade in FY2025. Infopro Digital Risk Ltd, Insurance Information Ltd and RWG Ltd were dissolved in 2020.

Proposed revenue figure: none by rule (tier C does not update the figure). The $50M on the row is the four-brand 2017 bundle and the row's own notes say it must not be attributed to Risk.net. If the parent relabel is chosen: "Infopro Digital Services Ltd (Risk.net et al.)", GBP 45.8M FY2025 (tier A). Parent founding year **not verified**: the company number was incorporated in 2003, the Infopro group founding year was not found, Risk magazine launched Dec 1987 ([Wikipedia](https://en.wikipedia.org/wiki/Risk_(magazine)), single source). The 30,000+ subscriber claim was not found.

Origin: CROSSED stays; I have not documented a single-title start for Risk magazine beyond the 1987 launch.

Downstream effect: none on counts. Risk.net already shows "Revenue estimate unverified" (`un`=1), which this tier C evidence does not clear for the hover text; whether to drop the flag is for Justin and Andy.

Gaps: Infopro Digital Holding (UK) and Infopro Digital B.V. consolidated accounts not examined.

---

## J3-b Defense One / GovExec

**Verdict: RELABEL. Rule 2.** No Defense One standalone revenue found, so rule 1 is not met; the parent runs the unit and is predominantly B2B media and events (it also now includes market-research and data units: Market Connections, GovTribe).

**Proposed name: "GovExec (publisher of Defense One)".**

Evidence (revenue above $10M):
- **A/B borderline, a projection:** Axios, Sept 14, 2021, CEO-sourced: about $50M on track for 2021, up from about $20M in 2020; 200+ employees against 80 at the March 2020 spin-off ([Axios](https://www.axios.com/2021/09/14/govexec-market-connections-acquisition), snippet; page returned 403).
- **B-:** A Media Operator, 2022-05-23: 2020 sales about $18M, 2022 projection "north of $70 million", about 300 employees ([A Media Operator](https://www.amediaoperator.com/podcast/tim-hartman-on-govexecs-rapidly-growing-business/), snippet, paywalled).
- **Corroboration only:** 177-300 employees x $150-250K = $27M-$75M; even the 80 employees at the 2020 spin-off give $12M-$20M. Datanyze lists $59.6M and 267 employees (unverified). I did not re-check the $9.8-16.6M broker estimates in the row notes, which I could not reproduce. No source I found puts the company below $10M. No tier A source (private company, no filings found).
- Both the Axios and A Media Operator figures are projections. I read them as clearing the line by 50% on every figure found (floor $18M for 2020), which is why the verdict stands under the evidence standard, but the standard calls for actual statements of revenue and these are CEO-sourced projections.

Proposed revenue figure and year: about $50M (2021 projection, Axios), 2020 floor about $18-20M. Per the rule the figure is updated only on tier A/B; this is borderline B, so leave the label "projected" as the row has it.

**Founding year (flag for the History dek):** Government Executive magazine's first issue was March 1969, founding editor and publisher C.W. Borklund ([GovExec](https://www.govexec.com/federal-news/fedblog/2019/03/five-decades-government-executive/155192/), [Wikipedia](https://en.wikipedia.org/wiki/Government_Executive); a 1999 editorial says January 1969). Defense One launched 2013. The company as an entity dates from the March 2020 spin-off, so 1969 is the flagship title's year, not the company's. **Using 1969 moves the row from 2013 (after the 1995 cut) to before it.**

Origin: keep CROSSED. Documentation: it began as a single print monthly for federal executives in 1969, on the web from 1996, last print issue 2015; acquired by National Journal Group in 1987, then Atlantic Media in the late 1990s, then sold to Growth Catalyst Partners in March 2020, terms undisclosed ([Adweek](https://www.adweek.com/digital/atlantic-media-sells-off-government-executive-media-group/)).

2025-26: Growth Catalyst Partners still owns it; GovExec bought Federal Business Council in Feb 2025; CEO Tim Hartman stepped down Oct 13-14, 2026 and Dan McCarthy took over ([Washington Technology](https://www.washingtontechnology.com/companies/2026/10/govexec-announces-leadership-change/416556/), [A Media Operator](https://www.amediaoperator.com/news/govexec-replaces-longtime-ceo-with-turnaround-executive/)). No revenue or headcount was given.

Downstream effect: name changes on the card. Band, cohort, mechanism and origin unchanged. If the row is dated 1969, History dek: before 1995 "24 of 38" becomes "25 of 39"; since 1995 "31 of 130" becomes "30 of 129" (99 under either way). If it stays 2013, no change.

---

## J3-c Insurance Journal

**Verdict: UNRESOLVED. Rule 4.** Rule 1 fails (tier C only; Owler's $5-25M range has a floor under $15M). Rule 2 fails (no group-level figure for Wells Media Group either). Rule 3 fails (nothing puts it below).

Evidence (all estimates, all tier C):
- Prospeo: $15M, 21-50 employees ([Prospeo](https://prospeo.io/c/wells-media-group)). A-Leads: $15M, about 50 employees ([A-Leads](https://a-leads.co/company/5714595_e314ea01)); the two probably share an upstream source.
- ZoomInfo: $17.1M, 11-50 employees (via search summary, [ZoomInfo](https://www.zoominfo.com/c/wells-media-group-inc/127451188)). LeadIQ: $25-50M (via search summary, [LeadIQ](https://leadiq.com/c/wells-media-group-inc/5a1da2d2230000520094c0dc)). Bounce Watch: about 49 employees.
- Owler: $5-25M, 25-100 employees ([Owler](https://www.owler.com/company/wellsmedia)). This is the estimate that fails the 50% test.
- **Corroboration only:** about 50 staff x $150-250K = $7.5-12.5M; 100 staff = $15-25M; 25 staff = $3.75-6.25M. This straddles the line and decides nothing. No official headcount found.
- No revenue in the ESOP announcements ([Insurance Journal](https://www.insurancejournal.com/magazines/mag-features/2021/12/20/645853.htm), [Claims Journal](https://www.claimsjournal.com/news/national/2021/12/13/307519.htm), [PR Newswire](https://www.prnewswire.com/news-releases/wells-media-group-transitions-ownership-to-its-employees-301442859.html)). Audience: 47,000+ BPA-audited print subscribers ([IJ](https://www.insurancejournal.com/advertise/magazine)), 441,351 monthly uniques per AAM Jan-Jun 2025 ([IJ](https://www.insurancejournal.com/advertise/ij-website-advertising.php)). No rate card or revenue found.
- **Leads tried:** ESOP coverage, Form 5500 searches (web search, form5500search.com, FreeERISA, which returned 403), industry rankings, executive interviews, headcount. Not found: any Wells Media Group ESOP 5500 filing, Folio/Connectiv ranking, interview with revenue. **Lead not exhausted:** a manual EFAST2 sponsor search (efast.dol.gov) for the Wells Media Group ESOP (assets, participants, contributions) was not run. Of the leads, it is the most likely to produce a tier A document, so if Justin and Andy want to avoid the exclusion, that is the 15 minutes to spend. The earlier "$597M" figure did not reappear.

Origin documentation (supports keeping CROSSED, company documents only): the About page says Insurance Journal "kicked off its legacy some time in 1923" and grew "from a regional Southern California magazine with 4,000 readers" ([IJ About](https://www.insurancejournal.com/about/)); the 2003 80th-anniversary story calls it "essentially a Southern California publication" ([IJ](https://www.insurancejournal.com/magazines/mag-coverstory/2003/10/20/33333.htm)). One weak directory source says it began as a life insurance magazine in Los Angeles. The 2023 "100 Years Young" piece was not found. Founding year 1923; the Wells family bought it in 1936 ([Wells Media](https://www.wellsmedia.com/)).

If relabeled later: "Wells Media Group (publisher of Insurance Journal)", founded 1923.

Downstream effect if excluded as "revenue unverifiable": see the net line. Above $10M 55 to 54; grew past 30 to 29; C9 17 to 16; M4 wedge 11 to 10; N 169 to 168; bands 80 / 34 / 55 become 80 / 34 / 54; History dek before 1995 "24 of 38" becomes "23 of 37".

---

## J5 Platformer

**Verdict: KEEP, BELOW $3.5M. Rule 1.** No tier A dollar figure exists for Platformer, so the figure stays an estimate.

Evidence:
- **A for scale (qualitative):** Newton, January 2024: paid subscribers "grew into the thousands", and leaving Substack saves "tens of thousands of dollars" a year, which is Substack's 10% cut ([Platformer](https://www.platformer.news/why-platformer-is-leaving-substack/)). A $3.5M year would mean a cut of about $350K, which does not fit.
- **B math:** Nieman Lab, Sept 2023: about 7,750 paid x about $100 a year = about $775K gross ([Nieman Lab](https://www.niemanlab.org/2023/09/what-casey-newton-learned-in-year-3-of-running-his-substack/)); 155K list, 95% free. Newton's year-3 post implies about $100 a sub and gives no count ([Platformer](https://www.platformer.news/how-platformer-is-changing-in-year/)).
- Year 4, Sept 2024: 190,196 total subscribers, revenue "up about 11 percent", ads "nearly" six figures in the first year, no dollar totals ([Platformer](https://www.platformer.news/leaving-substack-platformer-year-four/)). Year 5, Sept 2025: "thousands" of paid subscribers, 200K free, prices unchanged in five years, growth slowed, ads sold out, "five jobs" funded, no revenue figure ([Platformer](https://www.platformer.news/platformer-year-five-lessons/)).
- **The math for IN-band:** $3.5M at about $100 a year needs about 35,000 paying subscribers, about 18% of 190K, against "thousands" and a historical paid rate under 10%.
- **The conflicting claim:** "self-disclosed ~$3.5M ARR Dec 2023" was **not found** in any Platformer post, interview or search, so it is unsourced and meets no tier. The Ghost move was announced January 2024, not 2023.

Proposed revenue figure and year: unchanged at about $900K (range about $0.8-1.0M, FY2023-24; tier B subscription gross $775K for 2023). Most recent full year with a usable estimate is 2023-24.

Downstream effect: none. Gaps: no exact paid count, no group or founding tier prices, ad income undisclosed; I did not verify the Verge license or Hard Fork income.

---

## Quick confirmations (hover text only)

- **Puck / RedBird: closing NOT verified.** Announced 2026-09-24 at about $250M with about a month to close pending approval ([Dealroom](https://dealroom.co/news/156112-redbird-takes-majority-stake-in-puck-at-250m-valuation/)). Hollywood Reporter and Editor & Publisher use "closes" and "completed" but are dated the announcement day, likely loose wording ([Hollywood Reporter](https://www.hollywoodreporter.com/business/business-news/redbird-closes-deal-become-lead-investor-puck-1236709304/), [E&P](https://www.editorandpublisher.com/stories/redbird-clinches-deal-to-become-lead-investor-in-puck,263716)). Nothing dated after 2026-09-25. Neither the primary-source nor the two-independent-sources test is met. Hover implication: "acquired" is not yet supported.
- **CNN / Paramount-WBD: closed 2026-10-06** per three outlets ([CNBC](https://www.cnbc.com/2026/10/06/paramount-wbd-deal-timeline.html), [CBS](https://www.cbsnews.com/news/paramount-warner-bros-discovery-deal-skydance/), [PBS/AP](https://www.pbs.org/newshour/economy/after-tumultuous-fight-paramount-completes-takeover-of-warner-bros-to-become-hollywood-giant-skydance)). **The brief asked for a primary source and I did not find the closing release or 8-K** (the SEC exhibit that surfaced is the Feb 27, 2026 announcement), so strictly this is not confirmed at the standard you set.

---

Net change: above $10M 55 to 54, grew past 30 to 29, C9 17 to 16, M4 11 to 10, all from excluding Insurance Journal as unverifiable; Risk.net, GovExec and Platformer move no counts (History dek only: Insurance Journal out gives 23 of 37 and 31 of 130; GovExec dated 1969 instead gives 25 of 39 and 30 of 129; both together give 24 of 38 and 30 of 129).
