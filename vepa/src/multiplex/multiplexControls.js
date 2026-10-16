// ============================================================================
// VEPA4 — Chaos Multiplex run controls (D-044)
// UNDO / REDO of iterates, the full-screen long-press PEEK overlay, saved
// shard / generation SNAPSHOTS (IndexedDB) with RESTART / SEED / RESTORE /
// COMPARE, and the in-run randomisation strength + decay-per-generation
// sliders. Mounted by multiplexUI.js into the multiplex overlay + drawer.
// ============================================================================

import {
  captureGeneration,
  restoreGeneration,
  snapshotShardFull,
  shardQuickStats,
  getFitnessReport,
  setPeekCanvas,
  sourceFromSnapshot,
  seedFromSnapshot,
  loadSnapshotsUndoable,
  digestGeneration,
  VARIATION_FLOOR,
} from './multiplex.js';
import { createGenerationStack } from './generationStack.js';
import { createSnapshotStore, buildSnapshotRecord } from './snapshotStore.js';

/** Decay-per-generation slider range (fraction removed per iterate). */
export const DECAY_MAX = 0.3;
/** Randomisation strength slider range. */
export const VARIATION_MAX = 1;

export function formatBytes(b) {
  if (!(b > 0)) return '0 B';
  if (b < 1024) return `${b} B`;
  if (b < 1024 * 1024) return `${(b / 1024).toFixed(1)} KB`;
  return `${(b / (1024 * 1024)).toFixed(1)} MB`;
}

/** "×0.85/gen · next 12.8%" readout for the anneal controls. */
export function annealReadout(variation, decay) {
  const v = Math.max(0, Number(variation) || 0);
  const d = Math.max(0, Math.min(DECAY_MAX, Number(decay) || 0));
  const next = d > 0 && v > VARIATION_FLOOR ? Math.max(VARIATION_FLOOR, v * (1 - d)) : v;
  const factor = (1 - d).toFixed(2);
  return d > 0 ? `×${factor}/gen · NEXT ${(next * 100).toFixed(1)}%` : 'OFF · CONSTANT';
}

const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const sid = (id) => 'S' + String(id + 1).padStart(2, '0');
const fmt = (v, d = 1) => (Number.isFinite(v) ? v.toFixed(d) : '—');

/**
 * @param {object} p { mx, bus, overlay, drawer, getProvenance, applyShard, onExit, refresh, store }
 */
export function mountMultiplexControls(p) {
  const { mx, bus, overlay, drawer } = p;
  const refresh = p.refresh || (() => {});
  const stack = createGenerationStack();
  mx.undo = stack;
  const store = p.store || createSnapshotStore();
  let compareActive = null; // { names, fitnessKey }

  // ── PEEK overlay ──
  const peek = document.createElement('div');
  peek.id = 'mpx-peek';
  peek.className = 'mpx-peek';
  peek.setAttribute('aria-hidden', 'true');
  peek.innerHTML = '<canvas id="mpx-peek-canvas"></canvas><div class="mpx-peek-label" id="mpx-peek-label">PEEK</div>';
  overlay.appendChild(peek);
  const peekCanvas = peek.querySelector('canvas');
  let peekReady = false;
  function showPeek(id) {
    if (id === null || id === undefined) {
      peek.classList.remove('active');
      peek.setAttribute('aria-hidden', 'true');
      return;
    }
    peek.classList.add('active');
    peek.setAttribute('aria-hidden', 'false');
    const dpr = Math.min(1.5, (typeof window !== 'undefined' && window.devicePixelRatio) || 1);
    const w = Math.max(1, Math.round(peek.clientWidth * dpr));
    const h = Math.max(1, Math.round(peek.clientHeight * dpr));
    if (!peekReady || peekCanvas.width !== w || peekCanvas.height !== h) {
      peekCanvas.width = w; peekCanvas.height = h;
      peekReady = !!setPeekCanvas(mx, peekCanvas);
    }
    const sh = mx.shards[id];
    peek.querySelector('#mpx-peek-label').textContent = `PEEK ${sh && sh.label ? sh.label : sid(id)} · RELEASE TO CLOSE`;
  }

  // ── Drawer controls: UNDO / REDO, anneal, snapshots ──
  const strip = drawer.querySelector('.mpx-strip');
  const stripUndo = document.createElement('button');
  stripUndo.id = 'mpx-undo-strip';
  stripUndo.className = 'mpx-btn mpx-icon';
  stripUndo.type = 'button';
  stripUndo.title = 'Undo the last iterate';
  stripUndo.textContent = '↶';
  stripUndo.setAttribute('data-mpx-help', 'undo');
  strip.insertBefore(stripUndo, strip.querySelector('.mpx-chevron'));
  stripUndo.addEventListener('click', (e) => { e.stopPropagation(); undo(); });

  const actions = drawer.querySelector('.mpx-actions');
  const extra = document.createElement('div');
  extra.className = 'mpx-run-controls';
  extra.innerHTML = `
    <div class="mpx-actions mpx-undo-row">
      <button id="mpx-undo" class="mpx-btn mpx-action" type="button" title="Undo: restore the previous generation exactly" data-mpx-help="undo">↶ UNDO</button>
      <button id="mpx-redo" class="mpx-btn mpx-action" type="button" title="Redo the undone generation" data-mpx-help="undo">↷ REDO</button>
      <button id="mpx-snapshots-btn" class="mpx-btn mpx-action" type="button" title="Saved shard / generation snapshots" data-mpx-help="snapshots">▤ SNAPSHOTS</button>
    </div>
    <div class="mpx-stat" id="mpx-undo-stat">UNDO 0 · REDO 0</div>
    <div class="mpx-anneal" data-mpx-help="anneal">
      <label class="mpx-anneal-row" for="mpx-run-variation">
        <span>RANDOMISATION</span>
        <input id="mpx-run-variation" type="range" min="0" max="${VARIATION_MAX}" step="0.01">
        <span id="mpx-run-variation-value" class="mpx-anneal-val">—</span>
      </label>
      <label class="mpx-anneal-row" for="mpx-run-decay">
        <span>DECAY / GEN</span>
        <input id="mpx-run-decay" type="range" min="0" max="${DECAY_MAX}" step="0.01">
        <span id="mpx-run-decay-value" class="mpx-anneal-val">—</span>
      </label>
    </div>`;
  actions.parentNode.insertBefore(extra, actions.nextSibling);
  const undoBtn = extra.querySelector('#mpx-undo');
  const redoBtn = extra.querySelector('#mpx-redo');
  const varIn = extra.querySelector('#mpx-run-variation');
  const decIn = extra.querySelector('#mpx-run-decay');
  undoBtn.addEventListener('click', undo);
  redoBtn.addEventListener('click', redo);
  extra.querySelector('#mpx-snapshots-btn').addEventListener('click', () => togglePanel());
  varIn.addEventListener('input', () => {
    mx.config.variation = Math.max(0, Math.min(VARIATION_MAX, parseFloat(varIn.value) || 0));
    syncAnneal();
    if (bus) bus.emit('multiplex:annealChanged', { variation: mx.config.variation, cooling: mx.config.cooling });
  });
  decIn.addEventListener('input', () => {
    mx.config.cooling = Math.max(0, Math.min(DECAY_MAX, parseFloat(decIn.value) || 0));
    syncAnneal();
    if (bus) bus.emit('multiplex:annealChanged', { variation: mx.config.variation, cooling: mx.config.cooling });
  });

  function syncAnneal() {
    if (!mx.config) return;
    const v = Number(mx.config.variation) || 0;
    const d = Number(mx.config.cooling) || 0;
    if (document.activeElement !== varIn) varIn.value = String(v);
    if (document.activeElement !== decIn) decIn.value = String(d);
    extra.querySelector('#mpx-run-variation-value').textContent = `${(v * 100).toFixed(1)}%`;
    extra.querySelector('#mpx-run-decay-value').textContent = annealReadout(v, d);
  }

  function syncUndo() {
    const st = stack.stats();
    undoBtn.disabled = !st.undo;
    redoBtn.disabled = !st.redo;
    stripUndo.disabled = !st.undo;
    extra.querySelector('#mpx-undo-stat').textContent = `UNDO ${st.undo} · REDO ${st.redo} · ${formatBytes(st.bytes)} / ${formatBytes(st.budgetBytes)}`;
  }

  function undo() {
    if (!mx.active || !stack.canUndo) return false;
    const target = stack.undo(captureGeneration(mx));
    const ok = target && restoreGeneration(mx, target);
    compareActive = null;
    afterChange();
    if (bus) bus.emit('multiplex:undo', { generation: mx.iteration, ok: !!ok });
    return !!ok;
  }
  function redo() {
    if (!mx.active || !stack.canRedo) return false;
    const target = stack.redo(captureGeneration(mx));
    const ok = target && restoreGeneration(mx, target);
    compareActive = null;
    afterChange();
    if (bus) bus.emit('multiplex:redo', { generation: mx.iteration, ok: !!ok });
    return !!ok;
  }
  function afterChange() { syncUndo(); syncAnneal(); renderCompareStats(); refresh(); }

  // ── SNAPSHOTS panel ──
  const panel = document.createElement('div');
  panel.id = 'mpx-snapshots';
  panel.className = 'mpx-snapshots hidden';
  panel.innerHTML = `
    <div class="mpx-snap-head">
      <span class="mpx-title">SNAPSHOTS</span>
      <span id="mpx-snap-total" class="mpx-snap-total">—</span>
      <button id="mpx-snap-close" class="mpx-btn mpx-icon" type="button" title="Close">✕</button>
    </div>
    <div class="mpx-snap-save">
      <input id="mpx-snap-name" type="text" maxlength="80" placeholder="name (optional)" autocomplete="off">
      <button id="mpx-snap-save-shard" class="mpx-btn" type="button" title="Save the selected shard">💾 SAVE SHARD</button>
      <button id="mpx-snap-save-gen" class="mpx-btn" type="button" title="Save every shard of this generation">💾 SAVE GENERATION</button>
    </div>
    <div id="mpx-snap-list" class="mpx-snap-list"></div>
    <div class="mpx-snap-foot">
      <button id="mpx-snap-compare" class="mpx-btn" type="button" disabled title="Run the ticked snapshots side by side">⇆ COMPARE (0)</button>
      <button id="mpx-snap-compare-end" class="mpx-btn" type="button" disabled title="Leave COMPARE (same as UNDO)">✕ END COMPARE</button>
    </div>
    <div id="mpx-snap-stats" class="mpx-snap-stats"></div>
    <div id="mpx-snap-msg" class="mpx-snap-msg" role="status"></div>`;
  overlay.appendChild(panel);
  const listEl = panel.querySelector('#mpx-snap-list');
  const msg = (t) => { panel.querySelector('#mpx-snap-msg').textContent = t; };
  const picked = new Set();
  panel.querySelector('#mpx-snap-close').addEventListener('click', () => togglePanel(false));
  panel.querySelector('#mpx-snap-save-shard').addEventListener('click', () => save('shard'));
  panel.querySelector('#mpx-snap-save-gen').addEventListener('click', () => save('generation'));
  panel.querySelector('#mpx-snap-compare').addEventListener('click', () => compare([...picked]));
  panel.querySelector('#mpx-snap-compare-end').addEventListener('click', () => { if (compareActive) undo(); });

  function togglePanel(force) {
    const open = force === undefined ? panel.classList.contains('hidden') : !!force;
    panel.classList.toggle('hidden', !open);
    if (open) refreshList();
  }

  async function save(kind) {
    if (!mx.active || !mx.shards.length) return null;
    const prov = (p.getProvenance && p.getProvenance()) || {};
    const ids = kind === 'generation' ? mx.shards.map((s) => s.id) : [mx.selected];
    const report = getFitnessReport(mx);
    const fit = new Map(report.perShard.map((e) => [e.id, e.fitness]));
    const rec = buildSnapshotRecord({
      name: panel.querySelector('#mpx-snap-name').value,
      kind, generation: mx.iteration, shardIds: ids,
      shards: ids.map((id) => snapshotShardFull(mx.shards[id])),
      stats: ids.map((id) => ({ id, label: mx.shards[id].label || sid(id), ...shardQuickStats(mx.shards[id]), fitness: fit.get(id) ?? null })),
      gridCols: mx.config.cols, gridRows: mx.config.rows,
      seed: prov.seed, sourceSeed: mx.sourceSeed,
      liveEdited: prov.liveEdited, liveEditCount: prov.liveEditCount,
      config: { ...mx.config, fitnessWeights: { ...mx.config.fitnessWeights }, fitnessModes: { ...mx.config.fitnessModes } },
    });
    if (kind === 'generation') rec.selectedIndex = mx.selected;
    try {
      const meta = await store.save(rec);
      panel.querySelector('#mpx-snap-name').value = '';
      msg(`SAVED “${meta.name}” · ${formatBytes(meta.bytes)}${store.persistent ? '' : ' · MEMORY ONLY (no IndexedDB)'}`);
      await refreshList();
      if (bus) bus.emit('multiplex:snapshotSaved', { id: meta.id, kind });
      return meta;
    } catch (err) {
      msg(`SAVE FAILED: ${err && err.message ? err.message : err}`);
      return null;
    }
  }

  async function refreshList() {
    const { items, totalBytes } = await store.list();
    panel.querySelector('#mpx-snap-total').textContent = `${items.length} SAVED · ${formatBytes(totalBytes)}${store.persistent ? ' · INDEXEDDB' : ' · MEMORY'}`;
    for (const id of [...picked]) if (!items.some((m) => m.id === id)) picked.delete(id);
    listEl.innerHTML = items.length ? items.map((m) => {
      const when = new Date(m.createdAt);
      const t = `${when.toLocaleDateString()} ${when.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}`;
      const s0 = (m.stats && m.stats[0]) || {};
      const what = m.kind === 'generation' ? `GEN ${m.shardIds.length} SIMS` : `${sid(m.shardIds[0] || 0)}`;
      return `<div class="mpx-snap-row" data-id="${esc(m.id)}" data-kind="${m.kind}">
        <label class="mpx-snap-pick-wrap" title="Tick to COMPARE"><input class="mpx-snap-pick" type="checkbox" ${picked.has(m.id) ? 'checked' : ''}></label>
        <div class="mpx-snap-info">
          <div class="mpx-snap-name">${esc(m.name)}</div>
          <div class="mpx-snap-meta">${esc(t)} · ${what} · G${m.generation} · ${formatBytes(m.bytes)} · SEED ${m.seed === null || m.seed === undefined ? '—' : '0x' + (m.seed >>> 0).toString(16)}${m.liveEdited ? ' · <b class="mpx-snap-live">LIVE-EDITED</b>' : ''}</div>
          <div class="mpx-snap-meta">ALIVE ${s0.alive ?? '—'} · BOND ${fmt(s0.bondedPct)}% · SP ${s0.species ?? '—'}</div>
        </div>
        <div class="mpx-snap-acts">
          <button class="mpx-btn" data-act="sim" type="button" title="RESTART: load into a single sim (exits the multiplex)">▶ SIM</button>
          <button class="mpx-btn" data-act="seed" type="button" title="Seed a new generation from this snapshot">⚡ SEED</button>
          ${m.kind === 'generation' ? '<button class="mpx-btn" data-act="restore" type="button" title="Put this whole generation back on the grid">⟲ RESTORE</button>' : ''}
          <button class="mpx-btn mpx-danger" data-act="delete" type="button" title="Delete this one snapshot">🗑 DELETE</button>
        </div>
      </div>`;
    }).join('') : '<div class="mpx-snap-empty">No snapshots yet. SAVE SHARD or SAVE GENERATION.</div>';
    listEl.querySelectorAll('.mpx-snap-row').forEach((row) => {
      const id = row.dataset.id;
      row.querySelector('.mpx-snap-pick').addEventListener('change', (e) => {
        if (e.target.checked) picked.add(id); else picked.delete(id);
        syncCompareBtn();
      });
      row.querySelectorAll('button[data-act]').forEach((b) => b.addEventListener('click', () => act(b.dataset.act, id)));
    });
    syncCompareBtn();
    return items;
  }

  function syncCompareBtn() {
    const b = panel.querySelector('#mpx-snap-compare');
    b.textContent = `⇆ COMPARE (${picked.size})`;
    b.disabled = picked.size < 2;
    panel.querySelector('#mpx-snap-compare-end').disabled = !compareActive;
  }

  /** The representative shard of a record (generation → its selected shard). */
  const primary = (rec) => rec.shards[Math.max(0, Math.min(rec.shards.length - 1, rec.kind === 'generation' ? rec.selectedIndex | 0 : 0))];

  async function act(kind, id) {
    const rec = await store.load(id);
    if (!rec && kind !== 'delete') { msg('SNAPSHOT NOT FOUND'); return; }
    if (kind === 'delete') {
      const name = rec ? rec.name : id;
      const ok = typeof window === 'undefined' || typeof window.confirm !== 'function' || p.skipConfirm || window.confirm(`Delete snapshot “${name}”?`);
      if (!ok) return;
      await store.remove(id);
      picked.delete(id);
      msg(`DELETED “${name}”`);
      await refreshList();
      return;
    }
    if (kind === 'sim') {
      // RESTART into the single main sim.
      const src = sourceFromSnapshot(primary(rec));
      if (p.onExit) p.onExit({ importSelected: false });
      if (p.applyShard) p.applyShard(src);
      if (bus) bus.emit('multiplex:snapshotLoaded', { id, target: 'sim' });
      return;
    }
    if (kind === 'seed') {
      seedFromSnapshot(mx, primary(rec));
      compareActive = null;
      msg(`SEEDED G${mx.iteration} FROM “${rec.name}” (UNDO to go back)`);
      afterChange();
      return;
    }
    if (kind === 'restore') {
      loadSnapshotsUndoable(mx, rec.shards, { cols: rec.gridCols, generation: rec.generation });
      compareActive = null;
      msg(`RESTORED “${rec.name}” (UNDO to go back)`);
      afterChange();
    }
  }

  async function compare(ids) {
    if (!mx.active || ids.length < 2) return false;
    const recs = (await Promise.all(ids.map((id) => store.load(id)))).filter(Boolean);
    if (recs.length < 2) return false;
    const snaps = recs.map(primary);
    const names = recs.map((r) => r.name);
    loadSnapshotsUndoable(mx, snaps, { labels: names });
    compareActive = { names };
    msg(`COMPARING ${recs.length} SNAPSHOTS LIVE (UNDO / END COMPARE to go back)`);
    afterChange();
    syncCompareBtn();
    if (bus) bus.emit('multiplex:compare', { count: recs.length });
    return true;
  }

  function renderCompareStats() {
    const el = panel.querySelector('#mpx-snap-stats');
    if (!compareActive || !mx.active) { el.innerHTML = ''; syncCompareBtn(); return; }
    const report = getFitnessReport(mx);
    const fit = new Map(report.perShard.map((e) => [e.id, e.fitness]));
    el.innerHTML = `<table class="mpx-compare-table" id="mpx-snap-stats-table">
      <thead><tr><th>SNAPSHOT</th><th>ALIVE</th><th>BONDED %</th><th>SPECIES</th><th>ENERGY</th><th>FITNESS</th></tr></thead>
      <tbody>${mx.shards.map((sh, i) => {
        const s = shardQuickStats(sh);
        return `<tr data-shard="${i}"><td>${esc(compareActive.names[i] || sid(i))}</td><td>${s.alive}</td><td>${fmt(s.bondedPct)}</td><td>${s.species}</td><td>${fmt(s.energy, 2)}</td><td>${fmt(fit.get(sh.id), 3)}</td></tr>`;
      }).join('')}</tbody></table>`;
  }

  if (bus) {
    bus.on('multiplex:peek', (e) => showPeek(e && e.active ? e.id : null));
  }

  return {
    stack,
    store,
    undo,
    redo,
    save,
    compare,
    refreshList,
    togglePanel,
    /** Called by the controller on begin / exit. */
    reset() { stack.clear(); compareActive = null; picked.clear(); showPeek(null); afterChange(); },
    /** Metrics cadence (every 24 frames). */
    tick() { syncUndo(); syncAnneal(); renderCompareStats(); },
    sync: afterChange,
    digest: () => digestGeneration(mx),
    get comparing() { return !!compareActive; },
  };
}
