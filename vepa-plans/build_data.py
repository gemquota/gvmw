#!/usr/bin/env python3
"""Builds items.json for the VEPA plans catalogue. Evidence was gathered against
/workspace/vepa @ 436afd2 (v9.1.27) on 2026-10-02 (AEST)."""
import json, subprocess, os
REPO = '/workspace/vepa'
MOVED = {  # original path -> reason
 'docs/11-26-Audit/01-consolidated-audit-dialogue.md': 'Historical 9.1.4 audit-conversation reconstruction (2026-09-16). Its 12-step plan became AUDIT_REMEDIATION_PLAN.md (declared closed at 9.1.22) and its open items are carried by ARCHITECTURAL_RESOLUTION_MATRIX.md / FEATURE_STATUS_MATRIX.md.',
 'docs/11-26-Audit/02-message-answer-matrix.md': 'Historical 9.1.4 message-to-answer matrix; missing-answer register superseded by ARCHITECTURAL_RESOLUTION_MATRIX.md and BACKEND_ENVELOPES.md (open items preserved in the catalogue).',
 'docs/11-26-Audit/03-full-audit-answer-set.md': 'Historical 9.1.4 answer set; "technically open" list superseded by ARCHITECTURAL_RESOLUTION_MATRIX.md (open items preserved in the catalogue).',
 'docs/11-26-Audit/04-pasted-audit-baseline.md': 'Frozen 9.1.3 pasted audit (897 tests, commit a9f3103). Self-declares as a historical snapshot; its critical/high findings are resolved or tracked elsewhere.',
 'docs/CIVILIZATION-EXPANSION-REPORT-2026-09-30.md': 'Superseded by CIVILIZATION-SEQUEL-PLAN-2026-09-30.md (its own §7 addendum says so); phases 1-6 are done or carried forward, test counts (987) are stale.',
 'docs/dev/rrp-trilogy/intent.md': 'E·F·A trilogy design (2026-08-18). All three sets shipped (v8.2.0-v8.4.0); modules + tests present.',
 'docs/dev/rrp-trilogy/mermaid.md': 'Diagram companion of the completed E·F·A trilogy design.',
 'docs/dev/rrp-trilogy/traceability.md': 'Traceability matrix of the completed E·F·A trilogy design.',
 'docs/dev/rrp-trilogy-2/intent.md': 'D·G·H trilogy design (2026-08-18). All three sets shipped (v8.6.0-v8.8.0); modules + tests present.',
 'docs/dev/rrp-trilogy-2/mermaid.md': 'Diagram companion of the completed D·G·H trilogy design.',
 'docs/dev/rrp-trilogy-2/traceability.md': 'Traceability matrix of the completed D·G·H trilogy design.',
 'docs/dev/rrp-trilogy-3/intent.md': 'I·J·K trilogy design (2026-08-18). All three sets shipped (v8.9.0-v8.11.0); modules + tests present.',
 'docs/dev/rrp-trilogy-3/mermaid.md': 'Diagram companion of the completed I·J·K trilogy design.',
 'docs/dev/rrp-trilogy-3/traceability.md': 'Traceability matrix of the completed I·J·K trilogy design.',
 'docs/dev/rrp-trilogy-4/intent.md': 'L·M·N trilogy design (2026-08-19). All three sets shipped (v8.12.0-v8.14.0); modules + tests present.',
 'docs/dev/rrp-trilogy-4/mermaid.md': 'Diagram companion of the completed L·M·N trilogy design.',
 'docs/dev/rrp-trilogy-4/traceability.md': 'Traceability matrix of the completed L·M·N trilogy design.',
 'LAW_COMPENDIUM.md': 'Snapshot of VEPA 9.1.10 (records 88 files / 870 tests). Superseded by the generated, spec:check-guarded law records under docs/spec/laws/. Not referenced by any script, test or build.',
}

D = []  # documents
def doc(path, dtype, date='', version='', cls='current', reason='', files=1, note=''):
    rec = dict(path=path, type=dtype, date=date, version=version, classification=cls,
               reason=reason, fileCount=files, note=note)
    if path in MOVED:
        rec['classification'] = 'outdated-moved'; rec['reason'] = MOVED[path]; rec['movedTo'] = '.old/' + path
    D.append(rec)

# ---- Root
doc('README.md','readme','', '9.1.27','current','Project README — always kept.')
doc('AGENTS.md','agent-instructions','2026-09-23','9.1.22','outdated-retained','Content is stale (header 9.1.22, HEAD d2f9aa5, 860 tests, references to non-existent audit-suite/, LAW_COUNT 128), but it is the canonical agent entrypoint auto-loaded by agent tools; refresh rather than archive.')
doc('GEMINI.md','agent-instructions','2026-08-10','','current','Project mandates auto-loaded by Gemini agents; minor stale audit-suite/ references.')
doc('CHANGELOG.md','changelog/ledger','2026-10-01','9.1.27','current','Read by scripts/check-repository.mjs (version/changelog sync) — must stay.')
doc('PLAN.md','plan','2026-09-23','9.1.22','outdated-retained','Status "Complete" and all items done, but linked from README.md "Docs" and named in AGENTS.md §7/§10.1 SSOT mandates; retained to avoid breaking README/agent workflow.')
doc('SPEC.md','spec','2026-09-23','9.1.22','outdated-retained','Goals all met; acceptance/test counts stale (951 vs 1431). Linked from README.md "Docs" and AGENTS.md SSOT table; retained.')
doc('GUIDE.md','user-guide','','v8.x sections','current','User-facing design guide (not a plan); one dead link to docs/expansion/.')
doc('LAW_COMPENDIUM.md','reference','','9.1.10')
doc('src/physics/lawgroups/SPEC.md','spec/contract','','','current','Read by tests/unit/provenance.test.js and exports/generate-docs-concat.mjs; linked by generate-spec.mjs output.')
doc('exports/README.md','readme','','','current','Inside the provenance-validated exports/ tree.')
doc('exports/vepa-*-concat.md (2 snapshots)','derived snapshot','2026-08-14','7.0.0-draft','outdated-retained','Listed in exports/provenance.json + publication-plan.json and checked by tests/unit/batch5Reports.test.js; stale content (generated 2026-08-14) but must not move.',2)
# ---- docs/ top level
doc('docs/11-26-Audit/01-consolidated-audit-dialogue.md','audit','2026-09-16','9.1.4')
doc('docs/11-26-Audit/02-message-answer-matrix.md','audit','2026-09-16','9.1.4')
doc('docs/11-26-Audit/03-full-audit-answer-set.md','audit','2026-09-16','9.1.4')
doc('docs/11-26-Audit/04-pasted-audit-baseline.md','audit','2026-09-16','9.1.3')
doc('docs/A9-MIGRATION-PLAN.md','plan','2026-09-30','9.1.22','current','Open (A9 not started); referenced by tests/unit/lawsSingleton.test.js.')
doc('docs/ARCHITECTURAL_RESOLUTION_MATRIX.md','status-matrix','','9.1.22','current','Live tracker of technically-open items.')
doc('docs/AUDIT_CORPUS_OWNERSHIP.md','policy','','9.1.3','current','Active ownership policy for docs/audit (no deletion/relocation); deferred decisions still open.')
doc('docs/AUDIT_REMEDIATION_PLAN.md','plan','','9.1.21','current','Program declared closed at 9.1.22, but several acceptance criteria remain partial; cited by scripts/validate-signoff.mjs header and BACKEND_ENVELOPES.md.')
doc('docs/BACKEND_ENVELOPES.md','report','','9.1.22','current','Referenced by src/state/lawOntology.js and tests/unit/fmmParity.test.js.')
doc('docs/CIVILIZATION-EXPANSION-REPORT-2026-09-30.md','report','2026-09-30','9.1.22')
doc('docs/CIVILIZATION-SEQUEL-PLAN-2026-09-30.md','plan/report','2026-09-30','9.1.22','current','Holds the open A9-A12 carry-forward list and proxy boundaries; linked from docs/systems/implementation-gaps.md.')
doc('docs/CODEBASE-AUDIT-2026-09-30.md','audit','2026-09-30','9.1.22','current','Referenced from source comments (src/core/numeric.js, clipboard.js, dna/codec.js, physics/force.js, laws.js, render/zeroCopy.js, ui/analyticsPanel.js); A9-A12 still open.')
doc('docs/DECOMPOSITION_PLAN.md','proposal','','9.1.22','current','Proposed, awaiting confirmation; only P3 executed.')
doc('docs/DEEP_AUDIT_CLARIFICATIONS.md','audit','','9.1.3','outdated-retained','9.1.3 clarification superseded by FEATURE_STATUS_MATRIX/BACKEND_ENVELOPES, but linked from README.md (line 117) and SPEC.md header; retained.')
doc('docs/EXPORT_SNAPSHOT_POLICY.md','policy','','9.1.3','outdated-retained','Table is stale (still lists the retired vepa-codebase-full-concat.md) and superseded by exports/provenance.json + publication-plan.json, but linked from exports/README.md (provenance-covered tree); retained.')
doc('docs/FEATURE_STATUS_MATRIX.md','status-matrix','','9.1.22','current','Live feature-status record.')
doc('docs/LEGACY_TOOLING_INVENTORY.md','policy/inventory','','9.1.3','current','Active retention policy (cited by CODEBASE-AUDIT §6.3); accurate.')
doc('docs/MECHANICS_CONSUMER_MATRIX.md','status-matrix','','9.1.22','current','Read by tests/unit/backendArchitecture.test.js — must stay.')
doc('docs/RENDERER_BENCHMARK_REPORT.md','report','2026-09-23','9.1.21','current','Current benchmark report (results artifact in bench/results).')
doc('docs/REPOSITORY_HYGIENE.md','policy','','9.1.3','current','Active ownership/hygiene policy; one deferred decision open.')
# ---- docs/dev
doc('docs/dev/interaction-space.md','architecture','','','current','Describes the live interactionSpace registry.')
doc('docs/dev/law-relationship-architecture.md','roadmap','','','current','10-roadmap sequence; only 1-2 done.')
for t in ['rrp-trilogy','rrp-trilogy-2','rrp-trilogy-3','rrp-trilogy-4','rrp-trilogy-5','rrp-trilogy-6']:
    for f in ['intent','mermaid','traceability']:
        p=f'docs/dev/{t}/{f}.md'
        if t=='rrp-trilogy-5': doc(p,'design-spec','2026-08-19','v8.15-8.17','current','O and P shipped; Set Q (cosmology) not started.')
        elif t=='rrp-trilogy-6': doc(p,'design-spec','2026-08-19','v8.18-8.20','current','R·S·T not started.')
        else: doc(p,'design-spec','2026-08-18' if t!='rrp-trilogy-4' else '2026-08-19','')
# ---- docs/systems (published by `npm run build` via scripts/publish-system-atlas.mjs)
SYS_NOTE='docs/systems/ is copied wholesale into dist/ by scripts/publish-system-atlas.mjs (npm run build) and bundled by scripts/generate-systems-bundle.mjs.'
for f,t in [('README.md','index'),('overview.md','analysis'),('implementation-gaps.md','gap analysis'),('module-decomposition.md','proposal'),('meta-model.md','design'),('ontology.md','design'),('analysis-framework.md','design'),('comparison-matrix.md','analysis'),('deployment-publication.md','ops'),('roadmap-overview.md','roadmap'),('assessment-20260920.md','review ledger')]:
    doc('docs/systems/'+f,t,'2026-09-20' if 'assessment' in f else '', '9.1.15' if f in('implementation-gaps.md','assessment-20260920.md') else ('9.1.21' if f=='roadmap-overview.md' else ''),'current',SYS_NOTE)
doc('docs/systems/complete-atlas.md','generated bundle','2026-09-21','','current','Generated by npm run systems:bundle; '+SYS_NOTE)
doc('docs/systems/ui-module-report.md','generated report','','','current','Checked by npm run report:ui:check inside repository:check — must stay.')
SYSTEMS=['family-kinship','group-tribe-clan','mating-reproduction','nation-polity','civilization','culture-memory','relationship-laboratory','synthetic-society','ecology','economy-governance','infrastructure','species-lineage']
for s in SYSTEMS: doc(f'docs/systems/roadmap-{s}.md','roadmap','','9.1.21','current',SYS_NOTE)
doc('docs/systems/roadmaps/ (README + 48 A–D variants)','roadmap variants','2026-09-21','9.1.21','current','Variants are scheduled by src/state/systemVariants.js; '+SYS_NOTE,49)
doc('docs/systems/roles/ (README + 11 role files)','role catalogue','','','current',SYS_NOTE,12)
doc('docs/systems/past/0/ (5 archived copies)','archive','2026-09-20','pre-9.1.15','outdated-retained','Already an archive of superseded atlas files, but published by the build (publish-system-atlas copies docs/systems/ recursively); moving would change dist/ output.',5)
# ---- audit / spec
doc('docs/audit/laws/a3/ roll-ups (audit_progress, all_stage_*, category docs, mega ensemble)','audit','','128-law era','outdated-retained','Historical (128-law registry) but covered by docs/audit/provenance.json, required by validate-provenance (repository:check) and scanned by scripts/generate-spec.mjs (spec:check) — must not move.',15)
doc('docs/audit/laws/a3/stage-1/ (128 per-law reports)','audit','','128-law era','outdated-retained','Provenance-manifest record + spec generator input; moving breaks repository:check/spec:check.',128)
doc('docs/audit/laws/a3/stage-2/ (128 per-law proposals)','audit','','128-law era','outdated-retained','Provenance-manifest record + spec generator input.',128)
doc('docs/audit/laws/a3/stage-3/ (128 per-law sign-offs)','audit','','128-law era','outdated-retained','Provenance-manifest record + spec generator input; sign-off prose superseded by docs/spec/audit/signoff-manifest.json.',128)
doc('docs/audit/provenance.json','provenance manifest','','','current','Validated by scripts/validate-provenance.mjs (repository:check) and tests/unit/provenance.test.js.')
doc('docs/spec/review/coverage-gaps.md','generated review','','9.1.27','current','Generated by scripts/generate-spec.mjs; byte-checked by spec:check — must not move.')
doc('docs/spec/review/duplicates.md','generated review','','9.1.27','current','Generated by scripts/generate-spec.mjs; byte-checked by spec:check — must not move.')
doc('docs/spec/ (rest of generated tree incl. audit/signoff-manifest.json, laws/*.json, retained legacy records)','generated spec','','9.1.27','current','Generated by scripts/generate-spec.mjs and byte-checked by spec:check; manifests read by tests — must not move.',780)

# ---------------- ITEMS ----------------
I=[]
def item(id,title,status,cat,conf,evidence,sources,missing='',kind='planned'):
    I.append(dict(id=id,title=title,status=status,category=cat,confidence=conf,evidence=evidence,missing=missing,kind=kind,sources=[dict(file=f,loc=l) for f,l in sources]))
CA='docs/CODEBASE-AUDIT-2026-09-30.md'; ARP='docs/AUDIT_REMEDIATION_PLAN.md'; DP='docs/DECOMPOSITION_PLAN.md'
ARM='docs/ARCHITECTURAL_RESOLUTION_MATRIX.md'; FSM='docs/FEATURE_STATUS_MATRIX.md'; MCM='docs/MECHANICS_CONSUMER_MATRIX.md'
A9='docs/A9-MIGRATION-PLAN.md'; CEX='docs/CIVILIZATION-EXPANSION-REPORT-2026-09-30.md'; CSQ='docs/CIVILIZATION-SEQUEL-PLAN-2026-09-30.md'
A1='docs/11-26-Audit/01-consolidated-audit-dialogue.md'; A2='docs/11-26-Audit/02-message-answer-matrix.md'; A3='docs/11-26-Audit/03-full-audit-answer-set.md'; A4='docs/11-26-Audit/04-pasted-audit-baseline.md'
IG='docs/systems/implementation-gaps.md'; MD='docs/systems/module-decomposition.md'; LRA='docs/dev/law-relationship-architecture.md'
BE='docs/BACKEND_ENVELOPES.md'; RH='docs/REPOSITORY_HYGIENE.md'; ACO='docs/AUDIT_CORPUS_OWNERSHIP.md'; ESP='docs/EXPORT_SNAPSHOT_POLICY.md'; DAC='docs/DEEP_AUDIT_CLARIFICATIONS.md'
CG='docs/spec/review/coverage-gaps.md'

# --- Architecture / refactoring
item('A9','Remove the buffer_global singleton from laws.js (migrate 45 laws to explicit view param)','Not started','Architecture / refactor','verified',
 'src/physics/laws.js still has 49 `buffer_global` references and exports setBuffer(); src/physics/solver.js still calls setBuffer (2 matches). tests/unit/lawsSingleton.test.js characterises the current implicit-global behaviour.',
 [(CA,'§4.1 A9, §6.4'),(A9,'whole doc — 6 ordered steps'),(CEX,'§2 A9, §6'),(CSQ,'Open (carried forward)')],
 'All 6 steps of A9-MIGRATION-PLAN (view param, HISTORY context, 37 solver + 48 test call sites, delete singleton, guard test).')
item('A10','Shared render/core.js beneath Canvas2D and Pixi renderers','Not started','Architecture / refactor','verified',
 'src/render/ has only renderer.js, pixiRenderer.js, spriteSync.js, zeroCopy.js; only the asView helper was shared (zeroCopy.js).',[(CA,'§4.1 A10, §6.4'),(CEX,'§5'),(CSQ,'Open')],
 'Projection/background/cull/DPR abstraction; needs a browser render benchmark.')
item('A11','Split multiplex/multiplex.js (shardLifecycle / fitness / snapshot / render)','Not started','Architecture / refactor','verified',
 'src/multiplex/multiplex.js is still 1,522 lines; no split modules exist.',[(CA,'§4.1 A11, §6.4'),(DP,'§6 P5'),(CEX,'§5'),(CSQ,'Open')])
item('A12','Decompose main.js module-level singletons into a worldRuntime object','Not started','Architecture / refactor','verified',
 'src/main.js has grown to 1,826 lines with 42 top-level `let` bindings (audit measured 1,537 lines / 30+ singletons).',[(CA,'§4.1 A12, §6.4'),(CEX,'§5'),(CSQ,'Open — "now more valuable"')])
item('DP-P1','Decompose laws.js into src/physics/laws/{core,physics,biology,…}.js behind a facade','Not started','Architecture / refactor','verified',
 'No src/physics/laws/ directory; laws.js is 2,754 lines.',[(DP,'§2 Phase P1'),(A4,'§6 High #7 oversized hotspots')],'Plan is marked PROPOSED — awaiting user confirmation.')
item('DP-P2a','Solver leaf extractions (offspringRing, benchMode, buffers) + golden-parity fixture','Not started','Architecture / refactor','verified',
 'No src/physics/solver/ directory; no golden-parity script in bench/ or tests/ (grep "golden" → none).',[(DP,'§3 Phase P2 step 1')])
item('DP-P2b','Move grav/compute backend adapter behind solver/backends.js','Not started','Architecture / refactor','verified','solver.js still contains the BH/FMM/GPU adapter inline (e.g. `_useGPU` at solver.js:527).',[(DP,'§3 Phase P2 step 2')])
item('DP-P2c','Slice the ~1,675-line solve() into phase functions with a scratch context','Not started','Architecture / refactor','verified','solver.js is 1,988 lines; solve() not split.',[(DP,'§3 Phase P2 step 3')])
item('DP-P3','Split constants.js into src/constants/{stride,dna,laws,help,world}.js with a barrel facade','Done','Architecture / refactor','verified',
 'src/constants/ holds stride.js, dna.js, laws.js, help.js, world.js; src/constants.js is a 6-line re-export barrel; repository:check passes.',[(DP,'§4 Phase P3'),(A3,'§2.2')])
item('DP-P4','Extract workerBridge.js, spawn/population.js and intelligenceCadence.js from main.js','Not started','Architecture / refactor','verified','None of those files exist (src/ root has only constants.js, debug.js, main.js, react-entry.js).',[(DP,'§5 Phase P4')])
item('DP-P6','Split multiplexUI.js, worldPanel.js and worldSave.js','Not started','Architecture / refactor','verified','multiplexUI.js 840, worldPanel.js 553, worldSave.js 557 lines; no split modules.',[(DP,'§6 P6')])
item('DP-P7','Split dnaAnalytics.js and quantumMacro.js','Not started','Architecture / refactor','verified','dnaAnalytics.js 548, quantumMacro.js 493 lines; unsplit.',[(DP,'§6 P7')])
item('DP-P8','Split paramHelp.js / ui.js (only if touched)','Not started','Architecture / refactor','verified','paramHelp.js 515, ui.js 550 lines; optional by design.',[(DP,'§6 P8')])
# --- Duplication
item('CA-A1','Extract force3() guarded force triple and replace inline clamp(nanGuard()) force components','Done','Code duplication','verified',
 'src/physics/force.js exists; force3( used in physicsLaws (7), quantumLaws (3), thermoLaws (1). Remaining clamp(nanGuard()) sites clamp state scalars, as the audit\'s §6.3 correction says they should.',[(CA,'§2.2 P-1, §4.1 A1, §6.2, §6.3')])
item('CA-A2','Create core/numeric.js (clamp, nanGuard, num, hash2, dist2…) and delete local copies','Done','Code duplication','verified',
 'src/core/numeric.js exports num (l.66), hash2 (l.76), centroidDist2 (l.86); no other hash2/num/dist2 definitions in src/.',[(CA,'§2.1 DUP-4/5/8/9, §4.1 A2, §6.2')])
item('CA-A3','Delete dead applyAlloy from laws.js','Done','Code duplication','verified','Only export is src/physics/mergePhysics.js:333.',[(CA,'§2.3, §4.1 A3, §6.2')])
item('CA-A5','Unify the DNA quantize/dequantize codec (dna/codec.js)','Partial','Code duplication','verified',
 'src/dna/codec.js exists with 3 importers, but src/main.js:701 still dequantizes inline (`raw / 65535` loop).',[(CA,'§2.2 P-2, §4.1 A5, §6.2')],'Replace the remaining inline dequantize in main.js spawn path.')
item('CA-A6','Single clipboard helper and zero-copy view helper','Done','Code duplication','verified',
 'src/core/clipboard.js:33 fallbackCopy is the only definition; src/render/zeroCopy.js:23 asParticleView; pixiRenderer.js:26 asView is a one-line delegate.',[(CA,'§2.1 DUP-2/DUP-7, §4.1 A6, §6.2')])
item('CA-A7','Engine factory createEngine() + rename colliding update exports','Partial','Code duplication','verified',
 'Renames done: updateInsight (insightEngine.js:55), updateNarrative (narrativeEngine.js:170), updateGoal (goalEngine.js:115). No createEngine factory anywhere in src/.',[(CA,'§2.2 P-3, §4.1 A7, §6.2')],'Shared engine factory not introduced.')
item('CA-A8','Shared analytics panel shell (mountAnalyticsPanel) for all dashboards','Partial','Code duplication','verified',
 'src/ui/analyticsPanel.js used by ecoPanel, groupAnalytics, civilizationPanel. dnaAnalytics, speciesPanel, narrativePanel and intelPanel (own setValue at l.119) not migrated.',[(CA,'§2.1 DUP-6, §2.2 P-4, §4.1 A8, §6.2')],'Migrate the remaining 4 panels.')
item('CA-DUP1','Remove duplicate isAccretionLink / isAccretionPair','Partial','Code duplication','verified',
 'src/physics/laws.js:37 still defines a local isAccretionLink (used at l.943) alongside mergePhysics.js:64 isAccretionPair.',[(CA,'§2.1 DUP-1')])
item('CA-DUP3','Deduplicate cipherKey / cipherKeyFromStride crypto-key derivation','Not started','Code duplication','verified',
 'Both still exist: src/physics/laws.js:625 cipherKey and src/physics/lawgroups/infoLaws.js:49 cipherKeyFromStride.',[(CA,'§2.1 DUP-3')])
# --- Spec generator / docs tooling
item('CA-A4','Fix generate-spec.mjs reading the constants barrel (empty law catalog)','Done','Spec generator','verified',
 'scripts/generate-spec.mjs declares CONSTANTS_SOURCE_FILES (the 5 split modules) and cross-checks against imported LAW_COUNT/LAW_INDEXES; spec:check passes.',[(CA,'§3.1, §4.1 A4, §6.1')])
item('CA-H8','Make generate-spec import law catalogs instead of regex-parsing source','Partial','Spec generator','verified',
 'The generator imports REAL_LAW_* only as an integrity guard; LAW_HELP_DB, LAW_PARAMETERS etc. are still regex-extracted.',[(CA,'§4.2 H8')],'Replace regex extraction with imports.')
item('SPEC-HELP','Spec generator extracts 0/136 canonical LAW_HELP_DB entries (regex out of date)','Not started','Spec generator','verified',
 'docs/spec/review/coverage-gaps.md reports "Canonical LAW_HELP_DB entries: 0/136". generate-spec.mjs:218-226 expects `[idx]: { tier: \'…\' }` with single quotes, but src/constants/help.js uses NAME keys and double-quoted strings (128 `hint:` entries), so nothing matches.',
 [(CG,'Observed findings'),(A4,'§6 Critical #2 help metadata extraction untrustworthy')],'Generated help traceability is silently empty — same class of bug as the A4 barrel bug.',kind='finding')
item('CG-1','Make canonical LAW_HELP_DB the single owner of all help tiers (retire supplemental lawHelpPatches)','Not started','Law metadata','verified',
 'src/state/lawHelpPatches.js and mechanicsHelp.js still supply supplemental help merged at runtime (help.js:140-143).',[(CG,'Suggested improvements #1'),(RH,'Deferred decision #3')])
item('CG-2','Contract test asserting four non-empty help tiers + intentional-exception field per law','Unknown','Law metadata','inferred',
 'No test found asserting the `advanced` tier per law (grep in helpRegistry/lawCategories tests empty); LAW_COMPENDIUM notes only 62 laws have the 4th tier.',[(CG,'Suggested improvements #2')])
item('CG-3','Record semantic duplicate decisions before removing laws/subsystems','Partial','Law metadata','inferred','docs/spec/sim/concepts.md records some overlaps (FRICTION vs DRAG, INERTIA vs MASS_INERTIA); no formal decision log.',[(CG,'Suggested improvements #4'),('docs/spec/review/duplicates.md','whole file')])
item('CG-4','Run spec:check in CI','Done','CI / verification','verified','.github/workflows/deploy.yml runs `npm run repository:check`, which starts with `npm run spec:check`.',[(CG,'Suggested improvements #5')])
item('CG-5','ELECTRIC_FIELD needs implementation/evidence review','Not started','Law metadata','inferred','Flagged as the only law lacking implementation evidence in coverage-gaps.md; no ELECTRIC_FIELD record in docs/spec/audit/signoff-manifest.json (15 records).',[(CG,'Incomplete implementation evidence')])
# --- Repository hygiene / CI
item('CA-H1','Fix .gitignore dist/ typo and untrack dist/ + isolate/','Done','Repository hygiene','verified','.gitignore lists dist/ and isolate/; `git ls-files dist isolate` returns 0 files.',[(CA,'§1.3, §3.3, §4.2 H1, §6.5')])
item('CA-H2','Delete duplicate laws/ corpus (after merging the divergent physics.md line)','Done','Repository hygiene','verified','No laws/ directory in the tree.',[(CA,'§2.4, §4.2 H2, §6.4'),(CEX,'§2 H2')])
item('CA-H3','Collapse exports/*.md concat artifacts to the canonical two','Done','Exports','verified','exports/ holds only vepa-full-codebase-concat.md and vepa-docs-concat.md; retired entries recorded in exports/provenance.json and publication-plan.json; batch5Reports test asserts 2 exports + 2 retired.',[(CA,'§4.2 H3'),(CEX,'§2 H3'),(ESP,'Ownership table')])
item('CA-H4','Gate deploy on npm test (+ repository:check) in CI','Done','CI / verification','verified','deploy.yml: `npm ci` → `npm test` → `npm run repository:check` → build.',[(CA,'§3.3, §4.2 H4, §6.1')])
item('CA-H5','Remove archived tooling tests/run.mjs and scripts/patch-lawcat-test.mjs','Superseded','Repository hygiene','verified','Withdrawn by the audit itself (§6.3); both files retained and asserted by tests/unit/batch5Reports.test.js.',[(CA,'§4.2 H5, §6.3')])
item('CA-H6','Resolve dual lockfiles (npm vs bun)','Done','Repository hygiene','verified','bun.lock is gitignored and absent; package-lock.json is the SSOT used by `npm ci`.',[(CA,'§3.3, §4.2 H6'),(CEX,'§2 H6')])
item('CA-H7','Refresh SPEC.md (LAW_COUNT, test counts, legacy-tree contradiction) + vepa4 comments','Partial','Documentation','verified',
 'SPEC.md was refreshed to 136 laws / 951 tests and vepa4 comments now say dist/ and src/. But SPEC.md is stale again: header 9.1.22 and "109 files / 951 tests" vs actual 129 files / 1,431 tests.',[(CA,'§3.3, §4.2 H7, §6.2')],'Re-sync SPEC.md gate table and version.')
item('ARP-12','Continuously correct stale architecture/version/path claims','Partial','Documentation','verified',
 'Still stale: AGENTS.md header 9.1.22 + HEAD d2f9aa5 (actual 9.1.27 / 436afd2); AGENTS §8 says 860 tests and "no playwright.config" (it exists); §10.5 LAW_COUNT 128 (actual 136); README "Docs" links ../audit/FULL_AUDIT_2026-08-01.md (outside repo); GUIDE.md links missing docs/expansion/batches/.',
 [(ARP,'§3 rank 12'),(A4,'§6 Critical #1'),(CG,'Suggested improvements #3'),('AGENTS.md','header "Keep the map current"'),('docs/11-26-Audit/01-consolidated-audit-dialogue.md','§6 (128 vs 136)')])
item('AG-1','Re-sync AGENTS.md map (Active Target, §2.3 Git State, §8 test counts, Audit Hash)','Not started','Agent governance','verified',
 'AGENTS.md Audit Hash AGENTS_SYNC_v9.1.22_2026-09-23; VERSION is 9.1.27; git HEAD 436afd2.',[('AGENTS.md','header + §2.3 + §8')])
item('DAC-1','Rename audit-suite/ governance references to docs/audit/','Not started','Agent governance','verified',
 '11 `audit-suite` mentions remain across GEMINI.md and AGENTS.md (§7, §8, §10.3, §10.6, §13); no audit-suite/ directory exists.',[(DAC,'§2'),('GEMINI.md','§1.1'),('AGENTS.md','§7, §10.6')])
item('AG-2','Per-law RRP batches 15+ in audit-suite/laws-rrp','Superseded','Agent governance','verified','audit-suite/ no longer exists; tests/audit/batch_01-32.test.js and params_batch_01-18 cover all batches.',[('AGENTS.md','§13')])
item('AG-3','Resume the LAN-hub/phone multiplayer track','Superseded','Agent governance','verified','Dropped in the 4.7.0 release draft; no src/net/ or networkPanel.js in tree.',[('AGENTS.md','§13, §10.3')])
item('ARP-CC','Continuous controls in dev/release review (syntax-check, bench:backends, audit:inventory, artifact:inventory, git diff --check)','Partial','CI / verification','verified',
 'CI runs npm test, repository:check (spec:check + manifests + ui report) and build. syntax-check, bench:backends, audit:inventory, artifact:inventory and git diff --check are not in deploy.yml.',[(ARP,'§8')])
item('FSM-1','Expand browser/E2E workflow coverage','Partial','CI / verification','verified',
 'tests/e2e/physics-worker.spec.js and runtime-acceptance.spec.js exist, but CI never runs Playwright (deploy.yml has no e2e step).',[(FSM,'§2 Browser shell / Pixi rows'),(A4,'§6 Medium #9'),(A3,'§6')])
# --- Backends
item('ARP-1','Executable audit sign-off gate wired into repository:check','Done','Provenance / audit','verified',
 'scripts/validate-signoff.mjs called from check-repository.mjs; docs/spec/audit/signoff-manifest.json (15 records); tests/unit/auditSignoff.test.js.',[(ARP,'§3 rank 1, §4.1'),(ARM,'#6'),(A1,'§2.5 step 1'),(A4,'§6 High #6')])
item('ARP-2','Real-browser/device WebGPU parity and failure-lifecycle tests','Partial','Backends / performance','verified',
 'GPU path is wired opt-in (solver.js:527 `_useGPU = !!gpuForces`); tests/e2e/physics-worker.spec.js compares GPU vs CPU but returns {skipped:true} without a device, and CI never runs e2e. No recorded adapter/limits/tolerance report.',
 [(ARP,'§3 rank 2, §4.2'),(ARM,'#2'),(FSM,'§3 WebGPU row, §6 #2'),(A2,'§5 #2'),(A3,'§8 Technically open'),(DAC,'§3'),(BE,'§4'),(RH,'Deferred #4')],'Execute on a WebGPU-capable runner and store a machine-readable device report.')
item('ARP-3','Backend error/performance envelopes with exact CPU as reference','Done','Backends / performance','verified',
 'bench/backend-compare.mjs emits error/assessment envelopes; docs/BACKEND_ENVELOPES.md records 32-2048 fixtures; tests/unit/fmmParity.test.js pins the bands.',[(ARP,'§3 rank 3, §4.3'),(MCM,'Follow-up #3'),(A3,'§10')])
item('ARP-4','FMM keep/retire decision and placeholder removal','Done','Backends / performance','verified',
 'Decision recorded "retain experimental" (BACKEND_ENVELOPES §3); fmm.js:59 cellNeighbours is now a real toroidal stencil tested by fmmParity.test.js.',[(ARP,'§3 rank 4, §5.1'),(ARM,'#1'),(A4,'§6 High #5'),(A1,'§4')])
item('FMM-PROMO','FMM envelope parity (rmsRelative ≤ 0.1, 32–2048) before any promotion; DNA modifiers in far field','Not started','Backends / performance','verified',
 'Measured rmsRelative 1.15–2.02 at every scale (BACKEND_ENVELOPES §2); fmm.js header documents DNA modifiers absent from far-field.',[(ARM,'#1, Technically open #1'),(FSM,'§3 FMM rows, §6 #1'),(BE,'§2-3'),(A2,'§5 #1'),(A3,'§8')])
item('BH-ENV','Barnes–Hut envelope across population scales','Partial','Backends / performance','verified','Within envelope ≤512; marginal fail at 2048 (0.109 vs 0.1); tests pin only the ≤512 band.',[(ARM,'#3'),(BE,'§2'),(FSM,'§3 BH row')])
item('FSM-QUAD','Dedicated parity/error tests for octree useQuadrupole mode','Not started','Backends / performance','verified','No test file mentions quadrupole (grep tests/ → none); code path in src/physics/octree.js.',[(FSM,'§3 Quadrupole row')])
item('AUD-EXACT','Terminology: rename "exact CPU solver" to "reference CPU solver" (API/runtime)','Partial','Documentation','inferred','Mixed usage remains: worker/gpuCompute comments say "exact CPU", main.js:394 logs "reference CPU".',[(A2,'§5 #8'),(A3,'§8'),(A1,'§6')])
# --- Mechanics
item('ARP-5','Consolidate mechanics pair geometry in the hot path (or justify scalars)','Partial','Mechanics','inferred',
 'Hot-loop scalars documented as performance-specialized (MECHANICS_CONSUMER_MATRIX boundary rule 3). That rule claims value-equivalence is verified by mechanicsArchitecture.test.js, but the test only exercises getPairGeometry/diagnostics; no solver-vs-getPairGeometry parity test was found.',
 [(ARP,'§3 rank 5, §5.2'),(ARM,'#5, Technically open #4'),(FSM,'§2 Mechanics pair geometry, §5'),(RH,'Experimental/partial')],'Add a parity test comparing solver scalars to getPairGeometry.')
item('ARP-6','Mechanics diagnostics for COLL impulse, INERTIA, TOPOLOGY and momentum summaries','Partial','Mechanics','verified',
 'src/physics/mechanicsDiagnostics.js returns contact/momentum/torque/constraint/fragmentation/adhesion only; no COLL impulse, INERTIA or TOPOLOGY fields, no before/after momentum summary.',[(ARP,'§3 rank 6, §5.3'),(MCM,'Follow-up #1'),(ARM,'#5'),(A1,'§2.5 step 6')])
item('MCM-2','Browser fixture toggling Mechanics laws and checking worker state transitions','Partial','Mechanics','inferred','runtime-acceptance.spec.js:21 toggles CONTACT in the law grid; no assertion on worker particle-state transitions was found; not run in CI.',[(MCM,'Follow-up #2'),(ARP,'§5.3 acceptance')])
# --- Law ontology / semantics
item('ARP-7','Expand law ontology metadata by coupling/state risk','Partial','Law ontology / semantics','verified',
 'docs/spec/laws/ontology-coverage.json: 35 laws with metadata, 101 without. Priority tiers 1-4 landed (per ARCHITECTURAL_RESOLUTION_MATRIX); tier 5 "remaining in dependency order" not.',[(ARP,'§3 rank 7, §6.1'),(ARM,'#4, Technically open #3'),(A2,'§4 item 1'),(A3,'§4')])
item('ARP-8','Semantic behaviour + boundary tests for priority laws','Partial','Law ontology / semantics','inferred','Large audit suite (tests/audit batch_01-32, params_batch_01-18) plus unit tests; no per-law matrix showing behaviour+boundary coverage for every priority law; signoff manifest has only 15 records.',[(ARP,'§3 rank 8, §6.2'),(A2,'§5 #3'),(A3,'§8')])
item('AUD-CONS','Conservation and non-redundancy matrices across all 136 laws','Not started','Law ontology / semantics','inferred','No such artifact in docs/ or tests/ (grep for conservation/non-redundancy matrices → only the audit docs themselves).',[(A2,'§5 #7'),(A3,'§4.2, §8')])
item('AUD-STC','Formal state-transition / cross-subsystem mutation contract','Not started','Law ontology / semantics','inferred','No state-transition contract module or test found.',[(A3,'§8'),(A4,'§6 Medium #10')])
item('LRA-1','Roadmap 1 — relationship ontology foundations (vocabulary, validation, graph export)','Done','Law ontology / semantics','verified','src/state/lawOntology.js + src/physics/lawGraph.js (getLawRecord, inspectLaw, exportLawGraph*, findLawCycles, validateLawGraph); tests/unit/lawGraph.test.js.',[(LRA,'l.11 + whole doc')])
item('LRA-2','Roadmap 2 — Physics/Mechanics boundary (COLL vs CONTACT, MASS_INERTIA vs INERTIA)','Done','Law ontology / semantics','inferred','CONTACT correction vs COLL impulse separated (mechanicsLaws.js applyContactCorrection/applyCollisionImpulse; mechanicsArchitecture.test.js "keeps CONTACT geometric and separate from impact response"). MASS_INERTIA vs INERTIA documented as distinct in FEATURE_STATUS_MATRIX §5.',[(LRA,'l.12, Deferred overlap report'),(FSM,'§5'),(MCM,'Boundary rules')])
item('LRA-3','Roadmap 3 — state/resource accounting budgets','Not started','Law ontology / semantics','verified','No budget concept in lawOntology.js or lawGraph.js.',[(LRA,'l.13')])
item('LRA-4','Roadmap 4 — feedback & stability (cycle classes, bounded-loop diagnostics, runaway tests)','Partial','Law ontology / semantics','verified','findLawCycles() covers hard-dependency cycles only; only 4 ontology records carry a feedback field; no runaway-scenario diagnostics.',[(LRA,'l.14')])
item('LRA-5','Roadmap 5 — chemistry/thermal/EM coupling chains made explicit','Not started','Law ontology / semantics','inferred','No coupling-chain module or test found.',[(LRA,'l.15')])
item('LRA-6','Roadmap 6 — structure formation BOND → CONSTRAINT → TOPOLOGY','Partial','Law ontology / semantics','inferred','docs/dev/interaction-space.md + src/physics/interactionSpace.js describe the joining matrix; no formalised chain contract/tests.',[(LRA,'l.16'),('docs/dev/interaction-space.md','Joining matrix')])
item('LRA-7','Roadmap 7 — information/biology coupling trace','Not started','Law ontology / semantics','inferred','No trace module or test found.',[(LRA,'l.17')])
item('LRA-8','Roadmap 8 — quantum state machine (observation, coherence, uncertainty, wave/particle)','Not started','Law ontology / semantics','inferred','Quantum laws remain independent lawgroup functions; no state-machine module (quantumMacro.js is the Set N macroscale layer, not this).',[(LRA,'l.18')])
item('LRA-9','Roadmap 9 — emergent-chain cross-category integration tests','Not started','Law ontology / semantics','verified','No emergent-chain/cross-category scenario tests in tests/.',[(LRA,'l.19')])
item('LRA-10','Roadmap 10 — developer tooling/UI for relationship inspection','Not started','Law ontology / semantics','verified','No src/ui module imports lawGraph/inspectLaw/exportLawGraph.',[(LRA,'l.20')])
item('IS-1','Graph buffer for relationship state (move relationshipState into the solver path)','Not started','Law ontology / semantics','inferred','relationshipState.js stays "outside the solver Float32 hot path until a graph buffer is introduced"; no graph buffer exists.',[('docs/dev/interaction-space.md','Runtime compatibility and relationship state')])
# --- Provenance / exports
item('ARP-9','Audit-stage provenance manifests (stage, producer, date, source version) + provenance-header check','Partial','Provenance / audit','verified',
 'docs/audit/provenance.json covers the a3 tree at directory level and validate-provenance.mjs enforces coverage; per-stage producer/date/source-revision is absent ("producer not encoded") and no check for provenance headers exists.',[(ARP,'§3 rank 9, §7.1'),(ACO,'Deferred decisions'),(A2,'§5 #4'),(A3,'§8')])
item('ACO-2','Compare a3 roll-up claims against generated implementation/ontology manifests','Not started','Provenance / audit','inferred','audit_progress.md still claims 128 laws all complete (incl. TURBULENCE/CENTRIPETAL/ROTATION, no longer in LAW_INDEXES); no reconciliation report found.',[(ACO,'Deferred decisions #2'),('docs/audit/laws/a3/ roll-ups (audit_progress, all_stage_*, category docs, mega ensemble)','audit_progress.md')])
item('ACO-3','Decide whether historical audit reports live in repo, archive or release artifacts','Not started','Provenance / audit','verified','provenance.json still marks all records "retain"; no decision recorded.',[(ACO,'Deferred decisions #3'),(RH,'Deferred #1')])
item('A3-SIGNOFF','a3 Stage 1–3 audits and "fully verified" sign-offs for 128 laws','Superseded','Provenance / audit','verified','Registry is now 136 laws; sign-off authority moved to docs/spec/audit/signoff-manifest.json + validate-signoff.mjs; stage-3 prose ("617+ tests") is historical.',[('docs/audit/laws/a3/stage-3/ (128 per-law sign-offs)','e.g. 00_GRAV.md §4'),('docs/audit/laws/a3/ roll-ups (audit_progress, all_stage_*, category docs, mega ensemble)','audit_progress.md'),(ARM,'#6')])
item('ARP-10','Map export consumers, choose retention states, record producer/source revision in snapshot headers','Partial','Exports','verified',
 'Canonical set + producers + retired entries recorded (exports/provenance.json, publication-plan.json, repository-artifact-report.mjs). But both snapshots were generated 2026-08-14 from a 7.0.0-draft source and have not been regenerated; headers lack the source revision.',[(ARP,'§3 rank 10, §7.2'),(ARM,'#7, Technically open #5'),(ESP,'Retention decision'),(A2,'§5 #5'),(A3,'§1.3, §8'),(RH,'Deferred #2')],'Regenerate (npm run concat) and stamp source revision.')
item('AUD-PUB','Provision and CI-publish to the separate vepa-exports repository','Not started','Exports','verified','exports/publication-plan.json status "configured-not-published"; deploy.yml has no publication step.',[(A2,'§5 #6'),(A3,'§8, §10'),(A1,'§6')])
item('ESP-1','Update EXPORT_SNAPSHOT_POLICY table after the H3 retirement','Not started','Documentation','verified','Policy table still lists exports/vepa-codebase-full-concat.md as "retain pending review"; the file was retired 2026-09-30.',[(ESP,'Ownership table')],kind='finding')
item('ARP-11','Formalize historical-tool recovery/exclusion rules','Done','Repository hygiene','verified','scripts/repository-artifact-report.mjs classifies tests/run.mjs and patch-lawcat-test.mjs; tests/unit/batch5Reports.test.js asserts status and "deletion not authorized".',[(ARP,'§3 rank 11, §7.3'),(ARM,'#8'),('docs/LEGACY_TOOLING_INVENTORY.md','Policy')])
item('A4-SSOT','lawgroups/SPEC.md referenced as law SSOT but missing','Done','Documentation','verified','src/physics/lawgroups/SPEC.md exists; tests/unit/provenance.test.js asserts "Lawgroup Implementation Contract".',[(A4,'§6 Critical #3')],kind='finding')
item('A4-GPU','WebGPU disabled in solver via `_useGPU = false`','Done','Backends / performance','verified','solver.js:527 now `const _useGPU = !!gpuForces` (opt-in via computeEngine = gpu).',[(A4,'§6 High #4')],kind='finding')
# --- Civilization / social systems
item('CIV-1','Sparse relationship graph with stable pair keys + save/restore (individual recognition)','Partial','Civilization / social systems','verified',
 'civilization.js has pairKey kin edges (l.67/248) and serialize/restore. No general typed-edge registry with per-edge history/graph queries, and recordKin() has no runtime caller in src/ (only tests).',
 [(CEX,'§5 phase 1 (claims done)'),(IG,'rows Individual recognition + Relationship graph; next sequence #1'),(MD,'§1 relationship observation pipeline'),('docs/systems/meta-model.md','Suggested future registries: organizationGraph')],'Wire into runtime; add typed edges + history.')
item('CIV-2','Kin edges, households and care/resource transfer','Partial','Civilization / social systems','verified',
 'recordKin/createHousehold/joinHousehold/flowKinResources implemented and tested (civilization.test.js) but never called from main.js or any runtime module — the expansion report marks this "done".',[(CEX,'§5 phase 2'),(IG,'row Family; next sequence #2'),('docs/systems/roadmap-family-kinship.md','phases')],'Runtime wiring from lineage/births.')
item('CIV-3','Group-to-group federation + culture transmission fed from alliances','Done','Civilization / social systems','verified','main.js:1482 createFederation/addFederationMember; main.js:1442 transmitBetweenGroups on governance:alliance; cultureTransmission.test.js, civilizationWiring.test.js.',[(CEX,'§5 phase 3, §7'),(IG,'row Tribe/clan; next sequence #3'),(CSQ,'Where this came from')])
item('CIV-POL','Polity entities (jurisdiction, provinces, citizenship, institutions, succession)','Partial','Civilization / social systems','verified','foundPolity/claimTerritory/grantCitizenship/installSuccessor exist in civilization.js (l.428-534) with tests, but nothing in src/ calls foundPolity at runtime.',[(CEX,'§3 table Nation/polity, §4'),(IG,'row Nation')])
item('CIV-4','Durable structures with ownership, upkeep and dependencies','Done','Civilization / social systems','verified','src/state/structures.js; main.js:539/890/1681 createStructureRegistry and maintenance loop; structures.test.js (49), civilizationSequelWiring.test.js.',[(CSQ,'Phase 4'),(CEX,'§5 phase 4, §7'),(IG,'row Structure ownership; sequence #4'),('docs/systems/meta-model.md','structureRegistry')])
item('CIV-4b','Structures as physical objects (write field cells)','Not started','Civilization / social systems','verified','structures.js has no writeField call; construction.js still owns terrain.',[(CSQ,'What is still only a proxy'),(IG,'What must not yet be claimed')])
item('CIV-5','Multi-epoch continuity metrics + regime catalog','Done','Civilization / social systems','verified','src/state/continuity.js; main.js:1156 recordEraContinuity on epoch boundary; continuity.test.js.',[(CSQ,'Phase 5'),(CEX,'§5 phase 5'),(IG,'row Civilization; sequence #5'),('docs/systems/roadmap-civilization.md','phase 3')])
item('CIV-6','Codex explanations from evidence, never from law names','Done','Civilization / social systems','verified','src/state/codex.js (explainRegime, findLawAttribution guard); main.js:1157 recordCodexEntry; codex.test.js.',[(CSQ,'Phase 6'),(CEX,'§5 phase 6'),(IG,'row Codex ontology; sequence #6')])
item('CIV-6b','Codex feeds back into the simulation','Not started','Civilization / social systems','inferred','Codex only narrates (sequel plan); no feedback path from codex into solver/engines found.',[(CSQ,'What is still only a proxy')])
item('CIV-BUGS','Fix tally() retained→inherited ledger bug and structure record-id mismatch','Done','Civilization / social systems','verified','Pinned by cultureTransmission.test.js and civilizationSequelWiring.test.js (structureForGroup lookup).',[(CSQ,'Phase 4/5 bugs'),(CEX,'§7')],kind='finding')
item('CIV-7','Learned culture-transmission model (beyond hash-roll fidelity) and inter-world federation persistence','Not started','Civilization / social systems','inferred','Both called out as remaining proxies; no implementation found.',[(CSQ,'What is still only a proxy'),(CEX,'§6')])
item('IG-MATE','Explicit mate choice, courtship, pair lifecycle, rejection, mate memory','Not started','Civilization / social systems','verified','No mate-choice/courtship code in src/ (grep).',[(IG,'row Mating'),('docs/systems/roadmap-mating-reproduction.md','phases')])
item('IG-REPRO','Reproductive architectures (unary/binary/multi-parent/budding/fragmentation/colony) + reproduction ledger','Not started','Civilization / social systems','inferred','Single REPRO lifecycle path; no reproductiveStrategies/reproductionLedger modules.',[(IG,'row Reproductive architectures'),(MD,'§5')])
item('IG-BOUND','Emergent organism boundaries, merge/split events, collective fitness','Not started','Civilization / social systems','inferred','No such module or test found.',[(IG,'row Emergent boundaries')])
item('MD-KIN','kinshipGraph.js / familyProjection.js projections','Superseded','Civilization / social systems','verified','Kinship implemented instead inside src/state/civilization.js (see CIV-2).',[(MD,'§2')])
item('MD-ORG','Generic organizationRegistry/Relations/Detection instead of parallel registries','Superseded','Civilization / social systems','inferred','Federation/polity/culture built as record kinds on the shared systemLifecycle substrate in civilization.js rather than a separate organization registry.',[(MD,'§3, Invariant 6')])
item('MD-CULT','culturalTraits / culturalTransmission / culturalSelection (prestige, environmental selection)','Partial','Civilization / social systems','verified','Explicit symbol/norm objects + vertical/horizontal transmission in civilization.js; no prestige/environmental selection.',[(MD,'§4'),(IG,'row Cultural transmission')])
item('MD-ECON','resourceLedger.js / marketDynamics.js / polityProjection.js','Not started','Civilization / social systems','verified','None of the files exist.',[(MD,'§6')])
item('MD-REL','Relationship recorder/features/regimes pipeline modules','Not started','Civilization / social systems','verified','No relationshipRecorder/Features/Regimes files in src/engines/.',[(MD,'§1'),('docs/systems/assessment-20260920.md','Current conclusion')])
item('SYS-48','Integrate all 48 A–D roadmap variants via one registry (A→B→C→D, 47 seams, topology, replay)','Done','Systems roadmap','verified','src/state/systemVariants.js + systemLifecycle.js + systemFoundation.js; systemVariants/systemLifecycle/systemFoundation tests.',[('docs/systems/roadmaps/ (README + 48 A–D variants)','README'),('docs/systems/roadmap-overview.md','Synchronized delivery rule'),('SPEC.md','Problem statement'),('PLAN.md','v9.1.18-9.1.21 notes')])
NOTES={'family-kinship':'kin library in civilization.js not wired into runtime','group-tribe-clan':'federation wired (main.js:1482)','mating-reproduction':'no explicit mate choice / courtship','nation-polity':'polity functions exist but no runtime caller','civilization':'continuity + codex wired','culture-memory':'culture objects + alliance transmission wired','relationship-laboratory':'relationshipExplorer.js exists; no recorder pipeline','synthetic-society':'synthetic.js (Set P) exists','ecology':'ecoEngine.js metrics ring','economy-governance':'economy.js/governance.js proxies; no ledger','infrastructure':'structures.js upkeep; no field writes','species-lineage':'lineageTracker + speciation implemented'}
for s in SYSTEMS:
    item('SYS-'+s,f'{s.replace("-"," / ").title()} system roadmap — domain adapters & live coupling (phases 2–6)','Partial','Systems roadmap','inferred',
      f'Shared lifecycle substrate supplies records/events/emergence/reports for this system, but roadmap-overview.md says "domain-specific adapters and live simulation coupling remain separate future work". Domain note: {NOTES[s]}.',
      [(f'docs/systems/roadmap-{s}.md','phases 1–6'),('docs/systems/roadmaps/ (README + 48 A–D variants)',f'{s}-A..D.md'),('docs/systems/roles/ (README + 11 role files)','role file'),('docs/systems/roadmap-overview.md','Current delivery status')])
# --- Simulation feature sets (RRP trilogies)
TRI=[('E','Matter & Medium — vector fields, walls/biomes, portals, wells, hard COLL','src/physics/fields.js; tests/unit/fields.test.js','docs/dev/rrp-trilogy/intent.md','§2'),
('F','Civilizations — groups, roles, construction, economy, analytics','src/state/groupRegistry.js, construction.js, economy.js; groupRegistry/constructionEconomy tests','docs/dev/rrp-trilogy/intent.md','§3'),
('A','Living World — speciation, ecosystem analytics, world events','src/engines/speciation.js, ecoEngine.js, worldEvents.js; livingWorld.test.js','docs/dev/rrp-trilogy/intent.md','§4'),
('D','Deep Time & Epochs','src/engines/epochEngine.js; deepTime.test.js','docs/dev/rrp-trilogy-2/intent.md','Set D'),
('G','Memory & Culture buffers','src/state/memoryBuffers.js; memoryCulture.test.js','docs/dev/rrp-trilogy-2/intent.md','Set G'),
('H','Agency & Narrative actor + milestones','src/engines/agencyEngine.js, goalBehavior.js; agencyNarrative.test.js','docs/dev/rrp-trilogy-2/intent.md','Set H'),
('I','Tools & Artifacts','src/state/artifacts.js; artifacts.test.js','docs/dev/rrp-trilogy-3/intent.md','Set I l.18'),
('J','Society & Governance','src/state/governance.js; governance.test.js','docs/dev/rrp-trilogy-3/intent.md','Set J l.23'),
('K','Infrastructure & Energy','src/state/infrastructure.js; infrastructure.test.js','docs/dev/rrp-trilogy-3/intent.md','Set K l.28'),
('L','Exotic Matter','src/state/exoticMatter.js; exoticMatter.test.js','docs/dev/rrp-trilogy-4/intent.md','Set L l.19'),
('M','Relativity (curvature, lensing, dilation, E=mc²)','src/state/relativity.js; relativity.test.js','docs/dev/rrp-trilogy-4/intent.md','Set M l.28'),
('N','Quantum Macroscale','src/state/quantumMacro.js; quantumMacro.test.js','docs/dev/rrp-trilogy-4/intent.md','Set N l.34'),
('O','Stellar Physics (stars, black holes, supernovae)','src/state/stellar.js; stellar.test.js','docs/dev/rrp-trilogy-5/intent.md','Set O l.19'),
('P','Synthetic Life (synthetic organisms, uploads, machine groups)','src/state/synthetic.js; synthetic.test.js','docs/dev/rrp-trilogy-5/intent.md','Set P l.24')]
for k,t,ev,f,l in TRI:
    item('RRP-'+k,f'Set {k} — {t}','Done','Simulation feature sets','verified',ev+' (module + passing test present).',[(f,l),(f.replace('intent','traceability'),'matrix'),('AGENTS.md','header RRP trilogies'),('CHANGELOG.md','release entry')])
for k,t,f,l,mod in [('Q','Cosmology — multiverse shard exchange, cosmic epochs, dark-energy expansion','docs/dev/rrp-trilogy-5/intent.md','Set Q l.29','src/state/cosmology.js'),
 ('R','Entropy & Rebirth — heat death, Big Crunch/Bounce, entropy upkeep','docs/dev/rrp-trilogy-6/intent.md','Set R l.19','src/state/entropy.js'),
 ('S','Simulation Awareness — awareness arcs, meta-events, awareness UI','docs/dev/rrp-trilogy-6/intent.md','Set S l.24','src/state/awareness.js'),
 ('T','The Observer — god-mode gestures, graduation, new-game-plus','docs/dev/rrp-trilogy-6/intent.md','Set T l.29','src/state/transcendence.js')]:
    item('RRP-'+k,f'Set {k} — {t}','Not started','Simulation feature sets','verified',f'{mod} does not exist; no cosmology/heat-death/awareness/transcendence code in src/ (only unrelated CONSCIOUSNESS-law help text). CHANGELOG last mentions Set {k} as "next".',[(f,l),(f.replace('intent','traceability'),'matrix'),('AGENTS.md','header "Q v8.17.0 next"')])
# --- Root plan/spec
item('PLAN-V4','VEPA4 integrated-intelligence plan steps 1–10 (fork, PREDATION, signals, engine wiring, intel UI, tests, docs)','Done','Simulation feature sets','verified','Five engines imported/constructed in main.js; LAW_INDEXES.PREDATION = 51; signal.test.js and engines.test.js pass.',[('PLAN.md','## Steps 1–10'),(CA,'§3.2')])
for n,(t,ev) in enumerate([('Wire all five engines into main.js (event-driven)','insight/narrative/lineage/goal/timeline engines imported and constructed in main.js boot(); engines.test.js.'),
 ('Communication DNA physics (pulse, channel-filtered propagation, response, memory)','applySignalDecay/applySignalExchange in laws.js; tests/unit/signal.test.js.'),
 ('Restore PREDATION as an explicit law','LAW_INDEXES.PREDATION = 51 dispatched in solver; tests/audit/batch_11.test.js.'),
 ('World Intelligence Dashboard','src/ui/intelPanel.js + analytics panels mounted in WORLD/DATA tabs.'),
 ('No per-frame allocations in hot loops','zero-copy asParticleView; allocation-free pairwise path (v8.15.1).')],1):
    item(f'SPEC-G{n}',t,'Done','Simulation feature sets','verified' if n<4 else 'inferred',ev,[('SPEC.md',f'## Goals #{n}'),(CA,'§3.2')])
item('SPEC-AC4','Dashboard renders (REC toggle, scrub slider) — manual browser check','Unknown','Simulation feature sets','inferred','SPEC itself says DOM-driven with no unit test; not verified in this run.',[('SPEC.md','Acceptance Criteria #4')])
item('RB-1','Renderer benchmark on real GPU hardware (current results are SwiftShader only)','Not started','Rendering','verified','bench/results/renderer-benchmark.json records renderer "ANGLE … SwiftShader"; report says real-hardware tails must not be inferred.',[('docs/RENDERER_BENCHMARK_REPORT.md','§5 #2')])
item('RB-2','PixiJS as preferred backend with Canvas2D fallback and Settings toggle','Done','Rendering','verified','src/render/pixiRenderer.js + renderer.js fallback; settingsPanel.js:111 persists vepa-render-backend.',[('docs/RENDERER_BENCHMARK_REPORT.md','§5 #5, §7')])
item('LC-1','Reconcile legacy TURBULENCE/CENTRIPETAL/ROTATION names left in help/param/icon text','Partial','Law metadata','verified','Still referenced in src/constants/help.js (6), paramHelp.js (3), worldParams.js (3), physicsLaws.js (4), solver.js, tooltip.js, mechanicsHelp.js.',[('LAW_COMPENDIUM.md','§6 Known boundaries'),('docs/audit/laws/a3/ roll-ups (audit_progress, all_stage_*, category docs, mega ensemble)','audit_progress.md #85-87')])
item('FSM-SAVE','Formal world-save schema compatibility/migration policy','Partial','Simulation feature sets','verified','worldSave.js has WORLD_SAVE_VERSION = 1 and rejects newer versions (l.291); additive fields restore defaults; no written migration policy.',[(FSM,'§2 Persistence row')])

# ----- 2026-10-03 milestone (Codey build on branch codey/complete-plans; verified by fresh-worktree verifier passes)
doc('docs/FMM-INVESTIGATION.md','report','2026-10-03','9.1.27','current','Time-boxed FMM bug hunt (AC-89, D-008).')
doc('docs/WORLD-SAVE-POLICY.md','policy','2026-10-03','9.1.27','current','World-save compatibility policy (FSM-SAVE).')
doc('docs/MULTIPLEX-PERF.md','report','2026-10-03','9.1.27','current','Chaos Multiplex configuration, presets, worker pool and benchmarks (MX-20, D-014, D-016).')
doc('docs/GOLDEN-REBASELINE.md','report','2026-10-03','9.1.27','current','Golden-parity re-baseline for FIELD-ONCE default (D-016); legacy hashes kept.')
doc('bench/results/multiplex-mx20.md','report','2026-10-03','9.1.27','current','MX-20 benchmark tables: presets, combination grid, Chrome frame times.')
doc('docs/spec/review/duplicate-decisions.md','decision-log','2026-10-03','9.1.27','current','Duplicate-concept decision log (CG-3).')
H='codey/complete-plans'
UPD = {
 'AG-1': ('Done','AGENTS.md re-synced: v9.1.27, Audit Hash AGENTS_SYNC_v9.1.27_2026-10-03, live test counts, LAW_COUNT 136 / 160-bit lawState (d81e4df, e5547b8). VERIFY-B1 PASS.'),
 'DAC-1': ('Done','0 audit-suite references in AGENTS.md/GEMINI.md (6283aa9). VERIFY-B1 PASS.'),
 'CA-H7': ('Done','SPEC.md header 9.1.27 and gate counts synced to vitest JSON (9b75d29, later count re-syncs). VERIFY-B1 PASS.'),
 'ESP-1': ('Done','EXPORT_SNAPSHOT_POLICY records the 2026-09-30 retirement (a11fdc8). VERIFY-B1 PASS.'),
 'AUD-EXACT': ('Done',"gravEngine 'reference' canonical, 'exact' permanent alias, bit-identical test gravEngineAlias.test.js; 0 'exact CPU' in src (2a03db0). VERIFY-B1 PASS."),
 'LC-1': ('Done','Help/icon entries for retired TURBULENCE/CENTRIPETAL/ROTATION/ELASTICITY removed, knobs labelled (LEGACY), contract test helpLawNames.test.js (8512f4c). VERIFY-B1 PASS.'),
 'CG-3': ('Done','docs/spec/review/duplicate-decisions.md covers every pair (c40638a); FRICTION/DRAG marked open: needs Gem. VERIFY-B1 PASS (weak, doc-only).'),
 'FSM-SAVE': ('Done','docs/WORLD-SAVE-POLICY.md + worldSaveCompat.test.js; newer versions rejected on import and restore; civilization/codex and Mechanics pentaFlags now survive save/export (585fb76, d6d5bde). VERIFY-B1 PASS.'),
 'ARP-12': ('Partial','Hand-written docs 0 broken links; generators relink (docs/spec, complete-atlas); 3031 → 1 broken link. Remaining one is in stale exports/vepa-docs-concat.md (B5 ARP-10).'),
 'SPEC-HELP': ('Done','Generator reports canonical LAW_HELP_DB coverage 136/136 (was 0); specHelpCoverage.test.js (d5d6ed0). VERIFY-B2 PASS.'),
 'CA-H8': ('Done','generate-spec.mjs imports live constants/help modules, no regex extraction (d5d6ed0). VERIFY-B2 PASS.'),
 'CG-1': ('Done','lawHelpPatches.js removed, MECHANICS overlay folded into LAW_HELP_DB, no runtime merge; snapshot test lawHelpFold.test.js (910533c). VERIFY-B2 PASS.'),
 'CG-5': ('Done','ELECTRIC_FIELD gates applyFieldDrift, FIELD = central gradient only; ELECTRIC STORM + TIDAL_BLOOM include ELECTRIC_FIELD (default behaviour preserved: golden default hash identical pre/post); sign-off record (f5eaeea). VERIFY-B2 PASS.'),
 'CG-2': ('Done','helpTierContract.test.js over all 136 laws; 74 explicit ADVANCED_HELP_EXCEPTIONS (669632d). VERIFY-B2 PASS (weak: exceptions are a content gap).'),
 'CA-A5': ('Done','main.js spawn paths use codec.writeDNACache; bit-identical test dnaCacheCodec.test.js (f63a80e). VERIFY-B3 PASS.'),
 'CA-DUP1': ('Done','Single isAccretionPair (452f1af); singleImplementations.test.js. VERIFY-B3 PASS.'),
 'CA-DUP3': ('Done','Single cipherKey module src/physics/cipherKey.js (452f1af). VERIFY-B3 PASS.'),
 'CA-A7': ('Done','src/engines/createEngine.js used by insight/goal/timeline/narrative (36ccae3). VERIFY-B3 PASS.'),
 'CA-A8': ('Done','intelPanel uses the shared setCellValue (b43aeed); AC-18 narrowed by D-012 to dashboards with intel-grid cells (dnaAnalytics/speciesPanel/narrativePanel have none). VERIFY-B3 PASS.'),
 'DP-P2a': ('Partial','First half done: golden-parity fixture scripts/golden-parity.mjs + npm run golden:check, 12 scenarios (a4e52de).'),
 'SPEC-AC4': ('Not started','Now actionable as AC-91 (Playwright dashboard test, D-002); not built yet (Playwright browsers not installed).'),
}
WONT = {'DP-P8':'D-002: optional by design ("only if touched").','IS-1':'D-002: conditional design note with no driving need.',
        'CIV-7':'D-006: learned culture model is unspecified research.','FMM-PROMO':'D-008: repo decision RETAIN EXPERIMENTAL; replaced by the FMM hunt (FMM-HUNT).',
        'AUD-PUB':'D-007: needs a new repo, secrets and pushes (outside the box, irreversible).'}
byid={i['id']:i for i in I}
for k,(st,ev) in UPD.items():
    byid[k]['status']=st; byid[k]['evidence']=ev+f' [{H}]'
    if st=='Done': byid[k]['missing']=''
for k,why in WONT.items():
    byid[k]['status']="Won't do"; byid[k]['missing']=''; byid[k]['evidence']='Won\'t do — '+why
item('FMM-HUNT','Time-boxed FMM defect hunt (Q7 B)','Done','Backends / performance','verified','7 defects fixed in src/physics/fmm.js (missing near-field sentinel, duplicate stencil cells, dropped/duplicated far cells, repulsive far monopole, COM centring, quadrupole coefficient): rmsRelative 1.15–1.68 → 0 at 32, 0.10–0.27 at 128–4096; still > 0.1 so FMM stays experimental (3dc34f3).',[('docs/FMM-INVESTIGATION.md','whole report')])
item('E9','RRP E.9 — save/restore the PRNG seed and state (determinism)','Done','Simulation feature sets','verified','World saves carry an additive rng {seed,state}; restore resumes the exact sequence (worldSaveRng.test.js, mutation-checked) (bf34ecc). VERIFY-B3b PASS (AC-92).',[('docs/dev/rrp-trilogy/intent.md','Set E'),('docs/WORLD-SAVE-POLICY.md','Known gaps')])
item('LAW-PENTA','Multiplex shards drop Mechanics laws; randomizeLaws flips laws 96-103 for l ≥ 128','Done','Simulation feature sets','verified','pentaFlags kept through clone, snapshot/restore, history records and copy-to-world; randomizeLaws writes laws ≥128 to pentaFlags (multiplexPenta.test.js, mutation-checked) (1d57521). VERIFY-B3b PASS (AC-93).',[('AGENTS.md','lawState paragraph (pentaFlags warning)')])
item('DET-1','Remove wall-clock performance.now() from law hashing (laws.js ~414/470/1716/1800/1848)','Done','Simulation feature sets','verified','Laws read a tick clock (16 ms per solve, reset on restart, resumed from the save tick); golden hashes unchanged even with the clock stub removed (lawClock.test.js) (28f29a0). VERIFY-B3b PASS (AC-94).',[('docs/dev/rrp-trilogy-6/intent.md','R·S·T prerequisites')])
item('MX-20','Chaos Multiplex: 20 concurrent sims at 2.5% population with no lag (D-014, D-016 configurable A+B+C)','Done','Backends / performance','verified','D-016: configurable particles/sim 125–2,500 (↔ POP %), light/full preview laws (editable light set), decoupled tick scheduler (frame/fixed/adaptive), worker pool, presets Smooth 20 / Balanced / Full fidelity, settings persisted (f976ed4, f9f47c6, 3404dc0). Headless (8 vCPU, no GPU): Smooth 20 main 1.7/2.7 ms, 59.7 ticks/s per sim; Full fidelity main 0.03/0.8 ms, 0.45 ticks/s per sim — AC-95 PASS. Chrome on this GPU-less box: no config reaches 60 fps (baseline app 67–83 ms; SwiftShader); real-GPU check pending.',[('docs/MULTIPLEX-PERF.md','whole report'),('bench/results/multiplex-mx20.md','benchmark tables')])
item('FIELD-ONCE','advanceFields() runs inside the per-particle loop (field medium advances N× per tick)','Done','Backends / performance','verified','On by default (D-016, 6ba0ec4): fields advance once per solve. Golden re-baselined: 12 scenarios unchanged, new default-tidal-bloom-params scenario; legacy hash kept in docs/GOLDEN-REBASELINE.md (GOLDEN_FIELD_LEGACY=1). AC-96 PASS.',[('docs/GOLDEN-REBASELINE.md','whole note')])
item('HIDDEN-STATE','solve() keeps module-level state between worlds/shards (fields singleton, registries)','Done','Backends / performance','verified','Solver contexts (createSolverContext/enterSolverContext) hold the field medium, HISTORY/law clocks and solve tick; each multiplex sim has its own (in-thread and in workers). Tests: sim alone = interleaved with others + main world; two fresh all-laws runs identical; pool = in-thread bit for bit (f976ed4, 5c5b288). AC-97 PASS. Main-world reset still reuses the default context.',[('docs/MULTIPLEX-PERF.md','HIDDEN-STATE fix')])
item('RRP-GAPS','RRP A–Q sub-items verified PARTIAL/UNVERIFIED (E3,E4,K2,L4,L5,M2,M3,N1,O3,P3; UI: A3,A6,F8)','Partial','Simulation feature sets','verified','Fresh-context RRP verification (.codey/RRP-VERIFY.md): 69 sub-items, 52 PASS, 10 PARTIAL, 4 MISSING, 3 UNVERIFIED; Set Q prototyped only (branch codey/proto-set-q).',[('docs/dev/rrp-trilogy-5/intent.md','Sets O·P·Q'),('docs/dev/rrp-trilogy-4/intent.md','Sets L·M·N')])

# ----- 2026-10-03 evening round (D-019: B4 onwards; verified by fresh-worktree passes VERIFY-B4/B5/B6)
UPD2 = {
 'ARP-5': ('Done','Null-by-default runtimeConfig.pairProbe hook; pairScalarParity.test.js shows the hot-path scalars equal getPairGeometry within 1e-9 on 4 fixtures (close, wrap, coincident, 60-particle cloud) (4e8016a). VERIFY-B4 PASS.'),
 'ARP-6': ('Done','inspectMechanicsPair also reports collImpulse, inertia, topology and momentum before/after; mechanicsDiagnosticsFields.test.js (881ce9e). VERIFY-B4 PASS.'),
 'BH-ENV': ('Done','AC-22: bhThetaForPopulation(n) envelope (θ 0.7 at ≤128, −0.1 per doubling, floor 0.5; solver uses min(gravTheta, scaled) so the default is unchanged); bhThetaEnvelope.test.js 32–2048 (5ee635a). Finding for Gem: some seeds exceed 0.1 at ≥2048 (0.135–0.20) because cells straddle the minimum-image cut; options in VERIFY-B4. VERIFY-B4 PASS.'),
 'FSM-QUAD': ('Done','octreeQuadrupole.test.js pins quadrupole rms (0.0317 N=256, 0.0329 N=1024) (1870bc3). Finding: no accuracy gain over monopole; the "~10× more accurate" header claim is false (decision for Gem). VERIFY-B4 PASS.'),
 'ARP-CC': ('Done','deploy.yml "Repository controls" step: syntax-check, bench:backends, audit:inventory, artifact:inventory, git diff --exit-code (d8175ce). VERIFY-B4 PASS.'),
 'FSM-1': ('Done','CI installs Playwright and runs npm run test:e2e; bootApp() helper clears the launch modal; boot-render-worker.spec.js; dev-only __VEPA_TEST__ hooks (d8175ce, 9e1c98f). 11/11 e2e pass on /usr/bin/google-chrome. VERIFY-B4 PASS.'),
 'MCM-2': ('Done','mechanics-worker.spec.js: CONTACT on separates staged overlapping pairs in the worker vs law off (9b4b971). VERIFY-B4 PASS.'),
 'SPEC-AC4': ('Done','AC-91: timeline-dashboard.spec.js — dashboard renders, REC toggles, scrub restores an earlier tick (108db62). VERIFY-B4 PASS.'),
 'ARP-9': ('Done','provenance.json records carry stage, producer, date and sourceRevision; validate-provenance enforces the headers; provenanceHeaders.test.js (e068738). VERIFY-B5 PASS.'),
 'ACO-3': ('Done','D-009 retention recorded: records status retained-historical with retentionDecision; AUDIT_CORPUS_OWNERSHIP.md updated (e068738). VERIFY-B5 PASS.'),
 'ACO-2': ('Done','scripts/a3-reconciliation.mjs → docs/audit/A3-RECONCILIATION.md (28 disagreements: 10 retired/renamed, 2 index, 2 category, 13 uncovered, 128 vs 136); audit:reconcile[:check]; test (8ca7af7). VERIFY-B5 PASS.'),
 'ARP-10': ('Done','Export header (producer, AEST date, source revision); snapshots regenerated from clean tree at 2b25675; exports:check verifies headers + real commit; links rebased (27c04d9, 2b25675, e6f0c7b). VERIFY-B5 PASS.'),
 'ARP-12': ('Done','0 broken links (hand and generated) after the export relink (e6f0c7b). VERIFY-B5 PASS.'),
 'ARP-7': ('Done','implementedBy (file#function) for all 136 laws from a generated static scan (scripts/derive-law-implementations.mjs, laws:derive:check); undeclared laws get scanned stride reads/writes + note; coverage 136/136; descriptive only (da7189e). VERIFY-B6 PASS.'),
 'LRA-3': ('Done','src/state/stateBudgets.js: 8 budgeted fields cross-checked against the scan; 4 undeclared writes now declared; 5 reasoned exceptions (IONIZATION TEMPERATURE, LEARN MEMORY flagged for review); adversarial tests (bd367a5). VERIFY-B6 PASS.'),
 'AUD-STC': ('Done','src/state/strideWriteContract.js: writer ownership for 41 stride fields; test fails on undeclared writes, unknown fields, stale owners (91dfc59). VERIFY-B6 PASS.'),
}
for k,(st,ev) in UPD2.items():
    byid[k]['status']=st; byid[k]['evidence']=ev+f' [{H}]'
    if st=='Done': byid[k]['missing']=''

# ----- UPD3: 2026-10-04 round (recs D-020..D-023, perf pass, B6 rest, B7)
doc('docs/PERF-PASS-2026-10-04.md','report','2026-10-04','9.1.27','current','Perf pass: test build ran physics on the main thread without COOP/COEP; PERF-1 copy-mode worker fix.')
item('BH-PERIODIC','Periodic (wrap-aware) Barnes–Hut tree so cells never straddle the minimum-image cut','Not started','Backends / performance','verified','D-020 (rec 1): keep the BH θ envelope as-is; a periodic tree is the real fix for the ≥2048 seeds above 0.1 (e450cc2).',[(BE,'BH envelope decision D-020')])
item('PERF-1','Test build / GitHub Pages under 10 fps at ~300 particles','Done','Backends / performance','verified','Root cause: without COOP/COEP there is no SharedArrayBuffer, so physics ran on the main thread in rAF. Worker copy mode transfers the live particle slice each tick (09925f0). Headless Chrome, single sim: 300 → 11.8 to 60 fps; 1000 → 4.9 to 60; 2500 → 2.1 to 57; multiplex 60 to 60. Sim tick rate unchanged (solver per-pair cost; BLOCKED for Gem). VERIFY-PERF PASS.',[('docs/PERF-PASS-2026-10-04.md','whole note')])
UPD3 = {
 'LRA-4': ('Done','classifyLawCycles + loopDiagnostics; 4 runaway scenarios bounded (9b4c310). VERIFY-PERF PASS.'),
 'LRA-5': ('Done','6 coupling chains declared + ontology validator; each exercised end-to-end (7435373). VERIFY-B6b PASS.'),
 'LRA-6': ('Done','structureFormation.js BOND→CONSTRAINT→TOPOLOGY contract (44e6338). VERIFY-B6b PASS.'),
 'LRA-7': ('Done','informationTrace.js memory→learning→culture→behaviour→inheritance (5c59691). VERIFY-B6b PASS.'),
 'LRA-8': ('Done','quantumStateMachine.js: amplitude/mode/link axes, legal transitions, reciprocal entanglement invariant, checked every tick on a live fixture (80e38df). VERIFY-B6b PASS.'),
 'LRA-9': ('Done','crossCategoryScenarios.test.js: 5 cross-category contracts + all-laws boundedness (1563a90). VERIFY-B6b PASS.'),
 'LRA-10': ('Done','Dev-only law inspector (?lawInspector), stripped from production builds, DOM-tested (808ab25). VERIFY-B6b PASS.'),
 'ARP-8': ('Done','18 priority laws, 1 behaviour (on vs off) + 1 boundary test each; generated docs/spec/audit/priority-law-matrix.md; sign-off records per law (9571651). VERIFY-B6b PASS.'),
 'AUD-CONS': ('Done','Measured conservation + non-redundancy matrices for 136/136 laws, generated by generate-spec (spec:check guards) (b105e54). Findings: COMMS/ANTIMATTER undeclared writes; PROTOCOL≡POLARIZATION on the fixture; 24 laws no solo effect. VERIFY-B6b PASS.'),
 'CIV-1': ('Done','relationshipGraph.js typed edges, bounded history, queries, save/restore (c06ce0f); populated live by the civRuntime adapter (4907c64). VERIFY-B7 PASS.'),
 'CIV-2': ('Done','civRuntime adapter: live births → kin edges + households; conserved household care each social step; survives save/restore; headless live-loop test + e2e (4907c64). Off by default (runtimeConfig.civRuntime). VERIFY-B7 PASS.'),
 'CIV-POL': ('Done','civRuntime: federation ≥3 groups founds a polity (provinces, territory, citizenship, succession on ruler death) (4907c64). Off by default. VERIFY-B7 PASS.'),
 'MD-CULT': ('Done','culturalSelection.js prestige-biased fidelity + environmental selection, tests show each biases outcomes (e105616); live via civRuntime. VERIFY-B7 PASS.'),
 'MD-REL': ('Done','relationshipRecorder/Features/Regimes in src/engines (48a172e), fed by live adapter events (4907c64). VERIFY-B7 PASS.'),
}
for k,(st,ev) in UPD3.items():
    byid=globals().get('byid') or {i['id']:i for i in I}
    byid[k]['status']=st; byid[k]['evidence']=ev+f' [{H}]'
    if st=='Done': byid[k]['missing']=''

# ----- finalize
doc_by={d['path']:d for d in D}
for it in I:
    for s in it['sources']:
        d=doc_by.get(s['file'])
        if d is None: raise SystemExit('unknown source doc '+s['file']+' in '+it['id'])
        s['docType']=d['type']; s['docDate']=d['date']; s['docVersion']=d['version']; s['docClass']=d['classification']
        if d.get('movedTo'): s['movedTo']=d['movedTo']
    p=doc_by[it['sources'][0]['file']]
    it['primarySource']=p['path']; it['docType']=p['type']; it['docDate']=p['date']; it['docVersion']=p['version']; it['docClass']=p['classification']
ids=[i['id'] for i in I]; assert len(ids)==len(set(ids)), 'dup ids'
for d in D:
    d['itemCount']=sum(1 for it in I if any(s['file']==d['path'] for s in it['sources']))
counts={}
for it in I: counts[it['status']]=counts.get(it['status'],0)+1
actionable=[i for i in I if i['status'] not in ('Superseded',"Won't do",'Unknown')]
done=sum(1 for i in actionable if i['status']=='Done'); part=sum(1 for i in actionable if i['status']=='Partial')
meta=dict(repo='DayneK/vepa (local clone /workspace/vepa)',version=open(REPO+'/VERSION').read().strip(),
  head=subprocess.check_output(['git','-C',REPO,'rev-parse','--short','HEAD']).decode().strip(),
  generated=subprocess.check_output(['date','+%Y-%m-%d %H:%M']).decode().strip()+' (AEST, UTC+10); branch codey/complete-plans',
  completionFormula="(Done + 0.5 × Partial) / (all items − Superseded − Won't do − Unknown)",
  completionPct=round(100*(done+0.5*part)/len(actionable),1),
  strictDonePct=round(100*done/len(actionable),1),
  statusCounts=counts,itemCount=len(I),docRecordCount=len(D),docFileCount=sum(d['fileCount'] for d in D))
json.dump(dict(meta=meta,documents=D,items=I),open('/workspace/vepa-plans/items.json','w'),indent=1,ensure_ascii=False)
print(json.dumps(meta,indent=1))

# ---- Embed referenced files + vendored libs and render index.html from template.html
import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import embed; embed.main()
