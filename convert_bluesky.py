"""
convert_bluesky.py — Build assets/data/bluesky-creators.json from creators-master.csv.
Includes only creators with Social - BlueSky in any platform slot.
"""

import csv
import json
import os
import re

REPO_ROOT  = os.path.dirname(os.path.abspath(__file__))
MASTER_CSV = os.path.join(REPO_ROOT, 'assets', 'data', 'creators-master.csv')
OUT_JSON   = os.path.join(REPO_ROOT, 'assets', 'data', 'bluesky-creators.json')

BSKY_PREFIX = 'https://bsky.app/profile/'

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

PLATFORM_SLOTS = [
    ('Platform Primary',  'Link Primary'),
    ('Platform 2 Name',   'Platform 2 Link'),
    ('Platform 3 Name',   'Platform 3 Link'),
    ('Platform 4 Name',   'Platform 4 Link'),
]


def extract_handle(url):
    if not url:
        return ''
    url = url.strip()
    if not url.startswith(BSKY_PREFIX):
        return ''
    handle = url[len(BSKY_PREFIX):].rstrip('/')
    return handle


def main():
    skipped_empty   = 0
    skipped_invalid = 0
    skipped_dup     = 0
    processed       = 0

    seen_handles = {}  # handle -> first slug seen
    out = []

    with open(MASTER_CSV, encoding='utf-8-sig') as f:
        for row in csv.DictReader(f):
            bsky_url = ''
            for name_slot, link_slot in PLATFORM_SLOTS:
                if row.get(name_slot) == 'Social - BlueSky':
                    bsky_url = row.get(link_slot, '').strip()
                    break
            else:
                continue  # no Bluesky slot found

            processed += 1
            slug = row.get('slug', '').strip()
            handle = extract_handle(bsky_url)

            if not handle:
                print(f'  SKIP empty handle: {row["Creator Name"]} ({bsky_url!r})')
                skipped_empty += 1
                continue

            if 'handle.invalid' in handle:
                print(f'  SKIP handle.invalid: {row["Creator Name"]}')
                skipped_invalid += 1
                continue

            if handle in seen_handles:
                print(f'  SKIP duplicate handle @{handle}: {row["Creator Name"]} (slug={slug}) — already used by {seen_handles[handle]}')
                skipped_dup += 1
                continue

            seen_handles[handle] = slug

            extra_platforms = []
            for slot_name, slot_link in [('Platform 2 Name', 'Platform 2 Link'),
                                          ('Platform 3 Name', 'Platform 3 Link'),
                                          ('Platform 4 Name', 'Platform 4 Link')]:
                name_val = row.get(slot_name, '').strip()
                link_val = row.get(slot_link, '').strip()
                if name_val and name_val != 'Social - BlueSky':
                    extra_platforms.append({'name': name_val, 'url': link_val})

            out.append({
                'name':              row.get('Creator Name', '').strip(),
                'slug':              slug,
                'channel':           row.get('Creator Channel', '').strip(),
                'primary_url':       row.get('Link Primary', '').strip(),
                'platform_primary':  row.get('Platform Primary', '').strip(),
                'platforms':         extra_platforms,
                'bsky_handle':       handle,
                'bsky_url':          f'{BSKY_PREFIX}{handle}',
                'bsky_followers':    0,
                'topic':             row.get('Topic/Category', '').strip(),
                'geography':         row.get('Geography', '').strip(),
                'geo_region':        row.get('Geo Region', '').strip(),
                'geo_state':         row.get('Geo State', '').strip(),
                'geo_city':          row.get('Geo City', '').strip(),
                'groups':            row.get('Groups', '').strip(),
                'new_bsky_addition': slug in NEW_BSKY_SLUGS,
            })

    with open(OUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2, ensure_ascii=False)

    total_written = len(out)
    total_skipped = skipped_empty + skipped_invalid + skipped_dup
    print(f'\n--- Summary ---')
    print(f'  Rows with Social - BlueSky: {processed}')
    print(f'  Skipped — empty/non-bsky URL: {skipped_empty}')
    print(f'  Skipped — handle.invalid: {skipped_invalid}')
    print(f'  Skipped — duplicate handle: {skipped_dup}')
    print(f'  Written to JSON: {total_written}')
    print(f'  new_bsky_addition=true: {sum(1 for c in out if c["new_bsky_addition"])}')
    print(f'  Output: {OUT_JSON}')


if __name__ == '__main__':
    main()
