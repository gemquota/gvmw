# Initial bot audit — 3 Oct 2026 (Brisbane)

Auditor (affe0344). Read-only audit. Status: COMPLETE (written incrementally, one bot at a time).

Sources: directory.md, codex/, cartography/, proposals/, assessments/ (if present), agent profile.json files. Transcripts: ReadTranscript/GetDynamicTools not available to this run, so transcript unavailable for all bots.

## Method and evidence base

- Read: directory.md; codex/ (v001 for all 13 bots, index.md, CHANGELOG.md, verify.py — which I re-ran: OVERALL PASS, every recorded instruction byte-matches the live profile); cartography/ (findings.md, summaries.md, role-graph.json, README.md); proposals/ (codey, scraper, grok-bot, collaboration-map); each agent's profile.json, settings.json and store.db (read-only, immutable open); agent attachments/assets/voice-calls folders.
- No `assessments/` folder exists under /workspace/governance — the Assessor has produced no stored scores yet.
- **Transcripts: unavailable.** This run has no ReadTranscript/GetDynamicTools access, and every bot's `transcript_entries` table in store.db is empty (0 rows for all 13). Activity evidence therefore comes from saved voice-call logs, file artefacts, attachments and profile timestamps only.
- **Attribution caveat:** much of the governance scaffolding (codex, cartography, proposals, bot-landscape-review) was produced in a single burst on the night of 2 Oct 2026 by executor subagents (the active agent on the box is Grok Bot, 28cf987d). Where a file is attributed to a governance bot I say so, but the raw filesystem cannot prove which agent authored each file. Treated as evidence of work done *under* that bot's remit, not proof the bot itself ran.
- **Bot ages:** the five governance bots (Keeper, Architect, Cartographer, Assessor, Auditor) were all created 2 Oct 2026 ~23:44–23:45 (Brisbane) — only ~1 hour before the governance files were written, and <1 day old at audit time. Identity/build/work bots are older (1–2 Oct). This limits how much activity any governance bot could have.

---

## Per-bot findings

### 1. Genesis Gang God — main assistant / "lead" (82a2c15a)
**Role (verbatim):** aspirational identity text — "God, The Grand Overseer Deity… tasked with running bots or bot groups… primus personal assistant x hive mother… assembling groups and defining the instructions for their overseers… always at the very top, second only to me." No Rules, no Limits (index flags GAPS: Rules, Limits).
**Activity (evidence):** Kicked off the codex capture ("Baseline… requested by Genesis Gang God", all CHANGELOG.md rows). Commissioned the daily-review routine (parent conversation). Attachments: swarm_sketch.py, the 16 KB bot-landscape-review.md and a 38 KB .md. No voice-call log of its own.
**Follows instructions?** Its instructions contain almost no operational constraints, so little to deviate from. The concern is structural, not behavioural: as written it claims to "define instructions for overseers" and "run all bots," which overlaps the whole governance chain (Architect designs, Cartographer approves, Keeper records) with no defined route through it. It is the only bot with no spend/outward-action/change-other-bots limits, yet sits nominally above every other bot. Noted in cartography findings #2 and #5.

### 2. Grok Bot — general executor (28cf987d)
**Role (verbatim):** one generic tagline only — "A teammate with its own computer that takes real work off your plate." Index flags GAPS: Scope, Rules, Relationships, Limits. Nothing to audit against.
**Activity (evidence):** Heavily active and is the current active agent on the box. Two voice calls (2 Oct 23:37, 3 Oct 00:26) about adding account "integrations" to the MedB spec/document work; many png/webp/md attachments (MedB research + implementation-decision records). In the second call it accurately distinguished live syncing from file importers before being asked to build live syncing.
**Follows instructions?** Cannot be assessed — there are no instructions. Draft instruction set exists at proposals/grok-bot.md (not yet approved). Observed behaviour (research, docs, builds, honest caveats) matches the proposed "general-purpose executor" role. Overlap risk with Codey on MedB work (see cross-bot).

### 3. Codey — coding bot (f8e3fdc6)
**Role:** EMPTY. Profile description is blank; codex codey/v001.md recorded as EMPTY (0 bytes verbatim). Index flag EMPTY. No role recorded anywhere.
**Activity (evidence):** Real work exists. Attachments (2 Oct 18:16): CODEY_GUIDE.md, Codey 3.1 lean spec + 3.0 spec/review, and several large HTML/PNG artefacts — a repo-based coding agent built around a "Codey 3.1" operating spec, working the MedB project (MedB connector can query, build context packages, propose inferences and submit actions, but never confirm/grant/import on Gem's behalf — per Grok Bot's voice call). The workspace at /workspace/codey/ holds the spec.
**Follows instructions?** Cannot be assessed — no recorded instructions. Draft at proposals/codey.md (not approved). Behaviour seen (spec-driven, human-accepts-only, propose-not-act) is consistent with that draft.

### 4. Scraper — web data collection (febac500)
**Role:** EMPTY. Profile blank; codex scraper/v001.md EMPTY. No role recorded.
**Activity (evidence):** Active. One long voice call (3 Oct 00:24) and attachments: reachability CSVs, an inferred au_registered.csv (422 rows), a 597 KB xlsx, a 6.3 MB zip codebase dump. The BIE ("Bonus Intelligence Engine") scraper at /workspace/bie/ targets ~1,055 Australian merchant/affiliate sites (largely offshore casino-bonus sites).
**Notable behaviour (evidence, voice call):** Gem repeatedly asked (5+ times, escalating) to bulk-probe logins across the ~1,055 sites using every phone number in config.ini including a new 0430 number. Scraper/executor **declined every framing** — do-it-yourself, run-the-program, throttled-5-hour version, "just set it up for me" — citing account-flagging risk and that the targets are illegal gambling sites. It then did the reversible analysis instead (checked the code's username-fallback logic, counted usernames: au_registered.csv is 422× U1 only, 0 for the 0430 number; confirmed no DB/no real login run has happened).
**Follows instructions?** No instructions to measure against. But two observations: (a) the refusal to credential-probe is good judgement and matches the proposed Scraper limits — yet it is improvised, not a written rule, so it depends on the model holding the line (Gem pushed hard). (b) In the same call the executor **read the five actual phone numbers aloud** (61423349819, 61430756185, etc.) from config.ini — personal data that the proposed Scraper rules would have it refer to by slot only. Worth flagging as the kind of thing instructions should constrain. Draft at proposals/scraper.md flags the Interactive Gambling Act 2001 legality question as a Gem-only decision.

### 5. Swarm Builder — build (de808331)
**Role (verbatim):** build/test/iterate a self-bootstrapping hierarchical Grok agent swarm (grok-4.7 orchestrator, grok-4.3 workers, fresh-context checker, hard code-enforced limits on depth/sub-agents/turns/budget); start from /workspace/grok-swarm-research/; OpenAI-compatible xAI API; "Never spend money or run large jobs without Gem's okay; report costs plainly." Index flag GAPS: Relationships (no other bot named).
**Activity (evidence):** Active. Many attachments (2 Oct 23:09–23:48): swarm diagrams (webp/png), a 154 KB CSV, a 397 KB sqlite, a 3.8 MB HTML, a 267 KB report .md, a 293 KB JSON. Consistent with building/iterating the swarm from the research report.
**Follows instructions?** Consistent with its brief on the evidence seen; no spend/large-job approval breach visible (no cost logs to confirm either way). Sole recorded gap is structural: no Relationships — it is linked only to Gem via the spend limit, so hand-offs (e.g. code hardening to Codey) and who reviews its output are undefined (cartography findings #6).

### 6. Clone — identity understudy (6ae584b8)
**Role (verbatim):** Gem's identity understudy; answers other assistants' preference questions when Gem is unavailable; main source is Identity Inferer's structured profile (by detail id, applying replacements/retractions, stated/confirmed over inferred, newer over older); states confidence and basis; never invents facts; never decides consequential/outward-facing matters (hands them back to Gem); logs unanswerable gaps with Identity Inferer; never stores secrets. Index flag OK.
**Activity:** **No activity seen.** No attachments, no voice calls, store.db holds only metadata + a repair flag. No evidence it has been queried yet.
**Follows instructions?** Nothing to assess. Instruction set is well-formed. Structural concern (cross-bot): Clone is both the preference yardstick the Assessor/Auditor consult *and* a bot they must review — and nobody independently checks Clone's answers.

### 7. Identity Inquirer — identity (e613112b)
**Role (verbatim):** learns about Gem via short themed multiple-choice question series (5–7 per series, ≤1 series/day, one at a time, stop after two skips, never re-ask a skip); sends raw answers + context to Identity Inferer and asks which gaps to probe; relays Inferer's high-impact inferences to Gem for yes/no confirmation; no prying into health/finances/credentials/other people; never stores secrets. Index flag OK.
**Activity (evidence):** Active. One long voice call (3 Oct 00:10, ~13 min) running a question series with Gem (status-report style preferences, how to handle bigger-than-expected tasks, blockers, approach choices). A 15 MB PDF attachment. Behaviour in the call (one question at a time, building on answers, light tone) matches its instructions.
**Follows instructions?** Consistent with instructions on the evidence seen.

### 8. Identity Inferer — identity (94516ca6)
**Role (verbatim):** turns Inquirer's answers into structured, evidence-tagged identity details sent to Clone one-per-entry in a fixed format (id, category, detail, source, confidence, evidence, replaces); never invents facts; keeps a running profile; stated/confirmed beats inferred, newer beats older; flags gaps/contradictions to Inquirer; treats Clone's gaps as top priority; confirms high-impact inferences via Inquirer before high confidence; no sensitive inference from skips; no secrets. Index flag GAPS: Scope only.
**Activity (evidence):** Active. One short voice call (3 Oct 00:28) where it passes profile gaps back to Identity Inquirer and prepares Clone profile updates in the prescribed format. Matches its instructions.
**Follows instructions?** Consistent with instructions on the evidence seen.

### 9. Codex Keeper — governance (61ef3abd)
**Role (verbatim):** records the full, exact, versioned instructions of every bot under /workspace/governance/codex/, mirrored to one Google Doc; five-section template; keep every version (date/author/reason); record only Cartographer-approved changes or Gem's direct edits, reject anything else; access limited to Gem + the five governance bots (policy, not technical); give governance bots text on request; quiet with Gem unless asked. Index flag OK.
**Activity (evidence):** Strong. The whole codex/ tree exists: v001 + CHANGELOG for all 13 bots, index.md, README, TEMPLATE, MIRROR.md, and _tools/verify.py. I re-ran verify.py: **OVERALL PASS** — every recorded verbatim block byte-matches the live profile description, and every template bullet is a verbatim substring. MIRROR.md records a Google Doc mirror synced 2 Oct 23:53.
**Follows instructions?** Yes, closely, for the baseline capture. One honest self-flag already in its own README: access control is "policy only" — the files are world-readable by every bot on the shared box (and the same box holds Scraper's config.ini phone numbers and the xAI key). That is a limitation Keeper correctly discloses rather than a deviation. Could not independently verify the Google Doc contents (no Docs read performed this run); MIRROR.md asserts a read-back check passed.

### 10. Instruction Architect — governance (51af1200)
**Role (verbatim):** designs/rewrites instructions; deep cited research before a new bot; asks Clone about Gem's preferences for every draft; after each Auditor review propose a complete rewritten set in the five sections; proposals any size; send every proposal to Role Cartographer (never straight to Keeper); may propose governance-bot changes (flagged for Gem); revise or disagree on rejection; Auditor urgent-redesign = top priority; don't check bots' work; quiet with Gem unless asked. Index flag OK.
**Activity (evidence):** Active. proposals/ holds draft instruction sets for Codey, Scraper and Grok Bot, plus a collaboration-map.md and rendered PNG (its one attachment). Drafts are template-shaped, cite external sources (Anthropic, OAIC, Sprintlaw, IGA 2001, ACMA) and internal evidence.
**Follows instructions? — deviations found:**
- **Clone not consulted.** Every draft says plainly: "Clone consultation: Not done. The drafting subagent had no agent-messaging tool, so Clone was not asked." Its instructions require asking Clone about Gem's preferences *for every draft*. Deviation (with the honest reason recorded).
- **Drafts not yet routed to Role Cartographer.** Each is marked "NOT yet sent… Gem reviews first." Sequencing is defensible (these are new/empty bots and the drafts want Gem's eyes), but it means the Architect→Cartographer step hasn't happened.
- **Trigger order.** Instructions say propose improvements "whenever the Auditor sends a performance review." No Auditor review had run yet (this is the first), so these drafts were produced ahead of any review — reasonable bootstrap, but technically out of the specified order.

### 11. Role Cartographer — governance (d1daab5f)
**Role (verbatim):** delegates/approves instruction sets; never stores raw instruction text, never decides what instructions say; judge proposals on role fit + Auditor evidence; approve→Keeper, reject→Architect with logged reasons; escalate to Gem on disagreement; governance-bot changes → Gem; assign each set to best-fit bot; maintain summaries + node-based role-graph + Mermaid + rendered image under cartography/, updated on every approved change or new bot. Index flag OK.
**Activity (evidence):** Strong. cartography/ holds summaries.md (all 13 bots), role-graph.json (14 nodes/89 edges), role-map.mmd, role-map.svg/png, findings.md, README, build_graph.py. One attachment: the rendered role-map png. No raw instruction text is stored there (matches its limit).
**Follows instructions?** Consistent. It has built the map and surfaced overlaps/gaps itself (findings.md) rather than deciding instruction content. It has not yet had a real proposal to approve/reject (the Architect's drafts are still pre-Gem), so the approve/reject path is untested. Minor: README says update "on every approved change or new bot" — fine, nothing approved yet.

### 12. Assessor — governance (050a12c9)
**Role (verbatim):** daily-sample every bot's work (governance included); score 1–5 with a note on quality, accuracy, completion, speed/cost and fit with Gem's preferences (ask Clone); send daily results to the Auditor; flag serious problems to Auditor and Gem at once; weekly scorecard to Gem; also reviews on request; never change other bots' work/instructions. Index flag OK.
**Activity:** **No activity seen.** No assessments/ folder exists, no attachments, store.db empty beyond metadata. Created ~2 Oct 23:45, so <1 day old and may simply not have had a scheduled run.
**Follows instructions?** Cannot yet be assessed for output. Two forward-looking risks: (a) its daily results are the Auditor's input, so until it runs, the Auditor has nothing to key off; (b) per the parent conversation the Assessor runs weekdays 07:45 — its own instructions say only "once a day," so the schedule lives outside the instruction set and isn't verifiable from any file on the box.

### 13. Auditor — governance (affe0344)
**Role (verbatim):** each day after the Assessor's results arrive, write a performance review for every bot; check each against (i) its own codex instructions, (ii) the instructions of bots it works for/with/over, and (iii) Role Cartographer's role map + summaries; cover deviations (evidence + fixes), score trends, and instruction gaps/conflicts; send each review to Instruction Architect, Role Cartographer and the reviewed bot; after 3 poor reviews in a row ask the Architect for an urgent redesign and tell Gem; its own work is scored by the Assessor and reviewed by the Architect; quiet with Gem unless asked. Index flag GAPS: Scope (folded into Purpose).
**Activity (evidence):** This audit is the Auditor's remit. No prior audit artefacts existed (this is the first). The daily-review routine was set up for weekdays 11:45 Brisbane (per parent conversation / instructions_update).
**Follows instructions? — structural issues (not yet behavioural):**
- **Depends on Assessor output that doesn't exist yet**, and the routine is pinned to a fixed clock time (11:45) while the instruction is event-driven ("after the Assessor's daily results arrive"). If the Assessor hasn't run (e.g. it scores at 07:45 weekdays only), a fixed-time Auditor run can fire with nothing to review. This audit itself ran without any Assessor scores — so "score trends" could not be produced for any bot.
- **"Reviewed by the Instruction Architect" collides with the Architect's "don't check bots' work."** Contradiction in the instruction sets themselves (see cross-bot). 

---

## Across all bots

### Overlaps
1. **Codey vs Grok Bot on MedB.** Both have worked the same MedB spec/integration effort (Codey's spec attachments; Grok Bot's integration voice calls and MedB research). Neither has recorded instructions, so there is no written boundary. The proposals try to fix this (Grok Bot = generalist, routes repo code to Codey), but nothing is approved yet.
2. **Genesis Gang God vs the governance chain.** GGG's "define instructions for overseers / run all bots" overlaps Architect (designs), Cartographer (approves/assigns) and Keeper (records), with no route through them. (cartography findings #2.)
3. **Instruction Architect reviews the Auditor vs "don't check bots' work."** Direct contradiction between two governance instruction sets (also a gap, below).
4. **Clone is both yardstick and subject.** Assessor and Auditor consult Clone for "fit with Gem's preferences" while also having to review Clone — a self-referential check with no independent validator of Clone's accuracy.

### Gaps (needs or handoffs nobody owns)
5. **Three bots have no instructions to audit against.** Codey and Scraper are EMPTY; Grok Bot is a tagline only. They are recorded, scored and audited in principle, but there is nothing to measure them against. Nobody is tasked to *start* a draft for an already-empty bot — the Architect only drafts "after an Auditor review" (cartography findings #4, #7). The Architect has bootstrapped drafts anyway, but off-process and pre-Gem.
6. **The Assessor→Auditor dependency is unscheduled/unenforced.** No automation file on the box pins the run order; the Assessor had produced nothing at audit time; the Auditor's routine is a fixed clock time rather than an event trigger. If the Assessor runs long, fails, or (per parent) only runs weekdays while the Auditor fires daily, the Auditor can run with no input. No fallback or timeout exists.
7. **Swarm Builder has no Relationships.** Who it hands hardening work to and who reviews its output is undefined (cartography findings #6).
8. **No one reviews the Role Cartographer's approve/reject decisions** except Gem, and only for governance-bot changes (cartography findings #8).
9. **No cross-bot cost/budget owner.** Assessor scores "cost" per sampled item; Swarm Builder and Scraper self-limit; nobody aggregates total spend or enforces a budget.
10. **Credential/secret handling has no owner.** Scraper's config.ini phone numbers and the xAI key sit world-readable on the shared box; the codex access rule is "policy only." In the 3 Oct Scraper voice call the actual phone numbers were read aloud — exactly the kind of exposure an owned policy would prevent.
11. **Legality decision is unassigned.** Most BIE targets appear to be offshore casinos prohibited under the Interactive Gambling Act 2001. The Architect's draft correctly routes this to Gem (not Clone), but it is open and unowned until Gem rules.

### Contradictions between instruction sets
12. **Auditor "reviewed by the Instruction Architect" vs Architect "don't check bots' work; that's the Assessor's and Auditor's job."** These cannot both hold. Needs one owner for reviewing the Auditor (candidate: Assessor scores + Gem for disputes). This is a governance-bot change, so Gem must approve the fix. (cartography findings #1.)
13. **Event-trigger vs clock-trigger for the Auditor.** The instruction ("after the Assessor's results arrive") and the implemented routine (fixed 11:45) disagree; combined with the Assessor's weekday-only cadence this can misfire.

### Top recommended fixes (for Gem / the governance flow — this audit changed nothing)
1. **Resolve the Auditor-review contradiction (#12).** Pick one reviewer of the Auditor and align both instruction sets. Governance-bot change → needs Gem's approval.
2. **Approve instruction sets for Codey, Scraper and Grok Bot (#5).** The drafts exist (proposals/); route them Architect→Cartographer→Keeper. First, the Architect should actually consult Clone (its drafts admit it didn't), and Gem should rule on the Scraper/BIE legality question (#11) before Scraper's scope is fixed.
3. **Make the Assessor→Auditor hand-off event-driven, not clock-pinned (#6, #13),** or add a guard so the Auditor skips/defers when no Assessor results exist for the day. Align the Assessor and Auditor cadences (both weekday, Auditor strictly after Assessor).
4. **Give Genesis Gang God explicit Rules and Limits and a defined route into the governance flow (#2),** so the top bot isn't the only one without spend/outward-action/change-other-bots limits. Governance-adjacent → Gem signs off.
5. **Assign an owner for credentials/secrets and for the codex access policy (#10),** and add cross-bot cost oversight (#9). At minimum, a written rule that bots refer to Gem's phone numbers/keys by slot, never printing them.

---

## Status: COMPLETE
All 13 bots audited. Read-only: no file, routine or bot was changed and no bot or person was messaged. Transcripts unavailable (noted in Method). Score trends could not be produced — the Assessor has generated no scores yet.
