#!/usr/bin/env python3
"""Nodes and Networks launch-kit build. Python 3.7+, standard library only.

  python3 nn/build.py [--out DIR]     build into DIR (default nn/_out; build-dist.sh passes --out dist)
  python3 nn/build.py --watch         rebuild on save and serve http://localhost:8000 with live reload
  python3 nn/build.py --check         build into a temp folder and report problems only
  python3 nn/build.py --fallback      refresh nn/built/, the committed copy build-dist.sh uses if the build cannot run on Cloudflare
  --stamp TEXT                        label written in the build comment at the top of each page

Reads: nn/content/copy.md (every reader-facing word), nn/content/settings.json (report link, publisher line, width),
nn/data/nodes169.json + nn/data/public-snapshot.json (the data; see nn/tools/snapshot.py), nn/src/* (templates), nn/media/*.
Writes: nodes-and-networks/{index.html, explorer/, embed/, media/}.
Fails with the file, line and reason when copy.md has a missing string id or an unknown token."""
import json, base64, sys, re, os, html, shutil, pathlib, tempfile, time, threading, datetime

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent
SRC, DATA, CONTENT, MEDIA = HERE / 'src', HERE / 'data', HERE / 'content', HERE / 'media'
FONT = REPO / 'assets' / 'nn5' / 'fonts' / 'InterTight-var.woff2'
BASE = 'https://journalismatlas.com/nodes-and-networks/'
TABS = ['short', 'governance', 'ways', 'history']
NUM = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten']
CUT = 1995
COHORT_GROUP = {'C1': 'a', 'C2': 'a', 'C3': 'a', 'C4': 'b', 'C5': 'b', 'C6': 'b', 'C7': 'c', 'C8': 'c', 'C9': 'c'}
PATH_KEYS = ['M1_bundle', 'M2_ideology_audience', 'M3_new_org_team_and_portfolio', 'M4_B2B_expense_account', 'M5_philanthropic_endowment_scale', 'M6_diversification']
STATUS = {'CLOSED': 'closed', 'ACQUIRED': 'acquired', 'ABSORBED': 'absorbed'}
# Tokens the page's own script fills while it runs (names, counts per row, years). Everything else must be a build token.
LOCAL_TOKENS = {'n', 'name', 'year', 'status', 'value', 'over', 'tot', 'label', 'grew', 'above', 'cohort', 'shape', 'sentence', 'title', 'stat'}
# The paper's own wording. The build stops if any of these change in copy.md.
LOCKED = {
 'chapter1.paper': "Nine cohorts capture the range of journalism operators currently producing in the United States, in three groups.",
 'chapter2.paper': "Organizations that break past their cohort's typical ceiling almost always do so through one of six specific mechanisms — and rarely more than one.",
 'cohort.C1': 'Legacy Publishers', 'cohort.C2': 'Creator Brands', 'cohort.C3': 'Barbell Hybrids', 'cohort.C4': 'Philanthropic Mesh Networks',
 'cohort.C5': 'Public Media Networks', 'cohort.C6': 'Collaboration Layers', 'cohort.C7': 'Worker-Owned Co-ops', 'cohort.C8': 'Emerging Civic Actors',
 'cohort.C9': 'B2B/Professional Services',
 'group.a': 'Journalism as most people picture it', 'group.b': 'Funded by philanthropy and public money', 'group.c': 'Funded directly by audiences and the market',
 'mechanism1.full': "A bundle big enough to capture a subscriber's whole information budget",
 'mechanism2.full': 'An audience captured by ideology rather than reporting',
 'mechanism3.full': 'A newer organization that grew a team and a portfolio at once',
 'mechanism4.full': "B2B pricing built for an employer's expense account rather than a household budget",
 'mechanism5.full': 'Philanthropic scale large enough to function like an endowment',
 'mechanism6.full': 'Genuine diversification, with no single stream large enough to hurt if it disappeared',
}
# copy.md ids the page script reads (everything with these prefixes goes into the explorer's data)
JS_PREFIXES = ('header.', 'footer.', 'attr.', 'report.', 'tabs.', 'chapter', 'how_to_read.', 'explore.', 'chart.', 'in_short.', 'legend.', 'list.', 'labels.', 'card.', 'ann.', 'hist.')
# ids used only by Python (templates read them with {{id}} or the build reads them directly)
PY_IDS = ['cohort.C%d' % i for i in range(1, 10)] + ['group.a', 'group.b', 'group.c'] + ['mechanism%d.%s' % (i, k) for i in range(1, 7) for k in ('short', 'full')] + \
         ['video.cue%d' % i for i in range(1, 8)] + ['video.end_title', 'video.end_publisher', 'video.end_site'] + \
         ['embed.tab.%s' % t for t in TABS] + ['share.title', 'share.line', 'share.chapter1', 'share.chapter2', 'share.chapter3', 'share.alt_landing', 'share.alt_chapter', 'embed.still_alt']


STAMP = {'label': 'built locally', 'media': True}


def stamp(page):
    """Put a build comment at the top of the page source so you can tell which build is live."""
    c = '<!-- nn build: %s | %s -->\n' % (datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'), STAMP['label'])
    return page.replace('<!doctype html>\n', '<!doctype html>\n' + c, 1) if page.startswith('<!doctype html>\n') else c + page


class BuildError(Exception):
    pass


def argv(flag, default=None):
    return sys.argv[sys.argv.index(flag) + 1] if flag in sys.argv else default


# ---------------------------------------------------------------- copy.md
def parse_copy(path):
    """-> {id: (text, line_number, locked)}"""
    out, cur, in_comment = {}, None, False
    lines = path.read_text(encoding='utf-8').split('\n')
    for ln, line in enumerate(lines, 1):
        s = line.strip()
        if in_comment:
            if '-->' in s: in_comment = False
            continue
        if s.startswith('<!--'):
            if '-->' not in s: in_comment = True
            continue
        m = re.match(r'^##\s+(\S+)(\s+\[locked\])?\s*$', s)
        if m:
            cur = m.group(1)
            if cur in out: raise BuildError('%s line %d: the string id "%s" appears twice (first on line %d)' % (path.name, ln, cur, out[cur][1]))
            out[cur] = [[], ln, bool(m.group(2))]
            continue
        if s.startswith('#'):
            cur = None
            continue
        if cur and s: out[cur][0].append(s)
    return {k: (' '.join(v[0]), v[1], v[2]) for k, v in out.items()}


def used_ids():
    ids = set(PY_IDS)
    explorer = (SRC / 'explorer.tpl.html').read_text(encoding='utf-8') + (SRC / 'engine.js').read_text(encoding='utf-8')
    fam = ('header', 'footer', 'attr', 'report', 'tabs', 'chapter', 'chapter_nav', 'how_to_read', 'explore', 'in_short', 'legend', 'list', 'labels', 'card', 'ann', 'hist', 'chart')
    for m in re.finditer(r"\b(?:cp|c)\(", explorer):
        for q in re.findall(r"'([a-z_0-9]+\.[a-z_0-9.]+)'", explorer[m.end():m.end() + 120].split(')')[0] if False else explorer[m.end():m.end() + 100]):
            if re.sub(r'\d+$', '', q.split('.')[0]) in fam: ids.add(q)
    ids |= set(re.findall(r"'((?:report|landing|embed|share|video)\.[a-z_0-9.]+)'", pathlib.Path(__file__).read_text(encoding='utf-8'))) - {'embed.tab.', 'embed.tpl.html', 'landing.png', 'landing.tpl.html'}
    for t in ('landing.tpl.html', 'embed.tpl.html'):
        ids |= set(k for k in re.findall(r'\{\{([\w.]+)\}\}', (SRC / t).read_text(encoding='utf-8')) if '.' in k)
    return ids


TOKEN_RE = re.compile(r'\{(@)?([\w.]+)(?:\|(\w+))?\}')


def resolve(copy, tokens, settings_ids=None):
    """Fill {tokens} and {@refs}. Local tokens (see LOCAL_TOKENS) stay for the page script. -> {id: str}"""
    out, state = {}, {}

    def one(cid, stack=()):
        if cid in out: return out[cid]
        if cid in stack: raise BuildError('copy.md line %d: "%s" refers to itself' % (copy[cid][1], cid))
        text, ln, _ = copy[cid]

        def sub(m):
            ref, name, flt = m.groups()
            if ref:
                if name not in copy: raise BuildError('copy.md line %d, "%s": {@%s} points to a string that does not exist' % (ln, cid, name))
                val = one(name, stack + (cid,))
            elif name in tokens: val = str(tokens[name])
            elif name in LOCAL_TOKENS: return m.group(0)
            else:
                raise BuildError('copy.md line %d, "%s": unknown token {%s}. Known tokens are listed in nn/README.md.' % (ln, cid, name))
            if flt == 'cap': val = val[:1].upper() + val[1:]
            elif flt: raise BuildError('copy.md line %d, "%s": unknown filter |%s (only |cap exists)' % (ln, cid, flt))
            return val
        out[cid] = TOKEN_RE.sub(sub, text)
        return out[cid]
    for cid in copy: one(cid)
    return out


def check_copy(copy, needed):
    missing = sorted(needed - set(copy))
    if missing:
        raise BuildError('copy.md is missing %d string id%s: %s\n  Add a line "## %s" and the text under it.' % (len(missing), '' if len(missing) == 1 else 's', ', '.join(missing), missing[0]))
    for cid, want in LOCKED.items():
        if cid in copy and copy[cid][0] != want:
            raise BuildError('copy.md line %d: "%s" quotes the paper and cannot change here.\n  Expected: %s\n  Found:    %s' % (copy[cid][1], cid, want, copy[cid][0]))
    ok = re.compile(r'\$10M|\$10 million|\b[1-4]\.? (Who|How|When|Plain|Auto|Still)|Mechanism 1|asu\.edu|embed=1|\d+px|2026|\b2007\b|\b2015\b|\bB2B\b|\bC\d\b')
    warns = []
    for cid, (text, ln, locked) in copy.items():
        if locked or cid.startswith(('tabs.', 'cohort.', 'mechanism', 'group.')): continue
        bare = ok.sub('', TOKEN_RE.sub('', text))
        if re.search(r'\d', bare): warns.append('copy.md line %d, "%s": a number is typed by hand. Use a token so it follows the data.' % (ln, cid))
    return warns


# ---------------------------------------------------------------- data
def load_nodes():
    src = json.load(open(DATA / 'nodes169.json'))
    snap = json.load(open(DATA / 'public-snapshot.json'))
    nodes, sn = src['nodes'], snap['nodes']
    if len(nodes) != 169 or len(sn) != 169: raise BuildError('nodes169.json or public-snapshot.json no longer has 169 nodes. Re-run nn/tools/snapshot.py.')
    out = []
    for n, s in zip(nodes, sn):
        if n['i'] != s['i']: raise BuildError('public-snapshot.json is out of step with nodes169.json (node %s). Re-run nn/tools/snapshot.py.' % n['i'])
        d = {'i': n['i'], 'c': n['c'], 'g': n['g'], 'o': s['o'], 'm': s['m'], 'b': n['b'], 'fy': s['fy'], 'un': n['un'], 'rv': s['rv'], 'pf': n['p']['field'], 'nm': s['nm']}
        if s['st']: d['st'] = s['st']
        out.append(d)
    gov = [{'key': g['key'], 'a0': g['a0'], 'a1': g['a1']} for g in src['lenses']['gov']['geo']]
    return out, gov


def rnd(x): return int(x + 0.5)


def nm1(n): return re.sub(r' /.*$', '', re.sub(r'\s*\(.*?\)', '', n))


def tokens_for(nodes, cohort_names, settings, copy_r=None):
    """Every number and name the copy may use, derived from the data."""
    T = {}
    N = nodes
    over = [n for n in N if n['b'] == 2]
    codes = list(cohort_names)
    byc = [{'code': c, 'name': cohort_names[c], 'n': sum(1 for x in N if x['c'] == c), 'up': sum(1 for x in over if x['c'] == c), 'pre': sum(1 for x in N if x['c'] == c and x['fy'] and x['fy'] < CUT)} for c in codes]
    top = sorted(byc, key=lambda c: (-c['up'], c['n']))[:4]
    up_top = sum(c['up'] for c in top)
    dated = [n for n in N if n['fy']]
    pre = [n for n in dated if n['fy'] < CUT]; post = [n for n in dated if n['fy'] >= CUT]
    crossed = sum(1 for n in N if n['o'] == 'CROSSED')
    via = sum(1 for n in N if n['o'] == 'CROSSED' and n['m'] in PATH_KEYS)
    exc_n = sum(1 for n in N if n['o'] == 'CROSSED' and n['m'] not in PATH_KEYS)
    exc = [n for n in N if n['m'] == 'EXCEPTION_PLATFORM_LICENSING']
    started = [n for n in N if n['o'] == 'INHERITED']
    older = sorted([n for n in started if n['fy'] and not n['un']], key=lambda n: n['fy'])[:2]
    u = len(N) - len(dated)
    old_kinds = sum(1 for c in codes if any(n['c'] == c for n in pre))
    T.update(n_orgs=len(N), cohorts_n=len(codes), cohorts_word=NUM[len(codes)], top_n=len(top), top_word=NUM[len(top)], top_hold=up_top,
             over10m_total=len(over), rest_word=NUM[len(codes) - len(top)], rest_hold=len(over) - up_top, top_pct=rnd(100 * up_top / len(over)),
             crossed=crossed, six_way_growers=via, n_ways=6, ways_word='six', exceptions_n=exc_n,
             exceptions_phrase=('one exception' if exc_n == 1 else '%s exceptions' % (NUM[exc_n] if exc_n <= 10 else exc_n)),
             cut=CUT, hist_pre=len(pre), hist_pre_over=sum(1 for n in pre if n['b'] == 2), hist_post=len(post), hist_post_over=sum(1 for n in post if n['b'] == 2),
             hist_old_kinds_word=NUM[old_kinds], unverified_orgs='%d organization%s' % (u, '' if u == 1 else 's'), unverified_be='is' if u == 1 else 'are',
             started_above=len(started), under_n=sum(1 for n in N if n['o'] == 'NEVER_CROSSED'),
             exception_name=nm1(exc[0]['nm']) if exc else '', older_two=' and '.join(nm1(n['nm']) for n in older))
    top2 = sorted(byc, key=lambda c: -c['up'])[:2]
    small = [c for c in byc if c['up'] == 0]
    T.update(gov_top_name=top2[0]['name'], gov_top_up=top2[0]['up'], gov_top_n=top2[0]['n'], gov_second_name=top2[1]['name'], gov_second_up=top2[1]['up'], gov_second_n=top2[1]['n'],
             gov_small_names=' and '.join(c['name'] for c in small), gov_small_up=sum(c['up'] for c in small), gov_small_n=sum(c['n'] for c in small))
    for code in ('C5', 'C2', 'C7'):
        c = next(x for x in byc if x['code'] == code)
        T.update({'hist_%s_name' % code.lower(): c['name'], 'hist_%s_pre' % code.lower(): c['pre'], 'hist_%s_up' % code.lower(): c['up'], 'hist_%s_n' % code.lower(): c['n']})
    ru = settings['report_url'].strip()
    T.update(publisher_line=settings['publisher_line'], embed_width=settings['embed_width_hint'], embed_h_narrow=1900, embed_h_wide=1500, embed_breakpoint=760,
             report_url=ru or settings['report_fallback_url'])
    return T


# ---------------------------------------------------------------- html helpers
def inline(s):
    """Escape, then allow `code` and [text](url) in copy."""
    s = html.escape(s, quote=False)
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    return re.sub(r'\[([^\]]+)\]\(([^)\s]+)\)', r'<a href="\2">\1</a>', s)


def fill_tpl(tpl, R, extra=None, name=''):
    def sub(m):
        k = m.group(1)
        if extra and k in extra: return extra[k]
        if k not in R: raise BuildError('%s uses {{%s}}, which is not in copy.md' % (name, k))
        return inline(R[k])
    return re.sub(r'\{\{([\w.]+)\}\}', sub, tpl)


def timeline():
    return json.load(open(HERE / 'video' / 'timeline.json'))


def vtt(R, tl):
    def ts(t): return '%02d:%02d:%06.3f' % (int(t // 3600), int(t % 3600 // 60), t % 60)
    out = ['WEBVTT', '']
    for i, c in enumerate(tl['cues'], 1):
        out += [str(i), '%s --> %s' % (ts(c['start']), ts(c['end'])), R[c['id']], '']
    return '\n'.join(out)


# ---------------------------------------------------------------- build
def build(out):
    settings = json.load(open(CONTENT / 'settings.json'))
    for k in ('report_url', 'report_link_label', 'report_fallback_url', 'publisher_line', 'embed_width_hint'):
        if k not in settings: raise BuildError('settings.json is missing "%s"' % k)
    copy = parse_copy(CONTENT / 'copy.md')
    warns = check_copy(copy, used_ids())
    nodes, gov = load_nodes()
    # cohort names and mechanism text come from copy.md (locked), so a typo there is caught by the lock check above
    cohort_names = {'C%d' % i: copy['cohort.C%d' % i][0] for i in range(1, 10)}
    T = tokens_for(nodes, cohort_names, settings)
    tl = timeline()
    T['video_seconds'] = int(round(tl['duration']))
    has_report = bool(settings['report_url'].strip())
    probe = resolve(copy, {**T, 'report_label': ''})
    T['report_label'] = settings['report_link_label'] if has_report else probe['report.fallback_label']
    R = resolve(copy, T)
    known = set(used_ids())
    for cid in copy:
        if cid not in known: warns.append('copy.md line %d: "%s" is not used by any page.' % (copy[cid][1], cid))
    for w in warns: print('warning:', w)
    meta = {'n': len(nodes), 'names': True, 'cut': CUT,
            'cohorts': [{'code': c, 'name': cohort_names[c], 'g': COHORT_GROUP[c]} for c in cohort_names],
            'groups': {g: R['group.' + g] for g in 'abc'},
            'paths': [{'key': PATH_KEYS[i], 'short': R['mechanism%d.short' % (i + 1)], 'full': R['mechanism%d.full' % (i + 1)]} for i in range(6)],
            'noPath': any(x['m'] == 'INHERITED_SCALE' for x in nodes),
            'report': {'url': T['report_url'], 'label': T['report_label']},
            'cp': {k: v for k, v in R.items() if k.startswith(JS_PREFIXES)}}
    data = {'meta': meta, 'gov': gov, 'nodes': nodes}
    dj = json.dumps(data, separators=(',', ':'), ensure_ascii=False)
    if '</' in dj: raise BuildError('data contains "</", which would break the page')
    engine = (SRC / 'engine.js').read_text(encoding='utf-8')
    font = base64.b64encode(FONT.read_bytes()).decode()
    maxw = str(settings['embed_width_hint'])

    def head(title, desc, url, img, alt):
        e = lambda s: html.escape(s, quote=True)
        return ('<title>%s</title><meta name="description" content="%s"><link rel="canonical" href="%s">'
                '<meta property="og:type" content="website"><meta property="og:site_name" content="Independent Journalism Atlas"><meta property="og:title" content="%s"><meta property="og:description" content="%s">'
                '<meta property="og:url" content="%s"><meta property="og:image" content="%s"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="%s">'
                '<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="%s"><meta name="twitter:description" content="%s"><meta name="twitter:image" content="%s"><meta name="twitter:image:alt" content="%s">'
                % (e(title), e(desc), url, e(title), e(desc), url, img, e(alt), e(title), e(desc), img, e(alt)))
    og = lambda n: BASE + 'media/og/' + n
    page_alt = R['share.alt_landing']
    explorer = (SRC / 'explorer.tpl.html').read_text(encoding='utf-8')
    explorer = explorer.replace('<!--HEAD-->', head(R['header.title'] + ': Explorer', R['landing.meta_description'], BASE + 'explorer/', og('landing.png'), page_alt))
    explorer = explorer.replace('/*FONT*/', font).replace('/*DATA*/', dj).replace('/*ENGINE*/', engine).replace('/*MAXW*/', maxw)
    root = out / 'nodes-and-networks'
    for d in ('explorer', 'embed', 'media'): (root / d).mkdir(parents=True, exist_ok=True)
    (root / 'explorer' / 'index.html').write_text(stamp(explorer), encoding='utf-8')
    # landing
    chapters = ''.join('<li class="chap"><img src="media/og/chapter%d.png" width="1200" height="630" alt="%s" loading="lazy"><div><p class="n">%s</p><p class="s">%s</p><a href="explorer/?tab=%s">%s</a></div></li>' % (
        i, html.escape(R['share.alt_chapter'].replace('{name}', R['chapter%d.name' % i]).replace('{sentence}', R['chapter%d.sentence' % i]), quote=True),
        html.escape(R['tabs.' + t]), html.escape(R['chapter%d.sentence' % i]), t, html.escape(R['landing.chapter_link']))
        for i, t in ((1, 'governance'), (2, 'ways'), (3, 'history')))
    landing = fill_tpl((SRC / 'landing.tpl.html').read_text(encoding='utf-8'), R, {
        'HEAD': head(R['landing.page_title'], R['landing.meta_description'], BASE, og('landing.png'), page_alt),
        'CHAPTERS': chapters, 'REPORT_URL': html.escape(T['report_url'], quote=True), 'WIDTH': maxw}, 'landing.tpl.html')
    (root / 'index.html').write_text(stamp(landing), encoding='utf-8')
    # embed page: code samples are built from settings, then shown as text
    ex = BASE + 'explorer/'
    w, hn, hw = settings['embed_width_hint'], T['embed_h_narrow'], T['embed_h_wide']
    title = R['landing.explorer_title']
    code = {
        'CODE_PLAIN': '<iframe\n  src="%s?embed=1&tab=short"\n  title="%s"\n  loading="lazy"\n  style="display:block;width:100%%;max-width:%dpx;height:%dpx;margin:0 auto;border:0"></iframe>' % (ex, title, w, hn),
        'CODE_RESPONSIVE': '<style>.nn-frame{display:block;width:100%%;max-width:%dpx;height:%dpx;margin:0 auto;border:0}\n@media (min-width:%dpx){.nn-frame{height:%dpx}}</style>\n<iframe class="nn-frame" src="%s?embed=1&tab=short" title="%s" loading="lazy"></iframe>' % (w, hn, T['embed_breakpoint'], hw, ex, title),
        'CODE_AUTO': '<iframe id="nn-explorer" src="%s?embed=1&tab=short"\n  title="%s" loading="lazy"\n  style="display:block;width:100%%;max-width:%dpx;height:%dpx;margin:0 auto;border:0"></iframe>\n<script>\naddEventListener(\'message\', function (e) {\n  var d = e.data, f = document.getElementById(\'nn-explorer\');\n  if (!d || d.source !== \'nn-explorer\' || d.type !== \'height\' || e.source !== f.contentWindow) return;\n  f.style.height = d.height + \'px\';\n});\n</script>' % (ex, title, w, hn),
        'CODE_STILL': '<a href="%s?tab=short">\n  <img src="nodes-networks-in-short.png" width="1080" height="1350"\n       style="max-width:100%%;height:auto"\n       alt="%s">\n</a>' % (ex, R['embed.still_alt']),
    }
    esc_code = {k: html.escape(v, quote=False) for k, v in code.items()}
    rows = ''.join('<tr><th scope="row">%s</th><td><code>%s</code></td><td><a href="../explorer/?tab=%s">%s?tab=%s</a></td></tr>' % (html.escape(R['embed.tab.' + t]), t, t, ex, t) for t in TABS)
    embed = fill_tpl((SRC / 'embed.tpl.html').read_text(encoding='utf-8'), R, {
        **esc_code, 'HEAD': head(R['embed.page_title'], R['embed.meta_description'], BASE + 'embed/', og('landing.png'), page_alt), 'TAB_ROWS': rows}, 'embed.tpl.html')
    (root / 'embed' / 'index.html').write_text(stamp(embed), encoding='utf-8')
    # media: committed encodes, posters, share images, plus a caption file built from copy.md
    if STAMP['media']: copy_tree(MEDIA, root / 'media')
    (root / 'media' / 'nodes-networks.vtt').write_text(vtt(R, tl), encoding='utf-8')
    return R, T, warns


def copy_tree(src, dst):
    for dp, _, fs in os.walk(str(src)):
        rel = os.path.relpath(dp, str(src)); d = dst if rel == '.' else dst / rel
        d.mkdir(parents=True, exist_ok=True)
        for f in fs:
            if not f.startswith('.'): shutil.copy2(os.path.join(dp, f), str(d / f))


def run_build(out):
    try:
        R, T, warns = build(out)
    except BuildError as e:
        print('\nnn/build.py FAILED:\n  ' + str(e) + '\n', file=sys.stderr)
        return False
    print('nn build ok ->', out / 'nodes-and-networks')
    return True


# ---------------------------------------------------------------- watch
def watch(out):
    from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
    version = [time.time()]
    snippet = b'<script>(function(){var v;setInterval(function(){fetch("/__v").then(function(r){return r.text()}).then(function(t){if(v&&v!==t)location.reload();v=t}).catch(function(){})},700)})()</script>'

    class H(SimpleHTTPRequestHandler):
        def __init__(self, *a, **k): super().__init__(*a, directory=str(out), **k)
        def log_message(self, *a): pass
        def do_GET(self):
            if self.path == '/__v':
                self.send_response(200); self.send_header('Content-Type', 'text/plain'); self.end_headers(); self.wfile.write(str(version[0]).encode()); return
            p = self.translate_path(self.path.split('?')[0])
            if os.path.isdir(p): p = os.path.join(p, 'index.html')
            if p.endswith('.html') and os.path.exists(p):
                body = open(p, 'rb').read().replace(b'</body>', snippet + b'</body>')
                self.send_response(200); self.send_header('Content-Type', 'text/html; charset=utf-8'); self.send_header('Content-Length', str(len(body))); self.end_headers(); self.wfile.write(body); return
            super().do_GET()
    srv = ThreadingHTTPServer(('127.0.0.1', 8000), H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()

    def stamp():
        return max((f.stat().st_mtime for d in (SRC, DATA, CONTENT, MEDIA, HERE / 'video') if d.exists() for f in d.rglob('*') if f.is_file()), default=0)
    run_build(out); last = stamp()
    print('serving http://localhost:8000/nodes-and-networks/  (Ctrl-C to stop)')
    try:
        while True:
            time.sleep(0.6)
            s = stamp()
            if s != last:
                last = s; print('change detected, rebuilding'); run_build(out); version[0] = time.time()
    except KeyboardInterrupt:
        srv.shutdown()


if __name__ == '__main__':
    if sys.version_info < (3, 7): print('nn/build.py: Python 3.7+ needed', file=sys.stderr); sys.exit(1)
    if '--check' in sys.argv:
        tmp = pathlib.Path(tempfile.mkdtemp()); ok = run_build(tmp); shutil.rmtree(tmp, ignore_errors=True); sys.exit(0 if ok else 1)
    STAMP['label'] = argv('--stamp', STAMP['label'])
    if '--fallback' in sys.argv:   # refresh the committed copy that build-dist.sh uses when the Cloudflare build cannot run
        STAMP['label'] = 'fallback copy (built locally)'; STAMP['media'] = False
        fb = HERE / 'built'; shutil.rmtree(str(fb), ignore_errors=True); sys.exit(0 if run_build(fb) else 1)
    out = pathlib.Path(argv('--out', HERE / '_out')).resolve()
    if '--watch' in sys.argv: watch(out)
    else: sys.exit(0 if run_build(out) else 1)
