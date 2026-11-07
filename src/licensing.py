"""Does argon's AHR/STAT1-vs-EZH2 licensing model survive the N:C confound?
Pre-registered in LICENSING_PREREGISTRATION.md."""
import pandas as pd, numpy as np, json
from scipy.stats import spearmanr

PROLIF=['MKI67','TOP2A','MCM2','MCM6','PCNA','MYBL2']
ACTIVATING=['AHR','ARNT','STAT1','STAT2','IRF9','TAP1','TAP2','B2M','SP1']
SILENCING=['EZH2','EED','SUZ12']
LOWCOV=['IRF1','CYP1A1','NLRC5']

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
Zc=Z[C.index]; Zc=Zc.loc[Zc.notna().sum(axis=1)>=150]
X=np.c_[np.ones(len(C)),C.values]
def rsd(row):
    m=row.notna().values; y=row.values[m]; Xm=X[m]
    b=np.linalg.lstsq(Xm,y,rcond=None)[0]
    o=np.full(len(row),np.nan); o[m]=y-Xm@b; return o
R=pd.DataFrame(np.vstack([rsd(Zc.loc[g]) for g in Zc.index]),index=Zc.index,columns=C.index)
print(f'residualised: {R.shape}',flush=True)

def rho(a,b,mat):
    if a not in mat.index or b not in mat.index: return None
    x,y=mat.loc[a].values,mat.loc[b].values
    m=np.isfinite(x)&np.isfinite(y)
    if m.sum()<30: return None
    r,p=spearmanr(x[m],y[m]); return (round(float(r),3),round(float(p),4),int(m.sum()))

# --- GATE (argon's own spec) ---
g=rho('STAT1','TAP1',R)
gate = g is not None and g[0]>0.6
print(f'GATE STAT1 vs TAP1 after residualisation: {g} -> {"PASS" if gate else "FAIL"}',flush=True)

print('\n            raw rho vs MVP      residualised rho vs MVP')
rows={}
for g_ in ACTIVATING+SILENCING+LOWCOV:
    raw=rho('MVP',g_,Zc); res=rho('MVP',g_,R)
    rows[g_]={'raw':raw,'resid':res}
    tag=' (low coverage, no threshold)' if g_ in LOWCOV else ''
    print(f'  {g_:<8} {str(raw):<22} {str(res)}{tag}',flush=True)

# --- TEST A ---
keep=[g_ for g_ in ['AHR','STAT1','TAP1','IRF9'] if rows[g_]['resid'] and rows[g_]['resid'][0]>0.25]
allow=[g_ for g_ in ['AHR','STAT1','TAP1','IRF9'] if rows[g_]['resid'] and abs(rows[g_]['resid'][0])<0.15]
testA = 'SURVIVES' if len(keep)>=2 else ('FAILS' if len(allow)==4 else 'PARTIAL')
print(f'\nTEST A activating arm: rho>0.25 -> {keep} => {testA}',flush=True)

# --- TEST B: EZH2 vs nuclear background ---
nucset=[x for x in sets.get('GOCC_NUCLEAR_BODY',set()) if x in R.index and x!='MVP']
rng=np.random.default_rng(0)
pick=rng.choice(nucset,size=min(200,len(nucset)),replace=False)
dist=[]
for g_ in pick:
    r=rho('MVP',g_,R)
    if r: dist.append(r[0])
dist=np.array(dist)
ez=rows['EZH2']['resid'][0] if rows['EZH2']['resid'] else None
pct=float((dist<ez).mean()*100) if ez is not None else None
testB='EZH2-SPECIFIC' if (pct is not None and pct<5) else 'COMPARTMENT ARTEFACT'
print(f'\nTEST B: {len(dist)} random GOCC_NUCLEUS proteins vs MVP (residualised)')
print(f'  nuclear background rho: mean {dist.mean():+.3f}  5th pct {np.percentile(dist,5):+.3f}  median {np.median(dist):+.3f}')
print(f'  EZH2 residualised rho {ez:+.3f} sits at the {pct:.1f}th percentile of that background')
print(f'  PRC2 partners: EED {rows["EED"]["resid"]}  SUZ12 {rows["SUZ12"]["resid"]}')
print(f'TEST B verdict: {testB}',flush=True)

if not gate: verdict='UNINFORMATIVE (gate failed)'
elif testA=='FAILS' and testB=='COMPARTMENT ARTEFACT': verdict='KILL CONDITION MET - #103 struck'
else: verdict=f'activating arm {testA}; EZH2 arm {testB}'
print('\nVERDICT:',verdict,flush=True)
json.dump({'gate_stat1_tap1':g,'gate':bool(gate),'correlations':rows,
           'testA':testA,'testA_surviving':keep,
           'testB':testB,'ezh2_resid':ez,'ezh2_nuclear_percentile':pct,
           'nuclear_bg':{'n':len(dist),'mean':round(float(dist.mean()),3),
                         'p5':round(float(np.percentile(dist,5)),3),
                         'median':round(float(np.median(dist)),3)},
           'verdict':verdict},open('results/licensing.json','w'),indent=1,default=str)
