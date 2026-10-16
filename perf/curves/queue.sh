#!/bin/bash
while pgrep -f "curves/solver.py" >/dev/null; do sleep 10; done
echo "phase2 solver 30k-50k runs=2 $(date)"
SIZES=30000,35000,40000,45000,50000 RUNS=2 python3 /workspace/perf/curves/solver.py
echo "health $(date)"
PAR=4 python3 /workspace/perf/curves/health.py
echo "browser $(date)"
cd /workspace/perf; (python3 serve-coi.py 4190 /workspace/perf/build-100k >/dev/null 2>&1 &); sleep 1
/workspace/tools/node22/node-v22.23.3-linux-x64/bin/node /workspace/perf/curves/browser.mjs /workspace/perf/fid/presets4.json 2500,5000,10000,15000,20000,25000,50000 /workspace/out/fidelity-curves/browser-raw.csv
pkill -f "serve-coi.py 4190"
echo "all done $(date)"
