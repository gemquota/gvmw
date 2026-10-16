#!/bin/bash
# usage: prof.sh count ticks [laws] [repo]
R=${4:-/workspace/vepa}
D=/tmp/cpuprof-$1; rm -rf $D; mkdir -p $D
cd $R && node --cpu-prof --cpu-prof-dir=$D bench/solver-tps.mjs --child $1 $2 3 ${3:-tidal} >/dev/null
python3 - $D <<'PY'
import json,glob,collections,sys
p=json.load(open(glob.glob(sys.argv[1]+'/*.cpuprofile')[0]))
nodes={n['id']:n for n in p['nodes']}
self=collections.Counter(); dt=p['timeDeltas']
for i,s in enumerate(p['samples']): self[s]+=dt[i] if i<len(dt) else 0
tot=sum(self.values()); agg=collections.Counter()
for nid,t in self.items():
  cf=nodes[nid]['callFrame']; agg[(cf['functionName'] or '(anon)', cf['url'].split('/')[-1], cf['lineNumber']+1)]+=t
for k,v in agg.most_common(30): print(f"{100*v/tot:5.1f}% {k}")
PY
