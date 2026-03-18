# Platform Vocabulary Audit
### March 16, 2026 — Pre-cleanup mapping

This documents every hardcoded platform string in the live codebase, flags mismatches against Ryan's current controlled vocabulary, and notes implications for the three new platform values. No changes were made.

---

## 1. Complete list of hardcoded platform strings by file

### `assets/js/main.js` (powers `index.html`)

**`LABEL_ABBREVIATIONS` object** — used for display labels in filter UI and bubble chart:
```
Newsletter - Substack, Newsletter - Ghost, Newsletter - Beehiiv,
Newsletter - ConvertKit, Newsletter - Medium, Newsletter - Buttondown,
Video - YouTube, Video - Instagram, Video - TikTok, Video - Vimeo, Video - Facebook,
Podcast, Website, Social Media
```

**`platformColors` object** — used for sunburst chart segment colors:
```
Newsletter - Substack, Newsletter - Beehiiv, Newsletter - Other, Newsletter - Ghost,
Video - YouTube, Video - Instagram, Video - TikTok,
Social - Twitter / X, Social - BlueSky, Social - LinkedIn, Social - Facebook,
Podcast, Website
```

Note: `main.js` **does not** have a static filter pill list. Platform filter checkboxes on `index.html` are built dynamically from whatever unique `creator.platform` values exist in the JSON. So any platform value present in the JSON will appear in the filter, with or without an abbreviation.

### `pack.html`

**`PLATFORM_LABELS` object** — defines which platforms get filter pills (only these appear):
```
Newsletter - Substack, Newsletter - Beehiiv, Newsletter - Ghost, Newsletter - Other,
Video - YouTube, Video - TikTok, Video - Instagram,
Podcast,
Social - BlueSky, Social - Twitter / X,
Patreon, Website
```

**`PLATFORM_META` object** — used for canvas rendering (label + color dot). Covers a wider set:
```
Newsletter - Substack, Newsletter - Beehiiv, Newsletter - Ghost, Newsletter - Other,
Video - YouTube, Video - Instagram, Video - TikTok, Video - Twitch,
Social - Twitter / X, Social - BlueSky, Social - LinkedIn, Social - Facebook, Social - Threads,
Chat - SMS,
Podcast, Website, Patreon
```

Fallback: `getPlatformMeta()` returns `{ label: '···', color: '#6b7280' }` for any platform not in the map.

### `lists.html`

Two regex-based platform checks (not exact string matches):
- Line 743: `/youtube/i.test(d.platform)` — "Video Journalists" list
- Line 751: `/substack|beehiiv|ghost/i.test(d.platform)` — "Newsletter Journalists" list

These are case-insensitive regexes, so they won't break on minor string changes, but they will silently miss new newsletter/video platforms unless updated.

### `city-lab-chicago.html`

Inline hardcoded creator data with platform strings including:
```
Newsletter - Substack, Newsletter - Beehiiv, Newsletter - Ghost,
Newsletter (generic — non-standard),
Video - YouTube, Video - Instagram,
Podcast, Website
```
These are not read from `creators-data.json`. No impact from JSON changes.

---

## 2. Mismatches and flags

**`'Social Media'` in `main.js` LABEL_ABBREVIATIONS** — this is not a value in Ryan's current controlled vocabulary (which uses `'Social - Twitter / X'`, `'Social - BlueSky'`, etc.). Appears to be a legacy label. Likely unused against live data, but should be cleaned up.

**Platform list divergence between `main.js` and `pack.html`:**

| Platform | main.js LABEL_ABBREV | pack.html PLATFORM_LABELS | pack.html PLATFORM_META | In Ryan's vocab? |
|---|---|---|---|---|
| Newsletter - Substack | ✓ | ✓ | ✓ | ✓ |
| Newsletter - Ghost | ✓ | ✓ | ✓ | ✓ (was `Newsetter`, now fixed) |
| Newsletter - Beehiiv | ✓ | ✓ | ✓ | ✓ |
| Newsletter - Other | ✗ | ✓ | ✓ | ✓ (assumed) |
| Newsletter - ConvertKit | ✓ | ✗ | ✗ | Unknown — not in recent data |
| Newsletter - Medium | ✓ | ✗ | ✗ | Unknown — not in recent data |
| Newsletter - Buttondown | ✓ | ✗ | ✗ | Unknown — not in recent data |
| Video - YouTube | ✓ | ✓ | ✓ | ✓ |
| Video - Instagram | ✓ | ✓ | ✓ | ✓ |
| Video - TikTok | ✓ | ✓ | ✓ | ✓ |
| Video - Vimeo | ✓ | ✗ | ✗ | Unknown |
| Video - Facebook | ✓ | ✗ | ✗ | Unknown |
| Video - Twitch | ✗ | ✗ | ✓ | Unknown |
| Social - Twitter / X | ✗ | ✓ | ✓ | ✓ |
| Social - BlueSky | ✗ | ✓ | ✓ | ✓ |
| Social - LinkedIn | ✗ | ✗ | ✓ | Unknown |
| Social - Facebook | ✗ | ✗ | ✓ | Unknown |
| Social - Threads | ✗ | ✗ | ✓ | ✓ (new, 1 row) |
| Chat - SMS | ✗ | ✗ | ✓ | ✓ (new, 2 rows) |
| Podcast | ✓ | ✓ | ✓ | ✓ |
| Website | ✓ | ✓ | ✓ | ✓ |
| Patreon | ✗ | ✓ | ✓ | ✓ (new, 1 row) |
| Social Media (generic) | ✓ | ✗ | ✗ | No — legacy |

**No `"Newsetter - Ghost"` typo found anywhere in the JS code.** The old typo was only in Ryan's source CSV. All JS files already use the correct spelling `"Newsletter - Ghost"`. When Ryan's corrected CSV is converted, it will match the existing JS strings cleanly.

---

## 3. The three new platform values: display and filter implications

### `Patreon` (1 row)
- **`index.html` filter UI:** Will appear automatically in the checkbox list (dynamic population). No abbreviation label in `LABEL_ABBREVIATIONS` — displays as `"Patreon"` (full string, which is fine). No dedicated sunburst color — falls back to `getPlatformColor()` default (acid green). **Minor display gap, no broken behavior.**
- **`pack.html` filter pills:** Already in `PLATFORM_LABELS` → will appear as a pill when it's eventually added to the filter UI. Already in `PLATFORM_META` with label `'Pat'` and color `#FF424D`. **No issues.**

### `Chat - SMS` (2 rows)
- **`index.html` filter UI:** Will appear automatically in checkboxes. Not in `LABEL_ABBREVIATIONS` — displays as `"Chat - SMS"`. Not in `platformColors` — falls back to default. **Minor display gap, no broken behavior.**
- **`pack.html` filter pills:** NOT in `PLATFORM_LABELS` — will not appear as a pill. In `PLATFORM_META` with label `'SMS'` and color `#22c55e`. **Canvas rendering works. Filter pill gap is intentional per handoff brief.**
- **`lists.html`:** Regex checks won't match `Chat - SMS`. The 2 rows won't appear in the YouTube or Newsletter lists. This is correct behavior.

### `Social - Threads` (1 row)
- **`index.html` filter UI:** Will appear automatically in checkboxes. Not in `LABEL_ABBREVIATIONS` — displays as `"Social - Threads"`. Not in `platformColors` — falls back. **Minor display gap.**
- **`pack.html` filter pills:** NOT in `PLATFORM_LABELS` — no pill. In `PLATFORM_META` with label `'Threads'` and color `#a0a0a0`. **Canvas rendering works. No pill is intentional per handoff brief.**
- **`lists.html`:** Not matched by Newsletter or Video regexes. Correct.

**Summary:** None of the three new values will cause errors or broken UI. The gaps are cosmetic (no abbreviation label in main.js, no dedicated sunburst color for Chat - SMS and Social - Threads). When these platforms are eventually added to the filter pills, the work is: add to `pack.html` PLATFORM_LABELS, and add to `main.js` LABEL_ABBREVIATIONS and `platformColors`.

---

## 4. Where filter UI would need updating when adding new platforms

**`pack.html`:** Add the platform string to `PLATFORM_LABELS` → pill appears automatically. `PLATFORM_META` should also be updated for the canvas label/color dot (though the fallback `'···'` will work in the interim).

**`main.js`:** The filter checkbox list is fully dynamic — no code change needed for new values to appear. But for a proper abbreviation label, add to `LABEL_ABBREVIATIONS`. For a dedicated sunburst color, add to `platformColors`.

**`lists.html`:** The two regex-based lists (`/youtube/i`, `/substack|beehiiv|ghost/i`) would need updating if new video or newsletter platforms should be included in those curated lists.

---

## Recommended cleanup (not this session)

1. Remove `'Social Media'` (legacy, non-matching) from `main.js` LABEL_ABBREVIATIONS
2. Align `main.js` LABEL_ABBREVIATIONS to match the actual platform values in Ryan's live data — add `Social - Twitter / X`, `Social - BlueSky`, `Newsletter - Other`; verify whether ConvertKit, Medium, Buttondown, Vimeo, Video - Facebook are still in active use
3. Add `Chat - SMS` and `Social - Threads` to `main.js` LABEL_ABBREVIATIONS and `platformColors` when they're promoted to filter UI
4. Consider consolidating `PLATFORM_META` (pack.html) and `platformColors` (main.js) into a shared data file to avoid future drift
