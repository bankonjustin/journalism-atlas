import sys,json; sys.path.insert(0,'.')
from s1shot import *; from pages40 import PUB
JS=r"""()=>{
 const parse=c=>{const m=c&&c.match(/rgba?\(([\d.]+),\s*([\d.]+),\s*([\d.]+)(?:,\s*([\d.]+))?/);return m?[+m[1],+m[2],+m[3],m[4]===undefined?1:+m[4]]:null};
 const lum=([r,g,b])=>{const f=c=>{c/=255;return c<=0.03928?c/12.92:Math.pow((c+0.055)/1.055,2.4)};return .2126*f(r)+.7152*f(g)+.0722*f(b)};
 const out=[]; const vw=innerWidth;
 for(const el of document.querySelectorAll('body, body *')){
   const cs=getComputedStyle(el); const bg=parse(cs.backgroundColor); if(!bg||bg[3]<0.9||lum(bg)>0.12)continue;
   const r=el.getBoundingClientRect(); if(r.width<vw*0.5||r.height<60)continue;
   // skip if parent is also dark+opaque (outermost dark container only)
   const p=el.parentElement; if(p&&p!==document.documentElement){const pb=parse(getComputedStyle(p).backgroundColor); if(pb&&pb[3]>=0.9&&lum(pb)<=0.12&&el.tagName!=='BODY')continue;}
   out.push({tag:el.tagName.toLowerCase(),id:el.id,cls:typeof el.className==='string'?el.className:'',w:Math.round(r.width),h:Math.round(r.height),btns:el.querySelectorAll('button,a.btn,[class*=btn],[class*=cta],a').length});
 } return out}"""
serve(8991); res={}
with sync_playwright() as p:
    b=p.chromium.launch()
    for n,u,f in PUB:
        pg=b.new_page(viewport={'width':1440,'height':900})
        try:
            pg.goto('http://127.0.0.1:8991'+u,wait_until='domcontentloaded',timeout=30000); pg.wait_for_timeout(2500)
            res[f]=pg.evaluate(JS)
        except Exception as e: res[f]=[{'err':str(e)[:60]}]
        pg.close()
    b.close()
json.dump(res,open('darksec.json','w'),indent=1)
for f,v in res.items():
    print(f, [(x.get('tag'),(x.get('cls') or '')[:40],x.get('id'),x.get('h')) for x in v][:8])
