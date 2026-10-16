import { chromium } from '/workspace/vepa/node_modules/playwright/index.mjs';
const url = process.argv[2]; const iters = +(process.argv[3] || 10); const gap = +(process.argv[4] || 300);
const browser = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--disable-gpu'] });
const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
await ctx.addInitScript(() => { try { localStorage.setItem('vepa4.debugOverlay', 'false'); } catch (e) {} });
const page = await ctx.newPage();
const errors = []; page.on('pageerror', (e) => errors.push(e.message));
await page.goto(url);
await page.locator('.launch-primary').click({ timeout: 15000 }).catch(() => {});
await page.waitForTimeout(2500);
await page.evaluate(() => window.openChaosMultiplex());
await page.waitForTimeout(400);
await page.selectOption('#mpx-preset', 'full-fidelity');
await page.fill('#mpx-per-sim', '1250'); await page.locator('#mpx-per-sim').dispatchEvent('change');
await page.locator('#mpx-start').click();
const stat = () => page.evaluate(() => document.querySelector('#mpx-metrics-stats')?.textContent || '');
const log = [];
for (let i = 0; i < 4; i++) { await page.waitForTimeout(1000); log.push('t' + i + ' ' + await stat()); }
for (let i = 0; i < iters; i++) {
  await page.locator('#mpx-iterate-strip').click({ force: true }).catch((e) => log.push('click fail ' + e.message.slice(0, 80)));
  await page.waitForTimeout(gap); log.push('it' + (i + 1) + ' ' + await stat());
}
for (let i = 0; i < 3; i++) { await page.waitForTimeout(1500); log.push('post' + i + ' ' + await stat()); }
const chips = await page.evaluate(() => [...document.querySelectorAll('.mpx-metric-chip')].map((c) => c.textContent).join(' | '));
console.log(log.join('\n')); console.log('chips', chips); console.log('errors', errors.length, errors.slice(0, 5));
await page.screenshot({ path: '/tmp/mx-collapse.png' });
await browser.close();
