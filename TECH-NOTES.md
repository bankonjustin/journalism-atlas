# Atlas Tech Notes — March 2026

## Bug Fix: Group Filter (index.html)

**Date:** March 6, 2026
**Status:** Fixed

### What was wrong

The Groups filter sidebar on the index page was showing ~141 extra entries — things like "Culture & Media, Power & Politics" and "Journalism Formats, General News" — instead of just the 9 canonical groups.

**Root cause:** The `group` field in `creators-data.json` stores the raw value from the CSV's "Groups" column, which allows comma-separated multi-group assignments (e.g. `"Culture & Media, Power & Politics"`). The filter code was treating each unique string as a separate key, then a fallback loop was dumping all 141 unrecognized strings into the Groups filter UI. About 50% of creators (614/1,220) had multi-group assignments, so they were effectively invisible to the filter.

The same issue existed for Topics — 689/1,220 creators had comma-separated topic values, meaning the Topics filter had 584 options instead of the ~98 individual topics.

**Fix applied (`assets/js/main.js`):**
- Added `parseCreatorGroups()` — a helper that extracts individual group names from a compound string while correctly handling `"Science, Health & Environment"` (a group name that itself contains a comma)
- `buildFilterOptions()` now counts each constituent group separately, showing correct totals for all 9 groups
- Removed the fallback block that was appending compound group strings to the UI
- `applyFilters()` now matches a creator if *any* of their groups matches the selected filter
- Same fix applied to Topics filter (split on comma, count individually, match on any)

**Result:**
| Group | Before | After |
|---|---|---|
| Power & Politics | 86 | 288 |
| Money & Work | 122 | 237 |
| Civic Life | 37 | 205 |
| Social Issues | 31 | 134 |
| Science, Health & Environment | 79 | 172 |
| Culture & Media | 96 | 309 |
| Lifestyle & Personal Life | 99 | 253 |
| Journalism Formats | 29 | 126 |
| General News | 27 | 120 |

---

## Strategic Audit — Technical Debt & Recommendations

### What prompted this review

The group filter bug surfaced a broader pattern: the CSV schema allows multi-value fields (groups, topics) but the codebase was built assuming single values. As the atlas has grown — adding city-lab-dc, beat-labs, and ad-hoc design changes — this assumption has quietly broken in multiple places. Here's a tiered view of where things stand.

---

### Tier 1 — Fixed (in this session)

- **Group filter**: showing compound strings → fixed (see above)
- **Topic filter**: 584 pseudo-unique options → fixed, now shows ~98 individual topics

---

### Tier 2 — Short-term (next 1–2 sprints)

**1. Schema documentation in `convert.js`**
The converter (`convert.js`) has no documentation that `group` and `topic` are intentionally multi-value comma-separated strings. This will keep causing confusion. A comment block explaining the schema would prevent future devs from assuming they're single values.

**2. City-lab-dc data pipeline consistency**
`city-lab-dc.html` loads its own data files (`dmv-creators.json`, `dc-creators-full.json`, `dmv-recent-posts.json`) with a separate Python-based pipeline (`generate-dmv-feed.py`). This is intentional given its custom corpus, but the field schema should be verified to be consistent with the main atlas — especially if group/topic fields are ever used in DC filtering.

**3. Beat-lab pages (beat-tech, beat-finance, beat-climate)**
These appear to embed their own inline JavaScript rather than sharing `main.js`. Inline copies are where filter logic drift will accumulate. Worth checking if the group/topic parsing fix needs to be mirrored there, or if these pages can eventually reference a shared utility.

**4. `mobile.html`**
Has its own `data-loader.js`. Has not been updated since February. Same group/topic parsing issue likely applies if that page ever surfaces group-based filtering.

---

### Tier 3 — Longer-term (next major data refresh)

**Normalize `group` and `topic` to JSON arrays in `convert.js`**

The cleanest long-term fix: instead of storing `"Culture & Media, Power & Politics"` as a string, `convert.js` should output `["Culture & Media", "Power & Politics"]`. This eliminates the need for `parseCreatorGroups()` and the comma-ambiguity problem entirely.

**Why not now:** It's a breaking change. Every page that reads `creator.group` or `creator.topic` needs to be updated (index.html, city-lab-dc.html, beat-lab pages, mobile.html). That's a coordinated multi-file change best done when there's also a data refresh happening anyway.

---

### Data note

One creator has `group: "Sports"` — a value not in the 9 canonical groups. This is a data entry error in the CSV that should be cleaned up when the spreadsheet is next reviewed.

---

### Summary for DATA + DEV planning

| Issue | Type | Effort | Priority |
|---|---|---|---|
| Group/topic filter bug | Bug | Fixed | Done |
| Schema docs in convert.js | Tech debt | Low | High |
| Beat-lab JS inline copies | Tech debt / drift risk | Medium | Medium |
| mobile.html sync | Tech debt | Low-Medium | Medium |
| city-lab-dc schema audit | Consistency | Low | Medium |
| Normalize JSON to arrays | Refactor | High (multi-file) | Low (do at next data refresh) |
| CSV `Sports` group data error | Data quality | Trivial | Low |
