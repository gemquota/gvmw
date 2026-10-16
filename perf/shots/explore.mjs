import { chromium } from '/workspace/vepa/node_modules/playwright/index.mjs';
const b = await chromium.launch({ args: ['--enable-unsafe-swiftshader'] });
const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
await p.goto('http://127.0.0.1:4190/'); await p.waitForTimeout(4000);
await p.screenshot({ path: '/workspace/perf/shots/boot.png' });
const btns = await p.$$eval('button, [role=tab], .accordion-header, .tab', (els) => els.filter(e => e.offsetParent).map(e => (e.id ? '#' + e.id + ' ' : '') + (e.className || '') + ' :: ' + e.textContent.trim().slice(0, 30)));
console.log(btns.slice(0, 80).join('\n'));
await b.close();
