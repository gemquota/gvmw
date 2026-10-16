# VEPA roadmap (from Gem's interview answers) — v0, 5 Oct 2026
Status: draft, built up set by set. Sources: VEPA sets 1–4 (self-stated) + code check of /workspace/vepa v9.1.27.

## Phase 1 — Quick wins on what Gem already uses
- Typeable, reusable seed (replace hard-coded WORKER_SEED)
- Tappable branch tree on top of Chaos Multiplex
- Deeper analytics panels

## Phase 2 — Make the beings feel alive
- Switch on existing tribes/culture (civRuntime) and stabilise
- Real emotions and personality per being
- Richer memory (more than one number)

## Phase 3 — Coming back to a running world
- Short summary + replayable highlights on return
- Background running (peek-in play, 15–30 min sessions)

## Phase 4 — Look and money
- Pick art style (minimal / pixel / low-poly; undecided; painterly retracted)
- Paid cosmetic art styles (free with paid extras)

## Phase 5 — Minds
- Genuine self-models that could lead to emergence
- Self-awareness detector: alert Gem, flag highlight, protect the being
- Later ideas: low-cost LLM mind, own language + toggle translation, beings sense/talk to Gem, grief and revival

## Later / sharing
- Private first, then visit others' worlds, beings migrate between players
- Reactive ambient music
- Done for v1 = someone else plays it and gets it

## v1 suggested logical order (Inquirer, 5 Oct) — replaces phase order above pending Gem's OK
0. Foundations: typeable seed + performance budget for uncapped population on phone + save format that can hold richer being state
1. Event log / "notable moment" detector (feeds analytics, highlights, later self-awareness detector)
2. Beings: tribes/culture on -> richer memory -> emotions & personality
3. Branch tree on Multiplex (after being state is stable, so branches store the right data)
4. Return summary + highlights; catch-up simulation on return (phone browsers pause background tabs)
5. Art style decision -> paid cosmetic styles
6. Minds: self-models -> self-awareness detector (reuses step 1)
7. Later: LLM mind (cost-gated), language + translation, talking to beings, grief/revival, sharing, music
Issues found: uncapped population vs per-being emotions/memory/LLM cost; true background running not possible in a phone browser; cosmetics need a base art style first; highlights and detector share one event system.

## v1.1 Gem's refinements (5 Oct, self-stated) — v1 order confirmed "seems right"
- Performance: heavy features are toggleable, and limits are enforced automatically when needed (performance tiers).
- Persistent worlds run on a server, paid with credits. Credits can be bought, or earned slowly for free by engaging with and sharing the game.
- Pricing: nothing is paywalled except things with ongoing cost (server hosting), priced at most about 3x cost. Paid cosmetic styles are DROPPED; that answer was only the best option offered.
- Highlights are core. The self-awareness detector moves to the backlog.
- Free credits are earned from daily play time, sharing clips or worlds, inviting friends, and hidden milestones.
- When credits run out: pause and save; keep running at a 1% tick rate for a 48 h grace period (about 29 min of full-speed server time); then pause. Topping up resumes the world.
- The branch tree is on hold for now.
- Cosmetics: CONFIRMED allowed as small token purchases that are really donations, like UI recolours. No functionality behind them.
- Performance: per-feature toggles with a cost meter, and a warning before enabling anything heavy.

## v2 roadmap (5 Oct, after roadmap set 1)
1. FIRST PHONE MILESTONE: tribes and culture switched on and visible (civRuntime), with a basic performance budget
2. Foundations: typeable seed, per-feature toggles with cost meter + warning before heavy features, save format for richer being state
3. Notable-moment detector: new species, extinctions/crashes, tribes forming/splitting/fighting, weird anomalies, records
4. Return experience: text summary first with clips on tap, timeline markers to jump to, story-style feed; fast-forward on return
5. Beings: richer memory, then emotions and personality
6. Persistent server worlds via credits (buy or earn: daily play, sharing, invites, milestones); 1% tick for a 48 h grace period, then pause and save; priced at most about 3x cost
7. Art style decision; donation-style cosmetics such as UI recolours
8. Backlog: branch tree (on hold), self-models and self-awareness detector, LLM mind, language and translation, talking to beings, grief and revival, sharing and migration, music

## Tribes-milestone set (in progress, 5–6 Oct) — SELF-STATED
- See a tribe: colour tint per tribe, soft territory outlines/halos, faint lines linking members (no name labels).
- Culture means: shared behaviour habits, shared symbols/tokens, traditions passed to children, culture drift until tribes split.
- Tribe interactions: trade or share energy, fight over territory, merge or absorb.
- Tribes default: on if the device can handle it, per the cost meter.
- First phone milestone MUST include (all four): tribes visible (tint, halos, member lines); culture spreading (habits, symbols); trade/share, fight territory, merge/absorb; traditions passed to children.
- Done-bar for first phone milestone: about 30 fps on Gem's phone with all of that on.
- Below 30 fps: simplify territory halos first.
- Culture spreading on screen: members' colour shifts as they adopt it; small symbol icons pop up and spread; brief ripple when a being learns something.
- Territory fights on screen: borders flash/clash where they meet; beings visibly rush and collide; losers flee or die off (territory colour shifting to winner NOT picked).
- Trade/share on screen: glowing particles flow between tribes; a line between them pulses; both tribes brighten a little.
- Merge/absorb on screen: colours blend into one (merge); absorbing tribe's colour spreads over the other (absorb); burst of new member lines linking them. Halos joining NOT picked.
- Traditions to children on screen: child born already in tribe's colour; parent's symbol icon appears on the child.
- Culture split on screen: colour splits into two shades; member lines snap between halves; groups physically drift apart. Halo tearing NOT picked.
- Menus: one Tribes on/off toggle showing its cost; keep existing Civilisation stats panel. Per-visual toggles and tap-a-tribe info NOT picked for this milestone.
- Test pass criteria: within one 15-minute session on Gem's phone, Gem watches at least one tribe form on its own, sees a fight, trade or merge, and sees a tribe split from culture drift.

## Milestone 1 spec (9 Oct, SELF-STATED) — tribes and culture on and visible on phone
Done when: in one 15-minute session at about 30 fps on Gem's phone, a tribe forms unaided, a fight, trade or merge happens, and a culture-drift split happens.
Build pieces:
1a. Enable civRuntime behind one Tribes toggle with its cost shown (default on if the cost meter allows); keep the Civilisation stats panel.
1b. Tribe visuals: colour tint, soft territory halos, faint member lines. Halos are simplified first below 30 fps.
1c. Culture spread: member colour shifts, symbol icons pop up and spread, a ripple when a being learns.
1d. Traditions: child born in the tribe's colour, parent's symbol shown on the child.
1e. Fights: borders flash where they meet, beings rush and collide, losers flee or die.
1f. Trade: glowing particles flow, the link line pulses, both tribes brighten.
1g. Merge/absorb: colours blend (merge) or the absorber's colour spreads (absorb), with a burst of new member lines.
1h. Drift split: colour splits into two shades, member lines snap, groups drift apart.
Code note (code-verified): civRuntime already models federations (tribes) with fission/fusion, culture transmission parent-child and peer, and territory. It is gated by runtimeConfig.civRuntime=false. There is no tribe rendering yet.
- LLM mind (9 Oct, SELF-STATED): YES, but only for about 20 named beings, as a costed toggle (Engineer estimate ~US$0.43/h). Supersedes set 4. Stays after milestone 5 (beings).

## Expansion set (9 Oct, SELF-STATED)
- Broad areas wanted: world and environment; being life; tech and building; social and sharing; quality of life. Player powers NOT picked.
- World/environment wanted: weather (rain, storms, heat); seasons + day-night; depletable resources (food, minerals, energy spots); natural disasters (floods, quakes, meteors); biomes with different rules. Terrain NOT picked.
- Being life wanted (all): ageing + life stages (young/adult/elder); browsable family trees; roles/jobs (gatherer, builder, leader); names; friendships + rivalries; follow one being's life story.
- Tech/building wanted (all): crafted tools; structures (shelters, walls, stores); tech progression discovered over time; settlements growing into towns; farming/taming; tech lost when a tribe dies out.
- Social/sharing wanted (all): shared-world gallery; challenges (e.g. tribe alive 100 generations); record leaderboards; shareable seeds; share clips outside game; comments/likes.
- QoL wanted: short guided tutorial; tooltips as you meet things; simple mode default with advanced hidden; adjustable text size + contrast; starter world presets. Colour-blind palettes NOT picked.
- Priority: being life comes soonest after milestone 1.
- Being-life order: (1) follow one being's life story, (2) ageing + life stages, (3) family trees, (4) roles/jobs, (5) names, (6) friendships + rivalries.
- Follow one being (all): camera lock-on; life-event timeline; card with age, tribe, role, family; alert on big moments; offer to follow a child on death.
- Ageing (all): size/look change with age; abilities change (young learn fast, elders slower); elders pass culture more strongly; death of old age; only adults breed.
- Family trees: browse ancestors/descendants; tap a relative to jump to them; see traits + culture passed down; highlight long/famous lineages. Fading dead relatives NOT picked.
- Roles/jobs (all): emerge from behaviour; often inherited; tribe shifts roles by need; small icon/colour; leaders emerge and can be replaced.
- Names: auto-generated; from tribe's own language; family names passed down. Renaming + notable-only NOT picked.
- Friendships/rivalries (all): form from repeated good/bad interactions; friends help, rivals fight; faint friend/rival links; can cross tribes; grudges/bonds pass to children.
- World priority: resources first.
- Resources (all): spots deplete and slowly regrow; types food/minerals/energy; tribes compete/fight over rich spots; storable + tradeable between tribes; glowing patches on map.
- Seasons/day-night (all): seasonal resource growth; rest at night, gather by day; breeding seasons; seasonal tribe migration; lighting/colour shift.
- Weather (all): rain boosts growth; storms scatter/harm; heat/cold drain energy; beings seek shelter; visible rain/storm/heat effects.
- Biomes: different resources each; species adapt to biome; own colour palette; borders shift over time. Per-biome physics tweaks NOT picked.
- Disasters: linked to weather/biome; leave lasting changes; can be switched off. Random-rare, warning signs, always-highlight NOT picked.
- Tech order (Inquirer's logical order, Gem said 'your call'): tools -> structures -> farming/taming -> tech progression -> settlements to towns -> tech can be lost.
- Tools (all): discovered by trial and error; crafted from resources; boost gathering/building/fighting; wear out; know-how spreads through culture.
- Structures (all): shelters vs weather; walls defend territory; stores for lean seasons; decay into ruins if abandoned; built cooperatively.
- Farming/taming (all): plant new food spots; tame other species for food/work; farming makes tribes settle; crops fail in bad seasons/weather; discovered over time.
