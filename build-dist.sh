#!/bin/sh
# Cloudflare Pages build: copy ONLY public site files into dist/ (output directory = dist).
# Default-deny: anything not listed here (docs, scripts, pipeline, snapshots, *.md, *.py,
# the master CSV, .claude, .beads, _deprecated, ...) is never published.
# To publish a new top-level folder or data file, add it below.
set -eu

rm -rf dist
mkdir -p dist/assets/data dist/data dist/atlas-portal

# Pages and redirects
cp ./*.html _redirects robots.txt wire.json dist/
cp -R .well-known partners lab teamdmv watershed dist/

# Password-gated preview (functions/_middleware.js): only /watershed* invokes the Function
printf '%s\n' '{"version":1,"include":["/watershed","/watershed/*"],"exclude":[]}' > dist/_routes.json

# Unlisted previews: page HTML only (no docx/csv/json/notes ever sit under preview/)
mkdir -p dist/preview
(cd preview && find . -name index.html -exec sh -c 'mkdir -p "../dist/preview/$(dirname "$1")" && cp "$1" "../dist/preview/$1"' _ {} \;)
cp atlas-portal/*.html atlas-portal/script.js dist/atlas-portal/

# Assets
cp -R assets/css assets/js assets/images dist/assets/

# Data files that pages fetch
cp assets/data/creators-data.json assets/data/bluesky-creators.json assets/data/coops-data.json dist/assets/data/
cp data/chicago-pulse.json dist/data/

find dist -name .DS_Store -delete
