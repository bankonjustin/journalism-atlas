# Favicon answers for James, November 2026

**Answers:** "What we need from you, Justin" in `Atlas-Page-Template-Brief-2026-11.md`, in order.
**Facts checked against:** `main` at 258d135, Nov 4 2026. Colors and transparency were measured from the image files, not read from source (see 4 and 5).

## Corrections to the brief's assumptions

- **There is no `icon.svg`.** Nothing in the repo is named `icon.svg`, and no page links an SVG icon. The set the site uses is `favicon.ico`, `favicon-v2.png` and `apple-touch-icon.png`. Your partial and the v17 "only two icons" rule need to match this set.
- **Root `favicon.ico` was already the current design** (chartreuse with the black ATLAS globe). The brief assumed it was the old icon. Watershed's problem was a relative path (`assets/favicon.png`) that 404s under `/watershed/`, pointing at an old 140px JPEG saved as `.png`.
- **`header.js` and `footer.js` self-inject. There are no mount-point divs.** `header.js` inserts the nav before its own `<script>` tag. `footer.js` appends the footer to the end of `<body>`. The skeleton in 2.2 (`<div id="site-header">`, `<div id="site-footer">`) matches nothing on the homepage, so the `shared-header` and `shared-footer` checks should test for the script tags, not mount IDs.

## 1. Repo paths

| File | Path | Size |
|---|---|---|
| `icon.svg` | does not exist | n/a |
| `apple-touch-icon.png` | `/apple-touch-icon.png` (repo root) | 180 x 180 |
| `favicon-v2.png` | `/assets/img/favicon-v2.png` | 32 x 32 |
| `favicon.ico` | `/favicon.ico` (repo root) | 16, 32, 48 |

## 2. The homepage's exact markup

```html
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" href="/assets/img/favicon-v2.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
```

The apple-touch-icon tag has no `sizes` attribute. About 53 other pages carry the same three tags (one more page has the `favicon.ico` tag but not the other two). Watershed was the outlier, and PR A gives it and `/watershed/methods/` the same three tags.

## 3. What is at `/favicon.ico`

A three-image ICO (16, 32 and 48 px, PNG-encoded), the current design. **PR A left it unchanged.** It is a browser fallback with no counterpart in your "only two icons" list, so v17 should say whether it counts as one of the allowed icons. The build copies it to `dist/` (`build-dist.sh`).

## 4. Colors

There is no SVG to read hex values from. I sampled the PNGs and the ICO images instead. Two colors make up the design:

- **`#ceff00`**, the background, about 56% of the 180px icon. This is Acid.
- **`#000000`**, the globe and wordmark.

Other values in the files are anti-aliasing blends between those two. Please confirm both are Tier 1.

## 5. Opacity

`apple-touch-icon.png` is **opaque to its edges**: RGB, no alpha channel, with `#ceff00` in all four corners. `favicon-v2.png`, `favicon-v2-192.png` and all three ICO images are also opaque (minimum alpha 255).

## 6. Where `Journalism_Atlas_favicon.png` is used

`assets/images/icons/Journalism_Atlas_favicon.png` is a 140px JPEG saved as `.png`, showing the old white globe.

- **Live pages:** none.
- **Live docs:** `atlas-portal/README.md:63` (an example `<link>`, not a page).
- **v16.1:** `docs/design/DESIGN-TOKENS-v16.1.md:793`, in the asset list. Older token files in `docs/design/archive/` list it too.
- **Retired pages:** `_deprecated/` (`postcard`, `pack`, `what-we-do`, `index-mock-V1/V2`, `index-exploration-V1`). These are not published.
- **Private repo:** old page snapshots only.

After PR A, nothing live references it. It is still in the repo; v17 can delete it.

**Related: `watershed/assets/favicon.png`** is a second copy of the same old icon (140px JPEG saved as `.png`). It is now unreferenced and was not deleted. Flag it for v17 cleanup alongside `Journalism_Atlas_favicon.png`.

## 7. Other icons and manifests

- `assets/img/favicon-v2-192.png` (192px, current design) exists, but no page links it. Do not treat it as part of the set.
- **No web manifest**, no `manifest.json` or `.webmanifest`, and no Android icons.
- `assets/images/icons/Journalism_Atlas_icon_*.png` are brand icon variants (JPEG data), used as artwork, not favicons.

## 8. Exceptions-register pages and shared chrome

No Exceptions-register page loads a favicon today. Inventory:

- **No header, no footer, no icon tags:**
  - `preview/nodes-and-networks-edition-*` and `preview/nodes-and-networks-f348eb08` (page and explorer)
  - `preview/nn-launch-kit/*`, including `explorer`, `review`, `embed-test`, `explorer-named` and every `figures/*` page
  - the 7 figure embeds under `preview/nodes-and-networks-edition-*/embed/`
  - `nn/built/nodes-and-networks/explorer/`
- **Header script only, plus icon tags:** `nn/built/nodes-and-networks/index.html` and `nn/built/nodes-and-networks/embed/index.html`.
- **Header, footer and icon tags (not Exceptions pages):** `preview/research` and `preview/smartnews-d029dc36`.

**Question for you, decided after the Nov 5 launch:** the built N&N page `/nodes-and-networks/embed/` loads `header.js`. Should an embed carry the shared header at all? These pages are framed on partner sites. For the `check_pages.py` scope, Exceptions-register paths and any `embed/` page should stay out.
