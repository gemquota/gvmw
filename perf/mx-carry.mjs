// Reproduce NaN deltas: run a small multiplex in-thread and inspect the report.
const { PARTICLE_STRIDE: P, STRIDE_INDEXES: S, DNA_RANGES, LAW_INDEXES, WORLD_SIZE } = await import('/workspace/vepa/src/constants.js');
const { createLawState, set: setLaw } = await import('/workspace/vepa/src/state/lawState.js');
const { createDNABuffer, loadDefaults, getDNAFloat } = await import('/workspace/vepa/src/dna/dnaBuffer.js');
const { TIDAL_BLOOM } = await import('/workspace/vepa/src/state/defaultPresets.js');
const { runtimeConfig } = await import('/workspace/vepa/src/state/runtimeConfig.js');
const { createWorldParams } = await import('/workspace/vepa/src/state/worldParams.js');
const mxMod = await import('/workspace/vepa/src/multiplex/multiplex.js');
const { SplitMix32 } = await import('/workspace/vepa/src/core/prng.js');
const pop = +(process.argv[2] || 600), steps = +(process.argv[3] || 40);
const g = new SplitMix32(1);
const view = new Float32Array(pop * P); const dna = createDNABuffer(); loadDefaults(dna, DNA_RANGES);
for (let i = 0; i < pop; i++) { const b = i * P, s = i % 5;
  view[b + S.POS_X] = g.nextFloat(5, WORLD_SIZE - 5); view[b + S.POS_Y] = g.nextFloat(5, WORLD_SIZE - 5); view[b + S.POS_Z] = g.nextFloat(5, WORLD_SIZE - 5);
  view[b + S.MASS] = 1 + g.next(); view[b + S.ENERGY] = 50 + g.next() * 50; view[b + S.RADIUS] = 0.6; view[b + S.SPECIES_ID] = s;
  for (let k = 1; k <= 6; k++) view[b + S['BOND_PARTNER_' + k]] = -1;
  for (let d = 0; d < 42; d++) { const r = DNA_RANGES[d] || { min: -1, max: 1 }; view[b + S.DNA_CACHE_START + d] = getDNAFloat(dna, s, d, r.min, r.max); } }
const laws = createLawState(); for (const n of TIDAL_BLOOM.laws) if (LAW_INDEXES[n] !== undefined) setLaw(laws, LAW_INDEXES[n]);
runtimeConfig.worldParams = { ...createWorldParams(), ...TIDAL_BLOOM.worldParams };
const cfg = { ...mxMod.MULTIPLEX_DEFAULTS, seed: 7, useWorkers: false };
const mx = mxMod.createMultiplex(null);
mxMod.startMultiplex(mx, { view, count: pop, dna, laws, speciesCount: 5 }, cfg, null);
const show = (label) => { const r = mxMod.getFitnessReport(mx); const bad = r.perShard.flatMap((s) => Object.entries(s.rawMetrics).filter(([, v]) => !Number.isFinite(v)).map(([k, v]) => `${s.id}.${k}=${v}`));
  console.log(label, 'avgDelta', r.avgDelta, 'sel', r.perShard[0].metrics.delta, 'nonfinite', bad.slice(0, 6).join(' '), 'shards', mx.shards.length); };


// find non-finite particle fields


const alive = (sh) => { let a = 0; for (let i = 0; i < sh.count; i++) if (sh.view[i * P + S.DEAD] < 0.5) a++; return a; };
console.log('cap', mx.populationCap, 'gen0 alive', mx.shards.map(alive).join(','));
const s0 = mx.shards[mx.selected]; for (let i = 0; i < s0.count; i += 2) s0.view[i * P + S.DEAD] = 1; // kill half of the selected shard
console.log('selected after kill', alive(s0), 'count', s0.count);
mxMod.iterateMultiplex(mx, { manual: true });
console.log('gen1 alive', mx.shards.map(alive).join(','), 'counts', mx.shards.map((s) => s.count).join(','));
