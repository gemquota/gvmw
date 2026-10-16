import json, subprocess, csv, sys, os
os.chdir('/workspace/vepa')
NODE='/workspace/tools/node22/node-v22.23.3-linux-x64/bin/node'
stages=json.load(open(sys.argv[1]))  # [[label, "K=V,K=V" or "none"], ...]
out='/workspace/out/speed-charts/cumulative-raw.csv'
f=open(out,'w',newline=''); w=csv.writer(f)
w.writerow(['stage','settings','size','ms_per_tick','ticks_per_s','alive','species','bonded','bonded_pct','hash','load1'])
for label, spec in stages:
    r=subprocess.run([NODE,'bench/solver-tps.mjs','--sizes','2500,10000','--runs','1','--warm','3','--ticks','10','--json','--speed',spec],capture_output=True,text=True)
    if r.returncode: print(r.stderr); sys.exit(1)
    j=json.loads(r.stdout[r.stdout.index('{'):])
    for n,x in j['sizes'].items():
        w.writerow([label,spec,n,x['medMsPerTick'],x['ticksPerSec'],x['alive'],x['species'],x['bonded'],round(100*x['bonded']/max(1,x['alive']),2),x['hash'],j['load1Start']])
    f.flush(); print('done',label,flush=True)
