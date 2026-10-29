#!/usr/bin/env python3
"""LOCAL ONLY. Refresh nn/data/public-snapshot.json from the private canonical files.
The snapshot holds only values that already appear in the public explorer page (name, founding year,
revenue, origin, mechanism, status). The deploy build reads it, so the private CSVs never leave the private repo.
Usage: python3 nn/tools/snapshot.py [--csv PATH] [--recode PATH] [--origin v22|v22.3]
Reads the CSV and recode file read-only."""
import json, csv, sys, pathlib
HERE = pathlib.Path(__file__).resolve().parent.parent
ARG = lambda k, d: sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d
CSV = pathlib.Path(ARG('--csv', HERE.parent.parent / 'paper-one-band-dataset' / 'cohort_reference_expanded_v22.csv'))
RECODE = pathlib.Path(ARG('--recode', HERE.parent.parent / 'nodes-networks-v5' / 'launch-kit' / 'MECH-RECODE-PROPOSED.csv'))
ORIGIN_RULE = ARG('--origin', 'v22.3')
STATUS = {'CLOSED': 'closed', 'ACQUIRED': 'acquired', 'ABSORBED': 'absorbed'}
OMAP = {'BORN_ABOVE': 'INHERITED', 'CROSSED': 'CROSSED', 'NEVER_CROSSED': 'NEVER_CROSSED'}
nodes = json.load(open(HERE / 'data' / 'nodes169.json'))['nodes']
banded = [r for r in csv.DictReader(open(CSV)) if r['Band_Position']]
assert len(nodes) == 169 and len(banded) == 169, 'expected 169 banded rows'
assert all(n['name'] == banded[n['i']]['Organization / Creator'] for n in nodes if not n['un']), 'node order no longer matches the CSV'
recode = {}
for r in csv.DictReader(open(RECODE)):
    if (r.get('approved (yes/no)') or '').strip().lower() == 'yes' and r['proposed_path']: recode[(r['data_name'], r['cohort'])] = r['proposed_path']
assert recode, 'recode file has no approved rows'
byk = {(n['name'], n['c']): n for n in nodes}
assert all(k in byk for k in recode), 'a recode row matches no node'
out = []
for n in nodes:
    r = banded[n['i']]; nm, fy = n['name'], n['fy']
    if n['un']:
        assert r['Public_Release_Flag'] == 'EXCLUDE_UNVERIFIED' and r['Cohort'] == n['c']
        nm, fy = r['Organization / Creator'], int(float(r['Founding_Year']))
    o = n['orig']
    if ORIGIN_RULE == 'v22.3' and r['Origin_Position'] in OMAP: o = OMAP[r['Origin_Position']]
    out.append({'i': n['i'], 'nm': nm, 'fy': fy, 'o': o, 'm': recode.get((n['name'], n['c']), n['mech']), 'rv': int(float(r['Revenue_Raw'])), 'st': STATUS.get(n['cl'], '')})
json.dump({'origin_rule': ORIGIN_RULE, 'nodes': out}, open(HERE / 'data' / 'public-snapshot.json', 'w'), separators=(',', ':'))
print('snapshot', len(out), 'nodes, origin rule', ORIGIN_RULE)
