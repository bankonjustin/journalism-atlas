# Preview build ledger — Nodes and Networks (v938)

Built 2026-10-12 from `FINAL FINAL v938 - Networks and nodes (4).docx` (sha256 `43aa786b7c18…`, saved Oct 12 11:32). Staged only: nothing committed, nothing deployed.

**Preview URL once pushed:** `https://journalismatlas.com/preview/nodes-and-networks-f348eb08/`

---

## Before you push

Privacy: accepted as-is (Justin, 2026-10-12). No Access, no further repo changes.

These 3 older unpushed commits go out in the same push:

| Commit | Date | Message | Files |
|---|---|---|---|
| 83af51f | 2026-10-11 | Add build-dist.sh: copy-only allowlist so Pages publishes just site files | `build-dist.sh` (+23) |
| 5583ce3 | 2026-10-11 | Ignore dist/ build output | `.gitignore` (+3) |
| 82250f6 | 2026-10-11 | CLAUDE.md: document the build-dist.sh allowlist and the add-it-or-it-404s rule | `CLAUDE.md` (+3 −3) |

---

## Files created or changed

| Path | Status | What |
|---|---|---|
| `preview/nodes-and-networks-f348eb08/index.html` | new | The page (909 KB, of which the six inlined figures are most) |
| `robots.txt` | new | `User-agent: *` / `Disallow: /preview/` (the slug isn't named) |
| `build-dist.sh` | changed | Adds `robots.txt`, and copies only `index.html` files from `preview/` into `dist/` |
| `tools/preview-build/config.json` | new | docx path, figures folder, slug, byline override, expected counts, figure-to-embed map with per-figure `data_table` switch |
| `tools/preview-build/parse_docx.py` | new | docx → `content/content.json` + `content/content.md` (stdlib only; reads `word/document.xml`) |
| `tools/preview-build/build_page.py` | new | content.json + embeds → page, `build_report.json` |
| `tools/preview-build/validate.py` | new | Playwright checks against `dist/`, served over local HTTP → `validation.json`, `screenshots/` |
| `tools/preview-build/Makefile` | new | One-command re-run |
| `tools/preview-build/content/content.json`, `content.md` | new | Parsed content. **content.md is the file to diff after Brian's sweep.** |
| `tools/preview-build/build_report.json`, `validation.json` | new | Machine output behind this ledger |
| `tools/preview-build/screenshots/` | new, git-ignored | 10 MB of review images, not for commit |
| `tools/preview-build/.gitignore` | new | Ignores `screenshots/` and `__pycache__/` |

Not touched: any `cohort_reference_expanded_vN.csv`, any figure source or data in `paper-one-band-dataset/`, `research/nodes-and-networks.html`, `CLAUDE.md`, `CURRENT_STATE.md`.

## Re-run

```bash
make -C tools/preview-build preview DOCX="/path/to/fresh-export.docx"
```

This runs: parse → build page → `build-dist.sh` → Playwright checks. It exits non-zero if any check fails. `DOCX` is optional; when given, it's saved as the new `docx` in `config.json`. Then review:

```bash
git diff -- tools/preview-build/content/content.md
```

## Figure-to-embed mapping

Embeds come from `paper-one-band-dataset/figures_v22/html/`. Each one's data source is the matching `figures_v22/data/fig_*.csv`. All six are static SVG with built-in fonts, no JavaScript and no runtime data loading, so no data needed baking in (your point 4 didn't apply).

| # | Docx ¶ | Embed | Embed title | Next paragraph matches brief | Caption (2026-10-12) |
|---|---|---|---|---|---|
| 1 | 31 | `fig_funding_shocks.html` | Funding shocks, 2018 to 2026 | ✓ "The pattern is the same across every failure…" | supplied |
| 2 | 53 | `fig_nine_cohorts.html` | Nine cohorts | ✓ "Nine cohorts, one axis…" | supplied |
| 3 | 102 | `fig_inn_concentration.html` | INN concentration | ✓ "Texas Tribune is the more replicable counter-case…" | supplied (flag 9) |
| 4 | 133 | `fig_defector.html` | Defector: revenue and revenue per subscriber | ✓ "404 Media launched on $4,000…" | supplied; stale docx line not rendered |
| 5 | 177 | `fig_grant_dependency.html` | Grant dependency in the band | ✓ "Track the same organizations for three years…" | supplied |
| 6 | 181 | `fig_governance_lands.html` | Where governance lands | ✓ "Line up all nine cohorts…" | supplied |

**What the page takes from each embed:** the wide SVG plus its own phone-width SVG, which switches in below 620px. Each figure gets the label "Figure N — *embed title*".

**What it drops:** each embed's own caption and note, and its "Download CSV" link (`../data/fig_*.csv`). The link is stripped from the source line; the build stops if one survives.

**Data tables** (collapsed "Data table" under the figure, with the embed's source line): restored on **1, 2, 4, 6**. **Held on 3 and 5**, because those tables are org-level rows with values the figure doesn't show:
- Figure 3: exact revenue in dollars, filing year and sourcing tier for 7 organizations
- Figure 5: exact total revenue, EIN and sourcing tier for 17 organizations

To restore them, set `"data_table": true` for figures 3 and 5 in config.json and re-run. Figure 1's table includes source URLs and internal columns ("Verified", "Status vs earlier file"), shown exactly as they are in the embed.

**One rename:** the embeds' built-in fonts are renamed (`NNFig DM Sans`, `NNFig Libre Baskerville`) so they can't collide with the page's fonts. No data, label or value in any figure changed.

## Validation: 37/37 passed

| Check | Result |
|---|---|
| Served: page in `dist/`; only `index.html` under `/preview/` | PASS |
| Served: no `.docx`/`.csv`/ledger/`content.json` anywhere in `dist/` | PASS |
| `robots.txt` disallows `/preview/` without naming the slug | PASS |
| Slug not referenced by any other served file; no sitemap/RSS exists | PASS |
| Page loads over HTTP at the clean slug path | PASS |
| 1 title block · 5 sections (intro, i–iv) · 9 cohort headings | PASS |
| Cohort jump strip C1–C9 inside section II | PASS |
| 6 figures, none empty/zero-height (760 / 772 / 406 / 397 / 484 / 429 px at 1280) | PASS |
| Body word count: docx 7,927 · page 7,927 · **+0.00%** (docx total incl. title block 7,963) | PASS |
| No paragraphs dropped, duplicated or invented (checked paragraph by paragraph) | PASS |
| No "apergam", "carriesimmons", "@" mentions; none of the 8 docx comments' text in the page | PASS |
| No unflagged `[CAPTION NEEDED]` (0 on page; all six captions supplied) | PASS |
| No CSV/xlsx/download links; no "Download CSV" text; meta robots `noindex, nofollow`; banner text exact | PASS |
| Data tables only on approved figures (1, 2, 4, 6) | PASS |
| Byline renders "Justin Bank" | PASS |
| Fig 2 card-grid n: C1 18, C2 26, C3 8, C4 44, C5 14, C6 8, C7 7, C8 27, C9 17 = 169 (wide and phone) | PASS |
| Fig 6 stacked-bar rows each equal that cohort's n; total 169 (wide and phone) | PASS |
| No horizontal page scroll at 375 / 768 / 1280; all 6 figures render at each width | PASS |

Word count scope: everything from the Introduction heading to the end, headings included. Excluded on both sides: the title block, figures, figure captions, and the cohort strip. Also verified: the page has 24 external links (23 distinct URLs, as in the docx), and italics and bold are preserved.

## Flags (reported, not fixed)

1. **USAID figure: $268M vs $271.5M.** The text (¶25) says "The U.S. government froze **$271.5 million** in U.S. Agency for International Development journalism funding on Jan. 20, 2025." The figure 1 graphic says "USAID freezes media-support funding (**$268M**)". The open comment suggests dropping the number from the graphic. Your call. (`figure_sources.yml` notes that dollar figures appear on the graphic only where sourced.)
2. **The figure 3 image is inside one of your tracked deletions** (Justin Bank, 2026-10-08), together with the placeholder "(Figure 3 makes the concentration visible at a glance…)". If every change were accepted, figure 3 would be gone. I kept the image and dropped the placeholder text, assuming the image was meant to replace the placeholder (as `figure_list.md` says). The switch is `"keep_figures_in_deletions": true` in config.json. Best fixed in the doc by re-inserting the image outside the deletion.
3. **There are tracked changes in what should be a pen-down draft:** 1 insertion, 3 deletions, 1 deleted paragraph mark. Accepted as described.
   - ¶48 (Brian Cleveland): "— not a metaphorical one, an actual one, that shows" → "that show"
   - ¶102 (Justin Bank): the figure 3 placeholder plus the image (flag 2)
   - ¶179 (Brian Cleveland): deletes "The Colorado Sun is the one nonprofit in this study that doesn't need anyone's grant renewal to stay where it is. Almost everyone else in that range is waiting, to some degree, on someone else's decision." The paragraph mark goes too, so nothing is left of ¶179.
4. **Captions: resolved.** Justin supplied a title, caption and source line for all six figures (2026-10-12). They're stored in config.json (`title`, `caption`, `source` per figure) because the docx has none, so they survive re-runs. Precedence: config, then a docx caption line, then the placeholder. The docx's stale "*Figure 4: Defector Media Timeline*" line is still in the doc. It's matched as figure 4's caption line, so it doesn't render as body text, and the supplied caption shows instead. Delete it in the doc when convenient.
5. **Byline: resolved.** The docx title-block line (¶2) reads "Knight Center for the Future of News · ASU Cronkite School · Justin Bank (Independent Journalism Atlas)". Per Justin (2026-10-12), the page renders "Justin Bank". This is set by `"byline"` in config.json; it overrides the docx and survives re-runs. Remove the key to go back to the docx line.
6. **Small docx formatting quirks, kept as written:**
   - ¶25 has a double space ("Development  journalism").
   - Several links include a leading space inside the link text, e.g. "; Penske Media Corp. took the rest…", so the underline starts on the space.
   - The title heading ends in a trailing space.
7. **An older public preview is still live** at `/research/nodes-and-networks` (pandoc pipeline, `journalism-atlas-private/research/nodes-and-networks/sync_paper.py`, with iframes to the old ~300 KB figure wrappers). Once this page ships, the two will disagree. Consider retiring that page or redirecting it here. I didn't touch it.
8. **robots.txt caveat (accepted):** disallowing `/preview/` stops crawlers fetching the page, so they never see the noindex tag. If someone posts the URL publicly, search engines can still list the bare URL. That's acceptable given you're fine with the page being live.

9. **Caption checks (Justin's three, checked against the figure data):**
   - **Defector Year 3: the docx is wrong.** Defector's Year 3 letter says "the $4.5mm revenue Defector recognized this past year" (table: ~$4,500,000). The chart's $4.5M is right; the C7 paragraph's "$4.4 million" should become "$4.5 million". Not changed (prose comes from the docx).
   - **Figure 3: the caption overstates the split.** The six after ProPublica total $112.5M, which is 1.75× ProPublica's $64.3M, so "about as much again" is off. "Nearly twice as much again" is closer, or cut the sentence. Also, ProPublica is 9.5% of the $675M midpoint, so "roughly 9%" understates it slightly; "nearly 10%" matches the "tenth of the sector" title. The caption is currently rendered verbatim.
   - **Figure 5's metric:** the chart plots `Grant_Dependency_Pct` = contributions ÷ total revenue, from ProPublica's 990 extract (data dictionary v22). That contributions figure is Part VIII line 1h, the total of lines 1a–1f, so it *includes* government grants (1e). "Grants and donations" is accurate; "contributions" is accurate in the 990 sense.
   - **Figure 6 (not asked):** "Nearly every cohort leans hard toward one end" mirrors the paper's text, but Barbell Hybrids (38/25/38) and Philanthropic Networks (48/30/23) don't lean hard either way.

## Design notes

- **Kept from v16:** the palette, Libre Baskerville/DM Sans (via Google Fonts, as in v16), the masthead, section and cohort heading styles, the figure frame and caption styles, and the footer.
- **Dropped:** Chart.js (nothing uses it), the data tables, risk matrix, stat row, info boxes, abstract box, org lists and the old cohort-grid component.
- **Text sizes raised to the Atlas floors** in CLAUDE.md: body 16px, UI text 13px or larger, all-caps labels 11px.
- **Added:**
  - the slim banner
  - a sticky section nav (Intro, I–IV); the active section is highlighted, and hovering an item shows the section's full heading
  - the C1–C9 jump strip under the section II heading
  - `referrer: no-referrer`, so outbound links don't send the slug in the Referer header
- **Light mode only:** neither the v16 chrome nor the figure embeds have a dark theme.

## Screenshots (`tools/preview-build/screenshots/`, light mode)

- `375-top.png`, `768-top.png`, `1280-top.png`: the first screen at each width
- `375-full.jpg`, `768-full.jpg`, `1280-full.jpg`: the full page at each width
- `375-figure-1.png` … `375-figure-6.png`: each figure at phone width. The sticky nav shows over the top of some of these; that's the nav, not a defect in the figure.
- `375-cohort-strip.png`: the jump strip at phone width
- `375-figure-6-table.png`: figure 6 with its data table open at phone width
