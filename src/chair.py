#!/usr/bin/env python3
"""Tests A and B of the chair metaphor. Registered at 7c82d9c before any value was read."""
import csv, gzip, math, statistics as st, json, re
from scipy.stats import spearmanr

STAGES=['4wpc','5wpc','6wpc','7wpc','8wpc','9wpc','10wpc','11wpc','12wpc','13wpc','16wpc','18wpc',
        '19wpc','20wpc','newborn','infant','toddler','school','youngTeenager','teenager',
        'oldTeenager','youngAdult','youngMidAge','olderMidAge','senior']
SRANK={s.lower():i for i,s in enumerate(STAGES)}
PROLIF=['MKI67','TOP2A','PCNA','CCNB1']; HOUSE=['ACTB','GAPDH']; SUBJ=['MVP','TEP1','PARP4']
WANT=PROLIF+HOUSE+SUBJ

# ENSG <-> symbol map from the local HPA file (no network)
sym2ens={}
with open('data/raw/tissue/rna_tissue_consensus.tsv') as fh:
    for r in csv.DictReader(fh, delimiter='\t'):
        sym2ens.setdefault(r['Gene name'], r['Gene'])
ens={g: sym2ens.get(g) for g in WANT}
print("  ENSG resolution:", {g:(e or 'NOT FOUND') for g,e in ens.items()})
need={e:g for g,e in ens.items() if e}

# ---------- TEST A ----------
with open('data/raw/devel/Human.RPKM.txt') as fh:
    hdr=[h.strip('"') for h in fh.readline().split()]
    rows={}
    for line in fh:
        p=line.split()
        gid=p[0].strip('"')
        if gid in need: rows[need[gid]]=[float(x) for x in p[1:]]
print(f"  devel matrix: {len(hdr)} samples; genes found {sorted(rows)}")
cols=[]
for i,h in enumerate(hdr):
    m=re.match(r'([A-Za-z]+)\.([A-Za-z0-9]+)\.', h)
    if m and m.group(2).lower() in SRANK: cols.append((i, m.group(1), SRANK[m.group(2).lower()]))
organs=sorted({o for _,o,_ in cols})
print(f"  organs: {organs}")
A={}
for g,v in rows.items():
    A[g]={}
    for o in organs:
        idx=[(i,r) for i,oo,r in cols if oo==o]
        if len({r for _,r in idx})<8: continue
        x=[r for _,r in idx]; y=[math.log1p(v[i]) for i,_ in idx]
        rho,p=spearmanr(x,y)
        A[g][o]=(round(float(rho),3), float(p))
qual=sorted({o for g in A for o in A[g]})
print(f"\n  TEST A - Spearman rho(log1p RPKM, stage rank), organs with >=8 stages: {qual}")
print(f"  {'gene':7s} " + ' '.join(f'{o[:9]:>9s}' for o in qual) + "   neg/total")
for g in PROLIF+HOUSE+SUBJ:
    if g not in A: continue
    cells=' '.join(f"{A[g][o][0]:>+9.3f}" if o in A[g] else f"{'--':>9s}" for o in qual)
    neg=sum(1 for o in qual if o in A[g] and A[g][o][0]<0)
    print(f"  {g:7s} {cells}   {neg}/{len(A[g])}")
# gate
pneg=[sum(1 for o in A[g] if A[g][o][0]<0) for g in PROLIF if g in A]
g1=all(n>=5 for n in pneg) and len(pneg)==len(PROLIF)
pmed=st.median([abs(A[g][o][0]) for g in PROLIF if g in A for o in A[g]])
hmed={g: st.median([abs(A[g][o][0]) for o in A[g]]) for g in HOUSE if g in A}
g2=all(v<pmed for v in hmed.values()) and len(hmed)==len(HOUSE)
g3=all(ens[g] for g in WANT) and all(g in rows for g in WANT)
print(f"\n  GATE A1 prolif rho<0 in >=5/7 organs, all 4 markers: {'PASS' if g1 else 'FAIL'}  (neg counts {pneg})")
print(f"  GATE A2 housekeeping |rho| < prolif median |rho|={pmed:.3f}: {'PASS' if g2 else 'FAIL'}  ({ {k:round(v,3) for k,v in hmed.items()} })")
print(f"  GATE A3 all genes resolved and found                 : {'PASS' if g3 else 'FAIL'}")
gateA=g1 and g2 and g3
print(f"\n  >>> TEST A GATE: {'PASS' if gateA else 'FAIL - UNINFORMATIVE'}")
if gateA and 'MVP' in A:
    pos=sum(1 for o in A['MVP'] if A['MVP'][o][0]>0); tot=len(A['MVP'])
    print(f"      MVP rho>0 in {pos}/{tot} organs; median rho {st.median([A['MVP'][o][0] for o in A['MVP']]):+.3f}")
    print(f"      PREDICTION (rho>0 in a majority): {'MET' if pos>tot/2 else 'NOT MET'}")
    print(f"      KILL (rho<=0 in a majority)     : {'*** KILLED ***' if pos<=tot/2 else 'not killed'}")

# ---------- TEST B ----------
POST=['cerebral cortex','cerebellum','heart muscle','skeletal muscle']
PROL=['bone marrow','testis','small intestine','skin']
tis={}
with open('data/raw/tissue/rna_tissue_consensus.tsv') as fh:
    for r in csv.DictReader(fh, delimiter='\t'):
        if r['Gene name'] in WANT: tis.setdefault(r['Gene name'],{})[r['Tissue']]=float(r['nTPM'])
print(f"\n  TEST B - HPA nTPM, post-mitotic vs proliferative")
missing=[t for t in POST+PROL if not any(t in v for v in tis.values())]
print(f"  tissue names resolved: {len(POST+PROL)-len(missing)}/{len(POST+PROL)}" + (f"  MISSING {missing}" if missing else ""))
B={}
for g in PROLIF+SUBJ:
    if g not in tis: continue
    a=[tis[g][t] for t in POST if t in tis[g]]; b=[tis[g][t] for t in PROL if t in tis[g]]
    if a and b: B[g]=(st.median(a), st.median(b))
    print(f"  {g:7s} post-mitotic median {st.median(a):8.1f}   proliferative median {st.median(b):8.1f}   ratio {st.median(a)/max(st.median(b),1e-9):6.2f}")
gB = ('MKI67' in B and B['MKI67'][1]>B['MKI67'][0]) and ('TOP2A' in B and B['TOP2A'][1]>B['TOP2A'][0]) and not missing
print(f"\n  GATE B: MKI67 and TOP2A both higher in proliferative: {'PASS' if gB else 'FAIL'}")
if gB and 'MVP' in B:
    print(f"      MVP post-mitotic {B['MVP'][0]:.1f} vs proliferative {B['MVP'][1]:.1f}")
    print(f"      PREDICTION (post-mitotic higher): {'MET' if B['MVP'][0]>B['MVP'][1] else 'NOT MET'}")
json.dump({'A':A,'B':B}, open('results/chair.json','w'), indent=1, default=str)
