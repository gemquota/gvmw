# usage: res.py file choice1 choice2 ...  (ours|theirs|both|both_rev|SEP:<text between>) per conflict in order
import sys,re
p=sys.argv[1]; ch=sys.argv[2:]
L=open(p).read().split('\n'); out=[]; i=0; k=0
while i<len(L):
    if L[i].startswith('<<<<<<< '):
        o=[];t=[];i+=1
        while not L[i].startswith('=======') : o.append(L[i]); i+=1
        i+=1
        while not L[i].startswith('>>>>>>> '): t.append(L[i]); i+=1
        i+=1; c=ch[k]; k+=1
        if c=='ours': out+=o
        elif c=='theirs': out+=t
        elif c=='both': out+=o+t
        elif c=='both_rev': out+=t+o
        elif c.startswith('SEP:'): out+=o+c[4:].split('\\n')+t
        else: raise SystemExit('bad '+c)
    else: out.append(L[i]); i+=1
assert k==len(ch),(k,len(ch))
open(p,'w').write('\n'.join(out)); print(p,'resolved',k)
