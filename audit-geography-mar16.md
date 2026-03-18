# Geography Field Audit
### March 16, 2026 — Pre-cutover mapping

This documents every place `geography` (the freeform JSON field) is read across the codebase, so we can plan the cutover to structured geo fields. No changes were made in this session.

---

## 1. Every place `geography` is read and what it does

### `assets/js/main.js` (powers `index.html`)

| Location | What it does |
|---|---|
| Line 160–161 | Filter logic: `filterState.filters.geography.has(creator.geography)` — exact string match against the active filter set |
| Lines 167, 315 | Search: `creator.geography.toLowerCase().includes(s)` — geography is included in full-text search |
| Lines 408–442 | Filter UI population: iterates all `creator.geography` values from the JSON, counts them, and builds the checkbox list dynamically. No hardcoded values. |
| Lines 534, 552 | Table view: column header `"Geography"`, cell renders `creator.geography || '-'` |
| Lines 624–627 | Creator card/modal: displays `creator.geography` as a clickable tag that sets the geography filter |
| Lines 774–814 | URL state: writes `?geography=...` param and reads it back to restore filter state |
| Lines 1141–1142 | Bubble chart click handler: clicking a geography bubble calls `filterState.toggle('geography', bubble.name)` |
| Line ~891 | Bubble chart data: `c[currentBubbleMode]` — when mode is `'geography'`, this reads `c.geography` directly |

**Mode button:** `index.html` line 258 has a "By Geography" button that sets `currentBubbleMode = 'geography'`. The bubble chart then groups by `creator.geography`.

### `pack.html` (the Pack/bubble-pack view)

| Location | What it does |
|---|---|
| Lines 1432–1447 | `PRIMARY_GEOS` — hardcoded list of 13 geography pill values (see below) |
| Line 1497–1502 | Renders a pill button for each `PRIMARY_GEOS` entry; `btn.dataset.geo = geo` |
| Lines 1520–1521 | `toggleGeo()`: adds/removes from `activeGeos` Set |
| Line 1539 | Filter: `activeGeos.has(c.geography)` — exact match against freeform string |
| Lines 1328–1334 | URL param: `?geo=` → `activeGeos.add(geoVal)` |

**Hardcoded `PRIMARY_GEOS` values:**
```
'Chicago, IL', 'New York, NY', 'Washington, D.C.', 'Los Angeles, CA',
'San Francisco, CA', 'Boston, MA', 'Philadelphia, PA', 'Atlanta, GA',
'Austin, TX', 'National - US', 'United Kingdom', 'Canada', 'International'
```
These are exact strings matched against `creator.geography`. If the freeform field changes, these pills break silently (they just stop matching).

### `city-lab-chicago.html`

- Uses **inline hardcoded creator data** — NOT loaded from `creators-data.json`.
- `geography` field on each inline object is a simple string: `"Chicago"` or `"Illinois"`.
- Filter at line 1168: `c.geography === 'Illinois'` or `c.geography === 'Chicago'` (two-state dropdown, explicit string comparison).
- Table at line 1214: displays `c.geography`.
- **Not affected by changes to `creators-data.json`** — this page is self-contained.

### `city-lab-dc.html`

- Loads from `assets/data/dmv-creators.json`, `dmv-recent-posts.json`, `dc-creators-full.json`.
- `dmv-creators.json` schema has a `geography` field (e.g. `"Washington, D.C."`) plus a `subgeography` field. Neither `geoCity` nor `geoState` exist here.
- `dc-creators-full.json` uses a `location` field, not `geography`.
- `geoGroup()` function (line 1131): normalizes freeform geography into 4 buckets: `'Maryland'`, `'Virginia'`, `'Washington, D.C.'`, or passthrough. Uses string pattern matching (`includes('Maryland')`, `includes('D.C.')`, etc.).
- Filter at lines 1318, 1412: `geoGroup(c.geography) === geo` and `geoGroup(p.geography) === geo`.
- Table at line 1396: displays `c.geography` raw.
- **Not reading from `creators-data.json`** — uses its own separate JSON files.

### `city-lab-dc2.html`

- Same data sources as `city-lab-dc.html` (fetches `dmv-creators.json`, `dmv-recent-posts.json`, `dc-creators-full.json`).
- Same `geoGroup()` function (line 1327), same filter and display patterns.
- **Not reading from `creators-data.json`.**

### `lists.html`

| Location | What it does |
|---|---|
| Line 759 | Hardcoded list filter: `d.geography` tested against a regex of country names for the "International Voices" list |
| Line 859 | Search: `(d.geography || '').toLowerCase().includes(lower)` |
| Line 881 | Display: `d.geography || ''` in the creator card |

`lists.html` loads from `creators-data.json` (via the same data loader as `index.html`). The "International Voices" list filter is a regex test against `d.geography`:
```js
/brazil|germany|france|italy|japan|south korea|indonesia|india|philippines|hungary|austria|south asia|palestine|ukraine|iraq|dubai/i.test(d.geography)
```
This is freeform-string-dependent.

### Other files

- `beat-climate.html`, `beat-finance.html`, `beat-tech.html`: have a `<section id="geography">` in HTML but this is a page section anchor, not data access. No JS reads a `geography` field.
- `research.html`, `advisory.html`, etc.: no `geography` data access found.

---

## 2. Which uses can cleanly switch to structured fields

| Current use | Could switch to | Notes |
|---|---|---|
| `main.js` filter UI (checkbox population) | `geoCity` or `geoState` or `geoCountry` | Dynamically built from JSON — just change which field it reads. Straightforward. |
| `main.js` filter logic | `geoCity` / `geoState` / etc. | Same — once filter UI switches, filter logic follows. |
| `main.js` table column display | `geoCity`, `geoState`, or a formatted combination | Easy swap; consider showing `"City, State"` or `geoCountry` for internationals. |
| `main.js` bubble chart (geography mode) | `geoState` or `geoCountry` | Would need to pick one field as the grouping dimension, or add a sub-mode selector. |
| `main.js` search | Could search across multiple geo fields | Trivial to expand. |
| `lists.html` "International Voices" filter | `geoCountry !== 'United States'` or `geoRegion === 'International'` | Cleaner than regex; `geoRegion` = `"International"` is the direct equivalent. |
| `pack.html` `PRIMARY_GEOS` pills | `geoCity` + `geoState` → formatted string, or `geoCountry` | Requires deciding on the new display format and updating the hardcoded pill list. |

---

## 3. What needs more thought

**`pack.html` PRIMARY_GEOS pills** — this is the most complex. Today it does exact-string matching against `geography`. To switch, you'd need to either:
- Rebuild pills as `"City, State"` derived from `geoCity + geoState` (requires defining a canonical display format)
- Or replace with separate City / State / Country filter dimensions

The filter UI design question (flat pills vs. drill-down) needs to be answered first.

**`main.js` bubble chart geography mode** — currently groups creators by `geography` as a single flat dimension. With structured fields, the grouping dimension could be `geoState`, `geoCountry`, or `geoCity`. This needs a design decision about what the "By Geography" bubble view should show.

**`city-lab-dc.html` / `city-lab-dc2.html` `geoGroup()` function** — these pages use their own separate JSON files (`dmv-creators.json`, etc.) which have their own schema. These are NOT driven by `creators-data.json`. The geoGroup function is parsing those separate datasets. Cutover of `creators-data.json` doesn't affect these pages.

---

## 4. What breaks if `geography` is removed from the JSON today

Everything in `main.js` / `index.html` breaks immediately:
- Geography filter stops populating
- Geography filter stops working
- Bubble chart "By Geography" mode shows nothing
- Table geography column shows `-` for all rows
- Creator cards show no location
- URL state for geography filters breaks

`lists.html` "International Voices" list breaks (regex test returns false for all).

`pack.html` geo pills become non-functional (no matches).

`city-lab-dc.html` / `city-lab-dc2.html` / `city-lab-chicago.html` are **not affected** — they load separate JSON files.

**Bottom line:** Do not remove `geography` from `creators-data.json` until `main.js`, `pack.html`, and `lists.html` are all updated to use the structured fields. The parallel-field approach (both present simultaneously) is the safe transition path.

---

## Open question flagged

Ryan's reply (ryan_reply_mar16.md) says he'll likely drop `geography` from the JSON once structured fields are live and tested. The cutover session should update `main.js` (filter, table, bubble chart, search, URL state), `pack.html` (PRIMARY_GEOS pills and filter logic), and `lists.html` (International Voices filter) in one coordinated push.
