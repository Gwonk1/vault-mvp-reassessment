"""Named checks on the primary: ssGSEA scoring, TMB covariate, and ratio vs unit consistency."""
import sys,json,numpy as np,pandas as pd
sys.path.insert(0,'src')
from models import *
def ssgsea(m,genes,alpha=.25):
    idx=[m.index.get_loc(g) for g in resolve(genes,m.index)]
    out=[]
    R=m.rank(axis=0).values
    for j in range(m.shape[1]):
        o=np.argsort(-R[:,j]); rk=R[o,j]**alpha; hit=np.isin(o,idx)
        p=np.cumsum(rk*hit)/ (rk*hit).sum(); q=np.cumsum(~hit)/(~hit).sum()
        out.append((p-q).sum())
    return np.array(out)
rows={};tmb={}
z_std=lambda x:(x-np.nanmean(x))/np.nanstd(x,ddof=1)
for n in ICB:
    D,mt,(z,clin,cols)=cohort(n)
    m,_,_=load(n); m=m.loc[z.index,z.columns]; m1=m.drop(index=[g for g in TARGET_ALIASES if g in m.index])
    a,c=z_std(ssgsea(m1,SETS['ISG_RS'])),z_std(ssgsea(m1,SETS['IFNG_GS']))
    agree=(float(np.corrcoef(a,cols['a'])[0,1]),float(np.corrcoef(c,cols['c'])[0,1]))
    y=z.loc['MVP'].values
    X=np.column_stack([np.ones(len(y)),a,c,cols['purity'],cols['myeloid'],cols['lymphoid']])
    Xi=np.linalg.inv(X.T@X); b=Xi@X.T@y; s2=((y-X@b)**2).sum()/(len(y)-X.shape[1])
    rows[n]=(b[1],b[2],s2*Xi[1,1],s2*Xi[2,2],s2*(Xi[1,1]+Xi[2,2]-2*Xi[1,2]))+agree
    if clin is not None and 'TMB_NONSYNONYMOUS' in clin:
        t=pd.to_numeric(clin.TMB_NONSYNONYMOUS.reindex(z.columns),errors='coerce').values
        ok=np.isfinite(t)
        if ok.sum()>=15:
            Xt=np.column_stack([X[ok][:, :1],cols['a'][ok],cols['c'][ok],cols['purity'][ok],cols['myeloid'][ok],cols['lymphoid'][ok],z_std(np.log1p(t[ok]))])
            Xi=np.linalg.inv(Xt.T@Xt);b=Xi@Xt.T@y[ok];s2=((y[ok]-Xt@b)**2).sum()/(ok.sum()-Xt.shape[1])
            tmb[n]=(b[1],b[2],s2*Xi[1,1],s2*Xi[2,2],s2*(Xi[1,1]+Xi[2,2]-2*Xi[1,2]),int(ok.sum()))
def summ(d):
    A=np.array([v[:5] for v in d.values()])
    t=dict(ba=reml(A[:,0],A[:,2]),bc=reml(A[:,1],A[:,3]),d=reml(A[:,0]-A[:,1],A[:,4]))
    return label(t['ba'][:3],t['bc'][:3],t['d'][:3]),fmt(t)
print('ssGSEA',summ(rows)); print({k:(round(v[5],2),round(v[6],2)) for k,v in rows.items()})
print('TMB',summ(tmb),{k:v[5] for k,v in tmb.items()})
json.dump(dict(ssgsea=summ(rows),tmb=summ(tmb),score_agreement={k:v[5:7] for k,v in rows.items()},tmb_n={k:v[5] for k,v in tmb.items()}),open('results/bulk_robust.json','w'),indent=1,default=float)
