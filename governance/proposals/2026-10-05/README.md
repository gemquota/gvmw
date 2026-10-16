> **6 Oct 2026, 8:15am AEST:** five files here are SUPERSEDED by `../2026-10-06/` versions (archivist-v004, explorer-v004, safekeeper-v004, inquirer-v002, inferer-v002). The other seven stand. See `../2026-10-06/PRIORITY.md` for the order to approve in.

# Proposals for 5 Oct 2026 — from Scrutineer's reviews — NEEDS GEM'S DIRECT APPROVAL

Drafted by Architect from `reviews/2026-10-05.md` (Architect section and fix queue) and `reviews/streaks.md` (day 1; no Poor streaks, so no urgent redesigns). Style: bare bot names, Australian English, plain. **Every file here NEEDS GEM'S DIRECT APPROVAL.** Gem approves directly until P4 goes live, and governance-bot changes go to Gem. No profiles edited, nothing written to `codex/`, no agents messaged.

## Base checked first
- `codex/index.md` and `codex/_tools/verify.py` (run read-only, 5 Oct about 11:58am AEST): **36/36 latest codex versions match live profiles; OVERALL PASS.** So for each bot, "recorded" and "live" are the same version, and every proposal is built on that text.
- The index status cells still say "APPROVED, NOT YET DEPLOYED" for versions that are live; verify.py is the evidence I used (Scrutineer's reality conflict 2).

## Files
| Item | File | Bot | Current (recorded = live) | Next | One-line change | Approver |
|---|---|---|---|---|---|---|
| 1 | `marshal-v004.md` | Marshal | orchestration-conductor v003 | **v004** | Meter out (Gem sets budgets; Mediator once P4); approver chain = Gem until P4, then Assembler/Imitator, governance to Gem or Imitator; Arbiter not an approval step; drop "fastest path"; stalls to Mender | Gem |
| 2 | `scorer-v003.md` | Scorer | assessor v002 | **v003** | One dimension set for profile and routine; sample from files and `git log --all` across /workspace; no-artefact bots "not scored"; never scores itself | Gem (governance) |
| 3 | `safeguard-v004.md` | Safeguard | compliance-risk-officer v003 | **v004** | Receives the pre-action route and replies; logs Gem-approved actions; after-the-fact sweep each run; wider risky-action list; dry run ≠ go-ahead; pause lifts to Arbiter | Gem (governance) |
| 3 + 4 | `archivist-v004.md` | Archivist | codex-keeper v003 | **v004** | R-007 exception: deploy only on Gem's own words in its own chat, exact recorded text, Scrutineer checks independently; tell Safeguard first; current-state status cells; tell Assembler after each record/deploy | Gem (governance) |
| 3 + 7 | `explorer-v004.md` | Explorer | genesis-gang-god v003 | **v004** | Until P4, non-urgent items to Gem in one daily message (Messenger digest once live); "Gem approves until P4"; Safeguard route for own and routed risky work | Gem (R-008: confirmed directly, not via Explorer) |
| 3 | `emissary-v004.md` | Emissary | grok-bot v003 | **v004** | Safeguard pre-action route; raw inputs to Safekeeper before passing to another bot; Imitator once P4 | Gem |
| 3 | `engineer-v005.md` | Engineer | codey v004 | **v005** | Safeguard pre-action route; names its reviewers (verifier, Scrutineer, Gem's sign-off) | Gem |
| 3 | `extractor-v003.md` | Extractor | scraper v002 | **v003** | Safeguard dry run per new job/target or scope change; raw inputs to Safekeeper; Imitator once P4 | Gem |
| 5 | `inferer-v002.md` | Inferer | identity-inferer v001 | **v002** | Hold and queue updates in memory until P4, then send in numbered parts; never sets "confirmed" (Investigator only); current names; approved VOICE CALLS block | Gem |
| 6 | `inquirer-v002.md` | Inquirer | identity-inquirer v001 | **v002** | Approved VOICE CALLS block recorded; voice-call series allowed under the same limits (one a day across chat and calls); current names | Gem |
| 8 | `arbiter-v004.md` | Arbiter | arbiter v003 | **v004** | R-006: report Architect stalls to Mender and tell Gem; pause lifts name Safeguard and Mediator; Arbiter never approves | Gem (governance) |
| S2 | `safekeeper-v004.md` | Safekeeper | secrets-credentials-custodian v003 | **v004** | Owns the browser-artefact handling rule; checks shared browser-output folders by metadata only; flags leftovers; removing existing files stays Gem's call | Gem (governance) |

**Item 3 bot list:** the review says "the work and governance bots". I gave the route to the bots that actually take risky actions: Explorer, Emissary, Engineer, Extractor (work) and Archivist (deployments). Safeguard gets the receiving side. Editor (no outside actions) and the other governance bots (Architect, Assembler, Arbiter, Scorer, Scrutineer, Safekeeper only write governance files) don't get it. See judgement call 3.

**Scrutineer (skipped as asked):** the routine-vs-brief mismatch (who gets reviews) is fixed by aligning the routine to the brief, which needs **no brief change**. The only possible brief change is if Gem wants chain stalls copied to Marshal as well as Mender. If so, change Scrutineer v003's "Report any stall you detect to the Mender." to "Report any stall you detect to Mender, and copy Marshal when it breaks a routine chain." (would be auditor v004, Gem approves). Not drafted as a file: marshal-v004 has schedule.md say "stalls go to Mender", so it isn't needed.

## Rolemap-v3 fixes (rolemap-v3-fixes-2026-10-04): live vs pending
**Live now (in a deployed version):**
- B5 Imitator approval grant: clone v003, plus the follow-ups (codex-keeper v003, instruction-architect v003, role-cartographer v004, genesis-gang-god v003). Assembler's role-map files still say UNVERIFIED; that's Assembler's own work, not text.
- B1 Scrutineer/Architect: Architect checks no one (instruction-architect v003); Gem reviews Scrutineer (auditor v003).
- B2 stalls, partly: Mender owns them (mender v002); Marshal, Scrutineer and Architect texts point to Mender. The Arbiter text was the gap → item 8.
- B2 preference fit: Scorer records n/a until P4 (assessor v002).
- B2/B3 identity confirmation, Interrogator side: "only Investigator can mark a detail confirmed" (clone-accuracy-validator v003).
- B3 Scrutineer: Assembler's role map, Mender, reviews to Architect and Assembler (auditor v003).
- B3 name sweep: Architect, Archivist, Scorer, Scrutineer, Emissary, Engineer finals are deployed.
- B4 Extractor first brief (scraper v002) and B4 Explorer (2IC, never merged, R-007 limit; genesis-gang-god v003).
- B6 "nothing recorded": superseded. Finals recorded and deployed.

**Pending, now folded into today's files:**
- B1 Scorer self-exclusion → scorer-v003. B1 Safeguard dry-run vs go-ahead + Scrutineer audit → safeguard-v004. B1 Engineer reviewers → engineer-v005.
- B2 pauses (Arbiter side, Safeguard side) → arbiter-v004, safeguard-v004. B2 routing (drop "fastest path") → marshal-v004.
- B3 Marshal (approver, budget owner) → marshal-v004. B3 Inferer (names, confirmed, hold while dormant) → inferer-v002. B3 Inquirer (name) → inquirer-v002.
- B4 routing gaps (Safeguard, Safekeeper) → emissary-v004, engineer-v005, extractor-v003.

**Still pending, not in today's queue (no file drafted):**
- A roles-pipeline: Assembler applies profiles. Not live; in practice Gem delegated deployment to Archivist instead (see judgement call 1).
- B1 Mender: no deleting its own records without Scrutineer verifying and Gem approving (mender v002 unchanged).
- B1/B2 Interrogator samples Imitator's alignment verdicts, not just answers (clone-accuracy-validator v003 unchanged; Imitator dormant).
- B2 Mediator refers pause lifts to Arbiter (connector-steward v004 unchanged; dormant P4).
- B2 Mender state boundary note (repo-local checkpoints and schedule.md aren't the state record).
- B2 Messenger cost-alert route: Mediator drafts, Messenger delivers (comms-concierge v003 still lumps them under "straight from the raising bot"; dormant P4).
- B2/B3 Sourcer: "Surveyor" → Scrutineer as system-truth owner (sourcer v001; dormant P3).
- B4 Editor: Rules and incoming route (editor v001; dormant P5).
- B4 directory.md groups/Council refresh (not instruction text; Gem to direct).

## Judgement calls for Gem
1. **Who applies profile edits.** Item 4 writes in the R-007 exception for Archivist, matching what Gem actually did on 4 Oct. Roles-pipeline (A) proposed Assembler applies and Archivist checks. Pick one. If Archivist applies, it can't count as the check on its own deployment, so Scrutineer checks independently.
2. **Scorer dimensions.** I kept the approved profile set (quality, accuracy, completion, speed and cost, preference fit), folded helpfulness and tone into quality, and dropped instruction-following and safety as Scrutineer's and Safeguard's jobs. The alternative is adopting the routine's set.
3. **Which bots get the Safeguard route.** I chose the five that take risky actions. The review's wider "work and governance bots" would add Editor and six more governance bots for little gain.
4. **Gem-approved actions skip the wait.** If Gem has approved a specific action in the bot's own chat, the bot tells Safeguard before acting and doesn't wait. Stricter: always wait for the dry run. Looser: tell Safeguard afterwards.
5. **Widened risky-action list:** writes to outside services (Google Docs), pushes to shared repos and live profile deployments, as Scrutineer counted. Archivist's routine Doc mirror syncs are exempt as part of its brief. Confirm both.
6. **Inferer's queue lives in memory**, not a file. A file would let Scrutineer see it, but it would put Gem's personal details on the shared computer (Safekeeper's concern). Rolemap B3 had suggested a file, so this is a change from that.
7. **Inquirer on voice calls.** Allowed, under the same limits. The alternative is chat widgets only, which would mean calls never run series.
8. **Parked voice-call v002s.** Gem approved Inquirer v002 and Inferer v002 (VOICE CALLS block) on 4 Oct, but they were never recorded. Today's v002s include those blocks word for word and replace them, so each number is used once.
9. **VOICE CALLS blocks kept verbatim** (with "(ID) Inferer", "(Work) Emissary" and "(Checks) Safekeeper") instead of bare names, so the prefixes stay what the verification rule matches.
10. **Archivist tells Assembler** after each record or deployment. This came from Scrutineer's Assembler section, not the fix queue; drop it if Gem prefers.
11. **Message verification rule not in codex.** Five texts point to "the agent-to-agent message verification rule", but `codex/_shared/` only holds handoff-phase1 and collaboration-map. Archivist should record it (approved 4 Oct) or Gem should confirm where it lives.

## Follow-up 5 Oct, 1:25pm — Safeguard's limit proposals (risk/register.md)
Safeguard's first scheduled review (1:20pm) sent three limit proposals. They're folded into the drafts above as **amendments to the same versions** (no new numbers), plus one new Safekeeper version.

| Safeguard proposal | RR basis | Where | What |
|---|---|---|---|
| S1: Safeguard check before logged-in browsing of Gem's accounts and before gambling-related collection, list-building or promotion | RR-001 (Emissary-inferred automated browsing of Gem's logged-in Facebook and Messenger, 4 Oct 5:38–5:43pm); RR-002 (Extractor's Bonus Intelligence Engine: 1,615 casino and pokies sites with referral links; Interactive Gambling Act exposure); RR-009 (shared browser holds Gem's live sessions) | emissary-v004, extractor-v003, explorer-v004 (amended) | These two kinds of work **always wait for Safeguard's report**, even when Gem approved the task, unless Gem says in the bot's own chat to go ahead without one. For Explorer it's framed as **a check before the action, not a veto**; the decision stays with Gem |
| S2: no snapshots or screenshots of private content left in shared folders; Safekeeper owns the rule | RR-001 (five Messenger snapshots with third parties' private messages in world-readable `/workspace/.playwright-mcp/`); RR-010 (sensitive personal data in shared files) | safekeeper-v004 (new); obligation added to emissary-v004, extractor-v003, explorer-v004, engineer-v005 (amended) | Keep only what's needed, in a non-shared folder; clear your own temporary captures; tell Safekeeper about any you couldn't clear. Safekeeper checks metadata only, flags leftovers, and leaves deletion of existing files to Gem |
| S3: Extractor never ships or runs code with fingerprint evasion or proxy rotation | RR-002 (the packaged BIE code ships fingerprint-evasion and proxy-rotation features and an opsec guide) | extractor-v003 (amended); **option** in engineer-v005 | Even when the code came from Gem or earlier work; flag to Gem and Safeguard instead. Engineer option clearly marked, not in its block |

**Browser-driving bots in this batch:** Emissary, Extractor and Explorer (all browse), and Engineer (may drive the browser to test builds; inferred, not seen). The other bots in the batch (Marshal, Scorer, Safeguard, Archivist, Inferer, Inquirer, Arbiter) don't drive the browser in their briefs; Archivist's Doc mirror uses the connector. Outside this batch, Investigator (RR-008) and any later browser-driving bot will need the same line at their next version.

**Phone-number account matching stays excluded**, as Gem asked. Nothing here adds it, and the logged-in-browsing check doesn't authorise it.

## Judgement calls added 5 Oct, 1:25pm
12. **Explorer as 2IC.** Explorer's check is written as a check before the action, not a veto: Safeguard reports and Gem decides. Confirm it doesn't weaken Explorer's 2IC role, and that Gem, not Explorer, makes the final call on these two kinds of work.
13. **Extend proposal 3 to Engineer?** The BIE proxy rotation was a code issue under Engineer's old name (Codey). engineer-v005 carries an **OPTION** to bar Engineer from writing, shipping or running evasion code for any bot, even on request. Gem chooses; it isn't in the block unless Gem says so.
14. **No skip-the-wait for these two kinds of work.** Unlike the general route (judgement call 4), logged-in browsing and gambling work wait for Safeguard's report even if Gem approved, unless Gem waives it in the bot's own chat. Looser: apply the general rule.
15. **Clearing own captures vs "never deletes".** Emissary's text says it never deletes anything without Gem's approval. The new line treats a bot's own temporary captures from its own task as its working files, not Gem's, so it can clear them. Existing leftovers (the RR-001 snapshots) stay Gem's call. Confirm that line.
16. **"A folder that isn't shared" is limited.** Every bot runs as the same user on the shared computer, so owner-only permissions keep files away from other users but not from other bots. Safekeeper may recommend a better store.
17. **Engineer as browser-driving** is inferred. Drop the line if Gem knows Engineer never drives the browser.
18. **Wider personal-data rule?** RR-008 and RR-010 (Investigator's factcheck file, the incident file) aren't browser artefacts. Safekeeper's rule covers browser output only; Gem may want it widened to any file of personal details in shared folders.
