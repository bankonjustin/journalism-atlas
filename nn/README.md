# Nodes and Networks kit (live source)

Live at `journalismatlas.com/nodes-and-networks/` (landing), `/explorer/` (what ASU embeds), `/embed/` (copy-paste code).
This folder is the live source. `nodes-networks-v5/launch-kit/` is the archive.

## Change words in two minutes
1. On github.com open `nn/content/copy.md`, click the pencil, edit, commit to `main`.
2. Cloudflare rebuilds on every push. The pages update in about two minutes.

One heading per string (`## some.id`), the text below it. Numbers are tokens such as `{over10m_total}`; the build fills them from the data. Type a number by hand and the build warns. A missing string id or an unknown token fails the build and names the line. Strings marked `[locked]` quote the paper and the build refuses to change them.

Not changed by a push (these are baked into files): the video captions and end card, the share images (1200×630), the still image. After editing `video.*`, `share.*` or a chapter sentence, run `python3 nn/tools/render_media.py` on a Mac and commit `nn/media/`. The caption file (`.vtt`) is rebuilt on every deploy, but the burned-in captions need the re-render.

## Set the report address (one place)
Edit `nn/content/settings.json`. While `report_url` is empty, every link says "About the report" and goes to `report_fallback_url`. Fill `report_url` and the links say `report_link_label` and go to the paper. Nothing else changes. The video carries no report address.

## Preview on your machine
```
python3 nn/build.py --watch
```
Rebuilds on save, serves `http://localhost:8000/nodes-and-networks/`, reloads the browser.

## If the build can't run on Cloudflare
`build-dist.sh` never fails the site deploy over this kit. If Python is missing or too old, or the build fails, it publishes the committed copy in `nn/built/` and prints a loud warning in the build log. `sh ship.sh` refreshes `nn/built/` every time, so it is never stale after a ship. View source on any page: the first lines say `built on Cloudflare` or `fallback copy`. While the fallback is live, edits to `copy.md` do not show.

## If a build fails locally
 Read the build log: the message names the file, line and reason. Fix `copy.md` and push again. `python3 nn/build.py --check` shows the same message before you push.

## Preview before it goes live (optional)
Push to a branch named `nn-draft`. Cloudflare Pages makes a preview address for that branch. Open it, check the pages, then merge to `main`.

## Tokens you can use in copy.md
Counts and names, all from the data: `n_orgs`, `cohorts_word`, `top_word`, `top_hold`, `over10m_total`, `rest_word`, `rest_hold`, `top_pct`, `crossed`, `six_way_growers`, `ways_word`, `exceptions_phrase`, `cut`, `hist_pre`, `hist_pre_over`, `hist_post`, `hist_post_over`, `hist_old_kinds_word`, `unverified_orgs`, `unverified_be`, `started_above`, `under_n`, `exception_name`, `older_two`, `gov_top_*`, `gov_second_*`, `gov_small_*`, `hist_c2_*`, `hist_c5_*`, `hist_c7_*`.
From settings: `publisher_line`, `report_label`, `embed_width`, `video_seconds`.
Filters: `{name|cap}` capitalizes. `{@other.id}` pastes another string.
The page script also fills `{name}`, `{year}`, `{n}`, `{over}`, `{tot}` and a few others as it runs; leave those in place.

## Data
`nn/data/nodes169.json` is the public node file. `nn/data/public-snapshot.json` holds name, founding year, revenue, origin and mechanism for each node, all of which already appear in the public page. The private CSVs stay in `paper-one-band-dataset`. To refresh the snapshot after a data change, on a machine that has the private repos: `python3 nn/tools/snapshot.py`, then commit.

## Files
- `build.py` the build. `src/` templates and engine. `content/` copy and settings. `data/` data. `media/` videos, poster, share images, still (committed; Cloudflare cannot render them).
- `tools/render_media.py` renders media; `tools/encode.swift` is the H.264 encoder; `tools/snapshot.py` refreshes the data snapshot.
- `video/timeline.json` scene and caption timing.

## Embedding
The explorer may be framed by this site, `asu.edu` and `*.asu.edu` (`_headers`). Other sites are refused.
Old `/preview/nn-launch-kit/explorer/` and `/explorer-named/` addresses redirect to the new explorer and keep their query string (`_redirects`).

## Build needs
Python 3.7 or later, standard library only. `.python-version` (3.11) at the repo root asks Cloudflare for 3.11 on build images v2 and v3. Image v1 ignores it.
