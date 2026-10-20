# Review notes for James: SmartNews × Atlas page

Page: `preview/smartnews-d029dc36/index.html` (unlisted preview, `noindex`). Screenshots are in `screenshots/` next to this file. Everything below was built, not held back; each item is a question for you.

v1.1 changes: the routing row, the What/When/Who strip and the tracks section were cut. **The Mirror Principle is now served by the form's toggle** ("Applying for myself" / "Recommending someone") and the form's "Interested in" options, not a routing row. Rows 3 and 4 below are superseded: the track descriptions now live inside the form as option cards with a status pill.

Screenshot names in the table below refer to `screenshots-v1.0-superseded/`; current ones are in `screenshots/`.

Principles used: Tool, Mirror, Explanation, Surface Hierarchy, Brevity, Scale, Template. Tokens: `variables.css` (v14). No token value is inlined; nothing was approximated.

## Needs your sign-off

| # | Item | What I did | Question | Screenshot |
|---|---|---|---|---|
| 1 | **Co-brand band** | White band under the site header holding the Atlas lockup and the SmartNews logo, separated by ×. Marks unrecolored. Atlas 30 px tall, SmartNews 44 px tall (desktop); 19 / 28 px on mobile. | Is the optical weight equal, and is a white band with a partner logo OK on a non-partner page? "Partner assets appear in page headers only" is the guide's rule, and this is a header band. | `1440-01-hero`, `390-01-hero` |
| 2 | **Hero headline size** | Uses v14 Display (48 px / 800 / 1.1; 40 px under 768 px). The headline is 17 words, so it wraps to 3 lines at 30ch. | Fine at Display, or should a release headline be allowed larger? I did not go above the token. | `1440-01-hero` |
| 3 | **Routing row** | Four equal cards ("Why are you here?"), each a title plus one line of context, Material Symbols `arrow_forward` in olive. New component. | Does it match what you meant by Mirror? Should it sit directly under the hero (as built) or inside it? | `1440-02-routing-release` |
| 4 | **Track cards** (three ways in) | Card with an outline status pill, title, one paragraph, text link. Open-now pill uses olive text and border; the others use secondary text. New component, renders from data. | Pill treatment OK? One acid moment per composition: I used acid only for the primary buttons. | `1440-06-tracks-terms` |
| 5 | **Cohort grid** | Black cards with step-5 borders on the black stage, auto-fill columns (minmax 260 px), one card per creator, last card is the open seat with an acid border. Tested at 10 entries (4 columns). | Is an acid border on the open-seat card a second acid moment? Is an "open seat" card compatible with the Placeholder Principle? It is a CTA, not an empty slot, but it is close. | `1440-05-cohort` |
| 6 | **Merriweather in the release** | Release body and pull quotes in Merriweather 16 px / 1.8 in the 680 px column; all UI stays Inter. Quotes are 20 px italic with a 3 px olive left rule. | Italic at 20 px and an olive rule: OK? Neither is spelled out in the tokens. | `1440-03-release-quotes` |
| 7 | **"Why SmartNews" on light** | Light (Surface Hierarchy: dense information). The only dark blocks are hero, cohort, Atlas story. | Agree, or do you want it as a stage with the screenshot? | `1440-04-why-smartnews` |
| 8 | **Error color** | Validation text uses `--color-error` `#f50000` at 13 px. That is about 4.3:1 on white, under 4.5:1 for small text. | Darken the token for text use, or make validation text 14 px bold? | (form, `1440-08-form`) |
| 9 | **Atlas stat** | The live creator count ("about 2,400") uses `--color-display-dark` `#ffbc00` at Display size on black, per the v14 dark display accent. | Is this the intended use of that token? | `1440-07-atlas-story-form` |
| 10 | **Selected state on form choices** | Selected radio/checkbox cards get a black 2 px border (not acid or olive) so the page keeps one acid moment. Input borders are step 4 (3.2:1) for the 3:1 UI minimum. | OK, or should selection be olive? | `390-03-form` |
| 11 | **Preview banner and bracket tags** | Dark banner and a boxed highlight on every placeholder. Preview-only; not part of the final design. | None; for context so you do not review them as design. | `1440-01-hero` |
| 12 | **Reusable template** | Cohort, tracks, routes, terms and form options all render from data. | Should this become the "partner announcement" template? Recommendation is to extract after the second partner. | n/a |

## Observed, not touched

- **Header search field at 390 px:** in the shared header, the search input collapses to an empty rounded box beside the Search button. It is in `header.js` / `header.css`, so it affects every page. Screenshot `390-01-hero`.
- **Site has no OS dark theme.** The brief asked for light and dark screenshots; `prefers-color-scheme: dark` leaves this page unchanged (`1440-09-dark-scheme-footer`).
- **Header is the default white**; I did not request the black variant.
- **Icons:** the only icon is Material Symbols `arrow_forward` (24 px, olive) on the routing cards.
