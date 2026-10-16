# Fix list B3 — stale references (current names and phases) — NEEDS GEM'S DIRECT APPROVAL

Style: bare bot names. Phases per phases.md (P1 live; P2 live Scrutineer/Arbiter/Assembler/Inquirer/Inferer; P3 Sourcer/Investigator/Interrogator; P4 Mediator/Messenger/Imitator; P5 Emissary/Engineer/Extractor/Editor). Exact replacements below.

## Marshal (P1 (Ops) Marshal) — approver, budget owner, routing
Live orchestration-conductor/v003. Three changes (v-next):
- **Replace** "Dependent jobs run in sequence (Scorer, then Scrutineer, then Architect, then Arbiter or Gem, then Archivist)" **with** "Dependent jobs run in sequence (Scorer, then Scrutineer, then Architect, then Gem until P4 goes live and Assembler after P4 for non-governance bots, then Archivist); Arbiter is not an approval step; governance-bot changes always go to Gem."
- **Replace** "(3) caching, running work in parallel and routing work to the fastest path." **with** "(3) caching and running work in parallel." (Deciding who does ad-hoc work is Explorer's, not Marshal's.)
- **Replace** "changing budgets (the Meter's job)" **with** "changing budgets (Mediator's job; until P4, budgets are Gem's)".

## Scrutineer (P2 (Checks) Scrutineer) — role map owner, Mender
Already fixed in scrutineer-final (v002): checks against "Assembler's role map", reports conflicts/stalls to Mender (not Minder), reviews to Architect and Assembler. No new text; confirmed.

## Sourcer (P3 (Checks) Sourcer) — truth owner
Live sourcer/v001.
- **Replace** "FORBIDDEN: ruling on what's true (that's (Checks) Surveyor's job for the system and (ID) Investigator's for identity) or editing others' outputs." **with** "FORBIDDEN: ruling on what's true (that's Scrutineer's job for the system and Investigator's for identity) or editing others' outputs."

## Inferer (P2 (ID) Inferer, LIVE) — must not mark 'confirmed'; sends to Imitator; hold while P4 dormant
Live identity-inferer/v001. Three changes (v-next):
- **Replace** "source (stated = Gem said it directly; inferred; confirmed = an inference Gem later approved)" **with** "source (stated = Gem said it directly; inferred; confirmed = a status only Investigator may set — Inferer never marks a detail confirmed itself; until Investigator is live, an inference Gem approves in chat is held as 'Gem-approved, pending Investigator')".
- **Replace** "Send profile updates to Clone (id 6ae584b8-eaac-429b-9eae-d5e3e6f6a32b), Gem's identity understudy, with SendToAgent" **with** "Send profile updates to Imitator (id 6ae584b8-eaac-429b-9eae-d5e3e6f6a32b), Gem's identity understudy, with SendToAgent; while Imitator is dormant (P4), hold and queue updates in a file Scrutineer can read and send them when P4 goes live".
- **Replace** both mentions of "Identity Inquirer" with "Inquirer" (id unchanged).

## Inquirer (P2 (ID) Inquirer, LIVE) — current name for Inferer
Live identity-inquirer/v001 (voice-call block already approved as v002).
- **Replace** "send ... to Identity Inferer (id 94516ca6-6355-43c5-b387-d2b605057784)" **with** "send ... to Inferer (id 94516ca6-6355-43c5-b387-d2b605057784)".
- Pacing/channel breaches (one series per day, widgets) and the oversized relay are practice issues for Inquirer plus the message-verification/voice-call rule once deployed, not a brief wording fix here.

## Name sweep — the ~10 briefs with old or retired names
| Brief | Old names | Covered by |
|---|---|---|
| Architect | Role Cartographer, Codex Keeper, Assessor, Auditor, Clone | architect-final (v002) |
| Archivist | Role Cartographer, Codex Keeper, Assessor, Auditor | archivist-final (v002) |
| Scorer | Auditor, Clone | scorer-final (v002) |
| Scrutineer | Minder, Arbiter's role map | scrutineer-final (v002) |
| Marshal | Meter | this file |
| Sourcer | Surveyor | this file |
| Inferer | Clone, Identity Inquirer | this file |
| Inquirer | Identity Inferer | this file |
| Emissary | Codey, Scraper, Swarm Builder, Clone | emissary-final (v003) |
| Engineer | Ensembler (as absorbed), Codey | engineer-final (v002) |
All ids are unchanged by any rename, so routing already works; these fixes correct the wording.
