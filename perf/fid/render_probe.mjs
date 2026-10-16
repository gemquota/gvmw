import { chromium } from '/workspace/vepa/node_modules/playwright/index.mjs';
const b = await chromium.launch({ args: ['--enable-unsafe-swiftshader'] });
const run = async (label, vp, dpr, hide) => {
  const p = await b.newPage({ viewport: vp, deviceScaleFactor: dpr });
  await p.goto('http://127.0.0.1:4190/'); await p.waitForTimeout(2500);
  await p.click('.launch-primary').catch(() => {}); await p.waitForTimeout(1200);
  await p.click('#vepa-debug-hide', { timeout: 1500 }).catch(() => {});
  await p.evaluate(() => { const bus = window.__bus; bus.emit('world:paramChanged', { key: 'INITIAL_POP', value: 10000 }); bus.emit('sim:restart', {}); });
  if (hide) await p.addStyleTag({ content: 'canvas { visibility: hidden !important; }' });
  await p.waitForTimeout(2500);
  const r = await p.evaluate(async () => { const d = []; const t0 = performance.now(); let prev = t0; await new Promise((res) => { const f = (t) => { d.push(t - prev); prev = t; if (t - t0 < 5000) requestAnimationFrame(f); else res(); }; requestAnimationFrame(f); }); d.sort((a, b) => a - b); return { fps: d.length / ((performance.now() - t0) / 1000), p50: d[d.length >> 1], p95: d[Math.floor(d.length * 0.95)], canvas: [...document.querySelectorAll('canvas')].map((c) => `${c.width}x${c.height}`).join(' ') }; });
  console.log(label, JSON.stringify(r)); await p.close();
};
await run('1280x800 dpr1', { width: 1280, height: 800 }, 1, false);
await run('1280x800 dpr2', { width: 1280, height: 800 }, 2, false);
await run('640x400 dpr1', { width: 640, height: 400 }, 1, false);
await run('1280x800 dpr1 canvas hidden', { width: 1280, height: 800 }, 1, true);
await b.close();
