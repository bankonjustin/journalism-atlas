import sys, os, json
sys.path.insert(0,'.')
import numpy as np
from PIL import Image, ImageFilter
Image.MAX_IMAGE_PIXELS=None
from s1shot import REPO
S=REPO+'/docs/design/v15-session-2/screenshots/'
def load(p):
    im=Image.open(p).convert('RGB')
    if im.size[1]>40000: im=im.crop((0,0,im.size[0],15000))   # search.html: compare the first 15,000px only
    return np.asarray(im).astype(np.int16)
def noise_mask(name,w=1440):
    if not os.path.exists(S+'before2/%s-%d.png'%(name,w)): return None
    a=load(S+'before/%s-%d.png'%(name,w)); b=load(S+'before2/%s-%d.png'%(name,w))
    if a.shape!=b.shape: return None  # unstable height
    m=(np.abs(a-b).max(axis=2)>0)
    if not m.any(): return m
    im=Image.fromarray((m*255).astype('uint8')).filter(ImageFilter.MaxFilter(9))
    return np.asarray(im)>0
def compare(name,after_tag,w=1440,th=8,ref='before'):
    pa=S+'%s/%s-%d.png'%(ref,name,w); pb=S+'%s/%s-%d.png'%(after_tag,name,w)
    a=load(pa); b=load(pb)
    r=dict(page=name)
    if a.shape!=b.shape:
        r.update(status='FLAG',note='height/size changed %s -> %s'%(a.shape[:2],b.shape[:2])); return r
    d=np.abs(a-b).max(axis=2)
    nm=noise_mask(name,w)
    unstable = nm is None
    if nm is not None: d=np.where(nm,0,d)
    changed=(d>0)
    big=(d>th)
    r['changed_pct']=round(100*changed.mean(),2); r['maxdelta']=int(d.max()); r['big_px']=int(big.sum())
    if big.any():
        ys,xs=np.where(big); r['bbox']=(int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max()))
    r['status']='PASS' if not big.any() else 'FLAG'
    return r
if __name__=='__main__':
    tag=sys.argv[1]; pages=sys.argv[2].split(',') if len(sys.argv)>2 and sys.argv[2]!='all' else [f[:-4].rsplit('-',1)[0] for f in sorted(os.listdir(S+tag)) if f.endswith('-1440.png')]
    out=[compare(p,tag) for p in pages]
    for r in out: print(r)
    json.dump(out,open(S+'cmp-%s.json'%tag,'w'),indent=1)
