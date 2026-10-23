import sys,os,json; sys.path.insert(0,'.')
from s1shot import *
OUT=REPO+'/docs/design/v15-session-2/screenshots/c2'; os.makedirs(OUT,exist_ok=True)
PAGES=[('index','/'),('pulse','/pulse'),('research','/research'),('partners__ahp','/partners/ahp')]
JS="""()=>{const e=document.activeElement; if(!e||e===document.body) return null;
 const parse=c=>{const m=c.match(/rgba?\\(([\\d.]+),\\s*([\\d.]+),\\s*([\\d.]+)(?:,\\s*([\\d.]+))?/);return m?[+m[1],+m[2],+m[3],m[4]===undefined?1:+m[4]]:null};
 const lum=([r,g,b])=>{const f=c=>{c/=255;return c<=0.03928?c/12.92:Math.pow((c+0.055)/1.055,2.4)};return .2126*f(r)+.7152*f(g)+.0722*f(b)};
 let x=e.parentElement||e,dark=false;while(x&&x.nodeType===1){const bg=parse(getComputedStyle(x).backgroundColor);if(bg&&bg[3]>0.5){dark=lum(bg)<0.2;break}x=x.parentElement}
 const cs=getComputedStyle(e);const r=e.getBoundingClientRect();
 return {tag:e.tagName.toLowerCase(),cls:(typeof e.className==='string'?e.className:'').slice(0,40),txt:(e.innerText||e.value||e.getAttribute('aria-label')||'').trim().slice(0,24),ow:cs.outlineWidth,os:cs.outlineStyle,oc:cs.outlineColor,oo:cs.outlineOffset,dark:dark,hdr:!!e.closest('.top-nav,.mobile-menu'),y:Math.round(r.top+scrollY),vis:r.width>0&&r.height>0}}"""
serve(9001); summary={}
with sync_playwright() as p:
    b=p.chromium.launch()
    for name,url in PAGES:
        pg=b.new_page(viewport={'width':1440,'height':900}); pg.goto('http://127.0.0.1:9001'+url,wait_until='load'); pg.wait_for_timeout(2500)
        rows=[]; shots=set()
        for i in range(90):
            pg.keyboard.press('Tab'); pg.wait_for_timeout(40)
            r=pg.evaluate(JS)
            if not r or not r['vis']: continue
            rows.append(r)
            key=('hdr' if r['hdr'] else ('dark' if r['dark'] else 'light'))
            if key not in shots and len(shots)<3:
                shots.add(key); pg.screenshot(path='%s/%s-focus-%s.png'%(OUT,name,key))
        olive='rgb(93, 116, 0)'; lime='rgb(151, 214, 0)'
        bad=[r for r in rows if not (r['os']=='solid' and r['ow']=='2px' and r['oc']==(lime if r['dark'] else olive))]
        summary[name]=dict(focused=len(rows),dark=sum(r['dark'] for r in rows),light=sum(not r['dark'] for r in rows),bad=[(r['tag'],r['cls'],r['txt'],r['ow'],r['os'],r['oc'],'dark' if r['dark'] else 'light') for r in bad][:12],nbad=len(bad),shots=sorted(shots))
        pg.close()
    b.close()
for k,v in summary.items(): print(k,{a:b for a,b in v.items() if a!='bad'}); [print('    BAD',x) for x in v['bad']]
json.dump(summary,open('focus_c2.json','w'),indent=1)
