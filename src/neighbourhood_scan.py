"""Unbiased, replication-gated scan of MVP's co-abundance neighbourhood.
Pre-registered in NEIGHBOURHOOD_SCAN_PREREGISTRATION.md. No term chosen by hand."""
import pandas as pd, numpy as np, json
from scipy.stats import spearmanr, hypergeom

PROLIF=['MKI67','TOP2A','MCM2','MCM6','PCNA','MYBL2']
DATASETS=['brain_cptac_2020','coad_cptac_2019','gbm_cptac_2021','ucec_cptac_2020','ccle_broad_2019']
FAVOURED=['GOBP_PLASMA_MEMBRANE_REPAIR','GOCC_CAVEOLA','GOBP_PLASMA_MEMBRANE_ORGANIZATION',
          'GOCC_LATE_ENDOSOME','GOBP_ENDOSOMAL_TRANSPORT']

sets={}
for f in ['data/raw/eggnog/c5.go.bp.v2024.1.Hs.symbols.gmt',
          'data/raw/eggnog/c5.go.cc.v2024.1.Hs.symbols.gmt']:
    for line in open(f):
        p=line.rstrip('\n').split('\t'); sets[p[0]]=set(p[2:])
print(f'GO terms loaded: {len(sets)}',flush=True)

def bh(ps):
    ps=np.asarray(ps); o=np.argsort(ps); n=len(ps)
    q=np.empty(n); prev=1.0
    for i in range(n-1,-1,-1):
        prev=min(prev, ps[o[i]]*n/(i+1)); q[o[i]]=prev
    return q

def prep(name):
    M=pd.read_parquet(f'data/processed/prot/{name}.parquet'); M=M[~M.index.duplicated()]
    Z=M.sub(M.mean(axis=1),axis=0).div(M.std(axis=1).replace(0,np.nan),axis=0)
    cyto=[g for g in Z.index if str(g).startswith(('RPL','RPS')) and 'P1' not in str(g)]
    nuc=[g for g in Z.index if str(g).startswith(('HNRNP','SRSF','SF3B','SMC'))]
    nc=Z.loc[cyto].mean()-Z.loc[nuc].mean()
    C=pd.concat([nc.rename('nc')]+[Z.loc[g].rename(g) for g in PROLIF if g in Z.index],axis=1).dropna()
    Zc=Z[C.index]; Zc=Zc.loc[Zc.notna().sum(axis=1)>=max(30,int(0.4*len(C)))]
    X=np.c_[np.ones(len(C)),C.values]
    def rsd(row):
        m=row.notna().values; y=row.values[m]; Xm=X[m]
        b=np.linalg.lstsq(Xm,y,rcond=None)[0]
        o=np.full(len(row),np.nan); o[m]=y-Xm@b; return o
    R=pd.DataFrame(np.vstack([rsd(Zc.loc[g]) for g in Zc.index]),index=Zc.index,columns=C.index)
    return R,len(C)

def ranked(R,seed):
    if seed not in R.index: return None
    s=R.loc[seed].values; out={}
    for g in R.index:
        if g==seed: continue
        o=R.loc[g].values; m=np.isfinite(s)&np.isfinite(o)
        if m.sum()<30: continue
        r,_=spearmanr(s[m],o[m])
        if np.isfinite(r): out[g]=r
    return pd.Series(out).sort_values(ascending=False)

def scan(R,seed):
    rk=ranked(R,seed)
    if rk is None: return None
    universe=set(rk.index); N=len(universe); top=set(rk.index[:200]); K=200
    names,ps=[],[]
    for t,gs in sets.items():
        mem=gs&universe; n=len(mem)
        if n<10 or n>500: continue
        k=len(mem&top)
        if k==0: continue
        names.append(t); ps.append(hypergeom.sf(k-1,N,n,K))
    q=bh(ps)
    return pd.Series(q,index=names).sort_values()

prepped={}
for d in DATASETS:
    try: R,n=prep(d)
    except Exception as e: print(f'  {d}: skipped ({e})',flush=True); continue
    pr=ranked(R,'PARP4') is not None
    mvp=ranked(R,'MVP')
    if mvp is None: print(f'  {d}: MVP absent',flush=True); continue
    prank=(list(mvp.index).index('PARP4')+1) if 'PARP4' in mvp.index else None
    psma=ranked(R,'PSMA1')
    subs={g for g in R.index if str(g).startswith(('PSMA','PSMB','PSMC','PSMD'))}
    rec=len(set(psma.index[:50])&subs) if psma is not None else 0
    ok=(prank is not None and prank<=100) and rec>=8
    print(f'  {d:<20} n={n:<4} proteins={R.shape[0]:<5} PARP4 rank {prank} prot\'some {rec}/25 -> {"INCLUDED" if ok else "EXCLUDED"}',flush=True)
    if ok: prepped[d]=R

inc=list(prepped)
print(f'\nincluded datasets: {len(inc)}',flush=True)

# design gate: can this scan recover the proteasome from PSMA1?
psma_rep={}
for d in inc:
    q=scan(prepped[d],'PSMA1')
    if q is None: continue
    hits={t for t in q.index[q<0.05] if 'PROTEASOME' in t}
    for t in hits: psma_rep[t]=psma_rep.get(t,0)+1
maj=len(inc)//2+1
design_ok=any(v>=maj for v in psma_rep.values())
print(f'DESIGN GATE: proteasome terms replicating in >={maj} datasets: '
      f'{sum(1 for v in psma_rep.values() if v>=maj)} -> {"PASS" if design_ok else "FAIL"}',flush=True)

# MVP scan
rep={}
for d in inc:
    q=scan(prepped[d],'MVP')
    sig=list(q.index[q<0.05])
    print(f'  {d}: {len(sig)} terms at q<0.05',flush=True)
    for t in sig: rep[t]=rep.get(t,0)+1

tab=pd.Series(rep).sort_values(ascending=False) if rep else pd.Series(dtype=int)
replicating=[t for t,v in tab.items() if v>=maj]
half=[t for t,v in tab.items() if v==len(inc)/2]
if not design_ok: verdict='UNINFORMATIVE (scan design gate failed)'
elif replicating:  verdict=f'REPLICATING NEIGHBOURHOOD: {len(replicating)} term(s)'
elif not rep:      verdict='NO NEIGHBOURHOOD - zero terms significant anywhere'
else:              verdict='NO REPLICATING NEIGHBOURHOOD - all terms dataset-specific'
print(f'\nmajority threshold: {maj} of {len(inc)}')
print('VERDICT:',verdict,flush=True)
if len(tab): 
    print('\ntop terms by replication count:')
    print(tab.head(25).to_string(),flush=True)
print('\npreviously favoured terms:')
for t in FAVOURED: print(f'  {t:<40} replicates in {rep.get(t,0)} of {len(inc)}',flush=True)

json.dump({'verdict':verdict,'included':inc,'majority':maj,'design_gate':design_ok,
           'proteasome_control':psma_rep,
           'replicating':replicating,'exactly_half':half,
           'replication_counts':{k:int(v) for k,v in tab.items()},
           'favoured':{t:rep.get(t,0) for t in FAVOURED}},
          open('results/neighbourhood_scan.json','w'),indent=1)
