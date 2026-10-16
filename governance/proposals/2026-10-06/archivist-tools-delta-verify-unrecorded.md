# Archivist tool delta — verify.py lists live agents with no codex folder — NEEDS GEM'S DIRECT APPROVAL

| Field | Value |
|---|---|
| Owner | P1 (Roles) Archivist (owns `codex/_tools/`). Archivist applies it only after Gem approves; Architect doesn't write into `codex/` |
| Fix-queue item | 3 (unlisted agents) |
| Why | verify.py only checks the 36 known bots, so a new live agent like "P2 (ID) Inquirer copy" (`0314faa4…`, created 2:49am 6 Oct) goes unnoticed. Scrutineer found it by hand |
| Approver | **Gem, directly.** NEEDS GEM'S DIRECT APPROVAL |

## What it adds
A final section that reads every `/home/box/agent-data/agents/*/profile.json` and lists any agent whose id has no codex folder:
- **UNRECORDED AGENT**: has instructions (non-empty description). Archivist notes it in `codex/index.md` as "unrecorded live agent, awaiting Gem".
- **GROUP (INFO)**: empty description and no instructions (the group channels). Listed for information only.
- It **warns and doesn't fail** (OVERALL stays PASS), because an unrecorded agent is a governance gap, not a codex error. Gem can choose to make it fail (judgement call).

A read-only dry run of this logic on 6 Oct, about 8:15am AEST, found:
- UNRECORDED AGENT: `0314faa4-edcb-4aa4-91cc-876dc44f3a6e` "P2 (ID) Inquirer copy" (namedBy app, 1,278-character description).
- GROUP (INFO): Identity `0ecaea40…`, Delivery `3e9d6a26…`, Council `4dd4fd18…`, Operations `638e3cab…`, Assurance `b10e394f…`, Instruction Governance `e417910e…`.

## Proposed code (append to the end of verify.py, before the final OVERALL line)
```python
# --- Unrecorded live agents (warning only; Gem-approved delta, 2026-10-06) ---
known=set()
for f in glob.glob(f"{ROOT}/*/v001.md"):
    m=re.search(r"\| Bot id \| ([0-9a-f-]+) \|",open(f,encoding="utf-8").read())
    if m: known.add(m.group(1))
print("--- Live agents with no codex folder ---")
for d in sorted(glob.glob(f"{AG}/*/")):
    bid=os.path.basename(d.rstrip("/")); pf=os.path.join(d,"profile.json")
    if bid in known or not os.path.exists(pf): continue
    p=json.load(open(pf,encoding="utf-8"))
    kind="UNRECORDED AGENT" if (p.get("description") or "").strip() else "GROUP (INFO)"
    print(f"{kind:17} {bid} name={p.get('name')!r} namedBy={p.get('namedBy')}")
```
