"""Proliferation-state test per PROLIFERATION_PREREGISTRATION.md."""
import json,sys,numpy as np,pandas as pd
from scipy.stats import spearmanr
sys.path.insert(0,'src')
from models import load,zgenes,score,COV,TCGA,EXCL,COVGENES
from scores import load_sets,assert_no_target,TARGET_ALIASES
import json as _j
H={l.split('\t')[0]:l.strip().split('\t')[2:] for l in open('data/raw/genesets/h.all.gmt')}
PROL=sorted(set(H['HALLMARK_E2F_TARGETS'])|set(H['HALLMARK_G2M_CHECKPOINT']))
PROL=[g for g in PROL if g not in TARGET_ALIASES]
assert_no_target(PROL,'proliferation score')
print('proliferation set',len(PROL),'genes; MVP in raw set:',
      'MVP' in set(H['HALLMARK_E2F_TARGETS'])|set(H['HALLMARK_G2M_CHECKPOINT']),flush=True)
GATE=['MKI67','TOP2A','CCNB1']; WATCH=['MVP','TEP1','PARP4']+GATE
res={}
for n in TCGA:
    try: m,clin,note=load(n)
    except Exception as e: print('skip',n,repr(e)[:60]); continue
    floor=np.nanmin(m.values); expressed=(m>floor+1e-9).mean(axis=1)>=.5
    mm=m[expressed&(m.std(axis=1)>0)]
    z=zgenes(mm).dropna()
    z1=z.loc[[g for g in z.index if g not in TARGET_ALIASES]]
    p,kept=score(z1,PROL,'prolif')
    Z=lambda s:((s-s.mean())/s.std(ddof=1)).values
    cols={'p':Z(p)}
    for k,gs in COV.items(): cols[k]=Z(score(z1,gs,k)[0])
    X=np.column_stack([np.ones(z.shape[1])]+list(cols.values()))
    Xi=np.linalg.pinv(X); B=z.values@Xi.T
    adj=pd.Series(B[:,1],index=z.index)
    un=pd.Series([spearmanr(z.values[i],cols['p']).statistic for i in range(len(z))],index=z.index)
    keep=[g for g in z.index if g not in EXCL|COVGENES|set(PROL)]
    pa=adj.rank(pct=True)*100; pu=un.rank(pct=True)*100
    res[n]={'n':z.shape[1],'genes':len(z),'kept_prolif':len(kept),
            **{g:{'adj':None if g not in pa else round(float(pa[g]),1),
                  'unadj':None if g not in pu else round(float(pu[g]),1)} for g in WATCH}}
    print(n,res[n],flush=True)
need=4
tal=lambda g,k,lo: sum(1 for c in res if res[c][g][k] is not None and (res[c][g][k]<=10 if lo else res[c][g][k]>=90))
gate=sum(1 for g in GATE if tal(g,'adj',False)>=need)>=2
dn,up=tal('MVP','adj',True),tal('MVP','adj',False)
lab='UNINFORMATIVE' if not gate else ('NON-DIVIDING MARKER' if dn>=need else ('PROLIFERATION-ASSOCIATED' if up>=need else 'NO RELATION'))
print('\nGATE',{g:tal(g,'adj',False) for g in GATE},'->','PASS' if gate else 'FAIL',f'(need {need}/6 for 2 of 3)',flush=True)
print('LABEL',lab,'| MVP low in',dn,'cohorts, high in',up,'| unadjusted low',tal('MVP','unadj',True),'high',tal('MVP','unadj',False),flush=True)
json.dump({'per_cohort':res,'gate_pass':gate,'label':lab,'mvp_low':dn,'mvp_high':up},open('results/proliferation.json','w'),indent=1,default=float)
