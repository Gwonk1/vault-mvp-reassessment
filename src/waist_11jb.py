#!/usr/bin/env python3
"""Replicate the 12-residue waist result on 11JB (human, 78 chains). Registered above."""
import gzip
import numpy as np
from scipy.spatial import cKDTree
cols=[]; A=[]
with gzip.open('data/raw/struct/11JB.cif.gz','rt') as fh:
    inloop=False
    for line in fh:
        if line.startswith('_atom_site.'): cols.append(line.strip().split('.')[1]); inloop=True; continue
        if inloop and line.startswith('ATOM'):
            f=line.split()
            if len(f)<len(cols): continue
            A.append(f)
        elif inloop and A and not line.startswith(('ATOM','HETATM')): break
ix={c:i for i,c in enumerate(cols)}
ch=np.array([a[ix['auth_asym_id']] for a in A])
xyz=np.array([[float(a[ix['Cartn_x']]),float(a[ix['Cartn_y']]),float(a[ix['Cartn_z']])] for a in A])
resi=np.array([int(a[ix['auth_seq_id']]) if a[ix['auth_seq_id']].lstrip('-').isdigit() else -1 for a in A])
print(f"  ATOM records {len(A)}, chains {len(set(ch))}")
mz={c: xyz[ch==c,2].mean() for c in set(ch)}
med=np.median(list(mz.values()))
upper={c for c,v in mz.items() if v>med}
isup=np.array([c in upper for c in ch])
print(f"  GATE split: {len(upper)} / {len(set(ch))-len(upper)}  "
      f"{'PASS' if len(upper)==39 else 'FAIL'}")
near=np.abs(xyz[:,2]-med)<60
pA=near&isup; pB=near&~isup
print(f"  atoms within 60 A of the waist plane: {pA.sum()} / {pB.sum()}")
tree=cKDTree(xyz[pB])
hits=tree.query_ball_point(xyz[pA], r=4.5)
cset=sorted({int(resi[pA][i]) for i,l in enumerate(hits) if l and resi[pA][i]>0})
print(f"\n  11JB inter-half contact residues: {len(cset)}")
print(f"    {cset}")
rat=[1,2,3,4,6,21,42,43,44,45,46,47]
print(f"\n  4V60 (rat) was: {rat}")
nterm=[r for r in cset if r<=50]
print(f"  11JB contacts at residue <=50: {len(nterm)} of {len(cset)} ({100*len(nterm)/max(1,len(cset)):.0f}%)")
print(f"  PREDICTION (N-terminal dominated, total <30): "
      f"{'MET' if len(cset)<30 and len(nterm)>=0.6*len(cset) else 'NOT MET'}")
print(f"  shared residue numbers with 4V60: {sorted(set(cset)&set(rat))}")
