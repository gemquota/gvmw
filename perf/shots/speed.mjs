import { chromium } from '/workspace/vepa/node_modules/playwright/index.mjs';
const OUT = process.argv[2] || '/workspace/perf/shots';
const b = await chromium.launch({ args: ['--enable-unsafe-swiftshader'] });
async function openSpeed(p) {
  await p.goto('http://127.0.0.1:4190/'); await p.waitForTimeout(3000);
  await p.click('.launch-primary'); await p.waitForTimeout(1500);
  await p.click('#vepa-debug-hide').catch(() => {});
  await p.click('.sub-tab-btn:has-text("🌍")'); await p.waitForTimeout(500);
  await p.evaluate(() => {
    const sec = document.querySelector('.sub-accordion-section:has([data-speed-preset])');
    sec.classList.add('open'); sec.closest('.accordion-section').classList.add('open');
  });
  await p.waitForTimeout(300);
  return p.locator('.sub-accordion-section:has([data-speed-preset])');
}
for (const [w, h, tag] of [[1280, 800, 'desktop'], [390, 844, 'mobile']]) {
  const p = await b.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: tag === 'mobile' ? 2 : 1.5 });
  const sec = await openSpeed(p);
  await sec.scrollIntoViewIfNeeded();
  await p.screenshot({ path: `${OUT}/${tag}-full.png` });
  await sec.screenshot({ path: `${OUT}/${tag}-speed-group.png` });
  if (tag === 'desktop') {
    // help popup: right-click a label
    const lbl = sec.locator('.sc-label', { hasText: 'PAIR BUDGET' });
    await lbl.click({ button: 'right' }); await p.waitForTimeout(500);
    await p.screenshot({ path: `${OUT}/${tag}-speed-help.png` });
    await p.keyboard.press('Escape'); await p.mouse.click(5, 5); await p.waitForTimeout(300);
    await sec.locator('[data-speed-preset="fast"]').click(); await p.waitForTimeout(600);
    const sec2 = p.locator('.sub-accordion-section:has([data-speed-preset])');
    await sec2.scrollIntoViewIfNeeded().catch(() => {});
    await (await sec2.count() ? sec2 : sec).screenshot({ path: `${OUT}/${tag}-speed-after-fast.png` });
  }
  await p.close();
}
await b.close();
