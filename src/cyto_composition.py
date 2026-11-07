"""Is the cortical-actin neighbourhood just protein abundance?
Pre-registered in CYTO_COMPOSITION_PREREGISTRATION.md. Abundance-matched randoms."""
import pandas as pd, numpy as np, json, warnings; warnings.filterwarnings('ignore')
from scipy.stats import spearmanr

IFN=['STAT1','IRF9']; PROLIF=['MKI67','TOP2A','MCM2','MCM6','PCNA','MYBL2']
DECIDE=['coad_cptac_2019','ucec_cptac_2020','ccle_broad_2019']
CNS=['brain_cptac_2020','gbm_cptac_2021']
UNDER=['GOCC_RUFFLE','GOBP_ACTIN_FILAMENT_ORGANIZATION','GOBP_INFLAMMATORY_RESPONSE']
NEG=['GOBP_ANTIGEN_PROCESSING_AND_PRESENTATION','GOBP_RESPONSE_TO_TYPE_II_INTERFERON']
REF=['GOCC_MITOCHONDRION','GOCC_GOLGI_APPARATUS','GOCC_ENDOSOME']

sets={}
for f in ['data/raw/eggnog/c5.go.bp.v2024.1.Hs.symbols.gmt',
          'data/raw/eggnog/c5.go.cc.v2024.1.Hs.symbols.gmt']:
    for line in open(f):
        p=line.rstrip('\n').split('\t'); sets[p[0]]=set(p[2:])

def analyse(name):
    M=pd.read_parquet(f'data/processed/prot/{name}.parquet'); M=M[~M.index.duplicated()]
    Z=M.sub(M.mean(axis=1),axis=0).div(M.std(axis=1).replace(0,np.nan),axis=0)
    cyto=[g for g in Z.index if str(g).startswith(('RPL','RPS')) and 'P1' not in str(g)]
    nuc=[g for g in Z.index if str(g).startswith(('HNRNP','SRSF','SF3B','SMC'))]
    nc=Z.loc[cyto].mean()-Z.loc[nuc].mean()
    C=pd.concat([nc.rename('nc')]+[Z.loc[g].rename(g) for g in PROLIF+IFN if g in Z.index],axis=1).dropna()
    Zc=Z[C.index]; Zc=Zc.loc[Zc.notna().sum(axis=1)>=max(30,int(0.4*len(C)))]
    X=np.c_[np.ones(len(C)),C.values]
    def rsd(r):
        m=r.notna().values; y=r.values[m]; Xm=X[m]
        b=np.linalg.lstsq(Xm,y,rcond=None)[0]; o=np.full(len(r),np.nan); o[m]=y-Xm@b; return o
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
    def spec(gs,top,n=200):
        mem=[g for g in gs if g in R.index]
        if len(mem)<5: return None
        obs=len(set(mem)&top); prof=dec.loc[mem].value_counts(); hits=0
        for _ in range(n):
            pick=[]
            for d_,k in prof.items():
                pool=dec.index[dec==d_]
                if len(pool)==0: continue
                pick+=list(rng.choice(pool,size=min(k,len(pool)),replace=False))
            if len(set(pick)&top)>=obs: hits+=1
        return {'n':len(mem),'obs':obs,'exp':round(len(mem)*200/len(R),1),'p':hits/n}
    mvp=ranked('MVP'); top=set(mvp.index[:200])
    psma=ranked('PSMA1'); ptop=set(psma.index[:200]) if psma is not None else set()
    gate={t:spec(sets.get(t,set()),ptop) for t in
          ['GOCC_PROTEASOME_COMPLEX','GOCC_PROTEASOME_CORE_COMPLEX']}
    return {'n':len(C),'proteins':len(R),
            'gate':gate,
            'under':{t:spec(sets.get(t,set()),top) for t in UNDER},
            'neg':{t:spec(sets.get(t,set()),top) for t in NEG},
            'ref':{t:spec(sets.get(t,set()),top) for t in REF}}

out={}
for d in DECIDE+CNS:
    out[d]=analyse(d); r=out[d]
    print(f"=== {d}  n={r['n']} proteins={r['proteins']}",flush=True)
    print(f"  GATE proteasome (PSMA1 seed): "+", ".join(f"{k.split('_',1)[1][:22]} p={v['p'] if v else None}" for k,v in r['gate'].items()),flush=True)
    for lbl,blk in (('UNDER TEST',r['under']),('NEG CONTROL',r['neg']),('abundance ref',r['ref'])):
        for t,v in blk.items():
            print(f"  {lbl:<14} {t[:44]:<46} {v}",flush=True)

gate_ok=sum(1 for d in DECIDE if any(v and v['p']<0.05 for v in out[d]['gate'].values()))
print(f"\nGATE: proteasome clears abundance matching in {gate_ok}/3 non-CNS -> {'PASS' if gate_ok>=2 else 'FAIL'}",flush=True)
def clears(t,d): 
    v=out[d]['under'].get(t); return bool(v and v['p']<0.05)
surv=[t for t in ['GOCC_RUFFLE','GOBP_ACTIN_FILAMENT_ORGANIZATION']
      if clears(t,'ucec_cptac_2020') and clears(t,'ccle_broad_2019')]
if gate_ok<2: verdict='UNINFORMATIVE (gate failed)'
elif surv: verdict=f'#155 SURVIVES abundance matching: {surv}'
else: verdict='KILL CONDITION MET - #155 struck as a protein-abundance artefact'
print('VERDICT:',verdict,flush=True)
json.dump({'verdict':verdict,'gate_nonCNS_pass':gate_ok,'surviving':surv,'detail':out},
          open('results/cyto_composition.json','w'),indent=1,default=str)
