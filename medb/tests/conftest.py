import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import hashlib  # noqa: E402

from medb.auditors import key_fingerprint, new_statement, sign_statement  # noqa: E402
from medb.system import MedB, load_config  # noqa: E402
from medb.util import FixedClock  # noqa: E402


@pytest.fixture
def clock():
    return FixedClock("2026-08-01T00:00:00Z")


TEST_APPOINTER = "appointer:test-outside-party"
TEST_APPOINTER_KEY = hashlib.sha256(b"medb-test-appointer").digest()


@pytest.fixture(scope="session")
def appointer_key_file(tmp_path_factory):
    p = tmp_path_factory.mktemp("appointer") / "appointer.key"
    p.write_text(TEST_APPOINTER_KEY.hex())
    return str(p)


def appointer_config(key_file: str) -> dict:
    return load_config(overrides={"appointer": {"id": TEST_APPOINTER, "key_fingerprint": key_fingerprint(TEST_APPOINTER_KEY),
                                                "verify_key_file": key_file}})


def appoint(m, auditor_id="auditor:t1", carrier="courier", key=TEST_APPOINTER_KEY, **kw):
    """Act as the independent appointer: sign an APPOINT statement and submit it."""
    st = new_statement("APPOINT", TEST_APPOINTER, auditor_id=auditor_id, issued_at=m.clock.now_iso(), **kw)
    return m.auditors.submit_statement(st, sign_statement(key, st), actor=carrier)


@pytest.fixture
def m(clock, appointer_key_file):
    return MedB(clock=clock, seed=7, config=appointer_config(appointer_key_file))


@pytest.fixture
def auditor(m):
    appoint(m, "auditor:t1")
    return "auditor:t1"


@pytest.fixture
def agent(m):
    m.delegation.grant("agent:coder", "user")
    return "agent:coder"


def change(agent, path="src/ui/a.py", lines=10, **kw):
    a = {"agent": agent, "kind": "code_change", "changes": [{"path": path, "lines": lines}]}
    a.update(kw)
    return a


def gov_kinds(m):
    return [e["kind"] for e in m.gov.entries()]


@pytest.fixture(autouse=True)
def _no_network(monkeypatch):
    """Tests never leave the machine (F-13 anchoring is always mocked); loopback
    (the API tests' own server) is allowed."""
    import socket
    import urllib.request
    from urllib.parse import urlparse

    real_urlopen, real_conn = urllib.request.urlopen, socket.create_connection
    loop = ("127.0.0.1", "localhost", "::1")

    def urlopen(req, *a, **kw):
        url = req.full_url if hasattr(req, "full_url") else req
        if urlparse(url).hostname not in loop:
            raise AssertionError(f"external network access attempted in tests: {url}")
        return real_urlopen(req, *a, **kw)

    def create_connection(address, *a, **kw):
        if address[0] not in loop:
            raise AssertionError(f"external network access attempted in tests: {address}")
        return real_conn(address, *a, **kw)
    monkeypatch.setattr(urllib.request, "urlopen", urlopen)
    monkeypatch.setattr(socket, "create_connection", create_connection)
