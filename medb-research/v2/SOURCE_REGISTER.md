# Source Register and Verification Ledger

**Purpose:** Prevent bibliographic presence from being mistaken for full-text verification or proof of a MedB claim.

## Verification labels

- **Primary source located:** the original paper, standard, official project, or official documentation is identified.
- **Metadata/landing-page checked:** title, abstract, metadata, or official summary was inspected; full argument not necessarily read.
- **Full text reviewed:** the full source was actually reviewed for the claim being made.
- **Claim-specific verification needed:** the exact claim attributed to the source has not been checked closely enough.
- **Freshness-sensitive:** the source or product behavior may have changed since the original check.
- **Comparative evidence missing:** the source relationship is plausible but no controlled comparison supports a distinction or novelty claim.

## Source families and required treatment

| Source family | Original map's evidence basis | How to use it responsibly | Next action |
|---|---|---|---|
| Solid, MyData, PIMS, HAT | Mix of official pages and an EDPS PDF/landing-page limitation noted | Support descriptions of user-controlled data infrastructure; do not imply all projects remain operational or equivalent | Recheck current project status and official documentation |
| GDPR portability and DTI | Legal text and project source links | Distinguish legal scope from MedB's proposed stronger semantic portability | Have a qualified legal reader check jurisdiction-specific interpretations |
| Contextual integrity and formal privacy policies | Academic publications; at least one full-text limitation noted | Cite theory for contextual norms and flow constraints; do not imply it prescribes MedB's exact model | Review primary texts and compare formalisms |
| UCON, object capabilities, Macaroons, UCAN | Primary publications/specifications linked | Borrow established authority attenuation and ongoing-use concepts | Write explicit semantic mapping and test edge cases |
| Decentralized IFC and W3C PROV | Academic work and W3C standard linked | Use as foundations for label propagation and provenance; document what needs extension | Build ontology and schema crosswalk |
| Event sourcing and tamper-evident logs | Secondary explanation plus security paper | Separate reconstructible history from cryptographic tamper evidence and from truth of logged claims | Specify threat model and trusted logging boundary |
| Constitutional AI, Claude Constitution, OpenAI Model Spec | Mix of research paper and current/versioned official pages | Do not conflate model behavior guidance with external system governance | Recheck versions and precisely scope comparisons |
| Corrigibility, power-seeking, manipulation, preference shift | Academic papers, mostly arXiv links | Treat as motivating frameworks, not evidence that MedB's specific safeguards work | Review papers for scope and counterarguments |
| AI control, hidden-objective auditing, sandbagging | Research papers and evaluation methods | Compare experimental protocols rather than asserting MedB's protocol is unique | Reproduce or adapt baseline designs |
| SMACTR, NIST AI RMF, model cards, datasheets | Frameworks and primary papers | Use for audit lifecycle and documentation; avoid claiming adversarial blindness is wholly absent from all other work | Review closest audit variants |
| Narrative identity, assurance cases, legal compliance, constitutional theory | Explicitly identified gaps in the original map | Treat as priority gaps, not as settled conclusions | Commission focused literature searches and synthesis |

## Minimum fields for future source entries

For each source record:
1. Stable identifier and full citation.
2. Primary URL or DOI, with retrieval date.
3. Publication date and version.
4. Source class: paper, standard, official documentation, legal text, commentary, or implementation.
5. Verification method and full-text status.
6. Exact proposition supported, ideally with section/page.
7. MedB interpretation, clearly separated from the source's claim.
8. Counterargument, scope limitation, or conflicting source.
9. Related MedB requirement and test ID.
10. Freshness sensitivity and recheck date.

## Research-integrity warning

A source's existence does not prove that MedB has borrowed it correctly. A source's abstract does not establish every detail of the method. A lack of an obvious match in a limited search does not establish novelty. The original file's stated verification date is historical evidence about the research process, not a guarantee that every URL, product behavior, or version remains current.