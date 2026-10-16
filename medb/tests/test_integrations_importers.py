"""D-72: user-only local file importers into the corpus (off by default)."""
import hashlib
import json
import zipfile

import pytest

from conftest import appointer_config
from integ_fixtures import COOKIE_NAME, COOKIE_SECRET, write_all
from medb.errors import CapabilitySuspended, NotAuthorized, PermissionDenied
from medb.integrations import importers as imp
from medb.integrations.importers import ImportRefused, ImportsDisabled
from medb.interfaces import interface_inventory
from medb.system import MedB
from medb.util import FixedClock


@pytest.fixture
def files(tmp_path):
    return write_all(tmp_path / "imports")


@pytest.fixture
def mi(tmp_path, files, appointer_key_file):
    cfg = appointer_config(appointer_key_file)
    cfg["integrations"]["importers"].update(enabled=True, allowed_roots=[str(tmp_path / "imports")])
    m = MedB(db_path=str(tmp_path / "db.sqlite"), clock=FixedClock("2026-09-20T00:00:00Z"), seed=3, config=cfg)
    m.perms.grant("ingest", "user", scopes=["*"], sources=["*"], sensitivity_max="high")
    return m


def items(m):
    return list(m.corpus.items().values())


def test_off_by_default(m, files):
    assert m.importer.enabled is False
    with pytest.raises(ImportsDisabled):
        m.importer.import_file(str(files["note"]), actor="user")
    assert m.gov.entries(kinds=["IMPORT_REFUSED"])[-1]["body"]["reason"] == "importers_disabled"
    assert not m.corpus.items()


@pytest.mark.parametrize("actor", ["agent:coder", "reader", "system", "inference:x", "auditor:t1"])
def test_user_only(mi, files, actor):
    with pytest.raises(NotAuthorized):
        mi.importer.import_file(str(files["fhir"]), actor=actor)
    pa = mi.gov.entries(kinds=["PROHIBITED_ATTEMPT"])[-1]
    assert (pa["actor"], pa["body"]["reason"]) == (actor, "non_user_import")
    assert not mi.corpus.items()


def test_ingest_grant_required_before_reading(tmp_path, files, appointer_key_file, monkeypatch):
    cfg = appointer_config(appointer_key_file)
    cfg["integrations"]["importers"].update(enabled=True, allowed_roots=[str(files["fhir"].parent)])
    m = MedB(clock=FixedClock("2026-09-20T00:00:00Z"), seed=3, config=cfg)
    m.perms.grant("ingest", "user", scopes=["health"], sources=["clinic-letters"], sensitivity_max="high")
    read = []
    monkeypatch.setattr(imp, "file_sha256", lambda p: read.append(p) or ("x", 0))
    with pytest.raises(PermissionDenied):
        m.importer.import_file(str(files["fhir"]), actor="user")  # source import:fhir_r4_bundle not granted
    assert read == [] and not m.corpus.items()
    assert m.gov.entries(kinds=["PROHIBITED_ATTEMPT"])[-1]["body"]["reason"] == "ingest_without_grant"
    # sensitivity is part of the grant check: a moderate-max grant cannot take the default 'high'
    m.perms.grant("ingest", "user", scopes=["health"], sources=["import:fhir_r4_bundle"], sensitivity_max="moderate")
    with pytest.raises(PermissionDenied):
        m.importer.import_file(str(files["fhir"]), actor="user")


def test_fhir_bundle_provenance(mi, files):
    r = mi.importer.import_file(str(files["fhir"]), actor="user", account="patient-portal:gem")
    assert r["format"] == "fhir_r4_bundle" and r["ingested"] == 3
    assert r["skipped"] == {"fhir_Patient_not_imported": 1}
    sha = hashlib.sha256(files["fhir"].read_bytes()).hexdigest()
    its = items(mi)
    assert len(its) == 3
    for it in its:
        p = it["provenance"]
        assert (it["source"], it["scope"], it["sensitivity"], it["media_type"]) == \
            ("import:fhir_r4_bundle", "health", "high", "application/fhir+json")
        assert p["file_sha256"] == sha and p["file_name"] == "health_bundle.json" and p["run_id"] == r["run_id"]
        assert p["source_account"] == "patient-portal:gem" and p["importer"] == imp.IMPORTER_VERSION
        assert p["details"]["fhir"]["subject"] == "Patient/p1" and p["details"]["fhir"]["bundle_id"] == "bundle-1"
        assert p["third_party_content"] is False
    refs = sorted(it["provenance"]["record_ref"] for it in its)
    assert refs == ["Condition/c1", "MedicationStatement/m1", "Observation/o1"]
    obs = next(it for it in its if it["provenance"]["record_ref"] == "Observation/o1")
    assert mi.corpus.content(obs["corpus_id"]).startswith("Observation: Heart rate = 72 beats/minute")
    assert obs["provenance"]["details"]["fhir"]["meta_source"] == "clinic-portal"
    run = mi.gov.entries(kinds=["IMPORT_RUN"])[-1]
    assert run["actor"] == "user" and run["body"]["file_sha256"] == sha and run["body"]["ingested"] == 3
    # every item ingest is mirrored into gov, like any corpus ingest
    mirrored = [e for e in mi.gov.entries(kinds=["STATE_TRANSITION"]) if e["body"]["stream"] == "corpus"]
    assert len(mirrored) == 3
    assert mi.store.verify("corpus")["ok"] and mi.gov.verify()["ok"]


EXPECT = {  # fixture key -> (format, item count, default scope, any third-party)
    "note": ("text_note", 1, "notes", False), "csv": ("csv_rows", 2, "records", False),
    "ndjson": ("ndjson_records", 2, "records", False), "json": ("json_records", 3, "records", False),
    "mbox": ("gmail_mbox", 2, "correspondence", True), "chrome_takeout": ("chrome_history_takeout", 2, "browsing", False),
    "bm_html": ("chrome_bookmarks_html", 2, "browsing", False), "bm_json": ("chrome_bookmarks_json", 2, "browsing", False),
    "ics": ("calendar_ics", 2, "calendar", True), "vcf": ("contacts_vcf", 2, "contacts", True),
    "github": ("github_json", 2, "code", False), "fb_msgs": ("facebook_json", 2, "social", True),
    "fb_posts": ("facebook_json", 1, "social", False), "chrome_sqlite": ("chrome_history_sqlite", 2, "browsing", False),
    "ff_places": ("firefox_places_sqlite", 2, "browsing", False),
    "chrome_cookies": ("chrome_cookies_meta", 2, "browsing", False), "ff_cookies": ("firefox_cookies_meta", 1, "browsing", False),
}


@pytest.mark.parametrize("key", sorted(EXPECT))
def test_formats_detected_and_imported(mi, files, key):
    fmt, n, scope, third = EXPECT[key]
    r = mi.importer.import_file(str(files[key]), actor="user")
    assert (r["format"], r["ingested"], r["scope"], r["source"]) == (fmt, n, scope, f"import:{fmt}")
    assert (r["third_party_items"] > 0) == third
    for it in items(mi):
        assert it["provenance"]["format"] == fmt and it["sensitivity"] == "high"
        assert it["provenance"]["file_sha256"] == hashlib.sha256(files[key].read_bytes()).hexdigest()


def test_content_details(mi, files):
    mi.importer.import_file(str(files["mbox"]), actor="user")
    mi.importer.import_file(str(files["bm_html"]), actor="user")
    mi.importer.import_file(str(files["fb_msgs"]), actor="user")
    mi.importer.import_file(str(files["ics"]), actor="user")
    texts = {it["provenance"]["record_ref"]: mi.corpus.content(it["corpus_id"]) for it in items(mi)}
    assert "From the office." in texts["<m1@example.org>"]  # mbox >From un-escaped
    assert "[1 attachment(s) not imported]" in texts["<m2@example.org>"] and "JVBERi0" not in texts["<m2@example.org>"]
    assert "Folder: Health" in texts["https://asthma.example/"]
    assert any("Caf\u00e9" in t for t in texts.values())  # Facebook mojibake repaired
    assert "Bring inhaler and letter" in texts["ev1@google.com"] and "lee@example.org" in texts["ev1@google.com"]


def test_cookie_values_never_stored_logged_or_exported(mi, files, tmp_path):
    for k in ("chrome_cookies", "ff_cookies"):
        mi.importer.import_file(str(files[k]), actor="user")
    its = items(mi)
    assert sorted(it["provenance"]["record_ref"] for it in its) == ["bank.example", "mail.example", "shop.example"]
    bank = next(it for it in its if it["provenance"]["record_ref"] == "bank.example")
    meta = bank["provenance"]["details"]["cookie_meta"]
    assert meta["count"] == 2 and meta["values_imported"] is False and meta["first_seen"] and meta["last_seen"]
    # the SQL never even selects names or values
    for sql, _ in imp.COOKIE_SQL.values():
        assert "value" not in sql.lower() and "name" not in sql.lower()
    from medb.export import export
    mi.outbox.config["enabled"] = True
    mi.outbox.sync()
    export(mi, tmp_path / "exp", actor="user")
    mi.store.db.commit()
    blobs = [p.read_bytes() for p in tmp_path.glob("db.sqlite*")]  # incl. any -wal/-journal
    content = mi.store.db.execute("SELECT body FROM content").fetchall()
    events = mi.store.db.execute("SELECT body FROM events").fetchall()
    blobs.append(json.dumps([c[0] for c in content + events]).encode())
    assert any(b"bank.example" in b for b in blobs)  # the check can see imported metadata
    blobs += [p.read_bytes() for p in (tmp_path / "exp").rglob("*") if p.is_file()]
    blobs.append(json.dumps(mi.gov.entries()).encode())
    blobs.append(json.dumps(mi.q1.self_description()).encode())
    for b in blobs:
        for secret in (COOKIE_SECRET, COOKIE_NAME):
            assert secret.encode() not in b


@pytest.mark.parametrize("key,reason", [("unknown", "unknown_format"), ("other_sqlite", "unknown_format"),
                                        ("plain_html", "unknown_format")])
def test_unknown_formats_default_deny(mi, files, key, reason):
    with pytest.raises(ImportRefused) as e:
        mi.importer.import_file(str(files[key]), actor="user")
    assert e.value.reason == reason
    assert mi.gov.entries(kinds=["IMPORT_REFUSED"])[-1]["body"]["reason"] == reason
    assert not mi.corpus.items()


def test_explicit_format_must_match_content(mi, files):
    for key, fmt in (("json", "fhir_r4_bundle"), ("note", "gmail_mbox"), ("chrome_sqlite", "chrome_cookies_meta"),
                     ("csv", "json_records"), ("fhir", "text_note")):
        with pytest.raises(ImportRefused) as e:
            mi.importer.import_file(str(files[key]), actor="user", fmt=fmt)
        assert e.value.reason == "format_mismatch", (key, fmt)
    with pytest.raises(ImportRefused):
        mi.importer.import_file(str(files["json"]), actor="user", fmt="no_such_format")
    r = mi.importer.import_file(str(files["github"]), actor="user", fmt="json_records")  # JSON family: allowed
    assert r["format"] == "json_records"
    assert len(mi.corpus.items()) == 2


def test_disallowed_format_in_config(mi, files):
    mi.importer.config["formats"] = ["fhir_r4_bundle"]
    with pytest.raises(ImportRefused):
        mi.importer.import_file(str(files["mbox"]), actor="user")
    assert mi.importer.import_file(str(files["fhir"]), actor="user")["ingested"] == 3


def test_paths_confined_to_import_roots(mi, files, tmp_path):
    outside = tmp_path / "outside.md"
    outside.write_text("# secret")
    with pytest.raises(ImportRefused) as e:
        mi.importer.import_file(str(outside), actor="user")
    assert e.value.reason == "path_outside_import_roots"
    link = files["note"].parent / "link.md"
    link.symlink_to(outside)
    with pytest.raises(ImportRefused):
        mi.importer.import_file(str(link), actor="user")  # symlink escaping the root
    with pytest.raises(ImportRefused):
        mi.importer.import_file(str(files["note"].parent / ".." / "outside.md"), actor="user")
    with pytest.raises(ImportRefused) as e:
        mi.importer.import_file(str(files["note"].parent), actor="user")
    assert e.value.reason == "not_a_file"
    # relative paths resolve against the first root
    assert mi.importer.import_file("note.md", actor="user")["ingested"] == 1
    assert not any(it["provenance"]["file_name"] == "outside.md" for it in items(mi))


def test_size_and_item_limits(mi, files):
    mi.importer.config["max_items_per_run"] = 1
    r = mi.importer.import_file(str(files["csv"]), actor="user")
    assert r["ingested"] == 1 and r["truncated_at_max_items"] is True
    mi.importer.config["max_file_mb"] = 0.00001
    with pytest.raises(ImportRefused) as e:
        mi.importer.import_file(str(files["fhir"]), actor="user")
    assert e.value.reason == "file_too_large"


def test_mbox_is_streamed(mi, tmp_path):
    big = tmp_path / "imports" / "big.mbox"
    with open(big, "wb") as f:
        for i in range(1500):
            f.write(f"From x Mon Sep 01 10:00:00 2026\nMessage-ID: <b{i}@x>\nSubject: n{i}\n\nbody {i}\n\n".encode())
    gen = imp._mbox_messages(big)
    assert hasattr(gen, "__next__")  # a generator: one message in memory at a time
    assert next(gen).startswith(b"Message-ID: <b0@x>")
    r = mi.importer.import_file(str(big), actor="user")
    assert r["ingested"] == 1500


def test_imported_items_obey_withdrawal_and_use_closure(mi, files):
    mi.importer.import_file(str(files["fhir"]), actor="user")
    cid = items(mi)[0]["corpus_id"]
    with pytest.raises(PermissionDenied):
        mi.corpus.retrieve(cid, purpose="clinic-visit", actor="user")  # no use grant yet
    mi.perms.grant("use", "user", scopes=["health"], purposes=["clinic-visit"], sensitivity_max="high")
    assert mi.corpus.retrieve(cid, purpose="clinic-visit", actor="user")["content"]
    mi.corpus.withdraw(cid, actor="user")
    with pytest.raises(PermissionDenied):
        mi.corpus.retrieve(cid, purpose="clinic-visit", actor="user")


@pytest.mark.parametrize("prim", ["integrations.import", "corpus.ingest", "permissions.closure"])
def test_blocked_while_suspended(mi, files, prim):
    mi.suspensions.suspend(prim, "t", "UNDETERMINED", [], ["x"])
    with pytest.raises(CapabilitySuspended):
        mi.importer.import_file(str(files["note"]), actor="user")
    assert not mi.corpus.items()


def test_inventory_lists_importer_under_its_primitives():
    inv = interface_inventory()["primitives"]
    for p in ("integrations.import", "corpus.ingest", "permissions.closure"):
        assert "Importer.import_file" in inv[p]["interfaces"]
    assert inv["integrations.import"]["depends_on"] == ["corpus.ingest"]


def test_self_description_reports_importers(mi, m):
    assert m.q1.self_description()["integrations"]["importers"]["enabled"] is False
    st = mi.q1.self_description()["integrations"]["importers"]
    assert st["enabled"] is True and st["actor"] == "user" and "fhir_r4_bundle" in st["formats"]
