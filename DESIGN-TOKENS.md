# Atlas Design Tokens — v7
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
| Dark Olive | `#5d7400` | 93, 116, 0 | Tertiary / deep accent; eyebrow labels on light surfaces |
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
| Eyebrow / overline label — on light surfaces | Dark Olive | `#5d7400` |
| Eyebrow / overline label — on dark surfaces | Lime Green | `#97d600` |
| Secondary text on dark surfaces | Mid Gray | `#bdbdbd` |
| Error state | [TO CONFIRM] | |
| Muted / disabled | [TO CONFIRM] | |
| Border / divider | [TO CONFIRM] | |

> **Contrast rule — eyebrow labels (WCAG AA):** `#97d600` on white (`#ffffff`) or light gray (`#efeff2`) produces ~2.5:1 contrast — an accessibility failure. Use `#5d7400` (Dark Olive) for all small all-caps labels, eyebrows, and overlines on light surfaces. `#97d600` is approved on black or dark backgrounds only. Implemented May 2026.

> **Secondary text on dark surfaces (`#bdbdbd`):** Applies to all secondary/label text on black or near-black backgrounds (footer section headers, dark homepage sections). Contrast ratio on `#000000` is ~6.0:1 (WCAG AA). Do not use values darker than `#bdbdbd` for secondary text on dark surfaces.

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
| Monospace / numeric data | DM Mono | Google Fonts — replaces JetBrains Mono (May 2026). Lighter, more editorial feel. |

### Type Scale

*Confirmed May 7 2026 via James (#atlas-design).*

| Level | Size | Weight | Use |
|-------|------|--------|-----|
| Display | 36px | 800 | Hero headings |
| H1 | 28px | 700 | Page titles |
| H2 | 22px | 700 | Section heads |
| H3 | 16px | 700 | Card titles |
| Body | 17px | 400 | Default reading text |
| Small | 15px | 400 | Meta, labels, tags |
| Micro | 13px | 400 | Captions, timestamps |

> **Font size floor:** No UI element, label, tag, timestamp, or metadata string renders below 13px. Applied globally in `main.css` and `header.css` (May 2026 QA session). DM Mono decorative structural elements (axis ticks, matrix abbreviations, footer legal line, eyebrow dividers) are exempt from the 13px floor — these are intentional design decisions, not oversights. Do not change without confirming with James.

### Font Weights in Use
- **400** — Regular. Body copy, default UI text.
- **700** — Bold. Emphasis, subheadings, card titles.
- **800** — Extrabold. Display text, hero headings, primary labels.

*Note: 500, 600, and 900 are not in the system. Do not use.*

---

## Spacing & Layout

*Confirmed May 7 2026 via James (#atlas-design).*

### Base Unit
Base spacing unit: **4px** — all spacing values are multiples of 4px.

### Spacing Scale
```
xs:   4px
sm:   8px
md:   16px
lg:   24px
xl:   40px
2xl:  64px
```

### Border Radius
```
card:     6px
button:   6px
pill/tag: 9999px
```

### Max Content Width
```
full layout:  1440px
text column:  720px
card grid:    1440px
```

> **Reference device:** MacBook Air 13-inch M2 is the primary design reference. 27-inch external monitor is used to verify the 1440px max-width constraint holds at large viewports. Enforced across all page layout wrappers (May 2026).

---

## Iconography

- **Icon set:** Material Symbols Outlined — confirmed. Filled variant for active states only.
- **Icon size defaults:** [TO CONFIRM — James]
- **Icon weight/style variant:** Outlined (default); Filled (active states only)
- **Section header icons:** Circular, 40px diameter, `border-radius: 50%`, `flex-shrink: 0` — confirmed May 2026

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
- All logo files live in the GitHub repo under `assets/images/logos/`
- Transparent PNGs sized at 500×500px
- Contact james@happicamp.com for larger sizes or alternate formats

**Available logo variants (confirmed in repo):**

*Wordmark lockups — confirmed usage contexts:*
- `Journalism_Atlas_wordmark_horizontal_lockup_black.png` — site header (white/light background)
- `Journalism_Atlas_wordmark_horizontal_lockup_white.png` — footer (black background)
- `Journalism_Atlas_wordmark_stacked_green_white (3).png` — hero section on search.html
- `Journalism_Atlas_wordmark_stacked_black.png`
- `Journalism_Atlas_wordmark_stacked_white.png`
- `Journalism_Atlas_wordmark_stacked_gray.png`
- `Journalism_Atlas_wordmark_stacked_green_white.png`

*Logomark only:*
- `Journalism_Atlas_logo_acid_green.png`
- `Journalism_Atlas_logo_black.png`
- `Journalism_Atlas_logo_dark_gray.png`
- `Journalism_Atlas_logo_light_gray.png`
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
| May 2026 | Typography scale confirmed | James via #atlas-design May 7 2026. Display 36/800 through Micro 13/400. |
| May 2026 | Spacing scale confirmed | James via #atlas-design May 7 2026. Base 4px. xl=40px, 2xl=64px. Border radius 6px/9999px. |
| May 2026 | Max content width: 1440px full layout, 720px text column | James via #atlas-design May 7 2026. Enforced across all page layout wrappers. |
| May 2026 | Font weights locked to 400/700/800 only | Eliminates ambiguity between emphasis levels; 500/600/900 explicitly excluded |
| May 2026 | DM Mono as monospace font (replaces JetBrains Mono) | Lighter, more editorial feel; confirmed in HOW_WE_BUILD.md |
| May 2026 | Merriweather retired from font stack | Not in active use; serif role is vacant by design. Reintroduce only if a specific editorial use case requires it |
| May 2026 | Icons: Material Symbols Outlined; Filled for active states | Replaces legacy Material Icons reference |
| May 2026 | #97d600 prohibited on light surfaces for small text | Fails WCAG AA contrast (~2.5:1 on white/light gray). Use #5d7400 (Dark Olive) for all eyebrow/overline labels on light backgrounds. Implemented in QA session. |
| May 2026 | Secondary text on dark surfaces → #bdbdbd | Footer labels reading below WCAG AA on black. #bdbdbd (~6.0:1 on #000) chosen over bare AA floor (#a8a8a8, 4.5:1) because small all-caps widely-spaced labels need more contrast than body-weight text at equivalent size. |
| May 2026 | Font size floor: 13px minimum for all UI elements | WCAG AA compliance. Applied globally in main.css and header.css. DM Mono structural decoratives exempt by design. |
| May 2026 | Section header icons: 40px diameter circle | Standardized across Research & Writing page. Apply to any new section header icons. |
| May 2026 | DM Mono structural decoratives exempt from 13px floor | Axis ticks, matrix abbreviations, footer legal line, eyebrow dividers are structural — not content. Intentional design decisions confirmed in QA session. |
