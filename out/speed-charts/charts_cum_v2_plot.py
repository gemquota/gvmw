import csv, collections, statistics, textwrap, numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
D='/workspace/out/speed-charts'
BG='#0b0d14'; PANEL='#11141d'; FG='#d6dae4'; DIM='#7d8597'; C25='#4aa3ff'; C10='#ff5a5a'; GOLD='#f5c542'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'text.color':FG,'axes.labelcolor':FG,'xtick.color':DIM,'ytick.color':DIM,'axes.edgecolor':'#2a3040','figure.facecolor':BG,'axes.facecolor':PANEL,'grid.color':'#232838','savefig.facecolor':BG})
R=list(csv.DictReader(open(f'{D}/cumulative-v2-raw.csv')))
stages=[]; [stages.append(r['stage']) for r in R if r['stage'] not in stages]
ms=collections.defaultdict(list); bp={}
for r in R: ms[(r['stage'],r['size'])].append(float(r['ms_per_tick'])); bp[(r['stage'],r['size'])]=float(r['bonded_pct'])
fig,ax=plt.subplots(figsize=(16,7)); ax2=ax.twinx(); x=np.arange(len(stages)); w=0.38
summary=[]
for off,size,col in ((-w/2,'2500',C25),(w/2,'10000',C10)):
    base=statistics.median(ms[(stages[0],size)])
    sp=[[base/v for v in ms[(s,size)]] for s in stages]
    med=[statistics.median(v) for v in sp]; lo=[m-min(v) for m,v in zip(med,sp)]; hi=[max(v)-m for m,v in zip(med,sp)]
    ax.bar(x+off,med,w,color=col,alpha=.85,label=f'speed-up, {int(size):,} (median of 3; bars = min–max)',yerr=[lo,hi],ecolor=FG,capsize=3)
    for xi,v in zip(x+off,med): ax.text(xi,v+0.15,f'{v:.1f}×',ha='center',fontsize=7,color=FG)
    ax2.plot(x,[bp[(s,size)] for s in stages],'s--',color=col,lw=1.4,ms=5,label=f'bonded %, {int(size):,}')
    for s,m,v in zip(stages,med,sp): summary.append((s,size,m,min(v),max(v)))
ax.set_xticks(x); ax.set_xticklabels([textwrap.fill(s,13) for s in stages],fontsize=8)
agg=next(i for i,s in enumerate(stages) if s.startswith('aggressive')); ax.axvspan(agg-0.5,len(stages)-0.5,color='#ff5a5a',alpha=0.06)
ax.set_ylabel('cumulative speed-up vs defaults (×)'); ax2.set_ylabel('particles in a bond after 10 ticks (%)',color=DIM); ax2.tick_params(colors=DIM); ax2.set_ylim(0,105)
ax.grid(True,axis='y',alpha=.6)
h1,l1=ax.get_legend_handles_labels(); h2,l2=ax2.get_legend_handles_labels(); ax.legend(h1+h2,l1+l2,fontsize=8,facecolor=PANEL,edgecolor='#2a3040',labelcolor=FG,loc='center left')
ax.set_title('Sliders stacked (v2): 3 interleaved repeats per point, error bars = min–max; dashed = bonded % (deterministic, no error)',color=FG,fontsize=12)
fig.tight_layout(); fig.savefig(f'{D}/cumulative-v2.png',dpi=130)
with open(f'{D}/cumulative-v2-summary.csv','w',newline='') as f:
    w_=csv.writer(f); w_.writerow(['stage','size','speedup_median','speedup_min','speedup_max']); [w_.writerow([a,b,round(c,3),round(d,3),round(e,3)]) for a,b,c,d,e in summary]
for a,b,c,d,e in summary: print(f'{a[:30]:30s} {b:>5} {c:.2f} [{d:.2f}-{e:.2f}]')
