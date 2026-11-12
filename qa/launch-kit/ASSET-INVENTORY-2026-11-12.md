# Nodes and Networks: asset inventory, Nov 12, 2026

Read-only discovery (Part B of NN-LAUNCH-FLIP-AND-ASSET-DISCOVERY-BRIEF-v1.0). Repo: `~/Developer/atlas/journalism-atlas`. Outside the repo I listed names, sizes, dates and durations only, with one exception: Justin asked for the reels' end cards, so I pulled the last frame of four reel files (read-only, written to the scratchpad, nothing copied or moved).

Contact sheets (`fps=1/2.5,scale=360:-1,tile=5x4`) for every non-superseded repo video are in
`/private/tmp/claude-502/-Users-bankids--claude-spares-spare-vww99F/e9b5cb87-6efb-474e-94a4-43de7c80b4ee/scratchpad/sheets/` (one PNG per video, named by repo path with `__` for `/`). Frames at 8/10/12 s and reel last frames are in `.../scratchpad/cs/`.

**How far I checked.** I looked at pixels for: governance loops (8/10/12 s + sheet), launch 1x1 turn (sheet), teaser (sheet), a2 4x5 loop (sheet), every social end card (last frames), four reels (last frames). Everything else is judged from the ledgers, manifests and file dates, and is marked "not eyeballed". There is no OCR on this Mac, so "no stale tell" means none visible to me in the frames I viewed.

## Two facts that change what you can post today

1. **Almost none of the social video is on journalismatlas.com.** `nn/media/launch/` and `nn/media/social-r1/` are git-ignored (`.gitignore:25`, `:31`). A live HEAD request for `/nodes-and-networks/media/launch/nn-launch-1x1-turn.mp4` and for `/nodes-and-networks/media/social-r1/a2/...` returns the site's catch-all HTML. The governance loops (tracked in git) are also not deployed, because `build-dist.sh` only copies `teaser*`. These files exist only on this Mac, in the Desktop and Downloads zips, and in Drive. Back them up.
2. **The site returns 200 with the homepage for any unknown path** (see "Permanent explorer route"). That means a mistyped media URL looks like it works. Check `content-type`, not status.

---

## 1. Ready today

Clean of stale tells I could see, current (Path 2, Nov 2 "v22.5") data, safe to post.

| Asset | Path | Good for |
|---|---|---|
| **Launch "turn" video, 1:1**, 38 s, 1080x1080, Nov 2. Shows "17 of 17 legacy publishers… 0 of 34 co-ops and civic" (the Path 2 numbers), hover cards name organizations (allowed per Nov 1 ruling), end card credits Justin Bank / Knight Center, no URL. | `nn/media/launch/nn-launch-1x1-turn.mp4` (+ `.srt`, `-poster.png`) | LinkedIn and Bluesky feed. Put the Knight Center link in the post text. |
| **Launch "turn" video, 16:9**, 38 s, 1920x1080, Nov 2 (same render; sheet generated, not eyeballed) | `nn/media/launch/nn-launch-16x9-turn.mp4` (+ `.srt`, poster) | LinkedIn, Bluesky, Leaflet |
| **Launch "turn" video, 9:16**, 38 s, 1080x1920, Nov 2 (same render; not eyeballed) | `nn/media/launch/nn-launch-9x16-turn.mp4` (+ `.srt`, poster) | Vertical (Reels, Shorts, Stories) |
| **Launch GIFs**, 720x720: "30 grew" 7.4 s, "cohorts" 4.4 s. Not eyeballed; the files are Oct 30 and the clips are dated by name. Check the "cohorts" one first (it is the cohort-name one). | `nn/media/launch/gifs/` | Bluesky, LinkedIn |
| **Teaser**, 10.47 s, 1200x960, Nov 2, plus `@2x` (2400x1920), poster JPG and 800x640 GIF. Counts shown are current (30 grew / 25 started above), no URL, no names. | `preview/nn-launch-kit/media/teaser.mp4`, `teaser@2x.mp4`, `teaser-poster.jpg`, `teaser.gif` | LinkedIn, Bluesky, Leaflet. **This is the only teaser that is also live on the site** (HEAD 200 `video/mp4`). |
| **Social loops, no end card** (a1 Sollenberger/TBPN squares 7 s; a2 band dots 5.5 s; a3 bars 11 s; a4 Defector 9 s; a7 Muck Rack 5 s), 16:9 / 4:5 / 1:1 / 9:16. a2, a3 and a6 were re-rendered Nov 2 from the Path 2 constants; a1, a4 and a7 are Oct 30 renders that don't depend on cohort counts. a2 4x5 looked right in the sheet (17 legacy dots; see the label caveat below). a1, a3, a4, a7 not eyeballed. | `nn/media/social-r1/a{1,2,3,4,7}/nn-social-r1-aN-{ratio}-loop.mp4` | Vertical (9:16), LinkedIn (4:5, 1:1), Bluesky (1:1, 16:9) |
| **a6 radial map**, 4 s, 169 white marks, 55 turn gold; "-atlas" variants end on the Atlas card ("Explore the cohorts.", no URL). Re-rendered Nov 2. Last frames viewed; body not eyeballed. | `nn/media/social-r1/a6/nn-social-r1-a6-{ratio}-atlas.mp4` and `-close-atlas.mp4` (2 s) | Vertical, Leaflet |
| **Atlas end-card variants** (`*-end-atlas.mp4`): end card is the Atlas logo + "Explore the cohorts." + source line, no URL, no placeholder. Viewed for a1, a2, a3, a4, a6, a7. | `nn/media/social-r1/aN/*-end-atlas.mp4` | Anywhere you'll put the link in the post |
| **Carousel**, 10 slides + PDF + 18 singles, 1080x1350 / 1080x1080. C1 and C4 cards and the PDF were rebuilt Nov 2 (PDF dated Nov 2 21:55). Not eyeballed. | `nn/media/social-r1/a5/` (`carousel/`, `singles/`, `nn-social-r1-a5-carousel.pdf`) | LinkedIn (document post), Bluesky (images), Leaflet |
| **Kaleidoscope still**, 1204x1350, Nov 2 | `preview/nn-launch-kit/figures/kaleidoscope/still.png` | Any |
| **Share image for the N&N page**, 1200x630, Nov 1, title and tagline only (per its alt text) | `nn/media/og/landing.png` (live at `/nodes-and-networks/media/og/landing.png`, 200 `image/png`, 92 KB) | Link previews |

Teaser question ("which is the most produced"): the Nov 2 `teaser.mp4` is the current, production one. The Oct 30 cuts in `qa/teaser/out/` and `qa/teaser/out_timeline/` (1280x720 and 1080x1080, 9.47 s, plus GIFs) are earlier, plainer takes. I can't judge "jazzier" from stills; watch the Nov 2 teaser first, then `qa/teaser/out_timeline/teaser_square.mp4`.

---

## 2. Needs a fix first

| Asset | Problem | Smallest fix |
|---|---|---|
| **Governance loop 4:5 and 9:16** (24 s; 1080x1350 and 1080x1920; Oct 28). `preview/nn-launch-kit/video/nodes-networks-governance-{4x5,9x16}.mp4` | A boxed **"[REPORT URL: PLACEHOLDER]"** is burned in on every frame. At 8, 10 and 12 s the frame is the settled cohort map; I did **not** see "18 of 18" there. The legend reads Under $10M (114) / Started above (25) / Grew past (30). I can't tell from stills whether the Banner is in C1. This is **not** a post-Nov 3 render (Oct 28). | Re-render without the footer or with the real URL, and confirm the Banner is in C4. Or skip it: the Nov 2 turn videos cover the same ground. |
| **ASU end-card variants**: every `*-end-asu.mp4`, a6 `*-asu.mp4` and `*-close-asu.mp4`, and (outside the repo) the same files in the Desktop kits | End card shows **"LOGO PLACEHOLDER"** and **"[URL PLACEHOLDER]"** inside dashed boxes. Viewed for a1, a2, a3, a4, a6, a7. | Use the loop or `-atlas` variant, or re-render the end card with the ASU logo and the Knight Center URL. |
| **Reels, long**: `~/Downloads/nn-reel-long-feed-v3.mp4` and `-v3_1.mp4` (identical file, md5 `b1cb35b8…`), 47.7 s, 1080x1350, Oct 24 | End card shows **`cronkite.asu.edu/knightcenter`** with an arrow: the Knight Center root, not the report page (`cronkite.asu.edu/knightcenter/nodes-networks`). It is a real, working address. The placeholder (`ASU.com`) is gone. I did not check the middle of the reel for stale counts or the Banner. | Decide whether the root address is acceptable; otherwise re-render the end card. Check mid-reel counts before posting. |
| **Reels, short**: `~/Downloads/nn-reel-short-feed-v3.mp4`, `-v3_1.mp4`, `-v3_2.mp4` (all one file, md5 `4530d93e…`), 26.4 s, 1080x1350, Oct 24 | Same end card as the long reel. Same caveat. | Same. |
| **Reels, v1**: `nn-reel-long-feed.mp4` (30.0 s) and `nn-reel-short-feed.mp4` (15.0 s), Oct 24 | End card says `journalismatlas.com/research/nodes-and-networks` (works: 301 to `/nodes-and-networks/`), but the text is **garbled** ("Â·" and "$3.5Mâ€"$10M"). Headline on the short one is "Governance determines so much." | Don't post. Superseded by v3. |
| **`nn-reel-*-v2.mp4`** | **Not found by that name** on the Mac or in the repo. The Downloads set is unversioned (v1), `v3`, `v3_1`, `v3_2`. v3/v3_1/v3_2 are byte-identical copies, so "v2" may be what you call one of them. | Tell me which file you mean; I won't guess. |
| **a2 row labels** | In the a2 band-dot loop the cohort rows read "Philanthropic Networks" and "Public Media" (no C-codes). The current names are "Philanthropic Mesh Networks" and "Public Media Networks". The brief lists "C4 Philanthropic Networks" and "C5 Public Media" as stale tells; this is the same wording without the codes. Counts look current. | Your call: short labels may be deliberate. If not, re-render a2 with the current names. |
| **Edition pages still say "18 of 18"** | `preview/nodes-and-networks-edition-e852c5c5/index.html:179` ("Legacy: 18 of 18 above $10M"), `.../explorer/index.html:22`, `preview/nodes-and-networks-f348eb08/index.html:365` (two figure descriptions). Path 2 made it 17 of 17. These are noindex edition pages, but they are live. | Edit in place (not under `embed/`). I did not touch them. |
| **Fig 0 "Two numbers": Sollenberger/Epstein claim has no citation** | Neither figure page (`preview/nn-launch-kit/figures/scale/`, `edition/embed/fig-0-scale/`) nor the edition prose (`edition/index.html`) links to a source. The prose says Sollenberger "placed the president inside the redacted portions of the Epstein files" and that NPR confirmed it nine days later. The figure says "$8,800 … as of this writing"; the social ledger has 8,910 as of Oct 30. | Add a source line or link for the claim, and update or date the dollar figure. Not edited (the `embed/` copy is ASU-embedded territory). |
| **Chapter share images** | `nn/media/og/chapter1-3.png` are dated Nov 1, a day before Path 2. Not eyeballed. | Open each and check for cohort counts. |
| **Soft-404** | Unknown URLs return 200 + homepage. | See cleanup list. |

---

## 3. Everything else

Status: live / parked / superseded / orphaned.

### Video

| Asset | Path | Date | Status |
|---|---|---|---|
| Main film 16:9, 52 s, 1920x1080 | `nn/media/nodes-networks-16x9.mp4` (live HEAD 200, 13.8 MB) | Nov 2 | live (landing page) |
| Main film 9:16, 52 s, 1080x1920 | `nn/media/nodes-networks-9x16.mp4` | Nov 2 | parked (not served; `dist/` only) |
| Poster, "in short" still | `nn/media/nodes-networks-poster.jpg` (1280x720), `nodes-networks-in-short.png` (1080x1350) | Nov 2 / Nov 1 | live (landing page) |
| Launch turn videos, first cut (18 of 18) | `nn/media/launch/superseded/`, `superseded-2026-11-02/` (16x9, 1x1, 9x16 turn; 1x1 non-turn) | Oct 29–30 | superseded |
| Social loops, first cut | `nn/media/social-r1/superseded-2026-11-02/` (a2, a3, a6 and posters/QA) | Oct 30 | superseded |
| Teaser, first cut | `preview/nn-launch-kit/media/superseded-2026-11-02/` (mp4, @2x, poster) | Nov 2 | superseded |
| Teaser, early takes | `qa/teaser/out/`, `qa/teaser/out_timeline/` (mp4 1280x720 + square 1080, webm, GIF 800x450 / 1260 KB) | Oct 30 | parked |
| Governance loops 4:5 / 9:16 | `preview/nn-launch-kit/video/` | Oct 28 | parked (placeholder URL, see section 2) |
| Governance loop still | `preview/nn-launch-kit/nodes-networks-governance-4x5-still.png` (1080x1350) | Oct 28 | parked |
| Explorer screen recordings (webm): `gov-ways-history-gov_{radial,timeline}_{390,1200}`, 10.7 s | `qa/explorer/` | Oct 30 | parked (QA captures; 390-wide are vertical) |
| History recordings (webm): `turn-390/1200` 17.4 s, `radial/settle` 12–14 s | `qa/history-final/`, `qa/history-ab/` | Oct 31–Nov 2 | parked (QA captures) |
| ~75 more social-r1 files: `-end-asu`, `-end-atlas`, posters (PNG), 720 GIFs (a1, a2, a3, a4, a7; a2 GIF is 720x720, 5.3 s), QA check PNGs | `nn/media/social-r1/` | Oct 30–Nov 2 | live (local only); GIFs for a1, a4, a7 are Oct 30 renders; a2/a3 GIFs not date-checked |
| Full social manifest and ledgers | `nn/media/social-r1/manifest.md`, `manifest.csv`, `LEDGER.md`, `constants.json`, `constants_v22_5.json`, `PHASE0_REPORT.md`, `ORIGIN_DIFF_REPORT.md`, `CLAUDE-CODE-BRIEF-social-refresh-v22-5-2026-11-02.md` | Oct 30–Nov 2 | live (internal) |
| `dist/` and `nn/_out/` | duplicates of the above, plus `dist/…/launch/superseded` | Oct 30 builds | orphaned build output (git-ignored) |

### Zips, outside the repo (listing only)

| File | Date | Contents | Status |
|---|---|---|---|
| `~/Downloads/nn-social-v22-5-2026-11-02.zip` (125 MB) | **Nov 2, 22:46** | 141 entries: a1–a7, a5 carousel + PDF, a6 (24 files), `launch-gifs/` | **newest; has the Path 2 recut of a2, a3, a6 and a5** |
| `~/Desktop/nn-social-r1-full.zip` (129 MB) | Oct 30, 09:59 | 175 entries: same families plus 39 QA files | superseded by the Nov 2 zip |
| `~/Desktop/nn-social-r1-carrie-kit.zip` (81 MB) | Oct 30, 09:59 | 99 entries: deliverables only, no QA | superseded; **the "newer" question: neither Desktop zip is newer than the other (same minute); the Downloads v22-5 zip is newer than both** |
| `~/Desktop/nn-social-r1-carrie-kit/` and `~/Desktop/social-r1/` (expanded) | Oct 30 | expanded copies of the Oct 30 kit | superseded |
| `~/Downloads/nn-for-carrie-2026-11-02{,b,c}.zip`, `nn-launch-assets-2026-11-02.zip`, `nn-for-andy-2026-11-02.zip`, `nn-asu-review-2026-11-02.zip` | Nov 2 | Carrie / Andy handoffs | not opened (per rule); presumably the Drive handoff |

### Documents and data

| Asset | Path | Date | Status |
|---|---|---|---|
| COPY_EXPORT.md | `preview/nn-launch-kit/COPY_EXPORT.md` | Nov 2 | live (internal); manifest says some "Under $10M" lines need "in latest year" |
| EMBED.md | `preview/nn-launch-kit/EMBED.md` | — | live (internal) |
| PROOF-SHEET.md | **not found** in the repo or by name in Desktop/Downloads/Documents | — | not found |
| Methodology | `~/Downloads/Nodes and Networks Methodology and Approach.md` (+ ` (1).md`), `NN-methods-long-Justin-2026-11-02.docx`; not in the repo | Nov 2 | parked (outside repo) |
| Release zip (v22 → v22.5) | **No release zip in the repo.** Closest: `nn/data/nodes169.json` + `nodes169.CHANGELOG.md` (Nov 2); `~/Downloads/nn-dataset-sweep-20261102-115934.zip` (47 KB) | Nov 2 | open item (manifest) |
| Numbers | `qa/numbers-v22.5.md`, `qa/dataset-sweep.md`, `qa/research-open-rows.md` | Nov 2 | live (internal) |
| Embed codes / ASU ledgers | `qa/embed-codes.md`, `qa/embed-codes-asu.md`, `qa/ASU-LEDGER.md`, `qa/asu-embed-kit-2026-11-06.md`, `qa/handoff-fig1-2026-11-05/` | Nov 5–9 | live (internal) |
| Manuscript drafts | `~/Desktop/paper-one-upload-2026-08-26/` (v16, v17 web build, v18 html) and `FINAL FINAL v938` docx copies in Downloads | Aug–Oct | superseded |
| Private repo | `journalism-atlas-private/docs/nodes-and-networks-v5/` (4 v5 docs: copy decisions, kaleidoscope explorer build, review, build brief v2.0, Oct 23); `…/atlas-engine/runs/2026-09-17-nodes-and-networks-preview.md` | Oct 12–23 | parked; **nothing in the private repo is a media asset, and nothing there looks like it belongs in the public repo.** (`REELS.csv` is Vertical Natives research, not N&N.) The reverse: nothing public that belongs in private. |

### Figures and pages

| Asset | Path | Status |
|---|---|---|
| 7 launch-kit figures | `preview/nn-launch-kit/figures/{scale,timeline,map,defector,threshold,bands,kaleidoscope}/` | live (5 embedded by ASU) |
| Explorer (names **on**) | `preview/nn-launch-kit/explorer/` (ASU embed address, must not redirect) and `/nodes-and-networks/explorer/` (source `nn/built/…`) | live |
| Retired explorer-named | `preview/nn-launch-kit/explorer-named/` | superseded (301 to `/nodes-and-networks/explorer/`) |
| Staging explorer | `preview/nn-launch-kit-staging/explorer/` | orphaned |
| Edition (v5) and its embeds `fig-0`…`fig-6` | `preview/nodes-and-networks-edition-e852c5c5/` | live, noindex; ASU-embeddable; has "18 of 18" (section 2) |
| Older preview | `preview/nodes-and-networks-f348eb08/` | superseded (has "18 of 18") |
| Review page | `preview/nn-launch-kit/review/` | parked |
| Test pages | `preview/nn-launch-kit/embed-test/` | live (internal) |
| Edition OG images | `preview/nodes-and-networks-edition-e852c5c5/og/` (cover, fig-0…fig-6, `kaleido-gov-still.png`, 1200x630 per the lens report) | live; not eyeballed for stale counts |
| Landing page, embed page | `nn/built/nodes-and-networks/` (fallback copy rebuilt in today's commit) | live |

### Specific questions from the brief

- **Governance loop copies:** two in the repo (4:5, 9:16), both Oct 28. None post-dates Nov 3. No "18 of 18" visible at 8/10/12 s. The held Drive `launch-video/` copies are outside the repo and I didn't open them. Downloads also holds `nn-launch-1x1-turn.mp4` (Oct 30, 13,263,447 bytes) and `nn-launch-1x1-turn (1).mp4` (Nov 2, 13,265,849 bytes, byte-size matches the current repo render). **The one without "(1)" has the same size as the superseded first-cut "18 of 18" video: don't post it.** `~/Desktop/NN-for-Carrie/nn-launch-1x1-turn.mp4` is also that old size.
- **Kaleidoscope `?capture=1&t=` mode: does not exist.** The only URL parameter the figure reads is `theme=asu`. Its steps (the lenses) are: **field, gov (governance), origin, mech (six ways), born (when they started)**, plus Skip and "Watch it sort again". To get a still per lens you would add a capture mode or drive each step with Playwright. Today there is one still (`still.png`).
- **Budget lens:** there is no separate "budget" lens. "Closer to the center, smaller budget: under $3.5M, $3.5M–$10M, over $10M" is the revenue-band ring legend in the kaleidoscope figure (`figures/kaleidoscope/index.html`) and the explorer (`nn/built/nodes-and-networks/explorer/`); the reels use the same ring layout ("Turn the lens yourself"). The reels' own source is not in the repo; only `qa/video-recut/ORIGINAL.md` and `qa/video-recut/reference/kaleidoscope_reference.html` mention it.
- **Names on hover, live now:** names **on** (`"names":true` in both `/nodes-and-networks/explorer/` live and the source). Matches the Nov 1 ruling.
- **Lens edition:** **never started.** `qa/nodes-networks-lens/` holds only `STEP0-REPORT-2026-10-25.md` and `before/` screenshots. No `preview/` slug, no branch. The `lens` commit `ec88f54` (Oct 27) is unrelated (`scripts/build_lens_index.py`, `scripts/main_beats.py`).
- **Permanent explorer route `/research/nodes-and-networks/explorer/`:** **a catch-all, not a page.** It returns 200 with the homepage (title "Independent Journalism Atlas", canonical `/`, 126,283 bytes), identical to a made-up path. `_redirects` only redirects `/research/nodes-and-networks`, `.html` and the trailing-slash form (301 → `/nodes-and-networks/`). The real explorer is `/nodes-and-networks/explorer/`.
- **Carousel (Cowork, Oct 23):** no Cowork output folder was found. The only carousel is `a5` (Oct 30, refreshed Nov 2).

---

## Assets in no doc

Things I found that the manifest and handoffs don't mention:

1. **`~/Downloads/NN-social-posting-plan-2026-11-02.md`**: a Nov 2 social posting plan. Not opened.
2. **`~/Downloads/nn-social-v22-5-2026-11-02.zip`**: the only archive with the Path 2 recut social set, and the only copy outside the git-ignored folder.
3. **The git-ignored `nn/media/launch/` and `nn/media/social-r1/`**: about 150 MB of the best social material is on this Mac only (and in dist). Not in git, not deployed.
4. **`~/Downloads/nn-launch-1x1-turn.mp4` (no "(1)")** is the stale "18 of 18" video under a current-looking name.
5. **`~/Downloads/nn-for-carrie-2026-11-02b/teaser/`** (`teaser.mp4` 835 KB, `teaser@2x.mp4` 1.5 MB, poster, Nov 3) and **`.../homepage-video/nn-launch-1x1-turn.mp4`** (13,059,927 bytes, a size matching neither repo render). Possibly Carrie's versions. Not opened.
6. **QA screen recordings** (`qa/explorer/*.webm`, `qa/history-final/*.webm`): 390-wide vertical clips of the explorer, 10–17 s. Usable as raw material for a vertical.
7. **`~/Downloads/Nodes and Networks Turn.html`** (168 KB, Oct 23) and **`kaleidoscope_reference.html`** (Oct 29): the interactive sources of the turn video.
8. **`nn/media/launch/gifs/`**: two 720x720 launch GIFs (4.4 s and 7.4 s).
9. **`qa/teaser/out_timeline/teaser_square.mp4`**: a 1080x1080 teaser cut.
10. **`~/Desktop/paper-one-upload-2026-08-26/nodes_and_networks_v16/17/18.html`**: earlier web builds of the paper.
