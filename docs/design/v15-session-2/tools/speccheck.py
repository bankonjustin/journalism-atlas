import sys,json; sys.path.insert(0,'.')
from s1shot import *; from pages40 import PUB
"""For every .btn--primary / .btn--secondary on every public page: rest computed colours vs v15 spec (light/dark), min height, font; then hover the first of each distinct signature."""
RGB={'acid':'rgb(206, 255, 0)','s6':'rgb(48, 48, 48)','s5':'rgb(94, 94, 94)','s4':'rgb(144, 144, 144)','white':'rgb(255, 255, 255)','black':'rgb(0, 0, 0)'}
JS=r"""(sel)=>{
 const parse=c=>{const m=c&&c.match(/rgba?\(([\d.]+),\s*([\d.]+),\s*([\d.]+)(?:,\s*([\d.]+))?/);return m?[+m[1],+m[2],+m[3],m[4]===undefined?1:+m[4]]:null};
 const lum=([r,g,b])=>{const f=c=>{c/=255;return c<=0.03928?c/12.92:Math.pow((c+0.055)/1.055,2.4)};return .2126*f(r)+.7152*f(g)+.0722*f(b)};
 const surf=el=>{let e=el.parentElement;while(e&&e.nodeType===1){const bg=parse(getComputedStyle(e).backgroundColor);if(bg&&bg[3]>0.5)return lum(bg)<0.2?'dark':'light';e=e.parentElement}return 'light'};
 return [...document.querySelectorAll(sel)].filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&r.height>0}).map((e,i)=>{const cs=getComputedStyle(e);const r=e.getBoundingClientRect();
  return {i:i,sig:e.tagName.toLowerCase()+'.'+[...e.classList].filter(c=>!/^btn/.test(c)).slice(0,2).join('.'),txt:(e.innerText||e.value||'').trim().slice(0,30),surface:surf(e),bg:cs.backgroundColor,fg:cs.color,line:cs.borderTopColor,bw:cs.borderTopWidth,h:Math.round(r.height*10)/10,ff:cs.fontFamily.slice(0,10),fs:cs.fontSize,fw:cs.fontWeight,tt:cs.textTransform,rad:cs.borderTopLeftRadius,sel:e.matches('[aria-pressed="true"],[aria-selected="true"],.active,.is-selected,.selected,[class*="--active"]'),aria:(e.getAttribute('aria-pressed')||e.getAttribute('aria-selected')||''),grp:e.parentElement?[...e.parentElement.children].filter(c=>c.classList.contains('btn--secondary')).length:1}})}"""
def expect(kind,surface,sel):
    if kind=='primary':
        if sel: return (RGB['white'],RGB['black'],RGB['black'] if surface=='light' else RGB['white'])
        return (RGB['s6'],RGB['white'],RGB['s5'] if surface=='light' else RGB['s4'])
    if sel: return ((RGB['black'],RGB['white'],RGB['black']) if surface=='light' else (RGB['white'],RGB['black'],RGB['white']))
    return ('rgba(0, 0, 0, 0)',RGB['black'] if surface=='light' else RGB['white'],RGB['s6'] if surface=='light' else RGB['s4'])
def run(kinds=('primary','secondary'),only=None,port=9041,hover=True):
    serve(port); bad=[]; seen=collections.defaultdict(int) if False else {}
    import collections
    count=collections.Counter(); hv=[]
    with sync_playwright() as p:
        b=p.chromium.launch()
        for n,u,f in PUB:
            if only and n not in only: continue
            pg=b.new_page(viewport={'width':1440,'height':900})
            try:
                pg.goto('http://127.0.0.1:%d%s'%(port,u),wait_until='domcontentloaded',timeout=30000); pg.wait_for_timeout(2200)
            except Exception as e: print('ERR',n); pg.close(); continue
            for kind in kinds:
                sel='.btn--%s,.nav-search-btn'%kind if kind=='primary' else '.btn--secondary'
                for r in pg.evaluate(JS,sel):
                    count[kind]+=1
                    e=expect(kind,r['surface'],r['sel']); got=(r['bg'],r['fg'],r['line'])
                    probs=[]
                    if got!=e: probs.append('colours %s expected %s'%(got,e))
                    if r['h']<43.9: probs.append('height %s'%r['h'])
                    if r['tt']!='none': probs.append('text-transform '+r['tt'])
                    if r['fw']!='600' or r['fs']!='15px' or not r['ff'].startswith('Inter'): probs.append('type %s %s %s'%(r['ff'],r['fs'],r['fw']))
                    if r['rad']!='6px': probs.append('radius '+r['rad'])
                    if kind=='secondary' and r['grp']>=2 and r['aria'] not in ('true','false'): probs.append('no aria state')
                    if kind=='secondary' and r['aria']=='true' and not r['sel']: probs.append('aria true but class not selected')
                    if probs: bad.append((f,kind,r['sig'],r['txt'],r['surface'],probs))
                # hover first instance of each signature
                if hover:
                    done=set()
                    for r in pg.evaluate(JS,sel):
                        if r['sig'] in done or r['sel']: continue
                        done.add(r['sig'])
                        loc=pg.locator(sel).nth(r['i'] if False else 0)
                    # simpler: hover each distinct signature by index among visible
                    els=pg.locator(sel); cnt=els.count()
                    sigs=set()
                    for k in range(cnt):
                        el=els.nth(k)
                        try:
                            if not el.is_visible(): continue
                            sg=el.evaluate("e=>e.tagName.toLowerCase()+'.'+[...e.classList].filter(c=>!/^btn/.test(c)).slice(0,2).join('.')")
                            if sg in sigs: continue
                            sigs.add(sg); el.scroll_into_view_if_needed(timeout=2000); el.hover(timeout=2000); pg.wait_for_timeout(350)
                            st=el.evaluate("e=>[getComputedStyle(e).backgroundColor,getComputedStyle(e).color,getComputedStyle(e).borderTopColor]")
                            if tuple(st)!=(RGB['acid'],RGB['black'],RGB['acid']): hv.append((f,sg,st))
                            pg.mouse.move(0,0)
                        except Exception as ex: hv.append((f,sg if 'sg' in dir() else '?','hover-error '+str(ex)[:50]))
            pg.close()
        b.close()
    return count,bad,hv
if __name__=='__main__':
    only=sys.argv[1].split(',') if len(sys.argv)>1 and sys.argv[1]!='all' else None
    count,bad,hv=run(only=only)
    print('checked',dict(count)); print('REST problems:',len(bad))
    for x in bad: print('  ',x)
    print('HOVER problems:',len(hv))
    for x in hv: print('  ',x)
