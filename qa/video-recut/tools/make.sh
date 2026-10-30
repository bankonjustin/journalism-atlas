#!/bin/sh
# Re-render one launch format of the motion cut from the live explorer.
#   sh qa/video-recut/tools/make.sh 1x1
#   sh qa/video-recut/tools/make.sh 9x16
#   sh qa/video-recut/tools/make.sh 16x9
# Reads preview/nn-launch-kit/explorer/index.html (never writes to it). Writes nn/media/launch/ only (+ a temp work dir).
# No cut carries a URL (links go in each post's text), so nothing needs re-rendering when the report link exists.
# Needs: python3 + Playwright + Pillow, swiftc (macOS). No ffmpeg.
set -e
FMT="${1:-1x1}"; shift || true
REPO="$(cd "$(dirname "$0")/../../.." && pwd)"; T="$REPO/qa/video-recut/tools"; OUT="$REPO/nn/media/launch"; W="${TMPDIR:-/tmp}/nn-launch-turn-$FMT"
rm -rf "$W"; mkdir -p "$W/live" "$W/bin" "$OUT"
cp "$REPO/preview/nn-launch-kit/explorer/index.html" "$W/live/index.html"
for p in encode silence mux probe; do swiftc -O "$T/$p.swift" -o "$W/bin/$p" 2>/dev/null; done
python3 "$T/render3.py" "$W/live" "$W" --fmt "$FMT" "$@"
case "$FMT" in 1x1) PX="1080 1080"; BR=3200000;; 9x16) PX="1080 1920"; BR=2800000;; 16x9) PX="1920 1080"; BR=2800000;; esac
"$W/bin/encode" "$W/frames" "$W/v.mp4" $PX 30 $BR
"$W/bin/silence" "$W/a.m4a" 34
"$W/bin/mux" "$W/v.mp4" "$W/a.m4a" "$OUT/nn-launch-$FMT-turn.mp4" 2>&1 | grep -E '^(ok|failed)'
cp "$W/poster.png" "$OUT/nn-launch-$FMT-turn-poster.png"
python3 "$T/srt2.py" "$W/schedule.json" "$OUT/nn-launch-$FMT-turn.srt"
"$W/bin/probe" "$OUT/nn-launch-$FMT-turn.mp4"; ls -la "$OUT"/nn-launch-$FMT-turn*
