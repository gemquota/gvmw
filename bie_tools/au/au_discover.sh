#!/bin/bash
# AU discovery: sequential, checkpointed; each step appends to candidates_<tag>.csv. No merge here (AU-only merge done by m_au_merge.py).
cd /tmp
PY=/workspace/bie/.venv/bin/python; D=/workspace/bie_tools/discover.py; T=/workspace/bie_tools
step(){ echo "=== $(date +%T) $*"; "$@"; }
for r in 1 2; do
  f=$T/candidates_homepages.csv; [ -f $f ] && mv $f $T/candidates_homepages_au${r}done_prev.csv
  step $PY $D homepages
  f=$T/candidates_partners.csv; [ -f $f ] && mv $f $T/candidates_partners_au${r}done_prev.csv
  step $PY $D partners
done
HARVEST_ONLY=1 $PY $D telegram > /dev/null; step $PY $D testharvest telegram
step $PY $D urlscan 'domain:cdn.vefrop.com AND date:>now-120d' 'domain:xt30sf.b-cdn.net AND date:>now-120d'
TAG=au_pages step $PY $D pages https://pokiesmate.bet/bonus https://truebluepokies.win/bonus https://auspokieslist.com https://audplay.online https://gday77-australia.co
echo "=== ALL DONE $(date +%T)"
