#!/usr/bin/env python3
"""content/content.json + figure embeds -> preview/<slug>/index.html.

Chrome (type, palette, masthead, section and figure styles) comes from the v16
page; all prose comes from content.json. Figures are the figures_v22 embeds,
inlined: only their wide/narrow SVGs are taken. Each embed's title, cutline,
data table and "Download CSV" link are dropped, and its fonts are renamed so
they can't collide with the page's own. Figure data is not touched.

Writes build_report.json (figure mapping, warnings) for the ledger.
"""
import hashlib
import html
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CAPTION_PLACEHOLDER = '[CAPTION NEEDED]'
ROMAN = {'I': 'i', 'II': 'ii', 'III': 'iii', 'IV': 'iv', 'V': 'v'}


def esc(s):
    return html.escape(s, quote=False)


def text_of(runs):
    return ''.join(r.get('t', '\n' if r.get('br') else '') for r in runs)


def render_runs(runs):
    out = []
    for r in runs:
        if r.get('br'):
            out.append('<br>')
            continue
        if 'note' in r:
            n = r['note']
            out.append(f'<sup class="note-ref"><a href="#note-{n}" id="note-ref-{n}">{n}</a></sup>')
            continue
        t = esc(r['t'])
        if r.get('sup'):
            t = f'<sup>{t}</sup>'
        if r.get('i'):
            t = f'<em>{t}</em>'
        if r.get('b'):
            t = f'<strong>{t}</strong>'
        if r.get('href'):
            href = html.escape(r['href'])
            ext = '' if href.startswith('#') else ' target="_blank" rel="noopener noreferrer"'
            t = f'<a href="{href}"{ext}>{t}</a>'
        out.append(t)
    return ''.join(out)


# -- figures -----------------------------------------------------------------
FONT_RENAME = (("'DM Sans'", "'NNFig DM Sans'"), ("'Libre Baskerville'", "'NNFig Libre Baskerville'"))


def load_figure(path):
    src = path.read_text()
    style = re.search(r'<style>(.*?)</style>', src, re.S).group(1)
    fonts = ''.join(re.findall(r'@font-face\{[^}]*\}', style))
    svgs = dict(re.findall(r'<div class="(wide|narrow)">(<svg.*?</svg>)</div>', src, re.S))
    if set(svgs) != {'wide', 'narrow'}:
        sys.exit(f'{path.name}: expected one wide and one narrow SVG')
    title = re.search(r'<h2 class="title">(.*?)</h2>', src, re.S)
    table = re.search(r'<details>.*?</details>', src, re.S)
    table = table.group(0) if table else ''
    table = re.sub(r'<a href="[^"]+\.csv">Download CSV</a>\s*·\s*', '', table)
    if '.csv"' in table or 'Download CSV' in table:
        sys.exit(f'{path.name}: CSV link survived in data table')
    for a, b in FONT_RENAME:
        fonts = fonts.replace(a, b)
        svgs = {k: v.replace(a, b) for k, v in svgs.items()}
    dropped = {
        'csv_links': re.findall(r'href="([^"]+\.csv)"', src),
        'data_table': '<details>' in src,
        'cutline': bool(re.search(r'<figcaption>', src)),
    }
    return {
        'title': html.unescape(title.group(1)) if title else '',
        'table': table,
        'wide': svgs['wide'], 'narrow': svgs['narrow'],
        'fonts': fonts, 'dropped': dropped,
        'sha256': hashlib.sha256(src.encode()).hexdigest(),
    }


def render_figure(n, fig, fc, caption_runs, with_table):
    # Caption precedence: config.json (copy supplied for the figure) > docx caption line > placeholder.
    if fc.get('caption'):
        caption = esc(fc['caption'])
        if fc.get('source'):
            caption += f'<span class="viz-source">{esc(fc["source"])}</span>'
    elif caption_runs:
        caption = render_runs(caption_runs)
    else:
        caption = f'<span class="caption-needed">{CAPTION_PLACEHOLDER}</span>'
    title = fc.get('title') or fig['title']
    heading = (f'<div class="viz-label">Figure {n}</div>\n'
               + (f'<div class="viz-title">{esc(title)}</div>\n' if title else ''))
    return (f'<figure class="viz-wrap" id="figure-{n}" data-figure="{n}">\n'
            f'{heading}'
            f'<div class="viz-container"><div class="fig-wide">{fig["wide"]}</div>'
            f'<div class="fig-narrow">{fig["narrow"]}</div></div>\n'
            f'<figcaption class="viz-caption">{caption}</figcaption>\n'
            + (f'<div class="viz-data">{fig["table"]}</div>\n' if with_table and fig['table'] else '')
            + '</figure>')


# -- page structure ----------------------------------------------------------
def section_meta(heading):
    """'I. But first...' -> ('i', 'I', 'But first...'); 'Introduction: X' -> ('intro', 'Intro', ...)."""
    m = re.match(r'^(I{1,3}|IV|V)\.\s*(.*)$', heading.strip())
    if m:
        return ROMAN[m.group(1)], m.group(1), m.group(2).strip()
    if heading.lower().startswith('introduction'):
        return 'intro', 'Intro', re.sub(r'^Introduction:?\s*', '', heading.strip())
    return re.sub(r'[^a-z0-9]+', '-', heading.lower()).strip('-'), heading, heading


def cohort_meta(heading):
    m = re.match(r'^(C\d)\s*[—–-]\s*(.*)$', heading.strip())
    return (m.group(1), m.group(2).strip()) if m else (None, heading.strip())


def build(cfg, content):
    blocks = content['blocks']
    report = {'figures': [], 'warnings': [], 'captions_needed': []}
    figs_cfg = {f['n']: f for f in cfg['figures']}
    figdir = Path(cfg['figures_dir'])
    loaded = {n: load_figure(figdir / f['file']) for n, f in figs_cfg.items()}
    font_sets = {f['fonts'] for f in loaded.values()}
    if len(font_sets) != 1:
        report['warnings'].append('Figure embeds carry different font subsets; using all of them.')
    fig_fonts = ''.join(sorted(font_sets))

    # title block: H1s and anything before the first H2
    first_h2 = next(i for i, b in enumerate(blocks) if b['type'] == 'h2')
    head = blocks[:first_h2]
    h1s = [b for b in head if b['type'] == 'h1']
    title = text_of(h1s[0]['runs']).strip() if h1s else ''
    subtitle_html = render_runs(h1s[1]['runs']) if len(h1s) > 1 else ''
    if cfg.get('byline'):
        # Explicit override of the docx title-block line(s); see config.json "byline".
        meta_html = [f'<div class="masthead-meta byline">{esc(cfg["byline"])}</div>']
        report['byline_override'] = {'rendered': cfg['byline'],
                                     'docx': [text_of(b['runs']).strip() for b in head if b['type'] != 'h1']}
    else:
        meta_html = [f'<div class="masthead-meta" data-para="{b["para"]}">{render_runs(b["runs"])}</div>'
                     for b in head if b['type'] != 'h1']

    body, nav, cohorts = [], [], []
    open_section = open_cohort = False
    list_open = None  # (tag, list_id)
    i = first_h2
    while i < len(blocks):
        b = blocks[i]
        if list_open and (b['type'] != 'li' or b['list_id'] != list_open[1]):
            body.append(f'</{list_open[0]}>')
            list_open = None
        t = b['type']
        if t == 'h2':
            if open_cohort:
                body.append('</div>')
                open_cohort = False
            if open_section:
                body.append('</section>')
            sid, short, rest = section_meta(text_of(b['runs']))
            nav.append((sid, short, rest))
            num = '' if sid == 'intro' else f'<span class="section-num">{short}.</span> '
            lead = 'Introduction: ' if sid == 'intro' else ''
            body.append(f'<section class="section" id="{sid}" data-section="{sid}">')
            body.append(f'<h2 data-para="{b["para"]}">{num}{esc(lead)}<span class="h2-text">{esc(rest)}</span></h2>')
            if sid == 'ii':
                body.append('<!--COHORT_STRIP-->')
            open_section = True
        elif t == 'h3':
            if open_cohort:
                body.append('</div>')
            code, name = cohort_meta(text_of(b['runs']))
            cid = code.lower() if code else re.sub(r'[^a-z0-9]+', '-', name.lower())
            if code:
                cohorts.append((cid, code, name))
            body.append(f'<div class="cohort-section" id="{cid}" data-cohort="{code or ""}">')
            code_html = f'<span class="cohort-num">{code}</span> <span class="cohort-dash">—</span> ' if code else ''
            body.append(f'<h3 class="cohort-title" data-para="{b["para"]}">{code_html}{esc(name)}</h3>')
            open_cohort = True
        elif t == 'figure':
            n = b['n']
            fc = figs_cfg.get(n)
            if not fc:
                report['warnings'].append(f'Docx image {n} (para {b["para"]}) has no embed in config.')
                i += 1
                continue
            caption = None
            nxt = blocks[i + 1] if i + 1 < len(blocks) else None
            if nxt and nxt['type'] == 'p' and re.match(r'^\s*(Figure|Fig\.)\s*\d', text_of(nxt['runs'])):
                caption = nxt['runs']
                nxt_para = nxt['para']
                i += 1
                nxt = blocks[i + 1] if i + 1 < len(blocks) else None
            if caption is None and not fc.get('caption'):
                report['captions_needed'].append(n)
            following = text_of(nxt['runs']).strip() if nxt and 'runs' in nxt else ''
            ok = following.startswith(fc['precedes'])
            if not ok:
                report['warnings'].append(
                    f'Figure {n}: expected next paragraph to start "{fc["precedes"]}", found "{following[:60]}"')
            fig = loaded[n]
            report['figures'].append({
                'n': n, 'name': fc['name'], 'embed': fc['file'], 'embed_title': fig['title'],
                'embed_sha256': fig['sha256'][:12], 'docx_para': b['para'],
                'in_tracked_deletion': bool(b.get('in_deletion')),
                'precedes': following[:70], 'anchor_ok': ok, 'dropped': fig['dropped'],
                'caption': 'config' if fc.get('caption') else ('docx' if caption else 'placeholder'),
                'docx_caption_ignored': bool(caption and fc.get('caption')),
                'data_table': bool(fc.get('data_table') and fig['table']),
                'caption_text': text_of(caption) if caption else None,
                'caption_para': nxt_para if caption else None,
            })
            body.append(render_figure(n, fig, fc, caption, fc.get('data_table', False)))
        elif t == 'li':
            if not list_open:
                tag = 'ol' if b['ordered'] else 'ul'
                body.append(f'<{tag} data-list="{b["list_id"]}">')
                list_open = (tag, b['list_id'])
            body.append(f'<li data-para="{b["para"]}">{render_runs(b["runs"])}</li>')
        else:
            body.append(f'<p data-para="{b["para"]}">{render_runs(b["runs"])}</p>')
        i += 1
    if list_open:
        body.append(f'</{list_open[0]}>')
    if open_cohort:
        body.append('</div>')
    if open_section:
        body.append('</section>')

    strip = ('<nav class="cohort-strip" aria-label="Jump to cohort"><span class="strip-label">Jump to</span>'
             + ''.join(f'<a href="#{cid}" title="{esc(name)}">{code}</a>' for cid, code, name in cohorts)
             + '</nav>')
    body_html = '\n'.join(body).replace('<!--COHORT_STRIP-->', strip)

    notes_html = ''
    if content['notes']:
        items = ''.join(f'<li id="note-{n["n"]}">{render_runs(n["runs"])} '
                        f'<a href="#note-ref-{n["n"]}" aria-label="Back to text">↩</a></li>'
                        for n in content['notes'])
        notes_html = f'<section class="section notes" id="notes"><h2>Notes</h2><ol>{items}</ol></section>'

    nav_html = ''.join(
        f'<a href="#{sid}" data-target="{sid}" title="{esc(rest)}">{esc(short)}</a>'
        for sid, short, rest in nav)

    page = TEMPLATE
    for k, v in {
        '%%TITLE%%': esc(title),
        '%%SUBTITLE%%': subtitle_html,
        '%%META%%': '\n'.join(meta_html),
        '%%NAV%%': nav_html,
        '%%BODY%%': body_html,
        '%%NOTES%%': notes_html,
        '%%FIGFONTS%%': fig_fonts,
        '%%SOURCE%%': esc(content['source']['file']),
        '%%SOURCE_SHA%%': content['source']['sha256'][:12],
        '%%PARSED%%': content['source']['parsed'],
    }.items():
        page = page.replace(k, v)
    report['nav'] = [s for s, _, _ in nav]
    report['cohorts'] = [c for _, c, _ in cohorts]
    return page, report


TEMPLATE = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex, nofollow">
<meta name="referrer" content="no-referrer">
<title>%%TITLE%% — Pre-publication draft</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&family=DM+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
  /* Figure fonts, carried over from the figures_v22 embeds under their own names. */
  %%FIGFONTS%%

  /* Chrome from nodes_and_networks_v16.html. Text sizes raised to the Atlas floors
     (body 16px, UI text 13px, all-caps labels 11px). */
  :root {
    --ink: #1a1a18;
    --ink-light: #4a4a46;
    --ink-faint: #6b6b64;
    --rule: #ddddd8;
    --rule-light: #eeeeea;
    --bg: #faf9f5;
    --bg-warm: #f5f4ef;
    --blue: #185FA5;
    --max-w: 740px;
    --nav-h: 48px;
    --font-body: 'Libre Baskerville', Georgia, serif;
    --font-ui: 'DM Sans', system-ui, sans-serif;
  }
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  html { font-size: 16px; scroll-padding-top: calc(var(--nav-h) + 16px); }
  body { background: var(--bg); color: var(--ink); font-family: var(--font-body); line-height: 1.75; -webkit-font-smoothing: antialiased; overflow-x: hidden; }
  a { color: var(--blue); text-underline-offset: 2px; }
  a:focus-visible { outline: 2px solid var(--blue); outline-offset: 2px; }

  .draft-banner { background: var(--ink); color: var(--bg); font-family: var(--font-ui); font-size: 13px; line-height: 1.45; text-align: center; padding: 8px 16px; }
  .draft-banner strong { font-weight: 600; }
  .draft-banner span { display: block; color: #c9c9c2; }

  .masthead { border-bottom: 2px solid var(--ink); padding: 2.5rem 2rem 1.5rem; max-width: var(--max-w); margin: 0 auto; }
  .masthead h1 { font-size: 2.4rem; font-weight: 700; line-height: 1.15; letter-spacing: -0.02em; margin-bottom: 0.5rem; overflow-wrap: break-word; }
  .masthead-sub { font-size: 1.1rem; font-style: italic; color: var(--ink-light); margin-bottom: 1.25rem; }
  .masthead-meta { font-family: var(--font-ui); font-size: 13px; color: var(--ink-faint); }

  .section-nav { position: sticky; top: 0; z-index: 10; background: var(--bg); border-bottom: 1px solid var(--rule); }
  .section-nav-inner { max-width: var(--max-w); margin: 0 auto; padding: 0 2rem; display: flex; gap: 4px; overflow-x: auto; scrollbar-width: none; height: var(--nav-h); align-items: center; }
  .section-nav-inner::-webkit-scrollbar { display: none; }
  .section-nav a { font-family: var(--font-ui); font-size: 13px; font-weight: 600; color: var(--ink-light); text-decoration: none; padding: 6px 12px; border-radius: 6px; white-space: nowrap; }
  .section-nav a:hover { background: var(--bg-warm); color: var(--ink); }
  .section-nav a.active { color: var(--ink); background: var(--bg-warm); box-shadow: inset 0 -2px 0 var(--blue); }

  .content { max-width: var(--max-w); margin: 0 auto; padding: 0 2rem 6rem; }
  .section { margin-top: 3.5rem; padding-top: 2rem; border-top: 1px solid var(--rule); }
  .section:first-child { border-top: none; margin-top: 1rem; }
  .section-num { font-family: var(--font-ui); font-size: 0.85em; color: var(--ink-faint); font-weight: 600; }
  h2 { font-size: 1.5rem; font-weight: 700; line-height: 1.25; letter-spacing: -0.01em; margin-bottom: 1.25rem; }

  .cohort-strip { display: flex; flex-wrap: wrap; gap: 6px; align-items: center; margin: 0 0 2rem; padding: 10px 12px; background: var(--bg-warm); border: 1px solid var(--rule); border-radius: 6px; }
  .strip-label { font-family: var(--font-ui); font-size: 11px; font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase; color: var(--ink-faint); margin-right: 4px; white-space: nowrap; }
  .cohort-strip a { font-family: var(--font-ui); font-size: 13px; font-weight: 600; color: var(--blue); text-decoration: none; padding: 4px 10px; border: 1px solid var(--rule); border-radius: 9999px; background: var(--bg); white-space: nowrap; }
  .cohort-strip a:hover { border-color: var(--blue); }

  .cohort-section { margin-top: 3rem; padding-top: 2rem; border-top: 2px solid var(--rule); }
  .cohort-title { font-family: var(--font-ui); font-size: 1.15rem; font-weight: 600; line-height: 1.35; margin-bottom: 1rem; }
  .cohort-num { color: var(--blue); font-weight: 700; }
  .cohort-dash { color: var(--ink-faint); }

  p { margin-bottom: 1.1rem; font-size: 1rem; }
  ul, ol { margin: 0 0 1.25rem 1.5rem; }
  li { margin-bottom: 0.6rem; font-size: 1rem; padding-left: 0.25rem; }
  strong { font-weight: 700; }
  em { font-style: italic; }
  p a, li a { overflow-wrap: anywhere; }

  .viz-wrap { margin: 2.5rem 0; }
  .viz-label { font-family: var(--font-ui); font-size: 11px; font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase; color: var(--ink-faint); margin-bottom: 0.25rem; }
  .viz-title { font-family: var(--font-ui); font-size: 1.05rem; font-weight: 600; line-height: 1.35; color: var(--ink); margin-bottom: 0.75rem; }
  .viz-source { display: block; margin-top: 0.4rem; font-size: 13px; color: var(--ink-faint); }
  .viz-container { background: #fff; border: 1px solid var(--rule); padding: 1rem; overflow-x: auto; }
  .viz-container svg { display: block; width: 100%; height: auto; }
  .fig-narrow { display: none; }
  @media (max-width: 620px) { .fig-wide { display: none; } .fig-narrow { display: block; } }
  .viz-caption { font-family: var(--font-ui); font-size: 14px; color: var(--ink-light); margin-top: 0.75rem; line-height: 1.5; }
  .viz-data details { margin-top: 0.75rem; font-family: var(--font-ui); font-size: 13px; color: var(--ink-light); }
  .viz-data summary { cursor: pointer; font-weight: 600; color: var(--ink); }
  .viz-data .tw { overflow-x: auto; margin-top: 8px; border: 1px solid var(--rule); background: #fff; }
  .viz-data table { border-collapse: collapse; font-size: 13px; width: 100%; }
  .viz-data th, .viz-data td { border-bottom: 1px solid var(--rule-light); padding: 6px 10px; text-align: left; white-space: nowrap; vertical-align: top; }
  .viz-data th { font-weight: 600; color: var(--ink); border-bottom: 2px solid var(--ink); }
  .viz-data p { font-size: 13px; color: var(--ink-faint); margin: 8px 0 0; }
  .caption-needed { display: inline-block; background: #fdf0d8; color: #7a4a00; border: 1px dashed #BA7517; padding: 2px 8px; border-radius: 6px; font-weight: 600; font-size: 13px; }

  .notes ol { font-family: var(--font-ui); font-size: 14px; }
  .note-ref a { text-decoration: none; font-family: var(--font-ui); font-size: 0.75em; }

  .footer { max-width: var(--max-w); margin: 0 auto; padding: 2rem 2rem 3rem; border-top: 2px solid var(--ink); font-family: var(--font-ui); font-size: 13px; color: var(--ink-faint); display: flex; justify-content: space-between; gap: 1rem; flex-wrap: wrap; }

  @media (max-width: 600px) {
    .masthead { padding: 1.75rem 16px 1.25rem; }
    .masthead h1 { font-size: 1.75rem; }
    .section-nav-inner { padding: 0 8px; }
    .content { padding: 0 16px 4rem; }
    .footer { padding: 1.5rem 16px 2.5rem; }
    h2 { font-size: 1.25rem; }
    .viz-container { padding: 8px; }
  }
</style>
</head>
<body>

<div class="draft-banner" role="note"><strong>Pre-publication draft. Please don't share or cite.</strong>
<span>Forthcoming from the Knight Center for the Future of News at ASU's Cronkite School.</span></div>

<header class="masthead">
  <h1>%%TITLE%%</h1>
  <div class="masthead-sub">%%SUBTITLE%%</div>
  %%META%%
</header>

<nav class="section-nav" aria-label="Sections"><div class="section-nav-inner">%%NAV%%</div></nav>

<main class="content" id="paper">
%%BODY%%
%%NOTES%%
</main>

<footer class="footer">
  <span>Pre-publication draft · not for distribution</span>
  <span>Built from %%SOURCE%% (%%SOURCE_SHA%%) on %%PARSED%%</span>
</footer>

<script>
// Highlight the section in view in the sticky nav: the last section whose top has
// passed just under the nav.
(function () {
  var nav = document.querySelector('.section-nav');
  var links = [].slice.call(nav.querySelectorAll('a'));
  var sections = links.map(function (a) { return document.getElementById(a.dataset.target); });
  var current = -1, queued = false;
  function update() {
    queued = false;
    var line = nav.getBoundingClientRect().bottom + 24, idx = -1;
    sections.forEach(function (s, i) { if (s && s.getBoundingClientRect().top <= line) idx = i; });
    if (idx === current) return;
    if (current >= 0) links[current].classList.remove('active');
    current = idx;
    if (idx >= 0) links[idx].classList.add('active');
  }
  window.addEventListener('scroll', function () { if (!queued) { queued = true; requestAnimationFrame(update); } }, { passive: true });
  update();
})();
</script>
</body>
</html>
'''


def main():
    cfg = json.loads((HERE / 'config.json').read_text())
    content = json.loads((HERE / 'content' / 'content.json').read_text())
    page, report = build(cfg, content)
    out = (HERE / cfg['site_root'] / 'preview' / cfg['slug'] / 'index.html').resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page)
    report['output'] = str(out)
    report['bytes'] = len(page.encode())
    (HERE / 'build_report.json').write_text(json.dumps(report, indent=1, ensure_ascii=False) + '\n')
    print(f'wrote {out} ({report["bytes"]:,} bytes); captions needed: {report["captions_needed"]}')
    for w in report['warnings']:
        print('WARNING:', w)


if __name__ == '__main__':
    main()
