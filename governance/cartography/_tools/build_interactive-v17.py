#!/usr/bin/env python3
"""Build cartography/role-map-interactive.html from role-graph.json + summaries.md (+ codex index.md
for deployed dates). Self-contained: all CSS/JS inlined, no network. Descriptive only.
Includes only what's already in the role map summaries/notes: no instruction text, no secrets.
Rebuild with each map version:  python3 _tools/build_interactive.py
"""
import json, re, html, datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent          # cartography/
CODEX = HERE.parent / 'codex'
OUT = HERE / 'role-map-interactive.html'

g = json.loads((HERE / 'role-graph.json').read_text())
summ = (HERE / 'summaries.md').read_text()
index = (CODEX / 'index.md').read_text()

def plain(s):  # strip light markdown
    return re.sub(r'\*\*|`', '', s).strip()

# --- summaries: '### <heading> — `<id8>` — <folder>/<ver>' then paragraph + '- ' bullets
sections = {}
for m in re.finditer(r'^### (.+?) — `([0-9a-f]{8})` — (\S+)(.*)$\n((?:(?!^#{2,3} |^---).*\n?)*)', summ, re.M):
    para, bullets = [], []
    for line in m.group(5).splitlines():
        line = line.strip()
        if not line: continue
        (bullets.append(plain(line[2:])) if line.startswith('- ') else para.append(plain(line)))
    sections[m.group(2)] = {'paragraph': ' '.join(para), 'bullets': bullets, 'summary_version': m.group(3)}
# former table rows: | name | id8[ / id8] | -> | note |
former_rows = {}
for m in re.finditer(r'^\| ([^|]+) \| ([0-9a-f]{8}(?: / [0-9a-f]{8})?) \| ([^|]+) \| ([^|]+) \|$', summ, re.M):
    for i in m.group(2).split(' / '):
        former_rows[i] = {'takeover': plain(m.group(3)), 'note': plain(m.group(4))}

# --- codex index: deployed date per agent id (short phrase only, not the notes)
deployed = {}
for row in index.splitlines():
    cells = [c.strip() for c in row.split('|')]
    if len(cells) < 10 or not re.fullmatch(r'[0-9a-f-]{36}', cells[3]): continue
    notes, flag, updated = cells[9], cells[7], cells[6]
    m = (re.search(r'(deployed \d{1,2} Oct 2026 (?:at|~)\s?[^;)]*?AEST)', notes)
         or re.search(r'(applied by Explorer at [0-9:]+ AEST \d{1,2} Oct 2026)', notes)
         or re.search(r'(DELETED from live \([^)]*\))', notes))
    deployed[cells[3]] = {'deployed': m.group(1) if m else None, 'flag': flag, 'updated': updated}

GROUPS = ['Roles', 'Checks', 'Ops', 'ID', 'Work']
STATUS = {'active': 'Live', 'dormant': 'Dormant', 'retired_gone': 'Retired (deleted)', 'former_gone': 'Former (deleted)', 'unrecorded': 'Unrecorded, awaiting Gem', 'retired_nocodex': 'Retired (Gem, 22 Oct 6:37pm); deletion not confirmed'}
nodes = []
for n in g['nodes']:
    if n['type'] == 'human':
        nodes.append({'key': n['key'], 'name': 'Gem', 'group': 'Gem', 'status': 'Owner', 'tier': 'gem',
                      'phase': '-', 'phaseStatus': 'Approves (chat or voice call)', 'note': n.get('note', ''),
                      'summary': {'paragraph': 'Gem Quota, owner and approving authority. ' + n.get('note', ''),
                                  'bullets': [plain(v) for v in g.get('rules', {}).values()]}})
        continue
    sid = n['id'][:8]
    name = re.sub(r'^RETIRED ', '', n['name'])
    codex = n.get('live_codex') or n.get('codex', '')   # live version; a newer approved one goes in 'pending'
    ver = '/'.join(codex.split('/')[-2:]).replace('.md', '') if codex else None
    d = deployed.get(n['id'], {})
    s = sections.get(sid)
    if not s and sid in former_rows:
        fr = former_rows[sid]; s = {'paragraph': fr['note'], 'bullets': ['Taken over by: ' + fr['takeover']]}
    ms = n.get('map_status')
    nodes.append({'key': n['key'], 'name': name, 'shortId': sid, 'group': n.get('category'),
                  'phase': n.get('phase') or '-', 'phaseStatus': n.get('phase_status', ''),
                  'status': STATUS.get(ms, ms), 'tier': 'unrecorded' if ms in ('unrecorded', 'retired_nocodex') else (n.get('phase') or 'former'),
                  'live': ms == 'active', 'formerName': n.get('former_name'),
                  'absorbed': n.get('absorbed', []), 'codexVersion': ver,
                  'deployed': d.get('deployed'), 'indexFlag': d.get('flag'), 'lastUpdated': d.get('updated'),
                  'pending': n.get('pending'), 'note': n.get('note', ''), 'summary': s or {'paragraph': n.get('note', ''), 'bullets': []}})

byname = {n['name']: n for n in g['nodes']}
def etype(e):
    r = e['relation'].lower()
    if e['status'].startswith(('retired', 'former')): return 'former'
    if e['to_name'] == 'Safeguard': return 'safeguard'
    if any(w in r for w in ('stay with', 'leaves with', 'gem-only', 'gem only:')): return 'limits'
    if e.get('flow') == 'approval' or 'propos' in r or 'approv' in r: return 'approves'
    if 'route' in r or r.startswith('assigns'): return 'routes'
    if e['from_name'] in ('Scorer', 'Scrutineer', 'Arbiter') or any(w in r for w in ('review', 'test', 'hypothes')): return 'checks'
    return 'handoff'
edges = []
for e in g['edges']:
    edges.append({'from': byname[e['from_name']]['key'], 'to': byname[e['to_name']]['key'],
                  'label': e['relation'], 'type': etype(e), 'status': e['status'],
                  'dormant': e['status'] != 'current' and not e['status'].startswith(('retired', 'former')),
                  'sources': ['/'.join(s.split('/')[-2:]).replace('.md', '') for s in e.get('source', [])
                              if 'codex/' in s] })
ETYPES = [
  ['approves', 'Approves / proposes', '#6a1b9a'],
  ['checks', 'Checks / reviews', '#00838f'],
  ['routes', 'Routes to', '#2e7d32'],
  ['safeguard', 'Safeguard-first (repo pushes, risky plans)', '#d50000'],
  ['limits', 'Limits kept by Gem', '#4e342e'],
  ['handoff', 'Hand-off / reports', '#78909c'],
  ['former', 'Retired / former takeover', '#a0a0a0'],
]
data = {'version': g['version'], 'note': g.get('sources', {}).get('note', ''),
        'built': datetime.datetime.now().strftime('%-d %b %Y, %-I:%M%p AEST').replace('AM', 'am').replace('PM', 'pm'),
        'groups': GROUPS, 'etypes': ETYPES, 'nodes': nodes, 'edges': edges}
# guard: nothing secret-looking or instruction-like slips in
blob = json.dumps(data, ensure_ascii=False)
for pat in [r'\+?\d[\d ]{8,}\d', r'(?i)(api[_-]?key|password|secret=|token=|bearer )', r'Exact instructions']:
    assert not re.search(pat, blob), f'blocked content pattern {pat}'
blob = blob.replace('</', '<\\/')

TEMPLATE = (HERE / '_tools' / 'interactive_template.html').read_text()
OUT.write_text(TEMPLATE.replace('/*__DATA__*/null', blob).replace('__TITLE__', html.escape('Role map ' + g['version'].split(',')[0] + ' — interactive')))
print(f'wrote {OUT} ({OUT.stat().st_size} bytes; {len(nodes)} nodes, {len(edges)} edges; '
      f'{sum(1 for n in nodes if n.get("deployed"))} with deploy dates; {len(sections)} summary sections)')
