import json, collections, subprocess, os, datetime
exec(open('triage_final.py').read())
items = {i['id']: i for i in json.load(open('../items.json'))['items']}
REPO = '/workspace/vepa'
NOW = subprocess.check_output(['date','-Iseconds']).decode().strip()
BATCH_ORDER = ['B1','B2','B3','B4','B5','B6','B7','B8','B9','B10','B11','—']
BATCH_NAME = {
 'B1':'Doc & stale-claim fixes','B2':'Spec generator & help correctness','B3':'Small code de-duplication',
 'B4':'Tests, envelopes & CI controls','B5':'Provenance & exports','B6':'Law ontology & semantics (metadata/tests, no behaviour change)',
 'B7':'Civilisation wiring of existing libraries','B8':'New civilisation systems (default-off)','B9':'Architecture refactors (gated by DECOMPOSITION_PLAN approval)',
 'B10':'External: real GPU hardware & publishing','B11':'Feature sets Q–T (product decision)','—':'Recommended Won\'t do / reclassify'}
DAYS = {'S':0.5,'M':1.5,'L':4,'XL':8}
rows = sorted(T, key=lambda t: (BATCH_ORDER.index(t[3]), [x[0] for x in T].index(t[0])))
acmap = {}
for n,t in enumerate(rows,1): acmap[t[0]] = f'AC-{n}'

# ---------------- intent.md
L=[]
L.append('# I-complete-plans: Implement every Partial and Not started plan item in vepa\n')
L.append('## Goal')
L.append('Bring all 86 Partial (40) and Not started (46) items listed in `/workspace/vepa-plans/items.json` to Done in this local clone, so every progress bar in the vepa plans table is green. Work stays local on branch `codey/complete-plans`; nothing is pushed, published or deployed.\n')
L.append('Each criterion below maps to exactly one item ID (in brackets). Status in the table is re-derived from the code after the verifier runs, never from the builder\'s claims.\n')
L.append('## Acceptance Criteria')
cur=None
for t in rows:
    b=t[3]
    if b!=cur:
        cur=b; L.append(f'\n### {b if b!="—" else "R"} — {BATCH_NAME[b]}' if b!='—' else f'\n### Items Codey recommends reclassifying (see P-1…P-5; criteria stand until Gem decides)')
    L.append(f'- {acmap[t[0]]} [{t[0]}]: {t[8]}')
L.append('\n### Cross-cutting')
L.append(f'- AC-{len(rows)+1} [ALL]: After the final batch, `npm test`, `npm run repository:check` and `npm run build` all pass on Node 22, with no existing test weakened, skipped or deleted unless an ACTIVE decision authorises it.')
L.append(f'- AC-{len(rows)+2} [ALL]: Every refactor batch preserves simulation behaviour: the golden-parity fixture (from AC for DP-P2a) produces the same hash before and after, except where an ACTIVE decision authorises a behaviour change.')
L.append('\n## Scope')
for p in ['src/','tests/','scripts/','bench/','docs/ (not .old/)','exports/','.github/workflows/','Root docs: AGENTS.md, README.md, SPEC.md, GUIDE.md, PLAN.md, GEMINI.md','package.json scripts (no dependency version changes)']:
    L.append(f'- {p}')
L.append('\n## Out of Scope')
for p in ['Pushing, opening PRs, deploying to gh-pages/Vercel, or publishing anywhere (all irreversible; each needs its own decision).',
          'Version bumps, release entries and the AGENTS.md §10.4 release ritual.',
          'Major dependency upgrades and fixing the 5 `npm audit` advisories.',
          'The 47 Done, 6 Superseded and 2 Unknown items (CG-2, SPEC-AC4), unless Gem adopts P-8.',
          'Editing historical CHANGELOG.md entries or files under .old/ (other than .old/README.md).',
          'Regenerating the plans table itself; that is a reporting step done after verification.']:
    L.append(f'- {p}')
L.append('\n## Proposed (unconfirmed)')
props = [
 'P-1: Reclassify DP-P8 (split paramHelp.js/ui.js) as Won\'t do — the plan itself says "only if touched".',
 'P-2: Reclassify IS-1 (graph buffer for relationship state) as Won\'t do — conditional in the design note, adds a hot-path buffer with no driving need.',
 'P-3: Reclassify CIV-7 as Won\'t do (the "learned culture model" is open research); keep cross-world federation persistence as a new small item if wanted.',
 'P-4: Reclassify FMM-PROMO as Won\'t do per the existing recorded "RETAIN EXPERIMENTAL" FMM decision, after a 1-day time-boxed bug hunt (rmsRelative 1.15–2.02 is worse than plain Barnes–Hut, which suggests a defect).',
 'P-5: Treat ARP-2 and RB-1 as hardware-gated: build the harness here, Gem runs it on a real GPU; reclassify AUD-PUB as Won\'t do for this intent (needs a new repo, secrets and pushes).',
 'P-6: Add a "Won\'t do" status to the plans table, excluded from the % like Superseded, and drop Superseded/Won\'t do segments from the bars so "all green" is visible.',
 'P-7: Accept gravEngine:\'reference\' as the new name with \'exact\' kept as a permanent alias (AUD-EXACT).',
 'P-8: Also close the 2 Unknown items (CG-2 help-tier contract test; SPEC-AC4 dashboard check via Playwright) so no bar has a grey segment.',
 'P-9: Define SYS-* "done" as one live domain adapter + save/restore + runtime test per system (not full phases 2–6).',
 'P-10: Ship new behaviour-changing civilisation systems (B8) behind default-off toggles, with a golden check that "off" is unchanged.',
 'P-11: Prototype Set Q (cosmology) on `codey/proto-cosmology` before building any of RRP-Q…T; decide R–T after seeing it.',
 'P-12: Gate every refactor on the golden-parity fixture; do A9 before DP-P1; stop on any golden-hash change.',
 'P-13: Fix links in AGENTS.md/PLAN.md that point at files moved to .old/; leave CHANGELOG.md history untouched.',
 'P-14: Fix CG-5 by gating the EM drift on ELECTRIC_FIELD only and adding ELECTRIC_FIELD to the "ELECTRIC STORM" preset.',
]
L += ['- '+p for p in props]
open(f'{REPO}/.codey/intent.md','w').write('\n'.join(L)+'\n')

# ---------------- decisions.jsonl
D = {"schema":1,"id":"D-001","intent":"I-complete-plans","type":"decision","scope":"task",
     "question":"What should this task cover?",
     "decision":"Address all partial and not started items so every bar is green (all 40 Partial and 46 Not started items in /workspace/vepa-plans/items.json).",
     "basis":"explicit","supersedes":[],"source":"human","timestamp":NOW}
open(f'{REPO}/.codey/decisions.jsonl','w').write(json.dumps(D,ensure_ascii=False)+'\n')

json.dump({'rows':rows,'acmap':acmap,'now':NOW,'props':props}, open('/tmp/codey_state.json','w'))
print('ACs', len(rows)+2)
