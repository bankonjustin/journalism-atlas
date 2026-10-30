#!/usr/bin/env python3
"""Embed sizing checks for the N&N explorer. Needs servers: 8801 (repo root = explorer origin), 8802 (qa/nn-final-oct29/host = cross-origin white host).
   python3 qa/nn-final-oct29/sizing.py"""
import json, pathlib, sys
from playwright.sync_api import sync_playwright
OUT = pathlib.Path(__file__).parent / 'shots'; OUT.mkdir(exist_ok=True)
HOST = 'http://localhost:8802/'
TABS = ['governance', 'ways', 'history']; WIDTHS = [320, 375, 430, 600, 760]
res = []; rows = []
def run(br, tab, host_w, scheme, shot=None, noembed=False):
    ctx = br.new_context(viewport={'width': host_w, 'height': 900}, color_scheme=scheme, device_scale_factor=1)
    pg = ctx.new_page(); errs = []; pg.on('pageerror', lambda e: errs.append(str(e))); pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
    pg.goto(HOST + '?tab=' + tab + ('&noembed=1' if noembed else '')); fr = pg.frame_locator('iframe'); fr.locator('#tabs .tab').first.wait_for(); pg.wait_for_timeout(700)
    f = [x for x in pg.frames if x != pg.main_frame][0]
    m = f.evaluate('''() => { const de = document.documentElement, main = document.querySelector('main'), r = main.getBoundingClientRect();
      const over = [...document.querySelectorAll('main *')].filter(e => { const b = e.getBoundingClientRect(); return b.width && (b.right > de.clientWidth + .5 || b.left < -.5) && !e.closest('svg') && !e.classList.contains('sr') }).map(e => e.tagName + '.' + e.className).slice(0, 5);
      const svg = document.querySelector('#hist svg'); let sv = [];
      if (svg && !document.getElementById('hist').hidden) { const sr = svg.getBoundingClientRect(); sv = [...svg.querySelectorAll('text')].filter(t => { const b = t.getBoundingClientRect(); return b.left < sr.left - .5 || b.right > sr.right + .5 }).map(t => t.textContent).slice(0, 5) }
      return { h: Math.ceil(r.bottom + scrollY), sw: de.scrollWidth, cw: de.clientWidth, sh: de.scrollHeight, ch: de.clientHeight, over, svgClip: sv, embed: de.classList.contains('embed'), font: getComputedStyle(document.body).fontFamily.slice(0, 20), bg: getComputedStyle(document.body).backgroundColor, hist: !document.getElementById('hist').hidden } }''')
    fw = pg.eval_on_selector('iframe', 'e => e.getBoundingClientRect().width'); fh = pg.eval_on_selector('iframe', 'e => e.getBoundingClientRect().height')
    # tooltip in frame: hover/tap a mark near the right edge and a left one
    tipok = None
    try:
        if tab == 'history':
            n = f.locator('#hsvg .mk').count(); tl = []
            for idx in (0, n // 3, n - 1):
                mk = f.locator('#hsvg .mk').nth(idx); mk.scroll_into_view_if_needed(); box = mk.bounding_box(); cx, cy = box['x'] + box['width'] / 2, box['y'] + box['height'] / 2; pg.mouse.move(cx - 25, cy); pg.mouse.move(cx, cy, steps=5); pg.wait_for_timeout(80)
                tl.append(f.evaluate('() => { const t = document.getElementById("htip"), b = t.getBoundingClientRect(); return t.hidden ? null : [b.left, b.right, document.documentElement.clientWidth] }'))
            tipok = all(t and t[0] >= -.5 and t[1] <= t[2] + .5 for t in tl) or ('tl=' + json.dumps(tl))
        else:
            tl = []
            for nm in ('New York Times', 'Axios', 'ProPublica', 'Joe Rogan Experience'):
                pt = f.evaluate('(n) => window.NNX.pt(n)', nm)
                if not pt: continue
                f.evaluate('window.scrollTo(0,0)'); fo = pg.eval_on_selector('iframe', 'e => { const b = e.getBoundingClientRect(); return [b.left, b.top] }')
                pg.mouse.move(fo[0] + pt['x'], fo[1] + pt['y']); pg.wait_for_timeout(80)
                tl.append(f.evaluate('() => { const t = document.getElementById("tip"), b = t.getBoundingClientRect(); return t.hidden ? null : [b.left, b.right, document.documentElement.clientWidth] }'))
            tipok = bool(tl) and all(t and t[0] >= -.5 and t[1] <= t[2] + .5 for t in tl)
    except Exception as e: tipok = 'ERR ' + str(e)[:80]
    if shot: pg.screenshot(path=str(OUT / shot), full_page=False)
    ctx.close()
    return m, fw, fh, tipok, errs
with sync_playwright() as pw:
    br = pw.chromium.launch(); bad = 0
    for tab in TABS:
        for w in WIDTHS + [1400]:
            for scheme in (['light', 'dark'] if w in (375, 1400) else ['light']):
                shot = f'{tab}-{w}{"-darkOS" if scheme == "dark" else ""}.png' if (w in (375, 760, 1400) or scheme == 'dark') else None
                m, fw, fh, tipok, errs = run(br, tab, w, scheme, shot)
                ok = m['h'] <= 1650 and m['sw'] <= m['cw'] and m['sh'] <= m['ch'] and not m['over'] and not m['svgClip'] and tipok is True and m['embed'] and m['font'].startswith('Arial') and not errs and fh == 1650 and fw <= 760
                bad += not ok
                print(('PASS' if ok else 'FAIL'), tab, 'host', w, scheme, 'iframe', fw, 'x', fh, '| content h', m['h'], '| sw/cw', m['sw'], m['cw'], '| sh/ch', m['sh'], m['ch'], '| over', m['over'], m['svgClip'], '| tip', tipok, '|', m['font'], m['bg'], errs[:2])
                rows.append({'tab': tab, 'host': w, 'scheme': scheme, 'iframe_w': fw, 'h': m['h'], 'ok': ok})
    # cross-origin trigger without ?embed=1
    for tab in TABS:
        m, fw, fh, tipok, errs = run(br, tab, 375, 'light', None, noembed=True); ok = m['embed'] and m['font'].startswith('Arial') and m['h'] <= 1650; bad += not ok
        print(('PASS' if ok else 'FAIL'), 'no ?embed=1 (cross-origin trigger)', tab, 'embed class', m['embed'], m['font'], m['h'])
    br.close()
json.dump(rows, open(OUT.parent / 'sizing.json', 'w'), indent=1)
print('FAILURES', bad)
