import json,sys,glob,collections
p=json.load(open(glob.glob(sys.argv[1]+'/*.cpuprofile')[0]))
nodes={n['id']:n for n in p['nodes']}
self=collections.Counter()
for sid,dt in zip(p['samples'],p['timeDeltas']): self[sid]+=dt
tot=sum(self.values())
fn=collections.Counter()
for i,t in self.items():
    cf=nodes[i]['callFrame']; fn[f"{cf['functionName'] or '(anon)'} {cf['url'].split('/')[-1]}:{cf['lineNumber']+1}"]+=t
for k,v in fn.most_common(int(sys.argv[2]) if len(sys.argv)>2 else 25): print(f"{100*v/tot:5.1f}% {k}")
