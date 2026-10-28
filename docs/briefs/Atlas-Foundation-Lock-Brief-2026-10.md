# Atlas Foundation Lock Brief — Installing v16

*Developer brief for Claude Code · Owner: James Bareham, Creative Director · For: Justin Bank · October 27, 2026*
*Implements DESIGN-TOKENS-v16.md and ATLAS-BRAND-GUIDE-v5.md. Introduces no new design values.*

**Do this brief first.** The Type Consolidation brief and the Pulse and For Brands brief both depend on it.

---

## 1. What This Brief Does

It installs v16 and v5 as the only design documents in the repo, updates the files Claude Code reads at the start of every session so they agree with v16, archives outdated files, and adds the checks that make the rules hold: a brand check in every build, required review from James for the files that hold the rules, and branch protection.

**Nothing on the live site changes visually.** Every step is documents, configuration or checks. The only code change (fallback fonts and token names in `variables.css`) adds variables without changing what any page renders.

### Why
For Brands and Pulse shipped with Merriweather headlines. Claude Code was given a brief built on a display serif, chose v15, and then swapped the brief's serif for v15's only serif. Nothing stopped it:
- v15 never said which typeface headings use.
- `CLAUDE.md` said nothing about Merriweather.
- `WORKFLOW.md` told Claude Code to route every design question to Justin as the decision-maker, so the font call never reached the token owner.
- `README.md`, a root copy of brand guide v3, `START-HERE.md` and `pulse_tokens.md` still carry retired fonts, colors and rules that a session can pick up.
- No build check looks at type, size or color.

v16 closes the gaps in the rules. This brief closes the gaps in the repo.

---

## 2. Before You Start

- **Work on a `dev` branch.** From this brief on, changes reach `main` by pull request (step 8).
- **Stage by explicit path.** Justin edits the Nodes and Networks edition in the same working tree (`assets/nn5/*`, `preview/nodes-and-networks-edition-*`, `_headers`, `CURRENT_STATE.md`), and GitHub Desktop commits whatever is there. Don't stage those files with this work.
- **Don't touch Nodes and Networks.** Its paths are excluded from every rule and check in v16 (DESIGN-TOKENS-v16.md § Exceptions).
- **Check the `_headers` file after any Nodes and Networks build;** the NN5 tooling rewrites it.

---

## 3. Step 1: Install the Documents

```bash
mkdir -p docs/design/archive docs/briefs
git mv docs/design/DESIGN-TOKENS-v15.md      docs/design/archive/DESIGN-TOKENS-v15.md
git mv docs/design/ATLAS-BRAND-GUIDE-v4.md   docs/design/archive/ATLAS-BRAND-GUIDE-v4.md
git mv ATLAS-BRAND-GUIDE-v3.md               docs/design/archive/ATLAS-BRAND-GUIDE-v3.md
git mv pulse_tokens.md                       docs/design/archive/pulse_tokens-2026-10-26.md
# then add the new files from this handoff:
#   docs/design/DESIGN-TOKENS-v16.md
#   docs/design/ATLAS-BRAND-GUIDE-v5.md
#   docs/briefs/Atlas-Foundation-Lock-Brief-2026-10.md      (this file)
#   docs/briefs/Atlas-Type-Consolidation-Brief-2026-10.md
#   docs/briefs/Atlas-Pulse-For-Brands-Brief-2026-10.md
```

Add a one-line header to each archived file: `> Superseded by docs/design/DESIGN-TOKENS-v16.md and ATLAS-BRAND-GUIDE-v5.md (October 27, 2026). Do not implement from this file.`

---

## 4. Step 2: Update `CLAUDE.md`

### 2a. References
Replace every `docs/design/DESIGN-TOKENS-v15.md` with `docs/design/DESIGN-TOKENS-v16.md`, and every `docs/design/ATLAS-BRAND-GUIDE-v4.md` with `docs/design/ATLAS-BRAND-GUIDE-v5.md`. Only in `CLAUDE.md` and `WORKFLOW.md`; leave dated reports, ledgers and briefs as they are (they're records).

### 2b. Header (lines 4–5)
```markdown
*Owner: Justin (product, structure, copy, build) | Design rules: locked in docs/design/DESIGN-TOKENS-v16.md, owned by James (james@journalismatlas.com)*
*Last updated: October 27, 2026 (design tokens v16, brand guide v5)*
```

### 2c. Required reading table (line 25–26)
Replace the two design rows with:
```markdown
| `docs/design/DESIGN-TOKENS-v16.md` | Before any CSS, styling, markup with inline styles, chart or canvas work. Read **Governance, Locks and Exceptions** first |
| `docs/design/ATLAS-BRAND-GUIDE-v5.md` | Before writing any user-facing copy (voice, self-description, em dash style, database-size wording) |
```

### 2d. Insert at the top of `## Design System` (before the first paragraph)
```markdown
### Locked rules (read first; DESIGN-TOKENS-v16.md § Governance, Locks and Exceptions)

- **Design values are locked to v16.** Every color, typeface, size, weight, spacing value, radius and component state comes from a role in v16. Never pick one. If something seems to need a value v16 doesn't have, don't build it: list it for James's next token version.
- **Apply briefs by role, not by resemblance.** If a brief, mockup or request names a font, color or rule not in v16 (for example Playfair Display, DM Sans, Space Mono, an orange "live" accent), don't map it to the nearest token. Apply the token for each element's role (a headline is Inter at its Type Scale size), build that, and list what the brief wanted that v16 can't give.
- **This holds whoever asks,** Justin and James included. Rules change only through a new token version.
- **Never edit to make a request fit:** `docs/design/*`, `assets/css/variables.css`, `scripts/check_brand.py`, `scripts/brand-baseline.json`, `build-dist.sh` or `.github/`. These need James's review (CODEOWNERS).
- **Undefined means unbuilt:** no dark mode, "live" color, warning color or page-local token sets until v16 (or a later version) defines them.
- **Run `python3 scripts/check_brand.py`** before asking for review. The build runs it too and fails on any new violation.
- **Exceptions are by path only** (v16 § Exceptions): Nodes and Networks, and `atlas-portal/google-form-template.html`.
```

### 2e. Typography rules (replace the "Body copy minimum" bullet at line 84 and the "Font weights" bullet at line 87)
```markdown
- **Three typefaces only (v16 § Font Allowlist):** Inter 400/600/700, Source Code Pro 500, Merriweather 400 (editorial article body only), plus Material Symbols Outlined for icons. No other family anywhere, including system stacks typed on a page.
- **Typeface by role (v16):** every heading at every level is Inter (`--font-heading`), on every page. Merriweather (`--font-prose`) is running body prose inside editorial articles only (`watershed/`, long-form report pages). Never on landing, product, Pulse, For Brands, partner or City Lab pages, and never on a heading, claim, lede, numeral or pull quote.
- **Mono by role (v16):** Source Code Pro is for all-caps labels (Label 13px, 0.08–0.12em) and tags (Tag 12px, 0.08em) only. Sentence-case text is Inter Small 13px; bold numerals are Inter 700 at a type-scale size.
- **Type floor (v16):** no text below 12px anywhere, including charts, legends, tooltips, inline styles and canvas. 12px is Source Code Pro Tag only; all other text is 13px or larger. If text doesn't fit, change the layout, not the size.
- **Fonts are set only through `var(--font-primary|heading|mono|prose)`.** Only `variables.css` names a family. Pages don't load fonts; `header.js` does.
- **Text colors are role variables,** never `rgba()` white or black.
- **Font weights:** Inter 400/600/700; Source Code Pro 500. No Inter 500, no 800 or 900.
```

### 2f. Shared header component (line 112)
Replace the font bullet with:
```markdown
- Loads the site fonts for every page: Inter 400/600/700, Source Code Pro 500 and Material Symbols Outlined (DESIGN-TOKENS-v16.md § Font Loading). Pages don't add their own font links; editorial article pages also load Merriweather.
```

### 2g. "What requires James's sign-off before implementing" (lines 127–131)
Replace the section with:
```markdown
### What changes only with a new token version (James)

- Any color, typeface, size, weight, spacing value, radius, icon or component state not in DESIGN-TOKENS-v16.md
- Any new component type not already defined in the tokens doc
- Full card vs. small card definitions in the postcard system
- Any new exception to the font or color rules
- Any edit to the protected files listed under Locked rules

Everything else (product, structure, pages, copy, build, priorities) is Justin's call.
```

### 2h. v15 rollout status (line 60)
Rename it **"v15/v16 rollout status"** and add: `v16 adds no visual values; it locks v15 and adds the type rules above. The type work is in docs/briefs/Atlas-Type-Consolidation-Brief-2026-10.md. Until a stage ships, live pages can still show the old look; the brand check's baseline records what's left, and new work may not add to it.`

---

## 5. Step 3: Update `WORKFLOW.md`

### 3a. Replace `## Decision Authority`
```markdown
## Decision Authority

**Justin makes product, structure, page, copy, build and release decisions.**

**Design values are not decisions to make in a session.** Colors, typefaces, sizes, weights, spacing, radius, icons and component states are locked in `docs/design/DESIGN-TOKENS-v16.md`. They change only through a new token version written or approved by **James Bareham** (Creative Director, james@journalismatlas.com). If a task seems to need one, stop and list it for James; don't build it, and don't map it to the nearest token.

- **James Bareham**: owns the design tokens and brand guide. His principles live at `_reference/james-design-principles.md`; where a value there conflicts with v16, v16 wins.
- **Ryan**: data advisor. Consult before modifying `creators-data.json`, `creators-master.csv`, or the data pipeline (`convert.js`, `DATA-OPS-PROTOCOL.md`).

When in doubt about anything other than design values: stop, surface the question, wait for Justin's call.
```

### 3b. "What Done Means," item 2
```markdown
2. **It fits design standards**: `python3 scripts/check_brand.py` passes (no new violations); tokens from `variables.css` only; fonts only through `var(--font-*)`; no hardcoded colors, unapproved fonts, sizes below the floor, or unapproved weights
```

### 3c. Session Start Checklist
Change the tokens line to: `Read docs/design/DESIGN-TOKENS-v16.md (Governance, Locks and Exceptions first) if the session touches any styling, inline styles, charts or canvas text`.

### 3d. Deploy Process
```markdown
1. Work on the `dev` branch; Cloudflare builds a preview for it
2. Verify in the browser (load the page, check console, check design) and run `python3 scripts/check_brand.py`
3. Push `dev` via GitHub Desktop and open a pull request to `main`
4. James reviews design changes on the preview; files under CODEOWNERS need his approval. The `brand-check` status must pass
5. Merge; Cloudflare deploys `main` within about a minute
6. Test on the live URL in a fresh incognito window (cached redirects can mask issues)
```

### 3e. "When to Stop and Ask," add
```markdown
- A brief, mockup or request names a font, color, size or rule that isn't in DESIGN-TOKENS-v16.md (apply by role; list the gap for James)
- `check_brand.py` fails and the fix would mean editing the baseline, the check, `variables.css` or the tokens
```

---

## 6. Step 4: Clean Up Outdated Files

| File | Action |
|---|---|
| `README.md` § "🎨 Design System" (Colors, Typography) and the "Google Fonts" and "Material Icons" lines under Libraries | Replace with: `Design system: see docs/design/DESIGN-TOKENS-v16.md (canonical) and docs/design/ATLAS-BRAND-GUIDE-v5.md. Fonts: Inter, Source Code Pro, Merriweather (articles only); icons: Material Symbols Outlined.` |
| `START-HERE.md` § "For James" (eight v14-era items dated Oct 6) | Move to `docs/design/archive/START-HERE-v14-items-2026-10-06.md`. Keep the "For Justin" and SmartNews sections. Add at the top: `Design rules: DESIGN-TOKENS-v16.md. Open design questions for James live in docs/design/v15-session-2/JAMES-OPEN-ITEMS.md.` |
| `james-design-principles.md` / `.pdf` (root, `docs/`, `_reference/`) | Keep one copy at `_reference/` (the path `CLAUDE.md` and `WORKFLOW.md` cite); delete the duplicates. Add a header line: `Where a value here conflicts with DESIGN-TOKENS-v16.md, v16 wins.` |
| `docs/design/v15-session-2/SESSION-3-HANDOFF.md` | Under "What Session 3 should pick up," mark items 2 (eyebrows) and 3 (tags) as replaced by `docs/briefs/Atlas-Type-Consolidation-Brief-2026-10.md` |
| `pulse_redesign_ledger.md`, `for_brands_redesign_ledger.md` | Add a header line: `Font, color and "live" choices below are superseded by DESIGN-TOKENS-v16 and docs/briefs/Atlas-Pulse-For-Brands-Brief-2026-10.md.` |

---

## 7. Step 5: Font Tokens in `variables.css`

Replace the font family block (lines 169–176) with the v16 block. This adds tokens and fallbacks without changing what any page renders.

```css
  /* Font families. DESIGN-TOKENS-v16.md § Font Tokens.
     The ONLY place in the codebase that names a font family. Pages use these variables. */
  --font-primary: 'Inter', 'Inter Fallback', sans-serif;                    /* UI and body */
  --font-heading: var(--font-primary);                                      /* every heading, every page */
  --font-mono:    'Source Code Pro', 'Source Code Pro Fallback', monospace; /* all-caps labels and tags only */
  --font-prose:   'Merriweather', 'Merriweather Fallback', serif;           /* editorial article body prose only */

  /* Retired in v16. Kept only until the Pulse and For Brands brief removes the last use; then delete. */
  --font-editorial: var(--font-prose);
```

`--font-ui` is unused outside Watershed (which defines its own); delete it from `variables.css`.

**Size variables.** The current size block (lines 178–192) doesn't match v15: it defines `--text-label` as 14px (v15 Label is 13px), keeps the retired 11px `--text-micro`, and has 14px variables that aren't scale sizes. None of the off-scale variables is used on a live page (checked October 27), so replacing the block is invisible. Replace it with the block in DESIGN-TOKENS-v16.md § Type Scale ("Size variables"), and keep the line-height variables that follow it.

Add the fallback faces at the top of `variables.css`, outside `:root`:

```css
/* Metric-matched local fallbacks (DESIGN-TOKENS-v16.md § Font Tokens). Implementation values for layout stability. */
@font-face { font-family: "Inter Fallback"; src: local("Arial"), local("Arimo"), local("Liberation Sans"); size-adjust: 107.5%; ascent-override: 90.1%; descent-override: 22.4%; line-gap-override: 0%; }
@font-face { font-family: "Source Code Pro Fallback"; src: local("Courier New"), local("CourierNewPSMT"), local("Liberation Mono"); size-adjust: 100%; ascent-override: 98.4%; descent-override: 27.3%; line-gap-override: 0%; }
@font-face { font-family: "Merriweather Fallback"; src: local("Georgia"); }
```

---

## 8. Step 6: Add the Brand Check to the Build

1. Add `scripts/check_brand.py` from this handoff.
2. In the repo root, on the current `dev` state, generate the baseline: `python3 scripts/check_brand.py --write-baseline`. Commit `scripts/brand-baseline.json`. (On the public repo on October 27 it recorded 2,308 violations in 59 files; your working tree will differ.)
3. Add to `build-dist.sh`, right after `set -eu`:
   ```sh
   # Brand check (DESIGN-TOKENS-v16.md § Enforcement): fail the deploy on any new font, size, weight or color violation
   python3 scripts/check_brand.py || { echo "build-dist: brand check failed; see the list above and docs/design/DESIGN-TOKENS-v16.md" >&2; exit 1; }
   ```
4. Confirm the first Cloudflare build log shows the check running and passing. (If the build image lacks `python3`, stop and tell James and Justin; don't remove the line.)
5. Test it: on a scratch branch, add `.x{font-family:"Playfair Display";font-size:10px;color:#ff9600}` to any page. The check must fail with `font-family`, `font-size` and `color`. Delete the branch.

**How the baseline works.** It records how many violations of each rule each file has today. A build fails if any file gains one. When a brief fixes violations, regenerate the baseline in the same pull request so the counts go down and stay down. Because the baseline is under CODEOWNERS, James sees every change to it; a baseline that goes **up** is a red flag.

**Modes:** `--report` lists everything (never fails); `--strict` fails on any violation; naming files (`python3 scripts/check_brand.py pulse.html`) checks those files strictly.

---

## 9. Step 7: Protect the Rules on GitHub

1. Add `.github/CODEOWNERS` and `.github/workflows/brand-check.yml` from this handoff. Replace `@james-github-username` with James's GitHub username.
2. Add James as a collaborator with write access.
3. Settings → Branches (or Rules → Rulesets) for `main`:
   - Require a pull request before merging
   - Require review from Code Owners
   - Require status checks to pass: `brand-check`
   - Do not allow bypassing the above settings (include administrators)
4. **Plan note.** Branch protection is free for public repositories. The repo is public today and contains internal material (held-back creator lists, rejected-creator notes, private pipeline paths). If it's made private, protection needs a paid GitHub plan; the cleanest route is a TIJA LLC organization account on a Team plan, with Justin and James as owners. ⚑ Justin and James to decide.

The owner of a repository can always change its settings. These steps don't make the rules impossible to change; they make every change visible and reviewed.

---

## 10. Step 8: Staging

Confirm Cloudflare Pages builds a preview deployment for `dev` (Settings → Builds & deployments → Preview branches). This is the staging URL James reviews. It's also prerequisite P4 in `docs/design/v15-discovery/V15-SCOPE-BUCKETS.md`.

---

## 11. What Comes Next

1. **This brief** (no visible change).
2. **`Atlas-Type-Consolidation-Brief-2026-10.md`:** one set of fonts and sizes across the shared header, the shared footer and every public page. This is where the 8–11px text is fixed.
3. **`Atlas-Pulse-For-Brands-Brief-2026-10.md`:** the two new pages.
4. **Final lock:** when `python3 scripts/check_brand.py --strict` reports zero `font-family`, `font-literal`, `serif-*` and `font-size` violations, self-host the fonts and add the font content-security policy (DESIGN-TOKENS-v16.md § Enforcement, item 4). Off-system colors are handled in the next update.

---

## 12. Acceptance

- `docs/design/` holds only DESIGN-TOKENS-v16.md, ATLAS-BRAND-GUIDE-v5.md, `archive/` and the v15 working folders. No brand guide or token file in the repo root.
- `grep -rn "DESIGN-TOKENS-v15\|BRAND-GUIDE-v4" CLAUDE.md WORKFLOW.md README.md START-HERE.md` returns nothing.
- `grep -n "Hanken\|CCFF00" README.md` returns nothing.
- `python3 scripts/check_brand.py` passes on `dev`; the Playfair test in step 6 fails it.
- The Cloudflare build log shows the check; the GitHub `brand-check` status appears on the pull request.
- A pull request touching `variables.css` asks for James's review.
- No visible change on the staging preview compared with `main`.
