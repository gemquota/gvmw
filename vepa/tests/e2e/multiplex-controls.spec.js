// D-044 (AC-97 / AC-98 / AC-99 / AC-100): Chaos Multiplex long-press PEEK,
// exact UNDO of an iterate, and a SNAPSHOT save → restore round trip that
// survives a reload (IndexedDB), with single-record delete.
import { test, expect } from '@playwright/test';
import { bootApp } from './boot.js';

const SHOTS = process.env.MPX_SHOTS || '';

async function startMultiplex(page) {
  await page.evaluate(() => window.openChaosMultiplex());
  await expect(page.locator('#chaos-modal')).toHaveClass(/open/);
  await page.locator('#mpx-preset').selectOption('smooth-20');
  await page.locator('#mpx-start').click();
  await expect(page.locator('#multiplex-overlay')).toHaveClass(/active/);
  await expect.poll(() => page.evaluate(() => window.__VEPA_MX__.shards())).toBe(20);
  await page.evaluate(() => { const h = document.querySelector('#vepa-debug-hide'); if (h) h.click(); });
}
async function expandDrawer(page) {
  const drawer = page.locator('#multiplex-drawer');
  if (!(await drawer.evaluate((d) => d.classList.contains('expanded')))) await page.locator('#multiplex-drawer .mpx-chevron').click();
  await expect(drawer).toHaveClass(/expanded/);
}
const pauseSettled = async (page) => {
  await page.evaluate(() => window.__VEPA_MX__.setPaused(true));
  await page.waitForTimeout(600);
  const a = await page.evaluate(() => window.__VEPA_MX__.digest());
  await page.waitForTimeout(300);
  expect(await page.evaluate(() => window.__VEPA_MX__.digest())).toBe(a);
  return a;
};

test('PEEK: hold ~350 ms shows a shard full screen until release; a quick tap selects (AC-97)', async ({ page }) => {
  const errors = [];
  page.on('pageerror', (e) => errors.push(e.message));
  await bootApp(page);
  await startMultiplex(page);
  const cell = page.locator('.shard-cell').nth(2).locator('canvas');
  const box = await cell.boundingBox();
  const cx = box.x + box.width / 2; const cy = box.y + box.height / 2;
  const before = await page.evaluate(() => window.__VEPA_MX__.selected());
  await page.mouse.move(cx, cy);
  await page.mouse.down();
  await page.waitForTimeout(700);
  await expect(page.locator('#mpx-peek')).toHaveClass(/active/);
  expect(await page.evaluate(() => window.__VEPA_MX__.peek())).toBe(2);
  if (SHOTS) await page.screenshot({ path: `${SHOTS}/02-peek.png` });
  await page.mouse.up();
  await expect(page.locator('#mpx-peek')).not.toHaveClass(/active/);
  expect(await page.evaluate(() => window.__VEPA_MX__.peek())).toBe(null);
  expect(await page.evaluate(() => window.__VEPA_MX__.selected())).toBe(before); // release ≠ select
  // Quick tap still selects.
  await page.mouse.down();
  await page.waitForTimeout(60);
  await page.mouse.up();
  await expect.poll(() => page.evaluate(() => window.__VEPA_MX__.selected())).toBe(2);
  // No context menu on a long-press (phones): the default is prevented.
  const prevented = await cell.evaluate((c) => !c.dispatchEvent(new MouseEvent('contextmenu', { bubbles: true, cancelable: true })));
  expect(prevented).toBe(true);
  const css = await cell.evaluate((c) => getComputedStyle(c).userSelect);
  expect(css).toBe('none');
  expect(errors).toEqual([]);
});

test('UNDO restores the previous generation exactly; REDO re-applies (AC-98 / AC-100)', async ({ page }) => {
  const errors = [];
  page.on('pageerror', (e) => errors.push(e.message));
  await bootApp(page);
  await startMultiplex(page);
  await expandDrawer(page);
  // Anneal controls are on the drawer and drive the next iterate.
  await page.locator('#mpx-run-variation').fill('0.4');
  await page.locator('#mpx-run-decay').fill('0.15');
  await expect(page.locator('#mpx-run-decay-value')).toHaveText('×0.85/gen · NEXT 34.0%');
  await expect(page.locator('#mpx-undo')).toBeDisabled();
  const d0 = await pauseSettled(page);
  const g0 = await page.evaluate(() => window.__VEPA_MX__.iteration());
  await page.locator('#mpx-iterate').click();
  await expect.poll(() => page.evaluate(() => window.__VEPA_MX__.iteration())).toBe(g0 + 1);
  expect((await page.evaluate(() => window.__VEPA_MX__.config())).variation).toBeCloseTo(0.34, 5);
  const d1 = await pauseSettled(page);
  expect(d1).not.toBe(d0);
  if (SHOTS) await page.screenshot({ path: `${SHOTS}/03-drawer-undo-anneal.png` });
  await page.locator('#mpx-undo').click();
  expect(await page.evaluate(() => window.__VEPA_MX__.digest())).toBe(d0);
  expect(await page.evaluate(() => window.__VEPA_MX__.iteration())).toBe(g0);
  expect((await page.evaluate(() => window.__VEPA_MX__.config())).variation).toBeCloseTo(0.4, 5);
  await expect(page.locator('#mpx-redo')).toBeEnabled();
  await page.locator('#mpx-redo').click();
  expect(await page.evaluate(() => window.__VEPA_MX__.digest())).toBe(d1);
  // The strip ↶ works while the drawer is minimized too.
  await page.locator('#mpx-minimize').click();
  await page.locator('#mpx-undo-strip').click();
  expect(await page.evaluate(() => window.__VEPA_MX__.digest())).toBe(d0);
  expect(errors).toEqual([]);
});

test('SNAPSHOTS: save a generation, restore it after iterating, survive a reload, delete one (AC-99)', async ({ page }) => {
  const errors = [];
  page.on('pageerror', (e) => errors.push(e.message));
  await bootApp(page);
  await startMultiplex(page);
  await expandDrawer(page);
  await page.locator('#mpx-snapshots-btn').click();
  await expect(page.locator('#mpx-snapshots')).toBeVisible();
  await pauseSettled(page);
  const sig0 = await page.evaluate(() => window.__VEPA_MX__.shardSig());
  await page.locator('#mpx-snap-name').fill('e2e generation');
  await page.locator('#mpx-snap-save-gen').click();
  const row = page.locator('.mpx-snap-row', { hasText: 'e2e generation' });
  await expect(row).toHaveCount(1);
  await expect(row).toContainText('GEN 20 SIMS');
  await expect(row).toContainText('SEED 0x');
  await expect(page.locator('#mpx-snap-total')).toContainText(/1 SAVED · [\d.]+ (KB|MB) · INDEXEDDB/);
  // Select a shard and save it too, for COMPARE.
  await page.locator('.mpx-metric-chip').nth(3).click();
  await page.locator('#mpx-snap-save-shard').click();
  await expect(page.locator('.mpx-snap-row')).toHaveCount(2);
  if (SHOTS) await page.screenshot({ path: `${SHOTS}/04-snapshots-panel.png` });

  await page.locator('#mpx-iterate').click();
  await pauseSettled(page);
  expect(await page.evaluate(() => window.__VEPA_MX__.shardSig())).not.toEqual(sig0);
  await row.locator('button[data-act="restore"]').click();
  await expect.poll(() => page.evaluate(() => window.__VEPA_MX__.shardSig())).toEqual(sig0);

  // COMPARE the two snapshots live with the stats table; END COMPARE = undo.
  for (const r of await page.locator('.mpx-snap-row .mpx-snap-pick').all()) await r.check();
  await page.locator('#mpx-snap-compare').click();
  await expect.poll(() => page.evaluate(() => window.__VEPA_MX__.shards())).toBe(2);
  await page.evaluate(() => window.__VEPA_MX__.setPaused(false));
  await expect(page.locator('#mpx-snap-stats-table tbody tr')).toHaveCount(2, { timeout: 10_000 });
  await expect(page.locator('#mpx-snap-stats-table thead')).toContainText('BONDED %');
  if (SHOTS) await page.screenshot({ path: `${SHOTS}/05-compare.png` });
  await page.locator('#mpx-snap-compare-end').click();
  await expect.poll(() => page.evaluate(() => window.__VEPA_MX__.shards())).toBe(20);

  // Reload: the snapshots persist (IndexedDB); delete exactly one.
  await page.reload();
  await bootApp(page);
  await startMultiplex(page);
  await expandDrawer(page);
  await page.locator('#mpx-snapshots-btn').click();
  await expect(page.locator('.mpx-snap-row')).toHaveCount(2);
  page.once('dialog', (d) => d.accept());
  await page.locator('.mpx-snap-row', { hasText: 'e2e generation' }).locator('button[data-act="delete"]').click();
  await expect(page.locator('.mpx-snap-row')).toHaveCount(1);
  await expect(page.locator('#mpx-snapshots button', { hasText: /DELETE ALL|CLEAR ALL/i })).toHaveCount(0);
  expect(errors).toEqual([]);
});
