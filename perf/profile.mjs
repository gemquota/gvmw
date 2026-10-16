// Perf profiler for the built VEPA app. usage: node profile.mjs <pop> <mode single|multiplex> [secs]
import { chromium } from '/workspace/vepa/node_modules/playwright/index.mjs';
const [pop = '300', mode = 'single', secsArg = '6'] = process.argv.slice(2);
const secs = Number(secsArg);
const url = process.env.URL || 'http://127.0.0.1:4180/';
const headed = !!process.env.HEADED;
const browser = await chromium.launch({ executablePath: '/usr/bin/google-chrome', headless: !headed,
  args: process.env.NOGPU ? ['--disable-gpu'] : ['--enable-unsafe-swiftshader', '--disable-gpu-sandbox', '--use-gl=angle', '--use-angle=swiftshader', '--ignore-gpu-blocklist'] });
const ctx = await browser.newContext({ viewport: { width: 1400, height: 900 } });
await ctx.addInitScript(({ pop, backend }) => {
  localStorage.setItem('vepa-launch-settings', JSON.stringify({ presetId: 'TIDAL_BLOOM', renderBackend: backend, computeEngine: 'gpu', simSpeed: 1, worldSize: null, initialPop: pop }));
}, { pop: Number(pop), backend: process.env.BACKEND || 'canvas2d' });
await ctx.addInitScript(() => {
  const W = window.Worker; window.__wt = [];
  window.Worker = function (...a) { const w = new W(...a); w.addEventListener('message', (e) => { const m = e.data || {}; if (m.type === 'TICK_COMPLETE') window.__wt.push([performance.now(), m.tickDuration, m.particleCount]); }); return w; };
  window.Worker.prototype = W.prototype;
});
const page = await ctx.newPage();
const logs = [];
page.on('console', (m) => { if (/error|warn/i.test(m.type())) logs.push(m.text().slice(0, 200)); });
await page.goto(url);
const launch = page.locator('.launch-primary');
await launch.waitFor({ state: 'visible', timeout: 20000 }).then(() => launch.click()).catch(() => {});
await page.waitForFunction(() => typeof window.openChaosMultiplex === 'function', null, { timeout: 60000 });
if (mode === 'multiplex') {
  await page.evaluate(() => window.openChaosMultiplex());
  await page.click('#mpx-start');
}
await page.waitForTimeout(4000); // warm-up
const cdp = await ctx.newCDPSession(page);
await cdp.send('Profiler.enable');
await cdp.send('Profiler.setSamplingInterval', { interval: 200 });
await cdp.send('Performance.enable');
const m0 = (await cdp.send('Performance.getMetrics')).metrics;
const tickOf = () => page.evaluate(() => Number((document.getElementById('hud-tick')?.textContent || '0').split('\n')[0].replace(/,/g, '')) || 0);
const mxTick = () => page.evaluate(() => { const t = document.body.innerText.match(/TICK[^0-9]*([0-9,]+)/); return t ? Number(t[1].replace(/,/g, '')) : 0; });
const tick0 = await tickOf();
await cdp.send('Profiler.start');
const fpsInfo = await page.evaluate((ms) => new Promise((res) => {
  const t = []; const start = performance.now();
  function f(now) { t.push(now); if (now - start < ms) requestAnimationFrame(f); else res(t); }
  requestAnimationFrame(f);
}), secs * 1000);
const { profile } = await cdp.send('Profiler.stop');
const tick1 = await tickOf();
const wt = await page.evaluate(() => { const a = window.__wt.slice(-40); return a.length ? { n: a.length, workerTickMs: +(a.reduce((x, y) => x + y[1], 0) / a.length).toFixed(1), particles: a.at(-1)[2], intervalMs: a.length > 1 ? +((a.at(-1)[0] - a[0][0]) / (a.length - 1)).toFixed(1) : null } : null; });
const pcount = await page.evaluate(() => document.getElementById('hud-particles')?.textContent || document.getElementById('hud-particles')?.title);
const m1 = (await cdp.send('Performance.getMetrics')).metrics;
const stats = await page.evaluate(() => {
  const txt = (s) => document.querySelector(s)?.textContent || '';
  return { hud: [...document.querySelectorAll('[id*=perf],[class*=perf]')].slice(0, 6).map((e) => e.textContent.trim().slice(0, 80)), worker: typeof Worker };
});
const d = fpsInfo.slice(1).map((v, i) => v - fpsInfo[i]); d.sort((a, b) => a - b);
const fps = (fpsInfo.length - 1) / ((fpsInfo.at(-1) - fpsInfo[0]) / 1000);
// aggregate self time by function and by category
const byId = new Map(profile.nodes.map((n) => [n.id, n]));
const self = new Map();
const dts = profile.timeDeltas; let total = 0;
profile.samples.forEach((id, i) => { const dt = dts[i] || 0; total += dt; self.set(id, (self.get(id) || 0) + dt); });
const fn = new Map(), cat = new Map();
const categorize = (n) => {
  const u = n.callFrame.url || '', f = n.callFrame.functionName;
  if (f === '(garbage collector)') return 'GC';
  if (f === '(idle)') return 'idle';
  if (f === '(program)') return 'program/native';
  if (/solver|laws|lawgroups|physics|octree|synergy|mergePhysics/i.test(u + f)) return 'physics';
  if (/fields/i.test(u + f)) return 'field';
  if (/render|pixi|sprite|canvas/i.test(u + f)) return 'render';
  if (/ui|panel|hud|html|dom/i.test(u + f)) return 'ui';
  return 'other:' + (u.split('/').pop() || '(native)');
};
for (const [id, t] of self) {
  const n = byId.get(id);
  const key = `${n.callFrame.functionName || '(anon)'} ${(n.callFrame.url || '').split('/').pop()}:${n.callFrame.lineNumber + 1}`;
  fn.set(key, (fn.get(key) || 0) + t);
  const c = categorize(n); cat.set(c, (cat.get(c) || 0) + t);
}
const met = (arr, k) => arr.find((m) => m.name === k)?.value || 0;
const out = {
  pop: Number(pop), mode, worker: wt, simTicksPerSec: +((tick1 - tick0) / secs).toFixed(1), hudParticles: pcount, fps: +fps.toFixed(1), frameMs: { p50: +d[Math.floor(d.length / 2)]?.toFixed(1), p95: +d[Math.floor(d.length * 0.95)]?.toFixed(1), max: +d.at(-1)?.toFixed(1) },
  mainThreadBusyPct: +(100 * (1 - (cat.get('idle') || 0) / total)).toFixed(1),
  categoriesMsPerFrame: Object.fromEntries([...cat].sort((a, b) => b[1] - a[1]).map(([k, v]) => [k, +(v / 1000 / (fpsInfo.length - 1)).toFixed(2)])),
  topSelf: [...fn].sort((a, b) => b[1] - a[1]).slice(0, 15).map(([k, v]) => `${(v / total * 100).toFixed(1)}% ${k}`),
  layoutCount: met(m1, 'LayoutCount') - met(m0, 'LayoutCount'), recalcStyle: met(m1, 'RecalcStyleCount') - met(m0, 'RecalcStyleCount'),
  jsHeapMB: +(met(m1, 'JSHeapUsedSize') / 1e6).toFixed(1), workers: page.workers().length, hud: stats.hud, logs: logs.slice(0, 5),
};
console.log(JSON.stringify(out, null, 1));
await browser.close();
