#!/bin/sh
# Cloudflare Pages build: copy ONLY public site files into dist/ (output directory = dist).
# Default-deny: anything not listed here (docs, scripts, pipeline, snapshots, *.md, *.py,
# the master CSV, .claude, .beads, _deprecated, ...) is never published.
# To publish a new top-level folder or data file, add it below.
set -eu
# Brand check (DESIGN-TOKENS-v16.md § Enforcement): fail the deploy on any new font, size, weight or color violation.
# check_brand.py needs Python 3.7+. If the build image has none, skip loudly rather than block the deploy;
# the required GitHub brand-check status still enforces the rules on every pull request.
if command -v python3 >/dev/null 2>&1 && python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3, 7) else 1)'; then
  python3 scripts/check_brand.py || { echo "build-dist: brand check failed; see the list above and docs/design/DESIGN-TOKENS-v16.md" >&2; exit 1; }
else
  echo "build-dist: WARNING: python3 (3.7+) not found; BRAND CHECK SKIPPED. Set PYTHON_VERSION=3.11 in Cloudflare Pages, or choose build image v2/v3." >&2
fi

rm -rf dist
mkdir -p dist/assets/data dist/data dist/atlas-portal

# Pages and redirects
cp ./*.html _redirects _headers robots.txt wire.json favicon.ico apple-touch-icon.png dist/
cp -R .well-known partners lab teamdmv watershed dist/

# Unlisted previews: page HTML only (no docx/csv/json/notes ever sit under preview/)
mkdir -p dist/preview
(cd preview && find . -name index.html -exec sh -c 'mkdir -p "../dist/preview/$(dirname "$1")" && cp "$1" "../dist/preview/$1"' _ {} \;)
cp atlas-portal/*.html atlas-portal/script.js dist/atlas-portal/

# Nodes and Networks launch kit. This step never fails the site deploy.
# Preferred: build it here from nn/content/copy.md and stamp the pages "built on Cloudflare".
# Fallback: if Python is missing or too old (Pages build image v1) or the build fails, publish the committed copy in nn/built/
# (refreshed by ship.sh) and print a loud warning. The page source says which one is live: view source, first lines.
# preview/nn-launch-kit/explorer/ is the permanent ASU embed address and is published as committed. Only the retired explorer-named copy is dropped (_redirects forwards it).
rm -rf dist/preview/nn-launch-kit/explorer-named
NNTMP=$(mktemp -d)
if command -v python3 >/dev/null 2>&1 && python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3, 7) else 1)' && python3 nn/build.py --out "$NNTMP" --stamp "built on Cloudflare"; then
  cp -R "$NNTMP/nodes-and-networks" dist/
else
  echo "################################################################" >&2
  echo "build-dist: WARNING: the Nodes and Networks build did not run (Python 3.7+ missing or too old, or the build failed; see above)." >&2
  echo "build-dist: WARNING: publishing the COMMITTED FALLBACK COPY in nn/built/. Edits to nn/content/copy.md will NOT show until the build runs." >&2
  echo "################################################################" >&2
  if [ -d nn/built/nodes-and-networks ]; then
    rm -rf dist/nodes-and-networks; cp -R nn/built/nodes-and-networks dist/
    mkdir -p dist/nodes-and-networks/media && cp -R nn/media/. dist/nodes-and-networks/media/
  else
    echo "build-dist: WARNING: nn/built/ is missing too, so /nodes-and-networks/ is NOT published this deploy. Run sh ship.sh." >&2
  fi
fi
rm -rf "$NNTMP"

# Assets
cp -R assets/css assets/js assets/images assets/img dist/assets/

# Nodes and Networks interactive edition (unlisted until launch): assets and share images
cp -R assets/nn5 dist/assets/
for d in preview/*/og; do [ -d "$d" ] && mkdir -p "dist/$d" && cp "$d"/*.png "dist/$d/"; done

# Data files that pages fetch
cp assets/data/creators-data.json assets/data/bluesky-creators.json assets/data/coops-data.json dist/assets/data/
cp data/chicago-pulse.json data/research.json data/social.json dist/data/
# Research hub: poster images and logos per piece (assets/research/<slug>/)
cp -R assets/research dist/assets/
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
find dist -name .gitkeep -delete
