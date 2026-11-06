"""Collect plotted values into one JSON."""
import sys,json,numpy as np,pandas as pd
sys.path.insert(0,'src')
from models import load,zgenes,score,SETS,TARGET_ALIASES
b=json.load(open('results/bulk.json')); k=json.load(open('results/sc_kim.json')); j=json.load(open('results/sc_jerby.json'))
per=b['primary']['per']
forest=[dict(name=n,n=v['n'],ba=v['ba'],bc=v['bc'],sa=v['va']**.5,sc=v['vc']**.5) for n,v in per.items()]
pool=b['primary']['t']
tests=[('Bulk ICB pool',b['primary']['t'],b['primary']['null']),('Lung malignant',k['kim_malignant']['t'],k['kim_malignant']['null']),('Melanoma malignant',j['jerby_malignant']['t'],j['jerby_malignant']['null'])]
nulls=[dict(name=a,d=t['d'],pct=n['pct_genome'],bg=n['bg_q'],isg=n['isg_q'],ifng=n['ifng_q'],auc=n.get('auc',n.get('auc_members'))) for a,t,n in tests]
pts={'lung':pd.read_csv('results/kim_malignant.patients.csv'),'mel':pd.read_csv('results/jerby_malignant.patients.csv')}
pp={x:d[['patient','n','rho_a','rho_c','d']].round(3).to_dict('records') for x,d in pts.items()}
sc={}
for n in ['imvigor','liu']:
    m,_,_=load(n); z=zgenes(m[m.std(axis=1)>0]).dropna(); z1=z.drop(index=[g for g in TARGET_ALIASES if g in z.index])
    sc[n]=dict(mvp=z.loc['MVP'].round(3).tolist(),a=score(z1,SETS['ISG_RS'])[0].round(3).tolist(),c=score(z1,SETS['IFNG_GS'])[0].round(3).tolist())
json.dump(dict(forest=forest,pool=pool,nulls=nulls,patients=pp,scatter=sc),open('results/figdata.json','w'))
print({k:len(v) for k,v in dict(forest=forest,nulls=nulls).items()}, sum(f['n'] for f in forest))
