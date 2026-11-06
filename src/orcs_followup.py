"""Exploratory, after the verdict: direction of MVP hits, fragility of the genotoxic p, baseline rarity."""
import sys,glob,numpy as np,pandas as pd
sys.path.insert(0,'src')
from orcs_run import *
R=run(); U,M,g=R['U'],R['M'],list(R['genes'])
i=g.index('MVP'); h=U[M[i]==2]
for _,r in h.iterrows():
    f=glob.glob(f"data/raw/orcs/screens/*SCREEN_{r.id}-*")[0]
    d=pd.read_csv(f,sep='\t',dtype=str,quoting=3); x=d[d.OFFICIAL_SYMBOL=='MVP'].iloc[0]
    sc={r[f'SCORE.{k}_TYPE']:x[f'SCORE.{k}'] for k in range(1,6) if r[f'SCORE.{k}_TYPE']!='-'}
    print(r.id,r.AUTHOR,'|',r.CONDITION_NAME,'|',r.CELL_LINE,'|',r.SCREEN_TYPE,'|',r.SCREEN_RATIONALE,'| hits',int(r.NUMBER_OF_HITS),'of',int(r.SCORES_SIZE),f"({r.NUMBER_OF_HITS/r.SCORES_SIZE:.0%})",'|',r.SIGNIFICANCE_CRITERIA[:70],'|',sc)
# all screens MVP tested in genotoxic class, by paper
w=U.cls=='genotoxic'; print('\ngenotoxic: tested',int((M[i,w]>0).sum()),'hit',int((M[i,w]==2).sum()),'papers',U[w].SOURCE_ID.nunique())
# fragility: drop screens calling >25% of genes hits, then recompute class p
def classp(mask):
    s=np.nan_to_num(scores(M,U,mask)); r=np.nan_to_num(scores(M,U,~mask)); o=np.argsort(r,kind='stable'); rk=int(np.where(o==i)[0][0]); N=len(s); a=max(0,min(rk-500,N-1001)); win=o[a:a+1001]; win=win[win!=i]
    return s[i],(1+(s[win]>=s[i]).sum())/(len(win)+1)
print('genotoxic all',classp(w.values))
frac=(U.NUMBER_OF_HITS/U.SCORES_SIZE).values
print('genotoxic, screens with <25% of genes as hits only',classp(w.values&(frac<.25)),'dropped',int((w.values&(frac>=.25)).sum()))
for c in ['FANCA','FANCD2','XRCC1']:
    j=g.index(c); print(c,'genotoxic tested',int((M[j,w]>0).sum()),'hits',int((M[j,w]==2).sum()),'papers',int(R['npap'].loc[c,'genotoxic']),'raw p',round(R['p'].loc[c,'genotoxic'],4))
print('MVP-like count: genes with p<=MVP genotoxic p', round((R['p']['genotoxic']<=R['p'].loc['MVP','genotoxic']).mean(),4))
print('any class raw p<=.049 among all genes', round((R['p']<=.049).any(axis=1).mean(),3))
# baseline
b=(U.cls=='baseline_fitness').values; t=(M[:,b]>0).sum(axis=1); hh=(M[:,b]==2).sum(axis=1)
print('\nbaseline: MVP tested',int(t[i]),'hits',int(hh[i]),'; genes with 0 baseline hits',round((hh==0).mean(),3),'; median hits per gene',float(np.median(hh)))
for c in ['MVP','TEP1','PARP4','STAT1','RPL3']:
    j=g.index(c); print(' ',c,'baseline hits',int(hh[j]),'of',int(t[j]),'overall pct',round((R['overall']<R['overall'][c]).mean()*100,1))
