# Nodes and Networks: ASU theme, History dial, teaser. Ledger (Oct 30, 2026)

Nothing was committed from the terminal. Justin's GitHub Desktop commit `24bc4a1` ("so many") landed mid-session and captured an early state of Phase 1–2; everything after that is uncommitted. Not deployed.

## Halt conditions
- No data or count changes (N=169 untouched).
- `build.py` ran clean throughout.
- Default theme check (explorer, no params, 1200 and 390 px, reduced motion): In short, Governance, 6 Ways are **pixel-identical** before and after. History differs, by design (new radial view).
- Default theme check (figure pages): theme is gated, no param = no change. Verified `data-nn-theme` is absent without `?theme=asu`/`?embed=1`.

## Files touched
**Shared theme (new)**
- `assets/nn5/nn-theme.js`: switch (`?embed=1` or `?theme=asu`), group colors, Arial, hex remap for generated SVG.
- `assets/nn5/nn-theme.css`: Arial variables, ASU palette (light and dark blocks), maroon interface rules.

**Figures (`embed/fig-0…6`)**
- `preview/nodes-and-networks-edition-e852c5c5/embed/fig-*/index.html` (7): add the two theme tags.
- `assets/nn5/js/figs/kaleido.js`: canvas font and zone/year ring colors read the theme.
- Mirrored outside this repo: `nodes-networks-v5/edition/src/js/figs/kaleido.js` and the head template in `nodes-networks-v5/edition/tools/build_edition.py`, so an edition rebuild keeps the hooks. `nn-theme.*` itself lives only in `assets/nn5/` (a rebuild that wipes that folder would drop it).

**Explorer**
- `nn/src/explorer.tpl.html`, `nn/src/engine.js`, `nn/build.py` (inlines the theme files, so the explorer stays one self-contained file), `nn/content/copy.md` (new strings: `hist.ring_core`, `hist.ring_unverified`, `chapter3.foot_radial`).
- `nn/built/nodes-and-networks/*` refreshed with `build.py --fallback`. The Arial switch the brief wanted is present in built (`NN_FAM` appears 3 times). `index 2.html` / `nodes-networks 2.vtt` duplicates: **listed, not deleted** (the refresh removed them; I restored them from git): `nn/built/nodes-and-networks/index 2.html`, `embed/index 2.html`, `explorer/index 2.html`, `media/nodes-networks 2.vtt`.

**QA and deliverables**
- `qa/theme/`: `swatches.*`, `groupb-*` comparison renders, `figs/*-before-after.png` (7 figures x 1200/390), `figs/heights.json`, `embed_codes.md`, `hist-radial-*.png`, `hist-timeline-1000.png`, `asu-explorer-*.png`.
- `qa/explorer/`: 4 webm videos (radial and timeline x 1200 and 390), Governance → 6 Ways → History → Governance.
- `qa/teaser/capture_teaser.py` + `qa/teaser/out/` (radial) and `out_timeline/`: `teaser.mp4`, `teaser.webm`, `teaser.gif`, `teaser_square.mp4`.
- Tools: Homebrew `ffmpeg` installed.

## Judgment calls
1. **Theme trigger for the figures.** The figure URLs are path-based (`/embed/fig-x/`) with no `?embed=1`, so the figures turn ASU only with `?theme=asu`. `embed_codes.md` therefore uses `?theme=asu&v=asu1`, not just `?v=asu1`. If the live iframes omit `theme=asu`, the figures stay in the default look. Tell Carrie to use the file as written.
2. **Three group colors, not nine.** The charts encode three groups (a, b, c), so the nine-color remap was not applied (it would change what the charts show). Group a Gold `#FFC627`, b Pink `#E74973`, c Gray 4 `#BFBFBF`, neutral `#747474`.
3. **Light-mode figure fills.** Group b is pink in light mode too; light-mode "maroon text" is `#8C1D40`; dark-mode group-b text is pink (the color key survives).
4. **No hairline strokes on the explorer's black stage.** Every fill is at least 4.49:1 on black, so strokes were not needed. Light-page figures: gold gets the `#484848` edge via `--g-gold-edge`; **light-page group c (`#BFBFBF`, 1.84:1 on white) has no stroke yet**. Flagged below.
5. **Text grays, three steps:** `#E8E8E8`, `#D0D0D0`, `#BFBFBF` on dark. Light-page ink-2 and ink-3 both became `#484848` (`#747474` is never text), so those two now match.
6. **Maroon `#8C1D40` for interface only:** selected tab and selected chapter button (white text), section rules (`.chap` top border), focus rings on light pages. On black, rules and focus rings are Gold, never maroon. There are no CTA button fills in the explorer; the "explore" link and the report link are text links.
7. **The explorer had no Governance → 6 Ways tween** (tab switches are instant, a rule from Oct 28). The dial turn exists only in the edition's "Turn the lens" figure. I reused its exact blend (1.5 s + 0.4 s angular stagger, ease-in-out cubic). The turn plays whenever History is involved, and for Governance ↔ 6 Ways only with `?morph=1` (teaser and QA videos). Default Governance ↔ 6 Ways stays instant. Reduced motion: everything instant.
8. **6 Ways is angular** (wedges with start and end angles). Each mark keeps its 6 Ways angle; overlaps are resolved by small angle nudges inside the mark's own wedge, never by changing radius.
9. **Radius = founding year** (oldest at center): core circle before 1970 (r .30), rings at 1995 (data `cut`) and 2008, a ring at 2026, dashed outer ring "Founding year not verified" for missing or unverified years (4 marks). `1970`, `2008`, `2026` are fixed in code (the build warns about a number typed by hand in `chapter3.foot_radial`); only `1995` comes from data.
10. **Dot size:** the explorer has no size encoding (all marks equal). Used revenue band: 0.72 / 1 / 1.38 x. No square-root revenue scale, no new data. Shapes (square, triangle, circle) unchanged.
11. **Gray-out and highlight in History** reuse the 6 Ways logic and list controls. During the turn the gray-out follows each mark's opacity, so nothing pops.
12. **Rings sweep outward** center-first (core, 1995, 2008, 2026, unverified), each about 400 ms, staggered by 100 ms.
13. **Timeline fallback (`?history=timeline`)** runs the same dial turn, then swaps to the existing per-cohort SVG timeline. I did not build dots physically settling into the timeline's positions; it is a swap at the end of the turn. The era bar chart was removed from that timeline too.
14. **Copy.** `chapter3.foot` said the axis runs left to right and unverified marks are "not shown", which is false for the radial view, so the radial view uses new `chapter3.foot_radial`. The old foot still serves the timeline flag.
15. **Teaser.** Frame-exact capture on a virtual clock (3200x1800, 30 fps), so output is deterministic. 1.2 s holds (not 1.5, so the loop stays under 10 s: 9.47 s), the loop ends on the opening Governance frame. `?bare=1` was added to the explorer: shapes and rings only, no chrome, spokes or labels.

## Where the pre/post counts appear
Removed from the History view: the era bar chart ("N of N over $10M" per era) and its legend.
**Still there (not touched, your call):**
- History dek (`chapter3.dek`): "24 of 38 ... 31 of 130".
- History chapter line (`chapter3.sentence`): "24 of 38 founded before 1995 run over $10M".
- In short tab: the History row's chapter line and the small era-bar thumbnail (`eraThumb`).
- Landing/share copy that reuses `chapter3.sentence` (`copy.md` line ~575).
- Per-cohort "x of y over $10M" row labels, only in the `?history=timeline` fallback.

(The brief's "63 / 47" does not match the data: the cut gives 38 before 1995 and 130 since. Check which numbers Andy meant.)

## Contrast check (dark stage unless noted; WCAG ratios)
| Pair | Ratio | Verdict |
|---|---|---|
| Gold `#FFC627` / black | 13.4 | pass |
| Pink `#E74973` (fill and text) / black | 5.6 | pass |
| Group c `#BFBFBF` / black | 11.4 | pass |
| Neutral `#747474` / black (fills and lines only) | 4.49 | fill passes 3:1; **below 4.5 for text, so never used as text** |
| Text `#E8E8E8` / `#D0D0D0` / `#BFBFBF` / black | 17.1 / 13.6 / 11.4 | pass |
| White on maroon `#8C1D40` | 8.9 | pass |
| Maroon `#8C1D40` / black | 2.4 | **fails**; not used on black (Gold used) |
| Grid / rules `#484848` / black | 2.3 | **below 3:1**; decorative lines |
| Light page: ink `#191919`, `#484848` on white | 17.6, 9.2 | pass |
| Light page: maroon text / focus on white | 8.9 | pass |
| Light page: pink fill on white | 3.75 | pass (non-text) |
| Light page: gold fill on white | 1.57 | fails alone; passes with the `#484848` edge (applied) |
| Light page: group c `#BFBFBF` fill on white | 1.84 alone; with the `#484848` edge (9.15) | **passes with the edge (round 2)** |
| Light page: `#747474` fill on white | 4.67 | pass |
| Neutral vs group c on black | 2.5 | distinct (gray-out logic holds) |
| Pink vs gold | 2.4 | distinct by hue, not by lightness |

## Flagged / not done
- The History radial view is dense at the bottom: about 110 marks founded 2008 or later share one wedge and a narrow radius band. Overlaps are reduced but remain. On 390 px it is tighter. The timeline flag is the fallback.
- The `?history=timeline` teaser runs but the SVG timeline is not shown in bare mode (text hidden); verify before using that file. The delivered teaser is the radial version.
- Unused copy strings now warn in the build (`hist.era_title`, `hist.key_started`, `hist.era_aria_full`). Left in place.
- Figure heights in `embed_codes.md` were tested at 390 / 760 / 1200 px in Chromium only. The ASU-confirmed iframe URLs may differ.
- The edition's own `explorer` page under `preview/…edition…/explorer/` was not themed (not requested).
- JS cache: the figure's `kaleido.js` still imports with `?v=a7031425`, so browsers can keep the old file for up to 10 minutes (`_headers`).

## Round 2 (Oct 30, later)
1. **Group c stroke on light pages.** Done in `assets/nn5/nn-theme.css`, not in `figs/*.js` (the diamonds are CSS clip-path shapes, so a JS change would not reach them): a `#484848` edge on the group c diamonds (fig 5 marks and legend, fig 3-style tags) and on group c bars/lines (`cohort-line`, `map-line`, `dock-line`). Light page only; the dark page keeps no edge. Screenshots: `qa/theme/groupc-*.png`, `qa/theme/figs/fig-2-map-*` and `fig-5-bands-split-*` (before/after at 1200 and 390). Mirrored into `nodes-networks-v5/edition/`: `src/theme/nn-theme.{css,js}` plus two lines in `tools/build_edition.py` that write them into `assets/nn5/`. (`nodes-networks-v5` is not a git repo, so there is nothing to commit there.)
2. **Morph is the default under ASU.** `MORPH` is now on when the theme is on (`?theme=asu` or `?embed=1`); `?morph=0` turns it off. The default journalismatlas.com theme still switches Governance ↔ 6 Ways instantly (pixel check below). **Teaser captured with:** `?theme=asu&bare=1&morph=1&tab=governance` (radial History, no `history=timeline`). Checked frame by frame: the Governance → 6 Ways → History → Governance loop has no cut; motion starts at 1.2 s, 4.35 s and 7.5 s. Specs and exports unchanged (9.47 s, 30 fps; `qa/teaser/out/`). The `out_timeline/` files are from round 1 and are **not** re-recorded; ignore them.
3. **History rings sized by count.** Each ring's radius is set so every organization gets about equal area: pre-1970 core 19, 1970–1995 16, 1995–2008 17, 2008–2026 113, unverified 4 (dashed ring). Angles are unchanged. The 113 marks from 2008 on now fill the outer band instead of a thin rim. Year position inside each era is still linear in the year. Ring labels are staggered in angle so they do not overlap. The core label count is 19, not the 21 I wrote in round 1 (21 included unverified marks). Screenshots: `qa/theme/hist-radial-1200.png`, `hist-radial-390.png`; video: `qa/explorer/gov-ways-history-gov_radial_{1200,390}.webm` (recorded without `morph=1`, to prove the ASU default). `?history=timeline` untouched. Dek counts ("24 of 38 … 31 of 130") kept.

**Default-theme pixel check (after round 2):** In short, Governance and 6 Ways at 1200 and 390 px identical to before; History differs by design.
