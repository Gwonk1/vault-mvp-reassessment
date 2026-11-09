#!/usr/bin/env python3
"""Tier 0a step 1: MVP CDS per species, FAST and INCREMENTAL.
Rewritten after the first version spent 18 min on 2 species (budget too generous)
and wrote its FASTA only at the end, losing both. Registered at 06dd589."""
import json, time, urllib.request, urllib.error, pathlib, sys
# species that actually returned MVP CDS in the dnds3 run; mouse/macaque/pig failed there
SP=['rattus_norvegicus','canis_lupus_familiaris','bos_taurus','ovis_aries','equus_caballus',
    'oryctolagus_cuniculus','monodelphis_domestica','gallus_gallus','xenopus_tropicalis']
UA={'User-Agent':'vault-reassessment/1.0 (research script)','Accept':'application/json'}
OUT=pathlib.Path('/tmp/claude-1000/-home-graham-projects/46738ac0-1f6d-4b80-81fe-caa9aa37b1a5/scratchpad/t0')
OUT.mkdir(parents=True, exist_ok=True)
FA=OUT/'mvp_cds.fna'
FA.write_text('')                      # fresh, then append per species

def get(sp, tries=2, to=45):
    url=(f"https://rest.ensembl.org/homology/symbol/homo_sapiens/MVP"
         f"?type=orthologues;content-type=application/json;sequence=cds;target_species={sp}")
    for a in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=to) as r:
                return json.loads(r.read())
        except Exception as e:
            if a+1 < tries: time.sleep(4); continue
            return {'_err': f'{type(e).__name__}'}

def emit(name, seq):
    with FA.open('a') as fh: fh.write(f">{name}\n{seq}\n")

have_human=False
for sp in SP:
    t0=time.time(); d=get(sp)
    if '_err' in d or not d.get('data') or not d['data'][0].get('homologies'):
        print(f"  {sp:26s} {d.get('_err','no homology'):18s} {time.time()-t0:5.1f}s", flush=True); continue
    h=d['data'][0]['homologies']
    o2o=[x for x in h if x.get('type')=='ortholog_one2one']
    pick=sorted(o2o or h, key=lambda x:(-(x['target'].get('perc_id') or 0), x['target']['id']))[0]
    if not have_human:
        hs=(pick['source'].get('align_seq') or '').replace('-','')
        if hs: emit('human', hs); have_human=True; print(f"  human                      CDS {len(hs):5d} nt", flush=True)
    ts=(pick['target'].get('align_seq') or '').replace('-','')
    if ts:
        emit(sp, ts)
        print(f"  {sp:26s} CDS {len(ts):5d} nt  {pick.get('type'):20s} {time.time()-t0:5.1f}s", flush=True)
    time.sleep(0.8)
n=FA.read_text().count('>')
print(f"\n  {n} sequences written incrementally -> {FA}", flush=True)
