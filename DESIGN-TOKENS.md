# Atlas Design Tokens
*Canonical design reference — committed to repo as source of truth for implementation*

*Last updated: April 2026*
*Owner: James (james@happicamp.com)*

> **How this file works:** This is the single source of truth for all visual decisions. When Justin implements design changes with Claude Code, he references this document. If it's not here, it doesn't get implemented. If it changes here, it changes everywhere. Fill in any blanks marked [TO CONFIRM] and update as needed.

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
| Error state | [TO CONFIRM] | |
| Muted / disabled | [TO CONFIRM] | |
| Border / divider | [TO CONFIRM] | |

---

## D3 Visualization Color Array

*Used in: sunburst/wheel, bubble chart, treemap. Currently improvised — James should own this palette.*

```javascript
// CURRENT PLACEHOLDER — needs James's sign-off
const ATLAS_VIZ_COLORS = [
  "#ceff00", // acid green
  "#97d600", // lime green
  "#5d7400", // dark olive
  // [TO COMPLETE — James to provide full array for all topic categories]
];
```

**Topic categories that need color assignments:**
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

### Font Stack

| Role | Family | Notes |
|------|--------|-------|
| Primary / UI | Hanken Grotesk | Google Fonts — confirmed in use |
| Secondary / editorial | Merriweather | Google Fonts — [TO CONFIRM: still in use?] |
| Monospace (if any) | [TO CONFIRM] | |

### Type Scale

*[TO FILL IN — James to confirm or define]*

| Level | Size | Weight | Use |
|-------|------|--------|-----|
| Display | | | Hero headings |
| H1 | | | Page titles |
| H2 | | | Section heads |
| H3 | | | Card titles |
| Body | | | Default text |
| Small | | | Meta, labels, tags |
| Micro | | | Captions, timestamps |

### Font Weights in Use
*[TO CONFIRM — list weights James has approved]*
- 400 (regular)
- 600 (semibold)?
- 700 (bold)?
- 800 (extrabold)?

---

## Spacing & Layout

*[TO FILL IN — James to define or confirm]*

### Base Unit
Base spacing unit: [TO CONFIRM — e.g., 4px or 8px]

### Spacing Scale
```
xs:  
sm:  
md:  
lg:  
xl:  
2xl: 
```

### Border Radius
```
card:    
button:  
pill/tag: 
```

### Max Content Width

All pages and layouts site-wide are capped at 1440px. Content should be centered within the viewport at wider screen sizes — the background may extend edge-to-edge but the content wrapper must not exceed this maximum. This applies to the homepage, all subpages, and any new pages or products (including Unf*ck Your Algorithm, Starter Packs, etc.).

```
full layout:  1440px  /* Hard cap — applies to all pages, site-wide */
text column:  720px   /* Long-form text, editorial content */
card grid:    1320px  /* Leaves 60px padding each side at full layout width */
```

**Implementation note for Justin:** Apply `max-width: 1440px; margin: 0 auto;` to the top-level layout wrapper on every page. The card grid and text column widths nest inside that wrapper and should also be centered with `margin: 0 auto`.

---

## Iconography

- **Icon set:** Material Icons (currently in use — [TO CONFIRM: still the approved set?])
- **Icon size defaults:** [TO CONFIRM]
- **Icon weight/style variant:** [TO CONFIRM — outlined, filled, rounded?]

---

## Component States

*[TO FILL IN — define for cards, buttons, filters, tags]*

### Interactive States
- Default
- Hover
- Active / Selected
- Disabled
- Focus (keyboard nav)

### Card States
- Default
- Hover
- Selected (in pack-builder mode)

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

*Append decisions here so there's a record of why things are the way they are.*

| Date | Decision | Rationale |
|------|----------|-----------|
| Feb 2026 | Hanken Grotesk as primary font | Clean, geometric, works well at small sizes for data-dense UI |
| Feb 2026 | Acid green (#ceff00) as primary accent | Brand differentiation, energy, established in Style Guide |
| Apr 2026 | Max layout width set to 1440px site-wide | 13-inch MacBook as design reference; prevents content from stretching on large monitors |
