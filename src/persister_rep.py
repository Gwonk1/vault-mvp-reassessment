"""Replication arm: GSE149383 (Aissa et al.). Same estimand as the primary, different lab and drugs."""
import json, sys
import numpy as np, pandas as pd
sys.path.insert(0, 'src')
from scores import load_sets, resolve, assert_no_target
from persister import GATE, EFFLUX, IFN_CTRL, PERS, WATCH, MIN_DET, zsc

R = 'data/raw/persister/g149/'
ARMS = {
    'M14_melanoma_vem_D3': ('GSM3972655_M14Day0.dge.txt.gz', 'GSM3972656_M14Day3_Vem.dge.txt.gz'),
    'PC9_erl_D11': ('GSM3972657_D0.dge.txt.gz', 'GSM3972662_D11.dge.txt.gz'),
    'PC9_erl_D19_vs_DMSO': ('GSM3972672_D19DMSO.dge.txt.gz', 'GSM3972673_D19_ERL.dge.txt.gz'),
}
S = load_sets()


def load(f):
    d = pd.read_csv(R + f, sep='\t', index_col=0)
    d = d[~d.index.duplicated()]
    return d


def main():
    out = {}
    for name, (c, t) in ARMS.items():
        A, B = load(c), load(t)
        g = A.index.intersection(B.index)
        A, B = A.loc[g], B.loc[g]
        V = np.hstack([A.values, B.values]).astype(np.float32)
        treat = np.r_[np.zeros(A.shape[1]), np.ones(B.shape[1])]
        tot = V.sum(0)
        ok = tot > 0
        if (~ok).any():
            print(' dropping', int((~ok).sum()), 'cells with zero counts', flush=True)
        V, treat, tot = V[:, ok], treat[ok], tot[ok]
        L = np.log1p(V * (1e4 / tot))
        det = (L > 0).mean(axis=1)
        keep = det >= MIN_DET
        L, gg = L[keep], g[keep]

        def sc(key):
            idx = [gg.get_loc(x) for x in resolve(S[key], gg)]
            assert_no_target([gg[i] for i in idx], key)
            M = L[idx]
            sd = M.std(axis=1, ddof=1, keepdims=True)
            return ((M - M.mean(axis=1, keepdims=True)) / np.where(sd > 0, sd, 1)).mean(axis=0), len(idx)

        sg, ng = sc('HALLMARK_IFNG'); sa, na = sc('HALLMARK_IFNA')
        X0 = np.column_stack([np.ones(len(treat)), treat])
        X1 = np.column_stack([np.ones(len(treat)), zsc(sg), zsc(sa), treat])
        b0 = L @ np.linalg.pinv(X0).T
        b1 = L @ np.linalg.pinv(X1).T
        d = pd.DataFrame({'raw': b0[:, 1], 'resid': b1[:, 3], 'det': det[keep]}, index=gg)
        d['pct_raw'] = d.raw.rank(pct=True) * 100
        d['pct_resid'] = d.resid.rank(pct=True) * 100
        out[name] = d
        print(f'\n-- {name}: control {A.shape[1]} cells, treated {B.shape[1]}, genes {len(d)}, IFNG {ng} IFNA {na}', flush=True)
        print(d.reindex(WATCH).round(3).to_string(), flush=True)
    pd.to_pickle(out, 'data/processed/persister_replication.pkl')
    res = {}
    for g in WATCH:
        res[g] = {k: (None if g not in v.index else round(float(v.pct_raw[g]), 1)) for k, v in out.items()}
    res_r = {g: {k: (None if g not in v.index else round(float(v.pct_resid[g]), 1)) for k, v in out.items()} for g in ['MVP']}
    print('\npct_raw by arm:')
    for g, v in res.items():
        print(' ', g, v, flush=True)
    print('MVP pct_resid:', res_r['MVP'], flush=True)
    json.dump(dict(pct_raw=res, mvp_pct_resid=res_r['MVP'],
                   n={k: [int(v.shape[0])] for k, v in out.items()}),
              open('results/persister_replication.json', 'w'), indent=1, default=float)


if __name__ == '__main__':
    main()
