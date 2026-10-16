// Task A (2026-10-16): fps vs particle count, headless Chrome, NO GPU (SwiftShader), 1280x800, same method as 10 Oct browser.mjs
// usage: node fps.mjs <LEVEL> <sizes comma> <reps> <out.csv>
import { chromium } from '/workspace/vepa/node_modules/playwright/index.mjs';
import fs from 'node:fs';
import { fidelityPreset, SPEED_SLIDER_KEYS } from '/workspace/vepa/src/state/worldParams.js';
const [LEVEL = 'HIGH', SIZES_S = '1000', REPS_S = '2', OUT = '/workspace/out/fps-thresholds/fps-raw.csv'] = process.argv.slice(2);
const SIZES = SIZES_S.split(',').map(Number); const REPS = Number(REPS_S);
const PRESET = Object.fromEntries(SPEED_SLIDER_KEYS.map((k) => [k, fidelityPreset(LEVEL)[k]]));
const WARM = 5000, MEAS = 10000;
const HDR = 'level,size,rep,particles_seen,fps,frame_ms_p50,frame_ms_p95,sim_ticks_per_s,engine,respawn_ms,note';
if (!fs.existsSync(OUT)) fs.writeFileSync(OUT, HDR + '\n');
const b = await chromium.launch({ args: ['--enable-unsafe-swiftshader', '--enable-precise-memory-info'] });
for (const size of SIZES) for (let rep = 1; rep <= REPS; rep++) {
  const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
  await p.goto('http://127.0.0.1:4190/');
  await p.waitForSelector('#launch-overlay [data-act="launch"]', { timeout: 30000 });
  await p.click('#launch-overlay [data-act="launch"]'); await p.waitForTimeout(1200);
  await p.click('#vepa-debug-hide', { timeout: 1500 }).catch(() => {});
  const respawn = await p.evaluate(({ size, level, preset }) => new Promise((res) => {
    const bus = window.__bus;
    window.__fb = { ticks: 0, last: null, engine: '?' };
    bus.on('physics:backend', (e) => { window.__fb.engine = e.engine; });
    bus.emit('compute:proposal', { parameter: 'computeEngine', value: 'cpu' });
    // The default TIDAL BLOOM preset caps MAX_POP at 6,000; raise the caps to the target size.
    bus.emit('world:paramChanged', { key: 'PARTICLE_COUNT', value: Math.max(size, 6000) });
    bus.emit('world:paramChanged', { key: 'MAX_POP', value: Math.max(size, 6000) });
    bus.emit('world:paramChanged', { key: 'INITIAL_POP', value: size });
    if (level !== 'HIGH') for (const [k, v] of Object.entries(preset)) bus.emit('world:paramChanged', { key: k, value: v });
    let first = true; const t = performance.now();
    bus.on('physics:tick', (e) => { window.__fb.ticks++; window.__fb.last = e; if (first && e.particleCount >= size * 0.99) { first = false; res(performance.now() - t); } });
    bus.emit('sim:restart', {});
    setTimeout(() => res(-1), 120000);
  }), { size, level: LEVEL, preset: PRESET });
  await p.waitForTimeout(WARM);
  const m = await p.evaluate(async (ms) => {
    const d = []; const t0 = performance.now(); let prev = t0; const k0 = window.__fb.ticks;
    await new Promise((res) => { const f = (t) => { d.push(t - prev); prev = t; if (t - t0 < ms) requestAnimationFrame(f); else res(); }; requestAnimationFrame(f); });
    const el = performance.now() - t0; d.sort((a, b) => a - b); const q = (x) => d[Math.min(d.length - 1, Math.floor(x * d.length))];
    return { fps: d.length / (el / 1000), p50: q(0.5), p95: q(0.95), tps: (window.__fb.ticks - k0) / (el / 1000), pc: (window.__fb.last || {}).particleCount, engine: window.__fb.engine };
  }, MEAS);
  const row = [LEVEL, size, rep, m.pc, m.fps.toFixed(1), m.p50.toFixed(1), m.p95.toFixed(1), m.tps.toFixed(2), m.engine, Math.round(respawn), 'headless Chrome NO GPU (SwiftShader) 1280x800'].join(',');
  console.log(row); fs.appendFileSync(OUT, row + '\n');
  await p.close();
}
await b.close();
