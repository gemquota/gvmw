#!/bin/bash
source /workspace/tools/codey/env.sh >/dev/null 2>&1
cd /workspace/perf/nansweep
for root in /tmp/wt-nanbase /workspace/vepa; do
 for sz in "1000 600" "2500 600" "10000 200"; do
  for sp in none SPEED_NEIGHBORS_48 SPEED_NARROW_MID SPEED_PAIR_CAP SPEED_NEAR_SYMBIOSIS SPEED_SOCIAL_HALF SPEED_FAST; do echo "$root $sz $sp"; done; done; done |
 xargs -P 4 -L 1 bash -c 'node /workspace/perf/nansweep/nansweep.mjs $0 --child $1 $2 0 tidal $3' > sweep.jsonl 2> sweep.err
echo DONE >> sweep.err
