"""D-76: the live_sync outbound class -- strict per-provider HTTPS allowlist, refused before connecting."""
import socket

import pytest

from medb import netscan
from medb.integrations import oauth
from medb.integrations.sync_http import ALLOWED_HOSTS, HostNotAllowed, SyncHttp, SyncHttpError, check_url
from sync_env import make
from sync_fakes import Fake


def never(*a, **kw):
    raise AssertionError("transport must not be called for a refused URL")


@pytest.mark.parametrize("prov,url", [
    ("google", "http://gmail.googleapis.com/gmail/v1/users/me/profile"),      # not HTTPS
    ("google", "https://evil.example/x"),                                       # not on any allowlist
    ("google", "https://api.github.com/user"),                                  # another provider's host
    ("github", "https://gmail.googleapis.com/x"),
    ("github", "https://api.github.com.evil.example/user"),                     # suffix trick
    ("github", "https://evil.example@api.github.com/user"),                     # userinfo
    ("facebook", "https://graph.facebook.com/me"),                              # Facebook removed (D-79)
    ("github", "https://api.github.com:8443/user"),                             # non-standard port
    ("github", "ftp://api.github.com/user"),
    ("nosuch", "https://api.github.com/user"),                                  # unknown provider
    ("google", "https://127.0.0.1/token"),
])
def test_refused_before_any_connection(prov, url, monkeypatch):
    opened = []
    monkeypatch.setattr(socket, "create_connection", lambda *a, **k: opened.append(a) or (_ for _ in ()).throw(AssertionError))
    monkeypatch.setattr(socket.socket, "connect", lambda *a, **k: opened.append(a))
    with pytest.raises(HostNotAllowed):
        check_url(prov, url)
    with pytest.raises(HostNotAllowed):
        SyncHttp(never).request(prov, "GET", url)
    with pytest.raises(HostNotAllowed):
        SyncHttp().request(prov, "GET", url)  # the real HTTPS transport: still refused before a socket exists
    assert opened == []


def test_allowlist_is_fixed_and_https_only():
    assert ALLOWED_HOSTS == {
        "google": ("accounts.google.com", "oauth2.googleapis.com", "gmail.googleapis.com", "www.googleapis.com",
                   "people.googleapis.com"),
        "github": ("github.com", "api.github.com")}
    assert not any("facebook" in h for hs in ALLOWED_HOSTS.values() for h in hs)  # D-79
    for prov, hosts in ALLOWED_HOSTS.items():
        for h in hosts:
            check_url(prov, f"https://{h}/x")
    # every OAuth endpoint MedB uses is on its provider's allowlist
    for prov, url in (("google", oauth.GOOGLE_AUTH), ("google", oauth.GOOGLE_TOKEN), ("google", oauth.GOOGLE_REVOKE),
                      ("github", oauth.GITHUB_DEVICE), ("github", oauth.GITHUB_TOKEN)):
        check_url(prov, url)


def test_params_cannot_smuggle_a_host():
    seen = []
    SyncHttp(lambda *a: seen.append(a[1]) or (200, {}, b"{}")).request("github", "GET", "https://api.github.com/user",
                                                                      params={"x": "https://evil.example/"})
    assert seen and seen[0].startswith("https://api.github.com/user?")


def test_redirects_are_not_followed():
    calls = []

    def t(method, url, headers, body, timeout):
        calls.append(url)
        return 302, {"location": "https://evil.example/"}, b""
    with pytest.raises(SyncHttpError) as e:
        SyncHttp(t).request("github", "GET", "https://api.github.com/user")
    assert e.value.status == 302 and calls == ["https://api.github.com/user"]


def test_token_only_in_authorization_header():
    seen = []
    SyncHttp(lambda m, u, h, b, t: seen.append((u, h, b)) or (200, {}, b"{}")).request(
        "github", "GET", "https://api.github.com/user", token="SEKRIT")
    u, h, b = seen[0]
    assert h["Authorization"] == "Bearer SEKRIT" and "SEKRIT" not in u and b is None


def test_netscan_reports_enabled_services_and_hosts(tmp_path, appointer_key_file):
    m = make(tmp_path, appointer_key_file, Fake(), services=("github", "google_calendar"))
    net = m.q1.self_description()["network"]
    e = {x["module"]: x for x in net["modules_with_network_code"]}["medb.integrations.sync_http"]
    assert e["enabled"] is True and e["services_enabled"] == ["github", "google_calendar"]
    assert e["hosts_in_use"] == sorted(ALLOWED_HOSTS["github"] + ALLOWED_HOSTS["google"])
    assert net["outbound_enabled"] is True and e["class"] == "live_sync"
    integ = m.q1.self_description()["integrations"]["live_sync"]
    assert integ["enabled"] is True and integ["hosts_in_use"] == e["hosts_in_use"] and integ["https_only"] is True


def test_default_config_reaches_no_host(m):
    assert m.sync.enabled is False and m.sync.hosts_in_use() == []
    assert all(not v["enabled"] for v in m.sync.status().values())
    assert netscan.network_profile(m)["outbound_enabled"] is False
