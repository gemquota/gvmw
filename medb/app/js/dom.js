// DOM helpers. All untrusted text is inserted with textContent / text nodes only.
// No HTML-string injection anywhere in this app: text goes in via textContent only.
export function h(tag, props, ...children) {
  const el = document.createElement(tag);
  if (props) {
    for (const [k, v] of Object.entries(props)) {
      if (v === undefined || v === null || v === false) continue;
      if (k === "class") el.className = v;
      else if (k === "text") el.textContent = String(v);
      else if (k.startsWith("on") && typeof v === "function") el.addEventListener(k.slice(2).toLowerCase(), v);
      else if (k === "dataset") Object.assign(el.dataset, v);
      else if (k === "value") el.value = v;
      else if (k === "checked") el.checked = !!v;
      else if (k === "disabled") el.disabled = !!v;
      else if (k === "style" && typeof v === "object") Object.assign(el.style, v);
      else if (k === "href") { const s = String(v); if (s.startsWith("#") || s.startsWith("/") || s.startsWith("https://")) el.setAttribute("href", s); }
      else el.setAttribute(k, v === true ? "" : String(v));
    }
  }
  append(el, children);
  return el;
}
export function append(el, children) {
  for (const c of children.flat(Infinity)) {
    if (c === null || c === undefined || c === false) continue;
    el.appendChild(c instanceof Node ? c : document.createTextNode(String(c)));
  }
  return el;
}
export function clear(el) { while (el.firstChild) el.removeChild(el.firstChild); return el; }
export function replace(el, ...children) { clear(el); return append(el, children); }

const SVGNS = "http://www.w3.org/2000/svg";
export function s(tag, attrs, ...children) {
  const el = document.createElementNS(SVGNS, tag);
  for (const [k, v] of Object.entries(attrs || {})) {
    if (v === undefined || v === null) continue;
    if (k.startsWith("on") && typeof v === "function") el.addEventListener(k.slice(2).toLowerCase(), v);
    else if (k === "text") el.textContent = String(v);
    else el.setAttribute(k, String(v));
  }
  for (const c of children.flat(Infinity)) if (c) el.appendChild(c instanceof Node ? c : document.createTextNode(String(c)));
  return el;
}

// ---- formatting
export function fmtTs(ts) {
  if (!ts) return "—";
  const d = new Date(ts);
  if (isNaN(d)) return String(ts);
  return d.toLocaleString(undefined, { year: "numeric", month: "short", day: "2-digit", hour: "2-digit", minute: "2-digit", second: "2-digit" });
}
export function tsEl(ts) { return h("span", { title: ts ? ts + " (UTC)" : "" }, fmtTs(ts)); }
export function short(id, n = 10) { const t = String(id ?? ""); return t.length > n + 6 ? t.slice(0, n + 6) + "…" : t; }
export function objText(o) { return typeof o === "string" ? o : JSON.stringify(o); }
export function json(o) { return h("pre", { class: "json" }, JSON.stringify(o, null, 2)); }
export function badge(text, kind = "") { return h("span", { class: "badge " + kind }, text); }

export const STATUS_KIND = { active: "ok", deleted: "bad", rejected: "warn", disavowed: "warn", superseded: "", withdrawn: "warn",
  SUSPENDED: "bad", NONCOMPLIANT: "bad", RESOLVED_PASS: "ok", OPEN: "info", APPROVED: "ok", REJECTED: "warn",
  UNDERDETERMINED: "bad", AUTHORIZED: "ok", REQUIRES_ESCALATION: "warn", PROHIBITED: "bad" };
export function statusBadge(st) { return badge(st, STATUS_KIND[st] ?? ""); }
export function confBadge(c) {
  const m = { user_asserted: ["you stated", "info"], user_confirmed: ["you confirmed", "ok"], unconfirmed: ["MedB inference · unconfirmed", "warn"], user_rejected: ["you rejected", "bad"] };
  const [t, k] = m[c] ?? [c, ""];
  return badge(t, k);
}
export function mediationBadge(v) {
  if (v === true) return badge("MedB-mediated", "accent");
  if (v === "possibly") return badge("mediation possible", "accent");
  return null;
}

// ---- toasts
export function toast(title, detail = "", kind = "") {
  const t = h("div", { class: "toast " + kind, role: kind === "bad" ? "alert" : "status" }, h("b", null, title), detail ? h("div", { class: "muted" }, detail) : null);
  document.getElementById("toasts").appendChild(t);
  setTimeout(() => t.remove(), kind === "bad" ? 9000 : 4500);
}

// ---- dialog (confirm / custom). Resolves with the value from onOk, or null on cancel.
export function dialog({ title, body, okText = "OK", okKind = "primary", cancelText = "Cancel", onOk, wide }) {
  const dlg = document.getElementById("dialog");
  return new Promise((resolve) => {
    let done = false;
    const finish = (v) => { if (done) return; done = true; dlg.close(); resolve(v); };
    const ok = h("button", { class: "btn " + okKind, type: "button" }, okText);
    const cancel = h("button", { class: "btn", type: "button" }, cancelText);
    ok.addEventListener("click", async () => {
      try { const v = onOk ? await onOk() : true; if (v !== undefined && v !== false) finish(v); }
      catch (e) { toast("Error", e.message || String(e), "bad"); }
    });
    cancel.addEventListener("click", () => finish(null));
    replace(dlg, h("div", { class: "d-head" }, title), h("div", { class: "d-body" }, body), h("div", { class: "d-foot" }, cancel, ok));
    dlg.style.width = wide ? "min(860px,95vw)" : "";
    dlg.onclose = () => finish(null);
    dlg.showModal();
    (dlg.querySelector("input,select,textarea") || ok).focus();
  });
}
export function confirmDanger(title, message, okText = "Confirm") {
  return dialog({ title, body: h("p", null, message), okText, okKind: "danger solid" });
}
export function field(label, input, cls = "") { return h("label", { class: "f " + cls }, label, input); }
export function card(title, ...children) { return h("section", { class: "card" }, title ? h("h2", null, title) : null, ...children); }
export function emptyRow(cols, text = "Nothing here yet.") { return h("tr", null, h("td", { colspan: cols, class: "empty" }, text)); }
