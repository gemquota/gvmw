// usage: node mx-refill-check.mjs <url> <on|off> [iters] [gapMs]
import { chromium } from '/workspace/vepa/node_modules/playwright/index.mjs';
const [url, mode, itersArg, gapArg] = process.argv.slice(2);
const iters = +(itersArg || 10); const gap = +(gapArg || 1500);
const browser = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--disable-gpu'] });
const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
await ctx.addInitScript(() => { try { localStorage.setItem('vepa4.debugOverlay', 'false'); localStorage.removeItem('vepa-multiplex-settings'); } catch (e) {} });
const page = await ctx.newPage();
const errors = []; page.on('pageerror', (e) => errors.push(e.message));
await page.goto(url);
await page.locator('.launch-primary').click({ timeout: 15000 }).catch(() => {});
await page.waitForTimeout(2500);
await page.evaluate(() => window.openChaosMultiplex());
await page.waitForTimeout(400);
await page.selectOption('#mpx-preset', 'full-fidelity');
await page.fill('#mpx-per-sim', '1250'); await page.locator('#mpx-per-sim').dispatchEvent('input');
await page.evaluate((on) => { const r = document.querySelector('input[name="mpx-derive"][value="clone"]'); r.checked = true; document.querySelector('#mpx-refill').checked = on; }, mode === 'on');
await page.locator('#mpx-start').click();
const stat = () => page.evaluate(() => document.querySelector('#mpx-metrics-stats')?.textContent || '');
const aliveOf = (t) => +((/ALIVE (\d+)/.exec(t) || [])[1] || NaN);
await page.waitForTimeout(4000);
const before = await stat();
const log = [];
for (let i = 0; i < iters; i++) {
  await page.locator('#mpx-iterate-strip').click({ force: true });
  await page.waitForTimeout(gap);
  log.push(aliveOf(await stat()));
}
await page.waitForTimeout(1500);
const after = await stat();
const perShard = await page.evaluate(() => [...document.querySelectorAll('.mpx-metric-chip')].length);
console.log(JSON.stringify({ mode, before, after, aliveBefore: aliveOf(before), aliveAfter: aliveOf(after), perIter: log, shards: perShard, errors }));
await browser.close();
