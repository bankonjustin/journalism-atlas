# Atlas v16.1 Level-Set — Pulse and For Brands

*Working document for Justin and Claude Code · Owner: James Bareham, Creative Director · November 3, 2026*
*Implements DESIGN-TOKENS-v16.1.md and ATLAS-BRAND-GUIDE-v5.1.md. Audited against `main` at `e2890fa` (November 3, 2026, 03:46 ET).*

**Goal:** bring Pulse and For Brands into line with the rest of journalismatlas.com under v16.1, and remove everything that was blocking it. When this document is done, both pages use Inter for every heading, Source Code Pro only for all-caps labels and tags, and the one error red, with no page-only dark mode.

---

## 0. Authority: What This Document Overrules

James approved every decision in section 1 on November 3, 2026. They're written into DESIGN-TOKENS-v16.1.md and ATLAS-BRAND-GUIDE-v5.1.md, so they're design rules, not suggestions.

**Order of precedence:** DESIGN-TOKENS-v16.1.md, then ATLAS-BRAND-GUIDE-v5.1.md, then this document, then everything else in the repo.

**This document overrules and closes:**

| Where | What | Now |
|---|---|---|
| `docs/design/CLAUDE-DESIGN-RULES.md` § "Provisional, confirm with James" | "Monospace = live or versioned data only," "Acid = changed recently," the four provisional error roles | **Withdrawn.** Delete the section (step A3) |
| `docs/design/DESIGN-STATE-2026-10-31.md` § 5 (S1–S7) and agenda items 1, 2, 4, 5 | Defaults, including S7 "interim = current pages unchanged" | **Answered** in section 1. Pulse and For Brands change now |
| `docs/design/v15-session-2/JAMES-OPEN-ITEMS.md` S1–S7 and item 4 | Open | **Answered** in section 1 |
| `docs/briefs/Atlas-Pulse-For-Brands-Brief-2026-10.md` | The October 27 brief | **Replaced** by this document (its line numbers are out of date after the November 2 Pulse rewrite) |
| `Atlas-Foundation-Lock-Brief-2026-10.md` step 7, `V16-INSTALL-NOTES-FOR-JAMES-2026-10.md` § 2, and any text in `CLAUDE.md`, `WORKFLOW.md`, `CLAUDE-DESIGN-RULES.md` or `START-HERE.md` saying a change waits for James's GitHub access or review | Waiting on James | **Deferred** until after the level-set (v16.1 § Enforcement, item 3). Justin makes every change; nothing waits on James's login |
| Comments in `for-brands.html` (lines 32–36) and `pulse.html` (lines 985–988) that state design rules | Page-level rules ("Source Code Pro is reserved for live data," "Acid = live/now," "follows the viewer's theme") | **Void.** Replace as below |

If anything else in the repo stops this work, v16.1 wins. Note it in the commit message; don't wait.

---

## 1. James's Decisions (November 3, 2026)

| # | Question | Decision |
|---|---|---|
| S1 | Provisional rules in `CLAUDE-DESIGN-RULES.md` | **Withdrawn.** v16.1 is the only rule set. Source Code Pro is for all-caps labels and tags; Acid Green means interaction |
| S2 | Error red | **`#b3261e`, one red site-wide, through `--color-error`.** On light surfaces: text, icons, outlines or fills. On dark surfaces: fill with white text only. Replaces `#f50000`; `#f2b8b5` and the other provisional values are not used |
| S3 | Acid and Lime with transparency (144 uses) | **Allowed** as hover and overlay tints in backgrounds, borders and shadows until v17. Never text. No visible change |
| S4 | CODEOWNERS and review | **Deferred** until the site is level-set. Justin does everything |
| S5 | Repo private, TIJA LLC org | Not a design decision; Justin's call. Nothing here depends on it |
| S6 | Team DMV header and footer | **Closed:** Team DMV was retired on November 2 (`386090b`) |
| S7 | Pulse and For Brands interim defaults | **Ship now**, using v16.1 § Interim Treatments |
| Item 4 | Tab strips | **Secondary buttons** |
| — | Pulse dark mode | **Remove.** A full site dark mode is a later design initiative, once the site is consistent |
| — | Timing | **Now.** Both pages are live, so the November 5 launch doesn't affect this work |
| — | Scope | **Pulse and For Brands**, plus the error red site-wide. Nothing else on the site changes in this update |

---

## Part A: Install v16.1 and Clear the Blockers

**A1. Install the documents.**
```bash
git mv docs/design/DESIGN-TOKENS-v16.md    docs/design/archive/DESIGN-TOKENS-v16.md
git mv docs/design/ATLAS-BRAND-GUIDE-v5.md docs/design/archive/ATLAS-BRAND-GUIDE-v5.md
git mv docs/briefs/Atlas-Pulse-For-Brands-Brief-2026-10.md docs/design/archive/Atlas-Pulse-For-Brands-Brief-2026-10.md
# add from this handoff:
#   docs/design/DESIGN-TOKENS-v16.1.md
#   docs/design/ATLAS-BRAND-GUIDE-v5.1.md
#   docs/briefs/Atlas-v16.1-Level-Set-Pulse-For-Brands-2026-11.md   (this file)
```
Add to the top of each archived file: `> Superseded by DESIGN-TOKENS-v16.1.md / ATLAS-BRAND-GUIDE-v5.1.md (November 3, 2026). Do not implement from this file.`

**A2. Update references.** In `CLAUDE.md`, `WORKFLOW.md`, `docs/design/CLAUDE-DESIGN-RULES.md` and `START-HERE.md`, replace `DESIGN-TOKENS-v16.md` with `DESIGN-TOKENS-v16.1.md` and `ATLAS-BRAND-GUIDE-v5.md` with `ATLAS-BRAND-GUIDE-v5.1.md`. Leave dated reports, ledgers and briefs as they are.

**A3. Fix `docs/design/CLAUDE-DESIGN-RULES.md`.**
1. Delete the whole section `## Provisional, confirm with James` (the three bullets and its intro line).
2. In its place, add:
```markdown
## v16.1 rules (DESIGN-TOKENS-v16.1.md)

- **No provisional rules.** This file restates the tokens. A rule not in DESIGN-TOKENS-v16.1.md doesn't apply, wherever it's written.
- **Error red is `#b3261e` (`--color-error`).** Light surfaces: text, icons, outlines or fills. Dark surfaces: a fill with `--color-on-error` (`#ffffff`) text only, never text, icons or thin lines. Error text starts with "Error:" or sits beside an error icon.
- **No dark mode.** No `prefers-color-scheme` styles, no `color-scheme: dark`, no `data-theme` switching, on any page. A full site dark mode is a later initiative.
- **Acid and Lime tints** (with transparency) are allowed in `background`, `border-color`, `box-shadow`, `outline` and non-text graphic fills, until v17. Never as text, icons or thin strokes.
- **Interim treatments** (live signal, warnings, phone Display size, strokes on dark mastheads, tab strips): DESIGN-TOKENS-v16.1.md § Interim Treatments.
```
3. In `## Locked rules`, change the "Never edit to make a request fit" bullet's last sentence to: `Changes to them come through a new token version. (James's GitHub review is deferred until the site is level-set; until then the build check is the lock.)`
4. In `## What changes only with a new token version (James)`, keep the list; the tokens are still changed only by a new version James writes or approves. That approval can happen outside GitHub (as v16.1 did).

**A4. Remove "waiting on James" from the repo.** In `CLAUDE.md`, `WORKFLOW.md`, `START-HERE.md` and `docs/design/DESIGN-STATE-2026-10-31.md`, change any step that waits on James's GitHub access, username or review to: `Deferred until after the v16.1 level-set (DESIGN-TOKENS-v16.1.md § Enforcement, item 3).` In `JAMES-OPEN-ITEMS.md`, mark S1–S7 and item 4 as answered, with a pointer to section 1 of this document.

---

## Part B: Update the Brand Check

`scripts/check_brand.py` needs two changes so it matches v16.1. Both are in the same pull request as Part C, so the build stays green.

**B1. Error red in the palette.** In `PALETTE` (line 69), replace `"f50000"` with `"b3261e"`. Update the docstring line for `color` to say "v16.1 palette."

**B2. Allow Acid and Lime tints outside text.** In the `COLOR_FUNC` loop (around line 250) and the `color-alpha` branch (around line 246), skip a match when it's Acid or Lime with transparency and it isn't a text color:

```python
TINT_BASES = {"ceff00", "97d600"}   # v16.1 § Tints: Acid and Lime tints allowed outside text, until v17

def is_tint(call):
    """rgba()/hsla() of Acid (206,255,0) or Lime (151,214,0) with alpha."""
    name, _, args = call.partition("(")
    nums = re.findall(r"[\d.]+", args)
    if not name.strip().lower().startswith("rgb") or len(nums) < 4:
        return False
    hexv = "".join(f"{int(float(n)):02x}" for n in nums[:3])
    return hexv in TINT_BASES

# in the color-alpha branch:
        elif alpha:
            if h in TINT_BASES and not is_text_color(text, m.start()):
                continue  # v16.1 tint
            add("color-alpha", m.start(), "#" + m.group(1))

# in the COLOR_FUNC loop, before add("color-func", ...):
        if is_tint(m.group(0)) and not is_text_color(text, m.start()):
            continue  # v16.1 tint
```
Add a `tints` line to the rules docstring. Then regenerate the baseline (`python3 scripts/check_brand.py --write-baseline`) in the same commit; the `color-func` count falls by about 95 (tested on November 3 against `e2890fa`; the remaining tint uses are text colors and stay flagged). `--tight` requires the regeneration, and `--guard-baseline` allows it because `check_brand.py` changed in the same pull request.

---

## Part C: One Error Red, Site-Wide

**C1. `assets/css/variables.css`.**
- Line 116: `--color-error: #b3261e;   /* v16.1. Light: text, icons, outlines, fills. Dark: fill only, with --color-on-error text */`
- Add below it: `--color-on-error: #ffffff;  /* text on an error fill */`
- Delete `--color-error-dark: #ff4422;` (line 132).
- Delete the `PROVISIONAL (Oct 28, 2026)` comment and the four `--color-*-provisional` variables (lines 134–142).

**C2. Every error use.** Audited November 3:

| File | Line | Now | v16.1 |
|---|---|---|---|
| `assets/js/main.js` | 425 | `color: var(--color-error-provisional)` (search page loading error, light surface) | `color: var(--color-error)`. It already starts with "Error:" |
| `pulse.html` | 1102 | `.form-msg[data-state="error"] { color: #f50000; }` | `color: var(--color-error);` (the form is on a light surface) |
| `pulse.html` | 1103 | Dark-mode override `#ff6b6b` | Delete (Part E1 removes dark mode) |
| `for-brands.html` | 206 | `var(--color-error)` | No change; it picks up the new red (light surface) |
| `chicago-survey.html` (internal) | 602–606 | `.field .error-msg` at 12px, `#ff6b6b`, on a dark page | Dark surface, so the fill pattern: `background: var(--color-error); color: var(--color-on-error); font-size: 13px; padding: 4px 8px; border-radius: 6px`, with an "Error:" prefix |
| `preview/smartnews-d029dc36/` | 204–208 | `var(--color-error)` | No change; picks up the new red. Check its surface: fill pattern if dark |

Then search once more: `grep -rniE "f50000|ff4422|ff6b6b|error-provisional|color-error-dark" --include=*.html --include=*.css --include=*.js . | grep -vE "_deprecated|nn/|preview/nodes|assets/nn5|nodes-networks|docs/"`. **Not errors, leave alone:** `#ff4422` and `#FF6B6B` in `index.html` 1489, `main.js` 1738, `mobile.html` 839/861/991 and the internal `atlas_*` pages are chart category colors, which move to `ATLAS_VIZ_COLORS` in the separate taxonomy project.

**C3. Error text rule.** Every error message reads "Error: …" or sits beside an error icon (`error` in Material Symbols), so it isn't carried by color alone. Add the prefix wherever a message lacks one.

---

## Part D: `for-brands.html`

### D1. Fonts
- **Lines 25–28:** delete the `preconnect`, `preload` and `<noscript>` Google Fonts lines. `header.js` loads Inter, Source Code Pro and Material Symbols.
- **Lines 32–36:** replace the header comment with:
  ```css
  /* /for-brands. Tokens only: docs/design/DESIGN-TOKENS-v16.1.md.
     Headings and UI: Inter (--font-heading / --font-primary). All-caps labels and tags: Source Code Pro 500 (--font-mono). */
  ```
- **Lines 38–40:** delete both `@font-face` rules and the inline `:root` font line. `variables.css` defines the fonts and fallbacks.

### D2. Headings (Merriweather → Inter)

| Line | Selector | Now | v16.1 |
|---|---|---|---|
| 48 | `.serif` | Merriweather 700 | **Delete the class** |
| 52–53 | `.claim` (seven section H2s) | Merriweather 700, 28px; 36px at ≥900px | H2: Inter 700, 28px, line height 1.25, all widths. Delete line 53 |
| 72 | `.hero h1` | Merriweather 700, `clamp(36px, 5.2vw, 64px)`, line height 1.08, −0.02em | Display: Inter 700, 48px, line height 1.1, no letter-spacing, all widths |
| 79 | `.lens-label` | Merriweather 700, 22px | H3: Inter 600, 20px, line height 1.3 |
| 89–90 | `.lens-frame` | Merriweather 700, 24px; 28px at ≥900px | H2: Inter 700, 28px, line height 1.25. Delete line 90 |
| 122 | `.lens-empty .lens-frame` | 22px | H3: 20px, Inter 600 |
| 133 | `.shift-grid h3` | Merriweather, 24px | H3 |
| 148 | `.turn-n` (stat numerals) | Merriweather 700, 48px | Inter 700, 48px, line height 1.1, `tabular-nums` |
| 154 | `.rel-grid h3` | Merriweather, 28px | H3 |
| 157 | `.rel-close p` | Merriweather 700, `clamp(28px, 4vw, 48px)` | H2 |
| 164 | `.ladder h3` | Merriweather, 22px | H3 |
| 209 | `.confirm h3` | Merriweather, 32px | H3 |
| 315 | `<h3 class="serif" style="font-size:28px;line-height:1.2">` | Inline Merriweather | Remove the class and inline style; it takes the H3 style |

```css
/* Headings: Inter at v16.1 sizes (DESIGN-TOKENS-v16.1.md § Typeface by Role, § Type Scale) */
.hero h1      { font-family: var(--font-heading); font-weight: 700; font-size: var(--text-display); line-height: 1.1; color: #fff; max-width: 14em; }
.claim, .rel-close p { font-family: var(--font-heading); font-weight: 700; font-size: var(--text-h2); line-height: 1.25; color: var(--color-heading); }
.claim        { max-width: 22em; }
.rel-close p  { max-width: 16em; }
.lens-frame   { font-family: var(--font-heading); font-weight: 700; font-size: var(--text-h2); line-height: 1.25; color: #fff; max-width: 30em; }
.lens-empty .lens-frame { font-weight: 600; font-size: var(--text-h3); line-height: 1.3; }
.lens-label   { display: block; font-family: var(--font-heading); font-weight: 600; font-size: var(--text-h3); line-height: 1.3; color: #fff; margin-bottom: 16px; }
.shift-grid h3, .rel-grid h3, .confirm h3 { font-family: var(--font-heading); font-weight: 600; font-size: var(--text-h3); line-height: 1.3; color: var(--color-heading); margin-bottom: 12px; }
.ladder h3    { font-family: var(--font-heading); font-weight: 600; font-size: var(--text-h3); line-height: 1.3; color: var(--color-heading); }
.turn-n       { font-family: var(--font-heading); font-weight: 700; font-size: var(--text-display); line-height: 1.1; color: var(--color-heading); font-variant-numeric: tabular-nums; }
```
Replace `var(--color-text-header)` with `var(--color-heading)` throughout the page (both are `#000000`; `--color-heading` is the v16.1 role).

### D3. Live data, the live dot and the lines

| Line | Now | v16.1 |
|---|---|---|
| 59 | `.live`: Source Code Pro at `0.92em` inside sentences (counts, dates) | Mixed-case numbers in a sentence are Inter: `font-family: inherit; font-size: inherit; font-variant-numeric: tabular-nums; letter-spacing: normal` |
| 115 | `.lens-heads .by .live { font-size: 12px; }` | Delete (it inherits the 13px byline) |
| 60 | `.live-dot` rests as an Acid fill | Interim live signal: `background: #ffffff` (dark surface) |
| 91 | `.lens-frame .live`: Acid text, mono, 0.85em | `color: #ffffff; font-family: inherit; font-size: inherit` |
| 95 | `.lr-lines path`: Acid strokes at 70% | Interim stroke on dark: `stroke: var(--gray-cool-3); opacity: 1` |

### D4. Other rules

| Line | Now | v16.1 |
|---|---|---|
| 44 | `body { background: #fff; }` | `background: var(--color-bg)`. Sections that should stay white use `var(--color-surface)` (check `.light`, `.intake`) |
| 230, 273, 299, 333, 361, 383, 409, 446 | Sentence-case headlines ("Trust moved. Here's the map.") | Title case (v16.1 Type Scale). Wording is Justin's; only the case changes |

---

## Part E: `pulse.html`

### E1. Remove the dark mode
- **Line 990:** delete `color-scheme: light dark;` from the `:root` rule.
- **Lines 991–1010:** delete both `@media (prefers-color-scheme: dark)` blocks and every `:root[data-theme="dark"]` rule.
- **Line 1103:** delete the dark-mode error override.
- **Lines 985–988:** replace the comment with: `/* Pulse. Tokens only: DESIGN-TOKENS-v16.1.md. No dark mode (v16.1): the page renders the same for every viewer. */`
- If any script sets `data-theme` on `<html>` or offers a theme toggle, remove it.

The dark bands that are part of the design (the signal band, the story stack, the ticker) stay dark for everyone, as on every other page.

### E2. Page-local tokens (line 989)
Delete the `--p-*` variables and point every use at the role variables:

| Local | Value | Becomes |
|---|---|---|
| `--p-surface` | `#ffffff` | `--color-surface` |
| `--p-surface-2` | `#f4f4f6` | `--color-bg` |
| `--p-fill` | `#e4e4e8` | `--color-bg` (fills), `--color-border` (dividers, e.g. line 160) |
| `--p-border` | `#d4d4d8` | `--color-border` |
| `--p-ink` | `#1a1a1a` | `--color-text` (`--color-heading` on headings) |
| `--p-ink-2` | `#5e5e5e` | `--color-text-secondary` |
| `--p-link` | | `--color-link` |
| `--p-focus` | `#5d7400` | `--color-focus-on-light` |
| `--p-hover-text` | `#000` | `--color-heading` |

### E3. Fonts
- **Lines 22–23:** delete the Merriweather `preload` and `<noscript>` links.
- **Lines 32–36 and 983:** delete the page's `@font-face` fallbacks (including `Merriweather Fallback`); `variables.css` defines them.
- **Line 41 and about 30 other rules** (listed by `python3 scripts/check_brand.py pulse.html` as `font-literal`): replace `'Inter', 'Inter Fallback', …` with `var(--font-primary)`. Line 41 also drops `-apple-system, BlinkMacSystemFont`.
- **Line 3423** (inline style in JS): `font-family: var(--font-primary)`.
- **Lines 1027–1028, the headline:**
```css
.pulse-hero .masthead-title { font-family: var(--font-heading); font-size: var(--text-display); font-weight: 700; line-height: 1.1;
                              color: var(--color-heading); max-width: 17em; margin: 0 0 32px; min-height: 2.2em; }
```

### E4. Source Code Pro by role
Pulse has 64 Source Code Pro rules in use, and none sets `text-transform: uppercase`, so they all render in mixed case. That was the withdrawn "monospace = live data" rule. Under v16.1 each one becomes one of four things:

- **Label:** Source Code Pro 500, 13px (`--text-label`), uppercase, 0.12em (0.08em for dense rows), line height 1.4
- **Tag:** Source Code Pro 500, 12px (`--text-tag`), uppercase, 0.08em, line height 1.2 (1.4 for meta lines)
- **Small:** Inter 400, 13px (`--text-small`), sentence case, letter-spacing normal; `tabular-nums` for numbers
- **Button or input:** the Secondary button spec (Inter 600, 15px, sentence case, 44px) or Body (Inter 400, 16px)

| Becomes | Selectors |
|---|---|
| **Label** | `.signal-band-eyebrow`, `.section-eyebrow`, `.intel-section-eyebrow`, `.header-intel-eyebrow`, `.header-intel-brands-label`, `.audience-bridge-label`, `.masthead-dateline`, `.pulse-hero .masthead-dateline` (0.04em → 0.12em), `.creator-strip-header`, `.picks-label`, `.plat-intro` if it's a heading (Small if it's a sentence) |
| **Tag** | `.signal-beat-tag`, `.signal-reason-tag`, `.beat-tag`, `.platform-tag`, `.stat-pill`, `.intel-week-badge`, `.pulse-ticker-item-beat`, `.creator-chip-platform`, `.field-summary-draft`, `.signal-card-meta`, `.pick-meta`, `.c-meta`, `.post-date` (meta lines, line height 1.4); chart labels `.heat-beat-label`, `.heat-date-tick`, `.co-col-label`, `.co-row-label`, `.co-cell`, `.plat-label`, `.beat-map-label`, `.f-label.f-count`, `.fp-sub`, `.c-day`, `.pick::before`, `summary::after` indicators |
| **Small** | `.field-summary-byline`, `.beat-trend-name`, `.beat-trend-pct`, `.corpus-cluster-count`, `.beat-map-count`, `.beat-map-more`, `.pulse-ticker-item-time`, `.beat-name`, `.beat-count`, `.post-count-label`, `.creator-name` (the Pulse card hierarchy: creator name is Small), `.post-geo`, `.creator-chip-count`, `.co-section-sub`, `.plat-pct`, `.intel-post-creator`, `.fp-count`, `.fp-n` |
| **Secondary button** | `.analysis-tab`, `.heat-toggle-btn`, `.rhythm-view-btn`, `.story-stack-beat` (see E6) |
| **Body (input)** | `.beat-search-input` |

Check each selector against what it actually renders. If a "Label" or "Tag" renders a sentence or a name that must stay in mixed case, it becomes Small instead. Don't add uppercase to people's names, publication names or handles.

**Also:**
- **Line 653:** delete `main .link-instruction { text-transform: none; letter-spacing: 0; }`. Instruction links are Labels: caps, ending in →.
- **12px Inter (only Source Code Pro Tags may be 12px):** `.f-label` (line 1036) → 13px Small; `.signal-tab-count` (242) → 13px; `.city-spotlight-eyebrow` (976) → Label; `.beat-trend-arrow` (167) → 13px.
- **Unused rules:** delete `.live-badge`, `.page-subhead-method`, `.pulse-thesis-band p`, `.field-summary-eyebrow` (this also clears the Lime-text violation at line 153), `.story-cluster-voice-count`, `.rail-eyebrow`, `.archive-eyebrow`, `.archive-method`. Search the page and its scripts first to confirm each is unused.

### E5. Tags
Tags follow v16.1: fill or outline, never both; 6px radius; padding `4px 8px`, or `3px 7px` when outlined; no hover; no pointer cursor.

| Lines | Selector | Now | v16.1 (dark surface) |
|---|---|---|---|
| 146, 250 | `.signal-beat-tag` | Acid text, Acid fill **and** border, pill, `cursor: pointer` | Beat tag: 8px dot in the beat's color, 6px gap, `#ffffff` text, `1px solid #5e5e5e`, no fill, 6px radius, no cursor |
| 147, 251 | `.signal-reason-tag` | White at 30%, pill, `TODO-JAMES` | Status, in progress: `#ffffff` text, `1px solid #ffffff`, 6px radius. Delete the TODO |
| 60–70 | `.live-badge` | Acid text, fill and border | Unused: delete (E4) |

### E6. Tab strips and filters (secondary buttons)
- **`.signal-tab`** (line 3852) already uses `btn btn--secondary`. Make sure the selected tab uses the Selected state (light: black fill, white text; dark: white fill, black text) driven by `aria-selected="true"`, not a separate `.active` style. `.signal-tab-count` goes to 13px.
- **`.analysis-tab`** (lines 677–699): underline tabs in mono. Restyle as secondary buttons: Inter 600, 15px, sentence case, 44px minimum height, 6px radius, `1px solid var(--color-button-2-outline)`, black text at rest; Acid fill on hover and press; Selected = black fill, white text (`aria-selected="true"`). Remove the underline and the `--color-accent-on-light` active color. Keep the icon at 18px (inline size).
- **`.heat-toggle-btn`, `.rhythm-view-btn`:** the same secondary button spec.
- **`.story-stack-beat`** (lines 194–195): it filters, so it's a secondary button on a dark surface: transparent, `#ffffff` text, `1px solid #909090`, 44px, Acid fill with black text on hover and press, white fill with black text when selected. Remove the pill and the tinted fill.

### E7. Color

| Lines | Now | v16.1 |
|---|---|---|
| 140, 189, 200, 206, 181, 254 | Acid text at rest: `.signal-band-eyebrow` (allowed: eyebrow on dark), `.story-stack-creator`, `.corpus-cluster-count`, `.lede-creator`, `.signal-card-creator` | Keep Acid on `.signal-band-eyebrow` only. The others: `#ffffff` at rest, Acid on hover and press |
| 230 | `.pulse-ticker-item-beat`: Acid at 35% as text | Tag, `--color-text-on-dark-2` |
| 40 rules (e.g. 116, 120–121, 141, 147, 150, 176, 188, 191–194, 201–211, 217–231, 237, 251, 255, 287, 635–643, 656, 664–665, 938, 953–971, 2563) | Text in white or Acid at 18–85% opacity | Secondary text on dark → `--color-text-on-dark-2` (`#c6c6c6`); primary text on dark (85% and up) → `#ffffff`; disabled → step 4. Transparent text is off-system |
| 14 × `#888`, 13 × `#aaa`, 7 × `#bbb`, `#767676`, `#606068`, `#444`, `#b0b0b8` | Off-scale grays | Light surface → `--color-text-secondary`; dark surface → `--color-text-on-dark-2`; borders → `--color-border` / `--color-border-on-dark` |
| `#1a1a1a` (345, 606, 616), `#111111` (50, 139, 174, 235), `#d4d4d8` (515) | Off-scale | `#1a1a1a` → `--color-text`; `#111111` → `--color-surface-dark`; `#d4d4d8` → `--color-border` |
| 170, 1026 | `#b45309` for trend-down and "stale" | Interim warning: `--color-text-secondary`, with the meaning in the text ("▼ 12%", "Updated 6 days ago") |
| 644 | `.masthead-stale { color: #ffbc00; }` | Unused once E1 is done? If still rendered on a dark surface, `--color-text-on-dark-2` plus wording, as above |
| 2812–2825 | `BEAT_COLORS`: Tailwind hexes; also colors for **Newsletter, Video, Audio / Podcast, Web / Social** | Content-type and platform rows are monotone now: `--gray-cool-6` (`#303036`, graphic surface). Beat rows stay until Ryan's taxonomy mapping moves charts to `ATLAS_VIZ_COLORS` (the known interim; leave them in the baseline) |
| 2829, 2842 | `#f0f0f2` empty cell | `#efeff4` (Cool step 2) |
| 3423, 3441 | Inline `#888`, `#bbb` in JS strings | `var(--color-text-secondary)` |
| Masthead graphic strokes on dark (if any rest in Acid) | | Interim: Cool step 3 `#c6c6cd` |

Acid and Lime tints in backgrounds, borders and shadows (e.g. line 144 hover border, 193 underline color) are allowed until v17 (v16.1 § Tints). Leave them.

---

## Part F: Review and Ship

1. **One pull request per part:** A+B+C together (docs, check, error red), then D (For Brands), then E (Pulse). Each regenerates the baseline in the same commit; counts must only go down.
2. **Preview before `main`.** Justin's call on process, but a branch push gets a Cloudflare preview URL. James reviews Pulse and For Brands there before merge. No GitHub access is needed to look at a preview.
3. **Screenshots** before and after at 390, 768 and 1440px for both pages, in `docs/design/v16.1-level-set/`.
4. **Layout checks:**
   - Headings that shrink (64px → 48px hero; 36px → 28px claims) shouldn't leave awkward single words.
   - Pulse labels that gain caps and 0.12em spacing get wider: check the signal band, the beat map, the heat grid, the co-occurrence table and the ticker at 390px.
   - The analysis tabs become 44px buttons: check they wrap or scroll at 390px.
5. **Run** `python3 scripts/check_brand.py pulse.html for-brands.html`. After Part E, the only results left on these two pages are the known beat colors in `BEAT_COLORS`.

## Acceptance

- `grep -ci merriweather pulse.html for-brands.html` returns 0 and 0. No Google Fonts links on either page.
- Every heading on both pages computes to Inter (DevTools). The For Brands hero and the Pulse headline are 48px.
- Every Source Code Pro element on both pages is uppercase and 12px or 13px.
- With the device set to dark mode, Pulse looks the same as with it set to light.
- No Acid Green at rest except `.signal-band-eyebrow` (an eyebrow on dark). No Lime text. No pill radius. No transparent text.
- Error messages are `#b3261e` on light surfaces, with "Error:" or an icon. `grep -rniE "f50000|error-provisional|color-error-dark"` finds nothing outside archives.
- `docs/design/CLAUDE-DESIGN-RULES.md` has no "Provisional" section. Nothing in the repo says work waits on James's GitHub access.
- `python3 scripts/check_brand.py --tight` passes; the baseline is lower than before.
- James signs off on the preview.

---

## Part G: Not in This Update

- **The rest of the site** (shared header and footer, the other pages, 8–11px text): `Atlas-Type-Consolidation-Brief-2026-10.md`, after this.
- **Sizes between scale steps** (14px, 15px outside buttons): a later update.
- **v17 decisions:** a "live" signal, a warning color, a phone Display step, strokes on dark mastheads, named tint roles, and a full site dark mode (after the site is consistent).
- **GitHub code-owner review:** after the level-set.
