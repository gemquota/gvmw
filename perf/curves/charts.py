import csv, json, os, matplotlib, numpy as np
matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, NullFormatter
D='/workspace/out/fidelity-curves'
BG='#0b0d14'; PANEL='#11141d'; FG='#e4e7ee'; DIM='#9aa2b3'
COL={'HIGH':'#4aa3ff','MEDIUM':'#f5c542','LOW':'#ff9a3c','LOWEST':'#ff5a7a'}
MK={'HIGH':'o','MEDIUM':'s','LOW':'^','LOWEST':'D'}
L=['HIGH','MEDIUM','LOW','LOWEST']
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':14,'axes.titlesize':18,'axes.labelsize':15,'xtick.labelsize':13,'ytick.labelsize':13,'legend.fontsize':14,
  'text.color':FG,'axes.labelcolor':FG,'xtick.color':DIM,'ytick.color':DIM,'axes.edgecolor':'#2f3547','figure.facecolor':BG,'axes.facecolor':PANEL,'grid.color':'#2a3042','savefig.facecolor':BG})
kfmt=FuncFormatter(lambda v,_: f'{v/1000:g}k' if v>=1000 else f'{v:g}')
def rd(f): return list(csv.DictReader(open(f'{D}/{f}'))) if os.path.exists(f'{D}/{f}') else []
S={(r['preset'],int(r['size'])):r for r in rd('solver-raw.csv')}
H={(r['preset'],int(r['size'])):r for r in rd('health150-raw.csv')}
B={(r['preset'],int(r['size'])):r for r in rd('browser-raw.csv')}
sizes=lambda T: sorted({k[1] for k in T})
import glob as _g
for _f in sorted(_g.glob(f'{D}/timeline-raw/*.csv')):
  for _r in csv.DictReader(open(_f)):
    k=(_r['preset'],int(_r['size']))
    if _r['tick']=='150' and k not in H: H[k]={'bonded_pct_150':_r['bonded_pct'],'src':'timeline'}
T=['# FIDELITY curves: tables','',
 'Box: 8 vCPU Xeon, Node 22, NO GPU. Solver = `bench/solver-tps.mjs --speed <level>`, TIDAL_BLOOM bench world. Timing: 30 ticks after 3 warm-up, median of 3 fresh-process runs up to 25,000 and median of 2 at 30,000–50,000 (chosen for time; see the `runs` column in solver-raw.csv). Rows marked † are median of 2. Bonded % at 150 ticks: the tick-150 sample of the long timeline runs (500–10,000; larger sizes in phase 2). Browser: headless Chrome, NO GPU (SwiftShader software rendering), 1280×800, DPR 1. Multiplex: 20 sims × 2,500, Full fidelity, worker pool 7 (measured earlier today in the D-039 batch, not rerun).','']
import textwrap
def fig(title,sub,right=0.83):
  f,ax=plt.subplots(figsize=(1600/150,900/150),dpi=150)
  f.subplots_adjust(left=0.1,right=right,top=0.8,bottom=0.13)
  f.text(0.1,0.945,title,fontsize=18,color=FG,weight='bold'); f.text(0.1,0.905,textwrap.fill(sub,110),fontsize=12,color=DIM,va='top',linespacing=1.3)
  ax.grid(True,which='major',alpha=.8); ax.grid(True,which='minor',alpha=.3)
  return f,ax
def endlabels(ax,pts):
  # pts: list of (level, x_last, y_last); spread labels to avoid overlap (in display space)
  if not pts: return
  tr=ax.transData; inv=tr.inverted()
  disp=sorted([(tr.transform((x,y))[1],lv,x,y) for lv,x,y in pts])
  out=[]; gap=24
  for i,(yd,lv,x,y) in enumerate(disp):
    if out and yd-out[-1][0]<gap: yd=out[-1][0]+gap
    out.append((yd,lv,x,y))
  for yd,lv,x,y in out:
    xd=tr.transform((x,y))[0]
    ax.annotate(lv,xy=(x,y),xytext=(xd+12,yd),textcoords='figure pixels' if False else None,fontsize=14,color=COL[lv],weight='bold',va='center',annotation_clip=False) if False else None
    ax.text(*inv.transform((xd+10,yd)),lv,fontsize=14,color=COL[lv],weight='bold',va='center',clip_on=False)
def save(f,name): f.savefig(f'{D}/{name}',dpi=150); plt.close(f)
def table(title,head,rows,note=''):
  T.extend([f'## {title}','']+([note,''] if note else [])+['| '+' | '.join(head)+' |','|'+'---|'*len(head)]+['| '+' | '.join(map(str,r))+' |' for r in rows]+[''])
def lines(name,title,sub,data,ylabel,logx=True,logy=False,ylim=None,yfmt=None,hline=None,xs_label='particles (log scale)',tblname=None,tblfmt='{:.2f}',xlab=None):
  f,ax=fig(title,sub); pts=[]; allx=set()
  for lv in L:
    xy=[(x,y) for x,y in data.get(lv,[]) if y is not None]
    if not xy: continue
    xs,ys=zip(*xy); allx|=set(xs)
    ax.plot(xs,ys,marker=MK[lv],color=COL[lv],lw=2.6,ms=7,label=lv); pts.append((lv,xs[-1],ys[-1]))
  if logx: ax.set_xscale('log'); ax.xaxis.set_major_formatter(kfmt); ax.xaxis.set_minor_formatter(NullFormatter())
  ax.set_xticks(sorted(allx) if len(allx)<=8 else [500,1000,2500,5000,10000,25000,50000] if logx else sorted(allx))
  if logx: ax.xaxis.set_major_formatter(kfmt)
  if logy:
    from matplotlib.ticker import LogLocator
    ax.set_yscale('log'); ax.yaxis.set_major_locator(LogLocator(base=10,subs=(1,2,5))); ax.yaxis.set_minor_formatter(NullFormatter())
  if ylim: ax.set_ylim(*ylim)
  if yfmt: ax.yaxis.set_major_formatter(yfmt)
  if hline is not None: ax.axhline(hline,color=DIM,lw=1.2,ls='--')
  ax.set_xlabel(xlab or xs_label); ax.set_ylabel(ylabel)
  f.canvas.draw(); endlabels(ax,pts); save(f,name)
  xsorted=sorted(allx)
  table(tblname or title,['particles']+L,[[f'{x:,}'+('†' if x>=30000 and tblname and tblname[:2] in ('01','02','04','13') else '')]+[(tblfmt.format(dict(data[lv]).get(x)) if dict(data.get(lv,[])).get(x) is not None else '–') for lv in L] for x in xsorted])
ss=sizes(S)
tps=lambda lv,n: float(S[(lv,n)]['ticks_per_s']) if (lv,n) in S else None
# 01 speed-up
lines('01-speedup-vs-high.png','How much faster each FIDELITY level runs than HIGH','Solver ticks per second ÷ HIGH at the same particle count. Median of 3 runs (2 at 30k–50k), 8-vCPU box, no GPU.',
 {lv:[(n,tps(lv,n)/tps('HIGH',n) if tps(lv,n) and tps('HIGH',n) else None) for n in ss] for lv in L},'speed-up vs HIGH (×)',hline=1,yfmt=FuncFormatter(lambda v,_: f'{v:g}×'),tblname='01 Speed-up vs HIGH (×)')
# 02 raw
lines('02-solver-ticks-per-second.png','Raw solver speed by particle count','Simulation ticks per second (log scale). Higher is faster. Median of 3 runs (2 at 30k–50k).',
 {lv:[(n,tps(lv,n)) for n in ss] for lv in L},'ticks per second (log scale)',logy=True,yfmt=FuncFormatter(lambda v,_: f'{v:g}'),tblname='02 Solver ticks/s')
# 03 / 04 bonded
hs=sizes(H)
lines('03-bonded-after-150-ticks.png','How much structure forms: bonded particles after 150 ticks','Share of living particles with at least one bond after 150 ticks (the tick-150 sample of the long runs). HIGH = the reference. Sizes above 10,000 come in phase 2.',
 {lv:[(n,float(H[(lv,n)]['bonded_pct_150']) if (lv,n) in H else None) for n in hs] for lv in L},'bonded % of living particles',ylim=(0,103),tblname='03 Bonded % after 150 ticks',tblfmt='{:.1f}')
lines('04-bonded-after-30-ticks.png','Early structure: bonded particles after 30 ticks','Same measure after only 30 ticks (end of the timing runs). Lower levels bond more slowly at first.',
 {lv:[(n,float(S[(lv,n)]['bonded_pct_30']) if (lv,n) in S else None) for n in ss] for lv in L},'bonded % of living particles',ylim=(0,103),tblname='04 Bonded % after 30 ticks',tblfmt='{:.1f}')
# browser
bs=sizes(B)
bv=lambda k: {lv:[(n,float(B[(lv,n)][k]) if (lv,n) in B else None) for n in bs] for lv in L}
lines('05-browser-sim-ticks.png','In the browser: simulation ticks per second','Live app, headless Chrome with NO GPU (software rendering), 1280×800. Physics runs in a worker.',
 bv('sim_ticks_per_s'),'sim ticks per second (log scale)',logy=True,yfmt=FuncFormatter(lambda v,_: f'{v:g}'),tblname='05 Browser sim ticks/s (headless Chrome, NO GPU)')
lines('06-browser-fps.png','In the browser: frames per second','Same runs. Drawing is software-rendered here (NO GPU), so fps mostly reflects particle count, not FIDELITY.',
 bv('fps'),'frames per second',ylim=(0,65),tblname='06 Browser fps (headless Chrome, NO GPU)',tblfmt='{:.1f}')
lines('07-browser-frame-p95.png','In the browser: slow frames (95th percentile frame time)','95% of frames took this long or less. Lower is smoother. Headless Chrome, NO GPU.',
 bv('frame_ms_p95'),'frame time p95 (ms)',tblname='07 Browser frame time p95 ms (headless Chrome, NO GPU)',tblfmt='{:.1f}')
lines('08-browser-js-heap.png','In the browser: main-thread JS heap','performance.memory.usedJSHeapSize on the page (the particle SharedArrayBuffer is not counted here). Headless Chrome, NO GPU.',
 bv('js_heap_main_mb'),'JS heap (MB)',tblname='08 Browser main JS heap MB',tblfmt='{:.1f}')
# memory
lines('09-bench-memory-rss.png','Memory of the solver bench process by particle count','Resident memory (RSS) of the Node bench child at the end of the timed run (buffers are allocated once, so close to the peak). Includes Node itself; jumps of ±30 MB are garbage-collector timing, not the level.',
 {lv:[(n,float(S[(lv,n)]['end_rss_mb']) if (lv,n) in S else None) for n in ss] for lv in L},'RSS (MB)',tblname='09 Bench child RSS MB at end of timed run',tblfmt='{:.0f}')
lines('10-bench-heap.png','JS heap of the solver bench by particle count','V8 heap used at the end of the timed run (MB). The particle buffer (400 B per particle slot) is outside the heap.',
 {lv:[(n,float(S[(lv,n)]['end_heap_mb']) if (lv,n) in S else None) for n in ss] for lv in L},'heap used (MB)',tblname='10 Bench child heap MB at end of timed run',tblfmt='{:.1f}')
# 11 multiplex bars
t=open('/workspace/perf/fid/mpx-fid4.json').read(); md=json.loads(t[t.index('{'):]); M={r['case'].split()[-1]:r for r in md['results']}
f,ax=fig('Multiplex (20 sims × 2,500): ticks per second per sim','Full fidelity preset. LOW also cuts LAW COUNT to 48 and LOWEST to 16, which is most of the gain. Error bar = slowest sim.',right=0.95)
v=[M[lv]['tpsPerSim'] for lv in L]; mn=[M[lv]['tpsMin'] for lv in L]
ax.bar(L,v,color=[COL[lv] for lv in L],width=0.6)
ax.errorbar(L,v,yerr=[np.array(v)-np.array(mn),[0]*4],fmt='none',ecolor=FG,capsize=8,lw=1.5)
for i,(a,b) in enumerate(zip(v,mn)): ax.text(i,a+0.5,f'{a:g}/s  ({a/v[0]:.1f}×)',ha='center',fontsize=14,color=FG)
ax.set_ylabel('ticks per second per sim'); ax.grid(True,axis='x',alpha=0); ax.set_ylim(0,max(v)*1.18)
save(f,'11-multiplex-per-sim.png')
table('11 Multiplex Full fidelity per-sim ticks/s',['level','law count','ticks/s per sim','slowest sim','× vs HIGH','frame p95 ms'],[[lv,{'HIGH':136,'MEDIUM':136,'LOW':48,'LOWEST':16}[lv],M[lv]['tpsPerSim'],M[lv]['tpsMin'],f"{M[lv]['tpsPerSim']/v[0]:.1f}×",M[lv]['frameP95Ms']] for lv in L])
# 12 trade-off scatter
f,ax=fig('Trade-off: speed gained vs structure kept','Each point = one level at one particle count. x = speed-up vs HIGH, y = bonded % after 150 ticks. Up and right is best.')
rows=[]
for lv in L:
  xy=[(tps(lv,n)/tps('HIGH',n),float(H[(lv,n)]['bonded_pct_150']),n) for n in ss if (lv,n) in H and tps(lv,n)]
  if not xy: continue
  xs,ys,ns=zip(*xy); ax.scatter(xs,ys,s=[40+60*np.log10(n/400) for n in ns],color=COL[lv],label=lv,alpha=.9,edgecolors='white',linewidths=.6)
  rows+= [[lv,f'{n:,}',f'{x:.2f}×',f'{y:.1f}'] for x,y,n in xy]
ax.set_xscale('log'); ax.xaxis.set_major_formatter(FuncFormatter(lambda v,_: f'{v:g}×')); ax.set_xticks([1,2,3,5,8]); ax.set_ylim(0,103)
ax.set_xlabel('speed-up vs HIGH (log scale)'); ax.set_ylabel('bonded % after 150 ticks')
ax.legend(loc='upper left',bbox_to_anchor=(1.01,1),frameon=False,title='dot size = particles',title_fontsize=12,labelcolor=FG)
save(f,'12-tradeoff-speed-vs-bonding.png')
table('12 Trade-off: speed-up vs bonded % after 150 ticks',['level','particles','speed-up','bonded % @150'],rows)
# 13 cost per particle
lines('13-cost-per-1000-particles.png','How the cost per particle grows with population','Milliseconds per tick for every 1,000 particles. It falls above 2,500 because ADAPTIVE QUALITY (on by default) shrinks the neighbour limit as the population grows (×√(2,500 ÷ particles)).',
 {lv:[(n,1000*float(S[(lv,n)]['ms_per_tick_median'])/n if (lv,n) in S else None) for n in ss] for lv in L},'ms per tick per 1,000 particles (log)',logy=True,yfmt=FuncFormatter(lambda v,_: f'{v:g}'),tblname='13 ms per tick per 1,000 particles')
open(f'{D}/TABLES.md','w').write('\n'.join(T)+'\n'); print('charts ok')

# ---------------- timelines (one run per level and size, sampled 50..2000 ticks) ----------------
import glob
TLR=[r for f in sorted(glob.glob(f'{D}/timeline-raw/*.csv')) for r in csv.DictReader(open(f))]
TLd={}
for r in TLR: TLd.setdefault((r['preset'],int(r['size'])),[]).append(r)
tsz=sorted({k[1] for k in TLd})
TLNOTE=('Timelines: ONE run per level and size, 2,000 ticks, sampled at 50, 100, …, 2,000. The 32 runs ran 8 at a time on the 8-vCPU box, so their ticks/s '
        'is lower than the quiet speed curves (01, 02); read them for the trend over time. The bench world does not add offspring to the buffer, so births = offspring '
        'the solver requested (not spawned) and deaths = start count − alive.')
T.extend(['## Timelines','',TLNOTE,''])
def tl(lv,n,k,fn=float): return [(int(r['tick']),fn(r[k])) for r in TLd.get((lv,n),[])]
def tlines(name,title,sub,key,ylabel,n,ylim=None,logy=False,fmt='{:.1f}',tbl=None):
  data={lv:tl(lv,n,key) for lv in L}
  if not any(data.values()): return
  lines(name,title,sub,data,ylabel,logx=False,logy=logy,ylim=ylim,tblname=tbl,tblfmt=fmt,xlab='simulation tick')
for i,n in enumerate(tsz):
  tlines(f'20-bonded-over-time-{n:05d}.png',f'Bonded % over 2,000 ticks at {n:,} particles','Share of living particles with at least one bond, sampled within one run per level. HIGH = the reference.',
         'bonded_pct','bonded % of living particles',n,ylim=(0,103),tbl=f'20 Bonded % over time, {n:,} particles')
for i,n in enumerate(tsz):
  tlines(f'22-speed-over-time-{n:05d}.png',f'Speed over 2,000 ticks at {n:,} particles','Ticks per second in each sampling window (log scale). Ran 8 runs at once on 8 vCPU: compare levels, not with the quiet curves.',
         'window_ticks_per_s','ticks per second in window (log)',n,logy=True,fmt='{:.2f}',tbl=f'22 Ticks/s per window over time, {n:,} particles')
  tb=[[lv]+[TLd[(lv,n)][-1][k] for k in ('tick','cum_ticks_per_s')] for lv in L if (lv,n) in TLd]
  table(f'22b Cumulative ticks/s at the last sample, {n:,} particles',['level','ticks run','cumulative ticks/s'],tb)
# alive / species / births / energy summary
rows=[]
for n in tsz:
  for lv in L:
    rs=TLd.get((lv,n));
    if not rs: continue
    rows.append([f'{n:,}',lv,rs[-1]['tick'],min(int(r['alive']) for r in rs),rs[-1]['alive'],min(int(r['species']) for r in rs),rs[-1]['births_cum'],rs[-1]['deaths_cum'],rs[0]['mean_energy'],rs[-1]['mean_energy'],max(int(r['nan_repairs']) for r in rs),max(int(r['nan_energy']) for r in rs)])
table('21 Alive, species, births, deaths, energy over the timeline runs',['particles','level','last tick','min alive','alive at end','min species','births (requested)','deaths','mean energy @50','mean energy @end','NaN repairs','NaN energy'],rows)
for key,ttl,yl,nm in [('alive','Living particles over 2,000 ticks','living particles (% of start)','21a-alive-over-time.png'),('species','Living species over 2,000 ticks','species alive','21b-species-over-time.png'),('mean_energy','Mean particle energy over 2,000 ticks','mean energy','21c-energy-over-time.png')]:
  f,ax=fig(ttl,'Every level at every size from 500 to 10,000 particles: line colour = level, line style = size (solid 10k, dashed 5k, dotted 2.5k, faint = smaller).')
  sty={10000:('-',1),5000:('--',1),2500:(':',1)}
  for n in tsz:
    ls,al=sty.get(n,('-',0.35))
    for lv in L:
      rs=TLd.get((lv,n));
      if not rs: continue
      y=[float(r[key])*(100/n if key=='alive' else 1) for r in rs]; ax.plot([int(r['tick']) for r in rs],y,ls,color=COL[lv],alpha=al,lw=2.2)
  from matplotlib.lines import Line2D
  ax.legend([Line2D([0],[0],color=COL[lv],lw=3) for lv in L]+[Line2D([0],[0],color=DIM,ls=s,lw=2) for s in ('-','--',':')],L+['10k','5k','2.5k'],loc='upper left',bbox_to_anchor=(1.01,1),frameon=False,labelcolor=FG)
  ax.set_xlabel('simulation tick'); ax.set_ylabel(yl)
  if key=='species': ax.set_ylim(0,6)
  if key=='alive': ax.set_ylim(0,105)
  save(f,nm)
open(f'{D}/TABLES.md','w').write('\n'.join(T)+'\n'); print('timeline charts ok', len(TLd))
