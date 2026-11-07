"""Zheng 2025 V5-TurboID contact test. Pre-registered in TURBOID_PREREGISTRATION.md."""
import pandas as pd, numpy as np, json, warnings
warnings.filterwarnings('ignore')
from scipy.stats import hypergeom

XL='data/raw/zheng2025/Supplementary_Table_2.xlsx'
BAITS=['PARP1','PARP2','PARP3','PARP4','PARP5A','PARP5B','PARP6','PARP7','PARP8','PARP9',
       'PARP10','PARP11','PARP12','PARP13','PARP14','PARP15','PARP16']
FC,PV=' Log2(FoldChange)','P.value'
FAVOURED=['GOBP_PLASMA_MEMBRANE_REPAIR','GOCC_CAVEOLA','GOBP_PLASMA_MEMBRANE_ORGANIZATION',
          'GOCC_LATE_ENDOSOME','GOBP_ENDOSOMAL_TRANSPORT']
IMMUNE=['GOBP_INFLAMMATORY_RESPONSE','GOBP_RESPONSE_TO_BACTERIUM','GOCC_RUFFLE',
        'GOBP_ANTIGEN_PROCESSING_AND_PRESENTATION']
NAMED=['MVP','PARP4','TEP1','ANXA2','S100A10','EHD2','EHD4','CAPN2','MYOF','AHNAK',
       'IQGAP1','CD63','OPTN','VPS35','FLOT1','FLOT2']

sets={}
for f in ['data/raw/eggnog/c5.go.bp.v2024.1.Hs.symbols.gmt',
          'data/raw/eggnog/c5.go.cc.v2024.1.Hs.symbols.gmt']:
    for line in open(f):
        p=line.rstrip('\n').split('\t'); sets[p[0]]=set(p[2:])

sheets={}
for b in BAITS:
    d=pd.read_excel(XL,sheet_name=b)
    d=d.dropna(subset=['Gene Symbol']).copy()
    d['Gene Symbol']=d['Gene Symbol'].astype(str).str.strip()
    d=d.drop_duplicates('Gene Symbol').set_index('Gene Symbol')
    sheets[b]=d
    print(f'  {b:<8} {len(d)} preys',flush=True)

def enriched(d,g):
    if g not in d.index: return None
    r=d.loc[g]
    return {'fc':float(r[FC]),'p':float(r[PV]),
            'hit':bool(r[FC]>1 and r[PV]<0.05)}

# --- GATE ---
self_hits={b:enriched(sheets[b],b) for b in BAITS}
n_self=sum(1 for b,v in self_hits.items() if v and v['hit'])
g1=bool(self_hits['PARP4'] and self_hits['PARP4']['hit'])
g2=n_self>=12
print(f"\nGATE1 PARP4 self-labelling: {self_hits['PARP4']} -> {'PASS' if g1 else 'FAIL'}",flush=True)
print(f'GATE2 baits enriching own symbol: {n_self}/17 -> {"PASS" if g2 else "FAIL"}',flush=True)

p4=sheets['PARP4']
# --- PRIMARY: MVP ---
mvp=enriched(p4,'MVP')
others={b:enriched(sheets[b],'MVP') for b in BAITS if b!='PARP4'}
meas={b:v['fc'] for b,v in others.items() if v}
spec_n=sum(1 for v in meas.values() if (mvp and mvp['fc']>v))
print(f'\nPRIMARY MVP in PARP4: {mvp}',flush=True)
print(f'  MVP measured in {len(meas)} of 16 other baits; PARP4 fc exceeds {spec_n} of them',flush=True)
print(f'  other-bait MVP fc: {dict(sorted(meas.items(), key=lambda kv:-kv[1])[:6])}',flush=True)
specific=bool(mvp and mvp['hit'] and spec_n>=14)
if not(g1 and g2): verdict='UNINFORMATIVE (gate failed)'
elif mvp and mvp['hit'] and specific: verdict='MVP IS PARP4-PROXIMAL AND SPECIFIC'
elif mvp and mvp['hit']: verdict=f'MVP ENRICHED but specificity only {spec_n}/16'
elif mvp: verdict='KILL CONDITION MET - MVP present and NOT enriched'
else: verdict='MVP ABSENT from PARP4 sheet (uninformative on presence)'
print('VERDICT:',verdict,flush=True)

tep1=enriched(p4,'TEP1')
print(f'SECONDARY TEP1 in PARP4: {tep1}',flush=True)

# --- TERTIARY: term enrichment among PARP4-proximal ---
p4=p4[np.isfinite(p4[FC])&np.isfinite(p4[PV])]
prox=set(p4.index[(p4[FC]>1)&(p4[PV]<0.05)])
uni=set(p4.index); N=len(uni); K=len(prox)
print(f'\nPARP4-proximal set: {K} of {N} measured proteins',flush=True)
abund=p4['# Unique Peptides'].reindex(list(uni))
dec=pd.qcut(abund.rank(method='first'),10,labels=False,duplicates='drop')
rng=np.random.default_rng(0)
def spec_test(gs,n=200):
    mem=[g for g in gs if g in uni]
    if len(mem)<5: return None
    obs=len(set(mem)&prox); prof=dec.loc[mem].value_counts(); hits=0
    for _ in range(n):
        pick=[]
        for d_,k in prof.items():
            pool=dec.index[dec==d_]
            if len(pool)==0: continue
            pick+=list(rng.choice(pool,size=min(k,len(pool)),replace=False))
        if len(set(pick)&prox)>=obs: hits+=1
    return {'n':len(mem),'obs':obs,'exp':round(len(mem)*K/N,1),'p':hits/n}
print('\nTERTIARY - previously favoured (membrane) terms:')
fav={t:spec_test(sets.get(t,set())) for t in FAVOURED}
for t,v in fav.items(): print(f'  {t:<40} {v}',flush=True)
print('innate-immune terms that replicated in §31:')
imm={t:spec_test(sets.get(t,set())) for t in IMMUNE}
for t,v in imm.items(): print(f'  {t:<40} {v}',flush=True)
print('\nnamed proteins in PARP4 sheet:')
named={g:enriched(p4,g) for g in NAMED}
for g,v in named.items():
    s='HIT' if v and v['hit'] else ('present' if v else 'absent')
    print(f'  {g:<9} {s:<8} {v if v else ""}',flush=True)

json.dump({'gate_parp4_self':g1,'gate_baits_self':n_self,'verdict':verdict,
           'mvp_in_parp4':mvp,'mvp_other_baits':meas,'mvp_specificity_count':spec_n,
           'tep1':tep1,'proximal_n':K,'universe_n':N,
           'favoured_terms':fav,'immune_terms':imm,'named':named},
          open('results/turboid.json','w'),indent=1)
