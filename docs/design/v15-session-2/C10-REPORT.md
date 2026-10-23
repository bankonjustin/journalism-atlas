# C10 report: mobile header overflow

*Oct 23, 2026. C10a fixes phones; C10b (hamburger below 1280px) is marked "review before push". Status when written: Justin pushed Session 2 and C10a (through `62bbcb6`); C10b (`f17b9af`) and this report are the only local commits.*

| Commit | What |
|---|---|
| `31f0ff9` | **C10a**: header fits at 320–640px; Search moves into the mobile menu |
| `f17b9af` | **C10b**: hamburger takes over below 1280px. **Review before push** |

(`62bbcb6 "watershed"` between them is Justin's, not part of this work.)

## Step 0

**State.** Clean tree, `main` 14 ahead of `origin/main`, last commit `b403a43`. No git hooks and no push config; nothing auto-pushes.

**`_headers`.** The `/partners/_shell.html` and `/partners/_shell` `X-Robots-Tag: noindex` rules are present. The file is valid Cloudflare syntax (path line, indented header lines, no duplicates). Nothing to restore.

### Width budget at phone widths (contact.html, identical on every page that uses the shared header)

| Element | Width | Notes |
|---|---|---|
| Container padding | 16 + 16 | `.top-nav` ≤768px |
| Logo (`.nav-logo img`, 32px high) | 238 | 1000×134.5 viewBox; no mobile variant in v15 |
| Gap logo → search | 12 | |
| Search field | 192 | input, intrinsic minimum; 35px high |
| Gap field → button | 6 | |
| Search button (`.nav-search-btn`) | 93 | 44px high, 20px side padding |
| Hamburger | 44 | 44×44 with 8px padding |
| **Needed** | **585 + 32 = 617** | |

| Viewport | Container (vw − 32) | Needed | Short by | Page scrollWidth before |
|---|---|---|---|---|
| 320 | 288 | 585 | 297 | 601 |
| 360 | 328 | 585 | 257 | 601 |
| 375 | 343 | 585 | 242 | 601 |
| 390 | 358 | 585 | 227 | 601 |
| 414 | 382 | 585 | 203 | 601 |
| 768 | 736 | 585 | fits | 768 |

The hamburger sat at x = 557–601, outside every phone viewport. The header fits only from about 617px up.

**Second finding:** on 18 pages (`for-brands`, 13 partner pages, `latin-america-lab`, `city-lab-dc-v3`, the smartnews preview) the logo was not overflowing because it had been **crushed to ~11px wide** (page CSS lets it shrink), so the header looked "fitted" but the logo was a dash. Before the fix **all 38 pages with the shared header** had either an off-screen hamburger or a crushed logo; after, none do (checked at 320 and 390).

### Breakpoints (`header.css`, `header.js`) before C10

| Query | Where | Does |
|---|---|---|
| `max-width: 768px` | `header.css` | Hides `.nav-links`; shows hamburger and `.mobile-menu`; header padding 12/16px; logo 32px (28px scrolled); search font 14px; footer grid and padding |
| `max-width: 480px` | `header.css` | Footer single column |
| none | `header.js` | no media queries, no `matchMedia`; before this work |

The mobile menu took over from the desktop nav at 768px.

## Overflow list at 390px (before)

20 of 41 public pages scrolled sideways.

**Header causes (fixed by C10a):** `advisory`, `city-lab-chicago`, `co-ops`, `contact`, `how-we-did-this`, `lists`, `partners/index`, `partners/nj-lab`, `partners/njlab`, `pulse`, `research`, `submit-thanks`, `submit`, `updates`, `who-we-are`, `wire` (all 601px); `search` (435px); `about-this-project`, `bluesky-creator-intelligence`, `index` (601px of header, hidden behind a larger non-header cause below). `mobile.html` clips its hamburger at 601px but hides the overflow.

**Other causes (reported only, not touched):**

| Page | Width | Widest element | Note |
|---|---|---|---|
| `index.html` | 775 | `div.stat-cell` (right edge 775) | Stats strip. **On a real phone the browser zooms the whole homepage out to fit 775px**; the fixed mobile menu then appears off to the right. Needs its own fix. |
| `bluesky-creator-intelligence.html` | 708 | `div.stat-cell` | Same pattern |
| `about-this-project.html` | 447 | an unclassed `<a>` 427px wide | A long link |
| `for-brands.html` (320 only) | 367 | `div.gallery-offer-col` | |
| `partners/njlab.html` (320, 360) | 368 | `a.cta-btn.cta-primary` | nj-lab, pending F2 |
| `teamdmv/index.html` (320 only) | 324 | `a.feed-card` | no shared header |
| `preview/smartnews-d029dc36` (320 only) | 341 | `div.body` | |

Other observations, not fixed: partner pages show a 72px grey band above the header; `mobile.html` has its own header over the shared one.

## Fix chosen (C10a)

**Option used: 2, Search moves into the mobile menu, at ≤640px.**

- **Option 1 (icon button) doesn't fit.** Logo 238 + 12 + search icon 44 + hamburger 44 = 338px. The container is 288px at 320 and 328 at 360; it only fits from 370px up.
- **Option 3 (tighter padding and gaps) doesn't close the gap.** Even with 8px side padding (the `sm` step), 320px gives 304px against 338px.
- **Option 4 (smaller logo) is not allowed.** v15's Logo Usage has no mobile size or variant, and the logo is already 32px high at ≤768 (238px wide).

How it works:

- `header.js` moves the existing `.nav-search-container` node into `#mobileMenu` (above the links) at ≤640px and back above 640px. Ids and handlers are unchanged, so `main.js` on the search page and the Enter/click navigation behave as before.
- `header.css`, new `max-width: 640px` query: the logo never shrinks; in the menu the container gets padding, a divider and full width, and the field is 44px high.
- Order logo → hamburger at phone widths; 641–1279px keeps logo → search → hamburger.
- Search button wording is unchanged ("Search"). The field gets an `aria-label` ("Search creators, topics, places"); its placeholder is the same.
- Also in this commit: the closed menu is `visibility: hidden` (flips after the slide-out, immediately on open). Reason: with the search field now inside it, Tab on a phone would otherwise land on an off-screen input. It also removes a 1–2 grey-level shadow that leaked into the right edge at 641–768px.
- The menu's open/close behaviour and Session 2 states are untouched.

## Verification (C10a)

| Check | Result |
|---|---|
| Header-caused overflow at 320, 360, 375, 390, 414, 768 | gone on every public page (`scrollWidth` = viewport); only the non-header pages above remain |
| Logo and hamburger, 38 pages at 320 and 390 | logo 238px wide and hamburger inside the viewport on all 38 (before: 0 of 38) |
| Touch (Playwright touch emulation, 390) on `index`, `pulse`, `research`, `partners/ahp` | hamburger is 44×44 and fully on-screen; tap opens the menu; the first three items are inside the viewport and 58px high; tapping "For Brands" navigates to `/for-brands.html`; the close button and the overlay both close it |
| Search from the menu (same four pages) | type "climate" + tap Search → `/search?search=climate`, same as before |
| `search.html` at 390 | search box in the menu; `scrollWidth` 390 |
| Resize 700 → 390 → 1000 | box moves into the menu and back; header at 700px keeps the search |
| Keyboard (390) | Tab: logo → hamburger → page content; Enter on the hamburger opens the menu; the menu's search field and button show the 2px Dark Olive focus ring; Escape closes |
| Desktop pixel guard, header strip, 6 pages (`index`, `pulse`, `research`, `contact`, `for-brands`, `partners/ahp`) at 1280 and 1440 vs the pre-C10 tree | **identical, 12 of 12** |
| 900 and 1100px (before C10b) | identical |
| 768px | one difference: a 4px strip at the right edge, 1–2 grey levels, which is the closed menu's shadow no longer leaking. Intended |

Screenshots (gitignored): `screenshots/c10/c10_phone_sheet.png` (320 and 390, `index`, `pulse`, `partners/ahp`, before | after), `ahp_sheet.png`, and `desk_*` / `mid_*` pairs.

## C10b: mid-width desktop overflow (replaced; **review before push**)

The first version (`f17b9af`, hamburger at 1279px) was dropped before pushing and replaced with this one commit.

**Measured.** With 40px gaps the desktop nav needs a 1246px container and fits from exactly 1280px; from 769 to 1279px it ran past the container. With v15's `lg` 24px gap (Header Nav Spacing: "if cramped, fall back to lg") the links take 517px instead of 581px, and the nav **fits down to a 1215px viewport** (links end at 1183, container right edge 1183; at 1214px it overflows by 0.1px).

**Change** (`header.css`):
- `max-width: 1279px`: `.nav-links { gap: 1.5rem }`
- `max-width: 1214px`: hide `.nav-links`, show the hamburger and `.mobile-menu` (the three rules moved up from the 768px query; everything else in that query stays at 768px)

**Final breakpoint: the hamburger takes over at 1214px and below.** The desktop nav shows from 1215px up; 1215–1279px with 24px gaps, 1280px and up as before.

| Viewport | Result |
|---|---|
| 900, 1024, 1100, 1190 | logo + search + hamburger, no overflow (before: nav clipped at "Research & W…", "Submit", "Partne…") |
| 1214 | hamburger |
| 1215, 1250, 1279 | desktop nav, 24px gaps, fits exactly at 1215, no overflow |
| 1280, 1366, 1440 | desktop nav, **pixel-identical to `origin/main`**: header strip on `index`, `pulse`, `research`, `contact`, `for-brands`, `partners/ahp`, 18 of 18 |

Screenshots (gitignored): `screenshots/c10/c10b2_sheet.png` (1024, 1100, 1190, 1250, 1280, 1366; before above, after below).

Review question: viewports 769–1214px now use the hamburger (small laptops at 1024–1200, landscape tablets). That is as narrow a range as the spec's 24px gap allows without making the search field smaller.

## Non-header overflow fixes (separate commits)

| Page | Cause | Fix | Result |
|---|---|---|---|
| `index.html` (`905ac98`) | stats strip: five columns need 775px | below 800px, two columns with the fifth cell across the bottom | strip fits; 800px and wider identical |
| `bluesky-creator-intelligence.html` (`7f3da41`) | same stats strip, 708px | below 768px, same two-column layout | strip fits; the page still overflows (below) |
| `about-this-project.html` (`64fd970`) | **an image, not a text link**: the Project Oasis logo is 427px wide at 36px high | `max-width: 100%` on the logo row (the `overflow-wrap` fix would not have helped) | 320–1440px fit; desktop identical |
| `index.html` (`6151a43`) | two more causes behind the strip: the database cards (3 columns) and my own `white-space: nowrap` on "Open full Pulse feed →" from C6 | cards stack below 600px; the link may wrap at 480px and below | **homepage fits at 320, 360, 375, 390, 414, 600, 768, 1024, 1440** |
| partner pages (`partners:` commit) | grey band: `body { padding-top: 72px }` | removed on 13 pages | header at the top of the page; hero directly below |

The 800px, 1440px strip captures and the about logo row are pixel-identical to `origin/main`; the 390px captures are in `screenshots/c10/strips390_sheet.png` (before | after).

**Grey band diagnosis.** The partner pages kept `padding-top: 72px` on `body` from when their nav was `position: fixed`. The shared header is `position: sticky` and in flow, so the padding left a 72px empty strip above it. One declaration, partner pages only. Not changed: `nj-lab.html` and `njlab.html` (same declaration, pending F2).

## Still overflowing for non-header reasons (reported, not fixed)

| Page | Width | Cause |
|---|---|---|
| `bluesky-creator-intelligence.html` | 705px at 320–600px | no mobile layout: hero is `1fr 440px`, header row and section meta, the "Request a brief" button. Needs a real mobile pass, not a one-line fix |
| `for-brands.html` (320px only) | 367px | `div.gallery-offer-col` |
| `partners/njlab.html` (320 and 360px) | 368px | `a.cta-btn.cta-primary` (nj-lab, F2) |
| `teamdmv/index.html` (320px only) | 324px | `a.feed-card` (left alone) |
| `preview/smartnews-d029dc36/index.html` (320px only) | 341px | `div.body` (left alone) |

## Done when

- C10a committed; header overflow gone at 320–768; hamburger and menu work by touch and keyboard; desktop 1280+ identical. ✔
- C10b (replacement) committed and marked. ✔
- C10b not pushed (held for review). `git status` clean. ✔
