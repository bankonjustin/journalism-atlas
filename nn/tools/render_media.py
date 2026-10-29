#!/usr/bin/env python3
"""LOCAL ONLY. Re-renders the files Cloudflare cannot build: the two videos, the poster, the share images and the still.
Words come from nn/content/copy.md, so run this after changing any video.*, share.* or chapter wording.
  python3 nn/tools/render_media.py [--only video|og]
Needs: Python 3 with Playwright (chromium), Pillow, and `swift` (macOS) for the H.264 encode. Output: nn/media/."""
import sys, os, json, pathlib, shutil, subprocess, tempfile, threading, functools, http.server, importlib.util
HERE = pathlib.Path(__file__).resolve().parent
NN = HERE.parent
MEDIA = NN / 'media'
spec = importlib.util.spec_from_file_location('nnbuild', NN / 'build.py'); B = importlib.util.module_from_spec(spec); spec.loader.exec_module(B)
ONLY = sys.argv[sys.argv.index('--only') + 1] if '--only' in sys.argv else None
FPS, KBPS = 24, 2400
work = pathlib.Path(tempfile.mkdtemp(prefix='nnmedia-'))
site = work / 'site'
R, T, _ = B.build(site)
shutil.copy(B.FONT, site / 'InterTight-var.woff2')
H = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(site))
H.log_message = lambda *a, **k: None
srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), H); PORT = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()
EX = 'http://127.0.0.1:%d/nodes-and-networks/explorer/' % PORT
from playwright.sync_api import sync_playwright
MEDIA.mkdir(exist_ok=True); (MEDIA / 'og').mkdir(exist_ok=True)
HIDE = '.tabs,.steps,.chline,details.explore,.attr,.foot,.see{display:none!important} html,body{background:#fff!important}'
tl = B.timeline()


def beats(pw):
    """One crisp screenshot per scene, taken from the real explorer (embed mode, 2x)."""
    b = pw.chromium.launch(); pg = b.new_page(viewport={'width': 780, 'height': 1000}, device_scale_factor=2)
    out = {}
    for tab in ('short', 'governance', 'ways', 'history'):
        pg.goto(EX + '?embed=1&tab=' + tab); pg.wait_for_function('document.fonts.status==="loaded"'); pg.wait_for_timeout(900)
        pg.add_style_tag(content=HIDE); pg.wait_for_timeout(300)
        pg.locator('main').screenshot(path=str(work / ('beat-%s.png' % tab))); out[tab] = work / ('beat-%s.png' % tab)
        if tab != 'short':
            pg.locator('#hist' if tab == 'history' else '#stage').screenshot(path=str(work / ('chart-%s.png' % tab)))
    b.close(); return out


COMPOSER = r'''<!doctype html><meta charset="utf-8"><style>@font-face{font-family:"Inter Tight";src:url(InterTight-var.woff2);font-weight:500 800}html,body{margin:0;background:#fff}</style><canvas id="c"></canvas>
<script>
const CFG = __CFG__, ez = x => x < .5 ? 2 * x * x : 1 - Math.pow(-2 * x + 2, 2) / 2, cl = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const imgs = {}; let ready;
async function init(fmt) {
  const tall = fmt === '9x16', W = tall ? 1080 : 1920, H = tall ? 1920 : 1080, c = document.getElementById('c'); c.width = W; c.height = H; window.F = { tall, W, H, ctx: c.getContext('2d') };
  await Promise.all(['700 40px', '600 40px', '500 40px'].map(f => document.fonts.load(f + ' "Inter Tight"')));
  await Promise.all(Object.entries(CFG.beats).map(([k, u]) => new Promise(r => { const i = new Image(); i.onload = () => { imgs[k] = i; r(); }; i.src = u; })));
  return true;
}
function wrap(ctx, text, maxW) { const w = text.split(' '), out = []; let l = ''; w.forEach(x => { const t = l ? l + ' ' + x : x; if (l && ctx.measureText(t).width > maxW) { out.push(l); l = x; } else l = t; }); out.push(l); return out; }
function scene(t) { return CFG.scenes.find(s => t >= s.start && t < s.end) || CFG.scenes[CFG.scenes.length - 1]; }
function drawBeat(ctx, id, p, a) {
  const { tall, W, H } = F, im = imgs[id]; if (!im) return;
  const capH = tall ? 330 : 200, dw = tall ? 1000 : 1060, k = dw / im.width, dh = im.height * k, top = tall ? 70 : 30, wh = H - capH - top - 20, x = (W - dw) / 2;
  ctx.save(); ctx.globalAlpha = a; ctx.beginPath(); ctx.rect(0, top, W, wh); ctx.clip();
  const y = dh <= wh ? top + (wh - dh) / 2 : top - (dh - wh) * ez(cl((p - .12) / .76));
  ctx.drawImage(im, x, y, dw, dh); ctx.restore();
}
function renderAt(t) {
  const { tall, W, H, ctx } = F, capH = tall ? 330 : 200, s = scene(t), p = cl((t - s.start) / (s.end - s.start));
  ctx.globalAlpha = 1; ctx.fillStyle = '#fff'; ctx.fillRect(0, 0, W, H);
  if (s.id === 'end') {
    const f = cl((t - s.start) / .6); ctx.fillStyle = '#000'; ctx.fillRect(0, 0, W, H); ctx.globalAlpha = f; ctx.textAlign = 'center'; ctx.textBaseline = 'alphabetic';
    ctx.fillStyle = '#fff'; ctx.font = '700 ' + (tall ? 104 : 120) + 'px "Inter Tight"'; const tl = wrap(ctx, CFG.end.title, W - 160); tl.forEach((l, i) => ctx.fillText(l, W / 2, H / 2 - 30 + i * (tall ? 112 : 128)));
    ctx.fillStyle = '#d2d2d2'; ctx.font = '500 ' + (tall ? 38 : 40) + 'px "Inter Tight"'; wrap(ctx, CFG.end.publisher, W - 200).forEach((l, i) => ctx.fillText(l, W / 2, H / 2 + 50 + (tl.length - 1) * (tall ? 112 : 128) + i * 52));
    ctx.fillStyle = '#fff'; ctx.font = '700 ' + (tall ? 46 : 48) + 'px "Inter Tight"'; ctx.fillText(CFG.end.site, W / 2, H / 2 + 190 + (tl.length - 1) * (tall ? 112 : 128)); ctx.globalAlpha = 1; return true;
  }
  const i = CFG.scenes.indexOf(s), xf = .5;
  if (i > 0 && t - s.start < xf && CFG.scenes[i - 1].id !== 'end') { drawBeat(ctx, CFG.scenes[i - 1].id, 1, 1); drawBeat(ctx, s.id, p, ez((t - s.start) / xf)); } else drawBeat(ctx, s.id, p, 1);
  ctx.fillStyle = '#000'; ctx.fillRect(0, H - capH, W, capH);
  const cue = CFG.cues.find(c => t >= c.start && t < c.end);
  if (cue) {
    const a = cl((t - cue.start) / .3) * cl((cue.end - t) / .3); ctx.globalAlpha = a; ctx.fillStyle = '#fff'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    const fs = tall ? 58 : 52; ctx.font = '600 ' + fs + 'px "Inter Tight"'; const L = wrap(ctx, cue.text, W - (tall ? 120 : 220)), lh = fs * 1.25;
    L.forEach((l, j) => ctx.fillText(l, W / 2, H - capH / 2 - (L.length - 1) * lh / 2 + j * lh)); ctx.globalAlpha = 1;
  }
  return true;
}
</script>'''


def render_video(pw, bt):
    cfg = {'beats': {k: 'beat-%s.png' % k for k in bt}, 'scenes': tl['scenes'], 'end': {'title': R['video.end_title'], 'publisher': R['video.end_publisher'], 'site': R['video.end_site']},
           'cues': [{'start': c['start'], 'end': c['end'], 'text': R[c['id']]} for c in tl['cues']]}
    for k, v in bt.items(): shutil.copy(v, site / ('beat-%s.png' % k))
    (site / 'compose.html').write_text(COMPOSER.replace('__CFG__', json.dumps(cfg)))
    for fmt, (w, h) in (('16x9', (1920, 1080)), ('9x16', (1080, 1920))):
        fr = work / ('frames-' + fmt); fr.mkdir(exist_ok=True)
        b = pw.chromium.launch(); pg = b.new_page(viewport={'width': w, 'height': h})
        pg.on('pageerror', lambda e: print('page error:', e))
        pg.goto('http://127.0.0.1:%d/compose.html' % PORT); pg.evaluate('init(%r)' % ('9x16' if fmt == '9x16' else '16x9'))
        n = int(tl['duration'] * FPS)
        import base64
        for i in range(n):
            d = pg.evaluate("(renderAt(%f), document.getElementById('c').toDataURL('image/png'))" % (i / FPS))
            (fr / ('%05d.png' % i)).write_bytes(base64.b64decode(d.split(',')[1]))
            if fmt == '16x9' and i == int(3.0 * FPS):
                from PIL import Image
                Image.open(fr / ('%05d.png' % i)).convert('RGB').resize((1280, 720), Image.LANCZOS).save(MEDIA / 'nodes-networks-poster.jpg', quality=84, optimize=True)
        b.close()
        out = MEDIA / ('nodes-networks-%s.mp4' % fmt)
        subprocess.run(['swift', str(HERE / 'encode.swift'), str(fr), str(out), str(w), str(h), str(FPS), str(KBPS * 1000)], check=True)
        print(out.name, round(out.stat().st_size / 1e6, 1), 'MB')
        shutil.rmtree(fr)


def render_stills(pw, bt):
    from PIL import Image
    im = Image.open(bt['short']).convert('RGB'); w = 1080; k = w / im.width; im = im.resize((w, int(im.height * k)), Image.LANCZOS)
    canvas = Image.new('RGB', (1080, 1350), 'white'); canvas.paste(im, (0, max(0, (1350 - im.height) // 2))); canvas.save(MEDIA / 'nodes-networks-in-short.png', optimize=True)
    pages = [('landing', R['share.title'], R['share.line'], 'governance'), ('chapter1', R['chapter1.name'], R['share.chapter1'], 'governance'), ('chapter2', R['chapter2.name'], R['share.chapter2'], 'ways'), ('chapter3', R['chapter3.name'], R['share.chapter3'], 'history')]
    b = pw.chromium.launch(); pg = b.new_page(viewport={'width': 1200, 'height': 630})
    for name, head, line, tab in pages:
        from PIL import Image as _I
        ci = _I.open(work / ('chart-%s.png' % tab)).convert('RGB')
        if tab == 'history': ci = ci.crop((0, 0, ci.width, int(ci.height * .27)))   # era bars only: the full chart is unreadable at share size
        ci.save(site / ('chart-%s.png' % tab))
        kicker = '' if name == 'landing' else '<div class="k">%s</div>' % B.html.escape(R['share.title'])
        (site / ('og-%s.html' % name)).write_text('<meta charset="utf-8"><style>@font-face{font-family:"Inter Tight";src:url(InterTight-var.woff2);font-weight:500 800}*{box-sizing:border-box}body{margin:0;width:1200px;height:630px;background:#fff;color:#000;font-family:"Inter Tight",Arial,sans-serif;display:flex}'
                       '.t{flex:1;padding:56px 24px 48px 64px;display:flex;flex-direction:column;justify-content:space-between}.k{font:700 22px/1 "Inter Tight";letter-spacing:.08em;text-transform:uppercase;color:#6d6d6d;margin-bottom:16px}'
                       'h1{font:700 %dpx/1.05 "Inter Tight";margin:0 0 20px}p{font:600 30px/1.3 "Inter Tight";margin:0;color:#222}.f{font:500 22px/1.3 "Inter Tight";color:#555}.i{width:520px;padding:55px 64px 55px 0;display:flex;align-items:center}'
                       '.i img{width:100%%;max-height:520px;object-fit:contain;border-radius:6px;background:#000}</style>'
                       '<div class="t"><div>%s<h1>%s</h1><p>%s</p></div><div class="f">%s<br>journalismatlas.com</div></div><div class="i"><img src="http://127.0.0.1:%d/chart-%s.png"></div>'
                       % (60 if name == 'landing' else 52, kicker, B.html.escape(head), B.html.escape(line), B.html.escape(R['video.end_publisher']), PORT, tab))
        pg.goto('http://127.0.0.1:%d/og-%s.html' % (PORT, name), wait_until='networkidle')
        pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(300)
        pg.screenshot(path=str(MEDIA / 'og' / (name + '.png')))
    b.close()


with sync_playwright() as pw:
    bt = beats(pw)
    if ONLY in (None, 'og'): render_stills(pw, bt)
    if ONLY in (None, 'video'): render_video(pw, bt)
shutil.rmtree(work, ignore_errors=True)
print('done ->', MEDIA)
