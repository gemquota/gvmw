# External adversarial review of the swarm (Gem pasted it 22 Oct 2026, 7:50pm AEST)
Gem's answer to "what to do with it": "Both" (send to Architect + Arbiter for a response plan, AND start P0 fixes).

Verdict: "interesting governance prototype, unsafe production architecture". Limits are written rules, not access controls; 17 logical principals share ~1 technical principal (shared credentials).

Key findings:
1. No technical enforcement boundary; incidents (deletions, unknown actors, public repo, undry-run pushes, unknown tokens, lost governance state, untrustworthy mtimes) prove it.
2. Credentials, not Gem, are the effective top authority.
3. Too many interdependent governance roles; governance state drift across many files.
4. INC-009: governance silently stopped ~6 days -> need a watchdog independent of the swarm that alerts the human.
5. Mender as both operator and restore/evidence custodian is circular; need external append-only snapshots.
6. Filesystem times aren't evidence; need a hash-chained event ledger.
7. gvmw: data classification failure; personal info of others may raise Privacy Act APP 11/APP 8 and NDB assessment (30 days); consult an Australian privacy lawyer.
8. BIE should be a separate data domain the public poster can't read (IGA 2026 amendments, ACMA enforcement).
9. Extractor needs explicit capability classes (public fetch, API, authenticated, personal data, bulk, bypass = banned).
10. Dry runs should be exact transaction previews; approvals bound to an action hash.
11. Model approvals as objects (principal, action hash, target, scope, expiry, no delegation).
12. Don't let after-the-fact ratification become normal.
13. Imitator (Poor twice, 3/7) should be advisory only until it passes thresholds.
14. Need independence of failure domain, not just role.
15. Reduce what needs Gem's attention: approve classes with hard bounds.
16. Explorer has too large a blast radius; split gateway/router/state/digest functions (modules, not bots).
17-19. Consolidate to ~7 components (Gateway, Operations, Governance, Assurance, Identity, Workers); make deterministic: deploy recording, role maps, heartbeat, token inventory, backups, hashes, approval matching, logging, policy and permission checks, deletion protection, repo-visibility checks, job and billing monitoring.
20. Capability broker: bots never hold raw credentials.

Ranked P0: freeze gvmw writes; rotate wide-scope/unknown GitHub tokens; audit gvmw contents + history; separate personal/sensitive/BIE material from public; independent external backup of governance; independent liveness watchdog; technically gate destructive ops.
P1: scoped capabilities; action/approval hashes; external append-only ledger; separate policy enforcement from workers; independent restore authority; independent billing monitor; data classification; disable self-authorisation loops.
P2: merges (Mender+Mediator; Scorer+Scrutineer+Safeguard+Safekeeper; Architect+Archivist(+Arbiter as deterministic policy); Inquirer+Inferer+Investigator+Imitator; Explorer reduced to Gateway; keep Emissary, Engineer, Extractor).
Keep: authority ordering, no self-evaluation, dry runs, incident records, codex, ambiguity rule, separate public actor, independent identity assessment.
Scores: conceptual governance 8, authority modelling 8, audit 7, incident awareness 8, resilience 3, access control 2, credential isolation 2, liveness 3, recovery 3, privacy 3, legal containment 4, complexity 3, agent safety 3.
