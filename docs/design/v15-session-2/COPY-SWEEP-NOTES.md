# Copy sweep notes (v15 Session 2)

*Logged, not changed. Justin: "log them, don't change them." Words in every link are exactly as they were; the only text edits were adding a typed ` →` where a clear call to action had none (see "Arrows added").*

## Same destination, different wording

| Destination | Wordings in use | Where |
|---|---|---|
| `/about-this-project` | "How we built this" · "Learn how the Atlas works" · "About the Atlas" · "Read more about our governance approach" (advisory section) | `index`, `pulse` (2), `about-this-project` |
| `/for-brands` | "For brands" · "How it works for brands" · "Learn more" · "Track for PR & comms" · "Tell us what you're tracking" (to `#build-brief`) | `bluesky-creator-intelligence`, `pulse` (3), `research`, `for-brands` |
| `/search` (the database) | "Search the full Atlas" · "Search the database" · "Search creators" · "Search all creators in this beat" · "Explore the Atlas" · "Explore all N creators" · "View all" · "View in Atlas" · "Open in Atlas" · "Filter by topic in the full database" · "Explore the full database" | `for-brands`, `pulse`, `research`, `index`, `partners/iij`, `city-lab-dc-v3` |
| `/pulse` | "Explore Atlas Pulse" · "Open full Pulse feed" · "Explore the full digest" · "See it live" · "View Pulse" · "View the live digest" · "View creators with audience data" · "More {beat}" · "Learn more" (pulse brands band) | `for-brands`, `index`, `about-this-project`, `pulse` |
| `/research` | "View all research" · "Explore the Atlas" (research hero, goes to `/`) | `index`, `for-brands`, `about-this-project` |
| Partner "back to Atlas" | "Explore the Atlas" (button) vs "How we verify" (link to `/about-this-project`) | all 13 partner pages (consistent across pages) |

## Vague or inconsistent labels (candidates for a later copy pass)

- **"Visit →"** on 200+ partner and co-op cards is vague and the same on every card; "View →" (latin-america-lab) and "Read →" (research ticker) are the same idea with other verbs. `partners/iij` says "View in Atlas →" for the same card slot.
- **"Explore →"** (latin-america-lab spotlight cards) says nothing about the destination.
- **"Tell us →"** (city-lab-chicago hero) and "Tell us who we missed →" go to different places (mailto vs contact page) with near-identical words.
- **"Learn more →"** (pulse brands band) goes to `/for-brands`; "For brands →" and "How it works for brands →" go there too.
- **"Search the database →"** (pulse): fixed to point at `/search` (it pointed at `/index.html`, the homepage). Wording unchanged.
- "Full intelligence →" (search) and "Full intel brief →" (pulse) are two names for similar things; "Full intel brief" has `href="#"`.
- Several `href="#"` instruction links are wired by JS (`Open in Atlas →`, `See all in full Atlas →`, `Browse {cluster} →`); a no-JS visitor gets nothing.

## Arrows

- **One method sitewide: the arrow is typed text** (` →` or `&rarr;`), as `components.css` specifies (`.link-instruction` "always ends in ` →`; the words are written in the markup"). No `::after` arrows on links. The `::after` arrows left in `advisory.html`, `updates.html` and `about-this-project.html` are list bullets, not link arrows.
- **Arrows added: none.** Every converted link already ended in an arrow, so no text was edited. (Links that are calls to action but have no arrow, such as card titles that are links, were not converted; per the brief, non-arrow text that is not a call to action is an eyebrow.)
- **Mixed glyphs, left alone:** `↗` (external link: 30+ links: co-ops evidence links, partner "about" links, city-lab-dc `hyper-link`) and `↓` ("Read the methodology ↓", co-ops). See JAMES-OPEN-ITEMS #9.
- **Case:** the source text keeps its sentence case ("Explore Atlas Pulse →"); `.link-instruction` uppercases it with CSS. A copy edit would not be needed to change it.

## Eyebrows (not clickable, no arrow): left for Session 3

Source Code Pro caps labels without an arrow (for example "ATLAS PULSE · ALWAYS FREE", "ATLAS VERIFIED") are eyebrows per v15 and were not touched. Several still use DM Mono / JetBrains Mono at 8–11px (index, for-brands, pulse); that is Session 3's typography pass.
