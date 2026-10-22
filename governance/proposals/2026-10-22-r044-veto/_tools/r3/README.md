# r044-r047 batch (folder `2026-10-22-r044-veto/`), 22 Oct 2026, revision 3 — DRAFT, ALL GEM (R-027)

Reflects R-044 to R-048 in rulings.md. Nothing is approved, recorded or deployed. Revision 2 is kept in `_tools/r2/` and `_tools/build-r2.py.bak`.

## What the drafts do
- **imitator-v008:**
  - **Veto:** covers every Arbiter ruling (R-047). A veto on a ruling about Imitator or its checkers takes effect, but is flagged to Gem as self-interested. It never overrides Gem's words or deterministic checks. A vetoed ruling waits for Gem (a default I chose).
  - **Schedules:** Imitator may change bots' schedules, flagged in the digest, but not its checkers' schedules without Gem (R-046, R-048).
  - **Bots:** Imitator may approve another bot creating or retiring a bot, with a verified archive first (R-047c). Imitator's checkers and anything that costs money stay with Gem.
- **arbiter-v007:** the same veto and checker-schedule rules, from Arbiter's side.
- **emissary-v008:** may post as Gem without Gem approving each post's text. Any bot may originate a post, but only Emissary publishes it. Posts make no promises, there's a Safeguard dry run per post, and the gambling and BIE ban is unchanged (R-047, R-048).
- **Elsewhere:**
  - **Posting:** connector-limits v003 revision 5, rule 1, matches emissary-v008. Deploy them together.
  - **Projects public:** these are in GitHub revision 5b (github-v001, engineer-v008, safeguard-v008). Gem named the projects in Arbiter's chat at 8:06pm.
  - **gvmw:** its scan and dry run for every push are unchanged everywhere.
- **Not drafted:** Archivist's brief may also need a line for Imitator-approved retirements. I'm flagging it for Gem rather than widening this batch.

## Gem's words: direct or relayed
- **Direct:**
  - 7:00pm in Inquirer's chat: "C and Imitator can veto if desired" and "Yes, but flag it in the digest". Arbiter and Scrutineer read the transcript (R-044 update, R-048).
  - 8:06pm in Arbiter's chat: naming VEPA, Codey, swarm, SLAP.RED/Golf and MedB (R-047a).
- **Verified, but the wording comes through Imitator:**
  - **7:06pm card:** Investigator verified it (R-046 update).
  - **8:04pm card t56s1:** the quoted texts ("Your veto covers every Arbiter ruling / You can approve bots creating or retiring bots / Bots can make all five active projects public / Bots can post to social channels as me, no promises") are Imitator's report. Investigator verified Gem's picks (R-047).
  - **"No promises" is Imitator's own narrowing.** Gem's visible label was "Bots can post on social media as me" (R-047b, R-048).
  - **"All five active projects"** wasn't named by Gem until 8:06pm (R-047a).
  - **The archive before retirement** comes from Arbiter's reading, not Gem's words (R-047c).
- **Relayed only:** Gem's 7:55pm gvmw words, "Turn it on now, with a scan and dry run each push", were reported by Engineer (R-045 update). Arbiter accepted them because they add a check and remove none.
- **None of these are in approvals/ yet**, so the paste line has Gem restate them for Archivist (R-029).

## Hashes
| Draft | Base text | New text | File |
|---|---|---|---|
| imitator-v008 | db56debaa35f | 7fd84293df7e | af00634358d0 |
| arbiter-v007 | c0849fa416cb | 3d031639639f | fc80f5f4911e |
| emissary-v008 | d58a54aa7998 (codex v007, live) | 770cda3e8750 | 4a4e9a40520d |

## Paste line (Gem only)
`I confirm I told Inquirer at 7:00pm on 22 Oct: "C and Imitator can veto if desired" and "Yes, but flag it in the digest"; chose on Imitator's card at 7:06pm: "Yes, you can veto Arbiter in disputes and change bots' schedules (flagged in the digest)"; picked on Imitator's card t56s1 at 8:04pm that its veto covers every Arbiter ruling, that it can approve bots creating or retiring bots, that bots can make the five active projects public, and that bots can post on social media as me, no promises; and named VEPA, Codey, swarm, SLAP.RED/Golf and MedB in Arbiter's chat at 8:06pm. I approve r044-r047: imitator-v008 (7fd84293df7e), arbiter-v007 (3d031639639f) and emissary-v008 (770cda3e8750), after the redundancy batch — record and deploy with connector-limits v003.`
