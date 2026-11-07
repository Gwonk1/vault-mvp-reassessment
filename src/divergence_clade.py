"""Sensitivity: restrict the matched null to vertebrate-dominated groups, since MVP's group is 70% vertebrate."""
import numpy as np,pandas as pd,json
z=np.load('data/processed/eggnog_presence.npz'); M,OG,SP=z['M'],z['ogs'].tolist(),z['species']
tax=pd.read_csv('data/raw/eggnog/e5.taxid_info.tsv',sep='\t',dtype=str); tax.columns=['taxid','name','rank','names','lineage']; tax=tax.set_index('taxid')
nm=tax.names.reindex(SP).fillna('').values
isv=np.array(['Vertebrata' in x for x in nm])
frac={}
for i,o in enumerate(OG):
    p=M[i]
    if p.sum(): frac[o]=isv[p].mean()
D=pd.read_csv('results/divergence_matched.csv')
D['vfrac']=D.og.map(frac)
mvp=json.load(open('results/divergence.json'))
mv=mvp['mvp_identity']
print(f"MVP vertebrate fraction {frac['2QPP0']:.3f} | identity {mv:.4f}")
for thr in [0,.5,.6,.7]:
    S=D[D.vfrac>=thr]
    print(f' null restricted to >={thr:.0%} vertebrate: n={len(S)}, median identity {S.ident.median():.3f}, MVP percentile {100*(S.ident<mv).mean():.1f}')
S=D[D.vfrac>=.6]
json.dump({'mvp_vertebrate_fraction':float(frac['2QPP0']),'restricted_n':int(len(S)),
           'restricted_median_identity':float(S.ident.median()),
           'mvp_percentile_restricted':float(100*(S.ident<mv).mean()),
           'mvp_percentile_all':mvp['percentile']},open('results/divergence_clade.json','w'),indent=1)
