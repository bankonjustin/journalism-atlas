# ORIGINAL.md — the circle video, Phase 1 (read-only)

Written 2026-10-29. Nothing in the explorer, copy.md, `_headers` or `_redirects` was touched. Searched `nodes-networks-v5`, `journalism-atlas`, `journalism-atlas-private` (plus `-private-round7` and `-watershed-go`), ignored/superseded/scratch folders included. No ffmpeg/ffprobe on this Mac, so length and size come from `mdls`, and frames were pulled with an AVFoundation script.

## 1. Inventory of every .mp4/.webm/.mov (no .webm or .mov exist)

| Path | Modified | Length | Size (px) | Shows |
|---|---|---|---|---|
| `nodes-networks-v5/kaleidoscope/turn/nn-turn-feed.mp4` | Oct 23 22:02 | 15.0 s | 1080×1350 | **Circle video, short cut.** Black. Spiral build → spin → mirror → wedges → cohort sweep |
| `…/turn/nn-turn-square.mp4` | Oct 23 22:02 | 15.0 s | 1080×1080 | same, 1:1 |
| `…/turn/nn-turn-story.mp4` | Oct 23 22:02 | 15.0 s | 1080×1920 | same, 9:16 |
| `…/reel/nn-reel-long-square.mp4` | Oct 24 09:26 | 30.0 s | 1080×1080 | **Circle video, long cut.** The 15 s turn plus "How they got past $10M" and "When they started" |
| `…/reel/nn-reel-long-feed.mp4` | Oct 24 09:26 | 30.0 s | 1080×1350 | same, 4:5 |
| `…/reel/nn-reel-long-story.mp4` | Oct 24 09:27 | 30.0 s | 1080×1920 | same, 9:16 |
| `…/reel/nn-reel-short-square.mp4` / `-short-feed.mp4` / `-short-story.mp4` | Oct 24 09:27 | 15.0 s | 1080² / 1080×1350 / 1080×1920 | the turn again, with a footer URL |
| `…/reel/nn-reel-short-feed-540.gif`, `…/turn/nn-turn-feed-540.gif` | Oct 23–24 | n/a | 540 wide | GIFs of the same |
| `nodes-networks-v5/launch-kit/out/video/nodes-networks-governance-4x5.mp4` | Oct 28 15:10 | 24.0 s | 1080×1350 | v7 loop: coloured wedges (governance) rotate/fold, legend, "[REPORT URL: PLACEHOLDER]" button. No ways view |
| `…/launch-kit/out/video/nodes-networks-governance-9x16.mp4` | Oct 28 15:10 | 24.0 s | 1080×1920 | same, 9:16 |
| `journalism-atlas/preview/nn-launch-kit/video/nodes-networks-governance-{4x5,9x16}.mp4` | Oct 28 22:26 | 24.0 s | as above | byte-identical copies of the two above (same sizes) |
| `journalism-atlas/nn/media/nodes-networks-16x9.mp4` / `-9x16.mp4` | Oct 29 08:02–08:03 | 52 s | 1920×1080 / 1080×1920 | **Current v8 kit video.** White page, scrolling screenshots of the explorer tabs with captions. Not a circle video |
| `journalism-atlas/dist/nodes-and-networks/media/nodes-networks-{16x9,9x16}.mp4` | Oct 29 08:28 | 52 s | as above | build copies of the v8 pair |
| `…/dist/…/media/nodes-networks-16x9 2.mp4`, `-9x16 2.mp4` | Oct 29 08:28 | unreadable by Spotlight | | Finder-style duplicate copies (" 2"); same byte sizes as the v8 pair. Stray files |
| `journalism-atlas-private/docs/nodes-and-networks-v5/launch-kit/named-explorer-hover-capture.mp4` | Oct 26 22:53 | 22.4 s | 1100×1400 | screen capture of the old named-explorer hover (the earlier cursor-hover precedent) |

Render scripts found: `nodes-networks-v5/launch-kit/capture_video.py` + `encode.swift` + `qa/pass1/render_video.sh` (Oct 28 loop); `journalism-atlas/nn/tools/render_media.py` + `encode.swift` (v8, current); `launch-kit/record_named.py` (hover capture). **No script was found for the Oct 23/24 turn/reel MP4s themselves** (see §3).

## 2. Which one is the original

The circle video is the Oct 23–24 kaleidoscope render. Candidates, earliest first:

1. `turn/` (Oct 23, 15 s). Complete, but it stops at "Governance determines so much." It has no "how they got past $10M" wedge beat.
2. `reel/long` (Oct 24, 30 s). The same first 15 s, then the three-wedge "How they got past $10M" beat and "When they started". Its beat 7 is the only one that corresponds to today's "6 ways" tab, and it carries the "25 / 30 / 114" counts the brief says are now wrong.
3. `launch-kit` governance loop (Oct 28). Post-v7, so not the original; no ways view.

**Pick: `reel/nn-reel-long-square.mp4` (30 s).** The turn video is its first 15 s, so choosing the long cut loses nothing. This is a judgment call against the "earliest complete" rule, because the turn file is earlier. The brief's mention of the Ways chart and the Rogan counts only makes sense against the long cut. Say so if you want the 15 s version instead.

One wrinkle in the brief's wording: in the original, the rotating wedges are **governance cohorts** (C1–C9), and the wedge beat for ways is "Started above / Grew past it / Still under", three wedges, not the six mechanisms. The six-mechanism wedges never appeared in any video.

## 3. Render method

- Source: `reel/nn-reel-player.html`. A deterministic canvas frame function, `frame(ctx, F, t, cut)`, drawn from the embedded 169-row dataset, one renderer for all sizes ("so the MP4, the GIF, the share still and the live page cannot disagree"). Engine: `reel/nn-kaleido-engine.js`.
- It was **a synthetic canvas animation, not a recording of the explorer.** Marks, spiral, mirror, zones and wedges were drawn by the player's own code.
- Encode: `encode.swift` (AVFoundation H.264), same as the Oct 28 loop. The shell command for these two files is not in the repo. Inferred from the Oct 28 `render_video.sh`: Playwright frame-by-frame PNG capture, then `swift encode.swift <frames> <out.mp4> <w> <h> 30 <bps>`. Inferred, not confirmed.
- Output: 30 fps, 30.034 s, 5.5 to 8.6 MB per file.

## 4. Beat sheet — `nn-reel-long-square.mp4` (timings from the player's `SHOTS`/`TOUR` tables, checked against frames at 2.5 s steps)

Frame furniture throughout: top-left "NODES AND NETWORKS", top-right "KNIGHT CENTER · JOURNALISM ATLAS", black background, headline sans bold, subline serif.

| # | Time (s) | On screen / motion | Caption |
|---|---|---|---|
| 1 | 0.0–1.4 | Grey marks appear one by one along a golden-angle spiral | "169 organizations." |
| 2 | 1.4–4.6 | Field spins (1.6π ease-in-out over 6.4 s) and folds into an 18-segment mirror, a kaleidoscope. Illustration only | "From far away, the field looks like the trends you already know." |
| 3 | 4.6–7.7 | Mirror falls away, bare field holds ~0.7 s, then each mark flies to its cohort wedge and takes group colour (gold / maroon / grey) as it lands. Staggered by angle (~0.45 s) over 2.2 s | "Turn the lens to governance." |
| 4 | 7.7–8.9 | Dashed rings sweep in at $3.5M and $10M; zone pills "Under $3.5M", "$3.5M–$10M", "Over $10M"; cohort codes C1–C9 appear | "Closer to the center, smaller budgets. Lines at $3.5M and $10M." (the 15 s turn cut says "Two lines: $3.5M and $10M.") |
| 5 | 8.9–12.1 | Each cohort lights in turn (others dim to 18%); 0.30 s each, 0.47 s for the three smallest (C3, C6, C7) | Cohort code, name, count, e.g. "C4 Philanthropic Networks, 44 organizations" |
| 6 | 12.1–13.6 | All lit, hold | "Governance determines so much." |
| 7 | 13.6–19.4 | Marks regroup into **three wedges** with zones kept: "Started above", "Grew past it", "Still under" | "How they got past $10M." then "25 started above it. 30 grew past it. 114 are still under." |
| 8 | 19.4–25.2 | Marks move to founding year (oldest inside), zones fade, year rings appear | "When they started." then "Distance from the center now means founding year. 113 of 169 started in 2008 or later." |
| 9 | 25.2–30.0 | Back to governance wedges; footer fades in | "Turn the lens yourself." Footer: "169 U.S. journalism organizations · nine governance cohorts" and "journalismatlas.com/research/nodes-and-networks" |

## 5. Old numbers and labels now wrong (each checked against the current build)

Current build = `journalism-atlas/preview/nn-launch-kit/explorer/index.html` as it stood at the time of this read (uncommitted; md5 `47b7ad63bff848139b1cb894d1b4862b`). Counts are computed from its embedded `nn-data` JSON (`o`=origin, `m`=mechanism, `c`=cohort, `fy`=founding year).

| In the original | Current build | Status |
|---|---|---|
| "25 started above it. 30 grew past it. 114 are still under." | `INHERITED` 24, `CROSSED` 31, `NEVER_CROSSED` 114 (sums to 169). The Ways tab reads "All 31 organizations that grew past $10M did it through one of the six mechanisms." | **Confirmed.** Needs 24 / 31 / 114 |
| Rogan as the platform-licensing "exception"; "30 of 31 … one exception" (v7 loop legend: "Grew past $10M without one of the six", "Grew past $10M (30)", "Started above $10M (25)") | Joe Rogan Experience: cohort C2, `M3_new_org_team_and_portfolio`, founded 2009, origin `CROSSED`. No exception category in the legend or the data. Mechanism counts among the 31: 0 / 2 / 10 / 9 / 7 / 3 | **Confirmed** |
| Tab names "1 Who pays / 2 How they got big / 3 When they started" (old kit) | Governance / The 6 ways / History | **Confirmed**. Note the old `nn/` source and the 52 s v8 video still use the old names; the preview file is ahead of both |
| Active tab styling | Active tab is gold (`#FFC627`-family) with black text | **Confirmed** |
| No credit footer | Footer: "Nodes and Networks by Justin Bank for the Knight Center for the Future of News at Arizona State University's Walter Cronkite School of Journalism and Mass Communication" | **Confirmed.** Longer than the end-card line in the brief (it adds "Walter Cronkite School of Journalism and Mass Communication") |
| Org-name annotations on charts ("The exception: Joe Rogan Experience…", "among them AP Wire Service and New York Times") | None on any chart. Names only appear in the hover tooltip. The charts carry only cohort labels (Governance) and mechanism / group labels (6 ways) | **Confirmed** |
| Dashed rings at $3.5M / $10M, zone pills | **None.** The Governance and Ways charts have no rings or zones | **New finding, not on your list** |
| Spiral build, 18-segment mirror, spin | **None.** No intro animation of any kind (no `intro`, `spiral` or `mirror` code in the page) | **New finding.** See STORYBOARD |
| "Turn the lens" wording | The tab-switch is the only "turn"; the lens vocabulary does not appear anywhere in the explorer | **New finding** |
| "Distance from the center now means founding year" and the founding-year radial layout | History is now a bar chart plus left-to-right founding-year dot rows (SVG, 1995 line). No radial layout | **New finding** |
| "Governance determines so much." | Not on the page, not in `copy.md` | **New finding.** The line lives only in the old player |
| "C4 Philanthropic Networks" | "C4 · Philanthropic Mesh Networks" | New finding |
| Footer "169 U.S. journalism organizations · nine governance cohorts" (renders as "Â·" mojibake in the MP4) and URL `journalismatlas.com/research/nodes-and-networks` | Outdated URL and a visible encoding bug. Not to be reproduced | New finding |
| Mark shapes: diamond / square / circle per group | Circle = under $10M, triangle = grew past, square = started above | New finding |
| Same-from-the-data checks that still hold | 169 organizations; 9 cohorts; counts C1 18, C2 26, C3 8, C4 44, C5 14, C6 8, C7 7, C8 27, C9 17; 113 of 169 founded 2008 or later (1 org has no verified year) | Unchanged |
