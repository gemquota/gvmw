/**
 * D-043 LIVE EDITS setting.
 *
 * OFF (default): every WORLD, law, DNA, roster, preset, Chaos and runtime edit
 * is staged by the pending stores and applies on restart, so the launch seed
 * plus the configuration reproduces the run (upstream behaviour, golden).
 *
 * ON: whenever a pending store publishes a non-empty proposal, the session
 * coordinator (`applyPending`, main.js) commits it into the running world at
 * once, without a restart. The first applied edit marks the run as
 * live-edited: the seed can no longer reproduce it. A restart starts a fresh
 * run from the seed and clears the mark.
 */
export const LIVE_EDITS_DEFAULT = false;
export const LIVE_EDITS_STORAGE_KEY = 'vepa.liveEdits.v1';

/** Pending-store events that mean "there is a proposal"; payload → has changes. */
export const PENDING_EVENTS = Object.freeze({
  'law:pending': (p) => Array.isArray(p?.changes) && p.changes.length > 0,
  'world:paramsPending': (p) => Array.isArray(p?.changes) && p.changes.length > 0,
  'dna:pending': (p) => Array.isArray(p?.changes) && p.changes.length > 0,
  'species:pending': (p) => Number(p?.changes) !== 0 && p?.proposedCount !== null && p?.proposedCount !== undefined,
  'compute:pending': (p) => !!p?.changes && Object.keys(p.changes).length > 0,
});

export function createLiveEditsState({ enabled = LIVE_EDITS_DEFAULT } = {}) {
  return { enabled: !!enabled, liveEdited: false, liveEditCount: 0 };
}

export function readLiveEditsEnabled(storage) {
  try {
    const raw = storage?.getItem?.(LIVE_EDITS_STORAGE_KEY);
    return raw === 'on' ? true : LIVE_EDITS_DEFAULT;
  } catch { return LIVE_EDITS_DEFAULT; }
}

export function writeLiveEditsEnabled(storage, enabled) {
  try { storage?.setItem?.(LIVE_EDITS_STORAGE_KEY, enabled ? 'on' : 'off'); } catch { /* private mode */ }
}

/** Seed readout: 'Seed 42' or 'Seed 42 (live-edited)'. */
export function seedLabel(seed, liveEdited) {
  const s = Number.isFinite(seed) ? String(seed >>> 0) : '—';
  return `Seed ${s}${liveEdited ? ' (live-edited)' : ''}`;
}

/** The determinism record written into saves, snapshots and exports. */
export function determinismRecord(state, seed) {
  return {
    seed: Number.isFinite(seed) ? seed >>> 0 : null,
    liveEdited: !!state?.liveEdited,
    liveEditCount: Math.max(0, Math.trunc(Number(state?.liveEditCount) || 0)),
  };
}

/** Validate a determinism record read from a save; null when absent. */
export function normalizeDeterminism(rec) {
  if (!rec || typeof rec !== 'object') return null;
  return {
    seed: Number.isFinite(rec.seed) ? rec.seed >>> 0 : null,
    liveEdited: rec.liveEdited === true,
    liveEditCount: Math.max(0, Math.trunc(Number(rec.liveEditCount) || 0)),
  };
}

/**
 * Wire the setting to the bus.
 * @param {object} bus
 * @param {{ applyPending: () => number, getSeed?: () => number, storage?: Storage, state?: object, schedule?: (fn) => void }} opts
 *   applyPending commits every applicable proposal into the live world and
 *   returns how many changes it applied (0 = nothing).
 */
export function wireLiveEdits(bus, { applyPending, getSeed = () => null, storage = null, state = null, schedule = queueMicrotask } = {}) {
  const s = state || createLiveEditsState({ enabled: readLiveEditsEnabled(storage) });
  let queued = false;
  const publish = () => bus.emit('liveEdits:state', {
    enabled: s.enabled, liveEdited: s.liveEdited, liveEditCount: s.liveEditCount,
    seed: getSeed(), label: seedLabel(getSeed(), s.liveEdited),
  });
  const flush = () => {
    queued = false;
    if (!s.enabled) return 0;
    const applied = Math.max(0, Number(applyPending()) || 0);
    if (applied > 0) {
      s.liveEdited = true;
      s.liveEditCount += applied;
      publish();
      bus.emit('liveEdits:applied', { count: applied, total: s.liveEditCount });
    }
    return applied;
  };
  // Batch: a preset or Chaos stages laws, WORLD, roster and DNA in one go;
  // apply them together after the current synchronous handler finishes.
  const request = () => {
    if (!s.enabled || queued) return;
    queued = true;
    schedule(flush);
  };
  for (const [event, hasChanges] of Object.entries(PENDING_EVENTS)) {
    bus.on(event, (payload) => { if (hasChanges(payload)) request(); });
  }
  bus.on('liveEdits:set', ({ enabled } = {}) => {
    s.enabled = !!enabled;
    writeLiveEditsEnabled(storage, s.enabled);
    publish();
    // Turning ON applies whatever is already staged.
    if (s.enabled) {
      for (const ev of ['law:pendingRequested', 'world:pendingRequested', 'dna:pendingRequested', 'species:pendingRequested']) bus.emit(ev);
      request();
    }
  });
  bus.on('liveEdits:requested', publish);
  return {
    state: s,
    flush,
    publish,
    /** A restart starts a fresh run from the seed. */
    restarted() { s.liveEdited = false; s.liveEditCount = 0; publish(); },
    /** A restored save carries its own determinism record. */
    restored(rec) {
      const r = normalizeDeterminism(rec);
      s.liveEdited = !!r?.liveEdited;
      s.liveEditCount = r?.liveEditCount ?? 0;
      publish();
    },
    record: () => determinismRecord(s, getSeed()),
  };
}
