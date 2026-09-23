#!/usr/bin/env python3
import argparse, json, os, sys, urllib.request
BASE='https://openapi.tripo3d.ai/v3'
def req(path, method='GET', payload=None):
    key=os.environ.get('TRIPO_API_KEY')
    if not key: raise SystemExit('TRIPO_API_KEY is not set')
    data=None if payload is None else json.dumps(payload).encode()
    q=urllib.request.Request(BASE+path,data=data,method=method,headers={'Authorization':f'Bearer {key}','Content-Type':'application/json'})
    with urllib.request.urlopen(q,timeout=60) as r: return json.load(r)
p=argparse.ArgumentParser(); sub=p.add_subparsers(dest='cmd',required=True)
sub.add_parser('balance')
s=sub.add_parser('status'); s.add_argument('task_id')
m=sub.add_parser('multiview');
for v in ('front','back','left','right'): m.add_argument('--'+v)
m.add_argument('--model',default='v3.1-20260211'); m.add_argument('--texture',action='store_true'); m.add_argument('--pbr',action='store_true')
a=p.parse_args()
if a.cmd=='balance': out=req('/account/balance')
elif a.cmd=='status': out=req('/tasks/'+a.task_id)
else:
    views=[{v:getattr(a,v)} for v in ('front','back','left','right') if getattr(a,v)]
    if len(views)<2 or not a.front: raise SystemExit('multiview requires --front and at least one more view')
    out=req('/generation/multiview-to-model','POST',{'inputs':views,'model':a.model,'texture':a.texture,'pbr':a.pbr,'geometry_quality':'detailed'})
print(json.dumps(out,indent=2))
