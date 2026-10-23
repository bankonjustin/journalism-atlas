# V15 Scope Buckets

*Oct 22, 2026. Every item from "What changed in v15" (`DESIGN-TOKENS-v15.md` L10–26), plus the items v15 carries over from v14 that are still unimplemented, appears in exactly one bucket. Evidence and counts are in `V15-DISCOVERY-REPORT.md` (track references in brackets). Items are in suggested ship order within each bucket.*

**Totals: GREEN 16 · AMBER 16 · RED 5**, plus 4 prerequisites that aren't in v15 but should ride in Session 1 (end of file).

How to read "rollback": every GREEN item is meant to be one commit, so the rollback is `git revert` of that commit in GitHub Desktop. "Pages" means pages from the 40-page public set unless stated.

**Dependency map (short):** G1+G2+G3 ship as **one commit** (a repoint without the hex swaps leaves mixed-scale pages). G7 depends on nothing, but only looks right with G10 and A2/A3, so ship it with them. A6, A7 and A9 depend on P1 (Source Code Pro 500 loaded). A4 depends on A6's Label style. A8 (dropping Inter 500) must precede removing weight 500 from the font URL (P1 does the add, not the drop). R1 depends on Ryan's taxonomy mapping. A2/A3 depend on G7.

---

## GREEN: ship live without James

**G1. Repoint gray role variables from Cool to Neutral** *(v15 bullet: "The website moves to the Neutral scale")* [B]
- Files: `assets/css/variables.css` only (role variables `--color-bg/-text/-text-secondary/-muted/-border/-border-hover/-surface/-heading/-text-on-dark-2/-border-on-dark/-bg-dark/-text-dark/-muted-dark`, legacy `--light-gray/--dark-gray/--color-light-gray/--color-dark-gray`, plus `header.css`'s `var(--gray-cool-*)` uses).
- Pages: moves **6 public pages fully, 20 partly, 13 not at all** on its own. **Do not ship alone.**
- Visible effect: page background `#efeff4` → `#efefef`; text `#303036` → `#303030`. Contrast within 0.1 (v15 L129).
- Rollback: one commit. *Depends on G3 shipping in the same commit.*

**G2. Disabled/muted becomes `#909090` (Neutral step 4)** *(bullet: "Disabled state…")* [B]
- Files: rides on G1 through `--color-muted`; `research.html`/`header.css`/`partners/*` disabled rules use `var(--gray-cool-4/5)` and need the same swap (36 files have disabled rules).
- Visible effect: none (`#909097` → `#909090`).
- Rollback: same commit as G1.

**G3. Complete the Neutral move: Cool-hex replacement, unpin aliases, link `variables.css`** *(bullet: "Migration")* [B, C2]
- Files: **413 chrome hits of Cool hexes on public pages** (in 32 files, including 13 curator partner pages at 10–13 each, `index` 15, `pulse` 19, `wire` 18, `for-brands` 16, `research` 16, `city-lab-chicago` 24, `partners/nj-lab`/`njlab` 48 each), `header.css` footer (`#c6c6cd` ×4 and `#303036`), local `--page-bg: #efeff4` on ~15 pages (13 curator pages, `co-ops`, `bluesky-creator-intelligence`), `body { background: #efeff4 }` on `index`/`pulse`/`research`/nj-lab; remove the inline `--light-gray`/`--dark-gray` pins on `about-this-project`, `advisory`, `how-we-did-this`, `who-we-are`, `mobile`.
- Replace each hex with its role variable by role (v15 L233). The 17 Cool hits in public graphics stay (G4).
- Visible effect: background warms slightly; nothing else should move.
- Rollback: one commit. Review on a preview URL or staging (see P4).

**G4. Cool stays in graphics code; guard it** *(bullet: "Cool becomes the graphics scale")* [C2]
- Files: no change to the 25 graphics hits (`watershed-preview` SVG, nj-lab viz labels, Pulse heatmap cells). Add a one-line comment convention. Check the classification once by eye before G3's bulk replace.
- Visible effect: none. Rollback: n/a.

**G5. Embedded graphics count as their own surface** *(bullet)*
- Docs only (CLAUDE.md, `variables.css` header). Visible effect: none. Rollback: one commit.

**G6. No color coding by section or content type** *(bullet)* [E]
- Docs only. Audit found no per-section color coding in the chrome (platform-brand fills such as `.plat-instagram` are handled in A9). Visible effect: none.

**G7. `--color-hover` becomes Acid; move the 24 direct-Lime hovers** *(bullet: "Green means interaction", first clause)* [D]
- Files: `variables.css` (`--color-hover: var(--color-acid)`). **Zero repoint hazards**: all 67 current uses are fills or sit on dark surfaces. Then move the 24 hover/press rules that use Lime directly (public: `header.css` `.nav-search-btn:hover` (every page), `main.css` ×3, `partners/nj-lab|njlab` `.cta-primary:hover`, `city-lab-chicago` `.beats-toggle-btn:hover`, `watershed-preview`).
- Visible effect: hover fills go from Lime to the brighter Acid on ~37 pages.
- Rollback: one commit. *Looks right only alongside G10, A2, A3.*

**G8. One-acid-moment limit dropped** *(bullet)* · Docs only (CLAUDE.md L71 and the Pulse/homepage comments). Visible effect: none.

**G9. Resting green on non-interactive things becomes monotone** *(bullet: "No green at rest except…", v15 L230)* [D]
- Files: **olive text/borders on non-links: 1,154 elements on 21 pages**, e.g. `.creator-channel` and `.ci-followers`-type meta (13 curator pages, `bluesky-creator-intelligence`), `.org-structure`, `.ticker-card-byline`, `.cluster-count-n`; olive fills that aren't tags (`.creator-chip-count`, `.pulse-live-badge`). Rule: secondary text step 5, strokes step 3. Olive on dark (4 elements) → Acid.
- Visible effect: green meta text turns gray. Moderate and visible, but the rule is mechanical.
- Not included here: Acid fills on buttons (A2/A3), Lime remnants (A10), bars/dots (R4), `.card-link` (A4).
- Rollback: one commit.

**G10. Body links** *(bullet: Links, second row; dark-surface hover moves Lime → Acid)* [E]
- Files: `--color-link` (olive, underlined) on light with hover black; `--color-link-on-dark` white underlined with hover Acid. Where the underline is already present (237 anchors resolve olive+underline in the runtime scan) nothing changes; fix the pages where body links in prose lack it. Pages: partners (4 each), `about-this-project`, `contact`, `watershed-preview` (163).
- Visible effect: small. Rollback: one commit. *The "CTA links inside sentences" decision from `START-HERE.md` #2 maps to A4.*

**G11. Weight 800 retired; Display = 700** *(bullets: "weight 800 retired, Display drops to 700")* [C5, F]
- Files: **58 declarations in 12 files** (33 on 5 public pages: `city-lab-dc-v3` 14, `mobile` 7, `bluesky-creator-intelligence` 5, `teamdmv` 4, `lists` 3); `assets/js/main.js:1873` (D3 `font-weight 800`); `variables.css` `--weight-extrabold`/`--text-display` comment; remove `800` from the Inter URL in `header.js` and 19 page `<link>`/`@import`s.
- Visible effect: big headlines on those pages get slightly lighter.
- Rollback: one commit.

**G12. Pills retired: pill-radius rules become 6px** *(bullet: "Radius: 6px for everything; pills retired")* [C7]
- Files: **134 pill rules on 30 public pages** (`100px` ×133, `9999px` ×24; `city-lab-chicago` 17, `pulse` 14, `index` 12, `for-brands` 8); `variables.css` `--radius-pill`. `50%` circles stay (53 on public pages). Other radii (2–16px) are A15.
- Visible effect: round chips and tags become rounded rectangles across most pages. **Most visible GREEN item.** Many of these are clickable chips (R2/A3), so Justin may prefer to ship it with the tag/button work.
- Rollback: one commit.

**G13. Nav states: rest step 6, hover Dark Olive underlined, selected Dark Olive 2px underline, offset 8px** *(v15 "Nav (v15)", L535–543; carried from v14)* [E]
- Files: `header.js` (mark the current link with `aria-current="page"` from `location.pathname`: **no code sets it today**), `header.css` (`.nav-link:hover` currently goes black; `--header-fg-hover` stays for the black theme: Acid + underline). Typeface is **R3**, not here.
- Pages: all 37 that load `header.js`. Visible effect: a current-page indicator appears; hover turns olive.
- Rollback: one commit.

**G14. Content-type and status tags (exact spec)** *(bullet: "Tags: … content type, status…")* [E]
- Files: new `.tag` component CSS only (v15 L246–258). **No live instances** of the status tags (CHECKED TODAY, HIRED, BEING TESTED, KEPT SEPARATE appear only in `_deprecated/`) and content-type labels (Essay, Field Study…) appear only in the generated nodes-and-networks page and Pulse copy. Depends on P1 for SCP 500.
- Visible effect: none until used. Rollback: one commit.

**G15. Owner contact and doc updates** *(bullet: "Owner contact updated")* [A]
- Files: `CLAUDE.md` (proposed section: report Appendix B), `WORKFLOW.md`, `START-HERE.md`, `variables.css`/`header.css`/`header.js`/`main.css` header comments (v14→v15), `james@happicamp.com` → `james@journalismatlas.com`, and decide where the v15/v4 files live. Page comments can age out.
- Visible effect: none. Rollback: one commit.

**G16. Add the missing v15 variables (additive)** *(v15 L190–217)* [B]
- Files: `variables.css` only: `--color-surface-dark`, `--color-button`, `--color-button-outline`, `--color-button-outline-on-dark`, `--color-button-2-outline`; fix dead `--focus-ring-light/dark` (zero uses) and `--space-3xl: 96px` (check the 5 uses first); drop `--text-micro` and add Label/Tag tokens once A6 decides.
- Visible effect: none. Rollback: one commit.

---

## AMBER: ship with a default, James can veto

**A1. Off-system grays snap to Neutral by role** *(bullet: "Off-system grays now snap to Neutral")* [C]
- Evidence: 128 distinct off-scale grays, 2,004 uses (the warm family `#4a4a46`, `#ddddd8`, `#888880`, the `#1a1a18` family ×288, `#d4d4d8` ×107, `#b0b0b8` ×70, `#606068` ×70, and others). v15 itself says "a later release" using a by-role mapping reviewed on staging.
- **Default:** retarget the existing by-role proposal (`docs/V12-UNMAPPED-GRAYS-PROPOSAL-2026-10-06.md`) from Cool to Neutral and apply it to the public pages only. Last in the order: biggest and least reversible by eye.
- James question: none needed; the warm family was already ruled "not intentional".

**A2. Primary button** *(bullet: "Buttons: two styles", primary)* [D, E]
- Evidence: Acid-fill primaries on 37 pages, the header Search button on every page (`header.css`, 12px/700, 6px 14px padding, Acid, hover Lime), `.atlas-footer-btn` ×14, `.btn-acid`/`.btn-lime`/`.btn-primary`/`.cta-btn`/`.form-submit`/`.contact-email-btn`/`.submit-btn`.
- **Default:** classify each page's main action as primary (step-6 fill, white text, step-5 outline, 44px, Inter 600 15px); everything in a filter/option row is A3. A primary is never "selected" (Q12). The header Search button goes from 27px to 44px (the field beside it is 41px; the header grows about 3px) (Q14). Hero CTAs on black pages (homepage `.btn-acid`) follow the dark-surface spec (Q14).
- Questions: Q12, Q14. Depends on G7.

**A3. Secondary buttons: filter and beat rows, tabs shown as buttons** *(bullet: secondary)* [E]
- Evidence: `.hcn-pill`, `.beat-pill`, `.recency-btn`, `.chip.active` (Acid fill, 13 pages), `.filter-chip`, `.beat-chip/.plat-chip`, `.view-btn`; underline-style tab strips (`.tab-btn` in `city-lab-chicago`, for-brands tablist) are **NOT COVERED** by v15.
- **Default:** outline buttons; selected = black fill (white on dark). Acid-fill "active" chips become black. Underline tab strips are left alone. Dense rows keep their current height rather than 44px until James rules on Q15/R2.
- Question: R2 (clickable tags), Q15. Depends on G7.

**A4. Instruction links (`… →`)** *(bullet: Links, first row)* [E]
- Evidence: **124 arrow links in 29 files**, all sentence/title case, wording varies for the same destination; `.card-link` ×253 elements (13 partner pages, `co-ops`) are olive Inter 14px with a hover fill, a button-like link.
- **Default:** Source Code Pro 500 13px caps, letter-spacing **0.1em**, ` →` retained, step 6 at rest, Dark Olive underlined on hover (white → Acid on dark). `.card-link` becomes an instruction link (not a button). Wording left as is; copy unification is a separate pass.
- Questions: Q11, Q15. Depends on P1, A6.

**A5. Eyebrows** *(v15 L260–262)* [E]
- Evidence: `.hero-eyebrow` on **22 pages** (DM Mono 10px caps 0.12em), plus 20 others in Acid, white at 30–40% opacity, olive, step-5 gray.
- **Default:** SCP 500 13px caps 0.12em; step 5 on light, **step 3 on dark** (Acid only where an eyebrow currently is Acid and is the first label on its section: dark `p.hero-eyebrow`, `.lab-eyebrow`, `.spotlight-eyebrow`). Question: Q10. Depends on P1.

**A6. Micro → Label/Tag: convert mono-caps and caps labels** *(bullet: Typography, "Micro replaced by Label and Tag")* [C9]
- Evidence: **338 `text-transform: uppercase` rules (256 on public pages)**; DM Mono 74, JetBrains 26, Inter 231 (weight 700 ×117); sizes 9–13px; spacing 0.04–0.15em; `.nav-soon-badge` and footer labels too.
- **Default mapping (by selector role):** eyebrows and links → Label (13px, 0.08–0.12em); tags/badges/card meta → Tag (12px, 0.08em, line-height 1.2/1.4); table and stat labels → Label. All SCP 500. Remove the `header.css` JetBrains `@import` and DM Mono loads when the last user is converted.
- Question: Q1/Q9 for nav and footer. Depends on P1. Large visible change; ship per page group with before/after screenshots.

**A7. 13px floor for non-caps small text** *(Typography, Small 13px; 12px SCP exception only)* [C8]
- Evidence: **488 sub-13px rules on 34 public pages** (11px ×254, 12px ×252, 10px ×107, 9px ×102, 8px ×9), most non-caps Inter; plus 78 chart/SVG text sizes (graphics, out of scope).
- **Default:** raise non-caps Inter 9–12px text to 13px; 12px stays only as SCP Tag/meta after A6. Chart text is excluded. Expect reflow on dense pages (`pulse`, `index` tickers, partner cards).

**A8. Inter weight 500** *(Typography weights, "500: Source Code Pro only")* [C6]
- Evidence: **132 Inter-500 declarations (93 on public pages, 21 files)**: labels 27, tags/chips/pills 25, buttons 16, cards 9, nav 7, other 48.
- **Default:** 500 → 600 for buttons, nav, links and card titles; 500 → 400 for meta/captions; tags/labels go to SCP 500 via A6. Then drop 500 from the Inter URL. Question: Q5.

**A9. Platform tags (Newsletter, Podcast, …)** *(bullet: Tags)* [E]
- Evidence: `.db-pill.platform` (black fill), `.pill.platform` (outline, clickable, hover Lime), `.platform-tag`, `.plat-instagram` etc. brand-hex fills. v15 doesn't list this type.
- **Default:** monotone outline tag (`1px solid #c6c6c6`, step 6 text), no platform colors, non-clickable. Question: Q4. Depends on P1, G14.

**A10. Lime remnants outside the focus ring** *(bullet: "Lime… keyboard focus ring on dark only")* [D]
- Evidence: header `.nav-pulse-dot` (Lime fill, every page), nj-lab `.badge-verified` (Lime fill, 19 ×2), `.ci-platform.cross` (226 on the Bluesky page), mobile-menu hover border (Lime), `.nav-search:focus` border + glow (Lime on light), `.tab-btn.active` tint.
- **Default:** pulse dot → step 6 `#303030` (keeps the animation); verified badge → status tag "confirmed" (black fill, white text); mobile-menu border → Dark Olive; nav-search focus → olive only. Nothing else uses Lime. Questions: none needed beyond Q8 for the viz uses.

**A11. Table headers and data tables** [E]
- Evidence: `.creators-table th` (dark header, 700, Acid sort arrows, `#424242` hover), `.viz-creators-table th`.
- **Default:** header cells use the Label style (SCP 500 13px caps, white on step 6 as today); sort arrows Acid on dark; no other change. Question: Q6. Depends on P1.

**A12. Icon-only and toggle/action buttons (hover, press, selected on light)** [E]
- Evidence: hamburger/close in `header.css`, drawer close, and `search.html`'s add-to-pack; no save/follow/bookmark exists live.
- **Default:** 44×44, transparent at rest; hover/press = Acid fill with black icon; selected = Dark Olive filled glyph (light surface), Acid (dark). Question: Q7.

**A13. Footer links and labels** [E]
- Evidence: footer link Inter 13px `rgba(255,255,255,.55)` hover `#fff`; column titles/copy/legal **9–10px** mono caps loaded at 400 only; `#c6c6cd` hardcoded.
- **Default:** titles → Label (SCP 500 13px caps, step 3 `#c6c6c6`); links → Inter 13px step 3, hover white underlined; legal → Tag (12px). Question: Q9. Depends on P1.

**A14. Card hover and form inputs** [E]
- Evidence: `.creator-card:hover` = background `--color-bg` + border `--color-border-hover`; `.cluster-card:hover` border only; inputs have 4/6/8px radii.
- **Default:** keep the current hover behavior; retarget grays (G1/A1) and radius (A15) only. Inputs: 6px radius, olive focus border. Question: Q13.

**A15. Other radii (2, 3, 4, 8, 10, 12, 16px) vs "one radius"** [C7]
- Evidence: ~140 non-6px rules on public pages (badges 2px, selects 4px, cards 8–12px, mobile drawer 16px, modal `--radius-modal: 8px`).
- **Default:** form controls, cards, buttons, tags → 6px; bars/progress fills (2px), scrollbars, tooltips keep their value. James hasn't spoken to modals/drawers.

**A16. Components v15 doesn't cover** (mobile-menu link states, tooltips, drawers, pagination/"more" buttons, checkboxes/radios/selects, `:visited`) [E]
- **Default:** leave as they are except gray/radius retargeting (G1, A15) and removing Lime (A10). No James question unless he wants a spec.

---

## RED: blocked on James (or Ryan)

**R1. Beat category dots (`ATLAS_VIZ_COLORS`)** *(bullet: "Tags… beat category")* [G]
- Why blocked: 1 of 79 data topics matches a key; 0 of 9 groups; four hardcoded vocabularies map the same 9 keys differently; Pulse has its own 14-hex `BEAT_COLORS`. Needs Ryan's `topic → key` mapping and one display name per key. Only the hardcoded homepage cluster cards (6 of 9 exact) could ship early. Question: Q2.

**R2. Clickable tags** *(v15 L248: "Tags aren't clickable")* [E]
- Why blocked: existing clickable pills filter on click (`.creator-tag.clickable-tag`, `.creator-meta-item.clickable-tag` on every search card; `.pill.platform` on 13 partner pages; `.hcn-pill`, `.beat-pill`). Turning them into 44px buttons wrecks card density; leaving them as pills breaks the rule. No safe default. Question: Q3.

**R3. Main nav typeface** [E]
- Why blocked: v15 L359 says nav labels are SCP caps, the Nav section is silent; SCP caps adds 49px to the nav (581 → 630px) and pushes the overflow breakpoint up to 1280px unless gaps drop 40 → 32px. Question: Q1. (The nav already overflows below ~1100px today.) G13 ships the color/underline part without waiting.

**R4. Green inside charts / moving charts to `ATLAS_VIZ_COLORS`** *(carried from v14, "separate project")* [D, G]
- Why blocked: needs Ryan's mapping and James's call on whether Acid/Lime categories (`index` `CLUSTERS`, `search` `FIELD_GROUP_COLORS`/`FIELD_PLATFORM_COLORS`, bars and dots in `pulse`) stay or go. Question: Q8.

**R5. Long-form report: shared chrome and white "Jump to" sub-nav** *(carried from v14; v15 L270)* [E, I]
- Why blocked: the report page is generated (`tools/preview-build`) and does not use the shared header, footer, Inter, Merriweather or tokens; its template spec `Atlas-Long-Form-Report-Template-2026-09.md` isn't in the repo. Question: Q16.

---

## Prerequisites (not in v15, but v15 can't land without them)

- **P1. Fonts:** load Source Code Pro 500 (add to `header.js`; update `footer.js`), decide Merriweather loading, remove 800 (that part is G11). **Do not drop Inter 500 or JetBrains/DM Mono yet.** Files: `header.js`, `footer.js`. Visible effect: none.
- **P2. Broken loads:** fix `partners/nj-lab|njlab` `variables.css` path (`/assets/...`), link `variables.css` on `mobile` and `lists` (lists changes background `#f5f5f5` → `#efefef` and drops its off-system lime). Decide which nj-lab copy is canonical. Visible effect: small, visible on those pages. Ship before G3.
- **P3. Decide where `DESIGN-TOKENS-v15.md` and `ATLAS-BRAND-GUIDE-v4.md` live** (root vs `docs/design/`) and commit them; update CLAUDE.md in G15.
- **P4. Check Cloudflare preview deployments** (Justin) before any visible item ships.

---

## Recommended session shape

- **Session 1 (invisible or near-invisible; safe to push):** P2, P1 (additive), G15, G16, G5, G6, G8, G4, then **G1+G2+G3 as one commit**, then G11 (800→700). Review the Neutral move against the 14 baseline PNGs.
- **Session 2 (the green model and buttons, after a staging look):** G7, G9, G10, G13, A10, G12 (or hold G12 for Session 3), A2, A3.
- **Session 3 (type system, after James's answers):** A5, A6, A7, A8, A4, A9, A11–A14, G14, then A1 and A15 last.
- **Waiting on James/Ryan:** R1–R5.
