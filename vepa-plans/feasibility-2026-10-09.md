# VEPA roadmap: feasibility notes (9 Oct 2026)

Read-only check of `/workspace/vepa` v9.1.27 (branch `codey/complete-plans`, not modified) against `roadmap-from-interviews.md`.
Effort sizes are rough: **S** = days, **M** = 1–3 weeks, **L** = 1–3 months, **XL** = a quarter or more.
Performance figures used throughout: about 13 ticks/s at 300 particles (about 75 ms per tick) and about 860 ms per tick at 10k, on the 8-vCPU box with no GPU. Phones will usually be slower.

Three code facts come up repeatedly:
- **The particle stride is full.** `PARTICLE_STRIDE = 100` (`src/constants/stride.js`). Slots 0–98 are named, and `src/state/synthetic.js` uses 98 and 99 for synthetic flags and traits. **Slot 98 is double-booked:** `ACCR_LINK_MASK` (accretion bonds, `src/physics/mergePhysics.js`) and `OFFSET_SYNTHETIC_FLAGS` share it. That looks like a live bug worth a separate ticket. Any new per-being state should go into side tables keyed by particle index, like `civRuntime` already does with its Maps, rather than into new stride slots.
- **Particle indices are append-only.** The dead keep their slots (`civRuntime.js` header), so an index is a stable id within one world. It also means snapshots and buffers grow with cumulative births, not with the live population.
- **The sim is deterministic per build.** The worker uses a seeded SplitMix PRNG, the main PRNG state is saved (`rng` in the world save), and pooled multiplex runs are bit-identical to in-thread runs (`docs/MULTIPLEX-PERF.md`). Any solver change alters the golden hashes, so replays only hold within one build.

---

## 1. Grief and revival (deaths leave memory traces)
**Verdict: Feasible with work** · **Effort: M** (grief), **S–M** (revival on top)

At the moment a death mostly erases. `main.js` (~L1470) detects deaths on a cadence and calls `trackDeath` (`lineageTracker.js`), which logs only a cause. `civRuntimeOnDeath` (`civRuntime.js` L118) removes the being from its household and citizenship and calls `forgetNode`, which deletes every relationship edge. The one existing trace is the ASTRAL law. With it on, a dead particle becomes a ghost (`DEAD = 0.5`) whose SOUL fades by ×0.999 per tick. The ghost pulls on nearby living particles and passes a small slice of soul to same-species kin. That gives a ready-made, physical "presence of the dead", but nobody *remembers* anyone.

Grief needs a small change: copy the kin and household edges into a per-survivor "loss" record before `forgetNode` runs. The record holds who died, when, where and how, and a grief level that decays over time and modulates behaviour (for example lower activity, or drifting back to the death site). Revival is mechanically trivial, because the slot survives and spawn code already sets `DEAD = 0`. The real work is rules and bookkeeping: lineage and death statistics, energy conservation, and the save. A coherent rule would be "revivable only while the ASTRAL ghost still exists". Everything stays off the hot path because deaths are rare.
**Cheapest first step:** in `civRuntimeOnDeath`, snapshot the dead being's edges into a capped `losses` Map before `forgetNode`, save it as an additive field, and show a grieving count in the civ panel.

## 2. Beings forming beliefs about, and talking to, the player
**Verdict: Feasible with work** for beliefs and templated "speech". **Research-grade/costly** for open conversation.

The player currently has no presence in the world. Player actions show up only as bus events: `law:toggled` (`worldPanel.js`, `tooltip.js`), `world:paramChanged`, restores and saves, plus the agency engine's own field writes (`agencyEngine.js`, an automated "narrator" that nudges spawn rate or the INFO field). Beings sense only local stride fields (SIGNAL, SYMBOL_TOKEN, neighbours), so they cannot perceive any of this. The only existing "voices" are the template lines in `narrativeEngine.js`, and those are the narrator's voices, not the beings'.

Workable beliefs are statistics: per tribe, track how player interventions correlate with what followed ("when we starve, the sky sends energy"), and store them in a group side table next to `memoryBuffers.js`. Those beliefs can then bias behaviour and drive template lines ("The Reds expect rescue"). Free-form two-way conversation needs an LLM (see item 4 for cost) and a careful design so the LLM voices the being's measured beliefs instead of inventing new ones.
**Cheapest first step:** log player interventions as world events with a timestamp and location, compute one correlation per tribe ("interventions after crashes") and display it. No LLM needed.
**Effort:** M for beliefs plus templated speech; L+ for LLM dialogue.

## 3. Background/persistent runs with a recap on the phone (server worlds paid with credits)
**Verdict: Feasible with work** (server). Running in the background inside a phone browser is **Not feasible as framed**.

In the browser the sim simply stops when the tab is hidden: the loop runs on rAF and there is no `visibilitychange` handling in `main.js`. Phones also suspend background tabs. Catch-up on return can't recover much either, because a phone is already solver-bound at roughly real-time speed (300 particles about 13 ticks/s), so it can't simulate eight missed hours in seconds. A server is the honest route, and the code helps: the solver already runs headless in Node (`bench/solver.bench.mjs`, `bench/shard-worker-node.mjs`, worker_threads). The gap is that `main.js` (1,933 lines) is the orchestrator for civRuntime, lineage, world events and the rest, and it is DOM-coupled. A headless "world core" has to be extracted from it. Other pieces still to build: accounts, storage, a credit ledger, Web Push (on iOS this only works for a home-screen-installed PWA), and a recap built from the event log (v2 item 3). The current deploy is a static Vercel site with no backend.

Rough server cost, using about US$0.02–0.04 per vCPU-hour:
- A 300-particle world at full speed uses about half a core in Node (≈37 ms per tick per `PERF-PASS-2026-10-04.md`). That is about US$0.01–0.02/h, or roughly US$7–15 a month running 24/7.
- A 10k world saturates 8 vCPUs at about 1 tick/s. That is about US$0.25–0.35/h, or roughly US$180–250 a month.

At the agreed cap of 3x cost, small worlds are viable and big ones aren't. Credits should be priced per CPU-second, or per particle-tick, not per hour. The 48 h grace at 1% equals about 29 minutes of full-speed time, which matches the roadmap.
**Cheapest first step:** a Node script that loads a `.vepa.json` save, runs N ticks headless with civRuntime on, and writes the save plus an event log back out. That proves the server path and gives the recap its data.
**Effort:** L for headless core plus recap; XL with accounts, credits and push.

## 4. Uncapped population with low-cost LLM minds
**Verdict:** uncapped population **Not feasible as framed**: it can only mean "cap set by the device's budget", which is Feasible with work. LLM minds per being per tick are **Not feasible**; LLM minds for a few named beings on a slow cadence are **Feasible with work**.

The buffer is pre-allocated at `MAX_PARTICLES = 100000` (100k × 100 floats × 4 B = 40 MB), and births stop at the cap (`main.js` L691/L840). Because slots are append-only, dead particles eat capacity, so "uncapped" first needs slot reuse or compaction. The solver already scales its pair budget (`PAIRWISE_BUDGET` 96, divided by √(N/2500), in `solver.js` ~L397), and the cost is still about 860 ms per tick at 10k. Performance tiers should therefore choose the cap, and the cost meter should show ticks per second.

LLM maths uses the cheapest current tier (about US$0.10 per million input tokens and US$0.50 per million output, Oct 2026 list prices; these change) and a 400-token prompt with a 40-token reply, which comes to **≈ US$0.00006 per call**. Latency is about 0.5–1.5 s per call, which is 7–20 ticks at 300 particles.

| Policy | Calls | Cost |
|---|---|---|
| 1 being, every tick (13/s) | 46,800/h | **≈ US$2.80/h per being** |
| 300 beings, every tick | 3,900/s (far beyond API rate limits) | ≈ US$840/h |
| 10k beings, every tick (≈1.2/s) | 12,000/s | ≈ US$2,500/h |
| 300 beings, one call per 30 s | 10/s | ≈ US$2.20/h |
| 20 "named" beings, one call per 10 s | 2/s | ≈ US$0.43/h (≈ US$0.11–0.22 per 15–30 min session; ≈ US$1.30/h at 3x) |

The workable design is tiers. A cheap rule-based mind runs for everyone. An LLM runs asynchronously for a handful of beings the player is watching, decides every few seconds, and its replies apply some ticks late. Prompt caching of a shared world preamble cuts input cost further. On-device small models are possible on high-end phones, but they are slow and drain the battery.
**Cheapest first step:** add a "minded beings" toggle that sends one being's local state to an LLM every 10 s and logs the cost per call to the cost meter.
**Effort:** M for device-set caps plus slot reuse; L for tiered LLM minds.

## 5. Inherited memories beyond one decaying number
**Verdict: Feasible with work** · **Effort: M**

Per being there is one scalar, `MEMORY` (stride 61, clamped to 0..1), written by six laws (COMMS, CONSCIOUSNESS, FEEDBACK, LANGUAGE, MEMORY, OBSERVER, per `strideWriteContract.js`), with a DNA `MEMORY_DECAY` locus (40). Richer memory already exists above the individual: `memoryBuffers.js` keeps a 4-channel vector (activity, cohesion, exploration, threat) per species and per group, decaying at 0.999, and it outlives particles. Some inheritance also already happens. CULTURE and CODE blend the 42-float per-particle DNA cache between contacts, and REPRO copies that cache to offspring, so learned traits pass to children (`informationTrace.js` documents this path).

Per-being memory should be a side table: for example a 16-float vector plus a ring buffer of 8 episodes (what, who, where, when), about 200 B per being, or about 2 MB at 10k. The child copies a damped share of the parent's memory at `civRuntimeOnBirth`, which already receives parent and child. The catch is that the physics worker only sees the stride buffer. Side-table memory can drive main-thread decisions on a cadence, but it can't change pair forces unless a summary is written back into an existing stride field. The save policy allows this as an additive field without a version bump.
**Cheapest first step:** a per-being memory Map in civRuntime, filled from events that already exist (births, deaths, care transfers, alliances and conflicts), inherited at birth, and shown on tap.

## 6. Evolving language with toggleable translation
**Verdict: Feasible with work** for evolving vocabularies. **Research-grade** if you expect grammar to emerge. · **Effort: M–L**

What exists is thinner than the names suggest. SYMBOL (`laws.js` ~L2481) rounds `SYMBOL_TOKEN` to one of 8 values. The higher-MEMORY partner imprints its token on contact, and same-token pairs attract. That is a shared tag, not a word. LANGUAGE (~L2589) just averages two scalars (MEMORY) and spreads SIGNAL; nothing refers to anything.

A well-studied, buildable version is a naming/signalling game run per tribe. Meanings are grounded referents the sim already tracks (food or energy, threat, kin, territory, the player). Words are generated syllable strings, successful exchanges reinforce a word, and drift and tribe splits produce dialects. Translation then needs no AI and is honest: show each word's dominant meaning in that tribe with a confidence, and the toggle just swaps the display. Grammar or compositional language emerging on its own is an open research problem; don't promise it.
**Cheapest first step:** a per-tribe lexicon side table (meaning → word with weights), updated at the cadence `civRuntime` already runs on, plus a debug panel listing each tribe's words and their meanings.

## 7. Self-awareness detection
**Verdict: Feasible with work** for detecting defined *behavioural* markers, and only after real self-models exist. It cannot detect awareness itself. · **Effort: M** for the detector, plus **L** for the self-models it needs

Today's CONSCIOUSNESS law (`src/physics/lawgroups/metaLaws.js`) keeps an exponential average of the particle's own speed. When actual speed deviates by more than 0.3, it raises MEMORY and SIGNAL and costs energy. It runs at a hard-coded strength (`solver.js` L1540, `k = 0.5`). `CONSCIOUSNESS_PHI` is described in the UI as an "integrated-information threshold", but nothing in the solver reads it, and no Φ is computed anywhere. A detector pointed at this would fire constantly and mean nothing.

Once beings have real self-models (item 10), a detector can test operational markers. Examples:
- (a) a being predicts its own next state better than it predicts others' states;
- (b) it separates changes it caused from changes done to it (a mirror-test analogue);
- (c) switching the self-model off measurably hurts its survival or choices;
- (d) the effect persists over time and shows up in more than one being.

It should report "self-modelling behaviour detected (markers a–c, confidence X)", never "this being is aware". It reuses the notable-moment detector (v2 item 3), so build that first.
**Cheapest first step:** fix the labelling now: either wire `CONSCIOUSNESS_PHI` into the law or rename the param and update its help text so it stops implying measured integrated information.

## 8. Branching timelines kept in full
**Verdict: Feasible with work** if "in full" means *every branch can be restored exactly*. **Not feasible** on a phone if it means *every state of every branch is stored*. · **Effort: L**

The multiplex keeps a short history (`multiplex.js` `recordHistory`, `historyDepth` 6, max 12). Each entry stores light per-sim records (DNA, laws, params) plus full snapshots of only the selected and fittest sims, and the rest are re-rolled on revert. Multiplex sims run the solver only, not civRuntime, lineage or culture engines, so a branch made there carries no tribe state. The main timeline (`timelineEngine.js`) keeps 20 snapshots every 150 ticks.

Storage maths: a snapshot is about 400 B per particle *slot* (100 floats × 4 B), and slots include the dead. That is about 120 KB at 300, about 1 MB at 2,500 and about 4 MB at 10k, before about 33% base64 overhead on export. Full snapshots every 150 ticks come to:
- at 300 particles: about 38 MB/h per branch, or about 940 MB/h for 25 branches;
- at 10k (about 28 snapshots/h): about 110 MB/h per branch.

That is too much for a phone's IndexedDB, which Safari may also evict. Determinism gives a much cheaper design. Store each branch as its parent, the fork tick, the changed settings and the player-input log (a few KB each), plus keyframes. Keyframes every 60 s cost about 7 MB/h per branch at 300 particles and cap any restore at about 60 s of re-simulation. The catches: replay only holds on the same build, so each branch must pin its build and keep keyframes as a fallback. Every side engine (civRuntime and the rest) must also be deterministic and saved.
**Cheapest first step:** a test that saves, replays N ticks from the save, and compares the result hash bit for bit with civRuntime on. If that passes, the cheap branch format is safe.

## 9. Migrating beings between players
**Verdict: Feasible with work** as a file or link "being card". **XL** as live online migration. · **Effort: M** (card), **XL** (live)

A being is one stride row (400 B), which already includes its 42-float DNA cache, plus its species entry, plus any side-table state (memory, kin, culture). Problems:
- Identity is the particle index, which only holds within one world, so migration needs a global id.
- Species ids (max 64) and law sets differ between worlds, so the receiving world has to remap the species or adopt it as a new one, and the being may behave differently under different laws.
- Kin and tribe links don't travel.

Live migration needs accounts and server worlds (item 3). Moderation risk is low while beings are just numbers, and rises once they have LLM-generated names or speech.
**Cheapest first step:** export and import a single being as `.vepa-being.json` through the phone share sheet, arriving as a "visitor" species. It needs no server and reuses `worldSave.js` encoding.

## 10. Is genuine emergent self-awareness possible in the current architecture?
**Verdict: Not feasible as framed.** Behavioural self-modelling is **Feasible with work (and partly research-grade)**. Real awareness can't be produced or confirmed by these mechanisms. · **Effort: L** for real self-models

Plainly: in the current code, a being is about 100 numbers updated by fixed, hand-written rules. Its only "self-model" is a running average of its own speed. Nothing in it learns a representation, and nothing it does depends on modelling itself. Evolution and culture tune DNA parameters, but they can't grow new kinds of machinery the rules don't already contain. So nothing in this architecture can become self-aware; at most it can look self-aware.

What *is* buildable: give beings a small learned predictive model (a tiny network or table) of their own body, their neighbours and their surroundings, make their decisions use it, and let selection favour beings whose model works. That can produce real, measurable self-modelling behaviour, which is interesting, honest and a good game. Whether anything is *experienced* is a different question. There is no agreed test for awareness in any system, so no detector, Φ value or behaviour can confirm it, and this code certainly can't. One specific trap: LLM-driven beings will *say* "I know I exist" because they were trained on human writing. That reflects the model's training, not anything that emerged in VEPA, so the detector must never count LLM speech as evidence. I'd suggest rewording the Phase 5 line from "Genuine self-models that could lead to emergence" to "Working self-models, with markers we can measure". "Protect the being" works fine as a game mechanic either way.
**Cheapest first step:** prototype one learned self-predictor (for example predicting next-tick energy and position) for 50 beings in a side table, and measure markers (a)–(c) from item 7 against a control group without it.
