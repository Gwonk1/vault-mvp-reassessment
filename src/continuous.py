"""Redo every dichotomised contact test on the continuous measurement.
Pre-registered in CONTINUOUS_PREREGISTRATION.md."""
import openpyxl, json, numpy as np, pandas as pd, warnings
warnings.filterwarnings('ignore')

NDRAW = 2000
TARGETED = ['GOBP_CYTOPLASMIC_TRANSLATION','GOCC_RIBOSOME','GOBP_TRANSLATION','GOCC_RUFFLE',
            'GOBP_ACTIN_FILAMENT_ORGANIZATION','GOCC_MITOCHONDRION','GOCC_SMC5_SMC6_COMPLEX',
            'GOCC_SUMO_LIGASE_COMPLEX','GOBP_PROTEASOMAL_PROTEIN_CATABOLIC_PROCESS',
            'GOBP_PROTEIN_CATABOLIC_PROCESS','GOBP_MACROAUTOPHAGY']

sets={}
for f in ['data/raw/eggnog/c5.go.bp.v2024.1.Hs.symbols.gmt','data/raw/eggnog/c5.go.cc.v2024.1.Hs.symbols.gmt']:
    for line in open(f):
        p=line.rstrip('\n').split('\t'); sets[p[0]]=set(p[2:])

wb=openpyxl.load_workbook('argon/raw/lodwick_supp_4.xlsx',read_only=True,data_only=True)
rows=list(wb['Fig. 5c-d'].iter_rows(values_only=True))
D=pd.DataFrame(rows[1:],columns=list(rows[0])).dropna(subset=['GeneName'])
for c in D.columns[1:]: D[c]=pd.to_numeric(D[c],errors='coerce')
D=D.drop_duplicates('GeneName').set_index('GeneName')
uni=set(D.index); N=len(uni)
L=D['WT_LFC']
print(f'universe {N} | mean WT_LFC overall {L.mean():+.4f}', flush=True)

dec=pd.qcut(pd.Series(np.arange(N),index=D.index).rank(method='first'),10,labels=False,duplicates='drop')
rng=np.random.default_rng(0)
pools={d:dec.index[dec==d] for d in dec.unique()}

def shift(members,ndraw=NDRAW):
    mem=[g for g in members if g in uni]
    if len(mem)<3: return None
    obs=L.loc[mem].mean(); prof=dec.loc[mem].value_counts()
    mus=np.empty(ndraw)
    for i in range(ndraw):
        pick=[]
        for d_,k in prof.items():
            pool=pools[d_]; pick+=list(rng.choice(pool,size=min(k,len(pool)),replace=False))
        mus[i]=L.loc[pick].mean()
    pct=float((mus<obs).mean()*100)
    return {'n':len(mem),'mean':round(float(obs),4),'null_mean':round(float(mus.mean()),4),
            'null_sd':round(float(mus.std()),4),'pct':round(pct,2),
            'p_two_sided':round(2*min(pct,100-pct)/100,4)}

# --- GATE 1: the vault core must show a large positive shift ---
core=shift(['MVP','PARP4','TEP1'],ndraw=4000)
g1 = core is not None and core['pct']>=99.0
print(f"\nGATE1 vault core (MVP/PARP4/TEP1): {core}")
print(f"  -> percentile >=99: {g1}", flush=True)

# --- TARGETED ---
print('\nTARGETED (previously dichotomised contact tests):')
tgt={}
for t in TARGETED:
    r=shift(sets.get(t,set())); tgt[t]=r
    print(f'  {t[:52]:<54} {r}', flush=True)

# --- UNBIASED: all 10-500 member terms, continuous ---
terms={t:(gs&uni) for t,gs in sets.items()}
terms={t:m for t,m in terms.items() if 10<=len(m)<=500}
print(f'\nUNBIASED: {len(terms)} terms, continuous statistic (300 draws each for speed)', flush=True)
allr={}
for t,m in terms.items():
    allr[t]=shift(m,ndraw=300)
pcts=np.array([v['pct'] for v in allr.values() if v])
# --- GATE 3: calibration, percentiles must be ~uniform ---
q=[float(np.percentile(pcts,x)) for x in [10,25,50,75,90]]
g3 = 35<=np.median(pcts)<=65
print(f'  percentile distribution across terms: deciles {[round(x,1) for x in q]}')
print(f'  median {np.median(pcts):.1f} -> calibration gate (35-65): {g3}', flush=True)

ser=pd.Series({t:v['pct'] for t,v in allr.items() if v}).sort_values(ascending=False)
rank_trans=int((ser>=ser.get('GOBP_CYTOPLASMIC_TRANSLATION',0)).sum())
top_pct_trans=100*rank_trans/len(ser)
print(f'\nSPECIFICITY (the registered question):')
print(f'  GOBP_CYTOPLASMIC_TRANSLATION ranks {rank_trans} of {len(ser)} = top {top_pct_trans:.2f}%')
print(f'  top 15 terms by matched percentile:')
for t in ser.index[:15]:
    v=allr[t]; print(f'    {t[:54]:<56} n={v["n"]:<4} mean={v["mean"]:+.3f} pct={v["pct"]:.1f}', flush=True)
for t in TARGETED:
    if t in ser.index:
        r=int((ser>=ser[t]).sum()); print(f'  {t[:50]:<52} rank {r:>5} of {len(ser)} (top {100*r/len(ser):.2f}%)')

if not g1: verdict='UNINFORMATIVE (vault-core gate failed)'
elif not g3: verdict='UNINFORMATIVE (calibration gate failed)'
elif top_pct_trans<=2.0: verdict=f'TRANSLATION CONVERGENCE CORROBORATED (top {top_pct_trans:.2f}% of terms)'
elif top_pct_trans>10.0: verdict=f'TRANSLATION WEAKENED (outside top 10%: {top_pct_trans:.2f}%)'
else: verdict=f'TRANSLATION INTERMEDIATE ({top_pct_trans:.2f}%) - between the registered bars'
print('\nVERDICT:',verdict, flush=True)

json.dump({'gate1_core':core,'gate1_pass':bool(g1),'gate3_median_pct':float(np.median(pcts)),
           'gate3_pass':bool(g3),'targeted':tgt,'n_terms':len(ser),
           'translation_rank':rank_trans,'translation_top_pct':top_pct_trans,
           'top20':{t:allr[t] for t in ser.index[:20]},'verdict':verdict},
          open('results/continuous.json','w'),indent=1,default=str)
