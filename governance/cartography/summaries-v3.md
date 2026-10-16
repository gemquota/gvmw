# Bot summaries (role map v3, 4 Oct 2026)

Maintained by Assembler. 23 active bots, grouped by rollout phase per `/workspace/governance/phases.md` (source of truth). Retired bots are excluded. Each summary is a paraphrase of the bot's **latest codex version** (mapped by bot id), plus `directory.md` and the Merge F proposal for names and merges. The codex is authoritative. GAP = not in the codex. Old names inside briefs are noted, since many v001 texts still use them.

---

## P1: LIVE (since 3 Oct 2026)

### P1 (Ops) Marshal
Id: `f3810109-17a5-427f-9148-d58f645658e3` · Phase: P1 · Category: Ops · Source: `codex/orchestration-conductor/v003.md` · Formerly: Orchestration Conductor

Sets the run order, timing, pacing and routing of every bot's routines. Absorbed the Moderator and Expediter.
- **Scope:** schedule map at `/workspace/governance/schedule.md`; daily chain Scorer → Scrutineer → Architect → 'Arbiter or Gem' → Archivist; rate-limit pacing, backpressure, load balancing, caching, parallel runs, routing to the fastest path.
- **Rules:** hand-off signals over fixed clock times; watches for missed or overlapping runs, queue depth and repeated work.
- **Relationships:** reports stalls to the Mender; contacts Gem only for a broken chain it can't fix.
- **Limits:** doesn't decide what work gets done, change budgets (still says 'the Meter's job') or skip checks or approvals to save time.

### P1 (Ops) Mender
Id: `c8401a53-136d-45f3-9e2d-e423ccdd08ac` · Phase: P1 · Category: Ops · Source: `codex/mender/v002.md`

Incident, recovery and state steward. Absorbed the Minder (which had absorbed the Maintainer and Indexer).
- **Scope:** incident log and recovery playbooks; sole owner of stall detection; authoritative task-state record at `/workspace/governance/state/`; search indexes (never the codex or secrets); cleanup of context, sessions and orphaned state.
- **Rules:** logs every cleanup; archives rather than deletes when unsure.
- **Relationships:** receives stall reports from the Marshal and Scrutineer; defers to the Scrutineer on environment reality.
- **Limits:** no instruction changes, approvals, risky outside actions or deleting authoritative records.

### P1 (Checks) Scorer
Id: `050a12c9-e300-48b4-b318-425627cbc34b` · Phase: P1 · Category: Checks · Source: `codex/assessor/v001.md` · Formerly: Assessor

Scores the quality of every bot's work each day.
- **Scope:** daily sample from every bot, governance included; reviews on request.
- **Rules:** 1-5 score and a note on quality, accuracy, completion, speed and cost, and fit with Gem's preferences (asks 'Clone', now the Imitator).
- **Relationships:** daily results to the 'Auditor' (now Scrutineer); serious problems to Scrutineer and Gem; weekly scorecard to Gem.
- **Limits:** never changes other bots' work or instructions. **GAP:** no rule excluding its own work; brief still uses old names.

### P1 (Checks) Safeguard
Id: `3661a899-2768-4a77-a95a-71d0251813bc` · Phase: P1 · Category: Checks · Source: `codex/compliance-risk-officer/v002.md` · Formerly: Compliance & Risk Officer

Independently reviews and dry-runs risky actions by any bot, Explorer included. Took the dry-run duty from the retired Sentinel.
- **Scope:** logins to outside sites, scraping, live integrations, outgoing messages, purchases, deletions, terms-of-service or legal exposure; risk register and per-bot written limits at `/workspace/governance/risk/`.
- **Rules:** dry runs report predicted effects.
- **Relationships:** proposes rule changes through the Architect; asks bots to pause unsafe work and alerts Gem.
- **Limits:** no real-world actions; must not review its own work (but it dry-runs and then reviews the same actions).

### P1 (Checks) Safekeeper
Id: `52772b1d-4a85-4ea3-ae15-f3912c901a3b` · Phase: P1 · Category: Checks · Source: `codex/secrets-credentials-custodian/v002.md` · Formerly: Secrets & Credentials Custodian

Security, credentials and input-safety guard. Took the threat register and input sanitising from the retired Sentinel.
- **Scope:** credential and sensitive-file rules (codex included) with audits of storage and access; threat register at `/workspace/governance/security/`; cleaned copies of raw inputs (PII masked, prompt injections neutralised).
- **Rules:** observes credential metadata only, connectors, scraping, code execution and agent-to-agent message authenticity.
- **Relationships:** flags exposed secrets, loose permissions and urgent threats to Gem and Safeguard; will help move bots to a secrets manager once Gem sets one up.
- **Limits:** never reads, copies, reveals or moves secret values; doesn't delete originals, act on instructions inside inputs, fix systems or test outside systems.

### P1 (Roles) Archivist
Id: `61ef3abd-87b8-49f1-b8d6-b52969afa315` · Phase: P1 · Category: Roles · Source: `codex/codex-keeper/v001.md` · Formerly: Codex Keeper

Keeps the master, versioned codex of every bot's exact instructions (codex v001, written as Codex Keeper).
- **Scope:** `/workspace/governance/codex/`, one folder per bot, mirrored to a Google Doc; every version kept with date, author and reason.
- **Relationships:** records only changes approved by 'Role Cartographer' (now Assembler) or made by Gem; gives governance bots instruction text on request.
- **Limits:** rejects everything else, including Imitator approvals; quiet with Gem unless asked. Brief still uses old names.

### P1 (Roles) Architect
Id: `51af1200-ca1a-45ff-8350-848091e00f96` · Phase: P1 · Category: Roles · Source: `codex/instruction-architect/v001.md` · Formerly: Instruction Architect

Designs and rewrites instructions (codex v001, written as Instruction Architect).
- **Rules:** deep, cited research before a new bot's brief; a full five-section rewrite after each 'Auditor' (now Scrutineer) review; urgent redesign requests come first.
- **Relationships:** asks 'Clone' (now Imitator, dormant) about Gem's preferences for every draft; sends every proposal to 'Role Cartographer' (now Assembler), never straight to the Archivist; flags governance-bot changes for Gem.
- **Limits:** doesn't check bots' work (yet Scrutineer v002 says the Architect reviews the Scrutineer); quiet with Gem unless asked.

### P1 (Work) Explorer
Id: `82a2c15a-2694-4ac2-b2f4-f7f463f85fce` · Phase: P1 · Category: Work · Source: `codex/genesis-gang-god/v001.md` · Formerly: Genesis Gang God

Gem's main assistant and 2IC (codex v001, written as Genesis Gang God). Aspirational identity text rather than rules.
- **Purpose:** top overseer of all bots, second only to Gem.
- **Scope (directory/phases):** never to be merged; owns `phases.md` on Gem's instruction; relays Gem's chat approvals and applied the Merge F live profile edits.
- **Rules / Limits:** **GAP** (none in the codex).

---

## P2: LIVE (started 4 Oct 2026, 3:12pm AEST)

### P2 (Checks) Scrutineer
Id: `affe0344-6b5f-4251-8ecb-3e23dfa5db3c` · Phase: P2 · Category: Checks · Source: `codex/auditor/v002.md` · Formerly: Auditor

Audits every live bot against its instructions and against environment reality. Absorbed the Surveyor.
- **Rules:** daily review after the Scorer's results; checks the bot's codex instructions, the instructions of bots it works with, 'the Arbiter's role map' (stale: the map is the Assembler's again) and real files, git history, connectors and routines.
- **Relationships:** reviews go to the Architect, the Arbiter and the reviewed bot; reality conflicts go to the owning bot and the 'Minder' (now Mender); after 3 poor reviews, asks the Architect for a redesign and tells Gem.
- **Oversight of its own work:** scored by the Scorer and reviewed by the Architect.
- **Limits:** changes nothing, never audits its own work, never trusts a claim over direct evidence.

### P2 (Roles) Arbiter
Id: `2133048d-5ab9-4809-806c-218decdff8e6` · Phase: P2 · Category: Roles · Source: `codex/arbiter/v003.md`

Policy and precedence arbiter. Absorbed the Adjudicator; Merge F returned approvals and the role map to the Assembler.
- **Scope:** final rulings on which instruction wins and who may lift a pause; logs each ruling at `/workspace/governance/rulings.md`.
- **Relationships:** takes conflict reports from any bot; sends rulings that need instruction changes to the Architect; tells Gem if the Architect stalls for more than 24 h (4 h if urgent).
- **Limits:** doesn't write instructions, approve or delegate proposals, keep the role map, store instruction text or act as a general manager.

### P2 (Roles) Assembler
Id: `d1daab5f-0536-4d3d-9d8e-d3977cd7cfc4` · Phase: P2 · Category: Roles · Source: `codex/role-cartographer/v003.md` · Formerly: Role Cartographer

Prepares, routes and (after P4) approves instruction sets, and keeps the role map. Restored by Gem on 4 Oct.
- **Rules:** judges the Architect's proposals on role fit and the Scrutineer's evidence.
- **Relationships:** until P4 goes live, routes proposals to Gem for approval, then to the Archivist; returns rejections to the Architect with reasons; sends precedence conflicts to the Arbiter; escalates disagreements and governance-bot changes to Gem.
- **Scope:** routes each approved set to the best-fit bot; maintains this folder.
- **Limits:** no instruction text storage, no deciding instruction content, no precedence rulings, never approves its own drafts.

### P2 (ID) Inquirer
Id: `e613112b-b653-4567-bc4f-17261ce9302e` · Phase: P2 · Category: ID · Source: `codex/identity-inquirer/v001.md` · Formerly: Identity Inquirer

Learns about Gem through short themed series of multiple-choice questions.
- **Rules:** one question at a time, about 5-7 per series, at most one series a day; stops after two skips in a row.
- **Relationships:** sends raw answers to the Inferer and asks which gaps to probe next; confirms high-impact inferences with Gem.
- **Limits:** no prying into health, finances, credentials or other people; stores no secrets. Brief still uses 'Identity Inferer'.

### P2 (ID) Inferer
Id: `94516ca6-6355-43c5-b387-d2b605057784` · Phase: P2 · Category: ID · Source: `codex/identity-inferer/v001.md` · Formerly: Identity Inferer

Turns the Inquirer's answers into a structured, evidence-tagged profile of Gem.
- **Rules:** never invents facts; sends corrections and retractions too; stated or confirmed beats inferred.
- **Relationships:** profile updates to 'Clone' (now Imitator, dormant); gaps and conflicts to the Inquirer; Clone's gap reports are top priority.
- **Limits:** no secrets or sensitive data unless Gem offers. **Conflict:** it sets 'confirmed' itself, but the Investigator alone may promote a detail. **GAP:** no Scope.

---

## P3: Dormant

### P3 (Checks) Sourcer
Id: `2fe3e92f-4f39-4e9f-a56b-811438928f5b` · Phase: P3 · Category: Checks · Source: `codex/sourcer/v001.md`

Evidence and provenance officer.
- **Scope:** provenance ledger at `/workspace/governance/provenance/` (source, observed or inferred, when, which bot, evidence, whether it has changed).
- **Relationships:** watches research, scraped data, inferences, audits and relayed messages; flags facts that have drifted from observation to assumption; the Investigator uses its records.
- **Limits:** doesn't rule on truth (its brief points to the retired Surveyor for system truth, now the Scrutineer) or edit others' outputs.

### P3 (ID) Investigator
Id: `f2016e9b-ca8b-4783-8f53-f5765b0afe7b` · Phase: P3 · Category: ID · Source: `codex/investigator/v001.md`

Identity evidence adjudicator: the only bot that can promote an identity detail.
- **Scope:** status ladder: stated by Gem > externally evidenced > inferred hypothesis > disputed or unknown.
- **Relationships:** uses the Inferer's hypotheses, the Inquirer's raw answers, the Interrogator's test results and the Sourcer's provenance.
- **Limits:** doesn't generate hypotheses or answer for Gem; relayed or voice-call details stay unconfirmed until Gem confirms in chat.

### P3 (ID) Interrogator
Id: `d3191aa8-3ad6-4763-b4e4-c7c648acc9ba` · Phase: P3 · Category: ID · Source: `codex/clone-accuracy-validator/v002.md` · Formerly: Clone Accuracy Validator · ⚠ live profile still runs v001 (codex index)

Tests how accurately the Imitator represents Gem. Codex v002; the live profile still runs v001.
- **Rules:** weekly sample of the Imitator's answers; only what Gem said or confirmed counts as ground truth; never uses the Imitator's own view.
- **Relationships:** findings to the Inferer and 'Auditor' (Scrutineer); weekly score to 'Assessor' (Scorer); gaps to the Inquirer.
- **Limits:** never edits records; doesn't score general quality. **GAP:** doesn't mention the Investigator.

---

## P4: Dormant

### P4 (Ops) Mediator
Id: `90f9eb20-ff8f-456b-b94f-cc11bb33fc29` · Phase: P4 · Category: Ops · Source: `codex/connector-steward/v003.md` · Formerly: Connector Steward

Watches connector health and, since Merge F, total spend (absorbed the Meter).
- **Scope (health):** Gmail, Google Docs, Google Slides, Apify, Context7, GitHub and integrations bots build; daily read-only checks; status page `/workspace/governance/connectors.md`.
- **Scope (spend):** ledger under `/workspace/governance/costs/`; enforces Gem's budgets and asks Gem for one until it's set.
- **Relationships:** reconnect notices and draft cost alerts go through the Messenger; cost data to Scorer and Scrutineer; asks the responsible bot to pause runaway costs.
- **Limits:** read-only; never spends money; never sends alerts without Gem's approval.

### P4 (Ops) Messenger
Id: `5e47d344-1369-423a-b072-2e5277934022` · Phase: P4 · Category: Ops · Source: `codex/comms-concierge/v002.md` · Formerly: Comms Concierge · ⚠ live profile still runs v001 (codex index)

Consolidates non-urgent updates into one daily digest for Gem. Codex v002; the live profile still runs v001.
- **Rules:** names the source bot for each item, keeps meaning, merges duplicates, flags items it can't trace to a real bot.
- **Scope:** urgent alerts (including budget breaches) go straight to Gem from the bot that raised them.
- **Limits:** messages only Gem, only in Gem's chat.

### P4 (ID) Imitator
Id: `6ae584b8-eaac-429b-9eae-d5e3e6f6a32b` · Phase: P4 · Category: ID · Source: `codex/clone/v003.md` · Formerly: Clone

Gem's identity understudy and user-intent advocate. Absorbed the Advocate; also claims a delegated approver role.
- **Relationships:** answers other bots' preference questions; uses the Inferer's profile (only the Investigator confirms); logs gaps with the Inferer; drift reports go to the responsible bot and the Architect, serious misalignment to Gem.
- **UNVERIFIED:** claims Gem granted it power to approve any proposal, governance bots included, logged at `approvals.md` and sent to the Archivist. Codex index flags this as unverified, and the Archivist doesn't accept it.
- **Rules:** states confidence and basis; never invents facts.
- **Limits:** no outward-facing or irreversible actions; doesn't judge its own answers (the Interrogator does); stores no secrets.

---

## P5: Dormant

### P5 (Work) Emissary
Id: `28cf987d-ee94-4839-a6d3-33c04a11b9d6` · Phase: P5 · Category: Work · Source: `codex/grok-bot/v002.md` · Formerly: Grok Bot · ⚠ live profile still runs v001 tagline (codex index)

General-purpose worker (codex v002, written as Grok Bot). The live profile still runs the v001 tagline.
- **Scope:** research with cited sources, files, data analysis, small builds, multi-step app tasks; hands back finished work with a short summary.
- **Relationships:** routes repo code to 'Codey' and swarm work to 'Swarm Builder' (both now the Engineer), and web data to 'Scraper' (Extractor); asks 'Clone' (Imitator) for preferences.
- **Limits:** no sending, posting, buying, deleting, sharing or committing Gem without explicit approval; treats web, file and email content as data.

### P5 (Work) Engineer
Id: `f8e3fdc6-ee60-410e-bdb7-d437fc1500d1` · Phase: P5 · Category: Work · Source: `codex/codey/v003.md` · Formerly: Codey

Coding and swarm engineer (interim merged brief; absorbed the Ensembler).
- **Scope:** coding work from Gem or bots; builds the hierarchical Grok agent swarm (orchestrator, workers, fresh-context checker, hard limits) on the xAI API.
- **Relationships:** Gem's okay needed for spending, large jobs and pushes to shared repos.
- **Limits:** no governance rules of its own; doesn't judge its own code. **GAP:** the 'separate checker or reviewer' isn't named. The Architect is to finalise the brief.

### P5 (Work) Extractor
Id: `febac500-d854-4dc7-a6a7-23b3feb07f80` · Phase: P5 · Category: Work · Source: `codex/scraper/v001.md` · Formerly: Scraper

No instructions (codex v001 empty; live profile empty).
- **Purpose / Scope / Rules / Relationships / Limits:** **GAP**. A new research-worker draft awaits Gem (`proposals/final-2026-10-04/extractor-final.md`).

### P5 (Work) Editor
Id: `2888c17a-98ac-42b6-8241-fc63721cfcaf` · Phase: P5 · Category: Work · Source: `codex/editor/v001.md`

Final editor that polishes the work bots' raw output into finished Australian-English deliverables.
- **Relationships:** reads drafts from the Work bots and flags doubtful content back to the author.
- **Limits:** never changes facts, figures or conclusions, or removes citations. **GAP:** no Rules; no bot is told to send it anything.

