import sys; sys.path.insert(0,'.')
from s1shot import *; from pages40 import PUB
tag=sys.argv[1]; widths=tuple(int(x) for x in sys.argv[2].split(','))
only=sys.argv[3].split(',') if len(sys.argv)>3 and sys.argv[3] not in ('','all') else None
pages=[(n,u) for n,u,f in PUB if (not only or n in only)]
out=REPO+'/docs/design/v15-session-2/screenshots/'+tag
print(shoot(pages,out,widths=widths,port=int(sys.argv[4]) if len(sys.argv)>4 else 8811))
