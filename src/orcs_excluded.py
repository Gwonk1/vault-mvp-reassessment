"""Descriptive only: MVP rows in screens outside the universe (activation, hits-only)."""
import sys,glob,os,pandas as pd
sys.path.insert(0,'src')
from orcs_classes import load_index
I=load_index().set_index('id'); rows=[]
for f in glob.glob('data/raw/orcs/screens/*.screen.tab.txt'):
    s=os.path.basename(f).split('SCREEN_')[1].split('-')[0]
    if s not in I.index or I.universe[s]: continue
    for l in open(f,errors='ignore'):
        p=l.split('\t')
        if len(p)>12 and p[3]=='MVP': rows.append((s,p[12],I.LIBRARY_METHODOLOGY[s],I.AUTHOR[s],I.cls[s],I.CONDITION_NAME[s],I.CELL_LINE[s],I.SCREEN_RATIONALE[s]))
d=pd.DataFrame(rows,columns='id hit lib author cls cond line why'.split()); d.to_csv('results/orcs_mvp_excluded.csv',index=False)
print(len(I[~I.universe]),'excluded screens; MVP rows',len(d),'hits',(d.hit=='YES').sum()); print(d[d.hit=='YES'].to_string(max_colwidth=46))
