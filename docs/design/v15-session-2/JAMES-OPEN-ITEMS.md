# Open items for James (v15 Session 2)

*Each item says what was done, what is undecided, and where to look. Justin has already made calls on some; those are marked.*

## Decisions already made (for the record)

- **Nav Pulse dot (Lime, pulsing)** stays as is. Justin: it is a live indicator, not interaction. This is the only Lime at rest on the public pages (plus the homepage hero pill "LOCAL", item 8). Lime's job in the spec is the dark-surface focus ring; the dot is a deliberate exception.
- **Dark surfaces** use a container class `.on-dark` (or `data-surface="dark"`) with `:where()` custom-property variants (no added specificity), not guessed container names.
- **Header Search button** is written out in `header.css` (primary spec with literal fallbacks), not via `.btn` classes, because `header.css` loads on pages without `components.css`.
- **Selected-state ARIA** comes from one shared observer (`assets/js/components.js`) rather than editing ~40 page handlers.
- **Arrow method:** typed in the markup, no `::after`.

## Questions for James

1. **Header Search button is 44px (was 27px).** The header grows 3px on every page. OK, or should the field and button share a height?
2. **Hero buttons on black turned gray.** Primary on dark rests at `#303030` with a `#909090` outline. Does a gray button read as the main action on the black homepage hero, or should dark heroes get an exception?
3. **nj-lab / njlab (F2).** The header with the held-back C4 patch is white like other partner pages (`screenshots/f2/F2-compare.png`). The two pages still don't load `components.css` and carry a broken `variables.css` link. Apply the patch (`docs/design/v15-session-1/C4-held-back.patch`, needs hand-applying) and migrate them? `.cta-ghost` is untouched.
4. **Tab strips.** `.analysis-tab` (pulse), `.tab-btn` (city-lab-chicago, selected underline), `.layer-stat-btn` (city-lab-chicago) are underline/segment strips. The spec lists "tabs shown as buttons" as Secondary. Treat them as Secondary buttons, or give underline tabs their own state spec? (Only the Lime tint on the Chicago selected tab was removed.)
5. **Homepage hero pills `.hcn-pill`** are colour-matched to the canvas clusters (the graphic's legend). They keep their cluster colours at rest, including Lime and Acid for two of them. Legend, or buttons that should be monotone?
6. **Acid-coloured links at rest on dark:** `pulse` masthead creator names (`.lede-creator`) and the Chicago "245" stat link. Editorial highlights, or links that should rest white?
7. **Carousel dots** (`.featured-progress-dot`, 6px, selected = Acid). Below the 44px target; fine as indicators, or enlarge?
8. **Press / cite chips and "pub-arrow"** (`research` cards: a lone green `→` inside a whole-card link). Not restyled.
9. **`↗` and `↓` arrows (question).** About 40 links end in `↗` (external: co-ops evidence links, partner "Read X ↗", city-lab-dc source links) or `↓` ("Read the methodology ↓"). The spec says instruction links end in `→`. Keep `↗`/`↓` as external/jump cues, or make everything `→`? Left unchanged. The partner "about" links (`.about-link`, `↗`) are olive text at rest and aren't instruction links yet; they follow whatever you decide here.
10. **"Explore cluster →" on homepage cluster cards** is hidden (opacity 0) until the card is hovered. Under `(hover: none)` it now shows at rest. Should pointer devices see it at rest too?
11. **Homepage "Pulse" grid is one column at ≤480px.** The 13px caps instruction links ("MORE POLITICS →") didn't fit three narrow columns. Layout change; review before push.
12. **`aria-current` sections.** `aria-current="page"` = the nav item's own page; `="true"` = a page inside that item's section, both styled selected. Sections: Partners (`/partners/*`), Research (`/research/*`; none exist yet), Submit (`/submit-thanks`), About in the mobile menu (`who-we-are`, `how-we-did-this`, `advisory`). Right grouping? Nav has no About item on desktop.
13. **Inline "How we verify →" on partner pages** now sits 12px after the attribution sentence as an inline-block. It could be its own line.
14. **Report "Jump to" (C8):** restyled in the generator for the old preview only (white background, step-3 border, step 6 items, Dark Olive hover and selected). It keeps DM Sans and its own sticky bar, not the shared header. To move it into the shared header: add a `nav` slot to `header.js` that report pages fill (anchors + `aria-current` set by the scroll script), reuse `.nav-link` states, and drop the generator's CSS. Roughly half a day, mostly the sticky stacking with the 64–72px header. Justin's new edition (`preview/nodes-and-networks-edition-*`) was not touched.
15. **Icon-only buttons (`.btn-icon`)** are new: 44px target, no outline at rest, Acid fill and black icon on hover/press. The spec has no icon-button entry; add one or adjust.
16. **Bluesky page "For brands →"** was a link with a bottom rule; it is now a secondary button beside the primary "Get in touch →". The same in `city-lab-chicago` ("Tell us who we missed →" is a primary button in a note box).
17. **Header overflow at 390px (pre-existing, found in verification).** The mobile header (logo + search field + Search button + hamburger) is ~600px wide on a 390px screen, so the hamburger sits off-screen to the right of the viewport. It was ~577px before this session; the 44px Search button added ~24px. This is C10, which was skipped; see SESSION-3-HANDOFF.
18. **Copy:** wording differences for the same destination are logged in `COPY-SWEEP-NOTES.md`, unchanged.
