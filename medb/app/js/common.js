// Shared app state and helpers (kept separate from main.js to avoid import cycles).
import { h, toast } from "./dom.js";
import { get } from "./api.js";

export const state = { current: null, refresh: null, changeToken: null, dash: null, busy: false };

export function go(path) { location.hash = "#/" + path.replace(/^\/+/, ""); }

export function errorBox(e) {
  if (e?.status === 423) {
    return h("div", { class: "notice bad", role: "alert" },
      h("b", null, "Capability suspended (423). "),
      `The primitive ${e.body.primitive || ""} is suspended (record ${e.body.suspension_record || "?"}). `,
      "Suspensions cannot be lifted by any actor; only re-audit resolves them. ",
      h("a", { href: "#/suspensions" }, "Open suspension registry"));
  }
  if (e?.status === 403) return h("div", { class: "notice warn", role: "alert" }, h("b", null, "Not authorised (403). "), e.message);
  return h("div", { class: "notice bad", role: "alert" }, h("b", null, (e?.hint || "Error") + ": "), e?.message || String(e));
}
export function reportError(e, what = "Action failed") {
  const extra = e?.status === 423 ? ` — primitive ${e.body.primitive}, record ${e.body.suspension_record}` : "";
  toast(`${what}: ${e?.hint || "error"}`, (e?.message || String(e)) + extra, "bad");
}
export function updateBadges(d) {
  for (const b of document.querySelectorAll("[data-badge]")) {
    const v = b.dataset.badge === "suspensions" ? (d.suspensions || []).length : d[b.dataset.badge];
    b.textContent = v ? String(v) : "";
    b.hidden = !v;
  }
}
export async function refreshDash() {
  try { state.dash = await get("/api/app/dashboard"); updateBadges(state.dash); } catch { /* ignore */ }
  return state.dash;
}
export async function afterWrite() {
  state.changeToken = null;
  await refreshDash();
  if (state.refresh) { try { await state.refresh(); } catch { /* view shows its own errors */ } }
  try { state.changeToken = (await get("/api/app/changes")).token; } catch { /* */ }
}
// Run a write action with error reporting and a refresh afterwards.
export async function act(fn, okMsg, what) {
  state.busy = true;
  try { const r = await fn(); if (okMsg) toast(okMsg, "", "ok"); await afterWrite(); return r; }
  catch (e) { reportError(e, what); return undefined; }
  finally { state.busy = false; }
}
