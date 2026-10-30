#!/usr/bin/env python3
"""python3 srt.py <schedule.json> <out.srt>  (head + sub lines joined, split at every boundary)"""
import json, sys
d = json.load(open(sys.argv[1])); H, SU = d['HEAD'], d['SUB']; END = d['END']
cuts = sorted({0, 30000} | {x for s, e, *_ in H + SU for x in (s, e)} | {26000})
def ts(ms): return '%02d:%02d:%02d,%03d' % (ms // 3600000, ms // 60000 % 60, ms // 1000 % 60, ms % 1000)
out, n = [], 0
for a, b in zip(cuts, cuts[1:]):
    if a >= 26000: lines = END
    else: lines = [t for s, e, t, *_ in H if s <= a < e] + [t for s, e, t, *_ in SU if s <= a < e]
    if not lines: continue
    if out and out[-1][2] == lines and out[-1][1] == a: out[-1][1] = b
    else: out.append([a, b, lines])
with open(sys.argv[2], 'w') as f:
    for i, (a, b, l) in enumerate(out, 1): f.write('%d\n%s --> %s\n%s\n\n' % (i, ts(a), ts(b), '\n'.join(l)))
print(len(out), 'cues')
