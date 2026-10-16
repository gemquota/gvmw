source /workspace/tools/codey/env.sh >/dev/null 2>&1; cd /workspace/vepa
OUT=/workspace/perf/logs/sliders.jsonl; : > $OUT
run() { node bench/solver-tps.mjs --sizes 1000,2500,10000 --runs 1 --json --speed "$1" | python3 -c "
import json,sys;d=json.load(sys.stdin)
for k,v in d['sizes'].items(): print(json.dumps({'v':'$1','n':int(k),'tps':v['ticksPerSec'],'hash':v['hash'],'alive':v['alive'],'species':v['species'],'bonded':v['bonded'],'meanEnergy':v['meanEnergy']}))" >> $OUT; }
run none
for v in 8 16 24 48 192 512; do run PAIRWISE_BUDGET=$v; done
for v in 60 120 300 600; do run SPEED_MID_RANGE=$v; done
for v in 10 60; do run SPEED_NEAR_RANGE=$v; done
for v in 4 8 20 48; do run SPEED_PAIR_BUDGET=$v; done
for v in 30 120; do run SPEED_SYMBIOSIS_RANGE=$v; done
for v in 2 4 8 16 100; do run SPEED_SOCIAL_EVERY=$v; done
run fast
echo DONE >> $OUT
