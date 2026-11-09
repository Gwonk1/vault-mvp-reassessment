#!/usr/bin/env python3
"""Grok audit 008's prescription for TEST 3: is MVP's rise gene-specific, or is it
every gene that merely failed to decline? Stage medians, gene-wise fold distribution,
and a cross-gene-median residual."""
import csv, math, re, statistics as st, json
import numpy as np
from scipy.stats import spearmanr

STAGES=['4wpc','5wpc','6wpc','7wpc','8wpc','9wpc','10wpc','11wpc','12wpc','13wpc','16wpc','18wpc',
        '19wpc','20wpc','newborn','infant','toddler','school','youngTeenager','teenager',
        'oldTeenager','youngAdult','youngMidAge','olderMidAge','senior']
SRANK={s.lower():i for i,s in enumerate(STAGES)}
WATCH=['MVP','TEP1','PARP4','MKI67','TOP2A','PCNA','CCNB1','ACTB','GAPDH']
sym2ens={}; ens2sym={}
with open('data/raw/tissue/rna_tissue_consensus.tsv') as fh:
    for r in csv.DictReader(fh, delimiter='\t'):
        sym2ens.setdefault(r['Gene name'], r['Gene'])
for g in WATCH: ens2sym[sym2ens[g]]=g

with open('data/raw/devel/Human.RPKM.txt') as fh:
    hdr=[h.strip('"') for h in fh.readline().split()]
    gid=[]; M=[]
    for line in fh:
        p=line.split(); gid.append(p[0].strip('"')); M.append(p[1:])
X=np.array(M, dtype=np.float32); del M
print(f"  matrix {X.shape[0]} genes x {X.shape[1]} samples")

cols={}
for i,h in enumerate(hdr):
    m=re.match(r'([A-Za-z]+)\.([A-Za-z0-9]+)\.', h)
    if m and m.group(2).lower() in SRANK: cols.setdefault(m.group(1), {}).setdefault(SRANK[m.group(2).lower()], []).append(i)

out={}
for organ, stagemap in sorted(cols.items()):
    ranks=sorted(stagemap)
    if len(ranks)<8: continue
    # 1. stage medians
    SM=np.column_stack([np.median(X[:, stagemap[r]], axis=1) for r in ranks])
    # drop genes zero in >= half the stages
    keep=(SM>0).sum(axis=1) > len(ranks)/2
    SMk=SM[keep]; gk=[gid[i] for i in np.where(keep)[0]]
    L=np.log1p(SMk)
    # 2. per-gene rho on stage medians, and log2 fold (last 3 stages / first 3)
    rho=np.array([spearmanr(ranks, L[i])[0] for i in range(L.shape[0])])
    last3=np.median(SMk[:, -3:], axis=1); first3=np.median(SMk[:, :3], axis=1)
    fold=np.log2((last3+1e-6)/(first3+1e-6))
    # 4. residual vs the cross-gene median trajectory
    m_stage=np.median(L, axis=0)
    idx={g:i for i,g in enumerate(gk)}
    row={}
    for e,sym in ens2sym.items():
        if e not in idx: row[sym]=None; continue
        i=idx[e]
        pr=float((rho<rho[i]).mean()*100); pf=float((fold<fold[i]).mean()*100)
        rres=spearmanr(ranks, L[i]-m_stage)[0]
        row[sym]=dict(rho=round(float(rho[i]),3), rho_pct=round(pr,1),
                      fold=round(float(fold[i]),3), fold_pct=round(pf,1),
                      resid_rho=round(float(rres),3))
    out[organ]=dict(genes=int(L.shape[0]), frac_rho_pos=round(float((rho>0).mean()),3),
                    median_fold=round(float(np.median(fold)),3), rows=row)
    print(f"\n  {organ}: {L.shape[0]} genes kept, {len(ranks)} stages | "
          f"fraction with rho>0: {(rho>0).mean():.3f} | median log2 fold {np.median(fold):+.3f}")
    print(f"    {'gene':7s} {'rho':>7s} {'rho_pct':>8s} {'log2fold':>9s} {'fold_pct':>9s} {'resid_rho':>10s}")
    for sym in WATCH:
        v=row.get(sym)
        if v: print(f"    {sym:7s} {v['rho']:+7.3f} {v['rho_pct']:7.1f}% {v['fold']:+9.3f} {v['fold_pct']:8.1f}% {v['resid_rho']:+10.3f}")
json.dump(out, open('results/chair_repair.json','w'), indent=1)

print("\n  ===== grok's bar: is MVP extreme in the FOLD distribution (95th pct is the right order)? =====")
mvp_fp=[v['rows']['MVP']['fold_pct'] for v in out.values() if v['rows'].get('MVP')]
mvp_rp=[v['rows']['MVP']['rho_pct'] for v in out.values() if v['rows'].get('MVP')]
mvp_rr=[v['rows']['MVP']['resid_rho'] for v in out.values() if v['rows'].get('MVP')]
fpos=[v['frac_rho_pos'] for v in out.values()]
print(f"    MVP fold percentile per organ : {[round(x,1) for x in mvp_fp]}")
print(f"    MVP rho  percentile per organ : {[round(x,1) for x in mvp_rp]}")
print(f"    MVP residual rho per organ    : {mvp_rr}")
print(f"    fraction of ALL genes rho>0   : {fpos}")
print(f"\n    organs where MVP fold pct >= 95 : {sum(1 for x in mvp_fp if x>=95)}/{len(mvp_fp)}")
print(f"    organs where residual rho > 0.5 : {sum(1 for x in mvp_rr if x>0.5)}/{len(mvp_rr)}")
print(f"    was the 7/7 sign test mis-centered? median fraction of genes with rho>0 = {st.median(fpos):.3f}")
