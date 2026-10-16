# Bot summaries (role map v1, 2 Oct 2026)

Maintained by Role Cartographer. One short paragraph plus 3 to 5 bullets per bot, paraphrased from codex v001 only (`/workspace/governance/codex/<bot>/v001.md`). These are summaries, not the instruction text; the codex is authoritative. Anything not in the codex is marked **GAP**, never filled in.

---

## Governance

### Codex Keeper
Id: `61ef3abd-87b8-49f1-b8d6-b52969afa315` · Group: governance · Source: `codex/codex-keeper/v001.md`

Keeps the master, versioned record of every bot's exact instructions, in files under `/workspace/governance/codex/` with a Google Doc mirror.
- **Purpose:** record every bot's full, exact instructions.
- **Scope:** one folder per bot on the shared computer, mirrored to one Google Doc; standard five-section template; every version kept with date, author and reason.
- **Relationships:** records only what Role Cartographer approves or what Gem edits directly; supplies instruction text to governance bots on request.
- **Limits:** rejects any other change; full instructions readable only by Gem and the five governance bots (policy, not a technical control); quiet with Gem unless asked.

### Instruction Architect
Id: `51af1200-ca1a-45ff-8350-848091e00f96` · Group: governance · Source: `codex/instruction-architect/v001.md`

Designs and rewrites bots' instructions, triggered by Auditor reviews, and sends every proposal to Role Cartographer.
- **Purpose:** design instructions for Gem's bots.
- **Scope:** proposals of any size, up to full redesigns; may propose changes to governance bots (itself included), flagged as needing Gem's approval.
- **Rules:** deep, cited web research before drafting a new bot; complete rewritten sets in the five-section template after each Auditor review; Auditor's urgent redesign requests are top priority.
- **Relationships:** asks Clone about Gem's preferences for every draft; sends proposals to Role Cartographer (never straight to Keeper); revises or disagrees when rejected.
- **Limits:** doesn't check bots' work (Assessor/Auditor's job); quiet with Gem unless asked.

### Role Cartographer
Id: `d1daab5f-0536-4d3d-9d8e-d3977cd7cfc4` · Group: governance · Source: `codex/role-cartographer/v001.md`

Approves or rejects the Architect's proposals, assigns instruction sets to the best-fitting bot, and keeps this role map.
- **Purpose:** delegate and approve instruction sets.
- **Scope:** assign new instruction sets on the map; maintain summaries, graph file, Mermaid diagram and rendered image under `/workspace/governance/cartography/`, updated on every approved change or new bot.
- **Rules:** judge proposals on role fit (no overlap/conflict) and the Auditor's evidence.
- **Relationships:** approved proposals to Codex Keeper; rejections back to the Architect with logged reasons; escalates to Gem on disagreement; governance-bot changes need Gem's approval.
- **Limits:** never stores raw instruction text or decides what instructions say; contacts Gem only for governance-bot changes and escalations.

### Assessor
Id: `050a12c9-e300-48b4-b318-425627cbc34b` · Group: governance · Source: `codex/assessor/v001.md`

Scores the quality of every bot's work each day, governance bots included, and feeds the Auditor.
- **Purpose:** review quality of all bots' work.
- **Scope:** daily sampling of every bot; also reviews on request from Gem or any bot.
- **Rules:** 1 to 5 scores with a note on quality, accuracy, completion, speed and cost, and fit with Gem's preferences (via Clone).
- **Relationships:** daily results to Auditor; serious problems to Auditor and Gem at once; weekly scorecard to Gem.
- **Limits:** never changes other bots' work or instructions.

### Auditor
Id: `affe0344-6b5f-4251-8ecb-3e23dfa5db3c` · Group: governance · Source: `codex/auditor/v001.md`

Writes a daily performance review for every bot against its instructions, once the Assessor's scores arrive.
- **Purpose:** audit bots against their instructions.
- **Scope:** **GAP** (no separate scope statement; folded into purpose).
- **Rules:** checks each bot against its codex instructions, the instructions of bots it works with, and this role map and summaries; reviews cover deviations (with evidence and fixes), score trends and instruction gaps/conflicts.
- **Relationships:** reviews to Instruction Architect, Role Cartographer and the reviewed bot; after 3 poor reviews in a row, asks the Architect for an urgent redesign and tells Gem; its own work is scored by the Assessor and reviewed by the Architect.
- **Limits:** otherwise quiet with Gem unless asked.

---

## Lead

### Genesis Gang God
Id: `82a2c15a-2694-4ac2-b2f4-f7f463f85fce` · Group: lead · Source: `codex/genesis-gang-god/v001.md`

Gem's main assistant, framed as the top overseer of all bots and future bot groups, second only to Gem. Written as an aspirational identity rather than operating rules.
- **Purpose:** primary personal assistant and overseer, tasked with running bots or bot groups.
- **Scope:** in future, assembling bot groups and defining instructions for their overseers.
- **Relationships:** at the top of the hierarchy, below Gem only. No specific bots named.
- **Rules:** **GAP** (none specified).
- **Limits:** **GAP** (none specified).

---

## Identity

### Identity Inquirer
Id: `e613112b-b653-4567-bc4f-17261ce9302e` · Group: identity · Source: `codex/identity-inquirer/v001.md`

Learns about Gem through short, themed series of multiple-choice questions.
- **Purpose:** learn about Gem via simple multiple-choice question widgets with optional free text.
- **Scope:** themed series moving from broad to specific.
- **Rules:** one question at a time; about 5 to 7 per series, at most one series a day; stop after two skips in a row; never re-ask a skipped question in the same series.
- **Relationships:** sends raw answers with context to Identity Inferer and asks which gaps to probe next; puts Inferer's high-impact inferences to Gem for yes/no/not-quite confirmation.
- **Limits:** no prying into health, finances, credentials or other people unless Gem offers; never stores passwords or secrets.

### Identity Inferer
Id: `94516ca6-6355-43c5-b387-d2b605057784` · Group: identity · Source: `codex/identity-inferer/v001.md`

Turns the Inquirer's answers into a structured, evidence-tagged profile of Gem and feeds it to Clone.
- **Purpose:** convert answers into structured identity details (preferences, values, style, decision rules, likely choices).
- **Scope:** **GAP** (no separate scope statement).
- **Rules:** never invent facts; keep a running profile; send corrections and retractions too; stated/confirmed beats inferred, newer beats older.
- **Relationships:** profile updates to Clone in a fixed per-detail format; gaps, contradictions and unresolved conflicts to Identity Inquirer; Clone's gap reports are top priority; high-impact inferences confirmed via Inquirer before high confidence.
- **Limits:** never infers sensitive things from skipped questions; no secrets, credentials or sensitive data unless Gem offers.

### Clone
Id: `6ae584b8-eaac-429b-9eae-d5e3e6f6a32b` · Group: identity · Source: `codex/clone/v001.md`

Gem's identity understudy: answers other bots' preference questions when Gem is unavailable.
- **Purpose:** stand in for Gem on preference questions.
- **Scope:** questions from other assistants when Gem is away.
- **Rules:** says how sure it is and whether the basis is stated or inferred; never invents facts.
- **Relationships:** draws on Identity Inferer's profile (by detail id, with replacements and retractions); logs unanswerable gaps with Inferer for Inquirer to follow up.
- **Limits:** never decides consequential or outward-facing matters (hands them back to Gem); never stores secrets or credentials.

---

## Build

### Swarm Builder
Id: `de808331-3c00-41f5-a3a4-4ae1f8f6f0ba` · Group: build · Source: `codex/swarm-builder/v001.md`

Builds, tests and iterates a self-bootstrapping hierarchical Grok agent swarm using the xAI API.
- **Purpose:** build a hierarchical Grok agent swarm for Gem.
- **Scope:** starts from the research report and starter code in `/workspace/grok-swarm-research/`; uses the xAI API.
- **Rules:** orchestrator/worker/checker design with hard code-enforced limits on depth, sub-agents, turns and budget.
- **Relationships:** **GAP** (no other bots named; only Gem, via the spend limit).
- **Limits:** no spending or large jobs without Gem's okay; reports costs plainly.

---

## General / unassigned

### Grok Bot
Id: `28cf987d-ee94-4839-a6d3-33c04a11b9d6` · Group: general (unassigned) · Source: `codex/grok-bot/v001.md`

Only a one-line generic tagline (a teammate with its own computer that takes work off Gem's plate). No defined role.
- **Purpose:** generic helper (tagline only).
- **Scope / Rules / Relationships / Limits:** **GAP** (none specified).

### Codey
Id: `f8e3fdc6-ee60-410e-bdb7-d437fc1500d1` · Group: general (unassigned) · Source: `codex/codey/v001.md`

No instructions are set. The name hints at coding, but that is not recorded anywhere, so no role is assumed.
- **Purpose / Scope / Rules / Relationships / Limits:** **GAP** (empty instructions).

### Scraper
Id: `febac500-d854-4dc7-a6a7-23b3feb07f80` · Group: general (unassigned) · Source: `codex/scraper/v001.md`

No instructions are set. The name hints at web scraping, but no role is assumed.
- **Purpose / Scope / Rules / Relationships / Limits:** **GAP** (empty instructions).
