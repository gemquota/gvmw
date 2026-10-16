#!/usr/bin/env python3
"""Record Gem's 11:03am approval of the 8 RR-028 drafts (16 Oct), J1 default (Emissary only poster).
Explorer: batch-1 v003 already recorded; explorer-v004-combined recorded as v004 (README: both approved); explorer-v003-rr028 not recorded separately.
Checks first, then writes. Rewrites deploy_manifest_2026-10-16b.json as ONE final manifest (one entry per bot, final text)."""
import re, json, hashlib, sys
from pathlib import Path
G = Path('/workspace/governance'); C = G/'codex'; PR = G/'proposals/2026-10-16-rr028'
Q = "\"I approve all 8 drafts in proposals/2026-10-16-rr028, with Emissary as the only poster. Record and deploy them.\""
APPR = (f"Gem, directly in Archivist's chat 16 Oct 2026 11:03am AEST ({Q}). Recorded in approvals/2026-10-16-gem-direct-words.md at 11:04:36, before any deploy (R-029). J1 default chosen by Gem: Emissary is the only poster.")
AUTHOR = 'Architect (id 51af1200-ca1a-45ff-8350-848091e00f96)'
ITEMS = [
 ('connector-limits-v001', '_shared/connector-limits', 'v001', 'e812e6970cf0', ' New shared entry, owner Safeguard; recorded only, nothing to deploy. J1 default (Emissary only poster); J2 default (no dry-run waiver).'),
 ('mediator-v006', 'connector-steward', 'v006', '2d92ed3b15dd', ' J4: acceptance of a new integration is Gem\'s call. Profile name still "P4 (Ops) Mediator" (rename not part of this draft).'),
 ('emissary-v006', 'grok-bot', 'v006', 'cc9568126dba', ' J1 default: Emissary is the only postiz poster.'),
 ('explorer-v004-combined', 'explorer-copy', 'v004', '3b6bee90fd3d', ' Combined draft: 16 Oct explorer-v003 (directory handover, recorded as v003) plus the RR-028 line from explorer-v003-rr028 (sha256 e397f168ec7b, approved in the same words, not recorded separately because it uses the same base v002 and number v003; README "Conflicts").'),
 ('engineer-v007', 'codey', 'v007', '4b8e0bbd30e6', ''),
 ('extractor-v005', 'scraper', 'v005', '59e7922b297f', ''),
 ('safeguard-v006', 'compliance-risk-officer', 'v006', 'b7a6aaf78120', ' Approver Gem only: Safeguard checks Imitator (R-027); owns _shared/connector-limits/.'),
]
def block(t):
    k = '## Exact instructions (verbatim)' if '## Exact instructions (verbatim)' in t else '## Exact text (verbatim)'
    a = t.split(k); assert len(a) == 2; f = re.findall(r'```text\n(.*?)\n```', a[1], re.S); assert len(f) == 1; return f[0]
def changes(t): return re.findall(r'- Old: "(.*?)"\n\s+- New: "(.*?)"', t)
def apply(base, t, prop):
    for o, n in changes(t):
        assert base.count(o) == 1, (prop, o[:50]); base = base.replace(o, n)
    return base
directory = (G/'directory.md').read_text(); plan = []
for prop, folder, ver, fsha, extra in ITEMS:
    raw = (PR/f'{prop}.md').read_bytes(); h = hashlib.sha256(raw).hexdigest(); assert h.startswith(fsha), (prop, h[:12])
    t = raw.decode(); text = block(t); sha = hashlib.sha256(text.encode()).hexdigest()
    m = re.search(r'base sha256 (\w+); draft sha256 (\w+)', t)
    if m: assert sha.startswith(m.group(2)), prop
    shared = folder.startswith('_shared'); prev = None
    if (C/folder).exists():
        nums = sorted(int(p.stem[1:]) for p in (C/folder).glob('v[0-9][0-9][0-9].md')); prev = f'v{nums[-1]:03d}'
        assert int(ver[1:]) == nums[-1] + 1, (prop, prev)
    else: assert ver == 'v001' and shared
    assert not (C/folder/f'{ver}.md').exists()
    aid = name = None
    if not shared:
        base = block((C/folder/f'{prev}.md').read_text()); assert hashlib.sha256(base.encode()).hexdigest().startswith(m.group(1)), (prop, 'base sha')
        assert apply(base, t, prop) == text, (prop, 'rebuild')
        aid = re.search(r'(?:id|agent) `([0-9a-f-]{36})`', t).group(1); assert aid in directory, prop
        live = json.loads((Path('/home/box/agent-data/agents')/aid/'profile.json').read_text()); name = live['name']
        if folder == 'explorer-copy':
            v2 = block((C/folder/'v002.md').read_text()); assert live['description'] == v2, 'explorer live != v002'
            r = (PR/'explorer-v003-rr028.md').read_text(); assert hashlib.sha256(r.encode()).hexdigest().startswith('e397f168ec7b')
            assert apply(v2, r, 'rr028') == block(r), 'rr028 rebuild'
            assert changes(r) == changes(t), 'combined carries exactly the rr028 change'
            assert apply(base, r, 'rr028 on v003') == text, 'v003 + rr028 != combined'
        else:
            assert live['description'] == base, (prop, 'live != base')
    title = re.match(r'# (.+?)\n', t).group(1); reason = title.split(' — ')[1] + '.' + extra
    plan.append(dict(prop=prop, folder=folder, ver=ver, prev=prev, raw=raw, text=text, sha=sha, aid=aid, name=name, reason=reason, shared=shared))
    print('CHECK OK', prop, folder, prev, '->', ver, len(text), sha[:12], name or '(shared)')
if '--check' in sys.argv: sys.exit(0)
idx = (C/'index.md').read_text()
for p in plan:
    folder, ver = p['folder'], p['ver']; src = f"/workspace/governance/proposals/2026-10-16-rr028/{p['prop']}.md (file sha256 {hashlib.sha256(p['raw']).hexdigest()[:12]})"
    if p['shared']:
        (C/folder).mkdir(parents=True, exist_ok=False)
        body = (f"# Shared: Connector limits {ver}\n\n| Field | Value |\n|---|---|\n| Entry | Connector limits (shared governance document, not any one bot's instructions) |\n| Version | 1 |\n| Date | 2026-10-16 (AEST, UTC+10) |\n"
                f"| Author | {AUTHOR} |\n| Reason | {p['reason']} |\n| Approved by | {APPR} |\n| Source | {src} |\n| Owner | P1 (Checks) Safeguard (3661a899-2768-4a77-a95a-71d0251813bc) |\n| Previous version | (none, new entry) |\n"
                "| Status | APPROVED. Shared document; bots refer to it from their own instructions. Not a profile, so nothing to deploy. |\n\n## Exact text (verbatim)\n\n"
                "The fenced block below is the approved text copied exactly from the proposal's fenced 'Exact instructions (verbatim)' block, character for character (no trailing newline added inside the text).\n\n"
                f"```text\n{p['text']}\n```\n")
        (C/folder/'CHANGELOG.md').write_text("# Shared: Connector limits: changelog\n\nOwner: P1 (Checks) Safeguard (3661a899-2768-4a77-a95a-71d0251813bc). Shared governance document; not a profile.\n\n| Version | Date | Author | Approved by | Reason | File |\n|---|---|---|---|---|---|\n"
                                            f"| 1 | 2026-10-16 (AEST, UTC+10) | {AUTHOR} | {APPR} | {p['reason']} | v001.md |\n")
    else:
        body = (f"# {p['name']}: instructions {ver}\n\n| Field | Value |\n|---|---|\n| Bot name | {p['name']} |\n| Bot id | {p['aid']} |\n| Title | (none) |\n| Version | {int(ver[1:])} |\n"
                f"| Date | 2026-10-16 (AEST, UTC+10) |\n| Author | {AUTHOR} |\n| Reason | {p['reason']} |\n| Approved by | {APPR} |\n| Source | {src}; recorded as {ver}.md, the next number in this folder |\n"
                f"| Previous version | {p['prev']}.md |\n| Status | APPROVED, NOT DEPLOYED at recording (16 Oct 2026 AEST). After recording, deployment status is in CHANGELOG.md, which is authoritative. |\n\n"
                "## Exact instructions (verbatim)\n\nThe fenced block below is the approved instruction text copied exactly from the proposal's fenced 'Exact instructions (verbatim)' block, character for character (no trailing newline added inside the text).\n\n"
                f"```text\n{p['text']}\n```\n\n## Template sections\n\nNO-TEMPLATE-SECTIONS-IN-PROPOSAL: the approved proposal has no template sections, so none are invented here. The verbatim block above is authoritative.\n\n"
                + ''.join(f"### {s}\n(Not provided in the approved proposal; see the verbatim block above.)\n\n" for s in ['Purpose', 'Scope', 'Rules', 'Relationships', 'Limits']).rstrip('\n') + '\n')
        cl = C/folder/'CHANGELOG.md'; c = cl.read_text().rstrip('\n') + '\n'
        c += f"| {int(ver[1:])} | 2026-10-16 (AEST, UTC+10) | {AUTHOR} | {APPR} | {p['reason']} | {ver}.md |\n"
        if folder == 'explorer-copy':
            c += ("| (deployment status, no version change) | 2026-10-16 (AEST, UTC+10) | Archivist | n/a | v003.md is superseded before deployment: it won't be deployed on its own. v004.md (v003 + the RR-028 line) is the text to deploy, so the live profile goes from v002.md straight to v004.md in one write. "
                  "The v003 PENDING-DEPLOY row above is replaced by the v004 row below. | (no new file) |\n")
        c += (f"| (deployment status, no version change) | 2026-10-16 (AEST, UTC+10) | Archivist | n/a | PENDING-DEPLOY {ver}.md: approved; Gem asked for deployment at 11:03am AEST 16 Oct 2026 ({Q}); Gem's words recorded before deploying (R-029); "
              f"not yet applied to the live profile ({p['aid']} still runs {'v002' if folder=='explorer-copy' else p['prev']}.md). | (no new file) |\n")
        cl.write_text(c)
    vf = C/folder/f'{ver}.md'; vf.write_text(body); assert block(vf.read_text()) == p['text']
    lines = idx.split('\n'); hit = 0
    if p['shared']:
        for i, l in enumerate(lines):
            if l.startswith('| Message verification & safety rule |'):
                lines.insert(i+1, f"| Connector limits (RR-028) | `_shared/connector-limits/` | v001 | 2026-10-16 | Gem, directly in Archivist's chat 16 Oct 2026 11:03am AEST | Shared governance document (not a profile; nothing to deploy). Owner Safeguard. Postiz (Emissary only poster, J1), Vercel, Drive/Sheets, Calendar, new connectors. Cited by Emissary v006, Engineer v007, Explorer v004, Extractor v005, Mediator v006, Safeguard v006. |"); hit += 1; break
    else:
        for i, l in enumerate(lines):
            cells = l.split(' | ')
            if l.startswith('|') and len(cells) > 8 and cells[2] == p['aid']:
                cells[3] = f'[{folder}/]({folder}/{ver}.md)'; cells[4] = ver; cells[5] = '2026-10-16'; cells[6] = 'APPROVED (PENDING-DEPLOY)'
                lead = f"APPROVED {ver} by Gem (11:03am 16 Oct, Archivist's chat: {Q}); Gem asked for deployment; NOT yet deployed (live still runs {'v002' if folder=='explorer-copy' else p['prev']}). {p['reason']} "
                cells[8] = re.sub(r"^APPROVED v003 by Gem \(11:02am.*?Earlier: ", "Recorded v003 (Gem 11:02am, directory handover; superseded before deploy by v004). ", cells[8]) if folder == 'explorer-copy' else cells[8]
                cells[8] = lead + 'Earlier: ' + cells[8]; lines[i] = ' | '.join(cells); hit += 1
    assert hit == 1, (p['prop'], hit); idx = '\n'.join(lines)
idx = re.sub(r'^Last rebuilt: .*$', "Last rebuilt: 2026-10-16 (AEST, UTC+10) ~11:10am. Two Gem approvals in Archivist's chat: 11:02am (8 drafts: assessor v004, auditor v004, secrets-credentials-custodian v005, clone v006, identity-inferer v005, codex-keeper v007, explorer-copy v003 [superseded by v004 before deploy], shared message-verification-rule v003) and 11:03am (8 RR-028 drafts: shared connector-limits v001, connector-steward v006, grok-bot v006, explorer-copy v004, codey v007, scraper v005, compliance-risk-officer v006; explorer-v003-rr028 folded into v004). 12 profiles PENDING-DEPLOY (manifest 2026-10-16b). Rows: 37.", idx, count=1, flags=re.M)
(C/'index.md').write_text(idx)
# ONE final manifest: one entry per bot, latest recorded text
mf = C/'_tools/deploy_manifest_2026-10-16b.json'; man = json.loads(mf.read_text()); byid = {e['agentId']: e for e in man}
for p in plan:
    if p['shared']: continue
    byid[p['aid']] = {'folder': p['folder'], 'agentId': p['aid'], 'name': p['name'], 'version': p['ver'], 'field': 'description', 'text': p['text'], 'sha256': p['sha'], 'chars': len(p['text'])}
final = list(byid.values())
for e in final:  # each entry must be that folder's latest version, byte for byte
    nums = sorted(int(x.stem[1:]) for x in (C/e['folder']).glob('v[0-9][0-9][0-9].md')); assert e['version'] == f'v{nums[-1]:03d}', e['folder']
    assert block((C/e['folder']/f"{e['version']}.md").read_text()) == e['text'] and hashlib.sha256(e['text'].encode()).hexdigest() == e['sha256']
assert len({e['agentId'] for e in final}) == len(final) == 12
mf.write_text(json.dumps(final, indent=2, ensure_ascii=False) + '\n')
for e in final: print('MANIFEST', e['agentId'], e['name'], e['folder'], e['version'], e['chars'], e['sha256'][:12])
