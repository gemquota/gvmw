#!/usr/bin/env python3
"""Embeds referenced repo files and vendored libraries into index.html.
Called by build_data.py after items.json is written; it can also be run on its own.
Read-only with respect to /workspace/vepa."""
import json, os, re, subprocess, collections, fnmatch, gzip, base64

REPO = '/workspace/vepa'
OUT = '/workspace/vepa-plans'
VENDOR = OUT + '/vendor-src/node_modules'
MAX_FILE = 3_000_000          # per-file embed cap (bytes); larger files are truncated
TOTAL_BUDGET = 25_000_000     # stop embedding non-essential files beyond this

# Group document records -> the files they stand for. 'embed': 'all' | 'referenced'
GROUPS = {
 'exports/vepa-*-concat.md (2 snapshots)': (['exports/vepa-*-concat.md'], 'all'),
 'docs/systems/roadmaps/ (README + 48 A–D variants)': (['docs/systems/roadmaps/*'], 'all'),
 'docs/systems/roles/ (README + 11 role files)': (['docs/systems/roles/*'], 'all'),
 'docs/systems/past/0/ (5 archived copies)': (['docs/systems/past/0/*'], 'all'),
 'docs/audit/laws/a3/ roll-ups (audit_progress, all_stage_*, category docs, mega ensemble)': (['docs/audit/laws/a3/*'], 'all'),
 'docs/audit/laws/a3/stage-1/ (128 per-law reports)': (['docs/audit/laws/a3/stage-1/*'], 'all'),
 'docs/audit/laws/a3/stage-2/ (128 per-law proposals)': (['docs/audit/laws/a3/stage-2/*'], 'all'),
 'docs/audit/laws/a3/stage-3/ (128 per-law sign-offs)': (['docs/audit/laws/a3/stage-3/*'], 'all'),
 'docs/spec/ (rest of generated tree incl. audit/signoff-manifest.json, laws/*.json, retained legacy records)': (['docs/spec/**'], 'all'),
}
# Basenames that match several repo files: the one the catalogue means.
ALIAS = {'laws.js': 'src/physics/laws.js', 'react-entry.js': 'src/react-entry.js',
         'roadmap-overview.md': 'docs/systems/roadmap-overview.md'}
# Related files added by hand where the evidence names no file (each one checked against the repo).
CURATED = {
 'ARP-3': ['public/bench-report/index.html', 'bench/backend-compare.mjs'],
 'ARP-CC': ['.github/workflows/deploy.yml', 'package.json'],
 'RB-1': ['bench/results/renderer-benchmark.json'],
 'SPEC-HELP': ['scripts/generate-spec.mjs', 'src/constants/help.js'],
 'A12': ['src/main.js', 'index.html'],
}
LANG = {'.js':'javascript','.mjs':'javascript','.cjs':'javascript','.ts':'typescript','.json':'json','.css':'css',
        '.py':'python','.sh':'bash','.yml':'yaml','.yaml':'yaml','.md':'markdown','.html':'xml','.htm':'xml',
        '.toml':'ini','.txt':'plaintext','.svg':'xml','.xml':'xml','.mmd':'plaintext'}
TOKEN = re.compile(r'(?<![\w/.-])((?:\.{0,2}[\w.@-]*/)*[\w.-]+\.(?:json|mjs|cjs|js|ts|css|py|sh|ya?ml|md|html|txt|toml))(?::(\d+)(?:[-–](\d+))?)?')

def git_files():
    out = subprocess.run(['git', '-C', REPO, 'ls-files', '--cached'], capture_output=True, text=True, check=True).stdout
    return [f for f in out.split('\n') if f and os.path.isfile(os.path.join(REPO, f))]

def main():
    data = json.load(open(OUT + '/items.json'))
    files = git_files(); S = set(files)
    moved = {d['path']: d['movedTo'] for d in data['documents'] if d.get('movedTo')}
    def real(p):   # catalogue path -> path on disk (moved docs live under .old/)
        if p in S: return p
        if p in moved and moved[p] in S: return moved[p]
        if '.old/' + p in S: return '.old/' + p
        return None
    def resolve(tok):
        t = re.sub(r'^(\./)+', '', tok)
        r = real(t)
        if r: return r
        base = os.path.basename(t)
        if base in ALIAS and (t == base or ALIAS[base].endswith(t)): return ALIAS[base]
        c = [f for f in files if f.endswith('/' + t) or f == t]
        c2 = [f for f in c if not f.startswith(('docs/systems/past/', 'public/', '.old/', 'dist/'))] or c
        return c2[0] if len(c2) == 1 else None

    want = collections.OrderedDict()   # path -> reason (priority order)
    unresolved = collections.Counter()
    # 1. every single-file source document
    for d in data['documents']:
        if d['path'] in GROUPS:
            pats, mode = GROUPS[d['path']]
            lst = sorted(f for f in files if any(fnmatch.fnmatch(f, p) for p in pats))
            d['files'] = lst; d['embedMode'] = mode
            if mode == 'all':
                for f in lst: want.setdefault(f, 'source document (group)')
        else:
            r = real(d['path'])
            d['files'] = [r] if r else []; d['embedMode'] = 'all'
            if r: want.setdefault(r, 'source document')
    # 2. item sources + evidence / missing text + curated
    for it in data['items']:
        for s in it['sources']:
            s['path'] = real(s['file'])
            if s['path']: want.setdefault(s['path'], 'source document')
        refs, seen = [], set()
        def add(p, tok, a, b, kind):
            key = (p or tok, a, b)
            if key in seen: return
            seen.add(key)
            refs.append(dict(p=p, tok=tok, l=[int(a), int(b or a)] if a else None, kind=kind))
            if p: want.setdefault(p, 'evidence file')
        for kind, txt in (('evidence', it['evidence']), ('missing', it.get('missing', ''))):
            for m in TOKEN.finditer(txt or ''):
                tok = m.group(1)
                p = resolve(tok)
                if not p: unresolved[tok] += 1
                add(p, tok, m.group(2), m.group(3), kind)
        for p in CURATED.get(it['id'], []):
            if p in S: add(p, p, None, None, 'related')
        it['files'] = refs
    # 3. one hop of relative Markdown links from embedded .md docs (e.g. README -> docs/spec/README.md)
    LINK = re.compile(r'\]\(\s*<?([^)>\s#?]+)')
    linked = []
    for p0 in list(want):
        if not p0.endswith('.md'): continue
        txt = open(os.path.join(REPO, p0), encoding='utf-8', errors='replace').read()
        base = os.path.dirname(p0[5:] if p0.startswith('.old/') else p0)
        for m in LINK.finditer(txt):
            h = m.group(1)
            if re.match(r'^[a-z][\w+.-]*:', h, re.I): continue
            q = os.path.normpath(h.lstrip('/') if h.startswith('/') else os.path.join(base, h))
            r = real(q)
            if r and r not in want and os.path.getsize(os.path.join(REPO, r)) < 400_000 and os.path.splitext(r)[1].lower() in LANG:
                linked.append(r)
    for r in linked: want.setdefault(r, 'linked from an embedded doc')
    # Build embed map within budget
    emb, total, zbytes, skipped, truncated = {}, 0, 0, [], []
    for p, why in want.items():
        raw = open(os.path.join(REPO, p), 'rb').read()
        try: txt = raw.decode('utf-8')
        except UnicodeDecodeError: skipped.append((p, 'binary')); continue
        tr = False
        if len(raw) > MAX_FILE:
            txt = txt[:MAX_FILE]; tr = True; truncated.append((p, len(raw)))
        if total + len(txt) > TOTAL_BUDGET and why not in ('source document', 'evidence file'):
            skipped.append((p, 'size budget')); continue
        ext = os.path.splitext(p)[1].lower()
        z = base64.b64encode(gzip.compress(txt.encode('utf-8'), compresslevel=9, mtime=0)).decode('ascii')
        emb[p] = dict(z=z, lang=LANG.get(ext, 'plaintext'), size=len(raw), trunc=tr, why=why)
        total += len(raw); zbytes += len(z)
    listed_only = []
    for d in data['documents']:
        d['embedded'] = sum(1 for f in d['files'] if f in emb)
        if d['embedded'] < len(d['files']):
            listed_only.append((d['path'], len(d['files']) - d['embedded']))
    data['meta']['embed'] = dict(fileCount=len(emb), bytes=total, gzipBase64Bytes=zbytes, encoding='gzip+base64 per file, decoded lazily in the browser', truncated=truncated, skipped=skipped,
        listedOnly=listed_only, unresolvedRefs=sorted(unresolved.items()),
        note='Every file of every source document is embedded, including all of docs/spec/**. Unresolved refs are files the evidence says are missing, or tokens that are not repo paths.')
    # vendored libraries
    def rd(p): return open(p, encoding='utf-8').read()
    libs = {
      'marked': rd(VENDOR + '/marked/lib/marked.umd.js'),
      'purify': rd(VENDOR + '/dompurify/dist/purify.min.js'),
      'hljs': rd(VENDOR + '/@highlightjs/cdn-assets/highlight.min.js'),
    }
    vers = {k: json.load(open(VENDOR + '/' + n + '/package.json'))['version'] for k, n in
            (('marked', 'marked'), ('dompurify', 'dompurify'), ('highlight.js', '@highlightjs/cdn-assets'))}
    data['meta']['vendored'] = vers
    def js_safe(s): return s.replace('</script', '<\\/script').replace('<!--', '<\\!--')
    def json_safe(o): return json.dumps(o, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c').replace('\u2028', '\\u2028').replace('\u2029', '\\u2029')
    tpl = open(OUT + '/template.html', encoding='utf-8').read()
    parts = {'/*__LIB_MARKED__*/': js_safe(libs['marked']), '/*__LIB_PURIFY__*/': js_safe(libs['purify']),
             '/*__LIB_HLJS__*/': js_safe(libs['hljs']), '__FILES__': json_safe(emb), '__DATA__': json_safe(data)}
    # single pass, so placeholder-like text inside a library or file (hljs contains Perl's __DATA__) is never substituted
    html = re.sub('|'.join(re.escape(k) for k in parts), lambda m: parts[m.group(0)], tpl)
    open(OUT + '/index.html', 'w', encoding='utf-8').write(html)
    json.dump(data, open(OUT + '/items.json', 'w'), indent=1, ensure_ascii=False)
    print(json.dumps(dict(embedded=len(emb), embeddedBytes=total, gzipBase64Bytes=zbytes, htmlBytes=len(html.encode()), truncated=truncated,
          skipped=skipped, listedOnly=listed_only, unresolved=len(unresolved), vendored=vers), indent=1))
    print('unresolved:', sorted(unresolved.items()))

if __name__ == '__main__':
    main()
