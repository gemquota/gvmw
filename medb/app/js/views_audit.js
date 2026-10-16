// Auditor desk (F-04, D-69): appointment status, suspension evidence (audit plane only), audit results.
import { h, replace, tsEl, short, badge, statusBadge, dialog, confirmDanger, field, card, emptyRow, toast } from "./dom.js";
import { get, post, can, session } from "./api.js";
import { errorBox, act } from "./common.js";
import { btn } from "./views_knowledge.js";

const OUTCOMES = ["PASS", "FAIL", "UNDETERMINED", "AUDIT_INDETERMINACY"];
const RULES = {
  PASS: "Resolves the record (and records propagated from it).",
  FAIL: "The record becomes NONCOMPLIANT.",
  UNDETERMINED: "Stays SUSPENDED: re-audit inconclusive.",
  AUDIT_INDETERMINACY: "Stays SUSPENDED and REAUDIT_REQUIRED is logged. On its own it never suspends anything (F-08).",
  CONSTITUTIONAL_UNDERDETERMINATION: "Suspends the capability; must cite a Section III question (e.g. III.1).",
};
const STATUS_KIND = { SUSPENDED: "bad", NONCOMPLIANT: "bad", RESOLVED_PASS: "ok" };

export async function auditorDesk(main, route) {
  const top = h("div", { class: "grid cards" });
  const apBox = h("div");
  const recBox = h("div");
  const evBox = h("div");
  const resultBox = h("div");
  replace(main, h("div", { class: "stack" },
    h("div", { class: "notice info" }, "The auditor desk uses the audit plane only: suspension records, governance-log and audit-log evidence, hashes and identifiers, never claim content. ",
      "Auditors are appointed only by the independent appointer's signed statements (F-04); neither you nor the system can appoint one."),
    top, recBox, evBox, resultBox, apBox));
  let selected = route?.query?.get("record") || null;

  async function load() {
    let ap, sus, who;
    try { [ap, sus, who] = await Promise.all([get("/api/view/appointments"), get("/api/view/suspensions"), get("/api/app/whoami")]); }
    catch (e) { replace(top, errorBox(e)); return; }
    const mine = who.appointment;
    replace(top,
      card("You", h("div", { class: "stat" }, short(who.actor, 24)),
        mine ? (mine.active ? badge("appointment active", "ok") : badge("no active appointment", "bad")) : badge("not an auditor token", "warn"),
        mine ? h("div", { class: "muted" }, mine.appointments.length ? mine.appointments.map((a) => h("div", { class: "mono" }, a.appointment_id, " · ", a.active ? "active" : a.revoked_at ? "revoked" : "expired")) : "No appointment recorded for this id.") : null),
      card("Appointer (fixed)", ap.appointer ? [h("div", { class: "mono" }, ap.appointer.id), h("div", { class: "muted" }, "bound at ", ap.appointer.source, " · key ", short(ap.appointer.key_fingerprint, 12)), h("div", { class: "muted" }, ap.method)]
        : h("div", { class: "notice warn" }, "No appointer is bound to this database, so no auditor can act.")),
      card("Active auditors", h("div", { class: "stat" }, String(ap.active_auditors.length)), h("div", { class: "muted mono" }, ap.active_auditors.join(", ") || "none")));
    replace(apBox,
      card("Appointments (signed by the appointer; hash-chained, cross-linked to the governance log)", h("div", { class: "table-wrap" }, h("table", null, h("thead", null, h("tr", null, ["auditor", "appointment", "issued by", "recorded", "statement sha256", "state"].map((t) => h("th", null, t)))),
        h("tbody", null, ap.appointments.length ? ap.appointments.map((a) => h("tr", null, h("td", { class: "mono" }, a.auditor_id), h("td", { class: "mono" }, a.appointment_id), h("td", { class: "mono" }, a.appointer_id), h("td", null, tsEl(a.recorded_at)), h("td", { class: "mono" }, short(a.statement_sha256, 12)),
          h("td", null, a.active ? badge("active", "ok") : badge(a.revoked_at ? "revoked" : "expired", "warn")))) : emptyRow(6, "None.")))),
        h("div", { class: "muted" }, "appointments chain ", ap.verification.ok ? "verifies ✔" : "BROKEN ✖")));
    const recs = sus.records.slice().sort((a, b) => (a.status === "SUSPENDED" ? -1 : 1) - (b.status === "SUSPENDED" ? -1 : 1));
    if (selected === "first") selected = recs[0]?.record.record_id || null;
    replace(recBox, card(`Suspension records (${recs.length})`,
      h("div", { class: "table-wrap" }, h("table", null, h("thead", null, h("tr", null, ["capability", "classification", "status", "detected", ""].map((t) => h("th", null, t)))),
        h("tbody", null, recs.length ? recs.map((r) => h("tr", { class: r.record.record_id === selected ? "sel" : "" },
          h("td", { class: "mono" }, r.record.capability, r.record.propagated_from ? h("div", { class: "muted" }, "propagated") : null), h("td", null, badge(r.record.classification, "")),
          h("td", null, badge(r.status, STATUS_KIND[r.status] || "")), h("td", null, tsEl(r.record.detected_at)),
          h("td", null, h("button", { class: "btn small", type: "button", onclick: () => { selected = r.record.record_id; evidence(); load(); } }, "Evidence")))) : emptyRow(5, "No suspension records."))))));
    resultForm(sus);
    if (selected) await evidence();
  }

  async function evidence() {
    let ev;
    try { ev = await get("/api/view/audit_evidence", { record_id: selected }); } catch (e) { replace(evBox, errorBox(e)); return; }
    const rec = ev.record.record, open = ["SUSPENDED", "NONCOMPLIANT"].includes(ev.record.status);
    const outcome = h("select", null, OUTCOMES.map((o) => h("option", null, o)));
    const ref = h("input", { placeholder: "audit reference, e.g. reaudit-2026-10-02" });
    const rule = h("div", { class: "muted" }, RULES.PASS);
    outcome.addEventListener("change", () => { rule.textContent = RULES[outcome.value]; });
    async function resolve() {
      if (!ref.value.trim()) { toast("Audit reference required", "", "bad"); return; }
      const o = outcome.value;
      if ((o === "PASS" || o === "FAIL") && !(await confirmDanger(`Record ${o}?`, `${o} on ${rec.record_id} (${rec.capability}). ${RULES[o]} This is recorded permanently in the governance log.`, `Record ${o}`))) return;
      const r = await act(() => post("/api/audit/resolve", { record_id: rec.record_id, outcome: o, audit_ref: ref.value.trim() }), null, "Re-audit");
      if (r) toast(`Re-audit recorded: ${r.status}`, rec.record_id, r.status === "RESOLVED_PASS" ? "ok" : "warn");
    }
    replace(evBox, card(`Evidence · ${rec.record_id}`,
      h("dl", { class: "kv" }, h("dt", null, "Capability"), h("dd", { class: "mono" }, rec.capability), h("dt", null, "Status"), h("dd", null, badge(ev.record.status, STATUS_KIND[ev.record.status] || "")),
        h("dt", null, "Trigger"), h("dd", null, rec.trigger), h("dt", null, "Section III"), h("dd", null, rec.section_iii_ref || "—"),
        h("dt", null, "Evidence available"), h("dd", { class: "mono" }, (rec.evidence_available || []).join(", ") || "—"),
        h("dt", null, "Evidence missing"), h("dd", { class: "mono" }, (rec.evidence_missing || []).join(", ") || "—"),
        h("dt", null, "Propagated from / to"), h("dd", { class: "mono" }, rec.propagated_from || "—", " → ", ev.propagated_children.join(", ") || "—"),
        h("dt", null, "Resolution condition"), h("dd", null, rec.resolution_condition),
        h("dt", null, "Audit reads during"), h("dd", null, String(ev.audit_reads_count), " (auditlog stream, F-11)"),
        h("dt", null, "Chains"), h("dd", null, Object.entries(ev.chains).map(([k, v]) => badge(k + (v ? " ✔" : " ✖"), v ? "ok" : "bad")))),
      h("h3", null, "Transitions"),
      ev.record.transitions.length ? h("ol", { class: "timeline" }, ev.record.transitions.map((t) => h("li", null, h("b", null, `${t.from} → ${t.to}`), " · ", tsEl(t.ts), " · ", t.basis?.auditor || "", " · ", t.basis?.outcome || "", t.basis?.note ? ` (${t.basis.note})` : ""))) : h("p", { class: "muted" }, "None (no re-audit yet)."),
      h("h3", null, `Related governance entries (${ev.related_gov_entries.length})`),
      h("div", { class: "table-wrap" }, h("table", null, h("thead", null, h("tr", null, ["seq", "kind", "actor", "time", "hash"].map((t) => h("th", null, t)))),
        h("tbody", null, ev.related_gov_entries.slice(-12).reverse().map((e) => h("tr", null, h("td", { class: "mono" }, String(e.seq)), h("td", null, badge(e.kind, "")), h("td", null, e.actor), h("td", null, tsEl(e.ts)), h("td", { class: "mono" }, short(e.hash, 10))))))),
      open ? h("div", { class: "stack" }, h("h3", null, "Record re-audit outcome"),
        h("div", { class: "form" }, field("Outcome", outcome), field("Audit reference", ref), h("div", { class: "wide" }, rule), h("div", null, btn("Record outcome", "audit", resolve, "primary"))))
        : h("div", { class: "notice ok" }, "This record is closed (", ev.record.status, ").")));
  }

  function resultForm(sus) {
    const caps = new Set();
    for (const r of sus.records) caps.add(r.record.capability);
    ["context.ranking", "context.rendering", "context.build", "claims.retrieval", "delegation.evaluator", "authority.resolution", "governance.log"].forEach((c) => caps.add(c));
    const cap = h("select", null, [...caps].sort().map((c) => h("option", null, c)));
    const outcome = h("select", null, [...OUTCOMES, "CONSTITUTIONAL_UNDERDETERMINATION"].map((o) => h("option", null, o)));
    const ref = h("input", { placeholder: "audit reference" }), avail = h("input", { placeholder: "evidence available, comma-separated" }), missing = h("input", { placeholder: "evidence missing, comma-separated" });
    const s3 = h("input", { placeholder: "III.1 (only for CONSTITUTIONAL_UNDERDETERMINATION)" });
    const rule = h("div", { class: "muted" }, RULES.PASS);
    outcome.addEventListener("change", () => { rule.textContent = RULES[outcome.value]; });
    const csv = (v) => v.split(",").map((x) => x.trim()).filter(Boolean);
    async function submit() {
      if (!ref.value.trim()) { toast("Audit reference required", "", "bad"); return; }
      const o = outcome.value;
      if ((o !== "PASS" && o !== "AUDIT_INDETERMINACY") && !(await confirmDanger(`Record ${o} for ${cap.value}?`, `${RULES[o]} A suspension can never be lifted by any actor; only a later PASS re-audit resolves it.`, `Record ${o}`))) return;
      const r = await act(() => post("/api/audit/result", { capability: cap.value, outcome: o, audit_ref: ref.value.trim(), evidence_available: csv(avail.value), evidence_missing: csv(missing.value), section_iii_ref: s3.value.trim() || null }), null, "Audit result");
      if (r) toast("Audit result recorded", r.reaudit_required ? "Re-audit required (no automatic suspension, F-08)" : (r.records || []).map((x) => `${x.record_id}: ${x.status}`).join(", ") || "No record changed", "ok");
    }
    replace(resultBox, card("Record an audit result for a capability",
      h("p", { class: "muted" }, "Existing rules apply: PASS/FAIL act on open records for the capability; UNDETERMINED and CONSTITUTIONAL_UNDERDETERMINATION suspend it; AUDIT_INDETERMINACY only requires a re-audit (F-08)."),
      h("div", { class: "form" }, field("Capability", cap), field("Outcome", outcome), field("Audit reference", ref), field("Section III ref", s3), field("Evidence available", avail), field("Evidence missing", missing),
        h("div", { class: "wide" }, rule), h("div", null, btn("Record result", "audit", submit, "primary")))));
  }
  await load();
  return { refresh: load };
}
