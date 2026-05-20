# Atlas _redirects Audit
*Last updated: 2026-05-20*
*Cloudflare Pages redirect documentation*

---

## How This File Works

Cloudflare Pages has two mechanisms that can conflict. The **`_redirects` file** handles explicit rules in the format `/old-path  /new-path  301`. **"Pretty URLs"** is a Cloudflare platform feature that implicitly strips `.html` extensions, meaning `page.html` is automatically served at `/page` with no rule required. The conflict pattern: if `_redirects` contains a 200-rewrite rule pointing `/path` → `/path.html`, and Pretty URLs simultaneously strips `.html`, you get an infinite redirect loop. The fix is to never write 200-rewrite rules that overlap with what Pretty URLs already handles — and in practice, to never write 200-rewrite rules at all unless you have a deliberate URL-masking reason. **Cache persistence:** Cloudflare's edge cache can hold old redirect rules for minutes to hours after `_redirects` is corrected. Always test in a fresh incognito window; a stale cached 301 in your regular browser will mask the fix.

---

## Full Redirects Inventory

| # | Source | Destination | Status | Destination file exists | Notes |
|---|--------|-------------|--------|------------------------|-------|
| 1 | `/partner-list-cillizza` | `/partners/cillizza` | 301 | Yes — `partners/cillizza.html` | Correct |
| 2 | `/partner-list-cillizza/` | `/partners/cillizza` | 301 | Yes | Trailing-slash variant — correct |
| 3 | `/partner-icfj` | `/partners/icfj` | 301 | Yes — `partners/icfj.html` | Correct |
| 4 | `/partner-icfj/` | `/partners/icfj` | 301 | Yes | Trailing-slash variant — correct |
| 5 | `/partner-list-grist` | `/partners/grist` | 301 | **No — `partners/grist.html` does not exist** | Chain link — see chain note below |
| 6 | `/partner-list-grist/` | `/partners/grist` | 301 | No | Chain link |
| 7 | `/partner-list-stahl` | `/partners/grist` | 301 | No | Chain link |
| 8 | `/partner-list-stahl/` | `/partners/grist` | 301 | No | Chain link |
| 9 | `/partner-list-ahp-v1` | `/partners/ahp` | 301 | Yes — `partners/ahp.html` | Versioned source URL — correct destination |
| 10 | `/partner-list-ahp-v1/` | `/partners/ahp` | 301 | Yes | Trailing-slash variant |
| 11 | `/partner-list-ahp` | `/partners/ahp` | 301 | Yes | Correct |
| 12 | `/partner-list-ahp/` | `/partners/ahp` | 301 | Yes | Trailing-slash variant |
| 13 | `/partners/grist` | `/partners/jessica-stahl` | 301 | Yes — `partners/jessica-stahl.html` | **Chain destination** — see chain note |
| 14 | `/partners/grist/` | `/partners/jessica-stahl` | 301 | Yes | Trailing-slash variant |
| 15 | `/what-we-do.html` | `/about-this-project` | 301 | Yes — `about-this-project.html` | Correct; `.html` source variant |
| 16 | `/what-we-do` | `/about-this-project` | 301 | Yes | Correct |
| 17 | `/bluesky-creator-intelligence` | `/bluesky-intelligence` | 301 | Yes — `bluesky-intelligence.html` | Correct |
| 18 | `/bluesky-creator-intelligence.html` | `/bluesky-intelligence` | 301 | Yes | `.html` source variant — correct |
| 19 | `/submit` | `/contact` | 301 | Yes — `contact.html` | Correct status code (301 not 302) — see flag below |
| 20 | `/contact.html` | `/contact` | 301 | Yes | Correct — prevents Pretty URLs from having two live paths for same page |
| 21 | `/submit.html` | `/contact` | 301 | Yes | Correct |

**No 200-rewrite rules found** — no Pretty URLs conflict risk present.

---

## Chained Redirect (Action Required)

Rules 5–8 all point to `/partners/grist`, which does not exist as a file. Rules 13–14 then redirect `/partners/grist` → `/partners/jessica-stahl`. This creates a two-hop chain for anyone visiting `/partner-list-grist` or `/partner-list-stahl`:

```
/partner-list-grist  →  /partners/grist  →  /partners/jessica-stahl
/partner-list-stahl  →  /partners/grist  →  /partners/jessica-stahl
```

Cloudflare Pages will follow the chain (both rules are in `_redirects`), but this is fragile — if rule 13/14 is ever removed, rules 5–8 break entirely, and browsers have already cached the intermediate 301 to `/partners/grist`. **The fix is to collapse the chain by pointing rules 5–8 directly to `/partners/jessica-stahl`.**

**Proposed fix (replace lines 5–8 in `_redirects`):**
```
/partner-list-grist    /partners/jessica-stahl    301
/partner-list-grist/   /partners/jessica-stahl    301
/partner-list-stahl    /partners/jessica-stahl    301
/partner-list-stahl/   /partners/jessica-stahl    301
```

Rules 13–14 (`/partners/grist` → `/partners/jessica-stahl`) should be kept to handle any links that already resolved to the intermediate URL.

---

## Partner Redirect Coverage

| Partner page | Old root URL(s) covered by `_redirects` | Redirect rule exists | Destination exists | Notes |
|---|---|---|---|---|
| `partners/cillizza.html` | `/partner-list-cillizza` + trailing slash | Yes | Yes | Correct |
| `partners/icfj.html` | `/partner-icfj` + trailing slash | Yes | Yes | Correct |
| `partners/jessica-stahl.html` | `/partner-list-grist`, `/partner-list-stahl` + trailing slashes (via chain) | Yes (indirect) | Yes | Chain — fix recommended |
| `partners/ahp.html` | `/partner-list-ahp`, `/partner-list-ahp-v1` + trailing slashes | Yes | Yes | Correct |
| `partners/emily-atkin.html` | None known | **No rule** | Yes | No evidence of old root URL — may never have had one. Flag for Justin |
| `partners/joon-lee.html` | None known | **No rule** | Yes | Same |
| `partners/karen-attiah.html` | None known | **No rule** | Yes | Same |
| `partners/knowledge-creators.html` | None known | **No rule** | Yes | Same |
| `partners/natgeo.html` | None known | **No rule** | Yes | Same |
| `partners/news-creator-corps.html` | None known | **No rule** | Yes | Same |
| `partners/noah-smith.html` | None known | **No rule** | Yes | Same |
| `partners/rahim-jessani.html` | None known | **No rule** | Yes | Same |

**Note:** The eight partners with no redirect rules were built directly in `partners/` (no prior root-level URL), so missing redirects are expected. Justin should confirm whether any of these ever had a root-level URL that was shared publicly.

---

## Fixes Applied This Session

None were applied automatically. The chain issue (rules 5–8) requires Justin's confirmation before editing.

---

## Flags for Justin

| Issue | Question / Action needed |
|-------|--------------------------|
| **Chained redirect: grist** | Rules 5–8 point to `/partners/grist` (no file), which then chains to `/partners/jessica-stahl`. Recommend collapsing: change rules 5–8 to point directly to `/partners/jessica-stahl`. OK to apply? |
| **`/submit` retirement** | `submit.html` still exists in the repo and `submit.html`'s OG tags are therefore live. The `/submit` → `/contact` redirect is correct (301). But: is `submit.html` fully retired and safe to delete? If yes, delete it — its OG tags are moot and it can't be accidentally linked. If it should stay as a legacy page, no action needed. |
| **`/city-lab-dc` routing** | Both `city-lab-dc.html` (older, ~78 KB, title "Atlas City Lab — Washington, D.C. / DMV") and `city-lab-dc-v3.html` (canonical, ~100 KB, title "Who Covers Washington Now") exist. Both have `og:url = /city-lab-dc`. Pretty URLs serves `city-lab-dc.html` at `/city-lab-dc` — the older file, not v3. There is **no redirect in `_redirects`** from `/city-lab-dc` to `city-lab-dc-v3`. Visitors hitting `/city-lab-dc` are getting the wrong (older) file. **Action needed:** Add a rule `/ city-lab-dc  /city-lab-dc-v3  301` OR rename `city-lab-dc-v3.html` to `city-lab-dc.html` (after deleting/archiving the old one). Renaming is cleaner — no redirect needed, Pretty URLs handles it. |
| **`/pack` → `/postcard` missing** | `pack.html` still exists in the repo and Pretty URLs serves it at `/pack`. There is **no redirect** from `/pack` to `/postcard` in `_redirects`. If `/pack` was supposed to be retired in favor of `/postcard`, add: `/pack  /postcard  301`. If `pack.html` is intentionally separate from `postcard.html`, no action needed. |
| **`/mobile` — no redirect** | `mobile.html` exists and is accessible at `/mobile`. CLAUDE.md lists it as a fetch()-based page (not retired). If it should be retired or redirected to `/search`, a rule is needed. Currently it resolves as a live page. |
| **`/index-pre-homepage` — no redirect** | `index-pre-homepage.html` exists. CLAUDE.md says "do not delete until homepage is confirmed stable." It is currently accessible as a live URL at `/index-pre-homepage`. If the homepage is now stable, either delete it or add `/index-pre-homepage  /  301`. |
| **New partner pages (8 pages)** | `emily-atkin`, `joon-lee`, `karen-attiah`, `knowledge-creators`, `natgeo`, `news-creator-corps`, `noah-smith`, `rahim-jessani` have no redirect rules. If any of these ever had old root-level URLs that were shared publicly or linked externally, add rules now. If they were built directly in `partners/`, no action needed. |
| **`what-we-do.html` still in repo?** | `what-we-do.html` does **not** exist in the repo (redirect is in `_redirects` as expected, file was deleted or never committed). This is correct — nothing to do. |
| **`bluesky-intelligence` destination** | `bluesky-intelligence.html` exists. The redirect from `/bluesky-creator-intelligence` is correct. Note this page is listed in CLAUDE.md as internal/dev — if it should not be publicly accessible, a redirect to `/` or removal is needed. Currently it resolves as a live page. |

---

## Verified Correct (static analysis)

The following rules were confirmed correct by checking `_redirects` against file existence:

- `/partner-list-cillizza` → `/partners/cillizza` (301) — destination exists
- `/partner-icfj` → `/partners/icfj` (301) — destination exists
- `/partner-list-ahp` and `/partner-list-ahp-v1` → `/partners/ahp` (301) — destination exists
- `/what-we-do` and `/what-we-do.html` → `/about-this-project` (301) — destination exists, source file deleted
- `/bluesky-creator-intelligence` and `.html` variant → `/bluesky-intelligence` (301) — destination exists
- `/submit`, `/submit.html`, `/contact.html` → `/contact` (301) — destination exists, status code is 301 (permanent) not 302
- All trailing-slash variants pair correctly with their non-slash counterparts

---

## Known Risks

**Pretty URLs + `_redirects` conflict:** Cloudflare Pages' Pretty URLs feature automatically serves `page.html` at `/page`. This means any page with a `.html` file is accessible at both the clean URL and (sometimes) the `.html` URL. The `_redirects` file already handles the `.html` → clean URL case for `/contact.html` and `/what-we-do.html`. If new pages with `.html` URLs ever get linked externally, add a matching `.html` source rule pointing to the clean URL.

**No 200-rewrite rules present:** The current `_redirects` file contains no 200-rewrite rules. This is the correct state — no loop risk.

**Cache persistence:** After editing `_redirects`, Cloudflare edge cache can retain old rules for minutes to hours. Always test in an incognito window. A 301 cached in a regular browser will persist until cache expiry even after the rule is corrected.

**Chain fragility:** Rules 5–8 (grist/stahl) rely on rules 13–14 being present to reach the final destination. Removing rules 13–14 would silently break the chain without a file-system error.

**`/city-lab-dc` serving wrong file:** Until the `city-lab-dc.html` file is replaced or a redirect is added, visitors to `/city-lab-dc` receive the older 78 KB version, not the canonical `city-lab-dc-v3.html`. This is the highest-impact live bug in the current redirect configuration.

---

## How to Test After Changes

Since live curl tests were not run in this session, test the following manually after pushing:

1. Visit each source URL in incognito mode — confirm you land at the correct destination
2. For the `/city-lab-dc` fix: confirm the page title reads "Who Covers Washington Now" not "Atlas City Lab — Washington, D.C. / DMV"
3. For the grist chain fix: visit `/partner-list-grist` — confirm you land at `/partners/jessica-stahl` in a single hop (check Network tab in DevTools — should show one 301, not two)
4. For any new redirects: check HTTP status in DevTools Network tab — confirm 301 not 302
