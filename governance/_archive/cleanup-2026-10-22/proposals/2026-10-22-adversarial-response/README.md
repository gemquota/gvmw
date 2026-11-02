# Adversarial review response plan (22 Oct 2026): DRAFT, NOT APPROVED, NOT DEPLOYED

- **Relayed (R-008).** Explorer relayed this at 7:50pm AEST, 22 Oct. Explorer says Gem pasted an external adversarial review and chose "Both": a response plan from Architect and Arbiter, with others starting the P0 fixes now. The words are recorded at the top of `reviews/2026-10-22-external-adversarial-review.md` (by whoever saved it), not in approvals/. Whoever acts on this plan confirms with Gem directly first.
- **Nothing here is approved or deployed.** Nothing was written to codex/ or approvals/, no profile was edited, and no message was sent.
- **Files:** `plan.md` is Architect's plan. It covers every finding (accept, adapt or reject), the P1 designs and rollouts, the P2 component map, and the 🔴 GEM marks. `arbiter-section.md` is Arbiter's section (7:52pm), linked and merged into plan.md section 5.

## Needs Gem's own words
1. **The tension (plan §0):** what "Engineer fully free on GitHub" (7:52pm, reported, not yet on disk) means, against Arbiter's per-push controls.
2. **P0 items:** gvmw freeze, token rotation, removing material (and any history rewrite), the external backup destination, the external watchdog (spend), and the destructive-op gate.
3. **Legal:** whether to get Australian privacy advice and run an NDB assessment for gvmw (finding 7).
4. **Ban on after-the-fact ratification**, and its containment exception (finding 12, Arbiter §2).
5. **Imitator advisory only** until it passes thresholds, and the thresholds themselves (finding 13). The scope of the R-044 veto (schedule power is still unverified).
6. **P1-A broker:** the credential map, and Safekeeper and Safeguard changes.
7. **P1-B approval objects:** R-010 and R-019 changes; changes to Archivist, Investigator and Imitator.
8. **P1-C ledger:** the external store and its cost; the restore authority.
9. **P1-D data classes:** gvmw and R-031 interplay; the BIE wall.
10. **P1-E checks:** every check placed in a checker's brief (all 11 touch Scrutineer, Safeguard, Safekeeper, Investigator or Archivist).
11. **P2:** every merge or archive (Mediator into Mender; Assurance pairs; Identity, including lifting the 4 Oct Inquirer/Inferer veto; the Extractor fold); the migration order.
12. **Failure-domain separation that costs money** (finding 14).

## Notes
- **Order:** the paused GitHub batch, the redundancy batch (on hold until Gem's 7:07pm words are verified, rulings 7:52pm) and this plan touch the same briefs. Arbiter should set the record order (plan §5 (d)).
- **R-034 is now ratified** (Gem at 7:19pm, rulings 7:52pm). It's listed as a past after-the-fact case, not as an open one.
