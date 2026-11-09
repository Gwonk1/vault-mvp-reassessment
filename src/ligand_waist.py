#!/usr/bin/env python3
"""Waist contacts across the Lodwick ligand series. Registered at b94fef7.
Method identical to src/waist_contacts.py and src/waist_11jb.py."""
import gzip, collections, json
import numpy as np
from scipy.spatial import cKDTree

SERIES=[('9BW5','apo'),('9MXH','+NAD+'),('9MXV','+ADP'),('9BW6','+PARP4'),('9BW7','+PARP4/NAD+')]

def contacts(path):
    cols=[]; A=[]
    with gzip.open(path,'rt') as fh:
        inloop=False
        for line in fh:
            if line.startswith('_atom_site.'): cols.append(line.strip().split('.')[1]); inloop=True; continue
            if inloop and line.startswith('ATOM'):
                f=line.split()
                if len(f)<len(cols): continue
                A.append(f)
            elif inloop and A and not line.startswith(('ATOM','HETATM')): break
    if not A: return None
    ix={c:i for i,c in enumerate(cols)}
    # MVP chains only - exclude PARP4 so the comparison is like-for-like
    ent=np.array([a[ix['label_entity_id']] for a in A])
    main=collections.Counter(ent).most_common(1)[0][0]
    keep=ent==main
    ch=np.array([a[ix['auth_asym_id']] for a in A])[keep]
    xyz=np.array([[float(a[ix['Cartn_x']]),float(a[ix['Cartn_y']]),float(a[ix['Cartn_z']])] for a in A])[keep]
    resi=np.array([int(a[ix['auth_seq_id']]) if a[ix['auth_seq_id']].lstrip('-').isdigit() else -1
                   for a in A])[keep]
    mz={c: xyz[ch==c,2].mean() for c in set(ch)}
    med=np.median(list(mz.values()))
    up={c for c,v in mz.items() if v>med}
    isup=np.array([c in up for c in ch])
    near=np.abs(xyz[:,2]-med)<60
    pA=near&isup; pB=near&~isup
    if pA.sum()==0 or pB.sum()==0: return dict(err='one half empty near the waist')
    t=cKDTree(xyz[pB])
    hits=t.query_ball_point(xyz[pA], r=4.5)
    cs=sorted({int(resi[pA][i]) for i,l in enumerate(hits) if l and resi[pA][i]>0})
    return dict(nchain=len(set(ch)), split=(len(up), len(set(ch))-len(up)),
                mvp_chains_entity=main, contacts=cs)

res={}
print(f"  {'PDB':7s} {'ligand':14s} {'chains':>7s} {'split':>9s} {'n':>4s}  contacts")
for pdb,lig in SERIES:
    r=contacts(f'data/raw/struct/{pdb}-assembly1.cif.gz')
    if r is None or 'err' in r:
        print(f"  {pdb:7s} {lig:14s} PARSE/GATE FAIL: {r.get('err') if r else 'no atoms'}"); continue
    res[pdb]=dict(lig=lig, **r)
    print(f"  {pdb:7s} {lig:14s} {r['nchain']:7d} {str(r['split']):>9s} {len(r['contacts']):4d}  {r['contacts']}")

print(f"\n  previously: 4V60 (rat, xtal) [1,2,3,4,6,21,42,43,44,45,46,47] | 11JB (human, EM) [6,7,9,21,22,36,38,39,40,42]")
if len(res)>=2:
    sets={k:set(v['contacts']) for k,v in res.items()}
    print(f"\n  PREDICTION 1 (small, N-terminal dominated):")
    for k,v in res.items():
        cs=v['contacts']; nt=[r for r in cs if r<=50]
        ok = len(cs)<30 and len(nt)>=0.6*len(cs)
        print(f"    {k:7s} n={len(cs):3d}  <=50: {len(nt)}/{len(cs)}  -> {'MET' if ok else 'NOT MET'}")
    ks=list(sets)
    print(f"\n  PREDICTION 2 (pairwise overlap >=60%, counts within +/-8):")
    worst=1.0; worstpair=None
    for i,a in enumerate(ks):
        for b in ks[i+1:]:
            j=len(sets[a]&sets[b])/max(1,len(sets[a]|sets[b]))
            if j<worst: worst, worstpair = j, (a,b)
    cnts=[len(v) for v in sets.values()]
    print(f"    worst pairwise Jaccard: {worst:.2f} ({worstpair[0]} vs {worstpair[1]})")
    print(f"    count range {min(cnts)}..{max(cnts)} (spread {max(cnts)-min(cnts)})")
    print(f"    -> {'MET' if worst>=0.60 and max(cnts)-min(cnts)<=8 else 'NOT MET'}")
    cnt=collections.Counter(r for v in sets.values() for r in v)
    cons=sorted(r for r,n in cnt.items() if n>=4)
    print(f"\n  PREDICTION 3 (consensus set, contacting in >=4 of {len(sets)}): {len(cons)} residues")
    print(f"    CONSENSUS: {cons}")
    print(f"    in all {len(sets)}: {sorted(r for r,n in cnt.items() if n==len(sets))}")
json.dump(res, open('results/ligand_waist.json','w'), indent=1)
