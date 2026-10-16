source /workspace/tools/codey/env.sh >/dev/null 2>&1; cd /workspace/vepa
F="PAIRWISE_BUDGET=48,SPEED_MID_RANGE=120,SPEED_SYMBIOSIS_RANGE=30,SPEED_SOCIAL_EVERY=2"
for pb in 20 24 512; do node bench/solver-tps.mjs --sizes 10000 --runs 1 --json --speed $F,SPEED_PAIR_BUDGET=$pb | python3 -c "import json,sys;d=json.load(sys.stdin);print('$pb',d['sizes']['10000'])"; done
