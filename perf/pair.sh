#!/bin/bash
# usage: pair.sh pop secs  — browser A(4185)/B(4186) pairs ×2, worker ticks/s = 1000/intervalMs
P=$1; T=${2:-8}
for i in 1 2; do
  for L in A:4185 B:4186; do
    n=${L%%:*}; port=${L##*:}
    URL=http://127.0.0.1:$port/ node /workspace/perf/profile.mjs $P single $T 2>/dev/null > /workspace/perf/logs/pair-$P-$n-$i.json
    python3 -c "
import json;d=json.load(open('/workspace/perf/logs/pair-$P-$n-$i.json'));w=d['worker'] or {}
iv=w.get('intervalMs');print('$n run$i pop $P', 'tps', round(1000/iv,2) if iv else None,'workerTickMs',w.get('workerTickMs'),'particles',w.get('particles'),'fps',d['fps'])"
  done
done
