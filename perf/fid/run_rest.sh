#!/bin/bash
cd /workspace/vepa
N=/workspace/tools/node22/node-v22.23.3-linux-x64/bin/node
$N bench/multiplex-bench.mjs --fidelity --json > /workspace/perf/fid/mpx-fid4.json 2> /workspace/perf/fid/mpx-fid4.err
echo mpx-done
$N /workspace/perf/fid/browser_bench4.mjs /workspace/perf/fid/presets4.json 2500,10000,50000 /workspace/perf/fid/browser4-raw.csv
echo browser-done
