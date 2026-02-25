# Handoff: Mobile Drawer — Completed Implementation
**Last updated:** Feb 2026 (third session — see also HANDOFF-pack.md)
**Project:** Independent Journalism Atlas
**Location:** `/Users/justinbank/Documents/Code/Atlas.prototype/`

---

## Status: DONE

The bottom drawer is fully implemented in `index.html`. The feature is complete, bug-fixed, and tested. This document describes what was built and the current architecture so the next session can orient quickly without re-reading the code.

---

## What the Project Is

A single-page visualization atlas of ~1,001 independent journalism creators.

**Key files:**
- `index.html` — The only file that matters now. 5,800 lines. Contains all HTML, CSS, and JS inline. All drawer/pack work lives here.
- `mobile.html` — The older standalone mobile prototype the drawer was ported *from*. Keep as reference. Not served in production.
- `mobile/` — Even older modular mobile prototype (split CSS/JS). Effectively archived. Don't touch.
- `assets/data/creators-data.json` — 1,001 creators: `name`, `channel`, `link`, `platform`, `topic`, `group`, `geography`
- `atlas-portal/` — Separate postcard generator tool. Untouched, leave alone.

**Data hierarchy:**
- 9 **Groups** (e.g. "Power & Politics") — top-level meaningful categories, outer ring of wheel
- ~13 **Platforms** (e.g. "Video - YouTube") — inner ring of wheel
- 100+ **Topics** — too granular for wheel, used inside drawer for sub-grouping creator lists

---

## What Was Built

### 1. Three-State Bottom Drawer (≤768px only)

Activated when the user taps a sunburst wheel segment on a mobile/narrow viewport. Three height states:

| State | Height | Backdrop | Behaviour |
|-------|--------|----------|-----------|
| `full` | 72vh | Visible + opaque (tap to peek) | Full creator list, scrollable |
| `peek` | 28vh | Transparent, pointer-events:none | Partial list visible, wheel tappable above |
| `pill` | 52px | Transparent, pointer-events:none | Collapsed tab with "↑ tap to expand" hint |
| `closed` | off-screen | Hidden | Default / after back past pill |

**State machine:** `_drawerState` variable + `_setDrawerState(state)` function. Located in the main script block around line 4907.

**Key state transitions:**
- Wheel segment tap → `full` (via 800ms `_drawerOpenTimer` setTimeout — cancellable on rapid re-tap)
- Drag handle down → `full → peek → pill` based on velocity thresholds
- Drag handle up → `peek/pill → full`
- Content scroll to top + pull down → `full → peek`
- Close button (×) → steps down one state each tap
- Pill/handle tap → back to `full`
- Backdrop tap → `full → peek`
- Back button → steps down: `full → peek → pill → closed`, then normal navigation

**History management:** `pushState` is called on each state change so the back button navigates the drawer states before leaving the page. `_fromPopstate` flag prevents double-push during popstate handling.

### 2. Drag Gesture System

Handle element (`#atlasDrawerHandle`) has `touch-action: none` CSS, non-passive `touchmove` with `e.preventDefault()` to block iOS page scroll during drag. Live-drag animates height in both directions (up and down). Snap thresholds on release:

- From `full`: >160px down → `pill`, >60px down → `peek`, else snap back
- From `peek`: >60px down → `pill`, <-60px up → `full`, else snap back
- From `pill`: <-40px up → `full`, else snap back

### 3. Touch Containment (prevents page bleed on iOS)

Drawer content (`#atlasDrawerContent`) has:
- `overscroll-behavior: contain` CSS
- Non-passive `touchmove` listener that calls `preventDefault()` at scroll boundaries
- At top + pulling down: collapses drawer to `peek`
- At bottom: blocks scroll bleed
- Mid-list: `stopPropagation()` to contain

### 4. Pack / Starter Pack System

**Trigger:** "✦ Create a Pack" button in the controls bar. Hidden by default, springs in with animation when any filter is active.

**Selection flow:**
1. Filters active → Pack button appears in controls bar
2. Drawer opens (mobile) → creator cards become selectable (tap to toggle, green checkmark)
3. Drawer shows count footer with "Create a Pack" CTA
4. Desktop: modal pre-populates with first 12 of `filteredCreators`
5. Pack modal: name input, editable preview list (clickable names → creator channels), canvas postcard preview

**Canvas postcard** (`renderPackCanvas()`):
- 1080×1080px dark background (#0d0d0d) with film grain
- Acid green rules and labels
- Large watermark stamp (10% opacity center) + small seal (bottom right)
- Creator list: name in white, channel/platform in muted green, max 8 shown + "and N more"
- Stamp image: `assets/images/logos/Journalism_Atlas_logo_acid_green_distressed (4).png`

**Share flow** (`packShare()`):
- Best path: `navigator.share()` with image file + URL + named creator list in text
- Fallback: simultaneous download + clipboard copy
- Share text dynamically lists first 3 creator names: `"Adam Cole, Alicia Kennedy, Casey Lewis + 4 more — curated on the Independent Journalism Atlas"`

### 5. Creator Card Links (XSS-safe)

Cards use `data-link="..."` attribute (not inline onclick) with a single delegated click listener on the content div. Links open with `noopener`. Pack modal preview list shows creator names as `<a>` tags to their channels.

---

## Architecture: Key Variables & Functions

All in the main `<script>` block (~line 2640), globally scoped:

```
_drawerState          'closed'|'full'|'peek'|'pill'
_fromPopstate         bool — skip pushState during popstate handling
_drawerOpenTimer      setTimeout ref — cleared on rapid re-tap (race condition fix)
_atlasDrawerData      { platform, creators, specificGroup } — current drawer content

_setDrawerState(state)         Core state machine. Updates classes + history.
atlasOpenDrawer(p, c, g)       Opens/updates drawer. Guards: innerWidth, empty creators.
atlasCloseDrawer()             Removes all classes, resets state.
atlasExpandTopic(key)          Expands "Show more" — preserves scroll position.
_atlasDrawerCard(creator)      Returns card HTML with data-link (no inline onclick).
_atlasTopicKey(topic)          Sanitises topic name for use as data attribute key.
```

Pack functions (second `<script>` block, ~line 5300):
```
_packSelectedCreators[]        Currently selected creators for pack
_packCurrentDrawerCreators[]   All creators in current drawer view
_packStampImg                  Preloaded stamp Image object (null if load failed)

_packMaybeEnableSelection()    Called after drawer renders — enables selection if filters active
_packEnableDrawerSelection()   Adds selectable class + click handlers to all drawer cards
_packUpdateDrawerCount()       Updates footer count + enables/disables CTA
openPackModal()                Opens modal, pre-populates on desktop, renders canvas
renderPackCanvas()             Draws full 1080×1080 postcard
packShare()                    Exports canvas → Web Share API or download+clipboard fallback
```

Gesture IIFE (second `<script>` block, ~line 5125):
- Close button, handle click, backdrop click, drag start/move/end, content scroll containment, popstate handler

---

## CSS Class Scoping

All drawer CSS is prefixed `.atlas-drawer-*` and `.atlas-bottom-drawer` to avoid collision with existing `.creator-card`, `.creator-name` etc. in the desktop grid styles. Never remove the prefix.

Drawer is `display: none` by default, `display: flex` only inside `@media (max-width: 768px)`. Visibility is controlled by `transform: translateY(100%)` → `translateY(0)` via the `.visible` class, not by toggling display.

---

## Known Good / Don't Touch

- D3 sunburst: Platform (inner) → Group (outer), 18% innerRadiusOffset, padAngle — solid, don't touch
- `getPlatformColor()`, group color mapping — working correctly
- `filterState` object and all filter wiring — do not restructure
- `filteredCreators` (not `creatorsData`) is what the drawer uses — correct, filter-aware
- URL sync: `updateURL()` / `loadFiltersFromURL()` — already working, drawer doesn't need to touch it
- `atlasExpandTopic` is on `window` because it's called from inline `onclick` in generated HTML

---

## What's Not Built Yet (future sessions)

- **Creator profile cards** — tap a creator in the drawer to see a full profile modal. Needs richer data.
- **Desktop side panel** — deferred. Discussed: right-side slide-in panel at ~400px instead of inline table. User is open to it but "mobile drawer first."
- **Multi-segment union view** — tap a new segment while drawer is open → show combined creator list. Deferred as v2 (drawer peek/pill first).
- **Filter access from peek state** — a filter icon in the exposed peek strip so users can adjust filters without closing the drawer.
- **Starter pack backend** — current packs are ephemeral (image + URL share only). If packs need to be saveable/discoverable, needs Supabase or similar. URL-encoded selection is already implemented on `pack.html` — see `HANDOFF-pack.md`.
- **Creator data enrichment** — subscriber counts, founding year, price (free/paid), publication frequency. Most useful for sorting/filtering.

---

## Bugs Fixed This Session (for the record)

1. Drag threshold unreachable branch (`velocity > 200` after `velocity > 80`)
2. `passive: true` + `stopPropagation` — iOS ignores both; switched to non-passive with `preventDefault`
3. `history.state` null on page load caused first drawer open to never push state
4. Popstate double-push — `_setDrawerState` was pushing during popstate handling; fixed with `_fromPopstate` flag
5. Race condition — rapid segment taps could mix drawer content; fixed with `_drawerOpenTimer` + `clearTimeout`
6. XSS in creator card links — moved from inline `onclick` to `data-link` + delegated listener
7. Canvas context null crash — `getContext('2d')` return not guarded
8. Scroll position lost on topic expand — save/restore `scrollTop` around `innerHTML` assignment
9. Pack filename with special chars — slug now strips non-alphanumeric
10. `atlasOpenDrawer` title null dereference — guarded
11. Empty creators array — early return added
12. `_packMaybeEnableSelection` accessed `filterState` without guard
13. Close button click bubbling — added `e.stopPropagation()`
