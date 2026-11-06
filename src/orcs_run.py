"""ORCS condition test per ORCS_PREREGISTRATION.md. Usage: orcs_run.py controls | final"""
import json, sys, os, glob
import numpy as np, pandas as pd
sys.path.insert(0, 'src')
from orcs_classes import load_index
CACHE = 'data/processed/orcs_matrix.npz'
BLIND = {'MVP', 'TEP1', 'PARP4'}


def build(U):
    """gene x screen: 0 absent, 1 tested non-hit, 2 hit."""
    sid = {s: i for i, s in enumerate(U.id)}
    genes = {}; R, C, V = [], [], []
    for f in glob.glob('data/raw/orcs/screens/*.screen.tab.txt'):
        s = os.path.basename(f).split('SCREEN_')[1].split('-')[0]
        if s not in sid: continue
        d = pd.read_csv(f, sep='\t', usecols=['OFFICIAL_SYMBOL', 'HIT'], dtype=str, quoting=3)
        d = d.sort_values('HIT', ascending=False).drop_duplicates('OFFICIAL_SYMBOL')
        R.extend(genes.setdefault(g, len(genes)) for g in d.OFFICIAL_SYMBOL); C.extend([sid[s]] * len(d)); V.extend(np.where(d.HIT == 'YES', 2, 1))
    M = np.zeros((len(genes), len(sid)), dtype=np.uint8); M[R, C] = V
    np.savez_compressed(CACHE, M=M, genes=np.array(list(genes)), screens=np.array(U.id))


def scores(M, U, mask):
    """Mean across papers of per-paper hit fraction, using screens in mask."""
    out = np.zeros(M.shape[0]); n = np.zeros(M.shape[0]); paper = U.SOURCE_ID.values
    for p in pd.unique(paper[mask]):
        w = mask & (paper == p)
        t = (M[:, w] > 0).sum(axis=1); h = (M[:, w] == 2).sum(axis=1); ok = t > 0
        out[ok] += h[ok] / t[ok]; n[ok] += 1
    return np.divide(out, n, out=np.full(len(out), np.nan), where=n > 0)


def bh(p):
    p = np.asarray(p); o = np.argsort(p); q = np.empty(len(p)); m = len(p); run = 1.0
    for r in range(m - 1, -1, -1):
        run = min(run, p[o[r]] * m / (r + 1)); q[o[r]] = run
    return q


def run():
    I = load_index(); U = I[I.universe].reset_index(drop=True)
    if not os.path.exists(CACHE): build(U)
    z = np.load(CACHE, allow_pickle=False); M, genes = z['M'], z['genes']
    assert list(z['screens']) == list(U.id)
    keep = (M > 0).sum(axis=1) >= 200          # genes tested in a usable share of screens
    M, genes = M[keep], genes[keep]
    cls = U.cls.values; paper = U.SOURCE_ID.values; line = U.CELL_LINE.values
    testable = [c for c in pd.unique(cls) if U[U.cls == c].SOURCE_ID.nunique() >= 3]
    overall = scores(M, U, np.ones(len(U), bool))
    pv = pd.DataFrame(index=genes, columns=testable, dtype=float); sc = pv.copy(); npap = pv.copy(); nline = pv.copy(); rest = pv.copy()
    for c in testable:
        w = cls == c; s = scores(M, U, w); r = scores(M, U, ~w)
        o = np.argsort(np.nan_to_num(r), kind='stable'); ps = np.ones(len(s)); N = len(s); ss = np.nan_to_num(s)
        for rank, g in enumerate(o):
            a = max(0, min(rank - 500, N - 1001)); win = o[a:a + 1001]; win = win[win != g]
            ps[g] = (1 + (ss[win] >= ss[g]).sum()) / (len(win) + 1)
        pv[c] = ps; sc[c] = s; rest[c] = r
        H = M[:, w] == 2; pc = paper[w]; lc = line[w]
        up = pd.unique(pc); ul = pd.unique(lc)
        npap[c] = sum(H[:, pc == p].any(axis=1).astype(int) for p in up)
        nline[c] = sum(H[:, lc == l].any(axis=1).astype(int) for l in ul)
    q = pv.apply(lambda row: pd.Series(bh(row.values), index=row.index), axis=1)
    sig = (q < .05) & (npap >= 3) & (nline >= 2)
    return dict(I=I, U=U, M=M, genes=genes, overall=pd.Series(overall, index=genes), p=pv, q=q, sc=sc, rest=rest, npap=npap, nline=nline, sig=sig, testable=testable)


def result(R, g):
    i = list(R['genes']).index(g)
    t = pd.DataFrame({k: R[k].loc[g] for k in ['sc', 'rest', 'p', 'q', 'npap', 'nline', 'sig']})
    return t.sort_values('p').round(4)


if __name__ == '__main__':
    R = run(); mode = sys.argv[1]
    print('genes', len(R['genes']), 'screens', len(R['U']), 'testable', R['testable'])
    print('any-class signal rate, all genes', round(R['sig'].any(axis=1).mean(), 4)); print('per class', R['sig'].mean().round(4).to_dict())
    C = {'genotoxic': ['FANCD2', 'FANCA', 'XRCC1'], 'virus': ['ACE2', 'SLC35B2', 'EXT1'], 'immune_killing': ['JAK1', 'IFNGR1', 'B2M']}
    gate = {}
    for c, gs in C.items():
        v = {g: (bool(R['sig'].loc[g, c]), round(float(R['q'].loc[g, c]), 4), int(R['npap'].loc[g, c])) for g in gs if g in R['sig'].index}
        gate[c] = sum(x[0] for x in v.values()) >= 2; print(c, 'PASS' if gate[c] else 'FAIL', v)
    pct = R['overall'].rank(pct=True) * 100
    res = dict(n_genes=len(R['genes']), n_screens=len(R['U']), any_rate=float(R['sig'].any(axis=1).mean()), gate=gate)
    if mode == 'final':
        for g in sorted(BLIND):
            print(f'\n=== {g}: overall hit rate {R["overall"][g]:.4f}, genome percentile {pct[g]:.1f}, signal classes', list(R['sig'].columns[R['sig'].loc[g]]))
            print(result(R, g).to_string())
            res[g] = dict(overall=float(R['overall'][g]), pct=float(pct[g]), table=result(R, g).reset_index().to_dict('records'))
        U = R['U']; M = R['M']; i = list(R['genes']).index('MVP')
        h = U[M[i] == 2][['id', 'SOURCE_ID', 'AUTHOR', 'cls', 'CONDITION_NAME', 'CELL_LINE', 'SCREEN_RATIONALE', 'SCREEN_TYPE', 'NUMBER_OF_HITS', 'SCORES_SIZE']]
        print('\nMVP tested', int((M[i] > 0).sum()), 'hit', len(h)); h.to_csv('results/orcs_mvp_hits.csv', index=False)
        res['mvp_tested'] = int((M[i] > 0).sum()); res['mvp_hits'] = len(h)
        print(h.drop(columns=['SCREEN_TYPE']).to_string(max_colwidth=46))
    json.dump(res, open(f'results/orcs_{mode}.json', 'w'), indent=1, default=float)
