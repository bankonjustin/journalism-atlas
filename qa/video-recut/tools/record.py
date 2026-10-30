#!/usr/bin/env python3
"""Deterministic recorder for the N&N launch video (1:1 first).
python3 record.py <explorer_dir> <out_frames_dir> [--upto N]
Drives the REAL explorer (embed mode, 2x DPR) with Playwright's fake clock, so each frame is an exact 1/30 s step.
Numbers are derived from the explorer's embedded nn-data JSON. Captions/cursor/end card are composited in PIL."""
import sys, json, threading, functools, http.server, pathlib, io, math
from PIL import Image, ImageDraw, ImageFont
from playwright.sync_api import sync_playwright
SRC, OUT = sys.argv[1], pathlib.Path(sys.argv[2]); OUT.mkdir(parents=True, exist_ok=True)
UPTO = int(sys.argv[sys.argv.index('--upto') + 1]) if '--upto' in sys.argv else None
FMT = (sys.argv[sys.argv.index('--fmt') + 1] if '--fmt' in sys.argv else '1x1')
FPS, DUR = 30, 30000
S = 1080
FB, FR = '/System/Library/Fonts/Supplemental/Arial Bold.ttf', '/System/Library/Fonts/Supplemental/Arial.ttf'
BAND = 240
HIDE = '#title,#sent,#stat,#legend,#pos,#hint,#take,.credit,header{display:none!important} #list{position:absolute!important;left:-9999px!important} html,body{background:#fff!important}'

H = functools.partial(http.server.SimpleHTTPRequestHandler, directory=SRC); H.log_message = lambda *a, **k: None
srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), H); PORT = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()

def font(p, s): return ImageFont.truetype(p, int(s))
def wrap(d, t, f, w):
    out, l = [], ''
    for x in t.split(' '):
        s = (l + ' ' + x).strip()
        if d.textlength(s, font=f) > w and l: out.append(l); l = x
        else: l = s
    out.append(l); return out

with sync_playwright() as pw:
    b = pw.chromium.launch(); ctx = b.new_context(viewport={'width': 760, 'height': 900}, device_scale_factor=2)
    pg = ctx.new_page(); pg.clock.install(time=0)
    pg.goto('http://127.0.0.1:%d/index.html?embed=1&tab=ways' % PORT)
    pg.add_style_tag(content=HIDE)
    pg.clock.run_for(900); pg.wait_for_function('document.fonts.status==="loaded"')
    pg.clock.run_for(600)
    # ---- derive every number from the explorer's data
    D = pg.evaluate("""(()=>{const D=JSON.parse(document.getElementById('nn-data').textContent),N=D.nodes;
      const rows=[...document.querySelectorAll('#list .li')].map(li=>({key:li.dataset.key,txt:li.innerText.replace(/\\s+/g,' ').trim()}));
      return {T:N.length,A:N.filter(n=>n.o==='INHERITED').length,G:N.filter(n=>n.o==='CROSSED').length,U:N.filter(n=>n.o==='NEVER_CROSSED').length,
        F08:N.filter(n=>n.fy&&n.fy>=2008).length,rows}})()""")
    T, A, G, U, F08 = D['T'], D['A'], D['G'], D['U'], D['F08']
    gov_rows = None
    pg.evaluate("window.NNX.go('governance')"); pg.clock.run_for(2000)
    gov_rows = pg.evaluate("[...document.querySelectorAll('#list .li')].map(li=>({key:li.dataset.key,txt:li.innerText.replace(/\\s+/g,' ').trim()}))")
    pg.evaluate("window.NNX.go('ways')"); pg.clock.run_for(2000)
    assert len(gov_rows) == 9, gov_rows
    cohorts = []
    for r in gov_rows:  # "C1 · Legacy Publishers 18"
        code_name, n = r['txt'].rsplit(' ', 1); cohorts.append((code_name, int(n)))
    SMALL = {int(n) for _, n in cohorts if int(n) < 10}
    # ---- schedule (ms)
    sweep, t0 = [], 4500
    for code_name, n in cohorts:
        d = 900 if n < 10 else 500; sweep.append((t0, t0 + d, code_name, '%d organizations' % n)); t0 += d
    SW_END = t0
    HEAD = [(0, 2500, '169 organizations.'.replace('169', str(T)), 0), (2500, 4500, 'Now sort by governance.', 250)]
    SUB = [(3300, 4500, 'Nine kinds of newsroom, sorted by who pays.', 250)]
    for s, e, h, sub in sweep: HEAD.append((s, e, h, 0)); SUB.append((s, e, sub, 0))
    HEAD += [(SW_END, 12500, 'Governance determines so much.', 250), (12500, 18500, 'How they got past $10M.', 250),
             (18500, 21500, 'Hover any mark.', 250), (21500, 26000, 'When they started.', 250)]
    SUB += [(14300, 16000, '%d started above it. %d grew past it. %d are still under.' % (A, G, U), 250), (16000, 18500, 'All %d did it one of six ways.' % G, 250),
            (18500, 21500, 'Meet the organization behind it.', 250), (21500, 26000, '%d of %d started in 2008 or later.' % (F08, T), 250)]
    END_HEAD, END_SUB = 'Explore all %d organizations' % T, 'Nodes and Networks by Justin Bank for the Knight Center for the Future of News at Arizona State University.'
    json.dump({'HEAD': HEAD, 'SUB': SUB, 'END': [END_HEAD, END_SUB], 'derived': {'T': T, 'A': A, 'G': G, 'U': U, 'F08': F08, 'cohorts': cohorts}}, open(OUT.parent / ('schedule-%s.json' % FMT), 'w'), indent=1)
    TAB = {2500: 'governance', 12500: 'ways', 21500: 'history'}

    def layout():
        r = pg.evaluate("""(()=>{const t=document.querySelector('#tabs').getBoundingClientRect(),st=document.querySelector('#stage'),h=document.querySelector('#hist');
          const hv=!h.hidden&&h.getBoundingClientRect().height>0, e=(hv?h:st).getBoundingClientRect(); const bot=hv?Math.min(e.bottom,e.top+600):e.bottom; return {x:8,y:t.top,w:e.width,h:bot-t.top,hv}})()""")
        return r
    def chart(clip):
        png = pg.screenshot(clip={'x': clip['x'], 'y': clip['y'], 'width': clip['w'], 'height': clip['h']})
        return Image.open(io.BytesIO(png)).convert('RGB')
    def alpha_of(t, s, e, fi, fo=0):
        a = 1.0
        if fi and t < s + fi: a = min(a, max(0, (t - s) / fi))
        if fo and t > e - fo: a = min(a, max(0, (e - t) / fo))
        return a
    def draw_caption(im, t):
        d = ImageDraw.Draw(im)
        hs = [(h, a) for (s, e, h, fi) in HEAD if s <= t < e for a in [1.0 if s == 0 else alpha_of(t, s, e, fi)]]
        ss = [(h, a) for (s, e, h, fi) in SUB if s <= t < e for a in [alpha_of(t, s, e, fi)]]
        y = 34
        for txt, a in hs:
            sz = 68
            while d.textlength(txt, font=font(FB, sz)) > S - 96: sz -= 2
            col = int(255 * (1 - a)); d.text((48, y), txt, font=font(FB, sz), fill=(col, col, col)); hy = y + int(sz * 1.12)
        for txt, a in ss:
            f = font(FR, 44); col = int(51 + 204 * (1 - a)); yy = 34 + int(68 * 1.12) + 6
            for l in wrap(d, txt, f, S - 96): d.text((48, yy), l, font=f, fill=(col, col, col)); yy += 54
    def cursor(im, x, y):
        d = ImageDraw.Draw(im, 'RGBA'); k = 2.1
        pts = [(0, 0), (0, 17), (4.2, 13.4), (7.2, 20), (9.8, 18.9), (6.9, 12.5), (12.4, 12.5)]
        pts = [(x + px * k, y + py * k) for px, py in pts]
        d.polygon([(px + 2, py + 3) for px, py in pts], fill=(0, 0, 0, 70)); d.polygon(pts, fill='white', outline='black')
        d.line(pts + [pts[0]], fill='black', width=3)
    def end_card(t):
        im = Image.new('RGB', (S, S), 'black'); d = ImageDraw.Draw(im); hf = font(FB, 92)
        y = 290
        for l in wrap(d, END_HEAD, hf, S - 160): d.text((80, y), l, font=hf, fill='white'); y += 108
        y += 36; sf = font(FR, 42)
        for l in wrap(d, END_SUB, sf, S - 160): d.text((80, y), l, font=sf, fill=(215, 215, 215)); y += 54
        return im

    ev = dict(TAB); frames = 0; mouse = None; prev_tab_img = None; fade_from = None
    sweep_state = {'i': -1}; cur_clip = None; t_prev = 0; mpath = None; last_content = None
    for i in range(0, FPS * DUR // 1000):
        t = i * 1000 / FPS
        if UPTO is not None and i > UPTO: break
        if i:
            dt = round(i * 1000 / FPS) - round((i - 1) * 1000 / FPS); pg.clock.run_for(dt)
        # events
        for et in list(ev):
            if t >= et:
                tab = ev.pop(et)
                if tab == 'history': fade_from = (i, last_content.copy() if last_content else None)
                pg.evaluate("document.getElementById('t-%s').click()" % tab)
        # cohort sweep via the explorer's own legend hover handler
        k = next((j for j, (s, e, _, _) in enumerate(sweep) if s <= t < e), -1)
        if k != sweep_state['i']:
            pg.evaluate("""k=>{const L=[...document.querySelectorAll('#list .li')];L.forEach(l=>l.dispatchEvent(new PointerEvent('pointerleave',{bubbles:false,pointerType:'mouse'})));if(k>=0)L[k].dispatchEvent(new PointerEvent('pointerenter',{bubbles:false,pointerType:'mouse'}))}""", k)
            sweep_state['i'] = k
        # hover beat: cursor to Politico Pro
        cur_xy = None
        if 18500 <= t < 21500:
            if mpath is None:
                tgt = pg.evaluate("window.NNX.pt('Politico Pro')"); mpath = (tgt['x'] + 120, tgt['y'] - 190, tgt['x'], tgt['y'])
            u = min(1, (t - 18500) / 1300); e_ = u * u * (3 - 2 * u)
            mx, my = mpath[0] + (mpath[2] - mpath[0]) * e_, mpath[1] + (mpath[3] - mpath[1]) * e_
            pg.mouse.move(mx, my); cur_xy = (mx, my)
        elif mpath is not None and t >= 21500:
            pg.mouse.move(5, 5); mpath = None
        if t >= 26000: im = end_card(t)
        else:
            clip = layout(); cur_clip = clip
            c = chart(clip); h_ = clip['h']; s_ = min(S / clip['w'], (S - BAND) / h_)
            c = c.resize((int(clip['w'] * s_), int(h_ * s_)), Image.LANCZOS)
            im = Image.new('RGB', (S, S), 'white'); ox = (S - c.width) // 2; im.paste(c, (ox, BAND))
            last_content = im.copy()
            if fade_from and i - fade_from[0] < 12 and fade_from[1] is not None:
                im = Image.blend(fade_from[1], im, (i - fade_from[0] + 1) / 12)
            draw_caption(im, t)
            if cur_xy: cursor(im, ox + (cur_xy[0] - clip['x']) * s_, BAND + (cur_xy[1] - clip['y']) * s_)
            if t >= 25600:  # fade into end card
                im = Image.blend(im, end_card(t), min(1, (t - 25600) / 400))
        im.save(OUT / ('%04d.png' % i))
        if i % 60 == 0: print('frame', i, flush=True)
    b.close()
print('done')
