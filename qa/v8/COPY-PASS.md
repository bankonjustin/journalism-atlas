# Copy pass (v8): before and after

Every string is now in `nn/content/copy.md`. Numbers are tokens. Meaning kept unless flagged.

| Where | Before (v7) | After |
|---|---|---|
| Header sub | 169 U.S. journalism organizations · Nine governance cohorts | {n_orgs} U.S. journalism organizations, sorted into {cohorts_word} kinds of newsroom |
| In short, color key | Color is who pays. A square started above $10M, a triangle grew past it, and a dashed mark is the exception. | Color shows who pays. A square started above $10M. A triangle grew past it. A dashed triangle is the exception. |
| Chapter 1 line | Nine kinds of newsroom, grouped by who pays for them. Four of the nine hold 48 of the 55 organizations over $10 million. The other five hold 7. | Nine kinds of newsroom, sorted by who pays. Four of them hold 48 of the 55 organizations over $10 million. The other five hold 7. |
| Chapter 1 title | Four of nine kinds of newsroom hold 87% of the big ones. | Four of nine kinds of newsroom hold 87% of the organizations over $10 million. ("big ones" was undefined) |
| Chapter 1 stat | 169 organizations, 9 cohorts, 3 groups. | 169 organizations. Nine cohorts. Three groups. |
| Chapter 1 position note | Position: each wedge is one cohort. | Each wedge is one cohort. |
| Chapter 2 line | 31 organizations grew past $10 million. 30 did it one of six ways. | 31 organizations grew past $10 million. 30 of them did it one of six ways. |
| Chapter 2 title | The 6 ways to grow beyond $10M | Six ways to grow past $10 million |
| Chapter 2 stat | Of the 31 organizations that grew past $10M, 30 did it through one of the six mechanisms, with one exception. | Of the 31 organizations that grew past $10M, 30 did it one of six ways. One exception. |
| Chapter 2 position note | Position: each sector is one mechanism. ... still under $10M have their own sections. | Each sector is one mechanism. ... still under it have their own sections. |
| Chapter 3 line | ...But when they started matters less than who pays them. | ...But who pays matters more than when an organization started. |
| Chapter 3 dek | Organizations founded before 1995 — when the internet began reshaping print and broadcast distribution — mostly run above $10 million: 24 of 38. Organizations founded since mostly don't: 31 of 130. And only five of the nine kinds of organization in this study existed before 1995. The rest are new ways to pay for journalism, and most of the organizations using them are still small. | The internet began reshaping print and broadcast distribution in 1995. Organizations founded before then mostly run above $10 million: 24 of 38. Those founded since mostly don't: 31 of 130. Only five of the nine kinds of newsroom in this study existed before 1995. The rest are new ways to pay for journalism, and most of their organizations are still small. |
| Chapter 3 foot | Position: founding year, left to right; the axis is compressed before 1995. ... predicts an organization's revenue band more strongly... | Position is founding year, left to right. The axis is compressed before 1995. ... predicts an organization's revenue more strongly... ("revenue band" cut) |
| Legend row label | How they crossed $10M in revenue | Shape |
| Annotation, small cohorts | Co-ops and civic: 0 of 34 over $10M. | Worker-Owned Co-ops and Emerging Civic Actors: 0 of 34 over $10M. (paper's names) |
| Annotation, second | B2B: 11 of 17. | B2B/Professional Services: 11 of 17. (paper's name) |
| Card revenue line | Under $3.5M in revenue / $3.5M to $10M in revenue | $10M or under in revenue (the $3.5M band language is removed, per the ground rules) |
| Attribution | Walter Cronkite School of Journalism and Mass Communication at Arizona State University. | {publisher_line} (Knight Center for the Future of News, ASU Cronkite School) plus the report link |
| Report link | none | "About the report" until `report_url` is set; then "Read the full report" |
| Video | pre-v7 governance loop, "[REPORT URL: PLACEHOLDER]" baked in | Seven captions from copy.md over the v7 explorer; end card = title, publisher line, journalismatlas.com |
| Embed page | EMBED.md ("Replace {{EXPLORER_URL}}...") | New page with the same four snippets and the tab table, plain verbs, and a line on who may frame it |

## Flagged (kept as is, or needs Justin's call)
- **"Under $10M" vs "$10M or under"**: the chart labels say "Under $10M", the history legend and card say "$10M or under". The data splits at "over $10M", so the second is exact. Not changed because it touches a claim. Say the word and I will make them match.
- **Locked paper text** (chapter sentences quoted from the paper, nine cohort names, three group names, six mechanism descriptions) is untouched and guarded by the build.
- **Era labels** (1995–2007, 2008–2014, 2015 or later) and the axis ticks stay in the chart code: they are bin definitions, not prose.
- **"Four of them hold 48 of 55"** and the history lines are claims about counts. They are unchanged and now derive from the data in Python; the page script derives the same numbers for the charts, and I checked they agree (55 / 48 / 7, 24 of 38, 31 of 130).
