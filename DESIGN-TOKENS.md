# Atlas Design Tokens
*Canonical design reference — committed to repo as source of truth for implementation*

*Last updated: March 2026*
*Owner: James (james@happicamp.com)*

> **How this file works:** This is the single source of truth for all visual decisions. When Justin implements design changes with Claude Code, he references this document. If it's not here, it doesn't get implemented. If it changes here, it changes everywhere.

> **Mobile-first note:** The Atlas is used by creator-journalists on mobile as much as desktop. All tokens include mobile considerations. Optimized for 13-inch MacBook (1440px) on desktop and 390px iPhone on mobile.

---

## Color Palette

### Brand Colors (from Style Guide 2025)

| Name | Hex | sRGB | Use |
|------|-----|------|-----|
| Acid Green | `#ceff00` | 206, 255, 0 | Primary accent, CTAs, highlights |
| Lime Green | `#97d600` | 151, 214, 0 | Secondary accent |
| Dark Olive | `#5d7400` | 93, 116, 0 | Tertiary / deep accent |
| Dark Gray | `#313131` | 49, 49, 49 | Primary text, UI elements |
| Light Gray | `#efeff2` | 239, 239, 242 | Backgrounds, secondary surfaces |
| Black | `#000000` | 0, 0, 0 | Headers, strong contrast |
| White | `#ffffff` | 255, 255, 255 | Backgrounds, reversed text |

### Semantic Color Assignments

| Role | Color | Hex |
|------|-------|-----|
| Primary background | Light Gray | `#efeff2` |
| Card background | White | `#ffffff` |
| Primary text | Dark Gray | `#313131` |
| Heading text | Black | `#000000` |
| Primary accent / CTA | Acid Green | `#ceff00` |
| Hover / active state | Lime Green | `#97d600` |
| Error state | Blood Orange | `#ff4500` |
| Muted / disabled | Mid Gray | `#9a9a9a` |
| Border / divider | Soft Gray | `#d0d0d5` |

### CSS Custom Properties

```css
:root {
  /* Brand colors */
  --color-acid-green: #ceff00;
  --color-lime-green: #97d600;
  --color-dark-olive: #5d7400;
  --color-dark-gray: #313131;
  --color-light-gray: #efeff2;
  --color-black: #000000;
  --color-white: #ffffff;

  /* Semantic roles */
  --color-bg: #efeff2;
  --color-surface: #ffffff;
  --color-text: #313131;
  --color-heading: #000000;
  --color-accent: #ceff00;
  --color-accent-hover: #97d600;
  --color-error: #ff4500;
  --color-muted: #9a9a9a;
  --color-border: #d0d0d5;
}
```

---

## D3 Visualization Color Array

*Used in: sunburst/wheel, bubble chart, treemap. Currently placeholder — James to complete full array once Ryan's taxonomy is confirmed.*

```javascript
// PLACEHOLDER — needs full array for all topic categories
// Confirm category list with Ryan before finalizing
const ATLAS_VIZ_COLORS = [
  "#ceff00", // acid green
  "#97d600", // lime green
  "#5d7400", // dark olive
  // [TO COMPLETE — James to provide full array]
];
```

**Topic categories that need color assignments (confirm with Ryan's taxonomy):**
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
- [others — confirm with Ryan]

---

## Typography

### Font Stack

| Role | Family | Source | Use context |
|------|--------|--------|-------------|
| Primary / UI / Data | Hanken Grotesk | Google Fonts | All data views, filters, cards, navigation, labels, tags, buttons |
| Editorial / Long-form | Merriweather | Google Fonts | Pull quotes, creator bios, feature copy, Who We Are, about-style sections |
| Data / Numeric | JetBrains Mono | Google Fonts | Numbers, statistics, raw data, counts, any pure numeric display |

### Google Fonts Import

```css
@import url('https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@400;500&family=Merriweather:wght@400;500&family=JetBrains+Mono:wght@400&display=swap');
```

### Type Scale

*Informed by Material Design 3. Weights capped at 500 (Medium) — nothing heavier. Nothing below 12px on desktop, 13px on mobile.*

| Level | Desktop | Mobile | Weight | Font | Use |
|-------|---------|--------|--------|------|-----|
| Display | 45px | 32px | 400 | Hanken Grotesk | Hero moments only |
| H1 | 32px | 26px | 500 | Hanken Grotesk | Page titles |
| H2 | 24px | 20px | 500 | Hanken Grotesk | Section heads |
| H3 | 18px | 18px | 500 | Hanken Grotesk | Card titles |
| Body | 16px | 16px | 400 | Hanken Grotesk / Merriweather | Default text |
| Label | 14px | 14px | 500 | Hanken Grotesk | Tags, filters, UI labels |
| Data | 14px | 14px | 400 | JetBrains Mono | Numbers, counts, stats |
| Micro | 12px | 13px | 400 | Hanken Grotesk | Captions, timestamps |

### CSS Custom Properties

```css
:root {
  /* Font families */
  --font-ui: 'Hanken Grotesk', sans-serif;
  --font-editorial: 'Merriweather', serif;
  --font-data: 'JetBrains Mono', monospace;

  /* Font sizes — desktop */
  --text-display: 45px;
  --text-h1: 32px;
  --text-h2: 24px;
  --text-h3: 18px;
  --text-body: 16px;
  --text-label: 14px;
  --text-data: 14px;
  --text-micro: 12px;

  /* Font weights */
  --weight-regular: 400;
  --weight-medium: 500;
}

/* Mobile overrides — screens 768px and below */
@media (max-width: 768px) {
  :root {
    --text-display: 32px;
    --text-h1: 26px;
    --text-h2: 20px;
    --text-h3: 18px;
    --text-body: 16px;
    --text-label: 14px;
    --text-data: 14px;
    --text-micro: 13px;
  }
}
```

---

## Spacing & Layout

### Base Unit
**8px** — all spacing values are multiples of this unit.

### Spacing Scale

| Token | Value | Use |
|-------|-------|-----|
| xs | 4px | Tight internal padding, icon gaps |
| sm | 8px | Default internal component padding |
| md | 16px | Card padding, form field spacing |
| lg | 24px | Section breathing room |
| xl | 32px | Large section gaps |
| 2xl | 48px | Page-level vertical rhythm |

### Border Radius

*Material Design 3 aligned — functional, slightly rounded. Not pill-shaped except where explicitly noted.*

| Token | Value | Use |
|-------|-------|-----|
| xs | 4px | Chips, tags, small badges |
| sm | 8px | Buttons, input fields |
| md | 12px | Cards, panels, modals |
| lg | 16px | Larger containers, drawers |
| pill | 100px | Filter pills only — used sparingly |

### Max Content Widths

| Context | Value | Rationale |
|---------|-------|-----------|
| Full layout | 1440px | Optimized for 13-inch MacBook — fills screen without overflow |
| Text column | 640px | ~65–70 characters per line at 16px — optimal reading comfort |

### Mobile-Specific Tokens

| Token | Value | Rationale |
|-------|-------|-----------|
| Touch target minimum | 48×48px | Material Design 3 standard — every interactive element must meet this minimum |
| Mobile edge margin | 16px | Minimum content padding from screen edge on mobile — maps to `--space-md` |

*Justin: every button, filter chip, icon button, and interactive element must have a minimum hit area of 48×48px. If the visible element is smaller, use padding to expand the touch target without changing the visual size.*

### CSS Custom Properties

```css
:root {
  /* Spacing */
  --space-xs: 4px;
  --space-sm: 8px;
  --space-md: 16px;
  --space-lg: 24px;
  --space-xl: 32px;
  --space-2xl: 48px;

  /* Touch targets */
  --touch-target-min: 48px;

  /* Mobile */
  --mobile-edge-margin: 16px;

  /* Border radius */
  --radius-xs: 4px;
  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 16px;
  --radius-pill: 100px;

  /* Layout */
  --max-width-layout: 1440px;
  --max-width-text: 640px;
}
```

---

## Iconography

| Token | Value |
|-------|-------|
| Icon set | Material Symbols |
| Default style | Outlined |
| Active / selected style | Filled |
| Implementation | Variable font — weight, fill, and size controlled via CSS variables |

### Usage Convention
- **Outlined** = default state
- **Filled** = active or selected state
- This gives Justin a clear, implementable rule with no ambiguity

### Material Symbols Import

```html
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" />
```

---

## Component States

### Interactive States
- **Default** — base appearance
- **Hover** — Lime Green `#97d600` accent; subtle background shift
- **Active / Selected** — Acid Green `#ceff00` accent; filled icon variant
- **Disabled** — Mid Gray `#9a9a9a` text and icons; no interaction
- **Focus (keyboard nav)** — visible outline using Acid Green `#ceff00`; never remove focus indicators

### Card States
- **Default** — White `#ffffff` background, Soft Gray `#d0d0d5` border
- **Hover** — slight elevation or border color shift to Lime Green `#97d600`
- **Selected** (pack-builder mode) — Acid Green `#ceff00` border or background tint

---

## Logo Usage

Per the 2025 Style Guide:
- All logo files live in the GitHub repo under `/assets/`
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
- `Journalism_Atlas_icon_green_transparent.png`
- `Journalism_Atlas_icon_black_transparent.png`
- `Journalism_Atlas_icon_white_transparent.png`
- `Journalism_Atlas_favicon.png`

---

## Notes & Decisions Log

| Date | Decision | Rationale |
|------|----------|-----------|
| Feb 2026 | Hanken Grotesk as primary font | Clean, geometric, works well at small sizes for data-dense UI |
| Feb 2026 | Acid green (#ceff00) as primary accent | Brand differentiation, energy, established in Style Guide |
| Mar 2026 | Blood Orange (#ff4500) as error state | Warm, distinct, rhymes with Acid Green energy without competing |
| Mar 2026 | Mid Gray (#9a9a9a) as muted/disabled | Neutral de-emphasis, within existing gray family |
| Mar 2026 | Soft Gray (#d0d0d5) as border/divider | Subtle but visible; between bg and text without introducing new color |
| Mar 2026 | Merriweather scoped to editorial contexts only | Hanken Grotesk dominates data UI; Merriweather for bios, long-form, about copy |
| Mar 2026 | JetBrains Mono for numeric/data display | Designed for figure legibility; clear typographic register for raw data |
| Mar 2026 | Type scale weights capped at 500 | Material Design 3 principle — Regular and Medium only; nothing heavy |
| Mar 2026 | 8px base spacing unit | Aligns with Material Design 3 grid; invisible but felt consistency |
| Mar 2026 | 1440px max layout width | Optimized for 13-inch MacBook Pro/Air logical resolution |
| Mar 2026 | Material Symbols replacing Material Icons | Current Google standard; variable font = one dependency, more control |
| Mar 2026 | Outlined icons default, Filled for active states | Clean convention Justin can implement without judgment calls |
| Mar 2026 | Responsive type scale added — mobile overrides at 768px breakpoint | Display/H1/H2 too large for 390px mobile screens; Micro bumped to 13px for mobile legibility |
| Mar 2026 | 48×48px minimum touch target | Material Design 3 standard; critical for creator-journalists using site on mobile |
| Mar 2026 | 16px mobile edge margin | Prevents content running edge-to-edge on small screens; maps to --space-md |
