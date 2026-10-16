// The only way the app talks to MedB: the local HTTP API with a bearer token.
const KEY = "medb.app.token";
export const session = { token: sessionStorage.getItem(KEY), actor: null, can: new Set() };

export function setToken(t) { session.token = t; if (t) sessionStorage.setItem(KEY, t); else sessionStorage.removeItem(KEY); }

export class ApiError extends Error {
  constructor(status, body) {
    const hint = { 401: "Not signed in", 403: "Not authorised", 404: "Not found", 409: "Conflict", 423: "Capability suspended", 400: "Bad request" }[status] || `HTTP ${status}`;
    super(body?.detail || body?.error || hint);
    this.status = status; this.body = body || {}; this.hint = hint;
  }
}

export async function api(path, { method = "GET", body, raw = false } = {}) {
  const headers = { Authorization: "Bearer " + (session.token || "") };
  if (body !== undefined) headers["Content-Type"] = "application/json";
  const r = await fetch(path, { method, headers, body: body !== undefined ? JSON.stringify(body) : undefined, cache: "no-store" });
  if (raw && r.ok) return r;
  let data = null;
  try { data = await r.json(); } catch { data = null; }
  if (!r.ok) throw new ApiError(r.status, data);
  return data;
}
export const get = (p, q) => api(q ? p + "?" + new URLSearchParams(Object.entries(q).filter(([, v]) => v !== undefined && v !== null && v !== "")) : p);
export const post = (p, body) => api(p, { method: "POST", body });
export const can = (what) => session.can.has(what);
