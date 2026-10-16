# Findings (role map v2, 3 Oct 2026)

Based on codex v001 for all 21 bots, the structure in `directory.md`, and the pending proposals in `/workspace/governance/proposals/`, which are shown as **proposed**, not current. Edge evidence is in `role-graph.json`. The v1 findings are kept in `findings-v1.md`.

## New conflicts
1. **Deputy approvals vs the Keeper's intake rule.** The Governance Continuity Deputy may review and approve proposals when the Cartographer stalls, but Codex Keeper v001 only records changes approved by Role Cartographer or made by Gem. Until Keeper v002 lands, a Deputy approval can't be recorded and the backup path dead-ends. Keeper v002 is being drafted, and because it changes a governance bot it needs Gem's approval. *(governance-continuity-deputy/v001, codex-keeper/v001; codex index note)*
2. **Two sources for each bot's limits.** The Compliance & Risk Officer keeps separate written limits per bot in `/workspace/governance/risk/`, alongside the Limits section of each codex entry. The two will drift. **Suggestion:** make the codex Limits section the single source of truth. CRO's register would then reference it and send any new limit through the Architect → Cartographer → Keeper flow, which its instructions already require for rule changes. *(compliance-risk-officer/v001; codex README)*
3. **The Cartographer is spot-checked by a member of its own group.** The Deputy sits in Instruction Governance, which the Cartographer leads, and the Deputy both checks the Cartographer's approvals and can stand in for it. That limits how independent the check is, and no rule says what happens when a spot-check fails. *(directory.md; governance-continuity-deputy/v001)*
4. **Genesis Gang God's position is directory-only and has no limits.** GGG leads Delivery, sits on the Council and coordinates every group, Assurance and Instruction Governance included, yet its codex has no Rules or Limits. The Compliance & Risk Officer is meant to review GGG's risky actions while GGG coordinates the CRO's own group. *(directory.md; genesis-gang-god/v001; compliance-risk-officer/v001)*
5. **Lead and Council duties aren't in any lead's codex.** None of the five leads (Cartographer, Auditor, Inferer, Conductor, GGG) has leading a group or sitting on the Council in its instructions. The Council's decision rights relative to Cartographer approval and to Gem are undefined. *(directory.md vs the five v001 files)*

## New overlaps
6. **Three bots can ask other bots to pause.** The Compliance & Risk Officer (unsafe or non-compliant work) and the Cost & Budget Sentinel (costly work) can each ask a bot to pause, and the Orchestration Conductor nudges late bots. Nothing says who wins, or who lifts a pause.
7. **Three bots detect stalls.** The Conductor (missed or late runs), the Deputy (Architect or Cartographer silent for 24 h, 4 h if urgent) and the Auditor (3 poor reviews in a row) overlap. The Conductor could feed the Deputy's trigger.
8. **The Comms Concierge has no inbound routing.** The Concierge collects every bot's non-urgent updates, but only the Connector Steward's instructions send anything to it. The Assessor's weekly scorecard and the Sentinel's spend reports still go straight to Gem, and the Sentinel emails while the others use chat.
9. **Gaps in Clone's profile are reported along three routes.** Clone (to the Inferer), the Clone Accuracy Validator (to the Inquirer and Inferer) and the Inferer (to the Inquirer) all feed gaps in. The Inferer is meant to prioritise Clone's reports, but has no rule for the Validator's.
10. **Costs are tracked in two places.** Swarm Builder reports its own costs to Gem, and the Sentinel tracks all spend. Swarm Builder isn't told to report to the Sentinel.

## Still open from v1
- **Who reviews the Auditor:** still a conflict in the codex (Auditor v001 says the Architect reviews it; Architect v001 says it doesn't check work). **Proposed fix:** Auditor v002 (Gem reviews the Auditor), awaiting Gem's approval. Shown as a dashed "PROPOSED" edge.
- **Codey and Scraper are empty, and Grok Bot has only a tagline.** Architect drafts exist in `proposals/` (codey.md, grok-bot.md, scraper.md), routed to Gem first and not yet sent to the Cartographer. They're shown as proposed edges only. The Scraper draft raises a legal question (offshore gambling sites and the Interactive Gambling Act) that only Gem can decide.
- **Swarm Builder** still names no bots, though the directory now places it in Delivery under GGG.
- **Review of Cartographer approvals:** now partly covered by the Deputy's weekly spot-check (see 3).
- **Codex access control:** the Secrets & Credentials Custodian now audits access rules, including for the codex. It's still policy only.
- **New gaps:** the Secrets Custodian, Clone Accuracy Validator and Connector Steward have no Rules section; the Conductor has no limits beyond when to contact Gem; the Sentinel has no budget yet.

## Bots with few or no role-specific edges
- Grok Bot, Codey, Scraper: no current outgoing edges; proposed edges only.
- Swarm Builder: only an edge to Gem.
- Every bot now gets incoming fan-out duties from 10 bots (Keeper, Assessor, Auditor, Cartographer, CRO, Secrets Custodian, Conductor, Sentinel, Concierge, GGG).

## Suggested next steps (short)
1. Gem: approve or decline Auditor v002 and Keeper v002 (the Keeper change lets the Deputy's approvals be recorded).
2. Agree a single source of truth for limits (codex Limits) with the Compliance & Risk Officer, via the Architect.
3. Architect: add lead and Council duties to the five leads' instructions, and Rules and Limits for GGG. Changes to the Cartographer and Auditor need Gem.
4. Define pause precedence (CRO, Sentinel, Conductor) and who lifts a pause.
5. Route non-urgent reports through the Comms Concierge in the senders' instructions, or narrow the Concierge's scope.
6. Send the Codey, Grok Bot and Scraper drafts through approval once Gem has reviewed them, with Gem deciding the Scraper/BIE question.
7. Tidy `directory.md`: the "Oversight & operations" section is duplicated.
