import json, collections
st=json.load(open('/tmp/codey_state.json')); rows=st['rows']; acmap=st['acmap']
items={i['id']:i for i in json.load(open('../items.json'))['items']}
BATCH_ORDER=['B1','B2','B3','B4','B5','B6','B7','B8','B9','B10','B11','—']
BN={'B1':'Doc & stale-claim fixes','B2':'Spec generator & help correctness','B3':'Small code de-duplication',
 'B4':'Tests, envelopes & CI controls','B5':'Provenance & exports','B6':'Law ontology & semantics (metadata/tests, no behaviour change)',
 'B7':'Civilisation wiring of existing libraries','B8':'New civilisation systems (default-off)','B9':'Architecture refactors',
 'B10':'External: real GPU hardware & publishing','B11':'Feature sets Q–T','—':"Recommended Won't do / reclassify"}
DAYS={'S':0.5,'M':1.5,'L':4,'XL':8}
VER={
'B1':"Verifier writes a scratch check script outside the repo (grep for stale strings, a Markdown link checker over non-.old docs, compares SPEC.md/AGENTS.md counts with its own `vitest run` output). Adversarial per AC: e.g. a link with an anchor/relative `../`, a stale count hidden in a table cell. FSM-SAVE: new test is a **weak** PASS (same-diff test), so the verifier also hand-loads a crafted v2 save in a scratch script.",
'B2':"Verifier runs `npm run spec:generate` into a scratch copy and `npm run spec:check`, reads coverage-gaps.md itself, and diffs merged help text before/after (snapshot of `LAW_HELP_DB` serialised in scratch). Adversarial: a law with only a patch entry; a help string containing a quote/brace; CG-5 toggles ELECTRIC_FIELD alone and FIELD alone and compares accelerations. CG-5 is a behaviour change, so it needs the Q4 decision line before build.",
'B3':"Golden-parity fixture must exist first (built at the start of this batch, part of DP-P2a): deterministic seed → N ticks → SHA-256 of the particle buffer. Verifier reruns the full suite plus the golden hash on base and on HEAD; any hash change is FAIL. Adversarial: edge DNA values (0, 65535) through the codec; mismatched cipher keys; panels mounted with missing DOM nodes.",
'B4':"Verifier runs vitest, `npm run bench:backends:json`, `npm run test:e2e` (headless chromium on the box) and every new CI command locally. Any change to deploy.yml / vitest or playwright config is flagged; thresholds may not be loosened (BH-ENV must hit ≤ 0.1, not move the bar) unless an ACTIVE decision says so (Q7). New tests are weak PASSes, so each AC gets an independent scratch check (e.g. a hand-computed two-particle pair geometry, a 2048-particle BH run with a different seed).",
'B5':"Verifier reruns `provenance:check`, `exports:check`, `audit:inventory`, `artifact:inventory` and the new reconciliation script; it deletes one provenance header in a scratch copy to confirm the check fails (adversarial). ARP-10's regenerated 2.3 MB snapshot is checked by header + generator determinism (run twice, same hash).",
'B6':"Metadata must be derived from code, so the verifier spot-checks ≥10 random ontology records against the implementing function (file:line) and reruns registry validation. Golden hash must be unchanged (no behaviour change allowed in this batch). Adversarial: a declared budget field the law never writes; an undeclared write (AUD-STC guard must catch it).",
'B7':"Runtime wiring is checked in a live run, not only unit tests: verifier runs a headless worker/e2e session (or a scripted main-loop harness) for N ticks and asserts kin edges / households / polities appear, then save → restore → equal. Adversarial: particle index reuse after death (stale kin edge must not attach to a newborn), restore of a pre-feature save. Golden hash with civ features off must be unchanged.",
'B8':"Each system ships default-off (P-10). Verifier runs golden hash with the toggle off (must match base) and scenario tests with it on. Adversarial per AC: resource conservation in MD-ECON under bankruptcy; IG-MATE with a single eligible particle; CIV-4b structure at world boundary. Any behaviour change with the toggle off is FAIL.",
'B9':"Strictly behaviour-preserving: golden hash identical before/after every step, full suite green, `bench:backends` envelopes unchanged, render/solver benchmark within 5% of baseline (Playwright SwiftShader for A10). One step per commit so a FAIL is bisectable. A9 follows A9-MIGRATION-PLAN step order; partial migration is never left in HEAD. Adversarial: the guard test is run against a deliberately re-introduced singleton in a scratch copy and must fail.",
'B10':"Cannot be verified on the box (no GPU; publishing is irreversible). Verifier marks these UNVERIFIED → 'done pending your check'. Harness pieces (device-report writer, workflow file) can be checked statically. AUD-PUB never runs without its own ACTIVE decision covering that publish.",
'B11':"Product features: prototype first on `codey/proto-cosmology` (P-11), Gem chooses, then build from repo truth. Each set gets scenario tests + an e2e smoke; verifier checks determinism (same seed → same epoch journal) and the undo/reversibility risks listed in the trilogy intents.",
'—':"No build planned unless Gem rejects the reclassification; if reclassified, the verifier only checks that the table/status and reason are recorded.",
}
by=collections.defaultdict(list)
for t in rows: by[t[3]].append(t)
size=collections.Counter(t[1] for t in rows)
O=[]
w=O.append
w("# PLAN — I-complete-plans (planning only, nothing built yet)\n")
w(f"_Drafted by Codey {st['now']} (AEST). Agent interpretation (truth tier 4): this file is ephemeral, gitignored, and is **never** shown to the verifier. The intent (`.codey/intent.md`) and decisions are the only durable state._\n")
w("## 0. Where things stand\n")
w("- Branch `codey/complete-plans` created from `main` @ `436afd2`; commit `047194a` **chore: move outdated docs to .old** (18 renames + `.old/README.md`). Local only — not pushed.")
w("- Baseline on the branch: `vitest run` → **129 files / 1431 tests passed** (Node 20.19.2 on the box; CI uses Node 22, so Node 22 must be installed before verification — AC-87).")
w("- `.codey/` set up per Codey 3.1: `intent.md` (draft, **unconfirmed**), `decisions.jsonl` (D-001), `checkpoint.json` (phase `clarify`, gitignored), `lock` (gitignored). `.gitignore` gained the Codey entries. None of this is committed yet; I'd commit `intent.md` + `decisions.jsonl` + `.gitignore` once Gem confirms.")
w("- **Run phase: clarify.** No build until Gem answers the questions (QUESTIONS file) and confirms the intent hash.\n")
w("## 1. Counts\n")
w(f"86 items (40 Partial, 46 Not started). By size: **S {size['S']} · M {size['M']} · L {size['L']} · XL {size['XL']}**. Rough effort at S=0.5 d, M=1.5 d, L=4 d, XL=8 d agent-days: **≈{sum(DAYS[t[1]] for t in rows):.0f} agent-days** if everything is built; ≈{sum(DAYS[t[1]] for t in rows if t[3] not in ('—','B11','B10')):.0f} days excluding the four Won't-do recommendations, the Q–T feature sets and the hardware/publishing items.\n")
w("| Batch | Name | Items | S/M/L/XL | ≈days | Needs decision |")
w("|---|---|---:|---|---:|---|")
for b in BATCH_ORDER:
    l=by[b]; c=collections.Counter(t[1] for t in l)
    qs=sorted({t[5] for t in l if t[5]})
    w(f"| {b} | {BN[b]} | {len(l)} | {c['S']}/{c['M']}/{c['L']}/{c['XL']} | {sum(DAYS[t[1]] for t in l):.1f} | {', '.join(qs) or '—'} |")
w("")
w("## 2. Key findings from reading the code\n")
for f in [
"**SPEC-HELP is a real bug, confirmed.** `scripts/generate-spec.mjs` extracts LAW_HELP_DB with `/\\[(\\d+)\\]:\\s*\\{…\\}/` and single-quoted fields, but `src/constants/help.js` uses `NAME: { hint: \"…\" }`. Fixing CA-H8 (import the catalog as a module) fixes SPEC-HELP for free, and will regenerate much of `docs/spec/` (large but mechanical diff).",
"**CG-5 is a real bug, newly found.** `ELECTRIC_FIELD` (index 54) has no runtime consumer at all. The per-particle electromagnetism block in `src/physics/solver.js:1384` gates `applyFieldDrift` on `FIELD` (87), so FIELD runs *both* the central gradient (l.1200) and the EM polarity drift, and the ELECTRIC_FIELD toggle does nothing. The canonical help for FIELD describes the polarity drift while `lawHelpPatches.js` says FIELD is the central gradient — the two help sources disagree. Fixing it changes behaviour, hence Q4.",
"**Civilisation libraries are tested but unwired (CIV-1/2/POL).** `recordKin`, `createHousehold`, `foundPolity` etc. have no caller in `src/` outside `civilization.js`. The hook is easy: `spawnOffspring()` in `main.js` already calls `trackBirth(…, off.parentId, …)`. The real risk is identity: particles are addressed by buffer index, and indices are reused, so kin edges need stable IDs (or a death hook that clears edges).",
"**The 10 SYS-* items are umbrella items** over the same work as CIV-*, IG-*, MD-*. As written (\"phases 2–6\") each is XL and vague; `docs/systems/roadmap-overview.md` itself says Phases 1–5 exist as a shared substrate and only *domain adapters* remain. Hence Q5.",
"**The decomposition items (DP-P1…P8, A9–A12) are explicitly gated.** `docs/DECOMPOSITION_PLAN.md` is marked \"PROPOSED — awaiting review… only then do the extractions start\". A11 ≡ DP §6 P5; DP-P4 is the first step of A12; A9 must precede DP-P1 (splitting laws.js first would spread the singleton across files). Hence Q3.",
"**FMM-PROMO conflicts with a recorded decision** — `docs/BACKEND_ENVELOPES.md` §3: \"Decision: RETAIN EXPERIMENTAL\". Its error (rmsRelative 1.15–2.02) is *worse* than plain Barnes–Hut (≤0.1), which looks like a defect rather than a tuning gap.",
"**RRP-Q…T were designed on 2026-08-19 for v8.17–8.20.** Those version numbers have since shipped other work (now 9.1.27), and the docs assume a full 128-law budget (now 136). They are large product/design features (heat death, god-mode, self-aware species).",
"**Hardware-gated:** ARP-2 and RB-1 need a real GPU; the box has none (`nvidia-smi` absent, e2e GPU test self-skips). AUD-PUB needs a new GitHub repo, CI secrets and a push — outside the box and irreversible.",
"**Small quick wins confirmed:** laws.js:37 `isAccretionLink` is a byte-for-byte copy of `mergePhysics.isAccretionPair` (plus a dead `return false`); `cipherKeyFromStride` duplicates `laws.cipherKey`; main.js:698 still dequantises DNA inline; `audit-suite` appears 11× in AGENTS.md (0 in GEMINI.md now); README links `../audit/FULL_AUDIT_2026-08-01.md` (outside repo); GUIDE.md links missing `docs/expansion/batches/`.",
"**Bars and 'green':** the table's % excludes Superseded/Unknown, but the stacked bars still draw those segments in their own colours, and the 2 Unknown items (CG-2, SPEC-AC4) are outside the 86. Hence Q1 and P-6/P-8.",
]: w("- "+f)
w("")
w("## 3. Triage — all 86 items\n")
w("Columns: AC = criterion in intent.md · Size · Risk · Recommendation · Decision = question that must be answered first · Deps.\n")
for b in BATCH_ORDER:
    w(f"### {b} — {BN[b]}\n")
    w("| AC | Item | Status | Size | Risk | Recommendation | Decision | Deps | What's needed |")
    w("|---|---|---|---|---|---|---|---|---|")
    for t in by[b]:
        it=items[t[0]]
        need=t[7].replace('|','\\|')
        w(f"| {acmap[t[0]]} | **{t[0]}** — {it['title'].replace('|','/')} | {it['status']} | {t[1]} | {t[2]} | {t[4]} | {t[5] or '—'} | {t[6] or '—'} | {need} |")
    w("")
w("## 4. Reclassification recommendations (Superseded / Won't do)\n")
for x in [
"**DP-P8 → Won't do.** DECOMPOSITION_PLAN P8 is optional by design (\"only if touched\").",
"**IS-1 → Won't do.** The design note is conditional (\"until a graph buffer is introduced\"); adding a solver-path buffer is an XL hot-path change with no feature asking for it.",
"**CIV-7 → Won't do (or redefine).** A \"learned culture-transmission model\" has no spec and is research; cross-world federation persistence could be a separate small item.",
"**FMM-PROMO → Won't do, per the existing RETAIN EXPERIMENTAL decision** — after a 1-day time-boxed bug hunt (Q7).",
"**AUD-PUB → Won't do in this intent** (new repo, secrets, push; irreversible). ARP-2 / RB-1 → hardware-gated: harness here, Gem runs it (Q6).",
"**RRP-Q…T → Superseded candidates** if Gem no longer wants the Aug-2026 trilogy direction (Q2).",
"**SYS-* (10) → Superseded candidates** if Gem prefers to track only the concrete CIV/IG/MD items (Q5 option C).",
]: w("- "+x)
w("\nReclassifying is Gem's decision (it narrows D-001), so each one needs a decision line; until then the matching AC stands.\n")
w("## 5. Doc-only items\n")
w("AG-1, ARP-12, DAC-1, CA-H7, ESP-1, CG-3 are pure documentation. AUD-EXACT, LC-1 and FSM-SAVE are almost entirely doc/comment/string changes plus a small test. ACO-3 is a decision followed by a doc update. Together: 10 items, ≈5 agent-days at most, all in B1/B5.\n")
w("## 6. Batch plan (order and gates)\n")
order_note={
'B1':"First: no behaviour risk, removes stale claims that would otherwise mislead later work. Counts in AGENTS/SPEC get a second refresh at the very end (AC-87).",
'B2':"SPEC-HELP via CA-H8, then CG-1, then CG-5 (after Q4). Regenerates docs/spec.",
'B3':"Starts by building the golden-parity fixture (first half of DP-P2a) so every later code change has a behaviour oracle.",
'B4':"Needs Playwright chromium installed on the box (`npx playwright install chromium`, an external download → retried once on failure, then escalated). CI edits are local only.",
'B5':"ACO-3 waits on Q8. AUD-PUB moved to B10.",
'B6':"ARP-7 first (everything else reads the ontology). No behaviour change permitted; golden hash must match.",
'B7':"After Q5. CIV-2 → CIV-1 → CIV-POL → MD-CULT → MD-REL; SYS-* items close as their adapters land.",
'B8':"After Q5; default-off toggles (P-10).",
'B9':"After Q3. Order: DP-P2a → A9 → DP-P1 → DP-P2b → DP-P2c → DP-P4 → A12 → A11 → DP-P6 → DP-P7 → A10. One step per commit.",
'B10':"Harness work can run alongside B4; the hardware runs and any publish are Gem's.",
'B11':"After Q2; prototype first.",
'—':"Only if Gem rejects the reclassification.",
}
for b in BATCH_ORDER:
    l=by[b]
    w(f"### {b} — {BN[b]} ({len(l)} items, ≈{sum(DAYS[t[1]] for t in l):.1f} agent-days)")
    w(f"- Items: {', '.join(t[0] for t in l)}")
    w(f"- Order/gates: {order_note[b]}")
    w(f"- Verification: {VER[b]}\n")
w("## 7. Verification rules applied to every batch (Codey 3.1 §3.3)\n")
for x in [
"Fresh-context verifier, fixed prompt, read-only on the repo; it runs the tests itself and sees only the confirmed intent (Proposed stripped), ACTIVE decisions, the diff against `047194a`, and its own output. It never sees this PLAN.",
"Verdict per AC: PASS / FAIL / UNVERIFIED with command, output excerpt and file:line.",
"Gamed-test flags: any added, weakened or skipped test, any change to vitest/playwright config or deploy.yml is listed. A weakened or skipped existing test without an ACTIVE decision → that AC is FAIL.",
"Weak PASS when the only evidence is a test written in the same diff — expected for most B4/B6 items, so each gets an independent scratch check.",
"One adversarial check per AC (listed per batch above).",
"No tests ⇒ UNVERIFIED, never PASS; doc items are checked by scratch scripts; hardware items end as \"done pending your check\".",
"Bounded repair: max 3 attempts per failure, early stop on a repeated failure signature; external failures (npm/Playwright downloads, GPU absence) are escalated, never coded around.",
"Checkpoint drift check before every change and every verification; checkpoint rewritten after every Codey write.",
]: w("- "+x)
w("")
w("## 8. Irreversibility gate (§4) — actions that will need their own decision\n")
for x in ["Any `git push`, PR, gh-pages/Vercel deploy, or publishing to a vepa-exports repo (AUD-PUB).",
          "Deleting files outside the task's diff — e.g. removing `src/state/lawHelpPatches.js` is inside the diff (CG-1) and is fine; moving `docs/audit/laws/a3` (Q8 option B/C) is not.",
          "Major dependency bumps (none planned). Secrets: none needed for any planned batch except AUD-PUB.",
          "Note: the world-save format (FSM-SAVE, CIV-*) is local data, not a migration of a database; old saves must still load (tested), so no gate is triggered unless WORLD_SAVE_VERSION changes."]: w("- "+x)
w("")
w("## 9. Risks\n")
for x in ["Particle-index reuse breaks kin/polity identity (B7) — needs stable IDs first.",
          "docs/spec regeneration (B2) produces a very large diff; reviewed by generator determinism, not line by line.",
          "Solver refactors (B9) are the highest regression risk; mitigated by the golden fixture and one-step commits.",
          "Playwright in CI may be flaky; e2e job uses retries=0 locally for verification so flakiness surfaces.",
          "Scale: ≈200+ agent-days if everything is built. Even with the recommended reclassifications it is a multi-week programme; I'd verify and report after each batch so Gem can stop at any point."]: w("- "+x)
w("\n## 10. Next step\n\nGem answers the questions in `.codey/QUESTIONS-complete-plans.md`. Each answer becomes a decision line (D-002…); I update the affected ACs, Gem confirms the intent (an `intent_confirmed` line with the new hash), and Batch 1 starts.\n")
open('/workspace/vepa/.codey/PLAN-complete-plans.md','w').write('\n'.join(O))
print(size, sum(DAYS[t[1]] for t in rows))
for b in BATCH_ORDER:
    l=by[b]; print(b, BN[b], len(l), sum(DAYS[t[1]] for t in l), collections.Counter(t[1] for t in l))
