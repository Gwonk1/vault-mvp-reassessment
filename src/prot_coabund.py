"""Protein co-abundance per PROTEOMICS_PREREGISTRATION.md. Usage: prot_coabund.py controls|final"""
import glob,json,os,sys,re
import numpy as np, pandas as pd
from scipy.stats import hypergeom
sys.path.insert(0,'src')
from models import reml
P='data/processed/prot/'; MIN_PROT=2000; MIN_SAMP=50; MIN_MEAS=.5; MIN_COH=3
CTRL={'PSMA1':r'^PSM','NDUFS2':r'^NDUF','RPL7':r'^(RPL|RPS)'}

def cohorts(primary=True):
    out={}
    for f in sorted(glob.glob(P+'*.parquet')):
        st=os.path.basename(f)[:-8]
        if st.endswith('.clin'): continue
        if primary and st.startswith('ccle'): continue
        if not primary and not st.startswith('ccle'): continue
        M=pd.read_parquet(f)
        M=M[~M.index.duplicated()]
        if M.shape[0]<MIN_PROT or M.shape[1]<MIN_SAMP: continue
        c=P+st+'.clin.parquet'
        if os.path.exists(c):
            cl=pd.read_parquet(c).set_index('sampleId').reindex(M.columns)
            keep=[s for s in M.columns if not (re.search(r'-1[01]$',s) and False)]
            if 'patientId' in cl: keep=list(cl.loc[~cl.patientId.duplicated()].index)
            M=M[[k for k in keep if k in M.columns]]
        if M.shape[1]>=MIN_SAMP: out[st]=M
    return out

def corr_with(M,target):
    """Spearman of target against every row, pairwise-complete."""
    if target not in M.index: return None,0
    X=M.loc[[target]].values[0]
    ok=np.isfinite(X)
    if ok.sum()<MIN_SAMP: return None,0
    A=M.loc[:,M.columns[ok]]
    meas=A.notna().mean(axis=1)
    A=A[meas>=MIN_MEAS]
    R=A.rank(axis=1).values
    x=R[list(A.index).index(target)] if target in A.index else None
    if x is None: return None,0
    m=np.isfinite(R)&np.isfinite(x)
    n=m.sum(1); Rz=np.where(m,R,0); xz=np.where(m,x,0)
    sx=xz.sum(1); sy=Rz.sum(1); sxy=(Rz*xz).sum(1); sx2=(xz**2).sum(1); sy2=(Rz**2).sum(1)
    den=np.sqrt(np.maximum((n*sx2-sx**2)*(n*sy2-sy**2),1e-12))
    r=np.where(n>=20,(n*sxy-sx*sy)/den,np.nan)
    return pd.DataFrame({'r':r,'n':n},index=A.index), int(ok.sum())

def pooled(C,target):
    zs={}
    for st,M in C.items():
        d,_=corr_with(M,target)
        if d is None: continue
        z=np.arctanh(np.clip(d.r,-.999,.999)); v=1/np.maximum(d.n-3,1)
        zs[st]=pd.DataFrame({'z':z,'v':v})
    if len(zs)<2: return None
    Z=pd.concat({k:v.z for k,v in zs.items()},axis=1); V=pd.concat({k:v.v for k,v in zs.items()},axis=1)
    keep=Z.notna().sum(axis=1)>=MIN_COH
    Z,V=Z[keep],V[keep]
    est=[reml(Z.values[i],V.values[i])[:3] for i in range(len(Z))]
    out=pd.DataFrame(est,columns=['z','lo','hi'],index=Z.index)
    out['r']=np.tanh(out.z); out['k']=Z.notna().sum(axis=1)
    return out.sort_values('z',ascending=False)

def rm_pcs(M,k=3):
    A=M.copy()
    med=A.median(axis=1); A=A.T.fillna(med).T
    X=A.values; X=X-X.mean(axis=1,keepdims=True)
    U,S,Vt=np.linalg.svd(X,full_matrices=False)
    X2=X-(U[:,:k]*S[:k])@Vt[:k]
    return pd.DataFrame(X2,index=A.index,columns=A.columns).where(M.notna())

SETS={}
for f in ['c5.go.bp.v2024.1.Hs.symbols.gmt','c5.go.cc.v2024.1.Hs.symbols.gmt']:
    for l in open('data/raw/eggnog/'+f):
        p=l.rstrip('\n').split('\t'); SETS[p[0]]=set(p[2:])

def enrich(top,uni):
    T=set(top); U=set(uni); rows=[]
    for t,g in SETS.items():
        m=g&U
        if not 10<=len(m)<=500: continue
        k=len(T&m)
        if k: rows.append((t,k,len(m),hypergeom.sf(k-1,len(U),len(m),len(T))))
    r=pd.DataFrame(rows,columns=['term','k','K','p']).sort_values('p').reset_index(drop=True)
    if len(r): r['q']=(r.p*len(r)/(r.index+1)).iloc[::-1].cummin().iloc[::-1].clip(upper=1)
    return r

if __name__=='__main__':
    mode=sys.argv[1]
    C=cohorts(True)
    print('primary cohorts:',{k:v.shape for k,v in C.items()},flush=True)
    gate={}
    for g,pat in CTRL.items():
        po=pooled(C,g)
        if po is None: gate[g]=False; print('GATE',g,'no data',flush=True); continue
        top=[x for x in po.index[:21] if x!=g][:20]
        hit=sum(1 for x in top if re.match(pat,x))
        gate[g]=hit>=5
        print(f'GATE {g}: {hit}/20 same family ->','PASS' if gate[g] else 'FAIL','|',top[:10],flush=True)
    gate_pass=sum(gate.values())>=2
    print('GATE overall:','PASS' if gate_pass else 'FAIL',flush=True)
    res={'gate':gate,'gate_pass':gate_pass,'cohorts':{k:list(v.shape) for k,v in C.items()}}
    if mode=='final':
        po=pooled(C,'MVP'); uni=list(po.index)
        rk=lambda g:(None if g not in po.index else int(list(po.index).index(g))+1)
        n=len(po)
        print(f'\nMVP universe {n} proteins, cohorts {po.k.median():.0f} median',flush=True)
        for g in ['TEP1','PARP4']:
            r=rk(g); print(' ',g,'rank',r,'of',n,None if r is None else f'top {100*r/n:.2f}%',
                  po.loc[g,['r','lo','hi','k']].round(3).to_dict() if g in po.index else 'ABSENT',flush=True)
        t1,t4=rk('TEP1'),rk('PARP4')
        intop=lambda r,p: r is not None and r<=p*n
        if intop(t1,.01) and intop(t4,.01): lab='UNIT'
        elif intop(t1,.01) or intop(t4,.01): lab='PARTIAL'
        elif (t1 is None or not intop(t1,.05)) and (t4 is None or not intop(t4,.05)): lab='NOT A UNIT'
        else: lab='UNRESOLVED'
        print('PRIMARY A:',lab,flush=True)
        print('\ntop 40 co-abundant with MVP:',flush=True)
        print(po.head(40)[['r','lo','hi','k']].round(3).to_string(),flush=True)
        e=enrich(list(po.index[:100]),uni)
        print('\ntop terms:',flush=True); print(e.head(12).round(5).to_string(max_colwidth=58),flush=True)
        res.update(label_A=lab,tep1_rank=t1,parp4_rank=t4,n=n,
                   top40=[(g,float(po.r[g])) for g in po.index[:40]],
                   terms=e.head(20).to_dict('records'))
        po.to_parquet('data/processed/mvp_coabundance.parquet')
        json.dump(res,open('results/prot_final.json','w'),indent=1,default=float)
    else:
        json.dump(res,open('results/prot_controls.json','w'),indent=1,default=float)
