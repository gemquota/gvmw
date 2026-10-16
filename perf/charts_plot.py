import csv, collections, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
D='/workspace/out/speed-charts'
BG='#0b0d14'; PANEL='#11141d'; FG='#d6dae4'; DIM='#7d8597'; C25='#4aa3ff'; C10='#ff5a5a'; GOLD='#f5c542'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'text.color':FG,'axes.labelcolor':FG,'xtick.color':DIM,'ytick.color':DIM,
  'axes.edgecolor':'#2a3040','figure.facecolor':BG,'axes.facecolor':PANEL,'grid.color':'#232838','savefig.facecolor':BG})
META = {  # key: (title, default, FAST, log x, top-end label)
 'PAIRWISE_BUDGET':('Neighbour limit / particle',96,48,True,None),
 'SPEED_PAIR_BUDGET':('Pair budget / particle / tick',512,20,True,'OFF'),
 'SPEED_MID_RANGE':('Mid range (distance)',200,120,False,None),
 'SPEED_NEAR_RANGE':('Near / contact range',30,30,False,None),
 'SPEED_SYMBIOSIS_RANGE':('Symbiosis & parasite range',600,30,True,'ANY'),
 'SPEED_SOCIAL_EVERY':('Social & info laws every N ticks',1,2,False,None),
 'SPEED_EXPENSIVE_EVERY':('Expensive laws every N ticks (new)',1,None,False,None),
}
rows=list(csv.DictReader(open(f'{D}/individual-raw.csv')))
data=collections.defaultdict(lambda: collections.defaultdict(dict))
for r in rows: data[r['slider']][int(r['size'])][float(r['value'])]=r
lc=list(csv.DictReader(open(f'{D}/lawcount-raw.csv'))) if __import__('os').path.exists(f'{D}/lawcount-raw.csv') else []
keys=[k for k in META if k in data]
import statistics
BASE={size: statistics.median(float(data[k][size][META[k][1]]['ms_per_tick']) for k in keys if META[k][1] in data[k][size]) for size in (2500,10000)}
n=len(keys)+(1 if lc else 0); cols=4; rws=(n+cols-1)//cols
fig,axes=plt.subplots(rws,cols,figsize=(4.2*cols,3.3*rws)); axes=axes.flatten()
for ax,k in zip(axes,keys):
    t,dflt,fast,logx,top=META[k]
    for size,col in ((2500,C25),(10000,C10)):
        pts=data[k][size]
        if dflt not in pts: continue
        base=BASE[size]
        xs=sorted(pts); ys=[base/float(pts[x]['ms_per_tick']) for x in xs]
        ax.plot(xs,ys,'o-',color=col,lw=2,ms=4,label=f'{size:,} particles')
    ax.axhline(1,color=DIM,lw=0.8)
    ax.axvline(dflt,color=FG,ls='--',lw=1); ax.text(dflt,ax.get_ylim()[1],' default',color=FG,va='top',fontsize=8)
    if fast is not None and fast!=dflt:
        ax.axvline(fast,color=GOLD,ls=':',lw=1.5); ax.text(fast,ax.get_ylim()[1]*0.9,' FAST',color=GOLD,va='top',fontsize=8)
    if logx: ax.set_xscale('log')
    ax.set_title(t,color=FG,fontsize=11); ax.grid(True,alpha=0.6); ax.set_xlabel('slider value'+(f' (top end = {top})' if top else '')+(' · log scale' if logx else ''),fontsize=8)
    ax.set_ylabel('speed-up vs default (×)',fontsize=8)
i=len(keys)
if lc:
    ax=axes[i]; i+=1
    pts={int(r['law_count']):float(r['tps_per_sim']) for r in lc}
    base=pts[136]; xs=sorted(pts)
    ax.plot(xs,[pts[x]/base for x in xs],'o-',color='#b48cff',lw=2,ms=4,label='multiplex Full fidelity (per sim)')
    ax.axhline(1,color=DIM,lw=0.8); ax.axvline(136,color=FG,ls='--',lw=1); ax.text(136,ax.get_ylim()[1],'default ',color=FG,va='top',ha='right',fontsize=8)
    ax.axvline(16,color=GOLD,ls=':',lw=1.5); ax.text(16,ax.get_ylim()[1]*0.9,' 16 = light set',color=GOLD,va='top',fontsize=8)
    ax.set_title('Multiplex LAW COUNT (20 sims × 2,500)',color=FG,fontsize=11); ax.grid(True,alpha=0.6); ax.set_xlabel('laws kept (1–136)',fontsize=8); ax.set_ylabel('speed-up vs 136 (×)',fontsize=8)
    ax.legend(fontsize=8,facecolor=PANEL,edgecolor='#2a3040',labelcolor=FG)
for ax in axes[i:]: ax.axis('off')
axes[0].legend(fontsize=8,facecolor=PANEL,edgecolor='#2a3040',labelcolor=FG)
fig.suptitle('Speed sliders one at a time: speed-up vs default (higher = faster; bench:solver TIDAL_BLOOM, 1 run per point; baseline = median of the 7 default runs)',color=FG,fontsize=13)
fig.tight_layout(rect=(0,0,1,0.95)); fig.savefig(f'{D}/individual.png',dpi=130)
print('individual ok')
# cumulative
import os
if os.path.exists(f'{D}/cumulative-raw.csv'):
    cr=list(csv.DictReader(open(f'{D}/cumulative-raw.csv')))
    stages=[]; [stages.append(r['stage']) for r in cr if r['stage'] not in stages]
    fig,ax=plt.subplots(figsize=(16,6.8)); ax2=ax.twinx()
    import numpy as np
    x=np.arange(len(stages)); wdt=0.38
    for off,size,col in ((-wdt/2,2500,C25),(wdt/2,10000,C10)):
        m={r['stage']:r for r in cr if int(r['size'])==size}
        base=float(m[stages[0]]['ms_per_tick'])
        sp=[base/float(m[s]['ms_per_tick']) for s in stages]
        b=ax.bar(x+off,sp,wdt,color=col,alpha=0.85,label=f'speed-up, {size:,} particles')
        for xi,v in zip(x+off,sp): ax.text(xi,v+0.05,f'{v:.1f}×',ha='center',fontsize=8,color=FG)
        ax2.plot(x,[float(m[s]['bonded_pct']) for s in stages],'s--',color=col,lw=1.5,ms=5,label=f'bonded %, {size:,}')
    import textwrap
    ax.set_xticks(x); ax.set_xticklabels([textwrap.fill(s,13) for s in stages],fontsize=8)
    agg=next((i for i,s in enumerate(stages) if s.startswith('aggressive')),None)
    if agg is not None:
        ax.axvspan(agg-0.5,len(stages)-0.5,color='#ff5a5a',alpha=0.06)
        ax.text(agg-0.4,ax.get_ylim()[1]*0.97,'aggressive values →',color=GOLD,fontsize=9,va='top')
        ax.text(0.6,ax.get_ylim()[1]*0.97,'FAST values, stacked →',color=GOLD,fontsize=9,va='top')
    ax.set_ylabel('cumulative speed-up vs defaults (×)'); ax2.set_ylabel('particles in a bond at the end (%)',color=DIM)
    ax2.tick_params(colors=DIM); ax.grid(True,axis='y',alpha=0.6)
    h1,l1=ax.get_legend_handles_labels(); h2,l2=ax2.get_legend_handles_labels()
    ax.legend(h1+h2,l1+l2,fontsize=8,facecolor=PANEL,edgecolor='#2a3040',labelcolor=FG,loc='center left')
    ax.set_title('Sliders stacked one after another (biggest gain first): bars = speed-up, dashed = bonded % (behaviour cost)',color=FG,fontsize=12)
    fig.tight_layout(); fig.savefig(f'{D}/cumulative.png',dpi=130); print('cumulative ok')
