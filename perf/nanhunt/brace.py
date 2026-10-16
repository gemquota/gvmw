def match_end(lines, start):
    """Return the line index where the block opened on lines[start] closes."""
    depth=0; started=False; in_bc=False
    for k in range(start, len(lines)):
        l=lines[k]; i=0; q=None
        while i < len(l):
            c=l[i]; n=l[i+1] if i+1<len(l) else ''
            if in_bc:
                if c=='*' and n=='/': in_bc=False; i+=2; continue
                i+=1; continue
            if q:
                if c=='\\': i+=2; continue
                if c==q: q=None
                i+=1; continue
            if c=='/' and n=='/': break
            if c=='/' and n=='*': in_bc=True; i+=2; continue
            if c in '\'"`': q=c; i+=1; continue
            if c=='{': depth+=1; started=True
            elif c=='}':
                depth-=1
                if started and depth==0: return k
            i+=1
    raise SystemExit('no match')
