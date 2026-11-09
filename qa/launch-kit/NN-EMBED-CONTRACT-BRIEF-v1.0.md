# NN-EMBED-CONTRACT-BRIEF-v1.0

**For:** Claude Code, in `~/Documents/GitHub/journalism-atlas`
**From:** Justin, with a Cowork session, Nov 8, 2026
**Run after:** the Nov 9 ASU chart email has gone out. Do not run it before then.

## Changelog

- v1.0 (Nov 8, 2026): first version.

---

## Why this exists

Every Nodes and Networks chart fix travels a long chain:

Justin + Claude → branch → `main` → Cloudflare → Drive `embed-codes.md` → Carrie → ticket → ASU designer → cronkite.asu.edu

Every link in it has broken at least once:

- Fixes sat on a branch and never went live (Nov 3).
- The Drive `embed-codes.md` fell behind the repo (it's behind right now).
- Heights live in four places: `qa/embed-codes-asu.md`, `qa/embed-codes.md`, `qa/handoff-fig1-2026-11-05/embed-codes.md` and `qa/asu-chart-final-2026-11-09/ASU-TICKET.md`.
- A session made changes nobody asked for, so Carrie had to proofread everything again.

The main weakness is that ASU hard-codes each chart's height. So any change on our side that alters a height needs a ticket on theirs. ASU has no web team; changes go through tickets to a shared designer.

**What this brief builds:**

- one heights file;
- a generator that makes every hand-off file from it;
- a live check;
- a written "fit inside the box" rule.

Once these exist, most future chart fixes need nothing from ASU.

## Hard rules

1. **Change no chart content.** Don't edit anything under `preview/nn-launch-kit/figures/`, `preview/nn-launch-kit/explorer/` or `assets/nn5/`. This brief only adds tooling and docs. If you think a figure needs a change, list it in the report and stop.
2. **Move or rename no live URL.**
3. **No git writes.** Justin commits and pushes through GitHub Desktop only. Leave everything uncommitted and list it.
4. **Outside the repo, touch nothing.** No Drive, no email, no Cloudflare settings.
5. **Write only these new files:** `qa/launch-kit/heights.json`, `scripts/nn_embed_build.py`, `scripts/nn_embed_verify.js`, `qa/launch-kit/out/*`, `qa/launch-kit/CHANGE-ROUND-TEMPLATE.md`. Append to `qa/launch-kit/CHANGELOG-internal.md` and `qa/launch-kit/NN-LAUNCH-MANIFEST.md`. Anything else, ask first.
6. If two sources disagree (for example the ticket and `embed-codes-asu.md`), stop and ask. Don't pick one.

## Established facts (checked Nov 8, 2026)

- `main` = `origin/main` = `b446c8e`, the merge of PR #12 (`nn/asu-chart-final`, last commit `125fa22`, Nov 7 at 8:21 PM ET).
- Uncommitted: `qa/launch-kit/CHANGELOG-internal.md` (one new line) and the untracked `qa/asu-chart-final-2026-11-09/ASU-TICKET.md`.
- Checked live on Nov 8. None of the five figures (timeline, map, defector, threshold, bands) shows "Data table", the "by Justin Bank" credit or "Split by cohort".
- `ASU-TICKET.md` is the newest height set: desktop heights 1021 / 786 / 541 / 993 / 428 and a CSS block with breakpoints at under 390, 390, 576, 768, 992 and 1260 px. 1260 applies to the defector only. Each height is the content height plus 16 px.
- ASU embeds five iframes, all at `/preview/nn-launch-kit/figures/{timeline,map,defector,threshold,bands}/`, as read from the live page on Nov 6. The content column is 700 px from 992 px up, 552 at 768, 476 at 576, and the window minus 64 px below that. The defector sits in an accordion and is 57 px narrower below 992.
- Figure pages post their content height as `{type:"nn:resize", height}` via `postMessage`. Since Nov 6 that is a `getBoundingClientRect` height, so it can shrink.
- The figure pages force `?theme=asu` (light, Arial, maroon). The live chain is: Cloudflare Pages builds `main` through `build-dist.sh` into `dist/`.
- Cloudflare blocks curl from sandboxes. A real browser (Playwright/Chromium on this Mac) works.

## Assumptions to verify in Step 0

- Playwright plus Chromium can run on this Mac (`node -e "require('playwright')"`). If they can't, report it and propose an install. Don't install without asking.
- Whether Cloudflare serves the figure HTML byte-for-byte as committed, or rewrites it. This decides whether "live matches `main`" can be a hash check or has to be a content check.
- The defector's widths at 992–1259 and at 1260 and up. The ticket implies two different widths; measure them.
- Whether each figure page's own background fills the iframe, so a small gap below the content blends into ASU's white page.

---

## Step 0: verify (read-only)

1. `git status` and `git log --oneline -5`. Confirm the facts above.
2. Check the Playwright assumption.
3. Load each of the five live figure URLs at each column width. Record the reported `nn:resize` height and compare it with the ticket's numbers minus 16.
4. Check the defector widths, the background, and the hash-vs-content question.

**Stop and report**, with a table: figure × width → live content height, ticket height, difference.

## Step 1: one heights file

Create `qa/launch-kit/heights.json` as the single source. Seed it from `ASU-TICKET.md`. For each figure:

- `id`, the paper's figure number, `url`, `title`, iframe `class` and `max-width`;
- `heights`, keyed by breakpoint (`base`, `390`, `576`, `768`, `992`, plus `1260` for the defector);
- the column width each breakpoint is measured at.

Top-level fields:

- `contract_version` (start at `1`);
- `status`: `"proposed"` until Justin marks it `"applied"`, once Carrie confirms ASU applied the ticket;
- `source_commit`;
- `updated`.

**Stop and report.**

## Step 2: generator

Write `scripts/nn_embed_build.py`. Standard library only, and it runs as `--dry-run` by default. It reads `heights.json` and writes into `qa/launch-kit/out/`:

- `embed-codes.md`: the Carrie-facing file. It uses the same wording and layout as the current Drive version (the section in `qa/embed-codes-asu.md`), and opens with a stamp: `Chart update #N · <date> · commit <short hash> · contract v<N>`.
- `ASU-TICKET.md`: the same layout as today's ticket.
- `CHANGES.md`: a plain-English diff against the previous export. It says which figures and which heights changed, or "no height changes."

Run it once and confirm that its `ASU-TICKET.md` matches today's ticket line for line, apart from the stamp. If anything else differs, stop.

Mark the four old height files as superseded, with a one-line note at the top of each that points at `heights.json`. Don't delete them.

**Stop and report.**

## Step 3: live check

Write `scripts/nn_embed_verify.js` (Playwright). It does two things.

**Deploy check:**

- Run `git fetch` (read-only).
- Confirm `HEAD` is on `origin/main`.
- Confirm each live figure page matches the `origin/main` copy, using the method chosen in Step 0.
- Print `LIVE = MAIN` or `LIVE ≠ MAIN` for each figure.

**Fit check:** load each live figure at each contract width and catch its `nn:resize` height. Compare it with `heights.json` and grade it:

- `PASS`: content + 16 ≤ contract, and the leftover gap is 40 px or less.
- `GAP`: it fits, but leaves more than 40 px. This is a warning: it's visible white space.
- `TOO TALL`: content + 16 > contract. This fails, because ASU would cut the chart off.

The script exits non-zero on any `TOO TALL` or `LIVE ≠ MAIN`. Save a one-page report to `qa/launch-kit/out/VERIFY-<date>.md`.

**Stop and report**, with the first real run's output.

## Step 4: written rules and the change-round template

1. Add a **"Height contract"** section near the top of `NN-LAUNCH-MANIFEST.md`:
   - Once `status` is `applied`, ASU's heights are frozen.
   - Any chart change has to pass `nn_embed_verify.js` before anyone tells Carrie it's live.
   - A change that would make a chart `TOO TALL` is out of scope until after launch, unless Justin approves a new contract version and a ticket.
2. Create `qa/launch-kit/CHANGE-ROUND-TEMPLATE.md` for one round of client fixes:
   - a numbered list of the client's items, word for word;
   - for each item: the file touched, before/after screenshots at 436 and 700 px, and the verify result;
   - a scope fence: "Changed only the items above. Nothing else."
   - the stamp of the export that went to the client.
3. Add a "before you tell Carrie it's live" checklist to the manifest:
   - the commit is on `origin/main`;
   - `nn_embed_verify.js` passes;
   - the generator has been re-run;
   - Justin has replaced the Drive file (the old one goes to Drive Trash);
   - one email with one numbered update.

**Stop and report.**

## Final report

- What you changed, where it lives, and how to undo it.
- The list of uncommitted files for Justin to commit in GitHub Desktop, with a suggested commit message.
- Anything you noticed but didn't do.
- Add one line to `CHANGELOG-internal.md`.

## Not in scope

- Launch-day reverts (`4a6ec58`, `5c7184c`).
- Re-cutting the launch videos.
- The release zip.
- The explorer.
- Any figure content or design change.
- The Drive upload (Justin does it).
