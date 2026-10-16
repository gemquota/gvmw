# FIDELITY curves: tables

Box: 8 vCPU Xeon, Node 22, NO GPU. Solver = `bench/solver-tps.mjs --speed <level>`, TIDAL_BLOOM bench world. Timing: 30 ticks after 3 warm-up, median of 3 fresh-process runs up to 25,000 and median of 2 at 30,000–50,000 (chosen for time; see the `runs` column in solver-raw.csv). Rows marked † are median of 2. Bonded % at 150 ticks: the tick-150 sample of the long timeline runs (500–10,000; larger sizes in phase 2). Browser: headless Chrome, NO GPU (SwiftShader software rendering), 1280×800, DPR 1. Multiplex: 20 sims × 2,500, Full fidelity, worker pool 7 (measured earlier today in the D-039 batch, not rerun).

## 01 Speed-up vs HIGH (×)

| particles | HIGH | MEDIUM | LOW | LOWEST |
|---|---|---|---|---|
| 500 | 1.00 | 1.34 | 1.83 | 2.33 |
| 1,000 | 1.00 | 2.73 | 2.59 | 3.65 |
| 1,500 | 1.00 | 3.50 | 3.60 | 4.58 |
| 2,000 | 1.00 | 4.09 | 7.44 | 6.54 |
| 2,500 | 1.00 | 3.97 | 6.17 | 4.56 |
| 5,000 | 1.00 | 4.08 | 7.85 | 11.36 |
| 7,500 | 1.00 | 2.89 | 5.85 | 10.98 |
| 10,000 | 1.00 | 3.04 | 5.94 | 7.68 |
| 12,500 | 1.00 | 2.52 | 6.15 | 7.26 |
| 15,000 | 1.00 | 2.24 | 6.54 | 7.98 |
| 17,500 | 1.00 | 2.64 | 6.04 | 8.19 |
| 20,000 | 1.00 | 2.63 | 6.65 | 7.64 |
| 22,500 | 1.00 | 2.35 | 5.87 | 6.81 |
| 25,000 | 1.00 | 2.27 | 5.53 | 6.40 |
| 30,000† | 1.00 | 2.27 | 5.37 | 5.84 |
| 35,000† | 1.00 | 2.04 | 3.75 | 4.51 |
| 40,000† | 1.00 | 2.33 | 4.07 | 5.42 |
| 45,000† | 1.00 | 2.40 | 4.74 | 5.21 |
| 50,000† | 1.00 | 2.49 | 3.73 | 4.60 |

## 02 Solver ticks/s

| particles | HIGH | MEDIUM | LOW | LOWEST |
|---|---|---|---|---|
| 500 | 31.24 | 41.98 | 57.06 | 72.71 |
| 1,000 | 12.82 | 34.97 | 33.25 | 46.84 |
| 1,500 | 6.29 | 22.02 | 22.67 | 28.82 |
| 2,000 | 4.16 | 17.02 | 30.93 | 27.22 |
| 2,500 | 3.66 | 14.53 | 22.59 | 16.68 |
| 5,000 | 2.38 | 9.72 | 18.68 | 27.03 |
| 7,500 | 1.62 | 4.68 | 9.47 | 17.79 |
| 10,000 | 1.76 | 5.35 | 10.45 | 13.51 |
| 12,500 | 1.39 | 3.50 | 8.55 | 10.09 |
| 15,000 | 1.31 | 2.93 | 8.57 | 10.46 |
| 17,500 | 1.13 | 2.98 | 6.83 | 9.25 |
| 20,000 | 1.07 | 2.81 | 7.12 | 8.18 |
| 22,500 | 1.02 | 2.40 | 5.99 | 6.95 |
| 25,000 | 0.88 | 2.00 | 4.87 | 5.63 |
| 30,000† | 0.75 | 1.70 | 4.03 | 4.38 |
| 35,000† | 0.75 | 1.53 | 2.81 | 3.38 |
| 40,000† | 0.55 | 1.28 | 2.24 | 2.98 |
| 45,000† | 0.53 | 1.27 | 2.51 | 2.76 |
| 50,000† | 0.55 | 1.37 | 2.05 | 2.53 |

## 03 Bonded % after 150 ticks

| particles | HIGH | MEDIUM | LOW | LOWEST |
|---|---|---|---|---|

## 04 Bonded % after 30 ticks

| particles | HIGH | MEDIUM | LOW | LOWEST |
|---|---|---|---|---|
| 500 | 88.2 | 87.2 | 73.0 | 40.8 |
| 1,000 | 94.5 | 90.9 | 74.0 | 24.4 |
| 1,500 | 98.2 | 93.5 | 89.3 | 39.8 |
| 2,000 | 99.0 | 97.9 | 89.9 | 16.1 |
| 2,500 | 99.6 | 96.8 | 90.0 | 11.2 |
| 5,000 | 96.8 | 89.8 | 58.3 | 4.2 |
| 7,500 | 99.2 | 96.9 | 87.6 | 12.0 |
| 10,000 | 94.8 | 87.9 | 55.0 | 4.0 |
| 12,500 | 95.7 | 91.2 | 51.5 | 6.0 |
| 15,000 | 95.0 | 92.4 | 52.7 | 9.7 |
| 17,500 | 98.5 | 95.6 | 49.1 | 9.3 |
| 20,000 | 98.2 | 94.3 | 60.2 | 17.3 |
| 22,500 | 99.2 | 97.2 | 71.6 | 19.9 |
| 25,000 | 98.8 | 96.2 | 63.0 | 21.2 |
| 30,000† | 98.6 | 96.3 | 77.1 | 32.2 |
| 35,000† | 86.5 | 82.1 | 46.6 | 14.2 |
| 40,000† | 94.7 | 88.7 | 29.6 | 9.9 |
| 45,000† | 97.7 | 93.2 | 68.8 | 29.4 |
| 50,000† | 98.2 | 92.2 | 63.5 | 21.9 |

## 05 Browser sim ticks/s (headless Chrome, NO GPU)

| particles | HIGH | MEDIUM | LOW | LOWEST |
|---|---|---|---|---|

## 06 Browser fps (headless Chrome, NO GPU)

| particles | HIGH | MEDIUM | LOW | LOWEST |
|---|---|---|---|---|

## 07 Browser frame time p95 ms (headless Chrome, NO GPU)

| particles | HIGH | MEDIUM | LOW | LOWEST |
|---|---|---|---|---|

## 08 Browser main JS heap MB

| particles | HIGH | MEDIUM | LOW | LOWEST |
|---|---|---|---|---|

## 09 Bench child RSS MB at end of timed run

| particles | HIGH | MEDIUM | LOW | LOWEST |
|---|---|---|---|---|
| 500 | 161 | 116 | 206 | 179 |
| 1,000 | 160 | 142 | 135 | 133 |
| 1,500 | 152 | 158 | 182 | 165 |
| 2,000 | 154 | 165 | 144 | 172 |
| 2,500 | 145 | 139 | 139 | 160 |
| 5,000 | 110 | 121 | 171 | 188 |
| 7,500 | 156 | 125 | 174 | 206 |
| 10,000 | 180 | 196 | 223 | 196 |
| 12,500 | 188 | 230 | 204 | 210 |
| 15,000 | 193 | 192 | 192 | 217 |
| 17,500 | 190 | 219 | 232 | 186 |
| 20,000 | 190 | 194 | 218 | 190 |
| 22,500 | 213 | 200 | 220 | 204 |
| 25,000 | 216 | 224 | 191 | 181 |
| 30,000 | 195 | 190 | 204 | 234 |
| 35,000 | 172 | 197 | 219 | 208 |
| 40,000 | 230 | 214 | 199 | 213 |
| 45,000 | 209 | 188 | 189 | 174 |
| 50,000 | 208 | 241 | 214 | 195 |

## 10 Bench child heap MB at end of timed run

| particles | HIGH | MEDIUM | LOW | LOWEST |
|---|---|---|---|---|
| 500 | 11.7 | 12.5 | 12.2 | 13.0 |
| 1,000 | 12.9 | 14.5 | 13.3 | 19.9 |
| 1,500 | 15.6 | 13.9 | 14.4 | 14.6 |
| 2,000 | 12.0 | 10.8 | 12.4 | 12.8 |
| 2,500 | 10.9 | 13.2 | 13.7 | 18.1 |
| 5,000 | 18.6 | 20.4 | 23.8 | 28.7 |
| 7,500 | 17.7 | 21.8 | 33.3 | 37.0 |
| 10,000 | 27.5 | 38.9 | 15.7 | 20.2 |
| 12,500 | 31.0 | 39.6 | 28.8 | 35.3 |
| 15,000 | 18.5 | 13.7 | 22.8 | 34.0 |
| 17,500 | 12.5 | 16.7 | 42.6 | 22.7 |
| 20,000 | 15.2 | 21.6 | 36.0 | 13.0 |
| 22,500 | 17.9 | 26.9 | 36.2 | 25.4 |
| 25,000 | 23.7 | 22.9 | 47.9 | 30.0 |
| 30,000 | 34.7 | 26.4 | 27.4 | 38.1 |
| 35,000 | 29.0 | 43.0 | 33.6 | 43.9 |
| 40,000 | 11.4 | 24.0 | 35.1 | 37.2 |
| 45,000 | 24.4 | 38.0 | 39.3 | 34.2 |
| 50,000 | 38.2 | 32.3 | 32.1 | 35.7 |

## 11 Multiplex Full fidelity per-sim ticks/s

| level | law count | ticks/s per sim | slowest sim | × vs HIGH | frame p95 ms |
|---|---|---|---|---|---|
| HIGH | 136 | 0.77 | 0.5 | 1.0× | 19.34 |
| MEDIUM | 136 | 1.72 | 1.25 | 2.2× | 20.05 |
| LOW | 48 | 12.68 | 8.25 | 16.5× | 21.11 |
| LOWEST | 16 | 21.22 | 17.74 | 27.6× | 20 |

## 12 Trade-off: speed-up vs bonded % after 150 ticks

| level | particles | speed-up | bonded % @150 |
|---|---|---|---|

## 13 ms per tick per 1,000 particles

| particles | HIGH | MEDIUM | LOW | LOWEST |
|---|---|---|---|---|
| 500 | 64.02 | 47.64 | 35.04 | 27.50 |
| 1,000 | 78.01 | 28.60 | 30.07 | 21.35 |
| 1,500 | 106.03 | 30.27 | 29.41 | 23.13 |
| 2,000 | 120.27 | 29.38 | 16.16 | 18.37 |
| 2,500 | 109.22 | 27.54 | 17.71 | 23.97 |
| 5,000 | 83.99 | 20.57 | 10.71 | 7.40 |
| 7,500 | 82.46 | 28.48 | 14.08 | 7.49 |
| 10,000 | 56.86 | 18.70 | 9.57 | 7.40 |
| 12,500 | 57.63 | 22.85 | 9.36 | 7.93 |
| 15,000 | 51.08 | 22.78 | 7.78 | 6.37 |
| 17,500 | 50.62 | 19.14 | 8.37 | 6.18 |
| 20,000 | 46.77 | 17.82 | 7.02 | 6.11 |
| 22,500 | 43.49 | 18.52 | 7.42 | 6.39 |
| 25,000 | 45.39 | 19.96 | 8.22 | 7.10 |
| 30,000† | 44.22 | 19.60 | 8.28 | 7.60 |
| 35,000† | 38.19 | 18.73 | 10.17 | 8.47 |
| 40,000† | 45.28 | 19.53 | 11.16 | 8.39 |
| 45,000† | 41.95 | 17.48 | 8.84 | 8.05 |
| 50,000† | 36.44 | 14.59 | 9.75 | 7.90 |

## Timelines

Timelines: ONE run per level and size, 2,000 ticks, sampled at 50, 100, …, 2,000. The 32 runs ran 8 at a time on the 8-vCPU box, so their ticks/s is lower than the quiet speed curves (01, 02); read them for the trend over time. The bench world does not add offspring to the buffer, so births = offspring the solver requested (not spawned) and deaths = start count − alive.

## 20 Bonded % over time, 1,500 particles

| particles | HIGH | MEDIUM | LOW | LOWEST |
|---|---|---|---|---|
| 50 | 98.8 | – | – | – |

## 20 Bonded % over time, 7,500 particles

| particles | HIGH | MEDIUM | LOW | LOWEST |
|---|---|---|---|---|
| 50 | – | 97.3 | – | – |

## 20 Bonded % over time, 10,000 particles

| particles | HIGH | MEDIUM | LOW | LOWEST |
|---|---|---|---|---|
| 50 | – | – | 73.8 | 10.6 |
| 100 | – | – | – | 33.4 |
| 150 | – | – | – | 55.1 |

## 22 Ticks/s per window over time, 1,500 particles

| particles | HIGH | MEDIUM | LOW | LOWEST |
|---|---|---|---|---|
| 50 | 5.03 | – | – | – |

## 22b Cumulative ticks/s at the last sample, 1,500 particles

| level | ticks run | cumulative ticks/s |
|---|---|---|
| HIGH | 50 | 5.032 |

## 22 Ticks/s per window over time, 7,500 particles

| particles | HIGH | MEDIUM | LOW | LOWEST |
|---|---|---|---|---|
| 50 | – | 3.45 | – | – |

## 22b Cumulative ticks/s at the last sample, 7,500 particles

| level | ticks run | cumulative ticks/s |
|---|---|---|
| MEDIUM | 50 | 3.452 |

## 22 Ticks/s per window over time, 10,000 particles

| particles | HIGH | MEDIUM | LOW | LOWEST |
|---|---|---|---|---|
| 50 | – | – | 6.16 | 7.78 |
| 100 | – | – | – | 13.73 |
| 150 | – | – | – | 12.47 |

## 22b Cumulative ticks/s at the last sample, 10,000 particles

| level | ticks run | cumulative ticks/s |
|---|---|---|
| LOW | 50 | 6.163 |
| LOWEST | 150 | 10.657 |

## 21 Alive, species, births, deaths, energy over the timeline runs

| particles | level | last tick | min alive | alive at end | min species | births (requested) | deaths | mean energy @50 | mean energy @end | NaN repairs | NaN energy |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1,500 | HIGH | 50 | 1500 | 1500 | 5 | 0 | 0 | 66.80 | 66.80 | 0 | 0 |
| 7,500 | MEDIUM | 50 | 7500 | 7500 | 5 | 0 | 0 | 74.35 | 74.35 | 0 | 0 |
| 10,000 | LOW | 50 | 10000 | 10000 | 5 | 0 | 0 | 75.13 | 75.13 | 0 | 0 |
| 10,000 | LOWEST | 150 | 10000 | 10000 | 5 | 0 | 0 | 75.15 | 75.24 | 0 | 0 |

