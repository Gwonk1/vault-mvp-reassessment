"""Empirical null for the SMC5/6 continuous statistic, as pre-committed in the
SMC56_CONTINUOUS_PREREGISTRATION.md addendum. 200,000+ matched draws."""
import openpyxl, json, numpy as np, pandas as pd, warnings
warnings.filterwarnings('ignore')
from scipy.stats import norm, skew, kurtosis

NDRAW=400_000
sets={}
for f in ['data/raw/eggnog/c5.go.bp.v2024.1.Hs.symbols.gmt','data/raw/eggnog/c5.go.cc.v2024.1.Hs.symbols.gmt']:
    for line in open(f):
        p=line.rstrip('\n').split('\t'); sets[p[0]]=set(p[2:])
wb=openpyxl.load_workbook('argon/raw/lodwick_supp_4.xlsx',read_only=True,data_only=True)
rows=list(wb['Fig. 5c-d'].iter_rows(values_only=True))
D=pd.DataFrame(rows[1:],columns=list(rows[0])).dropna(subset=['GeneName'])
for c in D.columns[1:]: D[c]=pd.to_numeric(D[c],errors='coerce')
D=D.drop_duplicates('GeneName').set_index('GeneName')
uni=list(D.index); N=len(uni); L=D['WT_LFC']
print(f'universe {N} | WT_LFC skew {skew(L):.2f} excess kurtosis {kurtosis(L):.2f}')
print(f'  so the null of a small-n mean is NOT Gaussian - the addendum concern, quantified\n', flush=True)

dec=pd.qcut(pd.Series(np.arange(N),index=D.index).rank(method='first'),10,labels=False,duplicates='drop')
pool_by_dec={d:np.array([uni.index(g) for g in dec.index[dec==d]]) for d in sorted(dec.unique())}
vals=L.values
rng=np.random.default_rng(7)

def empirical(members,label,ndraw=NDRAW):
    mem=[g for g in members if g in L.index]
    obs=L.loc[mem].mean()
    prof=dec.loc[mem].value_counts().to_dict()
    mus=np.zeros(ndraw)
    for d_,k in prof.items():
        p=pool_by_dec[d_]
        idx=rng.integers(0,len(p),size=(ndraw,k))      # with replacement within decile
        mus+=vals[p[idx]].sum(axis=1)
    mus/=len(mem)
    ge=int((mus>=obs).sum())
    p_emp=(ge+1)/(ndraw+1)
    z=(obs-mus.mean())/mus.std(ddof=1)
    p_norm=norm.sf(z)
    print(f'{label}:')
    print(f'  n={len(mem)}  observed mean = {obs:+.4f}')
    print(f'  empirical null: mean {mus.mean():+.4f} sd {mus.std(ddof=1):.4f} '
          f'skew {skew(mus):+.2f} excess kurt {kurtosis(mus):+.2f}')
    print(f'  RAW COUNT of null draws >= observed: {ge} of {ndraw}')
    print(f'  empirical one-sided p = {p_emp:.3e}   (resolution limit {1/(ndraw+1):.2e})')
    print(f'  normal-approximation p = {p_norm:.3e}  from z = {z:.3f}')
    ratio = p_emp/p_norm if p_norm>0 else float('inf')
    print(f'  => empirical is {ratio:,.0f}x LESS extreme than the normal approximation'
          if ratio>1 else f'  => empirical and normal agree within {1/ratio:.1f}x', flush=True)
    return {'n':len(mem),'obs':float(obs),'null_mean':float(mus.mean()),'null_sd':float(mus.std(ddof=1)),
            'null_skew':float(skew(mus)),'null_kurt':float(kurtosis(mus)),'count_ge':ge,'ndraw':ndraw,
            'p_empirical':float(p_emp),'p_normal':float(p_norm),'z':float(z),'ratio':float(ratio)}

core=empirical(['MVP','PARP4','TEP1'],'GATE vault core (MVP/PARP4/TEP1)')
print()
smc=empirical(sets['GOCC_SMC5_SMC6_COMPLEX'],'GOCC_SMC5_SMC6_COMPLEX')

FAMILY=1849
q_emp = min(1.0, smc['p_empirical']*FAMILY/2)   # BH, rank 2 of 1849
q_core= min(1.0, core['p_empirical']*FAMILY/1)
print(f'\nBH over the {FAMILY}-term family, SMC5/6 at rank 2:')
print(f'  q_empirical = {q_emp:.4f}   (normal-approximation q was 0.0003)')
print(f'  vault-core gate q_empirical = {q_core:.3e} -> gate q<0.01: {q_core<0.01}')
gate=q_core<0.01
if not gate: verdict='UNINFORMATIVE (gate failed on the empirical statistic)'
elif q_emp<0.05: verdict=f'SMC5/6 SURVIVES on the EMPIRICAL null (q={q_emp:.4f})'
else: verdict=f'SMC5/6 DIES on the empirical null (q={q_emp:.4f}); the normal approximation was doing the work'
print('\nVERDICT:',verdict, flush=True)
json.dump({'core':core,'smc56':smc,'family':FAMILY,'q_empirical':q_emp,
           'q_core_empirical':q_core,'gate_pass':bool(gate),'verdict':verdict},
          open('results/smc56_empirical.json','w'),indent=1)
