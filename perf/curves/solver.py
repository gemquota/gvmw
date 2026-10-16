# Timing pass: 14 sizes x 4 levels, median of 3 fresh-process runs, 30 ticks after 3 warm-up.
# Appends one CSV row per (size, level) so an interruption keeps the data.
import json, subprocess, csv, os, sys, time
os.chdir('/workspace/vepa')
NODE='/workspace/tools/node22/node-v22.23.3-linux-x64/bin/node'
OUT='/workspace/out/fidelity-curves/solver-raw.csv'
SIZES=[int(s) for s in os.environ.get('SIZES','500,1000,1500,2000,2500,5000,7500,10000,12500,15000,17500,20000,22500,25000').split(',')]
RUNS=int(os.environ.get('RUNS','3'))
done=set()
if os.path.exists(OUT):
  for r in csv.DictReader(open(OUT)): done.add((r['preset'],int(r['size'])))
new=not os.path.exists(OUT); fh=open(OUT,'a',newline=''); w=csv.writer(fh)
if new: w.writerow(['preset','size','ticks','runs','ms_per_tick_median','ticks_per_s','runs_ms','hash','deterministic','alive','species','bonded_30','bonded_pct_30','nan_energy','nan_repairs','end_rss_mb','end_heap_mb','peak_rss_mb','buffer_mb','load1_start','load1_end','wall_s'])
for size in SIZES:
  for lv in ['HIGH','MEDIUM','LOW','LOWEST']:
    if (lv,size) in done: continue
    t0=time.time()
    p=subprocess.Popen([NODE,'bench/solver-tps.mjs','--sizes',str(size),'--runs',str(RUNS),'--warm','3','--ticks','30','--json','--speed',lv.lower()],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    so,se=p.communicate(); ru=None
    try:
      import resource; ru=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss/1024
    except Exception: pass
    if p.returncode: print('ERR',lv,size,se[-400:],flush=True); continue
    j=json.loads(so[so.index('{'):]); x=j['sizes'][str(size)]
    w.writerow([lv,size,30,RUNS,x['medMsPerTick'],x['ticksPerSec'],'/'.join(map(str,x['runsMs'])),x['hash'],x['deterministic'],x['alive'],x['species'],x['bonded'],round(100*x['bonded']/max(1,x['alive']),2),x['nanEnergy'],x['nanRepairs'],x['rssMB'],x['heapMB'],'',x['bufferMB'],j['load1Start'],j['load1End'],round(time.time()-t0,1)])
    fh.flush(); print(lv,size,x['ticksPerSec'],round(time.time()-t0),'s',flush=True)
