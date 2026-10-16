// Integrations (D-72..D-78): status of each integration, live account sync (user only), notification outbox feed,
// file importer (user only).
import { h, replace, tsEl, short, badge, field, card, emptyRow, dialog } from "./dom.js";
import { get, post, can } from "./api.js";
import { errorBox, act, reportError } from "./common.js";

const onOff = (v) => badge(v ? "enabled" : "disabled", v ? "ok" : "");
const EVENT_KIND = { ESCALATION_OPENED: "warn", SUSPENSION: "bad", OBLIGATION_BREACHED: "bad", INFERENCE_PROPOSED: "",
  SYNC_REMOTE_DELETION: "warn", SYNC_FAILED: "bad" };
const EVENT_LINK = { ESCALATION_OPENED: "#/escalations", SUSPENSION: "#/suspensions", OBLIGATION_BREACHED: "#/delegation",
  INFERENCE_PROPOSED: "#/claims", SYNC_REMOTE_DELETION: "#/integrations", SYNC_FAILED: "#/integrations" };

function kv(rows) {
  return h("dl", { class: "kv" }, ...rows.filter(Boolean).flatMap(([k, v]) => [h("dt", null, k), h("dd", null, v)]));
}

export async function integrations(main) {
  const top = h("div", { class: "grid cards" });
  const impBox = h("div");
  const feedBox = h("div");
  const runsBox = h("div");
  const mcpBox = h("div");
  const syncBox = h("div");
  replace(main, h("div", { class: "stack" },
    h("div", { class: "notice info" }, "All integrations are off by default and are switched on locally in data/integrations.json. ",
      "Only live account sync (D-76) leaves this machine: HTTPS, read-only, to a fixed host allowlist per provider, and only for ",
      "services you enabled and connected. Everything else stays on 127.0.0.1."),
    top, syncBox, impBox, feedBox, runsBox, mcpBox));

  async function load() {
    let st, feed, runs, mcp;
    try {
      [st, feed, runs, mcp] = await Promise.all([get("/api/integrations/status"), get("/api/view/outbox", { limit: 100 }),
        get("/api/view/import_runs"), get("/api/view/mcp_activity", { limit: 20 })]);
    } catch (e) { replace(top, errorBox(e)); return; }
    const m = st.mcp, im = st.importers, ob = st.outbox;
    replace(top,
      card("MCP server (AI assistants)", onOff(m.enabled),
        kv([["Actor", h("span", { class: "mono" }, m.actor || "—")], ["Inference actor", h("span", { class: "mono" }, m.inference_actor || "—")],
          ["API", h("span", { class: "mono" }, m.api_url || "—")], ["Tools", String(m.tools.length)],
          ["Last activity", m.last_activity ? tsEl(m.last_activity) : "none"],
          m.configured && m.config_errors.length ? ["Config", h("span", { class: "bad" }, m.config_errors.join("; "))] : null]),
        h("div", { class: "muted" }, "Never acts as you: no tools for self-accounts, confirmations, grants or escalation decisions.")),
      card("File importers", onOff(im.enabled),
        kv([["Actor", "user only"], ["Formats", String(im.formats.length)], ["Default sensitivity", im.default_sensitivity],
          ["Import roots", im.allowed_roots.length ? h("span", { class: "mono" }, im.allowed_roots.join(", ")) : "—"],
          ["Last activity", im.last_activity ? tsEl(im.last_activity) : "none"]]),
        h("div", { class: "muted" }, "Local files only; an ingest grant is required; cookie values are never read.")),
      card("Notification outbox", onOff(ob.enabled),
        kv([["Actor", "system"], ["Events", ob.events.join(", ") || "—"],
          ["Webhook", ob.webhook.enabled ? h("span", { class: "mono" }, ob.webhook.url) : "disabled"],
          ["Last activity", ob.last_activity ? tsEl(ob.last_activity) : "none"]]),
        h("div", { class: "muted" }, "Identifiers and kinds only, never content. Webhook: 127.0.0.1 / ::1 only.")));

    replace(feedBox, card(`Notifications (${feed.count})`,
      !feed.enabled ? h("div", { class: "notice" }, "The outbox is disabled, so no notifications are derived.") : null,
      h("div", { class: "table-wrap" }, h("table", null,
        h("thead", null, h("tr", null, ["event", "title", "references", "at", "delivery"].map((t) => h("th", null, t)))),
        h("tbody", null, feed.notifications.length ? feed.notifications.map((n) => h("tr", null,
          h("td", null, badge(n.event, EVENT_KIND[n.event] ?? "")),
          h("td", null, h("a", { href: EVENT_LINK[n.event] || "#/gov" }, n.title)),
          h("td", { class: "mono" }, Object.entries(n.refs || {}).filter(([, v]) => v !== null && v !== undefined)
            .map(([k, v]) => `${k}=${short(String(v), 14)}`).join("  ")),
          h("td", null, tsEl(n.at)),
          h("td", null, n.delivery ? (n.delivery.status ? badge(String(n.delivery.status), "ok") : badge("failed", "bad")) : "—")))
          : emptyRow(5, "No notifications.")))),
      h("div", { class: "muted" }, "outbox chain ", feed.verification.ok ? "verifies ✔" : "BROKEN ✖")));

    replace(runsBox, card("Import runs",
      h("div", { class: "table-wrap" }, h("table", null,
        h("thead", null, h("tr", null, ["when", "result", "file", "format", "items", "third-party", "sha256"].map((t) => h("th", null, t)))),
        h("tbody", null, runs.runs.length ? runs.runs.slice(0, 30).map((r) => h("tr", null,
          h("td", null, tsEl(r.ts)),
          h("td", null, r.kind === "IMPORT_RUN" ? badge("imported", "ok") : badge(r.reason || "refused", "warn")),
          h("td", { class: "mono" }, r.file_name || "—"), h("td", null, r.format || "—"),
          h("td", null, r.ingested ?? "—"), h("td", null, r.third_party_items ? String(r.third_party_items) : "—"),
          h("td", { class: "mono" }, r.file_sha256 ? short(r.file_sha256, 12) : "—")))
          : emptyRow(7, "No imports yet."))))));

    replace(mcpBox, card("Recent MCP calls",
      h("div", { class: "table-wrap" }, h("table", null,
        h("thead", null, h("tr", null, ["at", "tool", "actor", "status"].map((t) => h("th", null, t)))),
        h("tbody", null, mcp.calls.length ? mcp.calls.map((c) => h("tr", null, h("td", null, tsEl(c.at)),
          h("td", { class: "mono" }, c.tool), h("td", { class: "mono" }, c.actor),
          h("td", null, badge(String(c.status), c.status < 300 ? "ok" : c.status === 423 ? "bad" : "warn"))))
          : emptyRow(4, "No MCP calls recorded."))))));

    renderSync(st.live_sync);
    return im;
  }

  function renderSync(ls) {
    const mine = can("sync");
    const rows = Object.values(ls.services).map((sv) => {
      const last = sv.last_sync;
      const btns = [];
      if (mine && sv.enabled) {
        if (!sv.connected) btns.push(h("button", { class: "btn primary small", type: "button", disabled: !sv.connectable,
          title: sv.connectable ? "" : "missing: " + sv.not_connectable_because.join(", "), onclick: () => connect(sv) }, "Connect…"));
        else {
          btns.push(h("button", { class: "btn small", type: "button", onclick: () => act(async () => {
            const r = await post("/api/sync/run", { service: sv.service });
            if (!r.ok) throw Object.assign(new Error(r.error || "sync failed"), { hint: "Sync failed" });
            return r;
          }, `${sv.label}: sync finished`, "Sync") }, "Sync now"));
          btns.push(h("button", { class: "btn small danger", type: "button", onclick: () => dialog({ title: `Disconnect ${sv.label}?`,
            body: h("p", null, sv.provider === "local" ? "MedB stops reading this browser profile. Items already synced stay in the corpus (withdraw them there if you want)."
              : `Deletes the local ${sv.provider} token (it also serves your other ${sv.provider} services). Items already synced stay in the corpus. `
              + (sv.provider === "github" ? "Revoke the app at github.com/settings/applications too." : "MedB also asks the provider to revoke the token.")),
            okText: "Disconnect", okKind: "danger",
            onOk: () => act(() => post("/api/sync/disconnect", { service: sv.service, remote_revoke: sv.provider !== "local" }),
              `${sv.label} disconnected`, "Disconnect") }) }, "Disconnect"));
        }
      }
      return h("tr", null,
        h("td", null, h("b", null, sv.label), h("div", { class: "muted mono" }, sv.service)),
        h("td", null, onOff(sv.enabled), " ", sv.connected ? badge("connected", "ok") : badge("not connected", ""),
          sv.provider !== "local" && sv.enabled && sv.client_missing.length ? h("div", { class: "warn" }, `data/sync_clients.json missing: ${sv.client_missing.join(", ")}`) : null),
        h("td", { class: "mono" }, sv.account_id || "—"),
        h("td", null, last ? tsEl(last.at) : "never"),
        h("td", null, String(sv.items), last ? h("div", { class: "muted" }, `last: +${last.ingested} new, ${last.updated} updated, ${last.unchanged} unchanged`
          + (last.remote_deletions ? `, ${last.remote_deletions} deleted remotely` : "")) : null),
        h("td", null, last?.error ? h("span", { class: "bad" }, last.error) : "—"),
        h("td", { class: "mono" }, sv.hosts.length ? sv.hosts.join(" ") : "local files"),
        h("td", null, ...btns));
    });
    replace(syncBox, card("Live account sync", onOff(ls.enabled),
      h("p", { class: "muted" }, "Read-only scopes only. Tokens are stored locally in data/sync_tokens/ (0600, not encrypted — F-29) and are never shown, ",
        "logged or exported. Every synced item is sensitivity high, needs an ingest grant for source ", h("span", { class: "mono" }, "sync:<service>"),
        ", records its provenance, and is never erased (remote deletions are only reported). Assistants can never connect or sync. ",
        "Schedule: ", ls.schedule.enabled ? `every ${ls.schedule.interval_minutes} min` : "off", ". Setup: docs/INTEGRATIONS.md."),
      h("div", { class: "table-wrap" }, h("table", null,
        h("thead", null, h("tr", null, ["service", "status", "account", "last sync", "items", "error", "hosts", ""].map((t) => h("th", null, t)))),
        h("tbody", null, rows))),
      mine && ls.services && Object.values(ls.services).some((x) => x.connected) ? h("div", { class: "row" },
        h("button", { class: "btn", type: "button", onclick: () => act(() => post("/api/sync/run", { all: true }), "Sync finished", "Sync") }, "Sync all connected")) : null));
  }

  async function connect(sv) {
    let r;
    try { r = await post("/api/sync/connect", { service: sv.service }); } catch (e) { reportError(e, "Connect"); return; }
    if (r.mode === "local") { await act(async () => r, `${sv.label} connected`, "Connect"); return; }
    const status = h("div", { class: "notice" }, "Waiting for you to authorise…");
    const body = r.mode === "device"
      ? h("div", null, h("p", null, "Open ", h("a", { href: r.verification_uri, target: "_blank", rel: "noopener" }, r.verification_uri),
        " and enter this code:"), h("p", { class: "mono", style: "font-size:1.6em" }, r.user_code),
        h("p", { class: "muted" }, `Scopes requested: ${r.scopes.join(", ")}`), status)
      : h("div", null, h("p", null, "Sign in and approve read-only access in your browser:"),
        h("p", null, h("a", { class: "btn primary", href: r.auth_url, target: "_blank", rel: "noopener" }, `Open ${sv.provider} sign-in`)),
        h("p", { class: "muted" }, `Scopes requested: ${r.scopes.join(", ")}. You will be sent back to MedB on this machine.`), status);
    let stop = false;
    const poll = async () => {
      if (stop) return;
      try {
        const p = await post("/api/sync/connect_poll", { service: sv.service });
        if (!p.pending) { replace(status, h("span", { class: "ok" }, `Connected as ${p.account_id}.`)); stop = true; return; }
      } catch (e) { replace(status, errorBox(e)); stop = true; return; }
      setTimeout(poll, 1000 * Math.max(2, r.interval || 2));
    };
    setTimeout(poll, 1500);
    await dialog({ title: `Connect ${sv.label}`, body, okText: "Done", onOk: () => true });
    stop = true;
    await act(async () => true, null, "Connect");
  }

  async function importer(im) {
    if (!im.enabled) {
      replace(impBox, card("Import files", h("div", { class: "notice" },
        "File importers are disabled. Enable them in data/integrations.json (integrations.importers.enabled) and restart the API.")));
      return;
    }
    let files, fmts;
    try { [files, fmts] = await Promise.all([get("/api/import/files"), get("/api/import/formats")]); }
    catch (e) { replace(impBox, errorBox(e)); return; }
    const fileSel = h("select", null, files.files.length ? files.files.map((f) => h("option", { value: f.path }, `${f.path} (${Math.ceil(f.bytes / 1024)} KB)`))
      : h("option", { value: "" }, "No files in the import roots"));
    const fmtSel = h("select", null, h("option", { value: "" }, "auto-detect (unknown formats are refused)"),
      ...fmts.formats.map((f) => h("option", { value: f.id }, f.label)));
    const scope = h("input", { placeholder: "default for the format" });
    const source = h("input", { placeholder: "default import:<format>" });
    const sens = h("select", null, ...["high", "moderate", "low"].map((s) => h("option", { value: s }, s)));
    const account = h("input", { placeholder: "e.g. gmail:me@example.org (label only)" });
    const out = h("div");
    fmtSel.onchange = () => {
      const f = fmts.formats.find((x) => x.id === fmtSel.value);
      scope.placeholder = f ? f.default_scope : "default for the format";
      source.placeholder = f ? f.default_source : "default import:<format>";
    };
    const run = () => act(async () => {
      const r = await post("/api/import/file", { path: fileSel.value, format: fmtSel.value || null, scope: scope.value || null,
        source: source.value || null, sensitivity: sens.value, account: account.value || null });
      replace(out, h("div", { class: "notice ok" }, `Imported ${r.ingested} item(s) as ${r.format_label} into scope "${r.scope}" `,
        `(source ${r.source}, sensitivity ${r.sensitivity}). File sha256 ${short(r.file_sha256, 16)}. `,
        r.third_party_items ? `${r.third_party_items} item(s) contain other people's content (F-24). ` : "",
        Object.keys(r.skipped || {}).length ? `Skipped: ${JSON.stringify(r.skipped)}. ` : "",
        r.truncated_at_max_items ? "Stopped at max_items_per_run. " : "", h("a", { href: "#/corpus" }, "Open corpus")));
      return r;
    }, "Import finished", "Import");
    replace(impBox, card("Import files into the corpus",
      h("p", { class: "muted" }, "Your own exports only (Google Takeout, GitHub, Facebook, FHIR records, notes, browser profile copies). ",
        "The file must be under ", h("span", { class: "mono" }, files.roots.join(", ")), ". An ingest grant must cover the source, scope and sensitivity. ",
        "Cookie files yield per-domain metadata only; names and values are never read."),
      h("div", { class: "form" }, field("File", fileSel), field("Format", fmtSel), field("Scope", scope), field("Source", source),
        field("Sensitivity", sens), field("Source account (label)", account)),
      h("div", { class: "row" }, h("button", { class: "btn primary", type: "button", disabled: !files.files.length,
        onclick: () => dialog({ title: "Import this file?", body: h("p", null, `Import ${fileSel.value} into the corpus? Corpus items cannot be erased, only withdrawn (F-05).`),
          okText: "Import", onOk: run }) }, "Import…")),
      out));
  }
  const im = await load();
  if (im && can("import")) await importer(im);
  return { refresh: load };
}
