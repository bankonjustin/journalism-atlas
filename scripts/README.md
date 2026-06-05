# Atlas Chicago Scripts

## Refresh coverage feed data

Run from repo root:

```
node scripts/fetch_chicago_feeds.js
```

This fetches up to 3 recent items from all 65 RSS feeds in CHICAGO_FEEDS,
writes output to `data/chicago-pulse.json`, and prints a summary of what
loaded and what failed.

Commit `data/chicago-pulse.json` and push — Cloudflare Pages will deploy
the updated data within ~1 minute.

**Recommended cadence:** Weekly, or whenever you want fresh coverage data.

**To add/remove feeds:** Edit the FEEDS array in `scripts/fetch_chicago_feeds.js`
AND the CHICAGO_FEEDS array in `city-lab-chicago.html` — keep them in sync.
