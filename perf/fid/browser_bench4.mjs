// D-038 headless Chrome (NO GPU: SwiftShader software rendering) bench of FIDELITY presets.
import { chromium } from '/workspace/vepa/node_modules/playwright/index.mjs';
import { execSync } from 'node:child_process';
import fs from 'node:fs';
const K = { STRIDE: 100, DEAD: 52, MASS: 6, SP: 7, B1: 59, E: 50 };
const PRESETS = JSON.parse(fs.readFileSync(process.argv[2], 'utf8')); // {HIGH:{..},MEDIUM:{..},LOW:{..}}
const SIZES = (process.argv[3] || '100,500,2500,10000').split(',').map(Number);
const OUT = process.argv[4] || '/workspace/out/fidelity-bench/browser-raw.csv';
const MEASURE_MS = 6000, WARM_MS = 2500;
const rows = [['preset','size','particles_seen','page_ready_ms','respawn_to_first_full_tick_ms','fps','frame_ms_p50','frame_ms_p95','sim_ticks_per_s','js_heap_main_mb','worker_heap_mb','chrome_rss_mb','alive','species','bonded_pct','note']];
const chromeRss = () => { try { return Math.round(execSync("ps -eo rss,args | grep -E 'headless_shell|chrome' | grep -v grep | awk '{s+=$1} END {print s}'").toString().trim() / 1024); } catch { return null; } };
const b = await chromium.launch({ args: ['--enable-unsafe-swiftshader', '--js-flags=--expose-gc', '--enable-precise-memory-info'] });
for (const size of SIZES) for (const [lv, preset] of Object.entries(PRESETS)) {
  const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
  const tg = Date.now(); await p.goto('http://127.0.0.1:4190/'); await p.waitForSelector('.launch-primary', { timeout: 30000 }); const ready = Date.now() - tg; await p.waitForTimeout(1500);
  const WARM = size >= 50000 ? 8000 : WARM_MS, MEAS = size >= 50000 ? 10000 : MEASURE_MS;
  await p.click('.launch-primary').catch(() => {}); await p.waitForTimeout(1200);
  await p.click('#vepa-debug-hide', { timeout: 1500 }).catch(() => {});
  const respawn = await p.evaluate(({ size, preset }) => new Promise((res) => {
    const bus = window.__bus;
    bus.emit('world:paramChanged', { key: 'INITIAL_POP', value: size });
    for (const [k, v] of Object.entries(preset)) bus.emit('world:paramChanged', { key: k, value: v });
    window.__fb = { ticks: 0, last: null }; let first = true; const t = performance.now();
    bus.on('physics:tick', (e) => { window.__fb.ticks++; window.__fb.last = e; if (first && e.particleCount >= size * 0.99) { first = false; res(performance.now() - t); } });
    bus.emit('sim:restart', {});
    setTimeout(() => res(-1), 90000);
  }), { size, preset });
  await p.waitForTimeout(WARM);
  const m = await p.evaluate(async ({ ms, K }) => {
    const d = []; let t0 = performance.now(), prev = t0; const ticks0 = window.__fb.ticks;
    await new Promise((res) => { const f = (t) => { d.push(t - prev); prev = t; if (t - t0 < ms) requestAnimationFrame(f); else res(); }; requestAnimationFrame(f); });
    const el = performance.now() - t0; const ticks = window.__fb.ticks - ticks0;
    d.sort((a, b) => a - b); const q = (x) => d[Math.min(d.length - 1, Math.floor(x * d.length))];
    const e = window.__fb.last || {}; let alive = 0, bonded = 0; const sp = new Set();
    if (e.buffer) { const v = new Float32Array(e.buffer); for (let i = 0; i < e.particleCount; i++) { const o = i * K.STRIDE; if (v[o + K.DEAD] < 0.5 && v[o + K.MASS] > 0) { alive++; sp.add(v[o + K.SP]); if (v[o + K.B1] >= 0) bonded++; } } }
    return { fps: d.length / (el / 1000), p50: q(0.5), p95: q(0.95), tps: ticks / (el / 1000), heap: performance.memory ? performance.memory.usedJSHeapSize / 1048576 : null, pc: e.particleCount, alive, species: sp.size, bonded };
  }, { ms: MEAS, K });
  let wheap = null;
  for (const w of p.workers()) { try { const h = await w.evaluate(() => (self.performance && performance.memory ? performance.memory.usedJSHeapSize / 1048576 : null)); if (h != null) wheap = (wheap || 0) + h; } catch {} }
  const rss = chromeRss();
  rows.push([lv, size, m.pc, ready, Math.round(respawn), m.fps.toFixed(1), m.p50.toFixed(1), m.p95.toFixed(1), m.tps.toFixed(2), m.heap?.toFixed(1) ?? '', wheap?.toFixed(1) ?? 'n/a', rss ?? '', m.alive, m.species, m.alive ? (100 * m.bonded / m.alive).toFixed(1) : '', 'headless Chrome, NO GPU (SwiftShader), 1280x800']);
  console.log(rows[rows.length - 1].join(','));
  await p.close();
}
await b.close();
fs.writeFileSync(OUT, rows.map((r) => r.join(',')).join('\n') + '\n');
