# Findings (role map v1, 2 Oct 2026)

Based only on codex v001. Edge evidence is in `role-graph.json`.

## Overlaps and conflicts
1. **Architect reviewing the Auditor vs "don't check bots' work".** Auditor's instructions say its own work is reviewed by the Instruction Architect; the Architect's instructions say it must not check bots' work. Needs one owner for auditing the Auditor (e.g. Assessor scores plus Gem, or an explicit exception for the Architect). *(auditor/v001, instruction-architect/v001)*
2. **Genesis Gang God vs the governance chain.** GGG is told it will define instructions for overseers and run bot groups; that overlaps the Architect (designs instructions), Cartographer (assigns/approves) and Keeper (records). Its proposals have no defined route through the Architect → Cartographer → Keeper flow. *(genesis-gang-god/v001)*
3. **Clone answers preference questions for governance bots, but its own instructions don't name them.** Fine as a general service, but there is no rule for when Clone's answer is too low-confidence for a governance decision. *(clone, assessor, instruction-architect v001)*

## Missing roles and gaps
4. **Codey and Scraper have no instructions; Grok Bot has a tagline only.** No purpose, limits or relationships. They are still covered by Keeper (records), Assessor (scores) and Auditor (audits), but there's nothing to audit them against.
5. **Genesis Gang God has no Rules or Limits.** The top-ranked bot is the only one with no limits (e.g. on spending, outward-facing actions or changing other bots).
6. **Swarm Builder names no relationships.** Not linked to any other bot; it may end up overlapping with Grok Bot/Codey/Scraper once those are defined.
7. **Who requests instructions for new or empty bots is unclear.** The Architect drafts a new bot's instructions after research, and the Cartographer assigns them, but nobody is told to start a draft for an existing empty bot (only after an Auditor review).

## Unclear ownership
8. **Who reviews Role Cartographer's approvals?** The Auditor audits all bots, but no bot checks individual approve/reject decisions apart from Gem (for governance-bot changes).
9. **Codex mirror and access policy are policy only.** Keeper notes the files are readable by every bot on the shared computer. Worth Gem knowing; there's no technical owner for access control.

## Bots with no role-specific edges
- **Codey, Scraper, Grok Bot:** only incoming fan-out edges (recorded, scored, audited, mapped, overseen). No outgoing edges.
- **Swarm Builder:** only an edge to Gem (spend approval / cost reports).
- **Genesis Gang God:** only "second only to Gem" and an aspirational "runs all bots" fan-out; nothing concrete.

## Suggested next steps (short)
1. Ask Instruction Architect for draft instruction sets for Codey, Scraper and Grok Bot (research first, Clone for preferences), and send them to Role Cartographer.
2. Ask the Architect to propose Rules and Limits for Genesis Gang God, plus how it fits with the governance flow. (GGG isn't one of the five governance bots, but it's the top-ranked bot, so Gem should probably sign off.)
3. Settle who reviews the Auditor (finding 1). This is a governance-bot change, so it needs Gem's approval.
4. Add Relationships to Swarm Builder (who it hands work to and who checks it).
5. Re-run this map once any v002 is recorded.
