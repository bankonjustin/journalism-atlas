import sys; sys.path.insert(0,'/private/tmp/claude-502/-Users-bankids-Documents-GitHub/70fa26fc-8f34-41b1-b7d8-511f593c31ee/scratchpad')
from atlasscan import *
PUB=[]
for f in FILES:
    if f.endswith('.html') and page_class(f)=='public':
        u='/'+f[:-5]
        if f=='index.html': u='/'
        elif f.endswith('/index.html'): u='/'+f[:-10]+'/'
        PUB.append((f[:-5].replace('/','__') if f!='index.html' else 'index',u,f))
