# Phase-to-deployment cleanup and similar redundancy — assessment, 22 Oct 2026
Compiled about 10:55pm AEST (UTC+10) by Grok Bot. **Read-only: nothing was deleted or moved.** It covers `/workspace/governance` and the public repo `gemquota/swarm` (a fresh read-only clone in `/tmp/swarm-check`). The live references come from searching the 12 active bots' live profile descriptions (`/home/box/agent-data/agents/*/profile.json`), the highest version of each shared rule, and `rulings/in-force.md`. "None found" means a text search found no match. Briefs can describe a file without naming it, so the owner should confirm before archiving.
Archive means moving to `_archive/` with a backup and verified counts, as the redesign's resilience rule asks. Nothing should be deleted outright.

## Urgent

`phases.md` was moved tonight, but **live briefs still point to `/workspace/governance/phases.md`**: live briefs: Archivist, Emissary, Explorer, Scrutineer; binding docs: in-force.md. Those bots will now find no file. Architect should update the briefs, or the file should be restored, until that's done.

## B — Needs a brief or ruling change first (a live brief or binding doc points to it)

| # | Path | Why redundant / why keep | Size | Owner | Live references |
|---|---|---|---|---|---|
| B1 | `_archive/phases-retired-2026-10-22/phases.md (moved from phases.md tonight)` | Phase tracker; all five phases live, roster now 12. **Already moved, but live briefs still point to `/workspace/governance/phases.md`**, so those pointers are now broken. | 3 KB | Explorer | live briefs: Archivist, Emissary, Explorer, Scrutineer; binding docs: in-force.md |
| B2 | `"Dormant bot" rules (R-013 and the dormant clauses in live briefs)` | No bot is dormant since P5 went live 16 Oct; the clauses only govern a state that can no longer happen. Rule R-013 lives in rulings.md / in-force.md. | — | Arbiter (R-013); Architect (brief text) | live briefs: Emissary, Engineer, Explorer, Inferer, Safeguard; binding docs: in-force.md, shared/handoff-phase1 |
| B3 | `Phase prefixes in live bot names ("P1 (Checks) Safeguard" … "P5 (Work) Engineer")` | Prefixes encode rollout phase, which no longer means anything operationally. Changing them is a live-profile rename (needs approval and Archivist apply) and briefs/rulings cite names with prefixes. | — | Archivist (apply) with Gem/Imitator approval | live briefs: Architect, Archivist; binding docs: shared/collaboration-map, shared/connector-limits, shared/github, shared/handoff-phase1, shared/message-verification-rule |
| B4 | `"until P4 goes live" / "once P4 is live" conditional clauses in briefs` | Conditions on a phase that started 15 Oct; text can be simplified to the post-P4 rule. | — | Architect | live briefs: Arbiter, Architect, Archivist, Emissary, Engineer, Explorer, Imitator, Inferer, Investigator, Mender, Scrutineer; binding docs: shared/collaboration-map, shared/connector-limits, shared/handoff-phase1, shared/message-verification-rule |
| B5 | `handover/explorer-handover-2026-10-09.md` | One-off handover from the old Explorer (82a2c15a, gone). Explorer's live brief still tells it to read this file. | 5 KB | Explorer | live briefs: Explorer |

## A — Safe to archive now (no live brief or binding reference found)

| # | Path | Why redundant / why keep | Size | Owner | Live references |
|---|---|---|---|---|---|
| A0 | `codex/_shared/handoff-phase1/ (v001 + CHANGELOG)` | Phase-gate handoff spec from 4 Oct; describes P1 handoff and dormant phases that have all finished. | 5 KB | Archivist records; Gem approved | none found (the only match is the file itself) |
| A1 | `proposals/handoff-phase1-v001.md, proposals/phase1-interim-bundle-v001.md, proposals/final-2026-10-04/handoff-phase1-final.md` | Drafts of the phase-1 handoff, superseded by the recorded shared v001. | 9 KB | Architect | binding docs: shared/handoff-phase1 |
| A2 | `schedule.md.bak-p1` | Backup of the schedule from the P1 rollout. | — | Mender | none found |
| A3 | `Public repo: phase sections in governance/master/*.html (Part 2.1 phase tracker etc.)` | My compiled editions reproduce phases.md; on the next rebuild I can drop it. Push needs Engineer and Gem. | — | Grok Bot (compiler) / Engineer (push) | not applicable (content edit) |
| A4 | `proposals/2026-10-09-retire-merge/` | Retire/merge list applied 9 Oct 9:14am. | 55 KB | Architect | none found |
| A5 | `proposals/merge-F-unretire-assembler-2026-10-04.md` | Merge F applied 4 Oct; Assembler since retired. | 5 KB | Architect | binding docs: shared/handoff-phase1 |
| A6 | `proposals/2026-10-22-redundancy/` | Batch deployed 7:57pm; leftovers superseded by the redesign (redesign README). | 151 KB | Architect | none found |
| A7 | `proposals/2026-10-22-redesign/ (incl. _pre832, _prefinal, _r1–_r3)` | Batch recorded 9:45pm and deployed ~10:18–10:21pm; five merges done 10:42pm. | 678 KB | Architect | none found |
| A8 | `proposals/2026-10-22-r044-veto/, proposals/2026-10-16-github/, proposals/2026-10-22-gvmw/` | Recorded and deployed by 9:43pm (r044–r047, GitHub 5h, connector limits v003 Variant A); variants B/C not approved. | 199 KB | Architect | binding docs: shared/github, shared/message-verification-rule |
| A9 | `proposals/2026-10-05/, 2026-10-06/, 2026-10-09/, 2026-10-15/, 2026-10-16/, 2026-10-16-rr028/, 2026-10-16-deploy/, 2026-10-16-investigator/, 2026-10-16-connectors2/, final-2026-10-04/, imitator-approver-2026-10-04/, rolemap-v3-fixes-2026-10-04/` | Batches recorded (codex index) or superseded by later versions. | 73 KB | Architect | binding docs: shared/collaboration-map, shared/confirm-deployment, shared/github, shared/handoff-phase1, shared/message-verification-rule |
| A10 | `proposals/*-v002.md and single drafts for retired or rebriefed bots (clone-accuracy-validator, comms-concierge, cost-budget-sentinel, genesis-gang-god, governance-continuity-deputy, orchestration-conductor, connector-steward, secrets-credentials-custodian, auditor, compliance-risk-officer, codex-keeper, archivist-brief, codey.md, grok-bot.md, scraper.md, APPROVED-for-archivist-2026-10-04.md, agent-message-verification-rule-v001.md, collaboration-map.md/.png)` | Early-October drafts, all superseded by recorded codex versions; several bots retired. | — | Architect | none found |
| A11 | `proposals/2026-10-22-adversarial-response/ (plan.md + 3 .bak, README, arbiter-section, gem-answers)` | Response plan executed through the redesign; plan still contains healthchecks.io steps Gem scrapped at 8:28pm. Gem-answers file is evidence cited by R-051: archive, don't lose. | 103 KB | Architect / Arbiter | none found |
| A12 | `proposals/2026-10-10-backlog-triage.md` | 10 Oct triage; items resolved by later rulings (R-030, R-033) and deploys. | 15 KB | Explorer | none found |
| A13 | `codex/PENDING-FOR-ARBITER.md, codex/PENDING-FOR-ASSEMBLER.md` | Early October queues; Assembler retired 9 Oct; Arbiter items ruled (R-001–R-017). | 21 KB | Archivist | none found |
| A14 | `/home/box/agent-data/agents/6b01a4ef-… (and sand-data copy)` | New Bot retired 22 Oct; only empty assets/ and attachments/ remain. Deletion is Gem's (sidebar). | missing | Gem | none found |
| A15 | `risk/2026-10-22-liveness-watchdog-plan.md` | Plan implemented (watchdog installed 22 Oct; README in /workspace/watchdog is the live doc). | 2 KB | Safeguard | none found |
| A16 | `risk/2026-10-22-destructive-ops-gate.md` | Gem answered "Not now" (R-051). Deferred, not rejected: archive with a note so it can be revived. | 4 KB | Safeguard | none found |
| A17 | `archive/rulings-2026-10-22-pre-consolidation.md, root *.bak files (directory.md.bak-0909, -1504; schedule.md.bak-*), risk/register.md.bak-20261016` | Backups sitting outside _archive. | 74 KB | Archivist / Mender / Safeguard | not applicable (content edit) |
| A18 | `cartography v1–v21 versioned outputs (*-vN.mmd/.png/.svg/.html/.json, README/findings/summaries -vN)` | Superseded role-map versions (about 28 MB). README says "v1–vN kept as *-vN.*" by design, so move only with Archivist. | — | Archivist | none found |

## A2 — Edit in place by the owner (file stays; remove stale phase/retired content)

| # | Path | Why redundant / why keep | Size | Owner | Live references |
|---|---|---|---|---|---|
| A21 | `directory.md: per-phase headings ("### P1: live (7)" …) and "Active bots (17)"` | Roster grouped by rollout phase; stale count; retired five still listed under live phases. Edit in place (directory.md itself stays; briefs point to it). | — | Archivist | not applicable (content edit) |
| A22 | `codex/RENAMES.md section "Phase prefixes, 2026-10-04"` | History of the phase-prefix rename; only needed while names carry prefixes. Keep the old-name table above it (still the key for codex folder names). | missing | Archivist | live briefs: Archivist, Explorer |
| A23 | `rulings/in-force.md "P1 to P5" short-code entry (also published on gemquota/swarm)` | Defines phases that are all live; can say "historical". | missing | Arbiter | not applicable (content edit) |
| A24 | `Public repo: governance/cartography/role-map-interactive.html phase tiers and "dormant" legend` | Map groups bots by phase and has a dormant style; also still shows the five retired bots as live (built 10:24pm). | — | Archivist | not applicable (content edit) |
| A25 | `state/open.md stale "awaiting Gem" items` | Several waits were decided tonight (redesign, retirements, gvmw); last updated 6:45pm. | missing | Mender | not applicable (content edit) |
| A26 | `schedule.md entries for Scorer, Mediator, Safekeeper, Inquirer, Extractor (24 mentions)` | Routines of bots retired 10:42pm; duties now with Scrutineer, Mender, Safeguard, Inferer, Emissary. | — | Mender | not applicable (content edit) |
| A27 | `connectors.md and directory.md mentions of the five retired bots as owners` | Owner columns now point at retired bots. | — | Mediator→Mender (connectors), Archivist (directory) | not applicable (content edit) |

## C — Keep

| # | Path | Why redundant / why keep | Size | Owner | Live references |
|---|---|---|---|---|---|
| C1 | `codex/<retired bot folders> (advocate … swarm-builder, assessor, connector-steward, secrets-credentials-custodian, identity-inquirer, scraper, genesis-gang-god)` | Codex history is kept by rule (codex index: "History kept"; R-035 write-once). Retirement notices are the proof of retirement. | — | Archivist | not applicable (content edit) |
| C2 | `codex/_shared/collaboration-map/v001.md` | Still the highest version of a shared design doc; mentions phases and retired bots but no replacement exists. Candidate for a rewrite, not removal. | 4 KB | Architect / Archivist | binding docs: shared/collaboration-map |
| C3 | `assessments/, costs/, id-series/log.md, digest/, incidents/, approvals/, ledger/` | Records of retired bots' past duties; evidence for rulings, R-029 and audits. Ownership passed to the merge targets (Scrutineer, Mender, Inferer). | 71 KB | merge targets | live briefs: Inferer, Mender, Scrutineer; binding docs: shared/handoff-phase1 |
| C4 | `proposals/2026-10-22-clarity/, proposals/2026-10-22-PASTE-LINES.md, proposals/2026-10-22-token-rotation/` | Clarity batch not yet approved; paste lines still in use; token rotation stage 1 was approved by Gem ("Start stage 1 now") and is in progress (owner now Safeguard after Safekeeper merged). | 494 KB | Architect / Safeguard | not applicable (content edit) |
| C5 | `proposals/voice-call-messaging-v001.md` | No codex record of it found; may be live as copied brief lines (voice-call notes in 4 briefs). Status unclear: ask Architect before archiving. | 29 KB | Architect | live briefs: Inferer; binding docs: in-force.md, shared/message-verification-rule |
| C6 | `codex/_shared/deterministic-checks, approval-objects, resilience (healthchecks.io mentions)` | These only record that Gem scrapped healthchecks.io; that is correct current text, not a plan. | 11 KB | Archivist | not applicable (content edit) |
| C7 | `codex/_tools/ (verify.py, manifests, doc_sync)` | Deploy manifests are evidence; verify.py is used to check live vs codex. | 1.5 MB | Archivist | not applicable (content edit) |

## Public repo gemquota/swarm (read-only check)

- The site has no standalone phase files. Phase content reaches it through: the master editions (Part 2's phase tracker; group and phase labels on every bot), the role-map phase tiers and "dormant" legend, and the P1–P5 entry in `governance/rulings/in-force.md`. They are listed in the tables above under "Public repo" and "rulings/in-force.md".
- The two review reports (10 Oct and 15 Oct) are dated snapshots that describe phases P3/P4 going live. Keep them, labelled as dated, or retire them from the index page.
- Removing anything from the public repo is a push. That's Engineer's job, on Gem's words.

## Counts

- B (brief or ruling change first): 5
- A (safe to archive now): 19
- A2 (owner edits in place): 7
- C (keep): 7

## Cleanup carried out (22 Oct 2026, about 10:55–10:58pm AEST)

On Gem's 10:53pm words, "Yes, archive the 19 safe items (moved, not deleted)", group A was **moved, not deleted** to `_archive/cleanup-2026-10-22/<original path>`. The manifest, with per-file sha256 written before the move and re-verified after it, is `_archive/cleanup-2026-10-22/MANIFEST.md`.

- **Moved:** 48 paths, 139 files, 1,452,898 bytes. All hashes match at the new location.
  - In full: A0, A1, A2, A4, A5, A11, A12, A13, A15, A16 and A17.
  - In part: A9 (minus 2026-10-06 and final-2026-10-04) and A10 (minus collaboration-map.md).
- **Skipped because a binding shared rule still cites them:**
  - `proposals/2026-10-16-github` (shared github and message-verification-rule)
  - `proposals/2026-10-06` (confirm-deployment)
  - `proposals/final-2026-10-04` (collaboration-map; it also holds `handoff-phase1-final.md`)
  - `proposals/collaboration-map.md` (collaboration-map)
- **Skipped because they are read-only (frozen) folders:** A6 `proposals/2026-10-22-redundancy`, A7 `proposals/2026-10-22-redesign`, and A8 `proposals/2026-10-22-r044-veto` and `proposals/2026-10-22-gvmw`. Moving them would mean changing their permissions, so their owner (Architect) has to decide.
- **Not moved by design:**
  - A3: a public-repo rebuild and push.
  - A14: New Bot's agent folder (Gem, via the sidebar).
  - A18: role-map versions v1–v21 (Archivist's call).
- **Side effect:** a duplicate copy of `proposals/2026-10-22-redundancy` sits in the archive from a failed first move attempt. The original is untouched. That copy can be removed if Gem wishes.
