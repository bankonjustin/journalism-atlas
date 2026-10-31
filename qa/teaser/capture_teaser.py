#!/usr/bin/env python3
"""Nodes and Networks teaser: Governance -> 6 Ways -> History -> Governance, shapes only, seamless loop.
Deterministic: a virtual clock drives the explorer's own tween, one frame at a time, so output never depends on machine speed.
Usage:  python3 qa/teaser/capture_teaser.py [--history timeline] [--out DIR] [--fps 30]
Needs Playwright (python) and ffmpeg. Builds the explorer first (python3 nn/build.py) and reads nn/_out/.
Exports: teaser.mp4 (H.264, 1280 wide, no audio, faststart), teaser.webm, teaser.gif (800 wide, two-pass palette, <=5MB), teaser_square.mp4 (1080x1080).
"""
import argparse, pathlib, shutil, subprocess, sys
from playwright.sync_api import sync_playwright

ap = argparse.ArgumentParser(); ap.add_argument('--history', default=''); ap.add_argument('--out', default=''); ap.add_argument('--fps', type=int, default=30)
a = ap.parse_args(); REPO = pathlib.Path(__file__).resolve().parents[2]
OUT = pathlib.Path(a.out) if a.out else REPO / 'qa' / 'teaser' / ('out_timeline' if a.history == 'timeline' else 'out')
FR = OUT / 'frames'; shutil.rmtree(FR, ignore_errors=True); FR.mkdir(parents=True)
URL = (REPO / 'nn/_out/nodes-and-networks/explorer/index.html').as_uri() + '?theme=asu&bare=1&morph=1&tab=governance' + ('&history=timeline' if a.history == 'timeline' else '')
HOLD, MOVE = 1.2, 1.95            # seconds: hold on each view, the explorer's dial-turn tween (1.5 s + 0.4 s stagger)
STEPS = [(0, None), (HOLD, 'ways'), (HOLD + MOVE, 'history'), (HOLD + 2 * MOVE + HOLD, 'governance')]   # (time of the trigger, view)
STEPS = [(HOLD, 'ways'), (HOLD + MOVE + HOLD, 'history'), (HOLD + 2 * (MOVE + HOLD), 'governance')]
TOTAL = HOLD + 3 * (MOVE + HOLD) - HOLD                                                              # ends the moment Governance settles, so the loop restarts on the opening hold
VCLOCK = """(() => { let t = 0, q = []; performance.now = () => t; window.requestAnimationFrame = f => { q.push(f); return q.length; }; window.cancelAnimationFrame = () => { q = []; };
  window.__adv = ms => { t += ms; const c = q; q = []; c.forEach(f => f(t)); }; })();"""
n = round(TOTAL * a.fps)
with sync_playwright() as p:
    br = p.chromium.launch(); ctx = br.new_context(viewport={'width': 1600, 'height': 900}, device_scale_factor=2); ctx.add_init_script(VCLOCK)
    pg = ctx.new_page(); pg.goto(URL); pg.wait_for_timeout(1200); pg.evaluate('__adv(16)')
    todo = list(STEPS)
    for f in range(n):
        t = f / a.fps
        while todo and t >= todo[0][0] - 1e-6:
            pg.evaluate(f"NNX.go('{todo.pop(0)[1]}')")
        pg.screenshot(path=str(FR / f'f{f:04d}.png')); pg.evaluate(f'__adv({1000 / a.fps})')
    br.close()
print('frames', n, 'seconds', round(n / a.fps, 2))
def ff(*args): subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', *args], check=True)
src = ['-framerate', str(a.fps), '-i', str(FR / 'f%04d.png')]
ff(*src, '-vf', 'scale=1280:-2', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', '-an', '-movflags', '+faststart', str(OUT / 'teaser.mp4'))
ff(*src, '-vf', 'scale=1280:-2', '-c:v', 'libvpx-vp9', '-pix_fmt', 'yuv420p', '-crf', '32', '-b:v', '0', '-an', str(OUT / 'teaser.webm'))
ff(*src, '-vf', 'crop=1800:1800:700:0,scale=1080:1080', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', '-an', '-movflags', '+faststart', str(OUT / 'teaser_square.mp4'))
for fps, w in ((15, 800), (12, 800), (12, 640)):   # two-pass palette; step down only if over 5 MB
    flt = f'fps={fps},scale={w}:-1:flags=lanczos'
    ff(*src, '-vf', flt + ',palettegen=stats_mode=diff', str(OUT / 'palette.png'))
    ff(*src, '-i', str(OUT / 'palette.png'), '-lavfi', flt + '[x];[x][1:v]paletteuse=dither=bayer:bayer_scale=4', '-loop', '0', str(OUT / 'teaser.gif'))
    if (OUT / 'teaser.gif').stat().st_size <= 5 * 1024 * 1024: print('gif', fps, 'fps', w, 'px'); break
(OUT / 'palette.png').unlink(missing_ok=True); shutil.rmtree(FR)
for f in ('teaser.mp4', 'teaser.webm', 'teaser.gif', 'teaser_square.mp4'): print(f, round((OUT / f).stat().st_size / 1e6, 2), 'MB')
