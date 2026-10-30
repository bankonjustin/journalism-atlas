# STORYBOARD.md — N&N launch video recut (30 s)

Status: **awaiting approval. Nothing recorded.** Stills below are 1080×1080 frames made from real screenshots of the current explorer (a scratch copy of `preview/nn-launch-kit/explorer/index.html`, md5 `0133931bdde5cfb740b5879b0f30402f` at HEAD dccd9eb (re-shot Oct 29 after Part A), embed mode, 2x). The explorer is still being edited, so every still and number gets regenerated after "Part A is in".

All numbers are derived from the explorer's embedded `nn-data` JSON, never typed:
`A` = nodes with origin `INHERITED` = **24**; `G` = `CROSSED` = **31**; `U` = `NEVER_CROSSED` = **114**; `T` = node count = **169**; `F08` = founding year ≥ 2008 = **113**; cohort counts from `c` (C1 18, C2 26, C3 8, C4 44, C5 14, C6 8, C7 7, C8 27, C9 17).

## What the current explorer can and can't do (read this first)

- **The real motion available is the 1.5 s tab morph.** Marks fly from one radial layout to the other, staggered by angle. It runs between Governance and The 6 ways in both directions. It is not a spin around the center.
- **The History tab is an SVG chart.** There is no morph into or out of it, so it enters with a cut. I propose a 0.4 s dissolve in post, which is not explorer motion.
- **The explorer has no intro.** The spiral build, the spin and the mirror are gone. They were drawn by the old player, not by the explorer, and nothing in the explorer can reproduce them. The rings and zones are gone too.
- Because the brief says real motion only, the spiral and mirror beats are cut and replaced (see below). A faked version would no longer be the product.

## The beats

| # | Time | Original beat | What's recorded (real explorer) | Caption: old → new (derivation) | Still |
|---|---|---|---|---|---|
| 1 | 0.0–2.5 | Spiral build (0–1.4 s) | **Substitute.** Open on The 6 ways at rest: the radial wedge view, which makes a strong first frame and thumbnail | "169 organizations." → **"169 organizations."** (`T`, unchanged) | `01-open-ways.png` |
| 2 | 2.5–4.5 | Spin and mirror, then "Turn the lens" (1.4–7.7 s) | **Substitute.** Click Governance; the marks fly to the nine cohort wedges and the gold tab moves. This is the closest real "turn" | "From far away, the field looks like the trends you already know." / "Turn the lens to governance." → **"Now sort by governance."** (drops "lens", jargon you already edited out of the other explorer) | `02-morph-to-governance.png`, `03-governance-settled.png` |
| 3 | 4.5–10.5 | Cohort sweep (8.9–12.1 s) | Cursor moves down the cohort list, C1 to C9, one per beat. Each wedge lights, the rest dim. Real hover state. C3, C6, C7 (the three small cohorts) hold 0.9 s, the others 0.5 s. Longer than the original (6.0 s vs 3.2 s) because a real hover needs time to read | "C4 Philanthropic Networks, 44 organizations" → **"C4 · Philanthropic Mesh Networks / 44 organizations"** (`meta.cohorts` name, `c` count). Name changed in the data | `04-cohort-C4.png`, `05-cohort-C7.png` |
| 4 | 10.5–12.5 | "Governance determines so much." (12.1–13.6 s) | Cursor off, all nine wedges lit, hold | "Governance determines so much." → **"Governance determines so much."** Decision 3 below: this line is not anywhere on the current explorer | `06-governance-hold.png` |
| 5 | 12.5–18.5 | Three wedges, "How they got past $10M" (13.6–19.4 s) | Click The 6 ways; real 1.5 s morph (stills at 0.65 s mid-flight and settled), then hold on the settled chart | "How they got past $10M." (kept) + "25 started above it. 30 grew past it. 114 are still under." → "**{A} started above it. {G} grew past it. {U} are still under.**" = **24 started above it. 31 grew past it. 114 are still under.** Second line at 16.0 s: **"All 31 did it one of six ways."** (`G`; the explorer's own sentence has no exception) | `07-morph-to-ways.png`, `08-ways-settled.png` |
| 6 | 18.5–21.5 | **New** hover beat (the tap in 9:16) | On The 6 ways, cursor drifts to the **Politico Pro** mark (position from `NNX.pt('Politico Pro')`). The tooltip pops: name, C9 cohort, "Mechanism: B2B", over $10M, founded 2011. Tooltip text is the explorer's own | **"Hover any mark."** / "Meet the organization behind it." (new; the explorer's hint line reads "Hover over any mark to see the organization behind it.") | `09-hover-politico-pro.png` |
| 7 | 21.5–26.0 | Founding-year beat (19.4–25.2 s) | Click History; 0.4 s dissolve in; slow scroll or hold on the era bars (63 / 47 / 37 / 15 percent) and the founding-year rows | "When they started." (kept) + "Distance from the center now means founding year. 113 of 169 started in 2008 or later." → **"When they started."** / "**{F08} of {T} started in 2008 or later.**" = **113 of 169 started in 2008 or later.** Radial-distance sentence dropped; it is false now | `10-history.png` |
| 8 | 26.0–30.0 | "Turn the lens yourself." + URL | **End card** on black, no URL. Placeholder line only in the social cuts | "Turn the lens yourself." + footer URL → **"Explore all {T} organizations"** = **"Explore all 169 organizations"** + "Nodes and Networks by Justin Bank for the Knight Center for the Future of News at Arizona State University." | `11-end-card.png` |

Contact sheet note: in the stills the caption area is sized for the 1:1; the real render will enlarge type so it passes the 300 px check. The hover still's tooltip is small here because the whole chart is shown; the recording will zoom in on that region.

## What I cut and what I added

- **Cut (11.0 s of original):** spiral build 1.4 s; spin and mirror 3.2 s; bare-field pause 0.7 s; rings and zones 1.2 s; "Turn the lens yourself" return to governance 4.8 s (folded into the end card). The rest is the stretch of the original fly-to-wedges (2.2 s), now 1.5 s.
- **Added:** the cohort sweep is longer (+2.8 s) and there's a new hover beat (3.0 s).
- Runs 30.0 s total, the length of the original.

## Decisions I need from you

1. **Original = the 30 s Oct 24 reel**, not the 15 s Oct 23 turn (see ORIGINAL.md §2). Confirm.
2. **No intro in the explorer.** The proposal opens on The 6 ways and uses the morph as the "turn". Alternative: an illustrative spiral/mirror opening drawn outside the explorer. That breaks "real explorer" and I recommend against it.
3. **"Governance determines so much."** appears nowhere in the explorer or `copy.md`. Keep it as the thesis line (my pick) or drop it?
4. **Credit line:** the brief's end-card text omits "Walter Cronkite School of Journalism and Mass Communication", which the explorer's footer carries. I used the brief's line as written. Confirm.
5. **Hover target:** swapped to Politico Pro by the explorer session (grew past $10M, tooltip tag is unambiguous). Your call to confirm; Rogan and NYT were the alternatives.
6. **"How they got past $10M"** is kept from the original; the tab is now "The 6 ways". Rename the caption "The six ways past $10M"?
7. **Encoder and method (for Phase 3).** This Mac has no ffmpeg. The only ffmpeg here is Playwright's build, which cannot read or write H.264. Plan: drive the real explorer in Chromium at 2x, freeze `performance.now` / `requestAnimationFrame` and step the clock, so each frame is a real explorer frame with no dropped frames. Then encode with the repo's `encode.swift` (AVFoundation H.264). AVFoundation can add a silent AAC track and set faststart, but High profile and the 15 MB cap need checking on the first test render. If you'd rather install ffmpeg (Homebrew), say so; that's a system change I won't make unasked.
8. **Explorer in flux.** Re-shoot every still and re-derive every number at "Part A is in". If tab names, counts or the tooltip change, the beat table updates with them.

## Not reproduced from the original

The "Â·" encoding bug in the old footer, the `journalismatlas.com/research/nodes-and-networks` URL, the "KNIGHT CENTER · JOURNALISM ATLAS" header strip.
