"""Download CPTAC-style mass-spec protein matrices from cBioPortal."""
import os, time, json
import pandas as pd, requests
from concurrent.futures import ThreadPoolExecutor
API='https://www.cbioportal.org/api'; OUT='data/processed/prot'
S=requests.Session(); S.headers['Content-Type']='application/json'
def req(m,p,**kw):
    for i in range(6):
        try:
            r=S.request(m,API+p,timeout=400,**kw)
            if r.status_code==200: return r.json()
            err=r.status_code
        except requests.RequestException as e: err=e
        time.sleep(2**i)
    raise RuntimeError(f'{p}: {err}')
profs=[m for m in req('GET','/molecular-profiles?projection=SUMMARY&pageSize=100000')
       if m['molecularAlterationType']=='PROTEIN_LEVEL' and m['molecularProfileId'].endswith('protein_quantification')]
genes=pd.DataFrame(req('GET','/genes?pageSize=100000&projection=SUMMARY'))
genes=genes[(genes.entrezGeneId>0)&(genes.type=='protein-coding')]
ids=genes.entrezGeneId.tolist(); chunks=[ids[i:i+2000] for i in range(0,len(ids),2000)]
sym=dict(zip(genes.entrezGeneId,genes.hugoGeneSymbol))
for m in profs:
    st=m['studyId']; pid=m['molecularProfileId']; out=f'{OUT}/{st}.parquet'
    if os.path.exists(out): print('have',st,flush=True); continue
    try:
        samples=[s['sampleId'] for s in req('GET',f'/studies/{st}/samples?pageSize=100000')]
        if len(samples)<50: print('skip',st,len(samples),flush=True); continue
        def one(ch):
            return [(r['entrezGeneId'],r['sampleId'],r['value']) for r in
                    req('POST',f'/molecular-profiles/{pid}/molecular-data/fetch?projection=SUMMARY',
                        json={'entrezGeneIds':ch,'sampleIds':samples})]
        with ThreadPoolExecutor(3) as ex: parts=list(ex.map(one,chunks))
        d=pd.DataFrame([x for p in parts for x in p],columns=['e','s','v'])
        if not len(d): print('empty',st,flush=True); continue
        d['v']=pd.to_numeric(d.v,errors='coerce')
        M=d.pivot_table(index='e',columns='s',values='v',aggfunc='first')
        M.index=M.index.map(sym); M.columns=M.columns.astype(str)
        M.to_parquet(out)
        cl=pd.DataFrame(req('GET',f'/studies/{st}/clinical-data?clinicalDataType=SAMPLE&projection=DETAILED&pageSize=10000000'))
        if len(cl):
            c=cl.pivot_table(index='sampleId',columns='clinicalAttributeId',values='value',aggfunc='first')
            c['patientId']=cl.groupby('sampleId').patientId.first()
            c.reset_index().astype(str).to_parquet(f'{OUT}/{st}.clin.parquet')
        print('OK',st,M.shape,flush=True)
    except Exception as e: print('FAIL',st,repr(e)[:120],flush=True)
