"""Cross-test per CROSSTEST_PREREGISTRATION.md: co-abundance module vs physical vault IP-MS."""
import openpyxl,json,numpy as np,pandas as pd
from scipy.stats import hypergeom,spearmanr
wb=openpyxl.load_workbook('argon/raw/lodwick_supp_4.xlsx',read_only=True,data_only=True)
rows=list(wb['Fig. 5c-d'].iter_rows(values_only=True))
D=pd.DataFrame(rows[1:],columns=list(rows[0])).dropna(subset=['GeneName'])
for c in D.columns[1:]: D[c]=pd.to_numeric(D[c],errors='coerce')
D=D.drop_duplicates('GeneName').set_index('GeneName')
po=pd.read_parquet('data/processed/mvp_coabundance.parquet')
po=po[po.index!='MVP']
uni=[g for g in po.index if g in D.index]
print('my ranking',len(po),'| IP universe',len(D),'| shared',len(uni),flush=True)
S=D.loc[uni]
wt=set(S.index[(S.WT_LFC>0)&(S.LWTP>1.3)])
dep=set(S.index[(S.WT_LFC>0)&(S.LWTP>1.3)&(S.WTKD_LFC>0)&(S.WTKD_P>1.3)])
print(f'WT vault interactors in shared universe: {len(wt)} ({100*len(wt)/len(uni):.1f}%) | PARP4-dependent: {len(dep)}',flush=True)
top=[g for g in po.index if g in set(uni)][:100]
k=len(set(top)&wt)
p=hypergeom.sf(k-1,len(uni),len(wt),len(top))
print(f'\nPRIMARY: {k}/100 of my top co-abundant proteins are WT vault interactors (expected {len(top)*len(wt)/len(uni):.1f}) | hypergeom p = {p:.3g}',flush=True)
lab='PHYSICALLY CORROBORATED' if (p<.05 and k>=5) else 'NOT CORROBORATED'
print('VERDICT:',lab,flush=True)
rho=spearmanr(po.loc[uni].z.values,S.WT_LFC.values,nan_policy='omit')
print(f'\nSecondary 1: Spearman(my co-abundance z, WT_LFC) = {rho.statistic:+.3f} (p={rho.pvalue:.2g}, n={len(uni)})',flush=True)
kd=len(set(top)&dep)
base=len(dep)/max(len(wt),1)
obs=kd/max(k,1)
print(f'Secondary 2: PARP4-dependent among my top-100 interactors: {kd}/{k} = {100*obs:.1f}% vs {100*base:.1f}% of all WT interactors',flush=True)
print('\nSecondary 3: named membrane-repair genes',flush=True)
named=['ANXA2','S100A10','EHD2','EHD4','CAPN2','CAPNS1','IQGAP1','PARP4','TEP1']
r={g:(int(list(po.index).index(g))+1 if g in po.index else None) for g in named}
out=[]
for g in named:
    if g in D.index:
        d=D.loc[g]
        out.append(dict(gene=g,my_rank=r[g],WT_LFC=d.WT_LFC,negLog10P=d.LWTP,
                        interactor=bool(d.WT_LFC>0 and d.LWTP>1.3),
                        PARP4_dep=bool(d.WT_LFC>0 and d.LWTP>1.3 and d.WTKD_LFC>0 and d.WTKD_P>1.3)))
    else: out.append(dict(gene=g,my_rank=r[g],WT_LFC=None,negLog10P=None,interactor=None,PARP4_dep=None))
T=pd.DataFrame(out); print(T.to_string(index=False),flush=True)
print('\nTop 25 of mine that ARE vault interactors:',[g for g in top if g in wt][:25],flush=True)
json.dump(dict(shared=len(uni),wt_interactors=len(wt),parp4_dependent=len(dep),top100_overlap=k,
  expected=float(len(top)*len(wt)/len(uni)),hypergeom_p=float(p),verdict=lab,
  spearman=float(rho.statistic),spearman_p=float(rho.pvalue),
  parp4_dep_in_top=kd,parp4_dep_rate_top=float(obs),parp4_dep_rate_all=float(base),
  named=T.to_dict('records')),open('results/crosstest.json','w'),indent=1,default=float)
