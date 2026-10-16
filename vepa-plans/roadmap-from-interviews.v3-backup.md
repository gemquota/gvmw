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

# ROADMAP v3 (9 Oct) — built around the emergence ladder (Gem: "rebuild the roadmap around the emergence ladder")
Vision (SELF-STATED): particles fuse into protein-like structures, these grow into hunting clusters, then into cooperating metastructures, which fictionally awaken into agents with LLM brains that do the tribal, tech and human-like behaviour.
Honesty note: each rung is a designed rule the sim can reach, not hoped-for spontaneous emergence. Real consciousness is not claimed; awakening is a fictional game law.
Sub-items are SELF-STATED unless marked [suggested].

## A. Foundations
1. Foundations: typeable seed; per-feature toggles + cost meter + warning before heavy features; save format for multi-level state (molecules -> agents) [suggested]
2. Milestone 1, the first phone test: tribes + culture visible on today's groups (full spec above). It proves the social layer early, and later moves onto awakened agents.

## B. The emergence ladder (the spine)
3. Rung 1, molecules: tune bonding laws; stable-shape detector; molecule catalogue of shapes found [suggested]
4. Resources: spots deplete and regrow; food/minerals/energy; fought over; stored and traded; glowing patches. Placed early because structures need something to consume [suggested placement]
5. Rung 2, hunting clusters: bigger means more pull; absorb smaller clusters and particles; cluster identity persists [suggested]
6. Rung 3, metastructures: clusters dock by shape-fit; combined structure gains new abilities; can break apart [suggested]
7. Rung 4, awakening: fictional threshold (complexity, stability, memory); awakening is a highlight; the structure becomes an agent [suggested]
8. Rung 5, minds: cheap rule-based mind for every agent; LLM mind for about 20 named agents as a costed toggle (SELF-STATED)

## C. Agent life (agents, not raw particles, own all of this)
9. Follow one being: camera lock-on; life timeline; card with age/tribe/role/family; alerts on big moments; follow a child on death
10. Ageing: size/look change; young learn fast, elders slower; elders teach culture strongly; death of old age; only adults breed
11. Family trees: browse ancestors/descendants; tap to jump; traits + culture passed down; highlight famous lineages
12. Roles/jobs: emerge from behaviour; often inherited; tribe shifts roles by need; icon/colour; leaders emerge and get replaced
13. Names: auto-generated; from tribe language; family names passed down
14. Friendships/rivalries: form from repeated interactions; friends help, rivals fight; faint links; cross tribes; bonds/grudges inherited

## D. World
15. Seasons + day-night: seasonal growth; rest at night; breeding seasons; migration; lighting shift
16. Weather: rain boosts growth; storms scatter/harm; heat/cold drain energy; seek shelter; visible effects
17. Biomes: different resources; species adapt; own palette; shifting borders
18. Disasters: linked to weather/biome; lasting changes; toggle off

## E. Tech and building (order is Inquirer's, Gem said "your call")
19. Tools: trial and error; crafted from resources; boost gathering/building/fighting; wear out; spread through culture
20. Structures: shelters; walls; stores; decay into ruins; built together
21. Farming/taming: plant food spots; tame species; settle down; crop failure; discovered over time
22. Tech progression [suggested, Gem's answer pending]: emerges with no fixed tree; tribes differ; spreads by trade/war; discovery timeline
23. Settlements into towns [to be scoped]
24. Lost tech: dies with a tribe; ruins hold clues [suggested]

## F. Watching and coming back
25. Notable-moment detector: new species, extinctions, tribe events, anomalies, records, plus each ladder rung reached [suggested addition]
26. Return experience: text summary first, clips on tap; timeline markers; story feed; fast-forward

## G. Sharing, hosting, polish
27. Server worlds on credits: buy or earn (daily play, sharing, invites, milestones); 1% tick for 48 h then pause; at most about 3x cost
28. Sharing: gallery; challenges; leaderboards; shareable seeds; clips outside the game; likes and comments [to be scoped]
29. Quality of life: short tutorial; tooltips; simple mode with advanced hidden; text size + contrast; starter presets [to be scoped]
30. Art style + donation cosmetics (UI recolours)

## H. Backlog
Branch tree (on hold); self-models + measurable self-awareness markers; own language + translation; talking to beings; grief + revival; migrating beings between players; music
- Secret progression (9 Oct, SELF-STATED): Gem's concept is a secret progression from physics toy into an abstract high-fidelity civ sim. For new players: subtle hints that something more is possible (not fully hidden, no locked menus, not open).
- Hints: cryptic tooltips/law descriptions only. Lingering shapes, glows/sounds, rung teasers, lore lines NOT picked.
- Rung 1 molecule definition (Inquirer's call, Gem said 'your call'): holds its shape for a set time AND does something (stores energy, catalyses or moves). Self-copying is the bridge to Rung 2.
- Rung 2 hunting (all): bigger pull in smaller; actively chase prey; absorbing grows/strengthens; prey can dodge/break free; pack hunting.
- Rung 3 metastructures: shape-fit docking; break apart under stress; reproduce as a whole. Specialised parts + new abilities NOT picked.
- Rung 4 awakening trigger: size + structural complexity AND survives intact a long time AND enough memory. Inquirer's call on the rest: no random spark; it's a deterministic threshold so it's replayable from a seed; the threshold is tuneable in settings.
- Awakening on screen: brief glow/pulse; highlight + alert; named straight away; visibly acts with purpose. 'Subtle change only' NOT picked.
- Rung 5 rule-based minds (all): needs-driven (hunger, safety, social); learn from experience; copy successful neighbours; simple emotions steer choices; promotable to LLM mind when notable.
- LLM-mind promotion: tribe leaders; first to awaken in tribe/species; tech discoverers; long-lived elders. 'The one I follow' NOT picked.
- Towns (all): enough agents in one place; several structure kinds together; worn paths/roads; districts for farming, crafting, living; town gets a name.
- Sharing priority: world gallery first. (Note: a gallery needs server worlds/accounts, so it sits after item 27.)
- Gallery: browse + watch live; fork a world; sort by ladder rung reached. Featured/trending + private-by-default NOT picked.
- Challenges (all): reach a rung; tribe alive X generations; speed to a rung from a shared seed; weekly shared-seed challenge; constraint runs.
- QoL priority: simple mode with advanced settings hidden first. (Fits secret progression: simple surface, depth underneath.)
- Simple mode shows: starter preset picker; seed box; a few big sliders (gravity, energy); one button to reveal advanced. Play/pause-only NOT picked (implied present).
- Starter presets (all): primordial soup; head start (molecules formed); harsh world; peaceful; chaos (fictional laws up).
- Tutorial/tooltips: tutorial teaches physics toy only; higher-rung tooltips stay cryptic; clear help unlocks once a rung is reached; tutorial under 2 min. Skippable NOT picked.
- Leaderboards (all): fastest first awakening; longest lineage; biggest town; longest-running world; most tech discovered.
- Clip sharing (all): 10–30 s video; GIFs; story card + clip; watch link; seed included.
- Lost tech: ruins speed rediscovery; leftover tools findable and usable; flagged as highlight. 'Gone for good' NOT picked.
- Tech progression (all, SELF-STATED): emerges freely with no fixed tree; loose eras (stone/bronze/iron); tribes discover different tech; spreads via trade/conquest; viewable discovery timeline. Replaces the [suggested] tag on v3 item 22.

## v3 updates after the ladder set (9 Oct, SELF-STATED unless noted)
- Cross-cutting: secret progression. It looks like a physics toy, with cryptic tooltips as the only hint; the tutorial teaches physics only; clear help unlocks per rung reached.
- Item 3 Rung 1: a molecule = holds its shape for a set time + does something (Inquirer's call); self-copying bridges to Rung 2.
- Item 5 Rung 2: pull smaller in; chase; absorb to grow; prey can escape; pack hunting.
- Item 6 Rung 3: shape-fit docking; break apart under stress; reproduce as a whole.
- Item 7 Rung 4: needs size+complexity, long survival and memory; deterministic, tuneable threshold (Inquirer's call). On screen: glow/pulse, highlight + alert, named at once, acts with purpose.
- Item 8 Rung 5: rule minds = needs, learning, copying neighbours, simple emotions, promotable. LLM promotion: leaders, first awakened, inventors, elders (about 20 cap).
- Item 23 Towns: population; mixed structures; paths/roads; districts; named.
- Item 24 Lost tech: ruins speed rediscovery; leftover tools usable; highlight.
- Item 28 Sharing order: gallery first (needs server worlds). Gallery = watch live, fork, sort by rung. Challenges = rung, survival, speed, weekly seed, constraint runs. Leaderboards = fastest awakening, longest lineage, biggest town, oldest world, most tech. Clips = 10–30 s video, GIF, story card, watch link, seed.
- Item 29 QoL order: simple mode first (presets, seed box, few big sliders, reveal-advanced button). Presets: soup, head start, harsh, peaceful, chaos. Tutorial under 2 min. Text size/contrast stays.

## XL refinement set (10 Oct, SELF-STATED)
- Player role: set laws + seed then watch; small nudges like tweaking laws mid-run; beings can sense the player as a distant force. Pure observer NOT picked.
- Player as distant force: tribes form myths/religions about player; rituals to influence player; beliefs differ per tribe. Omens + awakened-only NOT picked.
- Law nudges: every nudge logged on timeline; disabled during challenges. No cooldown or size cap.
- Pacing soup->first awakening: under an hour to a few hours of play; faster with head-start preset. 'Days' + 'varies wildly' NOT picked.
- Rung indicator: cryptic glyph that changes per rung; rung name appears only once reached.
- Art style candidates: minimal abstract glowing particles; low-poly; cyberpunk neon. Pixel + shifts-by-rung NOT picked.
- ART STYLE DECIDED: minimal glowing particles with a cyberpunk neon palette. (Low-poly dropped as base.)
- Donation cosmetics: neon palette packs; UI recolours/themes; alternate rung glyph sets; supporter badge in gallery. Glow trails NOT picked.
- Seed: any text typed (hashed). Laws NOT included in seed (separate).
- Cost meter: estimated fps impact; battery drain estimate; bar of share of total budget; credit cost/hour on server worlds. Traffic light NOT picked.
- Save keeps: full world state at every level; seed + laws + nudge log (replayable); highlights + clips; family trees, names, histories. Small file size NOT required.
- Myths/religions (all): shrines/sacred structures; visible ritual gatherings; wars over beliefs; tap a tribe to read its myth about player; beliefs shift after law nudges.
- Rituals: picked 'purely flavour' AND 'request I can grant with a nudge' AND 'tiny real effect on laws' AND 'big rituals become highlights' (contradiction checked next).
- Rituals RESOLVED: mostly flavour, with a tiny real effect on laws; can show a request the player grants via nudge; big rituals become highlights.
- Fast-forward: offer to simulate all time away OR let player choose how far; only server worlds truly keep running, local ones pause. Cap NOT picked.
- Server world visibility: friends with a link; visitors watch only (no nudging). Public-in-gallery is opt-in via gallery publish.
- Detector ladder events (all): first stable molecule; first hunting cluster; first metastructure; every awakening; first myth/shrine; first town.
- Order after M1 (Inquirer's call): foundations first (seed, cost meter, save format), because the ladder needs multi-level saves and cost limits before it can run uncapped.
- Seasons + weather placed BEFORE awakening (pressure early life); move v3 items 15–16 up next to resources (item 4).
- Biomes + disasters also BEFORE awakening: whole World section (items 15–18) moves into the ladder, alongside resources.
- After awakening: interleave agent life and tech (e.g. follow-being + tools, ageing + structures, families + farming, roles + progression, names + towns, friendships + lost tech) [pairing suggested].
- Myths/religions placement (Inquirer's call): alongside roles and names, after awakening, since they need named tribes and leaders; shrines need structures first.
- Sharing placement (Inquirer's call): seeds + clip sharing early (cheap, no server, grows players, ready right after foundations); gallery + server worlds + leaderboards later (after agent life/tech, needs hosting + credits).
