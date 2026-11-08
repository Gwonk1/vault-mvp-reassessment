#!/usr/bin/env python3
"""Coverage repair for the dN/dS test. NOT BLIND: MVP=0.1431 was known before this ran.
See DNDS_PREREGISTRATION.md 'Repair run' and RESULTS.md 79."""
import json, time, urllib.request, urllib.error, statistics as st, warnings
warnings.filterwarnings('ignore')
from Bio.codonalign.codonseq import CodonSeq, cal_dn_ds

GENES=[('MVP','subject'),('TEP1','comparator'),('PARP4','comparator'),
       ('RPL7','essential'),('ACTB','essential'),('GAPDH','essential'),('TUBB','essential'),
       ('MX1','relaxed'),('CD4','relaxed'),('FCGR2B','relaxed')]
MAMMAL=["mus_musculus","rattus_norvegicus","canis_lupus_familiaris","bos_taurus",
        "macaca_mulatta","monodelphis_domestica","sus_scrofa","oryctolagus_cuniculus",
        "equus_caballus","ovis_aries"]
DEEP=['gallus_gallus','xenopus_tropicalis','danio_rerio']
SAT=1.5; STOPS={'TAA','TAG','TGA'}; OK=set('ACGT')

def fetch(gene, sp):
    """Returns (kind, payload). kind in {'ok','empty','http','net'} - never merged."""
    UA={"User-Agent":"vault-reassessment/1.0 (research script)"}
    url=(f"https://rest.ensembl.org/homology/symbol/homo_sapiens/{gene}"
         f"?type=orthologues;content-type=application/json;sequence=cds;target_species={sp}")
    for attempt in range(5):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120) as r:
                if r.status != 200: return ('http', f'status {r.status}')
                d=json.loads(r.read())
            hom=(d.get('data') or [{}])[0].get('homologies') or []
            return ('ok', hom) if hom else ('empty', 'HTTP 200, homology list empty')
        except urllib.error.HTTPError as e:
            if (e.code>=500 or e.code==429) and attempt<4: time.sleep(5*(2**attempt)); continue
            return ('http', f'HTTP {e.code}')
        except Exception as e:
            if attempt<4: time.sleep(3*(attempt+1)); continue
            return ('net', f'{type(e).__name__}')
    return ('net','retries exhausted')

def pick(h):
    o2o=[x for x in h if x.get('type')=='ortholog_one2one']
    return sorted(o2o or h, key=lambda x:(-(x['target'].get('perc_id') or 0), x['target']['id']))[0]

def clean(a,b):
    ka=[];kb=[]
    for i in range(0,min(len(a),len(b))-2,3):
        ca,cb=a[i:i+3].upper(),b[i:i+3].upper()
        if len(ca)<3 or len(cb)<3 or not set(ca)<=OK or not set(cb)<=OK: continue
        if ca in STOPS or cb in STOPS: continue
        ka.append(ca);kb.append(cb)
    return ''.join(ka),''.join(kb)

rows=[]
for gene,cls in GENES:
    for sp in MAMMAL+DEEP:
        tier='mammal' if sp in MAMMAL else 'deep'
        kind,payload=fetch(gene,sp); time.sleep(1.0)
        if kind!='ok':
            rows.append(dict(gene=gene,cls=cls,sp=sp,tier=tier,status=kind,detail=payload)); continue
        h=pick(payload)
        ca,cb=clean(h['source'].get('align_seq') or '', h['target'].get('align_seq') or '')
        n=len(ca)//3
        if n<100:
            rows.append(dict(gene=gene,cls=cls,sp=sp,tier=tier,status='short',detail=f'{n} codons')); continue
        try: dn,ds=cal_dn_ds(CodonSeq(ca),CodonSeq(cb),method='NG86')
        except Exception as e:
            rows.append(dict(gene=gene,cls=cls,sp=sp,tier=tier,status='ng86_err',detail=type(e).__name__)); continue
        if ds is None or ds<=0:
            rows.append(dict(gene=gene,cls=cls,sp=sp,tier=tier,status='ds_unusable',detail=str(ds))); continue
        rows.append(dict(gene=gene,cls=cls,sp=sp,tier=tier,status='ok',n_codons=n,
                         dn=round(dn,4),ds=round(ds,4),w=round(dn/ds,4),sat=bool(ds>SAT),
                         htype=h.get('type'),perc_id=h['target'].get('perc_id')))
        print(f"  {gene:7s} {sp:26s} {tier:6s} n={n:4d} dN={dn:.4f} dS={ds:.4f} w={dn/ds:.4f}"
              f"{'  [SAT]' if ds>SAT else ''}",flush=True)
json.dump(rows,open('results/dnds3.json','w'),indent=1)
print(f"\n  wrote results/dnds3.json ({len(rows)} rows)")
