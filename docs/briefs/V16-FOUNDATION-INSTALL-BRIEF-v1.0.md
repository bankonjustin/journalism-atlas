# V16 Foundation Install Brief — v1.0

*Claude Code working brief · Owner: Justin Bank · October 27, 2026*
*Wraps `docs/briefs/Atlas-Foundation-Lock-Brief-2026-10.md` (James Bareham) and applies amendments Justin has decided. Introduces no new design values.*

## Changelog
- **v1.0 (2026-10-27):** First version. Installs James's v16 handoff with five amendments: git mechanics, check coverage, baseline ratchet, serif path, narrowed CODEOWNERS. Justin decided to apply them directly and walk James through them afterward.

---

## 1. What This Brief Does

It installs James's v16 handoff (tokens v16, brand guide v5, three briefs, the brand check, CODEOWNERS, the GitHub workflow). Where this brief and James's Foundation Lock brief differ, **this brief wins**. Everywhere else, follow James's brief exactly.

**Decision record.** Justin reviewed the handoff on October 27 and decided:

1. **Install v16 as James wrote it.** Everything not amended below is unchanged.
2. **Apply five amendments now** (Part B onward). James is walked through them after install. Code records every deviation in a notes file for that conversation (Part F).
3. **Scope the lock to design.** James's review gates the design rules. It does not gate product docs, the build script, `_headers` or Nodes and Networks deploys.

**No visible change on the site.** Same as James's brief. If anything renders differently on the preview compared with `main`, stop.

**Out of scope:**
- `Atlas-Type-Consolidation-Brief-2026-10.md` and `Atlas-Pulse-For-Brands-Brief-2026-10.md` (the next two runs).
- Repo visibility and sensitive files. That work is `REPO-VISIBILITY-AND-DEPLOY-SURFACE-BRIEF-v1.0`. Don't move, delete or edit creator lists, rejection notes or pipeline paths here.
- Team DMV's header and footer. That is an open decision.
- Nodes and Networks. Don't touch any of its files.

---

## 2. House Rules for This Run

- **No git commands that change history or the index.** Use `mv`, not `git mv`. No `git add`, `commit`, `push`, `checkout` or `branch`. Justin stages by explicit path and pushes through GitHub Desktop. Read-only git (`git status`, `git diff`, `git log`, `git show`) is fine.
- **Justin creates the `dev` branch** in GitHub Desktop before Code starts. Confirm you're on it in Step 0.
- **Stage by explicit path.** The working tree has uncommitted Nodes and Networks work: `assets/nn5/*`, `preview/nodes-and-networks-edition-*`, `_headers`, `CURRENT_STATE.md`. List every file this brief touched at the end so Justin can stage exactly those.
- **Stop points:** after Step 0, and after Part C (before the baseline is written). Report, then wait for Justin.
- **Flag, don't reconcile.** If James's brief and the repo disagree (a line number, a file that isn't where he says), report it. Don't guess.

---

## 3. Established Facts vs. Assumptions to Verify

**Established (from reading the handoff zip on October 27):**
- The zip contains these files:
  - `Atlas-Project-Instructions-v4.md`
  - `.github/CODEOWNERS`
  - `.github/workflows/brand-check.yml`
  - `scripts/check_brand.py`
  - `docs/design/DESIGN-TOKENS-v16.md`
  - `docs/design/ATLAS-BRAND-GUIDE-v5.md`
  - the three briefs in `docs/briefs/`
- `check_brand.py` detects colors only as 3- or 6-digit hex. It doesn't catch `rgb()`, `hsl()`, 4- or 8-digit hex, or named colors.
- The check's ratchet is per file and per rule. Counts only fall when someone regenerates the baseline.
- `SERIF_ARTICLE_PATHS` is `("watershed/",)` only. v16 § Exceptions says long-form report template pages are also editorial articles.
- James's CODEOWNERS covers `CLAUDE.md`, `WORKFLOW.md`, `build-dist.sh`, `_headers` and all of `.github/`.
- James's brief says the NN5 tooling rewrites `_headers`.

**Assumptions to verify in Step 0.** James wrote against the public repo, and Justin's working tree differs. These are memory- or brief-derived:
- The line numbers James cites in `CLAUDE.md` (4–5, 25–26, 60, 84, 87, 112, 127–131) and `variables.css` (169–176, 178–192).
- That `ATLAS-BRAND-GUIDE-v3.md` is in the repo root. As of early October it existed only in `~/Downloads`.
- That `pulse_tokens.md`, `docs/design/DESIGN-TOKENS-v15.md` and `docs/design/ATLAS-BRAND-GUIDE-v4.md` are where James says.
- That no live page uses the off-scale size variables (`--text-micro`, the 14px non-scale sizes, 14px `--text-label`).
- That the Cloudflare Pages build image has `python3`.
- Whether any long-form report template pages exist, and at what path.
- The GitHub username to use for James.

---

## 4. Step 0: Verify (read-only), Then Stop

1. **Branch and tree.** Report the current branch; it must be `dev`. Report `git status`, and list every modified or untracked file. Mark which belong to Nodes and Networks.
2. **Handoff files.** Confirm the handoff zip contents are available to you. Justin will place them, or tell you where they are.
3. **Archive targets.** For each file in James's Step 1 table, report present or absent and its actual path. Do the same for the Step 4 cleanup table: `README.md` sections, `START-HERE.md` "For James", every copy of `james-design-principles.*`, `SESSION-3-HANDOFF.md`, and both ledgers.
4. **Line numbers.** For every `CLAUDE.md` and `variables.css` location James cites, quote the current lines. Say whether they match what his replacement expects. Where they don't, propose the correct anchor (a heading or unique string).
5. **Off-scale size variables.** Grep the public pages (everything the check scans) for each variable James's Step 5 removes. Report any use.
6. **Long-form reports.** Find any page built from `Atlas-Long-Form-Report-Template-2026-09.md`, and report its path or paths.
7. **Build image.** Check `build-dist.sh` and any Cloudflare config in the repo for the build image or Python version. If you can't determine it from the repo, say so. Justin will confirm in the first build log.
8. **Current violation count.** Copy James's unmodified `check_brand.py` into place and run `python3 scripts/check_brand.py --report`. Report the total and the per-rule counts. James recorded 2,308 in 59 files on the public repo. Don't write a baseline.

**Report and stop.** Justin confirms the anchors, the archive list and the report-page paths before Part A.

---

## 5. Part A: Install Documents and Update Rule Files

Follow James's brief §3–§7 (his Steps 1–5) with these changes.

**A1. Documents (James Step 1).**
- Use `mv`, not `git mv`. GitHub Desktop detects the renames.
- Add `docs/briefs/V16-FOUNDATION-INSTALL-BRIEF-v1.0.md` (this file) alongside James's three briefs.
- Skip any archive target that Step 0 found absent, and note it in Part F.

**A2. Split the design rules out of `CLAUDE.md` (amends James Step 2).**

Create `docs/design/CLAUDE-DESIGN-RULES.md`, titled "# Atlas Design Rules for Claude Code — v16". It holds the content James wrote for three sections:
- **2d** (Locked rules). Edit one bullet: replace the protected-files list with the narrowed list in Part D.
- **2e** (Typography rules).
- **2g** (What changes only with a new token version).

Open the file with: `*Owned by James Bareham. Implements DESIGN-TOKENS-v16.md. Where this file and CLAUDE.md differ on design, this file wins.*`

In `CLAUDE.md`, apply James's **2a, 2b, 2c, 2f and 2h** as written. Then make two additions:
- In the 2c required-reading table, add a row: `| docs/design/CLAUDE-DESIGN-RULES.md | Before any CSS, styling, inline styles, chart or canvas work. Read first; it overrides this file on design |`
- At the top of `## Design System`, replace 2d's block with:
  ```markdown
  **Design rules are locked to v16 and live in `docs/design/CLAUDE-DESIGN-RULES.md`. Read it before any styling work.** Never pick a design value; apply briefs by role; undefined means unbuilt. That file wins over anything in this section.
  ```
- Remove the old "Body copy minimum", "Font weights" and "What requires James's sign-off" text, as James intended. Its replacement now lives in the design rules file.

**A3. `WORKFLOW.md` (James Step 3).** Apply 3a–3e as written. In 3d step 4, the phrase "files under CODEOWNERS" now refers to the narrowed list. No edit is needed.

**A4. Cleanup (James Step 4).** Apply as written, using whatever paths Step 0 found.

**A5. `variables.css` (James Step 5).** Apply as written. Use Step 0's anchors if the line numbers moved. If Step 0 found a live use of a removed size variable, stop and report it instead of removing it.

---

## 6. Part B: Amend `scripts/check_brand.py`

Start from James's file. Keep every existing rule, allowlist, exclusion and mode. Changes:

**B1. Hex colors: 4- and 8-digit forms.**
- Extend `HEX` to match 3-, 4-, 6- and 8-digit hex.
- For 4- and 8-digit hex, strip the alpha and check the base against `PALETTE`:
  - Base not in the palette → rule `color`.
  - Base in the palette → rule `color-alpha` (palette color with transparency, to be reviewed by James).

**B2. Functional colors.** Flag every `rgb(`, `rgba(`, `hsl(` and `hsla(` in CSS, inline styles and JS strings as rule `color-func`. Don't try to map the values to the palette.

**B3. Named colors.** Flag CSS named color keywords as rule `color-name` when they are the value of a color-bearing property or attribute:
- CSS properties: `color`, `background`, `background-color`, `border*`, `outline*`, `fill`, `stroke`, `text-decoration-color`, `box-shadow`, `caret-color`, `accent-color`, `column-rule-color`.
- SVG attributes: `fill="…"`, `stroke="…"`.
- D3 and JS: `.attr('fill'|'stroke', …)`, `.style('color'|'fill'|'stroke'|'background', …)`, `.style.color = …`, `ctx.fillStyle` and `ctx.strokeStyle`.

Use the full CSS named-color list. Don't flag `white` and `black` (both are palette colors), or `transparent`, `currentColor`, `inherit`, `initial`, `unset`, `revert` and `none`.

**B4. Hex false positives.** Don't report a hex match in these cases:
- (a) It's preceded, ignoring quotes and whitespace, by `href=`, `xlink:href=`, `url(`, `querySelector(`, `querySelectorAll(`, `closest(` or `getElementById(`.
- (b) It's part of a CSS selector. Treat it as a selector when a `{` follows before the next `;`, `}` or newline, for example via the lookahead `(?=[^;{}\n]*\{)`.

Gradient stops like `#fff, #000)` must still be checked.

**B5. Ratchet tightening (`--tight`).** Add a `--tight` mode. It fails like the default mode on new violations. It also fails in two more cases:
- Any file and rule count is below its baseline.
- The baseline lists a file that no longer exists.

The failure message: `Baseline is loose: run python3 scripts/check_brand.py --write-baseline and include scripts/brand-baseline.json in this change.`

The default mode (used by `build-dist.sh`) is unchanged, so local and preview builds don't fail just because something improved.

**B6. Baseline guard (`--guard-baseline <git-ref>`).** CI only.
- Read the baseline at `<git-ref>` with `git show <ref>:scripts/brand-baseline.json`. If it doesn't exist there, pass.
- Fail if any file and rule count in the working baseline is higher than at the ref.
- **Exception:** allow increases when `scripts/check_brand.py` itself differs from the ref (`git diff --name-only <ref> -- scripts/check_brand.py`). A stricter check legitimately raises counts, and that file is under James's review.

Message on failure: `Baseline went up. Counts may only fall unless check_brand.py changed in the same pull request.`

**B7. Serif path.** If Step 0 found long-form report pages, add their path prefix to `SERIF_ARTICLE_PATHS`. Use a comment citing v16 § Exceptions ("editorial articles: watershed/ and long-form report template pages"). If none exist, leave the tuple as is and add the comment `# add the long-form report path here when the first report page is built (v16 § Exceptions)`.

**B8. Docstring.** Add the new rules (`color-alpha`, `color-func`, `color-name`) and modes (`--tight`, `--guard-baseline`) to the docstring.

**B9. Fixtures.** Add `scripts/brand-check-fixtures/should-pass.html` and `should-fail.html`. `scripts/` is excluded from normal runs, and naming a file runs it strictly.

`should-pass.html` must produce zero violations. It contains:
- `<a href="#bad">`
- `<a href="#add">`
- `document.querySelector('#bed')`
- a selector `#fade { }`
- `color: var(--color-text)`
- `color: #5d7400`
- `color: white`
- `fill: currentColor`
- `border-color: transparent`
- `font-family: var(--font-primary)`
- `font-size: 13px`
- `background: linear-gradient(#ffffff, #000000)`

`should-fail.html` must produce exactly these rules:

| Line | Rule |
|---|---|
| `color: orange` | color-name |
| `.attr("fill","tomato")` | color-name |
| `color: rgb(255,150,0)` | color-func |
| `background: hsl(30 100% 50%)` | color-func |
| `color: #ff960080` | color |
| `color: #00000080` | color-alpha |
| `font-family: "Playfair Display"` | font-literal + font-family |
| `font-size: 10px` | font-size |
| `.x{color:#ff9600}` | color |

---

## 7. Part C: Wire the Check into the Build

1. **`build-dist.sh`.** Add James's line right after `set -eu`, exactly as written in his §8.3. It uses the default mode.
2. **`.github/workflows/brand-check.yml`.** Replace James's file with:

```yaml
# Runs the Atlas brand check (DESIGN-TOKENS-v16.md § Enforcement).
# Make "brand-check" a required status check on main.
name: brand-check
on:
  push:
  pull_request:
jobs:
  brand-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - name: Check fonts, sizes and colors against DESIGN-TOKENS-v16
        run: python3 scripts/check_brand.py --tight
      - name: Baseline may only go down
        if: github.event_name == 'pull_request'
        run: python3 scripts/check_brand.py --guard-baseline "origin/${{ github.base_ref }}"
```

3. **Run the fixtures** (B9) and report the output.
4. **Run `--report`** on the whole tree and report the totals per rule. Show James's original rules and the new `color-alpha`, `color-func` and `color-name` rules separately.

**Stop. Report and wait for Justin.** The baseline is written only after Justin has seen these counts.

---

## 8. Part D: Baseline and CODEOWNERS

**D1. Baseline.** After Justin's go, run `python3 scripts/check_brand.py --write-baseline`, then `python3 scripts/check_brand.py --tight`. The second command must pass.

**D2. `.github/CODEOWNERS`.** Replace James's file with:

```
# Files that hold the Atlas design rules. Changes need James's review (DESIGN-TOKENS-v16.md § Enforcement).
# Scoped to design: product docs, build script, _headers and Nodes and Networks are Justin's.
/docs/design/                        @JAMES_GITHUB_USERNAME
/assets/css/variables.css            @JAMES_GITHUB_USERNAME
/scripts/check_brand.py              @JAMES_GITHUB_USERNAME
/.github/workflows/brand-check.yml   @JAMES_GITHUB_USERNAME
/.github/CODEOWNERS                  @JAMES_GITHUB_USERNAME
```

Replace the placeholder with the username Justin confirms. If Justin doesn't have it yet, leave the placeholder and say so in the report.

**What changed from James's version, and why:**

- **`scripts/brand-baseline.json` is no longer owned.** The B6 guard blocks any increase mechanically. Without that change, every PR that fixes a page would wait on James just to lower a count.
- **`build-dist.sh` is no longer owned.** The required CI check runs on its own, so deleting the line from `build-dist.sh` can't bypass enforcement.
- **`_headers` is no longer owned.** The NN5 tooling rewrites it, so owning it would gate every Nodes and Networks deploy.
- **`CLAUDE.md` and `WORKFLOW.md` are no longer owned.** The design rules now live in `docs/design/CLAUDE-DESIGN-RULES.md`, which is owned.
- **Only the brand-check workflow is owned, not all of `.github/`.** That is the file that could disable enforcement.

---

## 9. Part E: Justin's Manual Steps (GitHub and Cloudflare)

Code can't change these settings. Include this checklist verbatim at the end of the run report.

1. **Add James as a collaborator** with write access (repo → Settings → Collaborators).
2. **Ruleset for `main`** (Settings → Rules → Rulesets → New branch ruleset, target `main`):
   - Require a pull request before merging.
     - **Required approvals: 0**, so PRs that touch no owned files merge without a second reviewer.
     - **Require review from Code Owners: on.**
   - Require status checks to pass: `brand-check`.
   - Block force pushes.
   - Bypass list: empty. As repo owner, Justin can still edit the ruleset in an emergency, and that edit is logged.
3. **Test the ruleset** with two throwaway PRs from `dev`:
   - A comment-only change to `README.md`. It should merge with no review.
   - A comment-only change to `variables.css`. It should request James's review and block the merge.

   Close both without merging. If the first PR also demands a review, the 0-approvals setting didn't take; report it.
4. **Cloudflare Pages:** confirm preview deployments are on for `dev` (Settings → Builds & deployments → Preview branches). In the first `dev` build log, confirm the brand check ran and printed `OK`. If `python3` is missing, don't remove the line from `build-dist.sh`; tell Justin.
5. **James's Step 6.5 test.** On a scratch branch, add `.x{font-family:"Playfair Display";font-size:10px;color:#ff9600}` to any page. Push it and confirm both the Cloudflare build and `brand-check` fail. Then add `color: orange` instead and confirm it fails too. Delete the branch.

---

## 10. Part F: Notes for James

Write `docs/briefs/V16-INSTALL-NOTES-FOR-JAMES-2026-10.md`. Keep it short and factual: it's the agenda for Justin's walkthrough with James. It covers:

- **What was installed as written.**
- **Each amendment, one paragraph each:** what changed, why, and the file. The amendments are the design-rules file split, B1–B7 and the narrowed CODEOWNERS.
- **Anything from Step 0 that didn't match his brief:** missing archive targets, moved line numbers, report paths.
- **Baseline counts:** his original rules vs. the new color rules. The new rules mostly record existing off-palette usage for his next token version, not new problems.
- **Open items for James and Justin:**
  - Whether `color-alpha` and `color-func` uses get palette roles or a rule.
  - The open questions at the end of the Pulse and For Brands brief.
  - Team DMV's header and footer.
  - The TIJA LLC GitHub organization.

---

## 11. Acceptance

- [ ] All of James's §12 acceptance items pass, with "a pull request touching `variables.css` asks for James's review" confirmed by Part E's test.
- [ ] `docs/design/CLAUDE-DESIGN-RULES.md` exists, and `CLAUDE.md` points to it from the required-reading table and the top of `## Design System`.
- [ ] `grep -n "Merriweather\|Playfair\|DM Sans\|Space Mono" CLAUDE.md` returns only allowlist or pointer text. There must be no instruction to use a retired font.
- [ ] `should-pass.html` reports zero violations, and `should-fail.html` reports exactly the rules in B9.
- [ ] `python3 scripts/check_brand.py` and `--tight` both pass on `dev` after the baseline is written.
- [ ] In a test where one count is raised by hand, `--guard-baseline origin/main` fails. With `check_brand.py` also modified, it passes. Revert both afterward.
- [ ] CODEOWNERS matches D2.
- [ ] No Nodes and Networks file is modified by this run. `git status` is checked against the Step 0 list.
- [ ] No visible change on the `dev` preview compared with `main`.
- [ ] The run report ends with:
  - The explicit list of files to stage.
  - The Part E checklist.
  - The path to the notes for James.

---

## 12. Close-Out

- Append a `LEAVE-OFF-LOG.md` entry: what was installed, the baseline totals, and what's pending Justin's manual steps.
- Add to `START-HERE.md` (open decisions only):
  - Walk James through `V16-INSTALL-NOTES-FOR-JAMES-2026-10.md`.
  - Team DMV header and footer.
  - TIJA LLC GitHub organization and the repo going private (see the repo-visibility brief).
- **Next runs, in order:**
  1. `Atlas-Type-Consolidation-Brief-2026-10.md`
  2. `Atlas-Pulse-For-Brands-Brief-2026-10.md`

  Each regenerates the baseline in the same change, so counts go down.
