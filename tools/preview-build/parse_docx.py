#!/usr/bin/env python3
"""docx -> content.json + content.md for the Nodes and Networks preview page.

Reads word/document.xml directly (stdlib only, no pandoc). Accepted text only:
<w:ins>/<w:moveTo> kept, <w:del>/<w:moveFrom> dropped. comments.xml is never
read here, and comment anchors/references are skipped, so no comment text can
reach the output. Prose is preserved exactly: no quote or dash normalization.

Usage: python3 parse_docx.py [--docx PATH]   (default: config.json "docx")
"""
import argparse
import datetime
import hashlib
import json
import re
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

HERE = Path(__file__).resolve().parent
W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
PR = 'http://schemas.openxmlformats.org/package/2006/relationships'


def q(tag, ns=W):
    return f'{{{ns}}}{tag}'


def on(el):
    """Toggle property (<w:b/>, <w:i/>): present and not val=0/false."""
    if el is None:
        return False
    return el.get(q('val'), 'true').lower() not in ('0', 'false', 'off')


class Parser:
    def __init__(self, docx, keep_deleted_figures=True):
        self.keep_deleted_figures = keep_deleted_figures
        self.zip = zipfile.ZipFile(docx)
        names = set(self.zip.namelist())
        self.doc = ET.fromstring(self.zip.read('word/document.xml'))
        self.rels = {}
        rels = ET.fromstring(self.zip.read('word/_rels/document.xml.rels'))
        for rel in rels.iter(q('Relationship', PR)):
            self.rels[rel.get('Id')] = rel.get('Target')
        self.list_fmt = self._numbering() if 'word/numbering.xml' in names else {}
        self.notes = {}
        for kind in ('footnotes', 'endnotes'):
            if f'word/{kind}.xml' in names:
                self._load_notes(kind)
        self.stats = {'ins': 0, 'del': 0, 'moveFrom': 0, 'moveTo': 0,
                      'deleted_paragraph_marks': 0, 'comment_anchors_skipped': 0}
        self.tracked = []
        self.note_order = []

    def _numbering(self):
        root = ET.fromstring(self.zip.read('word/numbering.xml'))
        abstract = {}
        for an in root.iter(q('abstractNum')):
            levels = {}
            for lvl in an.iter(q('lvl')):
                fmt = lvl.find(q('numFmt'))
                levels[lvl.get(q('ilvl'))] = fmt.get(q('val')) if fmt is not None else 'decimal'
            abstract[an.get(q('abstractNumId'))] = levels
        out = {}
        for num in root.iter(q('num')):
            aid = num.find(q('abstractNumId')).get(q('val'))
            out[num.get(q('numId'))] = abstract.get(aid, {})
        return out

    def _load_notes(self, kind):
        root = ET.fromstring(self.zip.read(f'word/{kind}.xml'))
        for note in root:
            nid = note.get(q('id'))
            if note.get(q('type')) in ('separator', 'continuationSeparator', 'continuationNotice'):
                continue
            runs = []
            for p in note.iter(q('p')):
                runs += self.runs(p) + [{'t': ' '}]
            self.notes[(kind, nid)] = merge(runs)

    # -- inline content ------------------------------------------------------
    def runs(self, p, para_idx=None):
        """Return run dicts for a paragraph; drawings become {'figure': True}."""
        out = []
        self._walk(p, out, href=None, para_idx=para_idx)
        return out

    def _walk(self, el, out, href, para_idx):
        for child in el:
            tag = child.tag
            if tag == q('pPr'):
                rpr = child.find(q('rPr'))
                if rpr is not None and rpr.find(q('del')) is not None:
                    self.stats['deleted_paragraph_marks'] += 1
                continue
            if tag in (q('del'), q('moveFrom')):
                key = 'del' if tag == q('del') else 'moveFrom'
                self.stats[key] += 1
                text = ''.join(t.text or '' for t in child.iter(q('delText')))
                drawings = sum(1 for _ in child.iter(q('drawing')))
                self.tracked.append({'type': key, 'para': para_idx,
                                     'author': child.get(q('author')), 'text': text,
                                     'drawings': drawings})
                # A figure image caught inside a tracked deletion is kept only when
                # config says so; the ledger flags it either way.
                if self.keep_deleted_figures:
                    out.extend({'figure': True, 'in_deletion': True} for _ in range(drawings))
                continue
            if tag in (q('ins'), q('moveTo')):
                key = 'ins' if tag == q('ins') else 'moveTo'
                self.stats[key] += 1
                text = ''.join(t.text or '' for t in child.iter(q('t')))
                self.tracked.append({'type': key, 'para': para_idx,
                                     'author': child.get(q('author')), 'text': text})
                self._walk(child, out, href, para_idx)
                continue
            if tag in (q('commentRangeStart'), q('commentRangeEnd')):
                self.stats['comment_anchors_skipped'] += 1
                continue
            if tag == q('hyperlink'):
                rid = child.get(q('id', R))
                anchor = child.get(q('anchor'))
                link = self.rels.get(rid) if rid else (f'#{anchor}' if anchor else None)
                self._walk(child, out, link, para_idx)
                continue
            if tag == q('r'):
                self._run(child, out, href)
                continue
            if tag in (q('smartTag'), q('sdt'), q('sdtContent'), q('fldSimple')):
                self._walk(child, out, href, para_idx)
                continue
            # bookmarks, proofErr, permStart, etc. carry no text

    def _run(self, r, out, href):
        rpr = r.find(q('rPr'))
        b = on(rpr.find(q('b'))) if rpr is not None else False
        i = on(rpr.find(q('i'))) if rpr is not None else False
        sup = False
        if rpr is not None:
            va = rpr.find(q('vertAlign'))
            sup = va is not None and va.get(q('val')) == 'superscript'
        for c in r:
            tag = c.tag
            if tag == q('t'):
                out.append({'t': c.text or '', 'b': b, 'i': i, 'href': href, 'sup': sup})
            elif tag == q('tab'):
                out.append({'t': '\t', 'b': b, 'i': i, 'href': href})
            elif tag in (q('br'), q('cr')):
                out.append({'br': True})
            elif tag == q('noBreakHyphen'):
                out.append({'t': '‑', 'b': b, 'i': i, 'href': href})
            elif tag == q('sym'):
                out.append({'t': chr(int(c.get(q('char')), 16)), 'b': b, 'i': i, 'href': href})
            elif tag == q('drawing') or tag == q('pict'):
                out.append({'figure': True})
            elif tag in (q('footnoteReference'), q('endnoteReference')):
                kind = 'footnotes' if tag == q('footnoteReference') else 'endnotes'
                key = (kind, c.get(q('id')))
                self.note_order.append(key)
                out.append({'note': len(self.note_order)})
            # commentReference, delText, lastRenderedPageBreak: skipped

    # -- block content -------------------------------------------------------
    def parse(self):
        body = self.doc.find(q('body'))
        blocks = []
        fig_n = 0
        for idx, p in enumerate(c for c in body if c.tag == q('p')):
            ppr = p.find(q('pPr'))
            style = ''
            numpr = None
            if ppr is not None:
                ps = ppr.find(q('pStyle'))
                style = ps.get(q('val')) if ps is not None else ''
                numpr = ppr.find(q('numPr'))
            runs = self.runs(p, idx)
            # split around drawings so a figure inside a text paragraph stands alone
            segments, cur, fig_in_del = [], [], []
            for r in runs:
                if r.get('figure'):
                    fig_in_del.append(bool(r.get('in_deletion')))
                    segments.append(('text', cur))
                    segments.append(('figure', None))
                    cur = []
                else:
                    cur.append(r)
            segments.append(('text', cur))
            for kind, seg in segments:
                if kind == 'figure':
                    fig_n += 1
                    blocks.append({'type': 'figure', 'n': fig_n, 'para': idx})
                    if fig_in_del.pop(0):
                        blocks[-1]['in_deletion'] = True
                    continue
                seg = merge(seg)
                if not text_of(seg).strip():
                    continue
                block = {'type': block_type(style), 'para': idx, 'runs': seg}
                if numpr is not None and block['type'] == 'p':
                    ilvl = numpr.find(q('ilvl'))
                    nid = numpr.find(q('numId'))
                    ilvl = ilvl.get(q('val')) if ilvl is not None else '0'
                    nid = nid.get(q('val')) if nid is not None else '0'
                    fmt = self.list_fmt.get(nid, {}).get(ilvl, 'decimal')
                    block.update(type='li', list_id=nid, level=int(ilvl),
                                 ordered=fmt != 'bullet')
                blocks.append(block)
        notes = []
        for n, key in enumerate(self.note_order, 1):
            notes.append({'n': n, 'kind': key[0], 'runs': self.notes.get(key, [])})
        return blocks, notes


def block_type(style):
    s = style.lower().replace(' ', '')
    if s in ('heading1', 'title'):
        return 'h1'
    if s == 'heading2':
        return 'h2'
    if s == 'heading3':
        return 'h3'
    return 'p'


def merge(runs):
    """Merge adjacent runs with identical formatting; drop empty flags for a smaller diff."""
    out = []
    for r in runs:
        if 'br' in r or 'note' in r:
            out.append(r)
            continue
        r = {k: v for k, v in r.items() if v}
        if 't' not in r:
            continue
        if out and 't' in out[-1] and {k: v for k, v in out[-1].items() if k != 't'} == \
                {k: v for k, v in r.items() if k != 't'}:
            out[-1]['t'] += r['t']
        else:
            out.append(r)
    return out


def text_of(runs):
    return ''.join(r.get('t', '\n' if r.get('br') else '') for r in runs)


def to_markdown(content):
    """Human-diffable rendering of content.json (not used by the page build)."""
    lines = [f"<!-- generated from {content['source']['file']} sha256 {content['source']['sha256'][:12]} -->", '']

    def md(runs):
        s = ''
        for r in runs:
            if r.get('br'):
                s += '  \n'
                continue
            if 'note' in r:
                s += f"[^{r['note']}]"
                continue
            t = r['t']
            if r.get('i'):
                t = f'*{t}*'
            if r.get('b'):
                t = f'**{t}**'
            if r.get('href'):
                t = f"[{t}]({r['href']})"
            s += t
        return s

    for b in content['blocks']:
        if b['type'] == 'figure':
            lines += [f"[[FIGURE {b['n']}]]", '']
        elif b['type'] == 'li':
            marker = '1.' if b['ordered'] else '-'
            lines.append('  ' * b['level'] + f"{marker} {md(b['runs'])}")
        else:
            prefix = {'h1': '# ', 'h2': '## ', 'h3': '### ', 'p': ''}[b['type']]
            if lines and lines[-1].startswith(('1. ', '- ')):
                lines.append('')
            lines += [prefix + md(b['runs']), '']
    for n in content['notes']:
        lines += [f"[^{n['n']}]: {md(n['runs'])}", '']
    return '\n'.join(lines).rstrip() + '\n'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--docx')
    args = ap.parse_args()
    cfg = json.loads((HERE / 'config.json').read_text())
    docx = Path(args.docx or cfg['docx']).expanduser()
    if not docx.exists():
        sys.exit(f'docx not found: {docx}')
    p = Parser(docx, cfg.get('keep_figures_in_deletions', True))
    blocks, notes = p.parse()
    content = {
        'source': {
            'file': docx.name,
            'sha256': hashlib.sha256(docx.read_bytes()).hexdigest(),
            'parsed': datetime.date.today().isoformat(),
        },
        'tracked_changes': {'counts': p.stats, 'items': p.tracked},
        'blocks': blocks,
        'notes': notes,
    }
    out_dir = HERE / 'content'
    out_dir.mkdir(exist_ok=True)
    (out_dir / 'content.json').write_text(json.dumps(content, ensure_ascii=False, indent=1) + '\n')
    (out_dir / 'content.md').write_text(to_markdown(content))
    counts = {t: sum(1 for b in blocks if b['type'] == t) for t in ('h1', 'h2', 'h3', 'p', 'li', 'figure')}
    print(f'parsed {docx.name}: {counts}, notes={len(notes)}, tracked={p.stats}')


if __name__ == '__main__':
    main()
