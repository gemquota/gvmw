const { runtimeConfig } = await import('/workspace/vepa/src/state/runtimeConfig.js');
let pairs = 0, near = 0, mid = 0;
runtimeConfig.pairProbe = (kind, v, i, j, w, g) => { if (kind === 'pair') { pairs++; if (g.dist < 30) near++; if (g.dist < 200) mid++; } };

await import('./solve-bench.mjs');
console.log({ pairsPerTick: pairs / 5, nearPerTick: near / 5, midPerTick: mid / 5 });
