# Atlas Design Tokens — v8
*Canonical design reference — committed to repo as source of truth for implementation*

*Last updated: May 2026*
*Previous version: v7 (May 2026)*
*Owner: James (james@happicamp.com)*

> **How this file works:** This is the single source of truth for all visual decisions. When Justin implements design changes with Claude Code, he references this document. If it's not here, it doesn't get implemented. If it changes here, it changes everywhere.

---

## Color Palette

### Brand Colors (from Style Guide 2026)

| Name | Hex | sRGB | Use |
|------|-----|------|-----|
| Acid Green | `#ceff00` | 206, 255, 0 | Primary accent, CTAs, active states — one per screen composition maximum |
| Lime Green | `#97d600` | 151, 214, 0 | Hover states only |
| Dark Olive | `#5d7400` | 93, 116, 0 | Tertiary / deep accent |
| Dark Gray | `#313131` | 49, 49, 49 | Primary text, UI elements |
| Light Gray | `#efeff2` | 239, 239, 242 | Backgrounds, secondary surfaces |
| Black | `#000000` | 0, 0, 0 | Site header (always), headings, strong contrast |
| White | `#ffffff` | 255, 255, 255 | Card backgrounds, reversed text |

### Semantic Color Assignments

| Role | Hex | Notes |
|------|-----|-------|
| Primary background | `#efeff2` | Light Gray |
| Card background | `#ffffff` | White |
| Primary text | `#313131` | Dark Gray |
| Heading text | `#000000` | Black |
| Secondary text (light surfaces) | `#6b6b6b` | |
| Secondary text (dark surfaces) | `#bdbdbd` | Minimum for small all-caps labels — do not go lighter |
| Primary accent / CTA | `#ceff00` | Acid Green — never use as success/go signal |
| Hover state | `#97d600` | Lime Green — hover only, never default state |
| Error state | `#f50000` | Near-pure red — reserved for validation, destructive actions, failed states |
| On-error (text on error) | `#ffffff` | White |
| Muted / disabled | `#9e9e9e` | |
| Border / divider | `#bdbdbd` | |
| Site header background | `#000000` | Always black, site-wide constant regardless of page background |

---

## D3 Visualization Color Array

*Used in: sunburst/wheel, bubble chart, treemap, and all future data visualizations.*
*Locked May 2026. Probable additions pending Ryan taxonomy confirmation before activation.*
*Full rationale and decisions log: `ATLAS_VIZ_COLORS.md`*

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
  // ⚠ Contrast warning on pure black — adjust luminosity before activating.

  "Reserve A":              "#ea80fc",  // light magenta
  "Reserve B":              "#40c4ff",  // light cyan
  "Reserve C":              "#ffab40",  // light amber

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
- Acid green `#ceff00` is excluded from the viz palette — reserved for CTAs and active states only
- Error red is excluded — reserved for system feedback states only
- All confirmed colors pass contrast on both white and black backgrounds
- Luminosity target: ~50–65% HSL lightness across the confirmed set
- Do not activate probable additions until Ryan confirms category names and slugs

---

## Typography

### Font Stack

| Role | Family | Notes |
|------|--------|-------|
| Primary / UI | Hanken Grotesk | Google Fonts — confirmed |
| Monospace | DM Mono | Google Fonts — confirmed, replaces JetBrains Mono |
| Secondary serif | Merriweather | Retired from active use — reintroduce only if a specific serif use case arises |

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
The type scale only works if all levels play their part consistently. In Pulse cards specifically:
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
```

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

**Reference points:** Bloomberg (~1280px) and Wired (~1440px) are the design benchmarks. The Atlas targets Wired's contained-but-generous feel. Content should never sprawl to screen edges on large monitors.

---

## Iconography

- **Icon set:** Material Symbols Outlined — confirmed
- **Icon weight/style variant:** Outlined only — never filled
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
- Hover — Lime Green `#97d600`
- Active / Selected — Acid Green `#ceff00`
- Disabled — Muted Gray `#9e9e9e`
- Focus (keyboard nav) — `2px solid #97d600`, offset `2px` — consistent with hover state token; lime green focus ring is on-system and WCAG AA compliant

### Card States
- Default
- Hover
- Selected (in pack-builder mode)

---

## Logo Usage

Per the 2026 Style Guide:
- Logo asset master library: Google Drive folder `1BT48q5ng6FN0Y0e_XllWvNrI0LFmL_tN`
- Transparent PNGs sized at 500×500px (icons) and 3000×3000px (full logos)
- Contact james@happicamp.com for larger sizes or alternate formats
- **Footer logo height standard: 40px** — applied to the `img` element directly, not its container
- **Horizontal stacked lockup** = globe-plus-wordmark arranged horizontally (globe left, stacked wordmark right) — canonical name for that asset
- **Correct footer asset:** `Journalism_Atlas_wordmark_stacked_white.png`
- **Footer logo CSS — full required ruleset:**

```css
/* Target the img element directly — this controls the actual rendered size */
.footer-wordmark,
.site-footer .footer-brand img {
  height: 40px;
  width: auto;
  display: block;
  border: none;
  outline: none;
  box-shadow: none;
}

/* Target the logo's parent container — removes the vertical divider line */
.site-footer .footer-brand {
  border: none;
  border-right: none;
  border-left: none;
  padding-right: 0;
}
```

> ⚠ The `border-right` on the container is the cause of the white vertical line to the right of the logo. The `height: 40px` must be on the `img` tag itself — if applied to the container it will not scale the image.

**Available logo variants (confirmed in repo):**
- `Journalism_Atlas_logo_black.png`
- `Journalism_Atlas_logo_acid_green.png`
- `Journalism_Atlas_logo_dark_gray.png`
- `Journalism_Atlas_logo_light_gray.png`
- `Journalism_Atlas_wordmark_horizontal_lockup_black.png` — site header (white/light background)
- `Journalism_Atlas_wordmark_horizontal_lockup_white.png` — do not use in footer
- `Journalism_Atlas_wordmark_stacked_black.png`
- `Journalism_Atlas_wordmark_stacked_white.png` — **correct footer asset**
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
| Feb 2026 | Acid green `#ceff00` as primary accent | Brand differentiation, energy, established in Style Guide |
| May 2026 | DM Mono confirmed as monospace font | Replaces JetBrains Mono per HOW_WE_BUILD.md |
| May 2026 | Merriweather retired from active font stack | No current serif use case; reintroduce if one arises |
| May 2026 | Spacing base unit confirmed as 4px | Per HOW_WE_BUILD.md |
| May 2026 | Spacing xl → 32px, 2xl → 48px | Tightened from xl=40, 2xl=64; better density at large viewports |
| May 2026 | Border radius: 6px cards/buttons, 9999px pills/tags | Per HOW_WE_BUILD.md |
| May 2026 | Material Symbols Outlined confirmed as icon set | Replaces earlier Material Icons reference |
| May 2026 | Icon sizes locked: nav 24px, card header 24px, inline 18px, section header 28px | M3 standard sizing adapted for data-dense UI |
| May 2026 | Error state `#f50000` | Near-pure red — needs to grab attention immediately; M3 baseline `#b3261e` too dull |
| May 2026 | Muted/disabled `#9e9e9e` | Balanced contrast on both light and dark surfaces |
| May 2026 | Border/divider `#bdbdbd` | 1px lines at this value readable and appropriately subtle on both surfaces |
| May 2026 | Secondary text (dark surfaces) `#bdbdbd` | Small all-caps labels need more contrast than bare WCAG AA floor |
| May 2026 | D3 viz color array locked (9 confirmed + 6 probable + 3 reserve) | See ATLAS_VIZ_COLORS.md for full decisions log |
| May 2026 | Politics & Govt → `#78909c` warm slate | Red/blue carry partisan US associations; slate reads as civic/institutional |
| May 2026 | Environment → `#26a69a` teal-green | Prevents confusion with brand greens (acid/lime/olive family) |
| May 2026 | Acid green excluded from viz palette | Reserved for CTAs and active states only — never a category color |
| May 2026 | Site header always `#000000` | Site-wide constant regardless of page background |
| May 2026 | Footer logo height standard: 40px | Established during footer logo bug fix |
| May 2026 | Footer logo: `Journalism_Atlas_wordmark_stacked_white.png` | Footer has reverted twice to horizontal lockup — correct asset is stacked white; CSS fix lives in header.css |
| May 2026 | Card feature treatments apply to containers, never cards themselves | Cards must remain consistent; clicking anywhere except explicit external links stays on-site |
| May 2026 | Type scale locked: Display 48px / H1 36px / H2 28px / H3 20px / Body 16px / Small 13px / Micro 11px | Body anchored at 16px — comfortable reading baseline; H3 lifted to 20px/600 restores card hierarchy in Pulse cards |
| May 2026 | H3 at 20px/600 is highest-impact change | Article titles in Pulse cards were collapsing into same visual band as meta text; 20px/semibold restores clear card hierarchy |
| May 2026 | Micro at 11px requires weight 500 minimum | Small all-caps labels (TECH, CULTURE etc.) need compensating weight at this size for legibility; always letter-spaced 0.08–0.1em |
| May 2026 | Font weights: 400/500/600/700/800 | 500 added back for Micro; 600 added for H3/semibold; 900 excluded |
| May 2026 | Line heights specified per level | Display 1.1, H1 1.2, H2 1.25, H3 1.3, Body 1.6, Small 1.5, Micro 1.4 — tighter at large sizes, looser at reading sizes |
| May 2026 | Max content widths locked: full layout 1440px, card grid 1200px, text column 680px | Site was sprawling to screen edges on 27" monitors; 1440px ceiling aligns with Wired (benchmark); card grid at 1200px gives comfortable margin inside 1440px outer; text column at 680px = ~70 char reading measure at 16px body |
| May 2026 | Focus ring locked: `2px solid #97d600`, offset `2px` | Lime green is on-system (matches hover token), WCAG AA compliant |
| May 2026 | Footer white vertical line — `border-right` on logo container, not the img element | Previous fix only addressed img-level borders; container border must also be explicitly cleared |
| May 2026 | Footer `height: 40px` must target the `img` element directly | Applied to container it does not scale the image — selector precision critical |
