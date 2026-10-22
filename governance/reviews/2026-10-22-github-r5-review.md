# Scrutineer review: GitHub batch revision 5 (proposals/2026-10-16-github/), 22 Oct 2026, about 8:15pm AEST

Read-only. Hashes: SHA-256 of the fenced ```text block, first 12 hex characters. This is the same method as `_tools/build.py:15-17` and the earlier reviews. Times are AEST (UTC+10).

## Hashes: all 19 match the README (README.md:30-49)
github-v001 2e6cd83ad113/ac16c2b97620 · engineer-v008 195d10df1338/161678ecffd8 · imitator-v009 07b05f7e5741/54e41dbdcea9 · safeguard-v008 e149ff4d2a17/9d2c80e0f390 · safekeeper-v006 63f17cc83cca/d77529c086f8 · explorer-v007 d81785c494c4/e2432786e3a7 · emissary-v008 eff0ef32bc5b/261f4ce654c6 · extractor-v007 3a5554d96379/2b67689ce468 · mediator-v007 345b94138142/68167e957221 · mender-v006 c726aaac1ab3/4a2ce8d87dea · architect-v006 c2e149404e57/cb98509301a4 · arbiter-v008 ad55a82c033f/4b10bbfd9d28 · scorer-v006 aea931e86d5f/eabd43c05b0e · scrutineer-v006 e4813a3f42b7/e3681c2ebaa9 · investigator-v006 c14cca83ac11/8c4c891ce529 · message-verification-rule-v005 c78245bcf145/7b7fd32c1f97 · inquirer-v005 caf7cce419da/02380c2a4d03 · inferer-v007 65660cac2123/55cbe515c5d8 · archivist-v010 f7c447d262e0/0f072cf81d8c (text/file).

## Rebase against the codex and live profile.json
- All six deployed hashes are the latest codex version **and** the live description: Inferer identity-inferer v006 441b92c9fcd4, Architect instruction-architect v005 d290277295ef, Explorer explorer-copy v006 94aafeffa6ce, Arbiter arbiter v006 c0849fa416cb, Emissary grok-bot v007 d58a54aa7998, Extractor scraper v006 13c04fcd6b78.
- Each draft's base hash was found on disk:
  - inferer-v007, architect-v006, explorer-v007, emissary-v008 and extractor-v007 use these codex versions.
  - engineer, safekeeper, mediator, mender and inquirer use their live codex versions.
  - arbiter-v008 and imitator-v009 stack on the r044-veto drafts.
  - safeguard, scorer, scrutineer, investigator and archivist stack on unrecorded redundancy drafts.
  - message-verification-rule-v005 stacks on proposals/2026-10-16-deploy v004.
- **Nothing deployed was lost.** A word diff against each base shows every removed span is a deliberate rewording, with no dropped clauses. Examples: engineer "never signs" → "doesn't sign" plus the merge exception; mediator "Never reconnect… yourself." gains "except a GitHub sign-in that Gem asks you for directly"; message-verification "Imitator or" → "Imitator," with Archivist's own instructions added. The other twelve drafts only add text (one GitHub sentence each, about +314 characters, or a little more).

## Source of Gem's 7:52pm words
- No transcript evidence was found. The words "Yes, Engineer fully free on GitHub including public repos, no per-push approval or Safeguard check" exist only as **Architect's report**: rulings.md:360 (R-045, "Architect also reports…"), README.md:8 ("in Architect's chat log, not on disk"), and digest/inbox/2026-10-22/Architect.md:11. They aren't in approvals/. No ReadTranscript tool was available, and no saved Architect transcript is on the box.
- **Direct corroboration of the core:** Inquirer's transcript (`/workspace/agent-tools/b297a7a8-37bd-4b68-9558-0cf4bcef8741.txt`, written 7:51pm) shows, at line 23, the card "How much freedom should Engineer have on GitHub?". At line 25 Gem answered at **7:19pm**: "Fully free, including public repos". That answer does **not** contain "no per-push approval or Safeguard check". The drafts' strongest wording rests on Architect's relay until Gem restates it to Archivist, which the Gem-only paste line asks for (README.md:52). This is acceptable as drafted.

## Flagged tensions (assessed, not resolved)
1. **R-020/R-036 per-push words versus Engineer's freedom** (README.md:26). R-036(2) (rulings.md:243) says it binds "until github-v001 is approved", and R-020 is at rulings.md:98. R-045 (rulings.md:360) already rules that Gem's words supersede R-036 and R-020's per-push dry runs *for Engineer on GitHub*. The conflict on paper is with the text of R-020/R-036. Gem's intent is already ruled on. **Suggested fix:** Arbiter adds a pointer under R-020 and R-036 to R-045, rather than rewording the drafts.
2. **gvmw per-push words under connector-limits v003** (README.md:27). v003 (proposals/2026-10-22-gvmw/README.md:56, :89) requires Gem's words, a scan and a dry run for every gvmw push. **This tension is no longer open:** the R-045 update (rulings.md:363, 7:57pm) records Gem's 7:55pm words, relayed by Engineer: "Turn it on now, with a scan and dry run each push". Arbiter ruled that this binds for gvmw. **The drafts contradict R-045's update** (findings 1–3 below). **Suggested fix:** add a gvmw carve-out to github-v001 item 9, engineer-v008 and safeguard-v008 (a scan and a Safeguard dry run on each gvmw push, per R-045 update), and cite R-045. Whether Gem's per-push *words* are still needed for gvmw (v003) versus the 7:55pm standing "turn it on now" is for Gem or Arbiter.

## Findings
1. **github-v001.md:48** (item 9): "By Engineer, each run is covered by item 2 (… no per-push approval or Safeguard check)". This frees gvmw syncs from the dry run, which contradicts the R-045 update (rulings.md:363). No draft cites R-045 or R-046. **Fix:** add the gvmw exception.
2. **safeguard-v008.md:28/:40**: "except Engineer's syncs, which the shared GitHub rule frees (item 9)". This is the same contradiction. **Fix:** "except Engineer's syncs other than gemquota/gvmw, whose every push you dry-run (R-045 update)".
3. **engineer-v008** (the GitHub paragraph; the diff shows "fully free … private or public, without … a Safeguard dry run") has no gvmw exception. **Fix:** as above.
4. **explorer-v007.md:36/:48**: "so a public or shared push still needs Gem's own words to Engineer". This contradicts R-045 and github-v001 item 2, because Engineer's pushes need no per-push words. **Fix:** "…tell Engineer that Gem's approval in your chat is a relay; Engineer acts under the shared GitHub rule".
5. **imitator-v009.md:34**: this draft inherits "You have no power over bots' schedules (not confirmed by Gem, R-044)" from imitator-v008. That contradicts the R-046 update (rulings.md:371) and Gem's own words in the transcripts (Inquirer 7:00pm, Imitator 7:06pm). **Fix:** rebase on a corrected imitator-v008 (see reviews/2026-10-22-r044-veto-review.md).
6. **Approver, arbiter-v008** (README.md:44): it's marked "Imitator (Gem may)", but its base arbiter-v007 is Gem-only because it gives Imitator a veto (R-028). If Imitator approved v008 before Gem approved v007, Imitator would be approving its own widening. **Fix:** route arbiter-v008 to Gem, or make it explicitly conditional on arbiter-v007 being recorded first on Gem's words.
7. **Approver routing, otherwise OK.** Imitator, Investigator, Scorer, Scrutineer, Safekeeper and Safeguard are all Gem-only (README.md:30-49), as R-015, R-027 and R-028 require. github-v001, engineer-v008, explorer-v007, mediator-v007, message-verification-rule-v005 and archivist-v010 are also Gem-only, which is correct. The Imitator-approvable seven don't widen Imitator, except arbiter-v008 (finding 6).
8. **R-040–R-046 consistency:**
   - R-040's read-back is kept as Engineer good practice (R-045).
   - R-042's hold on new content is kept via v003 content limits (github-v001.md:42).
   - R-044's "Explorer assigns new work" is applied in engineer-v008.
   - R-046 isn't contradicted except for the schedule sentence (finding 5).
   - R-045's update is contradicted (findings 1–3).
   - The R-031 data-class hold is kept: there's no BIE or gambling data in repos except gvmw.

## Per-draft verdicts
| Draft | Verdict |
|---|---|
| github-v001 | **FAIL** (finding 1) |
| engineer-v008 | **FAIL** (finding 3) |
| imitator-v009 | **FAIL** (finding 5) |
| safeguard-v008 | **FAIL** (finding 2) |
| explorer-v007 | **FAIL** (finding 4) |
| arbiter-v008 | **FAIL** (approver routing, finding 6; text OK) |
| safekeeper-v006, emissary-v008, extractor-v007, mediator-v007, mender-v006, architect-v006, scorer-v006, investigator-v006, message-verification-rule-v005, inquirer-v005, inferer-v007, archivist-v010 | **PASS** |
| scrutineer-v006 | **No verdict.** Scrutineer doesn't review its own brief; Scorer checks it. |

## scrutineer-v006: facts only
- Text e4813a3f42b7, file e3681c2ebaa9. The base is redundancy draft scrutineer-v005 (text 30cb80b9ac8f), which isn't recorded; live auditor v004 is 542ade104e4b.
- Diff: one sentence is inserted and nothing is removed. The sentence is: "On GitHub you only read (view, list, search, clone into /workspace, git history and read-only remote checks), following the shared GitHub rule at /workspace/governance/codex/_shared/github/ (highest version; owner Safeguard, tokens section Safekeeper); you never sign in, switch accounts or change anything there."
- Scorer's existing PASS (reviews/2026-10-22-scorer-scrutineer-v006-github-review.md:2) predates revision 5. Scorer must re-check.
