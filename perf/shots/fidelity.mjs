import { chromium } from '/workspace/vepa/node_modules/playwright/index.mjs';
const OUT = '/workspace/out/fidelity-bench';
const b = await chromium.launch({ args: ['--enable-unsafe-swiftshader'] });
const sizes = [[1280, 800, 'desktop', 1.5], [390, 1500, 'phone390', 2]];
async function boot(w, h, dpr) {
  const p = await b.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: dpr, hasTouch: w < 500 });
  p.setDefaultTimeout(15000);
  await p.goto('http://127.0.0.1:4190/'); await p.waitForTimeout(3000);
  await p.click('.launch-primary'); await p.waitForTimeout(1500);
  await p.click('#vepa-debug-hide', { timeout: 2000 }).catch(() => {});
  return p;
}
async function openSpeed(p) {
  await p.click('.sub-tab-btn:has-text("🌍")'); await p.waitForTimeout(500);
  await p.evaluate(() => {
    const sec = document.querySelector('.sub-accordion-section:has([data-speed-preset])');
    sec.classList.add('open'); sec.closest('.accordion-section').classList.add('open');
    sec.scrollIntoView({ block: 'start' });
  });
  await p.waitForTimeout(400);
  return p.locator('.sub-accordion-section:has([data-speed-preset])');
}
async function snap(p, loc, path) {
  const bb = await loc.boundingBox();
  const vp = p.viewportSize();
  const clip = { x: Math.max(0, bb.x - 4), y: Math.max(0, bb.y - 4), width: Math.min(vp.width, bb.width + 8), height: Math.min(vp.height - Math.max(0, bb.y - 4), bb.height + 8) };
  await p.screenshot({ path, clip, timeout: 20000 });
  console.log('saved', path);
}
for (const [w, h, tag, dpr] of sizes) {
  let p = await boot(w, h, dpr);
  let sec = await openSpeed(p);
  await snap(p, sec, `${OUT}/${tag}-fidelity-HIGH.png`);
  for (const lv of ['MEDIUM', 'LOW', 'LOWEST']) {
    await p.click(`[data-fidelity="${lv}"]`); await p.waitForTimeout(800);
    sec = await openSpeed(p);
    await snap(p, sec, `${OUT}/${tag}-fidelity-${lv}.png`);
  }
  // nudge one slider -> CUSTOM
  await p.evaluate(() => { window.__bus && window.__bus.emit('world:paramChanged', { key: 'SPEED_MID_RANGE', value: 65 }); window.__bus && window.__bus.emit('world:paramsRestored'); });
  await p.waitForTimeout(500); sec = await openSpeed(p);
  await snap(p, sec.locator('.speed-presets'), `${OUT}/${tag}-fidelity-CUSTOM.png`);
  if (false) {
    await p.locator('.sub-accordion-section:has([data-speed-preset]) .sc-label, .sub-accordion-section:has([data-speed-preset]) [class*=label]').filter({ hasText: 'PAIR BUDGET' }).first().click({ button: 'right' }).catch(e => console.log('help fail', e.message));
    await p.waitForTimeout(600);
    await p.screenshot({ path: `${OUT}/${tag}-speed-help-pair-budget.png` }); console.log('saved help');
  }
  await p.close();
  // multiplex
  p = await boot(w, h, dpr);
  const bb = await p.locator('#chaos-btn').boundingBox();
  await p.mouse.move(bb.x + bb.width / 2, bb.y + bb.height / 2); await p.mouse.down(); await p.waitForTimeout(1200); await p.mouse.up();
  await p.waitForTimeout(800);
  await p.click('#chaos-tab-multiplex', { timeout: 3000 }).catch(e => console.log('menu tab fail'));
  await p.click('[data-action="multiplex"]', { timeout: 3000 }).catch(async () => { console.log('fallback hook'); await p.evaluate(() => window.openChaosMultiplex()); });
  await p.waitForTimeout(800);
  const open = await p.evaluate(() => document.getElementById('chaos-modal')?.classList.contains('open'));
  console.log('modal open', open);
  await p.click('#mpx-tab-grid').catch(() => {});
  for (const lv of ['LOW', 'LOWEST']) {
    await p.selectOption('#mpx-fidelity', lv); await p.waitForTimeout(400);
    const perf = p.locator('#mpx-perf-section');
    await perf.evaluate(el => el.scrollIntoView({ block: 'start' }));
    await p.waitForTimeout(300);
    await p.screenshot({ path: `${OUT}/${tag}-multiplex-fidelity-${lv}.png` }); console.log('saved mpx', lv);
    const box = await p.locator('.mpx-set-row:has(#mpx-fidelity)').boundingBox(); const box2 = await p.locator('.mpx-set-row:has(#mpx-law-count)').boundingBox();
    await p.screenshot({ path: `${OUT}/${tag}-multiplex-fidelity-crop-${lv}.png`, clip: { x: 0, y: box.y - 6, width: p.viewportSize().width, height: box2.y + box2.height - box.y + 12 } });
  }
  await p.close();
}
await b.close();
