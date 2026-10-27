# Embedding the Nodes and Networks explorer

Replace `{{EXPLORER_URL}}` with the final address once the report URL is set. Until then the preview address is
`https://journalismatlas.com/preview/nn-launch-kit/explorer/`.
Every example uses `?embed=1`, which removes the page header and footer, makes the background transparent and reports its height to the host page.

## 1. Plain iframe (any CMS that allows iframes)

The explorer reflows by width, so its height is not one fixed ratio. These heights fit every tab: **1400 px** under 640 px wide, **1200 px** from 640 px up.

```html
<iframe
  src="{{EXPLORER_URL}}?embed=1&tab=governance"
  title="Nodes and Networks explorer: 169 U.S. journalism organizations"
  loading="lazy"
  style="display:block;width:100%;max-width:760px;height:1400px;margin:0 auto;border:0"></iframe>
```

If the CMS allows a `<style>` block, this swaps the height by width:

```html
<style>.nn-frame{display:block;width:100%;max-width:760px;height:1400px;margin:0 auto;border:0}
@media (min-width:640px){.nn-frame{height:1200px}}</style>
<iframe class="nn-frame" src="{{EXPLORER_URL}}?embed=1&tab=governance" title="Nodes and Networks explorer" loading="lazy"></iframe>
```

## 2. Auto-height iframe (CMS allows scripts)

The explorer posts `{source:'nn-explorer', type:'height', height:<px>}` whenever its size changes. The listener resizes the frame to fit, so there is no empty space or inner scrollbar.

```html
<iframe id="nn-explorer" src="{{EXPLORER_URL}}?embed=1&tab=governance"
  title="Nodes and Networks explorer" loading="lazy"
  style="display:block;width:100%;max-width:760px;height:1400px;margin:0 auto;border:0"></iframe>
<script>
addEventListener('message', function (e) {
  var d = e.data, f = document.getElementById('nn-explorer');
  if (!d || d.source !== 'nn-explorer' || d.type !== 'height' || e.source !== f.contentWindow) return;
  f.style.height = d.height + 'px';
});
</script>
```

The `e.source` check accepts messages only from this frame. Use a second copy of the snippet with a different `id` for a second explorer on the same page.

## 3. Fallback (CMS strips iframes)

A still image of the governance tab, linked to the live explorer. File: `nodes-networks-governance-4x5-still.png` (1080 × 1350, upload it to the CMS media library).

```html
<a href="{{EXPLORER_URL}}?tab=governance">
  <img src="nodes-networks-governance-4x5-still.png" width="1080" height="1350"
       style="max-width:100%;height:auto"
       alt="169 U.S. journalism organizations arranged in nine governance cohorts, colored by governance group. Open the interactive explorer.">
</a>
```

## 4. Deep links

Add `&embed=1` to any of these when embedding.

| View | Link |
|---|---|
| Governance (default) | `{{EXPLORER_URL}}?tab=governance` |
| The 6 ways | `{{EXPLORER_URL}}?tab=ways` |
| History | `{{EXPLORER_URL}}?tab=history` |

## Notes for ASU

- Tabs are keyboard reachable (arrow keys move between them) and the explorer follows the visitor's light or dark setting. The chart stage is always black.
- With "reduce motion" on, tabs switch instantly with no animation.
- Hover or tap a mark for a card. The card shows cohort, path to size and year founded. This address withholds organization names; whether names appear is still an open decision.
- No cookies, no network requests, no external fonts or scripts: the page is one self-contained file.
- Open questions for ASU: whether iframes are allowed, whether scripts are allowed, and the maximum content width. These decide which snippet to use.
