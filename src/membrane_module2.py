"""Re-run of MEMBRANE_MODULE_PREREGISTRATION.md with pairwise-complete handling.
Run 1 (src/membrane_module.py) failed gate 1 because a no-NaN mask dropped TEP1,
measured in only 277 of 375 lines. That was an implementation defect, not a rule
change: the registered gate and thresholds are unchanged here."""
import pandas as pd, numpy as np, json
from scipy.stats import spearmanr

PRIMARY='GOBP_PLASMA_MEMBRANE_REPAIR'
SECONDARY=['GOCC_LYSOSOME','GOCC_LATE_ENDOSOME','GOBP_ENDOSOMAL_TRANSPORT',
           'GOCC_CAVEOLA','GOCC_MEMBRANE_RAFT','GOBP_PLASMA_MEMBRANE_ORGANIZATION']
PROLIF=['MKI67','TOP2A','MCM2','MCM6','PCNA','MYBL2']

sets={}
for f in ['data/raw/eggnog/c5.go.bp.v2024.1.Hs.symbols.gmt',
          'data/raw/eggnog/c5.go.cc.v2024.1.Hs.symbols.gmt']:
    for line in open(f):
        p=line.rstrip('\n').split('\t'); sets[p[0]]=set(p[2:])

M=pd.read_parquet('data/processed/prot/ccle_broad_2019.parquet'); M=M[~M.index.duplicated()]
Z=M.sub(M.mean(axis=1),axis=0).div(M.std(axis=1).replace(0,np.nan),axis=0)
cyto=[g for g in Z.index if str(g).startswith(('RPL','RPS')) and 'P1' not in str(g)]
nuc=[g for g in Z.index if str(g).startswith(('HNRNP','SRSF','SF3B','SMC'))]
nc=Z.loc[cyto].mean()-Z.loc[nuc].mean()
C=pd.concat([nc.rename('nc')]+[Z.loc[g].rename(g) for g in PROLIF if g in Z.index],axis=1).dropna()
print(f'proteins {Z.shape[0]}  lines with covariates {len(C)}',flush=True)

# keep proteins measured in >=150 covariate-complete lines
Zc=Z[C.index]
n_ok=Zc.notna().sum(axis=1)
Zc=Zc.loc[n_ok>=150]
print(f'proteins retained (>=150 lines): {Zc.shape[0]}  [run 1 retained 5063]',flush=True)

Xfull=np.c_[np.ones(len(C)),C.values]
def resid(row):
    m=row.notna().values
    y=row.values[m]; X=Xfull[m]
    b=np.linalg.lstsq(X,y,rcond=None)[0]
    out=np.full(len(row),np.nan); out[m]=y-X@b
    return out
R=pd.DataFrame(np.vstack([resid(Zc.loc[g]) for g in Zc.index]),index=Zc.index,columns=C.index)
print(f'residualised (pairwise): {R.shape}  TEP1 present: {"TEP1" in R.index}',flush=True)

def ranked(seed):
    s=R.loc[seed].values; out={}
    for g in R.index:
        if g==seed: continue
        o=R.loc[g].values; m=np.isfinite(s)&np.isfinite(o)
        if m.sum()<100: continue
        r,_=spearmanr(s[m],o[m])
        if np.isfinite(r): out[g]=r
    return pd.Series(out).sort_values(ascending=False)

mvp=ranked('MVP'); top200=set(mvp.index[:200])
g1={g:(list(mvp.index).index(g)+1 if g in mvp.index else None) for g in ['PARP4','TEP1']}
gate1=all(v is not None and v<=50 for v in g1.values())
psma=ranked('PSMA1')
subs={g for g in R.index if str(g).startswith(('PSMA','PSMB','PSMC','PSMD'))}
rec=len(set(psma.index[:50])&subs); gate2=rec>=10
print(f'\nGATE1 PARP4/TEP1 ranks {g1} -> {"PASS" if gate1 else "FAIL"}',flush=True)
print(f'GATE2 PSMA1 recovers {rec}/25 proteasome -> {"PASS" if gate2 else "FAIL"}',flush=True)

abund=M.mean(axis=1).reindex(R.index)
dec=pd.qcut(abund.rank(method='first'),10,labels=False)
rng=np.random.default_rng(0)
def spec(gs,n=200):
    mem=[g for g in gs if g in R.index]
    if len(mem)<5: return None
    obs=len(set(mem)&top200); prof=dec.loc[mem].value_counts(); hits=0
    for _ in range(n):
        pick=[]
        for d,k in prof.items():
            pool=dec.index[dec==d]; pick+=list(rng.choice(pool,size=min(k,len(pool)),replace=False))
        if len(set(pick)&top200)>=obs: hits+=1
    return {'n_members':len(mem),'observed_in_top200':obs,'specificity_p':hits/n}

prim=spec(sets.get(PRIMARY,set())); sec={t:spec(sets.get(t,set())) for t in SECONDARY}
print(f'\nPRIMARY {PRIMARY}: {prim}',flush=True)
for t,v in sec.items(): print(f'  {t}: {v}',flush=True)
if not(gate1 and gate2): verdict='UNINFORMATIVE (gate failed)'
elif prim and prim['specificity_p']<0.05: verdict='MODULE SURVIVES the confound'
else: verdict='MODULE DOES NOT SURVIVE - #41 stays struck, strengthened'
print('\nVERDICT:',verdict,flush=True)
print('\nMVP top 30 residualised correlates:'); print(mvp.head(30).round(3).to_string(),flush=True)
json.dump({'run':'pairwise-complete (run 2)','gate1_assembly':gate1,'gate1_ranks':g1,
           'gate2_proteasome':gate2,'gate2_recovered':rec,'verdict':verdict,
           'primary':{PRIMARY:prim},'secondary':sec,'n_proteins':int(R.shape[0]),
           'mvp_top30':{k:round(float(v),4) for k,v in mvp.head(30).items()}},
          open('results/membrane_module2.json','w'),indent=1)
