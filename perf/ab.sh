#!/bin/bash
# usage: ab.sh dirA dirB sizes runs  — bench:solver interleaved A,B,A,B
A=$1; B=$2; S=${3:-300,1000,2500,10000}; R=${4:-3}
for i in 1 2; do
  (cd $A && node bench/solver-tps.mjs --sizes $S --runs $R --json) > /tmp/ab-A-$i.json
  (cd $B && node bench/solver-tps.mjs --sizes $S --runs $R --json) > /tmp/ab-B-$i.json
done
python3 - <<'PY'
import json,statistics
res={}
for lab in 'AB':
  for i in (1,2):
    d=json.load(open(f'/tmp/ab-{lab}-{i}.json'))
    for k,v in d['sizes'].items():
      res.setdefault((lab,k),[]).append((v['medMsPerTick'],v['hash']))
sizes=sorted({k for _,k in res},key=int)
for k in sizes:
  a=[x[0] for x in res[('A',k)]]; b=[x[0] for x in res[('B',k)]]
  ha={x[1] for x in res[('A',k)]}; hb={x[1] for x in res[('B',k)]}
  ma=statistics.median(a); mb=statistics.median(b)
  print(f"{k:>6}: A {1000/ma:7.2f} t/s  B {1000/mb:7.2f} t/s  gain {ma/mb:5.3f}x  hashes {'SAME' if ha==hb and len(ha)==1 else 'DIFF '+str(ha)+str(hb)}")
PY
