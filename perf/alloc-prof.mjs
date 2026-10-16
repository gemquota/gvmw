// usage: node alloc-prof.mjs <repo> <count> <ticks>  — allocation sites incl. collected objects
import { Session } from 'node:inspector/promises';
const [repo, countArg = '1000', ticksArg = '8'] = process.argv.slice(2);
const s = new Session(); s.connect();
process.argv = [process.argv[0], `${repo}/bench/solver-tps.mjs`, '--child', countArg, ticksArg, '3', 'tidal'];
const realExit = process.exit; let done; const finished = new Promise((r) => { done = r; });
process.exit = () => done();
const origWrite = process.stdout.write.bind(process.stdout); process.stdout.write = () => true;
await s.post('HeapProfiler.enable');
await s.post('HeapProfiler.startSampling', { samplingInterval: 1024, includeObjectsCollectedByMajorGC: true, includeObjectsCollectedByMinorGC: true });
await import(`${repo}/bench/solver-tps.mjs`);
await finished;
const { profile } = await s.post('HeapProfiler.stopSampling');
const agg = new Map();
const walk = (n, stack) => {
  const cf = n.callFrame; const key = `${cf.functionName || '(anon)'} ${cf.url.split('/').pop()}:${cf.lineNumber + 1}`;
  agg.set(key, (agg.get(key) || 0) + n.selfSize);
  for (const c of n.children || []) walk(c);
};
walk(profile.head);
const tot = [...agg.values()].reduce((a, b) => a + b, 0);
process.stdout.write = origWrite;
for (const [k, v] of [...agg.entries()].sort((a, b) => b[1] - a[1]).slice(0, 25)) console.log(`${(100 * v / tot).toFixed(1).padStart(5)}% ${(v / 1e6).toFixed(1).padStart(8)}MB ${k}`);
realExit(0);
