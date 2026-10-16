"""D-73: local notification outbox and optional loopback-only webhook (off by default)."""
import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

import pytest

from conftest import appointer_config, change
from medb.errors import CapabilitySuspended
from medb.integrations.outbox import loopback_url, post_loopback
from medb.interfaces import interface_inventory
from medb.system import MedB
from medb.util import FixedClock


def make(appointer_key_file, sender=None, **over):
    cfg = appointer_config(appointer_key_file)
    cfg["integrations"]["outbox"].update(enabled=True, **over)
    return MedB(clock=FixedClock("2026-09-20T00:00:00Z"), seed=5, config=cfg,
                components={"outbox_sender": sender} if sender else None)


def provoke(m):
    """One of each notification kind."""
    m.perms.grant("infer", "user", scopes=["health"], sensitivity_max="high")
    c = m.claims.assert_claim("user", "has", "asthma-secret-text", scope="health")
    m.claims.propose("user", "carries", "inhaler-secret-text", scope="health", derived_from=[c], actor="inference:x")
    m.delegation.grant("agent:coder", "user")
    m.delegation.submit(change("agent:coder", path="src/auth/login.py", lines=5))  # critical -> escalation
    m.suspensions.suspend("context.ranking", "t", "UNDETERMINED", [], ["x"])
    m.delegation.set_condition("build_blocked", True, actor="environment")
    m.delegation.submit(change("agent:coder", lines=5, emergency={"condition": "build_blocked"}))
    m.clock.advance(minutes=61)
    m.delegation.check_obligations()


def test_off_by_default(m):
    assert m.outbox.enabled is False
    m.delegation.grant("agent:coder", "user")
    m.delegation.submit(change("agent:coder", path="src/auth/login.py", lines=5))
    assert m.outbox.sync() == [] and "outbox" not in m.store.streams()


def test_notifications_derived_without_content(appointer_key_file):
    m = make(appointer_key_file)
    provoke(m)
    new = m.outbox.sync()
    kinds = {n["event"] for n in new}
    assert kinds == {"INFERENCE_PROPOSED", "ESCALATION_OPENED", "SUSPENSION", "OBLIGATION_BREACHED"}
    feed = m.outbox.feed()
    assert feed["count"] == len(new) and feed["verification"]["ok"]
    blob = json.dumps(feed)
    assert "secret-text" not in blob  # ids and kinds only, never claim content
    esc = next(n for n in new if n["event"] == "ESCALATION_OPENED")
    assert esc["refs"]["escalation_id"] and esc["refs"]["agent"] == "agent:coder"
    assert m.outbox.sync() == []  # idempotent
    # the outbox is not cross-linked into gov (governance-log evidence unperturbed)
    assert not [e for e in m.gov.entries(kinds=["STATE_TRANSITION"]) if e["body"]["stream"] == "outbox"]


def test_obligation_breach_notified(appointer_key_file):
    m = make(appointer_key_file)
    m.delegation.grant("agent:coder", "user")
    m.delegation.set_condition("build_blocked", True, actor="environment")
    m.delegation.submit(change("agent:coder", lines=5, emergency={"condition": "build_blocked"}))
    m.clock.advance(minutes=61)
    assert m.delegation.check_obligations()
    assert "OBLIGATION_BREACHED" in {n["event"] for n in m.outbox.sync()}


def test_event_filter(appointer_key_file):
    m = make(appointer_key_file, events=["SUSPENSION"])
    provoke(m)
    assert {n["event"] for n in m.outbox.sync()} == {"SUSPENSION"}


@pytest.mark.parametrize("url,ok", [("http://127.0.0.1:9/hook", True), ("http://[::1]:9/x", True),
                                    ("http://localhost:9/", False), ("https://127.0.0.1/", False),
                                    ("http://example.org/", False), ("http://10.0.0.1/", False),
                                    ("http://user:pw@127.0.0.1/", False), (None, False), ("", False)])
def test_loopback_only_urls(url, ok):
    assert loopback_url(url) is ok


def test_webhook_off_by_default_even_with_outbox_on(appointer_key_file):
    sent = []
    m = make(appointer_key_file, sender=lambda *a: sent.append(a) or 200)
    provoke(m)
    m.outbox.sync()
    assert sent == [] and m.outbox.webhook()["enabled"] is False


def test_non_loopback_webhook_refused_without_network(appointer_key_file):
    sent = []
    m = make(appointer_key_file, sender=lambda *a: sent.append(a) or 200,
             webhook={"enabled": True, "url": "http://example.org/hook"})
    provoke(m)
    m.outbox.sync()
    assert sent == []
    d = [n["delivery"] for n in m.outbox.feed()["notifications"]]
    assert d and all(x["status"] is None and x["error"].startswith("refused") for x in d)
    with pytest.raises(ValueError):
        post_loopback("http://example.org/", {}, 1)


def test_webhook_posts_to_local_listener(appointer_key_file):
    got = []

    class H(BaseHTTPRequestHandler):
        def do_POST(self):
            got.append(json.loads(self.rfile.read(int(self.headers["Content-Length"]))))
            self.send_response(204)
            self.end_headers()

        def log_message(self, *a):
            pass
    srv = HTTPServer(("127.0.0.1", 0), H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    try:
        m = make(appointer_key_file, webhook={"enabled": True, "url": f"http://127.0.0.1:{srv.server_port}/medb"})
        provoke(m)
        new = m.outbox.sync()
    finally:
        srv.shutdown()
        srv.server_close()
    assert len(got) == len(new) and {g["event"] for g in got} == {n["event"] for n in new}
    assert all(n["delivery"]["status"] == 204 for n in m.outbox.feed()["notifications"])
    assert "secret-text" not in json.dumps(got)


def test_delivery_failure_recorded_not_fatal(appointer_key_file):
    def boom(*a):
        raise ConnectionRefusedError("nobody listening")
    m = make(appointer_key_file, sender=boom, webhook={"enabled": True, "url": "http://127.0.0.1:9/x"})
    provoke(m)
    assert m.outbox.sync()
    assert all("ConnectionRefusedError" in n["delivery"]["error"] for n in m.outbox.feed()["notifications"])


def test_suspended_outbox_refuses_sync(appointer_key_file):
    m = make(appointer_key_file)
    m.suspensions.suspend("integrations.outbox", "t", "UNDETERMINED", [], ["x"])
    with pytest.raises(CapabilitySuspended):
        m.outbox.sync()
    assert m.outbox.feed()["count"] == 0  # the feed (read) stays available


def test_inventory():
    inv = interface_inventory()["primitives"]["integrations.outbox"]
    assert "Outbox.sync" in inv["interfaces"] and inv["depends_on"] == ["governance.log"]
