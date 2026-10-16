// pair-distance histogram on the bench:solver world (TIDAL_BLOOM), via pairProbe
process.chdir('/workspace/vepa');
const COUNT = Number(process.argv[2] || 1000), TICKS = Number(process.argv[3] || 10);
const R = '/workspace/vepa/src/';
const { PARTICLE_STRIDE, STRIDE_INDEXES: S, DNA_RANGES, LAW_INDEXES, WORLD_SIZE } = await import(R + 'constants.js');
const { createLawState, set: setLaw } = await import(R + 'state/lawState.js');
const { createDNABuffer, loadDefaults, setDNAFloat, getDNAFloat } = await import(R + 'dna/dnaBuffer.js');
const { solve, drainOffspring } = await import(R + 'physics/solver.js');
const { TIDAL_BLOOM } = await import(R + 'state/defaultPresets.js');
const { runtimeConfig } = await import(R + 'state/runtimeConfig.js');
const wp = await import(R + 'state/worldParams.js');
let s = 0x9e3779b9 ^ COUNT; const rng = () => { s = (Math.imul(s, 1664525) + 1013904223) >>> 0; return s / 4294967296; };
runtimeConfig.worldParams = { ...wp.createWorldParams(), ...(TIDAL_BLOOM.worldParams || {}) };
const view = new Float32Array(COUNT * 2 * PARTICLE_STRIDE); const dna = createDNABuffer(); loadDefaults(dna, DNA_RANGES);
for (let sp = 0; sp < 5; sp++) for (let d = 0; d < 42; d++) { const r = DNA_RANGES[d] || { min: -1, max: 1 }; setDNAFloat(dna, sp, d, r.min + rng() * (r.max - r.min), r.min, r.max); }
for (let i = 0; i < COUNT; i++) { const b = i * PARTICLE_STRIDE, sp = i % 5;
  view[b + S.POS_X] = rng() * WORLD_SIZE; view[b + S.POS_Y] = rng() * WORLD_SIZE; view[b + S.POS_Z] = rng() * WORLD_SIZE;
  view[b + S.MASS] = 1 + rng(); view[b + S.SPECIES_ID] = sp; view[b + S.ENERGY] = 50 + rng() * 50; view[b + S.RADIUS] = 0.6 + rng() * 0.6;
  for (const k of ['BOND_PARTNER_1','BOND_PARTNER_2','BOND_PARTNER_3','BOND_PARTNER_4']) view[b + S[k]] = -1;
  for (let d = 0; d < 42; d++) { const r = DNA_RANGES[d] || { min: -1, max: 1 }; view[b + S.DNA_CACHE_START + d] = getDNAFloat(dna, sp, d, r.min, r.max); } }
const laws = createLawState(); for (const n of TIDAL_BLOOM.laws) if (LAW_INDEXES[n] !== undefined) setLaw(laws, LAW_INDEXES[n]);
if (wp.syncWrapLaw) wp.syncWrapLaw(runtimeConfig.worldParams, laws);
const edges = [5, 10, 20, 30, 40, 60, 80, 100, 120, 150, 200, 1e9]; const h = new Array(edges.length).fill(0); let tot = 0;
for (let t = 0; t < TICKS; t++) { if (t === TICKS - 3) runtimeConfig.pairProbe = (kind, v, a, b, w, p) => { if (kind !== 'pair') return; tot++; let k = 0; while (p.dist >= edges[k]) k++; h[k]++; };
  solve(view, COUNT, PARTICLE_STRIDE, laws, dna, WORLD_SIZE, 1 / 60, rng); drainOffspring(); }
let cum = 0; console.log(`N=${COUNT} world=${WORLD_SIZE} pairs/tick=${(tot / 3) | 0}`);
edges.forEach((e, k) => { cum += h[k]; console.log(`  < ${e === 1e9 ? 'inf' : e}: ${(100 * cum / tot).toFixed(1)}%`); });
