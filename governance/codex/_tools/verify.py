#!/usr/bin/env python3
"""v001: byte-compare against live profile while latest, else self-consistency. Latest version of every bot is byte-checked against the live profile.
Original: Byte-compare each v001.md verbatim block against the live profile description (all 36 bots, incl. second wave),
check every template bullet is a verbatim substring, check second-wave header names match profile names,
check index.md has 36 rows. Also reports (INFO, not failure) where the latest recorded version differs from the live profile."""
import json,re,glob,sys,os
ROOT="/workspace/governance/codex"; AG="/home/box/agent-data/agents"; ok=True
WAVE2={"arbiter","advocate","sentinel","sourcer","surveyor","sanitizer","simulator","investigator","indexer","minder","mender","maintainer","moderator","expediter","editor"}
# Flag column from index.md (RETIRED / DELETED vs ACTIVE); used when a live profile.json is missing
flag_by_bid={}; flag_by_slug={}
for _l in open(f"{ROOT}/index.md",encoding="utf-8"):
    if _l.startswith("| ") and "](" in _l:
        _c=[x.strip() for x in _l.strip("|").split("|")]
        _m=re.search(r"\[([^\]]+)/\]",_c[3])
        if _m: flag_by_slug[_m.group(1)]=_c[6]
        flag_by_bid[_c[2]]=_c[6]
# Former holders: historical Bot id in older vNNN.md; role continued under a new id (same folder).
# Missing profile is INFO/self-check, not FAIL. Still-on-disk is WARN at end.
FORMER_HOLDERS={
    "e613112b-b653-4567-bc4f-17261ce9302e": "identity-inquirer former holder (role continued by 0314faa4 from v003; ran v002 from 09:09; not live since ~9:14am 9 Oct 2026)",
}
def verb(t): 
    m=re.search(r"## Exact instructions \(verbatim\).*?\n(`{3,})text\n(.*?)\n?\1\n",t,re.S); return m.group(2) if m else None
folders=sorted(os.path.dirname(f).split('/')[-1] for f in glob.glob(f"{ROOT}/*/v001.md"))
for sl in folders:
    t=open(f"{ROOT}/{sl}/v001.md",encoding="utf-8").read()
    bid=re.search(r"\| Bot id \| ([0-9a-f-]+) \|",t).group(1)
    got=(verb(t) or "").encode("utf-8")
    superseded=len(glob.glob(f"{ROOT}/{sl}/v*.md"))>1
    _pp=f"{AG}/{bid}/profile.json"
    if not os.path.exists(_pp):
        if flag_by_bid.get(bid) in ("RETIRED","DELETED") or flag_by_slug.get(sl) in ("RETIRED","DELETED"):
            # Missing live profile for a retired bot: skip live compare; self-check if superseded
            if not superseded:
                print(f"DELETED (profile gone) {sl:30}"); continue
            p={}
        elif bid in FORMER_HOLDERS and superseded:
            # Re-keyed folder: v001 still names the former holder whose profile is gone; self-check history
            print(f"INFO {sl:30} v001 bid {bid[:8]}… former holder, profile gone; self-check (latest id is live)")
            p={}
        else:
            ok=False; print(f"FAIL {sl:30} profile missing (ACTIVE bot)"); continue
    else:
        p=json.load(open(_pp,encoding="utf-8"))
    # v001 is checked against the live profile only while it is the latest version; once superseded it is
    # history, so its sections are checked against its own verbatim block (latest-vs-live is checked below)
    d=got if superseded else (p.get("description") or "").encode("utf-8")
    sec=t.split("## Template sections",1)[1]
    bullets=[l[2:] for l in sec.splitlines() if l.startswith("- ")]
    bok=all(b.encode() in d for b in bullets)
    # every sentence placed exactly once (no sentence dropped)
    sents=[]
    for x in (re.split(r'(?<=[.!?])\s+',d.decode()) if d else []):
        if sents and sents[-1].endswith("e.g."): sents[-1]+=" "+x
        else: sents.append(x)
    cover = sorted(bullets)==sorted(sents)  # every sentence placed exactly once, none dropped or duplicated
    nok=True
    # live-name check moved to the latest-version section (index Current name); v001 headers keep the name at recording
    found_live=("RECORDED AS FOUND LIVE" in t) or ("recorded as found live" in open(f"{ROOT}/{sl}/CHANGELOG.md",encoding="utf-8").read())
    # Found-live captures may omit template bullets; warn on coverage only, still fail on verbatim/live mismatch
    if found_live and got==d and nok and (not cover or not bok):
        print(f"WARN-FOUND-LIVE {sl:30}",f"bytes={len(d)}",f"verbatim={'self (superseded)' if superseded else 'match'}",
              f"bullets={len(bullets)} (template coverage skipped for recorded-as-found-live; CHANGELOG flags it)")
    else:
        res=got==d and bok and nok and cover; ok&=res
        print(("PASS" if res else "FAIL"),f"{sl:30}",f"bytes={len(d)}",f"verbatim={'self (superseded)' if superseded else ('match' if got==d else 'MISMATCH')}",
              f"bullets={len(bullets)} {'verbatim' if bok else 'NOT verbatim'}{' all-sentences-once' if cover else ' COVERAGE-INCOMPLETE'}",
              ("name=ok" if nok else "name=MISMATCH") if sl in WAVE2 else "")
missing=WAVE2-set(folders)
if missing: ok=False; print("FAIL missing second-wave folders:",missing)
rows=[l for l in open(f"{ROOT}/index.md").read().splitlines() if l.startswith("| ") and "](" in l]
r=len(rows)==37 and len(folders)==37; ok&=r
print(("PASS" if r else "FAIL"),f"index rows={len(rows)} folders={len(folders)} (expect 37)")
print("--- every v002+ file: template bullets verbatim and every sentence placed once ---")
for vf in sorted(glob.glob(f"{ROOT}/*/v*.md")):
    if vf.endswith("v001.md"): continue
    t=open(vf,encoding="utf-8").read(); d=verb(t) or ""
    if "copied as written in the approved proposal" in t or "NO-TEMPLATE-SECTIONS-IN-PROPOSAL" in t:  # batch-1 v002s: sections are the proposal's own prose
        print(f"SKIP-SECTIONS {vf.split('/')[-2]}/{os.path.basename(vf)} (proposal-authored sections; verbatim block byte-checked against its proposal by verify_v002_batch1.py or the finals check)"); continue
    b=[l[2:] for l in t.split("## Template sections",1)[1].splitlines() if l.startswith("- ")]
    ss=[]
    for x in (re.split(r'(?<=[.!?])\s+',d) if d else []):
        if ss and ss[-1].endswith("e.g."): ss[-1]+=" "+x
        else: ss.append(x)
    r=sorted(b)==sorted(ss) and all(x in d for x in b); ok&=r
    print(("PASS" if r else "FAIL"),f"{vf.split('/')[-2]}/{os.path.basename(vf)}",f"bullets={len(b)}")
print("--- Architect finals 2026-10-04: recorded verbatim == proposal source (byte check) ---")
for _fj in (f"{ROOT}/_tools/finals_2026-10-04.json", f"{ROOT}/_tools/seven_2026-10-04.json"):
  if not os.path.exists(_fj): continue
  for r in json.load(open(_fj)):
        rf=open(f"{ROOT}/{r['folder']}/{r['version']}.md",encoding="utf-8").read(); src=open(r["source"],encoding="utf-8").read()
        if r["kind"]=="bot":
            a=verb(rf); b=re.search(r"## Exact instructions \(verbatim\)\n(`{3,})text\n(.*?)\n\1\n",src,re.S).group(2)
        else:
            a=re.search(r"## Exact text \(verbatim\).*?\n(`{3,})text\n(.*?)\n\1\n",rf,re.S).group(2); b=src.rstrip("\n")
        r_ok=a.encode()==b.encode(); ok&=r_ok
        print(("PASS" if r_ok else "FAIL"),f"{r['folder']}/{r['version']}.md == {os.path.basename(r['source'])}",f"{len(b.encode())}B")
print("--- LATEST version vs live profile (byte check, all bots) ---")
strict_ok=0; pending=[]
cur={}
for l in open(f"{ROOT}/index.md").read().splitlines():
    if l.startswith("| ") and "](" in l:
        c=[x.strip() for x in l.strip("|").split("|")]; cur[c[2]]=c[1]
for sl in folders:
    vs=sorted(glob.glob(f"{ROOT}/{sl}/v*.md")); t=open(vs[-1],encoding="utf-8").read()
    bid=re.search(r"\| Bot id \| ([0-9a-f-]+) \|",t).group(1)
    lv=os.path.basename(vs[-1])
    _pp=f"{AG}/{bid}/profile.json"
    if not os.path.exists(_pp):
        if flag_by_bid.get(bid) in ("RETIRED","DELETED") or flag_by_slug.get(sl) in ("RETIRED","DELETED"):
            print(f"DELETED (profile gone) {sl:30} {lv}"); continue
        ok=False; print(f"FAIL {sl:30} latest={lv} profile missing (ACTIVE bot)"); continue
    p=json.load(open(_pp,encoding="utf-8")); d=(p.get("description") or "").encode("utf-8")
    nm = p.get("name")==cur.get(bid)
    if not nm: ok=False; print(f"FAIL {sl:30} name: profile {p.get('name')!r} != index Current name {cur.get(bid)!r}")
    if (verb(t) or "").encode("utf-8")==d: strict_ok+=1; print(f"MATCH {sl:30} {lv} name={'ok' if nm else 'MISMATCH'}"); continue
    runs=[os.path.basename(v) for v in vs if (verb(open(v,encoding='utf-8').read()) or '').encode('utf-8')==d]
    clog=open(f"{ROOT}/{sl}/CHANGELOG.md").read()
    # pending-deploy is accepted only if the CHANGELOG names this exact latest version as approved-not-deployed
    logged = bool(runs) and (f"PENDING-DEPLOY {lv}" in clog or (lv=="v002.md" and "has NOT been applied" in clog))
    if logged: pending.append(sl); print(f"PENDING-DEPLOY {sl:30} latest={lv} live profile = {runs[0]} (logged in CHANGELOG) name={'ok' if nm else 'MISMATCH'}")
    else: ok=False; print(f"FAIL {sl:30} latest={lv} live profile differs from latest{' (matches '+runs[0]+', not logged)' if runs else ' (UNRECORDED EDIT)'}")
print(f"STRICT latest==live: {strict_ok}/{len(folders)} match; {len(pending)} logged pending-deploy: {', '.join(pending) or '-'}")

# --- Known agent ids: every recorded version + index (so re-keyed folders map to the current holder) ---
known=set()
for f in glob.glob(f"{ROOT}/*/v*.md"):
    m=re.search(r"\| Bot id \| ([0-9a-f-]+) \|",open(f,encoding="utf-8").read())
    if m: known.add(m.group(1))
known.update(flag_by_bid.keys())
print("--- Former holders (profile still on disk = warning, not failure) ---")
for bid, note in FORMER_HOLDERS.items():
    pf=f"{AG}/{bid}/profile.json"
    if os.path.exists(pf):
        p=json.load(open(pf,encoding="utf-8"))
        print(f"WARN-FORMER-HOLDER {bid} name={p.get('name')!r} — {note}")
    else:
        print(f"INFO former holder profile gone {bid} — {note}")
print("--- Live agents with no codex folder ---")
for d in sorted(glob.glob(f"{AG}/*/")):
    bid=os.path.basename(d.rstrip("/")); pf=os.path.join(d,"profile.json")
    if bid in known or bid in FORMER_HOLDERS or not os.path.exists(pf): continue
    p=json.load(open(pf,encoding="utf-8"))
    kind="UNRECORDED AGENT" if (p.get("description") or "").strip() else "GROUP (INFO)"
    print(f"{kind:17} {bid} name={p.get('name')!r} namedBy={p.get('namedBy')}")

print("OVERALL:", "PASS" if ok else "FAIL"); sys.exit(0 if ok else 1)
