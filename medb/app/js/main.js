import { h, replace, dialog, clear } from "./dom.js";
import { state, go, errorBox, refreshDash } from "./common.js";
import { api, get, session, setToken } from "./api.js";
import * as V1 from "./views_knowledge.js";
import * as V2 from "./views_governance.js";
import * as V3 from "./views_audit.js";
import * as V4 from "./views_integrations.js";

export const NAV = [
  { sec: "Overview" },
  { id: "dashboard", label: "Dashboard", ico: "◎", key: "1", view: V1.dashboard },
  { sec: "Knowledge" },
  { id: "claims", cap: true, label: "Claim ledger", ico: "≡", key: "2", view: V1.claims },
  { id: "claim", hidden: true, cap: true, label: "Claim", view: V1.claimDetail },
  { id: "corpus", cap: true, label: "Corpus", ico: "▤", key: "3", view: V1.corpus },
  { id: "permissions", cap: true, label: "Permissions", ico: "⚿", key: "4", view: V1.permissions },
  { id: "context", cap: true, label: "Context packages", ico: "▣", key: "5", view: V1.contextBuilder },
  { sec: "Governance" },
  { id: "escalations", label: "Escalations", ico: "⚑", key: "6", view: V2.escalations, badge: "escalations_open" },
  { id: "directives", cap: true, label: "Directives", ico: "§", key: "7", view: V2.directives },
  { id: "delegation", label: "Delegation", ico: "⇄", key: "8", view: V2.delegation },
  { id: "suspensions", label: "Suspensions", ico: "⛔", key: "9", view: V2.suspensions, badge: "suspensions" },
  { id: "gov", label: "Governance log", ico: "⛓", key: "0", view: V2.govLog },
  { id: "audit", label: "Audit log & anchors", ico: "⌖", view: V2.auditAnchors },
  { id: "auditor", label: "Auditor desk", ico: "⚖", view: V3.auditorDesk },
  { id: "integrations", label: "Integrations", ico: "⇆", view: V4.integrations },
  { id: "system", label: "System", ico: "⚙", view: V2.system },
];


// ---------------------------------------------------------------- theme
function applyTheme(t) {
  document.documentElement.dataset.theme = t;
  localStorage.setItem("medb.app.theme", t);
}
function toggleTheme() {
  const cur = document.documentElement.dataset.theme;
  const dark = cur === "dark" || (cur === "auto" && matchMedia("(prefers-color-scheme: dark)").matches);
  applyTheme(dark ? "light" : "dark");
}

// ---------------------------------------------------------------- routing
function parseRoute() {
  const raw = location.hash.replace(/^#\/?/, "");
  const [path, qs] = raw.split("?");
  const parts = path.split("/").filter(Boolean).map(decodeURIComponent);
  return { id: parts[0] || "dashboard", args: parts.slice(1), query: new URLSearchParams(qs || "") };
}

const isAuditor = () => (session.actor || "").startsWith("auditor:");
function buildNav() {
  const nav = document.getElementById("nav");
  clear(nav);
  for (const n of NAV) {
    if (n.sec) { if (!(n.sec === "Knowledge" && isAuditor())) nav.appendChild(h("div", { class: "sec" }, n.sec)); continue; }
    if (n.hidden || (n.cap && isAuditor())) continue;  // auditor tokens: audit plane only (D-69)
    nav.appendChild(h("a", { href: "#/" + n.id, dataset: { id: n.id }, "aria-keyshortcuts": n.key || null },
      h("span", { class: "ico", "aria-hidden": "true" }, n.ico), n.label,
      n.badge ? h("span", { class: "badge bad nav-badge", dataset: { badge: n.badge }, hidden: true }) : null,
      n.key && !n.badge ? h("span", { class: "k" }, n.key) : null));
  }
}
function markNav(id) {
  for (const a of document.querySelectorAll("#nav a")) a.classList.toggle("on", a.dataset.id === id || (id === "claim" && a.dataset.id === "claims"));
}
async function render() {
  const r = parseRoute();
  let n = NAV.find((x) => x.id === r.id) || NAV[1];
  if (n.cap && isAuditor()) n = NAV.find((x) => x.id === "auditor");
  const main = document.getElementById("main");
  document.getElementById("title").textContent = n.label;
  document.title = n.label + " · MedB";
  markNav(n.id);
  document.getElementById("sidebar").classList.remove("open");
  replace(main, h("div", { class: "empty" }, "Loading…"));
  state.current = n.id;
  state.refresh = null;
  try {
    const out = await n.view(main, r);
    if (state.current === n.id) state.refresh = out?.refresh || null;
  } catch (e) {
    replace(main, errorBox(e));
  }
}

// ---------------------------------------------------------------- live updates (polling; the API server is single-threaded)
async function poll() {
  if (!session.token) return;
  const live = document.getElementById("live");
  try {
    const c = await get("/api/app/changes");
    live.className = "live on"; live.textContent = "● live";
    live.title = "Live: last checked " + new Date().toLocaleTimeString();
    if (state.changeToken && c.token !== state.changeToken) {
      await refreshDash();
      if (state.refresh && !document.getElementById("dialog").open && !state.busy) {
        try { await state.refresh(); } catch { /* view shows its own errors */ }
      }
    }
    state.changeToken = c.token;
  } catch {
    live.className = "live off"; live.textContent = "● offline";
  }
}
// ---------------------------------------------------------------- auth
function loginScreen(msg) {
  document.getElementById("shell").hidden = true;
  const input = h("input", { type: "password", placeholder: "bearer token", autocomplete: "off", "aria-label": "token" });
  const box = h("div", { class: "card login" },
    h("h2", null, "Sign in to MedB"),
    h("p", { class: "muted" }, "Paste a token from data/api_tokens.json (user, reader, agent:coder or an auditor:… id), or open the link printed by python3 -m medb.api."),
    msg ? h("div", { class: "notice bad" }, msg) : null,
    h("div", { class: "row" }, input, h("button", { class: "btn primary", onclick: () => { setToken(input.value.trim()); location.hash = "#/dashboard"; location.reload(); } }, "Sign in")));
  document.body.appendChild(box);
  input.focus();
}

function shortcuts() {
  const rows = [["1–9, 0", "jump to section"], ["/", "focus search / filter"], ["t", "toggle dark / light"], ["r", "refresh view"], ["Esc", "close dialog"], ["?", "this help"]];
  dialog({ title: "Keyboard shortcuts", okText: "Close", cancelText: "Back",
    body: h("table", null, rows.map(([k, v]) => h("tr", null, h("td", null, h("kbd", null, k)), h("td", null, v)))) });
}

function keyboard(ev) {
  if (ev.target.closest("input,textarea,select,[contenteditable]") || ev.metaKey || ev.ctrlKey || ev.altKey) {
    if (ev.key === "Escape" && ev.target.blur) ev.target.blur();
    return;
  }
  if (document.getElementById("dialog").open) return;
  const n = NAV.find((x) => x.key === ev.key && !(x.cap && isAuditor()));
  if (n) { ev.preventDefault(); go(n.id); return; }
  if (ev.key === "/") { const f = document.querySelector("main [data-search]"); if (f) { ev.preventDefault(); f.focus(); } }
  else if (ev.key === "t") toggleTheme();
  else if (ev.key === "r") render();
  else if (ev.key === "?") shortcuts();
}

async function boot() {
  // token and options may arrive in the fragment: #token=...&theme=dark&go=/claim/<id>
  const frag = new URLSearchParams(location.hash.replace(/^#/, "").includes("token=") ? location.hash.slice(1) : "");
  if (frag.get("token")) setToken(frag.get("token"));
  if (frag.get("theme")) applyTheme(frag.get("theme"));
  else applyTheme(localStorage.getItem("medb.app.theme") || "auto");
  if (frag.get("token")) history.replaceState(null, "", "#" + (frag.get("go") || "/dashboard"));
  else if (!location.hash) history.replaceState(null, "", "#/dashboard");  // drop the token from the URL
  if (!session.token) return loginScreen();
  let who;
  try { who = await get("/api/app/whoami"); } catch (e) { setToken(null); return loginScreen(e.status === 401 ? "That token was not accepted." : e.message); }
  session.actor = who.actor; session.can = new Set(who.can);
  const chip = document.getElementById("actor");
  chip.textContent = "You are: " + who.actor + (who.read_only ? " (read-only)" : "");
  chip.className = "actor-chip " + (who.actor === "user" ? "user" : who.actor.startsWith("agent:") ? "agent" : who.actor.startsWith("auditor:") ? "auditor" : "reader");
  if (who.appointment && !who.appointment.active) chip.textContent += " · not appointed";
  document.getElementById("theme").addEventListener("click", toggleTheme);
  document.getElementById("logout").addEventListener("click", () => { setToken(null); location.hash = ""; location.reload(); });
  document.getElementById("menu").addEventListener("click", () => document.getElementById("sidebar").classList.toggle("open"));
  document.addEventListener("keydown", keyboard);
  buildNav();
  window.addEventListener("hashchange", render);
  await refreshDash();
  await render();
  setInterval(poll, 3000);
  poll();
}
boot();
