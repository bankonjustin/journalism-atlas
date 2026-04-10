# Atlas Design Tokens
*Canonical design reference — committed to repo as source of truth for implementation*

*Last updated: April 2026*
*Owner: James (james@happicamp.com)*

> **How this file works:** This is the single source of truth for all visual decisions. When Justin implements design changes with Claude Code, he references this document. If it's not here, it doesn't get implemented. If it changes here, it changes everywhere. Fill in any blanks marked [TO CONFIRM] and update as needed.

---

## Color Palette

### Design Philosophy

The Atlas is a tool, not an experience. The visual language is primarily black and white, with color used sparingly and deliberately — for impact, to signal interaction, or to aid navigation. Color should never be decorative.

This system follows Material Design 3 conventions for primary, secondary, and tertiary color roles. When in doubt, use less color, not more.

---

### Brand Colors (from Style Guide 2026)

| Name | Hex | sRGB | Role |
|------|-----|------|------|
| Acid Green | `#ceff00` | 206, 255, 0 | Primary — CTAs and active states only |
| Lime Green | `#97d600` | 151, 214, 0 | Tertiary — hover states only |
| Dark Gray | `#313131` | 49, 49, 49 | Secondary — UI chrome, labels, borders |
| Light Gray | `#efeff2` | 239, 239, 242 | Surface — page background |
| Black | `#000000` | 0, 0, 0 | Heading text, dark surfaces (footer, dark headers) |
| White | `#ffffff` | 255, 255, 255 | Card background, reversed text |

**Retired from UI use:**
- `#5d7400` (Dark Olive) — too close to other greens, insufficient contrast at small sizes. Reserved for potential future use only.
- `#00a896` (Teal) — was used on beat pages. Removed. Not part of the Atlas palette.

---

### Semantic Color Assignments

| Role | Color | Hex | Notes |
|------|-------|-----|-------|
| Page background | Light Gray | `#efeff2` | Default surface for all pages |
| Card background | White | `#ffffff` | All card variants |
| Primary text | Dark Gray | `#313131` | Body copy, labels, meta |
| Heading text | Black | `#000000` | Page titles, card titles, nav |
| Dark surface | Black | `#000000` | Footer, dark partner headers |
| Primary CTA / Active state | Acid Green | `#ceff00` | See critical usage rule below |
| Hover state | Lime Green | `#97d600` | Resting → hover transition only |
| UI chrome / borders / secondary buttons | Dark Gray | `#313131` | Filter chips, dividers, outlines |
| Disabled / muted | Dark Gray at 40% opacity | `#313131` at `opacity: 0.4` | Inactive states |
| Border / divider | `#d4d4d8` | `#d4d4d8` | Subtle separators in dense data views |

---

### ⚠️ Critical Usage Rule — Acid Green `#ceff00`

**Acid green must never appear in a context where it could be read as a "go" or "success" signal.**

The color sits in the yellow-green range and carries universal "go" associations. Misuse will confuse users who expect green to mean success, confirmation, or completion.

**Permitted uses:**
- The primary CTA button on a screen (one per screen composition, maximum)
- Active/selected state in navigation (e.g. current page indicator)
- Selected state on a card in pack-builder mode

**Never use for:**
- Success messages or confirmation states
- Completion indicators (e.g. "you followed this creator")
- Any state that communicates "done" or "approved"
- Decorative purposes
- More than one element per screen composition

---

### Status Colors (Outside Brand Palette)

Status colors carry universal meaning. They exist entirely outside the brand palette and are never used for decorative or navigational purposes.

| State | Color | Hex | Use |
|-------|-------|-----|-----|
| Success / Confirmed | System Green | `#1e8a3c` | Form success, follow confirmed |
| Warning / Caution | Amber | `#f59e0b` | Non-critical alerts, incomplete states |
| Error / Destructive | System Red | `#d32f2f` | Form errors, failed actions, destructive confirmations |

These colors do not appear in navigation, cards, filters, or visualizations under any circumstances.

---

### Visualization Colors (D3 — Secondary Palette)

The secondary brand palette is reserved exclusively for D3 visualizations (sunburst/wheel, bubble chart, treemap). These colors never appear in UI chrome, navigation, cards, or any interactive element.

```javascript
// ATLAS_VIZ_COLORS — secondary palette, visualization use only
// Assignment to topic categories pending Ryan's confirmed taxonomy
const ATLAS_VIZ_COLORS = [
  "#fff700", // yellow
  "#ff9600", // orange
  "#ff66ff", // pink-lilac
  "#ff33cc", // hot pink
  "#00e5ff", // cyan
  "#806600", // dark gold
  "#b35100", // burnt orange
  "#a100a1", // purple
  "#a1006c", // magenta
  "#005ea3", // blue
  // [TO COMPLETE — assign to topic categories once Ryan confirms taxonomy]
];
```

**Note:** Acid Green `#ceff00`, Lime Green `#97d600`, and Dark Olive `#5d7400` are intentionally excluded from the visualization array. Primary brand colors do not appear in the data layer.

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
```
full layout:  
text column:  
card grid:    
```

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

Per the 2026 Style Guide:
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
| Apr 2026 | Acid green restricted to CTA/active states only | Overuse was diluting brand signal; color should indicate function, not decorate |
| Apr 2026 | Acid green never used as success/go signal | Color's yellow-green range creates ambiguity with universal "go" semantics |
| Apr 2026 | Lime green demoted to hover-only | Tertiary role per M3 conventions; never appears in resting state |
| Apr 2026 | Dark Olive retired from UI | Insufficient contrast at small sizes; too close to other greens |
| Apr 2026 | Teal #00a896 removed from beat pages | Was not part of Atlas palette; was legacy drift |
| Apr 2026 | Status colors outside brand palette | Red/amber/green carry universal meaning independent of brand; mixing creates confusion |
| Apr 2026 | Secondary palette reserved for D3 only | Separation keeps UI chrome clean; makes visualization colors feel intentional when they appear |
| Apr 2026 | Black serves dual role: heading text + dark surfaces | Consistent with M3 surface/on-surface model |
