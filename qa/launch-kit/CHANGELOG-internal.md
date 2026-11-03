# NN launch kit: internal changelog (not for the ASU/Drive handoff)

Internal fix log split out of `embed-codes.md` on Nov 3, 2026. The clean designer version is in the Drive handoff folder.

## Nov 3, 2026 cleanup run (Cowork)

- The launch kit lives in `journalism-atlas` (the site repo), not `journalism-atlas-private`. Brief v5 named the wrong repo, so the "stranded figure fixes" it was hunting for did not exist: all v22.5 fixes were already committed and pushed.
- Deploy: Cloudflare Pages builds `main` of `bankonjustin/journalism-atlas` with `build-dist.sh` into `dist/`. The script copies `preview/**/index.html` (figures, explorer, embed-test), `preview/nn-launch-kit/media/teaser*` and the kaleidoscope `still.png`. `_headers` sets noindex on `/preview/nn-launch-kit/*` and `frame-ancestors 'self' https://asu.edu https://*.asu.edu https://journalismatlas.com` on `figures/*` and `explorer/*`.
- Earlier "curl returns nothing" was the sandbox proxy / Cloudflare blocking non-browser clients. From a real browser all 12 URLs (7 figures, explorer, embed-test, 3 media files) returned 200 with noindex and the correct frame-ancestors, and every v22.5 must/must-not check passed (Legacy 17, C4 45, MuckRock 90, Cityside 86.4, "nonprofits", "all 17", new cohort names, "in latest year", no CNN/Gannett old names).
- Committed: `b917faa` ASU maroon #8C1D40 for group b (theme cache key asu2), applied from a GitHub Desktop stash per Justin. Note: maroon on the black stage is about 2.4:1 contrast; fine as fill, weak as text. The explorer has its own palette and was not changed (another session owns it), so it may still show the pink.
- Committed: `9393cac` 7-figure embed test page at `preview/nn-launch-kit/embed-test/figures/`.
- Deleted: an Oct 11 GitHub Desktop stash of `dist/` build output on the `private` branch.
- PNGs for Drive `charts/` re-rendered at 1200 px from the committed files.
- Edition embed pages (`preview/nodes-and-networks-edition-e852c5c5/embed/*`) still reference `nn-theme.*?v=asu1`; out of scope.

## Test results

Playwright (Chromium), each page inside an iframe at 1200 and 390 px wide: no console errors, no page errors, no failed requests; `data-nn-theme="asu"` and Arial applied on all seven; the height the page posted equals the measured height. The test used a local server, so the `_headers` rules were not exercised: confirm framing from `cronkite.asu.edu` after the push.

## Old values fixed in the seven charts (file | old | new)

Source: `qa/numbers-v22.5.md`. The new pages are copies of the edition `embed/fig-*` pages; the edition originals were not touched. `169` was left alone.

| File (under `preview/nn-launch-kit/figures/`) | Old | New |
|---|---|---|
| `map/index.html` (text, aria-label, chip, table, JSON) | Legacy Publishers 18 organizations / `C1, n=18` / `n=18` | 17 |
| `map/index.html` (station, table, JSON) | Philanthropic Networks `C4, n=44` / 44 | 45 |
| `bands/index.html` (text, table, JSON) | C1: 18, 18 (100%) above $10M, "all 18 legacy publishers" | 17, 17 (100%), "all 17" |
| `bands/index.html` (table, JSON) | C4: 44; 21 (48%) / 13 (30%) / 10 (23%) | 45; 21 (47%) / 13 (29%) / 11 (24%) |
| `bands/index.html` (pooled "above $10M" dots) | 18 C1 dots, 10 C4 dots | 17 C1, 11 C4 (the Banner dot is now C4 pink) |
| `kaleidoscope/index.html` (embedded `nodes169` JSON) | C1 18, C4 44; Banner in C1 (gold); `CNN (Warner Bros. Discovery)`; `Gannett Co. Inc. (GCI)`; Puck `ACQUIRED` | The whole block is the v22.5 `nn/data/nodes169.json` (read only): C1 17, C4 45, Banner in C4, `CNN (Skydance)`, `USA TODAY Co. (formerly Gannett)`, Puck `DEAL_ANNOUNCED` |
| `kaleidoscope/index.html` (text) | "Legacy Publishers: 18 of 18 over $10M"; cohort list C1 18, C4 44 | 17 of 17; C1 17, C4 45 |
| `kaleidoscope/index.html` (table) | Banner row "C1 Legacy Publishers"; CNN and Gannett names; Puck note "acquired" | C4 Philanthropic Networks; new names; "deal announced" |

The band split (47.3/20.1/32.5) and Cramér's V do not appear in any of the seven charts. Fig 5's "80 (47%) / 34 (20%) / 55 (33%)" is still correct rounded.

## Round 2 fixes (threshold, kaleidoscope label, still)

| File | Old | New |
|---|---|---|
| `threshold/index.html` data and table | MuckRock 87.5 (2024) shown as 88%; Cityside 82.5 (2024) shown as 83% | MuckRock 90.0 (2025) → 90%; Cityside 86.4 (2025) → 86% (from `Grant_Dependency_Pct` and `990_Year` in v22.5) |
| `threshold/index.html` order | MuckRock and Cityside sorted at 88 and 83 | Re-sorted by value: CT Mirror 90.0, MuckRock 90.0 (tie, kept in the old order), IndiJ 87.9, City Bureau 87.6, Cityside 86.4. Still 15 of 17 above 80%; Colorado Sun 49, LION 72 |
| `threshold/index.html` wording (title, `<title>`, og/twitter titles, caption, alt) | "nonprofit newsrooms" | "nonprofits" (5 places) |
| `kaleidoscope/index.html` embedded data | `nodes169` re-serialized by me | The exact bytes of `nn/data/nodes169.json` (md5 `d42d0076d0454caf561ce482b28dd44b`, same for the file and the embedded block) |
| `kaleidoscope/index.html` BELOW label | `Under $10M`, empty `sub` | A small inline script right after the data block sets `sub` to "in latest year" (and the list label to "Under $10M in latest year") when the page loads, so the data block itself stays byte-identical. The legend now reads "Under $10M in latest year 114" |
| `kaleidoscope/still.png` | Old default-theme image, Banner in C1 sector | New ASU-look image of the default lens (Governance), 1204 x 1350, same size as before; Banner at angle 1.53 rad, inside the C4 sector (0.54 to 1.94) |

All other 16 threshold rows matched v22.5 exactly (value and filing year).

## Cohort names (round 3)

Rule: the paper's own short names (Section II three-group list), which also match the explorer's data block. The old names came from the edition figure pages (`map`, `bands`) and from `nn/data/nodes169.json` / `qa/numbers-v22.5.md` (`kaleidoscope`), none of which was checked against the paper.

| File (under `figures/`) | Old name | New name | Where the old name came from |
|---|---|---|---|
| `map`, `bands`, `kaleidoscope` | Philanthropic Networks | Philanthropic Mesh Networks | edition `fig-2-map`, `fig-5-bands`; `nodes169.json` |
| same | Public Media | Public Media Networks | same |
| same | Worker Co-ops | Worker-Owned Co-ops | same |
| same | Civic & Community | Emerging Civic Actors | same |
| same | B2B & Professional (and "B2B and Professional" in the map's alt text) | B2B/Professional Services | same |

C1 Legacy Publishers, C2 Creator Brands, C3 Barbell Hybrids and C6 Collaboration Layers already matched. `map` and `bands`: the names are changed in the labels, aria-labels, table cells and JSON. `kaleidoscope`: the `nodes169` block is untouched (md5 `d42d0076d0454caf561ce482b28dd44b`); the names are overridden when the page loads, and the legend, table and intro text are edited directly. `bands` still has the group legend "Philanthropic, Public Media, Collaboration" (a group label, not a cohort name).

Heights did not change: map 1046 / 1256 (desktop / phone; was 1240 before the label fix), bands 584 (1046 split) / 739 (1661 split), kaleidoscope 1681 / 1485. No console errors at 1200 or 390. At 390 px the map's station labels for C4, C5, C7, C8 and C9 wrap to two lines and nothing overflows the page, but labels in the left column are clipped by the black line (see below).

## Not verified or left as is

- **"in latest year" does not show on the chart wedge.** On the 6 ways lens the shared `kaleido.js` draws a wedge's second line only if it fits; on the left edge the label wraps to "Under / $10M" and the second line is dropped. The old edition page does exactly the same (compared side by side). It shows in the legend list. Showing it on the wedge needs a change in the shared `assets/nn5/js/figs/kaleido.js` (which the edition pages also use); not made.
- **St. Louis Public Radio is in v22.5 as an in-band row with a grant share (78.4%) but no 990 year, so it is not one of the 17 in the threshold chart.** Left out as before; say if the paper's 17 should include it.
- `timeline`: events say "completes its merger with Gannett" (Nov 2019). Historical; left as is.
- **Map at 390 px (fixed):** the left-column labels were clipped by the black trunk (also on the original page). The map page now adds 24 px of left padding to each line at widths up to 640 px (a `<style>` in `figures/map/index.html` only; the shared CSS is untouched). No label crosses the trunk at 390, 320, 640 or 1200 px; names are not shortened. Phone height 1240 → 1256 px.
- Kaleidoscope: the second name line is dropped on wedges without room (C7 shows only "C7"), as before.
- Kaleidoscope marks come from `nn/data/nodes169.json`, so they sit differently from the old edition version. Not pixel-compared against the explorer.

## Other places that still show OLD values (listed, not fixed)

| Asset | Where | Old value |
|---|---|---|
| Edition page `preview/nodes-and-networks-edition-e852c5c5/index.html` | L66 (and fig-2/fig-5 content inside it) | "Legacy Publishers (18 organizations)", `C1, n=18`; L48 Gannett merger (historical) |
| Share page `preview/nodes-and-networks-f348eb08/index.html` | L168, L170 | Gannett (historical event); other C1/C4 counts likely (not opened in full) |
| Edition `embed/fig-2-map`, `fig-5-bands`, `fig-6-kaleidoscope` | same as the table above | the original pages still carry the old numbers |
| Launch captions `nn/media/launch/nn-launch-{16x9,9x16,1x1}-turn.srt` and the `nn/_out` copies | cue 4, 8.5 to 11.9 s | **Changed to "17 of 17 legacy publishers top $10 million."** (six files). Both folders are gitignored, so these edits will not appear in a commit |
| Launch videos `nn/media/launch/nn-launch-{16x9,9x16,1x1}-turn.mp4` (38 s) | 8 to 12 s, Governance view | Frames checked. The C1 wedge shows 18 marks (14 squares, 4 triangles; counted by eye on the 16x9 frame), so the Banner is still drawn in C1. The burned-in headline reads "18 of 18 legacy publishers top $10 million." (the .srt fix does not change it if it is burned in). Cohort labels are the old names ("Philanthropic Mesh Networks", "Emerging Civic Actors", "B2B/Professional Services", "Public Media Networks", "Worker-Owned Co-ops") and the pink is the old color. RE-RECORD (or re-cut) 8 to 12 s of all three; the rest of each video was not checked |
| Launch poster PNGs, GIFs (`nn-launch-turn-30-grew-720.gif`, `nn-launch-turn-cohorts-720.gif`) | cohort and governance frames | Not checked; the cohort GIF almost certainly shows the Banner in C1 |
| Explorer builds `preview/nn-launch-kit-staging/explorer/index.html`, `nn/built/nodes-and-networks/*`, `nn/_out/...`, `nn/src/explorer.tpl.html` | 6, 3, 3 and 1 pattern hits | Not opened (other session owns the explorer and `copy.md`); `nn/built` and `nn/_out` are stale until `build.py` runs after the push |
| `preview/nn-launch-kit/COPY_EXPORT.md` | L19, L52, L53, L63, L86; L74 | "Under $10M" without "in latest year" on several lines; the History line "63% 24 of 38; 47% 8 of 17; …" is the old era chart text |
| `preview/nn-launch-kit/EMBED.md` | 2 pattern hits (likely `169`) | Not opened in detail |
| Social set `nn/media/social-r1/` (`manifest.*`, `qa/*.json`, `LEDGER.md`, ...) | many | Old cohort counts and names; the posters and clips need regenerating |
| Teaser `qa/teaser/out*/teaser.{mp4,gif,webm}` | History frames | Shows the old explorer; the new teaser is waiting on the explorer commit |
| Release zip `/Users/bankids/Documents/GitHub/paper-one-band-dataset/nodes_networks_release_v22.zip` (T3-17) | `release_v22/nodes_networks_dataset_v22.csv`, plus `figures/` | Older export (md5 `cf787f9d…`, 31 blank `revenue_year`); its figures show 47.1/20.0/32.9 and V 0.503/0.384. Replace with a v22.5 export and v22.5 figures |
| Paper repo (`paper-one-band-dataset`) | `dataset/CHECKSUMS.md5`, `nodes_and_networks_dataset_v22.csv` | Still v22 (md5 `8db4a0ff…`) |

No other page was found saying "169" next to the old split or V. The old 47.1/20.0/32.9 and 0.503/0.384 appear only in the paper repo's notes and the release zip, not in `preview/`, `nn/` or `qa/teaser/`, the only website folders I scanned. The homepage `index.html` and the other site pages were not scanned.

