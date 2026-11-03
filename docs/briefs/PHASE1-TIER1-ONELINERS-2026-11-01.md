# Phase 1 item 3: tier 1 one-liners (DECISIONS-QUEUE, `journalism-atlas-private/ops/`)

Nov 1, 2026, against `main` `8179b90`. Each row: current state, the exact change once you give the value. Nothing applied.

| # | Item | Current state | Change once ruled |
|---|---|---|---|
| L1 | Release time | `assets/js/nn-gate.js:6` `publishAt: '2026-11-05T12:00:00-05:00'` is the noon-ET placeholder (comment on line 2 says so). Carrie's time is not in either repo. Must be on `main` and deployed by Tue Nov 3. | `-var NN = { publishAt: '2026-11-05T12:00:00-05:00', url: ... }` / `+... publishAt: '2026-11-05T<HH:MM>:00-05:00' ...`. Eastern daylight time ended Sun Nov 1, so Nov 5 is EST and `-05:00` is the right offset. Also update the comment on line 2. |
| L2 | Push local commits | Done. `main` is even with `origin/main` at `8179b90`; `e5d9944`, `3a5277d`, `337256b`, `8fc8f1e` are all in history. | None. |
| L3 | for-brands gate | Done in `337256b`; the line is `[data-nn-show hidden]` and revealed by `nn-gate.js`. Its link still points to `/research` (`for-brands.html:420`). | Link change is part of `docs/patches/nn-launch-v2-2026-11.md` §4; safe to land early. |
| L4 | Homepage card date | Done in `8fc8f1e` ("Nov 5, 2026"), now hidden until the instant (`index.html:1081`, `data-nn-show hidden`). | None. If L1's time ever moves the date, the date text on the card is typed, not tokenized. |
| L5 | Names | Ruled ON (Oct 31, and again Nov 1 ruling 1). `meta.show_org_names` is `true` in `nodes169.json` but nothing in `build.py` reads it. | None. Remaining action is yours: tell Andy and Carrie names are public (due Mon Nov 2). |
| L6 | Report URL | `nn/content/settings.json:2` `"report_url": ""`. While empty, links read "About the report" and go to `report_fallback_url` (`https://journalismatlas.com/research#nodes-and-networks`). Carrie's URL not in either repo. | `-  "report_url": "",` / `+  "report_url": "<url>",`. Then `python3 nn/build.py --fallback` to refresh `nn/built/`. If the URL differs from `/nodes-and-networks/`, also the `for-brands.html:420` link in the patch. Note: `nn-gate.js` `url` (line 6) is the N&N landing page, a separate value from this report URL. |
| L7 | Count 169 | Derived: `nodes169.json` `meta.n` 169, `public-snapshot.json` 169 nodes, ASU embed 169. `build.py:159` stops the build if either file isn't 169. No 170th found. Editorial for Andy: Washington Post, Risk.net and Insurance Journal unverified; Radio Jornalera NJ has no founding year. | None unless ASU's final PDF says otherwise. You compare against the PDF; if it differs, flag and stop (the data files are read-only). |
| L8 | Embed domains | Frame rule for the explorer: `_headers:32` `Content-Security-Policy: frame-ancestors 'self' https://asu.edu https://*.asu.edu https://journalismatlas.com`. (The older `/preview/nn-launch-kit/explorer/*` rule is at `_headers:24`, same value.) The brief, queue and README all agree on this default. | To widen: append the origin to both lines, e.g. `... https://journalismatlas.com https://<new-origin>`. |
| L9 | `?nn=1` early reveal | `nn-gate.js:8` `var live = Date.now() >= Date.parse(NN.publishAt) \|\| /[?&]nn=1\b/.test(location.search);`. Works today (checked Phase 0 on four pages). | After launch (Fri): `-var live = Date.now() >= Date.parse(NN.publishAt) \|\| /[?&]nn=1\b/.test(location.search);` / `+var live = Date.now() >= Date.parse(NN.publishAt);`. |
| L10 | Launch target | `/nodes-and-networks/` is wired everywhere (`nn-gate.js` `url`, the patch, `_redirects:65-67`). Blocked by the Rogan ruling. | See `docs/briefs/PHASE1-ROGAN-LAUNCH-TARGET-OPTIONS-2026-11-01.md`. |
| L11 | Accept URL exposure for 5 days | The page is built and reachable, protected only by `_headers:36-41` (`X-Robots-Tag: noindex, nofollow` on `/nodes-and-networks/*`). No `noindex` meta on the built pages, and no site link to it before the instant. | Nothing to change now. The block comes out in the launch patch §2. |

## Things to know

- `ship.sh` commits and pushes to `main` after a y/n prompt. Don't use it under the "no commits or pushes" rule; refresh `nn/built/` with `python3 nn/build.py --fallback` and commit in Desktop.
- Stale refs, not touched: `.git/refs/remotes/origin/HEAD.lock` (Oct 6, 30 bytes) is still there. It is stale, flagged, and I have not removed it. Say the word and I'll delete it.
- `scripts/check_brand.py` exclusion of `preview/nn-launch-kit-staging/` (DECISIONS-QUEUE W12): the exclusion list says it changes "only with a new token version". Flag for James; it is what keeps the check at 2,766.
