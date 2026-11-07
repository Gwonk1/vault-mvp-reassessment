"""Developmental trend test per DEVELOPMENT_PREREGISTRATION.md."""
import gzip,json,re,sys
import numpy as np, pandas as pd
from scipy.stats import spearmanr
ORDER=['4wpc','5wpc','6wpc','7wpc','8wpc','9wpc','10wpc','11wpc','12wpc','13wpc','16wpc','18wpc','19wpc','20wpc',
       'newborn','infant','toddler','school','youngTeenager','teenager','oldTeenager','youngAdult','youngMidAge','olderMidAge','senior','Senior']
RANK={s:i for i,s in enumerate(ORDER)}
GATE=['LIN28A','LIN28B','IGF2BP1']; PROLIF=['MKI67','TOP2A','CCNB1']; WATCH=['MVP','TEP1','PARP4']+GATE+PROLIF
sym={}
for l in gzip.open('data/raw/cov/gencode.v19.gtf.gz','rt'):
    if l[0]=='#': continue
    f=l.split('\t')
    if f[2]=='gene':
        m=re.search(r'gene_id "(ENSGR?\d+)',f[8]); n=re.search(r'gene_name "([^"]+)"',f[8])
        if m and n: sym[m.group(1)]=n.group(1)
d=pd.read_csv('data/raw/devel/Human.RPKM.txt',sep=' ',index_col=0)
d.index=[sym.get(str(i).split('.')[0]) for i in d.index]
d=d[pd.notna(d.index)]; d=d[~d.index.duplicated()]
print('genes',d.shape[0],'samples',d.shape[1],flush=True)
org=pd.Series([c.split('.')[0] for c in d.columns],index=d.columns)
stg=pd.Series([c.split('.')[1] for c in d.columns],index=d.columns)
bad=sorted(set(stg)-set(RANK)); print('unmapped stages',bad,flush=True)
res={}
for o in sorted(set(org)):
    cols=[c for c in d.columns if org[c]==o and stg[c] in RANK]
    r=np.array([RANK[stg[c]] for c in cols])
    if len(set(r))<4: print('skip',o,len(cols)); continue
    X=d[cols]
    keep=(X>1).mean(axis=1)>=.25
    X=np.log2(X[keep]+1)
    rho=np.array([spearmanr(X.values[i],r).statistic for i in range(X.shape[0])])
    s=pd.Series(rho,index=X.index).dropna()
    pct=s.rank(pct=True)*100
    res[o]={'n':len(cols),'stages':int(len(set(r))),'genes':len(s),
            **{g:(None if g not in s.index else round(float(pct[g]),1)) for g in WATCH}}
    print(o,res[o],flush=True)
need=5
tal=lambda g,lo: sum(1 for o in res if res[o].get(g) is not None and (res[o][g]<=10 if lo else res[o][g]>=90))
gate_ok=sum(1 for g in GATE if tal(g,True)>=need)>=2
mvp_dn,mvp_up=tal('MVP',True),tal('MVP',False)
lab='UNINFORMATIVE' if not gate_ok else ('DEVELOPMENTAL SCAFFOLD' if mvp_dn>=need else ('RISES WITH MATURATION' if mvp_up>=need else 'NO DEVELOPMENTAL TREND'))
print('\nGATE',{g:tal(g,True) for g in GATE},'->','PASS' if gate_ok else 'FAIL',f'(need {need}/7 for 2 of 3)',flush=True)
print('PROLIFERATION',{g:tal(g,True) for g in PROLIF},flush=True)
print('LABEL',lab,'| MVP low in',mvp_dn,'organs, high in',mvp_up,flush=True)
json.dump({'per_organ':res,'gate_pass':gate_ok,'label':lab,'mvp_down':mvp_dn,'mvp_up':mvp_up},open('results/development.json','w'),indent=1,default=float)
