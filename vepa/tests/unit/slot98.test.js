// D-042: stride slot 98 is ACCR_LINK_MASK only; Set P synthetic flags + program
// live packed in SYNTHETIC_TAG (99). Before the fix both wrote 98.
import { describe, it, expect } from 'vitest';
import { PARTICLE_STRIDE as P, STRIDE_INDEXES as S } from '../../src/constants.js';
import { adjoinParticles, isAccretionPair } from '../../src/physics/mergePhysics.js';
import {
  OFFSET_SYNTHETIC_TAG, OFFSET_SYNTHETIC_FLAGS, SYN_FLAG_SYNTHETIC, SYN_FLAG_MACHINE,
  packSyntheticTag, syntheticFlagsOf, syntheticProgramOf,
} from '../../src/state/synthetic.js';

const BONDS = ['BOND_PARTNER_1', 'BOND_PARTNER_2', 'BOND_PARTNER_3', 'BOND_PARTNER_4', 'BOND_PARTNER_5', 'BOND_PARTNER_6'];
function view(n) {
  const v = new Float32Array(n * P);
  for (let i = 0; i < n; i++) { for (const b of BONDS) v[i * P + S[b]] = -1; v[i * P + S.MASS] = 1; v[i * P + S.RADIUS] = 1; v[i * P + S.POS_X] = i * 2; }
  return v;
}

describe('D-042 slot 98 / 99 split', () => {
  it('the two fields have their own slots, inside the stride', () => {
    expect(S.ACCR_LINK_MASK).toBe(98);
    expect(S.SYNTHETIC_TAG).toBe(99);
    expect(OFFSET_SYNTHETIC_TAG).toBe(99);
    expect(OFFSET_SYNTHETIC_FLAGS).not.toBe(S.ACCR_LINK_MASK);
    const vals = Object.values(S); expect(new Set(vals).size).toBe(vals.length);
    expect(Math.max(...vals)).toBeLessThan(P);
  });
  it('packs flags (low nibble) and program (high nibble) exactly', () => {
    for (let prog = 0; prog < 8; prog++) {
      const v = new Float32Array(P); v[OFFSET_SYNTHETIC_TAG] = packSyntheticTag(SYN_FLAG_SYNTHETIC | SYN_FLAG_MACHINE, prog);
      expect(syntheticFlagsOf(v, 0)).toBe(SYN_FLAG_SYNTHETIC | SYN_FLAG_MACHINE);
      expect(syntheticProgramOf(v, 0)).toBe(prog);
    }
  });
  it('an ACCR seam does not make a particle look synthetic, and a synthetic tag does not create seams', () => {
    const v = view(2);
    adjoinParticles(v, 0, P, P);
    expect(isAccretionPair(v, 0, P, P)).toBe(true);
    expect(v[S.ACCR_LINK_MASK] & 1).toBe(1);            // seam in slot 1 sets bit 0 (= old SYN_FLAG_SYNTHETIC)
    expect(syntheticFlagsOf(v, 0) & SYN_FLAG_SYNTHETIC).toBe(0);
    v[S.SYNTHETIC_TAG] = packSyntheticTag(SYN_FLAG_SYNTHETIC | SYN_FLAG_MACHINE, 3);
    expect(v[S.ACCR_LINK_MASK]).toBe(1);                // seam bits untouched
    expect(isAccretionPair(v, 0, P, P)).toBe(true);
  });
});
