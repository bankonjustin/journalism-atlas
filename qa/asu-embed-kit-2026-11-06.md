# ASU embed kit: auto-height listener, fixed-height fallback, embed codes (DRAFT)

Draft, Nov 6. Not in Drive yet. Heights are for the versions on branch `nn/asu-preview-fixes` (not yet pushed), light mode, data tables **closed**, each measured plus 16 px.
Re-measure on ASU's live page after the push before sending anything to Carrie.

## Measured on ASU's page today (before the push)

| Figure | ASU iframe height | Live content height at the 700 px column |
|---|---|---|
| Timeline | 1471 | 1506 |
| Map | 1050 | 1061 |
| Defector | 600 | 654 |
| Threshold | 1145 | 1148 |
| Bands | 600 | 607 |

- ASU iframes: `border:0;display:block;max-width:1200px;width:100%` (map 1400 px), no `title`, no class, no query string.
- Column width: 700 px at window widths 1100 and 1470. At a 500 px window (Chrome's minimum) it is 436 px for the four visible figures and 379 px for the Defector.
- Defector sits in a collapsed accordion. Opened, it is 700 px wide at a 1470 px window, with iframe height 600 against 654 of content. It posts the same height at 379 px.
- The page runs 10 inline scripts and has no `nn:resize` listener. Carrie should ask whether her designer can paste a script.
- Both "Explore the data" buttons point at the explorer with `embed=1` and `tab=ways`.

## "Explore the data" button

`https://journalismatlas.com/preview/nn-launch-kit/explorer/?tab=ways` (no `embed=1`; `tab=ways` kept to match what ASU chose).

## Embed codes

**Funding and organization timeline**
```html
<iframe class="nn-fig-timeline" src="https://journalismatlas.com/preview/nn-launch-kit/figures/timeline/"
  title="Funding and organization timeline, 2018–2026"
  width="100%" height="1129" loading="lazy" scrolling="no"
  style="border:0;display:block;width:100%;max-width:1200px"></iframe>
```

**The nine cohorts**
```html
<iframe class="nn-fig-map" src="https://journalismatlas.com/preview/nn-launch-kit/figures/map/"
  title="The nine cohorts, in three groups"
  width="100%" height="861" loading="lazy" scrolling="no"
  style="border:0;display:block;width:100%;max-width:1200px"></iframe>
```

**Defector revenue**
```html
<iframe class="nn-fig-defector" src="https://journalismatlas.com/preview/nn-launch-kit/figures/defector/"
  title="Defector revenue, Years 1–5"
  width="100%" height="670" loading="lazy" scrolling="no"
  style="border:0;display:block;width:100%;max-width:1200px"></iframe>
```

**Share of revenue from grants and donations**
```html
<iframe class="nn-fig-threshold" src="https://journalismatlas.com/preview/nn-launch-kit/figures/threshold/"
  title="Share of revenue from grants and donations, nonprofit newsrooms with $3.5M–$10M in revenue (17 organizations)"
  width="100%" height="1164" loading="lazy" scrolling="no"
  style="border:0;display:block;width:100%;max-width:1200px"></iframe>
```

**Revenue band distribution by cohort (n=169)**
```html
<iframe class="nn-fig-bands" src="https://journalismatlas.com/preview/nn-launch-kit/figures/bands/"
  title="Revenue band distribution by cohort (n=169)"
  width="100%" height="623" loading="lazy" scrolling="no"
  style="border:0;display:block;width:100%;max-width:1200px"></iframe>
```

## Option A: auto-height script (recommended)

Paste once on the page, after the iframes. Accepts messages only from journalismatlas.com, only from the iframe that sent them, and changes only that iframe's height. Tested on ASU's live page in Chrome (tab only): all four visible figures resized to their content. Iframes load lazily, so each resizes as it scrolls into view.

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

Message format: `{type:"nn:resize", height:<px>}`. Four figures also send `v`, `fig` and `nonce`.

## Option B: fixed heights (CSS)

Use if the page can't take the script. The classes are already on the embed codes above; the CSS wins over the `height` attribute.
Columns: 350 px phone (estimate, measured locally), 436 px and 700 px (measured on ASU). The breakpoints below are **viewport widths and are a guess**: replace 480 and 992 with the page's real breakpoints once known.

| Figure | 350 px column | 436 px column | 700 px column |
|---|---|---|---|
| timeline | 1512 | 1352 | 1129 |
| map | 1650 | 1523 | 861 |
| defector | 783 | 785 | 670 |
| threshold | 1423 | 1334 | 1164 |
| bands | 797 | 713 | 623 |

```css
.nn-fig-timeline{height:1512px}
.nn-fig-map{height:1650px}
.nn-fig-defector{height:783px}
.nn-fig-threshold{height:1423px}
.nn-fig-bands{height:797px}
@media (min-width:480px){
  .nn-fig-timeline{height:1352px}.nn-fig-map{height:1523px}.nn-fig-defector{height:785px}.nn-fig-threshold{height:1334px}.nn-fig-bands{height:713px}
}
@media (min-width:992px){
  .nn-fig-timeline{height:1129px}.nn-fig-map{height:861px}.nn-fig-defector{height:670px}.nn-fig-threshold{height:1164px}.nn-fig-bands{height:623px}
}
```

Limits of Option B:
- Opening the Figure 1 data table, or clicking "Split by cohort" in Figure 5, needs more room than these heights. Bands split view is 1450 px at 700, 1602 at 436 and about 1720 at 350. Only Option A handles those.
- Columns narrower than 350 px can clip the phone heights.
- Figure 1 is not monotonic with width (its layout switches at 520 px), so check it if a column lands between 436 and 700.
