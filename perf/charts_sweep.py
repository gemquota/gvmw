import json, subprocess, csv, sys, os
os.chdir('/workspace/vepa')
NODE = '/workspace/tools/node22/node-v22.23.3-linux-x64/bin/node'
SWEEPS = {
 'PAIRWISE_BUDGET':      [8,16,24,48,96,192,512],
 'SPEED_PAIR_BUDGET':    [8,12,20,40,80,160,512],
 'SPEED_MID_RANGE':      [30,60,120,200,400,600],
 'SPEED_NEAR_RANGE':     [10,20,30,45,60],
 'SPEED_SYMBIOSIS_RANGE':[10,30,100,300,600],
 'SPEED_SOCIAL_EVERY':   [1,2,4,8,16],
 'SPEED_EXPENSIVE_EVERY':[1,2,4,8,16],
}
only = sys.argv[1:] or list(SWEEPS)
out = '/workspace/out/speed-charts/individual-raw.csv'
new = not os.path.exists(out)
f = open(out, 'a', newline=''); w = csv.writer(f)
if new: w.writerow(['slider','value','size','ms_per_tick','ticks_per_s','alive','species','bonded','bonded_pct','hash','load1'])
for key in only:
    vals = SWEEPS[key]
    r = subprocess.run([NODE,'bench/solver-tps.mjs','--sizes','2500,10000','--runs','1','--warm','3','--json','--sweep',f"{key}={'/'.join(map(str,vals))}"] + ['--ticks','10'], capture_output=True, text=True)
    if r.returncode: print(r.stderr); sys.exit(1)
    j = json.loads(r.stdout[r.stdout.index('{'):])
    for v in vals:
        for n, x in j['variants'][f'{key}={v}'].items():
            w.writerow([key, v, n, x['medMsPerTick'], x['ticksPerSec'], x['alive'], x['species'], x['bonded'], round(100*x['bonded']/max(1,x['alive']),2), x['hash'], j['load1Start']])
    f.flush(); print('done', key, flush=True)
