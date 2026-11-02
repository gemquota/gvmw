#!/usr/bin/env python3
"""Validate Central's explicit semantic substrate.

Standard-library only. This validates repository data; it does not authenticate
authors or make inferred relationships authoritative.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

PROVENANCE = {"declared", "observed", "evidenced", "inferred", "unknown_disputed"}


def jsonl(path: Path):
    with path.open(encoding="utf-8") as f:
        for line_no, raw in enumerate(f, 1):
            if not raw.strip():
                continue
            try:
                value = json.loads(raw)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_no}: invalid JSON: {exc.msg}") from exc
            if not isinstance(value, dict):
                raise ValueError(f"{path}:{line_no}: record must be an object")
            yield line_no, value


def validate_documents(root: Path):
    errors = []
    ids = set()
    path = root / "shared/knowledge/documents.jsonl"
    for line, item in jsonl(path):
        for field in ("id", "type", "title", "provenance_type", "status"):
            if not isinstance(item.get(field), str) or not item[field]:
                errors.append(f"{path}:{line}: missing/invalid {field}")
        if item.get("id") in ids:
            errors.append(f"{path}:{line}: duplicate id {item['id']!r}")
        ids.add(item.get("id"))
        if item.get("provenance_type") not in PROVENANCE:
            errors.append(f"{path}:{line}: invalid provenance_type")
    return errors, ids


def validate_relations(root: Path, known_ids: set[str]):
    errors = []
    ids = set()
    path = root / "shared/knowledge/relations.jsonl"
    for line, item in jsonl(path):
        for field in ("id", "subject", "predicate", "object", "provenance_type", "status"):
            if not isinstance(item.get(field), str) or not item[field]:
                errors.append(f"{path}:{line}: missing/invalid {field}")
        if item.get("id") in ids:
            errors.append(f"{path}:{line}: duplicate relation id {item['id']!r}")
        ids.add(item.get("id"))
        if item.get("provenance_type") not in PROVENANCE:
            errors.append(f"{path}:{line}: invalid provenance_type")
        for field in ("subject", "object"):
            value = item.get(field)
            if value not in known_ids:
                errors.append(f"{path}:{line}: {field} references unknown entity {value!r}")
    return errors


def validate_events(root: Path):
    errors = []
    for relative, fields in {
        "shared/state/events.jsonl": ("id", "timestamp", "type", "summary", "actors", "source_refs"),
        "shared/state/snapshots.jsonl": ("id", "timestamp", "label", "source_commit", "state_file"),
        "shared/decisions.jsonl": ("id", "timestamp", "decision", "context", "alternatives", "rationale", "status", "affected_goals", "evidence", "review_trigger"),
        "shared/communications/threads.jsonl": ("thread_id", "title", "status", "message_ids", "topic"),
    }.items():
        path = root / relative
        ids = set()
        for line, item in jsonl(path):
            for field in fields:
                if field not in item:
                    errors.append(f"{path}:{line}: missing {field}")
            key = item.get(fields[0])
            if key in ids:
                errors.append(f"{path}:{line}: duplicate id {key!r}")
            ids.add(key)
    return errors


CR_KINDS = {"project", "research", "review", "decision", "implementation", "other"}
CR_STATUSES = {"open", "claimed", "in_progress", "in_review", "done", "withdrawn", "declined"}
CR_REQUIRED = ("id", "title", "kind", "target", "requested_by", "requested_at", "status",
               "claimed_by", "thread_id", "acceptance", "updated_at")


def validate_contribution_requests(root: Path):
    """Check shared/contribution-requests.jsonl against system/contribution-requests.md."""
    path = root / "shared/contribution-requests.jsonl"
    if not path.exists():
        return []
    threads_path = root / "shared/communications/threads.jsonl"
    threads = {item.get("thread_id") for _, item in jsonl(threads_path)} if threads_path.exists() else set()
    errors, ids = [], set()
    for line, item in jsonl(path):
        missing = [f for f in CR_REQUIRED if f not in item]
        if missing:
            errors.append(f"{path}:{line}: missing {', '.join(missing)}")
            continue
        if item["id"] in ids:
            errors.append(f"{path}:{line}: duplicate id {item['id']!r}")
        ids.add(item["id"])
        if item["kind"] not in CR_KINDS:
            errors.append(f"{path}:{line}: invalid kind {item['kind']!r}")
        if item["status"] not in CR_STATUSES:
            errors.append(f"{path}:{line}: invalid status {item['status']!r}")
        if not isinstance(item["claimed_by"], list):
            errors.append(f"{path}:{line}: claimed_by must be an array")
        elif item["status"] in {"claimed", "in_progress", "in_review", "done"} and not item["claimed_by"]:
            errors.append(f"{path}:{line}: status {item['status']!r} requires claimed_by")
        if item["status"] == "done" and (not item.get("completed_at") or not item.get("evidence")):
            errors.append(f"{path}:{line}: done requires completed_at and evidence")
        if item["thread_id"] not in threads:
            errors.append(f"{path}:{line}: unknown thread_id {item['thread_id']!r}")
        target = str(item["target"])
        if target.startswith("/") or ".." in Path(target).parts or not (root / target).exists():
            errors.append(f"{path}:{line}: target {target!r} does not exist in the repository")
    return errors


SIGNED_LEDGERS = ("shared/communications/log.jsonl", "shared/communications/forum.jsonl")


def signature_report(root: Path) -> list[str]:
    """Warn-only stub for system/sender-authentication.md. Never produces errors.

    Counts records that carry a `sig` object. Cryptographic verification is not
    implemented yet, so a present signature is reported as unverified.
    """
    warnings = []
    for relative in SIGNED_LEDGERS:
        path = root / relative
        if not path.exists():
            continue
        signed = unsigned = 0
        try:
            for _, item in jsonl(path):
                if isinstance(item.get("sig"), dict):
                    signed += 1
                else:
                    unsigned += 1
        except ValueError as exc:
            warnings.append(f"{relative}: cannot check signatures: {exc}")
            continue
        warnings.append(
            f"{relative}: {unsigned} unsigned, {signed} signed (signatures not yet verified; see system/sender-authentication.md)"
        )
    return warnings


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    root = Path(__file__).resolve().parents[1]
    errors = []
    try:
        document_errors, ids = validate_documents(root)
        errors.extend(document_errors)
        errors.extend(validate_relations(root, ids))
        errors.extend(validate_events(root))
        errors.extend(validate_contribution_requests(root))
    except (OSError, ValueError) as exc:
        errors.append(str(exc))
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        print(f"Semantic validation failed: {len(errors)} issue(s).")
        return 1
    print("Semantic validation passed.")
    if "--check-signatures" in argv:
        for warning in signature_report(root):
            print(f"WARN (advisory): {warning}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
