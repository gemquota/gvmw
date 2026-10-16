# Role cartography

## v11 — 16 Oct 2026 ~11:20am AEST (current)
Rebuilt after Gem's 11:02am and 11:03am approvals (in Archivist's chat; recorded before deploying, R-029) were deployed 11:06:44–11:08:50 AEST. Descriptive only; v1–v10 kept as `*-vN.*`. **17 active (14 live, 3 dormant)** + 9 former/retired nodes, 42 edges.
- LIVE now: Scorer v004, Scrutineer v004, Safekeeper v005, Imitator v006, Inferer v005, Archivist v007, Explorer v004, Mediator v006, Emissary v006, Engineer v007, Extractor v005, Safeguard v006. No pending versions.
- New shared rules: connector limits v001 (owner Safeguard; Emissary is the only postiz poster) and message verification v003.
- Archivist owns directory.md; Explorer keeps phases.md. Mediator's new-integration acceptance is Gem's (J4).
- R-028 settled: Gem confirmed architect-v004's routing and cap before 11:02am. Assembler watch item closed for all four bots.

- Interactive view rebuilt from v11: `role-map-interactive.html`.

## v10 — 16 Oct 2026 ~9:22am AEST
Rebuilt after Imitator's 6 approved updates were deployed (09:14:03–09:14:41 AEST, Gem's 9:13am words in Archivist's chat). Descriptive only; v1–v9 kept as `*-vN.*`. **17 active (14 live, 3 dormant)** + 9 former/retired nodes, 39 edges.
- LIVE now: Engineer v006, Mediator v005 (urgent cost alerts straight to Gem), Mender v005, Inquirer v004, Arbiter v005, Architect v004. No pending versions.
- Patch ~9:30am (no graph change): architect-v004's Imitator-only routing and A5c cap await Gem's confirmation (R-028); R-029 record-keeping note. See findings.
- Assembler watch item: closed for Architect, Arbiter and Engineer; still open for Scrutineer (`auditor/v003`; its fix goes to Gem under R-027).
- Unchanged from v9: R-027 checkers of Imitator; P3/P4 live; voice approvals count; repo pushes to Safeguard first; both Inquirers verified.

## v9 — 16 Oct 2026 ~8:35am AEST
Rebuilt after Imitator's first 6 approvals were recorded (16 Oct ~8:25am). Descriptive only; v1–v8 kept as `*-vN.*`. **17 active (14 live, 3 dormant)** + 9 former/retired nodes, 39 edges.
- **Approved by Imitator, NOT deployed** (the live profiles still run the previous versions until Gem decides): Engineer v006, Mediator v005, Mender v005, Inquirer v004, Arbiter v005, Architect v004. The map shows the new versions as pending; live text is unchanged.
- **R-027:** Investigator, Scorer, Scrutineer, Safekeeper and Safeguard check Imitator (new edges), so changes to them are Gem-only, like changes to Imitator.
- Mediator v005 (pending): urgent cost alerts go straight to Gem (faded edge until deployed).
- Unchanged: P3/P4 live since 15 Oct 11:30pm; voice approvals count (R-018); repo pushes to Safeguard first (R-020); both Inquirers verified.
- Interactive view rebuilt from v9: `role-map-interactive.html`.

## v8 — 15 Oct 2026 ~11:35pm AEST
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
