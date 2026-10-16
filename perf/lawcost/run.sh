#!/bin/bash
source /workspace/tools/codey/env.sh >/dev/null 2>&1
cd /workspace/perf/lawcost
LAWS=$(node -e 'import("/workspace/vepa/src/constants.js").then(c=>console.log(Object.keys(c.LAW_INDEXES).join(" ")))')
: > loo.jsonl
for rep in 1 2; do
  node loo.mjs /tmp/wt-noguard 1000 15 5 none >> loo.jsonl
  for L in $LAWS; do node loo.mjs /tmp/wt-noguard 1000 15 5 $L >> loo.jsonl; done
done
echo DONE >> loo.jsonl
