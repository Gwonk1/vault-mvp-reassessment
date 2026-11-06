"""Promised in PERSISTER_DEVIATIONS.md 3: cycling vs non-cycling persisters, reported separately."""
import json,sys,numpy as np,pandas as pd
sys.path.insert(0,'src')
from persister import build,META,CHUNK,MIN_CELLS,MIN_DET,WATCH
meta=pd.read_csv(META,index_col=0)
M,genes,cells=build(); meta=meta.loc[cells]
tot=np.zeros(M.shape[1])
for a in range(0,M.shape[0],CHUNK): tot+=M[a:a+CHUNK].sum(axis=0)
cp=1e4/tot; line=meta.cell_line.values; st=meta.sample_type.values
out={}
for arm in ['cycling','non-cycling']:
    for m in pd.unique(line):
        w=(line==m)&((st==arm)|(st=='naive'))
        if ((line==m)&(st==arm)).sum()<MIN_CELLS or ((line==m)&(st=='naive')).sum()<MIN_CELLS: continue
        t=(st[w]==arm).astype(float); X=np.column_stack([np.ones(w.sum()),t]); P=np.linalg.pinv(X)
        b=[];d=[]
        for a in range(0,M.shape[0],CHUNK):
            L=np.log1p(np.asarray(M[a:a+CHUNK])*cp)[:,w]
            b.append(L@P.T[:,1]); d.append((L>0).mean(axis=1))
        s=pd.DataFrame({'raw':np.concatenate(b),'det':np.concatenate(d)},index=genes)
        s=s[s.det>=MIN_DET]; s['pct']=s.raw.rank(pct=True)*100
        out[f'{m}|{arm}']={g:(None if g not in s.index else round(float(s.pct[g]),1)) for g in ['MVP','TOP2A','B2M','ISG15']}
        print(f'{m} {arm}: n_treated {int((t==1).sum())} genes {len(s)}',out[f'{m}|{arm}'],flush=True)
json.dump(out,open('results/persister_split.json','w'),indent=1)
