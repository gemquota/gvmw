# Bot summaries (role map v5, 9 Oct 2026 ~9:27 AEST)

Maintained by P1 (Roles) Archivist. Descriptive only from latest codex + phases.md. Scrutineer checks against reality.

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

### P1 (Checks) Safeguard — `3661a899` — compliance-risk-officer/v004
Risk review and dry runs for any bot/phase (R-013).
- Risk register; dry run ≠ go-ahead.
- Alerts Gem; proposes rules via Architect.

### P1 (Checks) Safekeeper — `52772b1d` — secrets-credentials-custodian/v004
Secrets, threats, input cleaning (from Sentinel).
- Never reads/moves secret values; R-009 draft rules not binding.

### P1 (Roles) Archivist — `61ef3abd` — codex-keeper/v005
Codex + Doc mirror + role map (cartography/).
- Gem approvals until P4; then Imitator (except Imitator/Investigator).
- Rebuild map within one working day of each record/deploy/merge/retirement.

### P1 (Roles) Architect — `51af1200` — instruction-architect/v003
Designs instructions; proposes to Gem (until P4) / Imitator; Archivist records.

### P1 (Work) Explorer — `04dcca0d` — explorer-copy/v001 **(active)**
Gem's 2IC; routes work; Messenger digest; applies Gem-approved profile edits in own chat only.

---

## P2: LIVE

### P2 (Checks) Scrutineer — `affe0344` — auditor/v003
Audits vs instructions + reality; absorbed Surveyor; checks role map.

### P2 (Roles) Arbiter — `2133048d` — arbiter/v004
Precedence rulings; never approves; absorbed Adjudicator.

### P2 (ID) Inferer — `94516ca6` — identity-inferer/v003
Structures identity from **Inquirer 0314faa4**; e613112b (if reappears) unverified.

### P2 (Ops) Mediator — `90f9eb20` — connector-steward/v004
Health/spend; phases.md P2; live name still P4 (rename unapplied).

### P2 (ID) Inquirer — `0314faa4` — identity-inquirer/v003 **(active)**
Active recorded Inquirer (Gem 9:24am; "0314faa4 owns it"). Identity Q-widgets; one series/day per role; sends answers to Inferer.

---

## P3–P5: Dormant

### P3 Investigator — `f2016e9b` — investigator/v002 — absorbed Interrogator; Imitator tests when P4.
### P4 Imitator — `6ae584b8` — clone/v004 — understudy; approver once P4.
### P5 Emissary — `28cf987d` — grok-bot/v004 · Engineer — `f8e3fdc6` — codey/v005 · Extractor — `febac500` — scraper/v003.

---

## Former / retired (profiles gone) — takeover arrows

| Former | Id | → | Note |
|---|---|---|---|
| Inquirer (former) | e613112b | 0314faa4 | Re-key at v003; R-012 ended; profile gone |
| Explorer (former) | 82a2c15a | 04dcca0d | Profile gone ~9:26am |
| Marshal | f3810109 | Mender | 9 Oct merge |
| Messenger | 5e47d344 | Explorer 04dcca0d | 9 Oct merge |
| Interrogator | d3191aa8 | Investigator | 9 Oct merge |
| Assembler | d1daab5f | Archivist (map); Gem→Imitator approvals | 9 Oct |
| Sourcer / Editor | 2fe3e92f / 2888c17a | (outright) | 9 Oct |
| Ensembler | de808331 | Engineer | 4 Oct |

## Deleted (12) — not mapped
Advocate, Meter, Expediter, Adjudicator, Indexer, Maintainer, Minder, Moderator, Sanitizer, Sentinel, Simulator, Surveyor.
