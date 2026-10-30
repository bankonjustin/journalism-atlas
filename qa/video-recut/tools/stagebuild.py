import re, json, pathlib
def build_stage(index_html, out_dir, tl, names, W=1080, H=1080, rest=None):
    s = pathlib.Path(index_html).read_text()
    nn = re.search(r"const NN = \(\(\) => \{.*?\n\}\)\(\);", s, re.S).group(0)
    data = re.search(r'<script type="application/json" id="nn-data">(.*?)</script>', s, re.S).group(1)
    js = (pathlib.Path(__file__).parent / 'stage_tpl.js').read_text()
    html = ('<!doctype html><meta charset="utf-8"><body style="margin:0;background:#000"><canvas id="st" width="' + str(2*W) + '" height="' + str(2*H) + '"></canvas><canvas id="out" width="' + str(W) + '" height="' + str(H) + '"></canvas>'
           '<script id="nn-data" type="application/json">' + data + '</script><script>window.NN_FAM="Arial,Helvetica,sans-serif";window.W=' + str(W) + ';window.H=' + str(H) + ';window.REST=' + json.dumps(rest or {'cx':540,'cy':691,'R':311}) + ';window.TL=' + json.dumps(tl) + ';window.NAMES=' + json.dumps(names) + ';\n' + nn + '\n</script><script>' + js + '</script>')
    p = pathlib.Path(out_dir) / 'stage.html'; p.write_text(html); return p
