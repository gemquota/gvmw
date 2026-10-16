// usage: node settings-shot.mjs <url> <prefix> [--start]
import { chromium } from '/workspace/vepa/node_modules/playwright/index.mjs';
const [url, prefix, ...flags] = process.argv.slice(2);
const OUT = '/workspace/out/settings-tabs';
const browser = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--disable-gpu'] });
const out = {};
for (const [w, h, mobile] of [[1280, 800, false], [390, 844, true]]) {
  const tag = `${w}x${h}`;
  const ctx = await browser.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: mobile ? 2 : 1, isMobile: mobile, hasTouch: mobile });
  await ctx.addInitScript(() => { try { localStorage.setItem('vepa4.debugOverlay', 'false'); } catch (e) {} });
  const page = await ctx.newPage();
  const errors = []; page.on('pageerror', (e) => errors.push(e.message));
  page.on('console', (m) => { if (m.type() === 'error') errors.push('console: ' + m.text().slice(0, 200)); });
  await page.goto(url);
  const launch = page.locator('.launch-primary');
  await launch.waitFor({ state: 'visible', timeout: 15000 }).then(() => launch.click()).catch(() => {});
  await page.waitForTimeout(2500);
  // CHAOS menu via long press
  const btn = page.locator('#chaos-btn');
  const box = await btn.boundingBox();
  await page.mouse.move(box.x + box.width / 2, box.y + box.height / 2);
  await page.mouse.down(); await page.waitForTimeout(900); await page.mouse.up();
  await page.waitForTimeout(400);
  const files = [];
  let f = `${OUT}/${prefix}-chaos-${tag}.png`; await page.screenshot({ path: f }); files.push(f);
  const chaosTabs = await page.locator('#chaos-menu [role=tab]').count();
  for (let i = 0; i < chaosTabs; i++) {
    await page.locator('#chaos-menu [role=tab]').nth(i).click(); await page.waitForTimeout(150);
    f = `${OUT}/${prefix}-chaos-tab${i + 1}-${tag}.png`; await page.screenshot({ path: f }); files.push(f);
  }
  const chaosInfo = await page.evaluate(() => { const m = document.querySelector('#chaos-menu .chaos-menu-content'); if (!m) return null; const b = m.getBoundingClientRect(); return { w: Math.round(b.width), h: Math.round(b.height), sw: m.scrollWidth, cw: m.clientWidth }; });
  // open multiplex settings
  await page.evaluate(() => { document.getElementById('chaos-menu')?.remove(); window.openChaosMultiplex && window.openChaosMultiplex(); });
  await page.waitForTimeout(500);
  f = `${OUT}/${prefix}-multiplex-${tag}.png`; await page.screenshot({ path: f }); files.push(f);
  const mpxTabs = await page.locator('#chaos-multiplex-modal [role=tab], .chaos-modal-panel [role=tab]').count();
  for (let i = 0; i < mpxTabs; i++) {
    await page.locator('.chaos-modal-panel [role=tab]').nth(i).click(); await page.waitForTimeout(150);
    f = `${OUT}/${prefix}-multiplex-tab${i + 1}-${tag}.png`; await page.screenshot({ path: f }); files.push(f);
  }
  const mpxInfo = await page.evaluate(() => { const p = document.querySelector('.chaos-modal-panel'); if (!p) return null; const b = p.getBoundingClientRect(); return { w: Math.round(b.width), h: Math.round(b.height), scrollH: p.scrollHeight, overflowX: p.scrollWidth > p.clientWidth + 1 }; });
  let stats = null;
  if (flags.includes('--start')) {
    await page.locator('#mpx-start').click().catch(() => {});
    const samples = [];
    for (let i = 0; i < 6; i++) { await page.waitForTimeout(700); samples.push(await page.evaluate(() => document.querySelector('#mpx-metrics-stats')?.textContent || '')); }
    stats = samples;
  }
  out[tag] = { files, errors: errors.slice(0, 8), errorCount: errors.length, chaosInfo, mpxInfo, chaosTabs, mpxTabs, stats };
  await ctx.close();
}
await browser.close();
console.log(JSON.stringify(out, null, 1));
