import json, subprocess, csv, os
os.chdir('/workspace/vepa')
NODE='/workspace/tools/node22/node-v22.23.3-linux-x64/bin/node'
out='/workspace/out/fidelity-bench/solver-raw.csv'
w=csv.writer(open(out,'w',newline=''))
w.writerow(['preset','size','ticks','runs','ms_per_tick_median','ticks_per_s','runs_ms','hash','deterministic','alive','species','bonded','bonded_pct','nan_energy','nan_repairs','rss_mb','heap_mb','buffer_mb','load1_start','load1_end','note'])
for size in [100,500,2500,10000,50000]:
  for preset in ['high','medium','low']:
    ticks = 10 if size==50000 else 30
    r=subprocess.run([NODE,'bench/solver-tps.mjs','--sizes',str(size),'--runs','3','--warm','3','--ticks',str(ticks),'--json','--speed',preset],capture_output=True,text=True)
    if r.returncode: print(r.stderr); continue
    j=json.loads(r.stdout[r.stdout.index('{'):]); x=j['sizes'][str(size)]
    w.writerow([preset.upper(),size,ticks,3,x['medMsPerTick'],x['ticksPerSec'],'/'.join(map(str,x['runsMs'])),x['hash'],x['deterministic'],x['alive'],x['species'],x['bonded'],round(100*x['bonded']/max(1,x['alive']),2),x['nanEnergy'],x['nanRepairs'],x['rssMB'],x['heapMB'],x['bufferMB'],j['load1Start'],j['load1End'],'DEV BENCH: above the app 10k cap (solver only)' if size>10000 else ''])
    print(preset,size,x['ticksPerSec'],flush=True)
