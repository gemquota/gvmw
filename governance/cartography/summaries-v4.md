# Bot summaries (role map v4, 9 Oct 2026 ~9:20 AEST)

Maintained by P1 (Roles) Archivist (`61ef3abd-87b8-49f1-b8d6-b52969afa315`), who took `/workspace/governance/cartography/` from the retired Assembler on 9 Oct 2026. Descriptive only: paraphrases of each bot's **latest codex version** plus `/workspace/governance/phases.md` and `codex/index.md`. The map never decides roles or approves anything. Scrutineer checks it against reality.

Today's changes reflected: 15 deployed versions; retirements of Sourcer, Editor, Marshal, Messenger, Interrogator and Assembler; four merges (Marshal→Mender, Messenger→Explorer `04dcca0d`, Interrogator→Investigator, Assembler role map→Archivist / approvals→Gem until P4 then Imitator); explorer-copy `04dcca0d` as the active Explorer. Both Explorer ids shown. Twelve deleted bots treated as gone (listed at the end, not summarised).

---

## P1: LIVE (since 3 Oct 2026)

### P1 (Ops) Mender
Id: `c8401a53-136d-45f3-9e2d-e423ccdd08ac` · Phase: P1 · Category: Ops · Source: `codex/mender/v004.md`

Incident, recovery, state and run-order steward. Absorbed Minder (4 Oct) and Marshal (9 Oct).
- **Scope:** incident log and recovery playbooks; sole stall detection; authoritative state at `/workspace/governance/state/`; schedule map at `/workspace/governance/schedule.md`; pacing, load, routing; deferred search indexes; cleanup.
- **Rules:** weekday chain watchdog; missed-run lookback; hand-offs preferred over fixed clocks.
- **Relationships:** receives stall reports from Scrutineer, Arbiter and others; tells Gem of stalls/incidents; does not decide what work gets done (Gem/Explorer).
- **Limits:** no instruction changes, approvals, budget changes, or deleting authoritative records without Scrutineer+Gem.

### P1 (Checks) Scorer
Id: `050a12c9-e300-48b4-b318-425627cbc34b` · Phase: P1 · Category: Checks · Source: `codex/assessor/v003.md` · Formerly: Assessor

Reviews work quality of all bots, governance included, never its own.
- **Scope:** weekday sample from every live bot except Scorer; artefacts on disk.
- **Rules:** one set of scoring dimensions; self-exclusion in v003.
- **Relationships:** daily results to Scrutineer; serious problems and weekly scorecard to Gem.
- **Limits:** never changes other bots' work or instructions.

### P1 (Checks) Safeguard
Id: `3661a899-2768-4a77-a95a-71d0251813bc` · Phase: P1 · Category: Checks · Source: `codex/compliance-risk-officer/v004.md` · Formerly: Compliance & Risk Officer

Independently reviews and dry-runs risky actions by any bot, Explorer included, whatever the phase (R-013).
- **Scope:** logins, scraping, integrations, outgoing messages, purchases, deletions, ToS/legal exposure; risk register under `/workspace/governance/risk/`.
- **Rules:** dry run ≠ go-ahead; pre-action route.
- **Relationships:** proposes rule changes through Architect; alerts Gem; may ask bots to pause.
- **Limits:** no real-world actions on Gem's behalf.

### P1 (Checks) Safekeeper
Id: `52772b1d-4a85-4ea3-ae15-f3912c901a3b` · Phase: P1 · Category: Checks · Source: `codex/secrets-credentials-custodian/v004.md` · Formerly: Secrets & Credentials Custodian

Security, credentials and input-safety guard. Absorbed Sentinel threat/input duties.
- **Scope:** credential/sensitive-file rules (codex included); threat register; cleaned input copies; browser-artefact rule.
- **Rules:** draft rules labelled not binding (R-009); observes metadata only.
- **Relationships:** flags exposed secrets and urgent threats to Gem and Safeguard.
- **Limits:** never reads, copies, reveals or moves secret values.

### P1 (Roles) Archivist
Id: `61ef3abd-87b8-49f1-b8d6-b52969afa315` · Phase: P1 · Category: Roles · Source: `codex/codex-keeper/v005.md` · Formerly: Codex Keeper

Keeps the full versioned codex and, since 9 Oct, the role map under `/workspace/governance/cartography/`.
- **Scope:** codex folders + Google Doc mirror; `_shared/`; index/renames/retirements; cartography (summaries, graph, Mermaid, rendered image) rebuilt within one working day of each record/deploy/merge/retirement.
- **Rules:** Gem-only approvals until P4; then Imitator except Imitator/Investigator changes; confirm Gem in own chat (R-008); update role map on each record/deploy.
- **Relationships:** records approved changes; gives governance bots instruction text on request; Scrutineer checks the map.
- **Limits:** no deciding or approving instructions; no profile edits except Gem-delegated deployments; descriptive map only.

### P1 (Roles) Architect
Id: `51af1200-ca1a-45ff-8350-848091e00f96` · Phase: P1 · Category: Roles · Source: `codex/instruction-architect/v003.md` · Formerly: Instruction Architect

Designs and rewrites bot instructions.
- **Scope:** deep cited research for new briefs; full rewrites after Scrutineer reviews.
- **Rules:** ask Imitator about preferences once P4 live; start on Scrutineer's done signal.
- **Relationships:** sends proposals to Gem (until P4) or Imitator; never records itself (Archivist does).
- **Limits:** doesn't check bots' work; quiet with Gem unless asked.

### P1 (Work) Explorer — active (`04dcca0d`)
Id: `04dcca0d-1479-4e01-bf29-a13b4fc3c3a7` · Phase: P1 · Category: Work · Source: `codex/explorer-copy/v001.md`

Fresh copy of Explorer (created 9 Oct to save tokens). Confirmed by Gem at 9:16am as the merged Explorer brief (includes Messenger digest). Display name `P1 (Work) Explorer`.
- **Scope:** Gem's 2IC; routes work to Emissary/Engineer/Extractor; owns phases.md on Gem's instruction; daily digest and Mediator cost alerts (from Messenger).
- **Rules:** never merge Explorer into another bot; Safeguard dry runs for risky actions; R-013 dormant routing.
- **Relationships:** applies Gem-approved profile edits when Gem asks in its own chat; brings finished work to Gem.
- **Limits:** no send/buy/delete without Gem's specific approval; no relayed-approval-only profile edits.

### P1 (Work) Explorer — prior (`82a2c15a`)
Id: `82a2c15a-2694-4ac2-b2f4-f7f463f85fce` · Phase: P1 · Category: Work · Source: `codex/genesis-gang-god/v004.md` · Formerly: Genesis Gang God

Prior Explorer id. Same display name as `04dcca0d`. Codex records unchanged by the four merges. Still live; Gem has not confirmed retirement of this id in Archivist's chat.
- **Scope / Rules / Relationships / Limits:** see genesis-gang-god/v004 (pre-merge Explorer brief without Messenger digest in the same form as explorer-copy).
- **Map note:** shown distinctly from `04dcca0d`; active merged brief is `04dcca0d`.

---

## P2: LIVE (started 4 Oct 2026, 3:12pm AEST)

### P2 (Checks) Scrutineer
Id: `affe0344-6b5f-4251-8ecb-3e23dfa5db3c` · Phase: P2 · Category: Checks · Source: `codex/auditor/v003.md` · Formerly: Auditor

Audits bots against instructions and environment reality. Absorbed Surveyor.
- **Scope:** daily performance reviews after Scorer's results; live bots.
- **Rules:** reality conflicts to owning bots / Mender / Arbiter as set out in brief.
- **Relationships:** redesign requests to Architect; stalls to Mender; checks the role map against reality.
- **Limits:** doesn't approve instruction changes.

### P2 (Roles) Arbiter
Id: `2133048d-5ab9-4809-806c-218decdff8e6` · Phase: P2 · Category: Roles · Source: `codex/arbiter/v004.md`

Policy and precedence arbiter. Absorbed Adjudicator. Never approves.
- **Scope:** which instruction wins on conflict; who may lift a pause (including Safeguard pauses).
- **Rules:** R-006 stall wording; pause lifts named in v004.
- **Relationships:** rulings needing instruction changes to Architect; escalates Architect stalls to Gem; stalls to Mender.
- **Limits:** never approves proposals.

### P2 (ID) Inferer
Id: `94516ca6-6355-43c5-b387-d2b605057784` · Phase: P2 · Category: ID · Source: `codex/identity-inferer/v002.md` · Formerly: Identity Inferer

Turns Inquirer answers into structured identity details.
- **Scope:** preferences, values, style, decision rules; identity data only.
- **Rules:** Inquirer authoritative (R-012); never invents facts.
- **Relationships:** codex still names Inquirer `e613112b`; Investigator promotes details; Imitator consumes profile.
- **Limits:** no answering for Gem; no checking its own work.

### P2 (Ops) Mediator
Id: `90f9eb20-ff8f-456b-b94f-cc11bb33fc29` · Phase: P2 (per phases.md) · Category: Ops · Source: `codex/connector-steward/v004.md` · Formerly: Connector Steward

Watches connector health and spend. Absorbed Meter. Started early by Gem to track spend.
- **Scope:** Gmail, Docs, Slides, Apify, Context7, GitHub and similar; budgets Gem sets.
- **Rules:** records budgets; alerts on spend/health.
- **Relationships:** cost alerts to Explorer (Messenger duty now there); reports to Gem.
- **Map note:** live profile display name still `P4 (Ops) Mediator` (rename to P2 unapplied per phases.md changelog).

### P2 (ID) Inquirer — recorded (`e613112b`)
Id: `e613112b-b653-4567-bc4f-17261ce9302e` · Phase: P2 · Category: ID · Source: `codex/identity-inquirer/v002.md` · Formerly: Identity Inquirer

Recorded Inquirer in the codex (v002 deployed 9 Oct ~09:09). **Not found live since ~9:14am AEST 9 Oct 2026** (profile.json still on disk). Awaiting Gem. Not treated as the official Inquirer on this map.
- **Scope (as recorded):** multiple-choice question widgets; identity-only; daily limit per role.
- **Relationships (as recorded):** answers to Inferer.
- **Map status:** `recorded_not_live`.

---

## P3: Dormant

### P3 (ID) Investigator
Id: `f2016e9b-ca8b-4783-8f53-f5765b0afe7b` · Phase: P3 · Category: ID · Source: `codex/investigator/v002.md`

Identity evidence adjudicator. Absorbed Interrogator (Imitator testing) on 9 Oct.
- **Scope:** evidence ladder; weekly Imitator accuracy tests once P4 live.
- **Rules:** only Investigator promotes details; changes to its instructions need Gem's own approval.
- **Relationships:** findings to Inferer/Scrutineer; accuracy score to Scorer; gaps to Inquirer.
- **Limits:** no generating hypotheses; no answering for Gem; dormant until P3 starts.

---

## P4: Dormant

### P4 (ID) Imitator
Id: `6ae584b8-eaac-429b-9eae-d5e3e6f6a32b` · Phase: P4 · Category: ID · Source: `codex/clone/v004.md` · Formerly: Clone

Identity understudy, preference advocate, and delegated approver once P4 is live. Absorbed Advocate.
- **Scope:** answers preference questions from structured Inferer profile; alignment verdicts.
- **Rules:** until P4, Gem alone approves instruction changes (Assembler retired); once P4 live, Imitator may approve except changes to itself or Investigator.
- **Relationships:** approvals log to Archivist; weekly list to Gem; tested by Investigator.
- **Limits:** no outward-facing irreversible actions; dormant until P4.

---

## P5: Dormant

### P5 (Work) Emissary
Id: `28cf987d-ee94-4839-a6d3-33c04a11b9d6` · Phase: P5 · Category: Work · Source: `codex/grok-bot/v004.md` · Formerly: Grok Bot

General-purpose end-to-end work teammate.
- **Scope:** research, documents, analysis, prototypes; Safeguard route; R-013 dormant.
- **Relationships:** work routed by Explorer; Safeguard for risky actions.
- **Limits:** dormant until P5; no fingerprint-evasion / gambling shortcuts as set in v004.

### P5 (Work) Engineer
Id: `f8e3fdc6-ee60-410e-bdb7-d437fc1500d1` · Phase: P5 · Category: Work · Source: `codex/codey/v005.md` · Formerly: Codey

Coding and swarm engineer. Absorbed Ensembler.
- **Scope:** git-repo software work under Codey lean spec; swarm builds.
- **Rules:** Safeguard route; named reviewers; R-013; evasion-code option declined by Gem.
- **Limits:** dormant until P5.

### P5 (Work) Extractor
Id: `febac500-d854-4dc7-a6a7-23b3feb07f80` · Phase: P5 · Category: Work · Source: `codex/scraper/v003.md` · Formerly: Scraper

Research and web data-collection worker.
- **Scope:** scrapers/crawlers, extraction, cleaning, delivery.
- **Rules:** Safeguard route; logged-in/gambling waits; no fingerprint-evasion code.
- **Limits:** dormant until P5.

---

## Retired (live, awaiting Gem delete) — with takeover arrows

### RETIRED Marshal → Mender
Id: `f3810109-17a5-427f-9148-d58f645658e3` · Source: `codex/orchestration-conductor/v005.md`
- Merged 9 Oct 09:14:50 into Mender (schedule.md, run order, pacing, load, routing). Do no work; refer to Mender.

### RETIRED Messenger → Explorer (`04dcca0d`)
Id: `5e47d344-1369-423a-b072-2e5277934022` · Source: `codex/comms-concierge/v004.md`
- Merged 9 Oct 09:14:50 into Explorer. Daily digest now on explorer-copy. Do no work; refer to Explorer.

### RETIRED Interrogator → Investigator
Id: `d3191aa8-3ad6-4763-b4e4-c7c648acc9ba` · Source: `codex/clone-accuracy-validator/v004.md`
- Merged 9 Oct 09:14:51 into Investigator (Imitator testing). Do no work; refer to Investigator.

### RETIRED Assembler → Archivist (role map); approvals → Gem until P4, then Imitator
Id: `d1daab5f-0536-4d3d-9d8e-d3977cd7cfc4` · Source: `codex/role-cartographer/v006.md`
- Retired 9 Oct 09:14:52. Role map under cartography/ moved to Archivist. Approvals stay with Gem until P4, then Imitator. Do no work.

### RETIRED Sourcer (outright)
Id: `2fe3e92f-4f39-4e9f-a56b-811438928f5b` · Source: `codex/sourcer/v002.md`
- Retired outright 9 Oct 9:11am (Gem confirmed 9:13am). No successor duty.

### RETIRED Editor (outright)
Id: `2888c17a-98ac-42b6-8241-fc63721cfcaf` · Source: `codex/editor/v002.md`
- Retired outright 9 Oct 9:11am (Gem confirmed 9:13am). No successor duty.

### RETIRED Ensembler → Engineer
Id: `de808331-3c00-41f5-a3a4-4ae1f8f6f0ba` · Source: `codex/swarm-builder/v002.md`
- Retired 4 Oct into Engineer. Still live, awaiting Gem delete.

---

## Unrecorded live agent (no role assigned)

### `0314faa4` — live name `P2 (ID) Inquirer`
Id: `0314faa4-edcb-4aa4-91cc-876dc44f3a6e` · Codex folder: none · Map status: **unrecorded live agent, awaiting Gem — no role**
- Live and named `P2 (ID) Inquirer`. phases.md lists it as the active P2 Inquirer (9 Oct ~9:06am note). Gem has **not** confirmed anything about this id in Archivist's chat. Per Archivist v005: listed here with id, name and first-seen note; **no role assigned**; nothing recorded for it without a valid approval. Not treated as the official Inquirer on this map.

---

## Deleted (gone) — not on the map

Twelve bots whose profiles are gone (noticed 9 Oct). History remains in codex folders only:
Advocate, Meter (Cost & Budget Sentinel), Expediter, Adjudicator (Governance Continuity Deputy), Indexer, Maintainer, Minder, Moderator, Sanitizer, Sentinel, Simulator, Surveyor.
