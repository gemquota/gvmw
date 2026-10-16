import json, subprocess, csv, sys, os
os.chdir('/workspace/vepa')
NODE='/workspace/tools/node22/node-v22.23.3-linux-x64/bin/node'
stages=json.load(open('/workspace/perf/cum_stages.json'))
out='/workspace/out/speed-charts/cumulative-v2-raw.csv'
f=open(out,'w',newline=''); w=csv.writer(f)
w.writerow(['stage','settings','size','rep','ms_per_tick','alive','species','bonded','bonded_pct','hash','load1'])
REPS=3
for rep in range(REPS):            # interleave repeats so slow drift hits every stage equally
  for label, spec in stages:
    r=subprocess.run([NODE,'bench/solver-tps.mjs','--sizes','2500,10000','--runs','1','--warm','3','--ticks','10','--json','--speed',spec],capture_output=True,text=True)
    if r.returncode: print(r.stderr); sys.exit(1)
    j=json.loads(r.stdout[r.stdout.index('{'):])
    for n,x in j['sizes'].items():
      w.writerow([label,spec,n,rep,x['medMsPerTick'],x['alive'],x['species'],x['bonded'],round(100*x['bonded']/max(1,x['alive']),2),x['hash'],j['load1Start']])
    f.flush(); print('done',rep,label,flush=True)
