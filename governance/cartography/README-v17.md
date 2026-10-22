# Role cartography

## v17 — 22 Oct 2026 8:01:02pm AEST (current)
Redundancy batch 2026-10-22 rev 2 is LIVE (deployed 7:57:01–7:57:52pm; Scrutineer verified, reviews/2026-10-22-redundancy-deploy-check.md): Inferer v006, Arbiter v006, Architect v005, Emissary v007, Extractor v006 and Explorer v006. Explorer assigns new work (R-044) and Mender keeps operational routing. New edges: Emissary → Explorer and Extractor → Explorer (hand back), and Architect → Archivist (drafts renames when Gem asks). Arbiter's stall clause is gone. No other change; v1–v16 kept as `*-vN.*`. 17 active, all live + 1 retired with no codex folder + 9 former/retired nodes, 51 edges.

- Interactive view rebuilt from v17: `role-map-interactive.html`.

## v16 — 22 Oct 2026 6:45:04pm AEST
**New Bot** (`6b01a4ef`) recorded as **retired** (Gem, 22 Oct 6:37pm, confirmed in Archivist's chat). It was gone from the live teammate list by about 6:40pm, so it was probably deleted by Gem, but deletion isn't confirmed and its folder remains. Drawn dotted grey in the "No codex folder" row, with no role and no edges. No codex change; v1–v15 kept as `*-vN.*`. 17 active, all live + 1 retired with no codex folder + 9 former/retired nodes, 48 edges.

- Interactive view rebuilt from v16: `role-map-interactive.html`.

## v15 — 22 Oct 2026 6:34:10pm AEST
Unrecorded live agent listed under Archivist's brief: **New Bot** (`6b01a4ef-8b54-44e6-ad11-64e7af681d12`), blank, with no codex folder. It's drawn as a node with no role and no relationships, awaiting Gem. First seen: profile.json created 19 Oct 2026 01:30:54 AEST; reported by Explorer to Archivist ~6:31pm AEST 22 Oct. No codex change; v1–v14 kept as `*-vN.*`. **17 active, all live** + 1 unrecorded + 9 former/retired nodes, 48 edges.

- Interactive view rebuilt from v15: `role-map-interactive.html` (new "Unrecorded" row).
- **INC-008 (22 Oct ~6:38pm):** the box restart briefly lost `/workspace/governance`. After Mender's restore (~6:43pm) the v15 files were back. Archivist checked them at 6:43pm by re-running `_tools/patch_v15.py` on the v14 files with the original time (6:34:10pm): all 8 source files were byte-identical, so v15 stands as restored and was not regenerated.

## v14 — 16 Oct 2026 3:58:15pm AEST
Rebuilt after shared connector limits v002 was recorded on Gem's 3:54pm words in Archivist's chat (default text d4fbfa8f391f, not variant B; shared document, no profile to deploy; verified by Scrutineer (PASS, reviews/2026-10-16-connector-limits-v002-check.md, written 3:58:26pm)). Descriptive only, from v002's text; v1–v13 kept as `*-vN.*`. **17 active, all live** + 9 former/retired nodes, 48 edges.
- New detail diagram `role-map-detail-connectors` and a `connectors` table in role-graph.json: who may use which connector under rules 1–19.
- Engineer: only Supabase user and GitHub writer, builds Zapier/n8n workflows. Extractor: runs Apify, with Mediator's spend check. Emissary: only postiz poster. Emissary, Explorer, Extractor and Engineer may write private Notion/Todoist items for Gem's direct work. No memory writers. Gmail sends need Gem's words; Imitator may approve a no-promises first reply (R-038).
- 4 new edges: Mediator → Safeguard (new connectors), Extractor → Mediator (Apify spend), Engineer → Safeguard (workflow/Supabase dry runs), Imitator → Safeguard (first-reply dry run).
- Cited by 6 live briefs (Emissary, Engineer, Explorer, Extractor, Mediator, Safeguard); 11 have no pointer yet.

- Interactive view rebuilt from v14: `role-map-interactive.html`.

## v13 — 16 Oct 2026 ~11:52am AEST
P5 (Emissary, Engineer, Extractor) went LIVE at 11:47am on 16 Oct 2026 (phases.md; Gem in Explorer's chat: "Initiate p5"). All five phases are live. Descriptive only; v1–v12 kept as `*-vN.*`. **17 active, all live** + 9 former/retired nodes, 44 edges.
- No codex change for P5: Emissary v006, Engineer v007 and Extractor v005 as before. Explorer's routing edges to them are no longer faded.
- Now live: Emissary is the only postiz poster, posting only text Gem approved word for word; Engineer's Vercel deployments count as public pushes; every public or shared repo push still goes to Safeguard first (R-020).

- Investigator v004 live 11:49:23 (Gem 11:48am): daily Imitator accuracy check and daily score to Scorer (new edge). Awaiting Scrutineer's check.
- Interactive view rebuilt from v13: `role-map-interactive.html`.

## v12 — 16 Oct 2026 ~11:50am AEST
Rebuilt after Gem's 11:41am approval in Archivist's chat (recorded first, R-029): Archivist v008 live 11:44:11 and Explorer v005 live 11:44:26; shared message verification v004 recorded. Descriptive only; v1–v11 kept as `*-vN.*`. **17 active (14 live, 3 dormant)** + 9 former/retired nodes, 43 edges.
- Archivist may now deploy a version Imitator approved within its authority, after a 1:1 check with Imitator and Safeguard's dry-run report (new edge Archivist → Safeguard). Never for Archivist's own brief, Imitator or its five checkers, role-widening, spending or irreversible steps.
- Explorer still never writes profiles (R-014). R-010 has no update in rulings.md yet. No pending versions.

- Interactive view rebuilt from v12: `role-map-interactive.html`.

## v11 — 16 Oct 2026 ~11:20am AEST
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
