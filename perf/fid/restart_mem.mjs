import { chromium } from '/workspace/vepa/node_modules/playwright/index.mjs';
import { execSync } from 'node:child_process';
const PORT = process.argv[2], LABEL = process.argv[3];
const rss = (t) => Math.round(execSync(`ps -eo rss,args | grep headless_shell | grep -- '${t}' | grep -v grep | awk '{s+=$1} END {print s}'`).toString().trim() / 1024);
const b = await chromium.launch({ args: ['--enable-unsafe-swiftshader', '--enable-precise-memory-info', '--renderer-process-limit=1'] });
const res = [];
for (let r = 0; r < 3; r++) {
  const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
  await p.goto(`http://127.0.0.1:${PORT}/`); await p.waitForSelector('.launch-primary'); await p.click('.launch-primary'); await p.waitForTimeout(3000);
  const boot = { renderer: rss('type=renderer'), all: rss(''), heap: await p.evaluate(() => +(performance.memory.usedJSHeapSize / 1048576).toFixed(1)) };
  await p.evaluate(() => window.__bus.emit('sim:restart', {})); await p.waitForTimeout(3000);
  const after = { renderer: rss('type=renderer'), all: rss('') };
  const pc = await p.evaluate(() => new Promise((r) => window.__bus.on('physics:tick', (e) => r(e.particleCount))));
  res.push({ boot, afterRestart: after, particles: pc }); await p.close();
}
await b.close(); console.log(LABEL, JSON.stringify(res));
