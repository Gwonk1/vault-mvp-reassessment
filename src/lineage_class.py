"""Is the MVP lineage pattern just epithelial identity?
Pre-registered in LINEAGE_CLASS_PREREGISTRATION.md. Classification fixed there."""
import pandas as pd, numpy as np, json

CLASS = {
    **{k: 'epithelial' for k in ['kidney','pancreas','gastric','colorectal','upper_aerodigestive',
                                 'skin','urinary_tract','lung','ovary','breast','liver','esophagus',
                                 'prostate','uterus']},
    **{k: 'haematopoietic' for k in ['blood','lymphocyte','plasma_cell']},
    **{k: 'mesenchymal' for k in ['bone','soft_tissue']},
    'central_nervous_system': 'neural',
}

M = pd.read_parquet('data/processed/prot/ccle_broad_2019.parquet')
clin = pd.read_parquet('data/processed/prot/ccle_broad_2019.clin.parquet').set_index('sampleId')
lines = M.columns.intersection(clin.index)
M, lin = M[lines], clin.loc[lines, 'LINEAGE'].astype(str)
Z = M.sub(M.mean(axis=1), axis=0).div(M.std(axis=1).replace(0, np.nan), axis=0)
counts = lin.value_counts(); keep = counts[counts >= 5].index

def lineage_means(g):
    if g not in Z.index: return None
    z = Z.loc[g]
    if isinstance(z, pd.DataFrame): z = z.mean(axis=0)
    return z.groupby(lin).mean().reindex(keep).dropna()

# --- GATE ---
gate, gd = False, {}
for mk in ['EPCAM', 'CDH1', 'KRT8']:
    s = lineage_means(mk)
    if s is None: gd[mk] = 'absent'; continue
    cls = pd.Series({k: CLASS.get(k) for k in s.index})
    e, h = s[cls == 'epithelial'].mean(), s[cls == 'haematopoietic'].mean()
    gd[mk] = {'epithelial': round(float(e), 3), 'haematopoietic': round(float(h), 3),
              'diff': round(float(e - h), 3)}
    if e - h >= 1.0: gate = True
print('GATE', 'PASS' if gate else 'FAIL', json.dumps(gd), flush=True)

# --- PRIMARY ---
mvp = lineage_means('MVP')
cls = pd.Series({k: CLASS.get(k) for k in mvp.index})
groups = {c: mvp[cls == c].values for c in ['epithelial', 'haematopoietic', 'mesenchymal']}
allv = np.concatenate(list(groups.values()))
grand = allv.mean()
ss_between = sum(len(v) * (v.mean() - grand) ** 2 for v in groups.values())
ss_total = ((allv - grand) ** 2).sum()
eta2 = ss_between / ss_total

epi = mvp[cls == 'epithelial']
spread = float(epi.max() - epi.min())

if not gate:                        verdict = 'UNINFORMATIVE (gate failed)'
elif eta2 >= 0.50 and spread < 1.0: verdict = 'H1 WINS - pattern is tissue class'
elif spread >= 1.5:                 verdict = 'H1 LOSES - structure survives within epithelium'
else:                               verdict = 'PARTIAL - no functional hypothesis promoted'

print(f'\nclass means: ' + '  '.join(f'{c}={v.mean():+.3f}(k={len(v)})' for c, v in groups.items()))
print(f'eta-squared (class) = {eta2:.3f}')
print(f'within-epithelial spread = {spread:.3f} z  '
      f'({epi.idxmax()} {epi.max():+.3f} .. {epi.idxmin()} {epi.min():+.3f})')
print(f'neural (CNS, descriptive) = {mvp.get("central_nervous_system", float("nan")):+.3f}')
print('VERDICT:', verdict, flush=True)
print('\nepithelial lineages ranked:'); print(epi.sort_values(ascending=False).round(3).to_string())

json.dump({'gate': gate, 'gate_detail': gd, 'eta2_class': round(float(eta2), 4),
           'within_epithelial_spread': round(spread, 4), 'verdict': verdict,
           'class_means': {c: round(float(v.mean()), 4) for c, v in groups.items()},
           'cns_z': round(float(mvp.get('central_nervous_system', np.nan)), 4),
           'epithelial_ranked': {k: round(float(v), 4) for k, v in
                                 epi.sort_values(ascending=False).items()}},
          open('results/lineage_class.json', 'w'), indent=1)
