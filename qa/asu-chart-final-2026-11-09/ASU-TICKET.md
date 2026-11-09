# Nodes and Networks: chart embed update

Replace the five chart embeds and add this CSS; no other changes.

## 1. The five chart embeds

Swap each existing chart embed for the matching snippet below. Each snippet has the same address as the current one, with the same title. The `height` is the desktop height. The CSS in section 2 sets the height at every other screen width.

**Figure 1**
```html
<iframe class="nn-fig-timeline" src="https://journalismatlas.com/preview/nn-launch-kit/figures/timeline/"
  title="Funding and organization timeline, 2018–2026"
  width="100%" height="1021" loading="lazy" scrolling="no"
  style="border:0;display:block;width:100%;max-width:1200px"></iframe>
```

**Figure 2**
```html
<iframe class="nn-fig-map" src="https://journalismatlas.com/preview/nn-launch-kit/figures/map/"
  title="The nine cohorts"
  width="100%" height="786" loading="lazy" scrolling="no"
  style="border:0;display:block;width:100%;max-width:1400px"></iframe>
```

**Figure 3** (this one sits in the accordion)
```html
<iframe class="nn-fig-defector" src="https://journalismatlas.com/preview/nn-launch-kit/figures/defector/"
  title="Defector revenue, Years 1–5"
  width="100%" height="541" loading="lazy" scrolling="no"
  style="border:0;display:block;width:100%;max-width:1200px"></iframe>
```

**Figure 4**
```html
<iframe class="nn-fig-threshold" src="https://journalismatlas.com/preview/nn-launch-kit/figures/threshold/"
  title="Share of revenue from grants and donations, nonprofit newsrooms with $3.5M–$10M in revenue"
  width="100%" height="993" loading="lazy" scrolling="no"
  style="border:0;display:block;width:100%;max-width:1200px"></iframe>
```

**Figure 5**
```html
<iframe class="nn-fig-bands" src="https://journalismatlas.com/preview/nn-launch-kit/figures/bands/"
  title="Revenue band distribution by cohort (n=169)"
  width="100%" height="428" loading="lazy" scrolling="no"
  style="border:0;display:block;width:100%;max-width:1200px"></iframe>
```

## 2. CSS (add once, in the page's custom CSS)

The charts changed height, so each one needs a new height at each screen width. Each height is the chart's height plus 16 px of room. The breakpoints match the page's own column widths. Figure 3 is narrower because it sits in the accordion, so it has its own numbers and one extra step at 1260 px.

```css
/* Under 390 px */
.nn-fig-timeline{height:1751px}
.nn-fig-map{height:1833px}
.nn-fig-defector{height:692px}
.nn-fig-threshold{height:1477px}
.nn-fig-bands{height:752px}

/* 390 px and up */
@media (min-width:390px){
  .nn-fig-timeline{height:1470px}
  .nn-fig-map{height:1643px}
  .nn-fig-defector{height:669px}
  .nn-fig-threshold{height:1284px}
  .nn-fig-bands{height:611px}
}

/* 576 px and up */
@media (min-width:576px){
  .nn-fig-timeline{height:1111px}
  .nn-fig-map{height:1421px}
  .nn-fig-defector{height:630px}
  .nn-fig-threshold{height:1154px}
  .nn-fig-bands{height:498px}
}

/* 768 px and up */
@media (min-width:768px){
  .nn-fig-timeline{height:1193px}
  .nn-fig-map{height:1310px}
  .nn-fig-defector{height:684px}
  .nn-fig-threshold{height:1114px}
  .nn-fig-bands{height:434px}
}

/* 992 px and up */
@media (min-width:992px){
  .nn-fig-timeline{height:1021px}
  .nn-fig-map{height:786px}
  .nn-fig-defector{height:517px}
  .nn-fig-threshold{height:993px}
  .nn-fig-bands{height:428px}
}

/* 1260 px and up: the accordion is wide enough for the full-size Figure 3 */
@media (min-width:1260px){
  .nn-fig-defector{height:541px}
}
```

## 3. "Explore the data" button

Point both "Explore the data" buttons to:

`https://journalismatlas.com/preview/nn-launch-kit/explorer/?tab=ways`
