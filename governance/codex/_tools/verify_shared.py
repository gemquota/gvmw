#!/usr/bin/env python3
"""Read-only check (16 Oct 2026): for each codex/_shared/*/vNNN.md, its fenced text must equal the fenced text of the
proposal named in its Source row, and any 'file sha256' / 'text sha256' prefixes stated there must match.
Run from codex/:  python3 -B _tools/verify_shared.py   Exit 1 on any MISMATCH, MISSING or AMBIGUOUS."""
import re, sys, hashlib
from pathlib import Path
C = Path(__file__).resolve().parent.parent
HEADS = ('## Exact text (verbatim)', '## Exact instructions (verbatim)')
def fence(t):
    for h in HEADS:
        if h in t:
            parts = t.split(h)
            if len(parts) != 2: return None, f'heading "{h}" appears {len(parts)-1} times'
            f = re.findall(r'```text\n(.*?)\n```', parts[1], re.S)
            return (f[0], None) if len(f) == 1 else (None, f'{len(f)} text fences under "{h}"')
    f = re.findall(r'```text\n(.*?)\n```', t, re.S)
    return (f[0], None) if len(f) == 1 else (None, f'no verbatim heading and {len(f)} text fences')
sha = lambda b: hashlib.sha256(b).hexdigest()
bad = 0; n = 0; legacy = 0
for vf in sorted(C.glob('_shared/*/v[0-9][0-9][0-9].md')):
    n += 1; rel = vf.relative_to(C); t = vf.read_text()
    m = re.search(r'^\| Source \| (\S+\.md)(.*)\|\s*$', t, re.M)
    if not m: print(f'NO-SOURCE  {rel}'); bad += 1; continue
    src = Path(m.group(1)); extra = m.group(2)
    if not src.exists(): print(f'MISSING    {rel}: source {src} not on disk'); bad += 1; continue
    a, ea = fence(t); raw = src.read_bytes(); b, eb = fence(raw.decode())
    if a is None: print(f'AMBIGUOUS  {rel}: version {ea}'); bad += 1; continue
    if b is None:  # older proposals (4-6 Oct) have no single fenced block: accept only if the exact text appears in the source
        src_t = raw.decode()
        cands = re.findall(r'```text\n(.*?)\n```', src_t, re.S)
        if a in cands: print(f'MATCH      {rel} == one of {len(cands)} fences in {src.name} ({len(a)} chars, text sha256 {sha(a.encode())[:12]})'); continue
        if a in src_t: print(f'CONTAINED  {rel}: exact text found inside {src.name} (no single fence there: {eb}); {len(a)} chars'); continue
        print(f'LEGACY     {rel}: {src.name} has {eb}, and the exact text isn\'t in it; not comparable here (verify.py has its own checks for some older shared files)'); legacy += 1; continue
    notes = []
    fs = re.search(r'file sha256 ([0-9a-f]{8,64})', extra); ts = re.search(r'text sha256 ([0-9a-f]{8,64})', extra)
    if fs and not sha(raw).startswith(fs.group(1)): notes.append(f'file sha256 now {sha(raw)[:12]}, stated {fs.group(1)}')
    if ts and not sha(b.encode()).startswith(ts.group(1)): notes.append(f'text sha256 now {sha(b.encode())[:12]}, stated {ts.group(1)}')
    if a != b: notes.insert(0, f'text differs (version {len(a)} chars {sha(a.encode())[:12]}, source {len(b)} chars {sha(b.encode())[:12]})')
    if notes: print(f'MISMATCH   {rel}: ' + '; '.join(notes)); bad += 1
    else: print(f'MATCH      {rel} == {src.name} ({len(a)} chars, text sha256 {sha(a.encode())[:12]}' + (', file hash ok' if fs else '') + ')')
print(f'SHARED: {n} version files, {n-bad-legacy} match, {legacy} legacy (not comparable), {bad} problem(s)'); print('OVERALL:', 'PASS' if bad == 0 else 'FAIL')
sys.exit(1 if bad else 0)
