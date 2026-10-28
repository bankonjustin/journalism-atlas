# Atlas Design Tokens — v16
*Canonical design reference — committed to repo as source of truth for implementation*

*Last updated: October 27, 2026*
*Previous version: v15 (October 22, 2026)*
*Owner: James (james@journalismatlas.com)*

> **How this file works:** This is the single source of truth for all visual decisions. When Justin implements design changes with Claude Code, he references this document. If it's not here, it doesn't get implemented. If it changes here, it changes everywhere. **The values and rules in this file are locked** (see Governance, Locks and Exceptions): no session, brief or request can add, change or override them. Only a new token version, approved by James, can.

### What changed in v16
v16 replaces v15 in full. **It's a consolidation, not a redesign:** every color, size, weight, spacing value and radius is the v15 value. v16 locks those values, closes the gaps that let pages ship off-system, and adds enforcement. Everything not listed here carries over from v15 unchanged.

- **Governance, locks and exceptions (new section).** Justin makes product, structure, copy and build decisions. Design values are fixed by this file and change only through a new token version approved by James. Claude refuses requests that would break them.
- **Font allowlist.** Inter, Merriweather and Source Code Pro are the only typefaces on journalismatlas.com, plus Material Symbols Outlined for icons. Every other family is off-system, including system font stacks named on a page.
- **Typeface by role.** Every heading at every level is Inter, on every page. Merriweather is body prose inside editorial articles only, never headings, subheads, claims, ledes, numerals or pullquotes.
- **Monospace by role.** Source Code Pro is for all-caps labels and tags only. Sentence-case text that was set in a mono font becomes Inter Small; bold mono numerals become Inter 700 at a type-scale size.
- **The type floor applies everywhere.** No text below 12px anywhere: pages, inline styles, chart legends and labels, canvas and SVG text. 12px is Source Code Pro Tag only; all other text is 13px or larger.
- **Font tokens.** `--font-heading` and `--font-prose` added; `--font-editorial` and `--font-ui` retired. Pages set type only through `var(--font-*)`; only `variables.css` names a family.
- **Fonts load in one place.** The shared `header.js` loads Inter, Source Code Pro and Material Symbols for every page. Pages don't add font links, except editorial articles loading Merriweather.
- **Inter weights are 400, 600 and 700.** Inter 500 is off-system (weight 500 was already Source Code Pro only in v15).
- **One header, one footer.** Footer type is specified (see Site Footer). No page carries its own footer strip.
- **Text colors come from role variables.** Opacity-based text colors (e.g. `rgba(255,255,255,0.3)`) are off-system.
- **Exceptions register.** Co-branded reports (Nodes and Networks) and one internal Google Form mock-up sit outside the rules, by name.
- **Enforcement (new section).** `scripts/check_brand.py` runs in every build and fails on new violations; GitHub requires James's review for the files that hold the rules.
- **Canonical files (new section).** One location for every design document; outdated files are archived.

### Carried over from v15
v15's changes, all still in force:

- **The website moves from the Cool to the Neutral gray scale.** Every semantic gray role now points at a `--gray-neutral-*` variable. See Semantic Color Assignments.
- **Cool becomes the graphics scale:** infographics, charts, data visualizations and editorial illustrations. Decks, social and print may use either.
- **Embedded graphics count as their own surface,** so a Cool-scale chart may sit on a Neutral-scale page without breaking the one-scale-per-surface rule.
- **Off-system grays now snap to Neutral** by role, not Cool.
- **Disabled state** is `#909090` (Neutral step 4), was `#909097`.
- **No color coding by section or content type** is now written into this file.
- **Green means interaction.** Acid Green marks hover, press and selected states (and may be used for eyebrows on dark surfaces). The one-acid-moment-per-composition limit is dropped. Lime Green is the keyboard focus ring on dark surfaces only; it's no longer a hover color.
- **Buttons: two styles,** replacing v14's acid-at-rest primary CTA. Primary: step-6 fill, white text, outline; white when selected. Secondary (filters and repeated options): outline only, black text; black when selected. Both turn Acid Green on hover and press. See Component States.
- **Links:** instruction links are Source Code Pro caps with →, underlined on hover; body links stay underlined at rest; dark-surface link hover moves from Lime to Acid Green.
- **Tags:** fill or outline, never both; content type, status and beat category standardized. See Tags and Labels.
- **Typography:** weight 800 retired, Display drops to 700. Micro (11px Inter) is replaced by Label (13px) and Tag (12px), both Source Code Pro Medium caps. 12px Source Code Pro is allowed below the 13px floor for tags, badges and card meta lines (e.g. the Pulse card date · publication line).
- **Radius:** 6px for everything; pills (`9999px`) retired.
- **Migration:** repoint the semantic role variables from Cool to Neutral; see Migrating to the Neutral scale.
- **Owner contact** updated to james@journalismatlas.com.

### Carried over from v14
- **Site header: white is the default** (the live look); black when a page needs it. This reverses the earlier v13, which made black the default.
- **Report "Jump to" sub-nav moves to white** to match the header, with Dark Olive hover and active states. See Site Header.
- **Inline text links:** Dark Olive, underlined, on light surfaces; white, underlined, on dark. New variables `--color-link` and `--color-link-on-dark`. *(v15: dark-surface hover is now Acid Green.)*
- **CSS variable migration:** add `--color-acid`, `--color-lime` and `--color-olive`, then migrate each use by role. `--color-accent` is not repointed in place.
- **Off-system grays:** any gray outside the two scales (including the warm-gray family) is off-system. *(v15: they now snap to Neutral.)*
- **Charts:** moving charts to `ATLAS_VIZ_COLORS` is a separate project, gated on Ryan's taxonomy mapping.
- **Logos:** web SVG folder added; the live header file `Journalism_Atlas_wordmark_horizontal_lockup_black.svg` is flagged for replacement.

### Carried over from v13
- **Greens by surface.** Acid Green is fill-only on light surfaces; never text, icons or thin strokes there (1.2:1 on white). *(v15: Lime Green is now the dark-surface focus ring only.)*
- **Dark Olive `#5d7400`** is the green for text, icons and thin strokes on light surfaces (5.3:1 on white).
- **Focus ring follows the surface:** Lime Green on dark, Dark Olive on light.
- **`#bdbdbd` mapping** clarified by role.
- **Tier 2 contrast figures** show both scales (Neutral / Cool).

*v12's changes (new monotone scales, five-tier structure, `#ffaa00`, black-or-white header, white header logo) are recorded in the decisions log.*

---

## Governance, Locks and Exceptions (v16)

### Who decides what

| Area | Decides | Notes |
|---|---|---|
| Product, structure, pages, priorities, copy, build and release | **Justin** (CEO) | Within the locked rules below |
| Design values and rules: color, type, size, weight, spacing, radius, iconography, component states | **Locked in this file** | Change only through a new token version written or approved by **James** (Creative Director) |
| Data categories, taxonomy and creator metadata | **Ryan** (COO) | Tier 4 color changes also need James's sign-off |

### What's locked
Everything in this file. In practice, nobody, including Claude, picks a color, typeface, size or weight. Every one of them comes from a role in this file. Specifically:

- **Typefaces:** the font allowlist (Typography). No other family, including system stacks, on any page.
- **Colors:** the five tiers. No other hex, and no opacity-based text color.
- **Type scale, weights and the type floor.**
- **Spacing scale, radius, widths, icon set and sizes.**
- **Component states:** buttons, links, tags, eyebrows, nav.
- **Anything not defined here doesn't get built** until a token version defines it. Examples that are not defined today: a site dark mode, a "live" status color, a warning color, page-local token sets.

### How Claude applies the locks
- Claude (in this project, in Claude Code and in any brief) implements only values and rules from this file and the brand guide.
- If a request, brief or reference design names a font, color, size or rule that isn't here, Claude doesn't translate it into the nearest token ("a display serif → our serif", "an orange accent → our accent"). It applies the token for each element's **role** (a headline is Inter at its Type Scale size), builds that, and lists what the request asked for that the tokens can't give.
- Claude doesn't edit this file, the brand guide, `variables.css`, `scripts/check_brand.py` or its baseline to make a request fit. Proposed changes go to James as a note for the next token version.
- These rules hold whoever asks, including Justin and James. James changes them by issuing a new version, not in a session.

### Exceptions
Only these sit outside the rules. An exception covers the named paths only and can be added only in a new token version.

| Exception | Paths | What's allowed | Why |
|---|---|---|---|
| **Co-branded report: Nodes and Networks** (with the Knight Center at Cronkite, ASU) | `preview/nodes-and-networks-*`, `preview/nn-launch-kit/`, `assets/nn5/`, `nodes-networks-v5/`, `tools/preview-build/` | The report's own type (Inter Tight, Source Serif 4; DM Sans and Libre Baskerville in the earlier preview) and palette | Co-branded publication with its own design. Left as is so nothing breaks before launch |
| **Internal Google Form mock-up** | `atlas-portal/google-form-template.html` | Roboto | Mirrors Google Forms on purpose; internal, `noindex` |

Future co-branded reports may get their own entry, with named fonts and paths. The Atlas pages around a co-branded report (header, footer, landing pages, links to it) follow the full rules.

**Project C** is a separate brand: Atlas tokens don't apply. Check projectc.biz/style-guide before flagging its choices.

---

## Color Palette

**Brand colors express; data colors encode.** Every color belongs to exactly one tier, and each tier has one job.

| Tier | Job | Where it's used |
|---|---|---|
| 1. Core brand | Identity | Hover, press and selected states; focus ring; brand marks |
| 2. Monotones | Structure | UI, text, surfaces, borders |
| 3. Brand secondary | Expression | Decks, social, Pulse and editorial graphics, campaigns, print |
| 4. Data categories | Encoding | Anything that represents a taxonomy category: charts, category tags, labels |
| 5. System | Feedback | Errors, focus, dark-mode display accent |

**Rules across tiers**
- Don't mix brand secondary and data-category colors in one composition.
- Shared hexes are allowed only when deliberate and documented here. Avoid near-duplicates.
- New data categories draw from the brand secondary palette first, where contrast allows.
- Editorial annotations (e.g. a "HIRED" badge) use monotones. System feedback uses Tier 5. Never conflate the two.

### Tier 1 — Core Brand

| Name | Hex | sRGB | Use |
|------|-----|------|-----|
| Acid Green | `#ceff00` | 206, 255, 0 | **Interaction (v15):** hover, press and selected states. Also eyebrow labels on dark surfaces. No per-composition limit. Never a success/go signal |
| Lime Green | `#97d600` | 151, 214, 0 | **In UI, the keyboard focus ring on dark surfaces only (v15).** No longer a hover color. Otherwise brand materials |
| Dark Olive | `#5d7400` | 93, 116, 0 | **In UI:** the green for text, icons, underlines and thin strokes on light surfaces — hover and selected text, the current nav item, body links, focus ring. Never a fill or button background. Otherwise design elements (decks, print, graphics) |

### Greens by Surface

| | On dark surfaces (step 6–8, black header) | On light surfaces (step 1–2, white header — the default) |
|---|---|---|
| **Acid Green `#ceff00`** | Hover, press and selected: fills, text, underlines, icons. Eyebrow labels (17.9:1 on black) | **Fill only** (button hover and press), with black text on top (17.9:1). Never text, icons or thin strokes (1.2:1 on white) |
| **Lime Green `#97d600`** | Keyboard focus ring only (11.9:1 on black) | Not used |
| **Dark Olive `#5d7400`** | Not used in UI (4.0:1 on black — use Acid Green) | Text, icons and underlines for hover and selected states; body links; focus ring (5.3:1 on white, 4.6:1 on Neutral step 2 `#efefef`) |

Links, buttons and nav are specified in Component States.

### Tier 2 — Monotones

Two 8-step scales with matched contrast, each with a job (v15):

- **Neutral — the website scale.** Every semantic gray role on the site.
- **Cool — the graphics scale.** Infographics, charts, data visualizations and editorial illustrations.
- **Decks, social and print** may use either scale.

**Use one scale consistently within a surface** — don't mix neutral and cool steps on the same page. An embedded graphic (chart, infographic, illustration) counts as its own surface: a Cool-scale graphic may sit on a Neutral page, but the page chrome around it stays Neutral.

| Step | Neutral | Cool | Contrast on white (Neutral / Cool) | Use |
|---|---|---|---|---|
| 1 | `#FFFFFF` | `#FFFFFF` | — | Card backgrounds, reversed text, white header |
| 2 | `#EFEFEF` | `#EFEFF4` | — | Page backgrounds, secondary surfaces |
| 3 | `#C6C6C6` | `#C6C6CD` | 1.7 / 1.7:1 | Borders/dividers on light surfaces; secondary text on dark surfaces (12.3 / 12.4:1 on black) |
| 4 | `#909090` | `#909097` | 3.2 / 3.2:1 | **Large text, UI elements and presentation backgrounds only** — never body or small text on white; muted/disabled |
| 5 | `#5E5E5E` | `#5E5E64` | 6.5 / 6.4:1 | Secondary text on light surfaces — the lightest step safe for body text on white |
| 6 | `#303030` | `#303036` | 13.2 / 13.1:1 | Primary text, UI workhorse |
| 7 | `#121212` | `#121218` | — | Dark surfaces |
| 8 | `#000000` | `#000000` | 21:1 | Headings, black header, strongest contrast |

```css
:root {
  /* Neutral scale */
  --gray-neutral-1: #ffffff;
  --gray-neutral-2: #efefef;
  --gray-neutral-3: #c6c6c6;
  --gray-neutral-4: #909090;
  --gray-neutral-5: #5e5e5e;
  --gray-neutral-6: #303030;
  --gray-neutral-7: #121212;
  --gray-neutral-8: #000000;

  /* Cool scale */
  --gray-cool-1: #ffffff;
  --gray-cool-2: #efeff4;
  --gray-cool-3: #c6c6cd;
  --gray-cool-4: #909097;
  --gray-cool-5: #5e5e64;
  --gray-cool-6: #303036;
  --gray-cool-7: #121218;
  --gray-cool-8: #000000;
}
```

**Site scale (v15):** the website uses the **Neutral** scale for its semantic roles (below). This replaces v14's Cool assignment. The visible shift is small: the page background warms slightly from `#efeff4` to `#efefef`, and contrast figures are within 0.1 of the Cool values. The **Cool** scale stays on-system for graphics (see above).

### Tier 3 — Brand Secondary

Expression only. Carries no meaning. **Never used for UI states or data categories.**

| | Top row | Bottom row |
|---|---|---|
| Yellow | `#fff700` | `#806600` |
| Orange | `#ffaa00` — Atlas brand orange | `#b35100` |
| Pink | `#ff66ff` | `#a100a1` |
| Magenta | `#ff33cc` | `#a1006c` |
| Cyan / Blue | `#00e5ff` | `#005ea3` |

- `#ffaa00` (sRGB 255, 170, 0; CMYK 0, 33, 100, 0) **replaces `#ff9600` everywhere**, including any D3 or chart code. Search the codebase for `#ff9600` and replace.
- The top row is bright: `#ffaa00` is 1.9:1 on white, so top-row colors never carry text on white. On black they're strong (`#ffaa00` 11:1).
- Full sRGB and CMYK values: Atlas-Style_Guide_October_2026_v1.pdf.

### Tier 4 — Data Categories

See the D3 Visualization Color Array below. Values are unchanged from v11; what changes is their status: **these colors now mean their category wherever they appear**, not only in D3 charts.

### Tier 5 — System

| Role | Value | Notes |
|---|---|---|
| Error state | `#f50000` | Validation, destructive actions, failed states |
| On-error (text on error) | `#ffffff` | |
| Focus ring (dark surfaces) | `2px solid #97d600`, offset `2px` | Keyboard navigation |
| Focus ring (light surfaces) | `2px solid #5d7400`, offset `2px` | Lime fails 3:1 on light surfaces (v13) |
| Dark-mode display accent | `#ffbc00` | Display use on dark surfaces (e.g. a large stat) |

Never decorative, never a category.

### Semantic Color Assignments

All gray roles reference the Neutral scale (see Site scale above). "Replaces" lists the v14 Cool value, then the pre-v14 value.

| Role | Token | Hex | Replaces | Notes |
|------|-------|-----|----------|-------|
| Primary background | `--gray-neutral-2` | `#efefef` | `#efeff4`; `#efeff2` | |
| Card background | `--gray-neutral-1` | `#ffffff` | `#ffffff` | |
| Dark surface | `--gray-neutral-7` | `#121212` | `#121218` | Panels, inputs and cards on dark sections |
| Primary text | `--gray-neutral-6` | `#303030` | `#303036`; `#313131` | 13.2:1 on white, 11.5:1 on page background |
| Heading text | `--gray-neutral-8` | `#000000` | `#000000` | |
| Secondary text (light surfaces) | `--gray-neutral-5` | `#5e5e5e` | `#5e5e64`; `#6b6b6b` | 6.5:1 on white, 5.6:1 on page background |
| Secondary text (dark surfaces) | `--gray-neutral-3` | `#c6c6c6` | `#c6c6cd`; `#bdbdbd`, `#a8a8a8` | 12.3:1 on black, 11.0:1 on step 7; covers small all-caps labels |
| Muted / disabled | `--gray-neutral-4` | `#909090` | `#909097`; `#9e9e9e` | Disabled UI is exempt from WCAG contrast; never use for readable small text |
| Border / divider (light surfaces) | `--gray-neutral-3` | `#c6c6c6` | `#c6c6cd`; `#bdbdbd` | |
| Border / divider (dark surfaces) | `--gray-neutral-5` | `#5e5e5e` | `#5e5e64`; `#bdbdbd` | Footer dividers keep their existing low-opacity treatment per footer-redesign-spec.md |
| Interaction (hover, press, selected) | `--color-accent` | `#ceff00` | `#97d600` (hover, v14) | Acid Green — never a success/go signal. Fill only on light surfaces |
| Interaction text on light (text, icons, underlines) | `--color-accent-on-light` | `#5d7400` | | Dark Olive — see Greens by Surface |
| Primary button | `--color-button` | `#303030` | `#ceff00` at rest (v14) | Step 6; white text; outline `--color-button-outline` (step 5 on light) or `--color-button-outline-on-dark` (step 4 on dark) |
| Secondary button outline | `--color-button-2-outline` | `#303030` | | No fill; `#000000` text on light. On dark: `#ffffff` text, outline `--color-button-outline-on-dark` |
| Focus ring (dark surfaces) | `--color-focus` | `#97d600` | | Lime Green — its only UI role |
| Error state | — | `#f50000` | | |
| Site header background | — | `#ffffff` (default) or `#000000` | "always `#000000`" | See Site Header below |
| Body link (light surfaces) | `--color-link` | `#5d7400` | | Underlined at rest; hover step 8 |
| Body link (dark surfaces) | `--color-link-on-dark` | `#ffffff` | | Underlined at rest; hover `#ceff00` (was `#97d600`) |
| Instruction link (light / dark) | `--color-text` / `#ffffff` | `#303030` / `#ffffff` | | Hover: `#5d7400` / `#ceff00`, underlined |

```css
:root {
  --color-bg:              var(--gray-neutral-2);
  --color-surface:         var(--gray-neutral-1);
  --color-surface-dark:    var(--gray-neutral-7);  /* new in v15 */
  --color-text:            var(--gray-neutral-6);
  --color-heading:         var(--gray-neutral-8);
  --color-text-secondary:  var(--gray-neutral-5);
  --color-text-on-dark-2:  var(--gray-neutral-3);
  --color-muted:           var(--gray-neutral-4);
  --color-border:          var(--gray-neutral-3);
  --color-border-on-dark:  var(--gray-neutral-5);

  --color-accent:          #ceff00;  /* hover, press, selected; fill-only on light surfaces */
  --color-hover:           #ceff00;  /* v15: was #97d600; kept as an alias of --color-accent */
  --color-accent-on-light: #5d7400;  /* text, icons, underlines on light surfaces */
  --color-button:          var(--gray-neutral-6);   /* v15 */
  --color-button-outline:  var(--gray-neutral-5);   /* v15, light surfaces */
  --color-button-outline-on-dark: var(--gray-neutral-4); /* v15 */
  --color-button-2-outline: var(--gray-neutral-6);  /* v15, secondary button on light */
  --color-focus:           #97d600;  /* dark surfaces; Lime's only UI role */
  --color-focus-on-light:  #5d7400;  /* light surfaces */
  --color-link:            #5d7400;  /* light surfaces, underlined */
  --color-link-on-dark:    #ffffff;  /* dark surfaces, underlined */
  --color-error:           #f50000;
  --color-on-error:        #ffffff;
  --color-display-dark:    #ffbc00;
}
```

**Mapping `#bdbdbd` (used for two roles in v11).** Decide by what the color is doing, not by its value:
- **Text** (a `color` property) on a dark surface → step 3, `--color-text-on-dark-2`.
- **Border** on a light surface → step 3, `--color-border`.
- **Border** on a dark surface → step 5, `--color-border-on-dark`.
- **Footer dividers** keep their existing low-opacity treatment.
- `#a8a8a8` (minimum secondary text) → step 3 on dark, step 5 on light.

**Migrating color variables.** The live site uses `--color-accent` for Lime Green; this file defines it as Acid Green. Don't repoint the existing name, because every current use would change at once. Instead:
1. Add explicit color names: `--color-acid: #ceff00; --color-lime: #97d600; --color-olive: #5d7400;`
2. Point each role variable above at them (e.g. `--color-accent: var(--color-acid);`).
3. Migrate each existing use by what it does: button at rest → `--color-button` with its outline; hover, press or selected fill → `--color-accent`; green text, icons or strokes on light → `--color-accent-on-light`; body links → `--color-link`. No green should remain on anything at rest except body links on light surfaces and eyebrows on dark. Existing Dark Olive text on light surfaces already passes and stays.

**Migrating to the Neutral scale (v15).** Because every role already goes through a semantic variable, the switch is one change: repoint the role variables from `--gray-cool-*` to the matching `--gray-neutral-*` step (as in the block above). Then:
1. Search site CSS, templates and inline styles for the seven Cool hexes (`#efeff4`, `#c6c6cd`, `#909097`, `#5e5e64`, `#303036`, `#121218`, plus `#efeff2`) and replace each with its role variable.
2. Leave Cool hexes inside chart, infographic and illustration code. Those are graphics surfaces.
3. Keep both scale definitions in `:root`; Cool stays on-system for graphics.
4. Review on staging. The visible change is the page background warming slightly; nothing else should move.

**Off-system grays.** Only the values in the two scales are on-system. Any other gray in the codebase (e.g. `#d4d4d8`, `#b0b0b8`, and the warm family `#888880`, `#4a4a46`, `#ddddd8`) is off-system—the warm family isn't intentional. Snap them all to the **Neutral** scale by role (v15; was Cool) in a later release, using a by-role mapping reviewed on staging. The six named grays come first.

**Text colors (v16).** Every text color is a role variable (or a hex from this file where a component spec gives one). Opacity-based text colors such as `rgba(255,255,255,0.3)` are off-system: they make contrast depend on the surface behind them, and most fail 4.5:1. On dark surfaces, secondary text is `--color-text-on-dark-2` (step 3); muted or disabled is step 4 or 5 per Component States. Low-opacity treatments stay allowed for dividers and decorative strokes (e.g. footer dividers per footer-redesign-spec.md), never for text.

**Implementation note:** after the swap, search the codebase for the six retired grays (`#313131`, `#efeff2`, `#6b6b6b`, `#9e9e9e`, `#bdbdbd`, `#a8a8a8`) and `#ff9600`. None should remain outside this file's history. Cool hexes should remain only in graphics code.

### Section and content-type color (v15)

The Atlas has no per-section color coding. Pulse, For Brands, Research & Writing and Partners all use the same system. A section's identity comes from typography and content, not from a color of its own. Content types (Essay, Field Study, Field Report, Report, Lab Note, Talk, Elsewhere) are told apart by their labels, not by color.

### Tags and Labels (v15)

**Fill or outline, never both.** Tags aren't clickable and have no hover. All tags: Source Code Pro 500, 12px, all caps, letter-spacing 0.08em, line height 1.2, padding `4px 8px` (`3px 7px` when outlined, so heights match), radius 6px.

| Tag type | Examples | Light surfaces | Dark surfaces |
|---|---|---|---|
| Content type | ESSAY, FIELD STUDY, REPORT | `#000000` text on `--gray-neutral-3` `#c6c6c6` fill (12.3:1) | Same |
| Status: confirmed | CHECKED TODAY, HIRED | `#ffffff` text on `#000000` fill | `#000000` text on `#ffffff` fill |
| Status: in progress | BEING TESTED | `#303030` text, `1px solid #303030` | `#ffffff` text, `1px solid #ffffff` |
| Status: excluded | KEPT SEPARATE | `#303030` text, `1px dashed #303030` | `#ffffff` text, `1px dashed #ffffff` |
| Beat category | TECHNOLOGY, HEALTH | 8px circle in the category's `ATLAS_VIZ_COLORS` hex, 6px gap, `#303030` text, `1px solid #c6c6c6` | Same dot, `#ffffff` text, `1px solid #5e5e5e` |

Beat tags carry their color on the dot, not as a fill, because several Tier 4 colors fail 4.5:1 with black or white text. Content-type and status tags never use Tier 3 or Tier 4 colors, and never Dark Olive as a fill.

### Eyebrows (v15)

Source Code Pro 500, 13px, all caps, letter-spacing 0.12em. No arrow, not clickable. `--color-text-secondary` (step 5) on light surfaces; `--color-text-on-dark-2` (step 3) or `#ceff00` on dark surfaces. The → arrow is what separates an instruction link from an eyebrow.

### Site Header

- **White (`#ffffff`) is the default** (the live look). Black (`#000000`) is available when a page needs it, as a deliberate per-page choice.
- Logo must match: `Atlas_logo_lockup_horizontal_blk_web.svg` on white, `Atlas_logo_lockup_horizontal_wht_web.svg` on black. The two files share identical geometry, so swapping them causes no layout shift.
- Nav text follows the header: step 1 on black; step 6 or 8 on white.
- Nav states: see Component States → Nav (v15). Selected: Dark Olive on white, Acid Green on black, both with a 2px underline.
- **Report "Jump to" sub-nav (long-form template):** matches the header and follows the Nav states. On the default white header: white background, step-3 bottom border, items in step 6; hover → Dark Olive, underlined; selected → Dark Olive with a 2px underline. On a black header: black background, items in step 1; hover → Acid Green, underlined; selected → Acid Green with a 2px underline. *(v15: black-header hover moves from Lime to Acid Green.)* This supersedes the black sub-nav in `Atlas-Long-Form-Report-Template-2026-09.md`.
- Anything docked to the header (e.g. the long-form report "Jump to" sub-nav) uses the same background as the header.

### Site Footer (v16)

- **One footer on every public page:** the shared footer rendered by `footer.js`, logo `Atlas_logo_lockup_stacked_wht_web.svg`, layout per `footer-redesign-spec.md`. No page adds its own footer, strip or "Powered by" line; anything a page needs to say at the bottom goes in the page body or the shared footer.
- Footer type (all on the dark footer surface):

| Element | Style | Color |
|---|---|---|
| Column titles | Label: Source Code Pro 500, 13px, all caps, 0.12em, line height 1.4 | `--color-text-on-dark-2` (step 3) |
| Column links | Inter 400, 13px (Small), line height 1.5 | `#ffffff`; hover Acid Green, underlined |
| Tagline | Inter 400, 13px (Small), sentence case, comma form: "The human infrastructure of trust, mapped." | `--color-text-on-dark-2` |
| Copyright line | Tag: Source Code Pro 500, 12px, all caps, 0.08em | `--color-text-on-dark-2` |
| Legal links | Tag: Source Code Pro 500, 12px, all caps, 0.08em | `#ffffff`; hover Acid Green, underlined |

- Touch targets: footer links are at least 44px tall on touch devices (padding, not larger type).

---

## D3 Visualization Color Array (Tier 4 — Data Categories)

*Used in: sunburst/wheel, bubble chart, treemap, all future data visualizations — and any non-chart element that represents a category (tags, labels).*
*Locked May 2026. Probable additions pending Ryan taxonomy confirmation before activation.*

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
  // ⚠ Too light on white and near-duplicates of brand secondary colors.
  //   Before activating: darken, and either adopt the matching brand secondary
  //   hex or move clearly away from it. Requires James sign-off.

  "Reserve A":              "#ea80fc",  // light magenta — near #ff66ff
  "Reserve B":              "#40c4ff",  // light cyan — near #00e5ff
  "Reserve C":              "#ffab40",  // light amber — near #ffaa00

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

**Implementation status (Oct 2026):** none of these values are in live code yet. Charts currently use brand secondary colors as category colors, a known interim state. Moving them to this array is a separate project, gated on Ryan's taxonomy mapping.

**Color assignment rules:**
- Acid green `#ceff00` is excluded — reserved for interaction states (v15)
- Error red is excluded — reserved for system feedback only
- Brand secondary colors (Tier 3) never appear in the same composition as category colors
- All confirmed colors pass contrast on both white and black backgrounds
- Luminosity target: ~50–65% HSL lightness across the confirmed set

---

## Typography

*v15: weight 800 retired; Micro replaced by Label and Tag in Source Code Pro. v16: font allowlist, typeface by role, monospace by role, type floor everywhere, font tokens.*

### Font Allowlist (v16)

These are the only typefaces on journalismatlas.com and in Atlas materials. Anything else is off-system, wherever it appears: a page, a stylesheet, an inline style, a script, a chart, a canvas.

| Family | Weights | Role |
|---|---|---|
| **Inter** | 400, 600, 700 | Everything except the two roles below |
| **Source Code Pro** | 500 only | All-caps labels and tags |
| **Merriweather** | 400 (italic 400 and 700 for inline emphasis) | Body prose inside editorial articles only |
| **Material Symbols Outlined** | Icon font | Icons only (see Iconography) |

**Off-system, by name (not a complete list; the allowlist is what counts):** Hanken Grotesk, DM Mono, JetBrains Mono, DM Sans, Playfair Display, Space Mono, Libre Baskerville, Inter Tight, Source Serif 4, Roboto, Georgia, Arial, Helvetica Neue, and system stacks (`-apple-system`, `BlinkMacSystemFont`, `system-ui`, `Segoe UI`) named on a page. Metric fallbacks for the three fonts are defined once, in `variables.css` (see Font Tokens). The only exceptions are in the Exceptions register.

### Font Stack

| Role | Family | Notes |
|------|--------|-------|
| Primary / UI | **Inter** | Google Fonts. Used everywhere: site, decks, Google Docs. Variable font (wght 100–900); the brand uses 400/600/700. Hanken Grotesk is retired from the brand entirely. |
| Monospace | Source Code Pro | Google Fonts. Weight 500 only. All-caps UI labels: eyebrows, tags, instruction links, footer and nav labels, card meta lines. 13px floor, except 12px tags, badges and card meta lines. |
| Secondary serif | **Merriweather** | Google Fonts. Body prose in editorial articles only (v16: see Typeface by Role). Never headings or display text. |
| Icons | Material Symbols Outlined | Google Fonts. See Iconography. |

### Typeface by Role (v16)

| Element | Typeface |
|---|---|
| Display, H1, H2, H3, H4, on every page including editorial articles | **Inter** (`--font-heading`) |
| Section claims, ledes, decks, subheads, framing lines, intros | **Inter** |
| Stat numerals, pullquotes, captions, figure titles, table text | **Inter** |
| Buttons, forms, nav, cards, body copy on non-article pages | **Inter** (`--font-primary`) |
| All-caps labels: eyebrows, instruction links, tags, badges, card meta lines, footer labels | **Source Code Pro 500** (`--font-mono`) |
| Running body prose (`p`, `li`, blockquote text) inside an **editorial article** | **Merriweather** (`--font-prose`) |

**Editorial articles** are essays and long-form reports published as articles: `watershed/` today, and pages built from the long-form report template. Landing pages, product pages, Pulse, For Brands, partner pages, City Labs and the database are never editorial articles, however editorial their tone. Watershed is the reference: Merriweather prose; Inter for its headings, pullquotes, figures and captions.

### Monospace by Role (v16)

Source Code Pro is for **all-caps labels and tags**. When converting older mono text (DM Mono, JetBrains Mono, or Source Code Pro used outside its role):

| What the text is | Becomes |
|---|---|
| All-caps eyebrow, section label, instruction link, filter or sort label, graphic heading | **Label:** Source Code Pro 500, 13px, caps, 0.08–0.12em |
| All-caps tag, badge, pill, chip, status, count label, card meta line, graphic legend | **Tag:** Source Code Pro 500, 12px, caps, 0.08em |
| Sentence-case text: handles, channel names, places, timestamps, counts in a sentence, notes, tooltips | **Small:** Inter 400, 13px; add `font-variant-numeric: tabular-nums` where numbers align |
| Bold numerals (stats, counts shown large) | **Inter 700** at a type-scale size (48, 36, 28 or 20px), `tabular-nums` |
| Form inputs | **Body:** Inter 400, 16px |

Letter-spacing on mono caps is 0.08em (Tag) or 0.08–0.12em (Label); nothing outside that range. Mono text is never set below 12px or above 13px except where a component spec says otherwise.

### Type Floor (v16)

- **No text below 12px anywhere:** pages, inline `style` attributes, chart and map labels, legends, tooltips, SVG and canvas text, and text written by scripts.
- **12px is Source Code Pro Tag only.** Every other text is 13px (Small) or larger.
- An embedded graphic is its own surface for color (Tier 2), but not for type: the floor applies inside it.
- Where a layout can't fit text at the floor, change the layout (wrap, stack, abbreviate, hide behind a disclosure), never the size.

### Font Tokens (v16)

Pages set type only through these variables. Only `assets/css/variables.css` names a font family.

```css
/* Metric-matched local fallbacks: defined once, here, so the swap to web fonts doesn't shift layout */
@font-face { font-family: "Inter Fallback"; src: local("Arial"), local("Arimo"), local("Liberation Sans"); size-adjust: 107.5%; ascent-override: 90.1%; descent-override: 22.4%; line-gap-override: 0%; }
@font-face { font-family: "Source Code Pro Fallback"; src: local("Courier New"), local("CourierNewPSMT"), local("Liberation Mono"); size-adjust: 100%; ascent-override: 98.4%; descent-override: 27.3%; line-gap-override: 0%; }
@font-face { font-family: "Merriweather Fallback"; src: local("Georgia"); } /* measure overrides for 400 when the next article adopts it */

:root {
  --font-primary: 'Inter', 'Inter Fallback', sans-serif;               /* UI and body */
  --font-heading: var(--font-primary);                                  /* v16: every heading, every page */
  --font-mono:    'Source Code Pro', 'Source Code Pro Fallback', monospace; /* all-caps labels and tags */
  --font-prose:   'Merriweather', 'Merriweather Fallback', serif;       /* v16: editorial article body prose only */
}
```

*Inter and Source Code Pro fallback metrics are carried over from the For Brands and Pulse implementations (measured from the font files). These are implementation values for layout stability, not design values. `--font-editorial` and the legacy `--font-ui` alias are retired: replace uses with `--font-prose` (article body) or `--font-heading` / `--font-primary`.*

### Font Loading (v16)

- The shared `assets/js/header.js` loads the fonts for every page: Inter 400/600/700, Source Code Pro 500 and Material Symbols Outlined. Pages don't add their own font links or `@import`s.
- Editorial article pages also load Merriweather 400 (plus italic 400 and 700 if the prose uses them).
- Target state (see Enforcement): the three fonts and the icon font are served from the site itself, and the site's content-security policy blocks fonts from anywhere else.

### Type Scale

| Level | Size | Weight | Line Height | Use |
|-------|------|--------|-------------|-----|
| Display | 48px | 700 | 1.1 | Hero headings only — homepage, landing pages. Use sparingly. *(v15: was 800)* |
| H1 | 36px | 700 | 1.2 | Page titles |
| H2 | 28px | 700 | 1.25 | Section heads |
| H3 | 20px | 600 | 1.3 | Card titles, drawer headers — often two lines in constrained widths |
| Body | 16px | 400 | 1.6 | Default reading text |
| Small | 13px | 400 | 1.5 | Meta, timestamps, source names, creator bylines — 13px is the floor |
| Label | 13px | 500, Source Code Pro | 1.4 | All caps: eyebrows and instruction links. Letter-spaced 0.08–0.12em *(v15: replaces Micro)* |
| Tag | 12px | 500, Source Code Pro | 1.2 (1.4 for meta lines) | All caps: tags, badges and card meta lines (date · publication). Letter-spaced 0.08em. The only size allowed below the 13px floor *(v15: replaces Micro)* |

Headlines are title case. Buttons are sentence case, Inter 600 at 15px.

**Size variables (v16).** `variables.css` implements the scale as below. Earlier variables that didn't match v15 (`--text-label: 14px`, `--text-micro: 11px`, `--text-body-md: 14px`, `--text-data: 14px`, `--text-micro-legacy: 12px`) are retired.

```css
:root {
  --text-display: 48px;  /* 700, lh 1.1 */
  --text-h1:      36px;  /* 700, lh 1.2 */
  --text-h2:      28px;  /* 700, lh 1.25 */
  --text-h3:      20px;  /* 600, lh 1.3 */
  --text-body:    16px;  /* 400, lh 1.6 */
  --text-button:  15px;  /* Inter 600, buttons only */
  --text-small:   13px;  /* 400, lh 1.5: the floor for everything except Tag */
  --text-label:   13px;  /* Source Code Pro 500, caps, lh 1.4, 0.08–0.12em */
  --text-tag:     12px;  /* Source Code Pro 500, caps, lh 1.2 (1.4 meta lines), 0.08em */
}
```

**Pulse card hierarchy — required implementation pattern:**
- Article title → H3 (20px / 600)
- Creator name → Small (13px / 400)
- Date · Publication → Tag size (12px / 500 Source Code Pro, all caps, step 5 `#5e5e5e`, line height 1.4). Not 13px: at Label size the mono caps outweigh the creator name above it.

### Font Weights in Use
- 400 (regular)
- 500 (medium) — Source Code Pro labels and tags only. *v16: Inter 500 is off-system; map it to 400 (text) or 600 (emphasis, UI).*
- 600 (semibold)
- 700 (bold)
- ~~800 (extrabold)~~ — retired in v15. Inter runs heavier than Hanken Grotesk, which the old scale was based on. ~~900~~ is likewise off-system.

---

## Spacing & Layout

*Unchanged from v11.*

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
3xl: 96px
```

**3xl (96px)** — added Jul 2026 for the footer redesign's column gutter. Use for any layout needing a generous gutter.

### Header Nav Spacing (Aug 2026)

| Gap | Token | Value |
|---|---|---|
| Logo → search bar | `2xl` | 48px |
| Search bar → first nav link | `2xl` | 48px |
| Between nav links (Pulse / For Brands / Research & Writing / Submit) | `xl` | 32px |
| Last nav link → Partners badge | `lg` | 24px |

Search bar capped at roughly 320–360px rather than flexing to fill available space. If cramped, fall back to `lg` (24px) between nav links. Confirm against the real rendered layout; "Research & Writing" is the tightest fit.

### Border Radius
```
card:     6px
button:   6px
input:    6px
tag:      6px   (v15: was 9999px pill)
circle:   50%   photos, avatars and status dots only
```

One radius for everything rectangular. Pills are retired.

### Max Content Width
```
full layout:  1440px — outer container; all content constrained within this, centered with margin: 0 auto
card grid:    1200px — card grids sit inside full layout with comfortable margin on both sides
text column:  680px  — editorial/reading contexts; approx 70 characters at 16px body
```

### Container Inner Padding

```css
.container {
  max-width: 1440px;
  margin-inline: auto;
  padding-inline: 16px; /* md token */
}
```

Apply consistently everywhere the container is used — hero, header, footer, card grids. **Every top-of-page section must use the same `full layout` container as the sections below it — hero sections are not exempt, regardless of any full-bleed background color they carry.** The footer is the reference implementation for the header. See `Atlas-Layout-Fix-Brief-2026-08.md`.

**Reference points:** Bloomberg (~1280px) and Wired (~1440px). The Atlas targets Wired's contained-but-generous feel.

---

## Iconography

*Unchanged from v11, except the selected color on light surfaces (v13).*

- **Icon set:** Material Symbols Outlined
- **Fill states:** Outlined by default, everywhere. **Toggle/action icons only** — save, follow, bookmark, and similar binary-state affordances (e.g. "add to pack") — switch to **filled** when active. **Persistent navigation and section icons stay outlined at every state**, with selection carried by color only (acid green on dark surfaces, Dark Olive on light).
- **Touch targets:** 44×44px minimum.
- **Icon size defaults:**

| Context | Size |
|---------|------|
| Nav | 24px |
| Card header | 24px |
| Inline / body | 18px |
| Section header | 28px |

---

## Component States

**Green means interaction (v15).** Buttons, tags, instruction links and nav rest in monotones. Green appears on hover, press and selected. Two deliberate exceptions rest in green: body links on light surfaces (Dark Olive, underlined) and eyebrows on dark surfaces (Acid Green allowed; not clickable).

### Interactive States

Use these names in code comments and reviews. Avoid "active," which means "being pressed" in CSS (`:active`) but "current page" in conversation.

| State | Meaning | CSS |
|---|---|---|
| Rest | Nothing happening | — |
| Hover / press | Pointer over it, or being clicked or tapped. Treated identically | `:hover`, `:active` |
| Selected | Current page, tab or filter. Persists | `[aria-current]`, `[aria-pressed="true"]`, `[aria-selected="true"]` |
| Focus | Reached by keyboard | `:focus-visible` — `2px solid #97d600` on dark, `2px solid #5d7400` on light, offset `2px` |
| Disabled | Unavailable | `[disabled]`, `[aria-disabled="true"]` |

On touch devices there's no hover; press gives the Acid Green feedback.

### Buttons (v15 — two styles; replaces v14's Primary CTA)

Both styles: 44px min height, 6px radius, Inter 600 15px, sentence case, padding `0 20px`. Both turn Acid Green on hover and press.

**Primary button** — the main action in a group (Search, Sign up, Send). One primary per group.

| State | Light surfaces | Dark surfaces |
|---|---|---|
| Rest | `#303030` fill, `#ffffff` text, `1px solid #5e5e5e` | `#303030` fill, `#ffffff` text, `1px solid #909090` |
| Hover / press | `#ceff00` fill and border, `#000000` text | Same |
| Selected | `#ffffff` fill, `#000000` text, `1px solid #000000` | `#ffffff` fill, `#000000` text, `1px solid #ffffff` |
| Selected + hover | `#ceff00` fill and border, `#000000` text | Same |
| Focus | Rest or current state + `2px solid #5d7400` ring, offset 2px | + `2px solid #97d600` ring, offset 2px |
| Disabled | No fill, `#909090` text, `1px solid #c6c6c6` | No fill, `#5e5e5e` text, `1px solid #303030` |

**Secondary button** — filters and other repeated options (beats, content-type filters, tabs shown as buttons). A row of them stays light so it doesn't compete with the primary action.

| State | Light surfaces | Dark surfaces |
|---|---|---|
| Rest | `transparent` fill, `#000000` text, `1px solid #303030` | `transparent` fill, `#ffffff` text, `1px solid #909090` |
| Hover / press | `#ceff00` fill and border, `#000000` text | Same |
| Selected | `#000000` fill and border, `#ffffff` text | `#ffffff` fill and border, `#000000` text |
| Selected + hover | `#ceff00` fill and border, `#000000` text | Same |
| Focus | + `2px solid #5d7400` ring, offset 2px | + `2px solid #97d600` ring, offset 2px |
| Disabled | No fill, `#909090` text, `1px solid #c6c6c6` | No fill, `#5e5e5e` text, `1px solid #303030` |

Selected is inverted (solid) rather than white, because a white fill would look identical to the outline at rest on a white surface.

Contrast: white on `#303030` 13.2:1; black on Acid Green 17.9:1; black on white 21:1; rest outlines pass 3:1 on both surfaces (`#303030` 13.2:1 on white, `#909090` 6.6:1 on black). There is no separate hover tint: Acid Green is the hover.

**Buttons vs tags:** buttons are 44px, Inter 600 sentence case and respond to hover; tags are 12px Source Code Pro caps (about 20px tall) and never respond to hover. Tags are a fill or an outline, never both.

**Visible change:** the live site's buttons rest in lime. Under v15 they rest in gray and turn Acid Green on hover and press. Dark Olive is never a button fill.

### Links (v15)

| Type | Type style | Light: rest → hover/press | Dark: rest → hover/press |
|---|---|---|---|
| Instruction link (MORE TECH →, VIEW IN ATLAS →) | Label: Source Code Pro 500, 13px, all caps, always ends in ` →` | `#303030` → `#5d7400`, underlined | `#ffffff` → `#ceff00`, underlined |
| Body link (inside a sentence) | Inherits surrounding text | `#5d7400` underlined → `#000000` underlined | `#ffffff` underlined → `#ceff00` underlined |

Underline: 1px, offset 3–4px. Selected instruction links (e.g. a current sub-page) use the hover color with the underline kept on. Body links stay underlined at rest so they never rely on color alone (WCAG 1.4.1).

### Nav (v15)

| State | White header | Black header |
|---|---|---|
| Rest | Step 6 `#303030` (or step 8) | `#ffffff` |
| Hover / press | `#5d7400`, underlined | `#ceff00`, underlined |
| Selected (current page) | `#5d7400`, 2px underline, offset 8px | `#ceff00`, 2px underline, offset 8px |

Nav icons stay outlined at every state; selection is carried by color and underline.

### Card States
- Default
- Hover
- Selected (in pack-builder mode)

---

## Logo Usage

Per the 2026 Style Guide (Atlas-Style_Guide_October_2026_v1.pdf):
- Logo asset library: mirrored in Google Drive (folder `1BT48q5ng6FN0Y0e_XllWvNrI0LFmL_tN`) and Dropbox (linked from the style guide). Both hold the same files; one is a backup of the other.
- **Web SVG logos** (header, footer and other `_web.svg` lockups): Google Drive folder https://drive.google.com/drive/folders/1p0i7PuLqrpOxcrHt0MEKGk1ghnzPXYgv. Pull SVGs for the site from here; the repo copy is what ships.
- Transparent PNGs sized at 500×500px (icons) and 3000×3000px (full logos)
- Contact james@journalismatlas.com for larger sizes or alternate formats

### Header logo

The live header currently uses `Journalism_Atlas_wordmark_horizontal_lockup_black.svg`, which isn't a listed asset. Replace it with `Atlas_logo_lockup_horizontal_blk_web.svg`.

| Header background | Asset |
|---|---|
| White `#ffffff` | `Atlas_logo_lockup_horizontal_blk_web.svg` |
| Black `#000000` | `Atlas_logo_lockup_horizontal_wht_web.svg` *(new, Oct 2026)* |

Both share an identical viewBox (1000 × 134.5) and path geometry. The white file sets `fill="#fff"` explicitly; the black file relies on the SVG default fill (black). Neither responds to CSS `color` — swap the file, don't recolor it.

### Footer logo

- `Atlas_logo_lockup_stacked_wht_web.svg`, white fill, sized to roughly one nav column's width per `footer-redesign-spec.md`. Set dimensions on the `img`/`svg` element directly, not the container.
- The footer's vertical divider rules are a deliberate design element (see `footer-redesign-spec.md`), not a recurrence of the May 2026 `border-right` bug.

**Available logo variants (in repo):**
- `Journalism_Atlas_logo_black.png`
- `Journalism_Atlas_logo_acid_green.png`
- `Journalism_Atlas_logo_dark_gray.png`
- `Journalism_Atlas_logo_light_gray.png`
- `Journalism_Atlas_wordmark_lockup_black.png`
- `Journalism_Atlas_wordmark_lockup_white.png`
- `Journalism_Atlas_wordmark_stacked_black.png`
- `Journalism_Atlas_wordmark_stacked_white.png` *(superseded in footer use — leave in repo)*
- `Journalism_Atlas_wordmark_stacked_gray.png`
- `Journalism_Atlas_wordmark_stacked_green_white.png`
- `Journalism_Atlas_icon_green_transparent.png`
- `Journalism_Atlas_icon_black_transparent.png`
- `Journalism_Atlas_icon_white_transparent.png`
- `Journalism_Atlas_favicon.png`
- `Atlas_logo_lockup_horizontal_blk_web.svg` *(header, white background)*
- `Atlas_logo_lockup_horizontal_wht_web.svg` *(header, black background — new Oct 2026)*
- `Atlas_logo_lockup_stacked_wht_web.svg` *(footer)*

---

## Accessibility

- WCAG 2.1 AA + Material Design 3. 4.5:1 for body text; 3:1 for large text and UI components.
- 13px type floor (12px Source Code Pro at weight 500 excepted for tags, badges and card meta lines); 44×44px touch targets. *v16: the floor applies everywhere, including graphics, inline styles and script-written text (see Type Floor).*
- Text colors are role variables, never opacity-based (see Text colors).
- Body links stay underlined at rest (never color alone). Every interactive element has a visible `:focus-visible` ring.
- Gray step 5 is the lightest step for body or small text on white. Step 4 (3.2:1) is large text and UI only.
- Acid Green and Lime Green are never text, icons or thin strokes on light surfaces. Use Dark Olive there (see Greens by Surface).
- Atlas tokens don't apply to Project C — check projectc.biz/style-guide before flagging its brand choices.

## Enforcement (v16)

The rules are enforced by the build, not by memory.

1. **`scripts/check_brand.py` runs in every build.** `build-dist.sh` runs it before copying files; a failure stops the Cloudflare deploy. It checks against allowlists, so anything not named in this file fails:

| Rule | Fails on |
|---|---|
| `font-family` | Any family not on the font allowlist, in CSS, inline styles, Google Fonts links, `@font-face` or canvas fonts |
| `font-literal` | A font family named on a page instead of `var(--font-*)` |
| `serif-scope` | Merriweather or a serif token outside an editorial article path |
| `serif-heading` | A serif on a heading-like selector, anywhere |
| `font-size` | Text below 12px, including inline styles and canvas fonts |
| `font-weight` | 800 or 900 |
| `pill-radius` | `border-radius` of 999px or 9999px |
| `color` | A hex color not in Tiers 1–5 or the two monotone scales |
| `lime-text` | Lime Green as a text color |

2. **Ratchet, then strict.** Today's site has known violations (2,308 in 59 files in the public repo on October 27, 2026; the count in the working tree will differ). They're recorded in `scripts/brand-baseline.json`. The build fails if any file gains a violation; fixing one lowers the count. When a file reaches zero, it stays at zero. The target is `--strict`: zero violations site-wide, except the Exceptions register.
3. **Protected files.** `.github/CODEOWNERS` names James as required reviewer for this file, the brand guide, `assets/css/variables.css`, `scripts/check_brand.py`, `scripts/brand-baseline.json`, `build-dist.sh`, `_headers`, `CLAUDE.md`, `WORKFLOW.md` and `.github/`. With branch protection on `main`, none of them change without James's approval, and nothing merges if the check fails.
4. **Not yet checked: sizes between scale steps.** About 670 declarations use 14px or 15px outside buttons. They're above the floor, so they don't block this update, but they aren't scale sizes. They're for the next update; the check gains a `font-scale` rule then.
5. **Browser-level lock (final phase).** Once the type consolidation is complete and the check passes `--strict` for fonts, the three fonts and the icon font are self-hosted under `/assets/fonts/`, and `_headers` sets a content-security policy that allows fonts and stylesheets from the site only. The Nodes and Networks paths are exempted from that policy.

---

## Canonical Files (v16)

One location for each design document. Anything else is history.

| File | Location | Status |
|---|---|---|
| Design tokens | `docs/design/DESIGN-TOKENS-v16.md` | Canonical |
| Brand guide | `docs/design/ATLAS-BRAND-GUIDE-v5.md` | Canonical |
| CSS tokens | `assets/css/variables.css` | Canonical implementation of this file |
| Brand check | `scripts/check_brand.py`, `scripts/brand-baseline.json` | Canonical |
| Print, logo and palette reference | `Atlas-Style_Guide_October_2026_v1.pdf` (Dropbox / Drive) | Canonical for logos and print color |
| Session rules for Claude Code | `CLAUDE.md`, `WORKFLOW.md` | Must match this file |
| DESIGN-TOKENS-v15.md, v14 | `docs/design/archive/` | Superseded |
| ATLAS-BRAND-GUIDE-v4.md, v3 (incl. the copy in the repo root) | `docs/design/archive/` | Superseded |
| `pulse_tokens.md` | `docs/design/archive/` | Superseded; page-local tokens are off-system |
| `README.md` § Design System | Replaced by a pointer to this file | Was outdated (Hanken Grotesk, `#CCFF00`) |
| `START-HERE.md` v14 design items | `docs/design/archive/` | Superseded by v15/v16 |
| `james-design-principles.md` / `.pdf` | Root, `docs/`, `_reference/` | Principles stand; where any value conflicts with this file, this file wins. One copy to be kept |
| Dated briefs and ledgers (`docs/briefs/`, `*_ledger.md`, `docs/V1x-*`) | As they are | Implementation records. Older values in them are superseded |

---

## Notes & Decisions Log

| Date | Decision | Rationale |
|------|----------|-----------|
| Feb 2026 | Hanken Grotesk as primary font | Clean, geometric, works well at small sizes for data-dense UI — *superseded Sep 2026* |
| Feb 2026 | Acid green `#ceff00` as primary accent | Brand differentiation, energy, established in Style Guide |
| May 2026 | DM Mono confirmed as monospace font | Replaces JetBrains Mono — *superseded Jul 2026* |
| May 2026 | Merriweather retired from active font stack | No current serif use case — *reactivated Sep 2026* |
| May 2026 | Spacing base unit confirmed as 4px | Per HOW_WE_BUILD.md |
| May 2026 | Border radius: 6px cards/buttons, 9999px pills/tags | Per HOW_WE_BUILD.md — *pills superseded Oct 2026 (v15)* |
| May 2026 | Material Symbols Outlined confirmed as icon set | Replaces earlier Material Icons reference |
| May 2026 | Icon sizes locked: nav 24px, card header 24px, inline 18px, section header 28px | M3 standard sizing adapted for data-dense UI |
| May 2026 | Error state `#f50000` | Needs to grab attention immediately; M3 baseline `#b3261e` too dull |
| May 2026 | Muted/disabled `#9e9e9e` | Balanced contrast on light and dark surfaces — *superseded Oct 2026* |
| May 2026 | Border/divider `#bdbdbd` | Readable, appropriately subtle 1px lines — *superseded Oct 2026* |
| May 2026 | Secondary text (dark surfaces) `#bdbdbd` | Small all-caps labels need more than the bare AA floor — *superseded Oct 2026* |
| May 2026 | D3 viz color array locked (15 confirmed + 3 reserve) | See ATLAS_VIZ_COLORS.md for full decisions log |
| May 2026 | Politics & Govt → `#78909c` warm slate | Red/blue carry partisan US associations |
| May 2026 | Environment → `#26a69a` teal-green | Prevents confusion with brand greens |
| May 2026 | Acid green excluded from viz palette | Reserved for CTAs and active states only |
| May 2026 | Site header always `#000000` | Site-wide constant — *superseded Oct 2026* |
| May 2026 | Footer logo height standard: 40px | *Superseded Jul 2026* |
| May 2026 | Card feature treatments apply to containers, never cards | Cards stay consistent; clicks stay on-site |
| May 2026 | Type scale locked: Display 48 / H1 36 / H2 28 / H3 20 / Body 16 / Small 13 / Micro 11 | ~1.25 ratio above body, tighter below for data-dense contexts — *Display weight and Micro superseded Oct 2026 (v15)* |
| May 2026 | H3 at 20px/600 | Restores Pulse card hierarchy |
| May 2026 | Micro at 11px requires weight 500 minimum | Legibility of small all-caps labels; letter-spaced 0.08–0.1em — *superseded Oct 2026 (v15)* |
| May 2026 | Line heights specified per level | Tighter at large sizes, looser at reading sizes |
| May 2026 | Max content widths locked: 1440 / 1200 / 680px | Stop sprawl on 27" monitors; Wired benchmark |
| May 2026 | Focus ring: `2px solid #97d600`, offset `2px` | On-system, WCAG AA compliant |
| May 2026 | Footer `border-right` cleared on logo container; height targets the `img` | Selector precision — earlier fixes missed the container |
| Jul 2026 | Source Code Pro replaces DM Mono | Footer redesign |
| Jul 2026 | Footer logo → `Atlas_logo_lockup_stacked_wht_web.svg`, sized to ~one nav column | Footer redesign |
| Jul 2026 | Header logo → `Atlas_logo_lockup_horizontal_blk_web.svg` | Header lockup moved to SVG |
| Jul 2026 | Footer column dividers are deliberate | Not a regression of the May 2026 bug |
| Jul 2026 | New spacing token 3xl (96px) | 2× 2xl; footer gutter |
| Aug 2026 | Hero/first-module sections must use the 1440px container | Implementation regression on five pages |
| Aug 2026 | Header constrained to the footer's container; header nav spacing table added | Header/footer inconsistency |
| Aug 2026 | Container inner padding 16px (`md`) | Breathing room on laptops near 1440px |
| Sep 2026 | Primary/UI font: Hanken Grotesk → Inter | Legibility on data-heavy text; closest Google Font to Neue Haas Grotesk; full 400–800 weights |
| Sep 2026 | Merriweather reactivated as paired editorial serif | Screen-legible pairing with Inter; Georgia and Newsreader passed over |
| Sep 2026 | Icon fill-on-select scoped to toggle/action icons | Shape change is an unambiguous click confirmation; nav icons stay outlined |
| **Oct 2026** | **Neutral and Cool 8-step monotone scales replace all previous grays** | The ad-hoc grays (`#313131`, `#efeff2`, `#6b6b6b`, `#9e9e9e`, `#bdbdbd`, `#a8a8a8`) had accumulated role by role. Two consistent scales give every surface, text and border role a defined step, with matched values across scales so they're interchangeable. Neutral step 4 set to `#909090` to keep the 144 base consistent with Cool. |
| **Oct 2026** | **Site uses the Cool scale for semantic roles** | `#efeff2`, the outgoing background, already had a cool cast; Cool step 2 is the closest match, so the visual shift is minimal. Either scale may be used in decks and other materials, but not mixed on one surface. — *superseded Oct 2026 (v15)* |
| **Oct 2026** | **Role remapping** | Primary text → step 6 (13.1:1). Secondary text on light → step 5, darker than `#6b6b6b`, improving contrast (6.4:1 on white). Secondary text on dark → step 3 (12.4:1 on black), absorbing `#bdbdbd` and `#a8a8a8`. Muted/disabled → step 4. Borders → step 3 on light, step 5 on dark. |
| **Oct 2026** | **Step 4 restricted to large text, UI elements and presentation backgrounds** | 3.2:1 on white — passes for large text and UI, fails for body text. |
| **Oct 2026** | **Five-tier color structure: Core brand, Monotones, Brand secondary, Data categories, System** | Brand colors express; data colors encode. The old rule reserving the secondary palette for D3 had been contradicted by the live site, where `ATLAS_VIZ_COLORS` and the secondary palette are entirely different sets. Separating by job prevents a decorative color being read as a category. |
| **Oct 2026** | **`#ffaa00` confirmed as Atlas brand orange; replaces `#ff9600` everywhere** | Style guide values corrected to sRGB 255, 170, 0 / CMYK 0, 33, 100, 0. One orange across brand and code. |
| **Oct 2026** | **Dark Olive `#5d7400` retired from UI** | Stays in the brand palette for design elements only. |
| **Oct 2026** | **Site header: black or white** | The "always black" constant had become fluid in practice. Header color is now a design choice; logo and docked elements must match it. |
| **Oct 2026** | **New asset: `Atlas_logo_lockup_horizontal_wht_web.svg`** | White header logo for the black-header option; identical geometry to the black version, so no layout shift on swap. |
| **Oct 2026** | **Reserve slots A/B/C flagged as near-duplicates of brand secondary colors** | `#ea80fc`/`#ff66ff`, `#40c4ff`/`#00e5ff`, `#ffab40`/`#ffaa00`. Before activation, darken and either align with or clearly separate from the secondary color. No values changed in v12. |
| **Oct 2026 (v13)** | **Greens by surface: Acid and Lime Green are fill-only on light surfaces** | Both fail the 3:1 non-text minimum on white (1.2:1 and 1.8:1). On light surfaces they work only as fills with black or step-6 text on top (17.9:1 / 11.2:1 for acid). On dark surfaces they keep their existing roles. A rumored "acid on dark only, lime on light only" rule was never canon and fails on contrast. |
| **Oct 2026 (v13)** | **Dark Olive `#5d7400` returns to the UI as the green for text, icons and thin strokes on light surfaces** | The only existing brand green that passes on light surfaces (5.3:1 on white, 4.6:1 on step 2). Reuses a brand color rather than inventing one. Narrows, rather than reverses, v12's retirement: it's still never a fill, CTA background or hover fill. |
| **Oct 2026 (v13)** | **Focus ring is Dark Olive on light surfaces** | The Lime Green ring fails 3:1 on white. Lime stays the focus ring on dark surfaces. |
| **Oct 2026 (v14)** | **Site header: white is the default; black when a page needs it** | White is the live look, so the default causes no visible change. Docked elements match the header, so the report sub-nav moves from black to white, with Dark Olive active and hover states (acid would be invisible on white). |
| **Oct 2026 (v14)** | **Inline links: Dark Olive, underlined, on light surfaces; white, underlined, on dark** | Keeps green as the signal for "interactive" on light surfaces at a passing ratio (5.3:1). On dark surfaces, acid is reserved for one moment per composition and lime is hover-only, so links rest in white. |
| **Oct 2026 (v14)** | **Color variables migrate by role; `--color-accent` isn't repointed in place** | The live site uses `--color-accent` for lime. Repointing it would change every use at once; explicit names plus a by-role migration keeps each change deliberate. |
| **Oct 2026 (v14)** | **All grays outside the two scales are off-system** | A staging audit found ~107 other colors in use, including an unintended warm-gray family. They snap to the Cool scale by role in a later release. — *target scale changed to Neutral in v15* |
| **Oct 2026 (v14)** | **Charts move to `ATLAS_VIZ_COLORS` as a separate project** | No category colors are in live code yet; charts currently use brand secondary colors, some too pale on white. The move needs Ryan's taxonomy mapping first. Until then this is a known interim state. |
| **Oct 2026 (v13)** | **`#bdbdbd` mapping clarified by role** | v11 used it for text on dark and for borders on both surfaces. Text → step 3; border on light → step 3; border on dark → step 5. |
| **Oct 2026 (v13)** | **Tier 2 contrast figures show both scales** | v12 listed the Neutral figures only; the site uses Cool. Both are now shown (e.g. 13.2 / 13.1:1). |
| **Oct 2026 (v14)** | **Primary CTA: acid at rest and active, lime on hover, black text** | Restores Acid Green as the primary accent the brand defines, with lime as the hover response. Reviewed as a rendered comparison against today's lime-at-rest buttons before sign-off. — *superseded Oct 2026 (v15)* |
| **Oct 2026 (v15)** | **Site moves from the Cool to the Neutral scale** | Part of an ongoing evaluation of the brand as the site expands in new directions. Contrast is matched across scales (within 0.1), so no accessibility change. One variable repoint per role. |
| **Oct 2026 (v15)** | **Cool becomes the graphics scale; an embedded graphic is its own surface** | Gives Cool a defined job instead of being a near-duplicate, and resolves the one-scale-per-surface rule for charts placed on pages. |
| **Oct 2026 (v15)** | **Off-system grays snap to Neutral** | Follows the site scale. |
| **Oct 2026 (v15)** | **No color coding by section or content type** | Restates the brand rule here so implementation can't drift. A short-lived content-type color experiment was rejected: Tier 3 can't carry meaning and Tier 4 hexes already mean beats. |
| **Oct 2026 (v15)** | **Tags split by job: category tags Tier 4; content-type and status labels monotone** | Keeps "data colors encode" true: only beat categories get a color. |
| **Oct 2026 (v15)** | **Tags are fill or outline; buttons are separated from tags by size, case and typeface** | Buttons (44px, Inter sentence case, hover) and tags (12px mono caps, no hover) can't be confused even when both are outlined. Beat color moves to a dot so every tag passes contrast. |
| **Oct 2026 (v15)** | **Secondary (outline) button for filters and repeated options** | A row of nine solid beat buttons competed with the Search button. Outline buttons (Material Design 3's medium-emphasis "outlined" pattern) keep the row light and the primary action clear. Selected inverts to solid so it stays visible on white. |
| **Oct 2026 (v15)** | **Green means interaction** | Buttons rest in gray and turn Acid Green on hover and press; lime-at-rest buttons were confusing. Acid Green may also mark eyebrows on dark surfaces. The one-acid-moment limit is dropped. Lime Green is reduced to the dark-surface focus ring so focus stays distinct from hover. |
| **Oct 2026 (v15)** | **Hover and press treated the same** | Material Design 3 separates them only by a faint tint (8% vs 10%); one clear Acid Green change is easier to read, and touch devices have no hover anyway. A separate hover tint was considered and rejected as a third look with no benefit. |
| **Oct 2026 (v15)** | **Selected is its own state: white button, or green with 2px underline for nav** | Without it, "pointing at" and "currently here" would look identical. |
| **Oct 2026 (v15)** | **Instruction links: Source Code Pro caps, → arrow, underline on hover** | Fixes mixed case and mismatched hover colors on the live homepage (e.g. white vs acid hovers on the same dark background). The arrow separates links from eyebrows. |
| **Oct 2026 (v15)** | **One radius: 6px; pills retired** | Compared 4px and 6px side by side; 6px gives a more definite corner. Pills read too round. |
| **Oct 2026 (v15)** | **Weight 800 retired; Display to 700** | The old scale was set for Hanken Grotesk; Inter is heavier, so 700 does the same job. |
| **Oct 2026 (v15)** | **All-caps labels move to Source Code Pro 500 (13px labels, 12px tags)** | One typeface for all UI chrome. 12px is allowed below the 13px floor for tags, badges and card meta lines. |
| **Oct 2026 (v15)** | **Pulse card date · publication line at 12px, not 13px** | Compared rendered: at 13px the mono caps outweighed the creator name and widened the line; 12px stays secondary and matches the beat tag on the same card. Up from 11px today. |
| **Oct 2026 (v16)** | **Design values are locked; Justin decides everything else** | For Brands and Pulse shipped with Merriweather headlines because a brief named a display serif and the tokens never said which face headings use. Locking values to this file, and enforcing them in the build, means a brief can't move them. |
| **Oct 2026 (v16)** | **Font allowlist: Inter, Merriweather, Source Code Pro (plus Material Symbols for icons)** | One coherent site. A blocklist always misses the next font; an allowlist doesn't. |
| **Oct 2026 (v16)** | **Headings are always Inter; Merriweather is article body prose only** | v15's "editorial body copy" was read as a tone, not a content type. Watershed is the model: serif for reading, Inter for structure. |
| **Oct 2026 (v16)** | **Monospace by role; sentence-case mono and bold mono numerals become Inter** | v15 gave Source Code Pro to all-caps labels only, but about 40 older mono declarations were sentence case and several were bold numerals at 22–28px. Mapping them to existing Inter levels adds no new values. |
| **Oct 2026 (v16)** | **Type floor applies everywhere, including graphics** | About 400 declarations set text below 12px (8–11px), mostly in mono labels, legends and the footer. One floor with no surface exceptions is simpler to check and meets WCAG intent. |
| **Oct 2026 (v16)** | **Footer type specified; one footer site-wide** | The footer ran at 9–10px, and five lab and partner pages added a second 9px "Powered by" strip at 22% white. |
| **Oct 2026 (v16)** | **Inter 500 off-system** | v15 already limited 500 to Source Code Pro; v16 states it for Inter so the font load can drop it. |
| **Oct 2026 (v16)** | **Opacity-based text colors off-system** | White at 18–45% opacity fails contrast and varies with the surface. Role variables are fixed and tested. |
| **Oct 2026 (v16)** | **Exceptions register: Nodes and Networks (co-branded), internal Google Form mock-up** | Co-branded reports can carry partner design. Named by path so the exception can't spread. |
| **Oct 2026 (v16)** | **Enforcement: allowlist check with a ratchet baseline, CODEOWNERS, then a font content-security policy** | Rules in documents depend on every session reading them; a build check doesn't. |
