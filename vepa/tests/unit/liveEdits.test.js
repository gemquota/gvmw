// D-043 LIVE EDITS: OFF = staged until restart (deterministic, upstream);
// ON = proposals commit into the running world at once, run marked live-edited.
import { describe, it, expect, vi, afterEach } from 'vitest';
import { EventBus } from '../../src/core/eventBus.js';
import {
  LIVE_EDITS_DEFAULT, LIVE_EDITS_STORAGE_KEY, wireLiveEdits, seedLabel, readLiveEditsEnabled,
  determinismRecord, normalizeDeterminism, createLiveEditsState,
} from '../../src/state/liveEdits.js';
import { wirePendingWorldParams } from '../../src/state/pendingWorldParams.js';
import { wirePendingLaws } from '../../src/state/pendingLaws.js';
import { applyWorldParam, createWorldParams, SPEED_SLIDER_KEYS } from '../../src/state/worldParams.js';
import { createLawState, isSet } from '../../src/state/lawState.js';
import { LAW_INDEXES } from '../../src/constants.js';
import {
  runtimeConfig, restartRuntimeOverrides, stageRuntimeOverride, commitRuntimeOverrides,
  clearRuntimeOverrides, RESTART_ONLY_RUNTIME_KEYS, WORKER_RUNTIME_KEYS,
} from '../../src/state/runtimeConfig.js';
import { captureWorldState, exportWorldSave, parseWorldSave } from '../../src/state/worldSave.js';
import { multiplexSpeedOverlay } from '../../src/multiplex/multiplex.js';
import { PARTICLE_STRIDE } from '../../src/constants.js';

const tickMicrotasks = () => new Promise((r) => setTimeout(r, 0));

function memoryStorage(init = {}) {
  const m = new Map(Object.entries(init));
  return { getItem: (k) => (m.has(k) ? m.get(k) : null), setItem: (k, v) => m.set(k, String(v)), map: m };
}

/** A miniature session: WORLD + law pending stores and a coordinator like main.js. */
function session({ enabled = false } = {}) {
  const bus = new EventBus();
  let world = createWorldParams();
  const laws = createLawState();
  const pendingLaws = wirePendingLaws(bus, { getLive: () => laws });
  const pendingWorld = wirePendingWorldParams(bus, {
    getLive: () => world,
    apply: ({ key, value }) => { world = applyWorldParam(world, key, value); },
  });
  const applyPending = vi.fn(() => pendingLaws.commit().length + pendingWorld.commit().length);
  const storage = memoryStorage(enabled ? { [LIVE_EDITS_STORAGE_KEY]: 'on' } : {});
  const states = [];
  bus.on('liveEdits:state', (s) => states.push(s));
  const ctl = wireLiveEdits(bus, { applyPending, getSeed: () => 1234, storage });
  return { bus, ctl, applyPending, storage, states, get world() { return world; }, laws, pendingWorld, pendingLaws };
}

afterEach(() => clearRuntimeOverrides());

describe('D-043 LIVE EDITS setting', () => {
  it('defaults OFF (deterministic) and only reads an explicit "on" from storage', () => {
    expect(LIVE_EDITS_DEFAULT).toBe(false);
    expect(createLiveEditsState().enabled).toBe(false);
    expect(readLiveEditsEnabled(null)).toBe(false);
    expect(readLiveEditsEnabled(memoryStorage({ [LIVE_EDITS_STORAGE_KEY]: 'off' }))).toBe(false);
    expect(readLiveEditsEnabled(memoryStorage({ [LIVE_EDITS_STORAGE_KEY]: 'on' }))).toBe(true);
    expect(readLiveEditsEnabled({ getItem: () => { throw new Error('private'); } })).toBe(false);
  });

  it('OFF: a WORLD edit (including a SPEED slider) stays pending and the live world is untouched', async () => {
    const s = session();
    const before = s.world.GLOBAL_G;
    s.bus.emit('world:paramChanged', { key: 'GLOBAL_G', value: before + 1 });
    s.bus.emit('world:paramChanged', { key: SPEED_SLIDER_KEYS[1], value: 0 });
    await tickMicrotasks();
    expect(s.applyPending).not.toHaveBeenCalled();
    expect(s.world.GLOBAL_G).toBe(before);
    expect(s.pendingWorld.snapshot().map((c) => c.key)).toEqual(expect.arrayContaining(['GLOBAL_G']));
    expect(s.ctl.state.liveEdited).toBe(false);
  });

  it('ON: a WORLD edit applies at once, nothing stays pending, and the run is marked live-edited', async () => {
    const s = session({ enabled: true });
    const before = s.world.GLOBAL_G;
    s.bus.emit('world:paramChanged', { key: 'GLOBAL_G', value: before + 1 });
    await tickMicrotasks();
    expect(s.world.GLOBAL_G).toBe(before + 1);
    expect(s.pendingWorld.snapshot()).toEqual([]);
    expect(s.ctl.state).toMatchObject({ enabled: true, liveEdited: true, liveEditCount: 1 });
    expect(s.states.at(-1).label).toBe('Seed 1234 (live-edited)');
  });

  it('ON: a preset-style batch (laws + WORLD) is applied in one commit', async () => {
    const s = session({ enabled: true });
    s.bus.emit('law:replacePending', { changes: [{ lawIndex: LAW_INDEXES.GRAV, active: !isSet(s.laws, LAW_INDEXES.GRAV) }] });
    s.bus.emit('world:replacePending', { changes: [{ key: 'DAMPING', value: 0.5 }, { key: 'WIND', value: 0.25 }] });
    await tickMicrotasks();
    expect(s.applyPending).toHaveBeenCalledTimes(1);
    expect(s.ctl.state.liveEditCount).toBe(3);
  });

  it('turning ON applies what is already staged; turning OFF stages again but keeps the mark until restart', async () => {
    const s = session();
    s.bus.emit('world:paramChanged', { key: 'WIND', value: 0.3 });
    await tickMicrotasks();
    expect(s.world.WIND).not.toBe(0.3);
    s.bus.emit('liveEdits:set', { enabled: true });
    await tickMicrotasks();
    expect(s.world.WIND).toBe(0.3);
    expect(s.storage.map.get(LIVE_EDITS_STORAGE_KEY)).toBe('on');
    s.bus.emit('liveEdits:set', { enabled: false });
    s.bus.emit('world:paramChanged', { key: 'WIND', value: 0.1 });
    await tickMicrotasks();
    expect(s.world.WIND).toBe(0.3);
    expect(s.ctl.state.liveEdited).toBe(true);
    s.ctl.restarted();
    expect(s.ctl.state).toMatchObject({ liveEdited: false, liveEditCount: 0 });
    expect(s.states.at(-1).label).toBe('Seed 1234');
  });

  it('an apply that changes nothing does not mark the run', async () => {
    const bus = new EventBus();
    const ctl = wireLiveEdits(bus, { applyPending: () => 0, storage: memoryStorage({ [LIVE_EDITS_STORAGE_KEY]: 'on' }) });
    bus.emit('compute:pending', { changes: { computeEngine: 'cpu' } });
    await tickMicrotasks();
    expect(ctl.state.liveEdited).toBe(false);
  });

  it('runtime commit keeps restart-only keys (computeEngine) staged; worker mirrors the runtime knobs', () => {
    expect(RESTART_ONLY_RUNTIME_KEYS).toEqual(['computeEngine']);
    expect(WORKER_RUNTIME_KEYS).toEqual(expect.arrayContaining(['maxForce', 'dragMultiplier', 'birthRate', 'deathRate', 'starMass']));
    const engine = runtimeConfig.computeEngine;
    const force = runtimeConfig.maxForce;
    stageRuntimeOverride('computeEngine', engine === 'gpu' ? 'cpu' : 'gpu');
    stageRuntimeOverride('maxForce', force === 10 ? 11 : 10);
    const applied = commitRuntimeOverrides({ exclude: RESTART_ONLY_RUNTIME_KEYS });
    expect(Object.keys(applied)).toEqual(['maxForce']);
    expect(runtimeConfig.computeEngine).toBe(engine);
    expect(Object.keys(restartRuntimeOverrides)).toEqual(['computeEngine']);
    runtimeConfig.maxForce = force;
  });

  it('seed label and determinism record', () => {
    expect(seedLabel(42, false)).toBe('Seed 42');
    expect(seedLabel(42, true)).toBe('Seed 42 (live-edited)');
    expect(seedLabel(undefined, false)).toBe('Seed —');
    expect(determinismRecord({ liveEdited: true, liveEditCount: 3 }, -1)).toEqual({ seed: 4294967295, liveEdited: true, liveEditCount: 3 });
    expect(normalizeDeterminism(null)).toBeNull();
    expect(normalizeDeterminism({ liveEdited: 'yes', seed: 'x' })).toEqual({ seed: null, liveEdited: false, liveEditCount: 0 });
  });

  it('saves and .vepa.json exports record the determinism mark; older saves read as null', () => {
    const view = new Float32Array(PARTICLE_STRIDE * 2);
    const det = { seed: 99, liveEdited: true, liveEditCount: 2 };
    const state = captureWorldState({ view, count: 2, speciesCount: 1, determinism: det });
    expect(state.determinism).toEqual(det);
    const back = parseWorldSave(exportWorldSave(state));
    expect(back.determinism).toEqual(det);
    const legacy = JSON.parse(exportWorldSave(state));
    delete legacy.determinism;
    expect(parseWorldSave(JSON.stringify(legacy)).determinism).toBeNull();
    {
      const bus = new EventBus();
      const ctl = wireLiveEdits(bus, { applyPending: () => 0, getSeed: () => 99 });
      ctl.restored(back.determinism);
      expect(ctl.state).toMatchObject({ liveEdited: true, liveEditCount: 2 });
      ctl.restored(null);
      expect(ctl.state.liveEdited).toBe(false);
    }
  });

  it('multiplex FIDELITY values travel in the multiplex config (only finite SPEED keys)', () => {
    expect(multiplexSpeedOverlay({})).toEqual({});
    const overlay = multiplexSpeedOverlay({ speedParams: { SPEED_SOCIAL_EVERY: 4, GLOBAL_G: 9, SPEED_NEAR_RANGE: NaN } });
    expect(overlay).toEqual({ SPEED_SOCIAL_EVERY: 4 });
  });
});
