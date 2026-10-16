// Timeline: ONE run per (size, level), sampling behaviour at fixed ticks. Same world/seed as bench/solver-tps.mjs.
// usage: node timeline.mjs COUNT level MAXTICK out.csv
import fs from 'node:fs';
const COUNT = Number(process.argv[2]); const SPEED = process.argv[3]; const MAXT = Number(process.argv[4]); const OUT = process.argv[5]; const LAWS = 'tidal';
const SAMPLES = [50,100,150,200,250,300,350,400,450,500,600,700,800,900,1000,1200,1400,1600,1800,2000].filter((t) => t <= MAXT);
  const SPECIES = 5;
  let s = 0x9e3779b9 ^ COUNT;
  const rng = () => { s = (Math.imul(s, 1664525) + 1013904223) >>> 0; return s / 4294967296; };
  let m = 0x5bd1e995; Math.random = () => { m = (Math.imul(m, 1103515245) + 12345) >>> 0; return m / 4294967296; };
  const { PARTICLE_STRIDE, STRIDE_INDEXES: S, DNA_RANGES, LAW_INDEXES, WORLD_SIZE } = await import('/workspace/vepa/src/constants.js');
  const { createLawState, set: setLaw } = await import('/workspace/vepa/src/state/lawState.js');
  const { createDNABuffer, loadDefaults, setDNAFloat, getDNAFloat } = await import('/workspace/vepa/src/dna/dnaBuffer.js');
  const { solve, drainOffspring, resetOffspringRing, getNonFiniteRepairCount } = await import('/workspace/vepa/src/physics/solver.js');
  const { TIDAL_BLOOM } = await import('/workspace/vepa/src/state/defaultPresets.js');
  const { runtimeConfig } = await import('/workspace/vepa/src/state/runtimeConfig.js');
  const wp = await import('/workspace/vepa/src/state/worldParams.js');
  const WORLD = WORLD_SIZE;
  runtimeConfig.worldParams = { ...wp.createWorldParams(), ...(TIDAL_BLOOM.worldParams || {}) };
  if (SPEED) {
    const set = ['high', 'medium', 'low', 'lowest'].includes(SPEED) ? wp.fidelityPreset(SPEED.toUpperCase()) : SPEED === 'fast' || SPEED === 'all' ? wp.SPEED_FAST_PRESET : Object.fromEntries(SPEED.split(',').map((kv) => kv.split('=')).map(([k, v]) => [k, Number(v)]));
    for (const [k, v] of Object.entries(set)) {
      if (!wp.SPEED_SLIDER_KEYS.includes(k) || !Number.isFinite(v)) { console.error(`unknown speed slider ${k}=${v}`); process.exit(2); }
      runtimeConfig.worldParams[k] = wp.clampWorldParam(k, v);
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
  let born = 0, solveMs = 0, lastT = 0, lastMs = 0;
  if (!fs.existsSync(OUT)) fs.writeFileSync(OUT, 'preset,size,tick,alive,species,bonded,bonded_pct,births_cum,deaths_cum,mean_energy,nan_energy,nan_repairs,cum_ticks_per_s,window_ticks_per_s,max_ticks,rss_mb,heap_mb\n');
  for (let t = 1; t <= MAXT; t++) {
    const t0 = performance.now();
    solve(view, COUNT, PARTICLE_STRIDE, laws, dna, WORLD, 1 / 60, rng); born += drainOffspring().length;
    solveMs += performance.now() - t0;
    if (SAMPLES.includes(t)) {
      let alive = 0, bonded = 0, energy = 0, nanE = 0; const sp = new Set();
      for (let i = 0; i < COUNT; i++) { const b = i * PARTICLE_STRIDE; if (view[b + S.DEAD] < 0.5 && view[b + S.MASS] > 0) { alive++; sp.add(view[b + S.SPECIES_ID]); const e = view[b + S.ENERGY]; if (Number.isFinite(e)) energy += e; else nanE++; if (view[b + S.BOND_PARTNER_1] >= 0) bonded++; } }
      const row = [SPEED.toUpperCase(), COUNT, t, alive, sp.size, bonded, (100 * bonded / Math.max(1, alive)).toFixed(2), born, COUNT - alive, (energy / Math.max(1, alive - nanE)).toFixed(2), nanE, getNonFiniteRepairCount(), (t / (solveMs / 1000)).toFixed(3), ((t - lastT) / ((solveMs - lastMs) / 1000)).toFixed(3), MAXT, (process.memoryUsage().rss / 1048576).toFixed(1), (process.memoryUsage().heapUsed / 1048576).toFixed(1)];
      fs.appendFileSync(OUT, row.join(',') + '\n'); lastT = t; lastMs = solveMs;
    }
  }
