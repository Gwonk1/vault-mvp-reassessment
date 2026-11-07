"""DepMap co-essentiality per COESSENTIALITY_PREREGISTRATION.md."""
import json,re,sys
import numpy as np, pandas as pd
D=pd.read_csv('data/raw/depmap/CRISPRGeneEffect.csv',index_col=0)
D.columns=[re.sub(r'\s*\(\d+\)$','',c) for c in D.columns]
D=D.loc[:,~D.columns.duplicated()]
print('cell lines',D.shape[0],'genes',D.shape[1],flush=True)
ok=(D.notna().sum(axis=0)>=300)&(D.std(axis=0)>0)
D=D.loc[:,ok]; print('after filter:',D.shape,flush=True)
X=D.values
mu=np.nanmean(X,axis=0); sd=np.nanstd(X,axis=0)
Z=(X-mu)/sd
M=np.isfinite(Z); Zz=np.where(M,Z,0)
genes=list(D.columns); gi={g:i for i,g in enumerate(genes)}
def corr(g):
    j=gi[g]; x=Zz[:,j]; mx=M[:,j]
    m=M&mx[:,None]; n=m.sum(0)
    sxy=(Zz*np.where(m,x[:,None],0)).sum(0)
    sx=(np.where(m,x[:,None],0)).sum(0); sy=(np.where(m,Zz,0)).sum(0)
    sx2=(np.where(m,x[:,None],0)**2).sum(0); sy2=(np.where(m,Zz,0)**2).sum(0)
    den=np.sqrt(np.maximum((n*sx2-sx**2)*(n*sy2-sy**2),1e-12))
    r=np.where(n>=300,(n*sxy-sx*sy)/den,np.nan)
    return pd.Series(r,index=genes).drop(g),n
from scipy import stats
def ranked(g):
    r,n=corr(g); nn=pd.Series(n,index=genes).drop(g)
    t=r*np.sqrt((nn-2)/np.maximum(1-r**2,1e-12))
    p=pd.Series(2*stats.t.sf(np.abs(t),nn-2),index=r.index)
    o=p.sort_values(); q=(o*len(o)/np.arange(1,len(o)+1))[::-1].cummin()[::-1].clip(upper=1)
    return pd.DataFrame({'r':r,'p':p,'q':q.reindex(r.index)}).sort_values('r',ascending=False)
res={}
for g,pat,need in [('NDUFS2',r'^NDUF',5),('CAV1',None,None)]:
    if g not in gi: print('GATE',g,'absent'); res[g]=False; continue
    t=ranked(g); top=list(t.index[:25])
    if pat: hit=sum(1 for x in top if re.match(pat,x)); ok2=hit>=need; print(f'GATE {g}: {hit}/25 {pat} -> ','PASS' if ok2 else 'FAIL','|',top[:8],flush=True)
    else:
        hit=[x for x in top if x in ('CAVIN1','EHD2')]; ok2=len(hit)==2
        print(f'GATE CAV1: recovered {hit} in top25 ->','PASS' if ok2 else 'FAIL','|',top[:10],flush=True)
    res[g]=bool(ok2)
gate2=res.get('CAV1',False)
out=dict(gates=res,n_lines=int(D.shape[0]),n_genes=int(D.shape[1]))
if 'MVP' not in gi:
    print('MVP absent from DepMap'); json.dump(out,open('results/coessentiality.json','w'),indent=1)
    raise SystemExit
t=ranked('MVP')
sig=t[t.q<.05]
lab=('HAS CO-ESSENTIAL PARTNERS' if len(sig) else 'NO CO-ESSENTIAL PARTNERS') if gate2 else 'UNINFORMATIVE'
print(f'\nMVP: genes tested {len(t)} | q<0.05: {len(sig)} | top r {t.r.iloc[0]:.3f} (q={t.q.iloc[0]:.3g})',flush=True)
print('VERDICT:',lab,flush=True)
print('\ntop 25 co-essential with MVP:',flush=True)
print(t.head(25).round(4).to_string(),flush=True)
core={g:(int(list(t.index).index(g))+1,round(float(t.r[g]),3),float(t.q[g])) for g in ['PARP4','TEP1','ANXA2','S100A10','CAV1','CAVIN1','EHD2'] if g in t.index}
print('\ncore / control ranks (rank, r, q):',core,flush=True)
t.head(300).to_csv('results/coessentiality_mvp_top300.csv')
out.update(verdict=lab,n_sig=int(len(sig)),top25=[(g,float(t.r[g]),float(t.q[g])) for g in t.index[:25]],core=core)
json.dump(out,open('results/coessentiality.json','w'),indent=1,default=float)
