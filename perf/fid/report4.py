import csv, json, glob, matplotlib, numpy as np, shutil
matplotlib.use('Agg'); import matplotlib.pyplot as plt
D='/workspace/out/fidelity-bench'; F='/workspace/perf/fid'
BG='#0b0d14'; PANEL='#11141d'; FG='#d6dae4'; DIM='#7d8597'; COL={'HIGH':'#4aa3ff','MEDIUM':'#f5c542','LOW':'#ff9a3c','LOWEST':'#ff5a5a'}
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'text.color':FG,'axes.labelcolor':FG,'xtick.color':DIM,'ytick.color':DIM,'axes.edgecolor':'#2a3040','figure.facecolor':BG,'axes.facecolor':PANEL,'grid.color':'#232838','savefig.facecolor':BG})
L=['HIGH','MEDIUM','LOW','LOWEST']; sz=[100,500,2500,10000,50000]
# solver (fix the old note: 50k is now inside the 100k cap)
S=list(csv.DictReader(open(f'{D}/solver-raw.csv')))
for r in S: r['note']='10 ticks timed at 50k' if r['size']=='50000' else ''
with open(f'{D}/solver-raw.csv','w',newline='') as fh: w=csv.DictWriter(fh,S[0].keys()); w.writeheader(); w.writerows(S)
s={(r['preset'],int(r['size'])):r for r in S}
# 150-tick health
H={}; rows=[]
for lv in L:
  for n in sz:
    t=open(f'{F}/h150/{lv.lower()}-{n}.json').read(); d=json.loads(t[t.index('{'):]); x=d['sizes'][str(n)]
    H[(lv,n)]=x; rows.append([lv,n,150,x['alive'],x['species'],x['bonded'],round(100*x['bonded']/max(1,x['alive']),1),x['nanEnergy'],x['nanRepairs'],x['hash']])
with open(f'{D}/health-150ticks.csv','w',newline='') as fh: w=csv.writer(fh); w.writerow(['preset','size','ticks','alive','species','bonded','bonded_pct','nan_energy','nan_repairs','hash']); w.writerows(rows)
# multiplex
t=open(f'{F}/mpx-fid4.json').read(); md=json.loads(t[t.index('{'):])
M=[{'preset':r['case'].split()[-1],'laws':r['laws'],'sims':r['sims'],'per_sim':r['perSim'],'tps_per_sim':r['tpsPerSim'],'tps_min':r['tpsMin'],'frame_p95_ms':r['frameP95Ms']} for r in md['results']]
with open(f'{D}/multiplex-raw.csv','w',newline='') as fh: w=csv.DictWriter(fh,M[0].keys()); w.writeheader(); w.writerows(M)
mp={r['preset']:float(r['tps_per_sim']) for r in M}
# browser
shutil.copy(f'{F}/browser4-raw.csv',f'{D}/browser-raw.csv')
B=list(csv.DictReader(open(f'{D}/browser-raw.csv'))); b={(r['preset'],int(r['size'])):r for r in B}; bz=sorted({int(r['size']) for r in B})
# chart
fig,axs=plt.subplots(1,3,figsize=(18,5.8)); x=np.arange(len(sz)); w=0.2
ax=axs[0]
for i,lv in enumerate(L):
  g=[float(s[(lv,n)]['ticks_per_s'])/float(s[('HIGH',n)]['ticks_per_s']) for n in sz]
  ax.bar(x+(i-1.5)*w,g,w,color=COL[lv],label=lv)
  for xi,v in zip(x+(i-1.5)*w,g): ax.text(xi,v+0.2,f'{v:.1f}',ha='center',fontsize=7,color=FG)
ax.set_xticks(x); ax.set_xticklabels([f'{n:,}' for n in sz]); ax.set_title('Solver speed-up vs HIGH (median of 3 runs)',color=FG); ax.set_ylabel('× ticks/s vs HIGH'); ax.set_xlabel('particles'); ax.grid(True,axis='y',alpha=.6); ax.legend(facecolor=PANEL,edgecolor='#2a3040',labelcolor=FG)
ax=axs[1]
for i,lv in enumerate(L):
  ax.bar(x+(i-1.5)*w,[100*H[(lv,n)]['bonded']/H[(lv,n)]['alive'] for n in sz],w,color=COL[lv],label=f'{lv} @150 ticks')
  ax.plot(x+(i-1.5)*w,[float(s[(lv,n)]['bonded_pct']) for n in sz],'o',color='white',ms=3)
ax.set_xticks(x); ax.set_xticklabels([f'{n:,}' for n in sz]); ax.set_ylim(0,122); ax.set_ylabel('bonded % of alive'); ax.set_xlabel('particles')
ax.set_title('Bonded %: bars after 150 ticks, dots after 30 ticks (10 at 50k)',color=FG,fontsize=10); ax.grid(True,axis='y',alpha=.5); ax.legend(facecolor=PANEL,edgecolor='#2a3040',labelcolor=FG,fontsize=7,loc='upper center',ncol=4)
ax=axs[2]; xb=np.arange(len(bz))
for i,lv in enumerate(L):
  ax.bar(xb+(i-1.5)*w,[float(b[(lv,n)]['sim_ticks_per_s']) for n in bz],w,color=COL[lv],label=f'{lv} sim ticks/s')
  ax.plot(xb+(i-1.5)*w,[float(b[(lv,n)]['fps']) for n in bz],'D',color=COL[lv],ms=6,mec='white')
ax.set_xticks(xb); ax.set_xticklabels([f'{n:,}' for n in bz]); ax.set_yscale('log'); ax.grid(True,axis='y',alpha=.5)
ax.set_title('Browser: sim ticks/s (bars), fps (diamonds)\nheadless Chrome, NO GPU (SwiftShader)',color=FG,fontsize=10); ax.set_xlabel('particles'); ax.legend(facecolor=PANEL,edgecolor='#2a3040',labelcolor=FG,fontsize=8)
fig.suptitle('FIDELITY HIGH / MEDIUM / LOW / LOWEST (D-039, cap 100,000 D-040). Multiplex Full fidelity per-sim ticks/s: '+' · '.join(f"{lv} {mp[lv]}" for lv in L),color=FG,fontsize=12)
fig.tight_layout(rect=(0,0,1,0.93)); fig.savefig(f'{D}/fidelity-bench.png',dpi=130)
# markdown
P=json.load(open(f'{F}/presets4.json')); keys=list(P['LOWEST'].keys())
o=['# FIDELITY bench (D-039: 4 levels; D-040: particle cap 100,000)','','Box: 8 vCPU Xeon, Node 22, NO GPU. Bench world TIDAL_BLOOM.','','## Levels','',
'| Slider | '+' | '.join(L)+' |','|---|'+'---|'*4]
for k in keys: o.append(f'| {k} | '+' | '.join(str(P[lv].get(k)) for lv in L)+' |')
o.append('| multiplex LAW COUNT | 136 | 136 | 48 | 16 |')
o+=['','## Solver (bench/solver-tps.mjs --speed high|medium|low|lowest): median of 3 fresh-process runs, 30 timed ticks (10 at 50k) after 3 warm-up','',
'| Particles | Preset | ticks/s | × vs HIGH | runs (ms/tick) | alive | species | bonded % @30 | NaN energy | NaN repairs | Node RSS MB | heap MB | buffer MB |','|---|---|---|---|---|---|---|---|---|---|---|---|---|']
for n in sz:
  for lv in L:
    r=s[(lv,n)]; g=float(r['ticks_per_s'])/float(s[('HIGH',n)]['ticks_per_s'])
    o.append(f"| {n:,} | {lv} | {r['ticks_per_s']} | {g:.2f}× | {r['runs_ms']} | {r['alive']} | {r['species']} | {r['bonded_pct']}{' (@10)' if n==50000 else ''} | {r['nan_energy']} | {r['nan_repairs']} | {r['rss_mb']} | {r['heap_mb']} | {r['buffer_mb']} |")
o+=['','## Speed-up vs HIGH (solver)','','| Particles | '+' | '.join(L)+' |','|---|'+'---|'*4]
for n in sz: o.append(f'| {n:,} | '+' | '.join(f"{float(s[(lv,n)]['ticks_per_s'])/float(s[('HIGH',n)]['ticks_per_s']):.2f}×" for lv in L)+' |')
o+=['','## Bonded % of alive (solver world): after 30 ticks (10 at 50k) / after 150 ticks','','| Particles | '+' | '.join(L)+' |','|---|'+'---|'*4]
for n in sz: o.append(f'| {n:,} | '+' | '.join(f"{s[(lv,n)]['bonded_pct']} / {100*H[(lv,n)]['bonded']/H[(lv,n)]['alive']:.1f}" for lv in L)+' |')
o+=['','150-tick runs: every level and size kept all particles alive and all 5 species, 0 NaN energy, 0 NaN repairs (health-150ticks.csv).','',
'## Browser: headless Chrome, NO GPU (SwiftShader software rendering), 1280×800, DPR 1','',
'Live app, boot world then INITIAL_POP = N, sim:restart. Warm-up 2.5 s then 6 s measured (8 s / 10 s at 50k). page ready = navigation to launch screen. respawn → first full tick = sim:restart until the first physics tick that reports ≥ 99% of N (this is the boot cost of a big world). Chrome RSS = all headless Chrome processes. Worker heap is not readable from a headless worker (n/a).','',
'| Particles | Preset | seen | page ready ms | respawn → first full tick ms | fps | frame ms p50 / p95 | sim ticks/s | × sim vs HIGH | main JS heap MB | Chrome RSS MB | alive | species | bonded % |','|---|---|---|---|---|---|---|---|---|---|---|---|---|---|']
for n in bz:
  for lv in L:
    r=b[(lv,n)]; g=float(r['sim_ticks_per_s'])/max(1e-9,float(b[('HIGH',n)]['sim_ticks_per_s']))
    o.append(f"| {n:,} | {lv} | {r['particles_seen']} | {r['page_ready_ms']} | {r['respawn_to_first_full_tick_ms']} | {r['fps']} | {r['frame_ms_p50']} / {r['frame_ms_p95']} | {r['sim_ticks_per_s']} | {g:.2f}× | {r['js_heap_main_mb']} | {r['chrome_rss_mb']} | {r['alive']} | {r['species']} | {r['bonded_pct']} |")
o+=['','## Multiplex Full fidelity (20 sims × 2,500, worker pool 7), per-sim ticks/s','','| Preset | laws | ticks/s per sim (min) | × vs HIGH | frame p95 ms |','|---|---|---|---|---|']
for r in M: o.append(f"| {r['preset']} | {r['laws']} | {r['tps_per_sim']} ({r['tps_min']}) | {float(r['tps_per_sim'])/mp['HIGH']:.1f}× | {r['frame_p95_ms']} |")
o+=['',open(f'{F}/cap_section.md').read()]
open(f'{D}/README.md','w').write('\n'.join(o)+'\n'); print('ok')
