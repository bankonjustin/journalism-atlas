# Atlas JavaScript Architecture Audit
*Last updated: 2026-05-19*
*Session: Architecture migration + error handling restructure*

---

## Summary

Three bugs were found and fixed across two sessions, all the same class: code in `main.js`
written with assumptions about one page's DOM that silently failed or threw on other pages.
Two caused the catch block to display a fake "Error loading data" message that multiple users
reported. This session fixed the root structural cause: the monolithic `DOMContentLoaded`
handler in `main.js` was replaced with per-page inline scripts. `main.js` is now a function
library. Each page calls only what it needs, in the correct order.

---

## What Was Fixed This Session

| Fix | File(s) | Severity | Notes |
|-----|---------|----------|-------|
| Error handling in `loadCreatorsData()` narrowed to fetch/parse only | `main.js` | Critical | Rendering errors now surface as console errors, not fake "Error loading data" user messages |
| `packModalBackdrop` listener moved from parse-time global to per-page init scripts | `main.js`, `search.html`, `index-pre-homepage.html` | High | Was unguarded at end of file; now explicit in each page's init |
| `DOMContentLoaded` handler removed from `main.js`; per-page scripts added | `main.js`, `search.html`, `index-pre-homepage.html` | Structural | Eliminates entire class of page-specific DOM assumption bugs |
| `loadFiltersFromURL()` order corrected | `search.html`, `index-pre-homepage.html` | High | Now runs BEFORE `loadCreatorsData()` so URL params are set when `applyFilters()` fires on data resolve |
| `navSearch` input listener null-guarded | `main.js` | High | Belt-and-suspenders for any future page where header.js might not inject the nav |
| `setupReadMore()` null-guarded (prior session) | `main.js` | High | Was throwing on `search.html`, silently blocking `loadFiltersFromURL()` |
| `totalCreatorsCount` null-guarded (prior session) | `main.js` | Critical | Element only exists on `index-pre-homepage.html`; was throwing on `search.html` inside the try block |
| Hardcoded `471` count replaced with `—` (prior session) | `search.html` | Low | Stale count from earlier database size |

---

## Open Flags

| Finding | File | Severity | Recommendation |
|---------|------|----------|----------------|
| `#ceff00` used in D3 bubble chart color scale (line ~966) | `main.js` | Medium | Bubble chart renders on light background — `#ceff00` is acid green (dark-only per James's rules). Needs James review before Sep launch. |
| `#97d600` comment at line ~1287 says "acid green" — incorrect | `main.js` | Low | `#97d600` is lime green (light backgrounds). Comment is wrong. Fix comment when touching that area. |
| `ATLAS_VIZ_COLORS` — placeholder pending James sign-off | `main.js` | Medium | Visualization color assignments per topic category are not finalized. Flag for James before September launch. |
| `setupScrollBehavior()` function is dead code | `main.js` | Low | `header.js` already handles scroll behavior (`nav.classList.toggle('scrolled', window.scrollY > 10)`). The function in `main.js` is redundant and no longer called. Safe to delete when touching that area. |
| `setupReadMore()` only relevant to `index-pre-homepage.html` | `main.js` | Low | That page is a dev archive. If it's ever retired, `setupReadMore()` can be deleted from `main.js`. |

---

## Key Architecture Finding: Which Pages Load main.js

This was the most important discovery of the session. `main.js` is NOT a truly universal
shared file — it is only loaded by two pages:

| Page | Loads main.js | Notes |
|------|---------------|-------|
| `search.html` | ✓ | Primary database explorer page |
| `index-pre-homepage.html` | ✓ | Dev archive (pre-launch homepage). Not public-facing. |
| `index.html` | — | Homepage. Has its own inline JS. Does NOT load main.js. |
| `postcard.html` | — | Pack builder. Fully self-contained inline JS. Does NOT load main.js. |
| `city-lab-*.html` | — | Inline data + inline JS. Do NOT load main.js. |
| `partners/*.html` | — | Inline JS. Do NOT load main.js. |

**Implication for future pages:** Any new page that needs the database (creator profiles, beat
pages, for-brands page) must add its own per-page init script when it loads `main.js`. It must
NOT add init calls back into `main.js` itself.

---

## Per-Page Init Map

*Update this table whenever a new page is added or a page's init changes.*

| Page | `loadFiltersFromURL` | `loadCreatorsData` | `setupReadMore` | `packModal` listener | Order rule |
|------|---------------------|-------------------|----------------|---------------------|-----------|
| `search.html` | ✓ (1st) | ✓ (2nd) | — | ✓ | filters → data |
| `index-pre-homepage.html` | ✓ (2nd) | ✓ (3rd) | ✓ (1st) | ✓ | readMore → filters → data |

**Non-negotiable rules:**
- `loadFiltersFromURL()` ALWAYS before `loadCreatorsData()` on any page that uses both.
- New pages must NEVER add init calls back into `main.js`. Per-page inline script only.
- Pages that don't need the database should NOT call `loadCreatorsData()`.

---

## Initialization Execution Map (post-migration)

```
main.js loaded (parse-time, synchronous)
  → Global state vars initialized (allCreators, filteredCreators, currentView, etc.)
  → FilterStateManager class defined
  → filterState = new FilterStateManager()
  → window.addEventListener('resize', ...)   [stays in main.js — intentional]
  → navSearchInput null guard + input listener wired
  → All functions defined (loadCreatorsData, buildFilterOptions, renderCreators, etc.)
  → Comment: "packModalBackdrop click-to-close is wired in each page's per-page init script"

Per-page inline script fires DOMContentLoaded (search.html):
  → loadFiltersFromURL()     [sync — reads URL params, sets filterState, populates navSearch]
  → loadCreatorsData()       [async — fires fetch, returns immediately]
     → fetch resolves
     → allCreators = data
     → buildFilterOptions()
     → filterState.applyFilters()   [filter state already set by loadFiltersFromURL above]
     → loadingState hidden
  → packModalBackdrop listener wired
```

---

## Hardcoded Data Values

| Value | Location | Status | Action |
|-------|----------|--------|--------|
| `ORDERED_GROUPS` array | `main.js` ~line 8 | Intentional — manually maintained | Add `// MANUAL: update when taxonomy changes` comment |
| `LABEL_ABBREVIATIONS` dict | `main.js` ~line 34 | Intentional — manually maintained | Add `// MANUAL: update when taxonomy changes` comment |
| `—` placeholder in results count | `search.html` | Auto-replaced by JS on data load | Fine |
| D3 color scales (hardcoded hex values) | `main.js` | Provisional | Needs James's canonical `ATLAS_VIZ_COLORS` assignments before Sep launch |
| Platform colors in sunburst (~line 1283) | `main.js` | Intentional | These are platform-type colors (Newsletter=blue, Video=red etc.) — not topic colors |

---

## Scale Watchlist

*Not bugs today. Watch these as the database grows toward 10K creators.*

**`creators-data.json` payload:** Currently **652 KB** for 1,453 creators (~449 bytes/creator).
Projected sizes:
- 5,000 creators → ~2.2 MB
- 10,000 creators → ~4.4 MB

At ~2 MB on mobile/slow connections, initial load time becomes noticeable. Recommend benchmarking
load time on throttled connection before the 5K milestone. Consider gzip (Cloudflare enables this
automatically) which typically reduces JSON by 70–80% — so 4.4 MB uncompressed ≈ ~900 KB served.

**`applyFilters()` loop:** Iterates full `allCreators` on every filter change. 1,453 is instant.
At 10K, iterating 10K objects on every keypress with a 150ms debounce is borderline on low-end
mobile. Profile performance at 5K; consider Web Workers or memoization before 10K.

**`buildFilterOptions()` at scale:** Builds filter dropdowns from data. At 10K creators with
expanded geography coverage, the geography and topic filter panels could become unwieldy.
Recommend evaluating filter UI (search-within-filter, virtual scroll) at the 3K milestone.

**D3 visualizations at scale:** Bubble chart, sunburst, and treemap render from `filteredCreators`
with no upper bound on node count. Performance and legibility will degrade above ~500 visible
nodes. Add a node count cap or "too many results — narrow your filters" state before visualizations
hit that threshold.

**City lab inline data:** `city-lab-chicago.html` has 245+ creators inlined as JS constants.
This pattern works but HTML file size grows linearly. Recommended threshold: if any city lab
exceeds 500 creators, evaluate migrating to the same `fetch()` pattern as `search.html`.

---

## CSS Token Observations (spot-check only)

| Finding | Location | Rule | Status |
|---------|----------|------|--------|
| `#ceff00` in D3 color scale | `main.js` ~966 | Acid green = dark backgrounds only | **Violation** — bubble chart is on white background. Needs James review. |
| `#ceff00` in canvas drawing (pack stamps) | `main.js` ~2901–3003 | Acid green = dark backgrounds only | **Correct** — pack canvas has dark background |
| `#97d600` labeled "acid green" in comment | `main.js` ~1287 | Comment error only; value is correct | Fix comment (`#97d600` is lime green, light-bg only) |

---

## Architecture Decision Log

*Append an entry whenever a significant architectural decision is made.*

**2026-05-19 — DOMContentLoaded migrated from `main.js` to per-page inline scripts.**
Rationale: eliminates entire class of page-specific DOM assumption bugs. Three bugs in two
sessions were all the same class; structural fix was the right call over continued null-guard
patching.
Constraint: all new pages that load `main.js` must add their own per-page init script —
never add init calls back into `main.js`.

**2026-05-19 — Error handling in `loadCreatorsData()` narrowed to fetch/parse only.**
Rationale: the broad try/catch was masking rendering bugs as fake "Error loading data" messages
that multiple users reported. Real fetch failures still show the error; rendering bugs now
surface as console errors.

---

## Production Test Checklist

Test on the **live site** after deploy. The local dev server strips query params on redirect —
`?search=taylor` testing locally is unreliable.

| URL | Expected result |
|-----|-----------------|
| `journalismatlas.com/search` | Loads, shows 1453 creators, no error message |
| `journalismatlas.com/search?search=taylor` | Shows 2 results, no error message |
| `journalismatlas.com/search?platform=Newsletter+-+Substack` | Filtered results, no error |
| `journalismatlas.com` | Homepage loads, hero works, cluster drawer opens |
| `journalismatlas.com/postcard` | Pack builder loads, creator picker populates |
| Browser back button from `search?search=taylor` | Returns to previous state cleanly |
