"""CNA-adjusted co-abundance per CNA_PREREGISTRATION.md."""
import glob,json,os,time,sys
import numpy as np,pandas as pd,requests
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0,'src')
from prot_coabund import cohorts,vreml,MIN_MEAS,MIN_SAMP,MIN_COH
API='https://www.cbioportal.org/api'; S=requests.Session(); S.headers['Content-Type']='application/json'
PREF={'brain_cptac_2020':'brain_cptac_2020_log2CNA','brca_cptac_2020':'brca_cptac_2020_log2CNA',
 'brca_dldccc_2022':'brca_dldccc_2022_log2CNA','brca_tcga_pan_can_atlas_2018':'brca_tcga_pan_can_atlas_2018_log2CNA',
 'coad_cptac_2019':'coad_cptac_2019_log2CNA','coadread_tcga_pan_can_atlas_2018':'coadread_tcga_pan_can_atlas_2018_log2CNA',
 'gbm_cptac_2021':'gbm_cptac_2021_log2CNA','mng_utoronto_2021':'mng_utoronto_2021_log2CNA',
 'ov_tcga_pan_can_atlas_2018':'ov_tcga_pan_can_atlas_2018_log2CNA',
 'luad_cptac_2020':'luad_cptac_2020_gistic','ucec_cptac_2020':'ucec_cptac_2020_gistic'}
def req(m,p,**kw):
    for i in range(6):
        try:
            r=S.request(m,API+p,timeout=400,**kw)
            if r.status_code==200: return r.json()
        except requests.RequestException: pass
        time.sleep(2**i)
    raise RuntimeError(p)
genes=pd.DataFrame(req('GET','/genes?pageSize=100000&projection=SUMMARY'))
genes=genes[(genes.entrezGeneId>0)&(genes.type=='protein-coding')]
sym=dict(zip(genes.entrezGeneId,genes.hugoGeneSymbol)); ids=genes.entrezGeneId.tolist()
os.makedirs('data/processed/cna',exist_ok=True)
C=cohorts(True)
CN={}
for st,M in C.items():
    pid=PREF.get(st)
    if not pid: print('no CNA:',st,flush=True); continue
    f=f'data/processed/cna/{st}.parquet'
    if not os.path.exists(f):
        samples=list(M.columns); ch=[ids[i:i+2000] for i in range(0,len(ids),2000)]
        def one(c): return [(r['entrezGeneId'],r['sampleId'],r['value']) for r in
            req('POST',f'/molecular-profiles/{pid}/molecular-data/fetch?projection=SUMMARY',json={'entrezGeneIds':c,'sampleIds':samples})]
        with ThreadPoolExecutor(4) as ex: parts=list(ex.map(one,ch))
        d=pd.DataFrame([x for p in parts for x in p],columns=['e','s','v'])
        if not len(d): print('empty CNA',st,flush=True); continue
        d['v']=pd.to_numeric(d.v,errors='coerce')
        A=d.pivot_table(index='e',columns='s',values='v',aggfunc='first'); A.index=A.index.map(sym)
        A.columns=A.columns.astype(str); A.to_parquet(f)
    CN[st]=pd.read_parquet(f); print('CNA',st,CN[st].shape,flush=True)
def resid(y,x):
    m=np.isfinite(y)&np.isfinite(x)
    if m.sum()<20 or np.nanstd(x[m])==0: return y
    b=np.polyfit(x[m],y[m],1); out=y.copy(); out[m]=y[m]-np.polyval(b,x[m]); return out
zs={}
for st,M in C.items():
    if st not in CN: continue
    A=CN[st]; cols=[c for c in M.columns if c in A.columns]
    if len(cols)<MIN_SAMP: print('too few CNA-matched samples',st,len(cols),flush=True); continue
    P=M[cols]; P=P[P.notna().mean(axis=1)>=MIN_MEAS]
    if 'MVP' not in P.index or 'MVP' not in A.index: continue
    mv=resid(P.loc['MVP'].values.astype(float),A.loc['MVP',cols].values.astype(float))
    R=np.vstack([resid(P.loc[g].values.astype(float), A.loc[g,cols].values.astype(float) if g in A.index else np.full(len(cols),np.nan)) for g in P.index])
    Rr=pd.DataFrame(R,index=P.index).rank(axis=1).values
    mr=pd.Series(mv).rank().values
    m=np.isfinite(Rr)&np.isfinite(mr); n=m.sum(1)
    Rz=np.where(m,Rr,0); xz=np.where(m,mr,0)
    sx=xz.sum(1);sy=Rz.sum(1);sxy=(Rz*xz).sum(1);sx2=(xz**2).sum(1);sy2=(Rz**2).sum(1)
    den=np.sqrt(np.maximum((n*sx2-sx**2)*(n*sy2-sy**2),1e-12))
    r=np.where(n>=20,(n*sxy-sx*sy)/den,np.nan)
    zs[st]=pd.DataFrame({'z':np.arctanh(np.clip(r,-.999,.999)),'v':1/np.maximum(n-3,1)},index=P.index)
    print(f'  adjusted {st}: {len(P)} proteins, {len(cols)} samples',flush=True)
Z=pd.concat({k:v.z for k,v in zs.items()},axis=1); V=pd.concat({k:v.v for k,v in zs.items()},axis=1)
keep=Z.notna().sum(axis=1)>=MIN_COH; Z,V=Z[keep],V[keep]
mu,k=vreml(Z.values,V.values)
po=pd.DataFrame({'z':mu,'k':k},index=Z.index).dropna(); po['r']=np.tanh(po.z)
po=po.sort_values('z',ascending=False); po=po[po.index!='MVP']
po.to_parquet('data/processed/mvp_coabundance_cna.parquet')
n=len(po); rk=lambda g: int(list(po.index).index(g))+1 if g in po.index else None
print(f'\nCNA-adjusted ranking: {n} proteins, {len(zs)} cohorts',flush=True)
print('top 25:',list(po.index[:25]),flush=True)
old=pd.read_parquet('data/processed/mvp_coabundance.parquet'); old=old[old.index!='MVP']
ork=lambda g: int(list(old.index).index(g))+1 if g in old.index else None
print('\n%-10s %10s %10s'%('gene','unadj','CNA-adj'),flush=True)
for g in ['PARP4','TEP1','ANXA2','S100A10','CAPN2','CAPNS1','EHD4','IQGAP1','PYCARD','MAPK3','SULT1A3','ALDOA']:
    print('%-10s %10s %10s'%(g,ork(g),rk(g)),flush=True)
gate=(rk('PARP4') or 1e9)<=.01*n and (rk('TEP1') or 1e9)<=.01*n
print('\nGATE PARP4+TEP1 still top 1%:',gate,flush=True)
json.dump(dict(n=n,cohorts=list(zs),gate=bool(gate),top40=list(po.index[:40]),
  ranks={g:{'unadj':ork(g),'cna_adj':rk(g)} for g in ['PARP4','TEP1','ANXA2','S100A10','CAPN2','CAPNS1','EHD4','IQGAP1','PYCARD','MAPK3','SULT1A3','ALDOA']}),
  open('results/cna_adjusted.json','w'),indent=1,default=float)
