// D-038/D-039 FIDELITY presets (PERFORMANCE › SPEED selector, multiplex GRID & PERF).
import { describe, it, expect } from 'vitest';
import {
  SPEED_FIDELITY_LEVELS, SPEED_SLIDER_KEYS, SPEED_FAST_PRESET, SPEED_LOW_PRESET, SPEED_LOWEST_PRESET, FIDELITY_LAW_COUNT,
  fidelityPreset, fidelityOf, migrateFidelityLevel, worldParamDef, createWorldParams,
} from '../../src/state/worldParams.js';
import { runSpeedWorld } from '../helpers/speedWorld.js';
import { PARTICLE_STRIDE, STRIDE_INDEXES as S } from '../../src/constants.js';

describe('FIDELITY presets (D-038/D-039)', () => {
  it('are HIGH / MEDIUM / LOW / LOWEST', () => {
    expect(SPEED_FIDELITY_LEVELS).toEqual(['HIGH', 'MEDIUM', 'LOW', 'LOWEST']);
  });
  it('HIGH = every speed slider at its default (= DEFAULTS), so a fresh world is HIGH', () => {
    const high = fidelityPreset('HIGH');
    for (const k of SPEED_SLIDER_KEYS) expect(high[k], k).toBe(worldParamDef(k).default);
    expect(fidelityOf(createWorldParams())).toBe('HIGH');
    expect(fidelityOf({})).toBe('HIGH');
  });
  it('HIGH is bit-identical to a world without the speed sliders', () => {
    const absent = runSpeedWorld({ params: Object.fromEntries(SPEED_SLIDER_KEYS.map((k) => [k, undefined])) });
    expect(runSpeedWorld({ params: fidelityPreset('HIGH') }).hash).toBe(absent.hash);
  });
  it('MEDIUM = the old FAST values', () => {
    expect(fidelityPreset('MEDIUM')).toEqual(SPEED_FAST_PRESET);
    expect(fidelityOf(SPEED_FAST_PRESET)).toBe('MEDIUM');
  });
  for (const [lv, preset] of [['LOW', SPEED_LOW_PRESET], ['LOWEST', SPEED_LOWEST_PRESET]]) {
    it(`${lv} sets every speed slider inside its range, and is detected`, () => {
      expect(fidelityPreset(lv)).toBe(preset);
      expect(Object.keys(preset).sort()).toEqual([...SPEED_SLIDER_KEYS].sort());
      for (const [k, v] of Object.entries(preset)) {
        expect(v, k).toBeGreaterThanOrEqual(worldParamDef(k).min);
        expect(v, k).toBeLessThanOrEqual(worldParamDef(k).max);
      }
      expect(fidelityOf(preset)).toBe(lv);
      expect(fidelityOf({ ...preset, SPEED_MID_RANGE: 61 })).toBe('CUSTOM');
    });
  }
  it('LOW is the milder D-039 cut (neighbour 24, pair budget 12), between MEDIUM and LOWEST', () => {
    expect(SPEED_LOW_PRESET.PAIRWISE_BUDGET).toBe(24);
    expect(SPEED_LOW_PRESET.SPEED_PAIR_BUDGET).toBe(12);
    // Higher = more fidelity for the limit/range sliders; lower = more fidelity for the cadences.
    for (const k of ['PAIRWISE_BUDGET', 'SPEED_MID_RANGE', 'SPEED_NEAR_RANGE', 'SPEED_PAIR_BUDGET', 'SPEED_SYMBIOSIS_RANGE']) {
      expect(SPEED_LOW_PRESET[k], k).toBeLessThanOrEqual(SPEED_FAST_PRESET[k]);
      expect(SPEED_LOW_PRESET[k], k).toBeGreaterThanOrEqual(SPEED_LOWEST_PRESET[k]);
    }
    for (const k of ['SPEED_SOCIAL_EVERY', 'SPEED_EXPENSIVE_EVERY']) {
      expect(SPEED_LOW_PRESET[k], k).toBeGreaterThanOrEqual(SPEED_FAST_PRESET[k]);
      expect(SPEED_LOW_PRESET[k], k).toBeLessThanOrEqual(SPEED_LOWEST_PRESET[k]);
    }
  });
  it('the four levels are all different', () => {
    const hashes = new Set(SPEED_FIDELITY_LEVELS.map((lv) => JSON.stringify(fidelityPreset(lv))));
    expect(hashes.size).toBe(4);
  });
  it('old D-038 LOW: slider values now read as LOWEST; an old level name LOW maps to LOWEST', async () => {
    const OLD_LOW = { PAIRWISE_BUDGET: 16, SPEED_MID_RANGE: 60, SPEED_NEAR_RANGE: 20, SPEED_PAIR_BUDGET: 8, SPEED_SYMBIOSIS_RANGE: 10, SPEED_SOCIAL_EVERY: 4, SPEED_EXPENSIVE_EVERY: 4 };
    expect(SPEED_LOWEST_PRESET).toEqual(OLD_LOW);
    const { parseWorldSave, restoreWorldState, WORLD_SAVE_FORMAT, WORLD_SAVE_VERSION } = await import('../../src/state/worldSave.js');
    const live = createWorldParams();
    restoreWorldState(parseWorldSave({ format: WORLD_SAVE_FORMAT, version: WORLD_SAVE_VERSION, particleCount: 0, speciesCount: 1, laws: { low: 0, high: 0, ext: 0, quad: 0, penta: 0 }, worldParams: { ...OLD_LOW } }), { worldParams: live });
    for (const [k, v] of Object.entries(OLD_LOW)) expect(live[k], k).toBe(v); // values unchanged
    expect(fidelityOf(live)).toBe('LOWEST');
    expect(migrateFidelityLevel('LOW', { preD039: true })).toBe('LOWEST');
    expect(migrateFidelityLevel('LOW')).toBe('LOW');
    expect(migrateFidelityLevel('bogus')).toBe('HIGH');
  });
  it('multiplex LAW COUNT: 136 for HIGH / MEDIUM, 48 for LOW, the 16-law light set for LOWEST', () => {
    expect(FIDELITY_LAW_COUNT).toEqual({ HIGH: 136, MEDIUM: 136, LOW: 48, LOWEST: 16 });
  });
  it.each(['MEDIUM', 'LOW', 'LOWEST'])('%s is deterministic and keeps a working sim (no NaN, everyone alive)', (lv) => {
    const a = runSpeedWorld({ params: fidelityPreset(lv), ticks: 20 });
    const b = runSpeedWorld({ params: fidelityPreset(lv), ticks: 20 });
    expect(a.hash).toBe(b.hash);
    expect(a.hash).not.toBe(runSpeedWorld({ params: {}, ticks: 20 }).hash);
    let alive = 0, bad = 0;
    for (let i = 0; i < 400; i++) {
      const b = i * PARTICLE_STRIDE;
      if (a.view[b + S.DEAD] < 0.5 && a.view[b + S.MASS] > 0) alive++;
      for (const k of [S.POS_X, S.POS_Y, S.POS_Z, S.VEL_X, S.ENERGY]) if (!Number.isFinite(a.view[b + k])) bad++;
    }
    expect(bad).toBe(0);
    expect(alive).toBe(400);
  });
});
