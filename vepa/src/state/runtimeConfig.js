/**
 * VEPA4 — Mutable runtime tunables
 * Shared across modules so settings sliders, goal-engine adjustments, and
 * signal tuning take effect without rebuilds.
 */
import { createWorldParams } from './worldParams.js';

const savedRenderBackend = typeof localStorage !== 'undefined'
  && localStorage.getItem('vepa-render-backend') === 'pixi'
  ? 'pixi'
  : 'canvas2d';

export const runtimeConfig = {
  starMass: 12,        // mass threshold for gravitational collapse (star)
  visualScale: 1.0,    // global particle size multiplier
  globalAlpha: 1.0,    // global particle opacity multiplier
  simSpeed: 1.0,       // physics time-step multiplier
  // v4 — goal-engine adjustable knobs (bounded by GoalEngine parameter ranges)
  maxForce: 50.0,      // global force clamp ceiling (solver MAX_FORCE is hard cap)
  forceScale: 1.0,     // global force multiplier applied before clamping
  dragMultiplier: 1.0, // global velocity damping multiplier (0.8–1.0)
  birthRate: 1.0,      // REPRO law synergy multiplier (0.01–1.0)
  deathRate: 1.0,      // LIFE law synergy multiplier (0.01–1.0)
  signalScale: 1.0,    // global communication DNA multiplier
  // v8.17 — gravity engine: 'reference' (default, per-pair DNA-aware reference
  // CPU solver; 'exact' is a permanent legacy alias), 'bh'
  // (Barnes–Hut monopole, O(N log N)), or 'fmm' (experimental FMM with
  // quadrupole terms; not more accurate than 'bh' today, see BACKEND_ENVELOPES). gravTheta is the opening angle
  // (0 = exact traversal; 0.4–0.7 typical). See src/physics/octree.js.
  gravEngine: 'reference', // legacy alias 'exact' behaves identically
  gravTheta: 0.5,
  // FIELD-ONCE (D-016): true (default) = the field medium advances once per tick;
  // false = legacy, once per particle per tick. See docs/GOLDEN-REBASELINE.md.
  fieldAdvanceOnce: true,
  // B7 (D-006): civilisation runtime adapter (src/engines/civRuntime.js) —
  // kinship, households, tribe, polity, culture selection, relationship lab.
  // Default off: when false the live sim never calls into the adapter.
  civRuntime: false,
  // ARP-5: test-only hook observing solver pair scalars; must stay null in production.
  pairProbe: null,
  // v9.0 — compute engine: GPU is the user-facing default. The worker probes
  // WebGPU once and falls back to the validated CPU path when unavailable;
  // explicit CPU selection remains available in SETTINGS > COMPUTE.
  computeEngine: 'gpu',
  renderBackend: savedRenderBackend,
  worldParams: createWorldParams(),
};

/** Gravity engines accepted by runtimeConfig.gravEngine. */
export const GRAV_ENGINES = Object.freeze(['reference', 'bh', 'fmm']);

/**
 * Canonical gravity-engine name. 'exact' is the permanent legacy alias for
 * 'reference' (the default per-pair CPU solver); anything unrecognised also
 * falls back to 'reference', matching how solve() dispatches.
 */
export function normalizeGravEngine(value) {
  if (value === 'exact') return 'reference';
  return GRAV_ENGINES.includes(value) ? value : 'reference';
}

/** Compute tunables changed by automatic planners but committed by restart. */
export const restartRuntimeOverrides = Object.create(null);
const RUNTIME_OVERRIDE_RANGES = Object.freeze({
  simSpeed: [0.1, 10],
  starMass: [4, 100],
  maxForce: [0.1, 50],
  dragMultiplier: [0.8, 1],
  birthRate: [0.01, 1],
  deathRate: [0.01, 1],
});

export function stageRuntimeOverride(key, value) {
  if (key === 'computeEngine') {
    if (value !== 'cpu' && value !== 'gpu') return false;
    if (value === runtimeConfig.computeEngine) delete restartRuntimeOverrides[key];
    else restartRuntimeOverrides[key] = value;
    return true;
  }
  const range = RUNTIME_OVERRIDE_RANGES[key];
  if (!range || typeof value !== 'number' || !Number.isFinite(value)) return false;
  const accepted = Math.max(range[0], Math.min(range[1], value));
  if (accepted === runtimeConfig[key]) delete restartRuntimeOverrides[key];
  else restartRuntimeOverrides[key] = accepted;
  return true;
}

/**
 * D-043: runtime keys that stay restart-only even with LIVE EDITS on.
 * computeEngine: switching CPU/WebGPU tears down and re-creates the physics
 * worker and its GPU device; doing that mid-run would drop in-flight births
 * and reset the worker's field / law-clock state, so it waits for restart.
 */
export const RESTART_ONLY_RUNTIME_KEYS = Object.freeze(['computeEngine']);

/** Commit staged runtime overrides; `exclude` keys stay staged. */
export function commitRuntimeOverrides({ exclude = [] } = {}) {
  const skip = new Set(exclude);
  const applied = {};
  for (const key of Object.keys(restartRuntimeOverrides)) {
    if (skip.has(key)) continue;
    applied[key] = restartRuntimeOverrides[key];
    delete restartRuntimeOverrides[key];
  }
  Object.assign(runtimeConfig, applied);
  return applied;
}

/** D-043: runtime knobs the physics worker must mirror (sent in its CONFIG). */
export const WORKER_RUNTIME_KEYS = Object.freeze(['maxForce', 'dragMultiplier', 'birthRate', 'deathRate', 'starMass']);

export function clearRuntimeOverrides() {
  for (const key of Object.keys(restartRuntimeOverrides)) delete restartRuntimeOverrides[key];
}
