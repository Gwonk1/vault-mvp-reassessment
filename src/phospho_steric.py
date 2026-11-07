"""Part 1 of PHOSPHO_PREREGISTRATION: can a kinase reach MVP's phosphosites in the closed 78-mer?"""
import gzip,json,numpy as np,pandas as pd
SITES=[445,585,867,873,876]
rows=[]
for l in gzip.open('data/raw/struct/11JB.cif.gz','rt'):
    if l.startswith('ATOM'):
        f=l.split()
        try: rows.append((f[5],f[6],int(f[8]),float(f[10]),float(f[11]),float(f[12]),f[3]))
        except Exception: pass
D=pd.DataFrame(rows,columns=['res','chain','seq','x','y','z','atom'])
P=D[['x','y','z']].values
C=P.mean(0); X=P-C
w,V=np.linalg.eigh(np.cov(X.T)); axis=V[:,np.argmax(w)]
d=P-C; pz=d@axis; pr=np.linalg.norm(d-np.outer(pz,axis),axis=1)
# angular coordinate around the axis
e1=V[:,np.argsort(w)[0]]; e2=np.cross(axis,e1)
pa=np.arctan2(d@e2,d@e1)
D['z_ax']=pz; D['r_ax']=pr; D['ang']=pa
print(f'11JB: {len(D)} protein atoms | z {pz.min():.0f}..{pz.max():.0f} | r {pr.min():.0f}..{pr.max():.0f}',flush=True)
out=[]
for s in SITES:
    sub=D[D.seq==s]
    if not len(sub): out.append(dict(site=s,status='not resolved in structure')); print(f'  S{s}: NOT RESOLVED'); continue
    # use one representative copy (all 78 are symmetric); take side-chain-ish atoms
    ch=sub.chain.iloc[0]; one=sub[sub.chain==ch]
    zc=float(one.z_ax.mean()); rc=float(one.r_ax.mean()); ac=float(one.ang.mean())
    slab=(np.abs(D.z_ax.values)>=abs(zc)-7.5)&(np.abs(D.z_ax.values)<=abs(zc)+7.5)
    shell=D.r_ax.values[slab]
    inner,outer=np.percentile(shell,[2,98])
    frac=(rc-inner)/max(outer-inner,1e-9)
    # radial clearance: protein atoms further out, within a local window in z and arc
    dz=np.abs(D.z_ax.values-zc); darc=np.abs(np.angle(np.exp(1j*(D.ang.values-ac))))*np.maximum(D.r_ax.values,1)
    for probe in (1.4,5.0):
        pass
    blockers={}
    for probe in (1.4,5.0):
        win=probe+2.0
        blocked=((D.r_ax.values>rc+1.0)&(dz<win)&(darc<win)).sum()
        blockers[probe]=int(blocked)
    lum={}
    for probe in (1.4,5.0):
        win=probe+2.0
        lum[probe]=int(((D.r_ax.values<rc-1.0)&(dz<win)&(darc<win)).sum())
    out.append(dict(site=s,aa=one.res.iloc[0],z=round(zc,1),r=round(rc,1),inner=round(inner,1),outer=round(outer,1),
                    frac_depth=round(frac,3),blockers_outward_1p4=blockers[1.4],blockers_outward_5p0=blockers[5.0],
                    blockers_inward_5p0=lum[5.0],copies=int(sub.chain.nunique())))
    print(f"  S{s} ({one.res.iloc[0]}): r={rc:.1f} shell[{inner:.0f},{outer:.0f}] depth={frac:.2f} | atoms blocking outward path: {blockers[1.4]} (1.4A win) / {blockers[5.0]} (5A win) | inward: {lum[5.0]}",flush=True)
R=pd.DataFrame(out)
R.to_csv('results/phospho_steric.csv',index=False)
res=R[R.get('frac_depth').notna()] if 'frac_depth' in R else R
occluded=[int(r.site) for _,r in res.iterrows() if r.blockers_outward_5p0>0]
lab='SHELL MUST OPEN' if occluded else 'NO EVIDENCE (all sites exterior-accessible)'
print(f'\nsites with protein blocking the outward path at kinase scale: {occluded}')
print('VERDICT:',lab)
json.dump(dict(verdict=lab,occluded_sites=occluded,sites=R.to_dict('records')),open('results/phospho_steric.json','w'),indent=1,default=float)
