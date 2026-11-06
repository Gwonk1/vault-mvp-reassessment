"""Download genome-wide expression + clinical data per cohort. Never prints expression values."""
import gzip, hashlib, json, os, sys, time
import numpy as np, pandas as pd, requests
from concurrent.futures import ThreadPoolExecutor

API = 'https://www.cbioportal.org/api'
OUT = 'data/processed/bulk'
os.makedirs(OUT, exist_ok=True)
S = requests.Session(); S.headers['Content-Type'] = 'application/json'
ICB = {
 'riaz':     ('mel_iatlas_riaz_nivolumab_2017', 'mel_iatlas_riaz_nivolumab_2017_rna_seq_mrna'),
 'hugo':     ('mel_iatlas_hugo_ucla_2016', 'mel_iatlas_hugo_ucla_2016_rna_seq_mrna'),
 'liu':      ('mel_iatlas_liu_2019', 'mel_iatlas_liu_2019_rna_seq_mrna'),
 'gide':     ('mel_iatlas_gide_2019', 'mel_iatlas_gide_2019_rna_seq_mrna'),
 'vanallen': ('skcm_dfci_2015', 'skcm_dfci_2015_rna_seq_mrna'),
 'imvigor':  ('blca_iatlas_imvigor210_2017', 'blca_iatlas_imvigor210_2017_rna_seq_mrna'),
}
TCGA = {c: (f'{c}_tcga_pan_can_atlas_2018', f'{c}_tcga_pan_can_atlas_2018_rna_seq_v2_mrna')
        for c in ['luad', 'lusc', 'skcm', 'paad', 'lihc', 'thca']}

def req(method, path, **kw):
    for i in range(6):
        try:
            r = S.request(method, API + path, timeout=300, **kw)
            if r.status_code == 200: return r.json()
            err = r.status_code
        except requests.RequestException as e:
            err = e
        time.sleep(2 ** i)
    raise RuntimeError(f'{path}: {err}')

def genes():
    p = OUT + '/genes.parquet'
    if os.path.exists(p): return pd.read_parquet(p)
    g = pd.DataFrame(req('GET', '/genes?pageSize=100000&projection=SUMMARY'))
    g = g[g.entrezGeneId > 0][['entrezGeneId', 'hugoGeneSymbol', 'type']]
    g = g[g.type == 'protein-coding']
    g.to_parquet(p); return g

def fetch(name, study, profile, g):
    p = f'{OUT}/{name}.expr.parquet'
    samples = [s['sampleId'] for s in req('GET', f'/studies/{study}/samples?pageSize=100000')]
    ids = g.entrezGeneId.tolist(); chunks = [ids[i:i + 1500] for i in range(0, len(ids), 1500)]
    def one(ch):
        rows = req('POST', f'/molecular-profiles/{profile}/molecular-data/fetch?projection=SUMMARY',
                   json={'entrezGeneIds': ch, 'sampleIds': samples})
        return [(r['entrezGeneId'], r['sampleId'], r['value']) for r in rows]
    if not os.path.exists(p):
        with ThreadPoolExecutor(4) as ex: parts = list(ex.map(one, chunks))
        d = pd.DataFrame([x for pt in parts for x in pt], columns=['e', 's', 'v'])
        d['v'] = pd.to_numeric(d.v, errors='coerce')
        m = d.pivot_table(index='e', columns='s', values='v', aggfunc='first')
        m.index = m.index.map(dict(zip(g.entrezGeneId, g.hugoGeneSymbol)))
        m.columns = m.columns.astype(str); m.to_parquet(p)
    else:
        m = pd.read_parquet(p)
    cl = {}
    for typ in ['SAMPLE', 'PATIENT']:
        rows = req('GET', f'/studies/{study}/clinical-data?clinicalDataType={typ}&projection=DETAILED&pageSize=10000000')
        for r in rows:
            cl.setdefault(r['sampleId'] if typ == 'SAMPLE' else None, {})
        d = pd.DataFrame(rows)
        if typ == 'SAMPLE':
            s = d.pivot_table(index='sampleId', columns='clinicalAttributeId', values='value', aggfunc='first')
            s['patientId'] = d.groupby('sampleId').patientId.first()
        else:
            q = d.pivot_table(index='patientId', columns='clinicalAttributeId', values='value', aggfunc='first') if len(d) else None
    s = s.reset_index()
    if q is not None:
        s = s.merge(q.reset_index(), on='patientId', how='left', suffixes=('', '_pt'))
    s.astype(str).to_parquet(f'{OUT}/{name}.clin.parquet')
    print(name, 'genes x samples', m.shape, 'sha256', hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16],
          'treatment:', s['SAMPLE_TREATMENT'].value_counts().to_dict() if 'SAMPLE_TREATMENT' in s else None, flush=True)

if __name__ == '__main__':
    g = genes()
    for name, (st, pr) in {**ICB, **TCGA}.items():
        try: fetch(name, st, pr, g)
        except Exception as e: print(name, 'FAILED', repr(e), flush=True)
