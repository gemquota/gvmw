import csv, collections, matplotlib, numpy as np
matplotlib.use('Agg'); import matplotlib.pyplot as plt
D='/workspace/out/fidelity-bench'
BG='#0b0d14'; PANEL='#11141d'; FG='#d6dae4'; DIM='#7d8597'; COL={'HIGH':'#4aa3ff','MEDIUM':'#f5c542','LOW':'#ff5a5a'}
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'text.color':FG,'axes.labelcolor':FG,'xtick.color':DIM,'ytick.color':DIM,'axes.edgecolor':'#2a3040','figure.facecolor':BG,'axes.facecolor':PANEL,'grid.color':'#232838','savefig.facecolor':BG})
S=list(csv.DictReader(open(f'{D}/solver-raw.csv'))); B=list(csv.DictReader(open(f'{D}/browser-raw.csv'))); M=list(csv.DictReader(open(f'{D}/multiplex-raw.csv')))
sz=[100,500,2500,10000,50000]; L=['HIGH','MEDIUM','LOW']
s={(r['preset'],int(r['size'])):r for r in S}; b={(r['preset'],int(r['size'])):r for r in B}
fig,axs=plt.subplots(1,3,figsize=(17,5.6))
x=np.arange(len(sz)); w=0.27
ax=axs[0]
for i,lv in enumerate(L):
    g=[float(s[(lv,n)]['ticks_per_s'])/float(s[('HIGH',n)]['ticks_per_s']) for n in sz]
    ax.bar(x+(i-1)*w,g,w,color=COL[lv],label=lv)
    for xi,v in zip(x+(i-1)*w,g): ax.text(xi,v+0.1,f'{v:.1f}×',ha='center',fontsize=7,color=FG)
ax.set_xticks(x); ax.set_xticklabels([f'{n:,}' + ('\n(dev bench,\nabove 10k cap)' if n>10000 else '') for n in sz],fontsize=8)
ax.set_title('Solver speed-up vs HIGH (median of 3 runs)',color=FG); ax.set_ylabel('× ticks/s vs HIGH'); ax.set_xlabel('particles'); ax.grid(True,axis='y',alpha=.6); ax.legend(facecolor=PANEL,edgecolor='#2a3040',labelcolor=FG)
ax=axs[1]
for i,lv in enumerate(L):
    ax.plot(sz,[float(s[(lv,n)]['ticks_per_s']) for n in sz],'o-',color=COL[lv],lw=2,label=f'{lv} ticks/s')
    ax2=ax
ax.set_xscale('log'); ax.set_yscale('log'); ax.set_xlabel('particles (log)'); ax.set_ylabel('solver ticks/s (log)'); ax.grid(True,which='both',alpha=.4)
ax.set_title('Solver ticks/s and bonded % (dashed)',color=FG)
axb=ax.twinx()
for lv in L: axb.plot(sz,[float(s[(lv,n)]['bonded_pct']) for n in sz],'s--',color=COL[lv],lw=1,ms=4,alpha=.8)
axb.set_ylabel('bonded % after 30 ticks (10 at 50k)',color=DIM); axb.tick_params(colors=DIM); axb.set_ylim(0,105)
ax.legend(facecolor=PANEL,edgecolor='#2a3040',labelcolor=FG,fontsize=8,loc='lower left')
ax=axs[2]; bz=[100,500,2500,10000]; xb=np.arange(len(bz))
for i,lv in enumerate(L):
    ax.bar(xb+(i-1)*w,[float(b[(lv,n)]['sim_ticks_per_s']) for n in bz],w,color=COL[lv],label=f'{lv} sim ticks/s')
    ax.plot(xb,[float(b[(lv,n)]['fps']) for n in bz],'D:',color=COL[lv],ms=5,lw=1)
ax.set_xticks(xb); ax.set_xticklabels([f'{n:,}' for n in bz]); ax.set_yscale('log'); ax.grid(True,axis='y',alpha=.5)
ax.set_title('Browser: sim ticks/s (bars), fps (dotted)\nheadless Chrome, NO GPU (SwiftShader)',color=FG,fontsize=10); ax.set_xlabel('particles requested'); ax.legend(facecolor=PANEL,edgecolor='#2a3040',labelcolor=FG,fontsize=8)
mp={r['preset']:float(r['tps_per_sim']) for r in M}
fig.suptitle(f"FIDELITY presets — multiplex Full fidelity per-sim ticks/s: HIGH {mp['HIGH']} · MEDIUM {mp['MEDIUM']} · LOW {mp['LOW']} (LOW also LAW COUNT 16)",color=FG,fontsize=12)
fig.tight_layout(rect=(0,0,1,0.93)); fig.savefig(f'{D}/fidelity-bench.png',dpi=130)
# markdown
o=['# FIDELITY bench (D-038)','',
'Box: 8 vCPU, Node 22, no GPU. Solver: `bench/solver-tps.mjs --speed high|medium|low`, TIDAL_BLOOM world, 30 ticks (10 at 50k) after 3 warm-up, median of 3 fresh-process runs. Memory columns are the Node bench process (RSS / JS heap), not the browser. Buffer = particle buffer (count × 2 slots × 100 floats × 4 B).',
'50,000 is a DEV BENCH above the app cap: the app allocates its particle buffer for MAX_PARTICLES = 10,000, so 50k cannot run in the browser; the solver itself has no cap, so the bench runs it directly.','',
'| Particles | Preset | ticks/s | × vs HIGH | runs (ms/tick) | alive | species | bonded % | NaN energy | NaN repairs | RSS MB | heap MB | buffer MB |','|---|---|---|---|---|---|---|---|---|---|---|---|---|']
for n in sz:
  for lv in L:
    r=s[(lv,n)]; g=float(r['ticks_per_s'])/float(s[('HIGH',n)]['ticks_per_s'])
    o.append(f"| {n:,}{' (dev)' if n>10000 else ''} | {lv} | {r['ticks_per_s']} | {g:.2f}× | {r['runs_ms']} | {r['alive']} | {r['species']} | {r['bonded_pct']} | {r['nan_energy']} | {r['nan_repairs']} | {r['rss_mb']} | {r['heap_mb']} | {r['buffer_mb']} |")
o+=['','## Browser (headless Chrome, NO GPU — SwiftShader software rendering; 1280×800, DPR 1)','',
'Live app (boot world, births on), 2.5 s warm-up then 6 s measured. Population grows at small sizes, so "particles seen" differs by preset. Worker heap: not readable from a headless worker (performance.memory is window-only) — n/a. Chrome RSS = all headless Chrome processes. NaN repairs are not exposed in the browser; see the solver table (all 0).','',
'| Particles | Preset | particles seen | fps | frame ms p50 / p95 | sim ticks/s | × sim vs HIGH | main JS heap MB | worker heap | Chrome RSS MB | alive | species | bonded % |','|---|---|---|---|---|---|---|---|---|---|---|---|---|']
for n in [100,500,2500,10000]:
  for lv in L:
    r=b[(lv,n)]; g=float(r['sim_ticks_per_s'])/float(b[('HIGH',n)]['sim_ticks_per_s'])
    o.append(f"| {n:,} | {lv} | {r['particles_seen']} | {r['fps']} | {r['frame_ms_p50']} / {r['frame_ms_p95']} | {r['sim_ticks_per_s']} | {g:.2f}× | {r['js_heap_main_mb']} | {r['worker_heap_mb']} | {r['chrome_rss_mb']} | {r['alive']} | {r['species']} | {r['bonded_pct']} |")
o+=['','## Multiplex Full fidelity (20 sims × 2,500, worker pool), per-sim ticks/s','','| Preset | laws | ticks/s per sim | × vs HIGH |','|---|---|---|---|']
for r in M: o.append(f"| {r['preset']} | {r['laws']} | {r['tps_per_sim']} | {float(r['tps_per_sim'])/mp['HIGH']:.1f}× |")
R=list(csv.DictReader(open(f'{D}/render-dpr-raw.csv')))
o+=['','## RENDER RESOLUTION (new, render-only) — headless Chrome, NO GPU, screen DPR 2, 1280×800 CSS','','| Particles | RENDER_MAX_DPR | fps | frame ms p50 / p95 | × fps vs 2 |','|---|---|---|---|---|']
for r in R: o.append(f"| {int(r['size']):,} | {r['RENDER_MAX_DPR']} | {r['fps']} | {r['frame_ms_p50']} / {r['frame_ms_p95']} | {r['gain_fps_vs_2']}× |")
open(f'{D}/README.md','w').write('\n'.join(o)+'\n'); print('ok')
