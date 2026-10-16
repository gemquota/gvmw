#!/usr/bin/env python3
"""EXPERIMENTER-ONLY: summarise subject runs so the experimenter can confirm
each variant manifests (or not) as designed. Never part of an envelope."""
import collections
import json
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def gov(db):
    con = sqlite3.connect(db)
    return [(k, a, json.loads(b)) for k, a, b in con.execute("SELECT kind, actor, body FROM events WHERE stream='gov' ORDER BY seq")]


def summarize(sid):
    es = gov(ROOT / "runs" / sid / "medb.sqlite")
    ev = [b for k, a, b in es if k == "ACTION_EVALUATED"]
    clauses = collections.Counter(f"{b['decision']}:{b['clause']}" for b in ev)
    pc = [(a, b["document"], b["version"]) for k, a, b in es if k == "POLICY_CHANGE"]
    pk = [b for k, a, b in es if k == "CONTEXT_PACKAGE_ISSUED"]
    emerg_exec = sum(1 for k, a, b in es if k == "ACTION_EXECUTED" and b["emergency"])
    return {"subject": sid, "decisions": dict(clauses), "policy_changes": pc,
            "emergency_executed": emerg_exec, "packages": len(pk),
            "packages_with_ranking_inputs": sum(1 for p in pk if "inputs" in p["ranking"]),
            "ranking_weights": pk[0]["ranking"].get("weights") if pk else None,
            "first_orders": [p["ranking"]["order"][:4] for p in pk[:1]],
            "underdetermination": [b.get("section_iii_ref") for k, a, b in es if k == "AUTHORITY_UNDERDETERMINATION"],
            "suspensions": [b["record"]["capability"] + "/" + b["record"]["classification"] for k, a, b in es if k == "SUSPENSION"],
            "breaches": sum(1 for k, a, b in es if k == "OBLIGATION_BREACHED")}


if __name__ == "__main__":
    for sid in sys.argv[1:] or sorted(p.name for p in (ROOT / "runs").iterdir()):
        print(json.dumps(summarize(sid)))
