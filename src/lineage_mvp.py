"""Is MVP's immunoglobulin co-expression caused by plasma cells being MVP-rich?
Pre-registered in ADRENAL_PREREGISTRATION.md (commit 64f8ce8). Cell lines carry
no immune infiltrate, so lineage-stratified protein is the discriminator."""
import pandas as pd, numpy as np, json

M = pd.read_parquet('data/processed/prot/ccle_broad_2019.parquet')
clin = pd.read_parquet('data/processed/prot/ccle_broad_2019.clin.parquet').set_index('sampleId')
lines = M.columns.intersection(clin.index)
M, lin = M[lines], clin.loc[lines, 'LINEAGE'].astype(str)
print(f'proteins {M.shape[0]} lines {M.shape[1]}', flush=True)

Z = M.sub(M.mean(axis=1), axis=0).div(M.std(axis=1).replace(0, np.nan), axis=0)
counts = lin.value_counts()
keep = counts[counts >= 5].index
print(f'lineages with n>=5: {len(keep)}  (n plasma_cell = {counts.get("plasma_cell", 0)})', flush=True)

def lineage_means(gene):
    if gene not in Z.index: return None
    z = Z.loc[gene]
    if isinstance(z, pd.DataFrame): z = z.mean(axis=0)
    return z.groupby(lin).mean().reindex(keep).dropna().sort_values(ascending=False)

# --- GATE: plasma-cell identity must be recoverable ---
gate, gate_detail = False, {}
for mk in ['MZB1', 'XBP1', 'SDC1', 'PRDM1', 'DERL3']:
    s = lineage_means(mk)
    if s is None:
        gate_detail[mk] = 'absent from matrix'; continue
    rank = list(s.index).index('plasma_cell') + 1 if 'plasma_cell' in s.index else None
    gate_detail[mk] = {'plasma_cell_rank': rank, 'n_lineages': len(s),
                       'top': s.index[0], 'pc_z': round(float(s.get('plasma_cell', np.nan)), 3)}
    if rank == 1: gate = True
print('GATE', 'PASS' if gate else 'FAIL', json.dumps(gate_detail, default=str), flush=True)

# --- PRIMARY ---
mvp = lineage_means('MVP')
rank = list(mvp.index).index('plasma_cell') + 1
n = len(mvp)
median_rank = (n + 1) / 2
if not gate:            verdict = 'UNINFORMATIVE (gate failed)'
elif rank <= 3:         verdict = 'INFILTRATE SUPPORTED'
elif rank >= median_rank: verdict = 'INFILTRATE NOT SUPPORTED - kill condition met'
else:                   verdict = 'EQUIVOCAL'

print(f'\nMVP: plasma_cell rank {rank} of {n} (median rank {median_rank}) '
      f'z={mvp["plasma_cell"]:+.3f}', flush=True)
print('VERDICT:', verdict, flush=True)
print('\nfull MVP lineage ranking (mean z):')
print(mvp.round(3).to_string(), flush=True)

json.dump({'gate': gate, 'gate_detail': gate_detail, 'verdict': verdict,
           'mvp_plasma_cell_rank': rank, 'n_lineages': n, 'median_rank': median_rank,
           'mvp_plasma_cell_z': round(float(mvp['plasma_cell']), 4),
           'n_plasma_cell_lines': int(counts.get('plasma_cell', 0)),
           'mvp_lineage_z': {k: round(float(v), 4) for k, v in mvp.items()}},
          open('results/lineage_mvp.json', 'w'), indent=1)
