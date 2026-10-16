// Screenshot the top bar at desktop and phone sizes. usage: node topbar-shot.mjs <url> <prefix>
import { chromium } from '/workspace/vepa/node_modules/playwright/index.mjs';
const [url, prefix] = process.argv.slice(2);
const browser = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--disable-gpu'] });
const out = {};
for (const [w, h, mobile] of [[1280, 800, false], [390, 844, true]]) {
  const ctx = await browser.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: mobile ? 3 : 1, isMobile: mobile, hasTouch: mobile });
  await ctx.addInitScript(() => { try { localStorage.setItem('vepa4.debugOverlay', 'false'); } catch (e) {} });
  const page = await ctx.newPage();
  const errors = []; page.on('pageerror', (e) => errors.push(e.message));
  await page.goto(url);
  const launch = page.locator('.launch-primary');
  await launch.waitFor({ state: 'visible', timeout: 15000 }).then(() => launch.click()).catch(() => {});
  await page.waitForTimeout(4000);
  const info = await page.evaluate(() => {
    const r = (s) => { const e = document.querySelector(s); if (!e) return null; const b = e.getBoundingClientRect(); return { x: Math.round(b.x), y: Math.round(b.y), w: Math.round(b.width), h: Math.round(b.height), text: e.textContent, count: e.dataset.count }; };
    const dot = document.querySelector('#hud-particles');
    const cs = dot && getComputedStyle(dot); const before = dot && getComputedStyle(dot, '::before'); const after = dot && getComputedStyle(dot, '::after');
    return { toolbar: r('#top-toolbar'), center: r('.toolbar-center'), orb: r('#hud-particles'), tick: r('#hud-tick'), count: r('#hud-population-count'), dot: r('#hud-status-dot'),
      orbStyle: cs && { w: cs.width, h: cs.height, radius: cs.borderRadius }, before: before && { content: before.content, w: before.width, h: before.height }, after: after && { content: after.content } };
  });
  const file = `/workspace/out/topbar/${prefix}-${w}x${h}.png`;
  await page.screenshot({ path: file, clip: { x: 0, y: 0, width: w, height: Math.min(h, 90) } });
  await page.screenshot({ path: file.replace('.png', '-full.png') });
  out[`${w}x${h}`] = { file, errors, ...info };
  await ctx.close();
}
await browser.close();
console.log(JSON.stringify(out, null, 1));
