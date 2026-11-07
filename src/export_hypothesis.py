"""Graham's export hypothesis: if loaded vaults are expelled rather than degraded,
secretion/export machinery should be near the vault. Empirical nulls, as section 50 requires."""
import openpyxl, json, numpy as np, pandas as pd, warnings
warnings.filterwarnings('ignore')
NDRAW=200_000
TERMS=['GOCC_SECRETORY_GRANULE','GOCC_SECRETORY_VESICLE','GOCC_LATE_ENDOSOME','GOBP_EXOCYTOSIS',
       'GOBP_VESICLE_MEDIATED_TRANSPORT','GOBP_EXPORT_FROM_CELL','GOBP_RESPONSE_TO_XENOBIOTIC_STIMULUS',
       'GOBP_DETOXIFICATION']
REF=['GOBP_PROTEASOMAL_PROTEIN_CATABOLIC_PROCESS','GOBP_MACROAUTOPHAGY','GOCC_RIBOSOME']
sets={}
for f in ['data/raw/eggnog/c5.go.bp.v2024.1.Hs.symbols.gmt','data/raw/eggnog/c5.go.cc.v2024.1.Hs.symbols.gmt']:
    for line in open(f):
        p=line.rstrip('\n').split('\t'); sets[p[0]]=set(p[2:])
wb=openpyxl.load_workbook('argon/raw/lodwick_supp_4.xlsx',read_only=True,data_only=True)
rows=list(wb['Fig. 5c-d'].iter_rows(values_only=True))
D=pd.DataFrame(rows[1:],columns=list(rows[0])).dropna(subset=['GeneName'])
for c in D.columns[1:]: D[c]=pd.to_numeric(D[c],errors='coerce')
D=D.drop_duplicates('GeneName').set_index('GeneName')
N=len(D); L=D['WT_LFC']; uni=set(D.index)
dec=pd.qcut(pd.Series(np.arange(N),index=D.index).rank(method='first'),10,labels=False,duplicates='drop')
pools={d:np.array([list(D.index).index(g) for g in dec.index[dec==d]]) for d in sorted(dec.unique())}
vals=L.values; rng=np.random.default_rng(3)
def emp(t):
    mem=[g for g in sets.get(t,set()) if g in uni]
    if len(mem)<10: return None
    obs=L.loc[mem].mean(); prof=dec.loc[mem].value_counts().to_dict()
    mus=np.zeros(NDRAW)
    for d_,k in prof.items():
        p=pools[d_]; j=rng.integers(0,len(p),size=(NDRAW,k)); mus+=vals[p[j]].sum(axis=1)
    mus/=len(mem)
    ge=int((mus>=obs).sum())
    return {'n':len(mem),'obs':round(float(obs),4),'null':round(float(mus.mean()),4),
            'pct':round(100*float((mus<obs).mean()),2),'ge':ge,'p_hi':(ge+1)/(NDRAW+1),
            'p_lo':(NDRAW-ge+1)/(NDRAW+1)}
# GATE: vault core must be enriched (sanity) on the same statistic
core=[g for g in ['MVP','PARP4','TEP1']]
obs=L.loc[core].mean(); prof=dec.loc[core].value_counts().to_dict()
mus=np.zeros(NDRAW)
for d_,k in prof.items():
    p=pools[d_]; j=rng.integers(0,len(p),size=(NDRAW,k)); mus+=vals[p[j]].sum(axis=1)
mus/=3; gate=int((mus>=obs).sum())<20
print(f'GATE vault core mean {obs:+.3f}, {int((mus>=obs).sum())} of {NDRAW} draws >= -> {"PASS" if gate else "FAIL"}\n',flush=True)
print('EXPORT / SECRETION machinery in the anti-MVP pulldown:')
res={}
for t in TERMS:
    r=emp(t); res[t]=r
    if r: print(f'  {t[:44]:<46} n={r["n"]:<4} obs={r["obs"]:+.3f} null={r["null"]:+.3f} pct={r["pct"]:5.1f}  p_enriched={r["p_hi"]:.3f} p_depleted={r["p_lo"]:.3f}',flush=True)
print('\nreference points from earlier sections:')
for t in REF:
    r=emp(t); res[t]=r
    if r: print(f'  {t[:44]:<46} n={r["n"]:<4} obs={r["obs"]:+.3f} pct={r["pct"]:5.1f}',flush=True)
enr=[t for t in TERMS if res[t] and res[t]['p_hi']<0.05]
dep=[t for t in TERMS if res[t] and res[t]['p_lo']<0.05]
print(f'\nenriched (p<0.05): {enr or "NONE"}')
print(f'depleted (p<0.05): {dep or "NONE"}')
verdict=('UNINFORMATIVE (gate failed)' if not gate else
 f'EXPORT MACHINERY PRESENT: {len(enr)}/{len(TERMS)} terms enriched' if enr else
 f'NO EXPORT MACHINERY near the vault: 0/{len(TERMS)} enriched, {len(dep)} depleted')
print('\nVERDICT:',verdict,flush=True)
json.dump({'gate':bool(gate),'terms':res,'enriched':enr,'depleted':dep,'verdict':verdict},
          open('results/export_hypothesis.json','w'),indent=1,default=str)
