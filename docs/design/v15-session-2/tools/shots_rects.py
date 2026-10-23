import sys,os,json; sys.path.insert(0,'.')
from s1shot import *; from pages40 import PUB
tag=sys.argv[1]; widths=[int(x) for x in sys.argv[2].split(',')]; only=sys.argv[3].split(',') if len(sys.argv)>3 and sys.argv[3]!='all' else None; port=int(sys.argv[4]) if len(sys.argv)>4 else 9051
sel=sys.argv[5] if len(sys.argv)>5 else '.btn,.nav-search-btn'
OUT=REPO+'/docs/design/v15-session-2/screenshots/'+tag; os.makedirs(OUT,exist_ok=True)
serve(port); rects={}
with sync_playwright() as p:
    b=p.chromium.launch()
    for w in widths:
        ctx=b.new_context(viewport={'width':w,'height':900 if w>600 else 844})
        for n,u,f in PUB:
            if only and n not in only: continue
            pg=ctx.new_page()
            try:
                try: pg.goto('http://127.0.0.1:%d%s'%(port,u),wait_until='load',timeout=30000)
                except Exception: pg.goto('http://127.0.0.1:%d%s'%(port,u),wait_until='domcontentloaded',timeout=30000)
                try: pg.wait_for_load_state('networkidle',timeout=8000)
                except Exception: pass
                pg.wait_for_timeout(1500)
                rects['%s-%d'%(n,w)]=pg.evaluate("""(sel)=>[...document.querySelectorAll(sel)].map(e=>{const r=e.getBoundingClientRect();return [Math.round(r.left+scrollX),Math.round(r.top+scrollY),Math.round(r.width),Math.round(r.height)]}).filter(r=>r[2]>0&&r[3]>0)""",sel)
                pg.screenshot(path='%s/%s-%d.png'%(OUT,n,w),full_page=True)
            except Exception as e: print('ERR',n,w,str(e)[:60])
            pg.close()
        ctx.close()
    b.close()
json.dump(rects,open(OUT+'/rects.json','w'))
print('done',len(rects))
