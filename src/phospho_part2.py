"""Part 2: phosphostoichiometry. dp = phosphosite residualised on its own gene's total protein."""
import json,os,time,sys,numpy as np,pandas as pd,requests
from scipy.stats import spearmanr
sys.path.insert(0,'src')
from prot_coabund import vreml
API='https://www.cbioportal.org/api'; S=requests.Session(); S.headers['Content-Type']='application/json'
PH={'brain_cptac_2020':'brain_cptac_2020_phosphoprotein','brca_cptac_2020':'brca_cptac_2020_phosphoproteome',
 'coad_cptac_2019':'coad_cptac_2019_phosphoprotein_quantification','gbm_cptac_2021':'gbm_cptac_2021_phosphoproteome',
 'luad_cptac_2020':'luad_cptac_2020_phosphoproteome','lusc_cptac_2021':'lusc_cptac_2021_phosphoproteome',
 'paad_cptac_2021':'paad_cptac_2021_phosphoproteome','ucec_cptac_2020':'ucec_cptac_2020_phosphoproteome'}
CORE=['MVP','PARP4','TEP1','ANXA2','S100A10']
SIG=['PTPN11','SRC','STAT1','PRKCA','PRKCD','PRKCE']
GATE=['MAPK1','MAPK3','MAP2K1','MAP2K2','RPS6KA1','RPS6KA3','BRAF','EGFR']
TARGETS=set(CORE+SIG+GATE)
rng=np.random.default_rng(20261107)
def req(m,p,**kw):
    for i in range(5):
        try:
            r=S.request(m,API+p,timeout=600,**kw)
            if r.status_code==200: return r.json()
        except requests.RequestException: pass
        time.sleep(2**i)
    return None
os.makedirs('data/processed/phospho',exist_ok=True)
res={}
for st,prof in PH.items():
    f=f'data/processed/phospho/{st}.parquet'
    if os.path.exists(f): res[st]=pd.read_parquet(f); print('have',st,res[st].shape,flush=True); continue
    meta=req('GET',f'/generic-assay-meta/{prof}')
    if not meta: print('no meta',st,flush=True); continue
    g={e['stableId']:(e.get('genericEntityMetaProperties') or {}).get('GENE_SYMBOL') for e in meta}
    tgt=[k for k,v in g.items() if v in TARGETS]
    rest=[k for k,v in g.items() if v and v not in TARGETS]
    bg=list(rng.choice(rest,min(1500,len(rest)),replace=False))
    ids=sorted(set(tgt+bg))
    d=req('POST',f'/generic_assay_data/{prof}/fetch?projection=SUMMARY',
          json={'genericAssayStableIds':ids,'sampleListId':f'{st}_all'})
    if not d: print('no data',st,flush=True); continue
    D=pd.DataFrame([(r['genericAssayStableId'],r['sampleId'],r.get('value')) for r in d],columns=['sid','sample','v'])
    D['v']=pd.to_numeric(D.v,errors='coerce')
    M=D.pivot_table(index='sid',columns='sample',values='v',aggfunc='first')
    M['__gene']=[g.get(i) for i in M.index]
    M.to_parquet(f); res[st]=M; print('fetched',st,M.shape,'| targets',len(tgt),flush=True)
print('\ncohorts with phospho:',list(res),flush=True)
def resid(y,x):
    m=np.isfinite(y)&np.isfinite(x)
    if m.sum()<25 or np.nanstd(x[m])==0: return None
    b=np.polyfit(x[m],y[m],1); out=np.full(len(y),np.nan); out[m]=y[m]-np.polyval(b,x[m]); return out
DP={}; LOAD={}
for st,M in res.items():
    P=pd.read_parquet(f'data/processed/prot/{st}.parquet'); P=P[~P.index.duplicated()]
    cols=[c for c in M.columns if c!='__gene' and c in P.columns]
    if len(cols)<30: print('too few matched samples',st,len(cols),flush=True); continue
    genes=M['__gene']
    dp={}
    for sid in M.index:
        gsym=genes[sid]
        if gsym not in P.index: continue
        r=resid(M.loc[sid,cols].values.astype(float),P.loc[gsym,cols].values.astype(float))
        if r is not None: dp[sid]=r
    DP[st]=(pd.DataFrame(dp,index=cols).T,genes)
    ld={}
    for p in ['PARP4','TEP1']:
        if p in P.index and 'MVP' in P.index:
            r=resid(P.loc[p,cols].values.astype(float),P.loc['MVP',cols].values.astype(float))
            if r is not None: ld[p]=pd.Series(r,index=cols)
    LOAD[st]=ld
    print(f'  {st}: {len(dp)} residualised sites, {len(cols)} samples, loading {list(ld)}',flush=True)
# GATE
gate_ok=False
for st,(T,genes) in DP.items():
    m1=[s for s in T.index if genes[s]=='MAPK1' and ('185' in str(s) or '187' in str(s))]
    if not m1: continue
    base=T.loc[m1[0]]
    def safe(r):
        m=np.isfinite(r.values)&np.isfinite(base.values)
        if m.sum()<20: return np.nan
        return spearmanr(r.values[m],base.values[m]).statistic
    rr=T.apply(safe,axis=1).drop(m1[0]).dropna().sort_values(ascending=False)
    top=[genes[s] for s in rr.index[:25]]
    hits=[g for g in top if g in ['MAPK3','MAP2K1','MAP2K2','RPS6KA1','RPS6KA3','BRAF','EGFR','MAPK1']]
    print(f'GATE {st}: MAPK1 top25 contains {sorted(set(hits))}',flush=True)
    if len(set(hits))>=3: gate_ok=True
print('GATE overall:','PASS' if gate_ok else 'FAIL',flush=True)
# PRIMARY
rows=[]
for st,(T,genes) in DP.items():
    mvp=[s for s in T.index if genes[s]=='MVP']
    for s in mvp:
        for p,ld in LOAD.get(st,{}).items():
            a=T.loc[s]; b=ld.reindex(a.index)
            m=np.isfinite(a)&np.isfinite(b)
            if m.sum()<25: continue
            r=spearmanr(a[m],b[m])
            rows.append(dict(cohort=st,site=s,partner=p,rho=r.statistic,p=r.pvalue,n=int(m.sum())))
R=pd.DataFrame(rows)
print(f'\nPRIMARY: dp_MVP vs per-vault partner loading ({len(R)} tests)',flush=True)
if len(R):
    R=R.sort_values('p'); R['q']=(R.p*len(R)/np.arange(1,len(R)+1)).iloc[::-1].cummin().iloc[::-1].clip(upper=1)
    print(R.round(4).to_string(index=False),flush=True)
    print('significant at q<0.05:',int((R.q<.05).sum()),flush=True)
json.dump(dict(gate=bool(gate_ok),cohorts=list(DP),primary=R.to_dict('records') if len(R) else [],
  n_sig=int((R.q<.05).sum()) if len(R) else 0),open('results/phospho_part2.json','w'),indent=1,default=float)
