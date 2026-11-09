#!/usr/bin/env python3
"""True inter-half waist contacts in 4V60-assembly1, then the registered conservation
comparison. Registered at e93ab2a. Numbering matches results/surface_residues.csv
because both derive from 4V60 (rat MVP)."""
import gzip, csv, statistics as st
import numpy as np
from scipy.spatial import cKDTree
from scipy.stats import mannwhitneyu

cols=[]; A=[]
with gzip.open('data/raw/struct/4V60-assembly1.cif.gz','rt') as fh:
    inloop=False
    for line in fh:
        if line.startswith('_atom_site.'): cols.append(line.strip().split('.')[1]); inloop=True; continue
        if inloop and line.startswith('ATOM'):
            f=line.split()
            if len(f)<len(cols): continue
            A.append(f)
        elif inloop and A and not line.startswith(('ATOM','HETATM')): break
ix={c:i for i,c in enumerate(cols)}
print(f"  ATOM records: {len(A)}")

ch=np.array([a[ix['auth_asym_id']] for a in A])
xyz=np.array([[float(a[ix['Cartn_x']]),float(a[ix['Cartn_y']]),float(a[ix['Cartn_z']])] for a in A])
resi=np.array([int(a[ix['auth_seq_id']]) if a[ix['auth_seq_id']].lstrip('-').isdigit() else -1 for a in A])

half2 = np.array([c.endswith('-2') for c in ch])
print(f"  half A (no suffix): {len(set(ch[~half2]))} chains | half B ('-2'): {len(set(ch[half2]))} chains")
print(f"  GATE 1 (39 and 39): {'PASS' if len(set(ch[~half2]))==39 and len(set(ch[half2]))==39 else 'FAIL'}")

# restrict to the waist neighbourhood for tractability, then find true cross-half contacts
near = np.abs(xyz[:,2]) < 60
pA = near & ~half2; pB = near & half2
print(f"  atoms within 60 A of the waist plane: half A {pA.sum()}, half B {pB.sum()}")
tree=cKDTree(xyz[pB])
pairs=tree.query_ball_point(xyz[pA], r=4.5)
contact_resi = sorted({int(resi[pA][i]) for i,lst in enumerate(pairs) if lst and resi[pA][i]>0})
print(f"\n  TRUE inter-half contact residues (any atom within 4.5 A of the other half): {len(contact_resi)}")
print(f"    residue numbers: {contact_resi}")

rows=list(csv.DictReader(open('results/surface_residues.csv')))
def g(r,k):
    try: return float(r[k])
    except: return None
ok=[r for r in rows if g(r,'cons') is not None]
cset=set(contact_resi)
waist=[r for r in ok if int(r['resi']) in cset]
iface=[r for r in ok if r['interface']=='True']
other_if=[r for r in iface if int(r['resi']) not in cset]
null=[r for r in ok if r['exposed']=='True' and r['interface']!='True']
C=lambda L:[g(r,'cons') for r in L]
print(f"\n  mapped to conservation data: waist {len(waist)} | other interface {len(other_if)} | null {len(null)}")
g2 = len(waist)>=40
g3 = st.mean(C(iface)) > st.mean(C(null))
print(f"  GATE 2 (>=40 waist-contact residues): {'PASS' if g2 else f'FAIL - n={len(waist)}, still underpowered'}")
print(f"  GATE 3 (interface > exposed non-interface): {'PASS' if g3 else 'FAIL'}  ({st.mean(C(iface)):.4f} vs {st.mean(C(null)):.4f})")
if not waist: raise SystemExit
print()
for nm,L in [('TRUE waist contacts',waist),('other interface',other_if),('null exposed non-interface',null)]:
    c=C(L); print(f"  {nm:28s} n={len(c):4d}  mean {st.mean(c):.4f}  median {st.median(c):.4f}")
wm,om=st.mean(C(waist)), st.mean(C(other_if))
U,p=mannwhitneyu(C(waist),C(other_if),alternative='two-sided')
Un,pn=mannwhitneyu(C(waist),C(null),alternative='two-sided')
print(f"\n  registered PREDICTION: waist < other interface")
print(f"    {wm:.4f} vs {om:.4f} -> {'MET' if wm<om else 'NOT MET'}   p={p:.4g}")
print(f"    (n=18 proxy version gave waist 0.8187 vs distal 0.7694, p=0.5906 - NOT MET)")
print(f"  waist vs null: {wm:.4f} vs {st.mean(C(null)):.4f}  p={pn:.4g}")
