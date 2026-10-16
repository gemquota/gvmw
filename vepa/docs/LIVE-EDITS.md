# LIVE EDITS (D-043, 2026-10-16)

Gem, chat 16 Oct 2026 14:35 AEST: sliders and parameters can be updated live,
behind a setting; live editing gives up deterministic seeds, and with the
setting off, edits wait for restart so the seed reproduces the run.

## Where

SETUP › WORLD, at the top of the WORLD controls, directly above the WORLD
pending notice and its APPLY & RESTART / DISCARD WORLD buttons:
a **LIVE EDITS** switch, the seed readout (`Seed N` or `Seed N (live-edited)`)
and a one-line explanation. A **LIVE-EDITED** badge appears in the top toolbar
(next to the tick readout) while the current run is live-edited.

## Behaviour

| | OFF (default) | ON |
|---|---|---|
| WORLD sliders, including SPEED (fidelity) and RENDER | staged until restart | applied immediately |
| Law toggles, law sets, law presets | staged | applied immediately |
| DNA sliders, species roster (clone/remove) | staged | applied immediately |
| Presets, Selective Chaos, narrative WORLD actions | staged | applied immediately |
| Runtime config (force cap, drag, birth/death rate, star mass, sim speed) | staged | applied immediately (also sent to the physics worker) |
| Compute engine CPU / WebGPU | staged | **still staged** (restart-only, see below) |
| Seed | reproduces the run | the first applied edit marks the run live-edited |

- The setting is remembered in `localStorage` (`vepa.liveEdits.v1`); it starts
  OFF in a fresh browser.
- Turning ON applies anything already staged. Turning OFF stages edits again;
  the live-edited mark stays until the next restart.
- A restart (either mode) starts a fresh run from the seed and clears the mark.
- World saves, undo snapshots and `.vepa.json` exports carry
  `determinism: {seed, liveEdited, liveEditCount}`; loading a save restores the
  mark from the file (see docs/WORLD-SAVE-POLICY.md).
- The toolbar Chaos button emits Chaos followed by a restart (upstream), so it
  starts a fresh run in either mode.
- Multiplex: the multiplex FIDELITY select now travels in the multiplex
  config (`speedParams`), so it applies to the next multiplex run even while
  the WORLD speed sliders are staged (OFF). It still mirrors its choice into
  the WORLD speed sliders (staged when OFF, live when ON).

## Not live (restart-only), with reasons

- **Compute engine (CPU ↔ WebGPU).** Switching needs the physics worker torn
  down and re-created with a new GPU device. Mid-run that drops in-flight
  offspring and resets the worker's field medium and law clock, so it stays
  restart-only (`RESTART_ONLY_RUNTIME_KEYS`).
- **Spawn-layout parameters** (INITIAL_POP, SHAPE, SPAWN_CENTRES,
  SPAWN_CENTRE_RANDOM, SPAWN_CENTRE_BIAS) are committed live, but they only
  describe how particles are placed when spawned: they affect new spawns from
  then on, and the existing population keeps its layout until a restart.
- **Launch-modal settings and the seed itself** are initializers, not live
  parameters; they apply at launch/restart by definition.
- **Multiplex settings** (LAW COUNT, per-sim population, etc.) configure the
  next multiplex run; a running multiplex keeps the settings it started with.

## Determinism and golden

OFF is upstream's staged behaviour. The golden-parity harness does not use the
UI or main.js, and its 13 scenarios are unchanged.
