# V15 Session 3: handoff

*Written Oct 23, 2026 at the end of Session 2. Read `V15-SESSION-2-REPORT.md`, then `JAMES-OPEN-ITEMS.md`. This replaces `HANDOFF.md` (the mid-session checkpoint).*

## State

Branch `main`, 13 local commits ahead of `origin/main` (`b8fc045` was the last pushed state), nothing pushed. Working tree clean at the end of the session.

## What Session 3 should pick up

1. **Bluesky page mobile layout** (705px at phone width: hero `1fr 440px`, header row, section meta, CTA). Also 320px-only: `for-brands` gallery column (367px) and `partners/njlab` CTA (368px). C10 is done (`C10-REPORT.md`); C10b (hamburger at 1214px, 24px gap from 1215–1279px) needs a decision before push.
2. **Eyebrows.** Non-clickable caps labels without arrows (v15: Source Code Pro 500, 13px, 0.12em, step 5 on light; step 3 or Acid on dark). Many are still DM Mono / JetBrains Mono at 8–11px (`index`, `for-brands`, `pulse`, `research`). The `link-instruction` work did not touch them.
3. **Tags** (12px Source Code Pro caps, 6px radius, no pills, no hover): not started.
4. **nj-lab / njlab** (F2): no `components.css`, broken `variables.css` link, `.cta-ghost`, `.cta-primary` with Lime hover. Needs James's answer on item 3 in open items first.
5. **Open items marked "unsure"** (tab strips, `hcn-pill`, carousel dots, `lede-creator`, Chicago "245" link): wait for James.
6. **Dead CSS** (`DEAD-CSS.txt`): ~60 selectors in 15 files; safe to delete after a quick visual check.
7. **Internal pages** that still use Lime in UI: `atlas-signal-brief`, `beat-*`, `chicago-*`, `njlab`. Not public; low priority.
8. **`↗`/`↓` arrows** (open item 9) after James decides.
9. **Copy sweep** (`COPY-SWEEP-NOTES.md`), if Justin wants it.

## Gotchas (carry over, plus new)

- **Justin edits the same working tree** (Nodes and Networks edition: `assets/nn5/*`, `preview/nodes-and-networks-edition-*`, `_headers`, `CURRENT_STATE.md`) and GitHub Desktop commits whatever is there. Stage by explicit path only (`tools/stage_mine.sh` allow-lists). Never `git add -A`.
- **`_headers`:** the `/partners/_shell` noindex rule is present now, but the NN5 build rewrites `_headers`. Re-check before pushing: `grep _shell _headers`.
- **Don't edit site files while a screenshot run is in progress** (runs read the working tree).
- **Page CSS beats `components.css`** at equal specificity (it loads first), and descendant selectors (`.footer a`, `.x-footer a`) beat single classes. When a converted link doesn't look right, search the page for a rule on its container. The audit scripts in `tools/` find these: check `font-family`, `color`, `text-decoration` against spec.
- **Hover underline thickness:** use `text-decoration-line: underline` in hover rules; the `text-decoration` shorthand resets thickness to `auto`.
- **Transitions:** read computed styles ≥300ms after forcing a state (`CSS.forcePseudoState`), or you read the rest colour.
- **JS-built markup** needs hand edits: `class="x${...}"` strings and `className =` assignments. `migrate.py` handles `class="..."` in templates but not dynamic class names.
- **Typed arrows:** the arrow is part of the words (`&rarr;` or `→`); `.link-instruction` never adds one.
- **Components:** `.btn .btn--primary` / `.btn--secondary`, `.btn-icon`, `.link-instruction`, `.link-body`; `.on-dark` on dark containers; `components.js` syncs selected ARIA. A `<button>` that should read as a link: `class="link-instruction"` (reset in `components.css`).
- `tools/` scripts expect old scratchpad paths in places (`atlasscan.py`, `pages40.py`); `cmp2.py`, `s1shot.py`, `migrate.py` work as-is (`cmp2.py` needs numpy, so don't run it with `python3 -I`). `search.html` full-page screenshots are unreliable (300,000px tall).
- A server already listens on port 8765 on Justin's machine and serves a different folder; use another port.
- Local servers need `_redirects` rewrites for clean URLs; `s1shot.serve` handles them.
