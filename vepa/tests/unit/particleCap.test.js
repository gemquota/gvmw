// D-040: engine particle cap back to 100,000; multiplex population basis kept at 10,000.
import { describe, it, expect } from 'vitest';
import { MAX_PARTICLES, MULTIPLEX_POP_BASE, PARTICLE_STRIDE } from '../../src/constants.js';
import { computeShardPopulationCap } from '../../src/multiplex/multiplex.js';
import { worldParamDef, clampWorldParam } from '../../src/state/worldParams.js';
import { createParticleBuffer } from '../../src/state/particleBuffer.js';

describe('D-040 particle cap', () => {
  it('engine cap is 100,000 and the world population params follow it', () => {
    expect(MAX_PARTICLES).toBe(100000);
    for (const k of ['PARTICLE_COUNT', 'INITIAL_POP', 'MAX_POP']) expect(worldParamDef(k).max).toBe(100000);
    expect(clampWorldParam('INITIAL_POP', 50000)).toBe(50000);
    expect(clampWorldParam('INITIAL_POP', 250000)).toBe(100000);
  });
  it('buffer is stride x 4 bytes x cap (40 MB at 100,000)', () => {
    expect(createParticleBuffer(MAX_PARTICLES, PARTICLE_STRIDE).buffer.byteLength).toBe(100000 * 100 * 4);
  });
  it('multiplex POP % and the auto curve keep their v9.3.1 particle counts', () => {
    expect(MULTIPLEX_POP_BASE).toBe(10000);
    expect(computeShardPopulationCap(4, 1, 25)).toBe(2500); // saved POP % 25 still = 2,500 per sim
    expect(computeShardPopulationCap(4, 1, 100)).toBe(10000);
    expect(computeShardPopulationCap(4)).toBe(5000);         // auto: 10,000 / sqrt(4)
    expect(computeShardPopulationCap(1)).toBe(10000);
    expect(computeShardPopulationCap(16, 0.5)).toBe(1250);
  });
});

import { clearParticleView } from '../../src/state/particleBuffer.js';
describe('D-040 clearParticleView', () => {
  it('is bit-identical to fill(0) (incl. -0 and NaN in the tail)', () => {
    for (const tail of [[], [-0], [NaN], [0, 0, -0, 0], [1e-30]]) {
      const a = new Float32Array(64), b = new Float32Array(64);
      for (let i = 0; i < 20; i++) a[i] = b[i] = (i % 3) - 1.5;
      tail.forEach((v, k) => { a[40 + k] = b[40 + k] = v; });
      a.fill(0); clearParticleView(b);
      expect(new Uint8Array(b.buffer)).toEqual(new Uint8Array(a.buffer));
    }
  });
  it('returns how much it zeroed (stops at the last non +0 float)', () => {
    const v = new Float32Array(100); v[9] = 2; expect(clearParticleView(v)).toBe(10); expect(clearParticleView(v)).toBe(0);
  });
});
