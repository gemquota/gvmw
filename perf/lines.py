import json,glob,collections,sys
# usage: lines.py profdir funcName file
p=json.load(open(glob.glob(sys.argv[1]+'/*.cpuprofile')[0]))
fn=sys.argv[2]; f=sys.argv[3]
c=collections.Counter(); tot=0
for n in p['nodes']:
  cf=n['callFrame']
  for pt in n.get('positionTicks',[]): tot+=pt['ticks']
  if cf['functionName']==fn and cf['url'].endswith(f):
    for pt in n.get('positionTicks',[]): c[pt['line']]+=pt['ticks']
src=open('/workspace/vepa/src/physics/'+f).read().split('\n') if '/' not in f else open(f).read().split('\n')
s=sum(c.values())
print('func ticks',s,'of',tot)
for line,t in c.most_common(40): print(f"{100*t/tot:5.1f}% L{line}: {src[line-1].strip()[:110]}")
