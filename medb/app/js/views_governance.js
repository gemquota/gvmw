// Escalations, directives, delegation, suspensions, governance log, audit log & anchors, system.
import { h, replace, tsEl, short, json, badge, statusBadge, dialog, confirmDanger, field, card, emptyRow, toast } from "./dom.js";
import { get, post, can, session, api } from "./api.js";
import { go, errorBox, act } from "./common.js";
import { dag } from "./graph.js";
import { btn } from "./views_knowledge.js";

function actionSummary(a) {
  return h("div", null,
    h("div", null, h("b", null, a.kind), " by ", a.agent, a.matter ? [" · matter ", badge(a.matter, "accent")] : null, a.emergency ? [" ", badge("emergency: " + a.emergency.condition, "warn")] : null),
    a.description ? h("div", { class: "muted" }, a.description) : null,
    (a.changes || []).length ? h("div", { class: "mono muted" }, a.changes.map((c) => `${c.path} (${c.lines} lines)`).join(" · ")) : null);
}
const basisText = (b) => (!b ? "—" : b.source === "env_condition" ? "recorded condition: " + b.conditions.map((c) => `${c.condition}${c.matter ? "@" + c.matter : ""} (by ${c.actor})`).join(", ") : b.source === "user" ? "set by you" : "default (deferrable)");

// ================================================================ escalations
export async function escalations(main) {
  const list = h("div", { class: "stack" });
  const showAll = h("input", { type: "checkbox", onchange: () => load() });
  replace(main, h("div", { class: "stack" },
    h("div", { class: "notice info" }, "Only you resolve escalations. Conflicting positions of equal standing are never tie-broken: if the decision can be deferred, nothing happens; if it cannot (you said so, or a deadline/outage is recorded), the matter is suspended as constitutional underdetermination (III.1). Agents cannot mark a decision non-deferrable (F-02)."),
    h("div", { class: "toolbar" }, h("label", { class: "inline" }, showAll, "show resolved")), list));
  async function load() {
    let d;
    try { d = await get("/api/view/escalations"); } catch (e) { replace(list, errorBox(e)); return; }
    const es = d.escalations.filter((e) => showAll.checked || e.status === "OPEN");
    replace(list, es.length ? es.map(escCard) : h("div", { class: "card empty" }, "Inbox zero — no open escalations."));
  }
  function escCard(e) {
    const open = e.status === "OPEN";
    const positions = [];
    const posBox = h("div");
    const addPos = (p = "approve") => {
      const row = { position: h("select", null, ["approve", "reject"].map((x) => h("option", { selected: x === p }, x))), priority: h("input", { type: "number", placeholder: "priority" }), statement: h("input", { placeholder: "what you said (optional)" }) };
      const el = h("div", { class: "pos-row" }, row.position, row.priority, row.statement, h("button", { class: "btn small", type: "button", "aria-label": "remove position", onclick: () => { positions.splice(positions.indexOf(row), 1); el.remove(); } }, "✕"));
      row.el = el; positions.push(row); posBox.appendChild(el);
    };
    const defer = h("select", { "aria-label": "deferrability" }, h("option", { value: "" }, "derive from recorded conditions"), h("option", { value: "false" }, "I say: cannot be deferred"), h("option", { value: "true" }, "I say: can be deferred"));
    const now = e.deferrability_now;
    async function resolve(body, label) {
      const distinct = new Set((body.positions || []).map((p) => p.position));
      const prios = (body.positions || []).map((p) => p.priority);
      const equal = distinct.size > 1 && !(prios.every((x) => x !== undefined && x !== null) && new Set(prios).size === prios.length);
      const nondef = body.deferrable === false || (body.deferrable === undefined && !now.deferrable);
      if (equal && nondef && !(await confirmDanger("Conflicting positions on a non-deferrable decision",
        `Your positions conflict with equal standing and the decision cannot be deferred. MedB will not choose for you: matter “${e.matter}” will be suspended as CONSTITUTIONAL_UNDERDETERMINATION (III.1). That suspension cannot be lifted by anyone, including you.`, "Record and suspend"))) return;
      await act(() => post("/api/escalations/resolve", { escalation_id: e.escalation_id, ...body }), label, "Resolve");
    }
    function collect() {
      const ps = positions.map((r) => ({ position: r.position.value, priority: r.priority.value === "" ? undefined : Number(r.priority.value), statement: r.statement.value || undefined }));
      const body = { positions: ps };
      if (defer.value) body.deferrable = defer.value === "true";
      return body;
    }
    return h("section", { class: "card" },
      h("div", { class: "row", style: { justifyContent: "space-between" } }, h("h2", null, "Escalation ", h("span", { class: "mono" }, short(e.escalation_id, 14))), h("div", { class: "row" }, statusBadge(e.status), badge(e.clause, "accent"), badge(e.review_type))),
      actionSummary(e.action),
      h("dl", { class: "kv", style: { marginTop: "10px" } }, h("dt", null, "Opened"), h("dd", null, tsEl(e.opened_at)),
        h("dt", null, "Facts"), h("dd", { class: "mono" }, JSON.stringify(e.facts)),
        h("dt", null, "Deferrable at opening"), h("dd", null, String(e.deferrable), " — ", basisText(e.deferrability_basis)),
        h("dt", null, "Deferrable now"), h("dd", null, now.deferrable ? badge("deferrable", "ok") : badge("non-deferrable", "bad"), " ", basisText(now.basis))),
      open ? h("div", { class: "stack", style: { marginTop: "12px" } },
        h("div", { class: "row" },
          btn("Approve", "resolve_escalation", () => resolve({ approve: true }, "Approved"), "primary"),
          btn("Reject", "resolve_escalation", () => resolve({ approve: false }, "Rejected"), "danger"),
          btn(`Record deadline for “${e.matter}”`, "set_condition", async () => {
            if (await confirmDanger("Record a deadline?", `This records that the decision on “${e.matter}” cannot wait. Conflicting equal positions on it will then cause a III.1 suspension instead of deferral.`, "Record deadline"))
              await act(() => post("/api/env/condition", { condition: "deadline", value: true, matter: e.matter, source: "user via app" }), "Deadline recorded", "Record deadline");
          })),
        h("details", null, h("summary", null, "Answer with positions (several, with priorities)"),
          h("p", { class: "muted" }, "Distinct priorities are your own ordering: the highest governs. Equal or missing priorities on different positions are a conflict."),
          posBox,
          h("div", { class: "row" }, h("button", { class: "btn small", type: "button", onclick: () => addPos() }, "+ position"), field("Deferrability", defer),
            btn("Submit positions", "resolve_escalation", () => { const b = collect(); if (!b.positions.length) return toast("Add at least one position", "", "warn"); resolve(b, "Recorded"); }, "primary"))))
        : null);
  }
  await load();
  return { refresh: load };
}

// ================================================================ directives
export async function directives(main) {
  const tbody = h("tbody");
  replace(main, h("div", { class: "stack" },
    h("div", { class: "notice info" }, "Directives are your stated positions when resolving escalations. They live in the separate normative stream, not the epistemic claims ledger (F-18), and are cross-linked into the governance log."),
    card("Normative directives", h("div", { class: "table-wrap" }, h("table", null, h("thead", null, h("tr", null, ["When", "Matter", "Position", "Priority", "Statement", "Escalation", "Event"].map((t) => h("th", null, t)))), tbody)))));
  async function load() {
    let d;
    try { d = await get("/api/view/directives"); } catch (e) { replace(tbody, h("tr", null, h("td", { colspan: 7 }, errorBox(e)))); return; }
    replace(tbody, d.directives.length ? d.directives.map((x) => h("tr", null, h("td", null, tsEl(x.ts)), h("td", null, badge(x.matter, "accent")), h("td", null, badge(x.position, x.position === "approve" ? "ok" : "warn")),
      h("td", null, x.priority ?? "—"), h("td", null, x.statement ?? "—"), h("td", { class: "mono" }, short(x.context?.escalation_id || "—", 14)), h("td", { class: "mono", title: x.event_hash }, "#" + x.seq + " " + short(x.event_hash, 8)))) : emptyRow(7, "No directives yet."));
  }
  await load();
  return { refresh: load };
}

// ================================================================ delegation
export async function delegation(main) {
  // Grant manager (D-70). The agent evaluator screen was removed; POST /api/delegation/evaluate stays for agents.
  const info = h("div", { class: "stack" });
  const chainBox = h("div");
  const i = { delegate: h("input", { placeholder: "agent:coder", value: "agent:coder" }), maxLines: h("input", { type: "number", min: 0, placeholder: "max lines / action" }),
    maxCum: h("input", { type: "number", min: 0, placeholder: "max cumulative lines" }), kinds: h("input", { placeholder: "allowed kinds, comma-separated (optional)" }),
    expires: h("input", { type: "datetime-local" }) };
  const limitsOf = (x) => {
    const l = {};
    if (x.maxLines.value !== "") l.max_lines_per_action = Number(x.maxLines.value);
    if (x.maxCum.value !== "") l.max_cumulative_lines = Number(x.maxCum.value);
    const k = x.kinds.value.split(",").map((t) => t.trim()).filter(Boolean); if (k.length) l.allowed_kinds = k;
    return l;
  };
  const iso = (v) => (v ? new Date(v).toISOString() : null);
  const rootCard = card("Create a root delegation grant",
    h("p", { class: "muted" }, "Only you can issue a root grant. Delegates may sub-delegate with narrower limits (never wider); revoking a grant revokes everything below it."),
    h("div", { class: "form" }, field("Delegate", i.delegate), field("Max lines / action", i.maxLines), field("Max cumulative lines", i.maxCum), field("Allowed kinds", i.kinds), field("Expires (optional)", i.expires),
      h("div", null, btn("Grant", "delegate_root", () => act(() => post("/api/delegation/grant", { delegate: i.delegate.value.trim(), limits: limitsOf(i), expires_at: iso(i.expires.value) }), "Delegation granted", "Grant"), "primary"))));
  replace(main, h("div", { class: "stack" }, rootCard, chainBox, info));

  async function subDelegate(g) {
    const x = { delegate: h("input", { placeholder: "agent:helper" }), maxLines: h("input", { type: "number", min: 0, placeholder: String(g.effective_limits.max_lines_per_action ?? "") }),
      maxCum: h("input", { type: "number", min: 0, placeholder: String(g.effective_limits.max_cumulative_lines ?? "") }), kinds: h("input", { placeholder: (g.effective_limits.allowed_kinds || []).join(", ") }) };
    const ok = await dialog({ title: `Sub-delegate from ${g.delegation_id}`, okText: "Sub-delegate",
      body: h("div", { class: "stack" }, h("p", { class: "muted" }, "Attenuation only: each limit must be at or below the parent's effective limit. Expiry is capped at the parent's."),
        h("div", { class: "muted mono" }, "parent effective limits: ", JSON.stringify(g.effective_limits)),
        h("div", { class: "form" }, field("Delegate", x.delegate), field("Max lines / action", x.maxLines), field("Max cumulative lines", x.maxCum), field("Allowed kinds", x.kinds))),
      onOk: () => (x.delegate.value.trim() ? true : (toast("Delegate required", "", "bad"), false)) });
    if (ok) await act(() => post("/api/delegation/grant", { delegate: x.delegate.value.trim(), parent: g.delegation_id, limits: limitsOf(x) }), "Sub-delegation granted", "Sub-delegate");
  }
  async function revoke(g) {
    if (await confirmDanger("Revoke delegation?", `Revoke ${g.delegation_id} (${g.delegate})? Every sub-delegation below it is revoked too, immediately.`, "Revoke"))
      await act(() => post("/api/delegation/revoke", { delegation_id: g.delegation_id }), "Revoked", "Revoke");
  }
  async function showChain(id) {
    let c;
    try { c = await get("/api/view/delegation_chain", { delegation_id: id }); } catch (e) { replace(chainBox, errorBox(e)); return; }
    const all = [...c.chain, ...c.descendants];
    const nodes = all.map((g) => ({ id: g.delegation_id, label: g.delegate, sub: (g.parent ? "sub · " : "root · ") + (g.active ? JSON.stringify(g.effective_limits) : "REVOKED"), status: g.active ? "ok" : "suspended", title: g.delegation_id }));
    const edges = all.filter((g) => g.parent).map((g) => ({ from: g.parent, to: g.delegation_id }));
    replace(chainBox, card(`Delegation chain · ${id}`,
      h("p", { class: "muted" }, "Root (granted by you) on the left; each arrow is an attenuation. Red: revoked (directly or above)."),
      dag({ nodes, edges, focus: id, nodeW: 220, onClick: (n) => showChain(n.id) }),
      h("table", null, h("thead", null, h("tr", null, ["Grant", "Delegate", "Granted by", "Own limits", "Effective limits", "Expires", "State"].map((t) => h("th", null, t)))),
        h("tbody", null, all.map((g) => h("tr", null, h("td", { class: "mono" }, g.delegation_id), h("td", null, g.delegate), h("td", null, g.granted_by), h("td", { class: "mono" }, JSON.stringify(g.limits)),
          h("td", { class: "mono" }, JSON.stringify(g.effective_limits)), h("td", null, g.expires_at ? tsEl(g.expires_at) : "—"), h("td", null, g.active ? badge("active", "ok") : badge("revoked", "bad"))))))));
  }
  async function load() {
    let d;
    try { d = await get("/api/view/delegation"); } catch (e) { replace(info, errorBox(e)); return; }
    const me = session.actor;
    replace(info,
      card("Delegation grants", h("table", null, h("thead", null, h("tr", null, ["Grant", "Delegate", "Effective limits", "Parent", "Granted", "State", ""].map((t) => h("th", null, t)))),
        h("tbody", null, d.grants.length ? d.grants.slice().reverse().map((g) => {
          const live = !g.chain_revoked_at && !(g.expires_at && g.expires_at <= new Date().toISOString());
          const holder = live && g.delegate === me;
          return h("tr", null, h("td", { class: "mono" }, g.delegation_id), h("td", null, g.delegate, holder ? [" ", badge("you hold this", "info")] : null), h("td", { class: "mono" }, JSON.stringify(g.effective_limits)),
            h("td", { class: "mono" }, g.parent || "root"), h("td", null, tsEl(g.granted_at), " by ", g.granted_by),
            h("td", null, g.chain_revoked_at ? badge(g.revoked_at ? "revoked" : "revoked above", "bad") : live ? badge("active", "ok") : badge("expired", "warn")),
            h("td", null, h("div", { class: "row" }, h("button", { class: "btn small", type: "button", onclick: () => showChain(g.delegation_id) }, "Chain"),
              holder ? btn("Sub-delegate…", "sub_delegate", () => subDelegate(g), "small") : null,
              !g.revoked_at ? btn("Revoke…", "delegation_revoke", () => revoke(g), "danger small") : null)));
        }) : emptyRow(7, "No delegation grants.")))),
      h("div", { class: "grid cards" },
        card("Budget (P-1.5)", h("div", { class: "stat" }, String(d.budget.used), h("small", null, `/ ${d.budget.limit} lines`)), h("div", { class: "muted" }, "baseline ", tsEl(d.budget.baseline))),
        card("Emergencies (P-1.6)", h("div", { class: "stat" }, String(d.emergencies.count), h("small", null, `/ ${d.emergencies.limit}`))),
        card("Recorded conditions", d.conditions.length ? d.conditions.slice(-6).reverse().map((c) => h("div", null, badge(c.condition + (c.matter ? "@" + c.matter : ""), c.value ? "warn" : ""), " ", String(c.value), " · ", c.actor, " · ", tsEl(c.ts))) : h("p", { class: "muted" }, "None."))),
      card("Recorded evaluations (agents submit via POST /api/delegation/evaluate)", d.recent_evaluations.length ? d.recent_evaluations.map((e) => h("details", { style: { borderBottom: "1px solid var(--border)", padding: "6px 0" } },
        h("summary", null, statusBadge(e.decision), " ", badge(e.clause, "accent"), " ", e.action.kind, " · ", (e.action.changes || []).map((c) => c.path).join(", "), " · ", tsEl(e.ts)), traceTable(e.trace))) : h("p", { class: "muted" }, "No evaluations yet.")));
    if (!chainBox.firstChild && d.grants.length) {
      const live = d.grants.filter((g) => !g.chain_revoked_at);
      const pick = live.find((g) => g.parent) || live[0] || d.grants[d.grants.length - 1];
      await showChain(pick.delegation_id);
    }
  }
  await load();
  return { refresh: load };
}
function traceTable(trace) {
  return h("table", { style: { marginTop: "6px" } }, h("thead", null, h("tr", null, h("th", null, "clause"), h("th", null, "result"), h("th", null, "detail"))),
    h("tbody", null, trace.map((t) => { const { clause, result, ...rest } = t; return h("tr", null, h("td", null, badge(clause, "accent")), h("td", null, result), h("td", { class: "mono" }, Object.keys(rest).length ? JSON.stringify(rest) : "")); })));
}
// ================================================================ suspensions
export async function suspensions(main) {
  const root = h("div", { class: "stack" });
  replace(main, root);
  async function load() {
    let g;
    try { g = await get("/api/view/primitive_graph"); } catch (e) { replace(root, errorBox(e)); return; }
    const nodes = g.nodes.map((n) => ({ id: n.id, label: n.id, sub: n.status === "ok" ? n.description : n.status.toUpperCase(), status: n.status, title: n.description }));
    const edges = g.edges.slice();
    const ids = new Set(nodes.map((n) => n.id));
    const addScoped = (cap, status) => {
      if (ids.has(cap)) return;
      const [base, matter] = cap.split(":");
      nodes.push({ id: cap, label: base, sub: ":" + matter + " · " + status.toUpperCase(), status, title: cap });
      ids.add(cap);
      edges.push({ from: base, to: cap });
    };
    for (const sc of g.scoped) addScoped(sc.id, "suspended");
    for (const a of g.adjacent) if (a.includes(":")) addScoped(a, "adjacent");
    const recById = Object.fromEntries(g.records.map((r) => [r.record.record_id, r]));
    const hl = [];
    for (const p of g.propagation) {
      const a = recById[p.from]?.record.capability, b = recById[p.to]?.record.capability;
      if (a && b && ids.has(a) && ids.has(b)) { hl.push({ from: a, to: b }); edges.push({ from: a, to: b, prop: true }); }
    }
    const active = g.records.filter((r) => ["SUSPENDED", "NONCOMPLIANT"].includes(r.status));
    replace(root,
      h("div", { class: "notice " + (active.length ? "bad" : "ok") }, active.length ? `${active.length} active suspension record(s). Suspension takes effect at the primitive (every interface reaching it is refused with 423) and propagates to direct dependents; indirect dependents are flagged adjacent. No actor can lift a suspension; only a PASS re-audit resolves it.` : "No active suspensions. All primitives are available."),
      card("Primitive dependency & suspension propagation", h("div", { class: "sub" }, "Arrows point from a primitive to the primitives that depend on it. Red dashed arrows: suspension propagation."),
        dag({ nodes, edges, highlight: hl, nodeW: 200, gapX: 46, fit: true, onClick: (n) => { const r = g.records.find((x) => x.record.capability === n.id); if (r) document.getElementById("rec-" + r.record.record_id)?.scrollIntoView({ behavior: "smooth" }); } }),
        h("div", { class: "legend" }, h("span", null, h("i", { class: "bad" }), "suspended"), h("span", null, h("i", { class: "warn" }), "adjacent (flagged, not suspended)"), h("span", null, h("i", { class: "ok" }), "available"))),
      card(`Suspension records (${g.records.length})`, g.records.length ? g.records.slice().reverse().map((r) => {
        const x = r.record;
        return h("details", { id: "rec-" + x.record_id, open: ["SUSPENDED", "NONCOMPLIANT"].includes(r.status), style: { borderBottom: "1px solid var(--border)", padding: "8px 0" } },
          h("summary", null, statusBadge(r.status), " ", h("span", { class: "mono" }, x.capability), " ", badge(x.classification, "bad"), x.propagated_from ? [" ", badge("propagated", "warn")] : null, " · ", tsEl(x.detected_at)),
          h("dl", { class: "kv", style: { marginTop: "8px" } },
            h("dt", null, "Record"), h("dd", { class: "mono" }, x.record_id), h("dt", null, "Trigger"), h("dd", null, x.trigger),
            x.section_iii_ref ? [h("dt", null, "Section III"), h("dd", null, x.section_iii_ref)] : null,
            h("dt", null, "Evidence available"), h("dd", null, x.evidence_available.join(", ") || "—"), h("dt", null, "Evidence missing"), h("dd", null, x.evidence_missing.join(", ") || "—"),
            h("dt", null, "Footprint"), h("dd", null, "direct: ", x.dependency_footprint.direct.join(", ") || "—", h("br"), "indirect: ", x.dependency_footprint.indirect.join(", ") || "—"),
            h("dt", null, "Interfaces"), h("dd", { class: "mono" }, x.interfaces.join(", ") || "—"),
            h("dt", null, "Resolution"), h("dd", null, x.resolution_condition),
            h("dt", null, "Transitions"), h("dd", null, r.transitions.length ? r.transitions.map((t) => h("div", null, `${t.from} → ${t.to} · `, tsEl(t.ts), " · ", t.basis?.auditor || "")) : "none")));
      }) : h("p", { class: "muted" }, "No suspension records.")));
  }
  await load();
  return { refresh: load };
}

// ================================================================ governance log explorer
export async function govLog(main, route) {
  const st = { kind: "", end: null, limit: 100, sel: route.query.get("seq") ? Number(route.query.get("seq")) : null };
  const kindSel = h("select", { "aria-label": "kind", onchange: (e) => { st.kind = e.target.value; load(); } });
  const search = h("input", { type: "search", placeholder: "filter actor / text  (/)", "data-search": "1", oninput: () => draw() });
  const tbody = h("tbody");
  const detail = h("div");
  const banner = h("div");
  const verifyBox = h("div");
  const pager = h("div", { class: "row" });
  let d = null;
  replace(main, h("div", { class: "stack" }, banner,
    h("section", { class: "card" },
      h("div", { class: "toolbar" }, kindSel, search, h("span", { class: "spacer" }), pager,
        h("button", { class: "btn", type: "button", onclick: verifyAll }, "Verify all chains"), btn("Integrity check (recorded)", "integrity_check", () => act(() => post("/api/integrity_check", {}), "Integrity check recorded", "Integrity check"))),
      verifyBox,
      h("div", { class: "grid two" },
        h("div", { class: "table-wrap" }, h("table", null, h("thead", null, h("tr", null, ["seq", "time", "kind", "actor", "chain"].map((t) => h("th", null, t)))), tbody)),
        detail))));
  async function load() {
    try { d = await get("/api/view/gov", { kind: st.kind, end_seq: st.end, limit: st.limit }); } catch (e) { replace(banner, errorBox(e)); return; }
    if (kindSel.options.length <= 1) replace(kindSel, h("option", { value: "" }, "all kinds"), d.kinds.map((k) => h("option", { value: k }, k)));
    const v = d.verification;
    replace(banner, h("div", { class: "notice " + (v.ok ? "ok" : "bad") }, v.ok ? `Governance chain verified: ${v.length} entries, head ${short(v.head, 16)}` : `Governance chain BROKEN at seq ${v.first_bad_seq}`));
    replace(pager,
      h("button", { class: "btn small", type: "button", disabled: d.start_seq <= 1, onclick: () => { st.end = Math.max(1, d.start_seq - 1); load(); } }, "← older"),
      h("span", { class: "muted" }, `seq ${d.start_seq}–${d.end_seq} of ${d.head_seq}`),
      h("button", { class: "btn small", type: "button", disabled: d.end_seq >= d.head_seq, onclick: () => { st.end = Math.min(d.head_seq, d.end_seq + st.limit); load(); } }, "newer →"),
      h("button", { class: "btn small", type: "button", disabled: st.end === null, onclick: () => { st.end = null; load(); } }, "latest"));
    draw();
  }
  function draw() {
    const q = search.value.toLowerCase();
    const es = d.entries.filter((e) => !q || (e.actor + " " + JSON.stringify(e.body)).toLowerCase().includes(q)).slice().reverse();
    const bySeq = Object.fromEntries(d.entries.map((e) => [e.seq, e]));
    replace(tbody, es.length ? es.map((e) => {
      const prev = bySeq[e.seq - 1];
      const link = prev ? prev.hash === e.prev_hash : null;
      const xl = d.cross_links_ok[e.seq];
      return h("tr", { class: "click" + (st.sel === e.seq ? " sel" : ""), tabindex: 0, onclick: () => { st.sel = e.seq; draw(); }, onkeydown: (ev) => { if (ev.key === "Enter") { st.sel = e.seq; draw(); } } },
        h("td", { class: "mono" }, e.seq), h("td", null, tsEl(e.ts)), h("td", null, badge(e.kind, e.kind === "PROHIBITED_ATTEMPT" ? "bad" : e.kind.startsWith("SUSPENSION") ? "warn" : "")), h("td", null, e.actor),
        h("td", { title: "prev_hash links to the previous entry's hash" }, link === null ? h("span", { class: "muted" }, "·") : link ? h("span", { class: "chain-ok" }, "✔") : h("span", { class: "chain-bad" }, "✘"),
          xl === undefined ? null : xl ? h("span", { class: "chain-ok", title: "cross-link to domain event verified" }, " ⇄") : h("span", { class: "chain-bad", title: "cross-link mismatch" }, " ⇄✘")));
    }) : emptyRow(5, "No entries."));
    const e = d.entries.find((x) => x.seq === st.sel);
    replace(detail, e ? h("section", { class: "card" }, h("h3", null, `#${e.seq} ${e.kind}`),
      h("dl", { class: "kv" }, h("dt", null, "time"), h("dd", null, tsEl(e.ts)), h("dt", null, "actor"), h("dd", null, e.actor), h("dt", null, "event id"), h("dd", { class: "mono" }, e.event_id),
        h("dt", null, "prev_hash"), h("dd", { class: "mono" }, e.prev_hash), h("dt", null, "hash"), h("dd", { class: "mono" }, e.hash)), h("h3", { style: { marginTop: "10px" } }, "body"), json(e.body))
      : h("div", { class: "card empty" }, "Select an entry to see its body and hashes."));
  }
  async function verifyAll() {
    try {
      const v = await get("/api/view/verify");
      replace(verifyBox, h("div", { class: "notice " + (v.ok ? "ok" : "bad"), style: { marginBottom: "10px" } },
        h("b", null, v.ok ? "All chains and cross-links verify. " : "Verification found problems. "),
        Object.values(v.streams).map((r) => h("span", { style: { marginRight: "10px" } }, r.ok ? "✔ " : "✘ ", r.stream, ` (${r.length})`)),
        v.cross_links_bad.length ? h("div", null, "bad cross-links at gov seq " + v.cross_links_bad.join(", ")) : null));
    } catch (e) { replace(verifyBox, errorBox(e)); }
  }
  await load();
  return { refresh: () => (st.end === null ? load() : Promise.resolve()) };
}

// ================================================================ audit log & anchors
export async function auditAnchors(main) {
  const root = h("div", { class: "stack" });
  replace(main, root);
  async function load() {
    let al, an;
    try { [al, an] = await Promise.all([get("/api/view/auditlog"), get("/api/view/anchors")]); } catch (e) { replace(root, errorBox(e)); return; }
    replace(root,
      card("Audit-read log (F-11)", h("div", { class: "sub" }, "Audit-plane reads stay open during suspension; each one made while any suspension is active is recorded here, in a separate hash-chained stream, so the governance log is not perturbed."),
        h("div", { class: "notice " + (al.verification.ok ? "ok" : "bad"), style: { marginBottom: "8px" } }, al.verification.ok ? `chain verified · ${al.verification.length} entries` : `chain broken at seq ${al.verification.first_bad_seq}`),
        h("div", { class: "table-wrap" }, h("table", null, h("thead", null, h("tr", null, ["seq", "time", "reader", "interface", "active suspensions"].map((t) => h("th", null, t)))),
          h("tbody", null, al.entries.length ? al.entries.slice().reverse().map((e) => h("tr", null, h("td", { class: "mono" }, e.seq), h("td", null, tsEl(e.ts)), h("td", null, e.body.reader), h("td", { class: "mono" }, e.body.interface), h("td", { class: "mono" }, e.body.active_suspensions.join(", "))))
            : emptyRow(5, "No audit reads during suspension."))))),
      card("External anchors (F-13)",
        h("div", { class: "notice " + (an.enabled ? "info" : "") }, an.enabled ? `Anchoring enabled · ${an.method} · ${an.tsa_url}. Only a SHA-256 digest of the stream heads leaves this machine.` : "External anchoring is off (config anchoring.enabled = false). Nothing leaves this machine. Enabling it is a configuration choice for you; the app cannot enable it."),
        h("div", { class: "row", style: { margin: "10px 0" } }, h("button", { class: "btn primary", type: "button", disabled: !an.enabled || !can("anchor"), title: !an.enabled ? "anchoring is disabled" : can("anchor") ? "" : "user only",
          onclick: async () => { if (await confirmDanger("Anchor stream heads externally?", `This sends one SHA-256 digest to ${an.tsa_url}. No content or identifiers are sent.`, "Send digest")) await act(() => post("/api/anchors/anchor", {}), "Anchored", "Anchor"); } }, "Anchor now")),
        h("h3", null, "Current stream heads"),
        h("table", null, h("tbody", null, Object.entries(an.current_heads).map(([s, v]) => h("tr", null, h("td", null, s), h("td", { class: "mono" }, "seq " + v.seq), h("td", { class: "mono" }, short(v.hash, 24)))))),
        h("h3", { style: { marginTop: "12px" } }, `Anchors (${an.anchors.length})`),
        an.anchors.length ? an.anchors.slice().reverse().map((a) => h("div", { class: "notice " + (a.verification.ok ? "ok" : "bad"), style: { marginBottom: "6px" } },
          h("b", null, a.anchor_id), " · ", tsEl(a.ts), " · digest ", h("span", { class: "mono" }, short(a.heads_digest, 16)), " · ", a.verification.ok ? "receipt binds heads" : "verification failed", " (signature: verify offline with openssl ts)"))
          : h("p", { class: "muted" }, "No anchors recorded.")));
  }
  await load();
  return { refresh: load };
}

// ================================================================ system
export async function system(main) {
  const root = h("div", { class: "stack" });
  replace(main, root);
  let tab = "self";
  async function load() {
    let sd, inv;
    try { [sd, inv] = await Promise.all([get("/api/q1/self_description"), get("/api/inventory")]); } catch (e) { replace(root, errorBox(e)); return; }
    const filter = h("input", { type: "search", placeholder: "filter interfaces / routes  (/)", "data-search": "1", oninput: () => drawTab() });
    const body = h("div");
    const tabs = h("div", { class: "tabs", role: "tablist" }, [["self", "Self-description"], ["inv", "Primitives"], ["routes", "HTTP routes"]].map(([k, l]) => h("button", { type: "button", role: "tab", class: tab === k ? "on" : "", "aria-selected": String(tab === k), onclick: () => { tab = k; load(); } }, l)));
    function drawTab() {
      const q = filter.value.toLowerCase();
      if (tab === "self") replace(body, h("dl", { class: "kv" }, h("dt", null, "System"), h("dd", null, `${sd.system} ${sd.version} (${sd.milestone})`), h("dt", null, "Charter digest"), h("dd", { class: "mono" }, sd.charter_digest),
        h("dt", null, "Network"), h("dd", null, netSummary(sd.network)), h("dt", null, "Streams"), h("dd", null, sd.storage.streams.join(", ")), h("dt", null, "Policies"), h("dd", { class: "mono" }, JSON.stringify(sd.policies)),
        h("dt", null, "Active suspensions"), h("dd", null, sd.active_suspensions.join(", ") || "none"), h("dt", null, "Components"),
        h("dd", null, h("table", null, h("tbody", null, Object.entries(sd.components).map(([k, v]) => h("tr", null, h("td", null, k), h("td", null, v.class), h("td", { class: "mono" }, short(v.source_sha256, 12))))))),
        h("dt", null, "Configuration"), h("dd", null, json(sd.configuration))));
      else if (tab === "inv") replace(body, h("div", { class: "table-wrap" }, h("table", null, h("thead", null, h("tr", null, ["Primitive", "Depends on", "Interfaces (plane)"].map((t) => h("th", null, t)))),
        h("tbody", null, Object.entries(inv.primitives).filter(([p, v]) => !q || (p + v.interfaces.join(" ")).toLowerCase().includes(q)).map(([p, v]) => h("tr", null, h("td", null, h("b", null, p), h("div", { class: "muted" }, v.description)), h("td", null, v.depends_on.join(", ") || "—"),
          h("td", null, v.interfaces.filter((x) => !q || x.toLowerCase().includes(q) || p.includes(q)).map((x) => h("div", { class: "mono" }, x, " ", badge(v.interface_planes[x] || "?", v.interface_planes[x] === "audit" ? "info" : ""))))))))));
      else replace(body, h("div", { class: "table-wrap" }, h("table", null, h("thead", null, h("tr", null, ["Method", "Path", "Plane", "Primitives", "Handler"].map((t) => h("th", null, t)))),
        h("tbody", null, Object.values(inv.routes).filter((r) => !q || (r.path + r.handler + r.primitives.join(" ")).toLowerCase().includes(q)).map((r) => h("tr", null, h("td", null, badge(r.method, r.method === "POST" ? "warn" : "info")), h("td", { class: "mono" }, r.path), h("td", null, r.plane), h("td", { class: "mono" }, r.primitives.join(", ") || "—"), h("td", { class: "mono" }, r.handler)))))));
    }
    replace(root,
      h("div", { class: "grid cards" },
        card("Export", h("p", { class: "muted" }, "Complete export (JSONL streams, content, state, PROV, schemas, standalone verifier), as a zip. Logged as EXPORT."),
          btn("Download export", "export", exportZip, "primary")),
        card("Integrity", h("p", { class: "muted" }, "Re-verify every hash chain and the append-only triggers. Recorded as INTEGRITY_CHECK; a broken chain suspends the primitive (UNDETERMINED)."),
          btn("Run integrity check", "integrity_check", async () => { const r = await act(() => post("/api/integrity_check", {}), null, "Integrity check"); if (r) toast(Object.values(r.streams).every((s) => s.ok) && r.triggers_ok ? "All chains verify" : "Integrity problem found", "", Object.values(r.streams).every((s) => s.ok) ? "ok" : "bad"); })),
        card("Q-1 audit queries", h("p", { class: "muted" }, "Exactly eight read-only audit queries, available over /api/q1/<query>."), h("div", { class: "row" }, (sd.q1_queries || []).map((q) => badge(q, "info"))))),
      h("section", { class: "card" }, tabs, h("div", { class: "toolbar" }, filter), body));
    drawTab();
  }
  await load();
  return {};
}
async function exportZip() {
  try {
    const r = await api("/api/export", { raw: true });
    const blob = await r.blob();
    const name = (r.headers.get("Content-Disposition") || "").match(/filename="([^"]+)"/)?.[1] || "medb-export.zip";
    const url = URL.createObjectURL(blob);
    const a = h("a", { download: name });
    a.href = url; document.body.appendChild(a); a.click(); a.remove();
    setTimeout(() => URL.revokeObjectURL(url), 5000);
    toast("Export downloaded", name, "ok");
  } catch (e) { toast("Export failed", e.message, "bad"); }
}

// D-68: the self-description's network profile is generated; summarise it, full record on expand
function netSummary(net) {
  if (typeof net !== "object" || !net) return String(net);
  const line = (e) => h("div", null, badge(e.direction, e.direction === "outbound" ? "warn" : "info"), " ", h("span", { class: "mono" }, e.module), " · ",
    e.direction === "outbound" ? `${e.protocol}; ${e.enabled ? "ENABLED" : "disabled"} (default ${e.default_enabled ? "on" : "off"}); sends: ${e.sends}`
      : `${e.protocol}; bound to ${(e.bind_hosts || []).join(", ")}`);
  return h("div", null, ...net.modules_with_network_code.map(line),
    net.undeclared.length ? h("div", null, badge(`${net.undeclared.length} undeclared network module(s)`, "bad")) : h("div", { class: "muted" }, "no other module has network code (generated: " + net.derived_from + ")"),
    h("details", null, h("summary", null, "full record"), h("pre", { class: "mono" }, JSON.stringify(net, null, 1))));
}
