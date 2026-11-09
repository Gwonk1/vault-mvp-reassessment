#!/usr/bin/env python3
"""Tier 0a step 1: harvest MVP CDS per species via the homology endpoint that works,
de-gap to recover raw CDS, write FASTA. Registered at 06dd589."""
import json, time, urllib.request, urllib.error, re, pathlib
SP=['rattus_norvegicus','canis_lupus_familiaris','bos_taurus','ovis_aries','equus_caballus',
    'oryctolagus_cuniculus','monodelphis_domestica','gallus_gallus','xenopus_tropicalis','danio_rerio']
UA={'User-Agent':'vault-reassessment/1.0 (research script)'}
OUT=pathlib.Path('/tmp/claude-1000/-home-graham-projects/46738ac0-1f6d-4b80-81fe-caa9aa37b1a5/scratchpad/t0')
OUT.mkdir(parents=True, exist_ok=True)

def get(sp):
    url=(f"https://rest.ensembl.org/homology/symbol/homo_sapiens/MVP"
         f"?type=orthologues;content-type=application/json;sequence=cds;target_species={sp}")
    for a in range(6):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=150) as r:
                if r.status!=200: raise urllib.error.HTTPError(url, r.status, 'bad', None, None)
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            if a<5: time.sleep(6*(a+1)); continue
            return {'_err':f'HTTP {e.code}'}
        except Exception as e:
            if a<5: time.sleep(5*(a+1)); continue
            return {'_err':type(e).__name__}

seqs={}
for sp in SP:
    d=get(sp); time.sleep(1.5)
    if '_err' in d or not d.get('data') or not d['data'][0].get('homologies'):
        print(f"  {sp:26s} {d.get('_err','no homology')}", flush=True); continue
    h=d['data'][0]['homologies']
    o2o=[x for x in h if x.get('type')=='ortholog_one2one']
    pick=sorted(o2o or h, key=lambda x:(-(x['target'].get('perc_id') or 0), x['target']['id']))[0]
    if 'human' not in seqs:
        hs=(pick['source'].get('align_seq') or '').replace('-','')
        if hs: seqs['human']=hs
    ts=(pick['target'].get('align_seq') or '').replace('-','')
    if ts:
        seqs[sp]=ts
        print(f"  {sp:26s} CDS {len(ts):5d} nt  ({pick.get('type')}, perc_id {pick['target'].get('perc_id')})", flush=True)

with open(OUT/'mvp_cds.fna','w') as fh:
    for k,v in seqs.items(): fh.write(f">{k}\n{v}\n")
print(f"\n  wrote {len(seqs)} CDS sequences -> {OUT/'mvp_cds.fna'}")
print("  lengths:", {k:len(v) for k,v in seqs.items()})
