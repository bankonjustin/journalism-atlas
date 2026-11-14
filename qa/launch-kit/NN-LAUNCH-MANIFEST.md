# Nodes and Networks: launch manifest

Read this before you touch the repo, the Drive handoff folder, or anything Carrie will see. It says what is live, who it is for, and what you may not do without asking. If anything here is wrong or stale, say so and stop. Don't work around it.

Last updated: Nov 3, 2026, 8:10 PM ET, by Justin (with a Cowork session).

## What we're shipping

The Knight Center for the Future of News at ASU is publishing *Nodes and Networks: Understanding How American Journalism Is Reorganizing in Real Time*, written by Justin Bank. The Knight Center page is going live around Wed/Thu, Nov 4–5. ASU's page embeds charts and the explorer, which we host on journalismatlas.com.

Our job right now is narrow: give Carrie a clean, correct set of embed codes that point at pages showing the current data. Nothing else.

## People

- **Justin Bank:** author and owner of this work. He is the only person who pushes to GitHub, and he does it through GitHub Desktop.
- **Andy Pergam:** Executive Director of the Knight Center and the paper's editor. He has the final call on editorial questions and wants minimal change at this stage.
- **Carrie Simmons:** the Knight Center's communications specialist. She builds and publishes the Knight Center page and works from the Drive handoff folder. Treat anything she reports as a bug report from the client.
- **Brian Cleveland:** copy editor.
- **ASU's designer:** wires our embeds into the Knight Center page. We don't talk to them directly.

## The two repos

- **`journalism-atlas`** (public) deploys to journalismatlas.com through Cloudflare when Justin pushes. The launch kit and the interactive edition both live here.
- **Branches in `journalism-atlas`:** only `main` deploys. The `nn-launch` branch was merged into `main` on Nov 3. Before you tell anyone a change is live, confirm its commit is on `origin/main`.
- **`journalism-atlas-private`** holds the Atlas database and the Vertical Natives work. It is **not** the launch kit. Brief v5 pointed here by mistake.

### Deploy facts

- Cloudflare Pages builds `main` of `bankonjustin/journalism-atlas`. A push usually goes live within about 5 minutes.
- `build-dist.sh` builds into `dist/`. It copies every `preview/**/index.html` (figures, explorer, embed-test, edition embeds), the files `preview/nn-launch-kit/media/teaser*`, and the kaleidoscope's `still.png`.
- `_headers` sets `noindex, nofollow` on `/preview/nn-launch-kit/*` and on the edition. It sets `frame-ancestors 'self' https://asu.edu https://*.asu.edu https://journalismatlas.com` on the launch-kit `figures/*` and `explorer/*`. Edition `embed/*` pages allow framing from anywhere (`frame-ancestors *`).
- Cloudflare blocks curl and the sandbox proxies. Verify from a real browser, such as the Cowork built-in browser running `fetch()` on the page.

## Live addresses: do not move, rename or delete

ASU may have embedded any of these. Until Carrie confirms which URLs are in the Knight Center page, treat all of them as load-bearing.

- **Explorer embed:** `journalismatlas.com/preview/nn-launch-kit/explorer/`. Justin's notes say ASU embeds this one.
- **The 7 launch-kit figures:** `journalismatlas.com/preview/nn-launch-kit/figures/{scale,timeline,map,defector,threshold,bands,kaleidoscope}/`. These are the URLs in the Drive `embed-codes.md`. **They show current (Path 2) data, verified live on Nov 3.**
- **Edition figures:** `journalismatlas.com/preview/nodes-and-networks-edition-e852c5c5/embed/fig-0` through `fig-6`. `_headers` says ASU's designer embeds these. **As of Nov 3, 6:25 PM ET, `fig-2-map`, `fig-4-threshold`, `fig-5-bands` and `fig-6-kaleidoscope` show current (Path 2) data**, verified live. They were rebuilt in place from the launch-kit copies and keep their own URL, credit line and default theme (they don't force the ASU look). So whichever set ASU embedded, the numbers are now right. `fig-0`, `fig-1` and `fig-3` had no stale numbers.
- **Test page:** `journalismatlas.com/preview/nn-launch-kit/embed-test/figures/` frames all 7 launch-kit figures with the exact `embed-codes.md` snippets. The older `embed-test/` page frames only the explorer.

**Confirmed ASU embeds (read from cronkite.asu.edu/knightcenter/nodes-networks, Nov 6, 2026):** five iframes, all launch-kit URLs: `/preview/nn-launch-kit/figures/{timeline,map,defector,threshold,bands}/`. No `edition-e852c5c5/embed/` URLs. The explorer is not embedded; two "Explore the data" buttons link to `/preview/nn-launch-kit/explorer/` with `embed=1&tab=ways` (to be changed to `?tab=ways`, no `embed=1`, by Carrie). ASU's content column is 700 px from 992 px windows up, 552 px at 768, 476 px at 576, window minus 64 px below that; the Defector (in an accordion) is 57 px narrower below 992 px. The page runs 10 inline scripts and has no `nn:resize` listener. ASU iframe heights before the Nov 6 update: 1471 / 1050 / 600 / 1145 / 600; they have since added `title` attributes. Details: `qa/asu-embed-kit-2026-11-06.md`.

**The Nov 5 launch-day gate is void** (launch slipped to early the week of Nov 9; the new date is Justin's call). The reverts of `4a6ec58` (strip) and `5c7184c` (hub card) wait for Justin; both are still on `main`, unreverted.

## Figure numbering: check it before you trust it

The paper numbers its figures 1–5. The edition embed pages are numbered `fig-0` to `fig-6`. The launch kit has 7 figures: Figure 0 (scale), 1–5, and the kaleidoscope. When someone says "Figure 2", confirm which page they mean by its URL and title before editing anything.

The paper's figures (per brief v4):

1. Funding and organization timeline, 2018–2026
2. The nine cohorts
3. Defector revenue, Years 1–5
4. Share of revenue from grants and donations, nonprofit newsrooms with $3.5M–$10M in revenue. **Title confirmed final on Nov 3: "nonprofit newsrooms".** Brief v5's "must NOT contain 'nonprofit newsrooms'" check is out of date.
5. Revenue band distribution by cohort

## Data state

The data was locked at 169 organizations (v22). On Nov 2, Justin reopened it for a minimal correction pass ("Path 2"). Path 2 did four things:

- Moved the Baltimore Banner from C1 to C4.
- Firmed up labels and data.
- Recomputed any figure that the corrections made stale.
- Disclosed the remaining edge cases in the methods section instead of rebuilding.

Any figure that counts organizations by cohort or by band can go stale after a Path 2 change. Regenerate figures from the current dataset. Never copy a number from this file, an old brief or memory into a chart.

## The Drive handoff folder

The folder is `nn-launch-assets-2026-11-02` (Drive ID `1xaO-JtSB57__wiGzoW0oVh-zzSlluF6l`). Carrie works from it. It holds:

- `embed-codes.md`
- `links.txt`
- `README.txt`
- `methodology-nodes-and-networks.docx` and `.md`
- `teaser/`
- `charts/` (`chart-0-scale.png` through `chart-6-kaleidoscope.png`, each 1200 px wide)

Rules for the folder:

- Every URL in `embed-codes.md` must load in a real browser and show the current data.
- The Drive connector can't overwrite files. Upload the new version, move the old one to Trash so it can be restored, and say which files you replaced.
- `launch-video/` is held out. It lives in `nn-launch-HOLD (not in Carrie's folder)` (ID `1oU8Zx0JBmk1f_sj_3AybFPZPTvEepzXu`) because the videos still say "18 of 18" at 8–12 s and need re-cutting.
- Internal fix logs go in the repo, at `journalism-atlas/qa/launch-kit/CHANGELOG-internal.md`. They never go in Carrie's files.

## Rules for any session

1. Do the task you were given. If you see other cleanup worth doing, list it at the end and ask. Don't do it.
2. Ask before editing any shared file, such as `assets/nn5/nn-theme.css`. A change there reaches every page that loads it, including pages ASU may embed.
3. Never move or rename a live address. If a page needs to change, change it in place.
4. Verify from a real browser. "curl returns nothing" doesn't mean the page is missing.
5. Never commit a file that contains `<<<<<<<` conflict markers.
6. When you finish, report three things: what you changed, where it lives, and how to undo it.
7. If two sources disagree, for example a brief and `_headers`, stop and ask Justin. Don't pick one.

## Who owns what

- **The explorer** belongs to a separate session. Don't edit it here. It has its own colors and doesn't load the theme file.
- **The theme file and the figure pages** can be changed by this kit only with Justin's sign-off.

## Current state (Nov 3, evening)

- The maroon theme swap (`#8C1D40` for group b, cache key `asu2`) is committed and live, kept on purpose to match ASU colors. It is in `nn-theme.css`, which the edition embed pages also load. The explorer may still show the old pink, so its owner needs to match it.
- Carrie's bug (Figures 2 and 4 showed old data) is fixed both ways. The Drive handoff points at the current launch-kit URLs, and the edition pages she may have wired now show current data too. The note to Carrie asking for her exact URLs is still worth sending.
- Waiting on Carrie for the exact URLs in the Knight Center page.

## Open items (not done; ask before doing)

- **Figure 1 (timeline) cohort names.** The launch-kit and edition copies still use two old cohort names in the event tags: "C4 Philanthropic Networks" and "C5 Public Media". Only names are affected, no numbers. The fix is a find-and-replace to "Philanthropic Mesh Networks" and "Public Media Networks". Awaiting Justin's OK.
- **Launch day:** the Nov 5 gate is void. Revert `4a6ec58` (strip) and `5c7184c` (hub card) when Justin sets the new launch date (early week of Nov 9).
- **Test page height.** The test page `embed-test/figures/` still frames Figure 2 at 1062 rather than 1008. Its resize script corrects this on load, but the page should be brought into line with embed-codes.md.
- **Kaleidoscope contrast.** The kaleidoscope's maroon marks sit on a stage that is always black, at about 1.6:1 contrast.
- **Kaleidoscope false positive.** The kaleidoscope pages keep the old cohort names inside the byte-identical `nodes169` data block, and a small script renames them on load. That's by design, so a text search for old names flags these pages even though they display correctly.
- **Launch videos.** They need re-cutting at 8–12 s ("18 of 18" headline, Banner in C1). The GIFs, posters and `social-r1` set are stale too.
- **Release zip.** Replace v22 with a v22.5 export.
- **`COPY_EXPORT.md`.** Several lines say "Under $10M" without "in latest year".
- **St. Louis Public Radio.** The threshold question is unresolved.
- **Private repo branch.** `chore/vertical-natives-housekeeping` is now redundant because its work is on `main`. Delete it only on Justin's say-so.
- **`.DS_Store`.** A stray one sits in Carrie's Drive folder. It's harmless.

## Change log

Add one line per session: the date, what changed, and how to undo it.

- 2026-11-03: Resolved the VEIN-LEDGER conflict in `journalism-atlas-private` (the chore branch's "spidering" commit brought onto `main`, then today's Vertical Natives work committed). Undo: revert `4217893` and `7dabac3`.
- 2026-11-03: Maroon swap committed (`b917faa`; revert to undo). 7-figure test page added (`9393cac`). Internal changelog added (`a22e59b`). Old October `dist/` stash deleted.
- 2026-11-03: Drive handoff files replaced (`embed-codes.md` split from the internal logs; `links.txt`; `README.txt`; all 7 PNGs). The old versions are in Drive Trash.
- 2026-11-03: Fig 4 title restored to "nonprofit newsrooms" (`3b613e6`; revert to undo). New `embed-codes.md` and `chart-4-threshold.png` uploaded; previous ones in Trash. `launch-video/` moved to the HOLD folder. README replaced; old one in Trash. Note to Carrie drafted.
- 2026-11-03: Edition `embed/fig-2-map`, `fig-4-threshold`, `fig-5-bands` and `fig-6-kaleidoscope` brought to Path 2 data in place (`eff7721`; `git revert eff7721` to undo). The kaleidoscope's fallback image now points at `/preview/nn-launch-kit/figures/kaleidoscope/still.png`. Verified live at 6:25 PM ET.
- 2026-11-03: Timeline cohort tags renamed in the kit and edition copies (`be3af46`; revert to undo).
- 2026-11-03: Found that the 2:49 PM ASU fixes (`1ea377e`: Fig 2 profile links hidden in the ASU look, Fig 2 height 1008/1201; Fig 4 "80% or more" caption; dark-mode pink on Figs 2 and 5) had been committed to the `nn-launch` branch, so they never went live. Merged all of `nn-launch` into `main` on Justin's call (`e42f2f6`; `git revert -m 1 e42f2f6` to undo). Conflicts resolved by keeping `asu2`, the "nonprofit newsrooms" title and the timeline names, and taking nn-launch's Fig 4 wording and dark-mode pink. Noindex is now off `/nodes-and-networks/` (kept on purpose).
- 2026-11-03: Held two launch-flip changes until launch day: the strip went back to Watershed (`4a6ec58`) and the hub's N&N record went back to placeholder (`5c7184c`). **On launch day, revert both** to show the N&N strip and hub card. The for-brands line is already gated by `nn-gate.js`.
- 2026-11-03: Pushed and verified live at 8:05 PM ET. Drive `embed-codes.md` (Fig 2 height 1008/1201; Fig 4 alt text), `chart-2-map.png` and `chart-4-threshold.png` replaced; old versions in Trash. Reply sent to Carrie on the "Explorer, embed and video for Monday" thread (Andy cc'd) with the Fig 2 and Fig 4 embed codes, asking for her exact URLs.
- 2026-11-06: ASU preview fixes (pushed as `0838969`; revert it to undo the figure changes). Figure 1: cohort tags and the "Cohorts tagged" column removed, light only, height now posted as content height. Figure 2: rebuilt in place as a static 3x3 grid. Figures 3, 4, 5: pinned to light. Drive `embed-codes.md` replaced (Option A script, Option B CSS, titles, explorer URL without `embed=1`); old version in Drive Trash. New `chart-1-timeline.png` and `chart-2-map.png` are in `qa/asu-preview-fixes-2026-11-06/drive-upload/`, not yet in Drive. Note: the manifest lives in `~/Downloads`, not in either repo.
- 2026-11-12: Launch-day flip (local commit, not pushed until Justin pushes). Strip back to N&N (`4a6ec58` reversed by hand into the commit); hub: N&N featured and live with date 2026-11-12, partner Knight Center for the Future of News at ASU, author Justin Bank, Watershed unfeatured; "Nov 5" to "Nov 12" on the homepage card and About lead; `report_url` set to https://cronkite.asu.edu/knightcenter/nodes-networks and `nn/built/` rebuilt (it was stale vs source: includes maroon swap and history thumbnail). `nn-gate.js` untouched (gate has been on since Nov 5 10 AM ET). Undo: `git revert <this commit>`.
- 2026-11-12: Social round 2, Phase 1 built in `nn/media/social-r2/` (git-ignored, local only; harness, turn loop, ceiling chart, six-ways carousel, turn video v2). Nothing live changed; `.gitignore` gained one line. Undo: delete `nn/media/social-r2/` and revert the `.gitignore` line.
- 2026-11-12: Social round 2, Phase 2 built in `nn/media/social-r2/phase2/` (born by decade, explorer walkthrough, sticker kit, stitch and quote templates; 2.1 on hold) plus `social-r2/PHASE3-FEASIBILITY.md`. Local only, nothing live changed. Undo: delete `nn/media/social-r2/phase2/`.
