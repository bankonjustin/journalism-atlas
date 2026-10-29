#!/bin/sh
# Ship the Nodes and Networks kit. Run from anywhere:  sh ship.sh
# 1 build, refresh the committed fallback copy (nn/built), brand check   2 show changed kit files, ask y/n   3 commit (message you type), push to main   4 print the live URLs
# Never force-pushes. Only stages the kit paths below and _headers/_redirects/build-dist.sh/brand check; every other change stays untouched.
set -eu
cd "$(dirname "$0")"
PATHS="nn .gitignore .python-version _headers _redirects build-dist.sh scripts/check_brand.py ship.sh"

echo "== 1. Build and brand check"
python3 nn/build.py --check
# Refresh the committed fallback copy so build-dist.sh never falls back to a stale build.
python3 nn/build.py --fallback
python3 scripts/check_brand.py --tight

echo; echo "== 2. Changed kit files"
CHANGED=$(git status --short -- $PATHS)
if [ -z "$CHANGED" ]; then echo "Nothing to ship."; exit 0; fi
echo "$CHANGED"
OTHER=$(git status --short | grep -v -E "^.. ($(echo $PATHS | sed 's/ /|/g'))" || true)
if [ -n "$OTHER" ]; then echo; echo "Not included (outside the kit paths):"; echo "$OTHER"; fi
printf "Commit these? [y/N] "; read -r ans
[ "$ans" = "y" ] || { echo "Stopped. Nothing committed."; exit 0; }

echo; echo "== 3. Commit"
BRANCH=$(git rev-parse --abbrev-ref HEAD)
printf "Commit message: "; read -r msg
[ -n "$msg" ] || { echo "Empty message. Stopped."; exit 1; }
git add -- $PATHS
git commit -m "$msg"
if [ "$BRANCH" != "main" ]; then echo "On branch $BRANCH, not main. Committed here; not pushed."; exit 0; fi
printf "Push to main now? (n = leave the commit for GitHub Desktop) [y/N] "; read -r p
if [ "$p" = "y" ]; then git push origin main; else echo "Committed, not pushed. Push from GitHub Desktop when ready."; fi

echo; echo "== 4. Check these once Cloudflare has deployed (about two minutes)"
for u in "" explorer/ "explorer/?tab=ways" embed/; do echo "  https://journalismatlas.com/nodes-and-networks/$u"; done
echo "  https://journalismatlas.com/preview/nn-launch-kit/explorer/?tab=history   (should land on /nodes-and-networks/explorer/, query kept)"
