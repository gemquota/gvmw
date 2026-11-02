# Role map v3 fixes — 2026-10-04 (for Gem to approve)

Drafted by Architect from Assembler's role map v3 (`cartography/findings.md`), Scrutineer's reality baseline (`reviews/2026-10-04-reality-baseline.md`), `phases.md`, `directory.md`, `rulings.md` and the `proposals/final-2026-10-04/` texts. **Every item here NEEDS GEM'S DIRECT APPROVAL.** These build on the finals; where a bot already has a final, the fix supersedes it with a **v-next** (noted) rather than forking it. Style: bare bot names, Australian English, plain. No profiles edited, nothing written to `codex/`, no agents messaged.

## Files
| File | What it covers |
|---|---|
| `roles-pipeline.md` | Part A: the five-stage Roles pipeline (draft / check / approve / record / apply+verify), the "until P4" variant, the profile-edit power flag and Gem's delegation wording |
| `fix-01-self-checking.md` | B1: independent checkers for Safeguard, Scorer, Mender, Imitator, Scrutineer/Architect, Engineer |
| `fix-02-overlaps.md` | B2: one owner each for stalls, pauses, routing, state, preference fit, truth, identity confirmation, cost alerts |
| `fix-03-stale-references.md` | B3: current names/phases for Marshal, Sourcer, Inferer, Inquirer (+ name-sweep table) |
| `fix-04-gaps.md` | B4: Extractor, Editor, input→Safekeeper and risky-action→Safeguard routes, Explorer |
| `fix-05-imitator-approval.md` | B5: leave Imitator approval as is, flag UNVERIFIED |
| `fix-06-not-in-codex.md` | B6: nothing recorded yet, pending Gem's direct confirmation |

## One-line summary of each fix
- **Pipeline (A):** Architect drafts → Scrutineer checks → Assembler approves (Gem until P4) → Archivist records → Assembler applies with Archivist byte-check + Scrutineer audit; Arbiter rules conflicts.
- **Safeguard (B1):** splits dry-run from signing off the same action; Scrutineer audits its dry-run reports.
- **Scorer (B1):** excludes itself from scoring; Scrutineer reviews Scorer, Gem reviews Scrutineer.
- **Mender (B1):** no deleting its own records without Scrutineer verifying and Gem approving; widened protected list.
- **Imitator (B1):** Interrogator samples its alignment verdicts, not just answers.
- **Scrutineer/Architect (B1):** confirmed — Architect checks no one; Gem reviews Scrutineer (finals already do this).
- **Engineer (B1):** names the reviewers — separate fresh-context verifier + Scrutineer audit + Gem's correctness sign-off.
- **Stalls (B2):** one owner, Mender (R-006); Arbiter only reports and escalates.
- **Pauses (B2):** Arbiter lifts pauses set by Safeguard and Mediator; both now refer to Arbiter.
- **Routing (B2):** Marshal = routine timing/throughput; Explorer = ad-hoc work; "fastest-path routing" removed from Marshal.
- **State (B2):** Mender owns the authoritative state record; Engineer's checkpoint and Marshal's schedule aren't it.
- **Preference fit (B2):** Imitator owns the model; Scorer consumes it (n/a until P4).
- **Truth (B2):** Scrutineer rules system truth, Investigator identity truth; Sourcer owns provenance only.
- **Identity confirmation (B2/B3):** Inferer never marks 'confirmed'; only Investigator promotes.
- **Cost alerts (B2):** one route — Mediator drafts, Messenger delivers to Gem as urgent, never without Gem's approval.
- **Marshal (B3):** approver = Gem until P4 then Assembler (Arbiter not an approval step); budget owner Mediator; drop fastest-path routing.
- **Sourcer / Inferer / Inquirer (B3):** current names (Scrutineer, Imitator, Inferer, Inquirer).
- **Extractor (B4):** reuse extractor-final; add input→Safekeeper and risky-action→Safeguard routes.
- **Editor (B4):** add Rules and an incoming route (Emissary/Engineer/Extractor send drafts; returns to author and Gem).
- **Routing gaps (B4):** raw inputs go to Safekeeper for cleaning; planned risky actions go to Safeguard for a dry run.
- **Explorer (B4):** reuse explorer-final (2IC, first point of contact, never merged, R-007 limit).
- **Imitator approval (B5):** unchanged, flagged UNVERIFIED until Gem confirms with Archivist.
- **Not in codex (B6):** the 14 queue items, the finals and these fixes are all unrecorded, pending Gem.

## Judgement calls for Gem
1. **Profile-edit power (A):** giving Assembler (or any bot) the power to edit live profiles conflicts with "only Gem applies" and R-007. Gem must send the written delegation in `roles-pipeline.md` before any bot applies profile edits. This also settles who applies edits (Explorer does today, unbriefed).
2. **Who reviews Scrutineer:** Gem (per the earlier decision) vs Architect. Finals assume Gem — confirm.
3. **Imitator approval grant (B5):** confirm or revoke, in Gem's own words, to Archivist.
4. **Engineer correctness sign-off (B1):** Gem, or a code reviewer Gem names?
5. **Preference source until P4 (B2):** with Imitator dormant, preference fit is n/a; accept that or appoint an interim source.
6. **directory.md groups/Council (B4):** refresh is Explorer's or Assembler's job, not an instruction-set change — Gem to direct.
