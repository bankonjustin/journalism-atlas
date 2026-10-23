"""Shared parser for v15 discovery. Read-only over the repo."""
import re, os, json, csv, collections

REPO = os.path.expanduser('~/Documents/GitHub/journalism-atlas')
SCR = '/private/tmp/claude-502/-Users-bankids-Documents-GitHub/70fa26fc-8f34-41b1-b7d8-511f593c31ee/scratchpad'
OUT = REPO + '/docs/design/v15-discovery'

FILES = [l.strip() for l in open(SCR + '/files.txt') if l.strip()]
FILES = [f for f in FILES if f.endswith(('.html', '.css', '.js')) and not f.startswith(('scripts/', 'convert.js', 'docs/'))]

INTERNAL_PREFIX = ('atlas-portal/', 'lab/', 'preview/smartnews')
INTERNAL_FILES = {
    'atlas-signal-brief.html', 'atlas_pulse_intelligence.html', 'atlas_wire_intelligence.html',
    'atlas_wire_review.html', 'beat-climate.html', 'beat-finance.html', 'beat-tech.html',
    'chicago-analysis.html', 'chicago-survey.html', 'index-pre-homepage.html',
    'partners/_reviewjames copy.html', 'partners/_reviewjames.html', 'partners/_shell.html',
    'partners/njlab copy.html',
}

def page_class(f):
    if not f.endswith('.html'):
        return 'asset'
    if f in INTERNAL_FILES or f.startswith(INTERNAL_PREFIX):
        return 'internal'
    return 'public'


def read(f):
    with open(os.path.join(REPO, f), encoding='utf-8', errors='replace') as fh:
        return fh.read()


def line_of(text, idx):
    return text.count('\n', 0, idx) + 1


def split_html(text):
    """Return list of (kind, start_idx, end_idx) for style/script blocks inside an html text."""
    blocks = []
    for m in re.finditer(r'<style\b[^>]*>(.*?)</style>', text, re.S | re.I):
        blocks.append(('style', m.start(1), m.end(1)))
    for m in re.finditer(r'<script\b([^>]*)>(.*?)</script>', text, re.S | re.I):
        if 'src=' in m.group(1) and not m.group(2).strip():
            continue
        blocks.append(('script', m.start(2), m.end(2)))
    return blocks


def parse_css(text, base_idx=0, full=None):
    """Return list of declarations: dict(line, selector, prop, value, at). line computed against `full` (or text)."""
    full = full if full is not None else text
    decls = []
    stack = []  # (selector, is_at, block_id)
    bid = 0
    buf = ''
    buf_start = 0
    i = 0
    n = len(text)
    in_decl_block = 0
    while i < n:
        c = text[i]
        if text.startswith('/*', i):
            j = text.find('*/', i + 2)
            i = n if j < 0 else j + 2
            continue
        if c in '"\'':
            q = c
            j = i + 1
            while j < n and text[j] != q:
                if text[j] == '\\':
                    j += 1
                j += 1
            buf += text[i:j + 1]
            i = j + 1
            continue
        if text.startswith('url(', i):
            j = text.find(')', i)
            j = n - 1 if j < 0 else j
            buf += text[i:j + 1]
            i = j + 1
            continue
        if c == '{':
            sel = ' '.join(buf.split())
            bid += 1
            stack.append((sel, sel.startswith('@'), (base_idx, bid)))
            buf = ''
            i += 1
            continue
        if c == '}':
            flush(buf, buf_start, stack, decls, base_idx, full)
            buf = ''
            if stack:
                stack.pop()
            i += 1
            continue
        if c == ';':
            flush(buf, buf_start, stack, decls, base_idx, full)
            buf = ''
            i += 1
            continue
        if not buf.strip():
            buf_start = i
        buf += c
        i += 1
    return decls


def flush(buf, buf_start, stack, decls, base_idx, full):
    b = buf.strip()
    if not b or ':' not in b or not stack:
        return
    if stack[-1][1]:  # directly inside an @rule without selector (e.g. @font-face, keyframes frame)
        pass
    prop, _, val = b.partition(':')
    prop = prop.strip()
    if not re.match(r'^-{0,2}[a-zA-Z][\w-]*$', prop):
        return
    sel = ''
    ats = []
    for s, is_at, _b in stack:
        if is_at:
            ats.append(s)
        else:
            sel = s if not sel else sel + ' | ' + s
    if not sel and ats:
        sel = ats[-1]
    decls.append(dict(block=stack[-1][2], line=line_of(full, base_idx + buf_start + (len(buf) - len(buf.lstrip()))), selector=sel,
                      prop=prop.lower() if not prop.startswith('--') else prop, value=' '.join(val.split()),
                      at=' '.join(ats)))


def all_css_decls(f):
    """Declarations from .css file or <style> blocks of html."""
    text = read(f)
    if f.endswith('.css'):
        return parse_css(text, 0, text)
    out = []
    for kind, s, e in split_html(text):
        if kind == 'style':
            out.extend(parse_css(text[s:e], s, text))
    return out


def inline_styles(f):
    """style="" attributes in html markup (outside script/style). returns dict(line, tag, cls, prop, value)."""
    text = read(f)
    if not f.endswith('.html'):
        return []
    out = []
    for m in re.finditer(r'<(\w[\w-]*)\b([^>]*?)\sstyle\s*=\s*"([^"]*)"([^>]*)>', text, re.S):
        tag = m.group(1)
        attrs = m.group(2) + ' ' + m.group(4)
        cm = re.search(r'class\s*=\s*"([^"]*)"', attrs)
        cls = cm.group(1) if cm else ''
        ln = line_of(text, m.start())
        for d in m.group(3).split(';'):
            if ':' in d:
                p, _, v = d.partition(':')
                out.append(dict(line=ln, tag=tag, cls=cls, prop=p.strip().lower(), value=v.strip()))
    return out


def js_lines(f):
    """yield (line_no, line_text) for JS: whole .js file or script blocks of html + HTML template strings in them."""
    text = read(f)
    if f.endswith('.js'):
        for i, l in enumerate(text.split('\n'), 1):
            yield i, l
        return
    if f.endswith('.html'):
        for kind, s, e in split_html(text):
            if kind == 'script':
                start = line_of(text, s)
                for k, l in enumerate(text[s:e].split('\n')):
                    yield start + k, l


def html_markup_lines(f):
    """lines of html that are outside <style>/<script> blocks."""
    text = read(f)
    if not f.endswith('.html'):
        return
    mask = [True] * len(text)
    for kind, s, e in split_html(text):
        for k in range(s, e):
            mask[k] = False
    ln = 1
    cur = []
    for k, ch in enumerate(text):
        if ch == '\n':
            yield ln, ''.join(cur)
            cur = []
            ln += 1
        elif mask[k]:
            cur.append(ch)
    yield ln, ''.join(cur)


def write_csv(path, rows, cols):
    with open(path, 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction='ignore')
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, '') for c in cols})

COLS = ['file', 'line', 'selector', 'property', 'value', 'role', 'surface', 'state', 'element', 'v15_status', 'note']

# ---- heuristics ----
DARK_SEL = re.compile(r'dark|hero|footer|canvas|on-dark|inverse|black|night|stage|banner|cta-band|\bftr|ticker|strip', re.I)
GRAPHIC_SEL = re.compile(r'chart|viz|svg|axis|treemap|sunburst|bubble|figure|\bfig|legend|arc\b|\.bar|node|\bd3|donut|sparkline|heat|swatch|infograph|map', re.I)

def state_of(selector):
    s = selector.lower()
    if ':focus-visible' in s or ':focus' in s:
        return 'focus'
    if ':hover' in s or ':active' in s:
        return 'hover/press'
    if '[aria-current' in s or '[aria-pressed' in s or '[aria-selected' in s or '.active' in s or '.selected' in s or '.is-active' in s or '.current' in s or '.on' in s.split()[-1:]:
        return 'selected'
    if ':disabled' in s or '[disabled' in s or 'disabled' in s:
        return 'disabled'
    if ':visited' in s:
        return 'visited'
    return 'rest'


def element_of(selector):
    s = selector.lower()
    for key, name in [('btn', 'button'), ('button', 'button'), ('cta', 'button'), ('chip', 'tag/chip'), ('pill', 'tag/chip'),
                      ('badge', 'tag/badge'), ('tag', 'tag/badge'), ('nav', 'nav'), ('link', 'link'), ('footer', 'footer'),
                      ('card', 'card'), ('input', 'input'), ('search', 'input'), ('select', 'input'), ('tab', 'tab'),
                      ('eyebrow', 'eyebrow'), ('label', 'label'), ('th', 'table'), ('table', 'table'), ('tooltip', 'tooltip'),
                      ('modal', 'modal'), ('drawer', 'drawer'), ('legend', 'chart')]:
        if key in s:
            return name
    if re.search(r'(^|[\s,|>+~])a(\b|:|\.|\[)', s):
        return 'link'
    return 'other'

COLOR_PROPS_TEXT = {'color', '-webkit-text-fill-color', 'caret-color'}
def role_of(prop):
    p = prop.lower()
    if p in COLOR_PROPS_TEXT:
        return 'text'
    if p.startswith('background') or p in ('fill',) and False:
        return 'fill'
    if p == 'fill':
        return 'fill/icon'
    if p == 'stroke':
        return 'stroke/icon'
    if p.startswith('border') or p.startswith('outline') or p == 'box-shadow' and False:
        return 'border/outline'
    if p == 'box-shadow':
        return 'shadow/ring'
    if p.startswith('text-decoration'):
        return 'underline'
    if p == 'accent-color':
        return 'form-accent'
    if p.startswith('--'):
        return 'variable-def'
    return p

HEX_RE = re.compile(r'#(?:[0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{3,4})\b')

def norm_hex(h):
    h = h.lower().lstrip('#')
    if len(h) in (3, 4):
        h = ''.join(c * 2 for c in h[:3])
    return '#' + h[:6]

def luminance(h):
    h = norm_hex(h).lstrip('#')
    r, g, b = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)

def rule_surface(decls_for_rule, selector):
    """guess surface for a rule from its own declarations + selector name."""
    for d in decls_for_rule:
        if d['prop'].startswith('background'):
            for h in HEX_RE.findall(d['value']):
                if luminance(h) < 0.12:
                    return 'dark'
            if re.search(r'var\(--(?:color-bg-dark|color-bg-card-dark|canvas-bg|black|color-black|gray-(?:cool|neutral)-[678]|color-surface-dark)\)', d['value']):
                return 'dark'
            if re.search(r'\b(black)\b', d['value']):
                return 'dark'
    for d in decls_for_rule:
        if d['prop'] == 'color':
            hs = HEX_RE.findall(d['value'])
            if hs and luminance(hs[0]) > 0.6 and 'var(' not in d['value']:
                return 'dark?'
            if re.search(r'var\(--(?:white|color-white|color-text-dark|color-surface|gray-(?:cool|neutral)-1|canvas-text-primary|color-text-on-dark-2|color-muted-dark|color-link-on-dark)\)', d['value']):
                return 'dark?'
    if DARK_SEL.search(selector):
        return 'dark?'
    return 'light?'
