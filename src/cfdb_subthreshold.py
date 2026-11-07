"""Is MVP's sub-threshold co-elution neighbourhood translation machinery?
Pre-registered in CFDB_SUBTHRESHOLD_PREREGISTRATION.md. Degree-matched randoms."""
import gzip, json, numpy as np, pandas as pd
from collections import defaultdict

PATH='data/raw/cfdb/Homo_sapiens.tsv.gz'
SEEDS=['MVP','PSMA1','RPL7']
TRANS=['GOBP_TRANSLATION','GOCC_RIBOSOME','GOBP_CYTOPLASMIC_TRANSLATION',
       'GOCC_RIBONUCLEOPROTEIN_COMPLEX','GOBP_RNA_CATABOLIC_PROCESS']
COMP=['GOBP_ACTIN_FILAMENT_ORGANIZATION','GOCC_RUFFLE','GOBP_PLASMA_MEMBRANE_REPAIR',
      'GOBP_INFLAMMATORY_RESPONSE']
NEG=['GOCC_MITOCHONDRION']

sets={}
for f in ['data/raw/eggnog/c5.go.bp.v2024.1.Hs.symbols.gmt',
          'data/raw/eggnog/c5.go.cc.v2024.1.Hs.symbols.gmt']:
    for line in open(f):
        p=line.rstrip('\n').split('\t'); sets[p[0]]=set(p[2:])

scores=defaultdict(dict); deg=defaultdict(int)
with gzip.open(PATH,'rt') as fh:
    next(fh)
    for line in fh:
        p=line.rstrip('\n').split('\t')
        if len(p)<4: continue
        a,b=p[0].strip('"'),p[1].strip('"')
        try: s,pr=float(p[2]),float(p[3])
        except ValueError: continue
        if pr>=0.5: deg[a]+=1; deg[b]+=1
        if a in SEEDS: scores[a][b]=s
        if b in SEEDS: scores[b][a]=s
print('scored partners: '+', '.join(f'{k}={len(v)}' for k,v in scores.items()),flush=True)

uni=sorted(set().union(*[set(v) for v in scores.values()]))
dser=pd.Series([deg.get(g,0) for g in uni],index=uni)
dec=pd.qcut(dser.rank(method='first'),10,labels=False,duplicates='drop')
rng=np.random.default_rng(0)

def spec(gs,top,n=200):
    mem=[g for g in gs if g in dec.index]
    if len(mem)<5: return None
    obs=len(set(mem)&top); prof=dec.loc[mem].value_counts(); hits=0
    for _ in range(n):
        pick=[]
        for d_,k in prof.items():
            pool=dec.index[dec==d_]
            if len(pool)==0: continue
            pick+=list(rng.choice(pool,size=min(k,len(pool)),replace=False))
        if len(set(pick)&top)>=obs: hits+=1
    return {'n':len(mem),'obs':obs,'exp':round(len(mem)*len(top)/len(dec),1),'p':hits/n}

tops={s:set(pd.Series(scores[s]).sort_values(ascending=False).index[:200]) for s in SEEDS}

# GATES
g1=spec(sets.get('GOCC_PROTEASOME_COMPLEX',set()),tops['PSMA1'])
g2=spec(sets.get('GOCC_RIBOSOME',set()),tops['RPL7'])
gate=bool(g1 and g1['p']<0.05 and g2 and g2['p']<0.05)
print(f"\nGATE PSMA1->proteasome {g1}\nGATE RPL7->ribosome  {g2}\n  => {'PASS' if gate else 'FAIL'}",flush=True)

res={}
print('\nMVP top-200 by score, degree-matched specificity:')
for lbl,panel in (('TRANSLATION',TRANS),('COMPARATOR (dead)',COMP),('NEG CONTROL',NEG)):
    for t in panel:
        v=spec(sets.get(t,set()),tops['MVP']); res[t]=v
        flag='CLEARS' if v and v['p']<0.05 else ''
        print(f'  {lbl:<18} {t[:42]:<44} {v}  {flag}',flush=True)

tc=[t for t in TRANS if res.get(t) and res[t]['p']<0.05]
cc=[t for t in COMP if res.get(t) and res[t]['p']<0.05]
ng=[t for t in NEG if res.get(t) and res[t]['p']<0.05]
if not gate: verdict='UNINFORMATIVE (gate failed)'
elif ng: verdict='UNINTERPRETABLE - mitochondrion clears, degree matching inadequate'
elif tc and not cc: verdict=f'TRANSLATION NEIGHBOURHOOD SUPPORTED: {tc}'
elif tc and cc: verdict=f'NOT SPECIFIC - translation {tc} but dead comparators also clear {cc}'
else: verdict='KILL CONDITION MET - no translation term clears; §35d observation dropped'
print('\nVERDICT:',verdict,flush=True)
json.dump({'gate':gate,'gate_detail':{'psma1_proteasome':g1,'rpl7_ribosome':g2},
           'results':res,'translation_clearing':tc,'comparators_clearing':cc,
           'verdict':verdict},open('results/cfdb_subthreshold.json','w'),indent=1,default=str)
