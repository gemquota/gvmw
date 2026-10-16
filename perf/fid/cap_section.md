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
