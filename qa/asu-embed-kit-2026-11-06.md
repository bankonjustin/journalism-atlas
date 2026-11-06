# ASU embed kit: internal notes (Nov 6, 2026)

All heights, the auto-height script, the fixed-height CSS, titles and the "Explore the data" URL live in **`qa/embed-codes-asu.md`** (the Drive `embed-codes.md`). This file keeps only what that file leaves out.

## ASU page, read-only measurements (Chrome, Nov 6)
- Before the update, the ASU iframes had `height` 1471 / 1050 / 600 / 1145 / 600 (timeline, map, defector, threshold, bands) against live content of 1506 / 1061 / 654 / 1148 / 607 at the 700 px column, so every chart was a little cut off.
- ASU iframes: `border:0;display:block;max-width:1200px;width:100%` (map 1400 px). The page has since added `title` attributes. Both "Explore the data" buttons pointed at the explorer with `embed=1` and `tab=ways`.
- The iframe's parent has `max-width:700px`. Column width by window width: 700 px from 992 px up, 552 px at 768 to 991, 476 px at 576 to 767, window minus 64 px below 576. The Defector sits in a collapsed accordion with a column 57 px narrower than the others (below 992 px).
- The page runs 10 inline scripts and has no `nn:resize` listener.
- After the update, live heights matched the branch measurements at the 700, 552, 476 and 436 px columns: timeline 1113 / 1283 / 1216 / 1336, map 845 / 1364 / 1491 / 1507, defector 654 at 700 (810 at 479, 758 at 379), threshold 1148 / 1265, bands 607 / 630. The timeline shrank from 1471 to 1113.

## Findings
- The old timeline measured `scrollHeight`, which never goes below the iframe's own height, so it could grow but not shrink. Fixed: it now measures content height.
- The four figures that load `embed.js` post their height from `requestAnimationFrame`, so an iframe scrolled out of view updates when it scrolls back in. The timeline posts directly.
- 1661 px for Figure 5 was the "Split by cohort" height at 390 px measured Nov 3. Default view is 583 to 859 px.
