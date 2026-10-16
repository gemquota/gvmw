// Dashboard, claim ledger, claim detail, corpus, permissions, context packages.
import { h, replace, append, clear, tsEl, short, objText, json, badge, statusBadge, confBadge, mediationBadge,
  dialog, confirmDanger, field, card, emptyRow, toast } from "./dom.js";
import { get, post, can, session } from "./api.js";
import { go, errorBox, act } from "./common.js";
import { dag } from "./graph.js";

const csv = (v) => String(v || "").split(",").map((x) => x.trim()).filter(Boolean);
const isoOf = (v) => (v ? new Date(v).toISOString() : null);
const needs = (what) => (what === "__none" ? "Not applicable in the current state" : can(what) ? null : `Not available to ${session.actor}`);
export function btn(label, what, onclick, cls = "") {
  const reason = what ? needs(what) : null;
  return h("button", { class: "btn " + cls, type: "button", disabled: !!reason, title: reason || label, onclick }, label);
}
export const stmt = (c) => (c.content_destroyed || c.subject === null ? "(content destroyed)" : `${c.subject} ${c.predicate} ${objText(c.object)}`);

// ================================================================ dashboard
export async function dashboard(main) {
  const wrap = h("div", { class: "stack" });
  replace(main, wrap);
  async function load() {
    let d, recent;
    try { [d, recent] = await Promise.all([get("/api/app/dashboard"), get("/api/view/gov", { limit: 10 })]); }
    catch (e) { replace(wrap, errorBox(e)); return; }
    const pct = Math.min(100, Math.round((100 * d.budget.used) / d.budget.limit));
    const ec = d.emergencies;
    const broken = Object.entries(d.chains).filter(([, r]) => !r.ok);
    replace(wrap,
      h("div", { class: "grid cards" },
        statCard("Claims", d.claims.total, "in the ledger",
          h("div", { class: "row" }, Object.entries(d.claims.by_status).map(([k, v]) => badge(`${k} ${v}`, k === "active" ? "ok" : k === "deleted" ? "bad" : ""))),
          d.claims.pending_proposals ? h("a", { href: "#/claims?filter=pending" }, `${d.claims.pending_proposals} inference proposal(s) await your review →`) : null),
        statCard("Chain integrity", d.chains_ok ? "Intact" : "BROKEN", `${Object.keys(d.chains).length} hash-chained streams`,
          broken.length ? h("div", { class: "notice bad" }, broken.map(([s, r]) => `${s} broken at seq ${r.first_bad_seq}`).join("; ")) : badge("all chains verify", "ok"),
          h("div", { class: "row", style: { marginTop: "8px" } },
            btn("Run integrity check", "integrity_check", () => act(() => post("/api/integrity_check", {}), "Integrity check recorded", "Integrity check")),
            h("a", { href: "#/gov" }, "explore →")), d.chains_ok ? "ok" : "bad"),
        statCard("Active suspensions", d.suspensions.length, "cannot be lifted by any actor",
          d.suspensions.slice(0, 4).map((s) => h("div", { class: "mono" }, s.capability, " ", badge(s.classification, "bad"))),
          h("a", { href: "#/suspensions" }, "registry & propagation graph →"), d.suspensions.length ? "bad" : "ok"),
        statCard("Open escalations", d.escalations_open, "awaiting your decision", h("a", { href: "#/escalations" }, "inbox →"), d.escalations_open ? "warn" : "ok"),
        statCard("Budget (P-1.5)", d.budget.used, `of ${d.budget.limit} lines / ${d.budget.window_days} days`,
          h("div", { class: "bar " + (pct >= 90 ? "bad" : pct >= 70 ? "warn" : "") }, h("span", { style: { width: pct + "%" } })),
          h("div", { class: "muted" }, `${d.budget.limit - d.budget.used} lines remain · baseline `, tsEl(d.budget.baseline))),
        statCard("Emergencies (P-1.6)", ec.count, `of ${ec.limit} in ${ec.window_days} days`,
          h("div", { class: "bar " + (ec.count >= ec.limit ? "bad" : "") }, h("span", { style: { width: Math.min(100, (100 * ec.count) / ec.limit) + "%" } })),
          h("div", { class: "muted" }, `obligations: ${d.obligations.OPEN} open · ${d.obligations.BREACHED} breached`)),
        statCard("Governance log", d.gov_length, "entries", h("div", { class: "muted" }, `audit reads during suspension: ${d.auditlog_reads}`),
          h("div", { class: "muted" }, `external anchoring: ${d.anchoring_enabled ? "enabled" : "off"} · ${d.anchors} anchor(s)`))),
      card("Recent governance activity",
        h("div", { class: "table-wrap" }, h("table", null,
          h("thead", null, h("tr", null, h("th", null, "seq"), h("th", null, "time"), h("th", null, "kind"), h("th", null, "actor"))),
          h("tbody", null, recent.entries.slice().reverse().map((e) =>
            h("tr", { class: "click", onclick: () => go("gov?seq=" + e.seq) }, h("td", { class: "mono" }, e.seq), h("td", null, tsEl(e.ts)), h("td", null, badge(e.kind)), h("td", null, e.actor))))))));
  }
  await load();
  return { refresh: load };
}
function statCard(title, value, sub, ...rest) {
  const tone = typeof rest[rest.length - 1] === "string" ? rest.pop() : "";
  return h("section", { class: "card" }, h("h3", { class: "muted" }, title),
    h("div", { class: "stat " + (tone === "bad" ? "chain-bad" : "") }, String(value), h("small", null, sub)), h("div", { class: "stack", style: { gap: "6px", marginTop: "8px" } }, rest));
}

// ================================================================ claims ledger
export async function claims(main, route) {
  const f = { q: "", status: "", origin: "", scope: "", pending: route.query.get("filter") === "pending" };
  let data = null, stamps = [], asOf = null;
  const search = h("input", { type: "search", placeholder: "Search claims…  (/)", "data-search": "1", "aria-label": "search claims", oninput: (e) => { f.q = e.target.value.toLowerCase(); draw(); } });
  const sel = (key, opts, label) => h("select", { "aria-label": label, onchange: (e) => { f[key] = e.target.value; draw(); } }, h("option", { value: "" }, label), opts.map((o) => h("option", { value: o }, o)));
  const statusSel = sel("status", ["active", "rejected", "superseded", "disavowed", "deleted"], "any status");
  const originSel = sel("origin", ["user_stated", "inference"], "any origin");
  const scopeSel = h("select", { "aria-label": "scope", onchange: (e) => { f.scope = e.target.value; draw(); } });
  const pendingCb = h("input", { type: "checkbox", checked: f.pending, onchange: (e) => { f.pending = e.target.checked; draw(); } });
  const slider = h("input", { type: "range", min: 0, max: 0, value: 0, "aria-label": "time travel (as of)" });
  const sliderLabel = h("span", { class: "mono" }, "now");
  slider.addEventListener("input", () => { sliderLabel.textContent = slider.value == slider.max ? "now" : new Date(stamps[slider.value]).toLocaleString(); });
  slider.addEventListener("change", () => { asOf = slider.value == slider.max ? null : stamps[slider.value]; load(); });
  const tbody = h("tbody");
  const count = h("span", { class: "muted" });
  const pendingBox = h("div");
  const asOfNote = h("div");

  const assertForm = assertCard();
  replace(main, h("div", { class: "stack" },
    h("section", { class: "card" },
      h("div", { class: "toolbar" }, search, statusSel, originSel, scopeSel, h("label", { class: "inline" }, pendingCb, "pending proposals only"), h("span", { class: "spacer" }), count),
      h("div", { class: "slider" }, h("div", null, h("label", { class: "f" }, "Time travel — the ledger as MedB recorded it at", slider)), sliderLabel),
      asOfNote,
      h("div", { class: "table-wrap", style: { marginTop: "10px" } }, h("table", null,
        h("thead", null, h("tr", null, ["Claim", "Status", "Origin / confirmation", "Scope", "Sensitivity", "v", "Last change"].map((t) => h("th", null, t)))), tbody))),
    pendingBox, assertForm));

  async function load() {
    try { data = await get("/api/view/claims", { as_of: asOf }); }
    catch (e) { replace(tbody, h("tr", null, h("td", { colspan: 7 }, errorBox(e)))); return; }
    if (!asOf) {
      stamps = [...new Set(data.claims.flatMap((c) => c.transitions.map((t) => t.ts)))].sort();
      stamps.push(data.now);
      slider.max = stamps.length - 1; slider.value = slider.max; sliderLabel.textContent = "now";
      const scopes = [...new Set(data.claims.map((c) => c.scope))].sort();
      replace(scopeSel, h("option", { value: "" }, "any scope"), scopes.map((s) => h("option", { value: s, selected: s === f.scope }, s)));
    }
    replace(asOfNote, asOf ? h("div", { class: "notice info" }, "Viewing the ledger as of ", tsEl(asOf), " — read-only historical view. Drag to the right end to return to now.") : null);
    draw();
    drawPending();
  }
  function draw() {
    const rows = data.claims.filter((c) => (!f.status || c.status === f.status) && (!f.origin || c.origin === f.origin) && (!f.scope || c.scope === f.scope)
      && (!f.pending || (c.status === "active" && c.confirmation === "unconfirmed"))
      && (!f.q || [stmt(c), c.claim_id, c.scope, c.source || ""].join(" ").toLowerCase().includes(f.q)));
    count.textContent = `${rows.length} of ${data.count} claims`;
    replace(tbody, rows.length ? rows.slice().reverse().map((c) => h("tr", { class: "click", tabindex: 0, onclick: () => go("claim/" + encodeURIComponent(c.claim_id)), onkeydown: (e) => { if (e.key === "Enter") go("claim/" + encodeURIComponent(c.claim_id)); } },
      h("td", null, h("div", { style: { fontWeight: 600 } }, stmt(c)), h("div", { class: "mono muted" }, c.claim_id), mediationBadge(c.medb_mediated)),
      h("td", null, statusBadge(c.status)),
      h("td", null, h("div", null, c.origin), confBadge(c.confirmation)),
      h("td", null, c.scope), h("td", null, c.sensitivity), h("td", null, c.version), h("td", null, tsEl(c.last_transition_at)))) : emptyRow(7, "No claims match."));
  }
  function drawPending() {
    const p = data.claims.filter((c) => c.status === "active" && c.confirmation === "unconfirmed");
    replace(pendingBox, asOf || !p.length ? null : card(`Inference proposals awaiting you (${p.length})`,
      h("p", { class: "muted" }, "Inference may propose; only you can confirm or reject (Principle: inference proposes, never promotes)."),
      p.map((c) => h("div", { class: "row", style: { justifyContent: "space-between", padding: "6px 0", borderBottom: "1px solid var(--border)" } },
        h("div", null, h("a", { href: "#/claim/" + encodeURIComponent(c.claim_id) }, stmt(c)), " ", h("span", { class: "muted" }, "derived from ", c.derived_from.map((d) => short(d)).join(", "))),
        h("div", { class: "row" },
          btn("Confirm", "confirm", () => act(() => post("/api/claims/confirm", { claim_id: c.claim_id }), "Confirmed", "Confirm"), "primary small"),
          btn("Reject", "reject", () => rejectDialog(c), "small"))))));
  }
  await load();
  return { refresh: () => (asOf ? Promise.resolve() : load()) };
}

function assertCard() {
  const i = { subject: h("input", { value: "user" }), predicate: h("input", { placeholder: "e.g. prefers" }), object: h("input", { placeholder: "e.g. written summaries" }),
    scope: h("input", { placeholder: "e.g. health" }), sensitivity: h("select", null, ["low", "moderate", "high", "special"].map((s) => h("option", { selected: s === "high" }, s))),
    source: h("input", { value: "user:self-account" }), vf: h("input", { type: "datetime-local" }), vt: h("input", { type: "datetime-local" }) };
  const go_ = () => act(async () => {
    const r = await post("/api/ingest/claim", { subject: i.subject.value, predicate: i.predicate.value, object: i.object.value, scope: i.scope.value,
      sensitivity: i.sensitivity.value, source: i.source.value, temporal_validity: { valid_from: isoOf(i.vf.value), valid_to: isoOf(i.vt.value) } });
    i.predicate.value = i.object.value = "";
    return r;
  }, "Claim asserted", "Assert");
  return card("State something about yourself (ASSERT)",
    h("p", { class: "muted" }, "A self-account. If MedB has produced any output before, it is recorded as possibly MedB-mediated (F-19)."),
    h("div", { class: "form" }, field("Subject", i.subject), field("Predicate", i.predicate), field("Object", i.object), field("Scope", i.scope),
      field("Sensitivity", i.sensitivity), field("Source", i.source), field("Valid from (optional)", i.vf), field("Valid to (optional)", i.vt),
      h("div", null, btn("Assert claim", "assert", go_, "primary"))));
}

async function rejectDialog(c) {
  const reason = h("input", { placeholder: "why (optional)" });
  const ok = await dialog({ title: "Reject inference proposal", body: h("div", { class: "stack" }, h("p", null, stmt(c)), field("Reason", reason)), okText: "Reject", okKind: "danger" });
  if (ok) await act(() => post("/api/claims/reject", { claim_id: c.claim_id, reason: reason.value }), "Rejected", "Reject");
}

// ================================================================ claim detail
export async function claimDetail(main, route) {
  const cid = route.args[0];
  let asOf = null, d = null;
  const root = h("div", { class: "stack" });
  replace(main, root);
  async function load() {
    try { d = await get("/api/view/claim", { claim_id: cid, as_of: asOf }); } catch (e) { replace(root, errorBox(e)); return; }
    draw();
  }
  function draw() {
    const c = d.current, then = d.as_of_state;
    const stamps = c.transitions.map((t) => t.ts).concat([d.now]);
    const idx = asOf ? Math.max(0, stamps.findIndex((t) => t === asOf)) : stamps.length - 1;
    const slider = h("input", { type: "range", min: 0, max: stamps.length - 1, value: idx, "aria-label": "time travel over this claim's history" });
    const lbl = h("span", { class: "mono" }, idx === stamps.length - 1 ? "now" : new Date(stamps[idx]).toLocaleString());
    slider.addEventListener("input", () => { lbl.textContent = slider.value == slider.max ? "now" : new Date(stamps[slider.value]).toLocaleString(); });
    slider.addEventListener("change", () => { asOf = slider.value == slider.max ? null : stamps[slider.value]; load(); });
    const dead = c.status === "deleted";
    const isProposal = c.origin === "inference" && c.confirmation === "unconfirmed" && c.status === "active";
    replace(root,
      h("div", null, h("a", { href: "#/claims" }, "← Claim ledger")),
      h("section", { class: "card" },
        h("div", { class: "row", style: { justifyContent: "space-between", alignItems: "flex-start" } },
          h("div", null, h("div", { class: "statement" }, stmt(c)),
            h("div", { class: "row", style: { marginTop: "6px" } }, statusBadge(c.status), confBadge(c.confirmation), badge(c.origin), badge("v" + c.version), badge(c.scope), badge(c.sensitivity), mediationBadge(c.medb_mediated)),
            h("div", { class: "mono muted", style: { marginTop: "6px" } }, c.claim_id)),
          h("div", { class: "row" },
            isProposal ? btn("Confirm", "confirm", () => act(() => post("/api/claims/confirm", { claim_id: cid }), "Confirmed", "Confirm"), "primary") : null,
            isProposal ? btn("Reject", "reject", () => rejectDialog(c)) : null,
            btn("Correct", dead ? "__none" : "correct", () => correctDialog(c)),
            btn("Supersede", dead ? "__none" : "supersede", () => supersedeDialog(c)),
            btn("Disavow", dead || c.status === "disavowed" ? "__none" : "disavow", () => disavowDialog(c)),
            btn("Delete…", dead ? "__none" : "delete", () => deleteDialog(c), "danger"))),
        h("dl", { class: "kv", style: { marginTop: "12px" } },
          h("dt", null, "Created"), h("dd", null, tsEl(c.created_at)), h("dt", null, "Source"), h("dd", null, c.source ?? "—"),
          h("dt", null, "Valid time"), h("dd", null, c.temporal_validity ? `${c.temporal_validity.valid_from || "−∞"} → ${c.temporal_validity.valid_to || "+∞"}` : "—"),
          h("dt", null, "Derived from"), h("dd", null, c.derived_from.length ? c.derived_from.map((x) => h("a", { href: "#/claim/" + encodeURIComponent(x), style: { marginRight: "8px" } }, short(x))) : "—"),
          h("dt", null, "Derived inferences"), h("dd", null, d.derived.length ? d.derived.map((x) => h("a", { href: "#/claim/" + encodeURIComponent(x), style: { marginRight: "8px" } }, short(x))) : "none"),
          c.mediation_basis ? [h("dt", null, "Mediation basis"), h("dd", { class: "mono" }, JSON.stringify(c.mediation_basis))] : null,
          c.superseded_by ? [h("dt", null, "Superseded by"), h("dd", null, h("a", { href: "#/claim/" + encodeURIComponent(c.superseded_by) }, c.superseded_by))] : null)),
      h("div", { class: "grid two" },
        h("section", { class: "card" }, h("h2", null, "Time travel"),
          h("div", { class: "slider" }, slider, lbl),
          then ? h("div", { class: "rendered", style: { marginTop: "10px" } },
            h("div", { class: "muted" }, asOf ? "As MedB recorded it at this time:" : "Current state:"),
            h("div", { style: { fontWeight: 600 } }, stmt(then)),
            h("div", { class: "row", style: { marginTop: "4px" } }, statusBadge(then.status), confBadge(then.confirmation), badge("v" + then.version)))
            : h("div", { class: "notice info", style: { marginTop: "10px" } }, "The claim did not exist yet at this time."),
          h("h3", { style: { marginTop: "14px" } }, "Transitions"),
          h("ol", { class: "timeline" }, c.transitions.map((t) => h("li", { class: "k-" + t.kind + (asOf && t.ts > asOf ? " future" : "") },
            h("b", null, t.kind), " · ", tsEl(t.ts), " · ", t.actor, h("div", { class: "mono muted", title: t.event_hash }, "event ", short(t.event_hash, 14)))))),
        h("section", { class: "card" }, h("h2", null, "Version history"),
          h("div", { class: "table-wrap" }, h("table", null,
            h("thead", null, h("tr", null, ["v", "when", "by", "content"].map((x) => h("th", null, x)))),
            h("tbody", null, d.versions.slice().reverse().map((v) => h("tr", null, h("td", null, v.version), h("td", null, tsEl(v.ts), h("div", { class: "muted" }, v.kind)), h("td", null, v.actor),
              h("td", null, v.content_destroyed ? badge("content destroyed", "bad") : h("div", null, `${v.subject} ${v.predicate} ${objText(v.object)}`),
                v.corrected_fields.length ? h("div", { class: "muted" }, "corrected: " + v.corrected_fields.join(", ")) : null)))))))),
      h("section", { class: "card" }, h("h2", null, "Derivation graph"),
        h("div", { class: "sub" }, "Inputs (left) to inferences (right). A deleted claim or withdrawn corpus item makes everything downstream unusable."),
        dag({ nodes: d.graph.nodes.map((n) => ({ ...n, sub: n.type === "corpus" ? "corpus · " + n.id : n.id, label: n.type === "claim" ? `${n.label} · ${n.origin === "inference" ? "inference" : "stated"}` : n.label })),
          edges: d.graph.edges, focus: cid, onClick: (n) => n.type === "claim" && n.id !== cid && go("claim/" + encodeURIComponent(n.id)) }),
        h("div", { class: "legend" }, h("span", null, h("i", { class: "ok" }), "usable"), h("span", null, h("i", { class: "bad" }), "deleted / missing"),
          h("span", null, h("i", { class: "warn" }), "rejected / disavowed / withdrawn"), h("span", null, h("i", { class: "ok dash" }), "corpus item"))));
  }

  async function correctDialog(c) {
    const fields = { subject: h("input", { value: c.subject ?? "" }), predicate: h("input", { value: c.predicate ?? "" }), object: h("input", { value: objText(c.object ?? "") }), source: h("input", { value: c.source ?? "" }) };
    const ok = await dialog({ title: "Correct claim (new version)", okText: "Save correction",
      body: h("div", { class: "form" }, Object.entries(fields).map(([k, el]) => field(k, el)), h("p", { class: "muted wide" }, "Corrections are new transitions; earlier versions stay in the history.")),
      onOk: () => {
        const ch = {};
        for (const [k, el] of Object.entries(fields)) if (el.value !== String(k === "object" ? objText(c.object ?? "") : c[k] ?? "")) ch[k] = el.value;
        if (!Object.keys(ch).length) throw new Error("Nothing changed");
        return ch;
      } });
    if (ok) await act(() => post("/api/claims/correct", { claim_id: cid, changes: ok }), "Correction recorded", "Correct");
  }
  async function supersedeDialog(c) {
    let all;
    try { all = await get("/api/view/claims"); } catch (e) { toast("Cannot list claims", e.message, "bad"); return; }
    const sel = h("select", null, all.claims.filter((x) => x.claim_id !== cid && x.status === "active").map((x) => h("option", { value: x.claim_id }, `${stmt(x)} (${short(x.claim_id)})`)));
    const ok = await dialog({ title: "Supersede by another claim", body: field("Superseding claim", sel), okText: "Supersede", onOk: () => sel.value || false });
    if (ok) await act(() => post("/api/claims/supersede", { claim_id: cid, by_claim_id: ok }), "Superseded", "Supersede");
  }
  async function disavowDialog(c) {
    const reason = h("input", { placeholder: "reason (optional)" });
    const ok = await dialog({ title: "Disavow this claim?", okText: "Disavow", okKind: "danger solid",
      body: h("div", { class: "stack" }, h("p", null, "“", stmt(c), "” will no longer be used. The record and its history are kept."), field("Reason", reason)) });
    if (ok) await act(() => post("/api/claims/disavow", { claim_id: cid, reason: reason.value }), "Disavowed", "Disavow");
  }
  async function deleteDialog(c) {
    let pv;
    try { pv = await get("/api/claims/delete_preview", { claim_id: cid }); } catch (e) { toast("Preview failed", e.message, "bad"); return; }
    const mode = { v: "none" };
    const boxes = pv.derived.map((x) => h("input", { type: "checkbox", value: x.claim_id, disabled: true, "aria-label": "destroy " + x.claim_id }));
    const radio = (v, label) => h("label", { class: "inline" }, h("input", { type: "radio", name: "dd", value: v, checked: v === "none", onchange: () => { mode.v = v; boxes.forEach((b) => (b.disabled = v !== "list")); } }), label);
    const body = h("div", { class: "stack" },
      h("div", { class: "notice bad" }, "Deleting destroys every content version of “", stmt(c), "”. The fact of deletion stays in the ledger. This cannot be undone."),
      pv.derived.length ? h("div", null,
        h("b", null, `${pv.derived.length} inference(s) are derived from this claim:`),
        h("div", { class: "row", style: { margin: "8px 0" } }, radio("none", "Keep them (unusable, content kept) — default"), radio("all", "Destroy all"), radio("list", "Choose…")),
        h("table", null, h("tbody", null, pv.derived.map((x, i) => h("tr", null, h("td", null, boxes[i]),
          h("td", null, h("div", null, x.content_destroyed ? "(content destroyed)" : `${x.predicate} ${objText(x.object)}`), h("div", { class: "mono muted" }, x.claim_id)),
          h("td", null, statusBadge(x.status), " ", confBadge(x.confirmation)))))))
        : h("p", { class: "muted" }, "No inferences are derived from this claim."));
    const ok = await dialog({ title: "Delete claim", body, okText: "Delete permanently", okKind: "danger solid", wide: true,
      onOk: () => (mode.v === "list" ? boxes.filter((b) => b.checked).map((b) => b.value) : mode.v) });
    if (ok !== null && ok !== undefined) await act(() => post("/api/claims/delete", { claim_id: cid, destroy_derived: ok }), "Claim deleted", "Delete");
  }
  await load();
  return { refresh: () => (asOf ? Promise.resolve() : load()) };
}

// ================================================================ corpus
export async function corpus(main, route) {
  const i = { content: h("textarea", { placeholder: "source material (stored immutably)" }), source: h("input", { placeholder: "e.g. clinic-letters" }), scope: h("input", { placeholder: "e.g. health" }),
    sensitivity: h("select", null, ["low", "moderate", "high", "special"].map((s) => h("option", { selected: s === "high" }, s))), media: h("input", { value: "text/plain" }) };
  const tbody = h("tbody");
  const viewer = h("div");
  replace(main, h("div", { class: "stack" }, viewer,
    card("Ingest", h("p", { class: "muted" }, "Requires an ingest grant covering the source and scope (default deny)."),
      h("div", { class: "form" }, field("Content", i.content, "wide"), field("Source", i.source), field("Scope", i.scope), field("Sensitivity", i.sensitivity), field("Media type", i.media),
        h("div", null, btn("Ingest", "ingest", () => act(async () => { const r = await post("/api/ingest/corpus", { content: i.content.value, source: i.source.value, scope: i.scope.value, sensitivity: i.sensitivity.value, media_type: i.media.value }); i.content.value = ""; return r; }, "Ingested", "Ingest"), "primary")))),
    card("Corpus items", h("p", { class: "muted" }, "There is no erasure. Withdrawing makes an item unusable for closure, inference and packages; its content is kept (F-05)."),
      h("div", { class: "table-wrap" }, h("table", null, h("thead", null, h("tr", null, ["Item", "Source", "Scope", "Sensitivity", "Ingested", "Status", ""].map((t) => h("th", null, t)))), tbody)))));
  async function view(it, purpose) {
    if (!purpose) {
      if (it.use_purposes.length === 1) purpose = it.use_purposes[0];
      else {
        const sel = h("select", null, it.use_purposes.map((p) => h("option", null, p)));
        const ok = await dialog({ title: `View ${it.corpus_id}`, okText: "View", body: h("div", { class: "stack" },
          h("p", { class: "muted" }, "Content is released only for a purpose an active use grant covers. The read is logged (identifiers only)."), field("Purpose", sel)) });
        if (!ok) return;
        purpose = sel.value;
      }
    }
    let r;
    try { r = await get("/api/view/corpus_content", { corpus_id: it.corpus_id, purpose }); } catch (e) { replace(viewer, card("Content viewer", errorBox(e))); return; }
    replace(viewer, card(`Content · ${r.corpus_id}`,
      h("dl", { class: "kv" }, h("dt", null, "Source"), h("dd", null, r.source), h("dt", null, "Scope / sensitivity"), h("dd", null, `${r.scope} · ${r.sensitivity}`),
        h("dt", null, "Media type"), h("dd", null, r.media_type), h("dt", null, "Ingested"), h("dd", null, tsEl(r.ingested_at)),
        h("dt", null, "Released for"), h("dd", null, badge(r.purpose, "accent"), " under ", h("span", { class: "mono" }, r.grant_id)),
        h("dt", null, "Logged"), h("dd", { class: "muted" }, "CLAIMS_RETRIEVED (corpus id, purpose, grant) in the governance log; visible in Q-1 claims_retrieved")),
      h("pre", { class: "content-view" }, typeof r.content === "string" ? r.content : JSON.stringify(r.content, null, 2)),
      h("div", null, h("button", { class: "btn small", type: "button", onclick: () => replace(viewer) }, "Close"))));
  }
  async function load() {
    let d;
    try { d = await get("/api/view/corpus"); } catch (e) { replace(tbody, h("tr", null, h("td", { colspan: 7 }, errorBox(e)))); return; }
    replace(tbody, d.items.length ? d.items.map((it) => h("tr", null, h("td", { class: "mono" }, it.corpus_id, h("div", { class: "muted" }, it.media_type)), h("td", null, it.source), h("td", null, it.scope), h("td", null, it.sensitivity),
      h("td", null, tsEl(it.ingested_at)), h("td", null, it.withdrawn ? [badge("withdrawn", "warn"), " ", tsEl(it.withdrawn_at)] : badge("usable", "ok")),
      h("td", null, h("div", { class: "row" }, h("button", { class: "btn small", type: "button", disabled: it.withdrawn || !it.use_purposes.length || !can("read_corpus"),
        title: it.withdrawn ? "Withdrawn: unusable, content retained (F-05)" : !it.use_purposes.length ? "No active use grant covers this item" : !can("read_corpus") ? `Not available to ${session.actor}` : "View content (purpose-bound, logged)",
        onclick: () => view(it) }, "View…"),
      it.withdrawn ? null : btn("Withdraw…", "withdraw", async () => {
        const reason = h("input", { placeholder: "reason (optional)" });
        const ok = await dialog({ title: "Withdraw corpus item?", okText: "Withdraw", okKind: "danger solid", body: h("div", { class: "stack" },
          h("div", { class: "notice warn" }, "Withdrawal is permanent for this item: it can no longer be used, and everything derived from it becomes unusable. Content is kept, not erased."), field("Reason", reason)) });
        if (ok) await act(() => post("/api/corpus/withdraw", { corpus_id: it.corpus_id, reason: reason.value }), "Withdrawn", "Withdraw");
      }, "danger small"))))) : emptyRow(7, "No corpus items."));
    return d;
  }
  const d0 = await load();
  const want = route?.query?.get("view");
  const item = want && d0?.items.find((x) => x.corpus_id === want || (want === "first" && !x.withdrawn && x.use_purposes.length));
  if (item) await view(item, route.query.get("purpose") || undefined);
  return { refresh: load };
}

// ================================================================ permissions
export async function permissions(main) {
  const i = { op: h("select", null, ["use", "infer", "model", "ingest"].map((o) => h("option", null, o))), scopes: h("input", { placeholder: "health, authority  (or *)" }),
    purposes: h("input", { placeholder: "clinic-visit (use only)" }), sources: h("input", { placeholder: "clinic-letters (ingest only)" }),
    sens: h("select", null, ["low", "moderate", "high", "special"].map((s) => h("option", { selected: s === "moderate" }, s))), compose: h("input", { type: "checkbox" }),
    expires: h("input", { type: "datetime-local" }), note: h("input", { placeholder: "note" }) };
  const tbody = h("tbody");
  const showRevoked = h("input", { type: "checkbox", onchange: () => load() });
  replace(main, h("div", { class: "stack" },
    card("Grant a permission", h("p", { class: "muted" }, "Default deny. Closure is computed over the full derivation path; combining inputs from several scopes needs a single grant with compose (Composition Rule)."),
      h("div", { class: "form" }, field("Operation", i.op), field("Scopes", i.scopes), field("Purposes", i.purposes), field("Sources", i.sources), field("Max sensitivity", i.sens),
        field("Expires (optional)", i.expires), field("Note", i.note), h("label", { class: "inline" }, i.compose, "compose (allow combining scopes)"),
        h("div", null, btn("Grant", "grant", () => act(() => post("/api/permissions/grant", { operation: i.op.value, scopes: csv(i.scopes.value), purposes: csv(i.purposes.value), sources: csv(i.sources.value),
          sensitivity_max: i.sens.value, compose: i.compose.checked, expires_at: isoOf(i.expires.value), note: i.note.value }), "Granted", "Grant"), "primary")))),
    card("Grants", h("div", { class: "toolbar" }, h("label", { class: "inline" }, showRevoked, "show revoked / expired")),
      h("div", { class: "table-wrap" }, h("table", null, h("thead", null, h("tr", null, ["Grant", "Operation", "Scopes", "Purposes / sources", "Max sens.", "Compose", "Granted", "State", ""].map((t) => h("th", null, t)))), tbody)))));
  async function load() {
    let d;
    try { d = await get("/api/view/permissions"); } catch (e) { replace(tbody, h("tr", null, h("td", { colspan: 9 }, errorBox(e)))); return; }
    const gs = d.grants.filter((g) => showRevoked.checked || g.active).reverse();
    replace(tbody, gs.length ? gs.map((g) => h("tr", null, h("td", { class: "mono" }, g.grant_id, g.note ? h("div", { class: "muted" }, g.note) : null), h("td", null, badge(g.operation, "accent")),
      h("td", null, g.scopes.join(", ")), h("td", null, [...(g.purposes || []), ...(g.sources || [])].join(", ") || "—"), h("td", null, g.sensitivity_max), h("td", null, g.compose ? badge("compose", "info") : "—"),
      h("td", null, tsEl(g.granted_at)), h("td", null, g.active ? badge("active", "ok") : g.revoked_at ? badge("revoked", "bad") : badge("expired", "warn")),
      h("td", null, g.active ? btn("Revoke…", "revoke", async () => {
        if (await confirmDanger("Revoke permission?", `Revoke ${g.operation} on ${g.scopes.join(", ")} (${g.grant_id})? Anything that relied on it stops being permitted immediately.`, "Revoke"))
          await act(() => post("/api/permissions/revoke", { grant_id: g.grant_id }), "Revoked", "Revoke");
      }, "danger small") : null))) : emptyRow(9, "No grants."));
  }
  await load();
  return { refresh: load };
}

// ================================================================ context packages
export async function contextBuilder(main, route) {
  const i = { purpose: h("input", { value: "clinic-visit" }), predicates: h("input", { value: "decides, has, carries" }), scopes: h("input", { placeholder: "(any permitted)" }),
    subject: h("input", { placeholder: "(any)" }), ttl: h("input", { type: "number", value: 60, min: 1, max: 1440 }) };
  const out = h("div", { class: "stack" });
  replace(main, h("div", { class: "stack" },
    card("Build a context package", h("p", { class: "muted" }, "Ephemeral and purpose-scoped. The package is logged (identifiers, ranking record, rendering keys) but not retained by MedB."),
      h("div", { class: "form" }, field("Purpose", i.purpose), field("Predicates", i.predicates), field("Scopes", i.scopes), field("Subject", i.subject), field("TTL (minutes)", i.ttl),
        h("div", null, btn("Build package", "build_package", build, "primary")))), out));
  async function build() {
    const r = await act(() => post("/api/context/build", { purpose: i.purpose.value, predicates: csv(i.predicates.value), scopes: csv(i.scopes.value), subject: i.subject.value || null, ttl_minutes: Number(i.ttl.value) || null }), null, "Build package");
    if (r) showPackage(out, r);
  }
  if (route?.query?.get("autobuild") === "1") await build();
  return {};
}
function showPackage(out, r) {
  const p = r.package, rank = p.rationale.ranking, rec = r.issuance_record?.body || {};
  const exp = h("span", { class: "badge info" });
  let started = false;
  const tick = () => { if (started && !exp.isConnected) return clearInterval(t); started = true; const s = Math.max(0, Math.round((new Date(p.expires_at) - Date.now()) / 1000)); exp.textContent = s ? `expires in ${Math.floor(s / 60)}m ${s % 60}s` : "expired"; };
  const t = setInterval(tick, 1000); tick();
  const byId = Object.fromEntries(p.claims.map((c) => [c.claim_id, c]));
  replace(out,
    h("section", { class: "card" }, h("h2", null, "Package ", h("span", { class: "mono" }, p.package_id), exp),
      h("dl", { class: "kv" }, h("dt", null, "Purpose"), h("dd", null, p.purpose), h("dt", null, "Requester"), h("dd", null, p.requester), h("dt", null, "Issued"), h("dd", null, tsEl(p.issued_at)),
        h("dt", null, "Grant"), h("dd", { class: "mono" }, p.boundary.grant_id || "none"), h("dt", null, "Modal findings"), h("dd", null, (rec.modal_findings || []).length ? badge(`${rec.modal_findings.length} finding(s)`, "bad") : badge("symmetric", "ok")))),
    h("div", { class: "grid two" },
      h("section", { class: "card" }, h("h2", null, `Claims (${p.claims.length})`),
        p.claims.length ? p.claims.map((c) => h("div", { class: "rendered" + (c.origin === "inference" ? " inf" : "") },
          h("div", null, c.rendered), h("div", { class: "row", style: { marginTop: "4px" } }, confBadge(c.confirmation), mediationBadge(c.medb_mediated), h("a", { class: "mono", href: "#/claim/" + encodeURIComponent(c.claim_id) }, short(c.claim_id)))))
          : h("p", { class: "muted" }, "No permitted claims."),
        p.frames.length ? [h("h3", null, "Frames"), p.frames.map((f) => h("div", { class: "rendered" }, f.rendered))] : null),
      h("div", { class: "stack" },
        card(`Contradictions (${p.contradictions.length})`, p.contradictions.length ? p.contradictions.map((x) => h("div", { class: "notice warn", style: { marginBottom: "6px" } },
          "Preserved, not resolved: ", x.claim_ids.map((id) => byId[id]?.statement || short(id)).join("  ⟷  "), h("div", { class: "muted" }, "basis: " + x.basis))) : h("p", { class: "muted" }, "None.")),
        card(`Unknowns (${p.unknowns.length})`, p.unknowns.length ? h("ul", null, p.unknowns.map((u) => h("li", null, u.predicate ? `predicate “${u.predicate}”: ${u.status}` : `${short(u.claim_id)}: ${u.status}`))) : h("p", { class: "muted" }, "None.")),
        card("Boundary", h("dl", { class: "kv" }, h("dt", null, "Scopes"), h("dd", null, p.boundary.scopes.join(", ") || "any permitted"),
          h("dt", null, "Excluded"), h("dd", null, Object.keys(p.boundary.excluded_counts).length ? Object.entries(p.boundary.excluded_counts).map(([k, v]) => h("div", null, `${v} × ${k}`)) : "nothing"),
          h("dt", null, "Withheld contradictions"), h("dd", null, String(p.boundary.contradictions_involving_withheld_claims)),
          h("dt", null, "Retention"), h("dd", null, p.boundary.retention), h("dt", null, "Authority"), h("dd", null, p.boundary.authority))))),
    card("Ranking record (logged in full)", h("div", { class: "sub" }, `ranker ${rank.ranker} · objective ${rank.objective} · weights ${JSON.stringify(rank.weights)}`),
      h("div", { class: "table-wrap" }, h("table", null, h("thead", null, h("tr", null, h("th", null, "#"), h("th", null, "claim"), h("th", null, "score"), Object.keys(rank.weights).map((w) => h("th", null, w)))),
        h("tbody", null, rank.order.map((id, n) => h("tr", null, h("td", null, n + 1), h("td", null, byId[id]?.statement || short(id)), h("td", { class: "mono" }, String(rank.scores[id])),
          Object.keys(rank.weights).map((w) => h("td", { class: "mono" }, String(rank.inputs[id]?.[w] ?? "—"))))))))));
}
