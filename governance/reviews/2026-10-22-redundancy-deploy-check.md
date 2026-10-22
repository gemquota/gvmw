# Deploy check: redundancy batch, six drafts (22 Oct 2026, 7:56 to 7:57pm)

Prepared by P2 (Checks) Scrutineer (`affe0344`), Thu 22 Oct 2026, about 8:02pm AEST (UTC+10). Read-only. I compared live profile.json descriptions, the codex vN.md fenced text, `codex/_tools/deploy_manifest_2026-10-22.json` (both its sha256 field and the hash of its text field) and the revision 2 draft fences. I also checked mtimes (all after the 6:39pm restore, so usable), CHANGELOGs, index.md and approvals, and ran verify.py and verify_shared.py read-only.

There is **no later revision** of the batch: every draft and README file is still dated 7:19pm, so revision 2 is the last one.

## Per bot
| Bot | Version | Live = codex = manifest = draft (sha256, first 12) | Chars | Version file → profile | CHANGELOG / index | Result |
|---|---|---|---|---|---|---|
| Inferer | identity-inferer v006 | 441b92c9fcd4 (all four) | 5288 | 7:56:10pm → 7:57:01pm | record + deploy rows; index v006 LIVE | **PASS** |
| Arbiter | arbiter v006 | c0849fa416cb (all four) | 1336 | 7:56:10pm → 7:57:05pm | same | **PASS on text; approval route flagged** |
| Architect | instruction-architect v005 | d290277295ef (all four) | 2201 | 7:56:10pm → 7:57:12pm | same | **PASS** |
| Emissary | grok-bot v007 | d58a54aa7998 (all four) | 5470 | 7:56:10pm → 7:57:23pm | same | **PASS on text; approval route flagged** |
| Extractor | scraper v006 | 13c04fcd6b78 (all four) | 5698 | 7:56:10pm → 7:57:37pm | same | **PASS on text; approval route flagged** |
| Explorer | explorer-copy v006 | 94aafeffa6ce (all four) | 7094 | 7:56:10pm → 7:57:52pm | same | **PASS** |

- **R-035:** every version file was written once, at 7:56:10pm, before its profile, and none has been touched since.
- The CHANGELOG rows (written 7:58:30pm) carry both the approval and the deployment.
- index.md rows show the new versions as OK (LIVE). The index header still reads "Last rebuilt: 2026-10-16 …", which is stale (minor).

## Gem's recorded words (approvals/2026-10-22-gem-direct-words.md; Archivist recorded them at 7:55:36pm, before any version file or profile)
- **7:53pm, Archivist's chat:** "I approve explorer v006". Gem also asked for it to deploy with the five. Archivist added the scope: file 3877021e4870, text 94aafeffa6ce.
- **7:54pm, Archivist's chat**, answering "Do you approve Inferer v006 and Architect v005 from proposals/2026-10-22-redundancy/?": "Yes, approve both and deploy all six". Archivist added the hashes: inferer 441b92c9fcd4, architect d290277295ef.
- **Order is correct:** words 7:53 and 7:54pm, recorded 7:55:36pm, version files 7:56:10pm, profiles 7:57:01 to 7:57:52pm (R-029).
- **Direct, not through Imitator:** yes for Explorer, Inferer and Architect. Gem's words name them by draft name; the hashes were added by Archivist and are the only revision 2 texts.
- **Arbiter, Emissary and Extractor were approved by Imitator,** 1:1 with Archivist at 7:52pm (approvals.md, 19:52 row; the CHANGELOG record rows say "Approver: Imitator"). Gem's only words covering them are "deploy all six", which is a direct deployment request, not an approval naming them or their hashes.
- **The 7:07pm words were never confirmed.** Nothing records Gem confirming "Yeah fix those and proceed as suggested". The paste lines that would have done it weren't used.
- **Collection-only or fold:** Gem's words don't say. Extractor v006 (collection only) is deployed. **The fold is excluded:** Extractor's profile is live, there's no merged Emissary brief, and nothing is archived or retired.

## Approval-route findings (for Arbiter)
1. **R-044** says: for the routing split (explorer, emissary, extractor), "Architect drafts, Scrutineer checks, and **Gem approves**", and "nothing deploys before Gem confirms the 7:07pm words". Emissary and Extractor were *approved* by Imitator. Gem's 7:54pm "deploy all six" is Gem's authority and arguably covers them by precedence. But it neither names them for approval nor confirms the 7:07pm words. **Arbiter should rule whether "deploy all six" cures this.** If it doesn't, Gem should give one line approving emissary-v007 (d58a54aa7998) and extractor-v006 (13c04fcd6b78) after the fact.
2. **arbiter-v006 was approved by Imitator.** That is a change to Arbiter's brief, while Imitator claims a veto over Arbiter (Imitator's approvals.md 19:06 row). R-044 holds that veto until Gem confirms it. Imitator approving Arbiter's brief at the same time is a conflict of interest. The same R-044 caveat applies: Imitator approved items resting on words it had relayed itself. Arbiter should rule; Gem can confirm directly.
3. **Imitator's 19:06 approvals.md row** records the veto and schedule powers as Gem-confirmed. R-044 says they're not confirmed until Gem confirms them directly. Not part of this deploy, but noted.

## Left undeployed (live profile = their latest codex = revision 1 base)
| Bot | Latest codex | Live hash | Profile mtime |
|---|---|---|---|
| Investigator | v004 | 68b76c08ba86 | 6:39:36pm (restore) |
| Imitator | clone v006 | 4a5e5def3406 | 6:39:30pm |
| Scorer | assessor v004 | 10e0324f805d | 6:39:33pm |
| Safeguard | compliance-risk-officer v006 | db379979d94d | 6:39:34pm |
| Archivist | codex-keeper v008 | 05e01c9ac670 | 6:39:33pm |
| Scrutineer | auditor v004 | 542ade104e4b | 6:39:33pm (facts only) |

None was deployed and none was recorded as a new version. **Mender v005 is unchanged:** live matches v005 (31e7be0b0f53), v005 is still the latest version, and the profile is untouched since 6:39:36pm.

## verify (read-only)
- `verify.py`: **OVERALL: PASS**. STRICT latest==live 17/37; all 17 live bots MATCH with name=ok, including the six new versions.
- `verify_shared.py`: **OVERALL: PASS**, 9 of 9 match.

## Pointer
Present. The 22 Oct approvals file has "Pointer added by Archivist at 7:52:19pm", which cites 6:45pm and 6:47pm at lines 61–62 of the 16 Oct file, plus the 6:48pm and 6:54pm words at lines 63–64. A backup was taken first.

## Other profile changes between 7:50 and 8:00pm
**None.** Exactly six profile.json files changed (7:57:01 to 7:57:52pm), all of them in the manifest.

## Result
**All six deployments are technically correct:** hashes, order, records and verify all PASS. Explorer, Inferer and Architect rest on Gem's direct words. **Arbiter, Emissary and Extractor rest on an Imitator approval plus Gem's "deploy all six",** which departs from R-044. Arbiter should rule; a one-line confirmation from Gem would settle it. There was no fold, and the six remaining drafts are undeployed.
