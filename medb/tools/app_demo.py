#!/usr/bin/env python3
"""Run the MedB API + interactive app on a throwaway database seeded with a
richer demo (used for screenshots). Never touches data/medb.sqlite.

    python3 tools/app_demo.py --db /tmp/medb_app_demo.sqlite --port 8766 --tokens /tmp/medb_app_demo_tokens.json

The rich seed includes a III.1 constitutional-underdetermination suspension,
which can never be lifted -- that is why it lives in a throwaway database.

F-04 (D-69): this script also *plays the independent appointer* for the demo
only: it creates a throwaway appointer key next to the demo DB, binds it at
genesis, and signs an appointment for ``auditor:demo-1`` (token in the demo
tokens file). Never do this for a real database.
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from medb.api import load_tokens, make_server  # noqa: E402
from medb.auditors import key_fingerprint, new_statement, sign_statement  # noqa: E402
from medb.system import MedB, load_config  # noqa: E402

DEMO_APPOINTER = "appointer:demo-outside-party"
DEMO_AUDITOR = "auditor:demo-1"
DEMO_KEY: list = []
from medb.util import SystemClock  # noqa: E402
import datetime as _dt  # noqa: E402


class SeedClock(SystemClock):
    """Past, stepped time while seeding; real time afterwards (monotonic)."""

    def __init__(self, days_ago: float = 9):
        self.t = _dt.datetime.now(_dt.timezone.utc) - _dt.timedelta(days=days_ago)
        self.seeding = True

    def step(self, **kw):
        self.t += _dt.timedelta(**kw)

    def now(self):
        return self.t if self.seeding else super().now()


def seed_rich(m, clk: SeedClock) -> None:
    if m.claims.state():
        return
    m.perms.grant("use", "user", scopes=["authority", "health"], purposes=["clinic-visit"], sensitivity_max="high", compose=True)
    m.perms.grant("infer", "user", scopes=["authority", "health"], sensitivity_max="high", compose=True)
    m.perms.grant("ingest", "user", scopes=["health"], sources=["clinic-letters"], sensitivity_max="high")
    m.perms.grant("model", "user", scopes=["authority", "health"], sensitivity_max="high")
    m.perms.grant("use", "user", scopes=["food"], purposes=["meal-planning"], sensitivity_max="high")
    clk.step(hours=3)
    a = m.claims.assert_claim("user", "decides", "my own treatment decisions", scope="authority", sensitivity="moderate")
    h = m.claims.assert_claim("user", "has", "asthma", scope="health")
    letter = m.corpus.ingest("Letter from Dr Lee: asthma review, reliever as needed.", source="clinic-letters",
                             scope="health", actor="user")
    old = m.corpus.ingest("Old referral (superseded).", source="clinic-letters", scope="health", actor="user")
    clk.step(hours=20)
    p = m.claims.propose("user", "decides", "the clinician should decide", scope="authority", derived_from=[a],
                         actor="inference:demo", sensitivity="moderate")
    inh = m.claims.propose("user", "carries", "a reliever inhaler", scope="health", derived_from=[h, letter["corpus_id"]],
                           actor="inference:demo")
    m.claims.propose("user", "avoids", "cold air when exercising", scope="health", derived_from=[inh],
                     actor="inference:demo")
    m.claims.propose("user", "needs", "an annual asthma review", scope="health", derived_from=[old["corpus_id"]],
                     actor="inference:demo")
    clk.step(days=1, hours=4)
    m.claims.correct(a, object="my own treatment decisions, after hearing options")
    m.claims.reject(p, reason="not how I decide")
    m.corpus.withdraw(old["corpus_id"], actor="user", reason="out of date")
    clk.step(hours=6)
    d = m.claims.assert_claim("user", "diagnosis", "demo-deleted-content", scope="health")
    m.claims.delete(d)
    m.context.build("clinic-visit", "agent:clinic-assistant", predicates=["decides", "has", "carries"])
    clk.step(days=1)
    m.claims.confirm(inh)
    m.claims.assert_claim("user", "prefers", "written summaries after appointments", scope="authority", sensitivity="moderate")
    m.claims.assert_claim("user", "decides", "with my partner present", scope="authority", sensitivity="moderate")
    m.context.build("clinic-visit", "agent:clinic-assistant", predicates=["decides", "has", "carries", "prefers"])
    clk.step(days=1)
    m.delegation.grant("agent:coder", "user")
    for i, (path, n) in enumerate([("src/ui/a.py", 12), ("src/ui/table.py", 30), ("src/utils/fmt.py", 18)]):
        m.delegation.submit({"agent": "agent:coder", "kind": "code_change", "changes": [{"path": path, "lines": n}]})
        clk.step(hours=2)
    r = m.delegation.submit({"agent": "agent:coder", "kind": "code_change", "description": "add CSV export",
                             "changes": [{"path": "src/ui/export.py", "lines": 80}]})
    clk.step(hours=1)
    m.delegation.resolve_escalation(r["escalation_id"], "user", positions=[{"position": "approve", "statement": "fine, ship it"}])
    clk.step(hours=5)
    m.delegation.set_condition("build_blocked", True, actor="environment", source="ci")
    m.delegation.submit({"agent": "agent:coder", "kind": "code_change", "emergency": {"condition": "build_blocked"},
                         "description": "fix broken import", "changes": [{"path": "src/ui/a.py", "lines": 2}]})
    m.delegation.set_condition("build_blocked", False, actor="environment", source="ci")
    clk.step(days=1)
    m.delegation.submit({"agent": "agent:coder", "kind": "code_change", "changes": [{"path": "src/auth/b.py", "lines": 3}],
                         "description": "tighten session check"})
    m.delegation.submit({"agent": "agent:coder", "kind": "code_change", "matter": "public-api-v2",
                         "description": "rename public endpoint", "tags": ["public_api"], "deferrable": False,
                         "changes": [{"path": "src/api/routes.py", "lines": 14}]})  # agent flag: ignored + logged (F-02)
    clk.step(days=1)
    # a III.1 conflict on a non-deferrable decision -> CU suspension (propagates; can never be lifted)
    m.delegation.set_condition("security_issue_open", True, actor="environment", source="advisory:token-exposure")
    m.delegation.set_condition("deadline", True, actor="environment", matter="token-exposure-response",
                               source="advisory: exposure window closes")
    r = m.delegation.submit({"agent": "agent:coder", "kind": "code_change", "matter": "token-exposure-response",
                             "description": "rotate leaked signing key",
                             "changes": [{"path": "src/security/tokens.py", "lines": 12}]})
    clk.step(minutes=20)
    m.delegation.resolve_escalation(r["escalation_id"], "user", positions=[
        {"position": "approve", "statement": "rotate the key now"},
        {"position": "reject", "statement": "do not rotate now"}])
    clk.step(hours=2)
    st = new_statement("APPOINT", DEMO_APPOINTER, auditor_id=DEMO_AUDITOR, issued_at=clk.now_iso())
    m.auditors.submit_statement(st, sign_statement(DEMO_KEY[0], st), actor="courier:demo")
    st = new_statement("APPOINT", DEMO_APPOINTER, auditor_id="auditor:demo-2", issued_at=clk.now_iso())
    a2 = m.auditors.submit_statement(st, sign_statement(DEMO_KEY[0], st), actor="courier:demo")
    st = new_statement("REVOKE", DEMO_APPOINTER, appointment_id=a2["appointment_id"])
    m.auditors.submit_statement(st, sign_statement(DEMO_KEY[0], st), actor="courier:demo")
    root = m.delegation.active_grant("agent:coder")
    m.delegation.grant("agent:coder-helper", "agent:coder", parent=root["delegation_id"],
                       limits={"max_lines_per_action": 20, "allowed_kinds": ["code_change"]})
    old = m.delegation.grant("agent:docs-bot", "user", limits={"max_lines_per_action": 15})
    m.delegation.grant("agent:docs-sub", "agent:docs-bot", parent=old["delegation_id"], limits={"max_lines_per_action": 5})
    m.delegation.revoke(old["delegation_id"], "user")
    m.suspensions.record_audit_result("context.ranking", "AUDIT_INDETERMINACY", DEMO_AUDITOR, "demo-audit-1",
                                      evidence_missing=["ranking inputs for one package"])
    m.q1.governance_log()  # an audit read during suspension -> auditlog
    clk.seeding = False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default="/tmp/medb_app_demo.sqlite")
    ap.add_argument("--tokens", default="/tmp/medb_app_demo_tokens.json")
    ap.add_argument("--port", type=int, default=8766)
    a = ap.parse_args()
    import os
    import secrets
    kf = Path(a.db).with_suffix(".appointer.key")
    if not kf.exists():
        fd = os.open(kf, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, "w") as f:
            f.write(secrets.token_bytes(32).hex())
    DEMO_KEY.append(bytes.fromhex(kf.read_text().strip()))
    imports = Path(a.db).with_name("medb_app_demo_imports")
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tests"))
    from integ_fixtures import chrome_profile, write_all  # synthetic samples (no real personal data)
    write_all(imports)
    chrome = Path(a.db).with_name("medb_app_demo_chrome") / "Default"
    if not (chrome / "History").exists():
        chrome_profile(chrome)
    cfg = load_config(overrides={"appointer": {"id": DEMO_APPOINTER, "key_fingerprint": key_fingerprint(DEMO_KEY[0]),
                                               "verify_key_file": str(kf)},
                                 # integrations on for the demo only (off by default; D-72..D-75)
                                 "integrations": {"importers": {"enabled": True, "allowed_roots": [str(imports)]},
                                                  "outbox": {"enabled": True}, "mcp": {"enabled": True},
                                                  # live sync (D-76..D-78): only a local sample Chrome profile is
                                                  # connected; GitHub is enabled but has no OAuth app (no network)
                                                  "sync": {"enabled": True,
                                                           "token_dir": str(Path(a.db).with_name("medb_app_demo_sync_tokens")),
                                                           "clients_file": str(Path(a.db).with_name("medb_app_demo_sync_clients.json")),
                                                           "services": {"chrome_local": {"enabled": True, "profile_path": str(chrome)},
                                                                        "github": {"enabled": True}}}}})
    clk = SeedClock()
    m = MedB(db_path=a.db, clock=clk, config=cfg)
    fresh = not m.claims.state()
    seed_rich(m, clk)
    clk.seeding = False
    if fresh:
        for fmt, scope in (("fhir_r4_bundle", "health"), ("gmail_mbox", "correspondence"), ("chrome_cookies_meta", "browsing")):
            m.perms.grant("ingest", "user", scopes=[scope], sources=[f"import:{fmt}"], sensitivity_max="high")
        m.importer.import_file("health_bundle.json", actor="user", account="patient-portal:demo")
        m.importer.import_file("All mail Including Spam and Trash.mbox", actor="user", account="gmail:demo@example.org")
        m.importer.import_file("Cookies", actor="user", account="chrome:demo-profile")
        try:
            m.importer.import_file("scan.xyz", actor="user")
        except Exception:
            pass  # unknown format: refused and logged (default deny)
        m.perms.grant("ingest", "user", scopes=["browsing"], sources=["sync:chrome_local"], sensitivity_max="high")
        m.sync.connect("chrome_local", actor="user")
        m.sync.sync("chrome_local", actor="user")
        m.outbox.sync()
    tokens = load_tokens(Path(a.tokens), actors=("user", "reader", "agent:coder", DEMO_AUDITOR, "auditor:demo-2",
                                                 "agent:assistant", "inference:assistant"))
    srv = make_server(m, tokens, "127.0.0.1", a.port)
    user = next(t for t, actor in tokens.items() if actor == "user")
    aud = next(t for t, actor in tokens.items() if actor == DEMO_AUDITOR)
    print(f"MedB app (demo DB {a.db}): http://127.0.0.1:{srv.server_port}/app/#token={user}", flush=True)
    print(f"Auditor ({DEMO_AUDITOR}): http://127.0.0.1:{srv.server_port}/app/#token={aud}&go=/auditor", flush=True)
    srv.serve_forever()


if __name__ == "__main__":
    main()
