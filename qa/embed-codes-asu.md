# Nodes and Networks: report chart embeds (ASU look), designer copy

Written for the ASU web designer. Seven charts, each at a permanent address that will not be renamed; the content behind it may be updated later.

## Read this first

- **ASU look is built in.** Arial and the ASU gold, no `?theme=` parameter needed. Use the URLs exactly as written.
- **No site chrome.** Each page is the chart only, with the credit line the explorer uses.
- **Not indexed, restricted framing.** These pages are marked `noindex, nofollow`, and the framing rule allows `asu.edu`, `*.asu.edu` (so `cronkite.asu.edu`), `journalismatlas.com` and the page itself. Other sites cannot frame these. **These are preview addresses and take effect only after the push.**
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
  width="100%" height="1600" loading="lazy" scrolling="no"
  style="border:0;display:block;width:100%;max-width:1200px"></iframe>
```

### Figure 2: The nine cohorts

- **Where:** Where the nine cohorts are introduced
- **URL:** `https://journalismatlas.com/preview/nn-launch-kit/figures/map/`
- **Desktop height measured:** 992 px (snippet uses 1008). **Phone (390 px) height:** 1201 px. Opening the C3 card adds about 24 px on desktop.
- **Alt text:** Nine governance cohorts drawn as stations on three lines, from Legacy Publishers (17 organizations) to B2B/Professional Services (17); 169 organizations in all.

```html
<iframe src="https://journalismatlas.com/preview/nn-launch-kit/figures/map/"
  title="The nine cohorts"
  width="100%" height="1008" loading="lazy" scrolling="no"
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
  width="100%" height="807" loading="lazy" scrolling="no"
  style="border:0;display:block;width:100%;max-width:1200px"></iframe>
```

### Figure 4: Share of revenue from grants and donations, nonprofits with $3.5M–$10M in revenue

- **Where:** Nonprofit / threshold section
- **URL:** `https://journalismatlas.com/preview/nn-launch-kit/figures/threshold/`
- **Desktop height measured:** 1129 px (snippet uses 1145). **Phone (390 px) height:** 1362 px.
- **Alt text:** Of 17 nonprofits with $3.5 million to $10 million in revenue, 15 get 80% or more of their revenue from grants or donations; Colorado Sun is at 49 percent and LION Publishers at 72 percent.

```html
<iframe src="https://journalismatlas.com/preview/nn-launch-kit/figures/threshold/"
  title="Share of revenue from grants and donations, nonprofits with $3.5M–$10M in revenue"
  width="100%" height="1145" loading="lazy" scrolling="no"
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
  width="100%" height="1062" loading="lazy" scrolling="no"
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

This is a separate snippet from the explorer iframe: a short looping video (10.5 s, no audio) that sits above the explorer button. It is not the explorer itself.

| File | Size | Notes |
|---|---|---|
| `teaser.mp4` | 0.84 MB | 1200 x 960, H.264, no audio, plays as soon as it loads |
| `teaser@2x.mp4` | 1.5 MB | 2400 x 1920, same encoding, used on high-density screens |
| `teaser-poster.jpg` | 0.09 MB | first frame, 1200 x 960 |

URLs: `https://journalismatlas.com/preview/nn-launch-kit/media/teaser.mp4`, `.../teaser@2x.mp4`, `.../teaser-poster.jpg`. Same restrictions as the charts: these are preview addresses and take effect after the push.

```html
<video autoplay muted loop playsinline preload="metadata" width="1200" height="960"
  style="width:100%;height:auto;display:block"
  poster="https://journalismatlas.com/preview/nn-launch-kit/media/teaser-poster.jpg">
  <source src="https://journalismatlas.com/preview/nn-launch-kit/media/teaser@2x.mp4" type="video/mp4" media="(min-resolution: 2dppx)">
  <source src="https://journalismatlas.com/preview/nn-launch-kit/media/teaser.mp4" type="video/mp4">
</video>
```

Add `aria-hidden="true"` if the video is purely decorative next to the button; add a `prefers-reduced-motion` rule (pause, or show only the poster) if ASU's pages do that elsewhere.
