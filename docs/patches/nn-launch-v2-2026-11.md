# Nodes and Networks launch flip, v2 (for Thu Nov 5, 2026)

Written Nov 1 against `main` at `8179b90`. NOT applied. Justin applies it by hand in GitHub Desktop on launch day.

**Supersedes** `docs/patches/strip-nn-launch-2026-11-05.md` (written before the gate work: wrong strip id, wrong `nn-gate.js` key, status flip no longer needed) and the `nn-launch` branch (`61ea380`, `451b4ac`, `5be2bbc`, `af432d2`). Those edit the same lines in `header.js` and `research.json` as `8179b90`, so merging the branch will conflict. Don't merge it; use this patch, then archive the branch.

## What the new gate already does (no change needed)

`assets/js/nn-gate.js` flips these at the `publishAt` instant, with no deploy: the homepage N&N card (`index.html`), the About lead swap (`about-this-project.html`), the `/for-brands` Research line, the hub piece (`data/research.json` entries with `"gate": "nn"` are filtered out before launch and forced `live` after, `research-hub.js:247-249`). **So `451b4ac` (status `placeholder` → `live`) is redundant. Skip it.**

The three changes below are NOT time-gated. Apply them together, at launch.

## 1. `assets/js/header.js`: replace the `ATLAS_STRIP` object (lines 16-25)

```js
var ATLAS_STRIP = {
  id: 'nodes-and-networks-2026-11',
  enabled: true,
  expires: '2026-12-15',
  selfPath: '/nodes-and-networks/',
  hideOn: [],
  announce: { label: 'New from the Atlas', text: 'Nodes and Networks, a field study of how American journalism is reorganizing', linkText: 'Read the study', href: '/nodes-and-networks/' },
  welcome:  { text: 'You’re reading the Independent Journalism Atlas. We map {count} independent journalists by beat and place.',
              links: [ { text: 'Explore the Atlas', href: '/search' }, { text: 'How we find them', href: '/how-we-did-this.html' } ] }
};
```

- New id re-shows the strip to everyone who dismissed `watershed-2026-11`.
- Wording is your D2 ruling. `5be2bbc` put "New from the Atlas:" inside `text` under a different label ("Research from the Atlas"); `main`'s label is already "New from the Atlas", so I moved the lead-in to the label rather than repeat it.
- `expires` is my pick (Watershed's is `2026-11-30`). Change it if you want a different run.
- `welcome` is copied from the current config; still `{count}`, no typed number.
- TK-PARTNER: no ASU Cronkite / Knight Center credit in the strip until you confirm wording.

## 2. `_headers`: delete the pre-launch noindex block (lines 36-41, plus the blank line above)

```
-
-# >>> nn pre-launch noindex (remove Nov 5)
-# Keeps the early page out of search until ASU publishes. The page stays reachable and the explorer frame rule above still applies.
-/nodes-and-networks/*
-  X-Robots-Tag: noindex, nofollow
-# <<<
```

Leave the `# >>> nn permanent home` block (lines 29-35) alone; it holds the ASU frame-ancestors rule. This is the same hunk as `61ea380`. Check afterwards that `curl -sI https://journalismatlas.com/nodes-and-networks/` no longer shows `x-robots-tag`. The page's own `<meta name="robots">` is a separate check (see "Checks").

## 3. `data/research.json`: swap the featured card

- `watershed` record (line 54): `"featured": true` → `"featured": false`
- `nodes-and-networks` record (line 76): `"featured": false` → `"featured": true`

Leave `"status": "placeholder"` and `"gate": "nn"` as they are. The hub takes the first piece that is `featured && live` (`research-hub.js:250`); without this swap Watershed keeps the featured slot after launch. Don't land this before launch: before the instant the N&N piece is filtered out, so unfeaturing Watershed would leave the hub with no featured card.

`hero_image.src` stays `""` unless you supply one (the card renders without an image). `authors` and `partners` stay empty (TK-PARTNER).

## 4. `for-brands.html`: link target (safe to land any time; the line is hidden until the instant)

```
-          <!-- SOFT: shown by assets/js/nn-gate.js at the N&N publish instant (data-nn-show). Link currently /research; swap to the paper's final URL at launch. -->
-          <li data-nn-show hidden><a href="/research">Nodes and Networks</a>: 169 organizations, and governance predicts scale.</li>
+          <!-- SOFT: shown by assets/js/nn-gate.js at the N&N publish instant (data-nn-show). Links to /nodes-and-networks/. -->
+          <li data-nn-show hidden><a href="/nodes-and-networks/">Nodes and Networks</a>: 169 organizations, and governance predicts scale.</li>
```

(lines 419-420; same hunk as `af432d2`.) If the paper's final URL is not `/nodes-and-networks/` (L6), use that URL here instead.

## Before this patch is applied (not part of it)

- L1: set the real release time in `assets/js/nn-gate.js:6` (`publishAt`) and push `main` by Tue Nov 3.
- Rogan / launch target ruling (see `docs/briefs/PHASE1-ROGAN-LAUNCH-TARGET-OPTIONS-2026-11-01.md`). The strip points at `/nodes-and-networks/`, so that page should be in its final state first.
- Optional, low priority: the `research.html` noscript link (line 694) still points to `/watershed/`. After launch the hub's featured piece is N&N, so you may want it to read "Nodes and Networks" with `/nodes-and-networks/`.

## Checks after applying (local server, 1280 and 390 px)

1. `/`: strip reads the new text and links to `/nodes-and-networks/`; N&N card visible.
2. `/research`: N&N is the featured card; Watershed sits in the grid.
3. `/nodes-and-networks/`: strip shows the welcome message (selfPath).
4. `/for-brands`: Research line links to `/nodes-and-networks/`.
5. `python3 scripts/check_brand.py --tight` stays at 2,766.
6. Search visibility: the three built pages in `nn/built/nodes-and-networks/` carry no `noindex` meta (grep, Nov 1), so the `_headers` block was the only source. `nn/src` has no robots tag either.
