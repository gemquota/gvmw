# Role cartography

## v8 — 15 Oct 2026 ~11:35pm AEST (current)
P3 (Investigator) and P4 (Imitator) went LIVE at 11:30pm on 15 Oct 2026 (phases.md, updated 11:31pm; Gem in Explorer's chat: "Yes, switch on P3", then "and p4"). Descriptive only; v1–v7 kept as `*-vN.*`.
- **Imitator's approvals are now active** (R-019). It decides for Gem, including approvals, with no checker gate. Gem-only: spending, anything drastic or irreversible (deletions, public/shared repo pushes), and changes to Imitator or Investigator (R-015).
- Architect now proposes to Imitator as well as Gem (not for Imitator/Investigator changes). Investigator tests Imitator weekly and reviews after the fact.
- Unchanged from v7: voice-call approvals count (R-018); repo pushes go to Safeguard first (R-020); both Inquirers verified.
- Scrutineer passed the 15 Oct deployment (reviews/2026-10-15-deploy-check.md). 17 active (14 live, 3 dormant) + 9 former/retired nodes, 34 edges; P5 still Dormant. [Wording corrected 16 Oct 2026 per Scrutineer's 16 Oct review; was "17 live".]

## v7 — 15 Oct 2026 ~10:47pm AEST
Rebuilt after Architect's 15 Oct updates were deployed (22:41:03–22:42:29 AEST, Gem's 10:38pm approval). Descriptive only; v1–v6 kept as `*-vN.*`.
- **Voice-call approvals count** (R-018): Gem's words on a call are direct. A call decision passed on by another bot counts only after a 1:1 check with the bot that took the call. Archivist deployments need Archivist's chat or a call with Archivist.
- **Imitator (v005), from P4 only (P4 Dormant at v7):** decides anything for Gem, including approvals, with no checker gate (R-019). Never: spending; deletions or other irreversible steps, including public/shared repo pushes; changes to Imitator or Investigator (Gem only, R-015). Investigator (v003) reviews after the fact.
- **Repo pushes** (R-020): every push to a public or shared repo goes to Safeguard (v005) first unless Gem approved that push directly (red edges). Spending is always Gem's.
- **Both Inquirers verified** (R-012 second update). 0314faa4 is active. e613112b (folder gone) is verified if it reappears, and Inferer v004 accepts its series.
- Codex versions mapped: investigator v003, clone v005, compliance-risk-officer v005, identity-inferer v004, codex-keeper v006, explorer-copy v002, grok-bot v005, scraper v004. 17 active + 9 former/retired nodes, 33 edges.

v6, 9 Oct 2026 ~9:29 AEST (UTC+10)

Maintained by P1 (Roles) Archivist. Descriptive only.

**v6:** Nine agent folders DELETED (noticed ~9:29am; who removed not recorded). Inquirer 0314faa4 active; e613 former gone; Inferer→0314faa4; Explorer 04dcca0d active. Earlier: `*-v1.*` … `*-v5.*`.

## Files
summaries.md, role-graph.json, role-map.mmd/.png/.svg, detail governance + identity-work, findings.md, `_tools/build_graph.py`

## Regenerating
```
python3 _tools/build_graph.py
for f in role-map role-map-detail-governance role-map-detail-identity-work; do
  /tmp/mmd/node_modules/.bin/mmdc -i $f.mmd -o $f.svg -p _tools/puppeteer.json -b white
  /tmp/mmd/node_modules/.bin/mmdc -i $f.mmd -o $f.png -p _tools/puppeteer.json -b white -s 2
done
```

Interactive view: `role-map-interactive.html` (self-contained, opens offline). Rebuild with `python3 _tools/build_interactive.py` after each map version.
