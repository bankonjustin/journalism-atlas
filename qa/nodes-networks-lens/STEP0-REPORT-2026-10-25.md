# Nodes and Networks, lens edition: Step 0 report (Oct 25, 2026)

Nothing built. No files in `dist/`, `preview/` or `assets/` were touched. Only additions: this report, `qa/nodes-networks-lens/before/` (12 screenshots), and a backup at `~/Documents/GitHub/nodes-networks-v5/backups/2026-10-25-pre-lens/` (outside the repo, so it can't be committed by accident).

## STOP-level finding: org names are already in the public repo

1. **`journalism-atlas` is public** (github.com/bankonjustin/journalism-atlas answers 200 unauthenticated; `-private` answers 404).
2. v5's explorer (`preview/nodes-and-networks-edition-e852c5c5/explorer/index.html`) and the `embed/fig-6-kaleidoscope/` page embed `nn-data` with **`"show_org_names":true`**: all 169 rows with real names, cohort, revenue band, origin (started above / grew past / still under), mechanism, founding year and closed/acquired status. Builder `tools/build_nodes169.py` has `SHOW_ORG_NAMES = True`; `edition/config.json` says `EXPLORER_PUBLIC: false`, which only gates the link, not the files.
3. Those files are in commit `07a622a "lets go"` and are **on `origin/main`**. The live URLs return a Cloudflare challenge/403 today, but the data is readable in the public GitHub repo. The paper says the dataset is "available on request" (Introduction, para 6).
4. Ground rule 7 therefore applies to the new edition: it embeds nothing beyond what v5 already embeds, and I'd build it with `SHOW_ORG_NAMES=false` (anonymous `n001`-style labels). Whether to scrub the v5 explorer/fig-6 files and the history is your call; I haven't touched them. Removing them from the working tree does not remove them from git history.

## 1. Repo and data location
- Public repo → data stays in `journalism-atlas-private` / `paper-one-band-dataset`. New edition embeds only the derived, name-free `nodes169` form (cohort, band, origin, mechanism, founding year, closed flag, precomputed positions; no dollar values, no names).

## 2. v5 source
- **Generated**, by `~/Documents/GitHub/nodes-networks-v5/edition/` (outside both repos): `tools/build_edition.py`, `stage.py` (copies into `journalism-atlas/preview/<slug>/`, `assets/nn5/`, `build-dist.sh`, `_headers`), `build_nodes169.py`, `qa.py`, `launch.py`. Reads patched `tools/preview-build/content/content.json` (read-only) plus figure data from `paper-one-band-dataset`.
- It is *not* `tools/preview-build/` but it consumes that content. Plan: copy `edition/` to `nodes-networks-v5/edition-lens/` with its own `config.json` (slug `nodes-and-networks-lens-<hash>`), assets under `assets/nn6/` so v5's `assets/nn5/` stays untouched, and regenerate; no hand edits in `dist/`.

## 3. Explorer embed
- Path: `preview/nodes-and-networks-edition-e852c5c5/explorer/` and `embed/fig-6-kaleidoscope/`. Source: `edition/src/js/figs/kaleido.js` (renderer, **Canvas 2D**) plus `kaleido-intro.js` (the opening). Reel counterpart: `kaleidoscope/reel/nn-kaleido-engine.js`.
- Data: `edition/src/data/nodes169.json`, embedded as `#nn-data` → `nodes169`. v5 story page's `nn-data` holds only fig1/2/4/5; **it does not read nodes169**, so "same data" is true only for the explorer and the reel.
- Lenses (5): field, governance, "Who got past $10M" (origin), "Six ways past $10M" (mech), "When they started" (born). The brief's four turns map to gov, budget, origin, born. Budget is shown as zone rings on gov/origin/mech; there is **no standalone budget lens** in the engine (gov already puts distance = band). The explorer's `mech` lens has no turn in the brief.
- Names: shown on hover card and in the list view when `show_org_names` is true (it is, today). 3 rows flagged `EXCLUDE_UNVERIFIED` are never named, and 16 rows aren't `INCLUDE` (proxy/historical figures).
- **Renderer vs brief:** the brief wants SVG with `<title>/<desc>` and static SVG frames for no-JS and print. The one existing renderer is Canvas. One renderer is possible (reuse `kaleido.js` for the live stage, with a build-time SVG serializer from the same layout data for frames), but that is a new piece of work. Decision needed (see below).

## 4. Data
- File: `edition/src/data/nodes169.json`, built from `cohort_reference_expanded_v22.csv` and `MECHANISM-CODING-RESOLVED-2026-10-23.csv`. **169 rows, OK.**
- Fields present: cohort, band (budget), origin (path past $10M), founding year (`fy`; 4 rows null = 3 unverified + 1 other). Exact dollars are intentionally not output.
- Reel numbers, all verified against the data: C2 = 26 ✓, C4 = 44 ✓, origin 25 / 30 / 114 ✓, founded 2008 or later = 113 of 169 ✓ (4 rows have no year, so 113/165 of rows with a year; the reel's denominator is 169).
- Other counts: bands 80 under $3.5M / 34 mid / 55 over $10M; flags INCLUDE 153.
- **Paper vs data, for COPY-DECISIONS:** the paper's founding claim uses **1995** ("founded before 1995 … overwhelmingly over $10 million"; "native to the current era … most sit below $3.5 million"), while the reel and explorer use **2008**. At the 1995 cut the data gives: 35 founded before 1995 with 21 over $10M (60%), 11 under $3.5M, 3 mid; 130 founded 1995+, 68 under $3.5M (52%), 31 over $10M. "Overwhelmingly" is a stretch for 60%; "most" is a bare majority. Flagged, not changed.

## 5. Family names
- **The paper gives no names, only descriptions** (Section II, "Nine cohorts capture… in three groups", 3-item list, `content.md` lines 91–95):
  1. "journalism as most people picture it — reporters, outlets, bylines" (C1–C3)
  2. "the infrastructure through which public-minded funding becomes public-interest reporting, and the cohorts most exposed to the funding collapse" (C4–C6)
  3. "the clearest evidence that audiences and the market are finding new ways to fund journalism directly" (C7–C9)
- v5's `lib.js` `GROUP_LABEL` shortens these to "Journalism as most people picture it" / "How public-minded funding becomes reporting" / "New ways audiences and markets pay directly". These are v5's, not the paper's.
- The older caption wording ("legacy-like journalism", "public-interest infrastructure", "market-funded") appears nowhere in `content.md` or the v5 page. (The phrase "public-interest infrastructure" does appear in C4's "What it is": "the field's public-interest infrastructure".)
- v5 already uses **three** group colors (gold `#F6C84E`, maroon `#812740` / `#B23A5E` on dark, grey `#868686` / `#A8A8A8`) with shapes circle / square / diamond. **There is no nine-color or subway-line-per-cohort system to migrate**; the subway lines already are the three groups. Cohort-specific coding is by label only.

## 6. Hollow markers and size (from `kaleido.js`, lines 64 and 120)
- **Hollow = organization is closed** (`cl === 'CLOSED'`, 5 orgs). Acquired (3) and absorbed (3) are drawn solid. The v5 legend labels it "Closed".
- **Size = revenue band** (3 sizes: .0095 / .014 / .0195 of radius for under $3.5M / mid / over $10M). Group-a circles also carry a thin black edge.

## 7. Prose-to-lens map (paper order differs from the reel)

| Lens | Where the argument lives | Anchor | Matches reel order? |
|---|---|---|---|
| Founding year | **Introduction**, para 4 ("Sort the field by when an organization came into existence…"), `content.md` line 27 | `#intro-h` | **No: first in the paper, last in the reel.** Uses 1995, not 2008. |
| Budget bands ($3.5M / $10M) | Introduction, same paragraph; bands reappear Section III on Fig 4 ("between $3.5 million and $10 million") and Fig 5 ("revenue bands") | `#intro-h`, `#paths-h` | Intro first; the bands are not explained until the Fig 4/5 passages |
| Governance (nine cohorts) | Section II, `#cohorts-h`, C1–C9 at `#c1-h`…`#c9-h` | | Reel: 1st; paper: 2nd |
| Path past $10M (six mechanisms) | Section III, `#paths-h`, six-item list then "No organization … above $10 million without … one of those six things" (line 338) | `#paths-h` | Paper: 3rd; reel: 3rd, but the reel's **25 / 30 / 114 "started above / grew past / still under" split does not appear in the prose**, only the six mechanisms do |
| Fig 5 (bands by cohort) | Section III, after Fig 4 | `#paths-h` (late) | Becomes Turn 2 per brief |

Paper order is therefore: **founding year + bands (Intro) → governance (II) → six paths (III) → bands by cohort (III, end)**. Reel order: governance → budget → past $10M → founding. The turns must follow the paper, so the proposed sequence is: Intro: field at rest, with founding year and budget bands available as the cover's first turns; II: governance wedges; III: path past $10M, then budget by cohort. That is a different number of turns than "four, ending in founding year". **Decision for Justin** (#3).
- Section I (economic context) sits between the Introduction and the cohorts, so "Two numbers" and the timeline stay in the pre-object zone, as the brief asks.

## 8. Baselines
`qa/nodes-networks-lens/before/`: `v5-{1400,768,390}-viewport.png` + `-full.png`, `explorer-…-viewport.png`, `embed-fig6-…-viewport.png`. No console errors and no horizontal overflow at any width. Explorer shots were caught mid-opening (2.5 s after load). v5 full page is ~49,430 px tall at 1400 and 71,562 at 390.

## 9. v5 embeds and share images (nothing deleted)
| Embed | Figure | Fate under the brief |
|---|---|---|
| `embed/fig-0-scale` | Two numbers | keep, restyle |
| `embed/fig-1-timeline` | Timeline | keep, restyle |
| `embed/fig-2-map` | **Subway cohort map** | **retired** |
| `embed/fig-3-defector` | Defector chart | keep as close-up |
| `embed/fig-4-threshold` | Dependence slider | keep as close-up |
| `embed/fig-5-bands` | **Figure 5** | **retired as standalone** (data table stays) |
| `embed/fig-6-kaleidoscope` + `explorer/` | Explorer | replaced by new explorer embed (**contains names**) |

Share images in `og/`: `cover`, `fig-0…fig-6` (each 1200×630), `kaleido-gov-still.png`. Retired: `fig-2-map-1200x630.png`, `fig-5-bands-1200x630.png`. Also `smartnews-d029dc36` and `f348eb08` untouched.

## Other things noticed
- `CLAUDE.md` and brand guide v4 say **Hanken Grotesk is retired** and the site is on Inter; the brief names Hanken Grotesk and Merriweather as "Atlas brand fonts". Needs confirming before the font-variable decision.
- The end-card URL placeholder `ASU.com/nodes-networks` is in the reel files only; still need the real address.
- v5 prose has known unresolved items (memory: El Tímpano $600K vs $350K, "a 42,500 subscribers" typo, missing Defector Year 5 sentence). They carry into the lens edition unchanged and belong in COPY-DECISIONS.
- Mobile 390px pinned stage at ~50% height: likely falls back to inline frames given Canvas label size (wedge labels use `max(12, R/24)`, so ≥12px is met, but marks are tiny). Will test in Phase 1.

## Decisions needed before Phase 1
1. **Org names / public repo (above).** Build the lens edition with `SHOW_ORG_NAMES=false`? And what to do about v5's explorer and fig-6, already pushed?
2. **Turn order.** Follow the paper (founding year + bands first) or keep the reel order and accept that the stage runs ahead of the prose for Turn 4? A third option: five turns instead of four.
3. **Founding cut.** Paper says 1995, reel/explorer say 2008. The stage's "2008 marker" would contradict the paragraph it sits beside.
4. **Family names.** The paper has descriptions, not names. Use v5's short phrases, the paper's own clauses, or just C1–C3 / C4–C6 / C7–C9?
5. **Renderer.** Reuse the Canvas `kaleido.js` plus a build-time SVG serializer for frames/no-JS/print, or port to SVG for the live stage as well (heavier, but gives real `<title>/<desc>` and one code path).
6. **Fonts.** Inter Tight + Source Serif 4 (v5), or Atlas brand (and which: brand guide v4 says Inter).
7. Proposed rule for open paragraphs above each drawer (to confirm after the above): keep the first two paragraphs ("What it is", "How it works" lead) open per cohort and collapse the remainder.
