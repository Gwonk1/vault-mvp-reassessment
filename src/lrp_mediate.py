"""Mediator dissection: what absorbs MVP's drug-resistance signal?"""
import re,json,numpy as np,pandas as pd
from scipy.stats import spearmanr
import statsmodels.api as sm
G=pd.concat([pd.read_excel(f'data/raw/gdsc/{f}_fitted_dose_response_27Oct23.xlsx') for f in ['GDSC1','GDSC2']],ignore_index=True)
G['cl']=G.CELL_LINE_NAME.astype(str).str.upper().str.replace(r'[^A-Z0-9]','',regex=True)
M=pd.read_parquet('data/processed/prot/ccle_broad_2019.parquet')
clin=pd.read_parquet('data/processed/prot/ccle_broad_2019.clin.parquet').set_index('sampleId')
key=lambda c: re.sub(r'[^A-Z0-9]','',c.split('_')[0].upper())
M.columns=[key(c) for c in M.columns]; M=M.loc[:,~M.columns.duplicated()]
shared=sorted(set(M.columns)&set(G.cl)); P=M[shared]
dt=pd.to_numeric(clin.DOUBLING_TIME,errors='coerce'); dt.index=[key(i) for i in clin.index]
dt=dt[~dt.index.duplicated()].reindex(shared)
lin=clin.LINEAGE.astype(str); lin.index=[key(i) for i in clin.index]; lin=lin[~lin.index.duplicated()].reindex(shared)
prolif=P.reindex(['MKI67','TOP2A','MCM2']).apply(lambda r:(r-r.mean())/r.std(),axis=1).mean()
auc=G[G.cl.isin(shared)].pivot_table(index='DRUG_NAME',columns='cl',values='AUC',aggfunc='mean')
Z=lambda s:(s-np.nanmean(s))/np.nanstd(s)
DRUGS=['Vinorelbine','Vinblastine','Paclitaxel','Docetaxel','Methotrexate','Etoposide','Epirubicin']
rows=[]
for d in DRUGS:
    if d not in auc.index: continue
    y=auc.loc[d]
    def fit(cols):
        df=pd.DataFrame({'y':y}).join(pd.DataFrame(cols))
        df=df.dropna()
        if len(df)<40: return None,0
        X=df.drop(columns='y').apply(Z)
        X=X.loc[:,X.std()>0]
        f=sm.OLS(Z(df.y.values),sm.add_constant(X)).fit()
        return f,len(df)
    base={'MVP':P.loc['MVP']}
    f0,n0=fit(base)
    f1,_=fit({**base,'ABCB1':P.loc['ABCB1']})
    f2,_=fit({**base,'dt':dt,'prolif':prolif})
    f3,_=fit({**base,'ABCB1':P.loc['ABCB1'],'dt':dt,'prolif':prolif})
    if f0 is None: continue
    g=lambda f: (float(f.params.get('MVP',np.nan)),float(f.pvalues.get('MVP',np.nan))) if f is not None else (np.nan,np.nan)
    b0,p0=g(f0); b1,p1=g(f1); b2,p2=g(f2); b3,p3=g(f3)
    rows.append(dict(drug=d,n=n0,beta_alone=b0,p_alone=p0,beta_adjABCB1=b1,p_adjABCB1=p1,
                     pct_absorbed_ABCB1=100*(1-b1/b0) if b0 else np.nan,
                     beta_adjProlif=b2,p_adjProlif=p2,pct_absorbed_prolif=100*(1-b2/b0) if b0 else np.nan,
                     beta_adjBoth=b3,p_adjBoth=p3))
R=pd.DataFrame(rows)
print('MVP standardized coefficient on drug AUC, before and after adjustment:\n',flush=True)
print(R[['drug','n','beta_alone','p_alone','beta_adjABCB1','p_adjABCB1','pct_absorbed_ABCB1','beta_adjProlif','p_adjProlif','beta_adjBoth','p_adjBoth']].round(3).to_string(index=False),flush=True)
print(f'\nmedian absorbed by ABCB1: {R.pct_absorbed_ABCB1.median():.0f}% | by doubling time + proliferation: {R.pct_absorbed_prolif.median():.0f}%',flush=True)
print(f'drugs still significant (p<0.05) after ABCB1: {int((R.p_adjABCB1<.05).sum())}/{len(R)} | after both: {int((R.p_adjBoth<.05).sum())}/{len(R)}',flush=True)
mb=spearmanr(P.loc['MVP'],P.loc['ABCB1'],nan_policy='omit')
print(f'\nMVP vs ABCB1 protein across {len(shared)} lines: rho {mb.statistic:+.3f} (p={mb.pvalue:.2g})',flush=True)
json.dump(dict(results=R.to_dict('records'),median_absorbed_abcb1=float(R.pct_absorbed_ABCB1.median()),
  median_absorbed_prolif=float(R.pct_absorbed_prolif.median()),
  mvp_abcb1_rho=float(mb.statistic),mvp_abcb1_p=float(mb.pvalue),
  sig_after_abcb1=int((R.p_adjABCB1<.05).sum()),sig_after_both=int((R.p_adjBoth<.05).sum())),
  open('results/lrp_mediate.json','w'),indent=1,default=float)
