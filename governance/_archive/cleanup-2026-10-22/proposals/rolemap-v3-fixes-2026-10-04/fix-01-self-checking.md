# Fix list B1 — self-checking (name an independent checker for each) — NEEDS GEM'S DIRECT APPROVAL

Principle: no bot grades or verifies its own work. Style: bare bot names. Each item gives the exact text to add or change, building on final-2026-10-04 where a final exists.

## Safeguard (P1 (Checks) Safeguard) — split dry-run from review of the same action
Supersedes safeguard-final (v002) with a **v-next** sentence change. Problem (findings 1 / G5): Safeguard dry-runs a risky action and then reviews the same action.
- **Add to Scope/Rules:** "Dry-running an action and signing off that same action are separate jobs: Safeguard produces the dry-run prediction and the risk review, but it never gives the go-ahead on an action it has dry-run — the go/no-go stays with the action's owner, and with Gem for high-consequence actions."
- **Add to Relationships:** "Scrutineer independently audits Safeguard's dry-run reports and risk reviews for quality; Safeguard reviews nothing of its own."
- Keeps the existing FORBIDDEN line "never reviews or dry-runs its own work".

## Scorer (P1 (Checks) Scorer) — exclude self; name an independent checker
Supersedes scorer-final (v002) with a **v-next** change. Problem (finding 2): Scorer scores "every bot ... included" with no self-exclusion, and nobody independently scores Scorer.
- **Replace** "Each weekday, sample recent work from every live bot." **with** "Each weekday, sample recent work from every live bot except Scorer itself; Scorer never scores its own work."
- **Add to Relationships:** "Scrutineer independently reviews Scorer's quality and its adherence to instructions; Gem reviews Scrutineer. Scorer does not score Scorer."

## Mender (P1 (Ops) Mender) — independent check before deleting its own records
No Mender final yet; this builds on mender-delta and mender/v002. Problem (finding 3): Mender owns state and indexes and also decides what to clean up, judging its own records disposable.
- **Replace the FORBIDDEN clause** "deleting authoritative records (the codex, provenance, incident logs, the state record)" **with** "deleting authoritative records (codex, provenance, incident logs, state record, proposals, approvals, cartography, rulings.md, risk/ and security/); deleting any of its own state or index records without Scrutineer verifying the record is disposable and Gem approving the deletion."
- **Add:** "Mender archives rather than deletes when unsure, logs every cleanup, and never judges its own records disposable on its own."

## Imitator (P4 (ID) Imitator) — don't self-grade verdicts or approvals
Dormant (P4); no final here. Problem (finding 4): Imitator gives alignment verdicts (and, if the grant stands, approvals) against its own preference model, and Interrogator tests only its answers.
- **Add to Interrogator's scope (see fix-02):** "Interrogator also samples Imitator's alignment verdicts, not only its answers, and reports wrong or unsupported verdicts."
- **Flag:** Imitator's approval power is left as is and marked UNVERIFIED pending Gem (see fix-05). While unverified, Imitator approvals are recommendations only and Archivist rejects them.

## Scrutineer and Architect — stop checking each other; Architect checks no one
Scrutineer-final (v002) already routes Scrutineer's review to Gem and Architect-final (v002) already says Architect checks no bots' work. Problem (finding 5) is resolved by those two finals; confirmed here with no new text:
- Architect: "Don't check bots' work yourself" stands; Architect is scored by Scorer and audited by Scrutineer.
- Scrutineer: reviewed by Gem (flagged in scrutineer-final for Gem's confirmation), scored by Scorer.
- **Judgement call for Gem:** confirm Gem (not Architect) reviews Scrutineer.

## Engineer (P5 (Work) Engineer) — name the reviewer
Supersedes engineer-final (v002) with a **v-next** addition. Problem (finding 6): Engineer is forbidden to judge its own code but no reviewer is named.
- **Add to Relationships/Rules:** "Engineer never signs off its own code. Its own separate fresh-context verifier reruns the tests; independently, Scrutineer audits Engineer's deliverables against the confirmed intent, and Gem (or a code reviewer Gem names) gives the final correctness sign-off before anything is accepted."
