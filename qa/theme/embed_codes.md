# Nodes and Networks: figure embed codes (ASU theme)

Each snippet loads one figure in the ASU look (Arial, ASU palette). Use the URLs exactly as written: `theme=asu` switches the look on, and `v=asu1` makes sure browsers and caches fetch the new version.

**Height:** the figure reports its own height to the page that embeds it. The fixed `height` below is the tallest the figure got in our tests at an iframe width of 390 px (phone), 760 px and 1200 px, plus a small margin, so nothing is cut off. If your page allows scripts, the optional resize snippet at the end trims the extra space.

**Address:** the figures are served from a preview address (not indexed by search engines). When the final address is set, swap only the part before `/embed/`; keep `?theme=asu&v=asu1`.

## Figure 0: scale of the field

Tested heights: 814 px at 390 wide, 894 px at 760, 1063 px at 1200.

```html
<iframe
  src="https://journalismatlas.com/preview/nodes-and-networks-edition-e852c5c5/embed/fig-0-scale/?theme=asu&v=asu1"
  title="scale of the field"
  loading="lazy"
  style="display:block;width:100%;max-width:1200px;height:1079px;border:0"></iframe>
```

## Figure 1: timeline

Tested heights: 1988 px at 390 wide, 1636 px at 760, 1000 px at 1200.

```html
<iframe
  src="https://journalismatlas.com/preview/nodes-and-networks-edition-e852c5c5/embed/fig-1-timeline/?theme=asu&v=asu1"
  title="timeline"
  loading="lazy"
  style="display:block;width:100%;max-width:1200px;height:2004px;border:0"></iframe>
```

## Figure 2: map

Tested heights: 1240 px at 390 wide, 1119 px at 760, 1046 px at 1200.

```html
<iframe
  src="https://journalismatlas.com/preview/nodes-and-networks-edition-e852c5c5/embed/fig-2-map/?theme=asu&v=asu1"
  title="map"
  loading="lazy"
  style="display:block;width:100%;max-width:1200px;height:1256px;border:0"></iframe>
```

## Figure 3: Defector revenue, Years 1-5

Tested heights: 748 px at 390 wide, 663 px at 760, 791 px at 1200.

```html
<iframe
  src="https://journalismatlas.com/preview/nodes-and-networks-edition-e852c5c5/embed/fig-3-defector/?theme=asu&v=asu1"
  title="Defector revenue, Years 1-5"
  loading="lazy"
  style="display:block;width:100%;max-width:1200px;height:807px;border:0"></iframe>
```

## Figure 4: the $10M threshold

Tested heights: 1384 px at 390 wide, 1129 px at 760, 1129 px at 1200.

```html
<iframe
  src="https://journalismatlas.com/preview/nodes-and-networks-edition-e852c5c5/embed/fig-4-threshold/?theme=asu&v=asu1"
  title="the $10M threshold"
  loading="lazy"
  style="display:block;width:100%;max-width:1200px;height:1400px;border:0"></iframe>
```

## Figure 5: revenue bands

Tested heights: 739 px at 390 wide, 622 px at 760, 584 px at 1200.

```html
<iframe
  src="https://journalismatlas.com/preview/nodes-and-networks-edition-e852c5c5/embed/fig-5-bands/?theme=asu&v=asu1"
  title="revenue bands"
  loading="lazy"
  style="display:block;width:100%;max-width:1200px;height:755px;border:0"></iframe>
```

## Figure 6: Turn the lens

Tested heights: 1485 px at 390 wide, 1614 px at 760, 1681 px at 1200.

```html
<iframe
  src="https://journalismatlas.com/preview/nodes-and-networks-edition-e852c5c5/embed/fig-6-kaleidoscope/?theme=asu&v=asu1"
  title="Turn the lens"
  loading="lazy"
  style="display:block;width:100%;max-width:1200px;height:1697px;border:0"></iframe>
```

## Optional: trim the height automatically

Add once per page, after the iframes. Each figure posts `{type:'nn:resize', v:1, fig:'<figure id>', height:<px>}` whenever its size changes.

```html
<script>
addEventListener('message', function (e) {
  var d = e.data;
  if (!d || d.type !== 'nn:resize' || d.v !== 1) return;
  document.querySelectorAll('iframe[src*="/embed/"]').forEach(function (f) {
    if (f.contentWindow === e.source) f.style.height = d.height + 'px';
  });
});
</script>
```

## The explorer button

Link the "explore" button to the explorer with the ASU look on:

`https://journalismatlas.com/nodes-and-networks/explorer/?theme=asu`

To frame it instead, add `&embed=1` (the explorer then also hides its page header and footer): `https://journalismatlas.com/nodes-and-networks/explorer/?embed=1&tab=ways`
