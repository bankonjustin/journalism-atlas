> **Superseded Nov 1, 2026 (evening).** Justin ruled option A, implemented differently: `nn/data/snapshot-overrides.csv` (not an edit to the recode CSV). Two claims below are wrong: `nn/` built 31 grew past / 24 started above (Iowa, not only Rogan), and `orig` did not match on all 169 rows (Iowa differed). See `nn/data/nodes169.CHANGELOG.md` and the leave-off log.

# Phase 1 item 1: Rogan and the launch target (needs Justin's ruling)

Nov 1, 2026. Nothing below is applied. Working tree is clean (`8179b90`). The options were tested in a scratch copy of `nn/` outside the repo; the repo was not touched.

## The problem

DECISIONS-QUEUE L10 sets `/nodes-and-networks/` (built from `nn/`) as the launch target. The same day, Carrie's ASU embed goes live with a different coding of one organization.

| | ASU embed (`preview/nn-launch-kit/explorer/`) | `nn/` build |
|---|---|---|
| Joe Rogan Experience | M3 (team + portfolio) | Exception (platform licensing) |
| Counts | 169 orgs; 30 grew past $10M, 25 started above, 114 below | same counts |
| "Exception" wording | none in the file | "one exception" (build prints "Zero exceptions." once Rogan is moved, see below) |
| "who pays" | none | 14 lines in `nn/content/copy.md` |

The two pages would disagree about Rogan on launch day, and `nn/` carries copy the brief's style rules ban.

## What I found that changes the shape of the fix

1. **`nodes169.json` does not need to change.** `nn/build.py:load_nodes()` takes each node's mechanism (`m`) from `nn/data/public-snapshot.json`, not from `nodes169.json`. `nn/tools/snapshot.py` builds that file from `nodes-networks-v5/launch-kit/MECH-RECODE-PROPOSED.csv` (approved rows) and falls back to `nodes169.json` only for rows with no approved recode. The build reads only `p.field` and `lenses.gov` from `nodes169.json`. So the read-only file stays read-only under every option below.
2. **Rogan's Exception coding is a ruling of yours, recorded in that recode file.** The approved row reads: `Joe Rogan Experience, C2, EXCEPTION_PLATFORM_LICENSING → EXCEPTION_PLATFORM_LICENSING, "stays the Exception per your Oct 26 decision", approved: yes`. The paper does not name Rogan ("Not named in the paper"). So option A overturns your Oct 26 call; it is not a data cleanup.
3. **The ASU embed's M3 for Rogan is not explained anywhere I read.** I don't know whether that was ASU's choice, an older coding, or a deliberate reversal. Ask Carrie before treating it as the paper's answer.
4. The embed codes the 25 "started above" orgs by their real mechanism; `nn/` collapses them to `INHERITED_SCALE`. That is a display difference, `orig` matches on all 169, and it doesn't touch the counts. Three names differ between the files (Washington Post, Risk.net, Insurance Journal, the three unverified ones). I did not diff them further.

## Option A: make `nn/` agree with the ASU embed (Rogan to M3). Recommended.

Why: one answer on Thursday, the ASU embed untouched, `/nodes-and-networks/` stays the target (L10), and the only canonical-data change is one recode row you approve.

Changes (about 20 minutes plus a build check and 1280/390 screenshots; ready by Tuesday):

1. **Recode row** in `nodes-networks-v5/launch-kit/MECH-RECODE-PROPOSED.csv` (outside this repo; your file):
   ```
   - Joe Rogan Experience,Joe Rogan Experience,C2,EXCEPTION_PLATFORM_LICENSING,EXCEPTION_PLATFORM_LICENSING,med,Crossed on an exclusive platform licensing deal; stays the Exception per your Oct 26 decision,Not named in the paper,,yes
   + Joe Rogan Experience,Joe Rogan Experience,C2,EXCEPTION_PLATFORM_LICENSING,M3_new_org_team_and_portfolio,med,<your reason>,Not named in the paper,,yes
   ```
2. **Regenerate** `nn/data/public-snapshot.json` with `python3 nn/tools/snapshot.py` (local only; reads the private CSV read-only). Expected diff is one field on node 18. I'll check `git diff` shows only that.
   ```
   -{"i":18,"nm":"Joe Rogan Experience","fy":2009,"o":"CROSSED","m":"EXCEPTION_PLATFORM_LICENSING",...
   +{"i":18,"nm":"Joe Rogan Experience","fy":2009,"o":"CROSSED","m":"M3_new_org_team_and_portfolio",...
   ```
3. **Engine guard**, `nn/src/engine.js:60`. Today the Exception sector is always drawn, so with no exception it would render an empty labelled wedge:
   ```
   -const keys = [...M.paths.map(p => p.key), 'EXCEPTION_PLATFORM_LICENSING', ...(N.some(n => n.o === 'INHERITED') ? ['INHERITED_SCALE'] : []), 'BELOW'];
   +const keys = [...M.paths.map(p => p.key), ...(N.some(n => n.m === 'EXCEPTION_PLATFORM_LICENSING') ? ['EXCEPTION_PLATFORM_LICENSING'] : []), ...(N.some(n => n.o === 'INHERITED') ? ['INHERITED_SCALE'] : []), 'BELOW'];
   ```
   The explorer template already guards its own exception rows (`EXC.length`, `hasExc`). With this guard, the scratch build passes (`build.py --check`: ok, warnings unchanged).
4. **Copy**, `nn/content/copy.md`. Tested: without edits the build prints "Zero exceptions." and "The exception: , a platform licensing deal."
   ```
   ## in_short.encoding   (line 71)
   -Color shows who pays. A square started above $10M. A triangle grew past it. A dashed triangle is the exception.
   +Color shows governance. A square started above $10M. A triangle grew past it.

   ## chapter2.stat   (line 114)
   -Of the {crossed} organizations that grew past $10M, {six_way_growers} did it one of six ways. {exceptions_phrase|cap}.
   +All {crossed} organizations that grew past $10M did it one of six ways.
   ```
   `chapter2.stat` assumes zero exceptions and will read wrong if the data changes; say if you'd rather keep a token-driven sentence. `ann.ways_exception`, `legend.grew_past_exception` and `list.no_mechanism*` become unused (the page doesn't render them with no exception); I'd leave them in place.
5. **Mechanical, option-independent:** replace "who pays" (14 lines: 42, 68, 71, 79, 82, 85, 131, 134, 140, 143, 502, 541, 572, 587) with governance wording. Proposed table:

   | Line | Now | Proposed |
   |---|---|---|
   | 42, 502 | `1 Who pays` | `1 Governance` |
   | 68 | Who pays for journalism shapes how big it gets. | Governance shapes how big a journalism organization gets. |
   | 79, 82 | `Chapter 1: who pays` / `Who pays` | `Chapter 1: governance` / `Governance` |
   | 85, 572 | sorted by who pays | sorted by governance |
   | 131 | But who pays matters more than when an organization started. | But governance matters more than when an organization started. |
   | 134 | Who pays them matters more. | How they are governed matters more. |
   | 140, 143 | Who pays predicts an organization's revenue more strongly than when it was founded. | Governance predicts an organization's revenue more strongly than when it was founded. |
   | 541 | colored by who pays | colored by governance |
   | 587 | (as 131) | (as 131) |

   Editorial: the chapter name change touches headings Andy may have on paper. Flag to Andy.
6. After copy edits: `python3 nn/build.py --fallback` to refresh `nn/built/` (never `ship.sh`: it commits and pushes). Then brand check and screenshots.

Risks: overturns your Oct 26 ruling; the paper doesn't name Rogan so nothing contradicts the change, but Carrie should confirm the M3 coding is intended. Copy edits go in under the launch freeze.

## Option B: make the launch target a page built around the live ASU explorer

The ASU file already has the right data and no "who pays" or "exception" wording, so there is nothing to recode. But it is a single explorer page, `noindex`, and I can't edit, move or redirect it. A target page would have to be a new Atlas-side wrapper that frames it. You'd lose the `nn/` chapters, video, share images and embed page, or have to rebuild them. Embed theme: the file uses the ASU look in `?embed=1`, so a full-page wrapper means checking which theme it shows standalone; I haven't tested that. It also changes L10 and puts a framed ASU page at the Atlas's launch URL. Not recommended for Wednesday.

## Option C: keep Rogan as the Exception and ask ASU to match

Keeps your Oct 26 ruling. Needs a change to the live ASU explorer (Carrie's file), which I can't make without an explicit ruling, and would need the embed's counts, legend and copy to grow an exception case it doesn't have today. Highest coordination cost with the least time.

## Option D: launch `nn/` as is, fix only the wording

Lowest effort: do item 5 above only. Leaves Rogan inconsistent between two pages that launch together. Only acceptable if Carrie confirms the ASU embed will be corrected to the Exception.

## Questions for you

1. Which option? I recommend A.
2. If A: what rationale goes in the recode row, and do you want me to tell Carrie about the M3 mismatch or will you?
3. If A: OK to apply the engine guard and copy edits (items 3–5) in the working tree for you to review and commit?
