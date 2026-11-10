#!/usr/bin/env python3
"""Sulfo-conjugation test. Registered at 65c9723 (SULFATE_PREREGISTRATION.md) before any value read.

Gate: SULT2A1 must put adrenal in its top 2 of 51; STS must put placenta in its top 5.
Primary (KILL-ONLY): percentile of the sulfo panel in MVP's genome-wide co-expression distribution.
Control: matched GI-weighted null, because MVP and the sulfotransferases are both GI genes (§11/§22).
Secondary: the adrenal-versus-placenta asymmetry the design rests on, with its own kill condition.
"""
import csv, json, statistics as st
from scipy.stats import spearmanr

TSV = 'data/raw/tissue/rna_tissue_consensus.tsv'
OUT = 'results/sulfate.json'

SULFO    = ['SULT2A1', 'SULT2B1', 'SULT1A1', 'SULT1A3', 'SULT1E1']
DONOR    = ['PAPSS1', 'PAPSS2', 'SLC35B2', 'SLC35B3']
DESULF   = ['STS', 'GNS', 'GALNS', 'ARSA', 'ARSB']
PANEL    = SULFO + DONOR + DESULF
GI       = ['colon', 'small intestine', 'duodenum', 'rectum']

# ---------------------------------------------------------------- load
# DEVIATION, recorded: §22 reports "15,736 expressed genes" but no script implementing that
# filter is in the repository, so it cannot be reused. The filter is defined here instead:
# nTPM >= 1 in at least 5 of the 51 tissues. The expressed-gene count will differ from §22's.
MIN_NTPM, MIN_TISSUES = 1.0, 5

expr = {}      # symbol -> {tissue: nTPM}
with open(TSV) as fh:
    for r in csv.DictReader(fh, delimiter='\t'):
        expr.setdefault(r['Gene name'], {})[r['Tissue']] = float(r['nTPM'])

tissues = sorted({t for v in expr.values() for t in v})
print(f"  loaded {len(expr)} symbols x {len(tissues)} tissues")
assert len(tissues) == 51, len(tissues)
for t in GI + ['adrenal gland', 'placenta']:
    assert t in tissues, t

def vec(sym):
    d = expr[sym]
    return [d.get(t, 0.0) for t in tissues]

expressed = [g for g, d in expr.items()
             if sum(1 for t in tissues if d.get(t, 0.0) >= MIN_NTPM) >= MIN_TISSUES
             and len(d) == len(tissues)]
print(f"  expressed by this file's filter (nTPM>={MIN_NTPM} in >={MIN_TISSUES} tissues): {len(expressed)}")

def rank_of(sym, tissue):
    """1-based rank of `tissue` within `sym`'s own 51 values, highest first."""
    d = expr[sym]
    order = sorted(tissues, key=lambda t: -d.get(t, 0.0))
    return order.index(tissue) + 1

res = {'filter': {'min_ntpm': MIN_NTPM, 'min_tissues': MIN_TISSUES,
                  'expressed_genes': len(expressed), 'n_tissues': len(tissues),
                  'deviation': 'the §22 filter could not be reused; no script implements it'}}

# ---------------------------------------------------------------- gate
gate = {'SULT2A1_adrenal_rank': rank_of('SULT2A1', 'adrenal gland'),
        'STS_placenta_rank':    rank_of('STS', 'placenta')}
gate['sult2a1_pass'] = gate['SULT2A1_adrenal_rank'] <= 2
gate['sts_pass']     = gate['STS_placenta_rank'] <= 5
gate['passed']       = gate['sult2a1_pass'] and gate['sts_pass']
res['gate'] = gate
print(f"  GATE: SULT2A1 adrenal rank {gate['SULT2A1_adrenal_rank']}/51 (need <=2) -> "
      f"{'pass' if gate['sult2a1_pass'] else 'FAIL'}")
print(f"  GATE: STS placenta rank {gate['STS_placenta_rank']}/51 (need <=5) -> "
      f"{'pass' if gate['sts_pass'] else 'FAIL'}")

# ---------------------------------------------------------------- secondary (runs regardless:
# it is the design's own kill condition, not a result conditional on the gate)
mvp = vec('MVP')
asym = {}
for g in ['MVP', 'SULT2A1', 'SULT2B1', 'STS', 'PAPSS2']:
    asym[g] = {'adrenal_rank': rank_of(g, 'adrenal gland'),
               'placenta_rank': rank_of(g, 'placenta'),
               'adrenal_ntpm': expr[g]['adrenal gland'],
               'placenta_ntpm': expr[g]['placenta']}
asym['asymmetry_exists'] = (asym['SULT2A1']['adrenal_rank'] < asym['SULT2A1']['placenta_rank']
                            and asym['STS']['placenta_rank'] < asym['STS']['adrenal_rank'])
asym['design_killed'] = asym['STS']['adrenal_rank'] < asym['STS']['placenta_rank']
res['secondary_asymmetry'] = asym
print("  SECONDARY adrenal/placenta ranks of 51:")
for g in ['MVP', 'SULT2A1', 'SULT2B1', 'STS', 'PAPSS2']:
    a = asym[g]
    print(f"    {g:8s} adrenal #{a['adrenal_rank']:<3d}({a['adrenal_ntpm']:8.1f})  "
          f"placenta #{a['placenta_rank']:<3d}({a['placenta_ntpm']:8.1f})")
print(f"  asymmetry exists: {asym['asymmetry_exists']}   DESIGN KILLED: {asym['design_killed']}")

# ---------------------------------------------------------------- primary
rhos = {}
for g in expressed:
    if g == 'MVP':
        continue
    rho, p = spearmanr(mvp, vec(g))
    if rho == rho:                       # drop NaN (zero-variance genes)
        rhos[g] = float(rho)
print(f"  MVP co-expression computed against {len(rhos)} genes")

ordered = sorted(rhos.values())
def pct(sym):
    if sym not in rhos:
        return None
    r = rhos[sym]
    below = sum(1 for v in ordered if v < r)
    return round(100.0 * below / len(ordered), 2)

prim = {g: {'rho': round(rhos[g], 4) if g in rhos else None,
            'percentile': pct(g),
            'rank': (sorted(rhos, key=lambda k: -rhos[k]).index(g) + 1) if g in rhos else None}
        for g in PANEL}
res['primary'] = prim
print("  PRIMARY percentile of MVP's genome-wide co-expression distribution:")
for g in PANEL:
    d = prim[g]
    tag = ('sulfo' if g in SULFO else 'donor' if g in DONOR else 'de-sulf')
    if d['percentile'] is None:
        print(f"    {g:9s} [{tag:7s}] not expressed by this filter")
    else:
        print(f"    {g:9s} [{tag:7s}] rho {d['rho']:+.3f}  pct {d['percentile']:6.2f}  "
              f"rank {d['rank']}/{len(rhos)}")

p2a1, p2b1, psts = prim['SULT2A1']['percentile'], prim['SULT2B1']['percentile'], prim['STS']['percentile']
killed_low  = (p2a1 is not None and p2a1 < 80) and (p2b1 is not None and p2b1 < 80)
killed_sts  = psts is not None and p2a1 is not None and p2b1 is not None and psts > max(p2a1, p2b1)
res['primary_verdict'] = {'killed_both_below_80': killed_low,
                          'killed_sts_above_both': killed_sts,
                          'KILLED': killed_low or killed_sts}
print(f"  PRIMARY VERDICT: both sulfotransferases below 80th pct = {killed_low}; "
      f"STS above both = {killed_sts}; KILLED = {killed_low or killed_sts}")

# ---------------------------------------------------------------- GI-matched control
# "GI-weighted" = how strongly a gene's own 51-tissue profile loads on the four GI tissues
gi_profile = [1.0 if t in GI else 0.0 for t in tissues]
gi_corr = {}
for g in expressed:
    rho, _ = spearmanr(vec(g), gi_profile)
    if rho == rho:
        gi_corr[g] = float(rho)
cut = sorted(gi_corr.values())[int(0.75 * len(gi_corr))]
matched = [g for g, v in gi_corr.items() if v >= cut and g in rhos]
mp = sorted(pct(g) for g in matched if pct(g) is not None)
q1, med, q3 = (mp[len(mp) // 4], mp[len(mp) // 2], mp[3 * len(mp) // 4])
ctrl = {'gi_corr_cutoff': round(cut, 4), 'matched_n': len(matched),
        'matched_pct_q1': q1, 'matched_pct_median': med, 'matched_pct_q3': q3,
        'SULT2A1_inside_iqr': (p2a1 is not None and q1 <= p2a1 <= q3),
        'SULT2B1_inside_iqr': (p2b1 is not None and q1 <= p2b1 <= q3)}
res['gi_matched_control'] = ctrl
print(f"  CONTROL: {len(matched)} GI-weighted genes, MVP-percentile IQR "
      f"[{q1:.1f}, {q3:.1f}] median {med:.1f}")
print(f"    SULT2A1 pct {p2a1} inside IQR: {ctrl['SULT2A1_inside_iqr']}   "
      f"SULT2B1 pct {p2b1} inside IQR: {ctrl['SULT2B1_inside_iqr']}")

with open(OUT, 'w') as fh:
    json.dump(res, fh, indent=1, sort_keys=True)
print(f"  wrote {OUT}")
