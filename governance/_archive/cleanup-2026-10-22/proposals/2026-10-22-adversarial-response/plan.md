# Response plan: external adversarial review (22 Oct 2026) — DRAFT, NOTHING APPROVED

Drafted by Architect, 22 Oct 2026, about 7:58pm AEST, for Gem. Relayed by Explorer at 7:50pm (R-008), so see README.md before acting on anything.
- **Sources:** `reviews/2026-10-22-external-adversarial-review.md` (the review; findings are numbered as there), `reviews/2026-10-22-swarm-brief-for-adversarial-review.md`, `rulings.md` (R-001 to R-044 and the 7:52pm notes), and Arbiter's section [`arbiter-section.md`](arbiter-section.md) (7:52pm), which is merged in below and linked in full.
- **Who does what:** P0 fixes are already being started by others under Gem's "Both", so this plan only lists them (section 1). Architect drafts; Arbiter rules; Gem approves.

**Legend.** 🔴 GEM = needs Gem's own words, because it touches Imitator, any of its five checkers (Investigator, Scorer, Scrutineer, Safekeeper, Safeguard; R-015, R-027, R-028), retiring or archiving a bot, spending, or something irreversible (R-019, R-034). Everything else can go to Imitator or Gem under R-004 and R-010, but because the source is relayed, Gem confirms the plan as a whole first.

---

## 0. Engineer on GitHub: Gem chose reading (b) 🔴 GEM (still to be recorded)
- **Gem's words:** Gem told Architect directly in chat, 7:52pm 22 Oct, choosing the option that explicitly said **"no per-push approval or Safeguard check"**. That's reading (b): Engineer is fully free on GitHub, and needs neither per-push words from Gem nor a Safeguard dry run.
- **Recording pending:** the words are in Architect's chat log, not on disk. Archivist still has to record them in approvals/ from Gem directly (R-029). The GitHub batch revision 5 paste lines open with Gem restating them.
- **Where it's applied:** GitHub batch revision 5 (`proposals/2026-10-16-github/`). Engineer still runs its own secret and content scan and logs each action, and Safeguard reviews the log afterwards, never as a gate.
- **What reading (b) doesn't change:** these keep Gem's words and a dry run unless Gem says otherwise:
  - a pull request to a repo Gem doesn't own;
  - a push that triggers a public deployment;
  - other deletions and history rewrites;
  - new public repos, gists and packages;
  - visibility and settings changes;
  - tokens.
- **Still in tension, for Gem and Arbiter:**
  - Arbiter's §1 (R-020/R-036 and gvmw rows) and checks 1, 2 and 4 assume per-push controls. Under (b), for Engineer, checks 2 (scan) and 1 (read-back) can run as non-blocking checks Engineer does itself, plus Safeguard's review afterwards. Check 4 (action-hash binding) doesn't apply to Engineer's pushes.
  - R-020 and R-036 need Arbiter to update them.
  - **Resolved (R-051):** Gem answered "Engineer fully free, no per-push checks". gvmw has no per-push words, scan or dry run; Gem then answered the card directly (Gem, 8:32pm on 22 Oct in Architect's chat: "gvmw: Engineer fully free, drop the per-push scan and dry run"): no per-push or per-sync-run scan or dry run on gvmw. Logging, the ban on secrets and the ban on new BIE data stay.
- This plan doesn't override either position beyond recording Gem's choice.

## 1. P0 (started by others; listed for tracking only)
| P0 item | Owner (suggested) | Needs Gem |
|---|---|---|
| Freeze gvmw writes | Engineer pauses the sync; Safeguard confirms | 🔴 (R-042: Gem chose public; a freeze is containment, reversible) |
| Rotate wide-scope or unknown GitHub tokens | Gem (sign-ins and keys are Gem's, connector-limits v002); Safekeeper lists them | 🔴 |
| Audit gvmw contents and history | Safeguard and Safekeeper, read-only | Read-only: no |
| Separate personal, sensitive and BIE material from the public repo | Engineer, after a backup and a dry run (connector-limits v003 B/C) | 🔴 (irreversible if history is rewritten) |
| Independent external backup of governance | Gem picks the destination | 🔴 (new destination, may cost) |
| Liveness watchdog | Local only: heartbeat lines checked by Scrutineer; outside watchdog scrapped (Gem, 8:28pm in Explorer's chat, relayed by Explorer: "Scrap health checks.io") | Done in redesign resilience-v001 |
| Technical gate on destructive ops | Engineer builds the wrapper; Safeguard reviews | 🔴 (changes how checkers work) |

## 2. Findings: accept, adapt or reject
| # | Finding | Call | Reasons and links |
|---|---|---|---|
| 1 | No technical enforcement boundary | **Accept** | Proved by INC-005 (9 folders), R-032/R-033 (28 moves), R-034 (120 captures), R-040 (34 unchecked commits), INC-008 (lost state). Answered by P1-A (broker) and the deletion gate (section 3) |
| 2 | Credentials, not Gem, are the effective top authority | **Accept** | Precedence (R-004, R-006 basis; Arbiter §4) is only as strong as access. Unknown tokens since 9 Oct (Safekeeper threat register). P1-A |
| 3 | Too many roles; state drifts across files | **Accept** | R-021 (directory vs phases), R-023/R-035 (status lines), role-map rebuilds. Answered by P1-E and P2 |
| 4 | INC-009: governance silent for about 6 days; need an outside watchdog | **Accept** | Mender, Scrutineer and Explorer, the in-swarm stall backups, all stopped together. Arbiter check 11. P0 and P1-E | **Only partly met:** Gem scrapped healthchecks.io (Gem, 8:28pm in Explorer's chat, relayed by Explorer: "Scrap health checks.io"), so the watchdog is local and shares the box with the swarm.
| 5 | Mender is both operator and restore custodian | **Accept** | INC-008: restore source unknown. Restore authority moves to an external snapshot that Archivist only reads (P1-C). Mender keeps operations (R-006, R-044) |
| 6 | File times aren't evidence; need a hash-chained ledger | **Accept** | INC-008 rewrote every mtime; the R-037/R-038 time slips. P1-C; Arbiter check 7 |
| 7 | gvmw: classification failure, Privacy Act APP 11/APP 8, NDB 30-day assessment; see a lawyer | **Adapt** | Gem accepted the risk at 6:48pm (R-042) and v003 records it. But an NDB assessment is a legal duty, not a preference, so this plan asks Gem whether to get advice. Bots don't give legal advice. 🔴 |
| 8 | BIE as a separate data domain the poster can't read | **Accept** | R-031, connector-limits v002 rule 6, Arbiter §1 (hold by data class). P1-D. It also blocks the Extractor fold unless there's a wall (redundancy batch) |
| 9 | Extractor capability classes; bypass banned | **Accept** | scraper v005 already bans evasion. Make the classes explicit in P1-A and P1-D |
| 10 | Dry runs as exact previews; approvals bound to an action hash | **Accept** | Arbiter §1 (R-020/R-036 row) and checks 4 and 6. P1-B |
| 11 | Approvals as objects | **Accept** | Arbiter §4. P1-B |
| 12 | Don't let after-the-fact ratification become normal | **Rejected by Gem** | Gem: "No, keep allowing it" (R-051). The ban is removed from this plan. |
| 13 | Imitator advisory only until it passes thresholds | **TODO** | Gem: "Advisory only for big or irreversible decisions". The exact scope waits on Arbiter's question to Gem; interim per R-051. |
| 14 | Independence of failure domain, not just of role | **Adapt** | It's one box and one billing account. Full separation costs money, so stage it: an external watchdog and backup first (P0), a separate checker credential later (P1-A stage 3). 🔴 for spend |
| 15 | Approve classes with hard bounds to reduce Gem's load | **Accept** | Fits connector-limits v003 (Explorer's sharing carve-out) and the standing sync approvals (Safeguard register, redundancy batch). P1-B class approvals |
| 16 | Explorer's blast radius; split gateway, router, state and digest | **Adapt** | Modules, not bots. R-014 already bans its profile writes. R-044 splits routing (Explorer assigns new work, Mender runs operations). P2 Gateway |
| 17–19 | About 7 components; make deterministic what can be | **Adapt** | P2 map (section 4) and P1-E. The 4 Oct veto on merging Inquirer and Inferer stands until Gem lifts it 🔴 |
| 20 | Capability broker; no raw credentials | **Accept, staged** | Platform constraint: connectors act as Gem's account. P1-A |
| P2 | Merge Arbiter into deterministic policy | **Reject in part** | Rulings on ambiguity, which the review says to keep, need judgement. Arbiter stays a role in Governance, and its checkable rulings become checks (Arbiter §3) |
| Scores | resilience 3, access 2, credentials 2 … | **Accept as baseline** | Re-score after P1 stage 2 |

## 3. P1 architecture changes
Each item has a design, the bots and rules it affects, and a staged rollout. Every stage is drafted by Architect, has its checker changes approved by Gem, is built by Engineer, and has its check reviewed by a bot other than its builder.

### P1-A Capability broker 🔴 GEM (Safekeeper and Safeguard change; credentials)
- **Design:** a small service on the box (`/opt/broker`) holds connector credentials that Gem enters. Bots call `broker <capability> <args>` and never see a token. The capability map lives in a file only Gem can change, for example `engineer: github.push.private, github.push.public(preview+scan+readback)`, `emissary: postiz.post(approved-text-hash)`, `extractor: fetch.public, fetch.api; bulk needs a preview; personal-data and bypass are banned`. Every call goes to the ledger (P1-C).
- **Affects:** every work bot; Safekeeper (secrets-credentials-custodian v005) owns the map; Safeguard (compliance-risk-officer v006); connector-limits v002 rules 13–18 and the shared GitHub draft.
- **Limit:** cloud connectors that run as Gem's account can't be wrapped from the box. For those the broker is advisory (it logs and checks against the map) until the platform offers per-bot scopes.
- **Rollout:** (1) inventory only: Safekeeper lists every token and scope, and Gem rotates the unknown ones (P0). (2) The broker wraps box-side git and gh (GitHub push, visibility) plus deletes. (3) Other CLIs, and a separate credential for the checkers.

### P1-B Approval objects bound to an action hash 🔴 GEM (R-010, R-019, Archivist and Investigator)
- **Design:** each approval is one record in `approvals/objects.jsonl`: `{id, principal: "Gem"|"Imitator", words, chat, time (system clock), action_class, target, action_hash, scope, expiry, delegable: false}`. `action_hash` is the sha256 of the exact preview (command, target, visibility, file list or diff hash, or the version text). The executor recomputes it and refuses if it differs or has expired. Class approvals (finding 15) set bounded `scope` instead of one hash.
- **Folded in from Arbiter:** a deploy needs a record before the write, and the live hash must equal the approved hash (§1 R-010 row; checks 3, 4 and 6). Irreversible classes are a fixed list (delete, public push or publish, send, share, visibility change, spend, credential change), and their principal must be Gem (§1 R-019 row; check 9). Checker changes are routed to Gem (check 10).
- **Affects:** Archivist (codex-keeper v008), Safeguard (dry run becomes a preview), Imitator (clone v006), Explorer, every executing bot; R-008, R-010, R-018, R-019, R-029, R-036.
- **Rollout:** (1) Shadow: records are written next to today's markdown, and Scrutineer compares them. (2) Enforced for deploys and deletes. (3) Enforced for outward actions, with class approvals offered to Gem.

### P1-C Append-only, hash-chained ledger, held off the box 🔴 GEM (spend, new destination)
- **Design:** each event (approval, action, deploy, ruling, incident, heartbeat) is a JSON line with `prev_sha` and a system-clock time, written by a single writer and mirrored hourly to an external store Gem picks (for example a private repo under Gem's own account with branch protection, or object storage with retention lock). Restore is from that snapshot. Archivist reads it; Mender doesn't write it (finding 5).
- **Affects:** Mender (mender v005), Archivist, Scrutineer (daily chain verification), INC handling, all rulings' times (Arbiter check 7).
- **Rollout:** (1) Local ledger plus a daily mirror. (2) Hourly mirror and a restore drill, verified by Scrutineer. (3) Ledger events become the evidence for rulings instead of mtimes.

### P1-D Data classes 🔴 GEM (touches gvmw, R-031, R-042)
- **Design:** classes are PUBLIC, INTERNAL, PERSONAL-GEM (identity notes), PERSONAL-OTHERS (third-party contacts), BIE-GAMBLING and SECRET. Tags are set by path rules in `data-classes.yaml` plus a content scan. A pre-push or pre-share scan blocks any class that isn't allowed at the destination. The BIE domain lives in its own folder, which Emissary (the poster) can't read once the broker is in place.
- **Folded in from Arbiter:** holds apply by data class, not file name (§1 R-031 row). "Public" means outside the box only where Gem names the destination.
- **Affects:** Extractor, Emissary, Engineer, Safeguard, Safekeeper; connector-limits v002 rules 6 and 14, v003, R-031, R-040 to R-043.
- **Rollout:** (1) Tag existing folders (read-only report). (2) Scan in warn mode on every push and share. (3) Block mode; the BIE folder is split from the poster.

### P1-E Deterministic services (Arbiter §3: 11 checks)
Each check has a fixed input, pass rule and fail action, and it never runs as the acting bot.

| # | Check | Runs as | Gem? |
|---|---|---|---|
| 1 | Visibility read-back after create or push; a mismatch pauses the sync | Post-push hook; Scrutineer reviews | 🔴 (Scrutineer) |
| 2 | Secret and data-class scan before push | Pre-push hook; Safekeeper owns the rules | 🔴 |
| 3 | Approval-quote match (exact, recorded before the action) | Scrutineer | 🔴 |
| 4 | Action-hash binding | Wrapper; Safeguard reviews | 🔴 |
| 5 | Version-file immutability | Scrutineer daily | 🔴 |
| 6 | Deploy hash = approved hash | Scrutineer after each deploy | 🔴 |
| 7 | System-clock stamps vs ledger | Scrutineer | 🔴 |
| 8 | Deletion gate (named path plus a verified archive) | Wrapper; Safekeeper checks the archive | 🔴 (irreversible) |
| 9 | Irreversible-class approver is Gem | Investigator | 🔴 |
| 10 | Checker-change router | Archivist before deploy; Scrutineer audits | 🔴 |
| 11 | Liveness watchdog, local only (outside service scrapped: Gem, 8:28pm in Explorer's chat, relayed by Explorer: "Scrap health checks.io") | Heartbeats checked by Scrutineer | Partly meets finding 4 |

Also deterministic, from finding 19: directory and role-map generation from the codex (Archivist's tool), the token inventory (Safekeeper, names and scopes only), job and billing monitoring (Mediator; a billing stop alerts Gem from outside the swarm).
- **Rollout:** checks 3, 5, 6 and 10 first (read-only scripts on existing files), then 1, 2 and 8 (hooks), then 4, 7, 9 and 11 (after P1-B and P1-C).
- 🔴 Every check that sits in a checker bot's brief is a checker change, so Gem approves those briefs.

### Also P1: independent restore authority, independent billing monitor, no self-authorisation
These are covered by P1-C (restore), check 11 plus Mediator's billing monitor (the external alert) and Arbiter §4 (self-benefiting claims have no effect until Gem confirms to a different bot). 🔴

## 4. P2 consolidation: 17 bots to about 7 components 🔴 GEM (retiring or archiving bots; Imitator and checkers)
Imitator is advisory only in every option.

| Component | Bots now | After | Notes |
|---|---|---|---|
| Gateway | Explorer | Explorer (front door, digest, assigns new work) | Phases and state move to generated files (P1-E) |
| Operations | Mender, Mediator | One bot (Mender keeps the name), with Mediator's connector health and spend as modules | Mediator archived 🔴 |
| Governance | Architect, Archivist, Arbiter | Architect drafts; Archivist records as a deterministic service plus a thin bot; Arbiter rules (kept as a role, see finding P2 reject) | Possibly two bots; Archivist's brief stays Gem-only |
| Assurance | Scorer, Scrutineer, Safeguard, Safekeeper | Two bots: Assessor (Scorer and Scrutineer) and Risk (Safeguard and Safekeeper), so no single checker checks everything | All are Imitator's checkers 🔴. Assessor can't review its own scoring: an external spot-check by Gem or Risk |
| Identity | Inquirer, Inferer, Investigator, Imitator | Inquirer+Inferer only if Gem lifts the 4 Oct veto 🔴; Investigator stays separate (it checks Imitator); Imitator advisory only | Imitator approvals end until it passes thresholds 🔴 |
| Workers | Emissary, Engineer, Extractor | Kept as three. The Extractor fold stays a separate Gem-only question (redundancy batch), now also blocked on P1-D's wall | — |

Result: about 11 bots in 7 components, or 10 with the Inquirer/Inferer merge.

**Migration order** (each step: archive first, delete nothing, retire only after the merged brief is deployed and checked):
1. Imitator becomes advisory only (one brief change plus R-019 and R-010 updated) 🔴
2. Mediator folds into Mender 🔴
3. Assurance pairs, with checker briefs rewritten 🔴
4. Governance: Archivist's deterministic tools first, then trim the briefs
5. Identity: only on Gem's word about the veto 🔴
6. Gateway trimmed after P1-E generates state

**Risks:**
- Fewer bots means fewer independent checks, so keep at least two Assurance bots and the local watchdog (the external one was scrapped by Gem at 8:28pm).
- Merged briefs get long and are followed less well.
- Version clashes with the paused GitHub batch and the redundancy batch, so record order must be set first.
- Losing duties in the merges, so every merge carries the old brief's rules word for word, and Scrutineer diffs them.
- Archive loss on the shared box (INC-005, INC-008), so take an external snapshot (P1-C) before any retirement.

## 5. Arbiter's input on precedence and rulings (labelled section)
Full text: [`arbiter-section.md`](arbiter-section.md). Arbiter's proposals, not Architect's; nothing binds until Gem approves.
- **Loopholes (§1):**
  - R-010: "within its authority" is judged by the two bots involved.
  - R-019: "irreversible" isn't defined, and ratification launders.
  - R-020/R-036: a dry run is a narrative, not a preview, and recurring syncs have no per-run check.
  - R-031: a hold on a file name is bypassed by copying.
  - R-034: there's no backup, so ratification can't restore.
  - gvmw: no visibility read-back, and a relayed quote started an outward action.
  - Each has a closing rule (merged into P1-B, P1-D and P1-E).
- **Ratification ban (§2): removed.** Gem rejected it ("No, keep allowing it", R-051).
  - **R-044 update (7:52pm):** the veto is verified from Gem's 7:00pm words in Inquirer's chat, "C and Imitator can veto if desired". It doesn't apply to disputes about Imitator or its checkers, or over Gem's words or deterministic checks. The schedule power is still unverified. 🔴
- **The tension with Gem's 7:52pm answer:** Arbiter's R-020/R-036 and gvmw points assume public pushes need Gem's per-push words. See section 0. Neither side is overridden here.

**Open for Arbiter:**
- (a) Rule on reading (a), (b) or (c) once Gem's 7:52pm words are recorded.
- (b) Say whether the containment exception covers pausing a gvmw sync (finding 7, P0 freeze).
- (c) Confirm whether "Arbiter as deterministic policy" is rejected in part, as section 2 proposes.
- (d) Set the record order across the GitHub, redundancy and adversarial batches.
