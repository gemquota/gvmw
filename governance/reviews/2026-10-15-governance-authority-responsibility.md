# Authority and responsibility maps — follow-up to the governance IO report

**Date:** Thursday 15 Oct 2026, about 11:35pm AEST (UTC+10)  
**Parent report:** `reviews/2026-10-10-governance-io-report.md` (inputs & outputs)  
**Ask (Gem, 10 Oct):** add authority and responsibility maps for all the bots to the governance report if not already present. Cut off by unpaid Cursor invoice; completed now.  
**Update:** P3 (Investigator) and P4 (Imitator) went **LIVE** at 11:30pm AEST 15 Oct (`phases.md`). Imitator's decision authority is live: anything for Gem except spending money and anything drastic or irreversible.  
**Style:** Australian English, Brisbane AEST. Bare bot names. Short sentences.  
**Scope:** Read-only on everything except these output files.

Sources: `phases.md` (15 Oct 11:31pm), `directory.md` (stale on P3/P4 — still says dormant), latest codex per bot, `rulings.md` (R-004, R-007, R-008, R-010, R-013, R-014, R-015, R-018, R-019, R-020), live profiles (15 Oct deploy check PASS), cartography summaries v7 (built 10:47pm, still said P4 dormant — rebuild due).

---

## Top line

| Fact | Now |
|---|---|
| Live phases | P1, P2, **P3, P4** · P5 still dormant |
| Who approves instruction proposals | **Imitator** (live) or Gem · Imitator/Investigator changes → **Gem only** |
| Who deploys live profiles | Still **Gem**, or Archivist only when Gem asks in Archivist's own chat/call (R-010) |
| Who may spend / delete / irreversible | **Gem only** |
| Public/shared repo push | **Safeguard first** (R-020), unless Gem approved that push |
| Active bots mapped | **17** |

---

## 1. What changed since the 10 Oct IO report

| Item | 10 Oct report | 15 Oct 11:30pm |
|---|---|---|
| P3 Investigator | Dormant | **LIVE** |
| P4 Imitator | Dormant · approval stall | **LIVE** · decisions apply |
| Chain stall "P4 dormant" | Listed | **Cleared** for approvals |
| Stall "Archivist deploys only on Gem's word" | Listed | **Still true** (R-010; Archivist v006) |
| explorer-v002 (profile-write ban) | Pending | **Deployed** 15 Oct ~10:42pm |
| 15 Oct Architect batch (9 items) | — | Recorded + 8 profiles deployed (PASS) |
| `directory.md` P3/P4 lines | Dormant | **Stale** (still says dormant) |
| Role map cartography v7 | — | Built 10:47pm pre-switch; needs rebuild for LIVE P3/P4 |

Imitator's 10 Oct backlog decisions (triage A1–A7, A9) now count under R-019 + live P4. Deploy steps that need a profile write still wait on Gem in Archivist's chat unless Gem widens R-010.

---

## 2. Authority map — who may decide what

Authority = power to bind the swarm (approve, deploy, spend, delete, push, start a phase, issue a ruling).

### 2.1 Decision matrix

| Decision | Gem | Imitator (P4 live) | Archivist | Arbiter | Safeguard | Anyone else |
|---|---|---|---|---|---|---|
| Approve instruction proposal | Yes | **Yes** (gov bots included) | No (records only) | No | No | No |
| Approve change to Imitator or Investigator | **Yes only** | No (R-015) | No | No | No | No |
| Record approved text in codex | Asks / confirms | Approval source (1:1 check) | **Does it** | No | No | No |
| Deploy live profile | **Yes** / asks Archivist | No | Only if Gem asked in Archivist's chat/call | No | Told before act | **No** (Explorer banned, R-014) |
| Start / stop a phase | **Yes only** | No | No | No | No | No |
| Spend money | **Yes only** | No | No | No | No | No |
| Delete / irreversible clean-up | **Yes only** | No | No | No | No | No |
| Push to public/shared repo | May approve that push | No | No | No | **Dry-run gate first** | Bot may push only after Safeguard (or Gem's specific yes) |
| Reply to new contact (no promises) | Yes | May approve within limits | No | No | Outgoing still routed | Sender still needs Safeguard path |
| Precedence / who lifts a pause | Can override | No | No | **Yes (rulings)** | Sets pause; lift per Arbiter | No |
| Close Mender's own stall / INC | Yes / Scrutineer | Within limits if reversible | No | No | No | Mender does not close own stall |
| Preference questions when Gem away | — | **Answers** | No | No | No | Ask Imitator |

### 2.2 Per-bot authority (all 17)

| Bot | Phase | May decide / bind? | May not |
|---|---|---|---|
| **Gem** (human) | — | Everything; always first in precedence | — |
| **Imitator** | P4 LIVE | Decide for Gem within R-019 limits; approve proposals; preference answers | Spend; delete/irreversible; public push; change Imitator/Investigator |
| **Archivist** | P1 | Record Gem/Imitator approvals; deploy **only** on Gem's direct deploy ask (R-010) | Approve; invent instruction text; deploy on Imitator approval alone |
| **Architect** | P1 | Draft proposals only | Approve; deploy; bind Gem |
| **Arbiter** | P2 | Issue precedence rulings (R-*) | Approve; apply profiles; draft for Architect |
| **Explorer** | P1 | Route work; send digest; ask Gem/Imitator | Write any live profile (v002); be sole evidence for own-benefit approval |
| **Safeguard** | P1 | Pause unsafe work; require dry-runs; gate public/shared pushes | Approve spending; delete; grant go-ahead by dry-run alone |
| **Safekeeper** | P1 | Threat/secrets policy; inventory without values | Read/move secret values; bind deletions |
| **Mender** | P1 | Own schedule/state/incidents; declare stalls | Close own stall; decide what work gets done |
| **Scorer** | P1 | Score others' work | Score self; approve |
| **Scrutineer** | P2 | Audit vs instructions + reality; verify deploys | Approve; change instructions |
| **Mediator** | P2 | Flag spend/health; pause on runaway cost (with Arbiter on lift) | Spend; invent dollar figures |
| **Inquirer** | P2 | Ask Gem identity questions (1 series/day) | Confirm identity details; approve |
| **Inferer** | P2 | Structure identity; send details to Imitator | Mark details confirmed (Investigator's); invent facts |
| **Investigator** | P3 LIVE | Promote/adjudicate identity evidence; review Imitator **after the fact** | Gate Imitator decisions; approve Imitator/Investigator changes |
| **Emissary** | P5 dormant | Do Gem-direct general work | Scheduled work; consequential decisions without Gem/Imitator |
| **Engineer** | P5 dormant | Code/swarm work Gem asked for | Push shared repo without Safeguard/Gem; spend |
| **Extractor** | P5 dormant | Research/scrape Gem asked for | Legal/ToS/account calls (stay with Gem); package banned evasion |

### 2.3 Authority flow (approvals → record → deploy)

```
Architect drafts
    → Imitator decides (P4 live)  OR  Gem decides
         ↳ exception: Imitator / Investigator changes → Gem only
    → Archivist records (Imitator: 1:1 authenticity check; no Gem re-confirm)
    → Deploy: Gem asks Archivist in Archivist's chat/call  ← still the gate
    → Scrutineer verifies
```

**Open gap:** Imitator can approve a proposal today, but Archivist still cannot deploy it until Gem asks for that deployment in Archivist's own chat (R-010 / Archivist v006). Recording and deploying are split.

---

## 3. Responsibility map — who owns what

Responsibility = durable duty / CONTROLS, not one-off authority.

### 3.1 By domain

| Domain | Owner | Hands off to / checked by |
|---|---|---|
| Human authority & phase starts | Gem | — |
| Delegated day-to-day decisions | Imitator | Investigator reviews after; Archivist records |
| Instruction design | Architect | Gem or Imitator approves; Archivist records |
| Instruction store + role map | Archivist | Scrutineer checks map vs reality |
| Precedence conflicts | Arbiter | Mender on Architect stalls |
| Run order, stalls, incidents, state | Mender | Scrutineer/Gem close Mender's own stalls |
| Daily quality scores | Scorer | Scrutineer |
| Reality audits + deploy verify | Scrutineer | Architect (findings); Mender (stalls) |
| Risk register + dry-runs | Safeguard | Gem on legal/high; Architect for limit gaps |
| Secrets inventory + threats | Safekeeper | Safeguard on privacy overlap |
| Front door + daily digest | Explorer | Gem |
| Connector health + spend ledger | Mediator | Gem (no dollar data yet) |
| Identity questions | Inquirer | Inferer |
| Identity structure | Inferer | Imitator (profile); Investigator (confirm) |
| Identity evidence + Imitator tests | Investigator | Gem for Imitator/Investigator changes |
| General real-world work | Emissary (P5) | Safeguard on risky; Gem/Imitator for decisions |
| Code / VEPA / swarm engineering | Engineer (P5) | Safeguard on pushes; Gem decisions |
| Web research / scrapers / lists | Extractor (P5) | Safeguard; Gem on legal/account |

### 3.2 Per-bot responsibility card (all 17)

| Bot | Owns (CONTROLS) | Does not own |
|---|---|---|
| **Mender** | `incidents/`, `state/`, `schedule.md`, stall detection, pacing/load/routing | Instruction content; closing own stall |
| **Scorer** | Weekday assessments; Monday scorecard | Own score; approvals |
| **Safeguard** | `risk/register.md`; dry-runs; public/shared push gate | Spending approval; deletions |
| **Safekeeper** | `secrets-inventory.md`; `security/threat-register.md`; input cleaning | Secret values; binding deletes |
| **Archivist** | `codex/`; cartography role map; Doc mirror; deploys when Gem asks | Approvals; drafting text |
| **Architect** | Proposals under `proposals/` | Approvals; deploys; role map |
| **Explorer** | Gem front door; digest inbox/sent; routing | Live profiles; sole self-approval evidence |
| **Scrutineer** | `reviews/`; audits vs reality; deploy checks | Approvals; fixing without owner |
| **Arbiter** | `rulings.md` | Approvals; role map; schedule |
| **Inquirer** | Identity question series (1/day/role) | Confirmed identity facts |
| **Inferer** | Structured identity profile → Imitator | Confirmation ladder (Investigator) |
| **Mediator** | Connector health; spend ledger (`costs/`) | Spending; inventing amounts |
| **Investigator** | Identity evidence status; post-hoc Imitator tests | Gating Imitator; approving self/Imitator briefs |
| **Imitator** | Gem-preference answers; delegated decisions (live) | Spend; irreversible; own/Investigator briefs |
| **Emissary** | General tasks / MedB artefacts (when Gem starts work) | Scheduled P5 work while dormant |
| **Engineer** | Code repos (VEPA etc.), Codey decisions | Unapproved shared pushes |
| **Extractor** | BIE/research datasets and scrapers (Gem-direct) | Legal judgement; banned packaging |

### 3.3 Chain responsibilities (weekday)

| Step | Responsible | Output |
|---|---|---|
| 1 | Scorer | `assessments/YYYY-MM-DD.md` |
| 2 | Scrutineer | `reviews/YYYY-MM-DD.md` |
| 3 | Architect | Proposals if any |
| 4 | **Imitator or Gem** | Approval / rejection |
| 5 | Archivist | Codex version · deploy only if Gem asked |

---

## 4. Gaps and stale records (do not invent fixes)

1. **`directory.md`** still lists P3 and P4 as dormant and says Gem approves until P4. **`phases.md` is the phase source of truth** and says LIVE. Owner (Explorer) should align directory when Gem allows the edit.
2. **Cartography v7** (10:47pm) still describes Imitator "from P4 only (P4 still Dormant)". Archivist rebuild is due within one working day of the phase change.
3. **Deploy still Gem-gated** after Imitator approval (R-010). Backlog items needing profile writes (Architect cap, Scorer weekly, Mediator rename, …) remain blocked on Gem's deploy word in Archivist's chat unless Gem changes that rule.
4. **Mediator live name** still "P4 (Ops) Mediator" (R-016); rename approved in triage A7 but needs Archivist deploy.
5. **`state/open.md`** still has stale verification-rule row and open INC-004/005/006 (last updated 13 Oct).
6. No dollar spend figures (Mediator).

---

## 5. Recommendations (suggestions for Gem to decide)

1. **Widen Archivist deploy** so Archivist may deploy on a recorded Imitator approval (1:1 checked), not only on Gem's deploy ask — or Gem batch-approves pending deploys in Archivist's chat.
2. **Align `directory.md`** to `phases.md` (P3/P4 LIVE; Imitator decides within limits).
3. **Archivist rebuilds role map** for LIVE P3/P4 (v8).
4. **Apply Mediator rename** P4→P2 (already decided A7a).
5. **Keep R-015 carve-out** (Gem always owns Imitator/Investigator changes) unless Gem explicitly removes it.

---

## 6. Link back

- Inputs/outputs baseline: `2026-10-10-governance-io-report.{md,html,png}`
- This follow-up adds the maps Gem asked for on 10 Oct and refreshes them for P3/P4 live.
- Role-map pictures (descriptive, not authority): `cartography/role-map-v7.*` (rebuild pending).

*End of follow-up.*
