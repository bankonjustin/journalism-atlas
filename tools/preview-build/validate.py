#!/usr/bin/env python3
"""Playwright validation for the preview page. Runs against dist/ (the output of
build-dist.sh, i.e. exactly what Cloudflare would serve), over a local HTTP server.

Writes validation.json and screenshots/. Exit code 1 if any check fails.
Reads comments.xml from the docx only to prove none of it leaked into the page.
"""
import functools
import http.server
import json
import re
import sys
import threading
import zipfile
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
CFG = json.loads((HERE / 'config.json').read_text())
REPO = (HERE / CFG['site_root']).resolve()
DIST = REPO / 'dist'
CONTENT = json.loads((HERE / 'content' / 'content.json').read_text())
REPORT = json.loads((HERE / 'build_report.json').read_text())
EXP = CFG['expected']
SHOTS = HERE / 'screenshots'
FIG_SKIP = 'figure, .cohort-strip'

results = []


def check(name, ok, detail=''):
    results.append({'check': name, 'pass': bool(ok), 'detail': detail})
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f' — {detail}' if detail else ''))


def words(s):
    return s.split()


def block_text(b):
    return ''.join(r.get('t', ' ' if r.get('br') else '') for r in b.get('runs', []))


def norm(s):
    return ' '.join(s.split())


def serve():
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(DIST))
    handler.log_message = lambda *a: None
    srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv


def docx_comments():
    z = zipfile.ZipFile(Path(CFG['docx']).expanduser())
    if 'word/comments.xml' not in z.namelist():
        return []
    xml = z.read('word/comments.xml').decode()
    out = []
    for body in re.findall(r'<w:comment [^>]*>(.*?)</w:comment>', xml, re.S):
        t = ''.join(re.findall(r'<w:t[^>]*>([^<]*)</w:t>', body)).strip()
        if t:
            out.append(t)
    return out


def served_path_checks():
    slug_dir = DIST / 'preview' / CFG['slug']
    check('served: page exists in dist/', (slug_dir / 'index.html').exists(), str(slug_dir.relative_to(REPO)))
    under_preview = [p for p in (DIST / 'preview').rglob('*') if p.is_file()]
    bad = [str(p.relative_to(DIST)) for p in under_preview
           if p.name != 'index.html' or p.suffix.lower() in ('.docx', '.csv', '.json', '.md')]
    check('served: only index.html under /preview/', not bad, ', '.join(bad) or f'{len(under_preview)} file(s)')
    leaks = [str(p.relative_to(DIST)) for p in DIST.rglob('*') if p.is_file() and (
        p.suffix.lower() in ('.docx', '.csv') or 'ledger' in p.name.lower()
        or 'content.json' == p.name or 'build_report' in p.name or 'validation' in p.name)]
    check('served: no .docx/.csv/ledger/content.json anywhere in dist/', not leaks, ', '.join(leaks))
    robots = (DIST / 'robots.txt').read_text() if (DIST / 'robots.txt').exists() else ''
    check('robots.txt disallows /preview/ without naming the slug',
          'Disallow: /preview/' in robots and CFG['slug'] not in robots, robots.strip().replace('\n', ' | '))
    linkers = [str(p.relative_to(DIST)) for p in DIST.rglob('*')
               if p.is_file() and p.suffix in ('.html', '.xml', '.txt', '.json', '.js')
               and p.parent != slug_dir and CFG['slug'] in p.read_text(errors='ignore')]
    check('slug not referenced by any other served file (sitemap/RSS/index/nav)', not linkers, ', '.join(linkers))
    sitemaps = [str(p.relative_to(DIST)) for p in DIST.rglob('*') if re.search(r'sitemap|rss|feed\.xml|atom', p.name, re.I)]
    check('no sitemap/RSS in dist that could list the page', not sitemaps, ', '.join(sitemaps) or 'none exist')


def main():
    served_path_checks()
    url_path = f"/preview/{CFG['slug']}/"
    srv = serve()
    base = f'http://127.0.0.1:{srv.server_address[1]}'
    SHOTS.mkdir(exist_ok=True)
    data = {}
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={'width': 1280, 'height': 900})
        resp = page.goto(base + url_path, wait_until='networkidle')
        check('page loads over HTTP at the clean slug path', resp and resp.ok, url_path)
        src = page.content()

        # -- structure
        check('1 title block', page.locator('header.masthead h1').count() == 1 and page.locator('h1').count() == 1)
        n_sec = page.locator('section.section[data-section]').count()
        check('5 sections (Intro + I–IV)', n_sec == EXP['sections'], f'{n_sec}: ' + ','.join(
            page.eval_on_selector_all('section.section[data-section]', 'els => els.map(e => e.id)')))
        n_coh = page.locator('h3.cohort-title').count()
        check('9 cohort headings', n_coh == EXP['cohorts'], str(n_coh))
        strip = page.eval_on_selector_all('.cohort-strip a', 'els => els.map(e => e.textContent)')
        in_ii = page.locator('section#ii .cohort-strip').count() == 1
        check('cohort jump strip C1–C9 inside section II', in_ii and strip == [f'C{i}' for i in range(1, 10)], ' '.join(strip))
        figs = page.eval_on_selector_all('figure[data-figure]', '''els => els.map(f => {
            const vis = [...f.querySelectorAll('svg')].filter(s => s.getBoundingClientRect().height > 0);
            const r = f.querySelector('.viz-container').getBoundingClientRect();
            return {n: f.dataset.figure, h: Math.round(r.height), w: Math.round(r.width), visible_svgs: vis.length};
        })''')
        check('6 rendered figures', len(figs) == EXP['figures'], str(len(figs)))
        empty = [f for f in figs if f['h'] < 50 or f['visible_svgs'] != 1]
        check('no empty or zero-height figure container (1280px)', not empty, json.dumps(empty) if empty else
              ', '.join(f"F{f['n']} {f['h']}px" for f in figs))

        # -- text parity
        rendered = page.evaluate(f'''() => {{
            const m = document.querySelector('main').cloneNode(true);
            m.querySelectorAll('{FIG_SKIP}').forEach(e => e.remove());
            return m.innerText;
        }}''')
        caption_paras = {(f['caption_para'], norm(f['caption_text'])) for f in REPORT['figures'] if f.get('caption_text')}
        blocks = CONTENT['blocks']
        first_h2 = next(i for i, b in enumerate(blocks) if b['type'] == 'h2')
        body_blocks = [b for b in blocks[first_h2:] if b['type'] != 'figure'
                       and (b['para'], norm(block_text(b))) not in caption_paras]
        docx_words = sum(len(words(block_text(b))) for b in body_blocks)
        page_words = len(words(rendered))
        diff = (page_words - docx_words) / docx_words * 100
        check('body word count within 1% of docx', abs(diff) <= 1,
              f'docx {docx_words:,} · page {page_words:,} · {diff:+.2f}% (docx total incl. title block: '
              f'{sum(len(words(block_text(b))) for b in blocks):,})')
        rendered_paras = page.eval_on_selector_all('main [data-para]', '''els => els.map(e =>
            ({para: +e.dataset.para, text: e.innerText}))''')
        expected = [(b['para'], norm(block_text(b))) for b in body_blocks]
        got = [(r['para'], norm(r['text'])) for r in rendered_paras]
        missing = [p for p in expected if p not in got]
        dupes = sorted({p for p in got if got.count(p) > 1})
        extra = [p for p in got if p not in expected]
        check('no paragraphs dropped', not missing, '; '.join(f'¶{p}: {t[:50]}' for p, t in missing[:10]))
        check('no paragraphs duplicated or invented', not dupes and not extra,
              '; '.join(f'¶{p}: {t[:50]}' for p, t in (dupes + extra)[:10]))

        # -- leaks
        body_text = page.evaluate('document.body.innerText')
        for handle in ('apergam', 'carriesimmons'):
            check(f'no "{handle}" anywhere in page source', handle not in src.lower())
        ats = re.findall(r'\S*@\S*', body_text)
        check('no "@" mentions in visible text', not ats, ' '.join(ats[:10]))
        comments = docx_comments()
        leaked = [c[:60] for c in comments if any(len(s) > 25 and s in src for s in re.split(r'(?<=[.?!])\s+', c))]
        check(f'no comment text in page ({len(comments)} docx comments checked)', not leaked, ' | '.join(leaked))
        placeholders = src.count('[CAPTION NEEDED]')
        check('every [CAPTION NEEDED] is flagged in the build report',
              placeholders == len(REPORT['captions_needed']),
              f'{placeholders} on page; flagged figures {REPORT["captions_needed"]}')
        csv_links = page.eval_on_selector_all('a[href$=".csv"], a[download], a[href$=".xlsx"]', 'els => els.map(e => e.href)')
        check('no dataset/CSV download links', not csv_links, ' '.join(csv_links))
        want = sorted(f['n'] for f in CFG['figures'] if f.get('data_table'))
        have = sorted(int(x) for x in page.eval_on_selector_all('figure[data-figure] .viz-data table',
                                                                'els => els.map(e => e.closest("figure").dataset.figure)'))
        check('data tables present only on approved figures', have == want, f'tables on {have}; approved {want}')
        check('no "Download CSV" text anywhere', 'download csv' not in src.lower())
        byline = CFG.get('byline')
        if byline:
            got_byline = page.inner_text('header.masthead .byline').strip()
            check('byline renders as configured', got_byline == byline, got_byline)
        robots_meta = page.get_attribute('meta[name=robots]', 'content') or ''
        check('meta robots noindex, nofollow', 'noindex' in robots_meta and 'nofollow' in robots_meta, robots_meta)
        banner = page.inner_text('.draft-banner')
        check('draft banner text', "Pre-publication draft. Please don't share or cite." in banner
              and "Forthcoming from the Knight Center for the Future of News at ASU's Cronkite School." in banner)

        # -- data asserts (read from the rendered figures; nothing is edited)
        exp_n = EXP['cohort_n']
        for variant in ('fig-wide', 'fig-narrow'):
            t2 = ' '.join(page.eval_on_selector_all(f'#figure-2 .{variant} svg text', 'els => els.map(e => e.textContent)'))
            card_n = {c: int(n) for c, n in re.findall(r'(C\d)\s*·\s*n=(\d+)', t2)}
            check(f'Fig 2 card-grid n match expected and sum to {EXP["cohort_total"]} ({variant})',
                  card_n == exp_n and sum(card_n.values()) == EXP['cohort_total'],
                  f'{card_n} sum={sum(card_n.values())}')
            titles = page.eval_on_selector_all(f'#figure-6 .{variant} svg title', 'els => els.map(e => e.textContent)')
            rows = {c: (int(a), int(b), int(d)) for c, a, b, d in
                    (re.match(r'(C\d)[^:]*: (\d+) below, (\d+) in, (\d+) above', t).groups()
                     for t in titles if re.match(r'(C\d)[^:]*: \d+ below', t))}
            if not rows:
                # Narrow variant has no per-segment titles: row titles give cohort order, and the
                # labels run "n=18", then (count, "NN%") pairs for each non-empty segment.
                order = [re.match(r'(C\d)', t).group(1) for t in titles if re.match(r'C\d ', t)]
                texts = page.eval_on_selector_all(f'#figure-6 .{variant} svg text', 'els => els.map(e => e.textContent.trim())')
                segs, cur = [], None
                for k, tx in enumerate(texts):
                    if re.fullmatch(r'n=\d+', tx):
                        cur = []
                        segs.append(cur)
                    elif cur is not None and re.fullmatch(r'\d+', tx) and k + 1 < len(texts) \
                            and re.fullmatch(r'\d+%', texts[k + 1]):
                        cur.append(int(tx))
                rows = dict(zip(order, (tuple(s) for s in segs)))
            bad = {c: (sum(v), exp_n.get(c)) for c, v in rows.items() if sum(v) != exp_n.get(c)}
            total = sum(sum(v) for v in rows.values())
            check(f'Fig 6 stacked-bar rows equal cohort n, total {EXP["cohort_total"]} ({variant})',
                  len(rows) == 9 and not bad and total == EXP['cohort_total'],
                  f'{len(rows)} rows, total {total}' + (f', mismatches {bad}' if bad else ''))
            data.setdefault('fig6_rows', {})[variant] = rows
            data.setdefault('fig2_n', {})[variant] = card_n

        # -- $268M open item (report only)
        fig1 = ' '.join(page.eval_on_selector_all('#figure-1 .fig-wide svg text, #figure-1 .fig-wide svg title',
                                                  'els => els.map(e => e.textContent)'))
        g = sorted(set(re.findall(r'USAID[^$]*\$[\d.,]+\s?[MB]?', fig1)))
        t = sorted(set(m for b in blocks for m in re.findall(
            r'[^.]*\$[\d.,]+ (?:million|billion)[^.]*U\.S\. Agency for International Development[^.]*', block_text(b))))
        data['usaid'] = {'graphic': g, 'text': t}
        print('INFO  USAID figure — graphic:', g, '| text:', t)

        # -- rendering
        for w in (375, 768, 1280):
            page.set_viewport_size({'width': w, 'height': 900})
            page.wait_for_timeout(300)
            sw = page.evaluate('document.documentElement.scrollWidth')
            check(f'no horizontal page scroll at {w}px', sw <= w, f'scrollWidth {sw}')
            figs_w = page.eval_on_selector_all('figure[data-figure]', '''els => els.map(f => {
                const vis = [...f.querySelectorAll('svg')].filter(s => s.getBoundingClientRect().height > 0);
                return {n: f.dataset.figure, h: Math.round(f.getBoundingClientRect().height), vis: vis.length};})''')
            bad = [f for f in figs_w if f['h'] < 50 or f['vis'] != 1]
            check(f'all 6 figures render at {w}px', len(figs_w) == 6 and not bad, json.dumps(bad) if bad else '')
            page.evaluate('window.scrollTo(0,0)')
            page.screenshot(path=str(SHOTS / f'{w}-top.png'))
            page.screenshot(path=str(SHOTS / f'{w}-full.jpg'), full_page=True, type='jpeg', quality=55)
            if w == 375:
                for f in range(1, 7):
                    page.locator(f'#figure-{f}').screenshot(path=str(SHOTS / f'375-figure-{f}.png'))
                page.locator('section#ii').scroll_into_view_if_needed()
                page.evaluate("document.querySelector('#ii .cohort-strip').scrollIntoView({block:'center'})")
                page.screenshot(path=str(SHOTS / '375-cohort-strip.png'))
        browser.close()
    srv.shutdown()
    failed = [r for r in results if not r['pass']]
    (HERE / 'validation.json').write_text(json.dumps({'results': results, 'data': data}, indent=1, ensure_ascii=False) + '\n')
    print(f'\n{len(results) - len(failed)}/{len(results)} checks passed')
    sys.exit(1 if failed else 0)


if __name__ == '__main__':
    main()
