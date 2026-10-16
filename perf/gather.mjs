// mean / p50 / p90 / max neighbour-gather size and distance spread in the bench:solver world
const R='/workspace/vepa';
const { WORLD_SIZE } = await import(R+'/src/constants.js');
const G = await import(R+'/src/physics/spatialGrid.js');
for (const N of [300,1000,2500,10000]) {
  let s = 0x9e3779b9 ^ N; const rng = () => { s = (Math.imul(s, 1664525) + 1013904223) >>> 0; return s / 4294967296; };
  const P=[]; for (let i=0;i<N;i++) P.push([rng()*WORLD_SIZE,rng()*WORLD_SIZE,rng()*WORLD_SIZE]);
  const dim=Math.max(12,Math.min(64,Math.round(Math.cbrt(N/1.4))));
  const g=G.createGrid? G.createGrid(dim,100): null;
  if(!g){console.log(Object.keys(G));process.exit()}
  G.clear(g); P.forEach((p,i)=>G.insert(g,i,p[0],p[1],p[2],WORLD_SIZE));
  const out=new Array(5000); const cnt=[]; let d200=0,d120=0,d30=0,tot=0;
  for (let i=0;i<N;i++){ const c=G.getNeighbors(g,P[i][0],P[i][1],P[i][2],WORLD_SIZE,out); cnt.push(c-1);
    for(let k=0;k<c;k++){const j=out[k]; if(j===i)continue; let d=0; for(let a=0;a<3;a++){let x=Math.abs(P[j][a]-P[i][a]); if(x>WORLD_SIZE/2)x=WORLD_SIZE-x; d+=x*x;} d=Math.sqrt(d); tot++; if(d<200)d200++; if(d<120)d120++; if(d<30)d30++;}}
  cnt.sort((a,b)=>a-b);
  console.log(JSON.stringify({N,dim,cell:+(WORLD_SIZE/dim).toFixed(0),mean:+(cnt.reduce((a,b)=>a+b,0)/N).toFixed(1),p50:cnt[N>>1],p90:cnt[Math.floor(N*0.9)],max:cnt[N-1],fracLt30:+(d30/tot).toFixed(3),fracLt120:+(d120/tot).toFixed(3),fracLt200:+(d200/tot).toFixed(3)}));
}
