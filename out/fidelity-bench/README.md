# FIDELITY bench (D-039: 4 levels; D-040: particle cap 100,000)

Box: 8 vCPU Xeon, Node 22, NO GPU. Bench world TIDAL_BLOOM.

## Levels

| Slider | HIGH | MEDIUM | LOW | LOWEST |
|---|---|---|---|---|
| PAIRWISE_BUDGET | 96 | 48 | 24 | 16 |
| SPEED_MID_RANGE | 200 | 120 | 90 | 60 |
| SPEED_NEAR_RANGE | 30 | 30 | 30 | 20 |
| SPEED_PAIR_BUDGET | 512 | 20 | 12 | 8 |
| SPEED_SYMBIOSIS_RANGE | 600 | 30 | 20 | 10 |
| SPEED_SOCIAL_EVERY | 1 | 2 | 3 | 4 |
| SPEED_EXPENSIVE_EVERY | 1 | 1 | 2 | 4 |
| multiplex LAW COUNT | 136 | 136 | 48 | 16 |

## Solver (bench/solver-tps.mjs --speed high|medium|low|lowest): median of 3 fresh-process runs, 30 timed ticks (10 at 50k) after 3 warm-up

| Particles | Preset | ticks/s | × vs HIGH | runs (ms/tick) | alive | species | bonded % @30 | NaN energy | NaN repairs | Node RSS MB | heap MB | buffer MB |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 100 | HIGH | 299.52 | 1.00× | 3.2/3.3/3.4 | 100 | 5 | 21.0 | 0 | 0 | 83.9 | 11.1 | 0.08 |
| 100 | MEDIUM | 295.34 | 0.99× | 3.3/3.4/3.4 | 100 | 5 | 23.0 | 0 | 0 | 84.9 | 11.5 | 0.08 |
| 100 | LOW | 340.62 | 1.14× | 2.8/2.9/3 | 100 | 5 | 15.0 | 0 | 0 | 83.2 | 8.5 | 0.08 |
| 100 | LOWEST | 363.53 | 1.21× | 2.7/2.8/2.8 | 100 | 5 | 10.0 | 0 | 0 | 84 | 10.8 | 0.08 |
| 500 | HIGH | 32.2 | 1.00× | 30.8/31.1/32.7 | 500 | 5 | 88.2 | 0 | 0 | 146.3 | 14.3 | 0.38 |
| 500 | MEDIUM | 43 | 1.34× | 22.4/23.3/24.9 | 500 | 5 | 87.2 | 0 | 0 | 114.7 | 13.6 | 0.38 |
| 500 | LOW | 55.95 | 1.74× | 17.7/17.9/18.2 | 500 | 5 | 73.0 | 0 | 0 | 135.6 | 14.1 | 0.38 |
| 500 | LOWEST | 73.47 | 2.28× | 12.8/13.6/13.9 | 500 | 5 | 40.8 | 0 | 0 | 164.6 | 12.1 | 0.38 |
| 2,500 | HIGH | 3.56 | 1.00× | 270/281/281.1 | 2500 | 5 | 99.56 | 0 | 0 | 159.6 | 16.1 | 1.91 |
| 2,500 | MEDIUM | 14.65 | 4.12× | 68/68.2/71.8 | 2500 | 5 | 96.8 | 0 | 0 | 169.9 | 12.2 | 1.91 |
| 2,500 | LOW | 21.8 | 6.12× | 42.5/45.9/46.4 | 2500 | 5 | 89.96 | 0 | 0 | 183.4 | 19.3 | 1.91 |
| 2,500 | LOWEST | 19.18 | 5.39× | 51/52.1/53 | 2500 | 5 | 11.16 | 0 | 0 | 170.1 | 17.5 | 1.91 |
| 10,000 | HIGH | 1.77 | 1.00× | 561.7/564.9/589.3 | 10000 | 5 | 94.79 | 0 | 0 | 159.7 | 38.6 | 7.63 |
| 10,000 | MEDIUM | 5.36 | 3.03× | 183.3/186.5/199.8 | 10000 | 5 | 87.89 | 0 | 0 | 150.4 | 36.1 | 7.63 |
| 10,000 | LOW | 11.19 | 6.32× | 88.5/89.4/93 | 10000 | 5 | 55.04 | 0 | 0 | 183 | 12.5 | 7.63 |
| 10,000 | LOWEST | 13 | 7.34× | 76/76.9/77 | 10000 | 5 | 4.01 | 0 | 0 | 213.8 | 17.9 | 7.63 |
| 50,000 | HIGH | 0.63 | 1.00× | 1543.1/1584.2/1648.1 | 50000 | 5 | 93.33 (@10) | 0 | 0 | 213.4 | 44.4 | 38.15 |
| 50,000 | MEDIUM | 1.24 | 1.97× | 797.1/804.5/846.8 | 50000 | 5 | 68.87 (@10) | 0 | 0 | 213.8 | 24.4 | 38.15 |
| 50,000 | LOW | 1.7 | 2.70× | 581.8/588.2/591.3 | 50000 | 5 | 29.7 (@10) | 0 | 0 | 210.1 | 25 | 38.15 |
| 50,000 | LOWEST | 2.32 | 3.68× | 420.3/431/448.6 | 50000 | 5 | 6.29 (@10) | 0 | 0 | 219.3 | 30 | 38.15 |

## Speed-up vs HIGH (solver)

| Particles | HIGH | MEDIUM | LOW | LOWEST |
|---|---|---|---|---|
| 100 | 1.00× | 0.99× | 1.14× | 1.21× |
| 500 | 1.00× | 1.34× | 1.74× | 2.28× |
| 2,500 | 1.00× | 4.12× | 6.12× | 5.39× |
| 10,000 | 1.00× | 3.03× | 6.32× | 7.34× |
| 50,000 | 1.00× | 1.97× | 2.70× | 3.68× |

## Bonded % of alive (solver world): after 30 ticks (10 at 50k) / after 150 ticks

| Particles | HIGH | MEDIUM | LOW | LOWEST |
|---|---|---|---|---|
| 100 | 21.0 / 45.0 | 23.0 / 43.0 | 15.0 / 53.0 | 10.0 / 45.0 |
| 500 | 88.2 / 92.8 | 87.2 / 91.0 | 73.0 / 90.4 | 40.8 / 86.4 |
| 2,500 | 99.56 / 99.6 | 96.8 / 96.8 | 89.96 / 93.2 | 11.16 / 87.3 |
| 10,000 | 94.79 / 98.3 | 87.89 / 96.5 | 55.04 / 93.8 | 4.01 / 55.1 |
| 50,000 | 93.33 / 99.1 | 68.87 / 99.0 | 29.7 / 95.2 | 6.29 / 75.6 |

150-tick runs: every level and size kept all particles alive and all 5 species, 0 NaN energy, 0 NaN repairs (health-150ticks.csv).

## Browser: headless Chrome, NO GPU (SwiftShader software rendering), 1280×800, DPR 1

Live app, boot world then INITIAL_POP = N, sim:restart. Warm-up 2.5 s then 6 s measured (8 s / 10 s at 50k). page ready = navigation to launch screen. respawn → first full tick = sim:restart until the first physics tick that reports ≥ 99% of N (this is the boot cost of a big world). Chrome RSS = all headless Chrome processes. Worker heap is not readable from a headless worker (n/a).

| Particles | Preset | seen | page ready ms | respawn → first full tick ms | fps | frame ms p50 / p95 | sim ticks/s | × sim vs HIGH | main JS heap MB | Chrome RSS MB | alive | species | bonded % |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2,500 | HIGH | 2526 | 362 | 422 | 60.0 | 16.7 / 16.7 | 2.33 | 1.00× | 11.1 | 623 | 2526 | 5 | 26.9 |
| 2,500 | MEDIUM | 2619 | 162 | 116 | 59.1 | 16.7 / 16.7 | 11.82 | 5.07× | 12.2 | 662 | 2617 | 5 | 16.8 |
| 2,500 | LOW | 2687 | 161 | 96 | 59.2 | 16.7 / 16.7 | 18.31 | 7.86× | 14.7 | 650 | 2678 | 5 | 27.3 |
| 2,500 | LOWEST | 2756 | 151 | 93 | 58.6 | 16.7 / 16.7 | 25.98 | 11.15× | 11.5 | 648 | 2751 | 5 | 11.3 |
| 10,000 | HIGH | 10000 | 134 | 774 | 25.3 | 33.3 / 50.0 | 1.16 | 1.00× | 9.7 | 644 | 10000 | 5 | 13.0 |
| 10,000 | MEDIUM | 10000 | 137 | 387 | 22.5 | 33.3 / 50.0 | 3.26 | 2.81× | 17.9 | 632 | 10000 | 5 | 10.7 |
| 10,000 | LOW | 10000 | 144 | 260 | 22.1 | 50.0 / 50.0 | 5.28 | 4.55× | 14.7 | 701 | 9995 | 5 | 9.8 |
| 10,000 | LOWEST | 10000 | 151 | 190 | 23.0 | 50.0 / 50.0 | 7.29 | 6.28× | 13.6 | 674 | 9993 | 5 | 3.5 |
| 50,000 | HIGH | 50000 | 143 | 1639 | 5.7 | 166.7 / 200.0 | 0.58 | 1.00× | 12.0 | 651 | 50000 | 5 | 13.1 |
| 50,000 | MEDIUM | 50000 | 145 | 948 | 5.4 | 183.3 / 250.0 | 1.08 | 1.86× | 16.7 | 670 | 49996 | 5 | 10.6 |
| 50,000 | LOW | 50000 | 150 | 780 | 5.1 | 183.3 / 283.3 | 1.47 | 2.53× | 17.0 | 723 | 50000 | 5 | 5.9 |
| 50,000 | LOWEST | 50000 | 159 | 860 | 5.2 | 183.3 / 216.7 | 1.66 | 2.86× | 18.7 | 711 | 49993 | 5 | 2.4 |

## Multiplex Full fidelity (20 sims × 2,500, worker pool 7), per-sim ticks/s

| Preset | laws | ticks/s per sim (min) | × vs HIGH | frame p95 ms |
|---|---|---|---|---|
| HIGH | full | 0.77 (0.5) | 1.0× | 19.34 |
| MEDIUM | full | 1.72 (1.25) | 2.2× | 20.05 |
| LOW | full top-48 | 12.68 (8.25) | 16.5× | 21.11 |
| LOWEST | full top-16 | 21.22 (17.74) | 27.6× | 20 |

## Particle cap 10,000 → 100,000 (D-040)

**Why upstream lowered it (v9.3.1, commit 031ca5e):** memory, not speed. Commit message: "Reduce maximum allocated particle capacity to 10,000 and keep launch and world population controls aligned." CHANGELOG 4.9.34 → 9.3.1: "Reduced the active particle-pool ceiling and world/launch population caps from 100,000 to 10,000 … Lower preallocated capacity reduces buffer demand; it does not establish a device-independent frame-rate guarantee." No phone measurement or perf number was given.

**Buffer cost** (stride 100 floats × 4 B × cap): 10,000 → 4.0 MB (3.81 MiB); 100,000 → 40 MB (38.15 MiB). One SharedArrayBuffer, shared by the main thread and the physics worker (not copied). The renderer and Pixi sprite pool grow with the live count, not the cap; multiplex shards size their own buffers (capacity = live count + headroom, ≤ 10,000 per sim).

**Measured** (headless Chrome, NO GPU, default boot world ≈ 925 particles, 3 runs each, `cap-memory-raw.csv`):

| Build | main JS heap at boot MB | renderer RSS at boot MB | renderer RSS after one restart MB |
|---|---|---|---|
| cap 10,000 (v9.3.1) | 7.4–10.1 | 240–276 | 248–256 |
| cap 100,000, old `fill(0)` on restart | 7.8–8.9 | 236–242 | 276–318 (+30–60) |
| cap 100,000 + `clearParticleView` (shipped) | 7.8–8.5 | 229–252 | 244–253 |

The SharedArrayBuffer is not in the JS heap and the OS only backs pages that are written, so boot costs the same. But `sim:restart` and world load did `view.fill(0)` over the whole buffer, which commits all 40 MB (Node check: RSS 46 → 84 MB). Fix: `clearParticleView` zeroes only up to the last float that is not +0 (scan from the end; reading does not commit pages; -0 and NaN stop the scan), so it is bit-identical to `fill(0)` (unit test) and small worlds stay at the v9.3.1 footprint. Growing the buffer on demand was not needed (and would mean re-handing a new SharedArrayBuffer to the worker mid-run).

**Golden / bench:** `golden-parity: OK (13 scenarios identical)`; bench hashes unchanged (2,500: 39917ba618ded639, 10,000: af40cf9839ec09d7). The cap does not enter any scenario (all far below 10,000 and no birth reaches the cap).

**POP %:** the multiplex POP % / SIM and the automatic shard curve now use `MULTIPLEX_POP_BASE = 10,000` instead of the cap, so a saved POP % 25 is still 2,500 per sim and a 2×2 auto grid is still 5,000 per sim (with the cap as basis they would have become 25,000 and 50,000). World saves store particle counts and MAX_POP / PARTICLE_COUNT as counts, so they load unchanged; only the defaults of PARTICLE_COUNT and MAX_POP (which equal the cap) go back to 100,000, as before v9.3.1.

