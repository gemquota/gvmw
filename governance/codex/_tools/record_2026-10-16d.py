#!/usr/bin/env python3
"""Record Gem's 11:41am approval of the 3 drafts in proposals/2026-10-16-deploy (16 Oct 2026).
Checks first (file hashes, base = latest codex = live, old->new rebuild, one fence), then writes. Manifest: deploy_manifest_2026-10-16c.json."""
import re, json, hashlib, sys
from pathlib import Path
G = Path('/workspace/governance'); C = G/'codex'; PR = G/'proposals/2026-10-16-deploy'
Q = "\"I approve all 3 drafts in proposals/2026-10-16-deploy. Record and deploy them.\""
APPR = (f"Gem, directly in Archivist's chat 16 Oct 2026 11:41am AEST ({Q}). Approver Gem directly (R-028: widens Imitator's effective power; R-027 for the Safekeeper-owned shared rule). "
        "Recorded in approvals/2026-10-16-gem-direct-words.md at 11:41:27, before any deploy (R-029). Context only (not the approval): Gem's 11:09am words in Explorer's chat, \"Yes, Imitator's approval is enough\", relayed to Architect by Explorer (R-008).")
AUTHOR = 'Architect (id 51af1200-ca1a-45ff-8350-848091e00f96)'
ITEMS = [  # prop, folder, ver, file sha prefix, agent id
 ('archivist-v008', 'codex-keeper', 'v008', '157b3f4a', '61ef3abd-87b8-49f1-b8d6-b52969afa315'),
 ('explorer-v005', 'explorer-copy', 'v005', 'f4f80c03', '04dcca0d-1479-4e01-bf29-a13b4fc3c3a7'),
 ('message-verification-rule-v004', '_shared/message-verification-rule', 'v004', '8bcacc54', None),
]
def block(t):
    k = '## Exact instructions (verbatim)' if '## Exact instructions (verbatim)' in t else '## Exact text (verbatim)'
    a = t.split(k); assert len(a) == 2; f = re.findall(r'```text\n(.*?)\n```', a[1], re.S); assert len(f) == 1, 'fence count'; return f[0]
def changes(t): return re.findall(r'^\s*- Old: "(.*)"[ \t]*\n\s*- New: "(.*)"[ \t]*$', t, re.M)  # whole line: values may contain inner quotes
plan = []
for prop, folder, ver, fsha, aid in ITEMS:
    raw = (PR/f'{prop}.md').read_bytes(); h = hashlib.sha256(raw).hexdigest(); assert h.startswith(fsha), (prop, h[:12])
    t = raw.decode(); assert t.count('```text') == 1, (prop, 'more than one text fence'); text = block(t); sha = hashlib.sha256(text.encode()).hexdigest()
    m = re.search(r'base sha256 (\w+); draft sha256 (\w+)', t); assert sha.startswith(m.group(2)), (prop, 'draft sha')
    nums = sorted(int(p.stem[1:]) for p in (C/folder).glob('v[0-9][0-9][0-9].md')); prev = f'v{nums[-1]:03d}'
    assert int(ver[1:]) == nums[-1] + 1 and not (C/folder/f'{ver}.md').exists(), (prop, prev)
    base = block((C/folder/f'{prev}.md').read_text()); assert hashlib.sha256(base.encode()).hexdigest().startswith(m.group(1)), (prop, 'base sha')
    r = base
    for o, n in changes(t): assert r.count(o) == 1, (prop, o[:50]); r = r.replace(o, n)
    assert r == text, (prop, 'rebuild'); assert changes(t), prop
    name = None
    if aid:
        assert aid in t
        live = json.loads((Path('/home/box/agent-data/agents')/aid/'profile.json').read_text()); name = live['name']
        assert live['description'] == base, (prop, 'live != base')
    title = re.match(r'# (.+?)\n', t).group(1); reason = title.split(' — ')[1] + '.'
    plan.append(dict(prop=prop, folder=folder, ver=ver, prev=prev, raw=raw, text=text, sha=sha, aid=aid, name=name, reason=reason, n=len(changes(t)), paras=text.count('\n\n'), nl=text.count('\n')))
    print('CHECK OK', prop, folder, prev, '->', ver, 'chars', len(text), sha, name or '(shared)', 'changes', len(changes(t)), 'newlines', text.count('\n'), 'blank-line breaks', text.count('\n\n'))
if '--check' in sys.argv: sys.exit(0)
idx = (C/'index.md').read_text(); lines = idx.split('\n')
for p in plan:
    folder, ver = p['folder'], p['ver']; src = f"/workspace/governance/proposals/2026-10-16-deploy/{p['prop']}.md (file sha256 {hashlib.sha256(p['raw']).hexdigest()[:12]})"
    if p['aid'] is None:
        body = (f"# Shared: Message verification & safety rule {ver}\n\n| Field | Value |\n|---|---|\n| Entry | Message verification & safety rule (shared governance document, not any one bot's instructions) |\n| Version | {int(ver[1:])} |\n| Date | 2026-10-16 (AEST, UTC+10) |\n"
                f"| Author | {AUTHOR} |\n| Reason | {p['reason']} Shared rule, owner Safekeeper; recorded only, nothing to deploy. |\n| Approved by | {APPR} |\n| Source | {src} |\n| Owner | P1 (Checks) Safekeeper (52772b1d-4a85-4ea3-ae15-f3912c901a3b) |\n| Previous version | {p['prev']}.md |\n"
                "| Status | APPROVED. Shared document; bots refer to it from their own instructions. Not a profile, so nothing to deploy. |\n\n## Exact text (verbatim)\n\n"
                "The fenced block below is the approved text copied exactly from the proposal's fenced 'Exact instructions (verbatim)' block, character for character (no trailing newline added inside the text).\n\n"
                f"```text\n{p['text']}\n```\n")
        cl = C/folder/'CHANGELOG.md'; c = cl.read_text().rstrip('\n') + '\n'
        c += f"| {int(ver[1:])} | 2026-10-16 (AEST, UTC+10) | {AUTHOR} | {APPR} | {p['reason']} Recorded only; not a profile, nothing to deploy. | {ver}.md |\n"; cl.write_text(c)
        hit = 0
        for i, l in enumerate(lines):
            if l.startswith('| Message verification & safety rule |'):
                lines[i] = (f"| Message verification & safety rule | `_shared/message-verification-rule/` | {ver} | 2026-10-16 | Gem, directly in Archivist's chat 16 Oct 2026 11:41am AEST | "
                            "Shared governance document (not a profile; nothing to deploy). v004 adds Archivist's narrow deploy exception for Imitator-approved versions (never Imitator, its checkers or role-widening). |"); hit += 1
        assert hit == 1
    else:
        body = (f"# {p['name']}: instructions {ver}\n\n| Field | Value |\n|---|---|\n| Bot name | {p['name']} |\n| Bot id | {p['aid']} |\n| Title | (none) |\n| Version | {int(ver[1:])} |\n"
                f"| Date | 2026-10-16 (AEST, UTC+10) |\n| Author | {AUTHOR} |\n| Reason | {p['reason']} |\n| Approved by | {APPR} |\n| Source | {src}; recorded as {ver}.md, the next number in this folder |\n"
                f"| Previous version | {p['prev']}.md |\n| Status | APPROVED, NOT DEPLOYED at recording (16 Oct 2026 AEST). After recording, deployment status is in CHANGELOG.md, which is authoritative. |\n\n"
                "## Exact instructions (verbatim)\n\nThe fenced block below is the approved instruction text copied exactly from the proposal's fenced 'Exact instructions (verbatim)' block, character for character (no trailing newline added inside the text).\n\n"
                f"```text\n{p['text']}\n```\n\n## Template sections\n\nNO-TEMPLATE-SECTIONS-IN-PROPOSAL: the approved proposal has no template sections, so none are invented here. The verbatim block above is authoritative.\n\n"
                + ''.join(f"### {s}\n(Not provided in the approved proposal; see the verbatim block above.)\n\n" for s in ['Purpose', 'Scope', 'Rules', 'Relationships', 'Limits']).rstrip('\n') + '\n')
        cl = C/folder/'CHANGELOG.md'; c = cl.read_text().rstrip('\n') + '\n'
        c += f"| {int(ver[1:])} | 2026-10-16 (AEST, UTC+10) | {AUTHOR} | {APPR} | {p['reason']} | {ver}.md |\n"
        c += (f"| (deployment status, no version change) | 2026-10-16 (AEST, UTC+10) | Archivist | n/a | PENDING-DEPLOY {ver}.md: approved; Gem asked for deployment at 11:41am AEST 16 Oct 2026 ({Q}); Gem's words recorded before deploying (R-029); "
              f"not yet applied to the live profile ({p['aid']} still runs {p['prev']}.md). | (no new file) |\n"); cl.write_text(c)
        hit = 0
        for i, l in enumerate(lines):
            cells = l.split(' | ')
            if l.startswith('|') and len(cells) > 8 and cells[2] == p['aid']:
                cells[3] = f'[{folder}/]({folder}/{ver}.md)'; cells[4] = ver; cells[5] = '2026-10-16'; cells[6] = 'APPROVED (PENDING-DEPLOY)'
                cells[8] = (f"Approved, pending deploy: {ver} approved by Gem (11:41am 16 Oct, Archivist's chat: {Q}); NOT yet deployed (live still runs {p['prev']}). {p['reason']} Earlier: " + cells[8])
                lines[i] = ' | '.join(cells); hit += 1
        assert hit == 1, p['prop']
    vf = C/folder/f'{ver}.md'; assert not vf.exists(); vf.write_text(body); assert block(vf.read_text()) == p['text']
idx = '\n'.join(lines)
idx = re.sub(r'^Last rebuilt: .*$', "Last rebuilt: 2026-10-16 (AEST, UTC+10) ~11:45am. Gem's 11:41am approval in Archivist's chat (3 drafts in proposals/2026-10-16-deploy): codex-keeper v008 and explorer-copy v005 approved, PENDING-DEPLOY (manifest 2026-10-16c); shared message-verification-rule v004 recorded (nothing to deploy). Earlier today: 11:02am and 11:03am batches, 12 deployed 11:06:44–11:08:50. Rows: 37.", idx, count=1, flags=re.M)
(C/'index.md').write_text(idx)
man = []
for p in plan:
    if p['aid'] is None: continue
    e = {'folder': p['folder'], 'agentId': p['aid'], 'name': p['name'], 'version': p['ver'], 'field': 'description', 'text': p['text'], 'sha256': p['sha'], 'chars': len(p['text'])}
    assert block((C/e['folder']/f"{e['version']}.md").read_text()) == e['text'] and hashlib.sha256(e['text'].encode()).hexdigest() == e['sha256']
    man.append(e)
mf = C/'_tools/deploy_manifest_2026-10-16c.json'; assert not mf.exists()
mf.write_text(json.dumps(man, indent=2, ensure_ascii=False) + '\n')
back = json.loads(mf.read_text())
for e, p in zip(back, [x for x in plan if x['aid']]): assert e['text'] == p['text']
for e in back: print('MANIFEST', e['agentId'], e['name'], e['folder'], e['version'], e['chars'], e['sha256'])
