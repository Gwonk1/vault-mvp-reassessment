"""Where does the bound ADP-ribose sit: lumenal, mid-shell (transmural), or exterior? PDB 11JB."""
import gzip,json,numpy as np,pandas as pd
rows=[]
for l in gzip.open('data/raw/struct/11JB.cif.gz','rt'):
    if l.startswith(('ATOM','HETATM')):
        f=l.split()
        try: rows.append((f[0],f[5],f[6],f[8],float(f[10]),float(f[11]),float(f[12])))
        except Exception: pass
D=pd.DataFrame(rows,columns=['rec','res','chain','seq','x','y','z'])
print('atoms',len(D),'| hetero residues:',D[D.rec=='HETATM'].res.value_counts().to_dict(),flush=True)
P=D[D.rec=='ATOM'][['x','y','z']].values
C=P.mean(0); X=P-C
w,V=np.linalg.eigh(np.cov(X.T)); axis=V[:,np.argmax(w)]
def cyl(A):
    d=A-C; zz=d@axis; rr=np.linalg.norm(d-np.outer(zz,axis),axis=1); return zz,rr
pz,pr=cyl(P)
print(f'protein: n={len(P)} z {pz.min():.0f}..{pz.max():.0f} r {pr.min():.0f}..{pr.max():.0f}',flush=True)
L=D[(D.rec=='HETATM')&(D.res=='AR6')]
lz,lr=cyl(L[['x','y','z']].values)
print(f'AR6 atoms {len(L)} | z {lz.min():.0f}..{lz.max():.0f} | r {lr.min():.0f}..{lr.max():.0f}',flush=True)
# per-AR6 molecule centroid
L=L.copy(); L['z_ax']=lz; L['r_ax']=lr
grp=L.groupby(['chain','seq'])[['z_ax','r_ax']].mean()
print('AR6 copies (by chain):',len(grp),flush=True)
res=[]
for ch,row in grp.iterrows():
    ch=str(ch)
    z,r=row.z_ax,row.r_ax
    m=(np.abs(pz)>=abs(z)-7.5)&(np.abs(pz)<=abs(z)+7.5)
    if m.sum()<500: continue
    shell=pr[m]
    inner,outer=np.percentile(shell,[2,98]); mid=np.median(shell)
    frac=(r-inner)/max(outer-inner,1e-9)
    res.append(dict(chain=ch,z=z,r=r,inner=inner,outer=outer,mid=mid,frac=frac,
                    pct_protein_inside=float((shell<r).mean()*100)))
R=pd.DataFrame(res)
R.to_csv('results/pocket_geometry.csv',index=False)
print(f'\nshell position of AR6 (0 = inner/lumen surface, 1 = outer surface):',flush=True)
print(R[['z','r','inner','outer','frac','pct_protein_inside']].describe().loc[['mean','50%','min','max']].round(2).to_string(),flush=True)
f=R.frac.median(); pin=R.pct_protein_inside.median()
verdict=('LUMENAL (inner third)' if f<.33 else 'EXTERIOR (outer third)' if f>.67 else 'MID-SHELL / TRANSMURAL-CAPABLE')
print(f'\nmedian fractional depth {f:.3f} | median % of shell protein radially inside the ligand {pin:.1f}%',flush=True)
print('VERDICT:',verdict,flush=True)
json.dump(dict(n_ar6_copies=int(len(R)),median_frac_depth=float(f),median_pct_protein_inside=float(pin),
   median_r=float(R.r.median()),median_inner=float(R.inner.median()),median_outer=float(R.outer.median()),
   verdict=verdict),open('results/pocket_geometry.json','w'),indent=1)
