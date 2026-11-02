import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts.agent_workspace import canonical_hash, check_derived_counts, derived_counts, read_jsonl, route_messages
from scripts.semantic_validate import main as semantic_main, signature_report, validate_contribution_requests

ROOT = Path(__file__).resolve().parents[1]


class DerivedCountTests(unittest.TestCase):
    def test_repository_docs_match_derived_counts(self):
        self.assertEqual(check_derived_counts(ROOT), [])

    def test_agent_workspace_count_matches_directories(self):
        expected = sum(1 for p in (ROOT / "agents").iterdir() if p.is_dir() and not p.name.startswith((".", "_")))
        self.assertEqual(derived_counts(ROOT)["agent_workspaces"], expected)

    def test_stale_count_is_reported(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for name in ("alpha", "beta"):
                (root / "agents" / name).mkdir(parents=True)
            (root / "doc.md").write_text(
                "We have <!-- central:count agent_workspaces -->3<!-- /central:count --> agents.\n",
                encoding="utf-8")
            errors = check_derived_counts(root)
            self.assertEqual(len(errors), 1)
            self.assertIn("agent_workspaces=3", errors[0])
            self.assertIn("has 2", errors[0])

    def test_unknown_count_key_is_reported(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "doc.md").write_text("<!-- central:count widgets -->1<!-- /central:count -->", encoding="utf-8")
            self.assertTrue(any("unknown derived count" in e for e in check_derived_counts(root)))


class SignatureStubTests(unittest.TestCase):
    def test_report_counts_signed_and_unsigned_records(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            ledger = root / "shared" / "communications"
            ledger.mkdir(parents=True)
            (ledger / "log.jsonl").write_text(
                json.dumps({"sender": "a", "content": "x"}) + "\n"
                + json.dumps({"sender": "b", "content": "y", "sig": {"key_id": "k", "algorithm": "ed25519", "value": "AA"}}) + "\n",
                encoding="utf-8")
            report = signature_report(root)
            self.assertEqual(len(report), 1)
            self.assertIn("1 unsigned, 1 signed", report[0])
            self.assertIn("not yet verified", report[0])

    def test_check_signatures_is_warn_only(self):
        self.assertEqual(semantic_main(["--check-signatures"]), 0)


class RoutingTests(unittest.TestCase):
    def _tree(self, root: Path) -> None:
        for name in ("alpha", "beta"):
            (root / "agents" / name / "inbox").mkdir(parents=True)
        ledger = root / "shared" / "communications"
        ledger.mkdir(parents=True)
        lines = [
            {"timestamp": "2026-01-01T00:00:00Z", "sender": "alpha", "target": "all", "type": "update", "content": "old"},
            {"message_id": "M-1", "thread_id": "TH-1", "timestamp": "2026-01-02T00:00:00Z",
             "sender": "alpha", "target": "beta", "type": "query", "content": "new"},
        ]
        (ledger / "log.jsonl").write_text("".join(json.dumps(x) + "\n" for x in lines), encoding="utf-8")

    def test_from_line_routes_only_new_message_with_ids(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self._tree(root)
            self.assertEqual(route_messages(root, dry_run=True), (3, 2))
            self.assertEqual(route_messages(root, from_line=2), (1, 1))
            self.assertEqual(route_messages(root, from_line=2), (0, 0))
            inbox = read_jsonl(root / "agents" / "beta" / "inbox" / "messages.jsonl")
            self.assertEqual(len(inbox), 1)
            self.assertEqual(inbox[0]["source_message_id"], "M-1")
            self.assertEqual(inbox[0]["thread_id"], "TH-1")
            self.assertEqual(inbox[0]["source_ref"], "shared/communications/log.jsonl#L2")
            self.assertEqual(inbox[0]["authentication"], "unverified-ledger-claim")
            self.assertFalse((root / "agents" / "alpha" / "inbox" / "messages.jsonl").exists())

    def test_first_real_routed_message_is_in_glm_inbox(self):
        ledger = read_jsonl(ROOT / "shared" / "communications" / "log.jsonl")
        line = next(i for i, r in enumerate(ledger, 1) if r.get("message_id") == "M-20261022-001")
        inbox = read_jsonl(ROOT / "agents" / "glm" / "inbox" / "messages.jsonl")
        routed = [m for m in inbox if m.get("source_message_id") == "M-20261022-001"]
        self.assertEqual(len(routed), 1)
        self.assertEqual(routed[0]["source_ref"], f"shared/communications/log.jsonl#L{line}")
        self.assertEqual(routed[0]["sender_claim"], "grok")
        self.assertEqual(routed[0]["message_id"], canonical_hash(ledger[line - 1], line))


class DashboardCacheTests(unittest.TestCase):
    def test_every_page_loads_cache_before_its_own_scripts(self):
        for page in sorted((ROOT / "dashboard").glob("*.html")):
            html = page.read_text(encoding="utf-8")
            if "api.github.com" not in html:
                continue
            tag = '<script src="./api-cache.js"></script>'
            self.assertIn(tag, html, page.name)
            self.assertEqual(html.find("<script"), html.find(tag), f"{page.name}: cache must load first")

    @unittest.skipUnless(shutil.which("node"), "node not installed")
    def test_cache_behaviour_in_node(self):
        result = subprocess.run(["node", str(ROOT / "tests" / "dashboard_api_cache_check.js")],
                                capture_output=True, text=True, timeout=60)
        self.assertEqual(result.returncode, 0, result.stderr)


class ContributionRequestTests(unittest.TestCase):
    def _root(self, temp: str, record: dict) -> Path:
        root = Path(temp)
        (root / "shared" / "communications").mkdir(parents=True)
        (root / "shared" / "communications" / "threads.jsonl").write_text(
            json.dumps({"thread_id": "TH-1", "title": "t", "status": "open", "message_ids": [], "topic": "x"}) + "\n",
            encoding="utf-8")
        (root / "doc.md").write_text("x", encoding="utf-8")
        (root / "shared" / "contribution-requests.jsonl").write_text(json.dumps(record) + "\n", encoding="utf-8")
        return root

    def _record(self, **changes):
        base = {"id": "CR-1", "title": "t", "kind": "review", "target": "doc.md", "requested_by": "a",
                "requested_at": "2026-01-01T00:00:00Z", "status": "open", "claimed_by": [], "thread_id": "TH-1",
                "acceptance": "a", "updated_at": "2026-01-01T00:00:00Z", "evidence": []}
        base.update(changes)
        return base

    def test_repository_requests_are_valid(self):
        self.assertEqual(validate_contribution_requests(ROOT), [])

    def test_valid_request_passes(self):
        with tempfile.TemporaryDirectory() as temp:
            self.assertEqual(validate_contribution_requests(self._root(temp, self._record())), [])

    def test_claimed_without_claimant_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            errors = validate_contribution_requests(self._root(temp, self._record(status="claimed")))
            self.assertTrue(any("requires claimed_by" in e for e in errors))

    def test_done_needs_evidence_and_known_thread_and_target(self):
        with tempfile.TemporaryDirectory() as temp:
            record = self._record(status="done", claimed_by=["b"], thread_id="TH-9", target="../etc/passwd")
            errors = validate_contribution_requests(self._root(temp, record))
            self.assertTrue(any("done requires" in e for e in errors))
            self.assertTrue(any("unknown thread_id" in e for e in errors))
            self.assertTrue(any("does not exist" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
