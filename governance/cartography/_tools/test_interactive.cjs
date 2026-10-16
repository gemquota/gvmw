// Headless check of role-map-interactive.html. Usage: NODE_PATH=/tmp/mmd/node_modules node _tools/test_interactive.cjs
const puppeteer = require('puppeteer');
const path = require('path');
const FILE = path.resolve(__dirname, '..', 'role-map-interactive.html');
const SHOT = path.resolve(__dirname, '..', 'role-map-interactive.png');
(async () => {
  const b = await puppeteer.launch({executablePath: '/usr/bin/google-chrome', headless: 'new', args: ['--no-sandbox', '--disable-gpu']});
  const p = await b.newPage(); await p.setViewport({width: 1600, height: 1000});
  const errors = [], external = [], res = {};
  p.on('console', m => { if (['error', 'warning'].includes(m.type())) errors.push(m.type() + ': ' + m.text()); });
  p.on('pageerror', e => errors.push('pageerror: ' + e.message));
  p.on('request', r => { if (!r.url().startsWith('file://') && !r.url().startsWith('data:')) external.push(r.url()); });
  await p.goto('file://' + FILE, {waitUntil: 'load'});
  res.counts = await p.evaluate(() => window.__roleMap && {nodes: window.__roleMap.nodes, edges: window.__roleMap.edges, drawnNodes: document.querySelectorAll('.node').length, drawnEdges: document.querySelectorAll('path.edge').length});
  const red = () => p.evaluate(() => [...document.querySelectorAll('path.edge[stroke="#d50000"]')].filter(e => e.style.display !== 'none').length);
  res.redVisible = await red();
  // hover Inferer -> neighbours highlighted, others dimmed
  const box = async k => { const e = await p.$(`.node[data-key="${k}"]`); return e.boundingBox(); };
  let bb = await box('INF'); await p.mouse.move(bb.x + bb.width/2, bb.y + bb.height/2);
  res.hover = await p.evaluate(() => ({dimmed: document.querySelectorAll('.node.dim').length, lit: document.querySelectorAll('.node:not(.dim)').length, labelsOn: document.querySelectorAll('.elabel.on').length}));
  await p.mouse.move(5, 990);
  // toggle Safeguard-first off and on
  await p.click('input[data-type="safeguard"]'); res.redAfterOff = await red();
  await p.click('input[data-type="safeguard"]'); res.redAfterOn = await red();
  // search
  await p.type('#search', 'safe'); res.searchSafe = await p.evaluate(() => [...document.querySelectorAll('.node.match')].map(n => n.dataset.key));
  await p.keyboard.press('Enter'); res.enterOpens = await p.evaluate(() => document.querySelector('#panel').classList.contains('open') && document.querySelector('#pbody h3').textContent);
  await p.keyboard.press('Escape'); await p.click('#search', {clickCount: 3}); await p.keyboard.press('Backspace');
  // zoom + pan + drag + reset
  bb = await box('SCO'); const t0 = await p.evaluate(() => document.querySelector('.node[data-key="SCO"]').getAttribute('transform'));
  await p.mouse.move(bb.x + 20, bb.y + 20); await p.mouse.down(); await p.mouse.move(bb.x + 90, bb.y + 70, {steps: 6}); await p.mouse.up();
  const t1 = await p.evaluate(() => document.querySelector('.node[data-key="SCO"]').getAttribute('transform'));
  const before = await p.evaluate(() => document.getElementById('vp').getAttribute('transform'));
  await p.mouse.move(800, 500); await p.mouse.wheel({deltaY: -400});
  await p.mouse.move(700, 900); await p.mouse.down(); await p.mouse.move(760, 940, {steps: 5}); await p.mouse.up();
  const afterZoomPan = await p.evaluate(() => document.getElementById('vp').getAttribute('transform'));
  res.dragDidNotOpenPanel = !(await p.evaluate(() => document.querySelector('#panel').classList.contains('open')));
  await p.click('#reset');
  const afterReset = await p.evaluate(() => [document.getElementById('vp').getAttribute('transform'), document.querySelector('.node[data-key="SCO"]').getAttribute('transform')]);
  res.zoomPanChanged = before !== afterZoomPan; res.dragMoved = t0 !== t1; res.resetRestores = afterReset[0] === before && afterReset[1] === t0;
  // toggle former off/on
  await p.click('#showFormer'); res.hiddenFormer = await p.evaluate(() => [...document.querySelectorAll('.node')].filter(n => n.style.display === 'none').length); await p.click('#showFormer');
  // click Imitator -> panel
  bb = await box(process.env.CLICK || 'IMI'); await p.mouse.click(bb.x + bb.width/2, bb.y + bb.height/2);
  res.panel = await p.evaluate(() => { const b = document.getElementById('pbody'); return {open: document.getElementById('panel').classList.contains('open'), title: b.querySelector('h3').textContent,
    dl: [...b.querySelectorAll('dt')].map(d => d.textContent + ': ' + d.nextSibling.textContent), bullets: b.querySelectorAll('ul:not(.rel) li').length,
    relHeads: [...b.querySelectorAll('h4')].map(h => h.textContent), relLinks: b.querySelectorAll('.rel a').length}; });
  await p.mouse.move(5, 990);
  await new Promise(r => setTimeout(r, 500)); // let the panel finish sliding in
  await p.screenshot({path: SHOT});
  res.errors = errors; res.external = external;
  console.log(JSON.stringify(res, null, 1));
  await b.close();
  process.exit(errors.length || external.length ? 1 : 0);
})().catch(e => { console.error(e); process.exit(2); });
