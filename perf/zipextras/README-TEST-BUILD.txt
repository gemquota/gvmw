VEPA test build — branch codey/complete-plans @ 657cacc (not pushed)

1. Unzip anywhere.
2. In the vepa-test-build folder run:   python3 serve-local.py
3. Open http://127.0.0.1:8000/ in Chrome or Edge.

The local server adds the cross-origin-isolation headers the simulator needs;
opening index.html directly from disk will not work.

This build includes the perf round PERF-2..PERF-8 (results-identical: golden
parity 13/13 and the bench:solver hashes are unchanged).

Speed options (D-034), all OFF by default and each CHANGES RESULTS when on:
SETUP > WORLD > PERFORMANCE > SPEED (neighbour limit 48, narrow mid range,
pair cap per tick, nearby-only symbiosis & parasite, social/info laws every
2nd tick, FAST bundle) and, in Chaos Multiplex > GRID & PERF, FULL FIDELITY ·
LIGHT LAWS. See docs/SPEED-OPTIONS.md in the repo.
