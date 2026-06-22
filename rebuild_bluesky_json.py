"""
rebuild_bluesky_json.py — Consolidate Bluesky intelligence data.

Task 1: Build assets/data/bluesky-creators.json from atlas_bluesky_handles.tsv
Task 3: Output ryan_handoff_bsky_enrichment_june18.csv (master creators missing Bluesky platform slot)
Task 4: Output ryan_handoff_new_candidates_june18.csv (net-new spidering candidates not in master)
"""

import csv
import json
import os
import re

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))

HANDLES_TSV     = os.path.join(REPO_ROOT, 'atlas_bluesky_handles.tsv')
VERIFIED_TSV    = os.path.join(REPO_ROOT, 'bluesky_verified_eligible.tsv')
S9_TSV          = os.path.join(REPO_ROOT, 'bluesky_s9_atlas_eligible.tsv')
MASTER_CSV      = os.path.join(REPO_ROOT, 'assets', 'data', 'creators-master.csv')
OUT_JSON        = os.path.join(REPO_ROOT, 'assets', 'data', 'bluesky-creators.json')
OUT_ENRICH_CSV  = os.path.join(REPO_ROOT, 'ryan_handoff_bsky_enrichment_june18.csv')
OUT_CANDS_CSV   = os.path.join(REPO_ROOT, 'ryan_handoff_new_candidates_june18.csv')

BSKY_PREFIX = 'https://bsky.app/profile/'

PLATFORM_SLOTS = [
    ('Platform Primary',  'Link Primary'),
    ('Platform 2 Name',   'Platform 2 Link'),
    ('Platform 3 Name',   'Platform 3 Link'),
    ('Platform 4 Name',   'Platform 4 Link'),
]

# Slugs confirmed by Ryan's June 2026 enrichment pass
NEW_BSKY_SLUGS = {
    'casey-lewis', 'emily-atkin', 'parker-molloy', 'amy-westervelt', 'andy-revkin',
    'bill-mckibben', 'brian-merchant', 'jared-yates-sexton', 'jordan-uhl',
    'kai-kupferschmidt', 'katelyn-burns', 'mims', 'paris-marx', 'rachel-donald',
    'raquel-willis', 'sara', 'sarah', 'saul', 'talia-jane', 'maya-higa',
    'anna-fifield', 'liz-carlson', 'thomas-goetz', 'brandon-chew', 'alex-ip',
    'alex-goldman', 'sara-yasin', 'robert-p-jones', 'jemar-tisby', 'anthea-butler',
    'sarah-posner', 'katherine-stewart', 'blake-chastain', 'angela-denker',
    'sarah-mccammon', 'samuel-perry', 'beth-allison-barr', 'mike-cosper',
    'preet-bharara', 'akhil-reed-amar', 'imani-barbarin', 'matthew-cortland',
    'andrew-pulrang', 'christian-bryant', 'joe-polito', 'sean-hammond',
    'garth-greenwell', 'robinson-meyer', 'russ-roberts', 'skanda-amarnath',
    'andrew-leach', 'britt-wray', 'kingsmill-bond', 'leah-stokes', 'todd-moss',
    'betsy-ladyzhets', 'caroline-criado-perez', 'celine-gounder', 'ed-yong',
    'laurie-garrett', 'dean-baker', 'john-russell', 'sarah-jaffe', 'teddy-ostrow',
    'addison-del-mastro', 'samuel-sinyangwe', 'meghan-mangrum', 'audrey-watters',
    'van-jackson', 'jack-murphy', 'dmitri-alperovitch', 'jordi-amaral',
    'julia-angwin', 'jessica-huseman', 'lee-drutman', 'elisabeth-bik',
    'derek-lowe', 'yawu-miller', 'nick-valencia', 'francesca-donner',
    'jonathan-rabb', 'packy-mccormick', 'trung-phan', 'dave-amos',
    'reece-martin', 'oh-the-urbanity', 'andrew-sage', 'alexander-avila',
    'attorney-ryan', 'blair-imani', 'gabriel-sanchez', 'lauren-green',
    'estee', 'anya', 'kate-wagner', 'dan-carlin', 'ken-layne', 'anthony-davis',
    'katie-halper', 'michael-hobbes', 'aubrey-gordon', 'sarah-marshall',
    'travis-view', 'jake-rockatansky', 'nathan-robinson', 'sam-seder',
    'glenn-kirschner', 'peter-zeihan', 'devory-darkins', 'farron-cousins',
    'jesse-dollemore', 'roland-s-martin', 'yuri-fernandes', 'miguel-lago',
    'gustavo-faleiros', 'lynn-ngugi', 'kiki-mordi', 'ruona-meyer',
    'jane-friedman', 'marcus-cleaver', 'gary-stager', 'steven-greenhouse',
    'ethan-clark', 'kate-schneider', 'brittney-mcnamara', 'jacob-carter',
    'michael-shellenberger', 'rachel-gilmore', 'vir-sanghvi', 'phillip-lewis',
    'zac-bowling', 'richard-heydarian', 'keren-landman', 'fraser-jones',
    'tod-maffin', 'chase-cain', 'rashmee-roshan-lall', 'jack-werner',
    'evan-lovett', 'jason-mundok', 'liz-neeley', 'sean-naylor',
    'stephanie-williams', 'ted-gioia', 'geoff-livingston', 'joe-flood',
    'mark-alan-andre', 'paul-thacker', 'phil-martin', 'valerie-plesch',
    'sharon-yang', 'cesar-madison-tapia', 'april', 'david-horton', 'lanna',
    'rachel-chefilicios', 'samara-singer', 'tim-ebner', 'felipe-cardenas',
    'rachel-dimsumgirl', 'kevin', 'ap', 'recel', 'nicole', 'jessica-nguyen',
    'lisa-morris', 'anna-tran', 'tara', 'cassandra-stone',
}


def make_slug(name):
    s = name.lower().strip()
    s = re.sub(r'[^a-z0-9\s-]', '', s)
    s = re.sub(r'\s+', '-', s)
    s = re.sub(r'-+', '-', s)
    return s.strip('-')


def has_bsky_slot(row):
    for name_slot, _ in PLATFORM_SLOTS:
        if row.get(name_slot) == 'Social - BlueSky':
            return True
    return False


# ── Load master CSV ────────────────────────────────────────────────────────────
print('Loading master CSV…')
master_by_name = {}   # lowercased name → row
master_by_slug = {}   # slug → row
with open(MASTER_CSV, encoding='utf-8-sig') as f:
    for row in csv.DictReader(f):
        key = row['Creator Name'].lower().strip()
        master_by_name[key] = row
        if row.get('slug'):
            master_by_slug[row['slug']] = row
print(f'  {len(master_by_name)} master creators loaded')


# ── Task 1: Build bluesky-creators.json ───────────────────────────────────────
print('\nTask 1 — Building bluesky-creators.json…')

with open(HANDLES_TSV, encoding='utf-8-sig') as f:
    tsv_rows = list(csv.DictReader(f, delimiter='\t'))

total_yes = sum(1 for r in tsv_rows if r['confirmed'] == 'YES')
print(f'  Total rows in TSV: {len(tsv_rows)}')
print(f'  YES rows: {total_yes}')

skip_likely = skip_empty = skip_invalid = skip_dupe = 0
matched = unmatched = 0
seen_handles = {}
out = []

for row in tsv_rows:
    if row['confirmed'] != 'YES':
        skip_likely += 1
        continue

    handle = (row['bsky_handle'] or '').strip()
    if not handle:
        skip_empty += 1
        continue
    if 'handle.invalid' in handle:
        print(f'  SKIP invalid: {row["atlas_name"]}')
        skip_invalid += 1
        continue

    handle_lc = handle.lower()
    if handle_lc in seen_handles:
        print(f'  SKIP dupe @{handle}: {row["atlas_name"]} (already used by {seen_handles[handle_lc]})')
        skip_dupe += 1
        continue
    seen_handles[handle_lc] = row['atlas_name']

    name = row['atlas_name'].strip()
    name_key = name.lower()
    master = master_by_name.get(name_key)

    if master:
        matched += 1
        slug = master.get('slug') or make_slug(name)
        entry = {
            'name':             master['Creator Name'].strip(),
            'slug':             slug,
            'channel':          master.get('Creator Channel', '').strip(),
            'primary_url':      master.get('Link Primary', '').strip(),
            'platform_primary': master.get('Platform Primary', '').strip(),
            'bsky_handle':      handle,
            'bsky_url':         f'{BSKY_PREFIX}{handle}',
            'bsky_followers':   int(row['bsky_followers'] or 0),
            'topic':            master.get('Topic/Category', '').strip(),
            'geography':        master.get('Geography', '').strip(),
            'geo_region':       master.get('Geo Region', '').strip(),
            'geo_state':        master.get('Geo State', '').strip(),
            'geo_city':         master.get('Geo City', '').strip(),
            'groups':           master.get('Groups', '').strip(),
            'confirmed':        'YES',
            'in_master':        True,
            'new_bsky_addition': slug in NEW_BSKY_SLUGS,
        }
    else:
        unmatched += 1
        slug = make_slug(name)
        entry = {
            'name':             name,
            'slug':             slug,
            'channel':          row.get('atlas_channel', '').strip(),
            'primary_url':      row.get('atlas_link', '').strip(),
            'platform_primary': row.get('atlas_platform', '').strip(),
            'bsky_handle':      handle,
            'bsky_url':         f'{BSKY_PREFIX}{handle}',
            'bsky_followers':   int(row['bsky_followers'] or 0),
            'topic':            '',
            'geography':        '',
            'geo_region':       '',
            'geo_state':        '',
            'geo_city':         '',
            'groups':           '',
            'confirmed':        'YES',
            'in_master':        False,
            'new_bsky_addition': slug in NEW_BSKY_SLUGS,
        }

    out.append(entry)

with open(OUT_JSON, 'w', encoding='utf-8') as f:
    json.dump(out, f, indent=2, ensure_ascii=False)

print(f'\n  Summary:')
print(f'    YES in TSV:       {total_yes}')
print(f'    Skipped LIKELY:   {skip_likely}')
print(f'    Skipped empty:    {skip_empty}')
print(f'    Skipped invalid:  {skip_invalid}')
print(f'    Skipped dupe:     {skip_dupe}')
print(f'    Matched to master:{matched}')
print(f'    Unmatched:        {unmatched}')
print(f'    Written:          {len(out)}')
print(f'    new_bsky_addition:{sum(1 for c in out if c["new_bsky_addition"])}')
print(f'  → {OUT_JSON}')


# ── Task 3: Ryan Handoff — existing master creators needing Bluesky slot ──────
print('\nTask 3 — ryan_handoff_bsky_enrichment_june18.csv…')

# Build set of YES handles indexed by lowercased name
yes_by_name = {}
for row in tsv_rows:
    if row['confirmed'] == 'YES':
        handle = (row['bsky_handle'] or '').strip()
        if handle and 'handle.invalid' not in handle:
            yes_by_name[row['atlas_name'].lower().strip()] = row

enrich_rows = []
for name_key, tsv_row in sorted(yes_by_name.items(), key=lambda x: x[0]):
    master = master_by_name.get(name_key)
    if not master:
        continue  # not in master — goes to Task 4
    if has_bsky_slot(master):
        continue  # already has a Bluesky platform slot

    handle = tsv_row['bsky_handle'].strip()
    enrich_rows.append({
        'Creator Name':          master['Creator Name'],
        'slug':                  master.get('slug', ''),
        'Current Platform Primary': master.get('Platform Primary', ''),
        'bsky_handle':           handle,
        'bsky_url':              f'{BSKY_PREFIX}{handle}',
        'confirmed':             'YES',
        'notes':                 tsv_row.get('notes', ''),
    })

with open(OUT_ENRICH_CSV, 'w', newline='', encoding='utf-8') as f:
    fieldnames = ['Creator Name', 'slug', 'Current Platform Primary', 'bsky_handle', 'bsky_url', 'confirmed', 'notes']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(enrich_rows)

print(f'  {len(enrich_rows)} creators need Bluesky platform entry added')
print(f'  → {OUT_ENRICH_CSV}')


# ── Task 4: Ryan Handoff — net-new spidering candidates ───────────────────────
print('\nTask 4 — ryan_handoff_new_candidates_june18.csv…')

with open(VERIFIED_TSV, encoding='utf-8-sig') as f:
    verified = list(csv.DictReader(f, delimiter='\t'))
with open(S9_TSV, encoding='utf-8-sig') as f:
    s9 = list(csv.DictReader(f, delimiter='\t'))

# Combine, dedup on bsky_handle
combined = {}
for row in verified:
    h = (row.get('bsky_handle') or '').strip().lower()
    if h:
        combined[h] = {**row, 'trustfnd_eligible': '', 'confirmed_eligible': 'YES'}
for row in s9:
    h = (row.get('bsky_handle') or '').strip().lower()
    if h:
        entry = combined.get(h, {})
        entry.update({**row, 'confirmed_eligible': 'YES'})
        combined[h] = entry

cand_rows = []
for h, row in combined.items():
    name_key = (row.get('name') or '').lower().strip()
    if name_key in master_by_name:
        continue  # already in master

    cand_rows.append({
        'name':               row.get('name', '').strip(),
        'bsky_handle':        row.get('bsky_handle', '').strip(),
        'bsky_followers':     int(row.get('bsky_followers') or 0),
        'primary_platform':   row.get('primary_platform', '').strip(),
        'primary_url':        row.get('primary_url', '').strip(),
        'beat':               row.get('beat', '').strip(),
        'geography':          row.get('geography', '').strip(),
        'confirmed_eligible': 'YES',
        'trustfnd_eligible':  row.get('trustfnd_eligible', '').strip(),
        'notes':              row.get('notes', '').strip(),
    })

cand_rows.sort(key=lambda r: -(r['bsky_followers']))

with open(OUT_CANDS_CSV, 'w', newline='', encoding='utf-8') as f:
    fieldnames = ['name', 'bsky_handle', 'bsky_followers', 'primary_platform', 'primary_url',
                  'beat', 'geography', 'confirmed_eligible', 'trustfnd_eligible', 'notes']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(cand_rows)

print(f'  {len(cand_rows)} net-new candidates (not in master):')
for r in cand_rows:
    print(f'    {r["name"]} (@{r["bsky_handle"]}, {r["bsky_followers"]:,} followers)')
print(f'  → {OUT_CANDS_CSV}')
