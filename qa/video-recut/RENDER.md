# Render notes — launch video (motion cut)

Outputs in `nn/media/launch/` (not committed):

| Format | File | Size | Length |
|---|---|---|---|
| 1:1 1080×1080 | `nn-launch-1x1-turn.mp4` (+ `-poster.png`, `.srt`) | 13.2 MB | 34 s |
| 9:16 1080×1920 | `nn-launch-9x16-turn.mp4` (+ poster, srt) | 11.6 MB | 34 s |
| 16:9 1920×1080 | `nn-launch-16x9-turn.mp4` (+ poster, srt) | 11.6 MB | 34 s |

All: H.264 High, yuv420p, 30 fps, faststart, silent AAC track. `nn-launch-1x1.mp4` (the earlier screen-recording cut) is still there, untouched.

## Re-render (one command per format)
```
sh qa/video-recut/tools/make.sh 1x1
sh qa/video-recut/tools/make.sh 9x16
sh qa/video-recut/tools/make.sh 16x9
```
- No cut carries a URL, so nothing needs a re-render when the report link goes live.
- Reads `preview/nn-launch-kit/explorer/index.html` as it stands (never writes to it) and rebuilds every number from its data. Needs python3 + Playwright + Pillow and swiftc. About 90 s per format.
- 9:16 keeps all text between y=250 and y=1520 (top 250 px and bottom 400 px clear). 16:9 puts the captions in a left column and the chart on the right.

Tools: `tools/render3.py` (compositor), `stagebuild.py` + `stage_tpl.js` (stage on the explorer's own NN engine), `srt2.py`, `encode/silence/mux/probe.swift`. `make-screenrec.sh` + `record.py` are the older screen-recording cut.
