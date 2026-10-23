import sys,os,json; sys.path.insert(0,'.')
from slices import mk
from playwright.sync_api import sync_playwright
from pages40 import PUB
FIND=r"""()=>{const all=[...document.querySelectorAll('body *')];const seen=new Set();const out=[];
 for(const e of document.querySelectorAll('.btn--secondary')){const p=e.parentElement;if(!p||seen.has(p))continue;const kids=[...p.children].filter(c=>c.classList.contains('btn--secondary'));if(kids.length<3)continue;seen.add(p);
  out.push({idx:all.indexOf(p),sig:p.tagName.toLowerCase()+(p.id?'#'+p.id:'')+(p.className&&typeof p.className==='string'?'.'+p.className.split(' ')[0]:''),n:kids.length})}return out}"""
ROWS=r"""(idxs)=>{const all=[...document.querySelectorAll('body *')];return idxs.map(i=>{const p=all[i];if(!p)return null;const tops=new Set([...p.children].filter(c=>c.getBoundingClientRect().height>0).map(c=>Math.round(c.getBoundingClientRect().top+scrollY)));return tops.size})}"""
def run(old,new,width=390,only=None):
    mk(old,9201); mk(new,9202); res=[]
    with sync_playwright() as p:
        b=p.chromium.launch()
        for n,u,f in PUB:
            if only and n not in only: continue
            pa=b.new_page(viewport={'width':width,'height':844}); pb=b.new_page(viewport={'width':width,'height':844})
            try:
                pb.goto('http://127.0.0.1:9202'+u,wait_until='domcontentloaded',timeout=30000); pb.wait_for_timeout(2500)
                groups=pb.evaluate(FIND)
                if not groups: pa.close(); pb.close(); continue
                pa.goto('http://127.0.0.1:9201'+u,wait_until='domcontentloaded',timeout=30000); pa.wait_for_timeout(2500)
                ia=[g['idx'] for g in groups]
                ra=pa.evaluate(ROWS,ia); rb=pb.evaluate(ROWS,ia)
                for g,x,y in zip(groups,ra,rb): res.append((f,g['sig'],g['n'],x,y))
            except Exception as e: res.append((f,'ERR',str(e)[:40]))
            pa.close(); pb.close()
        b.close()
    return res
if __name__=='__main__':
    old=sys.argv[1]; new=os.path.expanduser('~/Documents/GitHub/journalism-atlas')
    for r in run(old,new): print(r)
