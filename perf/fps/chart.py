import csv, statistics as st, sys
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
rows = list(csv.DictReader(open('/workspace/out/fps-thresholds/fps-raw.csv')))
thr = [float(x) for x in sys.argv[1].split(',')] if len(sys.argv) > 1 else []
fig, ax = plt.subplots(figsize=(10, 6), dpi=130)
for lvl, col, mk in [('HIGH', '#d33', 'o'), ('LOWEST', '#36c', 's')]:
    by = {}
    for r in rows:
        if r['level'] == lvl: by.setdefault(int(r['size']), []).append(float(r['fps']))
    xs = sorted(by); ys = [st.median(by[x]) for x in xs]
    if not xs: continue
    ax.plot(xs, ys, marker=mk, color=col, lw=2 if lvl == 'HIGH' else 1.2, ls='-' if lvl == 'HIGH' else '--', label=f'{lvl} fidelity (median of 2)')
    for x in xs:
        ax.scatter([x] * len(by[x]), by[x], color=col, s=10, alpha=0.35)
for y in (60, 30, 20, 10):
    ax.axhline(y, color='#888', lw=0.8, ls=':')
    ax.text(52000, y + 0.6, f'{y} fps', color='#666', fontsize=9, ha='right')
labels = ['<60', '<30', '<20', '<10']
for i, x in enumerate(thr):
    ax.axvline(x, color='#d33', lw=0.8, alpha=0.5)
    ax.text(x * 1.03, 63 - i * 4, f'{labels[i]} fps @ ~{int(x):,}', color='#a22', fontsize=9)
ax.set_xscale('log')
ax.set_xticks([1000, 2500, 5000, 10000, 20000, 50000]); ax.set_xticklabels(['1k', '2.5k', '5k', '10k', '20k', '50k'])
ax.set_ylim(0, 68)
ax.set_xlabel('particles (INITIAL_POP, log scale)'); ax.set_ylabel('browser fps (10 s after 5 s warm-up)')
ax.set_title('VEPA browser fps vs particle count — HEAD, CPU engine, LIVE EDITS off\nheadless Chromium, NO GPU (SwiftShader), 1280×800, 8 vCPU box')
ax.grid(alpha=0.25); ax.legend(loc='lower left')
fig.tight_layout(); fig.savefig('/workspace/out/fps-thresholds/fps-vs-particles.png')
print('ok')
