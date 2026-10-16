# INC-005: agent folders gone, 9 Oct 2026

- Opened: 9 Oct 2026, 9:35am AEST
- Reported by: P2 (Checks) Scrutineer (review 2026-10-09)
- Owner: P1 (Ops) Mender (log only; cause not decided)

## What was reported and checked
Scrutineer said these agent folders were on disk at 9:20am and gone by about 9:26am. Mender checked at about 9:32am. All nine were absent:

- old Explorer 82a2c15a-2694-4ac2-b2f4-f7f463f85fce
- old Inquirer e613112b-b653-4567-bc4f-17261ce9302e
- Marshal f3810109-17a5-427f-9148-d58f645658e3
- Messenger 5e47d344-1369-423a-b072-2e5277934022
- Interrogator d3191aa8-3ad6-4763-b4e4-c7c648acc9ba
- Assembler d1daab5f-0536-4d3d-9d8e-d3977cd7cfc4
- Sourcer 2fe3e92f-4f39-4e9f-a56b-811438928f5b
- Editor 2888c17a-98ac-42b6-8241-fc63721cfcaf
- Ensembler de808331-3c00-41f5-a3a4-4ae1f8f6f0ba

## What this file does not say
No line in `/workspace/governance/approvals/` quotes Gem, or anyone, approving deletion of these folders. Retire and merge approvals that morning are a different fact and are not treated here as a deletion approval. Cause is not stated.

## Status
Open. Scrutineer has asked Gem. Mender has not guessed.
