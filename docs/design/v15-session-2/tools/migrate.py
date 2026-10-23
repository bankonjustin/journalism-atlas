"""Migration helpers for v15 Session 2: add component classes, strip old visual CSS for those classes."""
import re, os, sys, json
REPO = os.path.expanduser('~/Documents/GitHub/journalism-atlas')

VISUAL = re.compile(r'^(background(-[a-z]+)?|color|border(-(top|right|bottom|left))?(-(color|width|style|radius))?|border-(top|bottom)-(left|right)-radius|box-shadow|font(-(family|size|weight|style|variant))?|letter-spacing|text-transform|text-decoration(-[a-z]+)?|line-height|padding(-(top|right|bottom|left))?|min-height|height|transition(-[a-z]+)?|cursor|outline(-[a-z]+)?|opacity|transform|-webkit-appearance|appearance|text-shadow|filter|text-underline-offset)$', re.I)
# 'display' removed only for inline-block / inline-flex (components.css provides inline-flex)
STATE = re.compile(r':(hover|active|focus|focus-visible|disabled|focus-within)|\[disabled|\[aria-(disabled|pressed|selected|current)|\.(active|is-active|selected|is-selected)\b')

def class_in_selector(sel, tokens):
    """True if the simple selector (no combinators) is one of tokens, optionally tag-prefixed, with pseudo/attr states."""
    sel = sel.strip()
    for t in tokens:
        if re.match(r'^(?:[a-z0-9]+)?\.%s(?![\w-])(?:%s)*$' % (re.escape(t), r'(?::[\w-]+(?:\([^)]*\))?|\[[^\]]*\]|\.[\w-]+)'), sel):
            return True
    return False

def process_css(css, tokens, log, keep_rest=True):
    """Strip visual declarations of rules targeting tokens. Returns new css."""
    out = []; pos = 0
    pat = re.compile(r'([^{}]+)\{([^{}]*)\}')
    def repl(m):
        sel_text, body = m.group(1), m.group(2)
        # peel off leading comments/@media wrapper remnants kept as-is
        lead = ''
        cm = re.match(r'^(\s*(?:/\*.*?\*/\s*)*)(.*)$', sel_text, re.S)
        lead, sel_only = cm.group(1), cm.group(2)
        if sel_only.strip().startswith('@'):
            return m.group(0)
        sels = [s for s in sel_only.split(',')]
        tgt = [s for s in sels if class_in_selector(s, tokens)]
        if not tgt:
            return m.group(0)
        others = [s for s in sels if not class_in_selector(s, tokens)]
        if others:
            # shared rule: drop only the target selectors, keep the rest untouched
            log.append(('shared-rule: removed selectors', [s.strip() for s in tgt]))
            return lead + ','.join(others).strip() + ' {' + body + '}'
        is_state = any(STATE.search(s) for s in tgt)
        decls = [d for d in re.split(r';(?![^()]*\))', body) if d.strip()]
        kept = []
        for d in decls:
            if ':' not in d: kept.append(d); continue
            prop, _, val = d.partition(':'); prop = prop.strip(); val = val.strip()
            if prop.startswith('--'): kept.append(d); continue
            if VISUAL.match(prop): continue
            if prop == 'display' and re.match(r'^(inline-block|inline-flex|inline)$', val): continue
            if is_state:   # state rules: keep nothing but layout-neutral props (there are none worth keeping)
                continue
            kept.append(d)
        log.append(('rule', ','.join(s.strip() for s in tgt)[:60], 'kept:' + ';'.join(k.strip() for k in kept)[:100]))
        if not kept:
            return lead.rstrip() + ('\n' if lead.strip() else '')
        return lead + sel_only.strip() + ' {' + ';'.join(kept).rstrip(';') + ';' + ' }'
    new = pat.sub(repl, css)
    # collapse blank-line runs left by deleted rules
    new = re.sub(r'\n[ \t]*\n[ \t]*\n+', '\n\n', new)
    return new

def style_blocks(text):
    return [(m.start(1), m.end(1)) for m in re.finditer(r'<style\b[^>]*>(.*?)</style>', text, re.S | re.I)]

def migrate_file(path, tokens, add_classes, strip_css=True, dry=False, only_tags=('a', 'button', 'input')):
    full = os.path.join(REPO, path)
    t = open(full, encoding='utf-8', newline='').read(); o = t
    log = []
    # 1. markup: add classes to elements carrying any token
    n_added = 0
    def addcls(m):
        nonlocal n_added
        tag, attrs = m.group(1), m.group(2)
        if tag.lower() not in only_tags: return m.group(0)
        cm = re.search(r'class="([^"]*)"', attrs)
        if not cm: return m.group(0)
        words = cm.group(1).split()
        if not any(tok in words for tok in tokens): return m.group(0)
        new = [w for w in add_classes.split() if w not in words]
        if not new: return m.group(0)
        n_added += 1
        attrs2 = attrs.replace(cm.group(0), 'class="%s"' % (cm.group(1) + ' ' + ' '.join(new)), 1)
        return '<' + tag + attrs2 + '>'
    # skip <style> and <script> text for markup edits? JS template strings carry markup too, so keep them.
    t = re.sub(r'<(\w+)(\s[^>]*)>', addcls, t)
    # JS-built markup via className / classList is handled manually by the caller
    # 2. CSS
    if strip_css:
        if path.endswith('.css'):
            t = process_css(t, tokens, log)
        else:
            for s, e in reversed(style_blocks(t)):
                t = t[:s] + process_css(t[s:e], tokens, log) + t[e:]
    if not dry and t != o:
        open(full, 'w', encoding='utf-8', newline='').write(t)
    return n_added, log
