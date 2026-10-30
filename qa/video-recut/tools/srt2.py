#!/usr/bin/env python3
"""python3 srt2.py <schedule.json> <out.srt>"""
import json, sys
d = json.load(open(sys.argv[1])); C = d['CAPS']; END = d['TL']['end']
H = [(s, e, t) for k, s, e, t, _ in C if k == 'H']; Sx = [(s, e, t) for k, s, e, t, _ in C if k == 'S']
cuts = sorted({0, END} | {x for s, e, _ in H + Sx for x in (s, e)})
ts = lambda ms: '%02d:%02d:%02d,%03d' % (ms // 3600000, ms // 60000 % 60, ms // 1000 % 60, ms % 1000)
out = []
for a, b in zip(cuts, cuts[1:]):
    l = [t for s, e, t in H if s <= a < e] + [t for s, e, t in Sx if s <= a < e]
    if not l: continue
    if out and out[-1][2] == l and out[-1][1] == a: out[-1][1] = b
    else: out.append([a, b, l])
open(sys.argv[2], 'w').write(''.join('%d\n%s --> %s\n%s\n\n' % (i, ts(a), ts(b), '\n'.join(l)) for i, (a, b, l) in enumerate(out, 1)))
print(len(out), 'cues')
