# SITE-RECONCILE-NN-PREP-BRIEF v1.0

From: Cowork session in the "Building the Database/Atlas" Project (plans, rulings, briefs)
To: Claude Code, running in `~/Documents/GitHub/journalism-atlas` (with `journalism-atlas-private` alongside)
Date: Sun Nov 1, 2026
Changelog: v1.0, first version.

Work in phases. Stop at the end of each phase, report in a short numbered list, and wait for Justin's rulings.

---

## Standing rules

- Don't commit or push. Leave changes in the working tree; Justin reviews and commits in GitHub Desktop. If a change has to land on a branch other than `main`, write it as a patch under `docs/patches/` and say so.
- Never run `nodes-networks-v5/launch-kit/deploy.py` or `build.py`.
- Never overwrite canonical data. `cohort_reference_expanded_v*.csv` and `nn/data/nodes169.json` are read-only. If a value looks wrong, flag it and stop.
- Don't edit, move, rename or redirect `preview/nn-launch-kit/explorer/index.html` (Carrie's live ASU embed) without an explicit ruling.
- Derive every number from the data the page loads. Don't type numbers from this brief.
- Split mechanical fixes (make them) from editorial calls (flag them for Justin, and for Andy on paper copy).
- Site copy: short declarative sentences, no bolded inline pseudo-headers, concrete before abstract. Use "governance", never "who pays". Use "above $10M", not "crossed". Use "who's in charge", not "who owns". Don't use "inherited" in reader copy. Write "$10M".
- Two design systems; don't mix them. The ASU embed (`?embed=1` / `?theme=asu`) uses Arial, gold `#FFC627` and maroon. The Atlas site uses the v16 tokens in `docs/design/DESIGN-TOKENS-v16.md` and `assets/css/variables.css`.
- After any visible change: run `python3 scripts/check_brand.py --tight`, then screenshot at 1280 and 390 px before and after.

## Rulings made Nov 1 (don't relitigate)

1. **Names everywhere.** The explorer, the parked edition and the social assets can all show organization names. This rules DECISIONS-QUEUE L5 as "names on". Still don't post the raw CSV.
2. **QA renders can stay in the public repo** for now (`qa/` PNGs, WebMs, MP4s, GIFs). Zip files still never get committed.
3. **Before launch, the site shows a small Watershed banner and no N&N preview.** This is already done in the working tree (see Established facts). It supersedes L3 and L4: the homepage card and the for-brands line are now hidden until launch, not dated.
4. **History A/B staging is back** at `preview/nn-launch-kit-staging/explorer/` for Andy and Carrie's vote. Justin leans settle.
5. **Work happens in Code.** The Cowork session does planning, rulings and briefs.

## Established facts (checked Nov 1, about 11:30 ET)

- `main` matched `origin/main` at `72cb218`. `journalism-atlas-private` is 11 commits ahead of origin (ops docs).
- Uncommitted changes from the Cowork session (9 files):
  - `preview/nn-launch-kit-staging/` restored from `_deprecated/`. The page carries its own noindex meta.
  - `scripts/check_brand.py` excludes `preview/nn-launch-kit-staging/`. Check passes at 2,766 = baseline. The exclusion list says it changes "only with a new token version", so flag this line for James.
  - `assets/js/header.js`: the banner is id `watershed-2026-11`, expires 2026-11-30, reads "New from the Atlas · A Watershed Moment for News Deserts · Read the essay", and links to `/watershed/`.
  - `assets/js/nn-gate.js`: sets `window.ATLAS_NN_LIVE` and supports `[data-nn-hide]` (hidden at launch) as well as `[data-nn-show]`.
  - `assets/js/research-hub.js` and `data/research.json`: pieces with `"gate": "nn"` are hidden before launch and treated as `live` after. `research.html` now loads `nn-gate.js` before `research-hub.js`. The noscript N&N link is removed.
  - `index.html`: the N&N card carries `data-nn-show hidden`.
  - `about-this-project.html`: a Watershed lead shows before launch; the N&N lead shows after. Plus one `p + p` spacing rule.
  - Checked in Chromium at 1280 and 390 px, before launch and with `?nn=1`. No "Thursday", "Nov 5" or N&N text shows before launch.
- Live ASU embed data, derived: 169 organizations, C1–C9; 30 grew past $10M, 25 started above, 114 below. Rogan is M3. Iowa Public Radio counts as started above. Washington Post, Risk.net and Insurance Journal are unverified. Radio Jornalera NJ has no founding year. The staging copy's data is identical.
- `nn/data/nodes169.json` matches on 30/25 but still codes Rogan as `EXCEPTION_PLATFORM_LICENSING`. The `nn/` build prints "30 of 31 … One exception." `nn/content/copy.md` still says "who pays" and "dashed triangle is the exception".
- The `nn-launch` branch (`5be2bbc`, `451b4ac`, `61ea380`, `af432d2`, merged `a8a5f1d`) is the launch-day flip. It edits the same lines in `header.js` and `research.json` as the Cowork changes, so a merge will conflict.

## Assumptions to verify in Phase 0

- Whether Justin has committed or pushed the Cowork changes since this brief was written.
- That `ops/DECISIONS-QUEUE.md`, `ops/CLEANUP-PLAN-2026-10-31.md` and `docs/design/DESIGN-STATE-2026-10-31.md` are still current.

---

## Phase 0: verify (read-only)

1. `git status` and `git log --oneline -10` in both repos. Report what's uncommitted, unpushed, or differs from the facts above.
2. Run `check_brand.py --tight`.
3. Open `/`, `/research`, `/about-this-project.html` and `/for-brands` with and without `?nn=1` (local server is fine), and confirm the pre-launch state.

**Stop and report.**

## Phase 1: launch readiness (target: ready by Wed Nov 4)

1. **Launch target conflict (the top item).** DECISIONS-QUEUE L10 makes `/nodes-and-networks/` the launch target. That page is built from `nn/`, which still shows Rogan as "the exception" and uses "who pays". The data fix lives in the read-only `nodes169.json`, so don't touch it. Lay out the options for Justin with their diffs, for example:
   - (a) Justin approves a one-row backport of Rogan to M3 in `nodes169.json`, plus copy fixes in `copy.md`.
   - (b) The launch target becomes a page built around the live ASU explorer.
   - (c) Another option you find.

   Stop for a ruling before changing anything.
2. **Launch flip.** Write `docs/patches/nn-launch-v2-2026-11.md`: the `nn-launch` changes redone on top of the current `main` working tree. That means:
   - the banner switches to N&N with a new id;
   - the noindex block for `/nodes-and-networks/*` comes out;
   - the for-brands link points at the final URL.

   With the new gate, `research.json` needs no status flip, so check whether that commit is now redundant. Justin applies the patch in Desktop.
3. **Remaining tier 1 items from DECISIONS-QUEUE:** L1 (release time; `publishAt` is a placeholder), L6 (report URL), L7 (169 against ASU's final PDF), L8, L9, L11. Show each item's current state and the exact one-line change, ready to apply once Justin gives the value.
4. **After the A/B vote** (separate ruling): port the winning History version into the live ASU file with the other behind its flag. Diff it and measure height against the 1,610 px contract in `EMBED.md`. Then re-record the teaser from the live explorer.
5. **Figure embeds** currently point at `/preview/nodes-and-networks-edition-e852c5c5/embed/…`. Recommend either committing to never moving that path or setting up a permanent address, before ASU's designer embeds them.

**Stop and report.**

## Phase 2: make the site sharp (after Phase 1 rulings; mostly after Nov 5)

Use `docs/design/DESIGN-STATE-2026-10-31.md` as the plan. Bring Justin the agenda items with their recommended defaults so he can accept them in one pass, then do the mechanical work:

- Brand-check burn-down in the approved order: `index.html`, `pulse.html`, `city-lab-chicago.html`. Regenerate the baseline in the same change.
- v15 Session 3, in the recommended order: Bluesky page mobile overflow, then nj-lab, then eyebrows.
- Research hub: James's review sheet (`docs/design/research-hub-review/`) and the `coming` vs `placeholder` contract (T9). Keep `placeholder` and fix the doc.
- For Brands and Pulse: interim defaults per S7 (current pages unchanged until v17), plus any outright bugs at 390 px.
- Pulse: confirm the last good run date and propose a weekly Routine spec (W5). Justin pastes the spec into the app himself.

Send only items that need James's eye to James. Make no token changes without a new token version.

**Stop and report.**

## Phase 3: directory cleanup

Follow `ops/CLEANUP-PLAN-2026-10-31.md`, with these Nov 1 changes:

- `qa/` stays public.
- Archives go to `_deprecated/`, not `_archive/`.
- Delete nothing without listing it first.

Candidates:

- the stale `nn/` fork, once Phase 1 decides its fate;
- `dist/` leftovers such as `index 4.html`;
- old local branches (`explorer-v04`, `explorer-v05`, `v16-install`, `favicon-v2`, `favicon-v3`, `retire-old-nn-preview`, `watershed-go`, `private`): report only;
- orphan Routine folders.

**Stop and report.**

## Not in scope

The GitHub two-account setup, repo visibility, the TIJA LLC org and the wider infrastructure review. Those are planned in the Cowork session the week of Nov 2.
