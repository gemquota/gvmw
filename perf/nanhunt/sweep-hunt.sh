#!/bin/bash
source /workspace/tools/codey/env.sh >/dev/null 2>&1
cd /tmp/nanhunt
run() { echo "== $*"; timeout 1500 node /workspace/perf/nanhunt/hunt.mjs "$@" 2>&1 | head -c 1500; echo; }
export -f run
{
for o in none SPEED_NEIGHBORS_48 SPEED_NARROW_MID SPEED_PAIR_CAP SPEED_NEAR_SYMBIOSIS SPEED_SOCIAL_HALF SPEED_FAST; do echo "2500 600 $o tidal"; done
echo "2500 600 none all"; echo "2500 600 SPEED_FAST all"; echo "10000 200 none all"
} | xargs -P 5 -L 1 bash -c 'run $0 $1 $2 /tmp/nanhunt/src $3' > /workspace/perf/logs/sweep-hunt.log 2>&1
MODE=dna bash -c 'run 2500 600 SPEED_FAST /tmp/nanhunt/src tidal; run 2500 600 none /tmp/nanhunt/src all' >> /workspace/perf/logs/sweep-hunt.log 2>&1
echo SWEEPDONE >> /workspace/perf/logs/sweep-hunt.log
