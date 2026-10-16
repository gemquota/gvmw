// D-043 (AC-96): LIVE EDITS in SETUP › WORLD. OFF (default): a WORLD slider
// edit stays pending until restart. ON: the same edit reaches the running
// world with no restart, and the seed readout says "(live-edited)".
import { test, expect } from '@playwright/test';

const SHOTS = process.env.LIVE_EDITS_SHOTS || '';

async function openRuntime(page) {
  const pageErrors = [];
  page.on('pageerror', (error) => pageErrors.push(error.message));
  await page.goto('/');
  await expect(page.locator('#sim-canvas')).toBeVisible();
  await page.waitForFunction(() => Boolean(window.__VEPA_DEBUG__?._active));
  await expect.poll(() => page.evaluate(() => Boolean(
    document.querySelector('#launch-overlay') || document.querySelector('#law-grid')?.children.length,
  ))).toBe(true);
  const launchOverlay = page.locator('#launch-overlay');
  if (await launchOverlay.count()) {
    await launchOverlay.locator('[data-act="launch"]').click();
    await expect(launchOverlay).toHaveCount(0);
  }
  await expect.poll(() => page.locator('#hud-tick').getAttribute('aria-label')).toMatch(/Tick [1-9]\d*,/);
  return pageErrors;
}

const tickOf = (page) => page.evaluate(() => window.__VEPA_TEST__.state().tick);
const liveWorldSize = (page) => page.evaluate(() => window.__VEPA_TEST__.worldParam('WORLD_SIZE'));

test('LIVE EDITS: OFF keeps a WORLD edit pending; ON applies it without a restart (AC-96)', async ({ page }) => {
  const pageErrors = await openRuntime(page);
  await page.locator('#main-panel .sub-tab-btn[data-sub="setup-world"]').click();
  await expect(page.locator('#setup-world')).toHaveClass(/active/);

  const toggle = page.locator('#live-edits-toggle');
  const seed = page.locator('#live-edits-seed');
  const status = page.locator('#setup-world [data-pending-status]');
  const slider = page.locator('#world-params .sc-row[data-key="WORLD_SIZE"] .sc-input');
  await expect(toggle).not.toBeChecked();                 // default OFF
  await expect(seed).toHaveText(/^Seed \d+$/);
  await expect(page.locator('#hud-live-edited')).toBeHidden();

  // OFF: staged, live world unchanged.
  const before = await liveWorldSize(page);
  await slider.focus();
  await slider.press('ArrowRight');
  await expect(status).toContainText('pending');
  expect(await liveWorldSize(page)).toBe(before);
  if (SHOTS) await page.locator('#live-edits-control').evaluate((el) => el.scrollIntoView({ block: 'start' }));
  if (SHOTS) await page.locator('#main-panel').screenshot({ path: `${SHOTS}/01-live-edits-off-pending.png` });
  await page.locator('#setup-world [data-pending-discard]').click();
  await expect(status).toContainText('No staged world changes');

  // ON: applied to the running world, no restart (tick keeps counting up).
  await page.locator('label.live-edits-toggle').click();
  await expect(toggle).toBeChecked();
  const tick0 = await tickOf(page);
  await slider.focus();
  await slider.press('ArrowRight');
  await expect.poll(() => liveWorldSize(page)).not.toBe(before);
  await expect(status).toContainText('No staged world changes');
  await expect(seed).toHaveText(/^Seed \d+ \(live-edited\)$/);
  await expect(page.locator('#hud-live-edited')).toBeVisible();
  await expect.poll(() => tickOf(page)).toBeGreaterThan(tick0);
  const det = await page.evaluate(() => window.__VEPA_TEST__.liveEdits());
  expect(det).toMatchObject({ enabled: true, liveEdited: true });
  if (SHOTS) {
    await page.locator('#live-edits-control').evaluate((el) => el.scrollIntoView({ block: 'start' }));
    await page.locator('#main-panel').screenshot({ path: `${SHOTS}/02-live-edits-on-live-edited.png` });
    // The dev-only debug overlay sits over the toolbar; hide it for the shot.
    await page.evaluate(() => { const d = document.getElementById('vepa-debug'); if (d) d.style.display = 'none'; });
    await page.screenshot({ path: `${SHOTS}/03-toolbar-live-edited-badge.png` });
  }
  expect(pageErrors).toEqual([]);
});
