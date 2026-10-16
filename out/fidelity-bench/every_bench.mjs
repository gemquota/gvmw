import { chromium } from '/workspace/vepa/node_modules/playwright/index.mjs';
const b = await chromium.launch({ args: ['--enable-unsafe-swiftshader'] });
const rows = [['size','screen_dpr','RENDER_EVERY','canvas','fps','frame_ms_p50','frame_ms_p95','sim_ticks_per_s','gain_fps_vs_1']];
const base = {};
for (const size of [2500, 10000]) for (const v of [1, 2, 3]) {
  const p = await b.newPage({ viewport: { width: 1280, height: 800 }, deviceScaleFactor: 1 });
  await p.goto('http://127.0.0.1:4190/'); await p.waitForTimeout(2500);
  await p.click('.launch-primary').catch(() => {}); await p.waitForTimeout(1200);
  await p.click('#vepa-debug-hide', { timeout: 1500 }).catch(() => {});
  await p.evaluate(({ size, v }) => { const bus = window.__bus; bus.emit('world:paramChanged', { key: 'INITIAL_POP', value: size }); bus.emit('world:paramChanged', { key: 'RENDER_EVERY', value: v }); bus.emit('sim:restart', {}); window.__t = 0; bus.on('physics:tick', () => window.__t++); }, { size, v });
  await p.waitForTimeout(2500);
  const r = await p.evaluate(async () => { const d = []; const t0 = performance.now(); let prev = t0; const k0 = window.__t; await new Promise((res) => { const f = (t) => { d.push(t - prev); prev = t; if (t - t0 < 5000) requestAnimationFrame(f); else res(); }; requestAnimationFrame(f); }); const el = (performance.now() - t0) / 1000; d.sort((a, b) => a - b); const c = document.querySelector('canvas'); return { fps: d.length / el, p50: d[d.length >> 1], p95: d[Math.floor(d.length * 0.95)], tps: (window.__t - k0) / el, canvas: `${c.width}x${c.height}` }; });
  if (v === 1) base[size] = r.fps;
  rows.push([size, 1, v, r.canvas, r.fps.toFixed(1), r.p50.toFixed(1), r.p95.toFixed(1), r.tps.toFixed(2), (r.fps / base[size]).toFixed(2)]);
  console.log(rows.at(-1).join(','));
  await p.close();
}
await b.close();
(await import('node:fs')).writeFileSync('/workspace/out/fidelity-bench/render-every-raw.csv', rows.map((r) => r.join(',')).join('\n') + '\n');
