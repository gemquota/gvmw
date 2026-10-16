"""D-76..D-78: live account sync -- OAuth flows, incremental/idempotent sync, provenance, deletions,
tokens never leak, user-only, suspension, scheduler. Fake providers only (no sockets off-machine)."""
import json
import os
import stat
import tempfile
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import pytest

from integ_fixtures import COOKIE_NAME, COOKIE_SECRET
from medb.errors import CapabilitySuspended, NotAuthorized, PermissionDenied
from medb.integrations.livesync import SERVICES, SyncDisabled, SyncRefused, SyncScheduler
from medb.interfaces import interface_inventory
from sync_env import ALL, browser_redirect, connect_github, connect_google, make, synced
from sync_fakes import ACCESS, SECRETS, Fake, raw_mail

PROV_KEYS = {"sync", "service", "provider", "account_id", "endpoint", "remote_id", "version", "run_id",
             "response_sha256", "supersedes_corpus_id", "third_party_content"}


@pytest.fixture
def fake():
    return Fake()


@pytest.fixture
def ms(tmp_path, appointer_key_file, fake):
    return make(tmp_path, appointer_key_file, fake)


# ------------------------------------------------------------------ off by default / opt-in
def test_off_by_default(m):
    for s in SERVICES:
        with pytest.raises(SyncDisabled):
            m.sync.connect(s, actor="user")
    assert {e["body"]["reason"] for e in m.gov.entries(kinds=["SYNC_REFUSED"])} == {"service_disabled"}
    assert m.q1.self_description()["integrations"]["live_sync"]["enabled"] is False


def test_per_service_opt_in(tmp_path, appointer_key_file, fake):
    m = make(tmp_path, appointer_key_file, fake, services=("github",))
    with pytest.raises(SyncDisabled):
        m.sync.connect("google_gmail", actor="user")
    assert m.sync.connect("github", actor="user")["mode"] == "device"
    assert m.sync.hosts_in_use() == ["api.github.com", "github.com"]


def test_client_registration_required(tmp_path, appointer_key_file, fake):
    m = make(tmp_path, appointer_key_file, fake, clients=False)
    with pytest.raises(SyncDisabled) as e:
        m.sync.connect("google_gmail", actor="user")
    assert e.value.reason == "oauth_client_not_configured" and fake.calls == []


# ------------------------------------------------------------------ OAuth flows
def test_google_loopback_pkce(ms, fake, tmp_path):
    r, out = connect_google(ms, fake)
    q = parse_qs(urlparse(r["auth_url"]).query)
    assert urlparse(r["auth_url"]).hostname == "accounts.google.com"
    assert q["code_challenge_method"] == ["S256"] and q["redirect_uri"][0].startswith("http://127.0.0.1:")
    assert set(q["scope"][0].split()) == {"https://www.googleapis.com/auth/gmail.readonly",
                                          "https://www.googleapis.com/auth/calendar.readonly",
                                          "https://www.googleapis.com/auth/contacts.readonly", "openid", "email"}
    assert out["connected"] and out["account_id"] == "google:gem@example.com"
    f = tmp_path / "tokens" / "google.json"
    assert stat.S_IMODE(f.stat().st_mode) == 0o600 and stat.S_IMODE(f.parent.stat().st_mode) == 0o700
    assert json.loads(f.read_text())["access_token"] == ACCESS["google"]
    for s in ("google_gmail", "google_calendar", "google_contacts"):  # one Google account serves all three
        assert ms.sync.status()[s]["connected"]


def test_google_state_mismatch_refused(ms, fake):
    r = ms.sync.connect("google_gmail", actor="user")
    browser_redirect(r["auth_url"], "auth-code-xyz", state="forged")
    import time
    for _ in range(50):
        try:
            if not ms.sync.connect_poll("google_gmail", actor="user").get("pending"):
                break
        except SyncRefused as e:
            assert e.reason == "oauth_denied"
            break
        time.sleep(0.05)
    else:
        raise AssertionError("no result")
    assert ms.sync.tokens.get("google") is None
    assert not any(c[2] == "/token" for c in fake.calls)  # code never exchanged


def test_non_read_only_scope_refused(ms, fake):
    fake.granted_google_scope += " https://www.googleapis.com/auth/gmail.modify"
    with pytest.raises(SyncRefused) as e:
        connect_google(ms, fake)
    assert e.value.reason == "scope_not_read_only" and ms.sync.tokens.get("google") is None


def test_github_device_flow(ms, fake):
    r = ms.sync.connect("github", actor="user")
    assert (r["mode"], r["user_code"], r["verification_uri"]) == ("device", "WDJB-MJHT", "https://github.com/login/device")
    assert "device_code" not in json.dumps(r)
    assert ms.sync.connect_poll("github", actor="user")["pending"] is True
    out = ms.sync.connect_poll("github", actor="user")
    assert out["connected"] and out["account_id"] == "github:gemq:42" and out["scopes"] == ["read:user"]


def test_github_extra_scope_refused(ms, fake):
    fake.github_scope = "read:user,repo,delete_repo"
    with pytest.raises(SyncRefused) as e:
        connect_github(ms)
    assert e.value.reason == "scope_not_read_only"


# ------------------------------------------------------------------ grant + provenance + idempotence
def test_sync_requires_ingest_grant(tmp_path, appointer_key_file, fake):
    m = make(tmp_path, appointer_key_file, fake, grant=False)
    connect_github(m)
    n = len(fake.calls)
    with pytest.raises(PermissionDenied):
        m.sync.sync("github", actor="user")
    assert len(fake.calls) == n  # refused before any API call
    m.perms.grant("ingest", "user", scopes=["code"], sources=["sync:github"], sensitivity_max="moderate")
    with pytest.raises(PermissionDenied):  # synced items are sensitivity high
        m.sync.sync("github", actor="user")
    m.perms.grant("ingest", "user", scopes=["code"], sources=["sync:github"], sensitivity_max="high")
    assert m.sync.sync("github", actor="user")["ok"]


def test_gmail_incremental_idempotent_deletions(ms, fake):
    connect_google(ms, fake)
    r1 = ms.sync.sync("google_gmail", actor="user")
    assert (r1["ingested"], r1["ok"]) == (2, True)
    items = synced(ms, "google_gmail")
    for it in items:
        p = it["provenance"]
        assert PROV_KEYS <= set(p) and it["sensitivity"] == "high" and it["source"] == "sync:google_gmail"
        assert p["endpoint"].startswith("gmail/v1/users/me/messages/") and len(p["response_sha256"]) == 64
        assert p["account_id"] == "google:gem@example.com" and p["run_id"] == r1["run_id"]
        assert it["media_type"] == "message/rfc822" and p["details"]["mail"]["from"].startswith("Dr Lee")
    # re-sync with no remote changes: history call, nothing new
    r2 = ms.sync.sync("google_gmail", actor="user")
    assert (r2["ingested"], r2["unchanged"]) == (0, 0) and len(synced(ms, "google_gmail")) == 2
    assert any(c[2].endswith("/history") and c[3]["startHistoryId"] == "200" for c in fake.calls)
    # remote: one new message, one deleted
    fake.mail["g3"], fake.mail_hist["g3"] = raw_mail(3), "201"
    fake.history = [{"messagesAdded": [{"message": {"id": "g3"}}]}, {"messagesDeleted": [{"message": {"id": "g1"}}]}]
    fake.history_id = "300"
    del fake.mail["g1"]
    r3 = ms.sync.sync("google_gmail", actor="user")
    assert (r3["ingested"], r3["remote_deletions"]) == (1, 1)
    assert not any(it["withdrawn"] for it in synced(ms))  # no erasure, no auto-withdraw (F-32)
    dels = ms.sync.events("google_gmail", kinds=["REMOTE_DELETION"])
    assert len(dels) == 1 and dels[0]["body"]["remote_id"] == "g1"
    feed = ms.outbox.sync()
    assert [n["event"] for n in feed if n["event"].startswith("SYNC_")] == ["SYNC_REMOTE_DELETION"]
    # history id too old -> full resync, still no duplicates; deletion not re-reported
    fake.history_404 = True
    r4 = ms.sync.sync("google_gmail", actor="user")
    assert r4["ok"] and r4["ingested"] == 0 and r4["unchanged"] == 2 and len(synced(ms, "google_gmail")) == 3


def test_calendar_sync_token_versions_and_410(ms, fake):
    connect_google(ms, fake)
    r1 = ms.sync.sync("google_calendar", actor="user")
    assert r1["ingested"] == 2
    first = {it["provenance"]["remote_id"]: it for it in synced(ms, "google_calendar")}
    assert "Attendees: lee@clinic.example" in ms.store.get_content(first["e1"]["content_ref"])["content"]
    assert first["e1"]["provenance"]["third_party_content"] is True
    # delta: e1 changed (new etag), e2 cancelled
    fake.cal_delta = [dict(fake.events["e1"], etag='"2"', summary="Asthma review (moved)"),
                      {"id": "e2", "status": "cancelled"}]
    r2 = ms.sync.sync("google_calendar", actor="user")
    assert (r2["updated"], r2["remote_deletions"], r2["ingested"]) == (1, 1, 0)
    newest = [it for it in synced(ms, "google_calendar") if it["provenance"]["version"] == '"2"'][0]
    assert newest["provenance"]["supersedes_corpus_id"] == first["e1"]["corpus_id"]
    assert any(c[3].get("syncToken") == "cal-s1" for c in fake.calls)
    # expired sync token -> full resync, idempotent
    fake.cal_410, fake.events["e1"]["etag"] = True, '"2"'
    r3 = ms.sync.sync("google_calendar", actor="user")
    assert r3["ok"] and r3["ingested"] == 0 and r3["updated"] == 0 and len(synced(ms, "google_calendar")) == 3


def test_contacts_sync(ms, fake):
    connect_google(ms, fake)
    assert ms.sync.sync("google_contacts", actor="user")["ingested"] == 1
    fake.people_delta = [{"resourceName": "people/c1", "metadata": {"deleted": True}},
                         {"resourceName": "people/c2", "etag": "p9", "names": [{"displayName": "Pharmacy"}]}]
    r = ms.sync.sync("google_contacts", actor="user")
    assert (r["ingested"], r["remote_deletions"]) == (1, 1)
    assert all(it["provenance"]["third_party_content"] for it in synced(ms, "google_contacts"))


def test_github_sync(ms, fake):
    connect_github(ms)
    r1 = ms.sync.sync("github", actor="user")
    kinds = sorted(it["provenance"]["remote_id"].split(":")[0] for it in synced(ms, "github"))
    assert kinds == ["event", "issue", "repo", "repo", "repo", "star", "user"]  # repos across 2 Link pages
    assert r1["third_party"] == 1  # the issue was opened by someone else
    r2 = ms.sync.sync("github", actor="user")
    assert (r2["ingested"], r2["updated"]) == (0, 0) and len(synced(ms, "github")) == 7
    ev_calls = [c for c in fake.calls if c[2] == "/users/gemq/events"]
    assert ev_calls[-1][4].get("If-None-Match") == 'W/"ev1"'  # conditional request -> 304
    assert [c for c in fake.calls if c[2] == "/issues"][-1][3]["since"] == "2026-09-02T00:00:00Z"
    fake.repos[0]["pushed_at"] = "2026-09-30T00:00:00Z"
    assert ms.sync.sync("github", actor="user")["updated"] == 1


def test_pagination_link_off_allowlist_refused(ms, fake):
    """A provider's 'next page' link is re-checked against the allowlist before connecting; cursor not advanced."""
    connect_github(ms)
    assert ms.sync.sync("github", actor="user")["ok"]
    before = ms.sync.cursor("github")
    fake.repos_next = "https://evil.example/steal?access_token=" + ACCESS["github"]
    fake.repos[0]["pushed_at"] = "2026-09-30T00:00:00Z"
    r = ms.sync.sync("github", actor="user")
    assert r["ok"] is False and "HostNotAllowed" in r["error"] and ACCESS["github"] not in r["error"]
    assert "evil.example" not in fake.hosts() and ms.sync.cursor("github") == before
    assert any(n["event"] == "SYNC_FAILED" for n in ms.outbox.sync())


def test_truncated_run_does_not_advance_cursor(tmp_path, appointer_key_file, fake):
    m = make(tmp_path, appointer_key_file, fake, max_items_per_run=1)
    connect_google(m, fake)
    r = m.sync.sync("google_gmail", actor="user")
    assert r["truncated"] and r["ingested"] == 1 and m.sync.cursor("google_gmail") is None
    r = m.sync.sync("google_gmail", actor="user")
    assert r["ingested"] == 1 and r["unchanged"] == 1 and not r["truncated"]
    assert m.sync.cursor("google_gmail") == {"history_id": "200"}


def test_token_refresh(ms, fake):
    connect_google(ms, fake)
    ms.clock.advance(hours=2)
    assert ms.sync.sync("google_contacts", actor="user")["ok"]
    assert any(c[5].get("grant_type") == "refresh_token" for c in fake.calls)


# ------------------------------------------------------------------ local browsers, live
def test_chrome_live_profile_cookie_metadata_only(ms, tmp_path, monkeypatch):
    made = []
    real = tempfile.mkdtemp
    monkeypatch.setattr(tempfile, "mkdtemp", lambda **kw: made.append(real(**kw)) or made[-1])
    prof = Path(ms.sync.svc_cfg("chrome_local")["profile_path"])
    before = {p: p.read_bytes() for p in prof.rglob("*") if p.is_file()}
    assert ms.sync.connect("chrome_local", actor="user")["account_id"] == "local:Default"
    r = ms.sync.sync("chrome_local", actor="user")
    assert r["ingested"] == 5  # 2 visits, 1 bookmark, 2 cookie domains
    assert made and not any(Path(d).exists() for d in made)  # temp copy removed
    assert {p: p.read_bytes() for p in prof.rglob("*") if p.is_file()} == before  # profile untouched
    bank = [it for it in synced(ms, "chrome_local") if it["provenance"]["remote_id"] == "cookies:bank.example"][0]
    assert bank["provenance"]["details"]["cookie_meta"] == {"domain": "bank.example", "count": 2,
                                                            "first_seen": bank["provenance"]["details"]["cookie_meta"]["first_seen"],
                                                            "last_seen": bank["provenance"]["details"]["cookie_meta"]["last_seen"],
                                                            "values_imported": False}
    assert ms.sync.sync("chrome_local", actor="user")["ingested"] == 0  # idempotent
    import sqlite3
    con = sqlite3.connect(prof / "History")
    con.execute("INSERT INTO urls VALUES(3,'https://pharmacy.example/','Pharmacy',1,13370000200000000)")
    con.commit(); con.close()
    r = ms.sync.sync("chrome_local", actor="user")
    assert r["ingested"] == 1 and r["unchanged"] >= 3
    _assert_absent(ms, tmp_path, [COOKIE_SECRET, COOKIE_NAME])


def test_firefox_live_profile(ms, tmp_path):
    ms.sync.connect("firefox_local", actor="user")
    r = ms.sync.sync("firefox_local", actor="user")
    assert r["ingested"] == 3  # 1 visited place, 1 bookmark, 1 cookie domain
    assert ms.sync.sync("firefox_local", actor="user")["ingested"] == 0
    _assert_absent(ms, tmp_path, [COOKIE_SECRET, COOKIE_NAME])


def test_local_connect_needs_profile(tmp_path, appointer_key_file, fake):
    m = make(tmp_path, appointer_key_file, fake)
    m.sync.config["services"]["chrome_local"]["profile_path"] = str(tmp_path / "nope")
    with pytest.raises(SyncRefused):
        m.sync.connect("chrome_local", actor="user")


# ------------------------------------------------------------------ tokens never leak
def _assert_absent(m, tmp_path, secrets, extra=()):
    from medb.export import export
    m.outbox.sync()
    out = tmp_path / f"exp-{len(list(tmp_path.glob('exp-*')))}"
    export(m, out, actor="user")
    m.store.db.commit()
    blobs = [p.read_bytes() for p in tmp_path.glob("db.sqlite*")]
    rows = m.store.db.execute("SELECT body FROM content").fetchall() + m.store.db.execute("SELECT body FROM events").fetchall()
    blobs.append(json.dumps([r[0] for r in rows]).encode())
    blobs += [p.read_bytes() for p in out.rglob("*") if p.is_file()]
    blobs.append(json.dumps(m.gov.entries()).encode())
    blobs.append(json.dumps(m.q1.self_description()).encode())
    blobs.append(json.dumps(m.sync.status()).encode())
    blobs.append(json.dumps(m.outbox.feed()).encode())
    blobs.append(json.dumps(m.config).encode())
    blobs += [x.encode() if isinstance(x, str) else x for x in extra]
    for b in blobs:
        for s in secrets:
            assert s.encode() not in b, s


def test_planted_tokens_appear_nowhere(ms, fake, tmp_path, capsys, caplog):
    connect_google(ms, fake)
    connect_github(ms)
    for s in ("google_gmail", "google_calendar", "google_contacts", "github"):
        assert ms.sync.sync(s, actor="user")["ok"], s
    ms.clock.advance(hours=2)
    ms.sync.sync("google_contacts", actor="user")  # refresh path too
    fake.repos_next = "https://evil.example/x?access_token=" + ACCESS["github"]
    fake.repos[0]["pushed_at"] = "2026-09-30T00:00:00Z"
    ms.sync.sync("github", actor="user")  # error path
    # the tokens really are on disk (so the check below is meaningful), 0600
    assert ACCESS["github"] in (tmp_path / "tokens" / "github.json").read_text()
    cap = capsys.readouterr()
    _assert_absent(ms, tmp_path, SECRETS, extra=[cap.out, cap.err, caplog.text])
    assert all(SyncRefused.__name__ not in json.dumps(v) for v in ms.sync.status().values())


# ------------------------------------------------------------------ disconnect
def test_disconnect_deletes_token(ms, fake, tmp_path):
    connect_google(ms, fake)
    out = ms.sync.disconnect("google_calendar", actor="user", remote_revoke=True)
    assert out["token_deleted"] and out["remote_revoke"] == "revoked"
    assert set(out["services"]) == {"google_gmail", "google_calendar", "google_contacts"}
    assert not (tmp_path / "tokens" / "google.json").exists()
    assert [c for c in fake.calls if c[2] == "/revoke"][0][5]["token"]  # sent in the form body only
    with pytest.raises(SyncRefused):
        ms.sync.sync("google_gmail", actor="user")
    connect_github(ms)
    assert "manual" in ms.sync.disconnect("github", actor="user", remote_revoke=True)["remote_revoke"]
    _assert_absent(ms, tmp_path, SECRETS)


# ------------------------------------------------------------------ assistants and others: never
@pytest.mark.parametrize("actor", ["agent:coder", "agent:assistant", "inference:assistant", "reader", "auditor:t1",
                                   "mcp", "system"])
def test_only_user_connects_and_disconnects(ms, fake, actor):
    for s in ("google_gmail", "github", "chrome_local"):
        with pytest.raises(NotAuthorized):
            ms.sync.connect(s, actor=actor)
        with pytest.raises(NotAuthorized):
            ms.sync.connect_poll(s, actor=actor)
        with pytest.raises(NotAuthorized):
            ms.sync.disconnect(s, actor=actor)
    assert fake.calls == []


@pytest.mark.parametrize("actor", ["agent:coder", "agent:assistant", "inference:assistant", "reader", "auditor:t1", "mcp"])
def test_only_user_or_schedule_syncs(ms, fake, actor):
    connect_github(ms)
    n = len(fake.calls)
    with pytest.raises(NotAuthorized):
        ms.sync.sync("github", actor=actor)
    assert len(fake.calls) == n and not synced(ms)
    assert ms.gov.entries(kinds=["PROHIBITED_ATTEMPT"])[-1]["body"]["reason"] == "sync_run_requires_user"


# ------------------------------------------------------------------ suspension
@pytest.mark.parametrize("prim", ["integrations.sync", "corpus.ingest"])
def test_suspension_blocks_sync_not_disconnect(ms, fake, prim):
    connect_github(ms)
    ms.suspensions.suspend(prim, "t", "UNDETERMINED", [], ["x"])
    n = len(fake.calls)
    with pytest.raises(CapabilitySuspended):
        ms.sync.sync("github", actor="user")
    if prim == "integrations.sync":
        with pytest.raises(CapabilitySuspended):
            ms.sync.connect("github", actor="user")
    assert len(fake.calls) == n
    assert ms.sync.disconnect("github", actor="user")["token_deleted"]  # revocation plane: always open


def test_inventory(ms):
    inv = interface_inventory()["primitives"]["integrations.sync"]
    assert inv["depends_on"] == ["corpus.ingest"]
    for i in ("SyncManager.connect", "SyncManager.connect_poll", "SyncManager.sync", "SyncManager.disconnect"):
        assert i in inv["interfaces"]
    assert inv["interface_planes"]["SyncManager.disconnect"] == "revocation"
    assert inv["interface_planes"]["SyncManager.sync"] == "capability"
    assert "SyncManager.sync" in interface_inventory()["primitives"]["corpus.ingest"]["interfaces"]


def test_sync_stream_hash_chained_and_mirrored(ms, fake):
    connect_github(ms)
    ms.sync.sync("github", actor="user")
    assert ms.store.verify("sync")["ok"]
    mirrored = [e for e in ms.gov.entries(kinds=["STATE_TRANSITION"]) if e["body"]["stream"] == "sync"]
    assert [e["body"]["event_kind"] for e in mirrored] == ["CONNECT", "RUN"]


# ------------------------------------------------------------------ scheduler
def test_scheduler_off_by_default(ms, fake):
    connect_github(ms)
    assert SyncScheduler(ms.sync).tick() == []


def test_scheduler_interval(ms, fake):
    connect_github(ms)
    ms.sync.config["schedule"] = {"enabled": True, "interval_minutes": 60}
    sch = SyncScheduler(ms.sync)
    out = sch.tick()
    assert [r["service"] for r in out] == ["github"] and out[0]["ok"]
    assert ms.sync.events("github", kinds=["RUN"])[-1]["actor"] == "system"
    assert sch.tick() == []
    ms.clock.advance(minutes=61)
    assert len(sch.tick()) == 1


def test_scheduler_inside_api_loop(ms, fake):
    from medb.api import make_server, serve
    connect_github(ms)
    ms.sync.config["schedule"] = {"enabled": True, "interval_minutes": 60}
    srv = make_server(ms, {"t": "user"}, port=0)
    try:
        serve(srv, ms, ticks=1)
    finally:
        srv.server_close()
    assert ms.sync.events("github", kinds=["RUN"])[-1]["actor"] == "system"


def test_facebook_removed(ms):
    """Gem removed Facebook from live sync (D-79): no service, no hosts, no scopes, refused as unknown."""
    from medb.integrations import oauth
    assert "facebook" not in SERVICES and "facebook" not in oauth.SCOPES
    with pytest.raises(SyncRefused) as e:
        ms.sync.connect("facebook", actor="user")
    assert e.value.reason == "unknown_service"
    sd = ms.q1.self_description()
    assert "facebook" not in json.dumps(sd["integrations"]["live_sync"]).lower()
    assert "facebook" not in json.dumps(sd["network"]).lower()
    # the Facebook *file* importer (your own DYI export, local only) is unaffected
    assert "facebook_json" in sd["integrations"]["importers"]["formats"]
