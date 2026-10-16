// usage: node solve-bench.mjs <N> <ticks> [world]
const N = Number(process.argv[2] || 300), TICKS = Number(process.argv[3] || 40), WORLD = Number(process.argv[4] || 1200);
const R = '/workspace/vepa/src';
const { PARTICLE_STRIDE, STRIDE_INDEXES: S, DNA_RANGES, LAW_INDEXES } = await import(R + '/constants.js');
const { createLawState, set: setLaw } = await import(R + '/state/lawState.js');
const { createDNABuffer, loadDefaults, setDNAFloat, getDNAFloat } = await import(R + '/dna/dnaBuffer.js');
const { solve, drainOffspring } = await import(R + '/physics/solver.js');
const { TIDAL_BLOOM } = await import(R + '/state/defaultPresets.js');
const { runtimeConfig } = await import(R + '/state/runtimeConfig.js');
const { createWorldParams } = await import(R + '/state/worldParams.js');
let s0 = 12345; const rng = () => ((s0 = (s0 * 1664525 + 1013904223) >>> 0) / 4294967296);
runtimeConfig.worldParams = { ...createWorldParams(), ...TIDAL_BLOOM.worldParams };
const view = new Float32Array(N * 2 * PARTICLE_STRIDE);
const dna = createDNABuffer(); loadDefaults(dna, DNA_RANGES);
for (let s = 0; s < 5; s++) for (let d = 0; d < 42; d++) { const r = DNA_RANGES[d] || { min: -1, max: 1 }; setDNAFloat(dna, s, d, r.min + rng() * (r.max - r.min), r.min, r.max); }
for (let i = 0; i < N; i++) {
  const b = i * PARTICLE_STRIDE, s = i % 5;
  view[b + S.POS_X] = rng() * WORLD; view[b + S.POS_Y] = rng() * WORLD; view[b + S.POS_Z] = rng() * WORLD;
  view[b + S.MASS] = 1 + rng(); view[b + S.SPECIES_ID] = s; view[b + S.ENERGY] = 50 + rng() * 50; view[b + S.RADIUS] = 0.6 + rng() * 0.6;
  for (let k = 1; k <= 4; k++) view[b + S['BOND_PARTNER_' + k]] = -1;
  for (let d = 0; d < 42; d++) { const r = DNA_RANGES[d] || { min: -1, max: 1 }; view[b + S.DNA_CACHE_START + d] = getDNAFloat(dna, s, d, r.min, r.max); }
}
const laws = createLawState(); for (const n of TIDAL_BLOOM.laws) setLaw(laws, LAW_INDEXES[n]);
const times = [];
for (let t = 0; t < TICKS; t++) { const a = performance.now(); solve(view, N, PARTICLE_STRIDE, laws, dna, WORLD, 1 / 60, rng); drainOffspring(); times.push(performance.now() - a); }
times.sort((a, b) => a - b);
console.log(JSON.stringify({ N, WORLD, laws: TIDAL_BLOOM.laws.length, p50ms: +times[times.length >> 1].toFixed(2), meanMs: +(times.reduce((a, b) => a + b) / times.length).toFixed(2) }));
