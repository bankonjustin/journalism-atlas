#!/usr/bin/env python3
"""Apply patches.json to content/content.json (parse-time mechanical fixes, logged).

Every edit must match exactly once at its (para, run); otherwise exit 1 and nothing is written.
'at': 'start' means the find string must be the run's prefix. Rewrites content/content.json (and content.md) in place and writes patches_log.json. The docx is never modified.
Run it right after parse_docx.py (make parse does); a second run without a re-parse fails, by design.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = json.loads((HERE / 'patches.json').read_text())
content = json.loads((HERE / 'content' / 'content.json').read_text())
log, errors = [], []
for p in spec['patches']:
    for e in p['edits']:
        blocks = [b for b in content['blocks'] if b.get('para') == e['para'] and 'runs' in b]
        if len(blocks) != 1:
            errors.append(f"{p['id']}: para {e['para']} matched {len(blocks)} blocks")
            continue
        runs = blocks[0]['runs']
        if e['run'] >= len(runs) or 't' not in runs[e['run']]:
            errors.append(f"{p['id']}: para {e['para']} run {e['run']} has no text")
            continue
        t = runs[e['run']]['t']
        n = t.count(e['find'])
        if n != 1 or (e.get('at') == 'start' and not t.startswith(e['find'])):
            errors.append(f"{p['id']}: '{e['find']}' matched {n}x in para {e['para']} run {e['run']} (need exactly 1)")
            continue
        runs[e['run']]['t'] = t.replace(e['find'], e['replace'], 1)
        log.append({'id': p['id'], 'reason': p['reason'], 'para': e['para'], 'run': e['run'],
                    'find': e['find'], 'replace': e['replace']})
if errors:
    print('PATCH FAILED:\n  ' + '\n  '.join(errors))
    sys.exit(1)
(HERE / 'content' / 'content.json').write_text(json.dumps(content, ensure_ascii=False, indent=1) + '\n')
from parse_docx import to_markdown
(HERE / 'content' / 'content.md').write_text(to_markdown(content))
(HERE / 'patches_log.json').write_text(json.dumps(log, ensure_ascii=False, indent=1))
print(f'patched: {len(log)} edits from {len(spec["patches"])} patches')
for l in log:
    print(f"  {l['id']} ¶{l['para']} run {l['run']}: {l['find']!r} -> {l['replace']!r}")
