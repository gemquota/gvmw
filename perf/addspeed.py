import sys, json
key, label, help_what, help_effect, help_tuning = sys.argv[1:6]
R='/workspace/vepa/'
def rep(p, old, new, cnt=1):
    s=open(R+p).read(); assert s.count(old)==cnt,(p,old[:70],s.count(old)); s=s.replace(old,new); open(R+p,'w').write(s)
p='src/state/worldParams.js'
s=open(R+p).read()
# insert after the last SPEED def line
lines=s.split('\n'); idx=max(i for i,l in enumerate(lines) if "subgroup: 'SPEED' }" in l)
lines.insert(idx+1, f"  {{ key: '{key}', label: '{label}', min: 0, max: 1, default: 0, step: 1, group: 'PERFORMANCE', subgroup: 'SPEED' }},")
s='\n'.join(lines)
import re
m=re.search(r"export const SPEED_PARAM_KEYS = Object.freeze\(\[([^\]]*)\]\);", s)
s=s.replace(m.group(0), f"export const SPEED_PARAM_KEYS = Object.freeze([{m.group(1)}, '{key}']);")
open(R+p,'w').write(s)
js=lambda t: "'" + t.replace("\\","\\\\").replace("'","\\'") + "'"
rep('src/ui/paramHelp.js',"  EXPENSIVE_LAW_CADENCE: {", f"  {key}: {{ what: {js(help_what)}, effect: {js(help_effect)}, tuning: {js(help_tuning)}, units: '0/1 toggle.' }},\n  EXPENSIVE_LAW_CADENCE: {{")
