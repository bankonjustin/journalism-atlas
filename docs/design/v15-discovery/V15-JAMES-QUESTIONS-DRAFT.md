# Questions for James: v15 → v15.1

*Draft for Justin to review before sending. Prepared Oct 22, 2026 from a read-only pass over the live code. "Live" below means the site as it stands today. Counts are real; where I describe how something looks, I've checked it in the code or in a rendered screenshot. Line references are to `DESIGN-TOKENS-v15.md`.*

**How to read this:** 16 questions, ordered by how much they hold up. 1–5 block the most work. Each has a recommendation I'd ship if you say nothing, so a short reply ("go with your recommendations except 3 and 8") is enough. Where we can ship something meanwhile, it says so.

---

## 1. Main nav: Inter or Source Code Pro caps?

**Context.** The font stack says nav labels are Source Code Pro; the Nav section only specifies color and underline.

**Evidence.**
- L359: "All-caps UI labels: eyebrows, tags, instruction links, **footer and nav labels**, card meta lines." The Nav section (L535–543) says nothing about typeface.
- Live: nav is Inter 15px regular, sentence case ("Research & Writing"), 40px between links.
- I measured the real header at 1440px. The five links take **581px** today; in Source Code Pro 13px caps with the same gaps they take **630px** (+49px). "Research & Writing" goes from 137px to 159px (+22px).
- At 1280px wide, caps with today's 40px gaps **overflow** the header. With your 32px gaps (L417) they fit (598px).
- Separately: today's desktop nav already overflows below about 1100px and doesn't switch to the menu until 768px. That's an existing bug.

**Options.**
- **A.** Keep Inter 15px sentence case. No spacing change.
- **B.** Source Code Pro caps 13px, gaps 32px (your table), and switch to the menu below about 1100px.
- **C.** Source Code Pro caps with the menu switch at 1280px.

**Recommendation: B.** It follows both of your own tables, and fixes the existing overflow. Say A if the nav should stay quiet. *We can ship the color and underline states now regardless (nav is olive on hover and for the current page).*

## 2. Beat dot colors: the site's beat names don't match the palette

**Context.** Beat tags get an 8px dot from the 9-color list. The names the site uses don't match the list.

**Evidence.**
- The nine keys: Politics & Government, Local News, Technology, Business & Finance, Culture & Arts, Sports, Health, Environment, International.
- Creators' topic tags come from data: **79 distinct tags, and only one ("Sports") equals a key** (59 of 2,432 creators by first topic). None of the nine creator groups match.
- Homepage cluster cards (hardcoded): **6 of 9 match exactly**; the other three are close: Climate & Environment, Health & Science, Culture & Media.
- Homepage hero pills: Politics, Tech, Culture, Climate, Health, Food, Local, Media, World (Food and Media have no key).
- Pulse beat pills: 12 main + 26 more topics, of which Media/Power, Government Accountability and Investigative have no key.
- Pulse's heatmap has its own 14-color map (a bright blue, purple, pink, and so on) unrelated to the palette.
- L339: "none of these values are in live code yet"; moving charts is gated on Ryan's mapping.

**Options.**
- **A.** Ship nothing until Ryan maps all 79 topics to the nine keys.
- **B.** Ship dots only on the homepage cluster cards now, after you confirm the three near-names (rename the cards, or accept "Climate & Environment" = Environment, etc.).
- **C.** Ship tags with no dot now (monotone outline), and add dots when the mapping lands.

**Recommendation: C now, B once you answer the near-names, A for everything data-driven.** C costs us nothing to undo.

## 3. Tags are never clickable, but ours are. What should they become?

**Context.** L248: "Tags aren't clickable and have no hover." Today many tag-looking pills filter the page when clicked.

**Evidence.**
- Every creator card on search has clickable tags (`.creator-tag` / `.creator-meta-item` marked clickable): location, platform and topic. Hover turns them lime today.
- Platform pills on all 13 curator partner pages (`.pill.platform`) link out, with a lime hover.
- Homepage beat pills (`.hcn-pill`) and Pulse beat pills (`.beat-pill`) are buttons that filter the page.
- Buttons are 44px tall (L494); a card tag row at 44px would stack the card.

**Options.**
- **A.** Make them Secondary buttons at their current size (an exception to the 44px rule for dense rows).
- **B.** Make them Secondary buttons at 44px and redesign the cards.
- **C.** Make the card tags plain non-clickable tags, and move filtering to a separate control.

**Recommendation: A, with you confirming a smaller height (about 28–32px) for filter chips inside cards.** C loses a real feature (click a topic to see more of it). B is a card redesign.

## 4. How do platform tags (Newsletter, Podcast, …) look?

**Context.** The tag table has content type, status and beat only. Platforms are everywhere.

**Evidence.**
- Live: black fill with white text on the homepage (`.db-pill.platform`); an outline pill on partner pages; and platform-brand colors on city-lab pages (Instagram pink, etc.).
- L244: "Content types… are told apart by their labels, not by color." Platforms are a similar kind of label.

**Options.**
- **A.** Monotone outline tag (like "in progress"), no color.
- **B.** Same as the gray content-type fill.
- **C.** Platform icon plus text, no tag.

**Recommendation: A.** It can't be mistaken for a content type (gray fill) or a beat (dot).

## 5. What happens to Inter weight 500?

**Context.** L384: weight 500 is for Source Code Pro only. Inter 500 is used a lot.

**Evidence.** **93 rules on public pages** use Inter 500: 27 labels and meta lines, 25 tags/chips, 16 buttons and CTAs, 9 cards, 7 nav items (the mobile menu links, for example).

**Options.**
- **A.** 500 → 600 for buttons, nav, links, titles; 500 → 400 for meta and captions; labels and tags move to Source Code Pro anyway.
- **B.** Everything 500 → 600.
- **C.** Everything 500 → 400.

**Recommendation: A.** Heavier where it carries action, lighter where it's meta.

## 6. Table column headers

**Context.** v15 has no table style.

**Evidence.** The creator table on search has a dark header row (dark gray fill, white bold sentence-case text) with Acid sort arrows. L372 says Label style is "eyebrows and instruction links".

**Options.** **A.** Label style (Source Code Pro caps 13px) on the existing dark header row. **B.** Light header row, Label style in step 5. **C.** Leave as is.

**Recommendation: A**, so tables read as the same family as eyebrows without changing their weight on the page.

## 7. Hover and press for icon-only and toggle buttons on light surfaces

**Context.** v15 covers the glyph (filled when active) but not what the button itself does.

**Evidence.** Live icon-only controls: the menu and close buttons, a few drawer and card actions. Save, follow and bookmark **don't exist yet**. An "add to pack" lives on search. L461: "selection carried by color only (acid green on dark surfaces, Dark Olive on light)."

**Options.**
- **A.** 44×44, transparent at rest; hover/press = Acid fill with a black icon; selected = Dark Olive filled glyph.
- **B.** Hover only changes the icon color to Dark Olive (no fill).
- **C.** Treat them as Secondary buttons.

**Recommendation: A**, consistent with "Acid is the hover" for everything else.

## 8. Does "green means interaction" apply inside charts?

**Context.** The viz palette excludes Acid, but the live charts use it.

**Evidence.**
- L342: "Acid green `#ceff00` is excluded — reserved for interaction states."
- Live canvases use Acid and Lime as *category* colors: homepage clusters (Climate & Science = Acid, Local News = Lime), search "field" view (Power & Politics = Acid, Civic Life = Lime; Substack = Acid).
- Pulse and several city-lab pages draw bars and dots in Acid on light backgrounds.

**Options.**
- **A.** Charts never use Acid or Lime; they move to the palette when Ryan's mapping lands (until then we leave them).
- **B.** Charts may use Acid only for the selected or hovered item.
- **C.** Allow Acid for one highlighted series.

**Recommendation: B**, which is what "Acid means interaction" implies and is easy to explain.

## 9. Footer link style

**Context.** L359 says footer *labels* are Source Code Pro; nothing says what footer *links* look like.

**Evidence.** Live footer: column titles, copyright and legal links are 9–10px mono caps (below the 13px floor); links are Inter 13px at 55% white with a white hover.

**Options.**
- **A.** Titles = Label (13px, step 3); links = Inter 13px step 3, white underlined on hover; legal = Tag (12px).
- **B.** Same, but hover = Acid underlined (consistent with dark-surface links).
- **C.** Leave the links, only fix titles.

**Recommendation: B.**

## 10. Dark-surface eyebrows: step 3 or Acid?

**Context.** L262: "`--color-text-on-dark-2` (step 3) or `#ceff00` on dark surfaces."

**Evidence.** The homepage and city-lab eyebrows (`.hero-eyebrow`, on 22 pages) are gray today. A few are Acid (`.lab-eyebrow`, `.spotlight-eyebrow`); some are white at 30–40% opacity.

**Options.** **A.** Step 3 by default; Acid only for the first eyebrow on a page. **B.** Acid for all dark eyebrows. **C.** Step 3 everywhere.

**Recommendation: A.**

## 11. One letter-spacing for instruction links

**Context.** L372 gives a range, 0.08–0.12em.

**Evidence.** The homepage's one existing mono link (`.hero-tertiary-link`) uses 0.08em; eyebrows in the CSS use 0.12em; the 124 arrow links today use no spacing.

**Options.** **A.** 0.1em. **B.** 0.08em (same as tags). **C.** 0.12em (same as eyebrows).

**Recommendation: A**, in the middle, so a link beside an eyebrow and a tag looks related to both.

## 12. When is a primary button "selected"?

**Context.** L502 gives a selected state for primary buttons (white fill).

**Evidence.** I couldn't find a primary button on the live site that stays selected (toggle-style). Selected states today are on filter chips and tabs, which are Secondary.

**Options.** **A.** A primary is never selected; only Secondary buttons are. **B.** A primary can be selected when it toggles a mode (list the cases).

**Recommendation: A.** Keeps the two styles' jobs separate.

## 13. Card hover and form inputs (you know these are open)

**Context.** v15 lists card states but doesn't style them, and doesn't style inputs.

**Evidence, so you can design against the real site.**
- Cards: hover is a background shift to the page gray plus a darker border on creator cards; border-only on the homepage cluster cards; a faint Acid-tinted border on dark gallery cards. Not green.
- Whole cards are links on the homepage clusters.
- Inputs: header search (Inter 15px, 8px radius, olive outline plus a lime border and glow on focus); form fields (16px, 6px radius, olive border on focus); homepage filter selects (13px, 4px radius, native).
- Checkboxes and radios are the browser defaults.

**Options.** **A.** Keep the card hover as is; inputs at 6px with an olive focus border and no Lime. **B.** Cards hover to Acid-tint. **C.** Wait for your spec.

**Recommendation: A**, until you've designed it.

---

## New questions I found

## 14. Header Search button, and the primary button on dark pages

**Context.** The "Search" button is v15's own example of a primary button (L494). It's in the header on every page. And primary buttons on dark surfaces rest in gray.

**Evidence.**
- Live header Search button: Acid fill, 12px bold text, **27px tall**, next to a 41px search field in a 74px header. A 44px button would be 3px taller than the field and grow the header by about 3px.
- The homepage hero CTA ("Explore the Atlas →") is an Acid button on black today. Under v15 it rests as `#303030` on black with a `#909090` outline: the main call to action on the page would be the quietest thing on it. L524 states the change in general terms but doesn't mention hero sections.

**Options.**
- **A.** Follow the spec exactly: 44px Search button; hero CTA = dark-surface primary (gray on black).
- **B.** Search button as spec'd, but the hero CTA on black pages gets a white-fill primary (the "selected" look, L502) so it stays the loudest thing on the page.
- **C.** Keep a hero exception: Acid at rest on dark.

**Recommendation: A for the header** (the 3px is not a problem). **For the hero, your call**: I'd rather not pick, but B keeps the main action visible without breaking your "green means interaction" rule.

## 15. Partner card links ("View on Substack →" and similar)

**Context.** These are neither body links nor buttons.

**Evidence.** `.card-link` appears on 13 curator pages and `co-ops` (253 on the pages I scanned): olive 14px text, a 44px-tall hit area, a lime fill on hover.

**Options.** **A.** Instruction link (Source Code Pro caps, step 6, olive underlined on hover). **B.** Secondary button.

**Recommendation: A.** They end in an arrow and point off-site, which is what the instruction link is for.

## 16. The long-form report page doesn't use the system

**Context.** The "Jump to" sub-nav moves to white with olive states (L270), but the report page doesn't use the shared header at all.

**Evidence.**
- The only report page (`/preview/nodes-and-networks…`, an unlisted preview, generated from a template) has its own chrome: DM Sans and Libre Baskerville (not Inter and Merriweather), a warm off-white `#faf9f5` background, blue body links, and its own sticky section nav and "Jump to cohort" strip.
- The template document the sub-nav spec lives in (`Atlas-Long-Form-Report-Template-2026-09.md`) isn't in the repo.
- The brand guide (v4, Section 7) calls this paper "the first long-form report" that "sets the template for those that follow", so this is the page people will compare to the guide.

**Options.** **A.** Rebuild the template on the shared header, Inter/Merriweather and neutral tokens, with the white "Jump to" sub-nav. **B.** Keep the report's own look; document it as a deliberate exception. **C.** Bring over only the sub-nav and links.

**Recommendation: A for the next report**; leave the current preview alone.

---

*Two smaller things I'm not asking about, with the default I'd use: the "Soon" badge on the Partners nav item becomes a Tag (Source Code Pro 12px caps, outline); and the pulsing Lime dot in the header becomes a dark-gray dot (Lime is the dark-surface focus ring only).*
