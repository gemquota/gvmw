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
const cfg = { ...mxMod.MULTIPLEX_DEFAULTS, seed: 7, useWorkers: false, cols: 1, rows: 1, particlesPerSim: pop, variation: 0 };
const mx = mxMod.createMultiplex(null);
mxMod.startMultiplex(mx, { view, count: pop, dna, laws, speciesCount: 5 }, cfg, null);
const show = (label) => { const r = mxMod.getFitnessReport(mx); const bad = r.perShard.flatMap((s) => Object.entries(s.rawMetrics).filter(([, v]) => !Number.isFinite(v)).map(([k, v]) => `${s.id}.${k}=${v}`));
  console.log(label, 'avgDelta', r.avgDelta, 'sel', r.perShard[0].metrics.delta, 'nonfinite', bad.slice(0, 6).join(' '), 'shards', mx.shards.length); };
show('iter0');
for (let t = 0; t < steps; t++) { mxMod.stepMultiplex(mx, 1 / 60, 1, WORLD_SIZE); if (t % 50 === 49) show('step' + (t + 1)); }
// find non-finite particle fields
for (const sh of mx.shards) { let nf = {}; for (let i = 0; i < sh.count; i++) for (const [k, idx] of Object.entries(S)) { const v = sh.view[i * P + idx]; if (!Number.isFinite(v)) nf[k] = (nf[k] || 0) + 1; } if (Object.keys(nf).length) { console.log('shard', sh.id, 'nonfinite fields', JSON.stringify(nf)); } }
mxMod.iterateMultiplex(mx); show('after-iterate');
