"""Primary bulk model, calibration null, held-out members, sensitivity analyses."""
import json, os, re, sys, warnings
import numpy as np, pandas as pd
from scipy import stats
import statsmodels.api as sm
sys.path.insert(0, 'src')
from scores import load_sets, resolve, to_log, zgenes, score, assert_no_target, TARGET_ALIASES
warnings.filterwarnings('ignore', category=RuntimeWarning)

B = 'data/processed/bulk'
ICB = ['riaz', 'hugo', 'liu', 'gide', 'vanallen', 'imvigor', 'jung']
TCGA = ['luad', 'lusc', 'skcm', 'paad', 'lihc', 'thca']
RESP1 = {'true','yes','responder','cb','dcb','clinical benefit','1','r'}
RESP0 = {'false','no','non-responder','ncb','ndb','nonresponder','no clinical benefit','0','nr'}
SETS = load_sets()
est = json.load(open('data/genesets/estimate.json'))
mcp = pd.read_csv('data/raw/cov/mcp_genes.txt', sep='\t')
pop = lambda *n: mcp[mcp['Cell population'].isin(n)]['HUGO symbols'].tolist()
EXCL = set(SETS['ISG_RS']) | set(SETS['IFNG_GS']) | TARGET_ALIASES
COV = {'purity': [g for g in est['stromal_signature'] + est['immune_signature'] if g not in EXCL],
       'myeloid': [g for g in pop('Monocytic lineage') if g not in EXCL],
       'lymphoid': [g for g in pop('T cells', 'CD8 T cells', 'Cytotoxic lymphocytes', 'NK cells', 'B lineage') if g not in EXCL]}
COVGENES = set(sum(COV.values(), []))


def load(name):
    m = pd.read_parquet(f'{B}/{name}.expr.parquet')
    m = m[~m.index.duplicated()]
    note = ''
    clin = None
    if os.path.exists(f'{B}/{name}.clin.parquet'):
        clin = pd.read_parquet(f'{B}/{name}.clin.parquet').set_index('sampleId')
    keep = list(m.columns)
    if clin is not None:
        clin = clin.reindex(m.columns)
        if 'SAMPLE_TREATMENT' in clin and clin.SAMPLE_TREATMENT.notna().any() and name not in TCGA:
            vals = clin.SAMPLE_TREATMENT.astype(str).str.lower()
            pre = vals.str.contains(r'^pre|before|baseline|naive')
            note += f'treatment {vals.value_counts().to_dict()}; '
            keep = list(clin.index[pre])
        elif name in TCGA:
            keep = [s for s in keep if re.search(r'-01$', s)]
        else:
            note += 'no treatment field, all samples used; '
        c = clin.loc[keep]
        keep = list(c[~c.patientId.duplicated()].index)
    m = m[keep].dropna(how='all')
    m = m[m.notna().mean(axis=1) > .95]
    m, u = to_log(m)
    return m.fillna(m.mean()), clin.loc[keep] if clin is not None else None, note + u


def fit_all(Y, X):
    """OLS of each row of Y on design X. Returns dict of beta, cov diag terms per gene."""
    XtXi = np.linalg.inv(X.T @ X)
    b = Y @ X @ XtXi
    res = Y - b @ X.T
    df = X.shape[0] - X.shape[1]
    s2 = (res ** 2).sum(axis=1) / df
    return b, s2, XtXi, df


def reml(y, v):
    y, v = np.asarray(y, float), np.asarray(v, float)
    ok = np.isfinite(y) & np.isfinite(v) & (v > 0)
    y, v = y[ok], v[ok]
    k = len(y)
    if k < 2:
        return (y[0] if k else np.nan, np.nan, np.nan, np.nan, 0.0, k)
    t2 = max(0.0, np.var(y, ddof=1) - v.mean())
    for _ in range(200):
        w = 1 / (v + t2)
        mu = (w * y).sum() / w.sum()
        new = max(0.0, (w ** 2 * ((y - mu) ** 2 - v)).sum() / (w ** 2).sum() + 1 / w.sum())
        if abs(new - t2) < 1e-8:
            t2 = new; break
        t2 = new
    w = 1 / (v + t2)
    mu = (w * y).sum() / w.sum()
    q = (w * (y - mu) ** 2).sum() / (k - 1)
    se = np.sqrt(max(q, 1e-12) / w.sum())
    h = stats.t.ppf(.975, k - 1) * se
    return mu, mu - h, mu + h, se, t2, k


def label(bi, bg, d):
    """Pre-registered outcome label. Each arg = (est, lo, hi)."""
    sig = lambda x: x[1] > 0 or x[2] < 0
    if bi[0] >= .10 and sig(bi) and d[0] > 0 and sig(d): return 'CHRONIC'
    if bg[0] >= .10 and sig(bg) and d[0] < 0 and sig(d): return 'ACUTE'
    if bi[0] <= -.10 and bg[0] <= -.10 and sig(bi) and sig(bg): return 'ANTI'
    none = lambda x: abs(x[0]) < .10 or not sig(x)
    if none(bi) and none(bg): return 'NEITHER'
    return 'BOTH/UNRESOLVED'


def cohort(name, cov=True, sets=('ISG_RS', 'IFNG_GS'), extra=None, drop_expr=True):
    m, clin, note = load(name)
    floor = np.nanmin(m.values)
    expressed = (m > floor + 1e-9).mean(axis=1) >= .5
    mm = m[expressed & (m.std(axis=1) > 0)]
    z = zgenes(mm).dropna()
    z1 = z.loc[[g for g in z.index if g not in TARGET_ALIASES]]  # scoring input is target free
    n = z.shape[1]
    a, ga = score(z1, SETS[sets[0]], sets[0]); c, gc = score(z1, SETS[sets[1]], sets[1])
    Z = lambda s: ((s - s.mean()) / s.std(ddof=1)).values
    cols = {'a': Z(a), 'c': Z(c)}
    if cov:
        for k, gs in COV.items():
            cols[k] = Z(score(z1, gs, k)[0])
    if extra is not None:
        cols.update(extra(clin, z.columns))
    X = np.column_stack([np.ones(n)] + list(cols.values()))
    Y = z.values
    b, s2, XtXi, df = fit_all(Y, X)
    D = pd.DataFrame({'ba': b[:, 1], 'bc': b[:, 2],
                      'va': s2 * XtXi[1, 1], 'vc': s2 * XtXi[2, 2],
                      'vd': s2 * (XtXi[1, 1] + XtXi[2, 2] - 2 * XtXi[1, 2])}, index=z.index)
    # held-out members: each member vs its own set with itself removed
    for setk, col in ((sets[0], 'a'), (sets[1], 'c')):
        mem = resolve(SETS[setk], z.index)
        for g in mem:
            s = z1.loc[[x for x in mem if x != g]].mean(axis=0)
            Xh = X.copy(); Xh[:, 1 if col == 'a' else 2] = Z(s)
            bh, s2h, XiH, _ = fit_all(z.loc[[g]].values, Xh)
            D.loc[g, ['ba', 'bc', 'va', 'vc', 'vd']] = [bh[0, 1], bh[0, 2], s2h[0] * XiH[1, 1], s2h[0] * XiH[2, 2],
                                                        s2h[0] * (XiH[1, 1] + XiH[2, 2] - 2 * XiH[1, 2])]
    vifs = {}
    for j, k in enumerate(cols):
        o = np.delete(X, j + 1, axis=1)
        r = X[:, j + 1] - o @ np.linalg.lstsq(o, X[:, j + 1], rcond=None)[0]
        vifs[k] = float((X[:, j + 1] ** 2).sum() / (r ** 2).sum()) if False else float(((X[:, j + 1] - X[:, j + 1].mean()) ** 2).sum() / (r ** 2).sum())
    D['d'] = D.ba - D.bc
    return D, dict(n=n, note=note, vif=vifs, kept_a=len(ga), kept_c=len(gc), r_ac=float(np.corrcoef(cols['a'], cols['c'])[0, 1])), (z, clin, cols)


def pool(res, target='MVP', min_k=3):
    genes = pd.Series(np.concatenate([d.index.values for d in res.values()])).value_counts()
    genes = genes[genes >= min_k].index
    ba = pd.concat({k: d.ba for k, d in res.items()}, axis=1).reindex(genes)
    bc = pd.concat({k: d.bc for k, d in res.items()}, axis=1).reindex(genes)
    va = pd.concat({k: d.va for k, d in res.items()}, axis=1).reindex(genes)
    vc = pd.concat({k: d.vc for k, d in res.items()}, axis=1).reindex(genes)
    vd = pd.concat({k: d.vd for k, d in res.items()}, axis=1).reindex(genes)
    dd = ba - bc
    rows = {}
    for i, g in enumerate(genes):
        y = dd.values[i]; v = vd.values[i]
        rows[g] = reml(y, v)[:3] + reml(ba.values[i], va.values[i])[:1] + reml(bc.values[i], vc.values[i])[:1]
    P = pd.DataFrame.from_dict(rows, orient='index', columns=['d', 'dlo', 'dhi', 'ba', 'bc'])
    t = {}
    if target in genes:
        i = list(genes).index(target)
        t = dict(ba=reml(ba.values[i], va.values[i]), bc=reml(bc.values[i], vc.values[i]), d=reml(dd.values[i], vd.values[i]))
    return P, t


def null_report(P, t, prefix=''):
    a, c = set(resolve(SETS['ISG_RS'], P.index)), set(resolve(SETS['IFNG_GS'], P.index))
    bg = P.loc[[g for g in P.index if g not in a | c | COVGENES | TARGET_ALIASES]]
    tv = t['d'][0]
    A, C = P.loc[sorted(a)].d, P.loc[sorted(c)].d
    auc = stats.mannwhitneyu(A, C).statistic / (len(A) * len(C))
    return dict(universe=len(bg), pct_genome=float((bg.d < tv).mean() * 100), bg_median=float(bg.d.median()),
                bg_q=[float(x) for x in bg.d.quantile([.1, .5, .9])],
                isg_q=[float(x) for x in A.quantile([.1, .5, .9])], ifng_q=[float(x) for x in C.quantile([.1, .5, .9])],
                pct_in_ISG=float((A < tv).mean() * 100), pct_in_IFNG=float((C < tv).mean() * 100), auc_members=float(auc),
                pct_ba=float((bg.ba < t['ba'][0]).mean() * 100), pct_bc=float((bg.bc < t['bc'][0]).mean() * 100))


def fmt(t):
    return {k: [round(float(x), 3) for x in v[:3]] + [round(float(v[4]), 4), v[5]] for k, v in t.items()}


def analyze(names, **kw):
    res, meta, ctx = {}, {}, {}
    for n in names:
        if not os.path.exists(f'{B}/{n}.expr.parquet'):
            continue
        D, mt, c = cohort(n, **kw)
        res[n], meta[n], ctx[n] = D, mt, c
    P, t = pool(res)
    lab = label(t['ba'][:3], t['bc'][:3], t['d'][:3])
    return dict(res=res, meta=meta, ctx=ctx, P=P, t=t, label=lab, null=null_report(P, t))


if __name__ == '__main__':
    out = {}
    prim = analyze(ICB)
    print('COHORTS'); [print(' ', k, v) for k, v in prim['meta'].items()]
    print('\nPRIMARY', prim['label'], fmt(prim['t'])); print(prim['null'])
    per = pd.DataFrame({k: d.loc['MVP', ['ba', 'bc', 'd', 'va', 'vc', 'vd']] for k, d in prim['res'].items()}).T.astype(float)
    per['n'] = [prim['meta'][k]['n'] for k in per.index]; print(per.round(3))
    out['primary'] = dict(label=prim['label'], t=fmt(prim['t']), null=prim['null'], meta=prim['meta'], per=per.to_dict('index'))
    prim['P'].to_parquet('data/processed/primary_pooled.parquet')

    sens = {'unadjusted': dict(cov=False), 'hallmark_IFNA_vs_IFNG': dict(sets=('HALLMARK_IFNA', 'HALLMARK_IFNG'))}
    SETS['ISG24'] = [g for g in SETS['ISG_RS'] if g in set(SETS['HALLMARK_IFNG']) | {'MVP'}]
    sens['ISG24_vs_IFNG'] = dict(sets=('ISG24', 'IFNG_GS'))
    out['sens'] = {}
    for k, kw in sens.items():
        r = analyze(ICB, **kw); out['sens'][k] = dict(label=r['label'], t=fmt(r['t']), null=r['null'])
        print('\nSENS', k, r['label'], fmt(r['t'])); print(r['null'])
    out['loo'] = {}
    for drop in prim['res']:
        rr = {k: v for k, v in prim['res'].items() if k != drop}
        P, t = pool(rr); out['loo'][drop] = dict(label=label(t['ba'][:3], t['bc'][:3], t['d'][:3]), t=fmt(t), pct=null_report(P, t)['pct_genome'])
        print('drop', drop, out['loo'][drop])

    # ratio, stratification, response
    rows = []
    for n, (z, clin, cols) in prim['ctx'].items():
        y = z.loc['MVP'].values
        ratio = cols['a'] - cols['c']
        ratio = (ratio - ratio.mean()) / ratio.std(ddof=1)
        X = sm.add_constant(np.column_stack([ratio, cols['purity'], cols['myeloid'], cols['lymphoid']]))
        f = sm.OLS(y, X).fit()
        hi = (cols['a'] >= np.quantile(cols['a'], 2 / 3)) & (cols['c'] <= np.quantile(cols['c'], 1 / 3))
        strat = (float(y[hi].mean() - y[~hi].mean()), int(hi.sum()))
        lr = dict(cohort=n, ratio_b=f.params[1], ratio_v=f.bse[1] ** 2, strat_diff=strat[0], strat_n=strat[1], resp_b=np.nan, resp_v=np.nan, lrt_p=np.nan, resp_n=np.nan)
        if clin is not None:
            col = next((c for c in ['RESPONDER', 'CLINICAL_BENEFIT'] if c in clin), None)
            if col:
                def code(v):
                    v = str(v).strip().lower()
                    if v in RESP1 or v.startswith('resp'): return 1
                    if v in RESP0 or v.startswith('non'): return 0
                    return np.nan
                r = clin[col].map(code).reindex(z.columns)
                ok = r.notna().values
                if ok.sum() >= 15 and 3 <= r[ok].sum() <= ok.sum() - 3:
                    try:
                        X0 = sm.add_constant(cols['a'][ok]); X1 = sm.add_constant(np.column_stack([cols['a'][ok], y[ok]]))
                        m0 = sm.Logit(r[ok].values, X0).fit(disp=0); m1 = sm.Logit(r[ok].values, X1).fit(disp=0)
                        Xm = sm.add_constant(y[ok]); mm = sm.Logit(r[ok].values, Xm).fit(disp=0)
                        lr.update(resp_b=mm.params[1], resp_v=mm.bse[1] ** 2, lrt_p=float(stats.chi2.sf(2 * (m1.llf - m0.llf), 1)), resp_n=int(ok.sum()))
                    except Exception as e:
                        print(n, 'logit failed', e)
        rows.append(lr)
    X = pd.DataFrame(rows).set_index('cohort'); print(X.round(3))
    out['ratio_meta'] = [float(v) for v in reml(X.ratio_b, X.ratio_v)[:3]]
    Xr = X.dropna(subset=['resp_b'])
    out['resp_meta'] = [float(v) for v in reml(Xr.resp_b, Xr.resp_v)[:3]] if len(Xr) >= 2 else None
    out['cohort_extra'] = X.to_dict('index')
    print('ratio meta', out['ratio_meta'], 'response meta (log OR per SD)', out['resp_meta'])

    # TCGA, exploratory
    out['tcga'] = {}
    for n in TCGA:
        if not os.path.exists(f'{B}/{n}.expr.parquet'): continue
        D, mt, c = cohort(n)
        t = dict(ba=D.ba['MVP'], bc=D.bc['MVP'], d=D.d['MVP'], se_d=float(np.sqrt(D.vd['MVP'])), n=mt['n'], vif=mt['vif'],
                 pct=float((D.d[[g for g in D.index if g not in EXCL | COVGENES]] < D.d['MVP']).mean() * 100))
        out['tcga'][n] = t; print('TCGA', n, {k: (round(v, 3) if isinstance(v, float) else v) for k, v in t.items() if k != 'vif'}, 'r_ac', round(mt['r_ac'], 2))
    json.dump(out, open('results/bulk.json', 'w'), indent=1, default=float)
