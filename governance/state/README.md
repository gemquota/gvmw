# State record (owner: P1 (Ops) Mender)

Authoritative record of task state, checkpoints, handoffs and resumability for Gem Quota's bots.
Path required by Mender brief (`mender/v002`). Created 6 Oct 2026, 8:10am AEST, after Scrutineer's third flag (reviews/2026-10-06.md, M1).

## Layout
- `chain/YYYY-MM-DD.md` — daily chain status (Scorer → Scrutineer → Architect → approver → Archivist)
- `open.md` — open stalls and items waiting on Gem or a bot
- Future: per-bot checkpoints and handoff receipts once the Architect's "Mender state boundary" draft lands

Do not delete this folder. Archive, don't destroy, anything you're unsure about.
