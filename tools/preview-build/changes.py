#!/usr/bin/env python3
"""CHANGES.md: paragraph-level diff between the deployed preview text (content.json as
committed at git HEAD) and the new build, grouped by section. Accepted text only; deleted
tracked text and comments are never read here. Prose is shown trimmed, old -> new.
"""
import datetime
import difflib
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = (HERE / '../..').resolve()
TRIM = 110


def text_of(runs):
    return ''.join(r.get('t', ' ' if r.get('br') else '') for r in runs)


def deleted_phrases(docx):
    """Tracked-deletion text from the docx, held in memory only, so it can be masked in CHANGES.md."""
    import re, zipfile
    xml = zipfile.ZipFile(Path(docx).expanduser()).read('word/document.xml').decode()
    out = []
    for body in re.findall(r'<w:del [^>]*>(.*?)</w:del>', xml, re.S):
        t = ' '.join(''.join(re.findall(r'<w:delText[^>]*>([^<]*)</w:delText>', body)).split())
        if len(t) >= 30:
            out.append(t)
    return sorted(out, key=len, reverse=True)


def sections(content, mask=()):
    """[(section heading, subheading) -> [paragraph text]] in document order."""
    out, order = {}, []
    sec = sub = '(title block)'
    for b in content['blocks']:
        if b['type'] == 'figure':
            continue
        t = ' '.join(text_of(b['runs']).split())
        for m in mask:
            t = t.replace(m, '[text deleted in the doc]')
        if b['type'] == 'h2':
            sec, sub = t, None
        elif b['type'] == 'h3':
            sub = t
        key = (sec, sub)
        if key not in out:
            out[key] = []
            order.append(key)
        out[key].append(t)
    return out, order


def trim(s, anchor=None):
    s = s.strip()
    if len(s) <= TRIM:
        return s
    return s[:TRIM].rstrip() + '…'


def word_diff(a, b):
    """Trimmed window around the first and last differing words."""
    aw, bw = a.split(), b.split()
    sm = difflib.SequenceMatcher(None, aw, bw, autojunk=False)
    ops = [o for o in sm.get_opcodes() if o[0] != 'equal']
    if not ops:
        return trim(a), trim(b)
    i1, j1 = min(o[1] for o in ops), min(o[3] for o in ops)
    i2, j2 = max(o[2] for o in ops), max(o[4] for o in ops)
    pad = 6
    def win(w, lo, hi):
        s = ' '.join(w[max(0, lo - pad):hi + pad])
        return ('… ' if lo - pad > 0 else '') + s + (' …' if hi + pad < len(w) else '')
    cut = lambda x: x if len(x) <= 320 else x[:320].rstrip() + ' …'
    return cut(win(aw, i1, i2)), cut(win(bw, j1, j2))


def main():
    new = json.loads((HERE / 'content' / 'content.json').read_text())
    old_raw = subprocess.run(['git', 'show', 'HEAD:tools/preview-build/content/content.json'], cwd=REPO,
                             capture_output=True, text=True, check=True).stdout
    old = json.loads(old_raw)
    mask = deleted_phrases(json.loads((HERE / 'config.json').read_text())['docx'])
    o_secs, o_order = sections(old, mask)
    n_secs, n_order = sections(new)
    lines = [f"# Changes since the deployed preview", '',
             f"**Draft: generated from a dry run. The lint gate currently fails on this docx, so no new page has been built.** "
             f"Old: {old['source']['file']} (the text now live). New: {new['source']['file']}. "
             f"Generated {datetime.date.today().isoformat()}. Accepted text only; figure labels, captions and the "
             "byline are listed at the end.", '']
    total = 0
    # pair sections: same key, or same top-level heading when a cohort heading changed
    keys = list(n_order) + [k for k in o_order if k not in n_secs]
    for key in keys:
        o, n = o_secs.get(key, []), n_secs.get(key, [])
        sm = difflib.SequenceMatcher(None, o, n, autojunk=False)
        items = []
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag == 'equal':
                continue
            if tag == 'replace':
                # pair paragraphs by similarity inside the block
                for k in range(max(i2 - i1, j2 - j1)):
                    a = o[i1 + k] if i1 + k < i2 else None
                    b = n[j1 + k] if j1 + k < j2 else None
                    if a and b:
                        r = difflib.SequenceMatcher(None, a, b, autojunk=False).quick_ratio()
                        if r < 0.5:
                            items += [f'- **Removed:** {trim(a)}', f'- **Added:** {trim(b)}']
                        else:
                            x, y = word_diff(a, b)
                            items.append(f'- **Changed:** {x}  →  {y}')
                    elif a:
                        items.append(f'- **Removed:** {trim(a)}')
                    else:
                        items.append(f'- **Added:** {trim(b)}')
            elif tag == 'delete':
                items += [f'- **Removed:** {trim(a)}' for a in o[i1:i2]]
            else:
                items += [f'- **Added:** {trim(b)}' for b in n[j1:j2]]
        if items:
            total += len(items)
            sec, sub = key
            lines += [f"## {sec}" + (f" › {sub}" if sub else ''), ''] + items + ['']
    # title block, byline, figures (from config at HEAD vs now)
    ocfg = json.loads(subprocess.run(['git', 'show', 'HEAD:tools/preview-build/config.json'], cwd=REPO,
                                     capture_output=True, text=True, check=True).stdout)
    cfg = json.loads((HERE / 'config.json').read_text())
    lines += ['## Title, byline and figures', '']
    ot = next(text_of(b['runs']).strip() for b in old['blocks'] if b['type'] == 'h1')
    nt = next(text_of(b['runs']).strip() for b in new['blocks'] if b['type'] == 'h1')
    if ot != nt:
        lines.append(f'- **Title:** {ot}  →  {nt}')
    if ocfg.get('byline') != cfg.get('byline'):
        lines.append(f"- **Byline:** {ocfg.get('byline')}  →  {cfg.get('byline')}")
    lines.append('- **Added:** a "Draft updated [date]" line under the banner.')
    for f in ocfg['figures']:
        lines.append(f"- Old Figure {f['n']} ({f['title']}): " + (
            'removed (INN treemap)' if f['file'] == 'fig_inn_concentration.html' else
            'now Figure ' + str(next(g['n'] for g in cfg['figures'] if g['file'] == f['file']))))
    for f in cfg['figures']:
        lines.append(f"- **{f['label']}**")
    lines.append('')
    if total == 0:
        lines += ['No paragraph-level changes.', '']
    lines += [f'_{total} changed paragraph(s)._', '']
    (HERE / 'CHANGES.md').write_text('\n'.join(lines))
    print(f'CHANGES.md: {total} change line(s)')


if __name__ == '__main__':
    main()
