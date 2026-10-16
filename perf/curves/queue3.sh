#!/bin/bash
# Phase 1: speed pass (19 sizes) -> long timelines 500..10k x 4 levels (8 balanced lanes) -> browser subset. Phase 2 later: health/timelines >10k.
N=/workspace/tools/node22/node-v22.23.3-linux-x64/bin/node
TLM=/workspace/perf/curves/timeline.mjs
TL=/workspace/out/fidelity-curves/timeline-raw; mkdir -p $TL
while pgrep -f "curves/solver.py" >/dev/null; do sleep 10; done
echo "phase2 solver 30k-50k runs=2 $(date)"
SIZES=30000,35000,40000,45000,50000 RUNS=2 python3 /workspace/perf/curves/solver.py
echo "timeline $(date)"
cd /workspace/vepa
lane(){ for spec in "$@"; do lv=${spec%:*}; n=${spec#*:}; [ -s $TL/${lv^^}-$n.csv ] && grep -q ",2000,2000," $TL/${lv^^}-$n.csv && continue; rm -f $TL/${lv^^}-$n.csv; $N $TLM $n $lv 2000 $TL/${lv^^}-$n.csv; echo "tl done $lv $n $(date +%T)"; done; }
lane high:10000 &
lane high:7500 &
lane high:5000 high:500 medium:500 medium:1000 &
lane high:2500 high:2000 &
lane high:1500 high:1000 medium:10000 medium:1500 &
lane medium:7500 medium:5000 medium:2500 medium:2000 &
lane low:10000 low:7500 low:5000 low:2500 low:2000 low:1500 low:1000 low:500 &
lane lowest:10000 lowest:7500 lowest:5000 lowest:2500 lowest:2000 lowest:1500 lowest:1000 lowest:500 &
wait
echo "browser $(date)"
cd /workspace/perf; (python3 serve-coi.py 4190 /workspace/perf/build-100k >/dev/null 2>&1 &); sleep 1
$N /workspace/perf/curves/browser.mjs /workspace/perf/fid/presets4.json 2500,5000,10000,15000,20000,25000,50000 /workspace/out/fidelity-curves/browser-raw.csv
pkill -f "serve-coi.py 4190"
echo "phase1 done $(date)"
