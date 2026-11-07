"""Is the SMC5/6 observation real, or an annotation coincidence / nuclear artefact?
Pre-registered in SMC56_PREREGISTRATION.md."""
import openpyxl, json, gzip, numpy as np, pandas as pd, warnings
warnings.filterwarnings('ignore')
from scipy.stats import hypergeom

SMC56 = ['SMC5', 'SMC6', 'NSMCE1', 'NSMCE2', 'NSMCE3', 'NSMCE4A']
CTRL  = ['SMC1A', 'SMC3', 'SMC2', 'SMC4']          # cohesin + condensin
TERM  = 'GOCC_SMC5_SMC6_COMPLEX'

sets = {}
for f in ['data/raw/eggnog/c5.go.bp.v2024.1.Hs.symbols.gmt',
          'data/raw/eggnog/c5.go.cc.v2024.1.Hs.symbols.gmt']:
    for line in open(f):
        p = line.rstrip('\n').split('\t'); sets[p[0]] = set(p[2:])

wb = openpyxl.load_workbook('argon/raw/lodwick_supp_4.xlsx', read_only=True, data_only=True)
rows = list(wb['Fig. 5c-d'].iter_rows(values_only=True))
D = pd.DataFrame(rows[1:], columns=list(rows[0])).dropna(subset=['GeneName'])
for c in D.columns[1:]: D[c] = pd.to_numeric(D[c], errors='coerce')
D = D.drop_duplicates('GeneName').set_index('GeneName')
uni = set(D.index); N = len(uni)
wt = set(D.index[(D.WT_LFC > 0) & (D.LWTP > 1.3)]); K = len(wt)
print(f'universe {N} | interactors {K}\n', flush=True)

# --- THREAT 1: BH across EVERY term with <10 members in the universe ---
fam = {t: (gs & uni) for t, gs in sets.items()}
fam = {t: m for t, m in fam.items() if 0 < len(m) < 10}
names, ps = [], []
for t, m in fam.items():
    names.append(t); ps.append(hypergeom.sf(len(m & wt) - 1, N, len(m), K))
o = np.argsort(ps); n = len(ps); qs = np.empty(n); prev = 1.0
for i in range(n - 1, -1, -1):
    prev = min(prev, ps[o[i]] * n / (i + 1)); qs[o[i]] = prev
Q = pd.Series(qs, index=names).sort_values()
print(f'THREAT 1: BH across all {n} small terms (<10 members in universe)')
print(f'  {TERM}: raw p={ps[names.index(TERM)]:.3e}  q={Q[TERM]:.4f}')
t1 = bool(Q[TERM] < 0.05)
print(f'  -> q<0.05: {t1}')
print('  top 8 of the family by q:')
for t in Q.index[:8]:
    m = fam[t]; print(f'    {t[:56]:<58} {len(m&wt)}/{len(m)}  q={Q[t]:.4f}', flush=True)

# --- THREAT 2: cohesin / condensin controls ---
def st(g):
    if g not in D.index: return None
    r = D.loc[g]
    return {'WT_LFC': round(float(r.WT_LFC), 3), 'LWTP': round(float(r.LWTP), 3),
            'interactor': bool(r.WT_LFC > 0 and r.LWTP > 1.3)}
print('\nTHREAT 2: SMC5/6 complex vs cohesin+condensin controls')
smc = {g: st(g) for g in SMC56}; ctl = {g: st(g) for g in CTRL}
for g, v in smc.items(): print(f'  SMC5/6  {g:<9} {v}', flush=True)
for g, v in ctl.items(): print(f'  CONTROL {g:<9} {v}', flush=True)
nctl = sum(1 for v in ctl.values() if v and v['interactor'])
t2 = bool(nctl < 2)
print(f'  -> {nctl}/4 cohesin+condensin members are interactors; control {"PASSES" if t2 else "FAILS"}', flush=True)

# --- THREAT 3: CFdb second instrument ---
want = set(['PARP4', 'TEP1'] + SMC56 + CTRL)
edges = {}
with gzip.open('data/raw/cfdb/Homo_sapiens.tsv.gz', 'rt') as fh:
    hdr = fh.readline().rstrip('\n').split('\t')
    ia, ib = hdr.index('protein_A'), hdr.index('protein_B')
    isc = hdr.index('score'); ipr = hdr.index('precision') if 'precision' in hdr else None
    for line in fh:
        p = line.rstrip('\n').split('\t')
        a, b = p[ia], p[ib]
        if a == 'MVP' and b in want: g = b
        elif b == 'MVP' and a in want: g = a
        else: continue
        pr = float(p[ipr]) if ipr is not None and p[ipr] not in ('', 'NA') else None
        prev = edges.get(g)
        if prev is None or (pr or 0) > (prev[1] or 0): edges[g] = (float(p[isc]), pr)
print('\nTHREAT 3: CFdb MVP edges (positive control = PARP4 at precision 0.676)')
for g in ['PARP4', 'TEP1'] + SMC56 + CTRL:
    e = edges.get(g)
    print(f'  MVP-{g:<9} ' + (f'score={e[0]:.4f} precision={e[1]}' if e else 'no edge found'), flush=True)
cf_gate = 'PARP4' in edges and (edges['PARP4'][1] or 0) > 0.5
cf_hits = [g for g in SMC56 if g in edges and (edges[g][1] or 0) > 0.5]
print(f'  CFdb lookup gate (PARP4 precision>0.5): {cf_gate}; SMC5/6 members with precision>0.5: {cf_hits or "none"}')
print('  (a CFdb negative is WEAK evidence per #180 - it misses TEP1 at 0.041)', flush=True)

verdict = ('SURVIVES - specific to the SMC5/6 complex' if (t1 and t2)
           else f'DIES - threat1_q<0.05={t1}, threat2_control_passes={t2}')
print('\nVERDICT:', verdict, flush=True)
json.dump({'n_small_terms': n, 'term_q': float(Q[TERM]), 'threat1_pass': t1,
           'smc56': smc, 'controls': ctl, 'n_controls_interactor': nctl, 'threat2_pass': t2,
           'cfdb': {k: list(v) for k, v in edges.items()}, 'cfdb_gate': bool(cf_gate),
           'cfdb_smc56_hits': cf_hits, 'verdict': verdict},
          open('results/smc56.json', 'w'), indent=1, default=str)
