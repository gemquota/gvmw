# Connector status (kept by Mediator, id 90f9eb20)

Read-only status checks only. Mediator never reconnects or re-authorises anything; Gem signs in. Times are AEST.

## Latest check: Thu 22 Oct 2026, 6:44pm (catch-up health check after 16-22 Oct outage; one light read per connection)

| Connector | Status | Notes |
|---|---|---|
| Gmail (default, slapredpokies, slapredgit, artifactrap, gemquota) | Connected, OK | get_me verified: dayne.keefe@, slap.red.pokies@, slapredgit@, artifactrap@, gemquota@gmail.com. All five labels now match their real accounts |
| Gmail-xai | Connected, OK | Send-as is artifactrap@gmail.com |
| Google Calendar (all five) | Connected, OK | Primary calendars: default = dayne.keefe@gmail.com, slapredpokies = slap.red.pokies@, slapredgit = slapredgit@, artifactrap = artifactrap@, gemquota = gemquota@gmail.com |
| Google Drive (default) | ERROR: insufficient scopes | list_recent_files returned 403 ACCESS_TOKEN_SCOPE_INSUFFICIENT. Gem needs to re-sign-in to this connection with full Drive access |
| Google Drive (slapredpokies, slapredgit, artifactrap, gemquota) | Connected, OK | list_recent_files worked (gemquota Drive is empty) |
| Google Drive-xai | Connected, OK | Root listing worked; same Drive as slapredgit |
| Google Docs, Slides, Sheets (all five) | Connected (status only) | No cheap read without a file id, so no call made |
| Vercel and Vercel-xai | Connected, OK | list_teams: no teams (personal account) |
| postiz | Connected, OK | integrationList is empty: no social channels connected |
| Apify | Connected, OK | Docs search worked. The MCP has no account or usage read |
| Context7 | QUOTA EXCEEDED | "Monthly quota exceeded". Needs a free Context7 API key (Gem enters it, rule 19) or wait for the monthly reset |
| Exa | Connected (status only) | No call made (it uses search quota) |
| Notion and Notion-xai | Connected, OK | Both signed in as artifactrap@gmail.com ("Artifact Rap's Space"), not gemquota@ |
| Todoist | Connected, OK | find-projects worked (Inbox) |
| Zapier | Connected, OK | No actions enabled yet |
| Supabase | Connected, OK | list_projects: no projects |
| GitHub-xai | Connected, OK | Signed in as gemquota |
| gh CLI (box) | OK | DayneK (active) and gemquota (inactive) |
| Origin (source control) | Connected (status only) | |
| X | Connected (status only) | |
| Mem0 | ERROR | Tool discovery fails (still no API key) |
| n8n | ERROR | Tool discovery fails (still no MCP URL) |
| Adapter | Needs sign-in | Unchanged since 16 Oct |
| Finance (xAI, bank linking) | Needs sign-in | Unchanged since 16 Oct |
| GitHub (built-in) | Not connected | Needs GitHub linked to Gem's Cursor account |

## History
- 16 Oct 2026: page started (it should have existed from 9 Oct; flagged by Scrutineer's 16 Oct review). No checks were run 9 to 15 Oct.
- 16 Oct 2026, 9:17am: Google Drive connected by Gem.
- 16 Oct 2026, 9:23am: Gem asked for Vercel, Google Calendar, Google Sheets and postiz; all installed. Vercel connected 9:24am. GitHub CLI on the box is signed in as DayneK; Gem asked about adding gemquota.

## Safeguard risk notes (RR-028, 16 Oct 2026, 9:25am)
Acceptance is Gem's call; Safeguard sets out the risks and proposes limits through Architect. Interim limits until a brief covers them:
- **postiz (High):** posts publicly as Gem to Facebook and Reddit, and posts can't be fully taken back. Gambling promotion to Australians risks breaching the Interactive Gambling Act, and both platforms restrict gambling and automated posting. Gem approves each exact post; no gambling content at all; every post goes to Safeguard for a dry run first.
- **Vercel:** deployments are public sites. Treat each like a public push: Safeguard first, unless Gem approved that deployment directly.
- **Google Sheets, Drive, Calendar:** these write to outside services. No uploading or sharing box files (especially personal or casino data) and no calendar invites to other people without Gem's direct OK.
- **Finance:** links bank accounts. Bring in Safekeeper if it ever connects.
- 16 Oct 2026, 11:19am: gemquota added to the box GitHub CLI from a token Gem provided (classic token, full scopes incl. delete_repo and admin:org). DayneK kept as the active default; switch with gh auth switch. Safekeeper and Safeguard told.
- 16 Oct 2026, 11:22am: Gem asked to add slap.red.pokies@, artifactrap@ and gemquota@gmail.com to every Google connector (Gmail, Docs, Slides, Drive, Sheets, Calendar). Existing default account is dayne.keefe@gmail.com (confirmed via Calendar). 18 sign-in cards shown, labelled slapredpokies, artifactrap and gemquota. Safeguard told.
- 16 Oct 2026, 11:24am: Gem added slapredgit@gmail.com to the request; six more cards shown (label slapredgit). slapredpokies verified on Calendar as slap.red.pokies@gmail.com; all six slapredpokies connectors connected.
- 16 Oct 2026, 11:45am: Sign-ins drifted, so labels didn't match the real accounts. With Gem's OK I removed the unused slapredgit sign-in slots, renamed artifactrap to slapredgit on all six Google connectors (verified on Gmail, Calendar, Drive and Sheets; inferred for Docs and Slides) and renamed gemquota to artifactrap on Gmail, Drive, Docs and Slides (verified on Gmail and Drive; inferred for Docs and Slides). Still to sign in: artifactrap on Calendar and Sheets, and gemquota on all six. slapredpokies is verified correct.

- 16 Oct 2026, 3:11pm: Notion, Exa and Todoist connected; Zapier and Supabase pending auth; n8n needs MCP URL; Mem0 needs API key (all installed at Gem's request, Gem advised to sign in as gemquota@gmail.com; account not yet verified). Safeguard notified (RR-041; proposed limits with Architect). Until Gem approves them, connector-limits v001 rule 5 applies: every send, write, workflow run or database change through these connectors needs Gem's direct words plus a Safeguard dry run first.
- 16 Oct 2026, 3:12pm: At Gem's request, set up Jupyter on the box (JupyterLab, Notebook, nbclassic, nbconvert, papermill in /workspace/tools/jupyter-venv, linked into /usr/local/bin) and the Obsidian app (v1.14.4 AppImage, extracted at /opt/obsidian/app, launcher /usr/local/bin/obsidian) plus a local git vault at /workspace/obsidian-vault. No remote yet.

- 16 Oct 2026, 3:12pm: Zapier connected (account not yet verified). Supabase still pending auth. RR-041 interim rule applies.

- 16 Oct 2026, 3:14pm: Supabase connected (account not yet verified). Still to go: n8n (needs MCP URL) and Mem0 (needs API key). RR-041 interim rule applies.

- 16 Oct 2026, 3:18pm: At Gem's request (DayneK chosen), created private repo DayneK/obsidian-vault and pushed the local vault from /workspace/obsidian-vault.

- 16 Oct 2026, 3:57pm: CORRECTION to the 3:11pm line. The interim rule summary there was broader than the text. Rule now in force: connector-limits v002 (Gem approved 3:54pm). Rule 5 wording: "Until this rule or a bot's brief covers a newly installed connector, every send, post, share, upload, deployment or purchase through it needs Gem's direct words and a Safeguard dry run first." v002 also gives specific rules: 7 for Zapier/n8n, 8 for Supabase (Engineer only), 9 for Notion/Todoist, 11 for Mem0 (no writers yet) and 19 for keys (Gem enters them in the connector's own settings). Engineer is the only bot that writes to GitHub and Supabase.

- 16 Oct 2026, 3:59pm: Engineer created repo gemquota/gvmw (reported as private, but actually PUBLIC from creation per Safeguard RR-045; Gem confirmed public on purpose at 6:45pm on 22 Oct) and pushed the checked workspace snapshot (commit e21adc3), on Gem's 3:57pm words. Only collaborator is gemquota.
- 22 Oct 2026, 6:44pm: catch-up health check after the 16-22 Oct outage: Gmail, Calendar, Drive (except default), Vercel, postiz, Apify, Notion, Todoist, Zapier, Supabase, GitHub-xai and gh CLI are fine, and all Google labels now match their real accounts. Problems: default Drive has insufficient scopes (403), Context7 is over its monthly quota, Mem0 and n8n fail discovery, and Adapter, Finance and built-in GitHub still need sign-in. Notion is signed in as artifactrap@, not gemquota@. No spend figures could be read.
- 22 Oct 7:55pm: default Drive (dayne.keefe) reconnected 7:20pm; read-only check returns no 403 but root and recent lists are empty, so full scope is unconfirmed. Notion on artifactrap@ confirmed by Gem. gvmw auto-sync approved by Gem (scan plus dry run per push).
