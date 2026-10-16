# Search indexes (owner: P1 (Ops) Mender)

Path required by Mender brief (`mender/v002`): "search indexes under /workspace/governance/index/, never indexing the codex or secrets."
Created 6 Oct 2026, 8:10am AEST after Scrutineer's third flag.

## Status: deferred (with reason)
No index built yet. Reasons:
1. Vector/graph tooling isn't set up on this computer, and there is no standing source feed.
2. Indexer's retired brief claimed the same path for knowledge indexes (including the codex). Mender's brief forbids indexing the codex or secrets. That boundary is one of Architect's pending "Mender state boundary" drafts. Until Gem approves it, this folder holds only this README.
3. Allowed future sources (once the boundary is clear): provenance ledger, identity profile, research reports, incidents. Not the codex, not secrets.

When an index is first built, add a dated subfolder and a one-line entry in `CHANGELOG.md` here. Never put secret values in any index file.
