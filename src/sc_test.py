"""Single-cell verdict. Within-patient models in a named compartment, combined across patients.

Usage: sc_test.py kim|jerby [malignant|myeloid]
"""
import json, sys
import numpy as np, pandas as pd, scipy.sparse as sp
from scipy import stats
sys.path.insert(0, 'src')
from scores import load_sets, resolve, assert_no_target, TARGET_ALIASES
from models import reml, label, fmt, SETS

MIN_CELLS, MIN_DET = 50, .01


def load_kim(comp, subtypes=('Malignant cells',), origins=None):
    M = sp.load_npz('data/processed/kim_lognorm.npz').tocsc()
    g = pd.read_parquet('data/processed/kim_genes.parquet').gene.values
    c = pd.read_parquet('data/processed/kim_cells.parquet')
    keep = np.array(c.Cell_subtype.isin(subtypes).values if comp == 'malignant' else (c.Cell_type == 'Myeloid cells').values, dtype=bool)
    if origins:
        keep &= c.Sample_Origin.isin(origins).values
    return M[:, np.where(keep)[0]], g, c.Sample.values[keep], np.log1p(c.libsize.values[keep])


def load_jerby(comp):
    a = pd.read_csv('data/raw/sc/GSE115978_cell.annotations.csv.gz').set_index('cells')
    t = pd.read_csv('data/raw/sc/GSE115978_tpm.csv.gz', index_col=0)
    a = a.loc[t.columns]
    keep = (a['cell.types'] == ('Mal' if comp == 'malignant' else 'Macrophage')).values
    M = sp.csc_matrix(np.log2(t.values[:, keep] + 1).astype(np.float32))
    return M, t.index.values, a.samples.values[keep], np.log1p(a['no.of.reads'].values[keep].astype(float))


def run(M, g, pat, depth, depth_cov=False, tag=''):
    M = M.tocsr()
    det = np.asarray((M > 0).mean(axis=1)).ravel()
    idx = pd.Series(np.arange(len(g)), index=g)
    idx = idx[~idx.index.duplicated()]
    uni = idx[det[idx.values] >= MIN_DET]
    assert 'MVP' in idx.index, 'MVP missing from matrix'
    print(tag, 'cells', M.shape[1], 'patients', pd.Series(pat).nunique(), 'universe', len(uni), 'MVP detection', round(det[idx['MVP']], 4), flush=True)
    sets = {k: resolve(SETS[k], uni.index) for k in ['ISG_RS', 'IFNG_GS']}
    for k, v in sets.items():
        assert_no_target(v, k)
    dropped = {k: sorted(set(SETS[k]) - set(v)) for k, v in sets.items()}
    print(' kept ISG.RS', len(sets['ISG_RS']), 'IFNG.GS', len(sets['IFNG_GS']), flush=True)
    genes = list(uni.index)
    pos = {x: i for i, x in enumerate(genes)}
    Xfull = M[uni.values, :].toarray().astype(np.float32)
    ai = np.array([pos[x] for x in sets['ISG_RS']]); ci = np.array([pos[x] for x in sets['IFNG_GS']])
    rows, per, pseudo = {}, [], []
    for p in pd.unique(pat):
        w = pat == p
        if w.sum() < MIN_CELLS:
            continue
        Y = Xfull[:, w].astype(np.float64)
        sd = Y.std(axis=1, ddof=1)
        Yz = (Y - Y.mean(axis=1, keepdims=True)) / np.where(sd > 0, sd, np.nan)[:, None]
        def sc(i):
            i = i[np.isfinite(Yz[i, 0])]
            s = Yz[i].mean(axis=0)
            return (s - s.mean()) / s.std(ddof=1)
        a, c = sc(ai), sc(ci)
        cols = [np.ones(w.sum()), a, c]
        if depth_cov:
            d = depth[w]; cols.append((d - d.mean()) / d.std(ddof=1))
        X = np.column_stack(cols)
        XtXi = np.linalg.inv(X.T @ X)
        ok = np.isfinite(Yz[:, 0])
        Z = Yz[ok]
        b = Z @ X @ XtXi
        s2 = ((Z - b @ X.T) ** 2).sum(axis=1) / (X.shape[0] - X.shape[1])
        D = pd.DataFrame({'ba': b[:, 1], 'bc': b[:, 2], 'va': s2 * XtXi[1, 1], 'vc': s2 * XtXi[2, 2],
                          'vd': s2 * (XtXi[1, 1] + XtXi[2, 2] - 2 * XtXi[1, 2])}, index=np.array(genes)[ok])
        # held-out members
        for key, ii, col in (('a', ai, 1), ('c', ci, 2)):
            for j in ii:
                if not ok[j]:
                    continue
                s = sc(ii[ii != j])
                Xh = X.copy(); Xh[:, col] = s
                Xi = np.linalg.inv(Xh.T @ Xh)
                bh = Yz[j] @ Xh @ Xi
                sh = ((Yz[j] - Xh @ bh) ** 2).sum() / (Xh.shape[0] - Xh.shape[1])
                D.loc[genes[j], ['ba', 'bc', 'va', 'vc', 'vd']] = [bh[1], bh[2], sh * Xi[1, 1], sh * Xi[2, 2], sh * (Xi[1, 1] + Xi[2, 2] - 2 * Xi[1, 2])]
        D['d'] = D.ba - D.bc
        rows[p] = D
        if ok[pos['MVP']]:
            mvp = Y[pos['MVP']]
            per.append(dict(patient=p, n=int(w.sum()), det=float((mvp > 0).mean()), rho_a=stats.spearmanr(mvp, a)[0], rho_c=stats.spearmanr(mvp, c)[0], ba=D.ba['MVP'], bc=D.bc['MVP'], d=D.d['MVP'], r_ac=float(np.corrcoef(a, c)[0, 1])))
        keepi = np.isfinite(Y.mean(axis=1))
        pseudo.append(dict(patient=p, mvp=Y[pos['MVP']].mean(), a=Y[ai].mean(), c=Y[ci].mean()))
    per = pd.DataFrame(per)
    if len(rows) < 3 or len(per) < 3:
        print(' UNUSABLE: fewer than 3 patients with enough cells', len(rows), flush=True)
        return dict(tag=tag, label='UNUSABLE', patients=len(rows), cells=int(M.shape[1])), per, pd.DataFrame({'d': []})
    print(' patients used', len(rows), 'with MVP variance', len(per), 'median cells', per.n.median(), 'median MVP detection', round(per.det.median(), 3), 'median r(ISG,IFNG)', round(per.r_ac.median(), 2), flush=True)
    # pool every gene in at least 5 patients
    cnt = pd.Series(np.concatenate([d.index.values for d in rows.values()])).value_counts()
    G = cnt[cnt >= max(5, len(rows) // 2)].index
    mats = {k: pd.concat({p: d[k] for p, d in rows.items()}, axis=1).reindex(G).values for k in ['ba', 'bc', 'd', 'va', 'vc', 'vd']}
    res = {}
    for i, x in enumerate(G):
        res[x] = reml(mats['d'][i], mats['vd'][i])[:3] + (reml(mats['ba'][i], mats['va'][i])[0], reml(mats['bc'][i], mats['vc'][i])[0])
    P = pd.DataFrame.from_dict(res, orient='index', columns=['d', 'dlo', 'dhi', 'ba', 'bc'])
    i = list(G).index('MVP')
    t = dict(ba=reml(mats['ba'][i], mats['va'][i]), bc=reml(mats['bc'][i], mats['vc'][i]), d=reml(mats['d'][i], mats['vd'][i]))
    lab = label(t['ba'][:3], t['bc'][:3], t['d'][:3])
    A = P.loc[[x for x in sets['ISG_RS'] if x in P.index]]; C = P.loc[[x for x in sets['IFNG_GS'] if x in P.index]]
    bg = P.loc[[x for x in P.index if x not in set(A.index) | set(C.index) | TARGET_ALIASES]]
    tv = t['d'][0]
    null = dict(universe=len(bg), pct_genome=float((bg.d < tv).mean() * 100), bg_q=[float(x) for x in bg.d.quantile([.1, .5, .9])],
                isg_q=[float(x) for x in A.d.quantile([.1, .5, .9])], ifng_q=[float(x) for x in C.d.quantile([.1, .5, .9])],
                auc=float(stats.mannwhitneyu(A.d, C.d).statistic / (len(A) * len(C))), pct_in_ISG=float((A.d < tv).mean() * 100), pct_in_IFNG=float((C.d < tv).mean() * 100),
                pct_ba=float((bg.ba < t['ba'][0]).mean() * 100), pct_bc=float((bg.bc < t['bc'][0]).mean() * 100))
    Rz = lambda c: np.arctanh(np.clip(per[c], -.999, .999))
    v = 1 / (per.n - 3)
    rho = {c: [float(np.tanh(x)) for x in reml(Rz(c), v)[:3]] for c in ['rho_a', 'rho_c']}
    psb = pd.DataFrame(pseudo); ps = {'n': len(psb), 'r_a': float(stats.spearmanr(psb.mvp, psb.a)[0]), 'r_c': float(stats.spearmanr(psb.mvp, psb.c)[0])}
    if len(psb) >= 6:
        Xp = np.column_stack([np.ones(len(psb))] + [(psb[k] - psb[k].mean()) / psb[k].std() for k in 'ac'])
        yp = (psb.mvp - psb.mvp.mean()) / psb.mvp.std()
        import statsmodels.api as sm
        f = sm.OLS(yp, Xp).fit(); ps.update(ba=float(f.params.iloc[1]), bc=float(f.params.iloc[2]), ci=f.conf_int().values[1:].round(3).tolist())
    sign = dict(frac_ba_pos=float((per.ba > 0).mean()), frac_bc_pos=float((per.bc > 0).mean()), frac_d_pos=float((per.d > 0).mean()))
    print(' VERDICT', lab, fmt(t), '\n null', null, '\n spearman', rho, '\n pseudobulk', ps, '\n sign', sign, flush=True)
    return dict(tag=tag, label=lab, t=fmt(t), null=null, spearman=rho, pseudobulk=ps, sign=sign, cells=int(M.shape[1]), patients=len(rows),
                mvp_detection=float(det[idx['MVP']]), dropped=dropped, kept={k: len(v) for k, v in sets.items()}), per, P


if __name__ == '__main__':
    out = {}
    which = sys.argv[1]
    if which == 'kim':
        jobs = {'kim_malignant': lambda: load_kim('malignant'),
                'kim_primary_tumor_incl_tS': lambda: load_kim('malignant', subtypes=('Malignant cells', 'tS1', 'tS2', 'tS3'), origins=['tLung', 'tL/B']),
                'kim_brain_mets': lambda: load_kim('malignant', origins=['mBrain']),
                'kim_LN_mets': lambda: load_kim('malignant', origins=['mLN']),
                'kim_myeloid': lambda: load_kim('myeloid')}
    else:
        jobs = {'jerby_malignant': lambda: load_jerby('malignant'), 'jerby_macrophage': lambda: load_jerby('myeloid')}
    for k, f in jobs.items():
        M, g, pat, dp = f()
        r, per, P = run(M, g, pat, dp, tag=k)
        out[k] = r; per.to_csv(f'results/{k}.patients.csv', index=False); P.to_parquet(f'data/processed/{k}.pooled.parquet')
        if 'malignant' in k and k in ('kim_malignant', 'jerby_malignant'):
            r2, _, _ = run(M, g, pat, dp, depth_cov=True, tag=k + '_depth_adjusted')
            out[k + '_depth_adjusted'] = r2
    json.dump(out, open(f'results/sc_{which}.json', 'w'), indent=1, default=float)
