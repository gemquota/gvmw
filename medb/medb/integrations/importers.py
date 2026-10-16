"""Local file importers into the corpus (DECISIONS D-72; off by default).

Files only, from a local path under a configured import root; no network,
no OAuth, no stored account credentials. Every run is:

* **user-only** (any other actor: ``PROHIBITED_ATTEMPT``);
* **grant-gated**: an active ``ingest`` grant must cover the run's source
  (default ``import:<format>``), scope and sensitivity *before* the file is read;
* **default-deny on format**: a file is imported only if its format is
  recognised (by extension *and* content sniffing); anything else is refused
  and logged (``IMPORT_REFUSED``);
* **provenance per item**: each corpus item records the importer, format,
  file name, file SHA-256, source account label, record index/reference and
  whether it contains third-party content;
* **streamed** where the format allows (mbox, CSV, NDJSON, ICS, VCF, Netscape
  bookmarks HTML, SQLite cursors). JSON documents are parsed whole, bounded by
  ``max_json_mb``;
* **logged**: one ``IMPORT_RUN`` gov entry per run (counts, hash, run id), and
  each item's INGEST is mirrored into gov as for any corpus ingest.

Browser cookies are never imported. The cookie importers read only metadata
columns (host, creation and last-access times) -- the SQL never selects
``name``, ``value`` or ``encrypted_value`` -- and aggregate them per domain,
so no cookie value can reach storage, logs or exports.
"""
from __future__ import annotations

import csv
import email
import email.policy
import hashlib
import io
import json
import re
import sqlite3
from datetime import datetime, timedelta, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import quote

from ..errors import NotAuthorized, PermissionDenied
from ..interfaces import reaches

IMPORTER_VERSION = "medb.integrations.importers/1"
SQLITE_MAGIC = b"SQLite format 3\x00"

# format id -> (label, default scope, media type, export kind)
FORMATS = {
    "text_note": ("Markdown / plain-text note", "notes", "text/markdown", "local notes"),
    "json_records": ("JSON records", "records", "application/json", "JSON file"),
    "ndjson_records": ("NDJSON / JSON Lines records", "records", "application/json", "JSON Lines file"),
    "csv_rows": ("CSV rows", "records", "text/csv", "CSV file"),
    "fhir_r4_bundle": ("FHIR R4 Bundle (patient-held record)", "health", "application/fhir+json", "FHIR R4 Bundle"),
    "gmail_mbox": ("Gmail / mbox mailbox (Google Takeout)", "correspondence", "message/rfc822", "Google Takeout: Mail"),
    "chrome_history_takeout": ("Chrome history (Google Takeout JSON)", "browsing", "application/json", "Google Takeout: Chrome"),
    "chrome_bookmarks_html": ("Bookmarks HTML (Takeout / browser export)", "browsing", "text/html", "Bookmarks HTML export"),
    "chrome_bookmarks_json": ("Chrome profile Bookmarks JSON", "browsing", "application/json", "Chrome profile"),
    "calendar_ics": ("Calendar .ics (Google Takeout)", "calendar", "text/calendar", "Google Takeout: Calendar"),
    "contacts_vcf": ("Contacts .vcf (Google Takeout)", "contacts", "text/vcard", "Google Takeout: Contacts"),
    "github_json": ("GitHub account export / repo metadata JSON", "code", "application/json", "GitHub export"),
    "facebook_json": ("Facebook 'Download your information' JSON", "social", "application/json", "Facebook DYI"),
    "chrome_history_sqlite": ("Chrome profile History (SQLite copy)", "browsing", "application/json", "Chrome profile"),
    "firefox_places_sqlite": ("Firefox places.sqlite (copy)", "browsing", "application/json", "Firefox profile"),
    "chrome_cookies_meta": ("Chrome Cookies (metadata only; values never read)", "browsing", "application/json", "Chrome profile"),
    "firefox_cookies_meta": ("Firefox cookies.sqlite (metadata only; values never read)", "browsing", "application/json", "Firefox profile"),
}
THIRD_PARTY_FORMATS = {"gmail_mbox", "contacts_vcf", "calendar_ics", "facebook_json"}  # see F-24
EXT = {".md": "text_note", ".markdown": "text_note", ".txt": "text_note", ".csv": "csv_rows", ".mbox": "gmail_mbox",
       ".ics": "calendar_ics", ".vcf": "contacts_vcf", ".ndjson": "ndjson_records", ".jsonl": "ndjson_records"}


class ImportRefused(Exception):
    """A run was refused before any item was ingested (format, path, size, disabled)."""
    def __init__(self, reason: str, detail: str = ""):
        super().__init__(detail or reason)
        self.reason = reason


class ImportsDisabled(ImportRefused):
    pass


# ----------------------------------------------------------------- helpers
def _iso(dt: datetime | None) -> str | None:
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ") if dt else None


def webkit_ts(us) -> str | None:
    """Chrome/WebKit microseconds since 1601-01-01."""
    try:
        us = int(us)
    except (TypeError, ValueError):
        return None
    return _iso(datetime(1601, 1, 1, tzinfo=timezone.utc) + timedelta(microseconds=us)) if us > 0 else None


def unix_us_ts(us) -> str | None:
    try:
        us = int(us)
    except (TypeError, ValueError):
        return None
    return _iso(datetime.fromtimestamp(us / 1e6, tz=timezone.utc)) if us > 0 else None


def unix_s_ts(s) -> str | None:
    try:
        s = float(s)
    except (TypeError, ValueError):
        return None
    return _iso(datetime.fromtimestamp(s, tz=timezone.utc)) if s > 0 else None


def file_sha256(path: Path) -> tuple[str, int]:
    h, n = hashlib.sha256(), 0
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
            n += len(chunk)
    return h.hexdigest(), n


def _clip(s: str, n: int) -> str:
    return s if len(s) <= n else s[:n] + f"\n[... truncated at {n} characters by the importer]"


def _pretty(o, n: int) -> str:
    return _clip(json.dumps(o, indent=1, ensure_ascii=False, sort_keys=True), n)


def _fb_fix(o):
    """Facebook DYI JSON encodes UTF-8 bytes as latin-1 code points; undo that."""
    if isinstance(o, str):
        try:
            return o.encode("latin-1").decode("utf-8")
        except (UnicodeEncodeError, UnicodeDecodeError):
            return o
    if isinstance(o, list):
        return [_fb_fix(x) for x in o]
    if isinstance(o, dict):
        return {_fb_fix(k): _fb_fix(v) for k, v in o.items()}
    return o


def _sqlite_ro(path: Path) -> sqlite3.Connection:
    # read-only + immutable: never writes, never takes locks on the user's copy
    return sqlite3.connect(f"file:{quote(str(path))}?mode=ro&immutable=1", uri=True)


def sqlite_tables(path: Path) -> set[str]:
    con = _sqlite_ro(path)
    try:
        return {r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    finally:
        con.close()


def _cols(con, table: str) -> set[str]:
    return {r[1] for r in con.execute(f"PRAGMA table_info({table})")}


# ----------------------------------------------------------------- detection
def detect(path: Path, max_json_bytes: int) -> str | None:
    """Recognised format id, or None (default-deny)."""
    with open(path, "rb") as f:
        head = f.read(4096)
    if head.startswith(SQLITE_MAGIC):
        t = sqlite_tables(path)
        if {"urls", "visits"} <= t:
            return "chrome_history_sqlite"
        if "moz_places" in t:
            return "firefox_places_sqlite"
        if "cookies" in t:
            con = _sqlite_ro(path)
            try:
                if {"host_key", "creation_utc"} <= _cols(con, "cookies"):
                    return "chrome_cookies_meta"
            finally:
                con.close()
        if "moz_cookies" in t:
            return "firefox_cookies_meta"
        return None
    ext = path.suffix.lower()
    text = head.decode("utf-8", "replace").lstrip("\ufeff \r\n\t")
    if ext in (".html", ".htm"):
        return "chrome_bookmarks_html" if "NETSCAPE-Bookmark-file" in text else None
    if ext == ".mbox":
        return "gmail_mbox" if text.startswith("From ") else None
    if ext == ".ics":
        return "calendar_ics" if text.upper().startswith("BEGIN:VCALENDAR") else None
    if ext == ".vcf":
        return "contacts_vcf" if text.upper().startswith("BEGIN:VCARD") else None
    if ext in EXT:
        return EXT[ext]
    if ext == ".json" or (ext == "" and text[:1] in "[{"):
        if path.stat().st_size > max_json_bytes:
            return None
        try:
            doc = json.loads(path.read_text(encoding="utf-8-sig"))
        except (ValueError, UnicodeDecodeError):
            return None
        return sniff_json(doc, path.name)
    return None


def sniff_json(doc, name: str) -> str:
    if isinstance(doc, dict):
        if doc.get("resourceType") == "Bundle":
            return "fhir_r4_bundle"
        if "Browser History" in doc:
            return "chrome_history_takeout"
        if "roots" in doc and isinstance(doc["roots"], dict):
            return "chrome_bookmarks_json"
        if "participants" in doc and "messages" in doc:
            return "facebook_json"
    items = doc if isinstance(doc, list) else []
    if items and all(isinstance(x, dict) for x in items[:20]):
        keys = set().union(*[set(x) for x in items[:20]])
        urls = " ".join(str(x.get("html_url") or x.get("url") or "") for x in items[:20])
        if "github.com" in urls or re.match(r"(repositories|issues|pull_requests|issue_comments|users|organizations)_\d+", name):
            return "github_json"
        if {"timestamp"} <= keys and ({"data"} & keys or {"attachments"} & keys):
            return "facebook_json"
    if isinstance(doc, dict) and ("html_url" in doc and "github.com" in str(doc.get("html_url"))):
        return "github_json"
    return "json_records"


# ----------------------------------------------------------------- parsers
# Each parser yields dicts: {content, ref, third_party, extra?}; ``n`` = max item characters.

def p_text_note(path, n, account):
    text = path.read_text(encoding="utf-8", errors="replace")
    title = next((ln.lstrip("# ").strip() for ln in text.splitlines() if ln.strip()), path.stem)
    yield {"content": _clip(text, n), "ref": title[:200], "third_party": False}


def p_json_records(path, n, account):
    doc = json.loads(path.read_text(encoding="utf-8-sig"))
    for i, rec in enumerate(doc if isinstance(doc, list) else [doc]):
        yield {"content": _pretty(rec, n), "ref": f"[{i}]", "third_party": False}


def p_ndjson_records(path, n, account):
    with open(path, encoding="utf-8-sig", errors="replace") as f:
        for i, line in enumerate(f):
            if line.strip():
                rec = json.loads(line)
                yield {"content": _pretty(rec, n), "ref": f"line {i + 1}", "third_party": False}


def p_csv_rows(path, n, account):
    with open(path, newline="", encoding="utf-8-sig", errors="replace") as f:
        for i, row in enumerate(csv.DictReader(f)):
            yield {"content": _clip("\n".join(f"{k}: {v}" for k, v in row.items()), n), "ref": f"row {i + 1}",
                   "third_party": False}


FHIR_TYPES = ("Observation", "Condition", "MedicationStatement")


def _code_text(cc) -> str:
    if not isinstance(cc, dict):
        return ""
    if cc.get("text"):
        return cc["text"]
    for c in cc.get("coding") or []:
        if c.get("display") or c.get("code"):
            return c.get("display") or f"{c.get('system', '')}|{c.get('code')}"
    return ""


def fhir_summary(r: dict) -> str:
    t = r.get("resourceType")
    if t == "Observation":
        if "valueQuantity" in r:
            vq = r["valueQuantity"]
            val = f"{vq.get('value')} {vq.get('unit') or vq.get('code') or ''}".strip()
        else:
            val = next((str(_code_text(r[k]) if isinstance(r[k], dict) else r[k]) for k in r if k.startswith("value")), "")
        when = r.get("effectiveDateTime") or (r.get("effectivePeriod") or {}).get("start") or r.get("issued")
        return f"Observation: {_code_text(r.get('code'))} = {val} ({r.get('status', '?')}; {when or 'no date'})"
    if t == "Condition":
        st = _code_text(r.get("clinicalStatus"))
        return f"Condition: {_code_text(r.get('code'))} (clinical status {st or '?'}; onset {r.get('onsetDateTime') or '?'})"
    if t == "MedicationStatement":
        med = _code_text(r.get("medicationCodeableConcept")) or (r.get("medicationReference") or {}).get("display", "")
        dose = "; ".join(d.get("text", "") for d in r.get("dosage") or [] if d.get("text"))
        return f"MedicationStatement: {med} ({r.get('status', '?')}){' - ' + dose if dose else ''}"
    return t or "?"


def p_fhir_r4_bundle(path, n, account, skipped):
    doc = json.loads(path.read_text(encoding="utf-8-sig"))
    if not (isinstance(doc, dict) and doc.get("resourceType") == "Bundle"):
        raise ImportRefused("format_mismatch", "not a FHIR R4 Bundle")
    for i, e in enumerate(doc.get("entry") or []):
        r = (e or {}).get("resource") or {}
        t = r.get("resourceType")
        if t not in FHIR_TYPES:
            skipped[f"fhir_{t or 'unknown'}_not_imported"] = skipped.get(f"fhir_{t or 'unknown'}_not_imported", 0) + 1
            continue
        subj = (r.get("subject") or r.get("patient") or {}).get("reference")
        yield {"content": _clip(fhir_summary(r) + "\n\n" + json.dumps(r, indent=1, ensure_ascii=False), n),
               "ref": f"{t}/{r.get('id', i)}", "third_party": False,
               "extra": {"fhir": {"bundle_id": doc.get("id"), "bundle_type": doc.get("type"), "resource_type": t,
                                  "resource_id": r.get("id"), "full_url": e.get("fullUrl"), "subject": subj,
                                  "meta_source": (r.get("meta") or {}).get("source"),
                                  "performer": [p.get("display") or p.get("reference") for p in r.get("performer") or []
                                                if isinstance(p, dict)] or None}}}


def _mbox_messages(path):
    """Stream an mbox file: yields raw message bytes (memory = one message)."""
    buf, prev_blank = [], True
    with open(path, "rb") as f:
        for line in f:
            if line.startswith(b"From ") and prev_blank:
                if buf:
                    yield b"".join(buf)
                buf = []
            else:
                buf.append(line[1:] if line.startswith(b">From ") else line)
            prev_blank = line.strip() == b""
    if buf:
        yield b"".join(buf)


class _Text(HTMLParser):
    def __init__(self):
        super().__init__()
        self.out = []

    def handle_data(self, d):
        self.out.append(d)


def _html_text(h: str) -> str:
    p = _Text()
    p.feed(h)
    return re.sub(r"\n\s*\n+", "\n\n", "".join(p.out)).strip()


def mail_item(raw: bytes, n: int, fallback_ref: str) -> dict:
    """One RFC 822 message -> corpus item (shared by the mbox importer and Gmail live sync)."""
    msg = email.message_from_bytes(raw, policy=email.policy.default)
    body, attachments = "", 0
    try:
        part = msg.get_body(preferencelist=("plain", "html"))
        if part is not None:
            body = part.get_content()
            if part.get_content_type() == "text/html":
                body = _html_text(body)
    except (KeyError, LookupError, ValueError):
        body = ""
    for _ in msg.iter_attachments():
        attachments += 1
    hdr = {}
    for k in ("From", "To", "Cc", "Date", "Subject"):
        try:
            hdr[k] = str(msg.get(k, ""))
        except Exception:  # malformed header
            hdr[k] = ""
    text = "\n".join(f"{k}: {v}" for k, v in hdr.items() if v) + "\n\n" + body
    if attachments:
        text += f"\n[{attachments} attachment(s) not imported]"
    labels = str(msg.get("X-Gmail-Labels", "")) or None
    return {"content": _clip(text, n), "ref": str(msg.get("Message-ID", fallback_ref)).strip(),
            "third_party": True,
            "extra": {"mail": {"from": hdr["From"] or None, "date": hdr["Date"] or None, "labels": labels,
                               "attachments_not_imported": attachments}}}


def p_gmail_mbox(path, n, account):
    for i, raw in enumerate(_mbox_messages(path)):
        yield mail_item(raw, n, f"message {i + 1}")


def p_chrome_history_takeout(path, n, account):
    doc = json.loads(path.read_text(encoding="utf-8-sig"))
    for i, h in enumerate(doc.get("Browser History") or []):
        when = unix_us_ts(h.get("time_usec"))
        yield {"content": f"Visited: {h.get('title') or ''}\n{h.get('url', '')}\nAt: {when}\nTransition: {h.get('page_transition', '')}",
               "ref": h.get("url", f"[{i}]")[:500], "third_party": False, "extra": {"visited_at": when}}


class _Bookmarks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.folders, self.cur, self.pending_h3, self.items = [], None, False, []
        self.text = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "h3":
            self.pending_h3, self.text = True, []
        elif tag == "a":
            self.cur, self.text = {"url": a.get("href", ""), "added": unix_s_ts(a.get("add_date"))}, []
        elif tag == "dl" and getattr(self, "_last_h3", None) is not None:
            self.folders.append(self._last_h3)
            self._last_h3 = None

    def handle_endtag(self, tag):
        if tag == "h3":
            self._last_h3, self.pending_h3 = "".join(self.text).strip(), False
        elif tag == "a" and self.cur is not None:
            self.cur.update(title="".join(self.text).strip(), folder="/".join(self.folders))
            self.items.append(self.cur)
            self.cur = None
        elif tag == "dl" and self.folders:
            self.folders.pop()

    def handle_data(self, d):
        self.text.append(d)


def p_chrome_bookmarks_html(path, n, account):
    p = _Bookmarks()
    with open(path, encoding="utf-8", errors="replace") as f:
        for chunk in iter(lambda: f.read(1 << 16), ""):
            p.feed(chunk)
            while p.items:
                b = p.items.pop(0)
                yield _bookmark(b)
    p.close()
    for b in p.items:
        yield _bookmark(b)


def _bookmark(b):
    return {"content": f"Bookmark: {b.get('title') or ''}\n{b['url']}\nFolder: {b.get('folder') or '/'}\nAdded: {b.get('added')}",
            "ref": b["url"][:500], "third_party": False}


def p_chrome_bookmarks_json(path, n, account):
    doc = json.loads(path.read_text(encoding="utf-8-sig"))

    def walk(node, folder):
        if node.get("type") == "url":
            yield _bookmark({"url": node.get("url", ""), "title": node.get("name"), "folder": folder,
                             "added": webkit_ts(node.get("date_added"))})
        for c in node.get("children") or []:
            yield from walk(c, folder + "/" + node.get("name", "") if node.get("type") == "folder" else folder)
    for name, root in (doc.get("roots") or {}).items():
        if isinstance(root, dict):
            yield from walk(root, "")


def _unfolded(path):
    """Yield logical lines of an RFC 5545/6350 file (streamed; folded lines joined)."""
    cur = None
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.rstrip("\r\n")
            if line[:1] in (" ", "\t") and cur is not None:
                cur += line[1:]
                continue
            if cur is not None:
                yield cur
            cur = line
    if cur is not None:
        yield cur


def _prop(line):
    k, _, v = line.partition(":")
    name = k.split(";", 1)[0].upper()
    return name, v.replace("\\n", "\n").replace("\\,", ",").replace("\\;", ";")


def _blocks(path, kind):
    block = None
    for line in _unfolded(path):
        u = line.upper()
        if u == f"BEGIN:{kind}":
            block = []
        elif u == f"END:{kind}" and block is not None:
            yield block
            block = None
        elif block is not None:
            block.append(_prop(line))


def p_calendar_ics(path, n, account):
    for i, props in enumerate(_blocks(path, "VEVENT")):
        d = {}
        att = []
        for k, v in props:
            if k == "ATTENDEE":
                att.append(v.replace("mailto:", ""))
            else:
                d.setdefault(k, v)
        lines = [f"Event: {d.get('SUMMARY', '')}", f"Start: {d.get('DTSTART', '')}", f"End: {d.get('DTEND', '')}"]
        for k in ("LOCATION", "ORGANIZER", "DESCRIPTION"):
            if d.get(k):
                lines.append(f"{k.title()}: {d[k].replace('mailto:', '')}")
        if att:
            lines.append("Attendees: " + ", ".join(att))
        yield {"content": _clip("\n".join(lines), n), "ref": d.get("UID", f"event {i + 1}"),
               "third_party": bool(att) or bool(d.get("ORGANIZER"))}


def p_contacts_vcf(path, n, account):
    for i, props in enumerate(_blocks(path, "VCARD")):
        lines = []
        name = None
        for k, v in props:
            if k in ("VERSION", "PRODID", "PHOTO"):
                continue
            if k == "FN":
                name = v
            lines.append(f"{k}: {v}")
        yield {"content": _clip("\n".join(lines), n), "ref": name or f"contact {i + 1}", "third_party": True}


def p_github_json(path, n, account):
    doc = json.loads(path.read_text(encoding="utf-8-sig"))
    kind = re.sub(r"_\d+$", "", path.stem)
    for i, rec in enumerate(doc if isinstance(doc, list) else [doc]):
        ref = (rec.get("html_url") or rec.get("url") or rec.get("full_name") or f"[{i}]") if isinstance(rec, dict) else f"[{i}]"
        yield {"content": _pretty(rec, n), "ref": str(ref)[:500], "third_party": False,
               "extra": {"github_record_kind": kind}}


def p_facebook_json(path, n, account):
    doc = _fb_fix(json.loads(path.read_text(encoding="utf-8-sig")))
    if isinstance(doc, dict) and "messages" in doc:
        parts = [p.get("name") for p in doc.get("participants") or [] if isinstance(p, dict)]
        for i, msg in enumerate(doc["messages"]):
            when = msg.get("timestamp_ms")
            when = unix_s_ts(when / 1000) if isinstance(when, (int, float)) else None
            text = f"From: {msg.get('sender_name', '')}\nAt: {when}\n\n{msg.get('content', '')}"
            yield {"content": _clip(text, n), "ref": f"message {i + 1}", "third_party": True,
                   "extra": {"participants": parts}}
        return
    if isinstance(doc, dict):
        lists = [v for v in doc.values() if isinstance(v, list)]
        doc = lists[0] if len(lists) == 1 else [doc]
    for i, rec in enumerate(doc):
        when = unix_s_ts(rec.get("timestamp")) if isinstance(rec, dict) else None
        yield {"content": _pretty(rec, n), "ref": f"[{i}]", "third_party": False, "extra": {"at": when}}


def p_chrome_history_sqlite(path, n, account):
    con = _sqlite_ro(path)
    try:
        for i, (url, title, visits, last) in enumerate(con.execute(
                "SELECT url, title, visit_count, last_visit_time FROM urls ORDER BY id")):
            when = webkit_ts(last)
            yield {"content": f"Visited: {title or ''}\n{url}\nVisits: {visits}\nLast visit: {when}",
                   "ref": (url or f"[{i}]")[:500], "third_party": False,
                   "extra": {"visit_count": visits, "last_visit": when}}
    finally:
        con.close()


def p_firefox_places_sqlite(path, n, account):
    con = _sqlite_ro(path)
    try:
        for i, (url, title, visits, last) in enumerate(con.execute(
                "SELECT url, title, visit_count, last_visit_date FROM moz_places WHERE visit_count > 0 ORDER BY id")):
            when = unix_us_ts(last)
            yield {"content": f"Visited: {title or ''}\n{url}\nVisits: {visits}\nLast visit: {when}",
                   "ref": (url or f"[{i}]")[:500], "third_party": False,
                   "extra": {"visit_count": visits, "last_visit": when}}
        if "moz_bookmarks" in {r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'")}:
            for url, title, added in con.execute(
                    "SELECT p.url, b.title, b.dateAdded FROM moz_bookmarks b JOIN moz_places p ON p.id = b.fk "
                    "WHERE b.type = 1 ORDER BY b.id"):
                yield _bookmark({"url": url or "", "title": title, "folder": None, "added": unix_us_ts(added)})
    finally:
        con.close()


# Cookie metadata. The SQL names only metadata columns; cookie names and values
# (``name``, ``value``, ``encrypted_value``) are never selected, so they never
# enter Python memory, let alone storage, logs or exports (D-72, Gem's rule).
COOKIE_SQL = {
    "chrome_cookies_meta": ("SELECT host_key, COUNT(*), MIN(creation_utc), MAX(last_access_utc) "
                            "FROM cookies GROUP BY host_key ORDER BY host_key", webkit_ts),
    "firefox_cookies_meta": ("SELECT host, COUNT(*), MIN(creationTime), MAX(lastAccessed) "
                             "FROM moz_cookies GROUP BY host ORDER BY host", unix_us_ts),
}


def _cookies(fmt):
    sql, conv = COOKIE_SQL[fmt]

    def parse(path, n, account):
        con = _sqlite_ro(path)
        try:
            for host, count, first, last in con.execute(sql):
                d = (host or "").lstrip(".")
                yield {"content": f"Cookie metadata for {d}: {count} cookie(s); first set {conv(first)}; "
                                  f"last accessed {conv(last)}. Cookie names and values were not read.",
                       "ref": d, "third_party": False,
                       "extra": {"cookie_meta": {"domain": d, "count": count, "first_seen": conv(first),
                                                 "last_seen": conv(last), "values_imported": False}}}
        finally:
            con.close()
    return parse


PARSERS = {
    "text_note": p_text_note, "json_records": p_json_records, "ndjson_records": p_ndjson_records,
    "csv_rows": p_csv_rows, "gmail_mbox": p_gmail_mbox, "chrome_history_takeout": p_chrome_history_takeout,
    "chrome_bookmarks_html": p_chrome_bookmarks_html, "chrome_bookmarks_json": p_chrome_bookmarks_json,
    "calendar_ics": p_calendar_ics, "contacts_vcf": p_contacts_vcf, "github_json": p_github_json,
    "facebook_json": p_facebook_json, "chrome_history_sqlite": p_chrome_history_sqlite,
    "firefox_places_sqlite": p_firefox_places_sqlite,
    "chrome_cookies_meta": _cookies("chrome_cookies_meta"), "firefox_cookies_meta": _cookies("firefox_cookies_meta"),
}
# formats whose content sniff must agree when the user names the format explicitly
_SNIFFED = {"fhir_r4_bundle", "chrome_history_takeout", "chrome_bookmarks_json", "chrome_history_sqlite",
            "firefox_places_sqlite", "chrome_cookies_meta", "firefox_cookies_meta", "gmail_mbox",
            "calendar_ics", "contacts_vcf", "chrome_bookmarks_html"}
_JSON_FAMILY = {"json_records", "github_json", "facebook_json"}


class Importer:
    """User-only file import into the corpus (``config.integrations.importers``)."""

    def __init__(self, medb, config: dict, root: Path, suspensions=None):
        self.m = medb
        self.config = config or {}
        self.root = Path(root)
        self._suspensions = suspensions

    @property
    def enabled(self) -> bool:
        return bool(self.config.get("enabled"))

    def roots(self) -> list[Path]:
        out = []
        for r in self.config.get("allowed_roots") or []:
            p = Path(r).expanduser()
            out.append((p if p.is_absolute() else self.root / p).resolve())
        return out

    def _refuse(self, actor, reason, detail, **kw):
        self.m.gov.record("IMPORT_REFUSED", actor, reason=reason, detail=detail, **kw)
        raise ImportRefused(reason, detail)

    def resolve_path(self, path: str, actor: str) -> Path:
        p = Path(path).expanduser()
        roots = self.roots()
        if not p.is_absolute() and roots:
            p = roots[0] / p
        rp = p.resolve()
        if not any(rp == r or r in rp.parents for r in roots):
            self._refuse(actor, "path_outside_import_roots", "file is not under a configured import root",
                         file_name=p.name)
        if not rp.is_file():
            self._refuse(actor, "not_a_file", "path is not a regular file", file_name=p.name)
        return rp

    def list_files(self) -> list[dict]:
        out = []
        for r in self.roots():
            if r.is_dir():
                for f in sorted(r.rglob("*")):
                    if f.is_file() and not f.name.startswith("."):
                        out.append({"path": str(f.relative_to(r)), "root": str(r), "bytes": f.stat().st_size})
        return out[:2000]

    @reaches("integrations.import", "corpus.ingest", "permissions.closure")
    def import_file(self, path: str, actor: str, fmt: str | None = None, scope: str | None = None,
                    source: str | None = None, sensitivity: str | None = None, account: str | None = None) -> dict:
        if actor != "user":
            self.m.gov.record("PROHIBITED_ATTEMPT", actor, reason="non_user_import", file_name=Path(path).name)
            raise NotAuthorized("only the user can import files into the corpus")
        if not self.enabled:
            self.m.gov.record("IMPORT_REFUSED", actor, reason="importers_disabled", detail="config.integrations.importers.enabled is false")
            raise ImportsDisabled("importers_disabled", "file importers are off (config.integrations.importers.enabled)")
        cfg = self.config
        rp = self.resolve_path(path, actor)
        size = rp.stat().st_size
        if size > float(cfg.get("max_file_mb", 512)) * (1 << 20):
            self._refuse(actor, "file_too_large", f"{size} bytes > max_file_mb", file_name=rp.name)
        max_json = int(float(cfg.get("max_json_mb", 64)) * (1 << 20))
        detected = detect(rp, max_json)
        allowed = set(cfg.get("formats") or FORMATS)
        if fmt in (None, "", "auto"):
            fmt = detected
        elif fmt not in FORMATS:
            fmt = None
        elif fmt in _SNIFFED and detected != fmt:
            self._refuse(actor, "format_mismatch", f"file does not look like {fmt} (detected {detected})", file_name=rp.name)
        elif fmt in _JSON_FAMILY and detected not in _JSON_FAMILY:
            self._refuse(actor, "format_mismatch", f"file is not a JSON document of that kind (detected {detected})",
                         file_name=rp.name)
        elif fmt == "text_note" and detected != "text_note":
            self._refuse(actor, "format_mismatch", f"not a text note (detected {detected})", file_name=rp.name)
        if fmt is None or fmt not in allowed:
            self._refuse(actor, "unknown_format", "unrecognised or disallowed format (default deny)",
                         file_name=rp.name, requested=fmt, detected=detected)
        label, def_scope, media, export_kind = FORMATS[fmt]
        scope = scope or def_scope
        source = source or f"import:{fmt}"
        sensitivity = sensitivity or cfg.get("default_sensitivity", "high")
        node = {"scope": scope, "sensitivity": sensitivity}
        grants = self.m.perms.covering("ingest", [node], source=source)
        if not grants:  # checked before the file is read
            self.m.gov.record("PROHIBITED_ATTEMPT", actor, reason="ingest_without_grant", source=source, scope=scope,
                              via="Importer.import_file")
            raise PermissionDenied(f"no ingest grant covers source={source} scope={scope} sensitivity={sensitivity}")
        sha, nbytes = file_sha256(rp)
        run_id = self.m.ids.new("import")
        max_items, max_chars = int(cfg.get("max_items_per_run", 100000)), int(cfg.get("max_item_chars", 200000))
        skipped: dict[str, int] = {}
        parser = PARSERS.get(fmt) or (lambda p, n, a: p_fhir_r4_bundle(p, n, a, skipped))
        ids, third, truncated = [], 0, False
        for i, item in enumerate(parser(rp, max_chars, account)):
            if len(ids) >= max_items:
                truncated = True
                break
            prov = {"importer": IMPORTER_VERSION, "run_id": run_id, "format": fmt, "export_kind": export_kind,
                    "file_name": rp.name, "file_sha256": sha, "source_account": account or None,
                    "record_index": i, "record_ref": item.get("ref"),
                    "third_party_content": bool(item.get("third_party"))}
            if item.get("extra"):
                prov["details"] = item["extra"]
            third += bool(item.get("third_party"))
            r = self.m.corpus.ingest(item["content"], source=source, scope=scope, actor=actor,
                                     sensitivity=sensitivity, media_type=media, provenance=prov)
            ids.append(r["corpus_id"])
        summary = {"run_id": run_id, "format": fmt, "format_label": label, "file_name": rp.name, "file_sha256": sha,
                   "file_bytes": nbytes, "source": source, "scope": scope, "sensitivity": sensitivity,
                   "source_account": account or None, "ingested": len(ids), "third_party_items": third,
                   "skipped": skipped, "truncated_at_max_items": truncated, "grant_id": grants[0]["grant_id"],
                   "first_corpus_id": ids[0] if ids else None, "last_corpus_id": ids[-1] if ids else None}
        self.m.gov.record("IMPORT_RUN", actor, **summary)
        return dict(summary, corpus_ids=ids[:500])
