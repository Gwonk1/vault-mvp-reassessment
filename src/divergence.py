"""Sequence divergence test per DIVERGENCE_PREREGISTRATION.md."""
import gzip,io,json,sys,tarfile
import numpy as np, pandas as pd
TAR='data/raw/divergence/2759_trimmed_algs.tar'; MVP='2QPP0'; SEED=20261106
rng=np.random.default_rng(SEED)
z=np.load('data/processed/eggnog_presence.npz'); M,OG=z['M'],z['ogs'].tolist()
nsp=dict(zip(OG,M.sum(axis=1)))
def ident(fa):
    seqs=[];cur=[]
    for ln in fa.decode('utf8','ignore').splitlines():
        if ln.startswith('>'):
            if cur: seqs.append(''.join(cur)); cur=[]
        else: cur.append(ln.strip())
    if cur: seqs.append(''.join(cur))
    if len(seqs)<4: return None
    A=np.array([list(s.upper()) for s in seqs if len(s)==len(seqs[0])])
    if len(A)<4: return None
    n=len(A); pairs=[(i,j) for i in range(n) for j in range(i+1,n)]
    if len(pairs)>300: pairs=[pairs[k] for k in rng.choice(len(pairs),300,replace=False)]
    v=[]
    for i,j in pairs:
        m=(A[i]!='-')&(A[j]!='-')
        if m.sum()>=50: v.append((A[i][m]==A[j][m]).mean())
    return (float(np.mean(v)),len(seqs),A.shape[1]) if len(v)>=10 else None
T=tarfile.open(TAR)
names={m.name.split('/')[-1].split('.')[0]:m for m in T.getmembers() if m.name.endswith('.faa.gz')}
print('alignments in tar',len(names),flush=True)
def get(og):
    if og not in names: return None
    return ident(gzip.decompress(T.extractfile(names[og]).read()))
mv=get(MVP); print('MVP',MVP,'identity/nseq/len',mv,'species',nsp.get(MVP),flush=True)
lo,hi=nsp[MVP]*.85,nsp[MVP]*1.15
cand=[o for o in names if o in nsp and lo<=nsp[o]<=hi and o!=MVP]
rng.shuffle(cand); print('species-matched candidates',len(cand),flush=True)
rows=[]
for o in cand:
    r=get(o)
    if r and abs(r[2]-mv[2])<=.3*mv[2]: rows.append((o,)+r)
    if len(rows)>=400: break
D=pd.DataFrame(rows,columns=['og','ident','n','len'])
pct=float((D.ident<mv[0]).mean()*100)
print('matched groups used',len(D),'| MVP identity',round(mv[0],4),'| percentile',round(pct,1),flush=True)
print('matched identity quantiles',D.ident.quantile([.1,.25,.5,.75,.9]).round(3).to_dict(),flush=True)
lab='UNUSUALLY DIVERGENT' if pct<=10 else ('UNUSUALLY CONSERVED' if pct>=90 else 'TYPICAL')
ctrl={}
D.to_csv('results/divergence_matched.csv',index=False)
for g,og in [('histone H3 (KOG1745)','KOG1745'),('RPL7 (KOG3184)','KOG3184'),('RPS6 (KOG1646)','KOG1646'),('ACTB (KOG0676)','KOG0676'),('TEP1 grp','KOG3602'),('PARP4 grp','KOG1037')]:
    r=get(og); ctrl[g]=None if not r else (round(r[0],3),round(float((D.ident<r[0]).mean()*100),1))
    print(' ctrl',g,og,ctrl[g],flush=True)
print('LABEL',lab,flush=True)
json.dump({'mvp_identity':mv[0],'mvp_nseq':mv[1],'align_len':mv[2],'percentile':pct,'label':lab,
           'matched_n':len(D),'controls':ctrl},open('results/divergence.json','w'),indent=1,default=float)
