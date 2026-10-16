# VEPA Roadmap v4 (full, hierarchical)
_Built from Gem's interview answers, 5–10 Oct 2026. Items marked (Inquirer's call) are where Gem said "your call"._

## Vision
- A secret progression: it starts as a physics toy and quietly becomes an abstract, high-fidelity civilisation sim
- The emergence ladder: particles → molecules → hunting clusters → metastructures → fictional awakening → minds → tribes, tech and culture
- Honesty: each rung is a designed rule, and awakening is a fictional game law, not real consciousness

## Cross-cutting principles
- **Look:** minimal glowing particles with a cyberpunk neon palette
- **Secret progression**
  - Cryptic tooltips and law descriptions are the only hints
  - A cryptic glyph changes per rung; the rung's name appears only once it's reached
  - The tutorial teaches the physics toy only; clear help unlocks per rung reached
- **Player role**
  - Sets the laws and seed, then watches
  - Can nudge laws mid-run; every nudge is logged on the timeline, and nudges are disabled during challenges
  - Beings sense the player as a distant force (see Myths and religions)
- **Performance**
  - A toggle per feature, with a cost meter and a warning before anything heavy
  - Limits enforced automatically when needed
- **Monetisation**
  - Nothing paywalled except ongoing costs (server hosting), at most about 3× cost
  - Donation-style cosmetics only, with no functionality behind them
  - Acceptable models: open source plus donations, hosting at a fair markup, selling tools, sponsorships or affiliates

---

## v1: The climb to awakening ("someone else plays it and gets it")

### 1. Milestone 1: tribes and culture visible on the phone
- **Done when:** in one 15-minute session at about 30 fps, a tribe forms on its own, a fight, trade or merge happens, and a culture-drift split happens
- 1a. civRuntime enabled behind one Tribes toggle with its cost shown (default on if the cost meter allows); keep the Civilisation stats panel
- 1b. Tribe visuals: a colour tint per tribe, soft territory halos, faint member lines (no labels)
  - Below 30 fps, simplify the halos first
- 1c. Culture spreading: members' colour shifts, symbol icons pop up and spread, a ripple when a being learns something
- 1d. Traditions: a child is born in the tribe's colour, with the parent's symbol icon on the child
- 1e. Fights: borders flash where they meet, beings rush and collide, losers flee or die
- 1f. Trade: glowing particles flow, the link line pulses, both tribes brighten
- 1g. Merge or absorb: colours blend (merge) or the absorber's colour spreads (absorb), with a burst of new member lines
- 1h. Drift split: the colour splits into two shades, member lines snap, the groups drift apart

### 2. Foundations
- 2a. Seed: any text you type
- 2b. Cost meter: estimated fps impact, battery drain, a bar showing share of the total budget, credits per hour on server worlds
- 2c. A toggle per feature, plus a warning before anything heavy
- 2d. Save format
  - Full world state at every level, from molecule to agent
  - Seed, laws and nudge log, so a run can be replayed
  - Highlights and clips
  - Family trees, names and histories

### 3. Simple mode and onboarding
- 3a. Simple mode by default: a starter preset picker, a seed box, a few big sliders (gravity, energy), one button to reveal advanced settings
- 3b. Starter presets: primordial soup, head start (molecules already formed), harsh world, peaceful, chaos
- 3c. Tutorial: under 2 minutes, physics toy only

### 4. Shareable seeds and clips
- 4a. Shareable seeds
- 4b. Clip sharing: 10–30 s video, GIFs, a story card with text plus the clip, a link others can open to watch, seed included

### 5. Rung 1: molecules
- 5a. A molecule counts when it holds its shape for a set time and does something (stores energy, speeds up reactions or moves) (Inquirer's call)
- 5b. Self-copying molecules are the bridge to Rung 2

### 6. World pressure (all before awakening)
- 6a. Resources
  - Food, minerals and energy
  - Spots run out and slowly regrow
  - Glowing patches on the map
  - Fought over; stored and traded between tribes
- 6b. Seasons and day-night
  - Resources grow more in some seasons
  - Rest at night, gather by day
  - Breeding seasons
  - Tribes migrate with the seasons
  - World lighting and colour shift
- 6c. Weather
  - Rain boosts growth
  - Storms scatter or harm beings
  - Heat and cold drain energy
  - Beings seek shelter
  - Visible rain, storm and heat effects
- 6d. Biomes
  - Different resources in each
  - Species adapt to their biome
  - Each has its own colour palette
  - Borders shift over time
- 6e. Disasters
  - Linked to weather and biome (e.g. floods in wet areas)
  - Leave lasting changes on the world
  - Can be switched off

### 7. Rung 2: hunting clusters
- 7a. Bigger clusters pull in smaller ones
- 7b. They actively chase prey
- 7c. Absorbing makes them grow and get stronger
- 7d. Prey can dodge or break free
- 7e. Several clusters can hunt together

### 8. Rung 3: metastructures
- 8a. Clusters dock when their shapes fit like puzzle pieces
- 8b. Can break apart under stress
- 8c. Can reproduce as a whole

### 9. Notable-moment detector
- 9a. General events: new species, extinctions and crashes, tribes forming, splitting or fighting, weird anomalies, records
- 9b. Ladder firsts: first stable molecule, first hunting cluster, first metastructure, every awakening, first myth or shrine, first town
- 9c. Also flags big rituals and lost tech

### 10. Return experience
- 10a. A text summary first, with clips on tap
- 10b. A timeline with markers you tap to jump to
- 10c. A story-style feed
- 10d. Fast-forward: simulate all the time away, or choose how far
- 10e. Local worlds pause; only server worlds keep running

### 11. Rung 4: awakening
- 11a. Trigger: enough size and structural complexity, surviving intact for a long time, and enough memory
- 11b. A fixed threshold with no random spark, so the same seed replays the same way; tuneable in settings (Inquirer's call)
- 11c. On screen: a brief glow or pulse, a highlight and alert, a name straight away, then it visibly acts with purpose

### 12. Rung 5: minds
- 12a. A rule-based mind for every agent: acts on needs (hunger, safety, social), learns from experience, copies successful neighbours, simple emotions steer choices
- 12b. LLM minds for about 20 notable agents, as a costed toggle (about US$0.43 an hour by Engineer's estimate)
  - Who gets one: tribe leaders, the first to awaken in a tribe or species, tech discoverers, long-lived elders
- 12c. Rule-based minds can be promoted to LLM minds

**v1 pacing target:** soup to first awakening in under an hour to a few hours of play, faster with the head-start preset

---

## v2: Agents build a civilisation (life and tech interleaved)

### 13. Following a being, plus tools
- 13a. Following a being: camera lock-on, a life-event timeline, a card with age, tribe, role and family, alerts on big moments, an offer to follow a child after death
- 13b. Tools: discovered by trial and error, crafted from resources, boost gathering, building or fighting, wear out, know-how spreads through culture

### 14. Ageing, plus structures
- 14a. Ageing: size and look change, young learn fast and elders slower, elders pass on culture more strongly, death of old age, only adults breed
- 14b. Structures: shelters from weather, walls defend territory, stores for lean seasons, decay into ruins when abandoned, built by several beings together

### 15. Family trees, plus farming and taming
- 15a. Family trees: browse ancestors and descendants, tap a relative to jump to them, see the traits and culture passed down, highlight long or famous lineages
- 15b. Farming and taming: plant new food spots, tame other species, farming makes tribes settle, crops fail in bad seasons, discovered over time

### 16. Roles and jobs, plus tech progression
- 16a. Roles: emerge from behaviour, often inherited, the tribe shifts roles by need, shown with an icon or colour, leaders emerge and can be replaced
- 16b. Tech progression: emerges freely with no fixed tree, loose eras (stone, bronze, iron), each tribe can discover different tech, spreads through trade or conquest, a discovery timeline you can view

### 17. Names, plus myths and religions
- 17a. Names: auto-generated, from the tribe's own language, family names passed down
- 17b. Myths and religions (Inquirer's call on placement)
  - Each tribe believes something different about the player
  - Shrines and sacred structures
  - Visible ritual gatherings
  - Wars over beliefs
  - Tap a tribe to read its myth about you
  - Beliefs shift after you nudge laws
  - Rituals: mostly flavour with a tiny real effect on the laws; can show a request you grant with a nudge; big rituals become highlights

### 18. Friendships and rivalries, plus towns
- 18a. Friendships and rivalries: form from repeated good or bad interactions, friends help and rivals fight, faint friend or rival links, can cross tribes, bonds and grudges pass to children
- 18b. Towns: enough agents in one place, several kinds of structures, worn paths and roads, areas for farming, crafting and living, the town gets a name

### 19. Lost tech
- 19a. Ruins let others rediscover it faster
- 19b. Leftover tools can be found and used
- 19c. Flagged as a highlight

---

## v3: Shared worlds

### 20. Server worlds on credits
- 20a. Credits can be bought or earned: daily play, sharing clips or worlds, inviting friends, hidden milestones
- 20b. When credits run out: 1% tick rate for a 48-hour grace period (about 29 minutes of server time), then pause and save; topping up resumes it
- 20c. Priced at most about 3× hosting cost
- 20d. Visibility: friends with a link; visitors can only watch

### 21. Gallery
- 21a. Browse and watch others' worlds live
- 21b. Copy a world and run your own version
- 21c. Sort by how far up the ladder a world got

### 22. Challenges and leaderboards
- 22a. Challenges: reach a rung, keep a tribe alive for X generations, fastest to a rung from a shared seed, a weekly shared-seed challenge, constraint runs (e.g. disasters on max)
- 22b. Leaderboards: fastest first awakening, longest lineage, biggest town, longest-running world, most tech discovered
- 22c. Comments and likes on shared worlds

### 23. Donation cosmetics
- 23a. Neon palette packs
- 23b. UI recolours and themes
- 23c. Alternate rung glyph sets
- 23d. A supporter badge in the gallery

### 24. Extra quality-of-life features
- 24a. Tooltips that explain things as you meet them (cryptic until each rung is reached)
- 24b. Adjustable text size and contrast

---

## Backlog
- Branch tree on Multiplex (on hold)
- Self-models with measurable self-awareness markers
- Own language plus a translation toggle
- Talking to beings
- Grief and revival
- Migrating beings between players (as exported "being cards")
- Reactive ambient music (Gem's own music stays separate)
