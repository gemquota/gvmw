# Golden-parity re-baseline log

## 2026-10-03: FIELD-ONCE on by default (D-016, AC-96)

**Change.** `runtimeConfig.fieldAdvanceOnce` now defaults to `true`. The field medium (`advanceFields`: diffusion, decay, advection) advances once per `solve()`, after the particle loop. Before this, the call sat inside the per-particle loop and ran N times per tick.

**Fixture impact.** The 12 existing scenarios run with default world params, where every `FIELD_*` value is 0 and the fields are off. Their hashes are **unchanged**. None of them exercised the field medium, which is why FIELD-ONCE went unnoticed.

To cover the change, one scenario was **added**, appended at the end so the earlier scenarios keep their seeds:

| Scenario | Legacy hash (per-particle advance, `GOLDEN_FIELD_LEGACY=1`) | New hash (D-016) |
|---|---|---|
| `default-tidal-bloom-params` | `5fd1fb81c0b138e83cb05d93d394469ea01f62f85f3e659e607784ca2d7d4ee7` | `fafed453f83a75b1666a31bfa77c55a106681bc6a9b67766cf28987a75f158ac` |

Old hashes of the unchanged scenarios, for reference: `none` 890b7a5c…, `default-tidal-bloom` 6ec06791…, `all-laws` 288ccae7…. The full list is in git history at 362fdce, `tests/fixtures/golden-parity.json`.

To reproduce the legacy hash:

    GOLDEN_FIELD_LEGACY=1 node scripts/golden-parity.mjs

**Behaviour impact.** Worlds with any `FIELD_*` parameter above 0 now evolve their medium at the intended rate. This includes the TIDAL_BLOOM boot world (FIELD_THERMAL 0.75, FIELD_INFO 0.6). Thermal and info gradients are therefore smoother and slower than before. The legacy behaviour stays available by setting `runtimeConfig.fieldAdvanceOnce = false`.

## 2026-10-09: upstream v9.2.0 WRAP law decides the world boundary (D-031 merge, D-032)

**Change (upstream, not ours).** Merging `origin/main` v9.2.0–v9.3.1 into `codey/complete-plans` brings upstream's INERTIA→WRAP rename: law 130 is now WRAP, and the solver's boundary step reads the WRAP law bit (`applyWrapBoundary(..., active[LAW_INDEXES.WRAP], ...)`) instead of the TOROIDAL EDGES world param. In the app, `syncWrapLaw` seeds the bit from TOROIDAL (default 1) at boot and on every `law:sync`. The harness passes each scenario's law list exactly, so scenarios whose list has no WRAP now run with walls (WALL REFLECT 1) instead of wrapping.

**Attribution check.** With the merged tree and only the boundary decision put back to the TOROIDAL param, all 13 scenarios reproduce the previous fixture exactly. So every hash change below comes from upstream's WRAP change. None comes from the local branch or from merge resolutions, and the harness itself is unchanged.

| Scenario | Previous hash | New hash |
|---|---|---|
| `default-tidal-bloom` | `6ec06791cec0…` | `104721a8fb53…` |
| `category-physics` | `6c5f1f56a3d0…` | `eb2640f06a41…` |
| `category-biology` | `336aa4416410…` | `e0cac94d8391…` |
| `category-quantum` | `27a5eed83946…` | `08861b63cd23…` |
| `default-tidal-bloom-params` | `fafed453f83a…` | `a0bd3b350bda…` |

The other 8 scenarios (`none`, `all-laws`, `category-mechanics`, which includes WRAP, and the five remaining categories) are unchanged. Upstream ships no golden fixture, so there were no upstream references to adopt; this re-record is the upstream behaviour change, recorded locally. Full previous list: `tests/fixtures/golden-parity.json` at `e8bce6a`.

## 2026-10-09: GENOTYPE keeps somatic DNA inside its declared ranges (D-035)

**Bug.** `applyGenotypeMutation` (law 48) random-walked a particle's DNA cache (somatic drift, epigenetic drift, gene flow, transposon jump) with no clamp. Loci drifted outside `DNA_RANGES`; `MEMORY_DECAY` (0.9–1) went negative, and the SIGNAL/MEMORY decay step's `Math.pow(MEMORY_DECAY, dt)` then returned NaN. NaN spread to SIGNAL and, through signal costs, to ENERGY. This is the "15 alive particles with NaN energy" seen with option 3 at 1,000 × 600, but it is not option-specific: the seeded 200 × 120 world in `tests/unit/nanEnergy.test.js` had 7 non-finite fields with every speed option off.

**Fix.** Every GENOTYPE write now goes through `writeSomaticLocus`, which clamps to the locus's `DNA_RANGES` and keeps the old value if the result is non-finite.

**Fixture impact.** Only the three scenarios with GENOTYPE on change. Within their 30 ticks the clamp fired about 2,500 times per scenario across 30+ loci (most often locus 27 and locus 40, MEMORY_DECAY, about 280–370 times each). Offspring counts are unchanged (0).

| Scenario | Previous hash | New hash |
|---|---|---|
| `default-tidal-bloom` | `104721a8fb53…` | `1bfffe1464de…` |
| `all-laws` | `288ccae7eb99…` | `39d69ef19f3b…` |
| `default-tidal-bloom-params` | `a0bd3b350bda…` | `4ccaed96ba4e…` |

The other 10 scenarios are unchanged.

## 2026-10-09: MIND floors the pair distance at 0.01 (D-035)

**Bug.** `applyMind` (law 37) returned `signalBoost = 0.01 × synergy / sqrt(distSq)`. For two same-species particles at exactly the same position (distSq 0) that is Infinity, and SIGNAL went to Infinity. Later steps then turned it into NaN (Infinity − Infinity, 0 × Infinity). The NaN hunt found this as the first non-finite write with FAST on (tick 3–5 at 1k, 2.5k and 10k), once the GENOTYPE fix was in.

**Fix.** The distance is floored at 0.01, as COMMS already does (`1 / max(dist, 0.01)`). The boost is unchanged for pairs further apart than 0.01.

**Fixture impact.** Three scenarios change. The floor applied 1 time in `default-tidal-bloom`, 378 times in `all-laws` (12 exact zeros) and 190 times in `default-tidal-bloom-params` (9 exact zeros), over 30 ticks. Offspring counts are unchanged (0).

| Scenario | Previous hash (after GENOTYPE fix) | New hash |
|---|---|---|
| `default-tidal-bloom` | `1bfffe1464de…` | `964e85bd6fc1…` |
| `all-laws` | `39d69ef19f3b…` | `c2db070d1864…` |
| `default-tidal-bloom-params` | `4ccaed96ba4e…` | `1b6560e2d4cc…` |

## 2026-10-16: upstream v9.3.3 / v9.3.4 contact hardening, merged (D-041)

**Source.** Upstream `origin/main` (79efba7), merged into `codey/complete-plans`. The physics changes are upstream's `2e6027a` (v9.3.3 "stage configuration safely and harden contact") and `534cfdb` (v9.3.4): the new final hard-contact pass `resolveParticleContacts` (src/physics/contactConstraints.js) after all motion when CONTACT/COLL/ACCR/BOND/POLYMER/ADHESION is on, ACCR seam refresh against final radii, ACCR dwell at touching (overlap ≥ -0.001), POLYMER force now applied and surface-based rest length plus POLYMER_LIMIT, BOND rest length scaled by BOND_ANGLE, ADHESION surface-gap closing, zero-distance CONTACT correction, and AFFINITY bond pull only for bonded pairs. (v9.3.4's uniform spawn height is not used by the golden harness, which places particles itself.)

**Attribution check.** Reverse-applying only upstream's 031ca5e..79efba7 diff of `src/physics/solver.js`, `src/physics/laws.js` and `src/physics/lawgroups/mechanicsLaws.js` to the merged tree gives `golden-parity: OK (13 scenarios identical)` against the pre-merge fixture. So every change below comes from upstream; this branch's side of the merge changes none.

| Scenario | Previous hash | New hash |
|---|---|---|
| `default-tidal-bloom` | `964e85bd6fc1…` | `08e8d279295f…` |
| `all-laws` | `c2db070d1864…` | `3633c54053cb…` |
| `category-physics` | `eb2640f06a41…` | `8b3409938987…` |
| `category-mechanics` | `50a962e6375d…` | `fc2c2fa361f4…` |
| `category-chemistry` | `b28fb59cb257…` | `ecddb3dd4bb9…` |
| `default-tidal-bloom-params` | `1b6560e2d4cc…` | `17b794fa2870…` |

Unchanged: `none`, `category-biology`, `category-thermodynamics`, `category-metaphysics`, `category-electromagnetism`, `category-information`, `category-quantum` (none of the touched laws is on in them). Offspring 0 in all, as before.
