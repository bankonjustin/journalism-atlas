# Strip swap for Nodes and Networks launch (Thursday Nov 5, 2026)

Ready to apply by hand. NOT applied. Three files change. Apply this FIRST on launch day, together with the paper going out, so the strip text and the hub link never lag the launch.

## 1. `assets/js/header.js`: replace the whole `ATLAS_STRIP` object (lines ~16-25)

```js
var ATLAS_STRIP = {
  id: 'nodes-and-networks-2026-11',
  enabled: true,
  expires: '2026-12-15',
  selfPath: '/nodes-and-networks/',
  hideOn: [],
  // TK-PARTNER: ASU Cronkite / Knight Center credit goes in only once Justin confirms the wording.
  announce: { label: 'New from the Atlas', text: 'Nodes and Networks: what 169 journalism organizations reveal about how independent media grows', linkText: 'Read the study', href: '/nodes-and-networks/' },
  welcome:  { text: 'You’re reading the Independent Journalism Atlas. We map {count} independent journalists by beat and place.',
              links: [ { text: 'Explore the Atlas', href: '/search' }, { text: 'How we find them', href: '/how-we-did-this.html' } ] }
};
```

The `welcome` block is copied verbatim from the current config (still `{count}`, no hardcoded number).
New id re-shows the strip to everyone who dismissed `research-2026-11`.

## 2. `data/research.json`

- `nodes-and-networks` record: `"status": "coming"` back to `"live"` (held since the Oct 31 pre-launch hold), and `"featured": true`.
- `watershed` record: `"featured": false`. The hub shows one featured card (`research-hub.js` takes the first `featured && live` piece), so Watershed must be unfeatured or it wins by order.
- `hero_image.src` stays `""` unless Justin supplies one. `authors` and `partners` stay empty (TK-PARTNER).

## 3. `_headers`: remove the pre-launch noindex block

Delete everything from `# >>> nn pre-launch noindex (remove Nov 5)` through the closing `# <<<` (the `/nodes-and-networks/*` `X-Robots-Tag: noindex, nofollow` rule). Leave the `nn permanent home` explorer frame-ancestors rule alone.

## Notes

- `/nodes-and-networks/` loads `header.js` (`nn/built/nodes-and-networks/index.html:38`), so welcome mode will work there.
- Homepage N&N card is date-gated by `assets/js/nn-gate.js` (`publishDate: '2026-11-05'`) and goes live on its own Thursday.
- Open TK: partner credit wording (ASU Cronkite / Knight Center).
