# Atlas Design Tokens — v13
*Canonical design reference — committed to repo as source of truth for implementation*

*Last updated: October 2026*
*Previous version: v12 (October 2026)*
*Owner: James (james@happicamp.com)*

> **How this file works:** This is the single source of truth for all visual decisions. When Justin implements design changes with Claude Code, he references this document. If it's not here, it doesn't get implemented. If it changes here, it changes everywhere.

### What changed in v13
- **Greens on light vs. dark surfaces.** Acid Green and Lime Green both fail the 3:1 UI minimum on light surfaces (1.2:1 and 1.8:1 on white). They're never used as text, icons or thin strokes on light surfaces — only as a fill, with black or step-6 text on top. On dark surfaces they're used freely within their existing roles. See Greens by Surface.
- **Dark Olive `#5d7400` returns to the UI in one role:** the green for text, icons and thin strokes on light surfaces (5.3:1 on white, 4.6:1 on the page background). Everywhere else it stays a design-element color, as in v12.
- **Focus ring follows the surface.** Lime Green on dark surfaces; Dark Olive on light surfaces.
- **Site header: black is the default and the priority.** White is available when a page needs it.
- **Retired-gray mapping clarified** for `#bdbdbd`, which v11 used as both text and border.
- **Tier 2 contrast figures** now show both scales (Neutral / Cool).
- **Unchanged from v12:** every other value — monotones, brand secondary, `ATLAS_VIZ_COLORS`, typography, spacing, layout, icons and logos.

*v13 replaces v12 in full. v12's changes (new monotone scales, five-tier structure, `#ffaa00`, black-or-white header, white header logo) are recorded in the decisions log.*

---

## Color Palette

**Brand colors express; data colors encode.** Every color belongs to exactly one tier, and each tier has one job.

| Tier | Job | Where it's used |
|---|---|---|
| 1. Core brand | Identity | CTAs, active and hover states; brand marks |
| 2. Monotones | Structure | UI, text, surfaces, borders |
| 3. Brand secondary | Expression | Decks, social, Pulse and editorial graphics, campaigns, print |
| 4. Data categories | Encoding | Anything that represents a taxonomy category: charts, category tags, labels |
| 5. System | Feedback | Errors, focus, dark-mode display accent |

**Rules across tiers**
- Don't mix brand secondary and data-category colors in one composition.
- Shared hexes are allowed only when deliberate and documented here. Avoid near-duplicates.
- New data categories draw from the brand secondary palette first, where contrast allows.
- Editorial annotations (e.g. a "HIRED" badge) use monotones. System feedback uses Tier 5. Never conflate the two.

### Tier 1 — Core Brand

| Name | Hex | sRGB | Use |
|------|-----|------|-----|
| Acid Green | `#ceff00` | 206, 255, 0 | CTAs and active states only — one per screen composition maximum; never a success/go signal |
| Lime Green | `#97d600` | 151, 214, 0 | Hover states only (also the focus ring, Tier 5) |
| Dark Olive | `#5d7400` | 93, 116, 0 | **In UI, one role only (v13):** the green for text, icons and thin strokes on light surfaces — e.g. an active nav item, selected icon or link-style CTA on white. Never a fill, button background or hover. Otherwise design elements only (decks, print, graphics) |

### Greens by Surface

| | On dark surfaces (step 6–8, black header) | On light surfaces (step 1–2, white header) |
|---|---|---|
| **Acid Green `#ceff00`** | Text, icons, strokes and fills for CTAs and active states (17.9:1 on black) | **Fill only**, with black or step-6 text on top (17.9:1 / 11.2:1). Never text, icons or thin strokes (1.2:1 on white) |
| **Lime Green `#97d600`** | Hover states; focus ring (11.9:1 on black) | **Fill only** (e.g. a hovered button), with black or step-6 text on top. Never text, icons or thin strokes (1.8:1 on white) |
| **Dark Olive `#5d7400`** | Not used in UI (4.0:1 on black — use the brighter greens) | Text, icons and thin strokes where green carries meaning: active, selected, link-style CTA, hover text, focus ring (5.3:1 on white, 4.6:1 on step 2) |

One composition still gets one acid-green moment at most; Dark Olive on a light surface counts as that moment when it marks the active state.

### Tier 2 — Monotones

Two 8-step scales. They're interchangeable and neither is the brand default, but **use one scale consistently within a surface** — don't mix neutral and cool steps on the same page.

| Step | Neutral | Cool | Contrast on white (Neutral / Cool) | Use |
|---|---|---|---|---|
| 1 | `#FFFFFF` | `#FFFFFF` | — | Card backgrounds, reversed text, white header |
| 2 | `#EFEFEF` | `#EFEFF4` | — | Page backgrounds, secondary surfaces |
| 3 | `#C6C6C6` | `#C6C6CD` | 1.7 / 1.7:1 | Borders/dividers on light surfaces; secondary text on dark surfaces (12.3 / 12.4:1 on black) |
| 4 | `#909090` | `#909097` | 3.2 / 3.2:1 | **Large text, UI elements and presentation backgrounds only** — never body or small text on white; muted/disabled |
| 5 | `#5E5E5E` | `#5E5E64` | 6.5 / 6.4:1 | Secondary text on light surfaces — the lightest step safe for body text on white |
| 6 | `#303030` | `#303036` | 13.2 / 13.1:1 | Primary text, UI workhorse |
| 7 | `#121212` | `#121218` | — | Dark surfaces |
| 8 | `#000000` | `#000000` | 21:1 | Headings, black header, strongest contrast |

```css
:root {
  /* Neutral scale */
  --gray-neutral-1: #ffffff;
  --gray-neutral-2: #efefef;
  --gray-neutral-3: #c6c6c6;
  --gray-neutral-4: #909090;
  --gray-neutral-5: #5e5e5e;
  --gray-neutral-6: #303030;
  --gray-neutral-7: #121212;
  --gray-neutral-8: #000000;

  /* Cool scale */
  --gray-cool-1: #ffffff;
  --gray-cool-2: #efeff4;
  --gray-cool-3: #c6c6cd;
  --gray-cool-4: #909097;
  --gray-cool-5: #5e5e64;
  --gray-cool-6: #303036;
  --gray-cool-7: #121218;
  --gray-cool-8: #000000;
}
```

**Site scale:** the website uses the **Cool** scale for its semantic roles (below). `#efeff2`, the previous page background, sits between the two step-2 values; Cool keeps the site's existing slightly cool cast. Decks and other materials may use either scale.

### Tier 3 — Brand Secondary

Expression only. Carries no meaning. **Never used for UI states or data categories.**

| | Top row | Bottom row |
|---|---|---|
| Yellow | `#fff700` | `#806600` |
| Orange | `#ffaa00` — Atlas brand orange | `#b35100` |
| Pink | `#ff66ff` | `#a100a1` |
| Magenta | `#ff33cc` | `#a1006c` |
| Cyan / Blue | `#00e5ff` | `#005ea3` |

- `#ffaa00` (sRGB 255, 170, 0; CMYK 0, 33, 100, 0) **replaces `#ff9600` everywhere**, including any D3 or chart code. Search the codebase for `#ff9600` and replace.
- The top row is bright: `#ffaa00` is 1.9:1 on white, so top-row colors never carry text on white. On black they're strong (`#ffaa00` 11:1).
- Full sRGB and CMYK values: Atlas-Style_Guide_October_2026_v1.pdf.

### Tier 4 — Data Categories

See the D3 Visualization Color Array below. Values are unchanged from v11; what changes is their status: **these colors now mean their category wherever they appear**, not only in D3 charts.

### Tier 5 — System

| Role | Value | Notes |
|---|---|---|
| Error state | `#f50000` | Validation, destructive actions, failed states |
| On-error (text on error) | `#ffffff` | |
| Focus ring (dark surfaces) | `2px solid #97d600`, offset `2px` | Keyboard navigation |
| Focus ring (light surfaces) | `2px solid #5d7400`, offset `2px` | Lime fails 3:1 on light surfaces (v13) |
| Dark-mode display accent | `#ffbc00` | Display use on dark surfaces (e.g. a large stat) |

Never decorative, never a category.

### Semantic Color Assignments

All gray roles reference the Cool scale (see Site scale above).

| Role | Token | Hex | Replaces | Notes |
|------|-------|-----|----------|-------|
| Primary background | `--gray-cool-2` | `#efeff4` | `#efeff2` | |
| Card background | `--gray-cool-1` | `#ffffff` | `#ffffff` | |
| Primary text | `--gray-cool-6` | `#303036` | `#313131` | 13.1:1 on white, 11.4:1 on page background |
| Heading text | `--gray-cool-8` | `#000000` | `#000000` | |
| Secondary text (light surfaces) | `--gray-cool-5` | `#5e5e64` | `#6b6b6b` | 6.4:1 on white, 5.6:1 on page background — darker than before, so contrast improves |
| Secondary text (dark surfaces) | `--gray-cool-3` | `#c6c6cd` | `#bdbdbd`, `#a8a8a8` | 12.4:1 on black; covers small all-caps labels |
| Muted / disabled | `--gray-cool-4` | `#909097` | `#9e9e9e` | Disabled UI is exempt from WCAG contrast; never use for readable small text |
| Border / divider (light surfaces) | `--gray-cool-3` | `#c6c6cd` | `#bdbdbd` | |
| Border / divider (dark surfaces) | `--gray-cool-5` | `#5e5e64` | `#bdbdbd` | Footer dividers keep their existing low-opacity treatment per footer-redesign-spec.md |
| Primary accent / CTA | — | `#ceff00` | | Acid Green — never a success/go signal. Fill only on light surfaces |
| Accent on light (text, icons, strokes) | — | `#5d7400` | | Dark Olive — see Greens by Surface |
| Hover state | — | `#97d600` | | Lime Green — hover only. Fill only on light surfaces |
| Error state | — | `#f50000` | | |
| Site header background | — | `#000000` (default) or `#ffffff` | "always `#000000`" | See Site Header below |

```css
:root {
  --color-bg:              var(--gray-cool-2);
  --color-surface:         var(--gray-cool-1);
  --color-text:            var(--gray-cool-6);
  --color-heading:         var(--gray-cool-8);
  --color-text-secondary:  var(--gray-cool-5);
  --color-text-on-dark-2:  var(--gray-cool-3);
  --color-muted:           var(--gray-cool-4);
  --color-border:          var(--gray-cool-3);
  --color-border-on-dark:  var(--gray-cool-5);

  --color-accent:          #ceff00;  /* fill-only on light surfaces */
  --color-hover:           #97d600;  /* fill-only on light surfaces */
  --color-accent-on-light: #5d7400;  /* text, icons, strokes on light surfaces */
  --color-focus:           #97d600;  /* dark surfaces */
  --color-focus-on-light:  #5d7400;  /* light surfaces */
  --color-error:           #f50000;
  --color-on-error:        #ffffff;
  --color-display-dark:    #ffbc00;
}
```

**Mapping `#bdbdbd` (used for two roles in v11).** Decide by what the color is doing, not by its value:
- **Text** (a `color` property) on a dark surface → step 3, `--color-text-on-dark-2`.
- **Border** on a light surface → step 3, `--color-border`.
- **Border** on a dark surface → step 5, `--color-border-on-dark`.
- **Footer dividers** keep their existing low-opacity treatment.
- `#a8a8a8` (minimum secondary text) → step 3 on dark, step 5 on light.

**Implementation note:** after the swap, search the codebase for the six retired grays (`#313131`, `#efeff2`, `#6b6b6b`, `#9e9e9e`, `#bdbdbd`, `#a8a8a8`) and `#ff9600`. None should remain outside this file's history.

### Site Header

- **Black (`#000000`) is the default and the priority.** White (`#ffffff`) is available when a page needs it, as a deliberate per-page choice.
- Logo must match: `Atlas_logo_lockup_horizontal_blk_web.svg` on white, `Atlas_logo_lockup_horizontal_wht_web.svg` on black. The two files share identical geometry, so swapping them causes no layout shift.
- Nav text follows the header: step 1 on black; step 6 or 8 on white.
- Active nav state: acid green on black; Dark Olive on white (see Greens by Surface).
- Anything docked to the header (e.g. the long-form report "Jump to" sub-nav) uses the same background as the header.

---

## D3 Visualization Color Array (Tier 4 — Data Categories)

*Used in: sunburst/wheel, bubble chart, treemap, all future data visualizations — and any non-chart element that represents a category (tags, labels).*
*Locked May 2026. Probable additions pending Ryan taxonomy confirmation before activation.*

```javascript
const ATLAS_VIZ_COLORS = {

  // CONFIRMED CATEGORIES (9)
  // These map to Ryan's current taxonomy. Do not reassign without James sign-off.

  "Politics & Government":  "#78909c",  // warm slate — intentionally non-partisan, avoids red/blue
  "Local News":             "#ff7043",  // vivid orange-red
  "Technology":             "#ba55cc",  // medium purple-magenta
  "Business & Finance":     "#c6a700",  // deep gold
  "Culture & Arts":         "#ef0e61",  // hot pink, slightly desaturated
  "Sports":                 "#2196f3",  // bold blue
  "Health":                 "#00acc1",  // cyan-teal
  "Environment":            "#26a69a",  // teal-green — distinct from brand greens
  "International":          "#d81b72",  // deep rose-pink

  // PROBABLE ADDITIONS (6)
  // Pre-assigned pending Ryan confirming taxonomy. Do not activate until
  // Ryan validates the category name and slug. Names below are working titles.

  "Criminal Justice":       "#e53935",  // strong red
  "Immigration":            "#7c4dff",  // electric violet
  "Science":                "#5b7fa6",  // denim blue-gray
  "Housing":                "#bf5a3a",  // terra cotta
  "Religion / Faith":       "#a1887f",  // warm taupe
  "Labor / Economy":        "#6a8d9b",  // cool blue-gray

  // RESERVE SLOTS (3)
  // Unassigned. Available for new categories Ryan adds.
  // ⚠ Too light on white and near-duplicates of brand secondary colors.
  //   Before activating: darken, and either adopt the matching brand secondary
  //   hex or move clearly away from it. Requires James sign-off.

  "Reserve A":              "#ea80fc",  // light magenta — near #ff66ff
  "Reserve B":              "#40c4ff",  // light cyan — near #00e5ff
  "Reserve C":              "#ffab40",  // light amber — near #ffaa00

};

// Flat array (for D3 contexts requiring ordered list rather than named map)
const ATLAS_VIZ_COLORS_ARRAY = [
  "#78909c",  // Politics & Government
  "#ff7043",  // Local News
  "#ba55cc",  // Technology
  "#c6a700",  // Business & Finance
  "#ef0e61",  // Culture & Arts
  "#2196f3",  // Sports
  "#00acc1",  // Health
  "#26a69a",  // Environment
  "#d81b72",  // International
  "#e53935",  // Criminal Justice
  "#7c4dff",  // Immigration
  "#5b7fa6",  // Science
  "#bf5a3a",  // Housing
  "#a1887f",  // Religion / Faith
  "#6a8d9b",  // Labor / Economy
];
```

**Color assignment rules:**
- Acid green `#ceff00` is excluded — reserved for CTAs and active states only
- Error red is excluded — reserved for system feedback only
- Brand secondary colors (Tier 3) never appear in the same composition as category colors
- All confirmed colors pass contrast on both white and black backgrounds
- Luminosity target: ~50–65% HSL lightness across the confirmed set

---

## Typography

*Unchanged from v11.*

### Font Stack

| Role | Family | Notes |
|------|--------|-------|
| Primary / UI | **Inter** | Google Fonts. Used everywhere: site, decks, Google Docs. Variable font (wght 100–900) covers the full 400/500/600/700/800 scale natively. Hanken Grotesk is retired from the brand entirely. |
| Monospace | Source Code Pro | Google Fonts. Mono UI chrome (footer, nav labels). 13px floor. |
| Secondary serif | **Merriweather** | Google Fonts. Long-form/editorial body copy, paired against Inter UI. |

### Type Scale

| Level | Size | Weight | Line Height | Use |
|-------|------|--------|-------------|-----|
| Display | 48px | 800 | 1.1 | Hero headings only — homepage, landing pages. Use sparingly. |
| H1 | 36px | 700 | 1.2 | Page titles |
| H2 | 28px | 700 | 1.25 | Section heads |
| H3 | 20px | 600 | 1.3 | Card titles, drawer headers — often two lines in constrained widths |
| Body | 16px | 400 | 1.6 | Default reading text |
| Small | 13px | 400 | 1.5 | Meta, timestamps, source names, creator bylines — 13px is the floor |
| Micro | 11px | 500 | 1.4 | All-caps labels only (TECH, CULTURE, POLITICS etc.) — weight 500 minimum at this size; always letter-spaced at 0.08–0.1em |

**Pulse card hierarchy — required implementation pattern:**
- Article title → H3 (20px / 600)
- Creator name → Small (13px / 400)
- Date · Publication → Micro (11px / 500, all-caps)

### Font Weights in Use
- 400 (regular)
- 500 (medium) — Micro labels only
- 600 (semibold)
- 700 (bold)
- 800 (extrabold)

---

## Spacing & Layout

*Unchanged from v11.*

### Base Unit
Base spacing unit: **4px**

### Spacing Scale
```
xs:  4px
sm:  8px
md:  16px
lg:  24px
xl:  32px
2xl: 48px
3xl: 96px
```

**3xl (96px)** — added Jul 2026 for the footer redesign's column gutter. Use for any layout needing a generous gutter.

### Header Nav Spacing (Aug 2026)

| Gap | Token | Value |
|---|---|---|
| Logo → search bar | `2xl` | 48px |
| Search bar → first nav link | `2xl` | 48px |
| Between nav links (Pulse / For Brands / Research & Writing / Submit) | `xl` | 32px |
| Last nav link → Partners badge | `lg` | 24px |

Search bar capped at roughly 320–360px rather than flexing to fill available space. If cramped, fall back to `lg` (24px) between nav links. Confirm against the real rendered layout; "Research & Writing" is the tightest fit.

### Border Radius
```
card:     6px
button:   6px
pill/tag: 9999px
```

### Max Content Width
```
full layout:  1440px — outer container; all content constrained within this, centered with margin: 0 auto
card grid:    1200px — card grids sit inside full layout with comfortable margin on both sides
text column:  680px  — editorial/reading contexts; approx 70 characters at 16px body
```

### Container Inner Padding

```css
.container {
  max-width: 1440px;
  margin-inline: auto;
  padding-inline: 16px; /* md token */
}
```

Apply consistently everywhere the container is used — hero, header, footer, card grids. **Every top-of-page section must use the same `full layout` container as the sections below it — hero sections are not exempt, regardless of any full-bleed background color they carry.** The footer is the reference implementation for the header. See `Atlas-Layout-Fix-Brief-2026-08.md`.

**Reference points:** Bloomberg (~1280px) and Wired (~1440px). The Atlas targets Wired's contained-but-generous feel.

---

## Iconography

*Unchanged from v11, except the selected color on light surfaces (v13).*

- **Icon set:** Material Symbols Outlined
- **Fill states:** Outlined by default, everywhere. **Toggle/action icons only** — save, follow, bookmark, and similar binary-state affordances (e.g. "add to pack") — switch to **filled** when active. **Persistent navigation and section icons stay outlined at every state**, with selection carried by color only (acid green on dark surfaces, Dark Olive on light).
- **Touch targets:** 44×44px minimum.
- **Icon size defaults:**

| Context | Size |
|---------|------|
| Nav | 24px |
| Card header | 24px |
| Inline / body | 18px |
| Section header | 28px |

---

## Component States

### Interactive States
- Default
- Hover — Lime Green `#97d600` (fill only on light surfaces; Dark Olive `#5d7400` where hover changes text or icon color on a light surface)
- Active / Selected — Acid Green `#ceff00` (fill only on light surfaces; Dark Olive `#5d7400` for active text, icons or underlines on a light surface)
- Disabled — `--color-muted` (`#909097`) *(was `#9e9e9e`)*
- Focus (keyboard nav) — `2px solid #97d600`, offset `2px` on dark surfaces; `2px solid #5d7400`, offset `2px` on light surfaces

### Card States
- Default
- Hover
- Selected (in pack-builder mode)

---

## Logo Usage

Per the 2026 Style Guide (Atlas-Style_Guide_October_2026_v1.pdf):
- Logo asset library: mirrored in Google Drive (folder `1BT48q5ng6FN0Y0e_XllWvNrI0LFmL_tN`) and Dropbox (linked from the style guide). Both hold the same files; one is a backup of the other.
- **Web SVG logos** (header, footer and other `_web.svg` lockups): Google Drive folder https://drive.google.com/drive/folders/1p0i7PuLqrpOxcrHt0MEKGk1ghnzPXYgv. Pull SVGs for the site from here; the repo copy is what ships.
- Transparent PNGs sized at 500×500px (icons) and 3000×3000px (full logos)
- Contact james@happicamp.com for larger sizes or alternate formats

### Header logo

| Header background | Asset |
|---|---|
| White `#ffffff` | `Atlas_logo_lockup_horizontal_blk_web.svg` |
| Black `#000000` | `Atlas_logo_lockup_horizontal_wht_web.svg` *(new, Oct 2026)* |

Both share an identical viewBox (1000 × 134.5) and path geometry. The white file sets `fill="#fff"` explicitly; the black file relies on the SVG default fill (black). Neither responds to CSS `color` — swap the file, don't recolor it.

### Footer logo

- `Atlas_logo_lockup_stacked_wht_web.svg`, white fill, sized to roughly one nav column's width per `footer-redesign-spec.md`. Set dimensions on the `img`/`svg` element directly, not the container.
- The footer's vertical divider rules are a deliberate design element (see `footer-redesign-spec.md`), not a recurrence of the May 2026 `border-right` bug.

**Available logo variants (in repo):**
- `Journalism_Atlas_logo_black.png`
- `Journalism_Atlas_logo_acid_green.png`
- `Journalism_Atlas_logo_dark_gray.png`
- `Journalism_Atlas_logo_light_gray.png`
- `Journalism_Atlas_wordmark_lockup_black.png`
- `Journalism_Atlas_wordmark_lockup_white.png`
- `Journalism_Atlas_wordmark_stacked_black.png`
- `Journalism_Atlas_wordmark_stacked_white.png` *(superseded in footer use — leave in repo)*
- `Journalism_Atlas_wordmark_stacked_gray.png`
- `Journalism_Atlas_wordmark_stacked_green_white.png`
- `Journalism_Atlas_icon_green_transparent.png`
- `Journalism_Atlas_icon_black_transparent.png`
- `Journalism_Atlas_icon_white_transparent.png`
- `Journalism_Atlas_favicon.png`
- `Atlas_logo_lockup_horizontal_blk_web.svg` *(header, white background)*
- `Atlas_logo_lockup_horizontal_wht_web.svg` *(header, black background — new Oct 2026)*
- `Atlas_logo_lockup_stacked_wht_web.svg` *(footer)*

---

## Accessibility

- WCAG 2.1 AA + Material Design 3. 4.5:1 for body text; 3:1 for large text and UI components.
- 13px type floor (Micro all-caps labels at 11px / weight 500 excepted); 44×44px touch targets.
- Gray step 5 is the lightest step for body or small text on white. Step 4 (3.2:1) is large text and UI only.
- Acid Green and Lime Green are never text, icons or thin strokes on light surfaces. Use Dark Olive there (see Greens by Surface).
- Atlas tokens don't apply to Project C — check projectc.biz/style-guide before flagging its brand choices.

---

## Notes & Decisions Log

| Date | Decision | Rationale |
|------|----------|-----------|
| Feb 2026 | Hanken Grotesk as primary font | Clean, geometric, works well at small sizes for data-dense UI — *superseded Sep 2026* |
| Feb 2026 | Acid green `#ceff00` as primary accent | Brand differentiation, energy, established in Style Guide |
| May 2026 | DM Mono confirmed as monospace font | Replaces JetBrains Mono — *superseded Jul 2026* |
| May 2026 | Merriweather retired from active font stack | No current serif use case — *reactivated Sep 2026* |
| May 2026 | Spacing base unit confirmed as 4px | Per HOW_WE_BUILD.md |
| May 2026 | Border radius: 6px cards/buttons, 9999px pills/tags | Per HOW_WE_BUILD.md |
| May 2026 | Material Symbols Outlined confirmed as icon set | Replaces earlier Material Icons reference |
| May 2026 | Icon sizes locked: nav 24px, card header 24px, inline 18px, section header 28px | M3 standard sizing adapted for data-dense UI |
| May 2026 | Error state `#f50000` | Needs to grab attention immediately; M3 baseline `#b3261e` too dull |
| May 2026 | Muted/disabled `#9e9e9e` | Balanced contrast on light and dark surfaces — *superseded Oct 2026* |
| May 2026 | Border/divider `#bdbdbd` | Readable, appropriately subtle 1px lines — *superseded Oct 2026* |
| May 2026 | Secondary text (dark surfaces) `#bdbdbd` | Small all-caps labels need more than the bare AA floor — *superseded Oct 2026* |
| May 2026 | D3 viz color array locked (15 confirmed + 3 reserve) | See ATLAS_VIZ_COLORS.md for full decisions log |
| May 2026 | Politics & Govt → `#78909c` warm slate | Red/blue carry partisan US associations |
| May 2026 | Environment → `#26a69a` teal-green | Prevents confusion with brand greens |
| May 2026 | Acid green excluded from viz palette | Reserved for CTAs and active states only |
| May 2026 | Site header always `#000000` | Site-wide constant — *superseded Oct 2026* |
| May 2026 | Footer logo height standard: 40px | *Superseded Jul 2026* |
| May 2026 | Card feature treatments apply to containers, never cards | Cards stay consistent; clicks stay on-site |
| May 2026 | Type scale locked: Display 48 / H1 36 / H2 28 / H3 20 / Body 16 / Small 13 / Micro 11 | ~1.25 ratio above body, tighter below for data-dense contexts |
| May 2026 | H3 at 20px/600 | Restores Pulse card hierarchy |
| May 2026 | Micro at 11px requires weight 500 minimum | Legibility of small all-caps labels; letter-spaced 0.08–0.1em |
| May 2026 | Line heights specified per level | Tighter at large sizes, looser at reading sizes |
| May 2026 | Max content widths locked: 1440 / 1200 / 680px | Stop sprawl on 27" monitors; Wired benchmark |
| May 2026 | Focus ring: `2px solid #97d600`, offset `2px` | On-system, WCAG AA compliant |
| May 2026 | Footer `border-right` cleared on logo container; height targets the `img` | Selector precision — earlier fixes missed the container |
| Jul 2026 | Source Code Pro replaces DM Mono | Footer redesign |
| Jul 2026 | Footer logo → `Atlas_logo_lockup_stacked_wht_web.svg`, sized to ~one nav column | Footer redesign |
| Jul 2026 | Header logo → `Atlas_logo_lockup_horizontal_blk_web.svg` | Header lockup moved to SVG |
| Jul 2026 | Footer column dividers are deliberate | Not a regression of the May 2026 bug |
| Jul 2026 | New spacing token 3xl (96px) | 2× 2xl; footer gutter |
| Aug 2026 | Hero/first-module sections must use the 1440px container | Implementation regression on five pages |
| Aug 2026 | Header constrained to the footer's container; header nav spacing table added | Header/footer inconsistency |
| Aug 2026 | Container inner padding 16px (`md`) | Breathing room on laptops near 1440px |
| Sep 2026 | Primary/UI font: Hanken Grotesk → Inter | Legibility on data-heavy text; closest Google Font to Neue Haas Grotesk; full 400–800 weights |
| Sep 2026 | Merriweather reactivated as paired editorial serif | Screen-legible pairing with Inter; Georgia and Newsreader passed over |
| Sep 2026 | Icon fill-on-select scoped to toggle/action icons | Shape change is an unambiguous click confirmation; nav icons stay outlined |
| **Oct 2026** | **Neutral and Cool 8-step monotone scales replace all previous grays** | The ad-hoc grays (`#313131`, `#efeff2`, `#6b6b6b`, `#9e9e9e`, `#bdbdbd`, `#a8a8a8`) had accumulated role by role. Two consistent scales give every surface, text and border role a defined step, with matched values across scales so they're interchangeable. Neutral step 4 set to `#909090` to keep the 144 base consistent with Cool. |
| **Oct 2026** | **Site uses the Cool scale for semantic roles** | `#efeff2`, the outgoing background, already had a cool cast; Cool step 2 is the closest match, so the visual shift is minimal. Either scale may be used in decks and other materials, but not mixed on one surface. |
| **Oct 2026** | **Role remapping** | Primary text → step 6 (13.1:1). Secondary text on light → step 5, darker than `#6b6b6b`, improving contrast (6.4:1 on white). Secondary text on dark → step 3 (12.4:1 on black), absorbing `#bdbdbd` and `#a8a8a8`. Muted/disabled → step 4. Borders → step 3 on light, step 5 on dark. |
| **Oct 2026** | **Step 4 restricted to large text, UI elements and presentation backgrounds** | 3.2:1 on white — passes for large text and UI, fails for body text. |
| **Oct 2026** | **Five-tier color structure: Core brand, Monotones, Brand secondary, Data categories, System** | Brand colors express; data colors encode. The old rule reserving the secondary palette for D3 had been contradicted by the live site, where `ATLAS_VIZ_COLORS` and the secondary palette are entirely different sets. Separating by job prevents a decorative color being read as a category. |
| **Oct 2026** | **`#ffaa00` confirmed as Atlas brand orange; replaces `#ff9600` everywhere** | Style guide values corrected to sRGB 255, 170, 0 / CMYK 0, 33, 100, 0. One orange across brand and code. |
| **Oct 2026** | **Dark Olive `#5d7400` retired from UI** | Stays in the brand palette for design elements only. |
| **Oct 2026** | **Site header: black or white** | The "always black" constant had become fluid in practice. Header color is now a design choice; logo and docked elements must match it. |
| **Oct 2026** | **New asset: `Atlas_logo_lockup_horizontal_wht_web.svg`** | White header logo for the black-header option; identical geometry to the black version, so no layout shift on swap. |
| **Oct 2026** | **Reserve slots A/B/C flagged as near-duplicates of brand secondary colors** | `#ea80fc`/`#ff66ff`, `#40c4ff`/`#00e5ff`, `#ffab40`/`#ffaa00`. Before activation, darken and either align with or clearly separate from the secondary color. No values changed in v12. |
| **Oct 2026 (v13)** | **Greens by surface: Acid and Lime Green are fill-only on light surfaces** | Both fail the 3:1 non-text minimum on white (1.2:1 and 1.8:1). On light surfaces they work only as fills with black or step-6 text on top (17.9:1 / 11.2:1 for acid). On dark surfaces they keep their existing roles. A rumored "acid on dark only, lime on light only" rule was never canon and fails on contrast. |
| **Oct 2026 (v13)** | **Dark Olive `#5d7400` returns to the UI as the green for text, icons and thin strokes on light surfaces** | The only existing brand green that passes on light surfaces (5.3:1 on white, 4.6:1 on step 2). Reuses a brand color rather than inventing one. Narrows, rather than reverses, v12's retirement: it's still never a fill, CTA background or hover fill. |
| **Oct 2026 (v13)** | **Focus ring is Dark Olive on light surfaces** | The Lime Green ring fails 3:1 on white. Lime stays the focus ring on dark surfaces. |
| **Oct 2026 (v13)** | **Site header: black is the default and the priority** | Matches the current look, so v12 ships with no visible header change. White remains available per page. |
| **Oct 2026 (v13)** | **`#bdbdbd` mapping clarified by role** | v11 used it for text on dark and for borders on both surfaces. Text → step 3; border on light → step 3; border on dark → step 5. |
| **Oct 2026 (v13)** | **Tier 2 contrast figures show both scales** | v12 listed the Neutral figures only; the site uses Cool. Both are now shown (e.g. 13.2 / 13.1:1). |
