"""Persister passenger test per PERSISTER_PREREGISTRATION.md (+ PERSISTER_DEVIATIONS.md).

Streams the Watermelon count matrix in gene chunks: never holds the dense matrix.
"""
import gzip, json, sys
import numpy as np, pandas as pd
sys.path.insert(0, 'src')
from scores import load_sets, resolve, assert_no_target, TARGET_ALIASES

R = 'data/raw/persister/'
MAT = R + 'GSE150949_pooled_watermelon.count.matrix.csv.gz'
META = R + 'GSE150949_pooled_watermelon.metadata.matrix.csv.gz'
CHUNK = 1500
MIN_CELLS = 100
MIN_DET = .05
SETS = load_sets()
IFNG, IFNA = SETS['HALLMARK_IFNG'], SETS['HALLMARK_IFNA']
assert_no_target(IFNG, 'HALLMARK_IFNG'); assert_no_target(IFNA, 'HALLMARK_IFNA')
GATE = ['MKI67', 'TOP2A', 'CCNB1']
EFFLUX = ['ABCB1', 'ABCG2', 'ABCC1']
IFN_CTRL = ['IFIT1', 'ISG15', 'STAT1', 'B2M']
PERS = ['AXL', 'NGFR', 'ALDH1A3', 'KDM5A']
WATCH = ['MVP', 'TEP1', 'PARP4'] + GATE + EFFLUX + IFN_CTRL + PERS


MM = 'data/processed/watermelon.memmap'


def build():
    """One streaming pass over the CSV into a float32 memmap on disk."""
    import os
    if os.path.exists(MM + '.genes.npy'):
        genes = np.load(MM + '.genes.npy', allow_pickle=False)
        cells = np.load(MM + '.cells.npy', allow_pickle=False)
        M = np.memmap(MM, dtype=np.float32, mode='r', shape=(len(genes), len(cells)))
        return M, pd.Index(genes), pd.Index(cells)
    genes, cells, parts, n = [], None, [], 0
    tmp = open(MM, 'wb')
    for ch in pd.read_csv(MAT, index_col=0, chunksize=CHUNK):
        if cells is None:
            cells = ch.columns
        ch.values.astype(np.float32).tofile(tmp)
        genes.extend(ch.index.tolist()); n += len(ch)
        print('  rows', n, flush=True)
    tmp.close()
    np.save(MM + '.genes.npy', np.array(genes, dtype='U40'))
    np.save(MM + '.cells.npy', np.array(cells.tolist(), dtype='U40'))
    M = np.memmap(MM, dtype=np.float32, mode='r', shape=(len(genes), len(cells)))
    return M, pd.Index(genes), pd.Index(cells)


def zsc(x):
    s = x.std(ddof=1)
    return (x - x.mean()) / (s if s > 0 else 1)


def main():
    meta = pd.read_csv(META, index_col=0)
    M, genes, cells = build()
    print('matrix', M.shape, flush=True)
    tot = pd.Series(np.zeros(M.shape[1], dtype=np.float64), index=cells)
    for a in range(0, M.shape[0], CHUNK):
        tot += M[a:a + CHUNK].sum(axis=0)
    rows = {g: np.asarray(M[genes.get_loc(g)]) for g in genes.intersection(set(IFNG) | set(IFNA))}
    meta = meta.loc[tot.index]
    treated = meta.sample_type.isin(['cycling', 'non-cycling']).values
    line = meta.cell_line.values
    models = [m for m in pd.unique(line)
              if ((line == m) & treated).sum() >= MIN_CELLS and ((line == m) & ~treated).sum() >= MIN_CELLS]
    extra = [(m, int(((line == m) & treated).sum()), int(((line == m) & ~treated).sum())) for m in pd.unique(line) if m not in models]
    print('usable models', models, '| excluded (treated, naive):', extra, flush=True)
    cp = 1e4 / tot.values

    def score(gs):
        g = resolve(gs, pd.Index(rows))
        assert_no_target(g, 'score input')
        M = np.vstack([np.log1p(rows[x] * cp) for x in g])
        M = (M - M.mean(axis=1, keepdims=True)) / np.where(M.std(axis=1, ddof=1, keepdims=True) > 0, M.std(axis=1, ddof=1, keepdims=True), 1)
        return M.mean(axis=0), len(g)

    sg, ng = score(IFNG); sa, na = score(IFNA)
    print('interferon scores from', ng, 'IFNG and', na, 'IFNA genes (MVP excluded)', flush=True)

    D = {}
    for m in models:
        w = line == m
        t = treated[w].astype(float)
        X0 = np.column_stack([np.ones(w.sum()), t])
        X1 = np.column_stack([np.ones(w.sum()), zsc(sg[w]), zsc(sa[w]), t])
        D[m] = dict(w=w, P0=np.linalg.pinv(X0), P1=np.linalg.pinv(X1), cyc=meta.sample_type.values[w])

    out = {m: {} for m in models}
    det = {m: {} for m in models}
    for a in range(0, M.shape[0], CHUNK):
        ch = pd.DataFrame(np.asarray(M[a:a + CHUNK]), index=genes[a:a + CHUNK])
        L = np.log1p(ch.values * cp)
        for m in models:
            w = D[m]['w']; Y = L[:, w]
            d = (Y > 0).mean(axis=1)
            b0 = Y @ D[m]['P0'].T
            b1 = Y @ D[m]['P1'].T
            for g, raw, res, dd in zip(ch.index, b0[:, 1], b1[:, 3], d):
                out[m][g] = (float(raw), float(res)); det[m][g] = float(dd)
    res = {}
    for m in models:
        d = pd.DataFrame(out[m], index=['raw', 'resid']).T
        d['det'] = pd.Series(det[m])
        d = d[d.det >= MIN_DET]
        d['pct_raw'] = d.raw.rank(pct=True) * 100
        d['pct_resid'] = d.resid.rank(pct=True) * 100
        res[m] = d
        print(f'\n-- {m}: genes {len(d)}, treated {int(D[m]["w"].sum() and (treated[D[m]["w"]]).sum())}, naive {int((~treated[D[m]["w"]]).sum())}', flush=True)
        print(d.reindex(WATCH).round(3).to_string())
    pd.to_pickle(res, 'data/processed/persister_watermelon.pkl')

    def tally(gene, col='pct_raw', hi=True):
        v = [res[m][col].get(gene, np.nan) for m in models]
        n = sum(1 for x in v if (x >= 90 if hi else x <= 10) and np.isfinite(x))
        return [None if not np.isfinite(x) else round(x, 1) for x in v], n

    need = max(1, int(np.ceil(2 / 3 * len(models))))
    gate = {g: tally(g, 'pct_raw', hi=False) for g in GATE}
    gate_pass = all(v[1] >= need for v in gate.values())
    print('\nGATE (proliferation genes must fall):', 'PASS' if gate_pass else 'FAIL', gate, f'need {need} of {len(models)}', flush=True)

    mvp_raw, n_raw = tally('MVP', 'pct_raw')
    mvp_res, n_res = tally('MVP', 'pct_resid')
    down, n_down = tally('MVP', 'pct_raw', hi=False)
    if not gate_pass:
        label = 'UNINFORMATIVE'
    elif n_raw >= need:
        label = 'PERSISTER MARKER'
    elif n_down >= need:
        label = 'DOWN IN PERSISTERS'
    else:
        label = 'NOT A PERSISTER MARKER'
    ifn = 'INTERFERON-EXPLAINED' if (label == 'PERSISTER MARKER' and n_res < need) else ('INDEPENDENT OF INTERFERON' if label == 'PERSISTER MARKER' else 'n/a')
    print(f'\nLABEL {label} | MVP pct_raw {mvp_raw} ({n_raw}/{len(models)} >=90) | pct_resid {mvp_res} ({n_res}) | interferon verdict: {ifn}', flush=True)
    print('\ncomparators (pct_raw per model, count >=90th):')
    for g in EFFLUX + IFN_CTRL + PERS + ['TEP1', 'PARP4']:
        v, n = tally(g); print(' ', g, v, n, flush=True)
    json.dump(dict(models=models, excluded=extra, need=need, gate={k: v[0] for k, v in gate.items()}, gate_pass=gate_pass,
                   label=label, interferon=ifn, mvp_raw=mvp_raw, mvp_resid=mvp_res,
                   comparators={g: tally(g)[0] for g in EFFLUX + IFN_CTRL + PERS + ['TEP1', 'PARP4']}),
              open('results/persister_primary.json', 'w'), indent=1, default=float)


if __name__ == '__main__':
    main()
