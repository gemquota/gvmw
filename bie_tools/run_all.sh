#!/bin/bash
# Sequential, checkpointed discovery runner. Each step appends rows to candidates_<tag>.csv as it goes; merge after each step.
cd /workspace/bie
PY=.venv/bin/python; D=/workspace/bie_tools/discover.py
step(){ echo "=== $(date +%T) $*"; "$@"; $PY $D merge; }
step $PY $D testharvest telegram
step $PY $D testharvest urlscan
step $PY $D testharvest sameip
TAG=websearch step $PY $D file /workspace/bie_tools/search_v3.txt
for round in 3 4 5; do
  before=$(wc -l < in/config/newurls_found.txt)
  for src in partners homepages; do
    f=/workspace/bie_tools/candidates_$src.csv; [ -f $f ] && mv $f /workspace/bie_tools/candidates_${src}_r$((round-1))done.csv
    step $PY $D $src
  done
  HARVEST_ONLY=1 $PY $D telegram > /dev/null; step $PY $D testharvest telegram   # new TG handles from new homepages
  after=$(wc -l < in/config/newurls_found.txt); echo "round $round added $((after-before))"
  [ $((after-before)) -lt 25 ] && break
done
echo "=== ALL DONE $(date +%T)"
