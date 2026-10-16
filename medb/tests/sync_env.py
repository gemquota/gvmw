"""Shared builders for live-sync tests."""
import json
import socket
import urllib.request
from urllib.parse import parse_qs, urlencode, urlparse

from conftest import appointer_config
from integ_fixtures import chrome_profile, firefox_profile  # noqa: F401  (live browser profiles)
from medb.system import MedB
from medb.util import FixedClock
from sync_fakes import CLIENTS

ALL = ("google_gmail", "google_calendar", "google_contacts", "github", "chrome_local", "firefox_local")


def free_port():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    p = s.getsockname()[1]
    s.close()
    return p


def make(tmp_path, akf, fake, services=ALL, grant=True, clients=True, **sync_over):
    cfg = appointer_config(akf)
    sc = cfg["integrations"]["sync"]
    sc.update(enabled=True, token_dir=str(tmp_path / "tokens"), clients_file=str(tmp_path / "clients.json"), **sync_over)
    for s in services:
        sc["services"][s]["enabled"] = True
    if "chrome_local" in services:
        sc["services"]["chrome_local"]["profile_path"] = str(chrome_profile(tmp_path / "chrome" / "Default"))
    if "firefox_local" in services:
        sc["services"]["firefox_local"]["profile_path"] = str(firefox_profile(tmp_path / "firefox" / "abc.default"))
    cfg["integrations"]["outbox"]["enabled"] = True
    if clients:
        (tmp_path / "clients.json").write_text(json.dumps(CLIENTS))
    m = MedB(db_path=str(tmp_path / "db.sqlite"), clock=FixedClock("2026-10-01T00:00:00Z"), seed=11, config=cfg,
             components={"sync_transport": fake})
    if grant:
        m.perms.grant("ingest", "user", scopes=["*"], sources=["*"], sensitivity_max="high")
    return m


def browser_redirect(auth_url, code, state=None, port=None, error=None):
    """Play the user's browser: follow the provider's redirect back to MedB's loopback listener."""
    q = parse_qs(urlparse(auth_url).query)
    redirect = q["redirect_uri"][0]
    args = {"state": state if state is not None else q["state"][0]}
    if error:
        args["error"] = error
    else:
        args["code"] = code
    url = redirect.replace("localhost", "127.0.0.1") + "?" + urlencode(args)
    with urllib.request.urlopen(url, timeout=5) as r:
        return r.status


def connect_google(m, fake):
    r = m.sync.connect("google_gmail", actor="user")
    fake.challenge = parse_qs(urlparse(r["auth_url"]).query)["code_challenge"][0]
    browser_redirect(r["auth_url"], "auth-code-xyz")
    for _ in range(50):
        out = m.sync.connect_poll("google_gmail", actor="user")
        if not out.get("pending"):
            return r, out
        import time
        time.sleep(0.05)
    raise AssertionError("google connect did not complete")


def connect_github(m):
    r = m.sync.connect("github", actor="user")
    while True:
        out = m.sync.connect_poll("github", actor="user")
        if not out.get("pending"):
            return r, out


def synced(m, service=None):
    return [it for it in m.corpus.items().values()
            if (it.get("provenance") or {}).get("sync") and (service is None or it["provenance"]["service"] == service)]
