"""Replication of the membrane-repair module in independent tumour cohorts, plus
SPFH specificity in CCLE. Pre-registered in MODULE_REPLICATION_PREREGISTRATION.md."""
import pandas as pd, numpy as np, json, glob, os
from scipy.stats import spearmanr

PRIMARY='GOBP_PLASMA_MEMBRANE_REPAIR'
SECOND=['GOCC_CAVEOLA','GOBP_PLASMA_MEMBRANE_ORGANIZATION','GOCC_LATE_ENDOSOME',
        'GOBP_ENDOSOMAL_TRANSPORT']
PROLIF=['MKI67','TOP2A','MCM2','MCM6','PCNA','MYBL2']
SPFH=['FLOT1','FLOT2','STOM','PHB','PHB2','ERLIN1','ERLIN2']

sets={}
for f in ['data/raw/eggnog/c5.go.bp.v2024.1.Hs.symbols.gmt',
          'data/raw/eggnog/c5.go.cc.v2024.1.Hs.symbols.gmt']:
    for line in open(f):
        p=line.rstrip('\n').split('\t'); sets[p[0]]=set(p[2:])

def analyse(M, label, seeds=('MVP',)):
    M=M[~M.index.duplicated()]
    Z=M.sub(M.mean(axis=1),axis=0).div(M.std(axis=1).replace(0,np.nan),axis=0)
    cyto=[g for g in Z.index if str(g).startswith(('RPL','RPS')) and 'P1' not in str(g)]
    nuc=[g for g in Z.index if str(g).startswith(('HNRNP','SRSF','SF3B','SMC'))]
    if len(cyto)<20 or len(nuc)<10: return {'cohort':label,'status':'no N:C proxy'}
    nc=Z.loc[cyto].mean()-Z.loc[nuc].mean()
    cols=[nc.rename('nc')]+[Z.loc[g].rename(g) for g in PROLIF if g in Z.index]
    C=pd.concat(cols,axis=1).dropna()
    if len(C)<50: return {'cohort':label,'status':f'only {len(C)} usable samples'}
    Zc=Z[C.index]; Zc=Zc.loc[Zc.notna().sum(axis=1)>=max(30,int(0.4*len(C)))]
    X=np.c_[np.ones(len(C)),C.values]
    def rsd(row):
        m=row.notna().values; y=row.values[m]; Xm=X[m]
        b=np.linalg.lstsq(Xm,y,rcond=None)[0]
        o=np.full(len(row),np.nan); o[m]=y-Xm@b; return o
    R=pd.DataFrame(np.vstack([rsd(Zc.loc[g]) for g in Zc.index]),index=Zc.index,columns=C.index)

    def ranked(seed):
        if seed not in R.index: return None
        s=R.loc[seed].values; out={}
        for g in R.index:
            if g==seed: continue
            o=R.loc[g].values; m=np.isfinite(s)&np.isfinite(o)
            if m.sum()<30: continue
            r,_=spearmanr(s[m],o[m])
            if np.isfinite(r): out[g]=r
        return pd.Series(out).sort_values(ascending=False)

    abund=M.mean(axis=1).reindex(R.index)
    dec=pd.qcut(abund.rank(method='first'),10,labels=False,duplicates='drop')
    rng=np.random.default_rng(0)
    def spec(gs,top):
        mem=[g for g in gs if g in R.index]
        if len(mem)<5: return None
        obs=len(set(mem)&top); prof=dec.loc[mem].value_counts(); hits=0
        for _ in range(200):
            pick=[]
            for d,k in prof.items():
                pool=dec.index[dec==d]
                if len(pool)==0: continue
                pick+=list(rng.choice(pool,size=min(k,len(pool)),replace=False))
            if len(set(pick)&top)>=obs: hits+=1
        return {'n':len(mem),'obs':obs,'p':hits/200}

    # gates
    mvp=ranked('MVP')
    if mvp is None: return {'cohort':label,'status':'MVP absent'}
    pr=(list(mvp.index).index('PARP4')+1) if 'PARP4' in mvp.index else None
    g1 = pr is not None and pr<=100
    psma=ranked('PSMA1')
    subs={g for g in R.index if str(g).startswith(('PSMA','PSMB','PSMC','PSMD'))}
    rec=len(set(psma.index[:50])&subs) if psma is not None else 0
    g2=rec>=8
    out={'cohort':label,'n_samples':int(len(C)),'n_proteins':int(R.shape[0]),
         'parp4_rank':pr,'gate_assembly':bool(g1),'proteasome_recovered':rec,
         'gate_complex':bool(g2),'status':'ok' if (g1 and g2) else 'UNINFORMATIVE (gate failed)'}
    res={}
    for seed in seeds:
        rk=ranked(seed)
        if rk is None: res[seed]=None; continue
        top=set(rk.index[:200])
        res[seed]={PRIMARY:spec(sets.get(PRIMARY,set()),top),
                   **{t:spec(sets.get(t,set()),top) for t in SECOND}}
    out['seeds']=res
    return out

# --- PRIMARY: independent CPTAC cohorts ---
coh=sorted(f for f in glob.glob('data/processed/prot/*_cptac_*.parquet') if '.clin.' not in f)
print(f'independent cohorts found: {len(coh)}',flush=True)
reps=[]
for f in coh:
    lbl=os.path.basename(f).replace('.parquet','')
    M=pd.read_parquet(f)
    if M.shape[1]<50 or M.shape[0]<2000:
        print(f'  {lbl}: skipped ({M.shape[0]}x{M.shape[1]})',flush=True); continue
    r=analyse(M,lbl)
    reps.append(r)
    pp=(r.get('seeds',{}).get('MVP') or {}).get(PRIMARY)
    print(f"  {lbl:<22} n={r.get('n_samples')} PARP4 rank {r.get('parp4_rank')} "
          f"prot'some {r.get('proteasome_recovered')}/25 -> {r['status']}"
          f"  {PRIMARY} p={pp['p'] if pp else None}",flush=True)

ok=[r for r in reps if r['status']=='ok']
clear=[r for r in ok if (r['seeds']['MVP'] or {}).get(PRIMARY) and r['seeds']['MVP'][PRIMARY]['p']<0.05]
n_ok,n_cl=len(ok),len(clear)
if n_ok==0: verdict='UNINFORMATIVE (no cohort passed gates)'
elif n_cl> n_ok/2: verdict='REPLICATES'
elif n_cl< n_ok/3: verdict='DOES NOT REPLICATE - #41 struck a third time on independent data'
else: verdict='PARTIAL REPLICATION - #41 unresolved'
print(f'\nreplication: {n_cl} of {n_ok} gate-passing cohorts clear p<0.05')
print('VERDICT:',verdict,flush=True)

# --- SECONDARY: SPFH specificity in CCLE ---
print('\nSPFH specificity in CCLE:',flush=True)
ccle=pd.read_parquet('data/processed/prot/ccle_broad_2019.parquet')
sp=analyse(ccle,'ccle_broad_2019',seeds=('MVP',)+tuple(SPFH))
spfh_clear=[]
for seed,v in (sp.get('seeds') or {}).items():
    pp=(v or {}).get(PRIMARY)
    flag='CLEARS' if pp and pp['p']<0.05 else 'no'
    if seed!='MVP' and pp and pp['p']<0.05: spfh_clear.append(seed)
    print(f'  {seed:<8} {PRIMARY} p={pp["p"] if pp else None}  {flag}',flush=True)
tested=[s for s in SPFH if (sp.get('seeds') or {}).get(s)]
spec_verdict=('MVP-SPECIFIC' if len(spfh_clear)<len(tested)/2 else 'GENERIC SPFH PROPERTY')
print(f'SPFH seeds clearing: {len(spfh_clear)} of {len(tested)} -> {spec_verdict}',flush=True)

json.dump({'replication':{'verdict':verdict,'n_gate_passing':n_ok,'n_clearing':n_cl,
                          'cohorts':reps},
           'spfh_specificity':{'verdict':spec_verdict,'seeds_clearing':spfh_clear,
                               'n_tested':len(tested),'detail':sp.get('seeds')}},
          open('results/module_replication.json','w'),indent=1,default=str)
