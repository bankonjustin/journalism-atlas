# Atlas Design Tokens
*Canonical design reference — committed to repo as source of truth for implementation*

*Last updated: May 2026*
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
| Secondary text on dark surfaces | Mid Gray | `#bdbdbd` |
| Error state | [TO CONFIRM] | |
| Muted / disabled | [TO CONFIRM] | |
| Border / divider | [TO CONFIRM] | |

> **Scope note — secondary text on dark surfaces (`#bdbdbd`):** Applies to all secondary/label text rendered on black or near-black backgrounds. Current applications: footer section headers (EXPLORE, ABOUT, CONNECT), dark-background homepage sections, Bluesky Creator Intelligence page secondary text. This is the site-wide floor for this context—do not use values darker than `#bdbdbd` for secondary text on dark surfaces. Contrast ratio on `#000000` is ~6.0:1 (WCAG AA compliant). Any instance currently set to `#a8a8a8` on dark surfaces should be updated to `#bdbdbd`.

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
| Secondary / editorial | Merriweather | Google Fonts — confirmed in use |
| Monospace / data & numeric | JetBrains Mono | Google Fonts |

### Type Scale

*[TO FILL IN — James to confirm or define]*

| Level | Size | Weight | Use |
|-------|------|--------|-----|
| Display | 36px | 800 | Hero headings |
| H1 | 28px | 700 | Page titles |
| H2 | 22px | 700 | Section heads |
| H3 | 16px | 700 | Card titles |
| Body | 17px | 400 | Default reading text |
| Small | 15px | 400 | Meta, labels, tags |
| Micro | 13px | 400 | Captions, timestamps |
| Editorial body | 18px | 400 | Merriweather — long-form editorial only |

### Font Weights in Use
- 400 (regular)
- 700 (bold)
- 800 (extrabold)

Note: 500 and 600 are not approved.

---

## Spacing & Layout

### Base Unit
Base spacing unit: 4px

### Spacing Scale
```
xs:  4px
sm:  8px
md:  16px
lg:  24px
xl:  40px
2xl: 64px
```

### Border Radius
```
card:     6px
button:   6px
pill/tag: 9999px
```

### Max Content Width
```
full layout: 1440px
text column: 720px
card grid:   1440px
```

---

## Iconography

- **Icon set:** Material Symbols Outlined
- **Style variant:** Outlined (default), Filled (active states only)
- **Icon size defaults:** [TO CONFIRM]

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
| May 2026 | Secondary text on dark surfaces → `#bdbdbd` | Footer EXPLORE/ABOUT/CONNECT labels reading below WCAG AA on black. `#bdbdbd` (~6.0:1 on #000) chosen over bare AA floor (`#a8a8a8`, 4.5:1) because small all-caps widely-spaced labels need more contrast than body-weight text at the same size. Supersedes any previous per-page `#a8a8a8` usage on dark surfaces. Applied globally: footer, dark homepage sections, Bluesky Creator Intelligence. |
| May 2026 | Typography scale and spacing confirmed | James via #atlas-design May 7 2026. Display 36/800 through Micro 13/400. Spacing base 4px. Border radius 6px/9999px. Max width 1440px. |
| May 2026 | Font weights: 400, 700, 800 only | 500 and 600 removed from approved set. Supersedes CLAUDE.md which previously listed 400/500/700. |
| May 2026 | JetBrains Mono added as monospace font | For data and numeric contexts. Third confirmed typeface alongside Hanken Grotesk and Merriweather. |
