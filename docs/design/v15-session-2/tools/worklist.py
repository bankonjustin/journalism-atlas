import sys,os,json,collections
sys.path.insert(0,'.')
from s1shot import *; from pages40 import PUB
JS=r"""
() => {
 const parse=c=>{const m=c&&c.match(/rgba?\(([\d.]+),\s*([\d.]+),\s*([\d.]+)(?:,\s*([\d.]+))?/);return m?[+m[1],+m[2],+m[3],m[4]===undefined?1:+m[4]]:null};
 const lum=([r,g,b])=>{const f=c=>{c/=255;return c<=0.03928?c/12.92:Math.pow((c+0.055)/1.055,2.4)};return .2126*f(r)+.7152*f(g)+.0722*f(b)};
 const surface=el=>{let e=el;while(e&&e.nodeType===1){const bg=parse(getComputedStyle(e).backgroundColor);if(bg&&bg[3]>0.5)return lum(bg)<0.2?'dark':'light';e=e.parentElement;}return 'light';};
 const sig=el=>{let s=el.tagName.toLowerCase();if(el.classList.length)s+='.'+[...el.classList].slice(0,3).join('.');return s};
 const out=[];
 const cand=document.querySelectorAll('button,input[type=submit],input[type=button],[role=button],[role=tab],a');
 for(const el of cand){
   const cs=getComputedStyle(el); if(cs.display==='none'||cs.visibility==='hidden')continue;
   const r=el.getBoundingClientRect(); if(r.width<8||r.height<8)continue;
   const cls=typeof el.className==='string'?el.className:'';
   const txt=(el.innerText||el.value||'').trim().replace(/\s+/g,' ');
   const arrow=/(→|›|»)\s*$/.test(txt);
   const bg=parse(cs.backgroundColor); const hasBg=bg&&bg[3]>0.1; const bw=parseFloat(cs.borderTopWidth)||0; const bordered=bw>0&&cs.borderTopStyle!=='none';
   const btnish=/btn|button|cta|chip|pill|tab|toggle|filter|sort|submit|view|seg|layer|recency/i.test(cls)||el.tagName==='BUTTON'||el.getAttribute('role')==='button'||el.getAttribute('role')==='tab'||el.tagName==='INPUT';
   const isLink=el.tagName==='A';
   if(isLink && !btnish && !arrow && !(hasBg&&r.height>=28)) { 
      // plain link: classify as nav/body later
      const inNav=!!el.closest('nav,header,.top-nav,footer,.site-footer');
      out.push({k:'link',sig:sig(el),txt:txt.slice(0,50),inNav:inNav,inFooter:!!el.closest('footer,.site-footer'),inP:!!el.closest('p,li,.prose,article,blockquote'),surface:surface(el),color:cs.color,ul:cs.textDecorationLine,ff:cs.fontFamily.slice(0,18),fs:cs.fontSize,fw:cs.fontWeight,tt:cs.textTransform,href:(el.getAttribute('href')||'').slice(0,50)});
      continue;
   }
   const sibs=el.parentElement?[...el.parentElement.children].filter(c=>c.tagName===el.tagName&&c.className===el.className).length:1;
   out.push({k:arrow&&!btnish?'arrowlink':'button',sig:sig(el),txt:txt.slice(0,50),tag:el.tagName.toLowerCase(),surface:surface(el),bg:cs.backgroundColor,color:cs.color,bc:cs.borderTopColor,bw:bw,radius:cs.borderTopLeftRadius,ff:cs.fontFamily.slice(0,18),fs:cs.fontSize,fw:cs.fontWeight,tt:cs.textTransform,h:Math.round(r.height),w:Math.round(r.width),sibs:sibs,
     sel:{cls:/(^|[-_\s])(active|selected|current|is-active|on)(\s|$|[-_])/.test(cls),ariaSel:el.getAttribute('aria-selected'),ariaPressed:el.getAttribute('aria-pressed'),ariaCur:el.getAttribute('aria-current'),role:el.getAttribute('role')},
     inNav:!!el.closest('nav,header,.top-nav'),inFooter:!!el.closest('footer,.site-footer'),disabled:el.disabled||el.getAttribute('aria-disabled')==='true',parent:(el.parentElement?sig(el.parentElement):'')});
 }
 return out;
}"""
def run(port=8951):
    serve(port); res=[]
    with sync_playwright() as p:
        b=p.chromium.launch(); ctx=b.new_context(viewport={'width':1440,'height':900})
        for n,u,f in PUB:
            pg=ctx.new_page()
            try:
                pg.goto('http://127.0.0.1:%d%s'%(port,u),wait_until='load',timeout=30000)
                try: pg.wait_for_load_state('networkidle',timeout=6000)
                except Exception: pass
                pg.wait_for_timeout(1200)
                h=pg.evaluate('document.documentElement.scrollHeight')
                for y in range(0,min(h,25000),900): pg.evaluate('window.scrollTo(0,%d)'%y); pg.wait_for_timeout(100)
                pg.evaluate('window.scrollTo(0,0)')
                for r in pg.evaluate(JS): r['file']=f; res.append(r)
            except Exception as e: res.append({'file':f,'error':str(e)[:100]})
            pg.close()
        b.close()
    return res
if __name__=='__main__':
    res=run(); json.dump(res,open('worklist.json','w')); print(len(res))
