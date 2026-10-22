import re
def sents(t):
    # split after . ; or : followed by space and a capital/quote/paren; keep exact separators
    parts=re.split(r'(?<=[.!?])(\s+)(?=[A-Z(\'"0-9])',t)
    out=[];seps=[]
    for i,p in enumerate(parts):
        if i%2==0: out.append(p)
        else: seps.append(p)
    return out,seps
