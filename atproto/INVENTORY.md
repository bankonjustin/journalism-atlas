# Atlas on standard.site: Phase A inventory

Read-only. Run 2026-10-26. Login was skipped (the app password in `.env` was rejected), so nothing here touched the account except public reads. Nothing was written, committed or pushed.

## 0. Blockers and flags first

| # | Item | Why it matters |
|---|---|---|
| 1 | **Login fails.** `.env` has `BSKY_HANDLE` / `BSKY_APP_PASSWORD` (dated Jun 17), and the PDS rejects the password. Brief expects `ATP_IDENTIFIER` / `ATP_APP_PASSWORD`. | Phase B can't write until a working app password exists. |
| 2 | **Cloudflare managed challenge on HTML.** `curl` to any HTML page (`/`, `/watershed/`, preview pages) returns **403 with `cf-mitigated: challenge`**, even with a browser or Bluesky Cardyb user agent. Images, `.well-known/atproto-did` and other non-HTML files return 200. | The brief's `verify` checks 2 and 3 (live HTML fetched with `curl`) will always fail. Bluesky's card crawler may also be challenged, which would break the enhanced card. Needs a Cloudflare rule (Justin). I made no change. |
| 3 | **`/.well-known/site.standard.publication` is a soft 200.** The file doesn't exist yet, but the live site answers 200 with the **homepage HTML** (`text/html`). | `verify` check 1 must compare the body, not just the status. It must not pass on a bare 200. |
| 4 | **Watershed has no visible publication date.** No `<time>`, no JSON-LD, and the byline reads only "By Justin Bank". The only date in the git history is the Oct 24 create and the Oct 26 launch commit. | `publishedAt` in the config can't be "from the page". Justin has to supply it. Candidates: 2026-10-25 (the `_redirects` comment says the preview slug was retired "at publish (Oct 25, 2026)") or 2026-10-26 (launch commit message "byline date set to Oct. 26"). |
| 5 | **Account display name** is "The Independent Journalism Atlas (TIJA)", not the brief's "Independent Journalism Atlas". The site `<title>` is "Independent Journalism Atlas". | Justin to confirm the publication `name`. |
| 6 | **No suitable icon.** The icons in `assets/images/icons/` are 504 px, and the `.png` files are actually JPEG data. A transparent or white-on-black icon should ideally be real PNG. | The brief asks for a PNG of at least 256 px. The 504 px files meet the size, but not the format. Justin to pick one, or supply a PNG. I won't convert silently. |
| 7 | **The N&N page lists an editor (Andy Pergam) and a publisher (Knight Center)** in its JSON-LD. | Not a lexicon field, so I won't carry it. Flagged for awareness. |

Stop conditions checked so far: handle resolves OK; `.env` is gitignored OK; no existing `site.standard.*` records OK (`listRecords` returned empty for publication and document, and the repo's collections are only profile, like, post, repost and follow); canonical URL is unambiguous OK (see below); `.well-known` is served OK. Login: **FAIL**. Lexicon fetch: **not yet run** (Phase B).

## 1. Build and deploy

- Host: **Cloudflare Pages**, repo `github.com/bankonjustin/journalism-atlas`, deployed through GitHub Desktop.
- Build: `build-dist.sh` (shell, default-deny allowlist) copies source into `dist/`. `dist/` is gitignored.
- The site is **hand-written HTML**, not generated. Only the `{{CREATOR_COUNT}}` and `{{COUNT_AS_OF}}` tokens are stamped into `dist/` at build time. **Edit the source files**, not `dist/`.
- `_headers` and `_redirects` are in the repo root. Note `_headers` currently has an uncommitted change (the nn-launch-kit block) and `preview/nn-launch-kit/` is untracked. Both predate this work.

## 2. Can it serve `.well-known/`?

Yes. `build-dist.sh` line 13 runs `cp -R .well-known …`. Cloudflare Pages has no Jekyll step. The existing file `/.well-known/atproto-did` is live (200, `application/octet-stream`, body `did:plc:b4w5zuldomsclxxhs5dp7pb4`). No config change is needed.

The new file `.well-known/site.standard.publication` will be copied by the same line, with no extension and so no content-type guess. It will probably be served as `application/octet-stream`, like `atproto-did`. `verify` will report it.

## 3. Watershed

| Fact | Value |
|---|---|
| Source file | `watershed/index.html` (static, 273 KB; supporting `watershed/methods/index.html`) |
| Live URL | `https://journalismatlas.com/watershed/` |
| Live now? | **Yes.** In a browser, `/watershed` resolves to `/watershed/` and the page loads. `curl` gets 403 (challenge, see flag 2), so I couldn't report a curl status code. |
| Canonical form | **Trailing slash.** `<link rel="canonical" href="https://journalismatlas.com/watershed/">` and `og:url` agree. `/watershed` and `/watershed/index.html` both redirect (opaque redirect in the browser, so normalized to `/watershed/`). Not ambiguous. |
| Record `path` | `/watershed/` |
| `<title>` | A Watershed Moment for News Deserts |
| Meta description | Medill's map shows where local news has dried up. Look closer and information is still moving — across county lines, and through platforms, beats and forms the count doesn't see. |
| `og:image` | `https://journalismatlas.com/watershed/assets/social-16x9.jpg` (1600×900 JPEG, 461 KB, under 1 MB). Also `leader-3x2.jpg` (738 KB). |
| Byline | By Justin Bank. Leader art by James Bareham. |
| Publication date | **Not on the page** (flag 4). |
| Old preview URL | `/watershed-preview-uhh7gdyn[/]` 301s to `/watershed/` |
| Existing link tags | None |

## 4. Nodes and Networks interactive edition

| Fact | Value |
|---|---|
| Source file | `preview/nodes-and-networks-edition-e852c5c5/index.html` (194 KB). Assets in `assets/nn5/`, share images in `preview/…/og/`. Builder lives outside the repo (`nodes-networks-v5`). |
| Live URL | `https://journalismatlas.com/preview/nodes-and-networks-edition-e852c5c5/` (unlisted preview; `noindex, nofollow` meta and header; `robots.txt` disallows `/preview/`). |
| Live now? | The old retired preview `…f348eb08/` is the current `_redirects` target for `/research/nodes-and-networks`. The edition preview is in the build allowlist. `curl` is challenged (403), so no curl status. In the browser, `/preview/nodes-and-networks-edition-e852c5c5` returns a redirect, i.e. it resolves to the slash form. |
| Canonical | `https://journalismatlas.com/preview/nodes-and-networks-edition-e852c5c5/`, with trailing slash. |
| `<title>` | Nodes and Networks: The Reorganization of American Journalism |
| Meta description | A field study of 169 U.S. journalism organizations in nine governance cohorts. Knight Center for the Future of News, ASU Cronkite School. |
| `og:image` | `…/og/cover-1200x630.png` (39 KB) |
| Publication date | Not on the page. There is a `datePublished` check pending, and none found in my grep. Oct 28 is the planned timing per the brief. |

**Decision needed before the second document.** This page is a `noindex` preview, and its canonical URL is the preview path. The final public URL isn't set yet. The record's `path` must match the canonical URL, so the launch step (which stages the final URL) has to happen first, or the path will be wrong. I'll keep `enabled: false` until then.

## 5. Homepage and essays index

- Homepage: `index.html`, `<head>` at lines 3 to 525, canonical `https://journalismatlas.com/`. It links to `/watershed/` (lines 538, 1081).
- Essays index: there is no dedicated one. **`research.html`** is the closest (canonical `https://journalismatlas.com/research`, `<head>` at lines 3 to 658). It's the research listing that holds the featured Watershed card. I'd put the publication tag on it. Confirm.
- Neither has an existing `site.standard` tag.

## 6. Existing atproto artifacts

- `.well-known/atproto-did`: exists, committed (`3f43100`), one line, `did:plc:b4w5zuldomsclxxhs5dp7pb4`. It matches the live file, and the PLC document lists `at://journalismatlas.com` as the handle. No DNS TXT record is set (the file route is used).
- Other `.well-known` files: none.
- PDS: `https://agrocybe.us-west.host.bsky.network`.
- Existing `site.standard.*` records: **none**.
- Profile: created 2025-12-15, 9 posts, 16 followers.

## 7. Proposed config values (for Justin to confirm)

- Colors from `ATLAS-BRAND-GUIDE-v3.md`: acid green `#ceff00` (CTAs only), dark olive `#5d7400`, black `#000000`, white `#ffffff`, brand orange `#ffaa00`. The brief says green, black and grey with an orange accent. A proposal: `background #ffffff`, `foreground #121212`, `accent #ffaa00`, `accentForeground #000000`. The guide restricts acid green to CTAs, so I avoided it as the accent. Orange `#ffaa00` on white is low contrast; the guide lists `#b35100` as its accessible text variant.
- Icon: needs a decision (flag 6).
- Watershed cover: `watershed/assets/social-16x9.jpg` (fits the size limit).
- N&N cover: `preview/nodes-and-networks-edition-e852c5c5/og/cover-1200x630.png`.

## Questions for Justin (before Phase B)

1. A new app password in `.env` (and use of `ATP_*` names).
2. The Watershed `publishedAt`: Oct 25 or Oct 26, 2026?
3. A Cloudflare rule so HTML isn't challenged for `curl` and Bluesky's crawler (or accept that `verify` must run another way).
4. The publication `name` and `description`.
5. The icon file (and whether a real PNG is acceptable to make).
6. Is `research.html` the right "essays index"?
7. How to handle the N&N final public URL.

Stopped here, awaiting approval to proceed to Phase B.
