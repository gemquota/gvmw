const root = process.argv[2];
const { runSpeedWorld } = await import(root + '/tests/helpers/speedWorld.js');
const [count, ticks, seed, spread, speed] = [+process.argv[3], +process.argv[4], +process.argv[5], +process.argv[6], process.argv[7] || ''];
const params = {}; for (const k of speed.split(',').filter(Boolean)) params[k] = 1;
const t0 = Date.now();
const { view } = runSpeedWorld({ count, ticks, seed, spread, params });
let bad = 0; for (let i = 0; i < view.length; i++) if (!Number.isFinite(view[i])) bad++;
console.log(JSON.stringify({ root: root.split('/').pop(), count, ticks, seed, spread, speed, bad, ms: Date.now() - t0 }));
