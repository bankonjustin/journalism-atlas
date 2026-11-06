# Nodes and Networks: report chart embeds (ASU look)

Updated Nov 6, 2026. Heights below were measured on the charts and confirmed on the live cronkite.asu.edu page at its 700, 552, 476 and 436 px columns after the update went live. Test page: https://journalismatlas.com/preview/nn-launch-kit/embed-test/figures/

This is for the ASU web designer. There are seven charts, and each one has a permanent address that will not be renamed. The content behind an address may be updated later. The numbers are v22.5.

## Read this first

- **The ASU look is built in.** The charts use Arial with ASU gold and maroon, and they need no `?theme=` parameter. They always use the light look. Use the URLs exactly as written.
- **No site chrome.** Each page shows the chart only, with the same credit line the explorer uses.
- **Not indexed, restricted framing.** The pages are served with `noindex, nofollow`. Framing is allowed from `asu.edu`, `*.asu.edu` (so `cronkite.asu.edu` works) and `journalismatlas.com`; other sites cannot frame these pages.
- **Two ways to set the height.** Option A (a short script) is recommended: it keeps every chart exactly the right height at every width, including when a reader opens a data table. Option B (fixed heights in CSS) works if the page cannot take a script.
- **Titles.** Every snippet below has a `title` for screen readers. Please keep them.

## Option A: auto-height script (recommended)

Paste this once on the page, after the iframes. It listens only to messages from journalismatlas.com, only from the iframe that sent the message, and it changes only that iframe's height. If several of our iframes are on the page, it handles each one separately. No `data-nn` attribute is needed.

```html
<script>
(function(){var O="https://journalismatlas.com";
addEventListener("message",function(e){
  if(e.origin!==O||!e.data||e.data.type!=="nn:resize")return;
  var h=Number(e.data.height);if(!(h>0&&h<6000))return;
  document.querySelectorAll('iframe[src^="'+O+'/preview/nn-launch-kit/figures/"]').forEach(function(f){
    if(f.contentWindow===e.source)f.style.height=Math.ceil(h)+"px";
  });
});})();
</script>
```

Notes:
- We tested this script on the live cronkite.asu.edu page. Every chart resized to its content.
- Charts that are scrolled out of view update when they scroll back into view. Browsers pause off-screen frames.
- The `height` in each snippet is only the starting height before the script runs: the desktop height for a 700 px column.

## Option B: fixed heights (CSS)

Use this if the page cannot run the script. The classes are already on the snippets below (`nn-fig-timeline` and so on). Paste the CSS once into the page's custom CSS. The CSS overrides the `height` attribute.

The heights are for the chart with any data table closed, plus 16 px. The breakpoints are the ones on cronkite.asu.edu: the content column is about 700 px wide from 992 px up, 552 px from 768 px, 476 px from 576 px, and the window width minus 64 px below that (the Defector chart sits in an accordion, so its column is narrower).

```css
.nn-fig-timeline{height:1910px}
.nn-fig-map{height:1952px}
.nn-fig-defector{height:884px}
.nn-fig-threshold{height:1652px}
.nn-fig-bands{height:1042px}
@media (min-width:390px){
  .nn-fig-timeline{height:1610px} .nn-fig-map{height:1744px} .nn-fig-defector{height:848px} .nn-fig-threshold{height:1440px} .nn-fig-bands{height:836px}
}
@media (min-width:576px){
  .nn-fig-timeline{height:1232px} .nn-fig-map{height:1507px} .nn-fig-defector{height:769px} .nn-fig-threshold{height:1316px} .nn-fig-bands{height:705px}
}
@media (min-width:768px){
  .nn-fig-timeline{height:1299px} .nn-fig-map{height:1380px} .nn-fig-defector{height:826px} .nn-fig-threshold{height:1281px} .nn-fig-bands{height:646px}
}
@media (min-width:992px){
  .nn-fig-timeline{height:1129px} .nn-fig-map{height:861px} .nn-fig-defector{height:670px} .nn-fig-threshold{height:1164px} .nn-fig-bands{height:623px}
}
```

| Chart | under 390 px | 390 px | 576 px | 768 px | 992 px and up |
|---|---|---|---|---|---|
| Figure 1 timeline | 1910 | 1610 | 1232 | 1299 | 1129 |
| Figure 2 map | 1952 | 1744 | 1507 | 1380 | 861 |
| Figure 3 defector | 884 | 848 | 769 | 826 | 670 |
| Figure 4 threshold | 1652 | 1440 | 1316 | 1281 | 1164 |
| Figure 5 bands | 1042 | 836 | 705 | 646 | 623 |

Limits of Option B:
- Opening a data table, or clicking "Split by cohort" in Figure 5, needs more room than these heights. The Figure 5 split view is about 1450 px at the 700 px column and up to 1720 px on phones. Only Option A handles that.
- A column narrower than the phone widths above can cut a chart off.

## "Explore the data" button

Link both buttons to the full explorer page: `https://journalismatlas.com/preview/nn-launch-kit/explorer/?tab=ways`

(The link no longer includes `embed=1`, so the explorer opens as its own full page. `tab=ways` keeps the view you chose.)

## Charts

| Figure | Title | Where it goes in the report | URL |
|---|---|---|---|
| Figure 0 | Scale of the field: one square vs. $100M | Right after the paper's sentence "Those two numbers sitting next to each other…" | `https://journalismatlas.com/preview/nn-launch-kit/figures/scale/` |
| Figure 1 | Funding and organization timeline, 2018–2026 | Section on funding shocks | `https://journalismatlas.com/preview/nn-launch-kit/figures/timeline/` |
| Figure 2 | The nine cohorts, in three groups | Where the nine cohorts are introduced | `https://journalismatlas.com/preview/nn-launch-kit/figures/map/` |
| Figure 3 | Defector revenue, Years 1–5 | Defector case study | `https://journalismatlas.com/preview/nn-launch-kit/figures/defector/` |
| Figure 4 | Share of revenue from grants and donations, nonprofit newsrooms with $3.5M–$10M in revenue | Nonprofit / threshold section | `https://journalismatlas.com/preview/nn-launch-kit/figures/threshold/` |
| Figure 5 | Revenue band distribution by cohort (n=169) | Bands / cohorts section | `https://journalismatlas.com/preview/nn-launch-kit/figures/bands/` |
| Explorer-style figure | Turn the lens: 169 organizations, five ways to sort them | Optional: where the report points to the explorer | `https://journalismatlas.com/preview/nn-launch-kit/figures/kaleidoscope/` |

The "Where it goes" column is a suggestion based on each figure's content. Confirm placement with Justin.

### Figure 0: Scale of the field: one square vs. $100M

- **Where:** Right after the paper's sentence "Those two numbers sitting next to each other…"
- **URL:** `https://journalismatlas.com/preview/nn-launch-kit/figures/scale/`
- **Height:** 1079 px (desktop); phone 814 px. Not changed in this update; use Option A to size it automatically.
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
- **Height:** 1129 px at the 700 px column; see Option B for other widths.
- **Alt text:** Timeline of 15 dated events in four lanes of pressure on American journalism, 2018 to 2026: platform withdrawal, government defunding, ownership retrenchment and nonprofit failure.

```html
<iframe class="nn-fig-timeline" src="https://journalismatlas.com/preview/nn-launch-kit/figures/timeline/"
  title="Funding and organization timeline, 2018–2026"
  width="100%" height="1129" loading="lazy" scrolling="no"
  style="border:0;display:block;width:100%;max-width:1200px"></iframe>
```

### Figure 2: The nine cohorts, in three groups

- **Where:** Where the nine cohorts are introduced
- **URL:** `https://journalismatlas.com/preview/nn-launch-kit/figures/map/`
- **Height:** 861 px at the 700 px column; see Option B for other widths.
- **Alt text:** The nine governance cohorts in three groups, from Legacy Publishers and Freelance Networks (17 organizations) to B2B and Professional Information Services (17); 169 organizations in all.

```html
<iframe class="nn-fig-map" src="https://journalismatlas.com/preview/nn-launch-kit/figures/map/"
  title="The nine cohorts, in three groups"
  width="100%" height="861" loading="lazy" scrolling="no"
  style="border:0;display:block;width:100%;max-width:1200px"></iframe>
```

### Figure 3: Defector revenue, Years 1–5

- **Where:** Defector case study
- **URL:** `https://journalismatlas.com/preview/nn-launch-kit/figures/defector/`
- **Height:** 670 px at the 700 px column; see Option B for other widths.
- **Alt text:** Defector's revenue rose from $3.2 million in 2020–21 to $4.65 million in 2024–25; subscriptions reached $3.8 million in 2023–24 and held there.

```html
<iframe class="nn-fig-defector" src="https://journalismatlas.com/preview/nn-launch-kit/figures/defector/"
  title="Defector revenue, Years 1–5"
  width="100%" height="670" loading="lazy" scrolling="no"
  style="border:0;display:block;width:100%;max-width:1200px"></iframe>
```

### Figure 4: Share of revenue from grants and donations, nonprofit newsrooms with $3.5M–$10M in revenue

- **Where:** Nonprofit / threshold section
- **URL:** `https://journalismatlas.com/preview/nn-launch-kit/figures/threshold/`
- **Height:** 1164 px at the 700 px column; see Option B for other widths.
- **Alt text:** Of 17 nonprofit newsrooms with $3.5 million to $10 million in revenue, 15 get 80 percent or more of their revenue from grants or donations; Colorado Sun is at 49 percent and LION Publishers at 72 percent.

```html
<iframe class="nn-fig-threshold" src="https://journalismatlas.com/preview/nn-launch-kit/figures/threshold/"
  title="Share of revenue from grants and donations, nonprofit newsrooms with $3.5M–$10M in revenue"
  width="100%" height="1164" loading="lazy" scrolling="no"
  style="border:0;display:block;width:100%;max-width:1200px"></iframe>
```

### Figure 5: Revenue band distribution by cohort (n=169)

- **Where:** Bands / cohorts section
- **URL:** `https://journalismatlas.com/preview/nn-launch-kit/figures/bands/`
- **Height:** 623 px at the 700 px column; see Option B for other widths.
- **Alt text:** 80 of 169 organizations are below $3.5 million, 34 are in the middle and 55 are above $10 million; all 17 legacy publishers are above $10 million and no worker co-op or civic organization is.

```html
<iframe class="nn-fig-bands" src="https://journalismatlas.com/preview/nn-launch-kit/figures/bands/"
  title="Revenue band distribution by cohort (n=169)"
  width="100%" height="623" loading="lazy" scrolling="no"
  style="border:0;display:block;width:100%;max-width:1200px"></iframe>
```

### Explorer-style figure: Turn the lens: 169 organizations, five ways to sort them

- **Where:** Optional: where the report points to the explorer
- **URL:** `https://journalismatlas.com/preview/nn-launch-kit/figures/kaleidoscope/`
- **Height:** 1697 px (desktop); phone 1485 px. Not changed in this update; use Option A to size it automatically.
- **Alt text:** 169 organizations drawn as marks around a center, re-sorted by five lenses: the field, governance, who got past $10M, six ways past $10M, and when they started.

```html
<iframe src="https://journalismatlas.com/preview/nn-launch-kit/figures/kaleidoscope/"
  title="Turn the lens: 169 organizations, five ways to sort them"
  width="100%" height="1697" loading="lazy" scrolling="no"
  style="border:0;display:block;width:100%;max-width:1200px"></iframe>
```

## Teaser video for the explorer button

A short loop of the explorer turning from "the 6 ways" to "History" and back: 10.47 s, 30 fps, no audio. It shows the explorer's chart area only, with no page chrome. The last frame matches the first, so it loops without a jump.

| File | Size | Notes |
|---|---|---|
| `teaser.mp4` | 0.83 MB | 1200 x 960, H.264, no audio, fast start |
| `teaser@2x.mp4` | 1.49 MB | 2400 x 1920, same encoding |
| `teaser-poster.jpg` | 0.09 MB | first frame, 1200 x 960 |

The files are at `https://journalismatlas.com/preview/nn-launch-kit/media/teaser.mp4`, `.../teaser@2x.mp4` and `.../teaser-poster.jpg`. They are also in the `teaser/` folder here.

```html
<video autoplay muted loop playsinline preload="metadata" width="1200" height="960"
  style="width:100%;height:auto;display:block"
  poster="https://journalismatlas.com/preview/nn-launch-kit/media/teaser-poster.jpg">
  <source src="https://journalismatlas.com/preview/nn-launch-kit/media/teaser@2x.mp4" type="video/mp4" media="(min-resolution: 2dppx)">
  <source src="https://journalismatlas.com/preview/nn-launch-kit/media/teaser.mp4" type="video/mp4">
</video>
```

If the video sits next to the button as decoration, add `aria-hidden="true"`. If ASU's pages handle reduced motion elsewhere, add a `prefers-reduced-motion` rule here too, to pause the video or show only the poster.
