# Live risks: actions on 9 Oct 2026 (AEST, UTC+10)

Done by Explorer's executor on Gem's approval (9:04am, relayed by Explorer). Rule: reversible only, move rather than delete, except the 5 Facebook snapshots Gem told us to delete (9:05am). Related: RR-001, RR-008, RR-009, RR-010 (risk/register.md); T-001, T-003, T-004 (security/threat-register.md).

## (a) Facebook-logged-in automation browser: found, NOT stopped

- **What it is:** Chrome, PID **271421**, `--user-data-dir=/home/box/chrome-profile/Fork-2`, `--remote-debugging-port=9224` (127.0.0.1), `--class=box-chrome`, display `:2`, started Tue 6 Oct 11:36pm. Profile folder last written 8:40am today.
- **Open tab (checked 9:06am, URL and title only):** `facebook.com/messages/t/…`, title "(20) Messenger | Facebook". So Gem's Facebook account is logged in and a Messenger conversation is open right now.
- **Who started it:** not a bot script. Parent is PID 53 (`/usr/local/bin/sand-exit-watch`, the box's own supervisor), via the `box-bounded-log` wrapper (PIDs 271423-271425, log `/tmp/chrome:2.log`). cwd of the browser is `/workspace`. Display `:2` belongs to **Emissary** (28cf987d) per `/home/box/.sand-window-assignments.json`, so this is Emissary's per-agent desktop browser.
- **"Playwright attached":** PID **271900** (parent PID 377, the box's exec-daemon) runs `sand-playwright-runtime … --cdp-endpoint http://127.0.0.1:9224`, with worker PIDs 274406-274408 (since 6 Oct 11:41pm). That's the box's standard browser-control tool for that desktop, not a separate scraper. The box's own services (PIDs 237 session-sync, 238 web-bot-auth, 267 ua-governor, 332 cookie-persist) are also connected to it, as they are to Engineer's browser (Fork-3, PID 322389, display `:3`, port 9225, which has a localhost VEPA tab open and no Facebook).
- **Decision: not stopped.** It's a box desktop browser, launched and supervised by the box itself, of the same kind as every other agent's desktop browser. It isn't clearly a separate automation or scraper process, and the rule was "if unsure, don't kill". The supervisor would also probably relaunch it, and the shared cookie seed (b) would log Facebook straight back in.
- **Recommended fix (Gem to choose):** (1) Gem opens Emissary's desktop and logs out of Facebook there. Logging out invalidates the session for every browser and the cookie seed. Or (2) Gem tells Explorer to `kill -TERM 271421`, knowing it may come back logged in. Either way, Facebook logins on the box need Gem's decision (RR-009).

## (b) Cookie file rewritten 8:49am: found, NOT moved

- **File:** `/home/box/sand-data/chrome-cookie-seed.json`. This is the same file as `/home/box/agent-data/chrome-cookie-seed.json`, because `agent-data` is a symlink to `sand-data`. Size 28,461 bytes, mode **644** (readable by every user), owner box, mtime **9 Oct 8:49:54am**. Contents weren't opened.
- **What writes it:** the box's own cookie-persistence service (PID 332, `/usr/local/bin/sand-cookie-persist.mjs`), which keeps logins shared across agents' browsers. It's box infrastructure, not an export made by a bot.
- **Other exports searched for:** cookie, storage_state, session and auth files, plus JSON with cookie fields (`sameSite`, `httpOnly`, `c_user`), across /workspace, /home/box/reference and /home/box/.config, excluding chrome-profile. **None found.** The only file under /workspace and /home/box written between 8:44 and 8:55am was the seed itself.
- **Decision: not moved or chmodded.** It's maintained live by the box's service and isn't a bot's export in /workspace, so moving it would break shared logins or just be rewritten. Every bot runs as the same user (uid 1000), so chmod 600 wouldn't stop a bot reading it anyway (T-006).
- **Recommended fix:** log out of the sites that shouldn't be shared (Facebook first) and let the service rewrite the seed. Safekeeper keeps T-001 open.

## (c) Gem's personal details: moved to quarantine

- `/workspace/id-investigator/factcheck-2026-10-04.md` (14,639 bytes, written 4 Oct 9:43pm, mode 644) was moved at **9:07am** to `/home/box/quarantine/2026-10-09/id-investigator/factcheck-2026-10-04.md`. sha256 868d0f7e5ca013392461eb8deb17dd5736ae59f98e121740cd0978bbc801c8cc, the same before and after.
- Its stale LibreOffice lock file `.~lock.factcheck-2026-10-04.md#` (5 Oct 6:15pm) was moved with it.
- Quarantine folders `/home/box/quarantine` and `/home/box/quarantine/2026-10-09` (plus its subfolder) are chmod 700, files chmod 600, with a README there.
- **Stub left** at the old path: one line saying where the file went and that only Gem can approve access.
- **Caution:** LibreOffice Writer (PIDs 760510 and 760528, started 7 Oct 9:31pm) still has the document open on display `:20`, which is **Investigator**'s desktop. It wasn't stopped. If someone presses Save there, Writer will write the full text back over the stub. Recommend Gem or Investigator closes that Writer window without saving.
- **Not moved (not flagged by the review, so outside the scope given):** `incidents/2026-10-03-identity-set5-unverified.md` (T-005 / RR-010: sensitive personal details quoted in an incident file). Recommend Gem decide whether to quarantine it too.

## Facebook snapshots in /workspace/.playwright-mcp/ (RR-001, T-003)

- **Deleted permanently at 9:05:49am** on Gem's direct words at 9:05am, "Yes, delete the Facebook snapshots" (relayed by Explorer; also recorded in Safeguard's chat). Exactly these 5 files, with their sha256 before deletion:
  - page-2026-10-04T07-38-13-843Z.yml: f8a15ff20f44d10ed4cf239fe68f679831191ea27a9384bebbb335a8c39b0495
  - page-2026-10-04T07-38-16-632Z.yml: 7515dd4d8c1b1c0d9e241fac7a790c04a87421a7772bb12ffd54973c2707dd07
  - page-2026-10-04T07-41-49-870Z.yml: 64ea119b62812076e112b26f549aea5c04b342c840b85061f51c720e829d1a4b
  - page-2026-10-04T07-41-55-483Z.yml: f1068cb2bb353d9fe438a8623247c77f49f412e89bee7a559d0e8f07929bb388
  - page-2026-10-04T07-43-08-711Z.yml: e52ae63b3015b465361023447775a9aff6f03cc5b9b85d82a4769ef9f8492608
  - Checked afterwards: all 5 are gone. They were never copied to quarantine.
- **Console logs kept in place (not moved):** `console-2026-10-04T07-38-07-625Z.log` (17 lines) and `console-2026-10-04T07-41-46-434Z.log` (423 lines, last written 6 Oct 10:22am). Checked: **no message content**. They hold only browser warnings, Facebook's "Stop!" self-XSS banner and websocket errors. But the websocket URLs include Facebook account and device identifiers (`x-dgw-uuid`, `x-dgw-deviceid`). Flagged for Gem and Safekeeper; not moved, because the instruction was to move them only if they held message content.
- Nothing else in that folder was touched. Older files there, from 1-4 Oct, weren't reviewed.

## Things noticed along the way
- At 9:03-9:04am today, 10 live `profile.json` files were rewritten (0314faa4, Emissary, Safeguard, Safekeeper, Archivist, Explorer, Mender, Assembler, Engineer, Extractor). The executor didn't do this. **[Inferred]** It's the deployment of the 6 Oct approvals, plus Gem renaming 0314faa4. The drafts in `proposals/2026-10-09-retire-merge/` are based on the profile text as it read at about 9:05am.

## Governance records updated (Job 1)
- `phases.md` and `directory.md` were backed up to `*.bak-0909`, then updated at 9:09am. The update shows: 6 bots retired; Mediator in P2, live; `0314faa4` as the active P2 (ID) Inquirer; `e613112b` as the old Inquirer, superseded and awaiting Gem's decision. Active total: 17.
- Profile drafts, not applied: `proposals/2026-10-09-retire-merge/apply.json` and `README.md`.
- Gem's words: `approvals/2026-10-09-gem-direct-words.md`.
- 9:09:19am: the profile of the **old** Inquirer `e613112b` was rewritten with new Inquirer text (it appears to be inquirer-v002, now 3,907 bytes). The executor didn't do this. The **active** Inquirer `0314faa4` still runs the v001 text. If v002 was meant for the active Inquirer, it went to the superseded agent. Flagged to Explorer and Gem. apply.json's rename of `e613112b` would replace this text with a retirement brief.
