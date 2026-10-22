# Off-box, append-only, hash-chained governance snapshot: plan
Engineer, 22 Oct 2026 AEST. P0 "independent external backup of governance" (review findings 5 and 6). This is a plan only.

## Goals
- A copy of governance that lives off this box and that no single bot can quietly edit or delete.
- Each snapshot commits to the previous one by hash, so gaps, edits and reordering are detectable.
- No secrets or private data in it (lesson from the gvmw audit).

## What goes in: an allowlist, not a denylist
Include: `governance/{rulings,phases,schedule,directory,approvals,connectors}.md`, `codex/**`, `incidents/**`, `reviews/**`, `assessments/**`, `digest/sent/**`, `digest/inbox/**`, `state/**`, `costs/**` (amounts only), `risk/**`, `proposals/**`.
Exclude always: `id-series/**`, `secrets-inventory.md`, `security/**` detail (keep only hashes), anything matching gitleaks rules, `*.bak*` and `_archive/**` (the chain replaces backups), BIE material, email addresses and phone numbers other than Gem's (redact them to `***`).
Gate: before a snapshot is sealed, `gitleaks dir` plus a PII regex pass must come back clean. Otherwise the snapshot is refused and the watchdog alerts.

## Chain format
Each run writes `manifests/<UTC-timestamp>.json`:
```json
{"seq": 42, "taken_at": "2026-10-23T08:45:00+10:00", "prev_manifest_sha256": "<hash of manifest 41>",
 "files": {"governance/rulings.md": "<sha256>", "...": "..."},
 "excluded_count": 17, "scanner": "gitleaks 8.21.2 clean", "host": "box"}
```
`manifest_sha256 = sha256(canonical JSON)`. The chain head is also written to `HEAD.txt`. A verifier recomputes the whole chain and the file hashes. The verifier runs off box, inside the GitHub Action from the watchdog plan. Optional: put the daily head hash in Gem's inbox (one line, sent by the watchdog service) as an outside witness.

## Storage options
| Option | Append-only how | Pros | Cons | Cost |
|---|---|---|---|---|
| **A. Private GitHub repo `gemquota/governance-snapshot`** (recommended to start) | Branch protection on `main`: no force push, no deletion, linear history, signed commits. Push with a fine-grained token scoped to this repo, contents write only. Admin stays with Gem | Free, versioned, diffable. Fits the watchdog (B) | An admin token can lift protection. Bots must never hold an admin-scope token (P0 token rotation) | Free |
| B. Google Drive with versioning | One file per manifest. Drive keeps revisions | Gem already uses Drive. Easy to browse | Not really append-only: the connector can trash files. Revisions expire after 30 days or 100 versions unless "keep forever" | Free up to 15 GB |
| C. Object storage with retention lock (Backblaze B2 Object Lock, AWS S3 Object Lock in compliance mode, Cloudflare R2 bucket lock) | WORM retention, for example 1 year. Even the account owner can't delete early in compliance mode | Strongest guarantee. Cheap | Needs a cloud account and a write-only key. A little more setup | B2 about US$6/TB/mo, so cents for us. S3 similar. R2 has a free tier |
| D. A + C | Repo for reading. Object Lock for the immutable copy | Best of both | Two moving parts | Cents a month |

Recommendation: start with A, add C when Gem is ready. Keep Drive (B) only as a convenience mirror.

## Who can do what
- Writer: one snapshot job with a write-only, single-target credential that cannot delete. It is not Mender, so the review's circularity is avoided.
- Verifier: the off-box GitHub Action. Read-only.
- Restore authority: Gem. Restores are pulled from the snapshot by Gem's instruction, with a Safeguard dry run.

## Needs Gem
Create the private repo and turn on branch protection, or pick C. Make the scoped token yourself, Gem, and don't reuse any existing wide token. Approve the allowlist. Approve the new routine. I can then write `snapshot.py` (build, scan, chain) with a dry-run mode. It isn't built yet, because the target choice decides its push step.
