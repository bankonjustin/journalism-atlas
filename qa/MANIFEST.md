# Explorer / figures audit manifest

Read-only audit, Oct 31 2026. No edits, builds, deploys or git writes were made. The only files written are this one and `qa/MANIFEST-appendix-redirects-headers-gitlog.txt` (untracked).

**Limit:** journalismatlas.com answers curl with a Cloudflare bot challenge (403). I did not try to get past it. "Public URL" below is derived from `build-dist.sh`, `_headers` and `_redirects`, not from fetching the live page. Open the URLs in a browser to confirm.

## 0. Headline findings

1. **The ASU embed is not built from `launch-kit/src`.** It is the committed, hand-maintained file `journalism-atlas/preview/nn-launch-kit/explorer/index.html` (98,330 bytes, last changed 28d7e82, Oct 30 10:06). `launch-kit/README.md` (Oct 29 18:49) says so: "hand-maintained in journalism-atlas. Do not run deploy.py against it." `build-dist.sh` publishes it as committed.
2. **The things you listed (tab labels, Rogan, Arial) exist only in that hand-edited file.** `launch-kit/src/explorer.tpl.html` and `launch-kit/out/explorer/index.html` (Oct 28) have the four-tab "In short" / "1 Who pays" layout, Rogan still `EXCEPTION_PLATFORM_LICENSING`, and no `?embed=1` Arial. Re-running `launch-kit/build.py` or `deploy.py` would overwrite the live ASU file with an older, wrong version.
3. **Tonight's work is in `nn/`, which was forked from the kit on Oct 29 08:34 (88b857a), before the ASU edits were made by hand.** `nn/` never received the 3-tab layout or the data fixes (see section 6).
4. **Two data differences exist in the live ASU file that `nn/data/nodes169.json` does not have:** Joe Rogan Experience `m` = `M3_new_org_team_and_portfolio` (not EXCEPTION), and Iowa Public Radio `o` = `INHERITED`, `m` = `INHERITED_SCALE` (not CROSSED / M6). Live: 30 CROSSED + 25 INHERITED = 55. nn: 31 CROSSED + 24 INHERITED = 55. So in the live file **30 grew past $10M, all via one of six; 25 started above.** Your brief says "all 31 above $10M"; that does not match the live data (55 above $10M, 30 of them grew past). Confirm which number you mean.
5. **`ASU-LEDGER.md` is stale on one point.** It says nothing was committed and nothing deployed. Commit `49bdb49` "explorer" (Oct 31 10:06) contains all of tonight's work and **is pushed** (it is `origin/main`). Cloudflare will have built it, so tonight's ASU-themed "In short" explorer is likely live at `/nodes-and-networks/explorer/`.
6. **`24bc4a1` removed the temporary noindex on `/nodes-and-networks/*`** that `c0ac95e` had added 7 minutes earlier. Both are pushed. The folder is no longer noindex ahead of the Nov 5 launch. Check whether that was intended.

## 1. Every explorer copy on disk

All paths relative to `~/Documents/GitHub/`. "Rogan" = classification of Joe Rogan Experience in the embedded data. "Embed Arial" = `?embed=1` switches font to Arial. "ASU theme" = ASU palette (gold `#FFC627`, pink `#E74973`, etc).

### 1a. Explorer HTML copies

| # | Path | Source that builds it | Public URL | Last modified | Tab labels | Rogan | Embed Arial | ASU theme | Used by |
|---|---|---|---|---|---|---|---|---|---|
| A | `journalism-atlas/preview/nn-launch-kit/explorer/index.html` (tracked, 98,330 B, md5 8fbf9809) | **None. Hand-edited in place.** Started from kit output, then edited in git (0695ed0, 88b857a, b091310, 40f50cd, dccd9eb, 50068d7, e14bf3d, 28d7e82) | `/preview/nn-launch-kit/explorer/` (`?embed=1&tab=ways`) | Oct 30 09:35 on disk; last commit Oct 30 10:06 | **Governance / The 6 ways / History** | **Reclassified to M3** | **Yes** (inline `NN_FAM`, added 40f50cd Oct 29) | Partial: gold selected tab and kit palette only; **no `nn-theme`, no pink/group remap** | **Carrie's iframe (ASU embed).** Permanent address per `_redirects` comment |
| B | `journalism-atlas/dist/preview/nn-launch-kit/explorer/index.html` (gitignored) | `build-dist.sh` copy of A | same as A | Oct 30 19:55 | same as A | M3 | Yes | same as A | Build output. Byte-identical to A (md5 8fbf9809) |
| C | `nodes-networks-v5/launch-kit/out/explorer/index.html` (114,197 B, md5 94220c34) | `launch-kit/src/explorer.tpl.html` + `engine.js` via `build.py` | Was `/preview/nn-launch-kit/explorer/` before Oct 29 | Oct 28 22:26 | In short / 1 Who pays / 2 How they got big / 3 When they started | **EXCEPTION_PLATFORM_LICENSING** | **No** (`EMBED` only strips header/footer) | No | Deprecated (superseded by A on Oct 29) |
| C2 | `journalism-atlas-private/docs/nodes-and-networks-v5/launch-kit/explorer-named/index.html` | Identical to C (same md5) | None (private repo) | Oct 28 22:26 | as C | EXCEPTION | No | No | Archive in private repo |
| D | `journalism-atlas/nn/src/explorer.tpl.html` (50,506 B) + `nn/src/engine.js` | Source for E/F/G. Build: `nn/build.py` + `nn/content/copy.md` + `nn/data/nodes169.json` | none (source) | Oct 30 22:56 (committed in 49bdb49) | tabs come from `copy.md`: In short / 1 Who pays / 2 How they got big / 3 When they started | n/a (data in `nn/data`: EXCEPTION) | Yes (`?embed=1` switches Arial and theme) | **Yes** (`nn-theme.css/js` inlined by `build.py`) | **The edition explorer source** (tonight's work) |
| E | `journalism-atlas/nn/built/nodes-and-networks/explorer/index.html` (tracked, 131,773 B) | D via `build.py --fallback` | `/nodes-and-networks/explorer/` (fallback copy only if the Cloudflare build fails; otherwise F is rebuilt on Cloudflare) | Oct 30 22:57 (commit 49bdb49) | In short / 1 Who pays / 2 How they got big / 3 When they started | EXCEPTION | Yes | Yes | **Edition / parked.** Frame-ancestors allows asu.edu, but Carrie's iframe points at A, not here |
| F | `journalism-atlas/nn/_out/nodes-and-networks/explorer/index.html` (gitignored, 131,757 B) | D, local build | same as E | Oct 30 22:56 | as E | EXCEPTION | Yes | Yes | Scratch build output |
| G | `journalism-atlas/dist/nodes-and-networks/explorer/index.html` (gitignored, 118,949 B) | `build-dist.sh` at Oct 30 19:55, i.e. before tonight's work | same as E | Oct 30 19:55 | as E | EXCEPTION | No | Partial (kit palette) | **Stale local build.** Does not match E |
| H | `journalism-atlas/nn/built/nodes-and-networks/explorer/index 2.html` (tracked, 118,959 B) | Finder-style duplicate of an older build | none (not `index.html`, so not served as a page) | Oct 30 22:57 | as C | EXCEPTION | No | No | **Junk duplicate.** Ledger says restored from git on purpose, listed not deleted |
| I | `journalism-atlas/preview/nn-launch-kit/explorer-named/index.html` (380 B) and `nodes-networks-v5/launch-kit/out/explorer-named/index.html` | stub | `/preview/nn-launch-kit/explorer-named/` is **301 to `/nodes-and-networks/explorer/`** and the folder is deleted from `dist` by `build-dist.sh` | Oct 28 22:26 | none | none | none | none | Retired |

### 1b. Kit sources

| Path | Last modified | Notes |
|---|---|---|
| `nodes-networks-v5/launch-kit/src/explorer.tpl.html` (48,504 B) | Oct 28 22:25 | Four tabs, no Rogan fix, no embed Arial, no theme |
| `nodes-networks-v5/launch-kit/src/engine.js` (9,530 B) | Oct 28 22:24 | `nn/src/engine.js` differs by 39 changed lines |
| `nodes-networks-v5/launch-kit/{build,deploy}.py` | Oct 28 19:28, Oct 28 18:44 | `deploy.py` would overwrite A. README says do not run it |

### 1c. The edition's own explorer (the "Turn the lens" page, an older design)

| Path | Source | Public URL | Last modified | Tabs | Rogan | Embed Arial | ASU theme | Used by |
|---|---|---|---|---|---|---|---|---|
| `journalism-atlas/preview/nodes-and-networks-edition-e852c5c5/explorer/index.html` (91,706 B, md5 3067644e) | `nodes-networks-v5/edition` build | `/preview/nodes-and-networks-edition-e852c5c5/explorer/` | Oct 24 14:32 | none (single "Turn the lens" page) | EXCEPTION | No | No (ledger: "not themed, not requested") | The unlisted edition. Not Carrie's |
| Copies, same md5: `dist/preview/...edition.../explorer/index.html` (+ `index 4.html`), `nodes-networks-v5/edition/out/preview/.../explorer/index.html`, `nodes-networks-v5/backups/2026-10-25-pre-lens/preview-slug/explorer/index.html`, and both copies under `journalism-atlas-watershed-go/` | | | | | | | | build outputs and backups |

### 1d. Other "explorer" files that are not live

`nodes-networks-v5/qa/explorer-v04-2026-10-24`, `explorer-v05-2026-10-24` (QA captures), `nodes-networks-v5/kaleidoscope/reel/nn-explorer-reference.html`, `journalism-atlas/qa/explorer/` (videos), `journalism-atlas/qa/v8/explorer-*.png`. Branches `explorer-v04`, `explorer-v05` (gone on origin), `v16-install` are old (Oct 5–24).

## 2. `_redirects` and `_headers`

Full current contents were printed during the audit and are reproduced here for the NN-relevant parts. **Full `git log -p` for both files is in `qa/MANIFEST-appendix-redirects-headers-gitlog.txt`** (592 lines; `_redirects` 15+ commits back to Apr 2026, `_headers` 12 commits back to Oct 23).

### `_redirects` (NN-relevant lines; everything else is partner/slug fixes)

```
/research/nodes-and-networks        /nodes-and-networks/   301
/research/nodes-and-networks.html   /nodes-and-networks/   301
/research/nodes-and-networks/       /nodes-and-networks/   301

# Nodes and Networks launch kit: /preview/nn-launch-kit/explorer/ is the permanent ASU embed address and must NOT redirect (Oct 29). Only the retired explorer-named address forwards.
/preview/nn-launch-kit/explorer-named          /nodes-and-networks/explorer/   301
/preview/nn-launch-kit/explorer-named/         /nodes-and-networks/explorer/   301
/preview/nn-launch-kit/explorer-named/index.html  /nodes-and-networks/explorer/   301
```

### `_headers` (NN-relevant lines)

```
# >>> nn5 edition rules
/preview/nodes-and-networks-edition-e852c5c5/*            X-Robots-Tag: noindex, nofollow
/preview/nodes-and-networks-edition-e852c5c5/embed/*      Content-Security-Policy: frame-ancestors *
# >>> nn launch kit
/preview/nn-launch-kit/*                                  X-Robots-Tag: noindex, nofollow
/preview/nn-launch-kit/explorer/*                         CSP: frame-ancestors 'self' https://asu.edu https://*.asu.edu https://journalismatlas.com
/preview/nn-launch-kit/explorer-named/*                   CSP: frame-ancestors 'self'
# >>> nn permanent home
/nodes-and-networks/explorer/*                            CSP: frame-ancestors 'self' https://asu.edu https://*.asu.edu https://journalismatlas.com
/nodes-and-networks/media/*                               Cache-Control: public, max-age=3600
```

### Is any rule sending `/preview/nn-launch-kit/*` anywhere?

- **Today: only `/preview/nn-launch-kit/explorer-named*` (3 lines, 301 to `/nodes-and-networks/explorer/`).** Nothing redirects `/preview/nn-launch-kit/explorer/`.
- **History:** commit `88b857a` (Oct 29 08:34, "pulse and nodes") added 301s for **both** `explorer` and `explorer-named` to `/nodes-and-networks/explorer/`. At that point the ASU embed URL was redirecting. Commit `b091310` (Oct 29 12:05, "serve preview path (no redirect/drop)") removed the `explorer` lines, about 3.5 hours later. Both are pushed. Today's `_redirects` was last changed in `24bc4a1` (only the `/research/nodes-and-networks` targets) and is pushed.
- **Headers:** `_headers` has `/preview/nn-launch-kit/*` noindex and the frame-ancestors CSP (added 0695ed0 Oct 26, 42b0817 Oct 27, edited 3b309c8 Oct 28). Those allow framing from `*.asu.edu`. None redirects.

## 3. Git state of `journalism-atlas`

```
5cd3923 homepage: retire porch, strip points to research hub   (Oct 31 10:15, LOCAL ONLY)
49bdb49 explorer                                               (Oct 31 10:06, pushed)
24bc4a1 so many                                                (Oct 30 22:36, pushed)
8f51cb8 docs: note contact attribution is GA4 page_location only
7f73dcc research.json: seed CNTI paper, Watershed dek from the essay, Toolkit/Map default CTAs
989be85 nn-gate: publish date Oct 28 -> Nov 5, 2026
c0ac95e Keep /nodes-and-networks/ out of search until the Nov 5 launch (X-Robots-Tag, temporary)
45002c0 docs: research hub James review sheet with screenshots (sample data)
480fa76 docs: research hub posting and editing guide
6c27e59 Watershed: Talked about on module and endcap button read from data/research.json
4d99a02 Research hub: preview at /preview/research/ (noindex), hub CSS and JS, Bluesky read-only module
acba6a3 build-dist: publish data/research.json, data/social.json, assets/research/
0154cfa Research hub: seed data/research.json and data/social.json (4 pieces, no posts)
250d626 Add hidden source and cta fields to /updates, filled from the query string
28d7e82 social
```

**24bc4a1 "so many" (Oct 30 22:36, GitHub Desktop, 55 files, +236/−76).** It captured the early phase of tonight's session, not just one thing:
- `_headers`: **removed** the temporary noindex on `/nodes-and-networks/*` and `/nodes-and-networks`.
- `_redirects`: `/research/nodes-and-networks*` now go to `/nodes-and-networks/` (was the old `/preview/nodes-and-networks-f348eb08/`).
- ASU theme: new `assets/nn5/nn-theme.css` and `nn-theme.js`; `assets/nn5/js/figs/kaleido.js` edited; 7 edition `embed/fig-*/index.html` get the two theme tags.
- Explorer: `nn/build.py`, `nn/src/engine.js`, `nn/src/explorer.tpl.html` (inlines the theme).
- Also: `assets/js/nn-gate.js` (publish date Nov 5), `data/research.json`, `research.html`, and ~35 QA PNGs and `qa/theme/embed_codes.md`.

**49bdb49 "explorer" (Oct 31 10:06, 31 files)** adds the radial History, count-sized rings, morph default, `?bare=1`, copy.md strings, `qa/ASU-LEDGER.md`, teaser files, and refreshes `nn/built/`. It does **not** touch `preview/nn-launch-kit/`.

**Status:** branch `main`, ahead of `origin/main` by 1 (`5cd3923`). Only untracked item: `docs/patches/` (`strip-nn-launch-2026-11-05.md`, written Oct 31 10:15, "NOT applied"). Working tree otherwise clean.

**Anything since 24bc4a1 pushed?** `49bdb49` yes. `5cd3923` (homepage strip, `assets/js/header.js` and `index.html`) **no**. Neither touches the ASU embed file.

## 4. Is `nodes-networks-v5/launch-kit` unchanged since Oct 30?

**Yes, nothing in it changed on or after Oct 30.** Latest modifications:

| File | mtime |
|---|---|
| `README.md` | Oct 29 18:49:13 (the "archive, do not run deploy.py" note) |
| `build.py` | Oct 28 19:28:47 |
| `deploy.py`, `record_named.py`, `test.py` | Oct 28 18:44:23 |
| `src/explorer.tpl.html` | Oct 28 22:25:30 |
| `src/engine.js` | Oct 28 22:24:39 |
| `out/explorer/index.html`, `out/proof-values.json` | Oct 28 22:26:17 |
| everything else | Oct 26–28 |

Not in git (`fatal: not a git repository`). **Backups:**
- `nodes-networks-v5/launch-kit/backup-named/{priv,pub}/index.html` (Oct 28 14:55, pre-explorer-named).
- `journalism-atlas-private/docs/nodes-and-networks-v5/launch-kit/` (git-tracked) holds `explorer-named/index.html` (byte-identical to `out/explorer/index.html`), `PROOF-SHEET.md`, `MECH-RECODE-PROPOSED.csv`. **It does not hold `src/`, `build.py` or `deploy.py`.**
- `nodes-networks-v5/backups/2026-10-25-pre-lens/` predates the kit.
- `nn/src/` in `journalism-atlas` is a git-tracked descendant of the kit src (forked Oct 29), not an exact copy.
- Time Machine: `tmutil latestbackup` fails ("Failed to mount destination"). **No verified backup of `launch-kit/src`.**
- Note: `nodes-networks-v5/edition/src` and `edition/tools` were modified Oct 30 22:55 (the ledger's mirrored theme edits). Not part of launch-kit, also not in git.

## 5. Figure sets

| Set | Source | Files | Last modified | Public URL | Reachable publicly? |
|---|---|---|---|---|---|
| **Edition embed figures** | `nodes-networks-v5/edition` (`build_edition.py`, `src/js/figs/*`) | `journalism-atlas/preview/nodes-and-networks-edition-e852c5c5/embed/fig-0-scale … fig-6-kaleidoscope/index.html` (7) | Oct 30 22:33 (theme tags from 24bc4a1) | `/preview/nodes-and-networks-edition-e852c5c5/embed/fig-N-…/` (themed only with `?theme=asu`) | **Yes, by URL.** Published by `build-dist.sh`; noindex; `frame-ancestors *` |
| Same, stale local build | `build-dist.sh` | `journalism-atlas/dist/preview/…/embed/fig-*` | Oct 30 19:55 | n/a | No (gitignored; pre-theme) |
| **`_deprecated` Chart.js** | old research page | `journalism-atlas/_deprecated/research-nodes-and-networks/figures/figure_1…6_*.html` (also in `journalism-atlas-watershed-go/_deprecated/…`, `paper-one-band-dataset/v16_latest/`) | Oct 15 08:59 (copies Sep 24, Oct 26) | none | **No.** `build-dist.sh` is default-deny and does not copy `_deprecated`. (Live fetch blocked, so unverified) |
| **`figures_v938_final`** | `paper-one-band-dataset/figures_v938_final/` (`html/`, `png/`, `pipeline/`, `screenshots/`, `verify_oct22/`, `LEDGER.md`) | | Oct 20 22:57 (pipeline Oct 23) | none | **No** (outside the site repo) |
| Carrie package | `paper-one-band-dataset/NodesAndNetworks_v938_figures_for_Carrie.zip` | `carrie_package_v938/html/Figure_1…5_*.html` | Oct 20 22:57 | none | No |
| Release zips | `paper-one-band-dataset/nodes_networks_release_v22.zip` (`figures/html/figure_1…8`, Oct 6); `~/Downloads/Nodes_and_Networks_embeds.zip` (7 html, Oct 8); `~/Downloads/Nodes_and_Networks_visuals_v938.zip` (Oct 7); `~/Downloads/v938_figure_reference.zip` (Oct 20) | | | none | No |
| Older paper previews | `paper-one-band-dataset/figures_preview_v22_1`, `sync_package_v22`, `sync_package_v22_1`, `v16_latest` | | Sep 24 – Oct 2 | none | No |

Not checked: contents of the zips beyond file lists; whether Carrie's CMS holds any pasted copies of these.

## 6. Version tree

```
launch-kit/src (Oct 26–28 22:25)  ── build.py ──► launch-kit/out/explorer (Oct 28 22:26)   4 tabs "In short", Rogan EXC, no Arial
        │                                              │
        │                                              ├─ deploy.py ─► preview/nn-launch-kit/explorer  (0695ed0 Oct 26 … 621a952 Oct 28)
        │                                              └─ copy ─► journalism-atlas-private/.../explorer-named (archive)
        │
        ├─ Oct 29 08:34  88b857a "pulse and nodes"
        │       ├─ fork: nn/src/{explorer.tpl.html,engine.js,build.py} + nn/content/copy.md + nn/data  ──► nn/built, /nodes-and-networks/explorer/
        │       └─ preview/nn-launch-kit/explorer given 301 → /nodes-and-networks/explorer/ (briefly)
        │
        └─ preview/nn-launch-kit/explorer then DIVERGES BY HAND (no src):
              Oct 29 12:05 b091310  "final ASU embed edits": −293 lines, 3 tabs (Governance / The 6 ways / History),
                                     Rogan EXCEPTION → M3, redirect removed, EMBED.md rewritten
              Oct 29 15:14 40f50cd  "qa": ?embed=1 Arial (NN_FAM), auto-embed when framed cross-origin
              Oct 29 18:53 dccd9eb  "carrie review"
              Oct 29 22:04 50068d7, 23:41 e14bf3d (GitHub web edits)
              Oct 30 10:06 28d7e82  Iowa Public Radio CROSSED/M6 → INHERITED/INHERITED_SCALE, last edit
                         ══► LIVE ASU EMBED (Carrie's iframe)

nn/src then evolves separately:
   Oct 29–30  copy.md tokenised, chapters, "In short"       (88b857a)
   Oct 30 22:36 24bc4a1  ASU theme inlined (nn-theme.css/js), build.py
   Oct 31 10:06 49bdb49  radial History, count-sized rings, morph default under ASU, bare=1
                         ══► nn/built → /nodes-and-networks/explorer/ (the "In short" explorer; parked/edition)
```

**What diverged and where:**

| Feature | launch-kit/src (Oct 28) | LIVE ASU (A) | nn/src (tonight) |
|---|---|---|---|
| Tabs | In short + 3 numbered | **Governance / The 6 ways / History** | In short + 3 numbered (from `copy.md`) |
| Rogan | EXCEPTION | **M3** | EXCEPTION (`nn/data/nodes169.json`) |
| Iowa Public Radio | CROSSED / M6 | **INHERITED / INHERITED_SCALE** | CROSSED / M6 |
| `?embed=1` Arial | no | yes (inline script, head) | yes (via `nn-theme.js`) |
| ASU palette | no | partial (gold tab only) | full, gated on `?embed=1` / `?theme=asu` |
| History | per-cohort SVG timeline | per-cohort SVG timeline (`HS`) | radial rings + timeline fallback |
| Gov ↔ 6 Ways | instant | instant | morph default under ASU |
| Copy | hard-coded strings | hard-coded strings | `cp('key')` from `copy.md` |
| `engine.js` | `gov`/`ways` | `gov`/`ways` | adds `hist` layout |
| Diff vs live | 466 changed lines (A vs C) | | 218 lines vs kit tpl, 39 lines engine |

## 7. Port plan: tonight's changes onto the ASU embed

First, an important decision before any porting: **`launch-kit/src` is the wrong target.** It is older than the live file and is not what ships. Porting there would produce a third version that nothing publishes. Real options:

| Option | Where | Effect |
|---|---|---|
| **1 (my recommendation, least risk)** | Edit `preview/nn-launch-kit/explorer/index.html` directly, since it is already hand-maintained and tracked | Changes land in git with history; Carrie's URL is unchanged; no build step to break |
| 2 | Add an `asu` target to `nn/build.py` (3 tabs, Rogan and Iowa fixes in data, no "In short") that emits the live path | Single source going forward, but a larger change and the first output will differ from today's bytes |
| 3 | Port into `launch-kit/src` and rebuild | Not recommended: archived, untracked, would overwrite A with a stale layout |

**Steps for option 1 (what each change takes):**

1. **ASU theme.** Add the inlined `nn-theme.css` + `nn-theme.js` (about 33 + 18 lines from 24bc4a1, plus 10 lines changed in 49bdb49) to A's `<head>`. A already runs `NN_EMBED`/`NN_FAM`; `nn-theme.js` sets its own font and the hex remap (`#f6c84e`→`#FFC627`, `#b23a5e`→`#E74973`), so **replace A's inline Arial script rather than adding a second one.** Theme must apply on `?embed=1` and on the auto-embed path (cross-origin framing). nn's switch only reads the URL, so the auto-embed branch needs adding to `nn-theme.js`.
2. **Radial History with count-sized rings.** Copy the `hist` layout from `nn/src/engine.js` and the History renderer, rings and ring labels from `nn/src/explorer.tpl.html` (about 90 changed lines in 49bdb49 plus the earlier 13 in 24bc4a1). Keep `?history=timeline` as the existing SVG path. Needs `1995` from `meta.cut` (present in A's data) and fixed `1970/2008/2026`.
3. **Governance ↔ 6 Ways morph default under ASU.** `MORPH` on when theme on; `?morph=0` disables. A's tab-switch code is a different shape from nn's (`engine: null` for History vs `engine: 'hist'`), so this is a manual re-wire, not a patch.
4. **63/47 removal.** The ledger says the brief's "63 / 47" does not match the data (data gives 38 before 1995 and 130 since). I could not find "63" or "47" as displayed counts in the live file; the only `63`/`47` hits in A are node indices in the JSON. **Needs Justin to say which numbers and where.** In nn, the era bar chart was removed from History; the dek (24 of 38 / 31 of 130) and the "In short" thumbnail still show counts.
5. **Data:** Rogan (M3) and Iowa (INHERITED) already correct in A. **Do not copy `nn/data/nodes169.json` over A's data.** Instead decide whether to backport those two fixes into `nn/data` (a data change; the ledger said N=169 untouched).

**Conflicts to expect:**
- **Tabs and copy:** nn's labels and chapter text come from `copy.md` (`1 Who pays` etc.); A has plain "Governance / The 6 ways / History". Do not carry over `cp()` calls; hard-code A's labels. nn's chapter strings still say "30 of 31 … One exception" (ann.ways_exception names Rogan): **wrong for the live data** (0 exceptions, 30 grew, per section 0).
- **Legend and encoding:** nn has a dashed-triangle "exception" shape and legend key (`grew_past_exception`, `labels.exception_*`, `list.no_mechanism`). With Rogan in M3 these must go or they render an empty exception slot.
- **`engine.js`:** nn's slot widths and keys include `EXCEPTION_PLATFORM_LICENSING`; A's engine has a different key set because Iowa is `INHERITED_SCALE`. Diff the two before merging layout code.
- **Height contract:** `EMBED.md` promises content never taller than about 1610 px (iframe fixed at 1650 px). The radial History at 390 and 760 px has not been measured against that in A. Re-measure before touching Carrie's embed.
- **Framing/CSP:** A is covered by `/preview/nn-launch-kit/explorer/*` frame-ancestors; nothing to change.
- **Visual regression:** nn verified "default theme pixel-identical" for its own page; A has no equivalent baseline. Capture A at 1200/760/390 (all three tabs) **before** editing.
- **Process:** nn's `build.py` copy-token warnings (hand-typed numbers) do not exist in A; there is no check that stops a wrong number.
- **Duplicate `index 2.html` files** tracked in `nn/built/`: harmless to Cloudflare but clutter; do not let a port script glob them.

## Open questions for Justin

1. Is the noindex removal in `24bc4a1` intended?
2. "All 31 above $10M": live data says 55 above $10M, 30 grew past, 25 started above. Which number, and does the Iowa reclassification stand?
3. Which "63 / 47" and where?
4. Option 1, 2 or 3 for the port?
5. Push `5cd3923` separately, or hold with the rest?
