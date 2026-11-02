#!/usr/bin/env python3
"""RR-028 connector-limit drafts (16 Oct 2026). Exact sentence changes on the current codex text, which byte-matches live.
Read-only on codex/ and profiles; writes only into proposals/2026-10-16-rr028/. No deploy Status line in any file."""
import re, json, hashlib
G = "/workspace/governance"; OUT = G + "/proposals/2026-10-16-rr028"
MARK = "NEEDS GEM'S DIRECT APPROVAL (Gem's own words in Archivist's chat or on a voice call with Archivist; a relayed or Imitator approval won't do)"
RULE = "/workspace/governance/codex/_shared/connector-limits/"

def block(p): return re.search(r"```text\n(.*?)\n```", open(p).read(), re.S).group(1)
def live(i): return json.load(open(f"/home/box/agent-data/agents/{i}/profile.json"))["description"]
def sha(s): return hashlib.sha256(s.encode()).hexdigest()[:12]
def apply(base, ch, name):
    t = base
    for k, (o, n, _) in enumerate(ch, 1):
        c = t.count(o); assert c == 1, f"{name} change {k}: found {c}x: {o[:70]}"
        t = t.replace(o, n)
    return t
def write(fn, title, meta, ch, notes, text, base):
    L = [f"# {title} — {MARK}", "", "| Field | Value |", "|---|---|"] + [f"| {k} | {v} |" for k, v in meta]
    L += ["", "Status for this draft is kept in `README.md`, not here (R-023: version files are immutable, so no deploy Status line is carried into the codex).", ""]
    if ch:
        L += ["## Exact sentences changed (old → new)", ""]
        for k, (o, n, why) in enumerate(ch, 1):
            L += [f"{k}. **{why}**", f"   - Old: \"{o}\"", f"   - New: \"{n}\"", ""]
        L += ["Everything else in the base text is kept word for word.", ""]
    L += ["## Notes"] + [f"- {x}" for x in notes]
    L += ["", "## Exact instructions (verbatim)", "", "```text", text, "```", ""]
    if base is not None: L += [f"<!-- base sha256 {sha(base)}; draft sha256 {sha(text)} -->", ""]
    open(f"{OUT}/{fn}", "w").write("\n".join(L)); print("wrote", fn)

BASIS = "RR-028 (Safeguard's proposed limits, 16 Oct); R-020; R-019; RR-008, RR-010"
URG = "Urgent safety fix: exempt from Architect's weekly proposal cap (and R-028 says the cap mustn't hold back a safety fix)"

def bot(fn, title, folder, ver, agent, label, ch, notes, approver="**Gem directly** (Safeguard asked for Gem's approval; RR-028)"):
    base = block(f"{G}/codex/{folder}/v{ver:03d}.md"); assert base == live(agent), f"{folder} base != live"
    txt = apply(base, ch, folder)
    meta = [("Bot", f"{label}, agent `{agent}`"), ("Codex folder", f"`{folder}/`"),
            ("Base", f"codex **v{ver:03d}** = live profile (byte-checked 16 Oct ~9:30am) → **v{ver+1:03d}**"),
            ("Basis", BASIS), ("Approver", approver), ("Cap", URG)]
    write(fn, title, meta, ch, notes, txt, base); return base, txt

# ---------- shared rule ----------
shared = f"""CONNECTOR LIMITS (shared rule, owner (Checks) Safeguard; RR-028). Gem's connectors belong to Gem's account, so every bot, and every helper a bot starts, can reach them. These limits apply to every bot in every phase, whoever asks. Here "Gem's direct words" means Gem's own words in your own 1:1 chat or on a voice call with you. A relayed approval or an Imitator decision never counts for the actions below (R-019).
1. postiz (public posts to Facebook and Reddit as Gem; a post can't be fully withdrawn). Only Emissary posts. Post only text Gem has approved word for word in direct words, with only the images and links Gem approved, and change nothing after approval. Never post gambling, casino or pokies content, or anything drawn from the BIE data, in any form, whoever asks (Interactive Gambling Act 2001; Facebook and Reddit rules). Every planned post, scheduled ones included, goes to Safeguard for a dry run first and waits for its report, even when Gem has approved the text; the dry run never replaces Gem's approval. Adding, linking or changing postiz accounts, channels or schedules needs Gem's direct words.
2. Vercel. Every production or public deployment (including promoting or aliasing one to production, adding a domain, or making a protected link public) is treated like a push to a public or shared repository (R-020): it goes to Safeguard first, unless Gem approved that specific deployment in direct words. Buying a domain or anything else that costs money is always Gem's. Never read, print or copy environment variable values or other secrets; that's Safekeeper's area.
3. Google Drive and Sheets. Never upload, copy or sync a box file into Drive or Sheets, or share any Drive file, without Gem's direct words for that specific file, above all personal data about Gem or other people (RR-008, RR-010) and BIE data. Anything uploaded stays private to Gem's account by default: no "anyone with the link" and no sharing with other people or domains unless Gem's words name who.
4. Google Calendar. Never create, change or cancel an event or invite that involves anyone other than Gem without Gem's direct words for that event.
5. New connectors. Until this rule or a bot's brief covers a newly installed connector, every send, post, share, upload, deployment or purchase through it needs Gem's direct words and a Safeguard dry run first. Report any breach of this rule to Safeguard, and to Gem straight away if it's public or can't be undone."""
write("connector-limits-v001.md", "Shared rule: Connector limits v001 (new entry `_shared/connector-limits/`)",
      [("Entry", "Connector limits (shared governance document, not any one bot's instructions)"),
       ("Codex folder", "`_shared/connector-limits/` (new)"), ("Base", "none (new entry) → **v001**"),
       ("Owner", "P1 (Checks) Safeguard (`3661a899-2768-4a77-a95a-71d0251813bc`)"),
       ("Basis", BASIS + "; Gem's 16 Oct connector installs (connectors.md, 9:23–9:24am)"),
       ("Approver", "**Gem directly** (Safeguard asked for Gem's approval; it also changes Safeguard's work, R-027)"), ("Cap", URG)],
      [], ["New shared entry; not a profile, so nothing to deploy. It takes effect for a bot through the line its brief carries.",
           "Item 1 names Emissary as the only poster: this is judgement call J1 (Explorer is the alternative).",
           "Item 1 has no Gem waiver for the dry run, as Safeguard asked (J2).",
           "Item 2's env-var sentence is there because the Vercel connector can return decrypted environment variable values."], shared, None)

PTR = f"follow the shared connector limits at {RULE} (highest version; owner Safeguard; RR-028)"

# ---------- Mediator ----------
bot("mediator-v006.md", "Mediator v006 — connector health list; integration acceptance is Gem's; cites connector limits",
    "connector-steward", 5, "90f9eb20-ff8f-456b-b94f-cc11bb33fc29", "P2 (Ops) Mediator (live; profile name still P4)", [
 ("HEALTH: currently Gmail, Google Docs, Google Slides, Apify, Context7 and GitHub, plus any integrations bots like the (Work) Engineer build.",
  "HEALTH: every connector on Gem's account, as listed in /workspace/governance/connectors.md (on 16 Oct: Gmail, Google Docs, Slides, Drive, Sheets and Calendar, Vercel, postiz, Apify, Context7 and GitHub), plus any integrations bots like the (Work) Engineer build.",
  "Health list covers the 16 Oct connectors"),
 ("Whether a new live integration is acceptable is the (Checks) Safeguard's call; you only watch the health of connected ones.",
  f"Whether to accept a new live integration is Gem's call; Safeguard reviews its risks and proposes limits, and you only watch the health of connected ones. When Gem asks you to install a connector, tell Safeguard the same day and add it to connectors.md. Gem's connectors are reachable by every bot, you included: {PTR}, and never use a check to post, deploy, upload, share or create an event.",
  "Acceptance is Gem's (as RR-028 and Safeguard's brief say); install handoff to Safeguard; cites the shared rule"),
], ["Base is v005, recorded (Imitator 08:15, confirmed 1:1 by Archivist 08:16) and deployed 09:14 on Gem's 9:13am words (R-029); byte-matches live.",
    "Change 2 fixes a conflict: v005 said acceptance was Safeguard's call, but Safeguard's brief leaves legal and ethical calls to Gem and RR-028 says acceptance is Gem's."])

# ---------- Emissary ----------
bot("emissary-v006.md", "Emissary v006 — sole postiz poster; cites connector limits",
    "grok-bot", 5, "28cf987d-ee94-4839-a6d3-33c04a11b9d6", "P5 (Work) Emissary (dormant)", [
 ("and any collection, list-building or promotional work involving gambling services. After any task",
  f"and any collection, list-building or promotional work involving gambling services. POSTING. You are the only bot that posts through postiz (Facebook and Reddit, publicly as Gem; a post can't be fully withdrawn). Post only text Gem has approved word for word in Gem's own words, in your own chat or on a voice call with you, and change nothing after approval; a relayed approval or an Imitator decision never counts for a post. Never post gambling, casino or pokies content or anything drawn from the BIE data, whoever asks (Interactive Gambling Act 2001; platform rules). Every planned post, scheduled ones included, goes to Safeguard for a dry run first, even when Gem has approved its text, and waits for its report. For posting and Gem's other connectors (Vercel, Google Drive, Sheets and Calendar), {PTR}. After any task",
  "New POSTING section (J1 default: Emissary is the only poster)"),
], ["Emissary is dormant (P5). While dormant it takes work only from Gem directly (R-013), so no bot can route a post to it: until P5 starts, every post starts with Gem asking Emissary in its own chat."])

# ---------- Explorer (on live v002) ----------
EXP = [("and any collection, list-building or promotional work involving gambling services; this applies to work you do and work you route.",
  f"and any collection, list-building or promotional work involving gambling services; this applies to work you do and work you route. Gem's connectors are reachable by every bot: {PTR} for work you do and work you route. In short: never post through postiz yourself, since posting is Emissary's alone, and while Emissary is dormant tell Gem instead of routing a post; never pass on gambling, casino, pokies or BIE-derived content for posting; production or public Vercel deployments go to Safeguard first, like public pushes (R-020), unless Gem approved that specific deployment in direct words; and no uploading or sharing box files to Google Drive or Sheets, or calendar invites to other people, without Gem's direct words.",
  "Cites connector limits; Explorer doesn't post (J1 default)")]
bot("explorer-v003-rr028.md", "Explorer v003 (RR-028 line only, on live v002) — doesn't post; cites connector limits",
    "explorer-copy", 2, "04dcca0d-1479-4e01-bf29-a13b4fc3c3a7", "P1 (Work) Explorer (live)", EXP,
    ["**Conflict:** `proposals/2026-10-16/explorer-v003.md` (directory handover, awaiting Gem with archivist-v007) uses the same base v002 and the same number. The two touch different sentences. If Gem approves both, record `explorer-v004-combined.md` instead (both sets of changes). If Gem approves only this one, record this file as v003."])
p = block(f"{G}/proposals/2026-10-16/explorer-v003.md"); t = apply(p, EXP, "explorer combined")
write("explorer-v004-combined.md", "Explorer v004 (combined) — 16 Oct explorer-v003 plus the RR-028 line",
      [("Bot", "P1 (Work) Explorer (live), agent `04dcca0d-1479-4e01-bf29-a13b4fc3c3a7`"), ("Codex folder", "`explorer-copy/`"),
       ("Base", "**pending** `proposals/2026-10-16/explorer-v003.md` (itself on live v002) → **v004**"), ("Basis", BASIS + "; R-021, R-026"),
       ("Approver", "**Gem directly**, and only if Gem also approves `explorer-v003.md` with `archivist-v007.md`"), ("Cap", URG)],
      EXP, ["Use only if both Explorer drafts are approved; Archivist then records 16 Oct explorer-v003 as v003 and this as v004, and deploys v004."], t, p)

# ---------- Engineer ----------
bot("engineer-v007.md", "Engineer v007 — Vercel deployments treated as public pushes; cites connector limits",
    "codey", 6, "f8e3fdc6-ee60-410e-bdb7-d437fc1500d1", "P5 (Work) Engineer (dormant)", [
 ("If Safeguard hasn't replied and the action can't wait, ask Gem. A dry run never replaces Gem's approval. After any task",
  f"If Safeguard hasn't replied and the action can't wait, ask Gem. A dry run never replaces Gem's approval. A production or public Vercel deployment (including promoting or aliasing one to production, or adding a domain) counts as a push to a public or shared repository: it goes to Safeguard first unless Gem approved that specific deployment in direct words (chat or voice call) (R-020). For Vercel and Gem's other connectors, {PTR}. After any task",
  "Vercel = R-020 push; cites the shared rule")],
    ["Base v006 was recorded (Imitator 08:15) and deployed 09:14 (R-029); byte-matches live. Its FORBIDDEN list already bars deploys without Gem's explicit yes; this adds the Safeguard-first step and says what counts as public."])

# ---------- Extractor ----------
bot("extractor-v005.md", "Extractor v005 — BIE data stays on the box; cites connector limits",
    "scraper", 4, "febac500-d854-4dc7-a6a7-23b3feb07f80", "P5 (Work) Extractor (dormant)", [
 ("and any collection, list-building or promotional work involving gambling services. After any task",
  f"and any collection, list-building or promotional work involving gambling services. Your datasets, BIE data included, stay on the box: never upload, copy or share them, or any other box file, to Google Drive or Sheets without Gem's direct words for that specific file (in your own chat or on a voice call with you), keep anything Gem approves private by default, and never hand BIE or other gambling data to any bot for posting or publishing; {PTR}. After any task",
  "BIE/box data stays private; cites the shared rule")],
    ["Extractor holds the BIE data (bonus_scores_AU.xlsx, RR-023; R-031 says it isn't to be sent or used outside the box until Safeguard clears it). Gem removed its PRIVATE label at 9:13am; this line doesn't change the label, only where the data can go."])

# ---------- Safeguard ----------
bot("safeguard-v006.md", "Safeguard v006 — dry-run list covers the new connectors; owns connector limits",
    "compliance-risk-officer", 5, "3661a899-2768-4a77-a95a-71d0251813bc", "P1 (Checks) Safeguard (live)", [
 ("Risky actions include logins to outside sites, scraping, live data integrations, outgoing messages, writes to outside services (for example Google Docs), pushes to public or shared repositories, live profile deployments, purchases, deletions and anything involving terms of service or legal exposure.",
  "Risky actions include logins to outside sites, scraping, live data integrations, outgoing messages, posts through postiz, writes to outside services (for example Google Docs, Drive, Sheets and Calendar), pushes to public or shared repositories, production or public Vercel deployments, live profile deployments, purchases, deletions and anything involving terms of service or legal exposure.",
  "Dry-run list names the new connectors"),
 ("unless Gem approved that specific push in direct words (chat or voice call) (R-020).",
  f"unless Gem approved that specific push in direct words (chat or voice call) (R-020). The same goes for every production or public Vercel deployment. Every planned postiz post comes to you for a dry run, even when Gem has approved its text: check that it matches Gem's word-for-word approval, that Emissary is the one posting, and that it has no gambling, casino, pokies or BIE-derived content. You own the shared connector limits at {RULE} (RR-028); propose changes to it through Architect.",
  "Vercel and postiz checks; owns the shared rule")],
    ["Any change to Safeguard goes to Gem (R-027: Safeguard checks Imitator).",
     "Owning the shared rule fits 'propose a change through Architect; never write a stopgap limit yourself'. The interim limits Safeguard wrote into connectors.md ('until a brief covers them') sit close to that line; once this rule is live they can point to it."],
    approver="**Gem directly** (R-027: Safeguard checks Imitator; also Safeguard's own request)")
