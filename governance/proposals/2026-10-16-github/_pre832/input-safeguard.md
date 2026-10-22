# Safeguard input: shared GitHub rule (16 Oct 2026)
Based on safeguard v006, rulings R-020/R-022/R-033, connector-limits v001, and RR-017, RR-020, RR-021, RR-033 and RR-037. Architect makes the proposal, Gem or Imitator approves, and Safeguard doesn't review this rule once it's drafted, because it sets Safeguard's own triggers.

## Suggested limits
1. Read-only by default. Any bot may read, list and clone repos into /workspace for its own task. Nothing else is allowed without a named role below.
2. Commits and pushes: Engineer only, as code owner. Other bots hand changes to Engineer. Every push to a public or shared repo comes to Safeguard for a dry run first, unless Gem approved that specific push in direct words (R-020). Pushes to private, unshared repos may go ahead without a dry run, but they must be logged.
3. Never push secrets, cookies, tokens, personal data, BIE or scraper outputs, or gambling, casino or pokies data to any repo, public or private. Safekeeper scans before any public push.
4. Changing visibility (private to public) counts as publishing. It needs Gem's direct words and a Safeguard dry run first.
5. Deletions: repo deletion, branch deletion on a public or shared repo, force-push, history rewrites, and deleting tags or releases. Each one needs Gem's direct words for that specific item (R-022/R-033). Inferred wording such as "I assume the same" doesn't count, and Imitator can't approve these.
6. Settings and admin: org or admin changes, collaborators, deploy keys, webhooks, Actions secrets, branch protection, transfers and token or app changes. These need Gem's direct words. Safekeeper owns any credential side.
7. Account choice: DayneK stays the default. Switching to gemquota needs a stated reason, gets logged, and is limited to the task. Neither token's delete_repo or admin:org scope may be used without item 5 or 6.
8. Imitator may approve reads, private commits and opening PRs only. It can't approve anything in items 4–6 or any public push.
9. Who's allowed: retired or dormant bots, and bots without GitHub in their brief, may only read.

## Dry-run triggers (send to Safeguard first)
- Any push, merge or PR merge to a public or shared repo.
- Any change from private to public, any new public repo, or a public fork.
- Any deletion, force-push or history rewrite.
- Any settings, collaborator, webhook, Actions or deploy-key change.
- Any action using the gemquota account.
- Anything touching the content listed in item 3.

## Logging
Every write (commit, push, PR, branch or settings change) gets one line in a shared log under governance/, recording the bot, account, repo, visibility and Gem's quote where one is needed. That lets Safeguard's scheduled run find after-the-fact items.
