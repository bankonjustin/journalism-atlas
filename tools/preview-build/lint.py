#!/usr/bin/env python3
"""Prose lint gate for the Nodes and Networks preview. Reads content/content.json
(accepted text only) and fails the build (exit 1) on any hit, printing the offending
sentence with +-60 characters of context. Figure source code is never linted.

Prose is not edited here or anywhere in the pipeline: fix the Google Doc and re-export.
Usage: python3 lint.py [--quiet]
"""
import json
import re
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
CFG = json.loads((HERE / 'config.json').read_text())
CONTENT = json.loads((HERE / 'content' / 'content.json').read_text())
LABELS = {f['n']: f['label'] for f in CFG['figures']}

# Tokens whose trailing period does not end a sentence.
ABBREV = {'u.s', 'u.k', 'd.c', 'inc', 'corp', 'co', 'ltd', 'llc', 'vs', 'etc', 'e.g', 'i.e', 'st', 'mr',
          'mrs', 'ms', 'dr', 'jr', 'sr', 'no', 'mt', 'dept', 'gov', 'sen', 'rep', 'al', 'approx', 'ca',
          'cf', 'vol', 'ed', 'a.m', 'p.m', 'jan', 'feb', 'mar', 'apr', 'jun', 'jul', 'aug', 'sep',
          'sept', 'oct', 'nov', 'dec', 'ph.d', 'm.d'}
CAPTION_LINE = re.compile(r'^\s*(Figure|Fig\.)\s*\d')


def text_of(runs):
    return ''.join(r.get('t', ' ' if r.get('br') else '') for r in runs)


def prose_and_captions():
    blocks = CONTENT['blocks']
    prose, captions = [], []
    for i, b in enumerate(blocks):
        if 'runs' not in b:
            continue
        t = text_of(b['runs'])
        prev = blocks[i - 1] if i else None
        if prev and prev['type'] == 'figure' and CAPTION_LINE.match(t):
            captions.append((b['para'], t))  # consumed as the docx caption line, not rendered
        else:
            prose.append((b['para'], t))
    return prose, captions


def docx_comments():
    z = zipfile.ZipFile(Path(CFG['docx']).expanduser())
    if 'word/comments.xml' not in z.namelist():
        return []
    xml = z.read('word/comments.xml').decode()
    out = []
    for body in re.findall(r'<w:comment [^>]*>(.*?)</w:comment>', xml, re.S):
        t = ' '.join(''.join(re.findall(r'<w:t[^>]*>([^<]*)</w:t>', body)).split())
        if t:
            out.append(t)
    return out


def ctx(text, m, pad=60):
    a, b = max(0, m.start() - pad), min(len(text), m.end() + pad)
    return ('…' if a else '') + text[a:b].replace('\n', ' ') + ('…' if b < len(text) else '')


def lint():
    prose, captions = prose_and_captions()
    hits = []

    def add(rule, para, text, m):
        hits.append({'rule': rule, 'para': para, 'context': ctx(text, m), 'match': m.group(0)})

    for para, t in prose:
        for m in re.finditer(r'::|;;|,,', t):
            add('doubled punctuation', para, t, m)
        for m in re.finditer(r'(?<![.…])\.\.(?!\.)', t):
            add('doubled punctuation', para, t, m)
        for m in re.finditer(r'[a-z][.,;:][A-Z]', t):
            add('sentence end jammed against next word', para, t, m)
        for m in re.finditer(r'(\S+)\.\s+([a-z]\w*)', t):
            tok = re.sub(r'^[\W_]+', '', m.group(1)).lower()
            if tok in ABBREV or re.fullmatch(r'[a-z]', tok) or re.fullmatch(r'(?:[a-z]\.)+[a-z]?', tok):
                continue
            add('lowercase word opens a sentence', para, t, m)
        for m in re.finditer(r'\b[A-Z]{2}[a-z]+\b', t):
            add('mixed-case typo', para, t, m)
        for m in re.finditer(r'\b9 cohorts?\b', t, re.I):
            add('numeral "9 cohorts" (the paper spells it "nine")', para, t, m)
        for m in re.finditer(r'\b(?:Figure|Fig\.)\s*(\d+)\b([^\n]*)', t):
            n = int(m.group(1))
            if n not in LABELS:
                add(f'Figure {n} does not exist (labels are 1-{len(LABELS)})', para, t, m)
        for m in re.finditer(r'@\S*', t):
            add('surviving @ handle', para, t, m)
        for m in re.finditer(r'\S*asu\.edu\S*', t, re.I):
            add('surviving asu.edu address', para, t, m)
    # docx caption lines: not rendered, but their label must equal the manifest label
    for para, t in captions:
        m = re.match(r'\s*(?:Figure|Fig\.)\s*(\d+)', t)
        n = int(m.group(1))
        if LABELS.get(n, '').strip() != t.strip():
            add(f'docx caption line differs from manifest label "{LABELS.get(n)}"', para, t, m)
    # comment text surviving into prose
    flat = ' '.join(' '.join(t for _, t in prose).split())
    for c in docx_comments():
        if len(c) > 25 and c in flat:
            hits.append({'rule': 'surviving comment text', 'para': None, 'context': c[:120], 'match': c[:40]})
    return hits


def main():
    hits = lint()
    for h in hits:
        print(f"LINT  ¶{h['para']}  {h['rule']}: “{h['match']}”\n      {h['context']}")
    if '--quiet' not in sys.argv:
        print(f'\nlint: {len(hits)} finding(s)')
    (HERE / 'lint_report.json').write_text(json.dumps(hits, indent=1, ensure_ascii=False) + '\n')
    # LINT_ADVISORY=1 is for dry runs in a scratch copy only; the real build never sets it.
    import os
    sys.exit(1 if hits and not os.environ.get('LINT_ADVISORY') else 0)


if __name__ == '__main__':
    main()
