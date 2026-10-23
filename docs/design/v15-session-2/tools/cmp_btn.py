import sys,os,json; sys.path.insert(0,'.')
import numpy as np
from PIL import Image, ImageFilter
Image.MAX_IMAGE_PIXELS=None
import cmp2 as cmp
S=cmp.S
def analyse(tag,ref='before',widths=(1440,390),pad=24,pages=None):
    rects=json.load(open(S+tag+'/rects.json'))
    out=[]
    names=sorted({f.rsplit('-',1)[0] for f in os.listdir(S+tag) if f.endswith('.png')})
    for n in names:
        if pages and n not in pages: continue
        for w in widths:
            pa=S+'%s/%s-%d.png'%(ref,n,w); pb=S+'%s/%s-%d.png'%(tag,n,w)
            if not (os.path.exists(pa) and os.path.exists(pb)): continue
            A=Image.open(pa); B=Image.open(pb)
            if A.size[1]>40000 or B.size[1]>40000:
                out.append((n,w,'skip(very tall)',A.size[1],B.size[1])); continue
            a=np.asarray(A.convert('RGB')).astype(int); b=np.asarray(B.convert('RGB')).astype(int)
            dh=b.shape[0]-a.shape[0]
            rs=rects.get('%s-%d'%(n,w),[])
            if a.shape!=b.shape:
                out.append((n,w,'HEIGHT %+d'%dh,len(rs),'buttons')); continue
            d=np.abs(a-b).max(axis=2)>8
            nm=cmp.noise_mask(n,w) if w==1440 else None
            if nm is not None and nm.shape==d.shape: d=d&~nm
            m=np.zeros(d.shape,bool)
            for x,y,ww,hh in rs: m[max(0,y-pad):y+hh+pad,max(0,x-pad):x+ww+pad]=True
            outside=int((d&~m).sum()); inside=int((d&m).sum())
            out.append((n,w,'same height',inside,outside))
    return out
if __name__=='__main__':
    tag=sys.argv[1]
    for r in analyse(tag): print(r)
