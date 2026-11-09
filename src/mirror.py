#!/usr/bin/env python3
"""TEST C: does a human paralogue of MVP exist at all? Registered at 7c82d9c."""
import gzip, re, json, warnings
warnings.filterwarnings('ignore')
from Bio import Align
from Bio.Align import substitution_matrices

prots={}
name=None; buf=[]
with gzip.open('data/raw/human_sp.fasta.gz','rt') as fh:
    for line in fh:
        if line.startswith('>'):
            if name and buf: prots.setdefault(name, ''.join(buf))
            m=re.search(r'\bGN=(\S+)', line); name=m.group(1) if m else None; buf=[]
        else: buf.append(line.strip())
    if name and buf: prots.setdefault(name, ''.join(buf))
print(f"  proteome searched: {len(prots)} proteins with gene names")

al=Align.PairwiseAligner(mode='local', substitution_matrix=substitution_matrices.load('BLOSUM62'),
                         open_gap_score=-11, extend_gap_score=-1)
K=6
def kmers(s): return {s[i:i+K] for i in range(len(s)-K+1)}

def best_hits(query_gene, topn=40, report=4):
    q=prots[query_gene]; qk=kmers(q)
    cand=sorted(((len(qk & kmers(s))/max(1,len(qk | kmers(s))), g)
                 for g,s in prots.items() if g!=query_gene and len(s)>=150),
                reverse=True)[:topn]
    out=[]
    for _,g in cand:
        s=prots[g]
        try: a=al.align(q,s)[0]
        except Exception: continue
        qa,sa=str(a[0]),str(a[1])
        cols=[(x,y) for x,y in zip(qa,sa) if x!='-' and y!='-']
        if not cols: continue
        ident=sum(1 for x,y in cols if x==y)/len(cols)
        out.append((round(ident*100,1), len(cols), g))
    # Rank by the REGISTERED criterion (>=200 aligned residues) rather than raw identity:
    # local alignment yields 6-8 residue perfect matches that otherwise outrank a true
    # paralogue at 98.9% over 375 aa. Fixed before MVP's result was ever printed, so this
    # repair is blind for the subject - the gate aborted first. See RESULTS 83c.
    long_hits=[h for h in out if h[1]>=200]
    long_hits.sort(reverse=True)
    if long_hits: return long_hits[:report]
    out.sort(key=lambda h:(h[1],h[0]), reverse=True)
    return out[:report]

print("\n  GATE C1 - known paralogue pairs must be recovered:")
gate=[]
for q, expect in [('ACTB','ACTG'), ('TUBB','TUBB')]:
    hits=best_hits(q)
    top=hits[0]
    found=any(re.match(expect, g) for _,_,g in hits[:2])
    gate.append(found and top[0]>=20 and top[1]>=200)
    print(f"    {q:6s} best: " + ', '.join(f"{g} {i}% / {L}aa" for i,L,g in hits[:3])
          + f"   -> {'PASS' if gate[-1] else 'FAIL'}")
g2 = len(prots) >= 20000
print(f"  GATE C2 >= 20,000 proteins searched: {'PASS' if g2 else 'FAIL'}  ({len(prots)})")
ok = all(gate) and g2
print(f"\n  >>> TEST C GATE: {'PASS' if ok else 'FAIL - UNINFORMATIVE'}")
res={}
if ok:
    for q in ('MVP','TEP1','PARP4'):
        hits=best_hits(q); res[q]=hits
        print(f"\n  {q} best non-self hits in the human proteome:")
        for i,L,g in hits: print(f"    {g:12s} {i:5.1f}% identity over {L:4d} aligned residues")
        top=hits[0]
        if q=='MVP':
            met = top[0]>=20 and top[1]>=200
            print(f"\n    PREDICTION (a paralogue at >=20% over >=200 aa): {'MET' if met else 'NOT MET'}")
            print(f"    KILL (no such hit -> MVP is single-copy in human): "
                  f"{'*** KILLED - no mirror protein exists in human ***' if not met else 'not killed'}")
json.dump(res, open('results/mirror.json','w'), indent=1)
