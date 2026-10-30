#!/usr/bin/env python3
"""Motion-piece renderer for the N&N launch video ("the turn").
python3 render3.py <explorer_dir_with_index.html> <work_dir> [--fmt 1x1|9x16|16x9] [--upto N]
Beats 1-4, 6, 7: stage built on the explorer's own NN engine/data/layouts (extracted from index.html at render time).
Beat 5: the real explorer, Playwright fake clock. Every number is derived from the explorer's nn-data."""
import sys, json, base64, io, pathlib, threading, functools, http.server
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from stagebuild import build_stage
from PIL import Image, ImageDraw, ImageFont
from playwright.sync_api import sync_playwright
SRC, WORK = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]); WORK.mkdir(parents=True, exist_ok=True)
UPTO = int(sys.argv[sys.argv.index('--upto') + 1]) if '--upto' in sys.argv else None
FMT = sys.argv[sys.argv.index('--fmt') + 1] if '--fmt' in sys.argv else '1x1'
FPS, END = 30, 34000; W, H = {'1x1': (1080, 1080), '9x16': (1080, 1920), '16x9': (1920, 1080)}[FMT]
CAPX, CAPY, CAPW, CAPC = {'1x1': (48, 34, 984, False), '9x16': (48, 270, 984, False), '16x9': (80, 0, 780, True)}[FMT]
FB, FR = '/System/Library/Fonts/Supplemental/Arial Bold.ttf', '/System/Library/Fonts/Supplemental/Arial.ttf'
TL = dict(mir0=3600, flyGov0=4800, flyGov1=6800, flyWays0=12600, flyWays1=14600, beat5=20400, flyHist0=25300, flyHist1=27000, rosette0=30000, rosette1=31800, end=END, ceil=dict(c1=[9000, 10700], c78=[10700, 12500]))
NAMES = [dict(key=k, label=l, t0=a, t1=b, dx=dx, dy=dy) for k, l, a, b, dx, dy in [
    ('Daily Wire', 'The Daily Wire', 14900, 16000, -230, -120), ('Semafor', 'Semafor', 16000, 17100, -60, -160), ('Politico Pro', 'Politico Pro', 17100, 18200, 140, -120),
    ('Marshall Project', 'The Marshall Project', 18200, 19300, 160, -70), ('Texas Tribune', 'Texas Tribune', 19300, 20400, 170, -50)]]
HOVERS = [('New York Times', 21200, 22400), ('States Newsroom', 22400, 23600), ('Defector (Year 5)', 23600, 24800)]
CREDIT = 'Nodes and Networks by Justin Bank for the Knight Center for the Future of News at Arizona State University.'
HND = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(SRC)); HND.log_message = lambda *a, **k: None
srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), HND); PORT = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()
ss = lambda a, b, t: (lambda x: x * x * (3 - 2 * x))(min(1, max(0, (t - a) / (b - a))))
def font(p, s): return ImageFont.truetype(p, int(s))
def wrap(d, t, f, w):
    out, l = [], ''
    for x in t.split(' '):
        s = (l + ' ' + x).strip()
        if d.textlength(s, font=f) > w and l: out.append(l); l = x
        else: l = s
    out.append(l); return out

with sync_playwright() as pw:
    b = pw.chromium.launch()
    # ---------- explorer: derived numbers, History positions + snapshot
    pg = b.new_page(viewport={'width': 760, 'height': 900}, device_scale_factor=2); pg.goto('http://127.0.0.1:%d/index.html?embed=1&tab=history' % PORT); pg.wait_for_function('document.fonts.status==="loaded"'); pg.wait_for_timeout(1200)
    hp = pg.evaluate("(()=>{const h=document.querySelector('#hist').getBoundingClientRect(),o={};document.querySelectorAll('#hist .mk').forEach(g=>{const r=g.querySelector('.ring').getBoundingClientRect();o[g.dataset.i]=[r.left+r.width/2-h.left,r.top+r.height/2-h.top]});return {o,w:h.width,h:h.height}})()")
    LN = pg.evaluate("""(()=>{const h=document.querySelector('#hist').getBoundingClientRect(),ls=[...document.querySelectorAll('#hsvg line')].filter(l=>l.getAttribute('stroke')==='#fff'&&l.getAttribute('stroke-width')==='3');
      const segs=ls.map(l=>{const r=l.getBoundingClientRect();return [r.left+r.width/2-h.left,r.top-h.top,r.bottom-h.top]});ls.forEach(l=>l.style.display='none');
      const bars=[...document.querySelectorAll('#hsvg g[role=img]')].map(g=>g.getBoundingClientRect().bottom-h.top);
      return {segs,barsBottom:Math.max(...bars)}})()""")
    hist_png = Image.open(io.BytesIO(pg.locator('#hist').screenshot())).convert('RGB'); pg.close()
    pg = b.new_page(viewport={'width': 760, 'height': 900}); pg.goto('http://127.0.0.1:%d/index.html?embed=1' % PORT)
    DER = pg.evaluate("""(()=>{const D=JSON.parse(document.getElementById('nn-data').textContent),N=D.nodes,o10=n=>n.o!=='NEVER_CROSSED';
      const c1=N.filter(n=>n.c==='C1'),c78=N.filter(n=>n.c==='C7'||n.c==='C8');
      return {T:N.length,G:N.filter(n=>n.o==='CROSSED').length,c1o:c1.filter(o10).length,c1n:c1.length,c78o:c78.filter(o10).length,c78n:c78.length}})()"""); pg.close()
    T, G = DER['T'], DER['G']
    mp = b.new_page(viewport={'width': 760, 'height': 900}); mp.goto('http://127.0.0.1:%d/index.html?embed=1&tab=ways' % PORT)
    mp.add_style_tag(content='#title,#sent,#stat,#legend,#pos,#hint,#take,.credit,header{display:none!important} #list{position:absolute!important;left:-9999px!important}'); mp.wait_for_timeout(1200)
    clip = mp.evaluate("(()=>{const t=document.querySelector('#tabs').getBoundingClientRect(),e=document.querySelector('#stage').getBoundingClientRect();return {x:8,y:t.top,w:e.width,h:e.bottom-t.top,pt:e.top-t.top,sh:e.height}})()"); mp.close()
    if FMT == '1x1': s_ = min(W / clip['w'], (H - 240) / clip['h']); ox0 = (W - clip['w'] * s_) / 2; oy0 = 240
    elif FMT == '9x16': s_ = 1.38; ox0 = (W - clip['w'] * s_) / 2; oy0 = 1100 - (clip['pt'] + clip['sh'] / 2) * s_
    else: s_ = 1.35; ox0 = W - 60 - clip['w'] * s_; oy0 = (H - clip['h'] * s_) / 2
    REST = {'cx': ox0 + clip['w'] / 2 * s_, 'cy': oy0 + (clip['pt'] + clip['sh'] / 2) * s_, 'R': .4 * clip['sh'] * s_}
    CAPS = [  # head cues, sub cues  (start, end, text, fade_in_ms, size)
        ('H', 0, 3900, 'American journalism no longer runs as a set of integrated newsrooms.', 0),
        ('H', 5000, 8600, 'Sort %d organizations by governance, and the field breaks into nine cohorts.' % T, 300),
        ('H', 8700, 12600, 'Governance sets ceilings.', 300),
        ('S', 9000, 12600, '%d of %d legacy publishers top $10 million. %d of %d co-ops and civic organizations do.' % (DER['c1o'], DER['c1n'], DER['c78o'], DER['c78n']), 300),
        ('H', 13000, 20400, '%d grew past $10 million. Each did it one of six ways.' % G, 300),
        ('H', 21000, 24900, 'Zoom in to the individual organization.', 300),
        ('H', 25500, 29900, 'When they started matters. Governance predicts even more.', 300),
        ('H', 30100, END, 'Explore the cohorts and what they reveal.', 300),
        ('S', 30100, END, CREDIT, 300)]
    json.dump({'CAPS': CAPS, 'TL': TL, 'DER': DER}, open(WORK / 'schedule.json', 'w'), indent=1)
    # ---------- stage frames
    if FMT == '1x1': HTOP = 246; HS = (H - HTOP - 14) / hp['h']; HOX = (W - hp['w'] * HS) / 2; ZH = H - HTOP - 14; ZX, ZWD = 0, W
    elif FMT == '9x16': HTOP = 580; HS = (1520 - HTOP) / hp['h']; HOX = (W - hp['w'] * HS) / 2; ZH = 1520 - HTOP; ZX, ZWD = 0, W
    else: HTOP = 40; HS = (H - 80) / hp['h']; HOX = W - hp['w'] * HS - 80; ZH = H - 80; ZWD = 1060; ZX = W - ZWD - 50
    pth = build_stage(SRC / 'index.html', WORK, TL, [], W, H, REST)
    sp = b.new_page(viewport={'width': 1100, 'height': 1100}); sp.goto('file://' + str(pth.resolve())); sp.wait_for_function('window.ready===true')
    idxs = sp.evaluate("n=>n.map(k=>N.findIndex(x=>x.nm.includes(k)))", [o['key'] for o in NAMES])
    for o, i in zip(NAMES, idxs): o['i'] = i
    pth = build_stage(SRC / 'index.html', WORK, TL, NAMES, W, H, REST); sp.goto('file://' + str(pth.resolve())); sp.wait_for_function('window.ready===true')
    sp.evaluate("a=>setHist(...a)", [hp['o'], HS, HOX, HTOP, 4.3])
    placement = sp.evaluate("placement()"); json.dump(placement, open(WORK / 'placement.json', 'w'), indent=1)
    # ---------- real explorer pass (beat 5)
    EP = {}
    ep = b.new_context(viewport={'width': 760, 'height': 900}, device_scale_factor=2).new_page(); ep.clock.install(time=0)
    ep.goto('http://127.0.0.1:%d/index.html?embed=1&tab=ways' % PORT)
    ep.add_style_tag(content='#title,#sent,#stat,#legend,#pos,#hint,#take,.credit,header{display:none!important} #list{position:absolute!important;left:-9999px!important} html,body{background:#000!important}')
    ep.clock.run_for(900); ep.wait_for_function('document.fonts.status==="loaded"'); ep.clock.run_for(800)
    pts = {nm: ep.evaluate("n=>window.NNX.pt(n)", nm) for nm, _, _ in HOVERS}; assert all(pts.values()), pts
    first = pts[HOVERS[0][0]]; mpos = [first['x'] + 110, first['y'] - 160]
    f0, f1 = int(TL['beat5'] * FPS / 1000), int(TL['flyHist0'] * FPS / 1000)
    for i in range(f0, f1 + 1):
        t = i * 1000 / FPS
        if i > f0: ep.clock.run_for(round(i * 1000 / FPS) - round((i - 1) * 1000 / FPS))
        tgt = None; cur_vis = False
        for nm, a, e in HOVERS:
            if a - 400 <= t < e: tgt = pts[nm]; ts = a - 400; break
        if tgt is not None:
            u = ss(0, 450, t - ts); prev = mpos  # glide from previous mouse pos to target
            if t < ts + 460: mpos0 = getattr(sys.modules[__name__], '_m0', mpos)
            mx = mpos[0] + (tgt['x'] - mpos[0]) * u; my = mpos[1] + (tgt['y'] - mpos[1]) * u
            ep.mouse.move(mx, my); cur_vis = True; cur_xy = (mx, my)
            if u >= 1: mpos = [tgt['x'], tgt['y']]
        elif t >= 24800 and mpos is not None:
            ep.mouse.move(5, 5)
        # zoom: ease in with the first hover, hold, ease out by 25100..25600
        z = 1 + .55 * ss(20800, 21500, t) * (1 - ss(24500, 25000, t))
        png = ep.screenshot(clip={'x': clip['x'], 'y': clip['y'], 'width': clip['w'], 'height': clip['h']})
        EP[i] = (Image.open(io.BytesIO(png)).convert('RGB'), z, (cur_xy if cur_vis else None))
    b.close()

def explorer_img(i):
    im, z, cxy = EP[i]; cw, ch = im.size
    if cxy: fx, fy = (cxy[0] - clip['x']) * 2, (cxy[1] - clip['y']) * 2
    else: fx, fy = cw / 2, ch / 2
    ww, wh = cw / z, ch / z; x0 = min(max(0, fx - ww / 2), cw - ww); y0 = min(max(0, fy - wh / 2 - 40 * (z - 1)), ch - wh)
    c = im.crop((int(x0), int(y0), int(x0 + ww), int(y0 + wh))).resize((int(clip['w'] * s_), int(clip['h'] * s_)), Image.LANCZOS)
    out = Image.new('RGB', (W, H), 'black'); ox = int(ox0); oy = int(oy0); out.paste(c, (ox, oy))
    if cxy:
        d = ImageDraw.Draw(out, 'RGBA'); px = ox + ((cxy[0] - clip['x']) * 2 - x0) / 2 * s_ * z * 0 + ((cxy[0] - clip['x']) * 2 - x0) * (c.width / ww); py = oy + ((cxy[1] - clip['y']) * 2 - y0) * (c.height / wh)
        k = 2.1; pts_ = [(0, 0), (0, 17), (4.2, 13.4), (7.2, 20), (9.8, 18.9), (6.9, 12.5), (12.4, 12.5)]; poly = [(px + a * k, py + b2 * k) for a, b2 in pts_]
        d.polygon([(a + 2, b2 + 3) for a, b2 in poly], fill=(0, 0, 0, 70)); d.polygon(poly, fill='white'); d.line(poly + [poly[0]], fill='black', width=3)
    return out

def caption(im, t, w=0):
    d = ImageDraw.Draw(im); items = []
    def colr(a, kind): return tuple(int(((255 if kind == 'h' else 189) * a)) for _ in range(3))
    for kind, s0, e0, txt, fi in CAPS:
        if kind != 'H' or not (s0 <= t < e0): continue
        a = 1.0 if s0 == 0 else min(1, (t - s0) / fi) if fi else 1.0
        maxl = 4 if CAPC else 2
        fs = 62; f = font(FB, fs); L_ = wrap(d, txt, f, CAPW)
        if len(L_) > maxl: fs = 54 if not CAPC else 52; f = font(FB, fs); L_ = wrap(d, txt, f, CAPW)
        if len(L_) == 1:
            fs = 68
            while d.textlength(txt, font=font(FB, fs)) > CAPW: fs -= 2
            f = font(FB, fs)
        for l in L_: items.append((l, f, colr(a, 'h'), int(fs * 1.12)))
        items.append(('', f, (0, 0, 0), 4))
    for kind, s0, e0, txt, fi in CAPS:
        if kind != 'S' or not (s0 <= t < e0): continue
        a = min(1, (t - s0) / fi) if fi else 1.0; fs = 36 if txt == CREDIT else 42; f = font(FR, fs)
        for l in wrap(d, txt, f, CAPW): items.append((l, f, colr(a, 's'), int(fs * 1.26)))
    tot = sum(i[3] for i in items); y = (H - tot) / 2 if CAPC else CAPY
    for l, f, c, lh in items:
        if l: d.text((CAPX, y), l, font=f, fill=c)
        y += lh

def flipw(t):
    if t < TL['beat5']: return 0.0
    if t < 21000: return ss(TL['beat5'], 21000, t)
    if t < 24800: return 1.0
    if t < 25300: return 1 - ss(24800, 25300, t)
    return 0.0
def histA(t):
    if t < 26800: return 0.0
    if t < TL['rosette0']: return ss(26800, 27300, t)
    return 1 - ss(TL['rosette0'], TL['rosette0'] + 450, t)
HW, HH = hp['w'], hp['h']; SEGS = sorted(LN['segs'], key=lambda q: q[1]); Y0, Y1 = SEGS[0][1], max(q[2] for q in SEGS); BB = LN['barsBottom']
def hist_view(t):
    kz = ss(27300, 28300, t) * (1 - ss(29400, 30000, t))
    sh = HH + (ZH * HW / ZWD - HH) * kz
    dw, dh = HW * HS + (ZWD - HW * HS) * kz, HH * HS + (ZH - HH * HS) * kz; dx = HOX + (ZX - HOX) * kz
    return kz, (dx, HTOP, dw, dh), (0, 0, HW, sh)
def hist_layer(t):
    kz, (dx, dy, dw, dh), (sx, sy, sw, sh) = hist_view(t); k2 = 2
    img = hist_png.crop((int(sx * k2), int(sy * k2), int((sx + sw) * k2), int((sy + sh) * k2))).resize((int(dw), int(dh)), Image.LANCZOS)
    f = dw / sw; d = ImageDraw.Draw(img, 'RGBA')
    if kz > 0 and int((BB + 8) * f) < img.height - 1: d.rectangle((0, int((BB + 8) * f), img.width, img.height), fill=(0, 0, 0, int(150 * kz)))
    yc = Y0 + (Y1 - Y0) * ss(27600, 28900, t)
    if t >= 27600:
        for x, a, b2 in SEGS:
            if a > yc: continue
            d.line([(x * f, a * f), (x * f, min(b2, yc) * f)], fill=(255, 255, 255, 255), width=max(2, int(3 * f)))
    return img, (int(dx), int(dy))
OUT = WORK / 'frames'; OUT.mkdir(exist_ok=True)
with sync_playwright() as pw:
    b = pw.chromium.launch(); sp = b.new_page(viewport={'width': 1100, 'height': 1100}); sp.goto('file://' + str(pth.resolve())); sp.wait_for_function('window.ready===true')
    sp.evaluate("a=>setHist(...a)", [hp['o'], HS, HOX, HTOP, 4.3])
    n = END * FPS // 1000
    for i in range(n):
        if UPTO is not None and i > UPTO: break
        t = i * 1000 / FPS
        st = Image.open(io.BytesIO(base64.b64decode(sp.evaluate("t=>renderAt(t)", t)))).convert('RGB')
        ha = histA(t)
        if ha > 0:
            hl_, (px, py) = hist_layer(t)
            st.paste(hl_, (px, py)) if ha >= .999 else st.paste(Image.blend(st.crop((px, py, px + hl_.width, py + hl_.height)), hl_, ha), (px, py))
        w = flipw(t)
        if w > 0 and i in EP: st = Image.blend(st, explorer_img(i), w)
        caption(st, t, 0)
        st.save(OUT / ('%04d.png' % i))
        if i % 60 == 0: print('frame', i, flush=True)
    sp.evaluate("t=>1", 0)
    pst = Image.open(io.BytesIO(base64.b64decode(sp.evaluate("t=>renderAt(t)", 33400)))).convert('RGB')
    CAPS_SAVE = list(CAPS); CAPS[:] = [c for c in CAPS if c[0] == 'H' and c[3].startswith('Explore')]; CAPS[0] = (CAPS[0][0], 0, END, CAPS[0][3], 0)
    caption(pst, 100, 0); CAPS[:] = CAPS_SAVE; pst.save(WORK / 'poster.png')
    b.close()
print('done')
