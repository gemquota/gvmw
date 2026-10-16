#!/usr/bin/env bash
# Run every Round 1 subject, then build blinded E-1 envelopes.
set -euo pipefail
cd "$(dirname "$0")/.."
PY=${PY:-.venv/bin/python}
for s in C0 F1 F2 F3 U1 CU1 X1 A B1 B2 B3; do "$PY" subjects/run_subject.py "$s" >/dev/null; echo "ran $s"; done
"$PY" experiment/build_envelopes.py
