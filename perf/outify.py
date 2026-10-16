import re,sys
def split_top(s):
    parts=[];depth=0;cur=''
    for ch in s:
        if ch in '([{': depth+=1
        elif ch in ')]}': depth-=1
        if ch==',' and depth==0: parts.append(cur); cur=''
        else: cur+=ch
    if cur.strip(): parts.append(cur)
    return [p.strip() for p in parts]
def func_range(src,name):
    m=re.search(r'^(export )?function '+name+r'\(([^)]*)\) \{', src, re.M)
    assert m, name
    # find end: first line '}' at col 0 after
    end=src.index('\n}\n', m.end())+2
    return m, end
def outify(src,name):
    m,end=func_range(src,name)
    params=m.group(2)
    newsig=m.group(0).replace('('+params+')','('+params+', out)')
    body=src[m.end():end]
    # object literal returns/assignments of {ax,ay,az}
    pat=re.compile(r'\{\s*ax:\s*', re.S)
    out=''; i=0; n=0
    while True:
        k=body.find('{',i)
        if k<0: out+=body[i:]; break
        mm=pat.match(body,k)
        if not mm: out+=body[i:k+1]; i=k+1; continue
        # find matching brace
        depth=0
        for j in range(k,len(body)):
            if body[j]=='{': depth+=1
            elif body[j]=='}':
                depth-=1
                if depth==0: break
        inner=body[k+1:j]
        props=split_top(inner)
        vals={}
        for p in props:
            key,_,v=p.partition(':'); vals[key.strip()]=v.strip()
        assert list(vals)==['ax','ay','az'], (name, vals)
        out+=body[i:k]+f"outForce(out, {vals['ax']}, {vals['ay']}, {vals['az']})"
        i=j+1; n+=1
    body=out
    c=body.count('force3(')
    body=body.replace('force3(','force3Into(out, ')
    return src[:m.start()]+newsig+body+src[end:], n+c
p,names=sys.argv[1],sys.argv[2:]
src=open(p).read()
for nm in names:
    src,n=outify(src,nm); print(nm,n)
open(p,'w').write(src)
