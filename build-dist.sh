#!/bin/sh
# Cloudflare Pages build: copy ONLY public site files into dist/ (output directory = dist).
# Default-deny: anything not listed here (docs, scripts, pipeline, snapshots, *.md, *.py,
# the master CSV, .claude, .beads, _deprecated, ...) is never published.
# To publish a new top-level folder or data file, add it below.
set -eu

rm -rf dist
mkdir -p dist/assets/data dist/data dist/atlas-portal

# Pages and redirects
cp ./*.html _redirects wire.json dist/
cp -R .well-known partners lab research teamdmv dist/
cp atlas-portal/*.html atlas-portal/script.js dist/atlas-portal/

# Assets
cp -R assets/css assets/js assets/images dist/assets/

# Data files that pages fetch
cp assets/data/creators-data.json assets/data/bluesky-creators.json dist/assets/data/
cp data/chicago-pulse.json dist/data/

find dist -name .DS_Store -delete
