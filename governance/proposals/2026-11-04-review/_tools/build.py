#!/usr/bin/env python3
"""4 Nov 2026 review follow-up. Hashes drafts in this folder. Reads codex/ only for base verify. No tokens. Do not record/deploy/commit/push."""
import re, hashlib, json
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
G = Path("/workspace/governance")

def fence_text(path: Path) -> str:
    m = re.search(r"```text\n(.*)\n```", path.read_text(), re.S)
    if not m:
        raise SystemExit(f"no Exact text fence in {path}")
    return m.group(1)

def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def main():
    results = {}
    for path in sorted(HERE.glob("*.md")):
        if path.name == "README.md":
            continue
        text = fence_text(path)
        results[path.name] = {
            "text_sha256": sha(text.encode()),
            "file_sha256": sha(path.read_bytes()),
            "text_bytes": len(text.encode()),
            "file_bytes": path.stat().st_size,
        }
    out = HERE / "_tools" / "hashes.json"
    out.write_text(json.dumps(results, indent=2) + "\n")
    for name, h in results.items():
        print(name)
        print("  text", h["text_sha256"])
        print("  file", h["file_sha256"])
    bases = {
        "deterministic-checks/v002": G / "codex/_shared/deterministic-checks/v002.md",
        "codey/v009": G / "codex/codey/v009.md",
    }
    print("BASES")
    for name, p in bases.items():
        print(" ", name + ":", sha(fence_text(p).encode()))

if __name__ == "__main__":
    main()
