# Design state, 2026-10-31

*For the review between Justin and James. Written by Code from the repo at production `main` (local HEAD after the Oct 31 sweep). Facts only, each with a path or hash; the agenda at the end has options and a recommended default. **No design changes were made.** Justin decides; James reviews.*

## 1. Installed design system

| Item | State | Evidence |
|---|---|---|
| Tokens | **v16** (`DESIGN-TOKENS-v16.md`) | Landed in `abbcc9c` "big design changes" (2026-10-28), second pass `39d06db`; branch `v16-install` merged by PR #6 (`439ff58`, 2026-10-28). |
| Brand guide | **v5** (`ATLAS-BRAND-GUIDE-v5.md`) | Same commits. Byte-identical to the copy in `~/Downloads`. |
| Design rules | `CLAUDE-DESIGN-RULES.md` (split out of `CLAUDE.md`; under James's review) | `docs/briefs/V16-INSTALL-NOTES-FOR-JAMES-2026-10.md` section 2. |
| Superseded | v15 tokens, brand guides v3 and v4, `pulse_tokens.md` | `docs/design/archive/`. |
| Install brief | `V16-FOUNDATION-INSTALL-BRIEF-v1.0.md`, with Justin's amendments (B1-B7) | `docs/briefs/`. |
| v15 sessions | Sessions 1 and 2 shipped; **Session 3 not started** | `docs/design/v15-session-2/SESSION-3-HANDOFF.md`; no Session 3 report in `docs/design/`. |
| Stale header text | `variables.css` header comments still say v15 | Install notes section 3. |

## 2. Brand check

| Item | State | Evidence |
|---|---|---|
| Baseline | **2,766 violations in 58 files** (was 2,777 in 59 before today) | `scripts/brand-baseline.json`; regenerated in `6c75194`. |
| CI mode | `check_brand.py --tight` on every push; `--guard-baseline origin/<base>` on pull requests (counts may only go down) | `.github/workflows/brand-check.yml`. |
| Local result | `--tight` exits 0; `--guard-baseline origin/main` says "no count went up" | Run 2026-10-31. |
| Was it red? | Yes, at `8b65f2b`, from `preview/nn-launch-kit-staging/explorer/index.html` (45 violations, baseline 0). **W12 outcome:** nothing referenced that path (`git grep` found only my own START-HERE note; not in `build-dist.sh`, `_redirects`, `_headers` or `EMBED.md`; the ASU embed address is `preview/nn-launch-kit/explorer/` and is untouched). Retired to `_deprecated/` in `be0d717`; the baseline was regenerated (`6c75194`) because two files left the scan. The stale `_reviewjames copy.html` baseline entry I created on Oct 31 also cleared. | |
| Exclusions | `EXCLUDED` in `check_brand.py` changes "only with a new token version". It covers `_deprecated/`, `preview/nn-launch-kit/`, `nn/`, `qa/`, `docs/` and others. `_archive/` is **scanned**, so production archives go to `_deprecated/` (rule recorded in `_archive/2026-10-sweep/MANIFEST.md`). | `scripts/check_brand.py:44-52`. |
| Burn-down | Approved order: `index.html`, `pulse.html`, `city-lab-chicago.html`, then by count. Each fix regenerates the baseline in the same change. | `START-HERE.md`. |
| What the baseline holds | Install notes section 4: original rules 2,310 (`color` 1,374, `font-size` 410, `font-literal` 272, `font-family` 151, `font-weight` 34, `serif-scope` 29, `pill-radius` 19, `serif-heading` 17, `lime-text` 4), plus `color-func` 467 (307 white or black text, 144 tinted palette colors in non-text properties, 16 other text). Counts have since fallen by 11 (2,777 to 2,766). | `docs/briefs/V16-INSTALL-NOTES-FOR-JAMES-2026-10.md`. |

## 3. Ownership and branches

| Item | State | Evidence |
|---|---|---|
| CODEOWNERS | **None** in either repo. Narrowed list ready: `/docs/design/`, `variables.css`, `check_brand.py`, `brand-check.yml`, CODEOWNERS itself. Needs James's GitHub username. | Install notes section 2; `ls .github`. |
| `origin/dev` vs `main` | `origin/dev` is a stale March branch (last commit `fc1a83e`, 2026-03-06). `main` is 508 commits ahead; the two differ by 919 files (+37,385 / -266,237). No local `dev` branch exists. The install notes say a fresh `dev` was cut from `main`; **that branch is NOT FOUND**. | `git rev-list --count origin/dev..main`; `git branch --list dev`. |
| Workflow doc vs practice | `WORKFLOW.md` Deploy Process says "work on `dev`, PR to `main`, James reviews". In practice commits go straight to `main`, and `james/*` branches (mentioned in an Oct 11 design-lane patch in the private repo) are NOT FOUND. | `WORKFLOW.md:54-60`; `git branch -a`. |
| Branch protection | Not possible while the repo is public on a free org (readiness item, W3). | `ops/DECISIONS-QUEUE.md` W3. |

## 4. `JAMES-OPEN-ITEMS.md` (v15 Session 2)

`docs/design/v15-session-2/JAMES-OPEN-ITEMS.md` has 18 numbered questions plus 5 recorded decisions. **No answers are recorded in any file.** Status: all 18 open. The ones that block other work:

| # | Question | Blocks |
|---|---|---|
| 3 | Apply the held-back nj-lab header patch (`v15-session-1/C4-held-back.patch`)? | nj-lab and njlab pages |
| 2 | Primary button on the black hero rests gray. Right, or exempt dark heroes? | Homepage hero |
| 4 | Tab strips: treat as Secondary buttons, or give underline tabs a spec? | Pulse, Chicago |
| 9 | About 40 links end in `↗` or `↓`; spec says `→`. Keep or convert? | Copy sweep |
| 17 | C10b: hamburger at 1214px and a 24px gap | Header |
| 15 | `.btn-icon` has no spec entry | Component set |
| 1, 5-8, 10-14, 16, 18 | Smaller: header search height, hero pills, Acid links at rest on dark, carousel dots, press chips, hover-only "Explore cluster", one-column Pulse grid at 480px, `aria-current` sections, inline "How we verify", Report "Jump to", Bluesky "For brands" button, copy wording | Various |

## 5. James's "seven Oct 28 questions": not found as a set

No file carries seven questions dated Oct 28. The closest lists are:
- **Install notes section 5 (Oct 27, six bullets):** tinted palette colors (144 hits) and the provisional error role; the open questions at the end of the Pulse and For Brands brief; lab notebook "Trace this number" (opens in place or side panel; one motion or none); Team DMV header and footer; the TIJA LLC organization and the repo going private; James's GitHub username. None has an answer on file.
- **Pulse and For Brands brief section 6 (six token-version decisions):** a "live" signal, a warning color, error-text contrast, a site dark mode, a responsive Display size, graphic strokes on dark mastheads. None has an answer on file.

If a seventh question exists, it is in Chat or email; please paste it. It would not be answerable from the repo.

## 6. Unmigrated surfaces

| Surface | State | Evidence |
|---|---|---|
| Bluesky page on mobile | Still overflows at phone width (705px; no mobile layout). Not touched since `50251de` (2026-10-27, an unrelated About commit). | `JAMES-OPEN-ITEMS.md` 19; `SESSION-3-HANDOFF.md` item 1. |
| nj-lab and njlab partner pages | No `components.css`; `variables.css` link flagged as broken (relative path) in START-HERE; 9 root and partner pages still don't load `variables.css` (START-HERE said 22 on Oct 6). Both are near-duplicates and both are live. | `grep -c components.css partners/nj-lab.html` = 0. |
| v15 Session 3 | Not started. Items: Bluesky mobile; eyebrows (many still DM Mono or JetBrains Mono at 8-11px on `index`, `for-brands`, `pulse`, `research`); tags (replaced by the Type Consolidation brief); nj-lab (needs James); dead CSS (`DEAD-CSS.txt`, about 60 selectors in 15 files); internal pages that use Lime in UI; `↗`/`↓` arrows; copy sweep. | `SESSION-3-HANDOFF.md`. |
| `ATLAS_VIZ_COLORS` | `ATLAS_VIZ_COLORS.md` is dated May 2026 ("signed off by James") and sits at the repo root, referenced in `CLAUDE.md` and 7 times in `DESIGN-TOKENS-v16.md`. About 27 JS-set greens in chart palettes were listed and not changed (START-HERE). v16 records no migration for it. | `git log -1` on the file: `aab28cb` 2026-05-28. |
| Report "Jump to" | Restyled for the old preview only; still DM Sans with its own sticky bar. | `JAMES-OPEN-ITEMS.md` 14. |
| Provisional rules | Error text roles, monospace = live or versioned data only, Acid = changed recently. | `CLAUDE-DESIGN-RULES.md`. |

## 7. Launch-week design facts (Nodes and Networks)
- The strip wording is Justin's (`nn-launch` `5be2bbc`): "New from the Atlas: Nodes and Networks, a field study of how American journalism is reorganizing".
- The research hub review sheet for James is `docs/design/research-hub-review/` (commit `45002c0`).
- The N&N explorer is under the co-branded exception (`nn/`, `preview/nn-launch-kit/` are excluded from the brand check).

---

# Review agenda for Justin and James

Each item: the decision, options, and a recommended default. Items 1-4 are token-version decisions (James writes or approves). Items 5-9 are process and structure.

| # | Decision | Options | Recommended default |
|---|---|---|---|
| 1 | **Tinted palette colors** (Acid or Lime with alpha, 144 `color-func` hits in non-text properties) | (a) allowed as tints and overlays; (b) get palette roles; (c) forbidden | (a). It drops the baseline's `color-func` count from 467 to 323 with no visual change. |
| 2 | **Error text roles** (`#f50000` is 4.3:1 on white and 3.7:1 on `--color-bg`, below 4.5:1; James rejected Material `#b3261e` in May as too dull) | keep the provisional `*-provisional` tokens; James picks a new red; use a darker red for text only | Keep the provisional tokens until James picks. |
| 3 | **"Trace this number" (About Phase 3):** open in place or in a side panel; one motion or none | in place; side panel; plain open with no motion | In place, no motion (v16 has no motion roles). |
| 4 | **Next token version list** (Pulse and For Brands brief section 6): live signal, warning color, site dark mode, responsive Display size, strokes on dark mastheads | write one v17 covering items 1-3 and these six; or defer all | One v17 after Nov 5. |
| 5 | **CODEOWNERS and James's GitHub username** | write now for the five design paths; wait for the privacy decision | Write now; Justin decides, James reviews design paths only. |
| 6 | **Branch workflow.** `WORKFLOW.md` says `dev` plus PR; practice is `main`; `dev` and `james/*` don't exist. | recreate `dev` and follow `WORKFLOW.md`; or change `WORKFLOW.md` to match practice | Change `WORKFLOW.md` to match practice (James reviews on a `james/*` branch; Justin merges). |
| 7 | **Where production archives live** | add `_archive/` to the checker's `EXCLUDED` (needs a token version); or keep archives in `_deprecated/` | Keep `_deprecated/`. A dead copy shouldn't earn a permanent exception. |
| 8 | **`JAMES-OPEN-ITEMS` 2, 3, 4, 9, 15, 17** (the blockers in section 4) | answer each; or answer 3 and 9 now and park the rest | Answer 3 (nj-lab) and 9 (arrows) first; they unblock Session 3. |
| 9 | **Session 3 order after Nov 5** | Bluesky mobile first; eyebrows first; nj-lab first | Bluesky mobile, then nj-lab, then eyebrows. The overflow is the only phone-width break left. |
| 10 | **Team DMV header and footer** | follow the site header; keep its own | Follow the site header. |
| 11 | **Retire or keep `preview/nodes-and-networks-f348eb08/`** (old v938 preview, frozen until after Nov 5) | archive to `_deprecated/` after launch; keep | Archive after launch. |
