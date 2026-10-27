# Pulse tokens (Phase 2, hero)

Built on the v15 neutrals in `assets/css/variables.css`. Light values are the page's existing colours; dark values use the v15 dark neutrals.

| Token | Light | Dark | Used for |
|---|---|---|---|
| `--p-surface` | #ffffff | #121212 (neutral-7) | cards, bands, panels (was hard-coded #fff / #fafafa) |
| `--p-surface-2` | #f4f4f6 | #1c1c1c | secondary fills |
| `--p-fill` | #e4e4e8 | #3a3a3a | tracks, chips |
| `--p-border` | #d4d4d8 | #5e5e5e (neutral-5) | hairlines |
| `--p-ink` | #1a1a1a | #efefef (neutral-2) | primary text on surfaces |
| `--p-ink-2` | #5e5e5e | #c6c6c6 (neutral-3) | secondary text |
| page background | #efefef (`--color-bg`) | #303030 (neutral-6) | body |

- Switching: `prefers-color-scheme`, with `data-theme="light|dark"` on `<html>` as an override hook (no toggle UI yet).
- The masthead and The Line are dark in both schemes. Acid (#ceff00) is the "live" colour on dark: the Line stroke, the end-point, creator names in the lede.
- Trend-down text in dark: #ffbc00 (`--color-display-dark`), because #b45309 fails contrast on dark.
- Reduced motion: all animation and transition durations collapse, the ticker stops, smooth scroll becomes instant, and The Line's draw-in plays only under `no-preference`.
- Colour never codes beats or content types on the page. Beat colour is chart-only (see `beats.proposed.json`, not approved, not used).
- Not yet converted to the tokens (Phase 3 sweep, found by search for hard-coded greys): `#888`, `#aaa`, `#bbb` text on surfaces that are not the masthead. Lighthouse contrast in dark: 0 failures; in light: 1 pre-existing (`.pulse-brands-cta-sub`, #888 on white).
