# V15 Session 2: report

*Oct 23, 2026. Branch `main`, 13 commits ahead of `origin/main`, **nothing pushed**. Components, link and nav states from `docs/design/DESIGN-TOKENS-v15.md` § Component States applied across the 34 public pages that load `components.css`.*

## Commits (oldest first, this run)

| Step | Commit | What |
|---|---|---|
| C5b | `1c74fed` | Ghost buttons become secondary (`index`, `for-brands`, `research` ×4, `latin-america-lab`); `submit-thanks` joins `components.css` |
| C6a | `480991c` | Body links in prose use `.link-body` |
| C6 | `da7adfc` | Instruction links use `.link-instruction` (349 visible links) |
| C6b | `d9963ee` | Footer links white, Acid + underline on hover (216 shared-footer links) |
| fix | `544c43a` | Hover underlines keep 1px thickness (shorthand was resetting it) |
| C7 | `f525740` | Header nav states and `aria-current` |
| fix | `7982377` | `pulse`: "Search the database →" goes to `/search` |
| fix | `572edbe` | `header.js` section matching (`aria-current="true"` for sub-pages) |
| C8 | `c28f255` | Report "Jump to" and cohort strip follow the white-header spec (edited in the generator) |
| C9 | `807b8d0` | No green buttons at rest; cluster link on touch; partner "How we verify →" spacing |
| C9b | `cbe7a3c` | Remaining toggles to secondary; new `.btn-icon`; soft CTA to instruction link |
| tidy | `51245ca` | Last Lime hover and unused Lime variable out of chicago; orphaned `.stat-sub` rule removed |

Earlier in Session 2 (see HANDOFF.md): F1–F4, C1–C5.

## C6a: body-link containers

`link-body` is on each link directly (no global `a` rule). Containers: partner attribution paragraphs (13 pages, `p.atlas-attribution-body`), `contact.html` (`.contact-sub`, `.contribute-intro`), `submit.html` (`.form-intro`, contact paragraph), Bluesky `p.hero-narrative`, city-lab-chicago context card, `who-we-are` team contact lines (Email, LinkedIn, Linktree), `wire.html` footer sentence. Redundant per-page `a` rules were deleted. Verified at rest: Dark Olive and underlined on light, white and underlined on dark; hover black / Acid.

## C6: instruction links

- Source Code Pro 500, 13px, caps, 0.08em, `#303030` → Dark Olive underlined on light; white → Acid underlined on dark.
- Whole-card links: cards untouched; only the "… →" line inside is restyled (`a:hover .link-instruction` rule in `components.css`).
- Page CSS that overrode the links (`.footer-links a`, `.intel-footer a`, `.archive-method a`, id selectors on the homepage drawer, and others) was removed.
- Audit (computed style, 1440): every visible `.link-instruction` matches spec at rest and hover; four apparent hover failures were harness artifacts (covered or closed-drawer elements; confirmed with a real mouse).
- **390px:** wraps and overflows fixed on `index` (Pulse grid, free notice) and `for-brands` (pulse intel header, follower note, footer). Remaining wraps are long phrases wrapping onto two lines ("Read the full living methodology… →", "View creators with audience data →", "Switch to Journalism →" inline in a sentence). Research ticker "Read →" links are one line inside a carousel that extends past the viewport by design.

## C7 / C8

- Nav: rest step 6 (`#303030`), hover/press Dark Olive underlined (Acid on black), current page 2px underline at offset 8px. `aria-current="page"` (exact) or `"true"` (section) set by `header.js`; mobile menu hover/selected bar is Dark Olive instead of Lime. Verified on pulse, for-brands, research, submit, partners, partner sub-pages, about sub-pages, and on the black header theme.
- Jump-to: white, step-3 border, step 6 items, Dark Olive hover and selected, no pills. Rebuilt page differs from before only in CSS and the active-link script (`aria-current` added).

## C9 / C9b

- Migrated by role: Bluesky "Get in touch →" (primary) and "For brands →" (secondary), Chicago "Tell us who we missed →" (primary), city-lab-dc "Show all", co-ops "Reset filters", search "Clear all filters" (both), wire Bluesky follow (secondary), search pack share (primary), pulse "Load 50 more" and "more topics", Chicago disclosure toggles (secondary). All `btn-lime*` uses were already primary from C4 and re-verified (gray at rest, Acid on hover).
- `.btn-icon` for close, pause and menu icons.
- **Green-at-rest scan (all 34 pages, interactive elements):** zero green buttons. What is left is documented: Dark Olive body links and selected nav (allowed); nav Pulse dot (Lime, approved); homepage `hcn-pill` (graphic legend); decorative or data uses (stat numbers, bars, avatars, badges); and the "unsure" items in JAMES-OPEN-ITEMS (#4–#9).
- **Lime only as the dark focus ring:** the only Lime at rest on public pages is the Pulse dot and the `LOCAL` hero pill. No Lime hover states remain (Chicago `beats-toggle` rule was dead and removed). Internal and archived pages (`atlas-signal-brief`, `beat-*`, `njlab`) still use Lime and were out of scope.

## Whole-session verification

| Check | Result |
|---|---|
| Contrast (24 pairs) | all pass; lowest is Dark Olive on `#efefef` at 4.6:1 (needs 4.5). Table in REVIEW-SHEET.html |
| Button spec at rest and hover | primary 67/67, secondary 258+/258+ (C4, C5) and all C5b/C9/C9b buttons match: 44px, 6px radius, Inter 600 15px |
| `:active` at 390 (touch emulation, forced pseudo-state) | primary, secondary, search button, secondary toggle, `.btn-icon`, instruction link, footer link, body link (light and dark): all change to the hover colours; `.nav-link` is hidden at 390 (hamburger) and covered by the mobile-menu rule |
| Body links underlined at rest everywhere | yes (every `.link-body`, all 13 partner pages, contact, submit, who-we-are, bluesky, chicago, wire) |
| Page heights vs Session 2 "before" | 38 of 40 pages changed height at 1440, as expected from the button/link restyle: partner and co-op cards are shorter (card "Visit →" is a text link, not a 44px chip: -100 to -440px), filter chips and toggles are taller (`city-lab-dc-v3` +198, `pulse` +141, `for-brands` +41). Pixel diff is not meaningful across height changes; the `domdiff` computed-style check (earlier) covers the rest. `search` (0.3% changed) and `bluesky`, `wire` carry animation noise |
| Horizontal overflow at 390 | the shared header was wider than the viewport on ~20 pages (577px before this session, 601px after the 44px Search button). Fixed by C10a; three pages still overflow for other reasons (`index` 775px, `bluesky-creator-intelligence` 708px, `about-this-project` 447px) |
| Dead CSS (static, by file) | `docs/design/v15-session-2/DEAD-CSS.txt`: 15 files, ~60 selectors with no markup. Not deleted, to keep this a no-surprise diff. One orphan I created (`.stat-sub` in `index`) was removed |

## Expected visible changes (summary for review)

- Buttons rest gray (primary) or outlined (secondary) and turn Acid on hover/press; no Acid or Lime button fills at rest.
- Links read as one system: caps mono instruction links, Dark Olive body links, white footer links.
- Header: 3px taller (Search button 44px); current page marked in Dark Olive with a 2px underline.
- Partner and co-op cards: shorter (text link replaces chip).
- Homepage: Pulse grid stacks to one column at ≤480px; "Explore cluster →" visible on touch.

## Not done

- C10 (phone header overflow and mid-width nav overflow): done afterwards, see `C10-REPORT.md` (`31f0ff9` phones, `f17b9af` below 1280px, review before push).
- Eyebrows (non-clickable, no arrow), type sizes below 13px and DM/JetBrains Mono leftovers: Session 3.
- nj-lab / njlab, `teamdmv`: untouched (item 3).
