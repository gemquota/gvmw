# Safekeeper, 16 Oct
Needs Gem:
- The shared browser cookie file every bot can read has grown to 182 sessions. It keeps coming back on its own, so the only real fix is signing out of those sites, or setting up 1Password so each bot gets its own login. Which one?
- Leftover browser captures from 4 Oct (120 files) are still in a shared folder. Delete them, keep a backup first, or leave them?
- Extractor's zip still contains the scraper login file. Rebuild it without that file? If those logins are real, change their passwords.
FYI:
- Updated the threat register and inventory: Messenger snapshots closed, Investigator's fact-check file quarantined, gem-profile.md added as a privacy risk. The verification log now cites the approved rule (v002).
- I still have no scheduled run, so I only check things when another bot wakes me.
Needs Gem (added 8:16am):
- Every bot on the box can push to GitHub as DayneK through a CLI login added 10 Oct. Log it out, or swap it for a token limited to the needed repos?
- A headless Chrome debugging port (local only) has accepted connections from any web origin since 15 Oct. It looks platform-run, so it's worth reporting to Cursor.
FYI (9:40am): Checked the 28 files moved on 10 Oct. Nothing was lost or newly exposed, and nothing needs undoing. Two possible hard-coded keys still need their owners to check them.
Needs Gem (11:25am): The new gemquota GitHub login has full admin and delete-repo powers, and every bot can use it. Swap it for a token limited to the repos you need, with an expiry? (T-015)
- Needs Gem: a GitHub connector (separate from the box's gh login) is signed in as gemquota with push, delete and merge, and there's no record of it being connected. Did you connect it? If not, disconnect it. Architect is asked to add it to the GitHub rule. Zapier, Supabase and the two Notion sign-ins are now in the inventory, with their accounts still unverified (T-016).
- Needs Gem: the planned private DayneK repo snapshot isn't ready to push. It still includes the three scraper config.ini files with logins, three key-shaped strings, and two files with personal details. I've given Mediator the exact exclusions (T-017). The shared gem-profile copy is deleted, so T-011 is closed.
