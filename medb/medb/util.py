"""Small shared utilities: canonical JSON, hashing, clocks, identifiers."""
from __future__ import annotations

import datetime as _dt
import hashlib
import json
import random
import secrets
from typing import Any

UTC = _dt.timezone.utc


def canonical(obj: Any) -> str:
    """Canonical JSON: sorted keys, no insignificant whitespace, UTF-8."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_hex(data: str | bytes) -> str:
    if isinstance(data, str):
        data = data.encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def digest(obj: Any) -> str:
    return sha256_hex(canonical(obj))


def iso(t: _dt.datetime) -> str:
    """Render an aware datetime as fixed-width UTC ISO-8601 (lexically sortable)."""
    if t.tzinfo is None:
        raise ValueError("naive datetime not allowed")
    return t.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def parse_iso(s: str) -> _dt.datetime:
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    t = _dt.datetime.fromisoformat(s)
    if t.tzinfo is None:
        raise ValueError("timestamp must carry a zone")
    return t.astimezone(UTC)


def norm_ts(s: str | _dt.datetime | None) -> str | None:
    """Normalise a timestamp argument (str or datetime) to canonical ISO form."""
    if s is None:
        return None
    if isinstance(s, _dt.datetime):
        return iso(s)
    return iso(parse_iso(s))


class Clock:
    def now(self) -> _dt.datetime:  # pragma: no cover - interface
        raise NotImplementedError

    def now_iso(self) -> str:
        return iso(self.now())


class SystemClock(Clock):
    def now(self) -> _dt.datetime:
        return _dt.datetime.now(UTC)


class FixedClock(Clock):
    """Deterministic clock for tests and scripted subject scenarios."""

    def __init__(self, start: str | _dt.datetime = "2026-08-01T00:00:00Z"):
        self._t = parse_iso(start) if isinstance(start, str) else start.astimezone(UTC)

    def now(self) -> _dt.datetime:
        return self._t

    def advance(self, **kw) -> _dt.datetime:
        self._t = self._t + _dt.timedelta(**kw)
        return self._t

    def set(self, t: str | _dt.datetime) -> None:
        self._t = parse_iso(t) if isinstance(t, str) else t.astimezone(UTC)


class IdGen:
    """Identifier source. Deterministic when seeded (reproducible subjects)."""

    def __init__(self, seed: int | None = None):
        self._rng = random.Random(seed) if seed is not None else None

    def new(self, prefix: str) -> str:
        if self._rng is None:
            return f"{prefix}-{secrets.token_hex(8)}"
        return f"{prefix}-{self._rng.getrandbits(64):016x}"

    def salt(self) -> str:
        if self._rng is None:
            return secrets.token_hex(16)
        return f"{self._rng.getrandbits(128):032x}"
