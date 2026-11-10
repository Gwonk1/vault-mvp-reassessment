#!/usr/bin/env python3
"""PAPSS2 class control. Registered at f6b455c (PAPSS2_PREREGISTRATION.md) before any value read.

Procedure (declared before being pointed at anything): for a seed S, take the N genes whose own
51-tissue profile is most similar to S's, and ask where rho(MVP, S) falls in the distribution of
rho(MVP, g) over that matched set.

Gate:    S = PARP4 must exceed the 95th percentile of its matched null at N=200, else GATE-FAILED.
Primary: S = PAPSS2. STRUCK at or below the 75th pct; NOT STRUCK above the 95th; else INDETERMINATE.
"""
import csv, json
from scipy.stats import spearmanr

TSV = 'data/raw/tissue/rna_tissue_consensus.tsv'
OUT = 'results/papss2.json'
MIN_NTPM, MIN_TISSUES = 1.0, 5          # identical to src/sulfate.py, so §107 and §108 compare
NS = [200, 500]

expr = {}
with open(TSV) as fh:
    for r in csv.DictReader(fh, delimiter='\t'):
        expr.setdefault(r['Gene name'], {})[r['Tissue']] = float(r['nTPM'])
tissues = sorted({t for v in expr.values() for t in v})
assert len(tissues) == 51, len(tissues)

def vec(sym):
    d = expr[sym]
    return [d.get(t, 0.0) for t in tissues]

expressed = [g for g, d in expr.items()
             if sum(1 for t in tissues if d.get(t, 0.0) >= MIN_NTPM) >= MIN_TISSUES
             and len(d) == len(tissues)]
print(f"  {len(expr)} symbols, {len(tissues)} tissues, {len(expressed)} expressed by the §107 filter")

mvp = vec('MVP')
vecs = {g: vec(g) for g in expressed}

# MVP against everything, once (the §107 distribution, recomputed here so this script stands alone)
mvp_rho = {}
for g in expressed:
    if g == 'MVP':
        continue
    rho, _ = spearmanr(mvp, vecs[g])
    if rho == rho:
        mvp_rho[g] = float(rho)
ordered_mvp = sorted(mvp_rho.values())
def mvp_pct(sym):
    r = mvp_rho[sym]
    return round(100.0 * sum(1 for v in ordered_mvp if v < r) / len(ordered_mvp), 2)
print(f"  MVP co-expression against {len(mvp_rho)} genes "
      f"(check vs §107: PAPSS2 pct {mvp_pct('PAPSS2')}, PAPSS1 pct {mvp_pct('PAPSS1')})")

def matched_null(seed, n):
    """Genes most similar to `seed`'s own tissue profile, and MVP's rho against each."""
    sv = vecs[seed]
    sim = {}
    for g in expressed:
        if g in (seed, 'MVP'):
            continue
        rho, _ = spearmanr(sv, vecs[g])
        if rho == rho:
            sim[g] = float(rho)
    nearest = sorted(sim, key=lambda k: -sim[k])[:n]
    null = sorted(mvp_rho[g] for g in nearest if g in mvp_rho)
    obs = mvp_rho[seed]
    pct = 100.0 * sum(1 for v in null if v < obs) / len(null)
    q = lambda f: null[min(len(null) - 1, int(f * len(null)))]
    return {'n_requested': n, 'n_null': len(null),
            'observed_rho_MVP_seed': round(obs, 4),
            'pct_in_matched_null': round(pct, 2),
            'null_q25': round(q(.25), 4), 'null_median': round(q(.50), 4),
            'null_q75': round(q(.75), 4), 'null_q95': round(q(.95), 4),
            'null_max': round(null[-1], 4),
            'nearest_15': nearest[:15],
            'nearest_15_profile_sim': [round(sim[g], 3) for g in nearest[:15]]}

res = {'filter': {'min_ntpm': MIN_NTPM, 'min_tissues': MIN_TISSUES,
                  'expressed_genes': len(expressed)},
       'genomewide_pct': {g: mvp_pct(g) for g in ['PAPSS2', 'PAPSS1', 'PARP4', 'TEP1']}}

# ---------------------------------------------------------------- gate
print("\n  GATE  (S = PARP4, a textbook subunit)")
res['gate'] = {str(n): matched_null('PARP4', n) for n in NS}
g200 = res['gate']['200']
res['gate']['passed'] = g200['pct_in_matched_null'] > 95.0
for n in NS:
    d = res['gate'][str(n)]
    print(f"    N={n:<4d} rho(MVP,PARP4)={d['observed_rho_MVP_seed']:+.3f}  "
          f"pct in matched null {d['pct_in_matched_null']:6.2f}  "
          f"null q25/med/q75/q95 {d['null_q25']:+.3f}/{d['null_median']:+.3f}/"
          f"{d['null_q75']:+.3f}/{d['null_q95']:+.3f}")
print(f"    GATE {'PASSED' if res['gate']['passed'] else 'FAILED'} "
      f"(needed >95th pct at N=200)")

# TEP1, descriptive only, not part of the gate
res['tep1_descriptive'] = {str(n): matched_null('TEP1', n) for n in NS}
d = res['tep1_descriptive']['200']
print(f"    TEP1 (descriptive, not gating): rho {d['observed_rho_MVP_seed']:+.3f}, "
      f"pct {d['pct_in_matched_null']:.2f}")

# ---------------------------------------------------------------- primary
print("\n  PRIMARY  (S = PAPSS2)")
res['primary'] = {str(n): matched_null('PAPSS2', n) for n in NS}
p200 = res['primary']['200']
for n in NS:
    d = res['primary'][str(n)]
    print(f"    N={n:<4d} rho(MVP,PAPSS2)={d['observed_rho_MVP_seed']:+.3f}  "
          f"pct in matched null {d['pct_in_matched_null']:6.2f}  "
          f"null q25/med/q75/q95 {d['null_q25']:+.3f}/{d['null_median']:+.3f}/"
          f"{d['null_q75']:+.3f}/{d['null_q95']:+.3f}  max {d['null_max']:+.3f}")
pc = p200['pct_in_matched_null']
verdict = 'STRUCK' if pc <= 75.0 else ('NOT STRUCK' if pc > 95.0 else 'INDETERMINATE')
res['primary_verdict'] = {'pct_at_N200': pc, 'verdict': verdict,
                          'interpretable': res['gate']['passed']}
print(f"    VERDICT: {verdict}"
      f"{'' if res['gate']['passed'] else '  (gate failed: NOT interpretable)'}")

# ---------------------------------------------------------------- secondary
papss2 = vecs['PAPSS2']
rev = {}
for g in expressed:
    if g == 'PAPSS2':
        continue
    rho, _ = spearmanr(papss2, vecs[g])
    if rho == rho:
        rev[g] = float(rho)
ro = sorted(rev.values())
res['reciprocal'] = {'MVP_pct_in_PAPSS2_distribution':
                     round(100.0 * sum(1 for v in ro if v < rev['MVP']) / len(ro), 2),
                     'MVP_rank': sorted(rev, key=lambda k: -rev[k]).index('MVP') + 1,
                     'n': len(rev)}
print(f"\n  SECONDARY reciprocal: MVP sits at the "
      f"{res['reciprocal']['MVP_pct_in_PAPSS2_distribution']}th pct of PAPSS2's own distribution "
      f"(rank {res['reciprocal']['MVP_rank']}/{res['reciprocal']['n']})")

res['internal_negative_PAPSS1'] = {str(n): matched_null('PAPSS1', n) for n in NS}
d = res['internal_negative_PAPSS1']['200']
print(f"  SECONDARY PAPSS1 (internal negative): rho {d['observed_rho_MVP_seed']:+.3f}, "
      f"pct in its own matched null {d['pct_in_matched_null']:.2f}")

print(f"\n  PAPSS2's 15 nearest profile neighbours: {p200['nearest_15']}")
print(f"  PARP4's  15 nearest profile neighbours: {g200['nearest_15']}")

with open(OUT, 'w') as fh:
    json.dump(res, fh, indent=1, sort_keys=True)
print(f"\n  wrote {OUT}")
