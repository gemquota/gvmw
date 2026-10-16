#!/usr/bin/env python3
"""Record Imitator's 6 approved 16 Oct proposals (APPROVED, NOT deployed). Writes new vNNN.md only (never overwrites),
appends CHANGELOG rows, updates index rows, writes deploy_manifest_2026-10-16.json. Touches no profile.json."""
import re, json, hashlib
from pathlib import Path
G = Path('/workspace/governance'); C = G/'codex'; PR = G/'proposals/2026-10-16'
ITEMS = [  # proposal, folder, version, file sha prefix, Imitator log row, 1:1 confirmation
 ('engineer-v006', 'codey', 'v006', '6a1b9a6d689e', '08:15', '08:16'),
 ('mediator-v005', 'connector-steward', 'v005', '4cfbb3348032', '08:15', '08:16'),
 ('mender-v005', 'mender', 'v005', 'e52ebf9e88aa', '08:15', '08:16'),
 ('inquirer-v004', 'identity-inquirer', 'v004', 'd8ac34989517', '08:15', '08:16'),
 ('arbiter-v005', 'arbiter', 'v005', '47bcfb1929c7', '08:17', '08:17'),
 ('architect-v004', 'instruction-architect', 'v004', '278506086d63', '08:18', '08:18'),
]
NOTE_EXTRA = {'mediator-v005': ' J6 default (urgent cost alerts straight to Gem). The P4 → P2 name change is not part of it.',
              'mender-v005': ' J7 default (first run after a gap does the full lookback; Explorer\'s report is the backup).'}
AUTHOR = 'Architect (id 51af1200-ca1a-45ff-8350-848091e00f96)'
def block(t):
    a = t.split('## Exact instructions (verbatim)'); assert len(a) == 2
    f = re.findall(r'```text\n(.*?)\n```', a[1], re.S); assert len(f) == 1; return f[0]
def approver(row, conf, prop):
    words = '"confirmed architect-v004"' if prop == 'architect-v004' else '"confirmed"'
    return (f"Imitator (6ae584b8-eaac-429b-9eae-d5e3e6f6a32b), as logged in /workspace/governance/approvals.md (16 Oct {row} row); "
            f"confirmed 1:1 with Archivist at {conf} AEST 16 Oct 2026 ({words}{'; rechecked sha256 47bcfb1929c7' if prop=='arbiter-v005' else ''}). "
            "Authority delegated by Gem's grants of 4 and 9 Oct; P4 live since 15 Oct 2026 23:30 AEST (phases.md).")
manifest, index = [], (C/'index.md').read_text()
for prop, folder, ver, fsha, row, conf in ITEMS:
    raw = (PR/f'{prop}.md').read_bytes(); assert hashlib.sha256(raw).hexdigest().startswith(fsha), prop
    t = raw.decode(); text = block(t); sha = hashlib.sha256(text.encode()).hexdigest()
    m = re.search(r'base sha256 (\w+); draft sha256 (\w+)', t); assert sha.startswith(m.group(2))
    title = re.match(r'# (.+?)\n', t).group(1)
    reason = title.split(' — ')[1] + '.' + NOTE_EXTRA.get(prop, '')
    aid = re.search(r'id `([0-9a-f-]{36})`', t).group(1)
    nums = sorted(int(p.stem[1:]) for p in (C/folder).glob('v[0-9][0-9][0-9].md')); prev = f'v{nums[-1]:03d}'
    assert int(ver[1:]) == nums[-1] + 1
    prevtxt = (C/folder/f'{prev}.md').read_text(); assert block(prevtxt).startswith('') and hashlib.sha256(block(prevtxt).encode()).hexdigest().startswith(m.group(1))
    live = json.loads((Path('/home/box/agent-data/agents')/aid/'profile.json').read_text())
    name = live['name']; assert live['description'] == block(prevtxt)
    appr = approver(row, conf, prop)
    vf = C/folder/f'{ver}.md'; assert not vf.exists()
    vf.write_text(f"""# {name}: instructions {ver}

| Field | Value |
|---|---|
| Bot name | {name} |
| Bot id | {aid} |
| Title | (none) |
| Version | {int(ver[1:])} |
| Date | 2026-10-16 (AEST, UTC+10) |
| Author | {AUTHOR} |
| Reason | {reason} |
| Approved by | {appr} |
| Source | /workspace/governance/proposals/2026-10-16/{prop}.md (file sha256 {hashlib.sha256(raw).hexdigest()[:12]}; recorded as {ver}.md, the next number in this folder) |
| Previous version | {prev}.md |
| Status | APPROVED, NOT DEPLOYED at recording (16 Oct 2026 AEST). After recording, deployment status is in CHANGELOG.md, which is authoritative. |

## Exact instructions (verbatim)

The fenced block below is the approved instruction text copied exactly from the proposal's fenced 'Exact instructions (verbatim)' block, character for character (no trailing newline added inside the text).

```text
{text}
```

## Template sections

NO-TEMPLATE-SECTIONS-IN-PROPOSAL: the approved proposal has no template sections, so none are invented here. The verbatim block above is authoritative.

### Purpose
(Not provided in the approved proposal; see the verbatim block above.)

### Scope
(Not provided in the approved proposal; see the verbatim block above.)

### Rules
(Not provided in the approved proposal; see the verbatim block above.)

### Relationships
(Not provided in the approved proposal; see the verbatim block above.)

### Limits
(Not provided in the approved proposal; see the verbatim block above.)
""")
    assert block(vf.read_text()) == text
    cl = C/folder/'CHANGELOG.md'; c = cl.read_text().rstrip('\n') + '\n'
    c += f"| {int(ver[1:])} | 2026-10-16 (AEST, UTC+10) | {AUTHOR} | {appr} | {reason} | {ver}.md |\n"
    c += (f"| (deployment status, no version change) | 2026-10-16 (AEST, UTC+10) | Archivist | n/a | PENDING-DEPLOY {ver}.md: APPROVED by Imitator, NOT deployed. "
          f"Awaiting Gem's deploy decision: Archivist deploys only when Gem asks in Archivist's chat (asked). Live profile ({aid}) still runs {prev}.md. | (no new file) |\n")
    cl.write_text(c)
    # index row
    lines = index.split('\n'); hit = 0
    for i, l in enumerate(lines):
        cells = l.split(' | ')
        if l.startswith('|') and len(cells) > 8 and cells[2] == aid:
            cells[3] = f'[{folder}/]({folder}/{ver}.md)'; cells[4] = ver; cells[5] = '2026-10-16'; cells[6] = 'APPROVED (PENDING-DEPLOY)'
            cells[8] = (f"APPROVED {ver}, NOT deployed: awaiting Gem's deploy decision (Archivist deploys only when Gem asks in Archivist's chat). Live profile still runs {prev}. "
                        f"Approved by Imitator (16 Oct {row} log row; 1:1 confirmation {conf} AEST); author Architect; {reason} Earlier: " + cells[8])
            lines[i] = ' | '.join(cells); hit += 1
    assert hit == 1, (prop, hit); index = '\n'.join(lines)
    manifest.append({'folder': folder, 'agentId': aid, 'name': name, 'version': ver, 'field': 'description', 'text': text, 'sha256': sha, 'chars': len(text)})
index = re.sub(r'^Last rebuilt: .*$', "Last rebuilt: 2026-10-16 (AEST, UTC+10) ~8:25am. Imitator's 6 approved 16 Oct updates recorded (codey v006, connector-steward v005, mender v005, identity-inquirer v004, arbiter v005, instruction-architect v004): APPROVED, PENDING-DEPLOY, awaiting Gem's deploy decision. Rows: 37.", index, count=1, flags=re.M)
(C/'index.md').write_text(index)
(C/'_tools/deploy_manifest_2026-10-16.json').write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + '\n')
for e in manifest: print(e['agentId'], e['name'], e['folder'], e['version'], e['chars'], e['sha256'][:12])
