# Archivist deploys Imitator-approved versions: drafts, 16 Oct 2026

These are drafts only. Nothing is recorded in codex/, no profile is edited and no bot has been messaged.

## Source: Gem's words to Explorer, relayed to Architect
- **16 Oct, 11:09am, Explorer's chat.** Logged in `approvals/2026-10-09-gem-direct-words.md`, line 42.
  - Explorer asked: "Should Archivist deploy changes Imitator has approved without waiting for you?"
  - Gem's exact words: "Yes, Imitator's approval is enough"
- **They reached Architect as a request relayed by Explorer.** They're Gem's direct words to Explorer, not to Architect or Archivist. Under R-008 and R-018, a relay is a reason to draft, not an approval.
- **The approver must confirm with Gem directly.** These drafts take effect only when Gem approves them in Gem's own words, in Archivist's chat or on a voice call with Archivist.
- **Rulings:** Arbiter has been told this conflicts with R-010. There's no new ruling on R-010 in `rulings.md` yet; the latest entries are R-028 update, R-030 update and R-030 final, all 11:08–11:09am. These drafts don't depend on one. If Gem approves them, the R-010 wording they amend changes, and Arbiter may record an R-010 update.

**Approver: Gem directly, for all three.** A relayed approval or an Imitator approval won't do. Reasons:
- The change widens Imitator's effective power (R-028).
- The shared rule is owned by Safekeeper, a checker (R-027).
- Explorer's brief says its changes need Gem's approval.

Gem asked for this, so Architect's weekly cap doesn't apply.

## Files
| File | Base (byte-checked = live, ~11:12am) | New | Status |
|---|---|---|---|
| `archivist-v008.md` | codex-keeper v007 | v008 | Awaiting Gem |
| `explorer-v005.md` | explorer-copy v004 | v005 | Awaiting Gem |
| `message-verification-rule-v004.md` | _shared v003 (shared rule; nothing to deploy) | v004 | Awaiting Gem |

## Changes
**Archivist v008 (three sentences):**
1. **Recording.** Archivist never records an Imitator approval of a change to Imitator, to a bot that checks it, or to a shared rule one of those bots owns. It also never records one that widens Imitator's own role or puts Imitator's own decisions into a brief (R-028). These cover safeguards (b), (c) and (d).
2. **Deployment has two cases.**
   - (a) Gem's own request, as today.
   - (b) New: a version recorded on Imitator's approval may be deployed without waiting for Gem, once:
     - Archivist has confirmed the approval 1:1 with Imitator itself, never through a relay or a file (safeguard a);
     - Safeguard has sent its dry-run report (J1).

     If Safeguard raises a concern, or hasn't replied and the deployment can't wait, Archivist asks Gem.
   - Case (b) excludes:
     - Archivist's own instructions (J3);
     - Imitator and the checkers: Investigator, Scorer, Scrutineer, Safekeeper and Safeguard (b);
     - changes that widen Imitator's role (c);
     - anything that spends money or can't be undone (e).
   - In both cases, Archivist records the approver's words before deploying (R-029).
3. **FORBIDDEN** now refers to "the deployment cases set out above".

**Explorer v005 (one sentence):** "Deployment is Gem's action, or Archivist's when Gem asks…" now adds "or when Archivist has recorded a version Imitator approved within its authority and confirmed that approval 1:1 with Imitator". The R-014 ban on Explorer writing any profile itself stays word for word.

**Message verification rule v004 (one sentence):** after "deploying a profile edit needs them given to the deploying bot itself (R-010)", it adds the same narrow Archivist exception, with the checkers and the R-028 exclusion named.

## Sweep (every live brief and both shared rules)
- **Found and changed:**
  - Archivist v007 (DEPLOYMENT and FORBIDDEN).
  - Explorer v004 ("in Archivist's own chat (R-010)").
  - Message verification v003 ("given to the deploying bot itself (R-010)").
- **Checked and left alone:**
  - **Engineer v007:** the deploys it means are code and Vercel deploys, not profiles.
  - **Safeguard v006:** "live profile deployments" stays on its risky list, which fits J1.
  - **Mediator v006:** "never use a check to … deploy".
  - **Connector limits v001:** Vercel deployments only.
  - **Investigator v003:** "changes to your instructions need Gem's own approval". That's about approval, not deployment, and it agrees with safeguard (b).
  - **No R-010 or Archivist-deployment wording** in Imitator, Inquirer, Inferer, Architect, Scorer, Scrutineer, Safekeeper, Arbiter, Mender, Emissary or Extractor.
- **All 17 live profiles** match their latest codex version, checked ~11:12am.
- **Pending drafts:** the only other one is `proposals/2026-10-16-investigator/investigator-v004.md`. Investigator is a checker, so it stays with Gem. There's no overlap.

## Judgement calls
- **J1. Does deploying under an Imitator approval still need a Safeguard dry run?**
  - **Default: yes, and Archivist waits for the report.** Safeguard's list has "live profile deployments" on it. Both earlier breaches came through relays. Under case (a), Gem's approval is why Archivist doesn't wait. Under case (b) Gem hasn't seen the specific version.
  - The dry run isn't a veto: if Safeguard has a concern, or can't reply in time, Archivist asks Gem.
  - Alternative: tell Safeguard and go ahead, as in case (a). That's faster but weaker.
- **J2. Does an Imitator approval mean "record and deploy"?**
  - **Default: yes, unless Imitator says "record only".** That's Gem's question as asked ("deploy changes Imitator has approved").
  - Imitator still sends Gem its weekly list of decisions, so Gem can undo anything.
- **J3. Archivist's own brief.** Default: excluded from case (b), so Archivist doesn't deploy its own instruction changes on Imitator's word; no bot verifies its own work. Imitator can still approve them for recording. Gem then asks Archivist to deploy them.
- **J4. Reading of "Imitator's approval is enough".**
  - **Default:** enough for Archivist to deploy without waiting, within Imitator's existing approval limits. That excludes Imitator, the checkers, role-widening, spending and irreversible actions.
  - **Not drafted:** making Imitator's approval enough for changes to Imitator or the checkers, or for outward or spending actions. That would contradict R-015, R-019, R-027 and R-028, and needs Gem's explicit words.
- **J5. Imitator's own brief** (clone v006) isn't changed. It already sends approvals to Archivist and a weekly list to Gem. Optional: add "say if an approval is record-only". It's left out because that's a change to Imitator, so it's Gem-only, and it isn't needed.
- **J6. R-010.** These drafts amend the briefs that carry R-010. Arbiter may want to issue an R-010 update once Gem approves, so that `rulings.md` matches.
