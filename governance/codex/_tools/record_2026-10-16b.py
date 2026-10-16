#!/usr/bin/env python3
"""Record Gem's 11:02am approval of the 8 drafts waiting on Gem (16 Oct). All checks first, then writes.
New vNNN.md only (never overwrites); appends CHANGELOG rows; updates index; writes deploy_manifest_2026-10-16b.json."""
import re, json, hashlib, sys
from pathlib import Path
G = Path('/workspace/governance'); C = G/'codex'; PR = G/'proposals/2026-10-16'
Q = "\"Yes, I approve all 8 drafts waiting on me. Record and deploy them.\""
APPR = (f"Gem, directly in Archivist's chat 16 Oct 2026 11:02am AEST ({Q}). Recorded in approvals/2026-10-16-gem-direct-words.md at 11:02:55, before any deploy (R-029). "
        "Context only (not the approval): Arbiter's relay of Gem's 9:25am words (R-008).")
AUTHOR = 'Architect (id 51af1200-ca1a-45ff-8350-848091e00f96)'
ITEMS = [  # proposal, folder, version, file sha prefix, extra reason
 ('scorer-v004', 'assessor', 'v004', '1ba3ef7b9152', ' Approver Gem: Scorer checks Imitator (R-027).'),
 ('scrutineer-v004', 'auditor', 'v004', '090cb2a3b6a7', ' Approver Gem: Scrutineer checks Imitator (R-027). Supersedes proposals/2026-10-09/scrutineer-v004.md.'),
 ('safekeeper-v005', 'secrets-credentials-custodian', 'v005', '395e82216689', ' Approver Gem: Safekeeper checks Imitator (R-027).'),
 ('imitator-v006', 'clone', 'v006', '01775c06964e', ' Approver Gem only: a change to Imitator itself (R-015).'),
 ('inferer-v005', 'identity-inferer', 'v005', '8b0d0c026d7d', ' J5 default: one owner-only file /home/box/id-private/gem-profile.md; the existing shared copy /workspace/id-notes/gem-profile.md is left for Gem to decide.'),
 ('archivist-v007', 'codex-keeper', 'v007', '5e3dc343bde3', ' D1 default: Archivist is the permanent owner of directory.md (R-021); approved as a pair with explorer-copy v003. Self-brief: approved by Gem directly.'),
 ('explorer-v003', 'explorer-copy', 'v003', 'b27fc4cf9726', ' Approved as a pair with codex-keeper v007 (Archivist owns directory.md; Explorer keeps phases.md).'),
 ('message-verification-rule-v003', '_shared/message-verification-rule', 'v003', '99969a87b2b6', ' Shared rule, owner Safekeeper; recorded only, nothing to deploy.'),
]
def block(t):
    a = t.split('## Exact instructions (verbatim)') if '## Exact instructions (verbatim)' in t else t.split('## Exact text (verbatim)')
    assert len(a) == 2; f = re.findall(r'```text\n(.*?)\n```', a[1], re.S); assert len(f) == 1; return f[0]
directory = (G/'directory.md').read_text(); plan = []
for prop, folder, ver, fsha, extra in ITEMS:
    raw = (PR/f'{prop}.md').read_bytes(); h = hashlib.sha256(raw).hexdigest(); assert h.startswith(fsha), (prop, h[:12])
    t = raw.decode(); text = block(t); sha = hashlib.sha256(text.encode()).hexdigest()
    m = re.search(r'base sha256 (\w+); draft sha256 (\w+)', t); assert sha.startswith(m.group(2)), prop
    nums = sorted(int(p.stem[1:]) for p in (C/folder).glob('v[0-9][0-9][0-9].md')); prev = f'v{nums[-1]:03d}'
    assert int(ver[1:]) == nums[-1] + 1 and not (C/folder/f'{ver}.md').exists(), (prop, prev)
    base = block((C/folder/f'{prev}.md').read_text()); assert hashlib.sha256(base.encode()).hexdigest().startswith(m.group(1)), prop
    rebuilt = base
    for o, n in re.findall(r'- Old: "(.*?)"\n\s+- New: "(.*?)"', t):
        assert rebuilt.count(o) == 1, (prop, o[:50]); rebuilt = rebuilt.replace(o, n)
    assert rebuilt == text, (prop, 'old->new rebuild differs')
    shared = folder.startswith('_shared')
    aid = name = None
    if not shared:
        aid = re.search(r'(?:id|agent) `([0-9a-f-]{36})`', t).group(1); assert aid in directory, prop
        live = json.loads((Path('/home/box/agent-data/agents')/aid/'profile.json').read_text())
        assert live['description'] == base, (prop, 'live != base'); name = live['name']
    title = re.match(r'# (.+?)\n', t).group(1)
    reason = title.split(' — ')[1] + '.' + extra
    plan.append(dict(prop=prop, folder=folder, ver=ver, prev=prev, raw=raw, text=text, sha=sha, aid=aid, name=name, reason=reason, shared=shared))
    print('CHECK OK', prop, folder, prev, '->', ver, len(text), sha[:12], name or '(shared)')
if '--check' in sys.argv: sys.exit(0)
idx = (C/'index.md').read_text(); manifest = []
for p in plan:
    folder, ver = p['folder'], p['ver']
    if p['shared']:
        hdr = (f"# Shared: Message verification & safety rule {ver}\n\n| Field | Value |\n|---|---|\n| Entry | Message verification & safety rule (shared governance document, not any one bot's instructions) |\n"
               f"| Version | {int(ver[1:])} |\n| Date | 2026-10-16 (AEST, UTC+10) |\n| Author | {AUTHOR} |\n| Reason | {p['reason']} |\n| Approved by | {APPR} |\n"
               f"| Source | /workspace/governance/proposals/2026-10-16/{p['prop']}.md (file sha256 {hashlib.sha256(p['raw']).hexdigest()[:12]}) |\n| Owner | P1 (Checks) Safekeeper (52772b1d-4a85-4ea3-ae15-f3912c901a3b) |\n"
               f"| Previous version | {p['prev']}.md |\n| Status | APPROVED. Shared document; bots refer to it from their own instructions. Not a profile, so nothing to deploy. |\n\n## Exact text (verbatim)\n\n")
        body = hdr + "The fenced block below is the approved text copied exactly from the proposal's fenced 'Exact instructions (verbatim)' block, character for character (no trailing newline added inside the text).\n\n```text\n" + p['text'] + "\n```\n"
    else:
        body = (f"# {p['name']}: instructions {ver}\n\n| Field | Value |\n|---|---|\n| Bot name | {p['name']} |\n| Bot id | {p['aid']} |\n| Title | (none) |\n| Version | {int(ver[1:])} |\n"
                f"| Date | 2026-10-16 (AEST, UTC+10) |\n| Author | {AUTHOR} |\n| Reason | {p['reason']} |\n| Approved by | {APPR} |\n"
                f"| Source | /workspace/governance/proposals/2026-10-16/{p['prop']}.md (file sha256 {hashlib.sha256(p['raw']).hexdigest()[:12]}; recorded as {ver}.md, the next number in this folder) |\n"
                f"| Previous version | {p['prev']}.md |\n| Status | APPROVED, NOT DEPLOYED at recording (16 Oct 2026 AEST). After recording, deployment status is in CHANGELOG.md, which is authoritative. |\n\n"
                "## Exact instructions (verbatim)\n\nThe fenced block below is the approved instruction text copied exactly from the proposal's fenced 'Exact instructions (verbatim)' block, character for character (no trailing newline added inside the text).\n\n"
                f"```text\n{p['text']}\n```\n\n## Template sections\n\nNO-TEMPLATE-SECTIONS-IN-PROPOSAL: the approved proposal has no template sections, so none are invented here. The verbatim block above is authoritative.\n\n"
                + ''.join(f"### {s}\n(Not provided in the approved proposal; see the verbatim block above.)\n\n" for s in ['Purpose', 'Scope', 'Rules', 'Relationships', 'Limits']).rstrip('\n') + '\n')
    vf = C/folder/f'{ver}.md'; assert not vf.exists(); vf.write_text(body); assert block(vf.read_text()) == p['text']
    cl = C/folder/'CHANGELOG.md'; c = cl.read_text().rstrip('\n') + '\n'
    c += f"| {int(ver[1:])} | 2026-10-16 (AEST, UTC+10) | {AUTHOR} | {APPR} | {p['reason']} | {ver}.md |\n"
    if not p['shared']:
        c += (f"| (deployment status, no version change) | 2026-10-16 (AEST, UTC+10) | Archivist | n/a | PENDING-DEPLOY {ver}.md: approved; Gem asked for deployment at 11:02am AEST 16 Oct 2026 ({Q}); "
              f"Gem's words recorded before deploying (R-029); not yet applied to the live profile ({p['aid']} still runs {p['prev']}.md). | (no new file) |\n")
    cl.write_text(c)
    lines = idx.split('\n'); hit = 0
    for i, l in enumerate(lines):
        cells = l.split(' | ')
        if p['shared'] and l.startswith('| Message verification & safety rule |'):
            cells[2] = ver; cells[3] = '2026-10-16'; cells[4] = "Gem, directly in Archivist's chat 16 Oct 2026 11:02am AEST"; lines[i] = ' | '.join(cells); hit += 1
        elif not p['shared'] and l.startswith('|') and len(cells) > 8 and cells[2] == p['aid']:
            cells[3] = f'[{folder}/]({folder}/{ver}.md)'; cells[4] = ver; cells[5] = '2026-10-16'; cells[6] = 'APPROVED (PENDING-DEPLOY)'
            cells[8] = (f"APPROVED {ver} by Gem (11:02am 16 Oct, Archivist's chat: {Q}); Gem asked for deployment; NOT yet deployed (live still runs {p['prev']}). {p['reason']} Earlier: " + cells[8])
            lines[i] = ' | '.join(cells); hit += 1
    assert hit == 1, (p['prop'], hit); idx = '\n'.join(lines)
    if not p['shared']:
        manifest.append({'folder': folder, 'agentId': p['aid'], 'name': p['name'], 'version': ver, 'field': 'description', 'text': p['text'], 'sha256': p['sha'], 'chars': len(p['text'])})
# architect-v004: Gem confirmed both R-028 items
cl = C/'instruction-architect/CHANGELOG.md'; c = cl.read_text(); assert 'Gem confirmed both R-028 items' not in c
c = c.rstrip('\n') + '\n' + ("| (approval status, no version change) | 2026-10-16 (AEST, UTC+10) | Archivist | Gem, directly in Archivist's chat 16 Oct 2026, before 11:02am AEST (exact time not visible), answering Archivist's R-028 card: "
     "\"Yes, I confirm both: the routing to Imitator and the 3-a-week cap\" | Gem confirmed both R-028 items in v004.md: (1) the routing change (non-checker proposals go to Imitator only); (2) the A5c weekly cap (about 3 proposals a week, 2-week trial). "
     "All of v004 now stands approved; no text change, no redeploy needed (live since 09:14:41). Gem's words recorded in approvals/2026-10-16-gem-direct-words.md at 11:02:55. | (no new file) |\n")
cl.write_text(c)
lines = idx.split('\n'); hit = 0
for i, l in enumerate(lines):
    cells = l.split(' | ')
    if l.startswith('|') and len(cells) > 8 and cells[2] == '51af1200-ca1a-45ff-8350-848091e00f96':
        cells[6] = 'OK (LIVE)'
        cells[8] = re.sub(r"^LIVE v004; 2 changes await Gem's confirmation \(R-028\):.*?See CHANGELOG\. ",
                          "LIVE v004 (deployed 16 Oct 2026 at 09:14:41 AEST). Gem confirmed both R-028 items (Imitator-only routing, A5c weekly cap) in Archivist's chat before 11:02am 16 Oct; all of v004 approved. ", cells[8])
        assert cells[8].startswith('LIVE v004 (deployed'); lines[i] = ' | '.join(cells); hit += 1
assert hit == 1; idx = '\n'.join(lines)
idx = idx.replace("- **R-029 record-keeping lapse (16 Oct).**", "- **R-029 record-keeping lapse (16 Oct).** Follow-up: for the 11:02am approval, Gem's words were recorded at 11:02:55, before any deploy.", 1)
idx = idx.replace("R-028: architect-v004's routing change and A5c cap await Gem).", "R-028: architect-v004's routing change and A5c cap awaited Gem; Gem confirmed both before 11:02am).", 1)
idx = idx.replace("Scrutineer's fix, `proposals/2026-10-16/scrutineer-v004.md`, goes to Gem under R-027 and isn't approved.", "Scrutineer's fix, `auditor/v004`, was approved by Gem at 11:02am and removes every Assembler mention; close once deployed.", 1)
idx = re.sub(r'^Last rebuilt: .*$', "Last rebuilt: 2026-10-16 (AEST, UTC+10) ~11:05am. Gem approved the 8 drafts waiting on Gem at 11:02am (assessor v004, auditor v004, secrets-credentials-custodian v005, clone v006, identity-inferer v005, codex-keeper v007, explorer-copy v003: PENDING-DEPLOY; shared message-verification-rule v003 recorded only). architect-v004's R-028 items confirmed by Gem. Rows: 37.", idx, count=1, flags=re.M)
(C/'index.md').write_text(idx)
(C/'_tools/deploy_manifest_2026-10-16b.json').write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + '\n')
for e in manifest: print('MANIFEST', e['agentId'], e['name'], e['folder'], e['version'], e['chars'], e['sha256'][:12])
