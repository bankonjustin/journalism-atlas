# Atlas Pulse and For Brands Brief — Bringing the New Pages onto v16

*Developer brief for Claude Code · Owner: James Bareham, Creative Director · For: Justin Bank · October 27, 2026*
*Implements DESIGN-TOKENS-v16.md and ATLAS-BRAND-GUIDE-v5.md. Introduces no new values. Replaces the earlier draft, Atlas-Typography-Fix-Brief-2026-10.md.*

**Pages:** `pulse.html` (commit `c3e416a`) and `for-brands.html` (commit `fb98a6d`), both published October 27, 2026.
**Prerequisites:** `Atlas-Foundation-Lock-Brief-2026-10.md` merged; Phase A (shared header and footer) of `Atlas-Type-Consolidation-Brief-2026-10.md` merged.

---

## 1. Summary

Both pages set every headline, subhead and display statistic in Merriweather Bold. Under v16, every heading is Inter, and Merriweather is body prose in editorial articles only (Watershed, long-form reports). Neither page is an editorial article.

Both pages also break other v15 rules that v16 now locks: pill tags, a Lime Green eyebrow, Acid Green at rest used to mean "live," labels at 12px with 0.14em spacing, transparent-white text, page-local tokens with off-system grays, a page-only dark mode, and chart colors for content types.

### How it happened
Justin's redesign brief specified Playfair Display, DM Sans and Space Mono with an orange "live" accent. Claude Code flagged the conflict with v15 and chose v15, but implemented it as a font-for-font swap: Playfair (a display serif) became Merriweather, v15's only serif. Its ledger records this as "Merriweather for the argument." Nothing stopped it. v15 didn't say which face headings use, `CLAUDE.md` was silent on Merriweather, `WORKFLOW.md` sent design calls to Justin rather than to the token owner, and the build didn't check type. Pulse then copied For Brands' headline style a day later.

v16 and the foundation brief close each of those gaps. This brief fixes the two pages.

### Interim defaults
Where v16 doesn't define something these pages use, the fix below applies the nearest **v16 role**, never a new value, and the item is listed in section 6 for James and Justin's next update. Per v16, undefined means unbuilt.

---

## 2. Fix: `for-brands.html`

### 2.1. Font loading (lines 27–28, 32–40)

Delete both Google Fonts links (`preload` and `<noscript>`): `header.js` loads the site fonts (DESIGN-TOKENS-v16.md § Font Loading).

Delete the page's local `@font-face` fallbacks and its inline `:root` font block (lines 37–40): `variables.css` now defines `--font-primary`, `--font-heading`, `--font-mono` and the fallbacks.

Replace the header comment (lines 32–35) with:
```css
/* /for-brands. Tokens only: docs/design/DESIGN-TOKENS-v16.md.
   Headings and UI: Inter (--font-heading / --font-primary). All-caps labels and tags: Source Code Pro 500 (--font-mono).
   No Merriweather: this is not an editorial article. */
```

### 2.2. Headings

| Line | Selector | Now | v16 |
|---|---|---|---|
| 48 | `.serif` | Merriweather 700 | Delete the class |
| 52–53 | `.claim` (7 section H2s) | Merriweather 700, 28px; 36px at ≥900px | H2: Inter 700, 28px, line height 1.25, all widths. Delete the 900px override |
| 72 | `.hero h1` | Merriweather 700, `clamp(36px, 5.2vw, 64px)`, line height 1.08, −0.02em | Display: Inter 700, 48px, line height 1.1, no letter-spacing, all widths |
| 79 | `.lens-label` | Merriweather 700, 22px | H3: Inter 600, 20px, line height 1.3 |
| 89–90 | `.lens-frame` | Merriweather 700, 24px; 28px at ≥900px | H2: Inter 700, 28px, line height 1.25. Delete the 900px override |
| 133 | `.shift-grid h3` | Merriweather, 24px | H3 |
| 148 | `.turn-n` (stat numerals) | Merriweather 700, 48px | Numeral: Inter 700, 48px (Display size), line height 1.1, `tabular-nums` |
| 154 | `.rel-grid h3` | Merriweather, 28px | H3 |
| 157 | `.rel-close p` | Merriweather 700, `clamp(28px, 4vw, 48px)` | H2 |
| 164 | `.ladder h3` | Merriweather, 22px | H3 |
| 209 | `.confirm h3` | Merriweather, 32px | H3 |
| 315 | `<h3 class="serif" style="font-size:28px;line-height:1.2">` | Inline Merriweather 28px | Remove the class and inline style; it's an `h3`, so H3 |

```css
/* Headings are Inter at v16 sizes. DESIGN-TOKENS-v16.md § Typeface by Role, § Type Scale */
.hero h1      { font-family: var(--font-heading); font-weight: 700; font-size: var(--text-display); line-height: 1.1; color: #fff; max-width: 14em; }
.claim,
.rel-close p  { font-family: var(--font-heading); font-weight: 700; font-size: var(--text-h2); line-height: 1.25; color: var(--color-heading); }
.claim        { max-width: 22em; }
.rel-close p  { max-width: 16em; }
.lens-frame   { font-family: var(--font-heading); font-weight: 700; font-size: var(--text-h2); line-height: 1.25; color: #fff; max-width: 30em; }
.lens-label   { display: block; font-family: var(--font-heading); font-weight: 600; font-size: var(--text-h3); line-height: 1.3; color: #fff; margin-bottom: 16px; }
.shift-grid h3, .rel-grid h3, .confirm h3 { font-family: var(--font-heading); font-weight: 600; font-size: var(--text-h3); line-height: 1.3; color: var(--color-heading); margin-bottom: 12px; }
.ladder h3    { font-family: var(--font-heading); font-weight: 600; font-size: var(--text-h3); line-height: 1.3; color: var(--color-heading); }
.turn-n       { font-family: var(--font-heading); font-weight: 700; font-size: var(--text-display); line-height: 1.1; color: var(--color-heading); font-variant-numeric: tabular-nums; }
/* Delete: .serif, and the 900px overrides for .claim and .lens-frame */
```

Use `--color-heading` (v16 role) instead of `--color-text-header` throughout.

### 2.3. Other v16 rules

| Line | Now | v16 rule | Fix |
|---|---|---|---|
| 230, 273–446 | Headlines in sentence case ("Your stakeholders follow people now, not mastheads.") | Headlines are title case (Type Scale) | Title case on the H1 and the seven `.claim` H2s; wording is Justin's |
| 60 | `.live-dot` rests as an Acid fill | Green means interaction; there's no "live" color | `#ffffff` dot on dark (interim) |
| 91 | `.lens-frame .live` rests in Acid text | Same | `#ffffff`; Source Code Pro only if the text is all caps, otherwise Inter at the surrounding size |
| 95 | `.lr-lines path` Acid strokes | Acid isn't a graphic color (excluded from the data palette) | `--gray-cool-3` (graphic surface, interim) |
| 44 | `body { background: #fff }` | Page background is `--color-bg` (step 2) | `background: var(--color-bg)`; white bands use `var(--color-surface)` |
| 59 | `.live` mono at `0.92em` in sentences | Source Code Pro is caps labels and tags only | Inter at the surrounding size, `tabular-nums` |

---

## 3. Fix: `pulse.html`

### 3.1. Fonts and headline

- Delete the Merriweather `preload` and `<noscript>` links (lines 22–23) and the `Merriweather Fallback` `@font-face` (line 983).
- Delete the page's `Inter Fallback` and `Source Code Pro Fallback` `@font-face` rules and its inline `--font-mono` (lines 32–37); `variables.css` defines them.
- Replace literal `'Inter', 'Inter Fallback', ...` stacks (about 30 rules) with `var(--font-primary)`.
- Line 1027, `.pulse-hero .masthead-title`:
```css
.pulse-hero .masthead-title { font-family: var(--font-heading); font-size: var(--text-display); font-weight: 700; line-height: 1.1;
                              color: var(--color-heading); max-width: 17em; margin: 0 0 32px; min-height: 2.2em; }
```
`min-height` moves from `2.16em` to `2.2em` to reserve two lines at line height 1.1.

### 3.2. Labels and eyebrows

| Line | Selector | Now | v16 |
|---|---|---|---|
| 140 | `.signal-band-eyebrow` | 12px, 0.14em, Acid | Label: 13px, 500, caps, 0.12em. Acid is allowed on dark eyebrows |
| 153 | `.field-summary-eyebrow` | 12px, **Lime text** | Label, `--color-text-secondary` (light surface). Lime is the dark focus ring only |
| 161 | `.audience-bridge-label` | 12px, 0.1em, `#888` | Label, `--color-text-secondary` |
| 176, 237 | `.masthead-dateline`, `.rail-eyebrow` | 12px, 0.14em, white at 45% / 35% | Label, `--color-text-on-dark-2` |
| 260 | `.archive-eyebrow` | 12px, 0.14em | Label, `--color-text-secondary` |
| 1023 | `.pulse-hero .masthead-dateline` | 13px, 0.04em | Label: 0.12em, caps |
| 150, 255 | `.signal-card-meta` | 12px, 0.04em, white at 28–35% | Tag (meta line): 12px, caps, 0.08em, line height 1.4, `--color-text-on-dark-2` |
| 120, 261 | `.page-subhead-method`, `.archive-method` | Mono, 12px, sentence case | Small: Inter 13px, `--color-text-on-dark-2` / `--color-text-secondary` |
| 166, 168, 217, 221, 222 | Beat map and trend names and counts | Mono 12px, sentence case | Tag if all caps; otherwise Small (Inter 13px, `tabular-nums` for counts) |

### 3.3. Tags

| Line | Selector | Now | v16 |
|---|---|---|---|
| 146, 250 | `.signal-beat-tag` | Acid text, Acid-tinted fill **and** border, pill, `cursor: pointer` | Beat tag on dark: 8px dot in the beat's color, 6px gap, `#ffffff` text, `1px solid #5e5e5e`, padding `3px 7px`, 6px radius. Remove the cursor |
| 147, 251 | `.signal-reason-tag` | Pill, white at 30% | Status "in progress" on dark: `#ffffff` text, `1px solid #ffffff`, 6px radius |
| 194 | `.story-stack-beat` | Pill, fill **and** border, hover, clickable | It filters, so it's a control: **secondary button** on dark (transparent, `#ffffff` text, `1px solid #909090`, 44px min height, Acid on hover and press, white when selected) |

### 3.4. Color

| Lines | Now | v16 |
|---|---|---|
| 181, 254 | `.lede-creator`, `.signal-card-creator` rest in Acid | `#ffffff` at rest; Acid on hover and press |
| ~16 rules (e.g. 120, 141, 188, 201, 207, 221, 229–231) | White text at 18–45% opacity | `--color-text-on-dark-2` (opacity text is off-system) |
| 154, 156, 261, 353, 443, 499 and others | `#888`, `#aaa`, `#bbb` | `--color-text-secondary` on light; `--color-text-on-dark-2` on dark |
| `--p-*` block (~line 990) | Page-local tokens (`#f4f4f6`, `#e4e4e8`, `#d4d4d8`, `#1a1a1a`, `#1c1c1c`, `#3a3a3a`) | Delete. `--p-surface` → `--color-surface`; `--p-surface-2`, `--p-fill` → `--color-bg`; `--p-border` → `--color-border`; `--p-ink` → `--color-text`; `--p-ink-2` → `--color-text-secondary`; `#111111` → `--color-surface-dark`; `#303036` → `#303030` |
| 991–1010 | `prefers-color-scheme: dark` theme | **Delete.** v16 defines no site dark mode. The masthead and The Line stay dark in all cases, as now |
| 170, 1026 | `#b45309` for trend-down and "stale" | No warning color in v16: `--color-text-secondary`, and make the meaning explicit in the text ("▼ 12%", "Updated 6 days ago") so it isn't carried by color |
| 1103 | `#ff6b6b` error | `var(--color-error)` |
| 2824–2839 | `BEAT_COLORS`: Tailwind hexes; also colors **Newsletter, Video, Audio / Podcast, Web / Social** | Platform and content-type rows: monotone now (`--gray-cool-6`; the chart is a graphic surface). Beat rows stay as they are until Ryan's taxonomy mapping moves charts to `ATLAS_VIZ_COLORS` (a separate, known project). The empty cell `#f0f0f2` → `--gray-cool-2` |
| The Line (masthead chart) | Acid stroke and end-point | `#ffffff` stroke and end-point on the dark masthead (interim; Acid is interaction only) |

Archive `pulse_tokens.md` (done in the foundation brief).

---

## 4. Process

- Work on `dev`; screenshots before and after at 390, 768 and 1440px; James reviews on the staging preview.
- Run `python3 scripts/check_brand.py pulse.html for-brands.html` while working; it lists every remaining violation in the two files.
- Regenerate the baseline in the same pull request. The two files' counts must drop to zero for `font-family`, `font-literal`, `serif-scope`, `serif-heading`, `font-size`, `pill-radius` and `lime-text`. Remaining `color` entries are only those listed above as interim or known (the beat colors).
- After this merges, delete `--font-editorial` from `variables.css` (its last site use was For Brands).

---

## 5. Acceptance

- `grep -i merriweather pulse.html for-brands.html` returns nothing; no font links on either page.
- Every `h1`–`h3`, `.claim`, `.lens-frame`, `.turn-n` and `.masthead-title` computes to Inter at the sizes above (DevTools).
- The Network panel shows no Merriweather request on either page.
- No Acid Green at rest on either page except Acid eyebrows on dark surfaces.
- No dark theme when the viewer's system is in dark mode.
- Lighthouse CLS stays under 0.1.
- James signs off on staging before the merge to `main`.

---

## 6. For the Next Update (James and Justin)

These are listed, not built. Each needs a token-version decision:
1. A "live" signal: whether one exists, and its color or form (today: white dot, interim).
2. A warning color for "stale" and trend-down (today: secondary text plus explicit wording).
3. Error text contrast: `#f50000` measures about 4.3:1 on white and 4.4:1 on `#121212`, just under 4.5:1 for small text.
4. A site dark mode, if wanted.
5. A responsive Display size for phones (today: 48px at all widths, per v16).
6. Graphic strokes on dark mastheads (The Line, convergence lines), now white or Cool gray as interim.
