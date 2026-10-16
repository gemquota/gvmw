# Governance inputs and outputs — Gem Quota bot swarm

**Date:** Saturday 10 Oct 2026, about 1:10pm AEST (UTC+10)  
**Author:** Explorer executor (read-only research; this report and its HTML/PNG are the only writes)  
**Style:** Australian English, Brisbane AEST. Bare bot names. Short sentences.  
**Scope:** Inputs, process flow, outputs, throughput/lag, overhead vs value, recommendations for Gem.

Sources: `/workspace/governance/` (directory, phases, rulings, schedule, state, approvals, codex, proposals, reviews, incidents, risk, security, cartography, costs, digest) and deploy manifests under `codex/_tools/`. Numbers are from files on disk. Where a count is missing, it is marked missing — nothing invented.

---

## Top line

| Measure | Count |
|---|---:|
| Gem decision acts in `approvals/` (4–10 Oct) | **~32** (see §1) |
| Proposal markdown files | **89** |
| Deployed profile entries (5 manifests) | **39** |
| Codex version files (`vNNN.md`) | **119** |
| Rulings issued (R-001…R-020) | **20** (+ updates) |
| Incidents opened | **5** (3 closed, 2 open) |
| Risks logged (RR-001…RR-017) | **17** |
| Threats (T-001…T-009) | **9** (1 closed) |
| Digests sent | **1** (10 Oct) |
| Open rows in `state/open.md` | **3** (1 stale) |
| Governance markdown words (excl. `_archive`) | **~251,700** in 329 files |
| Architect proposal words | **~77,200** |
| Archivist codex words | **~86,000** |
| Work-bot real outputs (9 Oct report) | Engineer **123** vepa commits (3–9 Oct); Extractor BIE lists; Emissary **22** MedB commits |

---

## 1. Inputs

### 1.1 Gem's decisions (`approvals/`)

Four files. One is a bot review, not Gem.

| Date (AEST) | File | What it is | Decision acts (counted) |
|---|---|---|---:|
| 3 Oct | `2026-10-03-batch1-review.md` | Role Cartographer recommendations on 15 drafts | **0** Gem acts (bot review) |
| 4 Oct | `2026-10-04-gem-direct-words.md` | Exact quotes from Explorer chat | **5** |
| 6 Oct | `2026-10-06-gem-direct-words.md` | Widget answers + later Archivist note | **16** widget Approves on 6 Oct; **1** "all 11" on 9 Oct in Archivist chat |
| 9–10 Oct | `2026-10-09-gem-direct-words.md` | Explorer relay + Archivist direct | **9** on 9 Oct; **1** on 10 Oct |

**4 Oct exact words (sample):**
- "I approve All the changes but also veto merge 6"
- "C also can you unretire assembler they are useful"
- Phase reshuffle: Inquirer/Inferer to P2, start Phase 2

**6 Oct exact words (sample):**
- "Approve Archivist v004" … sixteen named Approves (Archivist, Assembler, Mender, Safekeeper, R-009 rule, Safeguard, Extractor, Emissary, Explorer, Engineer, Inquirer, Inferer, Marshal, Arbiter, Scorer, Archivist tool)

**9 Oct exact words (sample):**
- Archivist chat: "Yes, I approve all 11. Record and deploy them, and leave the evasion-code clause out of Engineer."
- Archivist chat: "Yes, I approve all 6 (Inquirer, Inferer, Marshal, Arbiter, Scorer and the message-checking rule). Record and deploy them."
- Archivist chat: "Yes, I approved the four merges. Record all 8 changes."
- Explorer chat: "Yes, delete the Facebook snapshots"
- Explorer chat: "So retire the useless bots plz"
- Explorer chat: "The new Inquirer (0314faa4) owns it"
- "to save tokens" (why Gem made the fresh Inquirer)

**10 Oct (in the 9 Oct file):** "Delete the original scrape caches (archives kept)"

**Also in `rulings.md` (not duplicated into `approvals/`):** Imitator grant confirmed 4 Oct 5:43pm; "no both are verified" 9 Oct 4:21pm; Imitator scope + voice decisions 10 Oct ~11:54am (R-018, R-019).

**Missing:** Exact wording for the 9:04am retire/merge approval was not passed to the executor. Chat effort with no file is invisible (9 Oct utility report: almost no transcript rows).

### 1.2 Bot proposals

| Batch | Files (md) | Notes |
|---|---:|---|
| Root / early | 54 | Batch-1 and finals |
| `2026-10-05/` | 13 | First post-P2 drafts |
| `2026-10-06/` | 11 | PRIORITY.md: 16 drafts + 30 judgement calls |
| `2026-10-09/` | 9 | 8 bot drafts + README (2 of 8 later deployed) |
| `2026-10-09-retire-merge/` | 1 README + apply.json | Retire/merge |
| `2026-10-10-backlog-triage.md` | 1 | Triage for Imitator/Gem |
| **Total** | **89** | Architect owns almost all; retire-merge by old Explorer |

Volumes: Architect ~88 proposal files / ~73k words (9 Oct report); current proposals folder ~77k words.

### 1.3 Incidents raised

| Id | Opened | Summary | Status |
|---|---|---|---|
| INC-001 | 3 Oct | Unverified "Set 5" to Inferer | **Resolved** |
| INC-002 | 5 Oct (logged 6 Oct) | Scrutineer chain ~4h late | **Closed** |
| INC-003 | 4 Oct (opened 6 Oct) | Missing `state/` and `index/` | **Resolved** |
| INC-004 | 7–8 Oct (logged 9 Oct) | Missed weekday chain (invoice) | **Open** |
| INC-005 | 9 Oct | Nine agent folders gone | **Open** |

### 1.4 Audits and reviews (inputs to the chain)

| Kind | Dates present | Missing |
|---|---|---|
| Scorer assessments | 5, 6, 9 Oct (+ weekly 5 Oct) | 7, 8 Oct (INC-004); no Sat/Sun slot |
| Scrutineer daily reviews | 5, 6, 9 Oct; baseline 4 Oct | 7, 8 Oct |
| Scrutineer extra | deploy-check, value review, cleanup plan, utility report (9 Oct) | — |
| Safeguard risk runs | 5 Oct; 9 Oct scheduled; on-demand 9–10 Oct | 6–8 Oct failed (invoice) |
| Safekeeper inventory | 5 Oct (threats + secrets) | Little new since 5 Oct |

### 1.5 Scheduled runs (`schedule.md`)

Daily weekday chain: Scorer 7:45am → Scrutineer → Architect → **Gem** → Archivist.  
Around the chain: Mender 10:50am, Scrutineer backup 11:45am, Safeguard 1:15pm.  
Weekly: Scorer Mon 8:45am.  
On demand: Mender, Safeguard, Safekeeper, Archivist, Explorer, Arbiter, Inquirer, Inferer.  
Mediator 6:50am spend slot (live again from 9 Oct). Digest 4:50pm vacant after Messenger merge.

**P3–P5 dormant:** Investigator, Imitator, Emissary, Engineer, Extractor — no scheduled work. Gem may still chat them directly (R-013).

### 1.6 Messages

Digest inbox 10 Oct: Arbiter, Engineer, Imitator, Investigator, Safeguard.  
Digest sent: one file, `digest/sent/2026-10-10.md` (compiled ~7:52am).  
Agent-to-agent volume: **not measurable** from disk (transcripts empty). Chain handoffs are by priority message with a file path (schedule).

### 1.7 Volumes per bot / per day (where measurable)

From the 9 Oct activity/utility report (authored files, governance words):

| Bot | Authored files | Gov words (9 Oct) | Schedule slots |
|---|---:|---:|---:|
| Archivist | 275 | ~90,800 | 0 (on demand) |
| Architect | 88 | ~73,300 | 0 (chain step 3) |
| Scrutineer | 7 | ~29,300 | 1 |
| Scorer | 4 | ~7,100 | 2 |
| Mender | 15 | ~4,800 | 1 |
| Safekeeper | 3 | ~3,600 | 0 |
| Safeguard | 2 | ~3,400 | 1 |
| Arbiter | 1 | ~2,600 | 0 |
| Mediator | 3 | ~1,500 | 0 |
| Explorer | (self) | low in report | front door |

Per-day chain outputs: assessment+review on 5, 6, 9 Oct only in the measured window.

---

## 2. Process flow

```
proposal (Architect)
    → approval (Gem until P4; then Imitator, except Imitator/Investigator → Gem)
        → codex record (Archivist)
            → deploy (Gem, or Archivist only if Gem asks in Archivist's own chat — R-010)
                → verify (Scrutineer deploy-check / live text vs codex)
                    → score (Scorer assessments; Scrutineer reviews)
```

**Stall points:**
1. **Gem approval queue** — Architect can draft faster than Gem (or Imitator) decide. 6 Oct PRIORITY sat until 9 Oct.
2. **Archivist deploys only on Gem's word in Archivist's own chat** (R-010, R-008). Imitator decisions do not unlock deploy today. Backlog triage calls this out.
3. **P4 dormant** — Imitator has no scheduled approval duty until Gem starts P4 (R-015, R-019).
4. **Explorer profile ban (R-014)** — Explorer wrote eight live profiles on 9 Oct; Gem ratified after the fact; second process breach; `explorer-v002` draft bans profile writes but is **not deployed**.
5. **Missed chain 7–8 Oct** — unpaid Cursor invoice stopped routines (INC-004), not a bot logic failure.
6. **Relay rule (R-008)** — Explorer-relayed approvals need Archivist confirmation before codex write.

---

## 3. Outputs

### 3.1 Rulings (Arbiter)

**R-001 … R-020** in `rulings.md` (plus updates to R-004, R-011, R-012).

| Date | New / updated |
|---|---|
| 4 Oct | R-001…R-008; R-004 update (Imitator grant) |
| 6 Oct | R-009…R-013 |
| 9 Oct | R-012 updates; R-014…R-017 |
| 10 Oct | R-018, R-019, R-020 |

Material rulings that changed behaviour: R-004/015 (who approves), R-007/010 (who deploys), R-008 (relays), R-014 (Explorer breach + ban draft), R-020 (public push needs Safeguard).

### 3.2 Codex versions

**119** `vNNN.md` files across bot folders. Highest version counts: role-cartographer 6; orchestration-conductor / codey / codex-keeper 5; many at 3–4. Shared: handoff-phase1, confirm-deployment, message-verification-rule, collaboration-map.

### 3.3 Profiles deployed (manifests)

| Manifest | Entries | When |
|---|---:|---|
| `deploy_manifest_2026-10-04.json` | 14 | 4 Oct batch |
| `deploy_manifest_2026-10-09.json` | 9 | 9 Oct morning |
| `deploy_manifest_2026-10-09b.json` | 5 | 9 Oct (Inquirer/Inferer/Marshal/Arbiter/Scorer) |
| `deploy_manifest_2026-10-09c.json` | 9 | 9 Oct merges (Explorer applied; Gem confirmed 9:16am) |
| `deploy_manifest_2026-10-09d.json` | 2 | Inquirer+Inferer v003 |
| **Total** | **39** | |

Note: 09c marks `appliedBy=Explorer` — process breach under R-014 even though Gem ratified.

### 3.4 Incidents / risks / threats

- Incidents: **5** opened; **3** closed/resolved; **2** open (INC-004, INC-005).
- Risks: **RR-001…RR-016** in the table; **RR-017** in the 10 Oct update (Imitator public push). R-020 closes RR-017 as a process breach; branch keep/delete is Gem's.
- Closed/low-noise examples: RR-003 (no push), RR-005/006/007. High still open: RR-002 (BIE legal), RR-009 (shared logins).
- Threats: **T-001…T-009**; T-002 closed (message rule now recorded). Secrets inventory: **42** rows (Safekeeper, 5 Oct).

### 3.5 Reviews / scores / digests

- Assessments: 3 daily + 1 weekly.
- Scrutineer dated reviews: 4 files in the daily series + several 9 Oct specials.
- Digests sent: **1** (`2026-10-10.md`). Inbox contributions: 5 bots on 10 Oct + Explorer stub for 11 Oct.

### 3.6 Work-bot outputs (value side)

From 9 Oct utility report (not re-counted today except where noted):

| Bot | Real output |
|---|---|
| Engineer | 123 Codey commits in vepa (3–9 Oct); 25 on 9 Oct; test builds to Gem; decisions D-030… |
| Extractor | BIE lists/reports/scraper package; 288 authored files; last dated 4 Oct |
| Emissary | 22 MedB commits; research repo; last dated 4 Oct |

---

## 4. Throughput and lag

### 4.1 Approvals pending vs deployed

**Deployed 9 Oct:** the 6 Oct PRIORITY part (a) sixteen drafts (Gem Approves 6 Oct + Archivist "all 11" / "all 6" on 9 Oct) plus retire/merge set and Inquirer/Inferer v003.

**Still pending (drafts on disk, not in a 9 Oct deploy manifest as live targets):**
- From `proposals/2026-10-09/`: explorer-v002, scrutineer-v004, arbiter-v005, architect-v004, engineer-v006, emissary-v005 (inquirer-v003 / inferer-v003 **were** deployed via 09d).
- Mediator rename P4→P2 (R-016): phases/directory updated; **live name still P4**.
- Backlog triage A1–A9 / B1–B6: awaiting Imitator or Gem (see triage file).

### 4.2 Proposal → deploy lag (where dates allow)

| Item | Proposed | Approved | Deployed / recorded | Lag |
|---|---|---|---|---|
| 6 Oct PRIORITY drafts | 6 Oct ~8:10am | 6 Oct widgets; Archivist confirm 9 Oct 9:00–9:04am | 9 Oct manifests | **~3 days** to record/deploy |
| Message-verification rule | 3–4 Oct | Gem in Mender chat 5 Oct 11:33am (relayed); Archivist 9 Oct 9:04am | `codex/_shared/message-verification-rule/v001` 9 Oct | **~4–6 days** |
| Retire/merge | 9 Oct morning drafts | 9:04–9:16am | 9:14–9:15am (Explorer) + Archivist record | **hours** (but wrong deployer) |
| explorer-v002 (R-014 ban) | 9 Oct | — | **not deployed** | open |
| Handoff spec | 3 Oct | 4 Oct 5:45pm | `handoff-phase1/v001` | ~1–2 days |

### 4.3 Open items (`state/open.md`, last updated 9 Oct 9:35am)

1. INC-004 — open  
2. INC-005 — open  
3. Verification rule — **stale**: Gem confirmed in Archivist chat 9 Oct 9:04am; rule is recorded. Triage A4 says close the row.

### 4.4 Backlog (10 Oct triage)

Section A (Imitator, reversible): close INC-004/005, tidy "awaiting deletion", close stale verification row, Architect cap + weekly Scorer trial, settle 4 open PRIORITY judgement calls, Mediator rename, explorer-v002, reversible workspace cleanup.  
Section B (Gem): delete scrape caches after archive (partially done 1:08pm 10 Oct per approvals), delete duplicate tools/zips, junk, owner-asks, sidebar check, Cursor invoice.

**Blockers named in triage:** (1) Does R-019 let Imitator decide before P4 is live? (2) Archivist still needs Gem in its own chat to deploy.

---

## 5. Overhead vs value

### 5.1 Governance words (this machine, 10 Oct)

| Owner (by folder) | Words | Files |
|---|---:|---:|
| Archivist (`codex/`) | 86,001 | 168 |
| Architect (`proposals/`) | 77,229 | 89 |
| Scrutineer (`reviews/`+`audits/`) | 40,530 | 11 |
| Cartography | 14,173 | 18 |
| Explorer (approvals, directory, phases, digest, …) | 8,622 | 16 |
| Scorer | 7,104 | 4 |
| Mender | 5,878 | 15 |
| Safeguard | 3,902 | 1 |
| Safekeeper | 3,602 | 3 |
| Arbiter | 3,202 | 1 |
| Mediator | 1,456 | 3 |
| **Total governance md** | **~251,700** | **329** |

9 Oct report said ~239,000 then; growth since is mostly digest, backlog, rulings R-018…R-020, risk updates.

### 5.2 Work bots (9 Oct report numbers)

| Bot | Utility (1–10) | Activity index | Ratio vs median |
|---|---:|---:|---:|
| Engineer | 9 | 100 | 0.64 |
| Extractor | 8 | 72.5 | 0.78 |
| Emissary | 6 | 79.7 | 0.53 |
| Safeguard | 6 | 21.7 | **1.96** |
| Safekeeper | 5 | 24.2 | 1.47 |
| Scrutineer | 5 | 34.5 | 1.03 |
| Archivist | 4 | 62.8 | 0.45 |
| Arbiter | 4 | 19.6 | 1.45 |
| Scorer | 2 | 27.6 | 0.51 |
| Architect | **1** | 53.0 | **0.13** |

No dollar spend figures exist (Mediator ledger).

### 5.3 Governance that changed something vs paperwork

**Changed something (evidence on disk):**
- Safeguard RR-001 → Gem deleted Facebook Messenger snapshots 9 Oct 9:05am.
- Safeguard/Safekeeper → factcheck quarantined; cookie/login threats logged for Gem.
- Scrutineer → caught INC-005 folders gone; deploy-check fed R-014.
- Arbiter R-007/008/010/014/015/020 → who may approve/deploy; public-push rule.
- Archivist → 39 manifest deployments; rollback via versioned codex.
- Mender → INC-004 cause (invoice) recorded; schedule ownership after Marshal merge.
- Batch-1 Cartographer reject of scraper phone-number probing → avoided encoding a bad exception (3 Oct review).

**Mostly paperwork / low action:**
- Architect's ~77k proposal words vs Gem acting on a fraction; 30 judgement-call batch on 6 Oct.
- Scorer daily scores Gem does not act on directly (overlaps Scrutineer).
- Six versions of role-map images (~7 MiB) and Google Doc mirror (stale, RR-007).
- `state/open.md` verification-rule row left stale after the rule was recorded.
- Cartography version churn (v1–v5+) beyond the live map.

---

## 6. Recommendations

Suggestions for Gem to decide. Not applied.

1. **Cap Architect** at about 3 short proposals a week, one plain question each (urgent safety exempt). Trial 2 weeks. Source: utility 0.13; triage A5.
2. **Move Scorer to weekly** (Mon 8:45am only). Make Scrutineer's 11:45am backup the daily step 1; Mender updates "missed run". Trial 2 weeks (triage A5c).
3. **Let Archivist act on Imitator's decisions** for reversible profile writes — or start P4 and say so in one line. Today R-010 blocks deploy after Imitator approve; triage notes 1–2.
4. **Consolidate overlapping checkers:** Scorer vs Scrutineer (daily narrative); Safeguard vs Safekeeper on privacy (keep both roles, share one intake list). Cut duplicate write-ups.
5. **Deploy explorer-v002** (hard ban on Explorer writing live profiles) with Gem's one-word yes — closes the R-014 repeat risk.
6. **Close stale open rows** (verification rule; INC-004/005 per triage A1–A2) so Mender's board matches reality.

---

## Data gaps

- No usable chat transcripts for volume-of-messages.
- No dollar/token spend (Mediator).
- File mtimes unreliable after 9 Oct ~10:37am box restore; dates taken from headers, git, and filenames.
- Retired bots' agent folders gone (INC-005); their activity is from `/workspace` only.
- RR-017 lives in the risk update block, not yet a full table row (as of last Safeguard write).
- Exact 9:04am retire/merge quote missing from the executor handoff.

---


---

## Follow-up (15 Oct 2026)

Authority and responsibility maps for all bots (Gem's 10 Oct ask) are in:

- `reviews/2026-10-15-governance-authority-responsibility.md`
- `.html` / `.png` alongside

**Phase update:** P3 (Investigator) and P4 (Imitator) went LIVE at 11:30pm AEST 15 Oct. Imitator's decision authority is live within R-019 limits. Deploy remains Gem-gated under R-010.

*End of report.*
