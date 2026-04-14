# Atlas Design Tokens
*Canonical design reference — committed to repo as source of truth for implementation*

*Last updated: April 2026*
*Owner: James (james@happicamp.com)*

> **How this file works:** This is the single source of truth for all visual decisions. When Justin implements design changes with Claude Code, he references this document. If it's not here, it doesn't get implemented. If it changes here, it changes everywhere. Fill in any blanks marked [TO CONFIRM] and update as needed.

---

## Color Palette

### Primary Palette (from Style Guide 2026)

| Name | Hex | sRGB | Use |
|------|-----|------|-----|
| Light Gray | `#efeff2` | 239, 239, 242 | Primary background, secondary surfaces |
| Dark Gray | `#313131` | 49, 49, 49 | Primary text, UI elements |
| Acid Green | `#ceff00` | 206, 255, 0 | Primary accent, CTAs — **dark backgrounds only** |
| Lime Green | `#97d600` | 151, 214, 0 | Secondary accent — **light backgrounds only** |
| Dark Olive | `#5d7400` | 93, 116, 0 | Tertiary / deep accent |
| Black | `#000000` | 0, 0, 0 | Headers, strong contrast |
| White | `#ffffff` | 255, 255, 255 | Card backgrounds, reversed text |

### Secondary Palette — Light

| Name | Hex | sRGB |
|------|-----|------|
| Yellow | `#fff700` | 255, 247, 0 |
| Orange | `#ffaa00` | 255, 170, 0 |
| Light Pink | `#ff66ff` | 255, 102, 255 |
| Hot Pink | `#ff33cc` | 255, 51, 204 |
| Cyan | `#00e5ff` | 0, 229, 255 |

### Secondary Palette — Dark

| Name | Hex | sRGB |
|------|-----|------|
| Dark Gold | `#806600` | 128, 102, 0 |
| Dark Orange | `#b35100` | 179, 81, 0 |
| Dark Purple | `#a100a1` | 161, 0, 161 |
| Dark Magenta | `#a1006c` | 161, 0, 108 |
| Dark Blue | `#005ea3` | 0, 94, 163 |

> **Usage note:** Secondary palette is the candidate pool for visualization color assignments (topic categories). Light variants for use on dark/black backgrounds; dark variants for use on light/white backgrounds. Confirm specific assignments with James before implementing.

### Semantic Color Assignments

#### Global (mode-invariant)

| Role | Hex | Note |
|------|-----|------|
| Header text | `#000000` | Always black — consistent across all digital assets regardless of mode |

#### Light Mode

| Role | Hex | Note |
|------|-----|------|
| Primary background | `#efeff2` | |
| Card background | `#ffffff` | |
| Primary text | `#313131` | |
| Primary accent / CTA | `#97d600` | Lime green — light backgrounds only |
| Hover / active state | `#5d7400` | Dark olive |
| Error state | `#cc2200` | |
| Muted / disabled | `#b0b0b8` | |
| Border / divider | `#d4d4d8` | |

#### Dark Mode

| Role | Hex | Note |
|------|-----|------|
| Primary background | `#313131` | |
| Card background | `#000000` | |
| Primary text | `#efeff2` | |
| Primary accent / CTA | `#ceff00` | Acid green — dark backgrounds only |
| Hover / active state | `#97d600` | Lime green |
| Error state | `#ff4422` | |
| Muted / disabled | `#606068` | |
| Border / divider | `#48484f` | |

---

## Visualization Color Array

*Used in: sunburst/wheel, bubble chart, treemap. Implemented as a vanilla JS constant — not a D3 scale. Currently improvised — James to own final assignments.*

```javascript
// CURRENT PLACEHOLDER — needs James's sign-off
// Draw from secondary palette below; confirm category list with Ryan
const ATLAS_VIZ_COLORS = [
  "#ceff00", // acid green (primary — use sparingly, high visual weight)
  "#97d600", // lime green
  "#5d7400", // dark olive
  // [TO COMPLETE — James to assign one color per topic category]
];
```

**Available secondary colors for viz assignments:**

Light (for dark/black viz backgrounds):
`#fff700` `#ffaa00` `#ff66ff` `#ff33cc` `#00e5ff`

Dark (for light/white viz backgrounds):
`#806600` `#b35100` `#a100a1` `#a1006c` `#005ea3`

**Topic categories pending color assignment** (confirm full list with Ryan):
- Politics & Government
- Local News
- Technology
- Business & Finance
- Culture & Arts
- Sports
- Health
- Environment
- Education
- International
- General News
- [others — confirm with Ryan's taxonomy]

---

## Typography

*Conforms to Material Design 3 type scale. Mobile-first. All sizes in px.*

### Font Stack

| Role | Family | Source | Use |
|------|--------|--------|-----|
| Primary / UI | Hanken Grotesk | Google Fonts | All UI, data, labels, headings |
| Editorial | Merriweather | Google Fonts | Long-form editorial content only — not UI |

### Font Weights in Use

| Weight | Name | Use |
|--------|------|-----|
| 400 | Regular | Body text, editorial |
| 500 | Medium | Labels, tags, buttons, titles |
| 700 | Bold | Headings (H1–H3, Display) only |

> No other weights are in use. Do not introduce 600 or 800.

### Type Scale

*Based on M3 roles. Line heights and letter spacing optimised for legibility in a data-dense UI.*

| Level | M3 Role | Size | Weight | Line Height | Letter Spacing | Font | Use |
|-------|---------|------|--------|-------------|----------------|------|-----|
| Display | Display Small | 36px | 700 | 44px | -0.25px | Hanken Grotesk | Hero moments only |
| H1 | Headline Large | 32px | 700 | 40px | -0.25px | Hanken Grotesk | Page titles |
| H2 | Headline Medium | 28px | 700 | 36px | 0px | Hanken Grotesk | Section heads |
| H3 | Headline Small | 24px | 700 | 32px | 0px | Hanken Grotesk | Card titles, sub-sections |
| Title | Title Large | 22px | 500 | 28px | 0px | Hanken Grotesk | UI titles, modal headers |
| Body Large | Body Large | 16px | 400 | 26px | 0.15px | Hanken Grotesk | Default body — primary reading size |
| Body Medium | Body Medium | 14px | 400 | 22px | 0.25px | Hanken Grotesk | Secondary body, card content |
| Label | Label Large | 14px | 500 | 20px | 0.1px | Hanken Grotesk | Filter tags, UI labels, buttons |
| Small | Label Medium | 12px | 500 | 16px | 0.4px | Hanken Grotesk | Meta, timestamps, captions |
| Micro | Label Small | 11px | 500 | 16px | 0.5px | Hanken Grotesk | Fine print, footnotes — non-essential only |
| Editorial | — | 16px | 400 | 28px | 0.15px | Merriweather | Long-form editorial content only |

> **Line height note:** Body Large uses 26px (not M3's default 24px). The extra 2px is intentional — data-dense layouts benefit from the additional breathing room for scanability. Editorial (Merriweather) uses 28px; serif fonts require more interline space by nature of their letterforms.

> **Letter spacing note:** Negative tracking on Display and H1 only — large heavy type at 700 weight appears slightly loose and benefits from tightening. Positive tracking increases progressively at smaller sizes to prevent crowding.

### Dark Mode Typography Rules

Type scale values (size, weight, line height, letter spacing) are **mode-invariant** — the same tokens apply in both light and dark mode.

Two rules apply specifically to dark mode:

1. **Weight reduction on body text:** Light text on dark backgrounds appears optically heavier than the same weight on light. Prefer weight 400 for body text on dark backgrounds. Avoid weight 700 on anything smaller than H3.
2. **Minimum text size:** 12px is the floor for any text rendered on a dark background. Micro (11px) is acceptable on light backgrounds only, and only for non-essential content.

---

## Spacing & Layout

*Conforms to Material Design 3. Mobile-first. All values in px.*

### Base Unit

**8px.** All spacing values are multiples of 8px. The only exception is `xs` at 4px (half-unit), used for tight inline spacing only. Never land on an arbitrary value like 13px or 22px.

### Spacing Scale

| Token | Value | Typical use |
|-------|-------|-------------|
| xs | 4px | Icon gaps, tight inline spacing |
| sm | 8px | Between label and value, chip padding |
| md | 16px | Card internal padding, button padding |
| lg | 24px | Between cards, section internal spacing |
| xl | 32px | Section padding, generous component gaps |
| 2xl | 48px | Between major sections |
| 3xl | 64px | Page-level vertical rhythm, hero spacing |

### Border Radius

| Context | Value | Note |
|---------|-------|------|
| Card | 6px | |
| Button | 6px | |
| Input field | 6px | |
| Modal | 8px | Slightly softer at larger scale |
| Pill / tag | 100px | Fully rounded — M3 standard for chips |

> Pill/tag radius is always 100px regardless of the 6px base. Fully rounded chips are immediately readable as interactive filter elements.

### Max Content Width

| Context | Value |
|---------|-------|
| Full layout | 1440px |
| Text column (editorial) | 680px |
| Card grid | 1440px |

### Breakpoints

*Mobile-first. Min-width based.*

| Name | Value | Layout behaviour |
|------|-------|-----------------|
| Mobile | 0–767px | Single column, stacked layout |
| Tablet | 768px | Two column, filter sidebar appears |
| Desktop | 1024px | Full layout unlocked |
| Wide | 1440px | Max content width cap — no layout changes above this |

---

## Iconography

**Set:** Material Symbols (replaces legacy Material Icons)
**Google Fonts import:** `Material Symbols Outlined`

### Style & States

| State | Style | Note |
|-------|-------|------|
| Default | Outlined | All icons default to outlined |
| Active / selected | Filled | Swap to filled variant on active state only |

> Never mix Outlined and Rounded or Sharp variants. Outlined is the Atlas standard.

### Sizes

| Token | Size | Use |
|-------|------|-----|
| Icon SM | 20px | Inline icons, tight UI contexts, tags |
| Icon MD | 24px | Standard UI — buttons, navigation, filters |
| Icon LG | 40px | Decorative, empty states, hero moments |

### Weight & Grade

| Property | Value | Note |
|----------|-------|------|
| Weight (`wght`) | 400 | Matches body type weight — consistent visual rhythm |
| Grade (`GRAD`) | 0 | Default — no adjustment needed |
| Optical size (`opsz`) | Match icon size | 20 for SM, 24 for MD, 40 for LG |

### Color

Icons inherit from semantic text tokens — no separate icon color tokens.

| Context | Color token |
|---------|------------|
| Default icon | Primary text (`#313131` light / `#efeff2` dark) |
| Muted / inactive | Muted token (`#b0b0b8` light / `#606068` dark) |
| Active / accent | Primary accent (`#97d600` light / `#ceff00` dark) |
| Error | Error token (`#cc2200` light / `#ff4422` dark) |

---

## Component States

*All states defined for light and dark mode. Background shift is the primary interactive signal for cards. Accent fill is the selected signal for tags.*

### Cards

| State | Light mode | Dark mode |
|-------|-----------|-----------|
| Default | Background `#ffffff`, border `0.5px #d4d4d8` | Background `#313131`, border `0.5px #48484f` |
| Hover | Background `#efeff2`, border `0.5px #b0b0b8` | Background `#3e3e3e`, border `0.5px #606068` |
| Selected | Background `#efeff2`, border `1.5px #97d600` | Background `#3e3e3e`, border `1.5px #ceff00` |
| Disabled | Default styles, `opacity: 0.45` | Default styles, `opacity: 0.45` |

> Selected state combines background shift + accent border. Used in pack-builder mode when a creator card is added to a list.

### Filter Tags / Chips

| State | Light mode | Dark mode |
|-------|-----------|-----------|
| Default | Background `#ffffff`, border `0.5px #d4d4d8`, text `#313131` | Background `#313131`, border `0.5px #48484f`, text `#efeff2` |
| Hover | Background `#efeff2`, border `0.5px #b0b0b8`, text `#313131` | Background `#3e3e3e`, border `0.5px #606068`, text `#efeff2` |
| Selected | Background `#97d600`, border `0.5px #5d7400`, text `#313131` | Background `#ceff00`, border `0.5px #97d600`, text `#313131` |
| Disabled | Default styles, `opacity: 0.55` | Default styles, `opacity: 0.55` |

> Tag text is always `#313131` in selected state — both accent colors are light enough to support dark text in both modes.

### Buttons — Secondary (Ghost)

| State | Light mode | Dark mode |
|-------|-----------|-----------|
| Default | Background `transparent`, border `1.5px #d4d4d8`, text `#313131` | Background `transparent`, border `1.5px #606068`, text `#efeff2` |
| Hover | Background `#efeff2`, border `1.5px #b0b0b8`, text `#313131` | Background `#3a3a3a`, border `1.5px #808088`, text `#efeff2` |
| Disabled | Default styles, `opacity: 0.45` | Default styles, `opacity: 0.45` |

### Buttons — Primary (Accent fill)

| State | Light mode | Dark mode |
|-------|-----------|-----------|
| Default | Background `#97d600`, border `1.5px #5d7400`, text `#313131` | Background `#ceff00`, border `1.5px #97d600`, text `#313131` |
| Hover | Background `#5d7400`, border `1.5px #5d7400`, text `#ffffff` | Background `#97d600`, border `1.5px #5d7400`, text `#313131` |
| Disabled | Default styles, `opacity: 0.45` | Default styles, `opacity: 0.45` |

> Primary hover on light mode deepens to dark olive with white text — staying within the green family while providing clear depth. Primary text is always `#313131` on dark mode as accent colors are light enough to support it.

### Focus State (Keyboard Navigation)

| Element | Style |
|---------|-------|
| All interactive elements | `outline: 2px solid #97d600` (light) / `outline: 2px solid #ceff00` (dark), `outline-offset: 2px` |

> Focus ring uses accent color in both modes. Never remove focus styles — required for accessibility.

---

## Logo Usage

Per the 2025 Style Guide:
- All logo files live in the GitHub repo under `/assets/images/logos/`
- Transparent PNGs sized at 500×500px
- Contact james@happicamp.com for larger sizes or alternate formats

**Available logo variants (confirmed in repo):**
- `Journalism_Atlas_logo_black.png`
- `Journalism_Atlas_logo_acid_green.png`
- `Journalism_Atlas_logo_dark_gray.png`
- `Journalism_Atlas_logo_light_gray.png`
- `Journalism_Atlas_wordmark_lockup_black.png`
- `Journalism_Atlas_wordmark_lockup_white.png`
- `Journalism_Atlas_wordmark_stacked_black.png`
- `Journalism_Atlas_wordmark_stacked_white.png`
- `Journalism_Atlas_wordmark_stacked_gray.png`
- `Journalism_Atlas_wordmark_stacked_green_white.png`

---

## Notes & Decisions Log

*Append decisions here so there's a record of why things are the way they are.*

| Date | Decision | Rationale |
|------|----------|-----------|
| Feb 2026 | Hanken Grotesk as primary font | Clean, geometric, works well at small sizes for data-dense UI |
| Feb 2026 | Acid green (#ceff00) as primary accent | Brand differentiation, energy, established in Style Guide |
| Apr 2026 | Full secondary palette added (5 light, 5 dark) | Source pool for viz color assignments; from Style Guide 2026 |
| Apr 2026 | Acid green = dark backgrounds only; Lime green = light backgrounds only | Contrast and legibility rule; do not swap |
| Apr 2026 | Viz colors are vanilla JS constants, not D3 scales | Stack is plain HTML/CSS/JS — no D3 in use |
| Apr 2026 | DESIGN-TOKENS structured into Global / Light Mode / Dark Mode sections | Enables optimal per-mode tokens; Global holds mode-invariant constants |
| Apr 2026 | Header text always `#000000` regardless of mode | Brand consistency across all digital assets |
| Apr 2026 | Separate error, muted, and border tokens per mode | Universal tokens were a contrast compromise; mode-specific tokens are optimal |
| Apr 2026 | Type scale based on M3; Body Large (16px) as default body size | Mobile-first; current site type judged too small; M3 Body Large is correct floor |
| Apr 2026 | Font weights: 400 (body), 500 (labels/UI), 700 (headings only) | Clean and intentional; no 600 or 800 |
| Apr 2026 | Body Large line height 26px, not M3 default 24px | Data-dense UI needs extra breathing room for scanability |
| Apr 2026 | Type scale is mode-invariant; two dark mode rules added as principles | Size/weight/spacing don't change per mode; optical weight inflation on dark handled via rule not token |
| Apr 2026 | Micro (11px) permitted on light backgrounds only | Contrast risk on dark backgrounds at sub-12px; 12px is dark mode floor |
| Apr 2026 | Base spacing unit 8px; xs = 4px half-unit exception | M3 standard; keeps layout mathematically consistent |
| Apr 2026 | Border radius 6px base; pill/tag always 100px | 6px is visible and intentional without reading as consumer product; pills are M3 standard |
| Apr 2026 | Max content width 1440px; text column 680px | 1440px matches reference viewport; 680px is optimal editorial line length |
| Apr 2026 | Breakpoints: 768px tablet, 1024px desktop, 1440px wide | Mobile-first; filter sidebar appears at tablet breakpoint |
| Apr 2026 | Icon set: Material Symbols Outlined; replaces legacy Material Icons | Outlined = Atlas standard; Filled reserved for active states only |
| Apr 2026 | Icon sizes: 20px SM, 24px MD, 40px LG | Optical size matches icon size per M3 spec |
| Apr 2026 | Icon weight 400; matches body type | Consistent visual rhythm across type and iconography |
| Apr 2026 | Icons inherit semantic text color tokens | No separate icon color tokens needed |
| Apr 2026 | Card hover = background shift; not elevation | Flat signal; works in both modes; no shadow calculations |
| Apr 2026 | Card selected = background shift + accent border 1.5px | Dual signal needed for pack-builder mode clarity |
| Apr 2026 | Tag selected = full accent fill | Small components need strong selected signal; accent fill is unambiguous |
| Apr 2026 | Tag/selected text always #313131 | Both accent colors (lime/acid green) are light enough to support dark text |
| Apr 2026 | Primary button hover on light = dark olive + white text | Deepens within green family; sufficient contrast at hover |
| Apr 2026 | Focus ring = 2px accent color, offset 2px | Accessibility requirement; never remove focus styles |
