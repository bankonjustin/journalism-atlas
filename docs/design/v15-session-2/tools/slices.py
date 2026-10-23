import sys,os,io,http.server,socketserver,threading; sys.path.insert(0,'.')
from playwright.sync_api import sync_playwright
import numpy as np
from PIL import Image
SC=os.getcwd()
def mk(root,port):
    rewrites={}
    for l in open(os.path.join(root,'_redirects')):
        p=l.split()
        if len(p)>=3 and p[2]=='200' and not p[0].endswith('*'): rewrites[p[0]]=p[1]
    class H(http.server.SimpleHTTPRequestHandler):
        def __init__(s,*a,**k): super().__init__(*a,directory=root,**k)
        def log_message(s,*a): pass
        def translate_path(s,path):
            p=path.split('?')[0].split('#')[0]; p=rewrites.get(p,p); full=os.path.join(root,p.lstrip('/'))
            if os.path.isdir(full) and os.path.exists(os.path.join(full,'index.html')): return os.path.join(full,'index.html')
            if not os.path.exists(full) and os.path.exists(full+'.html'): return full+'.html'
            return super().translate_path(p)
    socketserver.TCPServer.allow_reuse_address=True
    s=socketserver.ThreadingTCPServer(('127.0.0.1',port),H); threading.Thread(target=s.serve_forever,daemon=True).start()
def slices(url,port,w,offs,settle=5000,h=1000):
    out=[]
    with sync_playwright() as p:
        b=p.chromium.launch(); pg=b.new_page(viewport={'width':w,'height':h})
        pg.goto('http://127.0.0.1:%d%s'%(port,url),wait_until='load'); 
        try: pg.wait_for_load_state('networkidle',timeout=8000)
        except Exception: pass
        pg.wait_for_timeout(settle)
        for o in offs:
            pg.evaluate('window.scrollTo(0,%d)'%o); pg.wait_for_timeout(700)
            out.append(np.asarray(Image.open(io.BytesIO(pg.screenshot())).convert('RGB')).astype(int))
        b.close()
    return out
if __name__=='__main__':
    url=sys.argv[1]; w=int(sys.argv[2]); offs=[int(x) for x in sys.argv[3].split(',')]
    mk(SC+'/oldtree',8901); mk(os.path.expanduser('~/Documents/GitHub/journalism-atlas'),8902)
    A=slices(url,8901,w,offs); B=slices(url,8902,w,offs)
    for o,a,b in zip(offs,A,B):
        d=np.abs(a-b).max(axis=2); print(url,w,'offset',o,'max',int(d.max()),'big>8:',int((d>8).sum()),'changed%%:%.2f'%(100*(d>0).mean()))
