import re, sys, os
src = sys.argv[1]; out = sys.argv[2]
text = open(src, encoding='utf-8').read()
sep = '=' * 80
# TOC paths from tree
toc_block = text.split('# Hierarchical Table of Contents', 1)[1].split('```', 2)[1]
paths, stack = [], []
for line in toc_block.splitlines():
    m = re.match(r'^((?:│   |    )*)(?:├── |└── )(.+)$', line)
    if not m: continue
    depth = len(m.group(1)) // 4; name = m.group(2).strip()
    stack = stack[:depth]
    if name.endswith('/'): stack.append(name.rstrip('/'))
    else: paths.append('/'.join(stack + [name]))
hdr = re.compile(r'(?:^|\n)' + sep + r'\nFile: (.+)\n' + sep + r'\n\n')
ms = list(hdr.finditer(text))
files = {}
for i, m in enumerate(ms):
    start = m.end(); end = ms[i+1].start() if i+1 < len(ms) else len(text)
    body = text[start:end]
    # dump appends "\n\n" after each file's content
    if body.endswith('\n\n'): body = body[:-2]
    else: print('WARN unexpected tail', m.group(1))
    lines = body.split('\n')
    if lines and lines[0].startswith('```'):
        print('NOTE fence at start of', m.group(1))
    files[m.group(1)] = body
for p, b in files.items():
    dst = os.path.join(out, p); os.makedirs(os.path.dirname(dst) or out, exist_ok=True)
    with open(dst, 'w', encoding='utf-8', newline='') as f: f.write(b)
print('TOC paths:', len(paths), 'extracted:', len(files))
print('missing from dump:', sorted(set(paths) - set(files)))
print('extra not in TOC:', sorted(set(files) - set(paths)))
print('missing on disk:', [p for p in paths if not os.path.isfile(os.path.join(out, p))])
