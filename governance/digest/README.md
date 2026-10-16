# Combined daily digest (owned by Explorer, 04dcca0d)

Gem asked on 10 Oct 2026 at 3:10am (relayed by Inquirer) for one combined daily summary from all bots, with any unread earlier ones shown together when Gem returns.

## How bots send their daily summary
- Write it as a short markdown file: `/workspace/governance/digest/inbox/YYYY-MM-DD/<BotName>.md` (date in Brisbane time; bare name, e.g. `Engineer.md`).
- At most about 10 lines. Group lines as Urgent, Needs Gem, FYI. Put any question for Gem as one line with the options.
- Append to the same file if you have more to add that day; don't make new ones.
- Do NOT message Gem separately with daily summaries. Urgent things still go straight to Gem (or to Explorer with priority).
- No secrets, tokens or private personal details in these files.

## What Explorer does
- Every day at 7:41am Brisbane, Explorer combines yesterday's and today's inbox files into `sent/YYYY-MM-DD.md` and sends it to Gem in Explorer's chat.
- `state.json` tracks which digests Gem hasn't seen yet. If Gem hasn't been active in Explorer's chat since the last digest, the next one includes the earlier unread ones as well.

## Compiling rules (added 16 Oct 2026 after Scrutineer's review)
- Only include a bot's line if there is an inbox file from that bot behind it. Never summarise a bot from memory or other files.
- File each inbox note under the date it was written (AEST), not the date it was compiled.
