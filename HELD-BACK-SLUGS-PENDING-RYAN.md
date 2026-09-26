# Held-back slugs — excluded from the 2026-09-26 convert.js pass

These 13 slugs (26 rows, still duplicated in `creators-master.csv`) were deliberately excluded from `creators-master-CONVERT-STAGING-20260926.csv` and therefore from the regenerated `creators-data.json` / `bluesky-creators.json` / `site-stats.json`. They are **not live on the site** until Ryan rules on each conflict and a follow-up conversion re-includes them. Full original context: `journalism-atlas-private/START-HERE.md`'s open-decisions queue and `LEAVE-OFF-LOG.md`'s 2026-09-21 (evening) entry.

| Slug | Reason held |
|---|---|
| `abigail-wilson-geiger` | `Groups` reclassification conflict — two copies disagree on Groups value. |
| `eman-sobhy` | `Groups` reclassification conflict. |
| `ethan-clark` | `Groups` reclassification conflict. |
| `gianna-toboni` | `Groups` reclassification conflict. |
| `james-ball` | `Groups` reclassification conflict. |
| `jason-selvig` | `Groups` reclassification conflict. |
| `jose-david-araujo` | `Groups` reclassification conflict. |
| `karim-zidan` | `Groups` reclassification conflict. |
| `landon-hustig` | `Groups` reclassification conflict. |
| `mohammad-taher` | `Groups` reclassification conflict. |
| `yannic-kilcher` | `Groups` reclassification conflict. |
| `andrea-cooper` | `Topic/Category` conflict — "Mental Health" vs. "Social Issues" framing between the two copies. |
| `virginia-heffernan` | Two different real podcast URLs listed as her Platform 2 (`whatroughbeastpod.com` vs. `omnishamblespod.substack.com`) — factual question of which show is current. |

## Side effect worth knowing

Two of these (`ethan-clark`, `james-ball`) have a Bluesky platform entry, so excluding them also dropped `bluesky-creators.json` from 573 → 571 entries in this pass — not a bug, just the same exclusion propagating downstream. Re-including these 13 slugs after Ryan's ruling will need `convert_bluesky.py` re-run too, not just `convert.js`.

## Next step (not built yet, per instruction)

Once Ryan rules on each of the 13: pick the correct row for each slug, remove the other, re-run `atlas_normalize.py --dry-run` to confirm the duplicate-slug flags clear, then re-run `convert.js` and `convert_bluesky.py` against the real (now-deduped) `creators-master.csv` directly — no staging copy needed at that point, since the conflict will be resolved in the source file itself. This is a small follow-up, not something to automate now.
