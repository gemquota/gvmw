#!/bin/bash
# 150-tick behaviour runs (timing not used), all levels x sizes, a few in parallel.
cd /workspace/vepa
N=/workspace/tools/node22/node-v22.23.3-linux-x64/bin/node
mkdir -p /workspace/perf/fid/h150
for lv in high medium low lowest; do
  for n in 100 500 2500 10000 50000; do
    $N bench/solver-tps.mjs --sizes $n --runs 1 --ticks 150 --warm 0 --json --speed $lv > /workspace/perf/fid/h150/$lv-$n.json 2>&1 &
  done
  wait
done
