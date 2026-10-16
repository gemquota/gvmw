# Connector status (kept by Mediator, id 90f9eb20)

Read-only status checks only. Mediator never reconnects or re-authorises anything; Gem signs in. Times are AEST.

## Latest check: Fri 16 Oct 2026, 9:14am (connector status list, read-only)

| Connector | Status | Notes |
|---|---|---|
| Gmail | Connected | |
| Google Docs | Connected | |
| Google Slides | Connected | |
| Apify | Connected | Usage-priced; no billing data read |
| Context7 | Connected | |
| Origin (source control) | Connected | |
| Google Drive | Connected | Gem signed in 16 Oct, 9:17am |
| Adapter | Needs sign-in | Gem chose to connect it on 16 Oct; sign-in card shown, waiting on Gem |
| Finance (xAI, bank linking) | Needs sign-in | Gem chose to connect it on 16 Oct; sign-in card shown. It links bank accounts, not xAI usage billing. Waiting on Gem |
| GitHub (built-in) | Not connected | Uses the GitHub link on Gem's Cursor account, which isn't linked yet. It can't be fixed from here |
| Vercel | Connected | Installed and signed in by Gem 16 Oct, 9:24am; new live integration, Safeguard review pending |
| Google Calendar | Connected | Installed 16 Oct 9:23am, signed in by Gem 9:28am |
| Google Sheets | Connected | Installed 16 Oct 9:23am, signed in by Gem 9:29am |
| postiz (social posting) | Connected (Gem signed in 9:31am) | Installed 16 Oct 9:23am at Gem's request for Facebook and Reddit posting; posts publicly as Gem; card shown |

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
