# Build an instrumented copy of the repo's src/ in /tmp/nanhunt/src.
import os, re, shutil, sys
sys.path.insert(0,'/workspace/perf/nanhunt')
from brace import match_end
SRC='/workspace/vepa/src'; DST='/tmp/nanhunt/src'
shutil.rmtree('/tmp/nanhunt', ignore_errors=True); shutil.copytree(SRC, DST)
p=DST+'/physics/solver.js'; L=open(p).read().split('\n')
def find(pat, start=0):
    for k in range(start, len(L)):
        if re.search(pat, L[k]): return k
    raise SystemExit('nf '+pat)
ph3=find(r'── Phase 3: Pairwise')
pl=find(r'^  for \(let i = 0; i < particleCount; i\+\+\) \{', ph3)
pl_end=match_end(L, pl)
pr=find(r'^    for \(let n = 0; n < limit; n\+\+\) \{', pl)
pr_end=match_end(L, pr)
jb=find(r'^      const jBase = j \* stride;', pr)
ib=find(r'const iBase = i \* stride;', pl)
fn_end=match_end(L, find(r'^export function solve\('))
out=[]
def prev_ok(k):
    j=k-1
    while j>=0 and not L[j].strip(): j-=1
    t=L[j].rstrip()
    return t.endswith((';','{','}')) or t.lstrip().startswith('//')
for k,l in enumerate(L):
    lab=f'L{k+1}'
    if not prev_ok(k):
        out.append(l)
        if k == ib: out.append(f'    if (globalThis.__nanOn) globalThis.__nanChk("L{k+1}-start", iBase, -1);')
        continue
    if jb < k < pr_end and re.match(r'^      (if \(|// ──|const \w+ = apply|apply)', l):
        out.append(f'      if (globalThis.__nanOn) globalThis.__nanChk("{lab}", iBase, jBase);')
    elif (ib < k < pr or pr_end < k < pl_end) and re.match(r'^\s{2,6}(if \(|// ──|const \w+ = apply|apply)', l):
        out.append(f'    if (globalThis.__nanOn) globalThis.__nanChk("{lab}", iBase, -1);')
    elif (ph3 < k < fn_end) and k > pl_end and re.match(r'^  (// ──|if \(|for \()', l):
        out.append(f'  if (globalThis.__nanOn) globalThis.__nanAll("{lab}");')
    elif k < pl and k > find(r'^export function solve\(') and re.match(r'^  // ── Phase', l):
        out.append(f'  if (globalThis.__nanOn) globalThis.__nanAll("{lab}");')
    out.append(l)
    if k == ib:  # right after iBase is defined
        out.append(f'    if (globalThis.__nanOn) globalThis.__nanChk("L{k+1}-start", iBase, -1);')
# end-of-solve check
s='\n'.join(out)
open(p,'w').write(s)
print('pl',pl+1,pl_end+1,'pr',pr+1,pr_end+1,'jb',jb+1,'ib',ib+1,'fn_end',fn_end+1)
