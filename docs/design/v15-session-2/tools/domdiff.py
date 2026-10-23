import sys,os,json,collections; sys.path.insert(0,'.')
from slices import mk
from playwright.sync_api import sync_playwright
from pages40 import PUB
PROPS=['color','backgroundColor','borderTopColor','borderTopWidth','borderRightWidth','borderBottomWidth','borderLeftWidth','borderTopLeftRadius','fontFamily','fontSize','fontWeight','textTransform','letterSpacing','lineHeight','paddingTop','paddingRight','paddingBottom','paddingLeft','marginTop','marginBottom','marginLeft','marginRight','display','boxShadow','opacity','textDecorationLine','outlineStyle']
JS=r"""(props)=>{const out=[];const skip=new Set(['SCRIPT','STYLE','NOSCRIPT','LINK','META','HEAD','TITLE']);
 const mig=e=>e.closest('.btn,.nav-search-btn,.link-instruction,.link-body');
 let i=0;for(const e of document.body.querySelectorAll('*')){ if(skip.has(e.tagName))continue; const cs=getComputedStyle(e); const r=e.getBoundingClientRect();
  out.push({sig:e.tagName.toLowerCase()+(e.id?'#'+e.id:'')+(typeof e.className==='string'&&e.className?'.'+e.className.split(/\s+/).filter(c=>!/^(btn|btn--primary|btn--secondary|on-dark|link-instruction|link-body)$/.test(c)).slice(0,2).join('.'):''),
   m:!!mig(e), vis:r.width>0&&r.height>0, p:props.map(k=>cs[k]), h:Math.round(r.height), w:Math.round(r.width)})} return out}"""
def snap(pg,url,port):
    pg.goto('http://127.0.0.1:%d%s'%(port,url),wait_until='domcontentloaded',timeout=30000); pg.wait_for_timeout(2600)
    return pg.evaluate(JS,PROPS)
def main(oldroot,newroot,only=None,width=1440):
    mk(oldroot,9101); mk(newroot,9102); report={}
    with sync_playwright() as p:
        b=p.chromium.launch()
        for n,u,f in PUB:
            if only and n not in only: continue
            pa=b.new_page(viewport={'width':width,'height':900}); pb=b.new_page(viewport={'width':width,'height':900})
            try:
                A=snap(pa,u,9101); B=snap(pb,u,9102)
            except Exception as e: report[f]={'err':str(e)[:60]}; pa.close(); pb.close(); continue
            pa.close(); pb.close()
            if len(A)!=len(B): report[f]={'domlen':(len(A),len(B))}; continue
            diffs=[]; sizes=[]
            for x,y in zip(A,B):
                if x['sig']!=y['sig'] or y['m']: continue
                dp=[PROPS[k] for k in range(len(PROPS)) if x['p'][k]!=y['p'][k]]
                if dp: diffs.append((y['sig'],dp[:4]))
            report[f]={'n':len(A),'styled_diffs':diffs[:15],'ndiff':len(diffs)}
        b.close()
    return report
if __name__=='__main__':
    old=sys.argv[1]; new=os.path.expanduser('~/Documents/GitHub/journalism-atlas'); only=sys.argv[2].split(',') if len(sys.argv)>2 and sys.argv[2]!='all' else None
    rep=main(old,new,only)
    json.dump(rep,open('domdiff.json','w'),indent=1)
    for f,r in rep.items():
        if r.get('ndiff') or 'err' in r or 'domlen' in r: print(f,r)
    print('pages:',len(rep),'with style diffs outside migrated components:',sum(1 for r in rep.values() if r.get('ndiff')))
