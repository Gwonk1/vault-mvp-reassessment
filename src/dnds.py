#!/usr/bin/env python3
"""dN/dS for MVP against controls, in lineages that retained MVP.
Registered in DNDS_PREREGISTRATION.md (commit e8997c8) before any value was computed."""
import json, time, urllib.request, statistics, warnings, sys
warnings.filterwarnings('ignore')
from Bio.codonalign.codonseq import CodonSeq, cal_dn_ds

GENES = [('MVP','subject'), ('TEP1','comparator'), ('PARP4','comparator'),
         ('RPL7','essential'), ('ACTB','essential'), ('GAPDH','essential'), ('TUBB','essential'),
         ('TRIM5','relaxed'), ('MX1','relaxed'), ('APOBEC3G','relaxed')]
SPECIES = ['mus_musculus','gallus_gallus','xenopus_tropicalis','danio_rerio','ciona_intestinalis']
SAT = 1.5                      # registered saturation threshold on dS
STOPS = {'TAA','TAG','TGA'}
OK = set('ACGT')

def fetch(gene, sp):
    url = (f"https://rest.ensembl.org/homology/symbol/homo_sapiens/{gene}"
           f"?type=orthologues;content-type=application/json;sequence=cds;target_species={sp}")
    for attempt in range(3):
        try:
            with urllib.request.urlopen(url, timeout=90) as r:
                return json.loads(r.read())
        except Exception as e:
            if attempt == 2: return {'_err': f'{type(e).__name__}: {e}'}
            time.sleep(2 + 3*attempt)

def pick(homologies):
    """Registered tie-break: one2one, else highest perc_id, else first stable id."""
    if not homologies: return None
    o2o = [h for h in homologies if h.get('type') == 'ortholog_one2one']
    pool = o2o or homologies
    return sorted(pool, key=lambda h: (-(h['target'].get('perc_id') or 0), h['target']['id']))[0]

def clean_codons(a, b):
    """Drop codon columns with a gap, ambiguity or stop in either sequence."""
    ka, kb = [], []
    for i in range(0, min(len(a), len(b)) - 2, 3):
        ca, cb = a[i:i+3].upper(), b[i:i+3].upper()
        if len(ca) < 3 or len(cb) < 3: continue
        if not set(ca) <= OK or not set(cb) <= OK: continue
        if ca in STOPS or cb in STOPS: continue
        ka.append(ca); kb.append(cb)
    return ''.join(ka), ''.join(kb)

rows = []
for gene, cls in GENES:
    for sp in SPECIES:
        d = fetch(gene, sp); time.sleep(0.35)
        if '_err' in d or not d.get('data') or not d['data'][0].get('homologies'):
            rows.append(dict(gene=gene, cls=cls, sp=sp, status=d.get('_err','no orthologue')))
            continue
        h = pick(d['data'][0]['homologies'])
        a, b = h['source'].get('align_seq') or '', h['target'].get('align_seq') or ''
        ca, cb = clean_codons(a, b)
        n = len(ca)//3
        if n < 100:
            rows.append(dict(gene=gene, cls=cls, sp=sp, status=f'only {n} clean codons')); continue
        try:
            dn, ds = cal_dn_ds(CodonSeq(ca), CodonSeq(cb), method='NG86')
        except Exception as e:
            rows.append(dict(gene=gene, cls=cls, sp=sp, status=f'NG86 {type(e).__name__}')); continue
        if ds is None or ds <= 0:
            rows.append(dict(gene=gene, cls=cls, sp=sp, status=f'dS={ds} unusable', dn=dn)); continue
        rows.append(dict(gene=gene, cls=cls, sp=sp, status='ok', n_codons=n, dn=round(dn,4),
                         ds=round(ds,4), w=round(dn/ds,4), sat=bool(ds > SAT),
                         htype=h.get('type'), perc_id=h['target'].get('perc_id')))
        print(f"  {gene:9s} {sp:22s} n={n:4d} dN={dn:.4f} dS={ds:.4f} w={dn/ds:.4f}"
              f"{'  [SATURATED]' if ds>SAT else ''}", flush=True)

json.dump(rows, open('results/dnds.json','w'), indent=1)
print(f"\n  wrote results/dnds.json ({len(rows)} rows)")
