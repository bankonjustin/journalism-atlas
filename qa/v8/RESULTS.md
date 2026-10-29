# v8 QA results

- PASS **screenshots: landing, embed, 4 explorer tabs at 1440, 390; 4 tabs in a 760 iframe**
- PASS **no page errors or console errors**
- PASS **headline-only read written** (qa/v8/HEADLINES.md)
- PASS **framing: explorer renders in an iframe from journalismatlas.com** ({'Content-Security-Policy': "frame-ancestors 'self' https://asu.edu https://*.asu.edu https://journalismatlas.com"})
- PASS **framing: another origin (example.com) is refused** (console refused=True)
- PASS **framing: an asu.edu page can frame it**
- PASS **copy.md round trip: one string changed, rebuilt, appears on landing and explorer**
- PASS **round trip: reverted and rebuilds clean**
- PASS **break test: missing string id fails with a readable message** (nn/build.py FAILED:   copy.md is missing 1 string id: in_short.see_chart   Add a line "## in_short.see_chart" and the text under it.)
- PASS **break test: unknown token fails with a readable message** (nn/build.py FAILED:   copy.md line 84, "chapter1.sentence": unknown token {top_holdd}. Known tokens are listed in nn/README.md.)
- PASS **break test: editing a locked paper string fails**
- PASS **hand-typed number warns but builds** (warning: copy.md line 93, "chapter1.stat": a number is typed by hand. Use a token so it follows the data.)
- PASS **copy.md restored unchanged**
- PASS **redirects: both old explorer paths 301 to /nodes-and-networks/explorer/ (no query in target, so Cloudflare keeps the visitor query)** (6 rules)
- PASS **redirects: no old explorer file is left in dist for a redirect to compete with**
- PASS **no public string contains placeholder, TBD, [ or ]**
- PASS **video: both encodes under 25 MB** (nodes-networks-16x9.mp4 13.9 MB, nodes-networks-9x16.mp4 12.0 MB)
- PASS **video: both encodes open and report length and size** (duration 52.00s 1920 x 1080 / duration 52.00s 1080 x 1920)
