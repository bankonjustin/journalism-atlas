# Held-back duplicate slugs — status as of 2026-10-05

**Updated 2026-10-05 by Justin's Claude (Claude Code).** This file originally (2026-09-26) said these 13 slugs were excluded from the regenerated `creators-data.json` and "not live on the site". **That is no longer true**, and the original "Groups reclassification conflict" label for 11 of them did not match the data.

## What is actually the case

- **All 13 slugs are live in `assets/data/creators-data.json`**, added in commit `1777ecb` (2026-09-28, Justin, message "update"; `creators-data.json` 2,417 → 2,430, `site-stats.json` `totalCreators` 2,430). One entry per slug, taken from the **first** of the two master rows.
- `creators-master.csv` still holds both rows for each slug: 2,443 rows, 2,430 unique slugs. The "13-row gap" `preflight.py` reports is exactly these 13 second rows.
- `assets/data/bluesky-creators.json` was **not** regenerated: still 571 entries, without `ethan-clark` and `james-ball`. (Those two have a Bluesky platform entry; `convert_bluesky.py` has not been re-run.)
- `data/atlas-private-columns.csv` (private repo) has 2,430 rows, no duplicate slugs. No change needed there.

## 11 slugs: byte-identical duplicates (no editorial decision needed)

Every column of the two master rows is identical. The "Groups conflict" described in `START-HERE.md` / the 2026-09-21 log is not present in the current file. The only action is deleting the second copy (all second copies sit in the Sept 18 append block, file lines 2350–2365). Proposed delete list: `journalism-atlas-private/PATCHES-PROPOSED/delete-second-row-11-identical-duplicates.csv` (not applied).

| Slug | Keep (file line) | Delete (file line) |
|---|---|---|
| `abigail-wilson-geiger` | 16 | 2360 |
| `eman-sobhy` | 719 | 2351 |
| `ethan-clark` | 773 | 2350 |
| `gianna-toboni` | 852 | 2361 |
| `james-ball` | 991 | 2362 |
| `jason-selvig` | 1025 | 2354 |
| `jose-david-araujo` | 1205 | 2364 |
| `karim-zidan` | 1255 | 2355 |
| `landon-hustig` | 1377 | 2353 |
| `mohammad-taher` | 1666 | 2352 |
| `yannic-kilcher` | 2318 | 2356 |

## 2 slugs: real conflicts (Ryan's call)

| Slug | Row 1 (file line; **the version currently live**) | Row 2 (file line; not live) |
|---|---|---|
| `andrea-cooper` | Line 137: Topic/Category `Mental Health, Travel`; Groups `Science Health & Environment, Lifestyle & Personal Life` | Line 2365: Topic/Category `Social Issues, Travel`; Groups `Lifestyle & Personal Life` |
| `virginia-heffernan` | Line 2291: Platform 2 = Podcast, `https://www.whatroughbeastpod.com` | Line 2357: Platform 2 = `https://omnishamblespod.substack.com` |

Live site values (`creators-data.json`): Andrea Cooper topic `Mental Health, Travel`, group `Science Health & Environment, Lifestyle & Personal Life` (= row 1). Virginia Heffernan secondary platform `Podcast → https://www.whatroughbeastpod.com` (= row 1). All other columns are identical between the two rows of each slug.

## Next step

1. Ryan picks the correct row for `andrea-cooper` and `virginia-heffernan`, and OKs deleting the second row of the 11 identical pairs.
2. Remove the unwanted rows in `creators-master.csv`; confirm `atlas_normalize.py --dry-run` no longer flags duplicate slugs.
3. If Ryan's pick differs from what is live (row 2 for either slug), re-run `convert.js`. `convert_bluesky.py` also needs a re-run to restore `ethan-clark` and `james-ball` to `bluesky-creators.json` (571 → 573).
4. Consider the staged `convert.js` duplicate-slug warning: `journalism-atlas-private/PATCHES-PROPOSED/convert.js.dup-slug-warning.patch` (not applied).

*Original 2026-09-26 context: `journalism-atlas-private/START-HERE.md` open-decisions queue and `LEAVE-OFF-LOG.md` 2026-09-21 (evening).*
