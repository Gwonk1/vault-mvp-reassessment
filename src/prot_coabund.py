"""Protein co-abundance per PROTEOMICS_PREREGISTRATION.md + PROTEOMICS_DEVIATIONS.md (items 4-6).
Usage: prot_coabund.py controls|final"""
import glob,json,os,re,sys
import numpy as np, pandas as pd
from scipy.stats import hypergeom
from concurrent.futures import ProcessPoolExecutor
P='data/processed/prot/'; MIN_PROT=2000; MIN_SAMP=50; MIN_MEAS=.5; MIN_COH=3
DROP={'brca_tcga','coadread_tcga','ov_tcga'}          # deviation 4: legacy duplicates of PanCanAtlas
CTRL={'PSMA1':r'^PSM','NDUFS2':r'^NDUF','RPL7':r'^(RPL|RPS)'}
SEED=20261106

def cohorts(primary=True):
    out={}
    for f in sorted(glob.glob(P+'*.parquet')):
        st=os.path.basename(f)[:-8]
        if st.endswith('.clin'): continue
        if st in DROP: continue
        if primary==st.startswith('ccle'): continue
        M=pd.read_parquet(f); M=M[~M.index.duplicated()]
        if M.shape[0]<MIN_PROT or M.shape[1]<MIN_SAMP: continue
        c=P+st+'.clin.parquet'
        if os.path.exists(c):
            cl=pd.read_parquet(c).set_index('sampleId').reindex(M.columns)
            keep=[s for s in M.columns if not re.search(r'-1[01]$',s)]      # deviation 5: drop normals
            cl=cl.loc[keep]
            if 'patientId' in cl: keep=list(cl.loc[~cl.patientId.duplicated()].index)
            M=M[[k for k in keep if k in M.columns]]
        if M.shape[1]>=MIN_SAMP: out[st]=M
    return out

def ranks(M,target):
    if target not in M.index: return None
    X=M.loc[target].values; ok=np.isfinite(X)
    if ok.sum()<MIN_SAMP: return None
    A=M.loc[:,M.columns[ok]]
    A=A[A.notna().mean(axis=1)>=MIN_MEAS]
    if target not in A.index: return None
    R=A.rank(axis=1).values; x=R[list(A.index).index(target)]
    m=np.isfinite(R)&np.isfinite(x); n=m.sum(1)
    Rz=np.where(m,R,0); xz=np.where(m,x,0)
    sx=xz.sum(1);sy=Rz.sum(1);sxy=(Rz*xz).sum(1);sx2=(xz**2).sum(1);sy2=(Rz**2).sum(1)
    den=np.sqrt(np.maximum((n*sx2-sx**2)*(n*sy2-sy**2),1e-12))
    r=np.where(n>=20,(n*sxy-sx*sy)/den,np.nan)
    return pd.DataFrame({'r':r,'n':n},index=A.index)

def vreml(Y,V,iters=60):
    """Vectorised Paule-Mandel random-effects pooling. Y,V: (genes,k) with NaN."""
    m=np.isfinite(Y)&np.isfinite(V)&(V>0)
    k=m.sum(1); t2=np.zeros(len(Y))
    Yz=np.where(m,Y,0); Vz=np.where(m,V,1)
    for _ in range(iters):
        w=np.where(m,1/(Vz+t2[:,None]),0); sw=w.sum(1)
        mu=(w*Yz).sum(1)/np.maximum(sw,1e-12)
        Q=(w*(Yz-mu[:,None])**2*m).sum(1)
        t2=np.maximum(0,t2+(Q-(k-1))/np.maximum(sw,1e-12))
    w=np.where(m,1/(Vz+t2[:,None]),0); sw=w.sum(1)
    mu=np.where(sw>0,(w*Yz).sum(1)/np.maximum(sw,1e-12),np.nan)
    return mu,k

def profile(C,target):
    zs={}
    for st,M in C.items():
        d=ranks(M,target)
        if d is None: continue
        zs[st]=pd.DataFrame({'z':np.arctanh(np.clip(d.r,-.999,.999)),'v':1/np.maximum(d.n-3,1)})
    if len(zs)<2: return None
    Z=pd.concat({k:v.z for k,v in zs.items()},axis=1); V=pd.concat({k:v.v for k,v in zs.items()},axis=1)
    keep=Z.notna().sum(axis=1)>=MIN_COH; Z,V=Z[keep],V[keep]
    mu,k=vreml(Z.values,V.values)
    out=pd.DataFrame({'z':mu,'k':k},index=Z.index).dropna()
    out['r']=np.tanh(out.z)
    return out.sort_values('z',ascending=False)

def rm_pcs(M,k=3):
    med=M.median(axis=1); A=M.T.fillna(med).T
    X=A.values-A.values.mean(axis=1,keepdims=True)
    U,S,Vt=np.linalg.svd(X,full_matrices=False)
    return pd.DataFrame(X-(U[:,:k]*S[:k])@Vt[:k],index=A.index,columns=A.columns).where(M.notna())

SETS={}
for f in ['c5.go.bp.v2024.1.Hs.symbols.gmt','c5.go.cc.v2024.1.Hs.symbols.gmt']:
    for l in open('data/raw/eggnog/'+f):
        p=l.rstrip('\n').split('\t'); SETS[p[0]]=set(p[2:])

def enrich(top,uni):
    T=set(top); U=set(uni); rows=[]
    for t,g in SETS.items():
        m=g&U
        if not 10<=len(m)<=500: continue
        kk=len(T&m)
        if kk: rows.append((t,kk,len(m),hypergeom.sf(kk-1,len(U),len(m),len(T))))
    r=pd.DataFrame(rows,columns=['term','k','K','p']).sort_values('p').reset_index(drop=True)
    if len(r): r['q']=(r.p*len(r)/(r.index+1)).iloc[::-1].cummin().iloc[::-1].clip(upper=1)
    return r

_C=None
def _init(C): 
    global _C; _C=C
def _one(g):
    po=profile(_C,g)
    if po is None or len(po)<200: return None
    e=enrich(list(po.index[:100]),list(po.index))
    return (g,float(po.r.abs().median()),set(e[e.q<.05].term) if len(e) else set())

if __name__=='__main__':
    mode=sys.argv[1]; C=cohorts(True)
    print('primary cohorts (%d):'%len(C),{k:list(v.shape) for k,v in C.items()},flush=True)
    gate={}
    for g,pat in CTRL.items():
        po=profile(C,g)
        if po is None: gate[g]=False; print('GATE',g,'no data',flush=True); continue
        top=[x for x in po.index[:21] if x!=g][:20]; hit=sum(1 for x in top if re.match(pat,x))
        gate[g]=hit>=5; print(f'GATE {g}: {hit}/20 same family ->','PASS' if gate[g] else 'FAIL','|',top[:8],flush=True)
    gp=sum(gate.values())>=2; print('GATE overall:','PASS' if gp else 'FAIL',flush=True)
    res={'gate':gate,'gate_pass':gp,'cohorts':{k:list(v.shape) for k,v in C.items()},'dropped_duplicates':sorted(DROP)}
    if mode=='final':
        po=profile(C,'MVP'); uni=list(po.index); n=len(po)
        rk=lambda g: None if g not in po.index else int(list(po.index).index(g))+1
        t1,t4=rk('TEP1'),rk('PARP4')
        print(f'\nMVP universe {n} | median cohorts {po.k.median():.0f}',flush=True)
        for g in ['TEP1','PARP4']:
            r=rk(g); print(' ',g,'rank',r,'of',n,'' if r is None else f'(top {100*r/n:.2f}%)',
                            po.loc[g,['r','k']].round(3).to_dict() if g in po.index else 'ABSENT',flush=True)
        it=lambda r,p: r is not None and r<=p*n
        lab=('UNIT' if it(t1,.01) and it(t4,.01) else 'PARTIAL' if it(t1,.01) or it(t4,.01)
             else 'NOT A UNIT' if (t1 is None or not it(t1,.05)) and (t4 is None or not it(t4,.05)) else 'UNRESOLVED')
        print('PRIMARY A:',lab,flush=True)
        print('\ntop 30:',flush=True); print(po.head(30)[['r','k']].round(3).to_string(),flush=True)
        e=enrich(list(po.index[:100]),uni)
        print('\ntop terms:',flush=True); print(e.head(10).round(5).to_string(max_colwidth=56),flush=True)
        # deviation 6a: 200 matched random queries for specificity
        meas=pd.Series({g:sum(1 for M in C.values() if g in M.index) for g in uni})
        mvp_med=float(po.r.abs().median())
        pool=[g for g in uni if g!='MVP' and abs(meas[g]-meas['MVP'])<=.1*meas['MVP']]
        rng=np.random.default_rng(SEED); rng.shuffle(pool)
        hits={}; used=0
        with ProcessPoolExecutor(6,initializer=_init,initargs=(C,)) as ex:
            for out in ex.map(_one,pool[:600],chunksize=4):
                if out is None: continue
                g,med,terms=out
                if abs(med-mvp_med)>.05: continue
                used+=1
                for t in terms: hits[t]=hits.get(t,0)+1
                if used>=200: break
        e['spec']=e.term.map(lambda t:hits.get(t,0)/max(used,1))
        e.to_csv('results/prot_enrichment_full.csv',index=False)
        json.dump({'used':used,'hits':hits},open('results/prot_matched_hits.json','w'),indent=1)
        sig=e[e.q<.05]
        print(f'  q<.05 terms: {len(sig)} | passing spec<0.05: {int((sig.spec<.05).sum())}',flush=True)
        for _,r in sig[sig.spec<.05].iterrows(): print('   DECIDING TERM:',r.term,'k',r.k,'K',r.K,'q',round(r.q,5),'spec',r.spec,flush=True)
        labB=('MODULE LEAD' if len(sig) and (sig.spec<.05).any() else 'NON-SPECIFIC' if len(sig) else 'NO MODULE')
        print(f'\nmatched queries used {used} | PRIMARY B: {labB}',flush=True)
        if len(sig): print(sig.head(10).round(4).to_string(max_colwidth=52),flush=True)
        # deviation 6b: 3-PC sensitivity
        Cp={k:rm_pcs(v) for k,v in C.items()}
        po2=profile(Cp,'MVP'); n2=len(po2)
        r1=None if 'TEP1' not in po2.index else int(list(po2.index).index('TEP1'))+1
        r4=None if 'PARP4' not in po2.index else int(list(po2.index).index('PARP4'))+1
        print(f'\n3-PC removed: universe {n2} | TEP1 rank {r1} | PARP4 rank {r4} | top10 {list(po2.index[:10])}',flush=True)
        e2=enrich(list(po2.index[:100]),list(po2.index)); e2['spec']=e2.term.map(lambda t:hits.get(t,0)/max(used,1))
        e2.to_csv('results/prot_enrichment_3pc.csv',index=False)
        s2=e2[(e2.q<.05)]
        print(f'  3-PC: q<.05 terms {len(s2)}, spec<0.05 {int((s2.spec<.05).sum())} | top:',list(s2.term[:4]),flush=True)
        # deviation 6c: CCLE cell-line replication
        CC=cohorts(False); rep=None
        if CC:
            print('\nCCLE replication cohorts:',{k:list(v.shape) for k,v in CC.items()},flush=True)
            d=ranks(list(CC.values())[0],'MVP')
            if d is not None:
                d=d.sort_values('r',ascending=False)
                rr=lambda g: None if g not in d.index else int(list(d.index).index(g))+1
                rep={'n':len(d),'TEP1':rr('TEP1'),'PARP4':rr('PARP4'),'top10':list(d.index[1:11])}
                print(' CCLE:',rep,flush=True)
                e3=enrich(list(d.index[:100]),list(d.index)); e3['spec']=e3.term.map(lambda t:hits.get(t,0)/max(used,1))
                e3.to_csv('results/prot_enrichment_ccle.csv',index=False)
                s3=e3[e3.q<.05]
                print(f'  CCLE: q<.05 terms {len(s3)}, spec<0.05 {int((s3.spec<.05).sum())} | top:',list(s3.term[:6]),flush=True)
                rep['terms']=s3.head(12).to_dict('records')
        res.update(label_A=lab,label_B=labB,tep1_rank=t1,parp4_rank=t4,n=n,matched_used=used,
                   top40=[(g,float(po.r[g])) for g in po.index[:40]],terms=e.head(60).to_dict('records'),
                   pc3={'n':n2,'tep1':r1,'parp4':r4,'top10':list(po2.index[:10])},ccle=rep)
        po.to_parquet('data/processed/mvp_coabundance.parquet')
    json.dump(res,open(f'results/prot_{mode}.json','w'),indent=1,default=float)
