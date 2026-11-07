"""Does the membrane-repair / endolysosomal module survive the cytoplasmic-mass confound?
Pre-registered in MEMBRANE_MODULE_PREREGISTRATION.md. Gene sets external, unmodified."""
import pandas as pd, numpy as np, json
from scipy.stats import spearmanr, chi2

PRIMARY = 'GOBP_PLASMA_MEMBRANE_REPAIR'
SECONDARY = ['GOCC_LYSOSOME','GOCC_LATE_ENDOSOME','GOBP_ENDOSOMAL_TRANSPORT',
             'GOCC_CAVEOLA','GOCC_MEMBRANE_RAFT']
PROLIF = ['MKI67','TOP2A','MCM2','MCM6','PCNA','MYBL2']

sets = {}
for f in ['data/raw/eggnog/c5.go.bp.v2024.1.Hs.symbols.gmt',
          'data/raw/eggnog/c5.go.cc.v2024.1.Hs.symbols.gmt']:
    for line in open(f):
        p = line.rstrip('\n').split('\t')
        sets[p[0]] = set(p[2:])

M = pd.read_parquet('data/processed/prot/ccle_broad_2019.parquet')
M = M[~M.index.duplicated()]
print(f'proteins {M.shape[0]} lines {M.shape[1]}', flush=True)
Z = M.sub(M.mean(axis=1), axis=0).div(M.std(axis=1).replace(0, np.nan), axis=0)

cyto = [g for g in Z.index if str(g).startswith(('RPL','RPS')) and 'P1' not in str(g)]
nuc  = [g for g in Z.index if str(g).startswith(('HNRNP','SRSF','SF3B','SMC'))]
nc = Z.loc[cyto].mean() - Z.loc[nuc].mean()
cov = [nc.rename('nc')] + [Z.loc[g].rename(g) for g in PROLIF if g in Z.index]
C = pd.concat(cov, axis=1).dropna()
print(f'covariates: N:C ({len(cyto)} cyto, {len(nuc)} nuc) + {len(C.columns)-1} proliferation', flush=True)

keep = Z.columns.intersection(C.index)
Zk, Ck = Z[keep], C.loc[keep]
X = np.c_[np.ones(len(Ck)), Ck.values]
XtXi_Xt = np.linalg.pinv(X)
V = Zk.values
ok = ~np.isnan(V).any(axis=1)
R = np.full_like(V, np.nan)
R[ok] = V[ok] - (V[ok] @ XtXi_Xt.T) @ X.T
Res = pd.DataFrame(R, index=Zk.index, columns=Zk.columns).dropna(how='all')
print(f'residualised matrix: {Res.shape}', flush=True)

def ranked(seed):
    s = Res.loc[seed].values
    out = {}
    for g, row in Res.iterrows():
        if g == seed: continue
        r, _ = spearmanr(s, row.values)
        if np.isfinite(r): out[g] = r
    return pd.Series(out).sort_values(ascending=False)

mvp = ranked('MVP')
top50, top200 = set(mvp.index[:50]), set(mvp.index[:200])

# --- GATE 1: assembly ---
g1 = {g: (int(list(mvp.index).index(g)) + 1 if g in mvp.index else None) for g in ['PARP4','TEP1']}
gate1 = all(v is not None and v <= 50 for v in g1.values())
# --- GATE 2: complex ---
psma = ranked('PSMA1')
prot_subs = {g for g in Res.index if str(g).startswith(('PSMA','PSMB','PSMC','PSMD'))}
rec = len(set(psma.index[:50]) & prot_subs)
gate2 = rec >= 10
print(f'GATE1 assembly PARP4/TEP1 ranks {g1} -> {"PASS" if gate1 else "FAIL"}', flush=True)
print(f'GATE2 PSMA1 recovers {rec}/25 proteasome in top50 -> {"PASS" if gate2 else "FAIL"}', flush=True)

# --- enrichment with matched-random specificity ---
abund = M.mean(axis=1).reindex(Res.index)
dec = pd.qcut(abund.rank(method='first'), 10, labels=False)
rng = np.random.default_rng(0)
def spec(gs, n_rand=200):
    members = [g for g in gs if g in Res.index]
    if len(members) < 5: return None
    obs = len(set(members) & top200)
    prof = dec.loc[members].value_counts()
    hits = 0
    for _ in range(n_rand):
        pick = []
        for d, k in prof.items():
            pool = dec.index[dec == d]
            pick += list(rng.choice(pool, size=min(k, len(pool)), replace=False))
        if len(set(pick) & top200) >= obs: hits += 1
    return {'n_members': len(members), 'observed_in_top200': obs,
            'specificity_p': hits / n_rand}

res = {'primary': {PRIMARY: spec(sets.get(PRIMARY, set()))}}
print(f"\nPRIMARY {PRIMARY}: {res['primary'][PRIMARY]}", flush=True)
res['secondary'] = {t: spec(sets.get(t, set())) for t in SECONDARY}
for t, v in res['secondary'].items(): print(f'  {t}: {v}', flush=True)

pp = res['primary'][PRIMARY]
if not (gate1 and gate2):      verdict = 'UNINFORMATIVE (gate failed)'
elif pp and pp['specificity_p'] < 0.05: verdict = 'MODULE SURVIVES the confound'
else:                          verdict = 'MODULE DOES NOT SURVIVE - #41 stays struck, strengthened'
print('\nVERDICT:', verdict, flush=True)

# post-hoc Fisher, declared as such
f = -2*(np.log(0.058) + np.log(0.067)); fp = 1 - chi2.cdf(f, 4)
print(f'POST-HOC (not the registered rule): Fisher of 0.058 and 0.067 -> X2={f:.2f}, p={fp:.4f}', flush=True)

print('\nMVP top 25 residualised correlates:')
print(mvp.head(25).round(3).to_string(), flush=True)

json.dump({'gate1_assembly': gate1, 'gate1_ranks': g1, 'gate2_proteasome': gate2,
           'gate2_recovered': rec, 'verdict': verdict, **res,
           'posthoc_fisher_p': round(float(fp), 5),
           'mvp_top25': {k: round(float(v), 4) for k, v in mvp.head(25).items()}},
          open('results/membrane_module.json','w'), indent=1)
