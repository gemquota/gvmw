"""Append-only, hash-chained event store on SQLite.

* Every stream (``gov``, ``claims``, ``permissions``, ``policy``, ``suspension``,
  ``corpus``, ``delegation``) is an independent hash chain: each event's hash is
  ``sha256(canonical({"prev": prev_hash, "record": record}))`` where ``record``
  holds every stored field except the hash itself. This is the linear-chain
  variant of a tamper-evident log (Crosby & Wallach 2009 describe a Merkle
  history tree; the linear chain is the M0 simplification, see DECISIONS D-04).
* UPDATE and DELETE on ``events`` are refused by SQLite triggers.
* Erasable content lives in a separate ``content`` table, referenced from events
  only by a *salted* commitment, so destroying content (claim deletion) never
  breaks a chain and the commitment cannot be brute-forced back to the content.
"""
from __future__ import annotations

import json
import sqlite3
from typing import Any, Iterable

from .errors import AppendOnlyViolation
from .util import canonical, sha256_hex

GENESIS_HASH = "0" * 64

_SCHEMA = """
CREATE TABLE IF NOT EXISTS events (
    stream   TEXT NOT NULL,
    seq      INTEGER NOT NULL,
    event_id TEXT NOT NULL UNIQUE,
    ts       TEXT NOT NULL,
    kind     TEXT NOT NULL,
    actor    TEXT NOT NULL,
    body     TEXT NOT NULL,
    prev_hash TEXT NOT NULL,
    hash     TEXT NOT NULL,
    PRIMARY KEY (stream, seq)
);
CREATE TRIGGER IF NOT EXISTS events_no_update BEFORE UPDATE ON events
BEGIN SELECT RAISE(ABORT, 'events are append-only'); END;
CREATE TRIGGER IF NOT EXISTS events_no_delete BEFORE DELETE ON events
BEGIN SELECT RAISE(ABORT, 'events are append-only'); END;
CREATE TABLE IF NOT EXISTS content (
    ref  TEXT PRIMARY KEY,
    salt TEXT NOT NULL,
    body TEXT NOT NULL
);
CREATE TRIGGER IF NOT EXISTS content_no_update BEFORE UPDATE ON content
BEGIN SELECT RAISE(ABORT, 'content is immutable (erasable only)'); END;
"""


def event_hash(prev_hash: str, record: dict) -> str:
    return sha256_hex(canonical({"prev": prev_hash, "record": record}))


def content_ref(salt: str, body: Any) -> str:
    return "c-" + sha256_hex(salt + canonical(body))


class EventStore:
    def __init__(self, path: str = ":memory:"):
        self.path = path
        self.db = sqlite3.connect(path, check_same_thread=False)  # API server is single-threaded (D-55)
        self.db.executescript(_SCHEMA)
        self.db.commit()

    # ---- events -----------------------------------------------------------
    def head(self, stream: str) -> tuple[int, str]:
        row = self.db.execute(
            "SELECT seq, hash FROM events WHERE stream=? ORDER BY seq DESC LIMIT 1", (stream,)
        ).fetchone()
        return (row[0], row[1]) if row else (0, GENESIS_HASH)

    def append(self, stream: str, kind: str, actor: str, body: dict, ts: str, event_id: str) -> dict:
        seq, prev = self.head(stream)
        record = {"stream": stream, "seq": seq + 1, "event_id": event_id, "ts": ts,
                  "kind": kind, "actor": actor, "body": body}
        h = event_hash(prev, record)
        self.db.execute(
            "INSERT INTO events(stream,seq,event_id,ts,kind,actor,body,prev_hash,hash) VALUES (?,?,?,?,?,?,?,?,?)",
            (stream, seq + 1, event_id, ts, kind, actor, canonical(body), prev, h),
        )
        self.db.commit()
        return dict(record, prev_hash=prev, hash=h)

    def events(self, stream: str, until_ts: str | None = None, kinds: Iterable[str] | None = None) -> list[dict]:
        q = "SELECT stream,seq,event_id,ts,kind,actor,body,prev_hash,hash FROM events WHERE stream=?"
        args: list[Any] = [stream]
        if until_ts is not None:
            q += " AND ts<=?"
            args.append(until_ts)
        q += " ORDER BY seq"
        out = []
        kindset = set(kinds) if kinds else None
        for r in self.db.execute(q, args):
            if kindset and r[4] not in kindset:
                continue
            out.append({"stream": r[0], "seq": r[1], "event_id": r[2], "ts": r[3], "kind": r[4],
                        "actor": r[5], "body": json.loads(r[6]), "prev_hash": r[7], "hash": r[8]})
        return out

    def change_token(self, ignore_kinds: tuple[str, ...] = (), ignore_streams: tuple[str, ...] = ()) -> str:
        """Opaque token that changes whenever a (non-ignored) event is appended.
        Reveals nothing about record content (used by the app's live updates)."""
        rows = self.db.execute("SELECT stream, COUNT(*), MAX(seq) FROM events WHERE kind NOT IN (%s) GROUP BY stream"
                               % ",".join("?" * len(ignore_kinds)) if ignore_kinds else
                               "SELECT stream, COUNT(*), MAX(seq) FROM events GROUP BY stream",
                               tuple(ignore_kinds)).fetchall()
        import hashlib
        return hashlib.sha256(repr(sorted(r for r in rows if r[0] not in ignore_streams)).encode()).hexdigest()[:16]

    def streams(self) -> list[str]:
        return [r[0] for r in self.db.execute("SELECT DISTINCT stream FROM events ORDER BY stream")]

    def verify(self, stream: str) -> dict:
        prev = GENESIS_HASH
        n = 0
        for e in self.events(stream):
            n += 1
            record = {k: e[k] for k in ("stream", "seq", "event_id", "ts", "kind", "actor", "body")}
            if e["prev_hash"] != prev or event_hash(prev, record) != e["hash"] or e["seq"] != n:
                return {"stream": stream, "ok": False, "first_bad_seq": e["seq"], "length": n}
            prev = e["hash"]
        return {"stream": stream, "ok": True, "first_bad_seq": None, "length": n, "head": prev}

    def raw_update_for_tamper_test(self, stream: str, seq: int, body: dict) -> None:
        """Test-only: simulate out-of-band tampering by dropping the trigger.

        Exists so tests can prove the chain detects tampering; nothing in the
        runtime calls it."""
        self.db.execute("DROP TRIGGER events_no_update")
        self.db.execute("UPDATE events SET body=? WHERE stream=? AND seq=?", (canonical(body), stream, seq))
        self.db.commit()

    # ---- erasable content -------------------------------------------------
    def put_content(self, body: Any, salt: str) -> str:
        ref = content_ref(salt, body)
        self.db.execute("INSERT OR IGNORE INTO content(ref,salt,body) VALUES (?,?,?)", (ref, salt, canonical(body)))
        self.db.commit()
        return ref

    def get_content(self, ref: str) -> Any | None:
        row = self.db.execute("SELECT body FROM content WHERE ref=?", (ref,)).fetchone()
        return json.loads(row[0]) if row else None

    def erase_content(self, ref: str) -> bool:
        cur = self.db.execute("DELETE FROM content WHERE ref=?", (ref,))
        self.db.commit()
        return cur.rowcount > 0

    def all_content(self) -> dict[str, dict]:
        return {r[0]: {"salt": r[1], "body": json.loads(r[2])}
                for r in self.db.execute("SELECT ref,salt,body FROM content ORDER BY ref")}

    def guard_append_only(self) -> None:
        """Assert triggers are installed (used by integrity checks)."""
        names = {r[0] for r in self.db.execute("SELECT name FROM sqlite_master WHERE type='trigger'")}
        for t in ("events_no_update", "events_no_delete"):
            if t not in names:
                raise AppendOnlyViolation(f"append-only trigger {t} missing")
