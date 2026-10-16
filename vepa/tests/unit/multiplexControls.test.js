// D-044 (AC-98 / AC-99 / AC-100 / AC-101): exact UNDO of multiplex iterates,
// the bounded generation stack, the snapshot store and compare stats.
import { describe, it, expect, afterEach } from 'vitest';
import { PARTICLE_STRIDE, STRIDE_INDEXES as S, LAW_INDEXES, DNA_RANGES } from '../../src/constants.js';
import { createLawState, set as lawSet } from '../../src/state/lawState.js';
import { createDNABuffer, loadDefaults } from '../../src/dna/dnaBuffer.js';
import { createWorldParams } from '../../src/state/worldParams.js';
import { runtimeConfig } from '../../src/state/runtimeConfig.js';
import { TIDAL_BLOOM } from '../../src/state/defaultPresets.js';
import { resetFields } from '../../src/physics/fields.js';
import {
  createMultiplex, startMultiplex, stopMultiplex, stepMultiplex, iterateMultiplex, revertMultiplex, MULTIPLEX_DEFAULTS,
  captureGeneration, restoreGeneration, digestGeneration, shardQuickStats, snapshotShardFull,
  loadSnapshotsUndoable, seedFromSnapshot, sourceFromSnapshot, setPeek, PEEK_HOLD_MS,
} from '../../src/multiplex/multiplex.js';
import { createGenerationStack, UNDO_BYTE_BUDGET } from '../../src/multiplex/generationStack.js';
import { createSnapshotStore, createMemorySnapshotAdapter, buildSnapshotRecord, snapshotRecordBytes } from '../../src/multiplex/snapshotStore.js';
import { annealReadout } from '../../src/multiplex/multiplexControls.js';

const savedWP = runtimeConfig.worldParams;
afterEach(() => { runtimeConfig.worldParams = savedWP; resetFields(); });

function source(n = 120) {
  const view = new Float32Array(n * PARTICLE_STRIDE);
  let s = 4242;
  const r = () => ((s = (s * 1103515245 + 12345) >>> 0) / 4294967296);
  for (let i = 0; i < n; i++) {
    const b = i * PARTICLE_STRIDE;
    view[b + S.POS_X] = 800 + r() * 400; view[b + S.POS_Y] = 800 + r() * 400; view[b + S.POS_Z] = 800 + r() * 400;
    view[b + S.MASS] = 1 + r(); view[b + S.ENERGY] = 70; view[b + S.RADIUS] = 0.7; view[b + S.SPECIES_ID] = i % 3;
    view[b + S.TEMPERATURE] = 0.5;
    for (const k of ['BOND_PARTNER_1', 'BOND_PARTNER_2', 'BOND_PARTNER_3', 'BOND_PARTNER_4']) view[b + S[k]] = -1;
  }
  const laws = createLawState();
  for (const name of TIDAL_BLOOM.laws) lawSet(laws, LAW_INDEXES[name]);
  const dna = createDNABuffer();
  loadDefaults(dna, DNA_RANGES);
  return { view, count: n, dna, laws, speciesCount: 3, worldParams: { ...createWorldParams(), ...TIDAL_BLOOM.worldParams } };
}
const cfg = (cols = 3) => ({ ...MULTIPLEX_DEFAULTS, cols, rows: 1, seed: 7, variation: 0.4, cooling: 0.15, randomizeLaws: false });

function running(cols = 3) {
  runtimeConfig.worldParams = { ...createWorldParams(), ...TIDAL_BLOOM.worldParams };
  const mx = createMultiplex(null);
  startMultiplex(mx, source(), cfg(cols), null);
  mx.undo = createGenerationStack();
  for (let t = 0; t < 4; t++) stepMultiplex(mx, 1 / 60, 1, 2000);
  return mx;
}

describe('D-044 UNDO iterate (AC-98)', () => {
  it('UNDO restores the previous generation exactly; REDO re-applies it', () => {
    const mx = running();
    const before = digestGeneration(mx);
    const genBefore = mx.iteration;
    const varBefore = mx.config.variation;
    const prngBefore = mx.shards.map((s) => s.prng.state);
    iterateMultiplex(mx, { manual: true });
    for (let t = 0; t < 3; t++) stepMultiplex(mx, 1 / 60, 1, 2000);
    const after = digestGeneration(mx);
    expect(after).not.toBe(before);
    expect(mx.config.variation).toBeLessThan(varBefore); // decay applied

    const target = mx.undo.undo(captureGeneration(mx));
    expect(restoreGeneration(mx, target)).toBe(true);
    expect(digestGeneration(mx)).toBe(before);
    expect(mx.iteration).toBe(genBefore);
    expect(mx.config.variation).toBe(varBefore);
    expect(mx.shards.map((s) => s.prng.state)).toEqual(prngBefore);

    const fwd = mx.undo.redo(captureGeneration(mx));
    restoreGeneration(mx, fwd);
    expect(digestGeneration(mx)).toBe(after);
    stopMultiplex(mx);
  });

  it('multi-step: 10 iterates undo back to the start, and a revert is undoable too', () => {
    const mx = running(2);
    const digests = [digestGeneration(mx)];
    for (let i = 0; i < 10; i++) {
      iterateMultiplex(mx, { manual: true });
      stepMultiplex(mx, 1 / 60, 1, 2000);
      digests.push(digestGeneration(mx));
    }
    expect(mx.undo.stats().undo).toBe(10);
    for (let i = 9; i >= 0; i--) {
      restoreGeneration(mx, mx.undo.undo(captureGeneration(mx)));
      expect(digestGeneration(mx)).toBe(digests[i]);
    }
    expect(mx.undo.canUndo).toBe(false);
    const d0 = digestGeneration(mx);
    // redo all the way, then revert to G2, then undo the revert.
    while (mx.undo.canRedo) restoreGeneration(mx, mx.undo.redo(captureGeneration(mx)));
    const top = digestGeneration(mx);
    expect(revertMultiplex(mx, mx.iteration - 1)).toBe(true);
    restoreGeneration(mx, mx.undo.undo(captureGeneration(mx)));
    expect(digestGeneration(mx)).toBe(top);
    expect(d0).toBe(digests[0]);
    stopMultiplex(mx);
  });

  it('the stack is bounded by steps and bytes; memory per step is stated', () => {
    const st = createGenerationStack({ maxSteps: 12, budgetBytes: 100 });
    for (let i = 0; i < 30; i++) st.push({ bytes: 10, i });
    expect(st.stats().undo).toBe(10);
    expect(st.stats().bytes).toBeLessThanOrEqual(100);
    const big = createGenerationStack({ maxSteps: 20, budgetBytes: 10 });
    big.push({ bytes: 50 });
    expect(big.stats().undo).toBe(1); // the newest step always stays
    // 20 sims × 2,500 live particles: per-step bytes from a real capture
    // scaled by particle count; ≥ 10 steps must fit the default budget.
    const mx = running(1);
    const gen = captureGeneration(mx);
    const sn = gen.shards[0];
    const fixed = gen.bytes - 2048 - sn.view.byteLength; // DNA, laws, speciation, params
    const perStep = 2048 + 20 * (fixed + 2500 * PARTICLE_STRIDE * 4);
    console.log(`[D-044] undo step @ 20 sims x 2,500: ${(perStep / 1048576).toFixed(1)} MB (fixed/shard ${fixed} B, ${PARTICLE_STRIDE * 4} B/particle)`);
    expect(Math.floor(UNDO_BYTE_BUDGET / perStep)).toBeGreaterThanOrEqual(10);
    stopMultiplex(mx);
  });
});

describe('D-044 SNAPSHOTS (AC-99)', () => {
  it('saves, lists newest first with sizes, loads and deletes one at a time', async () => {
    const store = createSnapshotStore(createMemorySnapshotAdapter());
    expect(typeof store.removeAll).toBe('undefined'); // no bulk wipe
    const mx = running(2);
    const a = await store.save(buildSnapshotRecord({ kind: 'shard', generation: 0, shardIds: [0], shards: [snapshotShardFull(mx.shards[0])], seed: 0x51f15e, liveEdited: true, liveEditCount: 3, now: 1000 }));
    const b = await store.save(buildSnapshotRecord({ name: 'whole', kind: 'generation', generation: 0, shardIds: [0, 1], shards: mx.shards.map(snapshotShardFull), seed: 9, now: 2000 }));
    const { items, totalBytes } = await store.list();
    expect(items.map((m) => m.id)).toEqual([b.id, a.id]);
    expect(totalBytes).toBe(a.bytes + b.bytes);
    expect(a.name).toMatch(/^S01 G0 /);
    expect(a.liveEdited).toBe(true);
    expect(a.seed).toBe(0x51f15e);
    const rec = await store.load(a.id);
    expect(rec.liveEditCount).toBe(3);
    expect(snapshotRecordBytes(rec)).toBe(a.bytes);
    await store.remove(a.id);
    expect((await store.list()).items.map((m) => m.id)).toEqual([b.id]);
    stopMultiplex(mx);
  });

  it('restore / compare from snapshots runs them live and is undoable; seed breeds from one', () => {
    const mx = running(3);
    const snaps = [snapshotShardFull(mx.shards[2]), snapshotShardFull(mx.shards[0])];
    const before = digestGeneration(mx);
    expect(loadSnapshotsUndoable(mx, snaps, { labels: ['x', 'y'] })).toBe(true);
    expect(mx.shards.length).toBe(2);
    expect(mx.shards[0].count).toBe(snaps[0].count);
    expect(Array.from(mx.shards[0].view.subarray(0, snaps[0].view.length))).toEqual(Array.from(snaps[0].view));
    stepMultiplex(mx, 1 / 60, 1, 2000);
    expect(mx.shards[0].tick).toBe(snaps[0].tick + 1);
    const stats = mx.shards.map(shardQuickStats);
    expect(stats[0].alive).toBeGreaterThan(0);
    expect(stats[0].species).toBeGreaterThan(0);
    // UNDO goes back to the 3-sim grid exactly.
    restoreGeneration(mx, mx.undo.undo(captureGeneration(mx)));
    expect(mx.shards.length).toBe(3);
    expect(digestGeneration(mx)).toBe(before);
    // SEED: a new generation derived from a snapshot (undoable).
    const g = mx.iteration;
    expect(seedFromSnapshot(mx, snaps[0])).toBe(true);
    expect(mx.iteration).toBe(g + 1);
    restoreGeneration(mx, mx.undo.undo(captureGeneration(mx)));
    expect(digestGeneration(mx)).toBe(before);
    const src = sourceFromSnapshot(snaps[0]);
    expect(src.count).toBe(snaps[0].count);
    expect(src.laws.lowFlags[0]).toBe(snaps[0].laws.lowFlags);
    stopMultiplex(mx);
  });
});

describe('D-044 PEEK + ANNEAL (AC-97 / AC-100)', () => {
  it('peek state toggles and clears on stop', () => {
    const mx = running(2);
    expect(PEEK_HOLD_MS).toBe(350);
    setPeek(mx, 1);
    expect(mx.peek).toBe(1);
    setPeek(mx, null);
    expect(mx.peek).toBe(null);
    setPeek(mx, 1);
    stopMultiplex(mx);
    expect(mx.peek).toBe(null);
  });
  it('anneal readout shows the factor and next variation, floored', () => {
    expect(annealReadout(0.4, 0.15)).toBe('×0.85/gen · NEXT 34.0%');
    expect(annealReadout(0.05, 0.15)).toBe('×0.85/gen · NEXT 5.0%');
    expect(annealReadout(0.4, 0)).toBe('OFF · CONSTANT');
  });
});
