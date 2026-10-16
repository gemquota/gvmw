#!/bin/bash
N=/workspace/tools/node22/node-v22.23.3-linux-x64/bin/node
while pgrep -f "curves/solver.py" >/dev/null; do sleep 10; done
echo "phase2 solver 30k-50k runs=2 $(date)"
SIZES=30000,35000,40000,45000,50000 RUNS=2 python3 /workspace/perf/curves/solver.py
echo "timeline $(date)"
cd /workspace/vepa
TL=/workspace/out/fidelity-curves/timeline-raw
mkdir -p $TL
# HIGH split per size (slowest); 10k HIGH capped at 1,000 ticks. Other levels: one lane each, sizes in turn.
for n in 1000 2500 5000; do $N /workspace/perf/curves/timeline.mjs $n high 2000 $TL/HIGH-$n.csv & done
$N /workspace/perf/curves/timeline.mjs 10000 high 1000 $TL/HIGH-10000.csv &
for lv in medium low lowest; do ( for n in 1000 2500 5000 10000; do $N /workspace/perf/curves/timeline.mjs $n $lv 2000 $TL/${lv^^}-$n.csv; done ) & done
wait
echo "health $(date)"
PAR=4 python3 /workspace/perf/curves/health.py
echo "browser $(date)"
cd /workspace/perf; (python3 serve-coi.py 4190 /workspace/perf/build-100k >/dev/null 2>&1 &); sleep 1
$N /workspace/perf/curves/browser.mjs /workspace/perf/fid/presets4.json 2500,5000,10000,15000,20000,25000,50000 /workspace/out/fidelity-curves/browser-raw.csv
pkill -f "serve-coi.py 4190"
echo "all done $(date)"
