"""Sample export files for the integrations tests (synthetic; no real personal data)."""
import json
import sqlite3
from pathlib import Path

COOKIE_SECRET = "SECRETCOOKIEVALUE-7f3a9c"
COOKIE_NAME = "SESSIONNAME-q8w"

FHIR = {"resourceType": "Bundle", "id": "bundle-1", "type": "collection", "entry": [
    {"fullUrl": "urn:uuid:p1", "resource": {"resourceType": "Patient", "id": "p1", "name": [{"text": "Test Patient"}]}},
    {"fullUrl": "urn:uuid:o1", "resource": {"resourceType": "Observation", "id": "o1", "status": "final",
     "code": {"coding": [{"system": "http://loinc.org", "code": "8867-4", "display": "Heart rate"}]},
     "subject": {"reference": "Patient/p1"}, "effectiveDateTime": "2026-09-01T09:00:00Z",
     "valueQuantity": {"value": 72, "unit": "beats/minute"}, "meta": {"source": "clinic-portal"},
     "performer": [{"display": "Dr Lee"}]}},
    {"fullUrl": "urn:uuid:c1", "resource": {"resourceType": "Condition", "id": "c1",
     "code": {"text": "Asthma"}, "clinicalStatus": {"coding": [{"code": "active"}]},
     "subject": {"reference": "Patient/p1"}, "onsetDateTime": "2010-05-01"}},
    {"fullUrl": "urn:uuid:m1", "resource": {"resourceType": "MedicationStatement", "id": "m1", "status": "active",
     "medicationCodeableConcept": {"text": "Salbutamol inhaler"}, "subject": {"reference": "Patient/p1"},
     "dosage": [{"text": "2 puffs as needed"}]}},
]}

MBOX = (b"From 1234@xxx Mon Sep 01 10:00:00 +0000 2026\n"
        b"X-Gmail-Labels: Inbox\nMessage-ID: <m1@example.org>\nFrom: Alice <alice@example.org>\nTo: me@example.org\n"
        b"Subject: Lunch\nDate: Mon, 01 Sep 2026 10:00:00 +0000\nContent-Type: text/plain\n\n"
        b"Hi, lunch on Friday?\n>From the office.\n\n"
        b"From 5678@xxx Tue Sep 02 10:00:00 +0000 2026\n"
        b"Message-ID: <m2@example.org>\nFrom: Bob <bob@example.org>\nTo: me@example.org\nSubject: Report\n"
        b"MIME-Version: 1.0\nContent-Type: multipart/mixed; boundary=XX\n\n--XX\nContent-Type: text/plain\n\n"
        b"See attached.\n--XX\nContent-Type: application/pdf\nContent-Disposition: attachment; filename=r.pdf\n"
        b"Content-Transfer-Encoding: base64\n\nJVBERi0=\n--XX--\n")

ICS = ("BEGIN:VCALENDAR\r\nVERSION:2.0\r\nBEGIN:VEVENT\r\nUID:ev1@google.com\r\nSUMMARY:Clinic appointment\r\n"
       "DTSTART:20260910T090000Z\r\nDTEND:20260910T093000Z\r\nLOCATION:Clinic\r\nDESCRIPTION:Bring inhaler and\r\n  "
       "letter\r\nATTENDEE;CN=Dr Lee:mailto:lee@example.org\r\nEND:VEVENT\r\nBEGIN:VEVENT\r\nUID:ev2@google.com\r\n"
       "SUMMARY:Run\r\nDTSTART:20260911T060000Z\r\nEND:VEVENT\r\nEND:VCALENDAR\r\n")

VCF = ("BEGIN:VCARD\r\nVERSION:3.0\r\nFN:Alice Example\r\nEMAIL:alice@example.org\r\nTEL:+61 400 000 000\r\nEND:VCARD\r\n"
       "BEGIN:VCARD\r\nVERSION:3.0\r\nFN:Bob Example\r\nORG:Clinic\r\nEND:VCARD\r\n")

BOOKMARKS_HTML = """<!DOCTYPE NETSCAPE-Bookmark-file-1>
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
<TITLE>Bookmarks</TITLE><H1>Bookmarks</H1>
<DL><p>
<DT><H3 ADD_DATE="1700000000">Health</H3>
<DL><p>
<DT><A HREF="https://asthma.example/" ADD_DATE="1700000001">Asthma info</A>
</DL><p>
<DT><A HREF="https://news.example/" ADD_DATE="1700000002">News</A>
</DL><p>
"""


def write_all(d: Path) -> dict:
    d.mkdir(parents=True, exist_ok=True)
    f = {}
    f["fhir"] = d / "health_bundle.json"
    f["fhir"].write_text(json.dumps(FHIR))
    f["note"] = d / "note.md"
    f["note"].write_text("# Sleep diary\n\nSlept 7h, woke once.\n")
    f["csv"] = d / "weights.csv"
    f["csv"].write_text("date,kg\n2026-09-01,70.1\n2026-09-08,69.8\n")
    f["ndjson"] = d / "steps.ndjson"
    f["ndjson"].write_text('{"d": "2026-09-01", "steps": 8000}\n\n{"d": "2026-09-02", "steps": 9100}\n')
    f["json"] = d / "misc.json"
    f["json"].write_text(json.dumps([{"a": 1}, {"a": 2}, {"a": 3}]))
    f["mbox"] = d / "All mail Including Spam and Trash.mbox"
    f["mbox"].write_bytes(MBOX)
    f["chrome_takeout"] = d / "BrowserHistory.json"
    f["chrome_takeout"].write_text(json.dumps({"Browser History": [
        {"title": "Asthma info", "url": "https://asthma.example/", "time_usec": 1756720000000000, "page_transition": "LINK"},
        {"title": "News", "url": "https://news.example/", "time_usec": 1756720100000000}]}))
    f["bm_html"] = d / "Bookmarks.html"
    f["bm_html"].write_text(BOOKMARKS_HTML)
    f["bm_json"] = d / "Bookmarks"
    f["bm_json"].write_text(json.dumps({"version": 1, "roots": {"bookmark_bar": {"type": "folder", "name": "Bar", "children": [
        {"type": "url", "name": "MedB", "url": "http://127.0.0.1:8765/app/", "date_added": "13370000000000000"},
        {"type": "folder", "name": "Docs", "children": [{"type": "url", "name": "FHIR", "url": "https://hl7.org/fhir/"}]}]}}}))
    f["ics"] = d / "calendar.ics"
    f["ics"].write_text(ICS)
    f["vcf"] = d / "contacts.vcf"
    f["vcf"].write_text(VCF)
    f["github"] = d / "repositories_000001.json"
    f["github"].write_text(json.dumps([{"full_name": "gem/medb", "html_url": "https://github.com/gem/medb", "private": True},
                                       {"full_name": "gem/notes", "html_url": "https://github.com/gem/notes"}]))
    moj = "Caf\u00e9".encode("utf-8").decode("latin-1")  # Facebook DYI mojibake
    f["fb_msgs"] = d / "message_1.json"
    f["fb_msgs"].write_text(json.dumps({"participants": [{"name": "Gem"}, {"name": "Carol"}], "messages": [
        {"sender_name": "Carol", "timestamp_ms": 1756720000000, "content": f"See you at the {moj}"},
        {"sender_name": "Gem", "timestamp_ms": 1756720100000, "content": "Yes!"}]}))
    f["fb_posts"] = d / "your_posts_1.json"
    f["fb_posts"].write_text(json.dumps([{"timestamp": 1756720000, "data": [{"post": "Hello"}]}]))
    f["chrome_sqlite"] = d / "History"
    con = sqlite3.connect(f["chrome_sqlite"])
    con.executescript("CREATE TABLE urls(id INTEGER PRIMARY KEY, url TEXT, title TEXT, visit_count INT, last_visit_time INT);"
                      "CREATE TABLE visits(id INTEGER PRIMARY KEY, url INT, visit_time INT);"
                      "INSERT INTO urls VALUES(1,'https://asthma.example/','Asthma info',3,13370000000000000);"
                      "INSERT INTO urls VALUES(2,'https://news.example/','News',1,13370000100000000);")
    con.commit(); con.close()
    f["ff_places"] = d / "places.sqlite"
    con = sqlite3.connect(f["ff_places"])
    con.executescript("CREATE TABLE moz_places(id INTEGER PRIMARY KEY, url TEXT, title TEXT, visit_count INT, last_visit_date INT);"
                      "CREATE TABLE moz_bookmarks(id INTEGER PRIMARY KEY, type INT, fk INT, title TEXT, dateAdded INT);"
                      "INSERT INTO moz_places VALUES(1,'https://asthma.example/','Asthma info',2,1756720000000000);"
                      "INSERT INTO moz_places VALUES(2,'https://never.example/','Never',0,NULL);"
                      "INSERT INTO moz_bookmarks VALUES(1,1,1,'Asthma bookmark',1756720000000000);")
    con.commit(); con.close()
    f["chrome_cookies"] = d / "Cookies"
    con = sqlite3.connect(f["chrome_cookies"])
    con.execute("CREATE TABLE cookies(creation_utc INT, host_key TEXT, name TEXT, value TEXT, encrypted_value BLOB, "
                "path TEXT, expires_utc INT, last_access_utc INT)")
    for i, host in enumerate([".bank.example", ".bank.example", "mail.example"]):
        con.execute("INSERT INTO cookies VALUES(?,?,?,?,?,?,?,?)", (13370000000000000 + i, host, COOKIE_NAME,
                    COOKIE_SECRET, (COOKIE_SECRET + "-enc").encode(), "/", 0, 13370000500000000 + i))
    con.commit(); con.close()
    f["ff_cookies"] = d / "cookies.sqlite"
    con = sqlite3.connect(f["ff_cookies"])
    con.execute("CREATE TABLE moz_cookies(id INTEGER PRIMARY KEY, host TEXT, name TEXT, value TEXT, creationTime INT, lastAccessed INT)")
    con.execute("INSERT INTO moz_cookies(host,name,value,creationTime,lastAccessed) VALUES('.shop.example',?,?,1756720000000000,1756729999000000)",
                (COOKIE_NAME, COOKIE_SECRET))
    con.commit(); con.close()
    f["unknown"] = d / "scan.xyz"
    f["unknown"].write_bytes(b"\x00\x01binary")
    f["other_sqlite"] = d / "other.db"
    con = sqlite3.connect(f["other_sqlite"]); con.execute("CREATE TABLE t(x)"); con.commit(); con.close()
    f["plain_html"] = d / "page.html"
    f["plain_html"].write_text("<html><body>hi</body></html>")
    return f


# ---- live browser profiles (D-78): a profile *directory* as the browser keeps it
def chrome_profile(d):
    d.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(d / "History")
    con.executescript("CREATE TABLE urls(id INTEGER PRIMARY KEY, url TEXT, title TEXT, visit_count INT, last_visit_time INT);"
                      "INSERT INTO urls VALUES(1,'https://asthma.example/','Asthma info',3,13370000000000000);"
                      "INSERT INTO urls VALUES(2,'https://news.example/','News',1,13370000100000000);")
    con.commit(); con.close()
    (d / "Bookmarks").write_text(json.dumps({"roots": {"bookmark_bar": {"type": "folder", "name": "Bar", "children": [
        {"type": "url", "guid": "b-1", "name": "Clinic", "url": "https://clinic.example/", "date_added": "13370000000000000"}]}}}))
    (d / "Network").mkdir(exist_ok=True)
    con = sqlite3.connect(d / "Network" / "Cookies")
    con.execute("CREATE TABLE cookies(creation_utc INT, host_key TEXT, name TEXT, value TEXT, encrypted_value BLOB, "
                "path TEXT, expires_utc INT, last_access_utc INT)")
    for i, host in enumerate([".bank.example", ".bank.example", "mail.example"]):
        con.execute("INSERT INTO cookies VALUES(?,?,?,?,?,?,?,?)", (13370000000000000 + i, host, COOKIE_NAME,
                    COOKIE_SECRET, (COOKIE_SECRET + "-enc").encode(), "/", 0, 13370000500000000 + i))
    con.commit(); con.close()
    return d


def firefox_profile(d):
    d.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(d / "places.sqlite")
    con.executescript("CREATE TABLE moz_places(id INTEGER PRIMARY KEY, url TEXT, title TEXT, visit_count INT, last_visit_date INT);"
                      "CREATE TABLE moz_bookmarks(id INTEGER PRIMARY KEY, type INT, fk INT, title TEXT, dateAdded INT, lastModified INT);"
                      "INSERT INTO moz_places VALUES(1,'https://asthma.example/','Asthma info',2,1756720000000000);"
                      "INSERT INTO moz_places VALUES(2,'https://never.example/','Never',0,NULL);"
                      "INSERT INTO moz_bookmarks VALUES(1,1,1,'Asthma bookmark',1756720000000000,1756720000000000);")
    con.commit(); con.close()
    con = sqlite3.connect(d / "cookies.sqlite")
    con.execute("CREATE TABLE moz_cookies(id INTEGER PRIMARY KEY, host TEXT, name TEXT, value TEXT, creationTime INT, lastAccessed INT)")
    con.execute("INSERT INTO moz_cookies(host,name,value,creationTime,lastAccessed) VALUES('.shop.example',?,?,1756720000000000,1756729999000000)",
                (COOKIE_NAME, COOKIE_SECRET))
    con.commit(); con.close()
    return d
