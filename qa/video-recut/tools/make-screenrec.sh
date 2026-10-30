#!/bin/sh
# Re-render one launch format from the live explorer.   sh qa/video-recut/tools/make.sh 1x1
# Reads preview/nn-launch-kit/explorer/index.html (never writes to it). Writes nn/media/launch/ and a temp work dir.
# Needs: python3 + Playwright + Pillow, swiftc (macOS). No ffmpeg.
set -e
FMT="${1:-1x1}"
REPO="$(cd "$(dirname "$0")/../../.." && pwd)"; T="$REPO/qa/video-recut/tools"; OUT="$REPO/nn/media/launch"; W="${TMPDIR:-/tmp}/nn-launch-$FMT"
rm -rf "$W"; mkdir -p "$W/live" "$W/bin" "$OUT"
cp "$REPO/preview/nn-launch-kit/explorer/index.html" "$W/live/index.html"
for p in encode silence mux probe; do swiftc -O "$T/$p.swift" -o "$W/bin/$p" 2>/dev/null; done
python3 "$T/record.py" "$W/live" "$W/frames" --fmt "$FMT"
case "$FMT" in 1x1) PX="1080 1080"; BR=3200000;; esac
"$W/bin/encode" "$W/frames" "$W/v.mp4" $PX 30 $BR
"$W/bin/silence" "$W/a.m4a" 30
"$W/bin/mux" "$W/v.mp4" "$W/a.m4a" "$OUT/nn-launch-$FMT.mp4" 2>&1 | grep -E '^(ok|failed)'
cp "$W/frames/0000.png" "$OUT/nn-launch-$FMT-poster.png"
python3 "$T/srt.py" "$W/schedule-$FMT.json" "$OUT/nn-launch-$FMT.srt"
"$W/bin/probe" "$OUT/nn-launch-$FMT.mp4"; ls -la "$OUT"/nn-launch-$FMT*
