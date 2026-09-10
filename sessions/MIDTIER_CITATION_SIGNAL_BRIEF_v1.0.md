Mid-Tier Citation Signal — Brief v1.0
For: Claude Code (run in Justin's environment, with actual repo access)
From: Claude Chat (strategic framing — no repo/file access from this session)
Date: September 9, 2026
Changelog: v1.0 — initial brief.

0. Why this brief exists
A recent work session named a specific, differentiated data point: media mentions calibrated to "pre-NYT level" — the citation tier that matters isn't "got cited by the New York Times," it's the tier below that, which funders and platforms don't already track. This is explicitly named as next-to-build, not built. This brief scopes it as a bounded, honestly-labeled experiment — unlike the other briefs, this signal is unproven, so the task is structured with a clear go/no-go rather than an assumed build.

1. Established facts
- Tubular via@ attribution mining is a validated, adjacent method: extracting "via @username" style credits from video titles. It works only where inline source credit already exists in the content — confirmed not to work against general-interest news publishers in a clean test. This new signal is different (text/article citations, not video-title credits) and should not be assumed to inherit that method's validation.
- No existing schema field tracks "who cites this creator" or a citation tier — this would be a genuinely new data point, not an extension of an existing column.
- Known platform access constraints: Substack, Beehiiv, and Instagram are egress-blocked in the current environment — use web search snippets, not web fetch, for research on these platforms.
- The four trust-core fields include "notable citations" as one of the load-bearing fields — this signal, if it works, is the concrete mechanism that would populate that field with real data rather than a manually-curated note.

2. Assumptions to verify
- What "mid-tier" actually means is currently undefined at the strategy level — there is no seed list of outlets. This must be defined before any extraction work, not inferred.
- Whether any existing Tubular or Pulse data already incidentally captures text-citation patterns that could be mined retroactively, cheaper than building new collection from scratch.
- Whether article-text citation mining is technically feasible at all given the egress-blocked platforms, or whether it only works against outlets with open web access (which may itself define what "mid-tier" can mean in practice, separate from the editorial definition).

3. Tasks
Task A — Define "mid-tier" concretely (propose, don't lock in)
Propose a seed list of outlets one tier below the major nationals already used in the via@ methodology — candidates: trade press, regional papers, niche digital-native outlets. This is a proposal for Justin/Ryan to confirm or adjust, not a unilateral decision.

Task B — Prototype a text-citation extractor
Build a small extraction script, in the spirit of the existing via@ regex approach, but targeting article body text for attribution patterns ("according to," "as [name] wrote," "cited by," name-drops with a link) rather than video-title credits. Test against a small sample (10–20 articles) from the seed list in Task A.

Task C — Cross-reference against master
Dedup extracted names against `creators-master.csv` by slug/name. Report what fraction are already-known creators (validates the signal is finding real people) versus genuinely net-new candidates (validates it as a discovery method, not just an enrichment one).

Task D — Report yield and false-positive rate, with a clear stop condition
This method is unproven — treat it as an experiment with an explicit go/no-go: if false-positive rate is high or net-new yield is near zero on the test sample, report that plainly and stop rather than expanding scope to "make it work."

Task E — If viable, propose the schema hook (don't build yet)
If Task D shows real signal, propose how this becomes the actual data behind the "notable citations" trust-core field — what gets stored, at what granularity, updated how often. Proposal only; no new columns added to master without normal review.

4. Guardrails
- This is explicitly experimental. Do not treat validated status from the via@ method as transferring to this one.
- Respect egress-block constraints — no direct fetch against Substack/Beehiiv/Instagram; use search snippets.
- No new columns in `creators-master.csv` until the signal is validated and reviewed.
- Small sample first (10–20 articles) before any larger run — this keeps the experiment cheap to kill if it doesn't work.
