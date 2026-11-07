"""Unbiased scan of the vault's physical interactome.
Pre-registered in IPMS_SCAN_PREREGISTRATION.md. Same table and parse as sections 13, 41 and 43."""
import openpyxl, json, re, numpy as np, pandas as pd, warnings
warnings.filterwarnings('ignore')
from scipy.stats import hypergeom

NRAND_SPEC = 200
NRAND_CAL = 20

sets = {}
for f in ['data/raw/eggnog/c5.go.bp.v2024.1.Hs.symbols.gmt',
          'data/raw/eggnog/c5.go.cc.v2024.1.Hs.symbols.gmt']:
    for line in open(f):
        p = line.rstrip('\n').split('\t')
        sets[p[0]] = set(p[2:])

wb = openpyxl.load_workbook('argon/raw/lodwick_supp_4.xlsx', read_only=True, data_only=True)
rows = list(wb['Fig. 5c-d'].iter_rows(values_only=True))
D = pd.DataFrame(rows[1:], columns=list(rows[0])).dropna(subset=['GeneName'])
for c in D.columns[1:]:
    D[c] = pd.to_numeric(D[c], errors='coerce')
D = D.drop_duplicates('GeneName').set_index('GeneName')
uni = set(D.index); N = len(uni)
wt = set(D.index[(D.WT_LFC > 0) & (D.LWTP > 1.3)]); K = len(wt)
print(f'universe {N} | WT vault interactors {K}', flush=True)

def bh(ps):
    ps = np.asarray(ps); o = np.argsort(ps); n = len(ps); q = np.empty(n); prev = 1.0
    for i in range(n - 1, -1, -1):
        prev = min(prev, ps[o[i]] * n / (i + 1)); q[o[i]] = prev
    return q

terms = {t: (gs & uni) for t, gs in sets.items()}
terms = {t: m for t, m in terms.items() if 10 <= len(m) <= 500}
print(f'terms tested: {len(terms)}', flush=True)

def scan(target):
    names, ps = [], []
    for t, m in terms.items():
        k = len(m & target)
        if k == 0: continue
        names.append(t); ps.append(hypergeom.sf(k - 1, N, len(m), len(target)))
    if not names: return pd.Series(dtype=float)
    return pd.Series(bh(ps), index=names).sort_values()

# --- CALIBRATION GATE: random 88-protein subsets ---
rng = np.random.default_rng(0)
allg = sorted(uni)
cal = []
for _ in range(NRAND_CAL):
    sub = set(rng.choice(allg, size=K, replace=False))
    cal.append(int((scan(sub) < 0.05).sum()))
cal = np.array(cal)
gate = bool(np.median(cal) == 0)
print(f'\nCALIBRATION {NRAND_CAL} random {K}-protein subsets: '
      f'median {np.median(cal):.1f} terms at q<0.05, mean {cal.mean():.2f}, max {cal.max()}')
print(f'  95th percentile {np.percentile(cal,95):.1f} -> {"PASS" if gate else "FAIL"}', flush=True)

# --- REAL SCAN ---
q = scan(wt)
sig = list(q.index[q < 0.05])
print(f'\nreal interactor set: {len(sig)} terms at q<0.05 '
      f'(random 95th pct = {np.percentile(cal,95):.1f})', flush=True)

# matched-random specificity for anything that cleared
abcol = next((c for c in D.columns if re.search(r'intens|abund|ibaq|pep', str(c), re.I)), None)
ab = D[abcol] if abcol is not None else pd.Series(np.arange(N), index=D.index)
dec = pd.qcut(ab.rank(method='first'), 10, labels=False, duplicates='drop')
def spec(gs, n=NRAND_SPEC):
    mem = [g for g in gs if g in dec.index]
    obs = len(set(mem) & wt); prof = dec.loc[mem].value_counts(); hits = 0
    for _ in range(n):
        pick = []
        for d_, kk in prof.items():
            pool = dec.index[dec == d_]
            if len(pool) == 0: continue
            pick += list(rng.choice(pool, size=min(kk, len(pool)), replace=False))
        if len(set(pick) & wt) >= obs: hits += 1
    return {'n': len(mem), 'obs': obs, 'exp': round(len(mem) * K / N, 2), 'p': hits / n}

survivors = {}
for t in sig[:25]:
    s = spec(terms[t]); survivors[t] = {'q': round(float(q[t]), 5), **s}
    flag = 'SURVIVES' if s['p'] < 0.05 else 'abundance artefact'
    print(f'  {t[:52]:<54} q={q[t]:.4f} {s} {flag}', flush=True)

kept = [t for t, v in survivors.items() if v['p'] < 0.05]
if not gate:          verdict = 'UNINFORMATIVE (calibration gate failed)'
elif kept and len(sig) > np.percentile(cal, 95):
                      verdict = f'PHYSICAL NEIGHBOURHOOD: {len(kept)} term(s) survive both filters'
elif not sig:         verdict = 'NO DETECTABLE PHYSICAL NEIGHBOURHOOD - zero terms at q<0.05'
else:                 verdict = f'NO SURVIVING TERM - {len(sig)} reached q<0.05, {len(kept)} survived matched-random'
print('\nVERDICT:', verdict, flush=True)

# --- SECONDARY: the interactome as a list ---
L = D.loc[sorted(wt)][['WT_LFC', 'LWTP', 'WTKD_LFC', 'WTKD_P']].copy()
L['parp4_dependent'] = (L.WTKD_LFC > 0) & (L.WTKD_P > 1.3)
L = L.sort_values('WT_LFC', ascending=False)
print(f'\ntop 20 of the {K} physical vault interactors by WT_LFC:')
print(L.head(20).round(3).to_string(), flush=True)
L.round(4).to_csv('results/ipms_interactome.csv')

json.dump({'universe': N, 'n_interactors': K, 'terms_tested': len(terms),
           'calibration': {'n': NRAND_CAL, 'median': float(np.median(cal)),
                           'mean': round(float(cal.mean()), 2), 'max': int(cal.max()),
                           'p95': float(np.percentile(cal, 95))},
           'gate': gate, 'n_sig': len(sig), 'survivors': survivors,
           'kept': kept, 'verdict': verdict},
          open('results/ipms_scan.json', 'w'), indent=1, default=str)
