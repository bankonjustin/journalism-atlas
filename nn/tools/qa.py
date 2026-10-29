#!/usr/bin/env python3
"""LOCAL ONLY. v8 checks: screenshots, headline read, copy round trip, break tests, redirects, framing, forbidden words, video files.
  python3 nn/tools/qa.py        writes into qa/v8/ and prints a pass/fail list."""
import sys, os, re, json, pathlib, shutil, subprocess, tempfile, importlib.util, mimetypes
HERE = pathlib.Path(__file__).resolve().parent; NN = HERE.parent; REPO = NN.parent; OUT = REPO / 'qa' / 'v8'
OUT.mkdir(parents=True, exist_ok=True)
spec = importlib.util.spec_from_file_location('nnbuild', NN / 'build.py'); B = importlib.util.module_from_spec(spec); spec.loader.exec_module(B)
site = pathlib.Path(tempfile.mkdtemp(prefix='nnqa-')); R, T, warns = B.build(site)
results = []
def check(name, ok, detail=''):
    results.append((name, ok, detail)); print(('PASS ' if ok else 'FAIL ') + name + (' | ' + detail if detail else ''))
from playwright.sync_api import sync_playwright
HOST = 'https://journalismatlas.com'
HEADERS = REPO / '_headers'
def csp_for(path):
    """Apply the _headers rules the way Cloudflare does (prefix globs, all matching blocks)."""
    out, cur = {}, None
    for line in HEADERS.read_text().split('\n'):
        if line.startswith('#') or not line.strip(): continue
        if not line.startswith((' ', '\t')): cur = line.strip(); continue
        if cur and (cur == path or (cur.endswith('*') and path.startswith(cur[:-1]))):
            k, v = line.strip().split(': ', 1); out[k] = v
    return out
def serve(route):
    url = route.request.url; path = url[len(HOST):].split('?')[0]
    if path == '/qa-host':
        q = route.request.url.split('?', 1)[1] if '?' in url else ''
        route.fulfill(status=200, content_type='text/html', body='<!doctype html><style>body{margin:0}</style><iframe id="f" src="/nodes-and-networks/explorer/?embed=1&%s" width="760" height="1000" style="border:0;display:block"></iframe><script>addEventListener("message",e=>{var d=e.data;if(d&&d.source==="nn-explorer")document.getElementById("f").style.height=d.height+"px"})</script>' % q); return
    f = site / path.lstrip('/')
    if path.startswith('/assets/') or path in ('/favicon.ico', '/apple-touch-icon.png'): f = REPO / path.lstrip('/')
    if f.is_dir(): f = f / 'index.html'
    if not f.exists(): route.fulfill(status=404, body='not found'); return
    h = csp_for(path if not path.endswith('index.html') else path.rsplit('index.html', 1)[0])
    route.fulfill(status=200, body=f.read_bytes(), content_type=mimetypes.guess_type(str(f))[0] or 'application/octet-stream', headers=h)
TABS = B.TABS; seen_text = []
with sync_playwright() as pw:
    br = pw.chromium.launch()
    def page(w, h=900):
        ctx = br.new_context(viewport={'width': w, 'height': h}); pg = ctx.new_page(); pg.route(HOST + '/**', serve); return pg
    errs = []
    # 1. screenshots
    for w in (1440, 390):
        pg = page(w); pg.on('pageerror', lambda e: errs.append(str(e))); pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
        for name, path in [('landing', '/nodes-and-networks/'), ('embed', '/nodes-and-networks/embed/')] + [('explorer-' + t, '/nodes-and-networks/explorer/?tab=' + t) for t in TABS]:
            pg.goto(HOST + path); pg.wait_for_timeout(1500 if name == 'landing' else 800)
            pg.screenshot(path=str(OUT / ('%s-%d.png' % (name, w))), full_page=True)
            seen_text.append((name, w, pg.evaluate("document.body.innerText"), pg.evaluate("[...document.querySelectorAll('[aria-label],[alt],[title],meta[content]')].map(e=>e.getAttribute('aria-label')||e.getAttribute('alt')||e.getAttribute('title')||e.getAttribute('content')).join(' | ')")))
    pg = page(1000)
    for t in TABS:
        pg.goto(HOST + '/qa-host?tab=' + t); pg.wait_for_timeout(1200); pg.screenshot(path=str(OUT / ('explorer-%s-iframe760.png' % t)), full_page=True)
    check('screenshots: landing, embed, 4 explorer tabs at 1440, 390; 4 tabs in a 760 iframe', len(list(OUT.glob('*.png'))) >= 16)
    check('no page errors or console errors', not [e for e in errs if 'Refused' not in e], '; '.join(errs)[:200])
    # 2. headlines
    md = ['# Headline-only read (v8)\n']
    for name, path in [('Landing', '/nodes-and-networks/'), ('Embed page', '/nodes-and-networks/embed/')] + [('Explorer: ' + t, '/nodes-and-networks/explorer/?tab=' + t) for t in TABS]:
        pg.goto(HOST + path); pg.wait_for_timeout(700)
        hs = pg.evaluate("[...document.querySelectorAll('h1,h2,h3,.top,.chline,.sn,.s,.stat,.enc')].filter(e=>e.offsetParent).map(e=>e.innerText.trim()).filter(Boolean)")
        md.append('## %s\n' % name + '\n'.join('- ' + h for h in hs) + '\n')
    (OUT / 'HEADLINES.md').write_text('\n'.join(md)); check('headline-only read written', True, 'qa/v8/HEADLINES.md')
    # 3. framing
    ok_pg = page(1000); msgs = []; ok_pg.on('console', lambda m: msgs.append(m.text))
    ok_pg.goto(HOST + '/qa-host?tab=short'); ok_pg.wait_for_timeout(1200)
    fr = [f for f in ok_pg.frames if 'explorer' in f.url]
    allowed = bool(fr) and fr[0].evaluate("document.querySelector('main') !== null")
    check('framing: explorer renders in an iframe from journalismatlas.com', allowed, str(csp_for('/nodes-and-networks/explorer/')))
    bad = br.new_context(); bp = bad.new_page(); bm = []; bp.on('console', lambda m: bm.append(m.text))
    bp.route('https://example.com/**', lambda r: r.fulfill(status=200, content_type='text/html', body='<!doctype html><iframe id="f" src="%s/nodes-and-networks/explorer/?embed=1" width="760" height="500"></iframe>' % HOST))
    bp.route(HOST + '/**', serve); bp.goto('https://example.com/x'); bp.wait_for_timeout(1500)
    fr = [f for f in bp.frames if 'explorer' in f.url]; blocked = (not fr) or all(not (lambda f: f.evaluate("!!document.querySelector('main')") if True else 0)(f) for f in fr if not f.is_detached()) if fr else True
    refused = any('frame-ancestors' in m or 'Refused to frame' in m for m in bm)
    check('framing: another origin (example.com) is refused', refused or blocked, 'console refused=%s' % refused)
    asu = br.new_context(); ap = asu.new_page(); am = []; ap.on('console', lambda m: am.append(m.text))
    ap.route('https://www.asu.edu/**', lambda r: r.fulfill(status=200, content_type='text/html', body='<!doctype html><iframe id="f" src="%s/nodes-and-networks/explorer/?embed=1" width="760" height="500"></iframe>' % HOST)); ap.route(HOST + '/**', serve)
    ap.goto('https://www.asu.edu/x'); ap.wait_for_timeout(1500); af = [f for f in ap.frames if 'explorer' in f.url]
    check('framing: an asu.edu page can frame it', bool(af) and af[0].evaluate("!!document.querySelector('main')"))
    br.close()
# 4. copy round trip and break tests
cp = NN / 'content' / 'copy.md'; orig = cp.read_text()
def run_check(): return subprocess.run([sys.executable, str(NN / 'build.py'), '--check'], capture_output=True, text=True)
try:
    cp.write_text(orig.replace('## in_short.top_line\nWho pays for journalism shapes how big it gets.', '## in_short.top_line\nROUNDTRIP TEST LINE.'))
    t2 = pathlib.Path(tempfile.mkdtemp()); r = subprocess.run([sys.executable, str(NN / 'build.py'), '--out', str(t2)], capture_output=True, text=True)
    changed = 'ROUNDTRIP TEST LINE.' in (t2 / 'nodes-and-networks' / 'index.html').read_text() and 'ROUNDTRIP TEST LINE.' in (t2 / 'nodes-and-networks' / 'explorer' / 'index.html').read_text()
    check('copy.md round trip: one string changed, rebuilt, appears on landing and explorer', changed)
    cp.write_text(orig); r = run_check(); check('round trip: reverted and rebuilds clean', r.returncode == 0)
    cp.write_text(orig.replace('## in_short.see_chart\nSee the chart\n\n', '')); r = run_check()
    check('break test: missing string id fails with a readable message', r.returncode != 0 and 'in_short.see_chart' in r.stderr, r.stderr.strip().replace('\n', ' ')[:200])
    cp.write_text(orig.replace('{top_hold} of the', '{top_holdd} of the', 1)); r = run_check()
    check('break test: unknown token fails with a readable message', r.returncode != 0 and 'unknown token {top_holdd}' in r.stderr and 'line' in r.stderr, r.stderr.strip().replace('\n', ' ')[:200])
    cp.write_text(orig.replace('Nine cohorts capture', 'Ten cohorts capture')); r = run_check()
    check('break test: editing a locked paper string fails', r.returncode != 0 and 'quotes the paper' in r.stderr)
    cp.write_text(orig.replace('{n_orgs} organizations. {cohorts_word|cap} cohorts.', '169 organizations. {cohorts_word|cap} cohorts.')); r = subprocess.run([sys.executable, str(NN / 'build.py'), '--check'], capture_output=True, text=True)
    check('hand-typed number warns but builds', r.returncode == 0 and 'typed by hand' in r.stdout, r.stdout.strip().split('\n')[0][:160])
finally:
    cp.write_text(orig)
check('copy.md restored unchanged', cp.read_text() == orig)
# 5. redirects (rule check; Cloudflare itself is checked after deploy)
rules = [l.split() for l in (REPO / '_redirects').read_text().split('\n') if l.startswith('/preview/nn-launch-kit/')]
want = {'/preview/nn-launch-kit/explorer/', '/preview/nn-launch-kit/explorer-named/'}
ok = want <= {r[0] for r in rules} and all(r[1] == '/nodes-and-networks/explorer/' and r[2] == '301' and '?' not in r[1] for r in rules)
check('redirects: both old explorer paths 301 to /nodes-and-networks/explorer/ (no query in target, so Cloudflare keeps the visitor query)', ok, '%d rules' % len(rules))
dist_old = REPO / 'dist' / 'preview' / 'nn-launch-kit'
check('redirects: no old explorer file is left in dist for a redirect to compete with', not (dist_old / 'explorer').exists() and not (dist_old / 'explorer-named').exists() if dist_old.exists() else True)
# 6. forbidden words and brackets
bad = []
for name, w, txt, attrs in seen_text:
    for field, s in (('text', txt), ('attrs', attrs)):
        if re.search(r'placeholder|tbd|[\[\]]', s, re.I): bad.append('%s@%d %s' % (name, w, field))
for k, v in R.items():
    if not k.startswith(('landing.meta', )) and re.search(r'placeholder|tbd|[\[\]]', v, re.I) and k not in ('embed.who',): bad.append('copy ' + k)
vt = (site / 'nodes-and-networks' / 'media' / 'nodes-networks.vtt').read_text()
if re.search(r'placeholder|tbd|[\[\]]', vt, re.I): bad.append('vtt')
check('no public string contains placeholder, TBD, [ or ]', not bad, ', '.join(sorted(set(bad)))[:300])
# 7. video
vids = [(f, f.stat().st_size) for f in sorted((NN / 'media').glob('*.mp4'))]
check('video: both encodes under 25 MB', len(vids) == 2 and all(s < 25e6 for _, s in vids), ', '.join('%s %.1f MB' % (f.name, s / 1e6) for f, s in vids))
meta = []
for f, _ in vids:
    r = subprocess.run(['swift', str(HERE / 'frame.swift'), str(f), str(OUT / 'video' / (f.stem + '-probe.png')), '1'], capture_output=True, text=True); meta.append(r.stdout.strip().split('\n')[-1])
check('video: both encodes open and report length and size', len(meta) == 2 and all('duration' in m for m in meta), ' / '.join(meta))
(OUT / 'RESULTS.md').write_text('# v8 QA results\n\n' + '\n'.join('- %s **%s**%s' % ('PASS' if ok else 'FAIL', n, (' (' + d + ')') if d else '') for n, ok, d in results) + '\n')
shutil.rmtree(site, ignore_errors=True)
sys.exit(0 if all(ok for _, ok, _ in results) else 1)
