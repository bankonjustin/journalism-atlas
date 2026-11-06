# Nodes and Networks: report chart embeds (ASU look)

> **Superseded Nov 6, 2026.** Heights, titles, the auto-height script and the fixed-height CSS now live only in `qa/embed-codes-asu.md` (the Drive copy). The snippet heights in this file were updated to match; the tables and "height measured" lines below are historic and not maintained.


Written for the ASU web designer. Seven charts, each at a permanent address that will not be renamed; the content behind it may be updated later (numbers are v22.5).

## Read this first

- **ASU look is built in.** Arial and the ASU gold, no `?theme=` parameter needed. Use the URLs exactly as written.
- **No site chrome.** Each page is the chart only, with the credit line the explorer uses.
- **Not indexed, restricted framing.** `noindex, nofollow` comes from `/preview/nn-launch-kit/*` in `_headers`; the `frame-ancestors` rule allows `asu.edu`, `*.asu.edu` (so `cronkite.asu.edu`), `journalismatlas.com` and the page itself. Other sites cannot frame these. **These are preview addresses and take effect only after the push.**
- **Height.** The `height` in each snippet is the desktop (1200 px wide) measurement plus 16 px. Phone height is the measurement at 390 px wide; if your layout is narrow, use it with a media query. Every chart also posts its height to the parent page (`postMessage`, type `nn:resize`) if you want the iframe to resize itself:

```html
<script>
addEventListener("message",function(e){
  if(!e.data||e.data.type!=="nn:resize")return;
  document.querySelectorAll("iframe[data-nn]").forEach(function(f){
    if(f.contentWindow===e.source)f.style.height=e.data.height+"px";
  });
});
</script>
```

  Add `data-nn` to the iframe if you use it.
- **Charts that change height when used.** Figure 5 grows when "Split by cohort" is clicked (584 to 1046 px on desktop, 739 to 1661 px on phone). Its snippet is already set to the taller, split-view height, so the default view has white space below it. Use the resize script above if that matters. The kaleidoscope changes by under 40 px.

## Charts

| Figure | Title | Where it goes in the report | URL | Phone height |
|---|---|---|---|---|
| Figure 0 | Scale of the field: one square vs. $100M | Right after the paper's sentence "Those two numbers sitting next to each other…" | `https://journalismatlas.com/preview/nn-launch-kit/figures/scale/` | 814 px |
| Figure 1 | Funding and organization timeline, 2018–2026 | Section on funding shocks | `https://journalismatlas.com/preview/nn-launch-kit/figures/timeline/` | 1842 px |
| Figure 2 | The nine cohorts | Where the nine cohorts are introduced | `https://journalismatlas.com/preview/nn-launch-kit/figures/map/` | 1201 px |
| Figure 3 | Defector revenue, Years 1–5 | Defector case study | `https://journalismatlas.com/preview/nn-launch-kit/figures/defector/` | 748 px |
| Figure 4 | Share of revenue from grants and donations, nonprofits with $3.5M–$10M in revenue | Nonprofit / threshold section | `https://journalismatlas.com/preview/nn-launch-kit/figures/threshold/` | 1362 px |
| Figure 5 | Revenue band distribution by cohort (n=169) | Bands / cohorts section | `https://journalismatlas.com/preview/nn-launch-kit/figures/bands/` | 1661 px |
| Explorer-style figure | Turn the lens: 169 organizations, five ways to sort them | Optional: where the report points to the explorer | `https://journalismatlas.com/preview/nn-launch-kit/figures/kaleidoscope/` | 1485 px |

"Where it goes" is a suggestion from the figure content; confirm placement with Justin.

### Figure 0: Scale of the field: one square vs. $100M

- **Where:** Right after the paper's sentence "Those two numbers sitting next to each other…"
- **URL:** `https://journalismatlas.com/preview/nn-launch-kit/figures/scale/`
- **Desktop height measured:** 1063 px (snippet uses 1079). **Phone (390 px) height:** 814 px.
- **Alt text:** One $8,800 square beside a field of squares drawn at $100 million, the low end of the reported price for OpenAI's TBPN purchase.

```html
<iframe src="https://journalismatlas.com/preview/nn-launch-kit/figures/scale/"
  title="Scale of the field: one square vs. $100M"
  width="100%" height="1079" loading="lazy" scrolling="no"
  style="border:0;display:block;width:100%;max-width:1200px"></iframe>
```

### Figure 1: Funding and organization timeline, 2018–2026

- **Where:** Section on funding shocks
- **URL:** `https://journalismatlas.com/preview/nn-launch-kit/figures/timeline/`
- **Desktop height measured:** 1455 to 1465 px at 720 px and wider (snippet uses 1600). The page height runs from about 1460 to 1600 px at column widths of 600 px and up; it rises to about 1730 px at 540 px and 1770 px at 521 px, and below 521 px the page switches to the phone list. **Phone (390 px) height:** 1842 px. Opening the "Data table" adds about 460 px on desktop and 733 px on phone; use the resize script above if that matters.
- **Alt text:** Timeline of 15 dated events in four lanes of pressure on American journalism, 2018 to 2026: platform withdrawal, government defunding, ownership retrenchment and nonprofit failure.

```html
<iframe src="https://journalismatlas.com/preview/nn-launch-kit/figures/timeline/"
  title="Funding and organization timeline, 2018–2026"
  width="100%" height="1129" loading="lazy" scrolling="no"
  style="border:0;display:block;width:100%;max-width:1200px"></iframe>
```

### Figure 2: The nine cohorts

- **Where:** Where the nine cohorts are introduced
- **URL:** `https://journalismatlas.com/preview/nn-launch-kit/figures/map/`
- **Desktop height measured:** 992 px (snippet uses 1008). **Phone (390 px) height:** 1201 px. Opening the C3 card adds about 24 px on desktop.
- **Alt text:** Nine governance cohorts drawn as stations on three lines, from Legacy Publishers (17 organizations) to B2B/Professional Services (17); 169 organizations in all.

```html
<iframe src="https://journalismatlas.com/preview/nn-launch-kit/figures/map/"
  title="The nine cohorts, in three groups"
  width="100%" height="861" loading="lazy" scrolling="no"
  style="border:0;display:block;width:100%;max-width:1200px"></iframe>
```

### Figure 3: Defector revenue, Years 1–5

- **Where:** Defector case study
- **URL:** `https://journalismatlas.com/preview/nn-launch-kit/figures/defector/`
- **Desktop height measured:** 791 px (snippet uses 807). **Phone (390 px) height:** 748 px.
- **Alt text:** Defector's revenue rose from $3.2 million in 2020–21 to $4.65 million in 2024–25; subscriptions reached $3.8 million in 2023–24 and held there.

```html
<iframe src="https://journalismatlas.com/preview/nn-launch-kit/figures/defector/"
  title="Defector revenue, Years 1–5"
  width="100%" height="670" loading="lazy" scrolling="no"
  style="border:0;display:block;width:100%;max-width:1200px"></iframe>
```

### Figure 4: Share of revenue from grants and donations, nonprofits with $3.5M–$10M in revenue

- **Where:** Nonprofit / threshold section
- **URL:** `https://journalismatlas.com/preview/nn-launch-kit/figures/threshold/`
- **Desktop height measured:** 1129 px (snippet uses 1145). **Phone (390 px) height:** 1362 px.
- **Alt text:** Of 17 nonprofits with $3.5 million to $10 million in revenue, 15 get 80 percent or more of their revenue from grants or donations; Colorado Sun is at 49 percent and LION Publishers at 72 percent.

```html
<iframe src="https://journalismatlas.com/preview/nn-launch-kit/figures/threshold/"
  title="Share of revenue from grants and donations, nonprofit newsrooms with $3.5M–$10M in revenue"
  width="100%" height="1164" loading="lazy" scrolling="no"
  style="border:0;display:block;width:100%;max-width:1200px"></iframe>
```

### Figure 5: Revenue band distribution by cohort (n=169)

- **Where:** Bands / cohorts section
- **URL:** `https://journalismatlas.com/preview/nn-launch-kit/figures/bands/`
- **Desktop height measured:** 1046 px (snippet uses 1062). **Phone (390 px) height:** 1661 px.
- **Alt text:** 80 of 169 organizations are below $3.5 million, 34 are in the middle and 55 are above $10 million; all 17 legacy publishers are above $10 million and no worker co-op or civic organization is.

```html
<iframe src="https://journalismatlas.com/preview/nn-launch-kit/figures/bands/"
  title="Revenue band distribution by cohort (n=169)"
  width="100%" height="623" loading="lazy" scrolling="no"
  style="border:0;display:block;width:100%;max-width:1200px"></iframe>
```

### Explorer-style figure: Turn the lens: 169 organizations, five ways to sort them

- **Where:** Optional: where the report points to the explorer
- **URL:** `https://journalismatlas.com/preview/nn-launch-kit/figures/kaleidoscope/`
- **Desktop height measured:** 1681 px (snippet uses 1697). **Phone (390 px) height:** 1485 px.
- **Alt text:** 169 organizations drawn as marks around a center, re-sorted by five lenses: the field, governance, who got past $10M, six ways past $10M, and when they started.

```html
<iframe src="https://journalismatlas.com/preview/nn-launch-kit/figures/kaleidoscope/"
  title="Turn the lens: 169 organizations, five ways to sort them"
  width="100%" height="1697" loading="lazy" scrolling="no"
  style="border:0;display:block;width:100%;max-width:1200px"></iframe>
```

## Teaser video for the explorer button

Recorded from the committed `preview/nn-launch-kit/explorer/index.html` (clean against HEAD; v22.5 data: C1 17, C4 45, "Under $10M in latest year" label visible). It is the 6 ways to History turn and back, 10.47 s, 30 fps, 1200 x 960 (the explorer's chart area only, no page chrome). The last frame equals the first, so it loops with no jump.

| File | Size | Notes |
|---|---|---|
| `preview/nn-launch-kit/media/teaser.mp4` | 0.83 MB | 1200 x 960, H.264 High, yuv420p, no audio track, moov atom first (faststart) |
| `preview/nn-launch-kit/media/teaser@2x.mp4` | 1.49 MB | 2400 x 1920, same encoding |
| `preview/nn-launch-kit/media/teaser-poster.jpg` | 0.09 MB | first frame, 1200 x 960 |

URLs: `https://journalismatlas.com/preview/nn-launch-kit/media/teaser.mp4`, `.../teaser@2x.mp4`, `.../teaser-poster.jpg`. Same noindex as the rest of the kit; the files are public once pushed (`build-dist.sh` now copies them).

```html
<video autoplay muted loop playsinline preload="metadata" width="1200" height="960"
  style="width:100%;height:auto;display:block"
  poster="https://journalismatlas.com/preview/nn-launch-kit/media/teaser-poster.jpg">
  <source src="https://journalismatlas.com/preview/nn-launch-kit/media/teaser@2x.mp4" type="video/mp4" media="(min-resolution: 2dppx)">
  <source src="https://journalismatlas.com/preview/nn-launch-kit/media/teaser.mp4" type="video/mp4">
</video>
```

Add `aria-hidden="true"` if the video is purely decorative next to the button; add a `prefers-reduced-motion` rule (pause or show only the poster) if ASU's pages do that elsewhere.

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
