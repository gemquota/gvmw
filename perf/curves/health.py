# Behaviour pass: 150 ticks, 1 run, no warm-up (timing NOT used). Peak RSS via wait4 (node parent + bench child).
import json, subprocess, csv, os, sys
from concurrent.futures import ThreadPoolExecutor
os.chdir('/workspace/vepa')
NODE='/workspace/tools/node22/node-v22.23.3-linux-x64/bin/node'
OUT='/workspace/out/fidelity-curves/health150-raw.csv'
SIZES=[int(s) for s in os.environ.get('SIZES','500,1000,1500,2000,2500,5000,7500,10000,12500,15000,17500,20000,22500,25000,30000,35000,40000,45000,50000').split(',')]
done=set()
if os.path.exists(OUT):
  for r in csv.DictReader(open(OUT)): done.add((r['preset'],int(r['size'])))
new=not os.path.exists(OUT); fh=open(OUT,'a',newline=''); w=csv.writer(fh)
if new: w.writerow(['preset','size','ticks','alive','species','bonded_150','bonded_pct_150','nan_energy','nan_repairs','end_rss_mb','end_heap_mb','peak_rss_mb','buffer_mb','hash']); fh.flush()
def job(a):
  lv,size=a
  p=subprocess.Popen([NODE,'bench/solver-tps.mjs','--sizes',str(size),'--runs','1','--warm','0','--ticks','150','--json','--speed',lv.lower()],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
  so=p.stdout.read(); p.stderr.read(); _,st,ru=os.wait4(p.pid,0)
  j=json.loads(so[so.index('{'):]); x=j['sizes'][str(size)]
  return [lv,size,150,x['alive'],x['species'],x['bonded'],round(100*x['bonded']/max(1,x['alive']),2),x['nanEnergy'],x['nanRepairs'],x['rssMB'],x['heapMB'],round(ru.ru_maxrss/1024,1),x['bufferMB'],x['hash']]
todo=[(lv,s) for s in SIZES for lv in ['HIGH','MEDIUM','LOW','LOWEST'] if (lv,s) not in done]
with ThreadPoolExecutor(int(os.environ.get('PAR','4'))) as ex:
  for row in ex.map(job,todo):
    w.writerow(row); fh.flush(); print(*row[:2],row[6],row[11],flush=True)
