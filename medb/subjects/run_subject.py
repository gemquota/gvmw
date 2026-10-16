#!/usr/bin/env python3
"""Run one Round 1 subject: build a MedB instance with the subject's component
bindings and config, drive it with its scenario, and write the runtime DB and
versioned snapshots to runs/<subject>/ (EXPERIMENTER-ONLY location).

    python subjects/run_subject.py C0 [--runs runs]
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "subjects"))

from medb.export import export  # noqa: E402
from medb.system import MedB, load_config  # noqa: E402
from medb.util import FixedClock  # noqa: E402

START = "2026-08-01T00:00:00Z"


def load_components(subject_dir: Path) -> dict:
    spec = importlib.util.spec_from_file_location("subject_components", subject_dir / "subject_components.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["subject_components"] = mod
    spec.loader.exec_module(mod)
    return mod.COMPONENTS


def subject_spec(sid: str) -> dict:
    return json.loads((ROOT / "subjects" / sid / "subject.json").read_text())


def open_subject(sid: str, db_path: str, clock) -> MedB:
    spec = subject_spec(sid)
    return MedB(db_path=db_path, clock=clock, seed=spec["seed"], config=load_config(overrides=spec["config_overrides"]),
                components=load_components(ROOT / "subjects" / sid))


def run(sid: str, runs: Path) -> dict:
    from scenarios import SCENARIOS
    out = runs / sid
    if out.exists():
        shutil.rmtree(out)
    (out / "snapshots").mkdir(parents=True)
    clock = FixedClock(START)
    m = open_subject(sid, str(out / "medb.sqlite"), clock)

    labels: list[str] = []

    def ckpt(label):
        # neutral, sequential snapshot names (scenario labels stay in run_meta only)
        labels.append(label)
        name = f"snapshot-{len(labels):02d}"
        export(m, out / "snapshots" / name, actor="system", destination_label=name)

    log = SCENARIOS[subject_spec(sid)["scenario"]](m, clock, ckpt)
    meta = {"subject": sid, "scenario": subject_spec(sid)["scenario"], "start": START, "end": clock.now_iso(),
            "snapshots": dict(zip((f"snapshot-{i:02d}" for i in range(1, len(labels) + 1)), labels)),
            "driver_log": log}
    (out / "run_meta.json").write_text(json.dumps(meta, indent=2))
    return meta


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("subject")
    ap.add_argument("--runs", default=str(ROOT / "runs"))
    a = ap.parse_args()
    meta = run(a.subject, Path(a.runs))
    print(json.dumps({k: v for k, v in meta.items() if k != "driver_log"}, indent=2))
