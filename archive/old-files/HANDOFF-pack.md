# Handoff: pack.html — Postcard Generator
**Last updated:** Feb 2026
**Project:** Independent Journalism Atlas
**File:** `/Users/justinbank/Documents/Code/Atlas.prototype/pack.html`

---

## Status: WORKING — active iteration

`pack.html` is a standalone postcard generator page. It lives alongside `index.html` but is fully self-contained — no D3, no wheel, no drawer. Purpose: narrative-first entry point where users browse the creator database, pick up to 12 creators, generate a 1080×1080 postcard image, and share it.

---

## Page Structure (top to bottom)

```
Fixed nav          ← logo + "← Explore the Atlas" link only (intentionally minimal)
#refBanner         ← slim acid-green banner (hidden by default, slides in on ?ref=pack)
.hero              ← full-bleed dark hero, ambient drifting names, headline, green CTA
.how-strip         ← 3-step "how it works" strip
#workspace         ← two-column layout: browser (left) + pack panel (right)
  .browser-col     ← search, group pills, platform pills, paginated creator grid
  .pack-col        ← canvas preview, pack name input, selected list, action buttons
#mobilePackBar     ← sticky bottom bar (mobile only)
#mobileModal       ← modal sheet with canvas + share button (mobile only)
```

---

## Data

Loads from `assets/data/creators-data.json` (same file as index.html).

Each creator object: `{ name, channel, link, platform, topic, group, geography }`

State variables:
```javascript
allCreators[]       // full dataset after fetch
filteredCreators[]  // post-filter slice
selectedCreators[]  // up to 12 chosen creators
activeGroups        // Set of active group pill filters
activePlatforms     // Set of active platform pill filters
searchQuery         // live search string
visibleCount        // pagination cursor (PAGE_SIZE = 48)
stampImg            // preloaded Image obj for canvas watermark (null if load fails)
```

---

## Key Functions

### Filters & Grid
```
buildFilters()          Renders group + platform pill buttons
toggleGroup(g, btn)     Adds/removes group from activeGroups, calls applyFilters()
togglePlatform(p, btn)  Adds/removes platform from activePlatforms, calls applyFilters()
applyFilters()          Rebuilds filteredCreators, resets pagination, calls renderGrid()
renderGrid()            Renders paginated creator cards — marks selected/maxed state
```

### Selection
```
toggleCreator(c)        Add/remove creator from selectedCreators (cap: MAX_PACK = 12)
removeCreator(name)     Remove by name (called from pack panel × button)
```

### Pack Panel
```
renderPackPanel()       Updates count, enables/disables buttons, renders selected list
                        Selected list shows creator name as <a> link → channel if available
getPackName(which)      Returns name input value ('desktop'|'mobile'), fallback 'My Atlas Pack'
```

### Canvas
```
renderCanvas(which)     Draws 1080×1080 postcard on 'desktop' or 'mobile' canvas
                        Called on: selection change, name input, stamp load, URL restore
```

Canvas spec:
- Background: `#0d0d0d` with film grain overlay
- Acid green (`#ceff00`) horizontal rules + "INDEPENDENT JOURNALISM ATLAS" label
- Creator list: name in white (700 weight), channel in muted green, max 8 shown + "and N more"
- Watermark stamp centered at 10% opacity, small seal bottom-right
- Stamp image: `assets/images/logos/Journalism_Atlas_logo_acid_green_distressed (4).png`

### Share / Export
```
copyImage()         Desktop primary — renders export canvas, uses ClipboardItem API
                    Safari: ClipboardItem({ 'image/png': blobPromise }) — must be Promise
                    Falls back to _triggerDownload() if clipboard blocked (non-HTTPS, Firefox)
copyLink()          Desktop secondary — writes _shareUrl() to clipboard
doShare('mobile')   Mobile — Web Share API with file attachment; falls back to download + clipboard
_triggerDownload()  Creates <a> + revokeObjectURL — used as fallback from copyImage()
_shareUrl()         Builds clean share URL (see URL Encoding section below)
_resetDesktopBtn()  Handles button label swap + 2s reset timer
_resetMobileBtn()   Same for mobile share button
```

### Desktop Actions (current UI — as of Liz/Ryan feedback)
Two equal-weight buttons in `.pack-action-row`:
- **⎘ Copy image** (`#packCopyImgDesktop`) — primary, acid green fill
- **⌁ Copy link** (`#packCopyDesktop`) — secondary, ghost outline

Both disabled when `selectedCreators.length === 0`. "Save file" was removed.

---

## URL Share System — Critical Details

This is the most recently iterated area. Get this right before touching it.

### Encoding (in `_shareUrl()`)
```javascript
// Always builds from bare pathname — never inherits stale ?creators= from current URL
const url = new URL(window.location.pathname, window.location.origin);
url.searchParams.set('ref', 'pack');
// Each name individually encodeURIComponent'd, joined with comma
url.searchParams.set('creators', selectedCreators.map(c => encodeURIComponent(c.name)).join(','));
// Pack name only if user typed one (not the default fallback)
if (packName && packName !== 'My Atlas Pack') url.searchParams.set('name', packName);
```

**Why comma not pipe `|`:** Pipes get mangled by iMessage, Gmail, Slack, and some link shorteners. Commas survive reliably.

**Why `pathname` not `href`:** If the sharer was themselves a recipient (landed on `?creators=...`), using `href` would inherit their incoming params and potentially corrupt the outgoing URL.

**Why `encodeURIComponent` per name:** `URLSearchParams.set()` encodes the whole value but some share sheets re-encode the full URL (double-encoding). Encoding each name individually + decoding on arrival handles both cases.

### Decoding (in `_restoreFromUrl()`)
```javascript
const raw = params.get('creators');  // URLSearchParams already does one decode pass
const names = raw.split(',').map(n => {
    try { return decodeURIComponent(n.trim()); } catch { return n.trim(); }
}).filter(Boolean);

// Lookup with double-decode fallback
let creator = byName.get(name);
if (!creator) {
    try { creator = byName.get(decodeURIComponent(name)); } catch {}
}
```

Two decode passes because: `URLSearchParams.get()` does pass 1, but if the URL was double-encoded in transit, the name is still encoded after pass 1. The fallback handles this silently.

### What gets restored
1. **Selected creators** — pre-selected in grid + pack panel + canvas rendered
2. **Pack name** — pre-filled in `#packNameDesktop` input
3. **Missing creator notice** — if any names don't match current dataset, subtle muted line appended to pack list: *"N creators from this pack no longer appear in the Atlas."*
4. **Scroll** — `setTimeout(400)` smooth scroll to `#workspace` so recipient lands on the pack

`_restoreFromUrl()` is called at the end of the data fetch `.then()` block — data is guaranteed loaded before any name lookup.

---

## Referral Banner (`#refBanner`)

Shown when URL contains `?ref=pack`. Lives at top of page, fixed position, slides in 600ms after load.

Behaviour:
- Auto-dismisses after 7s
- Dismisses on scroll >80px
- If `?creators=` also present: banner text swaps to *"Someone curated a reading list for you. ↓ Scroll to see it."*
- Hero copy also swaps on referral landing
- `dismissRefBanner()` handles cleanup

---

## Ambient Hero Animation

`.ambient-name` elements are injected by `buildAmbient()` after data loads. Each picks a random creator name, random position, random drift direction via CSS `@keyframes drift-*`. Pure CSS animation, no JS after initial build. Don't call `buildAmbient()` more than once.

---

## Mobile Flow

- Grid + browser: same as desktop
- Action: sticky `#mobilePackBar` at bottom (count + "✦ Create Pack" button)
- On tap: `#mobileModal` slides up (separate canvas `#mobilePackCanvas`)
- Share: `doShare('mobile')` → Web Share API with file + URL + text
- Mobile canvas renders independently from desktop canvas

---

## Known Issues / Things to Watch

- **Mobile pack name not synced to desktop name input** — `packNameMobile` and `packNameDesktop` are separate inputs. If user types a name on mobile modal, it doesn't populate the desktop input and vice versa. Currently fine since the two canvases render from their respective `getPackName()` calls.
- **Missing creator notice gets wiped** — the notice is appended to `#packList` after `renderPackPanel()`, but if the recipient then toggles a creator, `renderPackPanel()` rebuilds `#packList` innerHTML and the notice disappears. This is acceptable — it's only relevant on first load.
- **`?creators=` without `?ref=pack`** — URL still restores the pack fine (no banner, but pre-selection works). Edge case: someone manually constructs a URL. Not a problem.
- **Canvas stamp timing** — stamp preloads in an IIFE. If stamp loads after `_restoreFromUrl()` triggers `renderCanvas()`, the stamp `.onload` fires another `renderCanvas('desktop')`. Results in two renders on arrival — minor flicker, not a bug.

---

## What's Not Built Yet

- **Mobile pack name → shared URL** — `_shareUrl()` reads `getPackName('desktop')`. If user names the pack via the mobile modal input (`packNameMobile`), the name won't be in the share URL unless we unify the inputs or read both.
- **Re-share from recipient** — if a recipient modifies the pack and re-shares via mobile `doShare()`, the share text is correct but the URL should ideally update to reflect their new selection. Currently it does (since `_shareUrl()` always reads current `selectedCreators`) — but the mobile flow doesn't call `_shareUrl()` explicitly; it passes `shareUrl` computed at share time. Worth verifying.
- **Pack persistence** — packs are ephemeral, URL-only. No saved packs, no user accounts. If persistence is needed → Supabase with a short pack ID in the URL (`?pack=abc123`) would be cleaner than encoding all names.
- **OG / social preview image** — shared URLs don't have dynamic `og:image`. A server-side render of the canvas (or a static default image) would make link previews richer in iMessage/Slack/Twitter.
- **Analytics** — no tracking on which packs get shared, which creators appear most, how many recipients convert to sharers.

---

## Bugs Fixed This Session

1. **Pipe `|` separator mangled in transit** — switched to comma, each name individually `encodeURIComponent`'d
2. **Stale URL inherited on re-share** — `_shareUrl()` now builds from `window.location.pathname` not `window.location.href`
3. **Double-encoding from share sheets** — `_restoreFromUrl()` does a second `decodeURIComponent` fallback pass
4. **Missing creator silent failure** — names not found in dataset now surface a subtle notice in the pack list rather than silently shortening the pack
5. **Pack name not preserved in share URL** — `?name=` param added to `_shareUrl()`, restored in `_restoreFromUrl()`
6. **"Save file" removed** — desktop UX simplified to two buttons (copy image + copy link) per Liz/Ryan feedback
7. **`advisory.html` bullet mojibake** — `â†'` was a corrupted `→` in `.board-section li:before { content }`. Fixed.
