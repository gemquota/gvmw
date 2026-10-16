"""D-68: self_description reports network code generated from the code and config."""
from pathlib import Path

from medb import netscan
from medb.system import MedB, load_config
from medb.util import FixedClock


def test_scanner_detects_top_level_local_and_from_imports():
    src = ("import json\nfrom urllib.parse import urlparse\nimport socket as s\n"
           "def f():\n    import urllib.request\n    from http import client\n    from urllib import request\n")
    assert netscan.network_imports(src) == ["http.client", "socket", "urllib.request"]
    assert netscan.network_imports("from urllib.parse import quote\nimport hashlib\n") == []


def test_self_description_network_profile(m):
    net = m.q1.self_description()["network"]
    mods = {e["module"]: e for e in net["modules_with_network_code"]}
    assert set(mods) == {"medb.anchoring", "medb.api", "medb.integrations.outbox", "medb.integrations.mcp_server",
                 "medb.integrations.sync_http", "medb.integrations.oauth"}
    # the only outbound (off-machine) network code: RFC 3161 anchoring and live account sync (D-76), both off
    assert sorted(net["outbound_modules"]) == ["medb.anchoring", "medb.integrations.sync_http"]
    assert net["inbound_modules"] == ["medb.api"]
    # D-73/D-74: loopback-only clients, off by default
    assert sorted(net["loopback_modules"]) == ["medb.integrations.mcp_server", "medb.integrations.oauth",
                                               "medb.integrations.outbox"]
    o = mods["medb.integrations.oauth"]  # D-77: one-shot OAuth redirect listener, 127.0.0.1 only
    assert o["allowed_hosts"] == ["127.0.0.1"] and o["enabled"] is False and o["outbound"] is False
    s = mods["medb.integrations.sync_http"]
    assert s["class"] == "live_sync" and s["enabled"] is False and s["default_enabled"] is False
    assert s["services_enabled"] == [] and s["hosts_in_use"] == [] and "HTTPS only" in s["protocol"]
    assert s["allowed_hosts"]["github"] == ["github.com", "api.github.com"]
    for mod in ("medb.integrations.mcp_server", "medb.integrations.outbox"):
        assert mods[mod]["allowed_hosts"] == ["127.0.0.1", "::1"] and mods[mod]["enabled"] is False
        assert mods[mod]["outbound"] is False and mods[mod]["sends_content"] is False
    assert net["undeclared"] == []
    a = mods["medb.anchoring"]
    assert a["imports"] == ["urllib.request"] and a["direction"] == "outbound"
    assert "RFC 3161" in a["protocol"] and a["sends_content"] is False
    assert (a["enabled"], a["default_enabled"], a["method"]) == (False, False, "rfc3161")
    assert net["outbound_enabled"] is False
    assert mods["medb.api"]["bind_hosts"] == ["127.0.0.1"] and mods["medb.api"]["outbound"] is False


def test_profile_tracks_running_config():
    cfg = load_config(overrides={"anchoring": {"enabled": True, "tsa_url": "https://tsa.example/"}})
    m = MedB(clock=FixedClock("2026-08-01T00:00:00Z"), seed=7, config=cfg)
    a = {e["module"]: e for e in m.q1.self_description()["network"]["modules_with_network_code"]}["medb.anchoring"]
    assert a["enabled"] is True and a["tsa_url"] == "https://tsa.example/" and a["default_enabled"] is False
    assert m.q1.self_description()["network"]["outbound_enabled"] is True


def test_every_networked_module_in_package_is_declared():
    """Adding network code anywhere in medb without a NETWORK_DECLARATION is caught."""
    found = netscan.scan_package()
    assert set(found) == {"medb.anchoring", "medb.api", "medb.integrations.outbox", "medb.integrations.mcp_server",
                 "medb.integrations.sync_http", "medb.integrations.oauth"}
    import importlib
    for mod in found:
        assert isinstance(getattr(importlib.import_module(mod), "NETWORK_DECLARATION", None), dict), mod


def test_undeclared_network_module_is_reported(tmp_path, monkeypatch, m):
    pkg = tmp_path / "medb"
    pkg.mkdir()
    (pkg / "sneaky.py").write_text("def f():\n    import socket\n")
    assert netscan.scan_package(pkg) == {"medb.sneaky": ["socket"]}


def test_self_description_has_no_hand_written_network_string(m):
    assert isinstance(m.q1.self_description()["network"], dict)
    src = (Path(netscan.__file__).parent / "query.py").read_text()
    assert "no network code in substrate" not in src
