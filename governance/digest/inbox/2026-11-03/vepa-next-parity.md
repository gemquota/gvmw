# VEPA Next super-parity assessment (revised)

**Date:** 2026-11-03 **16:24 AEST** (Australia/Brisbane)  
**Assessor:** P5 (Work) Engineer for Gem Quota  
**Correction (owner pt120u):** treat **`vepa-docs`** (not `vepa-archive`) as the documentation subject; treat **`vepa-consolidation` as supposed to hold ALL vepa versions** and inventory what it actually contains vs known versions.  
**Scope (read-only):** `vepa-next`, `vepa-consolidation`, `vepa-docs`, and main `vepa` (gemquota + DayneK + local). Archive noted only as a referenced recovery source, not as the docs subject.  
**Definition of super parity:** `vepa-next` does everything the union of **vepa + consolidation + docs** requires or provides, **plus more**.  
**Method:** Located repos under `/workspace` and GitHub (`gemquota` + `DayneK`). Cloned into `/workspace/tmp-vepa-assess/` (added `vepa-docs`). Read READMEs, registers, ledgers, feature catalog, trackers. Re-inspected consolidation branches/tags/releases/LFS/submodules/tarballs. Ran feasible test suites earlier in this assessment. Did **not** push, commit, merge, delete, deploy, or edit source repos. Secret/gitignored content named only.

---

## 0. Executive verdict (revised)

| Question | Answer |
|---|---|
| Is functional **super parity** confirmed? | **Not met** |
| Partly met? | **Yes, narrowly:** Pages serves a near byte-copy of `gemquota/vepa@9.1.2` from `rebuild/source-faithful-baseline`; `main` adds SIM-contract foundations the full app does not yet absorb; docs catalog many required families Next has not closed. |
| Against union of **vepa + consolidation + docs**? | **No.** Next lags DayneK/local **9.3.5**, fails 86 unit tests on the 9.1.2 copy, does not implement most docs feature families / roadmap phases P5–P8, and consolidation does **not** actually store the version corpus Gem expects. |

**Single most important ambiguity:** `gemquota/vepa-next` still has **two product trees**:

1. **`main`** — SIM foundation / 8-law sandbox (`vepa-next@0.1.0`). Contract tests **254/254 pass**.
2. **`rebuild/source-faithful-baseline` (PR #30, open)** — wholesale import of **`gemquota/vepa` 9.1.2**. `src/` identical to gemquota. Unit tests **784 pass / 86 fail**. Pages deploys **this** branch. Live: https://gemquota.github.io/vepa-next/

**Second critical finding (corrected scope):** `vepa-consolidation` is an **evidence ledger + markdown inventory**, not an all-versions store. It holds **zero** version tags, **zero** releases, **no** LFS, **no** submodules, **no** tarballs, and **only** `main`. It *references* a handful of pinned commits in prose/CSV; it does **not** contain those trees.

---

## 1. Locations and repository metadata

Times below are **Australia/Brisbane (AEST, UTC+10)**.

### 1.1 gemquota/vepa-next

| Field | Value |
|---|---|
| Local clones | `/workspace/tmp-vepa-assess/vepa-next` (`main`); `/workspace/tmp-vepa-assess/vepa-next-rebuild` (`rebuild/source-faithful-baseline`) |
| GitHub | https://github.com/gemquota/vepa-next — **public** |
| Default / last `main` | `main`; tip around deploy-workflow commit 2026-11-01 **21:01 AEST** (sandbox tree) |
| Open PRs | **#30** rebuild/source-faithful-baseline (updated 2026-11-01 **21:28 AEST**) |
| Deploy | Pages builds **rebuild** branch (`deploy-source-baseline.yml`); legacy Pages job disabled |

### 1.2 gemquota/vepa-consolidation

| Field | Value |
|---|---|
| Local clone | `/workspace/tmp-vepa-assess/vepa-consolidation` |
| GitHub | https://github.com/gemquota/vepa-consolidation — **private** |
| Default branch | `main` only (`origin/main`) |
| Last commit | `2100e4b` — 2026-10-21 **05:07 AEST** — “docs(audit): record 136-law semantic audit outcome” |
| Tags | **none** |
| Releases | **none** (API length 0) |
| LFS | **none** (`git lfs` not configured; no `.gitattributes` LFS rules) |
| Submodules | **none** (no `.gitmodules`) |
| Tarballs / binary version packs | **none** in tree |
| Repo size | GitHub `size` ≈ 69; local working tree ~656 KB including `.old/` ledger snapshots |
| Purpose (README) | “evidence ledger and controlled staging area… **not the production runtime**” |
| Open PRs | None |

### 1.3 gemquota/vepa-docs *(replaces archive as docs subject)*

| Field | Value |
|---|---|
| Local clone | `/workspace/tmp-vepa-assess/vepa-docs` |
| GitHub | https://github.com/gemquota/vepa-docs — **private** |
| Default branch | `main` |
| Last push | 2026-10-31 **12:19 AEST** |
| Branches | `main` + merged topic branches still listed: `docs/complete-lineage-migration-plan`, `docs/p0-p10-readiness-2026-10-31`, `docs/pin-lineage-source-snapshots`, `docs/readiness-refresh-2026-10-31b` |
| Tags / releases | **none** |
| DayneK copy | **Not found** as a DayneK-owned `vepa-docs` repo |
| Local related | `/workspace/vepa/exports/vepa-docs-concat.md` — generated VEPA4 docs concat from product tree (9.1.22-era stamp), **not** a clone of gemquota/vepa-docs |

### 1.4 Main vepa (fourth full subject)

| Tip | Location | Version signal |
|---|---|---|
| gemquota/vepa `master` | `/workspace/tmp-vepa-assess/vepa` | package **9.1.2**; tip `24b56af` (2026-10-15) |
| DayneK/vepa `main` | `/workspace/tmp-vepa-assess/daynek-vepa` | package **9.3.5**; tip `79efba7` (describe `v9.3.5-6-g79efba7`) |
| local | `/workspace/vepa` branch `codey/complete-plans` | package **9.3.5**; tip ahead of remote; **2087/2087** tests earlier |

Related (not primary subjects): `gemquota/vepa4`, `gemquota/vepa-v3`, `DayneK/v5`, `gemquota/vepa-archive` (recovery tarball), `/workspace/vepa-plans`.

---

## 2. What vepa-docs is

**Role:** Canonical **project-wide documentation system** for the VEPA family — SIM restructure, cross-version feature recovery, Roadmap v4 interpretation, test/release governance, and three static doc apps. It is **not** a runtime and not a version store of application trees.

**Structure:** Numbered authority tree:

- `00-governance/` — charter, decisions, glossary, assumptions/risks  
- `10-product/` — `ROADMAP_V4_INTERPRETATION.md`  
- `20-architecture/` — module catalog, event/state contracts  
- `30-domain-systems/` — physics and laws  
- `40-data-and-persistence/` — world save schema  
- `50-engineering/` — engineering plan, **feature catalog**, lineage migration plan, provenance, physics fidelity, stable baseline benchmark, testing/release, status reports  
- `60-operations/` — **master roadmap tracker**, deployment, status reports  
- `70-reference/` — documentation catalog, archive review, duplicate report, source-document archive index, manifests  
- `apps/{docs,report,roadmap}/` — three static HTML explorers  
- `.old/` — pre-refactor docs + **41 core markdown snapshots** from source repos (not full trees)

Root-level `FEATURE_CATALOG_*.md`, `MASTER_ROADMAP_TRACKER.md`, etc. are **compatibility pointers** to the numbered paths.

### Versions / lineages docs cover (pins and references)

| Line | How docs treat it |
|---|---|
| DayneK/vepa (~9.3.5, pin `625c82e…` in older register; later lineage pins refresh) | Leading baseline candidate |
| DayneK/v5 (`fa148ba…`) | Historical + UI/correctness rework source |
| gemquota/vepa (**9.1.2**, pins `355ae70…` then lineage `24b56af…`) | Stable / VEPA4 product root |
| gemquota/vepa4 (`c3fbb07…`) | Law/feature/test comparison (overlaps vepa) |
| gemquota/vepa-v3 (`ccd2285…`) | Architecture/spec; worker `Math.random()` hazard |
| gemquota/vepa-next | Target; SIM contracts + 136-law catalog |
| gemquota/vepa-archive | Recovery-only tarball; integrity pending |
| gemquota/vv | Empty — no features |

Docs do **not** claim to embed every historical tag from gemquota’s long 4.x–9.1.x or DayneK 9.1.3–9.3.5 tag lists; they pin **heads/commits** for migration evidence.

### Documented feature / spec families (parity checklist inputs)

From `50-engineering/FEATURE_CATALOG_AND_MIGRATION_MAP.md` (KEEP/ADAPT/MERGE vocabulary). These are **required checklist rows** for Next super parity against docs:

1. Particle state / typed buffers (canonical stride/schema)  
2. Physics laws + law categories (one authoritative manifest; 136-law lineage)  
3. Spatial acceleration (grid + octree/FMM gravity separation)  
4. Contact/collision constraints (DayneK resolver adapted; residual penetration acknowledged)  
5. Randomness / seed (versioned injectable PRNG; ban ambient `Math.random`)  
6. World configuration transactions (session validates commit/reject/rollback)  
7. Species / DNA / genetics  
8. Intelligence engines (insight, narrative, lineage, goal, timeline)  
9. Communication / predation  
10. Chaos / multiplex  
11. Molecules / clusters / metastructures (roadmap rungs 0–3)  
12. Awakening / minds (+ optional LLM adapter)  
13. Resources / ecology  
14. Tribes / culture / technology  
15. Persistence / world saves (versioned schema, atomic recovery)  
16. History / highlights / replay  
17. UI / renderer (state-faithful projection)  
18–26. **V5 rework behaviors:** dead-law detection, WRAP restore, shared selection, SAVES/presets repair, narrative/analytics, law-grid search/bulk, backend-setting precedence  
27. Setup / presets / progressive help  
28. Performance / benchmarks  
29. Fidelity policy / backend capability  
30. Build / docs / generated exports drift control  
31. Hosting / privacy  

**Roadmap phases (master tracker):** P0–P4 partial on Next; **P5–P8 planned** (emergence, minds, resources/tribes, product setup); P9 docs apps initial; P10 release gates open. Tracker last coordinated update **2026-10-21**; lineage readiness refresh **2026-10-31**.

---

## 3. What vepa-consolidation actually contains vs “all versions”

### 3.1 Artifact inventory (what is physically in the repo)

| Artifact class | Present? | Detail |
|---|---|---|
| Branches | **`main` only** | No version branches, no `v9.*` branches |
| Tags | **None** | `git tag -l` empty; API tags empty |
| GitHub Releases | **None** | |
| Git LFS | **None** | |
| Submodules | **None** | |
| Tarballs / zips of vepa trees | **None** | Archive integrity doc *points at* `gemquota/vepa-archive` tarball elsewhere; not stored here |
| Runtime / `package.json` | **None** | Markdown + CSV only |
| `MIGRATION_LEDGER.csv` | **Yes (38 rows)** | Sources: **31 `new-authored`**, **7 `DayneK/vepa@625c82e…`**; destinations mostly `vepa-next`, 5 rows → `vepa-docs` |
| `.old/ledger/2026-10-16/*` | **Yes** | Historical CSV snapshots of the same ledger evolution |
| Prose registers | **Yes** | `SOURCE_REGISTER.md`, `SOURCE_INVENTORY.md`, `ADDITIONAL_REPOSITORY_REVIEW.md`, V5 docs, `LAW_AUDIT_136_SUMMARY.md`, `SIM_REFACTOR_POLICY.md`, `ARCHIVE_INTEGRITY_CHECK.md` (status: **pending**, tarball not downloaded in that session) |

**Contained as stored version trees: none.**  
**Contained as documented pin references (prose only):**

| Referenced source | Observed pin (register) | Version signal |
|---|---|---|
| DayneK/vepa | `625c82e90e771777b92897aa23dcb957e98c714a` | package **9.3.5** (README mismatch noted historically) |
| DayneK/v5 | `fa148baf57a7f006bbfc5e47be435212145cb574` | historical ~9.3.1 era |
| gemquota/vepa | `355ae700558590c2c7a905e43a6bdb7b16d5dc75` | **9.1.2** |
| gemquota/vepa4 | `c3fbb0795b691e9a43e9f66a8982882bbc11880a` | overlaps 9.1.2 |
| gemquota/vepa-v3 | `ccd2285ddf241c3d1ee2f6ebb4c8eea81824d973` | v3 line |
| gemquota/vepa-archive | `917a286…` | pre-v4 tarball **in another repo** |
| gemquota/vv | empty | — |

Ledger **does not** pin or migrate blobs from gemquota/vepa, vepa4, v3, or archive — only DayneK contact/spatial slices + new-authored SIM modules.

### 3.2 Known version universe (for “missing” comparison)

| Source of truth | What exists |
|---|---|
| **gemquota/vepa tags** | **47 tags**, including `v9.1.1` … `v9.0.0`, long `v8.*` / `v7.*` / `v4.6.*` history, `v4-architecture-roadmap`. **Note:** tip package is **9.1.2** but there is **no `v9.1.2` tag** in the tag list inspected. |
| **DayneK/vepa tags** | **12 tags:** `v9.1.3`, `v9.1.22`–`v9.1.27`, `v9.2.0`, `v9.3.0`, `v9.3.3`, `v9.3.4`, `v9.3.5` |
| **local `/workspace/vepa`** | Branch `codey/complete-plans` @ **9.3.5**; tags mirror DayneK 9.1.3–9.3.5; CHANGELOG maps **4.9.x → 9.x** through **9.3.5** (and back through 9.1.2, 9.0.0, 8.16.x, …) |
| **DayneK `main` HEAD** | `v9.3.5-6-g79efba7` (6 commits past tag) |

### 3.3 Missing from consolidation relative to that universe

If consolidation is supposed to **hold ALL vepa versions**, it is missing essentially the entire corpus:

- **All 47 gemquota/vepa tags** (and the untagged **9.1.2** tip tree)  
- **All 12 DayneK/vepa tags** and post-tag `main` / `codey/complete-plans` tips  
- **Full CHANGELOG lineage** (9.3.5 … 9.0.0 … 8.x … 4.6.x) as stored trees  
- **Full clones or mirrors** of DayneK/v5, gemquota/vepa4, gemquota/vepa-v3, archive tarball  
- **Any** branch-per-version, tag, release asset, LFS object, or submodule pointer that would make those versions recoverable **from consolidation alone**

What it **does** hold: migration **metadata** and a thin ledger of SIM slices already moved toward Next/docs.

**Verdict on consolidation’s “all versions” claim:** **Not satisfied.** Repo is a ledger/register, not a version vault.

---

## 4. Purpose and structure (subjects)

### 4.1 vepa-next

Unchanged dual identity from prior pass: `main` = SIM sandbox; `rebuild` = gemquota 9.1.2 app (Pages). Own `README_CAPABILITY_GAP_AUDIT.md` admits incomplete stable parity.

### 4.2 vepa-consolidation

Evidence ledger only (see §3). Incomplete checklist in its README: full file-level comparison, archive verify, stable/candidate baselines, migrate runtime slices, verify docs web apps.

### 4.3 vepa-docs

Canonical docs + trackers + feature catalog + three apps (see §2). Implementation status is **evidence-gated** and still mostly partial/planned for roadmap product features.

### 4.4 Main vepa

Full VEPA4 app. gemquota **9.1.2** (784/86 fail on current tests). DayneK/local **9.3.5** green (**1592** / **2087** tests). Local ahead with restart staging, system variants, multiplex pool, civ/relationship, etc.

---

## 5. Test and build results (executed this assessment; unchanged)

| Subject | Result |
|---|---|
| vepa-next `main` | **254/254** pass; `npm run check` pass |
| vepa-next rebuild / gemquota/vepa | **784 pass / 86 fail**; build pass → `.dist/` |
| DayneK/vepa `main` | **1592/1592**; build pass → `dist/` |
| local `/workspace/vepa` | **2087/2087** |
| consolidation / docs | N/A (docs; docs app static check historically green in docs CI) |

---

## 6. Feature inventory — union checklist (vepa ∪ consolidation ∪ docs)

Legend: Next status evaluates **both** tips (`main` / `rebuild`). Docs rows are from the feature catalog + tracker.

### 6.1 Docs feature families → Next

| Family (docs) | Next `main` | Next `rebuild`/Pages | Notes |
|---|---|---|---|
| Particle typed buffers / stride | Partial prototype | Present (gemquota copy) | Canonical layout migration unfinished |
| 136-law manifest + categories | Catalog + **8** executable | Source present; tests fail (128↔136 drift) | Docs: one authoritative manifest required |
| Spatial grid / FMM / octree | Grid + contact slice | Full solver paths in source | Stable-vs-next perf unproven |
| Contact constraints | Adapted + tests | In source | Docs residual-penetration hazard |
| Seeded PRNG / ban Math.random | Contract PRNG | Stable PRNG in source | v3 hazard must not be reintroduced |
| World-session transactions | **Present** (contracts) | Legacy paths; not SIM session | Docs require single authoritative boundary |
| DNA / species | Missing runtime | Source present | |
| Intelligence engines ×5 | Missing | Source present | |
| Communication / predation | Missing | Source present | |
| Chaos multiplex | Missing | Source present | DayneK richer |
| Molecules / clusters / meta (P5) | Missing | Partial/legacy only | Docs **planned** |
| Awakening / minds / LLM (P6) | Missing | Missing as docs-complete | **Planned** |
| Resources / ecology (P7) | Missing | Ecology present in stable; docs want accounting contracts | Partial vs docs bar |
| Tribes / culture / tech (P7) | Missing | Partial in stable | |
| Saves / replay / journal (P4) | Partial contracts + UI | Stable saves; not SIM replay suite | Docs: worker+session coordination open |
| UI / renderer fidelity | Minimal sandbox | Full panels | V5 selection/SAVES behaviors not fully SIM-merged |
| V5 rework behaviors (dead-law, WRAP, selection, presets, narrative, law-grid, backend precedence) | Partial mapping docs | Not DayneK/V5-complete | Consolidation `V5_REWORK_*` |
| Setup / presets / progressive help (P8) | Partial seed/save | Presets in source; DayneK launch/help ahead | |
| Benchmarks / fidelity policy | Missing / isolated policy | Bench scripts in source | Paired stable-vs-next open |
| Docs apps (P9) | N/A (live in vepa-docs) | N/A | Next not the docs host; apps real-browser smoke still pending per tracker |
| Hosting / privacy (P10) | Pages for rebuild | Config in tree | Docs release gates open |

### 6.2 Consolidation process outcomes → Next

| Capability | Consolidation | In Next |
|---|---|---|
| Multi-repo source register | Present (prose) | Partial docs/planning |
| File-level ledger complete | **Incomplete** (38 rows, mostly new-authored) | Not fully executed |
| Archive integrity verified | **Pending** | Not done |
| All-version store | **Missing** (see §3) | N/A — Next is not a version vault either |
| Runnable donor | None | Next has runtime (dual tips) |

### 6.3 Main vepa runtime → Next (summary)

| Bar | Met? |
|---|---|
| gemquota 9.1.2 **source** on rebuild | ≈ Yes (`diff -rq` clean earlier) |
| gemquota 9.1.2 **tests** | **No** (86 fail) |
| DayneK/local 9.3.5 features + green suite | **No** (rebuild behind; main sandbox far behind) |
| SIM “plus more” shipped inside full app | **No** (lives on `main`, not integrated into Pages app) |

### 6.4 Extras on Next beyond the union (candidates for “plus more”)

SIM world-session / transaction / event journal / replay / snapshot-store; energy ledger numerics; law command/manifest/registry split; stable-law inventory dispositions; v3 migration adapters; capability-gap audit docs; dependency-free MVPs; Pages under `/vepa-next/`. **Most are sandbox-only today.**

---

## 7. Revised verdict, gaps, fixes

### Verdict: **Super parity not met** against the union of vepa + consolidation + docs

- **vs docs:** Next has started P1–P4 SIM/physics/save slices but has **not** closed the documented feature catalog or phases P5–P8; even P3/P4 remain partial vs tracker evidence rules.  
- **vs consolidation:** Next is the intended runtime destination, but consolidation’s verification programme is incomplete — and consolidation itself **fails** the owner expectation of holding all versions. Super parity cannot lean on consolidation as a complete recovered corpus.  
- **vs gemquota 9.1.2:** rebuild ≈ source copy, **not** proven test/behavior parity.  
- **vs DayneK/local 9.3.5:** **behind**.  
- **Plus more:** SIM contracts are real, but **not integrated** into the deployed full app → do not yet count as shipped super-parity.

### Gaps ranked (revised)

1. **Dual-branch identity (`main` vs rebuild Pages app)** — Critical — unify tip; align CI with tree. **Size: L**  
2. **Behind DayneK/local 9.3.5** — Critical for vepa bar — re-pin and port restart/variants/multiplex/civ/Pixi paths; target 1592–2087 green. **Size: XL**  
3. **Docs feature-catalog / P5–P8 product families unimplemented** — Critical for docs bar — vertical slices per family with fixtures. **Size: XL**  
4. **86 failing tests on 9.1.2 rebuild** — High — fix 128→136 / aliases / DNA-field audits; gate PR #30. **Size: M**  
5. **SIM contracts not absorbed into full runtime** — High — wire session/energy/replay into worker+UI. **Size: L–XL**  
6. **Consolidation is not an all-versions store** — High (governance) — either ingest mirrors/tags/tarballs/LFS intentionally, or rewrite the charter so “all versions” lives in named source repos + archive, with consolidation remaining ledger-only. **Size: M docs / XL if vaulting**  
7. **Browser E2E / COOP-COEP / paired benchmarks unverified** — High — **Size: M–L**  
8. **Archive integrity + lineage L0 tree compares still open** (docs/consolidation) — Medium — **Size: M**  
9. **Open gemquota fix PRs (#5–#9) not in rebuild pin** — Medium — **Size: S–M**

---

## 8. Ambiguities and limits

- Which tip is “vepa-next”? Pages ≠ `main`.  
- Which vepa tip is authoritative for parity? Consolidation preferred DayneK; rebuild pinned gemquota 9.1.2; local is further ahead.  
- Consolidation “should hold all versions” vs README “ledger not runtime” — owner intent conflicts with current repo design; this report measures **actual contents**.  
- Archive still not treated as the docs subject; its tarball integrity remains pending in consolidation’s checklist.  
- E2E/browsers not run this pass; Pages HTML previously fetched (200, VEPA4 title).  
- Secret/gitignored: named only (`node_modules/`, `test-results/`).

---

## 9. Artifact index

- Clones: `/workspace/tmp-vepa-assess/{vepa-next,vepa-next-rebuild,vepa-consolidation,vepa-docs,vepa-archive,vepa,daynek-vepa}`  
- Local: `/workspace/vepa` (`codey/complete-plans`), `/workspace/vepa/exports/vepa-docs-concat.md`  
- Logs: `vepa-next-main-test.log`, `rebuild-test.log`, `rebuild-build.log`, `daynek-test.log`, `gemquota-vepa-test.log`, `local-vepa-test.log`  
- This report: `/workspace/governance/digest/inbox/2026-11-03/vepa-next-parity.md`
