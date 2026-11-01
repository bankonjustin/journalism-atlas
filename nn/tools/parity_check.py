#!/usr/bin/env python3
"""Compare nn/data/public-snapshot.json with the data inside the live ASU explorer
(preview/nn-launch-kit/explorer/index.html), all 169 rows: name, founding year, origin,
mechanism, revenue and status. Exits 1 on any difference. Read-only; standard library only.
Run locally and in brand-check.yml. nn/build.py only warns (parity_diffs), so a mismatch never
sends Cloudflare to the stale nn/built/ fallback.
Usage: python3 nn/tools/parity_check.py"""
import json, re, sys, pathlib
HERE = pathlib.Path(__file__).resolve().parent.parent
EMBED = HERE.parent / 'preview' / 'nn-launch-kit' / 'explorer' / 'index.html'
FIELDS = (('nm', 'name'), ('fy', 'founding year'), ('o', 'origin'), ('m', 'mechanism'), ('rv', 'revenue'), ('st', 'status'))


def parity_diffs():
    snap = json.load(open(HERE / 'data' / 'public-snapshot.json'))['nodes']
    m = re.search(r'<script type="application/json" id="nn-data">(.*?)</script>', open(EMBED, encoding='utf-8').read(), re.S)
    if not m: return ['no nn-data block found in %s' % EMBED]
    emb = json.loads(m.group(1))['nodes']
    if len(snap) != 169 or len(emb) != 169: return ['row counts: snapshot %d, embed %d (expected 169)' % (len(snap), len(emb))]
    out = []
    for s, e in zip(snap, emb):
        if s['i'] != e['i']: out.append('row order differs at node %s' % s['i']); continue
        for k, label in FIELDS:
            a, b = s.get(k) or '', e.get(k) or ''
            if a != b: out.append('node %s %s: %s %s -> embed %s' % (s['i'], s['nm'], label, a or '(none)', b or '(none)'))
    return out


if __name__ == '__main__':
    d = parity_diffs()
    for x in d: print('parity:', x)
    print('parity: %s' % ('OK, snapshot matches the live embed on all 169 rows' if not d else '%d difference(s)' % len(d)))
    sys.exit(1 if d else 0)
