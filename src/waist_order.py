#!/usr/bin/env python3
"""Waist vs cap order from deposited B-factors. Registered at e316176.
Parses the _atom_site loop header for indices rather than assuming them."""
import gzip, sys, statistics as st
import numpy as np
from scipy.stats import mannwhitneyu

def load(path):
    cols=[]; rows=[]
    with gzip.open(path,'rt') as fh:
        inloop=False
        for line in fh:
            if line.startswith('_atom_site.'):
                cols.append(line.strip().split('.')[1]); inloop=True; continue
            if inloop and (line.startswith('ATOM') or line.startswith('HETATM')):
                f=line.split()
                if len(f)<len(cols): continue
                rows.append(f)
            elif inloop and rows and not line.startswith(('ATOM','HETATM')):
                break
    if not cols: return None,None
    ix={c:i for i,c in enumerate(cols)}
    return ix, rows

for name,path in [('11JB','data/raw/struct/11JB.cif.gz'),
                  ('4V60','data/raw/struct/4V60-assembly1.cif.gz')]:
    ix,rows=load(path)
    if not ix: print(f"  {name}: could not parse atom_site header"); continue
    need=['label_atom_id','Cartn_z','B_iso_or_equiv','group_PDB']
    if any(k not in ix for k in need):
        print(f"  {name}: missing a needed column; have {sorted(ix)[:8]}..."); continue
    z=[]; b=[]
    for f in rows:
        if f[ix['group_PDB']]!='ATOM': continue
        if f[ix['label_atom_id']].strip('"')!='CA': continue
        try: z.append(float(f[ix['Cartn_z']])); b.append(float(f[ix['B_iso_or_equiv']]))
        except ValueError: continue
    if not z: print(f"  {name}: no CA atoms parsed"); continue
    z=np.array(z); b=np.array(b)
    print(f"\n  === {name} ===")
    print(f"    CA atoms: {len(z)}   z range {z.min():.1f}..{z.max():.1f}")
    iqr=np.percentile(b,75)-np.percentile(b,25)
    print(f"    B range {b.min():.2f}..{b.max():.2f}   median {np.median(b):.2f}   IQR {iqr:.3f}")
    if iqr<=0:
        print(f"    GATE FAIL: B-factors do not vary (IQR={iqr}); proxy carries no information - VOID")
        continue
    # waist plane = z nearest the particle centre; cap = furthest
    az=np.abs(z-np.median(z))
    lo,hi=np.percentile(az,15),np.percentile(az,85)
    waist=b[az<=lo]; cap=b[az>=hi]
    print(f"    GATE: IQR>0 PASS | waist n={len(waist)} cap n={len(cap)} "
          f"({'PASS' if min(len(waist),len(cap))>=200 else 'FAIL <200'})")
    if min(len(waist),len(cap))<200: continue
    U,p=mannwhitneyu(waist,cap,alternative='two-sided')
    print(f"    waist median B {np.median(waist):.2f}   cap median B {np.median(cap):.2f}")
    better = np.median(waist) < np.median(cap)
    print(f"    PREDICTION (waist better ordered, i.e. LOWER B): {'MET' if better else 'NOT MET'}")
    print(f"    Mann-Whitney p = {p:.4g}")
    print(f"    -> {'deposited particles were closed and consistent at the waist' if better else 'waist heterogeneity survived into the model'}")
