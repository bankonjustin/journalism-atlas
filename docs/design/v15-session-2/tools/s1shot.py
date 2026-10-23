import http.server, socketserver, threading, os, sys, json
from playwright.sync_api import sync_playwright
from PIL import Image, ImageChops
Image.MAX_IMAGE_PIXELS=None
REPO=os.path.expanduser('~/Documents/GitHub/journalism-atlas')
rewrites={}
for l in open(REPO+'/_redirects'):
    p=l.split()
    if len(p)>=3 and p[2]=='200' and not p[0].endswith('*'): rewrites[p[0]]=p[1]
class H(http.server.SimpleHTTPRequestHandler):
    def __init__(s,*a,**k): super().__init__(*a,directory=REPO,**k)
    def log_message(s,*a): pass
    def translate_path(s,path):
        p=path.split('?')[0].split('#')[0]; p=rewrites.get(p,p)
        full=os.path.join(REPO,p.lstrip('/'))
        if os.path.isdir(full) and os.path.exists(os.path.join(full,'index.html')): return os.path.join(full,'index.html')
        if not os.path.exists(full) and os.path.exists(full+'.html'): return full+'.html'
        return super().translate_path(p)
def serve(port):
    socketserver.TCPServer.allow_reuse_address=True
    srv=socketserver.ThreadingTCPServer(('127.0.0.1',port),H); threading.Thread(target=srv.serve_forever,daemon=True).start(); return srv
def shoot(pages, outdir, widths=(1440,), port=8801, settle=1500):
    """pages: list of (name,url). Saves outdir/name-W.png; returns log"""
    os.makedirs(outdir,exist_ok=True); serve(port); log={}
    with sync_playwright() as p:
        b=p.chromium.launch()
        for w in widths:
            ctx=b.new_context(viewport={'width':w,'height':900 if w>600 else 844},device_scale_factor=1)
            for name,url in pages:
                pg=ctx.new_page()
                try:
                    try: pg.goto('http://127.0.0.1:%d%s'%(port,url),wait_until='load',timeout=30000)
                    except Exception: pg.goto('http://127.0.0.1:%d%s'%(port,url),wait_until='domcontentloaded',timeout=30000)
                    try: pg.wait_for_load_state('networkidle',timeout=8000)
                    except Exception: pass
                    pg.wait_for_timeout(settle)
                    pg.screenshot(path='%s/%s-%d.png'%(outdir,name,w),full_page=True)
                    log[name+'-%d'%w]='ok'
                except Exception as e: log[name+'-%d'%w]='ERR '+str(e)[:100]
                pg.close()
            ctx.close()
        b.close()
    return log
def diff(a,b):
    A=Image.open(a).convert('RGB'); B=Image.open(b).convert('RGB')
    if A.size!=B.size: return dict(same=False,size=(A.size,B.size),pct=None)
    d=ImageChops.difference(A,B); bbox=d.getbbox()
    if not bbox: return dict(same=True,pct=0.0,maxdelta=0)
    px=sum(1 for v in d.convert('L').getdata() if v>0)
    return dict(same=False,pct=round(100*px/(A.size[0]*A.size[1]),3),bbox=bbox,maxdelta=max(d.convert('L').getdata()))
