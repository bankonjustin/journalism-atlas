# Atlas — Design Questions for James
*May 2026 · From Justin · For discussion before the next implementation session*

These are open questions that surfaced during the May 2026 design and QA session. Some are blocking for future Claude Code work. Some are judgment calls only James can make.

---

## Blocking — Claude Code can't proceed without these

### 1. Creator profile pages — live 404s
The homepage cluster drawer links to `/creators/[slug]` — individual creator profile pages. These currently 404. A visitor who clicks a creator name from the homepage hits a dead end.

**Need from James:** Is there a design for creator profile pages? What's the timeline? This is the biggest missing piece in the current user journey.

### 2. D3 visualization color array
The bubble chart, treemap, and any future data visualization are using an improvised three-color array. Every topic category needs a stable color assignment so vizzes are consistent across views and future pages.

**Need from James:** A full color array for all beat clusters (Politics & Government, Local News, Technology, Business & Finance, Culture & Arts, Sports, Health, Environment, International) plus any additional categories Ryan's taxonomy includes. These should be drawn from or harmonious with the brand palette.

### 3. Semantic colors — three gaps
Error state, muted/disabled, and border/divider colors are unassigned in the token file. These will be needed as soon as any form, filter, or interactive state is built.

**Need from James:** Hex values for all three. Suggested starting points to react to: error → something in the red/amber range; muted/disabled → mid-gray near `#a8a8a8`; border/divider → `#d4d4d8` is currently used in some places.

### 4. Icon size defaults
Material Symbols Outlined is confirmed. But there's no default size in the token file — 20px? 24px? Different sizes for different contexts?

**Need from James:** Default icon sizes for nav, card header, inline/body, and section header contexts.

---

## Design judgment — these affect appearance, need James's eye

### 5. Pulse page column layout
The current Pulse layout uses a `62fr / 38fr` CSS grid for the feed and sidebar. The May brief specified a fixed `380px` sidebar with `flex: 1` feed. We left the fr-based grid in place rather than change it without your sign-off.

**Question:** Is the fr-based grid intentional? At 38fr of a 1440px wrapper the sidebar reaches ~547px — is that the right behavior at large viewports? If the fixed-width model is preferred, say the word.

### 6. Project C Newsletter icon
The circular icon next to "Project C Newsletter" on the Research & Writing page uses a newspaper emoji inside a lime green circle. Every other section header icon uses Material Symbols Outlined.

**Question:** Is the emoji intentional as a Project C brand element, or should it be replaced with a Material Symbol for consistency?

### 7. Promo block as reusable component
The black promo card on Research & Writing (currently "The Top 50 Creator-Model Journalists") is hardcoded. As the Atlas publishes more research, this block will need to rotate.

**Question:** Should this be built as a proper component with title, body, CTA label, and URL as variables? If yes, how should content get passed in — static variables in the HTML, a JSON config file, or something else?

---

## Pages coming online — design prep needed

### 8. Beat Clusters pages
Beat Clusters links are in the footer as commented-out placeholders, ready to uncomment. These pages are 1–2 weeks out.

**Question:** Are the Beat Cluster page designs finalized? Is there a Figma or mockup, or will these be built from the existing cluster card pattern on the homepage?

### 9. City Labs — Chicago and DC
Both City Lab pages are now live at root but unlinked. `city-lab-dc.html` and `city-lab-dc2.html` are old fetch-based versions superseded by `city-lab-dc-v3.html`.

**Question:** Are these pages considered finished, or are design updates pending before they get linked? Also: recommend moving the deprecated DC versions to `_deprecated/` — confirm?

---

## Lower priority — worth having on record

### 10. Pulse indicator dot color
The Pulse nav indicator uses a small colored dot. Some pages show it in acid green, some in lime green. No confirmed rule.

**Question:** Is there a rule for the Pulse indicator dot color, or is it context-dependent?

### 11. Focus states for keyboard navigation
The token file lists focus as an interactive state but nothing is defined or implemented. WCAG AA requirement.

**Question:** What should the focus ring look like? Suggested: `2px solid #97d600`, offset `2px`. Confirm or propose an alternative.

### 12. Mobile design pass
The site has responsive breakpoints but no systematic mobile review has been done since the homepage migration. The Pulse two-column layout, Beat Cluster grid, and Research & Writing cards haven't been verified on mobile.

**Question:** Is a mobile design pass on the roadmap? Before or after Beat Clusters and City Labs go live?

---

*As James answers these, update DESIGN-TOKENS.md and log the decision with a date.*
