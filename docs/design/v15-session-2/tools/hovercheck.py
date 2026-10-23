import sys,json; sys.path.insert(0,'.')
from s1shot import *; from pages40 import PUB
JS=r"""()=>{
 const parse=c=>{const m=c&&c.match(/rgba?\(([\d.]+),\s*([\d.]+),\s*([\d.]+)(?:,\s*([\d.]+))?/);return m?[+m[1],+m[2],+m[3],m[4]===undefined?1:+m[4]]:null};
 const lum=([r,g,b])=>{const f=c=>{c/=255;return c<=0.03928?c/12.92:Math.pow((c+0.055)/1.055,2.4)};return .2126*f(r)+.7152*f(g)+.0722*f(b)};
 const surf=el=>{let e=el;while(e&&e.nodeType===1){const bg=parse(getComputedStyle(e).backgroundColor);if(bg&&bg[3]>0.5)return lum(bg)<0.2?'dark':'light';e=e.parentElement}return 'light'};
 const out=[]; const names=['--color-hover','--header-fg-hover','--color-accent-dark-hover'];
 const walk=(rules,sheet)=>{for(const r of rules){ if(r.cssRules&&!r.selectorText){walk(r.cssRules,sheet);continue} if(!r.style||!r.selectorText)continue;
   for(let i=0;i<r.style.length;i++){const p=r.style[i],v=r.style.getPropertyValue(p); if(names.some(n=>v.includes('var('+n))){ 
     if(!/:hover|:active/.test(r.selectorText))continue;
     let sel=r.selectorText.replace(/:hover|:active/g,'').replace(/:focus-visible/g,''); let els=[]; try{els=[...document.querySelectorAll(sel)]}catch(e){}
     if(!els.length){out.push({sel:r.selectorText,prop:p,n:0});continue}
     const surfs=[...new Set(els.map(surf))];
     out.push({sel:r.selectorText.slice(0,70),prop:p,n:els.length,surf:surfs.join('/')});
   }}}};
 for(const s of document.styleSheets){let rules;try{rules=s.cssRules}catch(e){continue} walk(rules,s)}
 return out}"""
serve(9021); res=[]
with sync_playwright() as p:
    b=p.chromium.launch()
    for n,u,f in PUB:
        pg=b.new_page(viewport={'width':1440,'height':900})
        try:
            pg.goto('http://127.0.0.1:9021'+u,wait_until='domcontentloaded',timeout=30000); pg.wait_for_timeout(2500)
            for r in pg.evaluate(JS): r['file']=f; res.append(r)
        except Exception as e: res.append({'file':f,'err':str(e)[:60]})
        pg.close()
    b.close()
fills=('background','background-color')
nonfill=[r for r in res if 'prop' in r and r['prop'] not in fills]
print('hover rules using --color-hover & co:',len([r for r in res if 'prop' in r]),'; non-fill:',len(nonfill))
for r in nonfill: print('  NONFILL',r)
unmatched=[r for r in res if r.get('n')==0]
print('rules matching no element on their page (JS-built or other state):',len(unmatched)); 
json.dump(res,open('hovercheck.json','w'))
