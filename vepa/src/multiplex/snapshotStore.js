// D-044 saved Chaos Multiplex snapshots (IndexedDB).
//
// A snapshot is one shard, or a whole generation, under a name and a
// timestamp. Each record keeps full shard snapshots (multiplex.js
// snapshotShardFull: particles, DNA, laws, PRNG, counters, speciation), the
// quick stats at save time, and provenance: the main-world seed, the
// multiplex source seed, and the D-043 live-edited flag. Only single-record
// delete is offered (no bulk wipe).

const DB_NAME = 'vepa4-mpx-snapshots';
const DB_VERSION = 1;
const META = 'meta';
const DATA = 'data';

export function snapshotRecordBytes(record) {
  let b = 1024;
  for (const sn of record.shards || []) {
    b += 512;
    if (sn.view) b += sn.view.byteLength;
    if (sn.dna) b += sn.dna.byteLength || sn.dna.length * 2;
    if (sn.sourceDna) b += sn.sourceDna.byteLength || sn.sourceDna.length * 2;
  }
  return b;
}

function metaOf(r) {
  return {
    id: r.id, name: r.name, createdAt: r.createdAt, kind: r.kind, generation: r.generation,
    shardIds: r.shardIds, gridCols: r.gridCols, gridRows: r.gridRows, seed: r.seed, sourceSeed: r.sourceSeed,
    liveEdited: !!r.liveEdited, stats: r.stats, bytes: r.bytes,
  };
}

/** In-memory adapter (tests and browsers without IndexedDB). */
export function createMemorySnapshotAdapter() {
  const meta = new Map();
  const data = new Map();
  return {
    kind: 'memory',
    async put(record) { meta.set(record.id, metaOf(record)); data.set(record.id, record); },
    async list() { return [...meta.values()]; },
    async get(id) { return data.get(id) || null; },
    async remove(id) { meta.delete(id); data.delete(id); },
  };
}

function idbOpen() {
  return new Promise((resolve, reject) => {
    if (typeof indexedDB === 'undefined') { reject(new Error('IndexedDB unavailable')); return; }
    const req = indexedDB.open(DB_NAME, DB_VERSION);
    req.onupgradeneeded = () => {
      const db = req.result;
      if (!db.objectStoreNames.contains(META)) db.createObjectStore(META, { keyPath: 'id' });
      if (!db.objectStoreNames.contains(DATA)) db.createObjectStore(DATA, { keyPath: 'id' });
    };
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error || new Error('IndexedDB open failed'));
  });
}
const done = (req) => new Promise((res, rej) => { req.onsuccess = () => res(req.result); req.onerror = () => rej(req.error); });

export function createIndexedDbSnapshotAdapter() {
  let dbp = null;
  const db = () => (dbp = dbp || idbOpen());
  const tx = async (stores, mode) => (await db()).transaction(stores, mode);
  return {
    kind: 'indexeddb',
    async put(record) {
      const t = await tx([META, DATA], 'readwrite');
      t.objectStore(META).put(metaOf(record));
      t.objectStore(DATA).put(record);
      await new Promise((res, rej) => { t.oncomplete = res; t.onerror = () => rej(t.error); t.onabort = () => rej(t.error); });
    },
    async list() { return done((await tx([META], 'readonly')).objectStore(META).getAll()); },
    async get(id) { return (await done((await tx([DATA], 'readonly')).objectStore(DATA).get(id))) || null; },
    async remove(id) {
      const t = await tx([META, DATA], 'readwrite');
      t.objectStore(META).delete(id);
      t.objectStore(DATA).delete(id);
      await new Promise((res, rej) => { t.oncomplete = res; t.onerror = () => rej(t.error); });
    },
  };
}

/** Pick IndexedDB when present, else memory (snapshots then last the session). */
export function createSnapshotStore(adapter = null) {
  let a = adapter;
  if (!a) {
    try { a = typeof indexedDB !== 'undefined' ? createIndexedDbSnapshotAdapter() : createMemorySnapshotAdapter(); }
    catch { a = createMemorySnapshotAdapter(); }
  }
  let n = 0;
  return {
    get persistent() { return a.kind === 'indexeddb'; },
    /** Save a record built by buildSnapshotRecord; returns its metadata. */
    async save(record) {
      const rec = { ...record };
      rec.id = rec.id || `snap-${rec.createdAt || Date.now()}-${(++n).toString(36)}-${Math.random().toString(36).slice(2, 6)}`;
      rec.bytes = snapshotRecordBytes(rec);
      await a.put(rec);
      return metaOf(rec);
    },
    /** Metadata, newest first, plus the total size. */
    async list() {
      const items = (await a.list()).sort((x, y) => (y.createdAt || 0) - (x.createdAt || 0));
      return { items, totalBytes: items.reduce((s, m) => s + (m.bytes || 0), 0) };
    },
    load: (id) => a.get(id),
    /** Delete ONE snapshot. There is intentionally no delete-all. */
    remove: (id) => a.remove(String(id)),
  };
}

/**
 * Build a snapshot record.
 * @param {object} p { name, kind: 'shard'|'generation', generation, shards: full snaps,
 *   shardIds, stats, gridCols, gridRows, seed, sourceSeed, liveEdited, liveEditCount, config, now }
 */
export function buildSnapshotRecord(p) {
  const createdAt = p.now || Date.now();
  const d = new Date(createdAt);
  const hh = String(d.getHours()).padStart(2, '0');
  const mm = String(d.getMinutes()).padStart(2, '0');
  const fallback = `${p.kind === 'generation' ? 'GEN' : 'S' + String((p.shardIds?.[0] ?? 0) + 1).padStart(2, '0')} G${p.generation ?? 0} ${hh}:${mm}`;
  return {
    name: String(p.name || '').trim().slice(0, 80) || fallback,
    createdAt,
    kind: p.kind === 'generation' ? 'generation' : 'shard',
    generation: p.generation ?? 0,
    shardIds: p.shardIds || [],
    gridCols: p.gridCols || 1,
    gridRows: p.gridRows || 1,
    seed: Number.isFinite(p.seed) ? p.seed >>> 0 : null,
    sourceSeed: Number.isFinite(p.sourceSeed) ? p.sourceSeed | 0 : null,
    liveEdited: !!p.liveEdited,
    liveEditCount: p.liveEditCount | 0,
    config: p.config ? { ...p.config } : null,
    stats: p.stats || [],
    shards: p.shards || [],
  };
}
