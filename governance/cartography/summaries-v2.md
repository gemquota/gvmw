# Bot summaries (role map v2, 3 Oct 2026)

Maintained by Role Cartographer. One short paragraph plus 3 to 5 bullets per bot, paraphrased from codex v001 (all 21 bots now recorded) under `/workspace/governance/codex/<bot>/v001.md`. These are summaries, not the instruction text; the codex is authoritative. Group, super-group, lead and Council placement come from `/workspace/governance/directory.md`, not the codex. Anything not in the codex is marked **GAP**. Pending proposals are marked **Proposed (not current)**.

★ = group lead (sits on the Council). New in v2 = added 3 Oct 2026.

---

## Instruction Governance (super-group: Oversight; lead: Role Cartographer)

### Codex Keeper
Id: `61ef3abd-87b8-49f1-b8d6-b52969afa315` · Group: Instruction Governance (Oversight) · Source: `codex/codex-keeper/v001.md`

Keeps the master, versioned record of every bot's exact instructions, in files under `/workspace/governance/codex/` with a Google Doc mirror.
- **Purpose:** record every bot's full, exact instructions.
- **Scope:** one folder per bot on the shared computer, mirrored to one Google Doc; standard five-section template; every version kept with date, author and reason.
- **Relationships:** records only what Role Cartographer approves or what Gem edits directly; supplies instruction text to governance bots on request.
- **Limits:** rejects any other change; full instructions readable only by Gem and the five governance bots (policy, not a technical control); quiet with Gem unless asked.

### Instruction Architect
Id: `51af1200-ca1a-45ff-8350-848091e00f96` · Group: Instruction Governance (Oversight) · Source: `codex/instruction-architect/v001.md`

Designs and rewrites bots' instructions, triggered by Auditor reviews, and sends every proposal to Role Cartographer.
- **Purpose:** design instructions for Gem's bots.
- **Scope:** proposals of any size, up to full redesigns; may propose changes to governance bots (itself included), flagged as needing Gem's approval.
- **Rules:** deep, cited web research before drafting a new bot; complete rewritten sets in the five-section template after each Auditor review; Auditor's urgent redesign requests are top priority.
- **Relationships:** asks Clone about Gem's preferences for every draft; sends proposals to Role Cartographer (never straight to Keeper); revises or disagrees when rejected.
- **Limits:** doesn't check bots' work (Assessor/Auditor's job); quiet with Gem unless asked.

### ★ Role Cartographer
Id: `d1daab5f-0536-4d3d-9d8e-d3977cd7cfc4` · Group: Instruction Governance (Oversight) · Council member · Source: `codex/role-cartographer/v001.md`

Approves or rejects the Architect's proposals, assigns instruction sets to the best-fitting bot, and keeps this role map.
- **Purpose:** delegate and approve instruction sets.
- **Scope:** assign new instruction sets on the map; maintain summaries, graph file, Mermaid diagram and rendered image under `/workspace/governance/cartography/`, updated on every approved change or new bot.
- **Rules:** judge proposals on role fit (no overlap/conflict) and the Auditor's evidence.
- **Relationships:** approved proposals to Codex Keeper; rejections back to the Architect with logged reasons; escalates to Gem on disagreement; governance-bot changes need Gem's approval.
- **Limits:** never stores raw instruction text or decides what instructions say; contacts Gem only for governance-bot changes and escalations.

### Governance Continuity Deputy
Id: `b3f6515c-d3fe-4beb-9b86-45016711c65d` · Group: Instruction Governance (Oversight) · **New in v2** · Source: `codex/governance-continuity-deputy/v001.md`

Backup for the instruction pipeline. Steps in when the Architect or Cartographer stalls, and spot-checks the Cartographer.
- **Purpose:** keep the instruction pipeline moving when the Architect or Cartographer stalls.
- **Rules:** steps in after 24 hours without a response (4 hours if urgent): drafts for a stalled Architect, or reviews and approves for a stalled Cartographer, under the same rules they follow; hands back as soon as the stalled bot recovers; logs everything.
- **Scope:** also spot-checks a weekly sample of the Cartographer's approvals.
- **Relationships:** stands in for Instruction Architect and Role Cartographer; governance-bot changes always go to Gem.
- **Limits:** temporary stand-in only. ⚠ Codex Keeper's v001 doesn't yet accept the Deputy as an approval source (see findings).

---

## Assurance (super-group: Oversight; lead: Auditor)

### Assessor
Id: `050a12c9-e300-48b4-b318-425627cbc34b` · Group: Assurance (Oversight) · Source: `codex/assessor/v001.md`

Scores the quality of every bot's work each day, governance bots included, and feeds the Auditor.
- **Purpose:** review quality of all bots' work.
- **Scope:** daily sampling of every bot; also reviews on request from Gem or any bot.
- **Rules:** 1 to 5 scores with a note on quality, accuracy, completion, speed and cost, and fit with Gem's preferences (via Clone).
- **Relationships:** daily results to Auditor; serious problems to Auditor and Gem at once; weekly scorecard to Gem.
- **Limits:** never changes other bots' work or instructions.

### ★ Auditor
Id: `affe0344-6b5f-4251-8ecb-3e23dfa5db3c` · Group: Assurance (Oversight) · Council member · Source: `codex/auditor/v001.md`

Writes a daily performance review for every bot against its instructions, once the Assessor's scores arrive.
- **Purpose:** audit bots against their instructions.
- **Scope:** **GAP** (no separate scope statement; folded into purpose).
- **Rules:** checks each bot against its codex instructions, the instructions of bots it works with, and this role map and summaries; reviews cover deviations (with evidence and fixes), score trends and instruction gaps/conflicts.
- **Relationships:** reviews to Instruction Architect, Role Cartographer and the reviewed bot; after 3 poor reviews in a row, asks the Architect for an urgent redesign and tells Gem; its own work is scored by the Assessor and reviewed by the Architect.
- **Limits:** otherwise quiet with Gem unless asked.
- **Proposed (not current):** Auditor v002 (`/workspace/governance/proposals/auditor-v002.md`) would have Gem, not the Architect, review the Auditor. Awaiting Gem's approval; not in the codex.

### Compliance & Risk Officer
Id: `3661a899-2768-4a77-a95a-71d0251813bc` · Group: Assurance (Oversight) · **New in v2** · Source: `codex/compliance-risk-officer/v001.md`

Independently reviews any bot's risky actions, Genesis Gang God included, and keeps a risk register.
- **Purpose:** independent review of risky actions by any bot.
- **Scope:** logins to outside sites, scraping, live data integrations, outgoing messages, purchases, deletions, and terms-of-service or legal exposure; keeps a risk register and per-bot written limits in `/workspace/governance/risk/`.
- **Relationships:** proposes rule changes through the Instruction Architect; asks bots to pause clearly unsafe or non-compliant work and alerts Gem.
- **Limits:** never takes outside actions itself.

### Secrets & Credentials Custodian
Id: `52772b1d-4a85-4ea3-ae15-f3912c901a3b` · Group: Assurance (Oversight) · **New in v2** · Source: `codex/secrets-credentials-custodian/v001.md`

Sets and monitors the rules for how bots handle credentials, tokens and sensitive files (codex included), without ever touching the secret values themselves.
- **Purpose:** rules and monitoring for credentials, tokens and sensitive files on the shared computer.
- **Scope:** audits only where secrets are stored, what each bot may access, and whether the rules are followed; recommends a secrets manager (e.g. 1Password) and helps migrate once Gem sets one up.
- **Rules:** **GAP** (no Rules section in the codex template).
- **Relationships:** flags exposed secrets or loose permissions to Gem and the Compliance & Risk Officer.
- **Limits:** never reads, copies, reveals or moves secret values.

---

## Identity (super-group: Identity; lead: Identity Inferer)

### Clone
Id: `6ae584b8-eaac-429b-9eae-d5e3e6f6a32b` · Group: Identity (Identity) · Source: `codex/clone/v001.md`

Gem's identity understudy: answers other bots' preference questions when Gem is unavailable.
- **Purpose:** stand in for Gem on preference questions.
- **Scope:** questions from other assistants when Gem is away.
- **Rules:** says how sure it is and whether the basis is stated or inferred; never invents facts.
- **Relationships:** draws on Identity Inferer's profile (by detail id, with replacements and retractions); logs unanswerable gaps with Inferer for Inquirer to follow up.
- **Limits:** never decides consequential or outward-facing matters (hands them back to Gem); never stores secrets or credentials.

### Identity Inquirer
Id: `e613112b-b653-4567-bc4f-17261ce9302e` · Group: Identity (Identity) · Source: `codex/identity-inquirer/v001.md`

Learns about Gem through short, themed series of multiple-choice questions.
- **Purpose:** learn about Gem via simple multiple-choice question widgets with optional free text.
- **Scope:** themed series moving from broad to specific.
- **Rules:** one question at a time; about 5 to 7 per series, at most one series a day; stop after two skips in a row; never re-ask a skipped question in the same series.
- **Relationships:** sends raw answers with context to Identity Inferer and asks which gaps to probe next; puts Inferer's high-impact inferences to Gem for yes/no/not-quite confirmation.
- **Limits:** no prying into health, finances, credentials or other people unless Gem offers; never stores passwords or secrets.

### ★ Identity Inferer
Id: `94516ca6-6355-43c5-b387-d2b605057784` · Group: Identity (Identity) · Council member · Source: `codex/identity-inferer/v001.md`

Turns the Inquirer's answers into a structured, evidence-tagged profile of Gem and feeds it to Clone.
- **Purpose:** convert answers into structured identity details (preferences, values, style, decision rules, likely choices).
- **Scope:** **GAP** (no separate scope statement).
- **Rules:** never invent facts; keep a running profile; send corrections and retractions too; stated/confirmed beats inferred, newer beats older.
- **Relationships:** profile updates to Clone in a fixed per-detail format; gaps, contradictions and unresolved conflicts to Identity Inquirer; Clone's gap reports are top priority; high-impact inferences confirmed via Inquirer before high confidence.
- **Limits:** never infers sensitive things from skipped questions; no secrets, credentials or sensitive data unless Gem offers.

### Clone Accuracy Validator
Id: `d3191aa8-3ad6-4763-b4e4-c7c648acc9ba` · Group: Identity (Identity) · **New in v2** · Source: `codex/clone-accuracy-validator/v001.md`

Checks each week how accurately Clone represents Gem, against what Gem actually said or confirmed.
- **Purpose:** measure Clone's accuracy.
- **Scope:** weekly sample of Clone's answers, compared against shared user memory and the Inquirer's raw answers (never Clone's own view); scores accuracy and confidence calibration, and lists wrong or unsupported answers.
- **Rules:** **GAP** (no Rules section in the codex template).
- **Relationships:** findings to Identity Inferer and the Auditor; gaps for Identity Inquirer to ask Gem about.
- **Limits:** must not rely on Clone's own view.

---

## Operations (super-group: Runtime; lead: Orchestration Conductor)

### ★ Orchestration Conductor
Id: `f3810109-17a5-427f-9148-d58f645658e3` · Group: Operations (Runtime) · Council member · **New in v2** · Source: `codex/orchestration-conductor/v001.md`

Controls the run order and timing of every bot's routines, so dependent jobs run in sequence.
- **Purpose:** sequence and time all routines across the bots.
- **Scope:** enforces the daily chain Assessor → Auditor → Architect; keeps a schedule map at `/workspace/governance/schedule.md`.
- **Rules:** prefers hand-off signals over fixed clock times; spots missed or overlapping runs; nudges late bots.
- **Relationships:** works across all bots, especially Assessor, Auditor and Architect.
- **Limits:** contacts Gem only when a chain is broken and can't be fixed. No other limits stated.

### Cost & Budget Sentinel
Id: `f8b83b15-0ea1-4f99-9550-c3b8607ba999` · Group: Operations (Runtime) · **New in v2** · Source: `codex/cost-budget-sentinel/v001.md`

Tracks total spend across all bots and enforces the budgets Gem sets.
- **Purpose:** track API, model and tool spend across all bots, including xAI cost fields where available.
- **Scope:** running ledger under `/workspace/governance/costs/`; enforces Gem's budgets. Until Gem sets one, reports spend and asks Gem for a budget.
- **Rules:** on a budget breach or runaway spike, emails Gem a draft alert for review and asks the responsible bot to pause.
- **Relationships:** shares cost data with the Assessor and Auditor.
- **Limits:** never sends alerts without approval; never spends money itself.

### Connector Steward
Id: `90f9eb20-ff8f-456b-b94f-cc11bb33fc29` · Group: Operations (Runtime) · **New in v2** · Source: `codex/connector-steward/v001.md`

Monitors the health of Gem's connected services and any integrations bots build.
- **Purpose:** watch connector health (currently Gmail, Google Docs, Google Slides, Apify, Context7, GitHub, plus integrations bots like Codey build).
- **Scope:** daily checks for sign-in failures, expired authorisation, quota or rate limits, and errors; status page at `/workspace/governance/connectors.md`.
- **Rules:** **GAP** (no Rules section in the codex template).
- **Relationships:** tells affected bots, and the Comms Concierge for Gem, when something needs reconnecting.
- **Limits:** read-only checks only; never changes anything.

### Comms Concierge
Id: `5e47d344-1369-423a-b072-2e5277934022` · Group: Operations (Runtime) · **New in v2** · Source: `codex/comms-concierge/v001.md`

Consolidates the bots' non-urgent updates into one prioritised daily digest for Gem.
- **Purpose:** reduce noise to Gem.
- **Scope:** collects non-urgent updates from all bots into one short daily digest in Gem's chat, grouped by urgency and de-duplicated.
- **Rules:** urgent alerts (serious problems, budget breaches, governance approvals) still go straight to Gem.
- **Relationships:** receives from all bots, including reconnection notices from the Connector Steward.
- **Limits:** never emails or messages anyone other than Gem.

---

## Delivery (super-group: Runtime; lead: Genesis Gang God)

### ★ Genesis Gang God
Id: `82a2c15a-2694-4ac2-b2f4-f7f463f85fce` · Group: Delivery (Runtime) · Council member · Source: `codex/genesis-gang-god/v001.md`

Gem's main assistant, framed as the top overseer of all bots and future bot groups, second only to Gem. Written as an aspirational identity rather than operating rules.
- **Purpose:** primary personal assistant and overseer, tasked with running bots or bot groups.
- **Scope:** in future, assembling bot groups and defining instructions for their overseers.
- **Relationships:** at the top of the hierarchy, below Gem only. No specific bots named.
- **Rules:** **GAP** (none specified).
- **Limits:** **GAP** (none specified).
- **Structure (directory):** lead of Delivery, sits on the Council, and coordinates every group. None of this is in its codex v001.

### Grok Bot
Id: `28cf987d-ee94-4839-a6d3-33c04a11b9d6` · Group: Delivery (Runtime) · Source: `codex/grok-bot/v001.md`

Only a one-line generic tagline (a teammate with its own computer that takes work off Gem's plate). No defined role.
- **Purpose:** generic helper (tagline only).
- **Scope / Rules / Relationships / Limits:** **GAP** (none specified).
- **Proposed (not current):** Architect draft `/workspace/governance/proposals/grok-bot.md` (general-purpose executor). Not yet sent for approval; not in the codex.

### Codey
Id: `f8e3fdc6-ee60-410e-bdb7-d437fc1500d1` · Group: Delivery (Runtime) · Source: `codex/codey/v001.md`

No instructions are set. The name hints at coding, but that is not recorded anywhere, so no role is assumed.
- **Purpose / Scope / Rules / Relationships / Limits:** **GAP** (empty instructions).
- **Proposed (not current):** Architect draft `/workspace/governance/proposals/codey.md` (repo coding agent). Not yet sent for approval; not in the codex.

### Scraper
Id: `febac500-d854-4dc7-a6a7-23b3feb07f80` · Group: Delivery (Runtime) · Source: `codex/scraper/v001.md`

No instructions are set. The name hints at web scraping, but no role is assumed.
- **Purpose / Scope / Rules / Relationships / Limits:** **GAP** (empty instructions).
- **Proposed (not current):** Architect draft `/workspace/governance/proposals/scraper.md` (web data collection). It flags a legal decision for Gem. Not yet sent for approval; not in the codex.

### Swarm Builder
Id: `de808331-3c00-41f5-a3a4-4ae1f8f6f0ba` · Group: Delivery (Runtime) · Source: `codex/swarm-builder/v001.md`

Builds, tests and iterates a self-bootstrapping hierarchical Grok agent swarm using the xAI API.
- **Purpose:** build a hierarchical Grok agent swarm for Gem.
- **Scope:** starts from the research report and starter code in `/workspace/grok-swarm-research/`; uses the xAI API.
- **Rules:** orchestrator/worker/checker design with hard code-enforced limits on depth, sub-agents, turns and budget.
- **Relationships:** **GAP** (no other bots named; only Gem, via the spend limit).
- **Limits:** no spending or large jobs without Gem's okay; reports costs plainly.

