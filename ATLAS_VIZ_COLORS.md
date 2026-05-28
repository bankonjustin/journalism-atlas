# ATLAS_VIZ_COLORS — Confirmed Color Array
*Blocker 2 resolution · May 2026 · Signed off by James*

---

## JavaScript Array — commit to repo

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
  // NOTE: these three have contrast warnings on pure black backgrounds —
  // do not activate without first adjusting luminosity to match the confirmed set.

  "Reserve A":              "#ea80fc",  // light magenta    ⚠ needs darkening before use
  "Reserve B":              "#40c4ff",  // light cyan       ⚠ needs darkening before use
  "Reserve C":              "#ffab40",  // light amber      ⚠ needs darkening before use

};
```

---

## Flat array (if D3 needs an ordered list rather than a map)

```javascript
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

---

## Key decisions log

| Decision | Rationale |
|----------|-----------|
| Politics → warm slate `#78909c`, not red or blue | Red and blue carry partisan associations in the US context; slate reads as civic/institutional without party coding |
| Environment → teal-green `#26a69a`, not brand green | Prevents confusion with Atlas brand greens (acid `#ceff00`, lime `#97d600`, olive `#5d7400`) |
| Sports → bold blue `#2196f3` | Conventional sports data viz association; opened up once Politics vacated the blue family |
| Science → denim blue-gray `#5b7fa6` | Previous assignment (`#7cb342`) too close to brand greens; blue-gray reads as analytical/empirical |
| Technology → `#ba55cc` (lightened from `#ab47bc`) | Original too dark relative to palette; lifted +4% lightness |
| Culture & Arts → `#ef0e61` (desaturated from `#f50057`) | Original too saturated relative to palette; midpoint between full and -20% saturation |
| Luminosity target | Palette calibrated to James's preferred range (~50–65% HSL lightness); darker colors lifted to match rather than lightening the reference group |
| Reserve slots carry contrast warnings | Three unassigned reserves are intentionally lighter as placeholders; must be adjusted before activating against dark backgrounds |
| Acid green `#ceff00` excluded | Reserved strictly for CTAs and active states; never used as a category color |
| Error red excluded | Reserved for system feedback states only |
