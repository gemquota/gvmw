// Boot memory: default world, no interaction beyond Launch. NO GPU headless Chrome.
import { chromium } from '/workspace/vepa/node_modules/playwright/index.mjs';
import { execSync } from 'node:child_process';
const PORT = process.argv[2]; const LABEL = process.argv[3];
const b = await chromium.launch({ args: ['--enable-unsafe-swiftshader', '--enable-precise-memory-info', '--js-flags=--expose-gc'] });
const out = [];
for (let r = 0; r < 3; r++) {
  const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
  const t0 = Date.now(); await p.goto(`http://127.0.0.1:${PORT}/`); await p.waitForSelector('.launch-primary'); const ready = Date.now() - t0;
  await p.click('.launch-primary'); await p.waitForTimeout(4000);
  const m = await p.evaluate(() => { if (window.gc) window.gc(); return { heap: performance.memory.usedJSHeapSize / 1048576, total: performance.memory.totalJSHeapSize / 1048576 }; });
  const rss = Math.round(execSync("ps -eo rss,args | grep -E 'headless_shell' | grep -v grep | awk '{s+=$1} END {print s}'").toString().trim() / 1024);
  out.push({ ready, ...m, rss }); await p.close();
}
await b.close();
console.log(LABEL, JSON.stringify(out));
