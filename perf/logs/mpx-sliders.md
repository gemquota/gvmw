Box: 8 vCPU, no GPU; pool 7 workers; FIELD-ONCE true; 4s per case after 1s warm-up.

| Case | Sims × particles | Laws | Ticks | Main ms med / p95 | Frame ms med / p95 | Sim ms / tick | Sim ms / frame (all sims) | Ticks/s per sim (min) | Skipped | 60 fps |
|---|---|---|---|---|---|---|---|---|---|---|
| Full fidelity speed=none | 20 × 2500 | full | adaptive / pool 7 | 0.02 / 1.09 | 16.67 / 19.46 | 458.24 | 145.03 | 0.79 (0.5) | 0 | yes |
| Full fidelity speed=PAIRWISE_BUDGET=48 | 20 × 2500 | full | adaptive / pool 7 | 0.02 / 0.71 | 16.67 / 18.76 | 430.72 | 140.74 | 0.8 (0.5) | 0 | yes |
| Full fidelity speed=SPEED_MID_RANGE=120 | 20 × 2500 | full | adaptive / pool 7 | 0.02 / 0.96 | 16.67 / 19.05 | 417.73 | 135.22 | 0.8 (0.5) | 0 | yes |
| Full fidelity speed=SPEED_PAIR_BUDGET=20 | 20 × 2500 | full | adaptive / pool 7 | 0.01 / 0.98 | 16.67 / 19.11 | 273.45 | 142.43 | 1.35 (1) | 0 | yes |
| Full fidelity speed=SPEED_SYMBIOSIS_RANGE=30 | 20 × 2500 | full | adaptive / pool 7 | 0.01 / 0.87 | 16.67 / 18.67 | 430.24 | 141.9 | 0.79 (0.5) | 0 | yes |
| Full fidelity speed=SPEED_SOCIAL_EVERY=2 | 20 × 2500 | full | adaptive / pool 7 | 0.01 / 0.68 | 16.67 / 18.7 | 414.54 | 141.36 | 0.88 (0.75) | 0 | yes |
| Full fidelity speed=fast | 20 × 2500 | full | adaptive / pool 7 | 0.01 / 1 | 16.67 / 19.41 | 216.6 | 142.55 | 1.61 (1.25) | 0 | yes |
| Full fidelity LAW COUNT 96 | 20 × 2500 | full top-96 | adaptive / pool 7 | 0.03 / 0.97 | 16.67 / 20 | 335.81 | 141.89 | 1.12 (0.5) | 0 | yes |
| Full fidelity LAW COUNT 48 | 20 × 2500 | full top-48 | adaptive / pool 7 | 0.46 / 1.55 | 16.67 / 19.98 | 170.97 | 144.92 | 2.22 (1) | 0 | yes |
| Full fidelity LAW COUNT 16 | 20 × 2500 | full top-16 | adaptive / pool 7 | 0.8 / 5.3 | 16.67 / 20 | 29.89 | 144.51 | 4.55 (1.25) | 0 | yes |
| Full fidelity LAW COUNT 16 + speed=fast | 20 × 2500 | full top-16 | adaptive / pool 7 | 1.76 / 10.89 | 16.67 / 19.93 | 16.5 | 132.71 | 11.52 (7.76) | 0 | yes |
rc=0
