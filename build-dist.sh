#!/bin/sh
# Cloudflare Pages build: copy ONLY public site files into dist/ (output directory = dist).
# Default-deny: anything not listed here (docs, scripts, pipeline, snapshots, *.md, *.py,
# the master CSV, .claude, .beads, _deprecated, ...) is never published.
# To publish a new top-level folder or data file, add it below.
set -eu

rm -rf dist
mkdir -p dist/assets/data dist/data dist/atlas-portal

# Pages and redirects
cp ./*.html _redirects _headers robots.txt wire.json favicon.ico apple-touch-icon.png dist/
cp -R .well-known partners lab teamdmv watershed dist/

# Unlisted previews: page HTML only (no docx/csv/json/notes ever sit under preview/)
mkdir -p dist/preview
(cd preview && find . -name index.html -exec sh -c 'mkdir -p "../dist/preview/$(dirname "$1")" && cp "$1" "../dist/preview/$1"' _ {} \;)
cp atlas-portal/*.html atlas-portal/script.js dist/atlas-portal/

# Assets
cp -R assets/css assets/js assets/images assets/img dist/assets/

# Nodes and Networks interactive edition (unlisted until launch): assets and share images
cp -R assets/nn5 dist/assets/
for d in preview/*/og; do [ -d "$d" ] && mkdir -p "dist/$d" && cp "$d"/*.png "dist/$d/"; done

# Data files that pages fetch
cp assets/data/creators-data.json assets/data/bluesky-creators.json assets/data/coops-data.json dist/assets/data/
cp data/chicago-pulse.json dist/data/
# Pulse: per-week post files fetched by pulse.html (written by pipelines/pulse/update_pulse.py)
cp -R assets/data/pulse dist/assets/data/
# Issue Lens index for /for-brands (written by scripts/build_lens_index.py, committed)
cp assets/data/lens-index.json dist/assets/data/

# Generated counts: fill {{CREATOR_COUNT}} / {{COUNT_AS_OF}} / {{BLUESKY_COUNT}} from assets/data/site-stats.json
# (written by convert.js from creators-master.csv). Source pages keep the tokens; only dist/ is stamped.
STATS=assets/data/site-stats.json
COUNT=$(sed -n 's/.*"totalCreatorsLabel": *"\([^"]*\)".*/\1/p' "$STATS")
ASOF=$(sed -n 's/.*"asOfLabel": *"\([^"]*\)".*/\1/p' "$STATS")
BSKY=$(sed -n 's/.*"blueskyCountLabel": *"\([^"]*\)".*/\1/p' "$STATS")
[ -n "$COUNT" ] && [ -n "$ASOF" ] && [ -n "$BSKY" ] || { echo "build-dist: $STATS is missing totalCreatorsLabel/asOfLabel/blueskyCountLabel; run node convert.js" >&2; exit 1; }
find dist -name '*.html' -exec sed -i.bak -e "s/{{CREATOR_COUNT}}/$COUNT/g" -e "s/{{COUNT_AS_OF}}/$ASOF/g" -e "s/{{BLUESKY_COUNT}}/$BSKY/g" {} +
find dist -name '*.bak' -delete
if grep -rlE '\{\{(CREATOR_COUNT|COUNT_AS_OF|BLUESKY_COUNT)\}\}' dist; then echo "build-dist: unresolved count tokens above" >&2; exit 1; fi

find dist -name .DS_Store -delete
