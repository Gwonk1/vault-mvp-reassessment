"""LRP chemoresistance dissection per LRP_PREREGISTRATION.md."""
import json,re,sys,numpy as np,pandas as pd
from scipy.stats import spearmanr
CYTO={'anthracycline':['Doxorubicin','Epirubicin','Daunorubicin','Mitoxantrone'],
 'platinum':['Cisplatin','Carboplatin','Oxaliplatin'],
 'antimetabolite':['Gemcitabine','5-Fluorouracil','Cytarabine','Methotrexate'],
 'topoisomerase':['Etoposide','Irinotecan','Topotecan','Camptothecin','SN-38'],
 'tubulin':['Paclitaxel','Docetaxel','Vinblastine','Vincristine','Vinorelbine','Docetaxel']}
ALLCYTO=[d for v in CYTO.values() for d in v]
VTRNA=['Doxorubicin','Epirubicin','Daunorubicin','Mitoxantrone']
G=[]
for f in ['GDSC1','GDSC2']:
    d=pd.read_excel(f'data/raw/gdsc/{f}_fitted_dose_response_27Oct23.xlsx')
    d['src']=f; G.append(d)
G=pd.concat(G,ignore_index=True)
print('GDSC rows',len(G),'| cols',[c for c in G.columns][:12],flush=True)
G['cl']=G.CELL_LINE_NAME.astype(str).str.upper().str.replace(r'[^A-Z0-9]','',regex=True)
M=pd.read_parquet('data/processed/prot/ccle_broad_2019.parquet')
clin=pd.read_parquet('data/processed/prot/ccle_broad_2019.clin.parquet').set_index('sampleId')
M.columns=[re.sub(r'[^A-Z0-9]','',c.split('_')[0].upper()) for c in M.columns]
M=M.loc[:,~M.columns.duplicated()]
shared=sorted(set(M.columns)&set(G.cl))
print('CCLE protein lines',M.shape[1],'| GDSC lines',G.cl.nunique(),'| matched',len(shared),flush=True)
P=M[shared]
dt=pd.to_numeric(clin.DOUBLING_TIME,errors='coerce')
dt.index=[re.sub(r'[^A-Z0-9]','',i.split('_')[0].upper()) for i in dt.index]
dt=dt[~dt.index.duplicated()].reindex(shared)
prolif=P.reindex(['MKI67','TOP2A','MCM2']).apply(lambda r:(r-r.mean())/r.std(),axis=1).mean()
auc=G[G.cl.isin(shared)].pivot_table(index='DRUG_NAME',columns='cl',values='AUC',aggfunc='mean')
print('drugs x lines:',auc.shape,'| doubling time available for',int(dt.notna().sum()),flush=True)
def corr_drug(vec,drug,extra=None):
    if drug not in auc.index: return None
    y=auc.loc[drug]; x=vec.reindex(y.index)
    m=np.isfinite(x)&np.isfinite(y)
    if m.sum()<40: return None
    return spearmanr(x[m],y[m])
def gate(prot,drugs,thr):
    out=[]
    for d in drugs:
        r=corr_drug(P.loc[prot] if prot in P.index else pd.Series(dtype=float),d)
        if r: out.append((d,round(r.statistic,3),r.pvalue))
    ok=any(p<thr and s>0 for _,s,p in out)
    return ok,out
g1,o1=gate('ABCB1',['Paclitaxel','Docetaxel','Vinblastine','Vincristine','Vinorelbine'],1e-3)
print('\nGATE1 ABCB1 -> tubulin resistance:','PASS' if g1 else 'FAIL',o1,flush=True)
g2,o2=gate('ABCC1',['Etoposide','Doxorubicin'],1e-2)
print('GATE2 ABCC1 -> etoposide/doxorubicin:','PASS' if g2 else 'FAIL',o2,flush=True)
if not (g1 or g2):
    json.dump(dict(gate1=g1,gate2=g2,o1=o1,o2=o2,verdict='GATES FAILED'),open('results/lrp.json','w'),indent=1,default=float)
    print('\nBoth gates failed - matching is broken, nothing reported about MVP.'); raise SystemExit
rows=[]
mvp=P.loc['MVP']
for cls,drugs in CYTO.items():
    for d in drugs:
        r=corr_drug(mvp,d)
        if r: rows.append(dict(drug=d,cls=cls,rho=r.statistic,p=r.pvalue,n=int(np.isfinite(auc.loc[d]).sum()),vtrna=d in VTRNA))
R=pd.DataFrame(rows).sort_values('p')
if len(R):
    R['q']=(R.p*len(R)/np.arange(1,len(R)+1)).iloc[::-1].cummin().iloc[::-1].clip(upper=1)
print(f'\nMVP protein vs cytotoxic drug AUC ({len(R)} drugs tested, positive rho = resistance):',flush=True)
print(R.round(4).to_string(index=False),flush=True)
sig=R[R.q<.05]
lab='BIOMARKER IS CELL-INTRINSIC' if len(sig) else 'NOT CELL-INTRINSIC'
print(f'\nq<0.05: {len(sig)} of {len(R)} -> VERDICT: {lab}',flush=True)
print(f'median rho across cytotoxics: {R.rho.median():+.3f} | vtRNA-binders {R[R.vtrna].rho.median():+.3f} vs others {R[~R.vtrna].rho.median():+.3f}',flush=True)
json.dump(dict(gate1=g1,gate2=g2,gate1_detail=o1,gate2_detail=o2,matched_lines=len(shared),
  verdict=lab,n_sig=int(len(sig)),results=R.to_dict('records'),
  median_rho=float(R.rho.median())),open('results/lrp.json','w'),indent=1,default=float)
