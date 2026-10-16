// usage: node hunt.mjs <count> <ticks> <speedKeys|none> [srcRoot=/tmp/nanhunt/src] [laws=tidal]
// Mirrors the bench:solver child world. Pass 1: find the first tick that ends
// with a non-finite field in an alive particle. Pass 2: rerun to that tick with
// the instrumented checks on and report the first statement window that wrote it.
const [COUNT, TICKS] = [Number(process.argv[2]), Number(process.argv[3])];
const SPEED = process.argv[4] && process.argv[4] !== 'none' ? process.argv[4] : '';
const R = (process.argv[5] || '/tmp/nanhunt/src') + '/';
const LAWS = process.argv[6] || 'tidal';
const { PARTICLE_STRIDE, STRIDE_INDEXES: S, DNA_RANGES, LAW_INDEXES, WORLD_SIZE } = await import(R + 'constants.js');
const { createLawState, set: setLaw } = await import(R + 'state/lawState.js');
const { createDNABuffer, loadDefaults, setDNAFloat, getDNAFloat } = await import(R + 'dna/dnaBuffer.js');
const sol = await import(R + 'physics/solver.js');
const { TIDAL_BLOOM } = await import(R + 'state/defaultPresets.js');
const { runtimeConfig } = await import(R + 'state/runtimeConfig.js');
const wp = await import(R + 'state/worldParams.js');
const FIELD = Object.fromEntries(Object.entries(S).map(([k, v]) => [v, k]));
const NUMF = PARTICLE_STRIDE;

function world() {
  let s = 0x9e3779b9 ^ COUNT;
  const rng = () => { s = (Math.imul(s, 1664525) + 1013904223) >>> 0; return s / 4294967296; };
  let m = 0x5bd1e995; Math.random = () => { m = (Math.imul(m, 1103515245) + 12345) >>> 0; return m / 4294967296; };
  runtimeConfig.worldParams = { ...wp.createWorldParams(), ...(TIDAL_BLOOM.worldParams || {}) };
  if (SPEED) for (const k of (SPEED === 'all' ? wp.SPEED_PARAM_KEYS : SPEED.split(','))) runtimeConfig.worldParams[k] = 1;
  const view = new Float32Array(COUNT * 2 * PARTICLE_STRIDE);
  const dna = createDNABuffer(); loadDefaults(dna, DNA_RANGES);
  for (let sp = 0; sp < 5; sp++) for (let d = 0; d < 42; d++) { const r = DNA_RANGES[d] || { min: -1, max: 1 }; setDNAFloat(dna, sp, d, r.min + rng() * (r.max - r.min), r.min, r.max); }
  for (let i = 0; i < COUNT; i++) {
    const b = i * PARTICLE_STRIDE, sp = i % 5;
    view[b + S.POS_X] = rng() * WORLD_SIZE; view[b + S.POS_Y] = rng() * WORLD_SIZE; view[b + S.POS_Z] = rng() * WORLD_SIZE;
    view[b + S.MASS] = 1 + rng(); view[b + S.SPECIES_ID] = sp; view[b + S.ENERGY] = 50 + rng() * 50;
    view[b + S.RADIUS] = 0.6 + rng() * 0.6;
    view[b + S.BOND_PARTNER_1] = -1; view[b + S.BOND_PARTNER_2] = -1; view[b + S.BOND_PARTNER_3] = -1; view[b + S.BOND_PARTNER_4] = -1;
    for (let d = 0; d < 42; d++) { const r = DNA_RANGES[d] || { min: -1, max: 1 }; view[b + S.DNA_CACHE_START + d] = getDNAFloat(dna, sp, d, r.min, r.max); }
  }
  const laws = createLawState();
  const names = LAWS === 'all' ? Object.keys(LAW_INDEXES) : TIDAL_BLOOM.laws;
  for (const n of names) if (LAW_INDEXES[n] !== undefined) setLaw(laws, LAW_INDEXES[n]);
  if (LAWS !== 'all' && wp.syncWrapLaw) wp.syncWrapLaw(runtimeConfig.worldParams, laws);
  sol.resetOffspringRing(); sol.resetSolverState(0);
  return { view, dna, laws, rng };
}
const DC = S.DNA_CACHE_START;
const MODE = process.env.MODE || 'nonfinite'; // or 'dna' (DNA cache out of its declared range)
const outOfRange = (f, v) => { const d = f - DC; if (d < 0 || d >= 42) return false; const r = DNA_RANGES[d]; if (!r) return false; const tol = 1e-5 * Math.max(1, Math.abs(r.max - r.min)); return v < r.min - tol || v > r.max + tol; };
const isBad = (f, v) => MODE === 'dna' ? (Number.isFinite(v) && outOfRange(f, v)) : !Number.isFinite(v);
function scan(view, n) {
  const bad = [];
  for (let i = 0; i < n; i++) { const b = i * NUMF; if (view[b + S.DEAD] >= 0.5 && MODE === 'dna') continue;
    for (let f = 0; f < NUMF; f++) if (isBad(f, view[b + f])) bad.push([i, FIELD[f] || ('DNA' + (f - DC)), view[b + f], view[b + S.DEAD] >= 0.5 ? 'dead' : 'alive']); }
  return bad;
}
// pass 1
let w = world(); let T = -1;
globalThis.__nanOn = false;
for (let t = 0; t < TICKS; t++) {
  sol.solve(w.view, COUNT, PARTICLE_STRIDE, w.laws, w.dna, WORLD_SIZE, 1 / 60, w.rng); sol.drainOffspring();
  const bad = scan(w.view, COUNT);
  if (bad.length) { T = t; console.log(`first non-finite at end of tick ${t}: ${bad.length} fields`, JSON.stringify(bad.slice(0, 8))); break; }
}
const finalBad = T < 0 ? [] : null;
if (T < 0) { console.log(`no non-finite field in ${TICKS} ticks`); process.exit(0); }
// pass 2
w = world();
for (let t = 0; t < T; t++) { sol.solve(w.view, COUNT, PARTICLE_STRIDE, w.laws, w.dna, WORLD_SIZE, 1 / 60, w.rng); sol.drainOffspring(); }
const view = w.view; const seen = new Set(scan(view, COUNT).map(([i, f]) => i + ':' + f));
let lastLabel = 'tick-start'; const snaps = new Map(); const hits = [];
const row = (b) => b < 0 ? null : Object.fromEntries([['DNA40_MEMORY_DECAY', view[b + S.DNA_CACHE_START + 40]], ['DNA20_SIGNAL_DECAY', view[b + S.DNA_CACHE_START + 20]], ['MEMORY', view[b + S.MEMORY]]].concat(['ENERGY', 'MASS', 'VEL_X', 'VEL_Y', 'VEL_Z', 'AGE', 'RADIUS', 'TEMPERATURE', 'CHARGE', 'SIGNAL', 'DEAD'].filter((k) => S[k] !== undefined).map((k) => [k, view[b + S[k]]])));
function check(label, ib, jb) {
  for (const b of [ib, jb]) { if (b < 0) continue;
    for (let f = 0; f < NUMF; f++) { const v = view[b + f];
      if (isBad(f, v)) { const key = (b / NUMF) + ':' + (FIELD[f] || f);
        if (!seen.has(key)) { seen.add(key); if (hits.length < 12) hits.push({ tick: T, particle: b / NUMF, field: FIELD[f] || ('DNA' + (f - DC)), value: v, prevValue: (snaps.get(b) || {})._raw ? snaps.get(b)._raw[f] : undefined, betweenChecks: [lastLabel, label], pair: [ib / NUMF, jb >= 0 ? jb / NUMF : -1], before: snaps.get(b) || null, after: row(b) }); } } } }
  for (const b of [ib, jb]) if (b >= 0) { const r = row(b); r._raw = Array.from(view.subarray(b, b + NUMF)); snaps.set(b, r); }
  lastLabel = label;
}
globalThis.__nanChk = check;
globalThis.__nanAll = (label) => { for (let i = 0; i < COUNT; i++) check(label, i * NUMF, -1); };
globalThis.__nanOn = true;
sol.solve(view, COUNT, PARTICLE_STRIDE, w.laws, w.dna, WORLD_SIZE, 1 / 60, w.rng);
globalThis.__nanOn = false;
for (const h of hits) { if (h.before) delete h.before._raw; console.log(JSON.stringify(h)); }
