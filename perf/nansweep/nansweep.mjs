import { createHash } from 'node:crypto';
const argv = process.argv.slice(2);
const ROOT = argv.shift();
{
  const COUNT = Number(argv[1]); const TICKS = Number(argv[2]); const WARM = Number(argv[3]); const LAWS = argv[4];
  const SPEED = argv[5] && argv[5] !== 'none' ? argv[5] : '';
  const SPECIES = 5;
  let s = 0x9e3779b9 ^ COUNT;
  const rng = () => { s = (Math.imul(s, 1664525) + 1013904223) >>> 0; return s / 4294967296; };
  let m = 0x5bd1e995; Math.random = () => { m = (Math.imul(m, 1103515245) + 12345) >>> 0; return m / 4294967296; };
  const { PARTICLE_STRIDE, STRIDE_INDEXES: S, DNA_RANGES, LAW_INDEXES, WORLD_SIZE } = await import(ROOT + '/src/constants.js');
  const { createLawState, set: setLaw } = await import(ROOT + '/src/state/lawState.js');
  const { createDNABuffer, loadDefaults, setDNAFloat, getDNAFloat } = await import(ROOT + '/src/dna/dnaBuffer.js');
  const SOL = await import(ROOT + '/src/physics/solver.js'); const { solve, drainOffspring, resetOffspringRing } = SOL;
  const { TIDAL_BLOOM } = await import(ROOT + '/src/state/defaultPresets.js');
  const { runtimeConfig } = await import(ROOT + '/src/state/runtimeConfig.js');
  const wp = await import(ROOT + '/src/state/worldParams.js');
  const WORLD = WORLD_SIZE;
  runtimeConfig.worldParams = { ...wp.createWorldParams(), ...(TIDAL_BLOOM.worldParams || {}) };
  if (SPEED) {
    const keys = SPEED === 'all' ? wp.SPEED_PARAM_KEYS : SPEED.split(',');
    for (const k of keys) {
      if (!wp.SPEED_PARAM_KEYS.includes(k)) { console.error(`unknown speed option ${k}`); process.exit(2); }
      runtimeConfig.worldParams[k] = 1;
    }
  }
  const view = new Float32Array(COUNT * 2 * PARTICLE_STRIDE);
  const dna = createDNABuffer(); loadDefaults(dna, DNA_RANGES);
  for (let sp = 0; sp < SPECIES; sp++) for (let d = 0; d < 42; d++) {
    const r = DNA_RANGES[d] || { min: -1, max: 1 };
    setDNAFloat(dna, sp, d, r.min + rng() * (r.max - r.min), r.min, r.max);
  }
  for (let i = 0; i < COUNT; i++) {
    const b = i * PARTICLE_STRIDE, sp = i % SPECIES;
    view[b + S.POS_X] = rng() * WORLD; view[b + S.POS_Y] = rng() * WORLD; view[b + S.POS_Z] = rng() * WORLD;
    view[b + S.MASS] = 1 + rng(); view[b + S.SPECIES_ID] = sp; view[b + S.ENERGY] = 50 + rng() * 50;
    view[b + S.RADIUS] = 0.6 + rng() * 0.6;
    view[b + S.BOND_PARTNER_1] = -1; view[b + S.BOND_PARTNER_2] = -1; view[b + S.BOND_PARTNER_3] = -1; view[b + S.BOND_PARTNER_4] = -1;
    for (let d = 0; d < 42; d++) { const r = DNA_RANGES[d] || { min: -1, max: 1 }; view[b + S.DNA_CACHE_START + d] = getDNAFloat(dna, sp, d, r.min, r.max); }
  }
  const laws = createLawState();
  const names = LAWS === 'all' ? Object.keys(LAW_INDEXES) : TIDAL_BLOOM.laws;
  for (const n of names) if (LAW_INDEXES[n] !== undefined) setLaw(laws, LAW_INDEXES[n]);
  if (LAWS !== 'all' && wp.syncWrapLaw) wp.syncWrapLaw(runtimeConfig.worldParams, laws);
  resetOffspringRing();
  const h = createHash('sha256');
  let born = 0;
  const step = () => { solve(view, COUNT, PARTICLE_STRIDE, laws, dna, WORLD, 1 / 60, rng); for (const o of drainOffspring()) { born++; h.update(JSON.stringify(o)); } };
  for (let t = 0; t < WARM; t++) step();
  const times = [];
  for (let t = 0; t < TICKS; t++) { const t0 = performance.now(); step(); times.push(performance.now() - t0); }
  h.update(Buffer.from(view.buffer, 0, COUNT * PARTICLE_STRIDE * 4));
  times.sort((a, b) => a - b);
  let alive = 0, nanEnergy = 0, badFields = 0, badParticles = 0, infFields = 0;
  for (let i = 0; i < COUNT * 2; i++) {
    const b = i * PARTICLE_STRIDE;
    if (!(view[b + S.DEAD] < 0.5 && view[b + S.MASS] > 0)) continue;
    alive++; if (!Number.isFinite(view[b + S.ENERGY])) nanEnergy++;
    let bad = 0; for (let k = 0; k < PARTICLE_STRIDE; k++) { const v = view[b + k]; if (!Number.isFinite(v)) { bad++; if (v === Infinity || v === -Infinity) infFields++; } }
    if (bad) { badParticles++; badFields += bad; }
  }
  const repairs = SOL.getNonFiniteRepairCount ? SOL.getNonFiniteRepairCount() : null;
  process.stdout.write(JSON.stringify({ root: ROOT.split('/').pop(), count: COUNT, ticks: TICKS, speed: SPEED || 'off', alive, nanEnergy, badParticles, badFields, infFields, repairs }) + '\n');
  process.exit(0);
}

