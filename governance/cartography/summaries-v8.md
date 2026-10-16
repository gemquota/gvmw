# Bot summaries (role map v8, 15 Oct 2026 ~11:35pm AEST)

## v8 — 15 Oct 2026 ~11:35pm AEST (current)
P3 (Investigator) and P4 (Imitator) went LIVE at 11:30pm on 15 Oct 2026 (phases.md, updated 11:31pm; Gem in Explorer's chat: "Yes, switch on P3", then "and p4"). Descriptive only; v1–v7 kept as `*-vN.*`.
- **Imitator's approvals are now active** (R-019). It decides for Gem, including approvals, with no checker gate. Gem-only: spending, anything drastic or irreversible (deletions, public/shared repo pushes), and changes to Imitator or Investigator (R-015).
- Architect now proposes to Imitator as well as Gem (not for Imitator/Investigator changes). Investigator tests Imitator weekly and reviews after the fact.
- Unchanged from v7: voice-call approvals count (R-018); repo pushes go to Safeguard first (R-020); both Inquirers verified.
- Scrutineer passed the 15 Oct deployment (reviews/2026-10-15-deploy-check.md). 17 active (14 live, 3 dormant) + 9 former/retired nodes, 34 edges; P5 still Dormant. [Wording corrected 16 Oct 2026 per Scrutineer's 16 Oct review; was "17 live".]

## v7 — 15 Oct 2026 ~10:47pm AEST
Rebuilt after Architect's 15 Oct updates were deployed (22:41:03–22:42:29 AEST, Gem's 10:38pm approval). Descriptive only; v1–v6 kept as `*-vN.*`.
- **Voice-call approvals count** (R-018): Gem's words on a call are direct. A call decision passed on by another bot counts only after a 1:1 check with the bot that took the call. Archivist deployments need Archivist's chat or a call with Archivist.
- **Imitator (v005), from P4 only (P4 still Dormant):** decides anything for Gem, including approvals, with no checker gate (R-019). Never: spending; deletions or other irreversible steps, including public/shared repo pushes; changes to Imitator or Investigator (Gem only, R-015). Investigator (v003) reviews after the fact.
- **Repo pushes** (R-020): every push to a public or shared repo goes to Safeguard (v005) first unless Gem approved that push directly (red edges). Spending is always Gem's.
- **Both Inquirers verified** (R-012 second update). 0314faa4 is active. e613112b (folder gone) is verified if it reappears, and Inferer v004 accepts its series.
- Codex versions mapped: investigator v003, clone v005, compliance-risk-officer v005, identity-inferer v004, codex-keeper v006, explorer-copy v002, grok-bot v005, scraper v004. 17 active + 9 former/retired nodes, 33 edges.

Maintained by P1 (Roles) Archivist. Descriptive only from latest codex + phases.md. Scrutineer checks against reality.

**v6 delta vs v5:** Index/CHANGELOG now DELETED (~9:29am notice; who removed not recorded) for the nine gone folders. e613 re-key row corrected (folder gone, not still on disk).

**v5 delta vs v4:** Inquirer **0314faa4** is the recorded active Inquirer (v003 deployed 09:25:56; folder re-keyed; R-012 ended). Former holder **e613112b** profile gone. Inferer **v003** points at 0314faa4. Former Explorer **82a2c15a** profile gone; active Explorer remains **04dcca0d**. No unrecorded live Inquirer.

---

## P1: LIVE

### P1 (Ops) Mender — `c8401a53` — mender/v004
Incident, recovery, state and run-order steward. Absorbed Minder + Marshal.
- Owns incidents/, state/, schedule.md; stall detection; pacing/load/routing.
- Chain watchdog; hand-offs over fixed clocks.
- Stalls to Gem; does not decide what work gets done.
- No instruction changes or deleting authoritative records without Scrutineer+Gem.

### P1 (Checks) Scorer — `050a12c9` — assessor/v003
Scores live bots daily; never its own work.
- Sample from artefacts; one dimension set; self-exclusion.
- Results to Scrutineer; serious issues and scorecard to Gem.

### P1 (Checks) Safeguard — `3661a899` — compliance-risk-officer/v005
Risk review and dry runs for any bot/phase (R-013).
- Risk register; dry run ≠ go-ahead.
- Every push to a public or shared repo comes here first unless Gem approved that push directly (R-020).
- Spending decisions are always Gem's.
- Alerts Gem; proposes rules via Architect.

### P1 (Checks) Safekeeper — `52772b1d` — secrets-credentials-custodian/v004
Secrets, threats, input cleaning (from Sentinel).
- Never reads/moves secret values; R-009 draft rules not binding.

### P1 (Roles) Archivist — `61ef3abd` — codex-keeper/v006
Codex + Doc mirror + role map (cartography/).
- Gem's approvals count in chat or on a voice call (R-018); a relayed call needs a 1:1 check.
- Imitator's approvals (live since P4, 15 Oct 11:30pm) need only a 1:1 authenticity check (R-019), never for Imitator/Investigator (Gem only).
- Rebuild map within one working day of each record/deploy/merge/retirement.

### P1 (Roles) Architect — `51af1200` — instruction-architect/v003
Designs instructions; proposes to Gem (until P4) / Imitator; Archivist records.

### P1 (Work) Explorer — `04dcca0d` — explorer-copy/v002 **(active)**
Gem's 2IC; routes work; Messenger digest.
- No profile edits (R-014); voice-call rules (R-018).
- Asks Imitator (live) for decisions within its limits; repo pushes to Safeguard first (R-020).

---

## P2: LIVE

### P2 (Checks) Scrutineer — `affe0344` — auditor/v003
Audits vs instructions + reality; absorbed Surveyor; checks role map.

### P2 (Roles) Arbiter — `2133048d` — arbiter/v004
Precedence rulings; never approves; absorbed Adjudicator.

### P2 (ID) Inferer — `94516ca6` — identity-inferer/v004
Structures identity from **Inquirer 0314faa4**.
- Both Inquirers verified (R-012 second update); e613112b's series accepted if it reappears.

### P2 (Ops) Mediator — `90f9eb20` — connector-steward/v004
Health/spend; phases.md P2; live name still P4 (rename unapplied).

### P2 (ID) Inquirer — `0314faa4` — identity-inquirer/v003 **(active)**
Active recorded Inquirer (Gem 9:24am; "0314faa4 owns it"). Identity Q-widgets; one series/day per role; sends answers to Inferer.
- Both Inquirers verified (R-012 second update).

---

## P3–P4: LIVE (started 15 Oct 2026, 11:30pm AEST)

### P3 (ID) Investigator — `f2016e9b` — investigator/v003
Identity evidence ladder; absorbed Interrogator.
- Tests Imitator weekly and reviews its decisions after the fact (not a gate).

### P4 (ID) Imitator — `6ae584b8` — clone/v005
Gem's understudy, live since 15 Oct 11:30pm; its approvals now apply.
- Decides anything for Gem, including approvals, with no checker gate (R-019).
- Never: spending; anything drastic or irreversible, such as deletions or public/shared repo pushes; changes to Imitator or Investigator (Gem only, R-015).

## P5: Dormant

### P5 (Work) Emissary — `28cf987d` — grok-bot/v005
General work routed by Explorer; dormant until P5.
- May ask Imitator (live) for decisions within its limits; repo pushes to Safeguard first.

### P5 (Work) Engineer — `f8e3fdc6` — codey/v005
Code and swarm work; absorbed Ensembler; dormant until P5.
- Safeguard route; named reviewers.

### P5 (Work) Extractor — `febac500` — scraper/v004
Research and data extraction routed by Explorer; dormant until P5.
- May ask Imitator (live) taste questions/decisions within limits; legal/ToS/account stay with Gem.

---

## Former / retired — DELETED (agent folders gone, noticed ~9:29am AEST; who removed not recorded) — takeover arrows

| Former | Id | → | Note |
|---|---|---|---|
| Inquirer (former) | e613112b | 0314faa4 | Re-key at v003; profile gone; verified (R-012 second update) |
| Explorer (former) | 82a2c15a | 04dcca0d | Profile gone ~9:26am |
| Marshal | f3810109 | Mender | 9 Oct merge |
| Messenger | 5e47d344 | Explorer 04dcca0d | 9 Oct merge |
| Interrogator | d3191aa8 | Investigator | 9 Oct merge |
| Assembler | d1daab5f | Archivist (map); Gem→Imitator approvals | 9 Oct |
| Sourcer / Editor | 2fe3e92f / 2888c17a | (outright) | 9 Oct |
| Ensembler | de808331 | Engineer | 4 Oct |

## Deleted (12) — not mapped
Advocate, Meter, Expediter, Adjudicator, Indexer, Maintainer, Minder, Moderator, Sanitizer, Sentinel, Simulator, Surveyor.
