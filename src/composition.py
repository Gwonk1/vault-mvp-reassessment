#!/usr/bin/env python3
"""Does MVP's composition look like a storage protein?
Registered in COMPOSITION_PREREGISTRATION.md (25c270b) before any value was computed."""
import gzip, re, statistics as st, json

# Standard residue formulas as incorporated into a peptide (minus water). Definitional.
N_PER = {**{a:1 for a in 'ACDEFGILMPSTVY'}, **{a:2 for a in 'NQKW'}, 'H':3, 'R':4}
S_PER = {'C':1, 'M':1}
C_PER = {'G':2,'A':3,'S':3,'P':5,'V':5,'T':4,'C':3,'L':6,'I':6,'N':4,'D':4,
         'Q':5,'K':6,'E':5,'M':5,'H':6,'F':9,'R':6,'Y':9,'W':11}
AAS = 'ACDEFGHIKLMNPQRSTVWY'

STORAGE  = ['CSN1S1','ALB','FTL']
STRUCT   = ['CLTC','ACTB','TUBB']
SUBJECT  = ['MVP','TEP1','PARP4']

prots = {}
name, buf = None, []
with gzip.open('data/raw/human_sp.fasta.gz','rt') as fh:
    for line in fh:
        if line.startswith('>'):
            if name and buf: prots.setdefault(name, ''.join(buf))
            m = re.search(r'\bGN=(\S+)', line); name = m.group(1) if m else None; buf = []
        else: buf.append(line.strip())
    if name and buf: prots.setdefault(name, ''.join(buf))

def stats(seq):
    seq = ''.join(c for c in seq.upper() if c in N_PER)
    n = len(seq)
    if n < 50: return None
    return dict(L=n,
                N=sum(N_PER[c] for c in seq)/n,
                S=sum(S_PER.get(c,0) for c in seq)/n,
                C=sum(C_PER[c] for c in seq)/n,
                freq={a: seq.count(a)/n for a in AAS})

allst = {g: s for g,s in ((g, stats(sq)) for g,sq in prots.items()) if s}
Nd = [s['N'] for s in allst.values()]; Sd = [s['S'] for s in allst.values()]
mN, sdN = st.mean(Nd), st.stdev(Nd); mS, sdS = st.mean(Sd), st.stdev(Sd)
fmean = {a: st.mean([s['freq'][a] for s in allst.values()]) for a in AAS}
fsd   = {a: st.stdev([s['freq'][a] for s in allst.values()]) for a in AAS}

print(f"  proteome baseline: {len(allst)} proteins >=50 aa of {len(prots)} parsed")
print(f"    N/residue  mean {mN:.4f}  sd {sdN:.4f}")
print(f"    S/residue  mean {mS:.4f}  sd {sdS:.4f}\n")
print(f"  {'gene':9s} {'group':11s} {'len':>5s} {'N/res':>7s} {'z(N)':>7s} {'S/res':>7s} {'z(S)':>7s}")
rows={}
for group, genes in [('STORAGE',STORAGE),('STRUCTURAL',STRUCT),('SUBJECT',SUBJECT)]:
    for g in genes:
        s = allst.get(g)
        if not s:
            print(f"  {g:9s} {group:11s}  NOT FOUND in the proteome by gene name"); rows[g]=None; continue
        zN=(s['N']-mN)/sdN; zS=(s['S']-mS)/sdS
        rows[g]=dict(group=group,L=s['L'],N=s['N'],zN=zN,S=s['S'],zS=zS)
        print(f"  {g:9s} {group:11s} {s['L']:5d} {s['N']:7.4f} {zN:+7.2f} {s['S']:7.4f} {zS:+7.2f}")

# registered gate
found = lambda gs: [g for g in gs if rows.get(g)]
c1 = sum(1 for g in found(STORAGE) if rows[g]['zN'] > 0)
c2 = sum(1 for g in found(STRUCT)  if rows[g]['zN'] <= 1.0)
c3 = len(found(STORAGE))==3 and len(found(STRUCT))==3 and len(found(SUBJECT))>=1
print(f"\n  CLAUSE 1 >=2 of 3 storage proteins above the mean      : {'PASS' if c1>=2 else 'FAIL'}  ({c1}/3, found {len(found(STORAGE))})")
print(f"  CLAUSE 2 >=2 of 3 structural proteins not above +1 SD  : {'PASS' if c2>=2 else 'FAIL'}  ({c2}/3, found {len(found(STRUCT))})")
print(f"  CLAUSE 3 all controls found by accession, counts shown : {'PASS' if c3 else 'FAIL'}")
gate = c1>=2 and c2>=2 and c3
print(f"\n  ===== GATE: {'PASS' if gate else 'FAIL - UNINFORMATIVE'} =====")
if gate and rows.get('MVP'):
    z = rows['MVP']['zN']
    print(f"\n  MVP nitrogen/residue z = {z:+.2f}")
    print(f"    PREDICTION (>= +1 SD above the mean): {'MET' if z>=1.0 else 'NOT MET'}")
    print(f"    KILL (within +1 SD)                : {'*** KILLED - no support from composition ***' if z<1.0 else 'not killed'}")
    m=allst['MVP']
    dev=sorted(((m['freq'][a]-fmean[a])/fsd[a], a) for a in AAS)
    print(f"\n  MVP's most depleted residues vs proteome: " + ', '.join(f'{a} {z_:+.2f}' for z_,a in dev[:5]))
    print(f"  MVP's most enriched residues vs proteome: " + ', '.join(f'{a} {z_:+.2f}' for z_,a in dev[-5:][::-1]))
json.dump({k:v for k,v in rows.items()}, open('results/composition.json','w'), indent=1)
