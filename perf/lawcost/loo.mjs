// Leave-one-out law cost: all-laws bench world (bench:solver setup), N particles.
// usage: node loo.mjs ROOT COUNT TICKS WARM [LAW|none]
const [ROOT, COUNT, TICKS, WARM, DROP] = [process.argv[2], +process.argv[3], +process.argv[4], +process.argv[5], process.argv[6] || 'none'];
let s = 0x9e3779b9 ^ COUNT;
const rng = () => { s = (Math.imul(s, 1664525) + 1013904223) >>> 0; return s / 4294967296; };
let m = 0x5bd1e995; Math.random = () => { m = (Math.imul(m, 1103515245) + 12345) >>> 0; return m / 4294967296; };
const { PARTICLE_STRIDE, STRIDE_INDEXES: S, DNA_RANGES, LAW_INDEXES, WORLD_SIZE } = await import(ROOT + '/src/constants.js');
const { createLawState, set: setLaw } = await import(ROOT + '/src/state/lawState.js');
const { createDNABuffer, loadDefaults, setDNAFloat, getDNAFloat } = await import(ROOT + '/src/dna/dnaBuffer.js');
const { solve, drainOffspring, resetOffspringRing, resetSolverState } = await import(ROOT + '/src/physics/solver.js');
const { TIDAL_BLOOM } = await import(ROOT + '/src/state/defaultPresets.js');
const { runtimeConfig } = await import(ROOT + '/src/state/runtimeConfig.js');
const wp = await import(ROOT + '/src/state/worldParams.js');
runtimeConfig.worldParams = { ...wp.createWorldParams(), ...(TIDAL_BLOOM.worldParams || {}) };
const WORLD = WORLD_SIZE;
const view = new Float32Array(COUNT * 2 * PARTICLE_STRIDE);
const dna = createDNABuffer(); loadDefaults(dna, DNA_RANGES);
for (let sp = 0; sp < 5; sp++) for (let d = 0; d < 42; d++) { const r = DNA_RANGES[d] || { min: -1, max: 1 }; setDNAFloat(dna, sp, d, r.min + rng() * (r.max - r.min), r.min, r.max); }
for (let i = 0; i < COUNT; i++) {
  const b = i * PARTICLE_STRIDE, sp = i % 5;
  view[b + S.POS_X] = rng() * WORLD; view[b + S.POS_Y] = rng() * WORLD; view[b + S.POS_Z] = rng() * WORLD;
  view[b + S.MASS] = 1 + rng(); view[b + S.SPECIES_ID] = sp; view[b + S.ENERGY] = 50 + rng() * 50; view[b + S.RADIUS] = 0.6 + rng() * 0.6;
  view[b + S.BOND_PARTNER_1] = -1; view[b + S.BOND_PARTNER_2] = -1; view[b + S.BOND_PARTNER_3] = -1; view[b + S.BOND_PARTNER_4] = -1;
  for (let d = 0; d < 42; d++) { const r = DNA_RANGES[d] || { min: -1, max: 1 }; view[b + S.DNA_CACHE_START + d] = getDNAFloat(dna, sp, d, r.min, r.max); }
}
const laws = createLawState();
for (const n of Object.keys(LAW_INDEXES)) if (n !== DROP) setLaw(laws, LAW_INDEXES[n]);
resetOffspringRing(); resetSolverState(0);
const step = () => { solve(view, COUNT, PARTICLE_STRIDE, laws, dna, WORLD, 1 / 60, rng); drainOffspring(); };
for (let t = 0; t < WARM; t++) step();
const times = [];
for (let t = 0; t < TICKS; t++) { const t0 = performance.now(); step(); times.push(performance.now() - t0); }
times.sort((a, b) => a - b);
console.log(JSON.stringify({ drop: DROP, medMs: times[times.length >> 1] }));
