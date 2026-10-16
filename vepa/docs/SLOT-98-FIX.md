# Stride slot 98 collision fix (D-042, 2026-10-16)

## The bug

Stride slot 98 had two owners since the initial import:

- `STRIDE_INDEXES.ACCR_LINK_MASK = 98` (src/constants/stride.js): bit n set means bond slot n (BOND_PARTNER_1..6) is an ACCR seam. Written by `adjoinParticles` (`|= 1 << n`) and `breakBondPair` (`&= ~(1 << n)`) in src/physics/mergePhysics.js; read by `isAccretionPair` (mergePhysics.js), which the solver uses for ACCR seam maintenance (including upstream v9.3.3's seam refresh), fusion exclusion and the contact pass; cleared on spawn/birth in src/main.js and on multiplex respawn; saved/restored in particleBuffer.js and world saves.
- `OFFSET_SYNTHETIC_FLAGS = 98` (src/state/synthetic.js, Set P): bit 1 SYNTHETIC, 2 UPLOADED, 4 MACHINE. Written by the P.1 synthetic spawn (`= SYNTHETIC | MACHINE` = 5); read by the P.2 upload scan (`& SYNTHETIC`, skip synthetics). Slot 99 held the program index.

## What broke

- **ACCR → Set P:** an ACCR seam in bond slot 1 sets bit 0 of slot 98, which the upload scan reads as SYNTHETIC. Real accreted particles were skipped as upload sources (uploaded consciousness picked other particles or skipped species whose scanned particles were seamed). Seams in slots 2 and 3 set the UPLOADED and MACHINE bits.
- **Set P → ACCR:** a synthetic spawn writes 5 into slot 98, which `isAccretionPair` reads as ACCR seams on bond slots 1 and 3 of that particle. The spawn does not reset the bond partners, so stale partner indices plus those bits could make a phantom seam. ACCR `breakBondPair` could also clear bit 0, so the particle stopped counting as synthetic.
- In practice the second path rarely reached the simulation: the synthetic spawn writes the particle at index `count` but nothing raises `particleCount` (separate bug, not fixed here), so the slot is overwritten by the next birth, which already resets slot 98 (but did not reset 99).

## The fix

The stride has no spare slot (0–7 core, 8–49 DNA cache, 50–98 named, 99 = synthetic trait), and growing the stride would change every buffer, save and multiplex shard. Instead the synthetic flags and program index are packed into one slot: `STRIDE_INDEXES.SYNTHETIC_TAG = 99` = flags (low nibble) | program << 4 (exact in float32). Slot 98 is ACCR only. `OFFSET_SYNTHETIC_FLAGS` / `OFFSET_SYNTHETIC_TRAIT` now point at 99 (kept for imports); reads go through `syntheticFlagsOf` / `syntheticProgramOf`. Births (three spawn paths in main.js) and multiplex respawn clear 99 as they already cleared 98.

## Impact

- Golden: 13/13 identical (the synthetic pass is not part of the solver). Bench hashes unchanged.
- Default behaviour: unchanged in the solver. Set P now ignores ACCR seams when choosing upload sources, and ACCR no longer sees synthetic flags as seams.
- Old saves: slot 99 used to hold a bare program index (0–7) only on synthetic particles, which in practice were never inside `particleCount`. A stale value left on a reused slot could now read as flags; births now clear it.
