#!/usr/bin/env python3
"""The independent appointer's tool (F-04, D-69). Run by the outside party, not by MedB.

    appointer.py keygen --id appointer:<name> --key KEYFILE [--config data/appointer.json]
        Creates a 32-byte HMAC key (hex, mode 0600) and the appointer config MedB reads
        (``{id, key_fingerprint, method, verify_key_file}``). A new database records this
        at genesis; a database created before F-04 binds it once (APPOINTER_BOUND) and
        refuses any later different appointer.
    appointer.py appoint --id appointer:<name> --key KEYFILE --auditor auditor:<id> [--expires ISO]
    appointer.py revoke  --id appointer:<name> --key KEYFILE --appointment appt-...
        Prints a JSON body ``{statement, signature}`` to POST to /api/auditors/statement
        (any token may carry it; the carrier gains nothing).

M0 limitation: HMAC-SHA256 is symmetric, so MedB's verify key is the signing key. Whoever
can read the key file on the MedB machine could forge appointments. Keep it readable only
by the appointer (and the MedB process); replace with asymmetric signatures later.
"""
import argparse, json, os, secrets, sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from medb.auditors import METHOD, key_fingerprint, new_statement, read_key, sign_statement  # noqa: E402


def _now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("keygen", "appoint", "revoke"):
        p = sub.add_parser(name)
        p.add_argument("--id", required=True, help="appointer id, e.g. appointer:acme-audit")
        p.add_argument("--key", required=True, help="key file (hex)")
        if name == "keygen":
            p.add_argument("--config", default="data/appointer.json")
        if name == "appoint":
            p.add_argument("--auditor", required=True)
            p.add_argument("--expires", default=None)
            p.add_argument("--scope", default=None)
        if name == "revoke":
            p.add_argument("--appointment", required=True)
    a = ap.parse_args(argv)
    if a.cmd == "keygen":
        kp = Path(a.key)
        if kp.exists():
            sys.exit(f"refusing to overwrite existing key {kp}")
        kp.parent.mkdir(parents=True, exist_ok=True)
        fd = os.open(kp, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        key = secrets.token_bytes(32)
        os.write(fd, key.hex().encode()); os.close(fd)
        cfg = {"id": a.id, "key_fingerprint": key_fingerprint(key), "method": METHOD,
               "verify_key_file": str(kp.resolve())}
        cp = Path(a.config); cp.parent.mkdir(parents=True, exist_ok=True)
        cp.write_text(json.dumps(cfg, indent=2) + "\n")
        print(json.dumps(cfg, indent=2))
        return 0
    key = read_key(a.key)
    if a.cmd == "appoint":
        st = new_statement("APPOINT", a.id, auditor_id=a.auditor, issued_at=_now(), expires_at=a.expires, scope=a.scope)
    else:
        st = new_statement("REVOKE", a.id, appointment_id=a.appointment, issued_at=_now())
    print(json.dumps({"statement": st, "signature": sign_statement(key, st)}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
