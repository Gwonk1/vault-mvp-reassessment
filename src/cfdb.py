"""CFdb native co-fractionation test. Pre-registered in CFDB_PREREGISTRATION.md;
threshold in CFDB_DEVIATIONS.md. Streams 47.4M pairs, keeps precision>=0.25."""
import gzip, json, numpy as np, pandas as pd
from collections import defaultdict

PATH='data/raw/cfdb/Homo_sapiens.tsv.gz'
THRESH=[0.50,0.75,0.90]
FAVOURED=['GOBP_PLASMA_MEMBRANE_REPAIR','GOCC_CAVEOLA','GOBP_PLASMA_MEMBRANE_ORGANIZATION',
          'GOCC_LATE_ENDOSOME']
IMMUNE=['GOBP_INFLAMMATORY_RESPONSE','GOBP_RESPONSE_TO_BACTERIUM','GOCC_RUFFLE',
        'GOBP_ANTIGEN_PROCESSING_AND_PRESENTATION']
NAMED=['PARP4','TEP1','ANXA2','S100A10','EHD2','EHD4','CAPN2','MYOF','AHNAK','IQGAP1',
       'CD63','OPTN','VPS35','FLOT1','FLOT2','CAVIN1']

sets={}
for f in ['data/raw/eggnog/c5.go.bp.v2024.1.Hs.symbols.gmt',
          'data/raw/eggnog/c5.go.cc.v2024.1.Hs.symbols.gmt']:
    for line in open(f):
        p=line.rstrip('\n').split('\t'); sets[p[0]]=set(p[2:])

edges=[]
with gzip.open(PATH,'rt') as fh:
    next(fh)
    for line in fh:
        p=line.rstrip('\n').split('\t')
        if len(p)<4: continue
        try: pr=float(p[3])
        except ValueError: continue
        if pr<0.25: continue
        edges.append((p[0].strip('"'),p[1].strip('"'),pr))
print(f'edges kept (precision>=0.25): {len(edges)}',flush=True)

def build(t):
    adj=defaultdict(set)
    for a,b,pr in edges:
        if pr>=t: adj[a].add(b); adj[b].add(a)
    return adj

out={'threshold_results':{}}
for t in THRESH:
    adj=build(t)
    uni=set(adj)
    # GATES
    psma=adj.get('PSMA1',set())
    g1=len({g for g in psma if g.startswith(('PSMA','PSMB','PSMC','PSMD'))})
    rpl7=adj.get('RPL7',set())
    g2=len({g for g in rpl7 if g.startswith(('RPL','RPS'))})
    gates=(g1>=5 and g2>=5)
    mvp=adj.get('MVP',set())
    # PRIMARY / SECONDARY
    prim={'PARP4':'PARP4' in mvp,'TEP1':'TEP1' in mvp}
    named={g:(g in mvp) for g in NAMED}
    # TERTIARY: degree-matched random
    deg={g:len(v) for g,v in adj.items()}
    gl=sorted(uni)
    degarr=np.array([deg[g] for g in gl])
    rng=np.random.default_rng(0)
    def spec(gs,n=200):
        mem=[g for g in gs if g in uni]
        if len(mem)<5: return None
        obs=len(set(mem)&mvp)
        # match on degree decile
        dser=pd.Series(degarr,index=gl)
        dec=pd.qcut(dser.rank(method='first'),10,labels=False,duplicates='drop')
        prof=dec.loc[mem].value_counts(); hits=0
        for _ in range(n):
            pick=[]
            for d_,k in prof.items():
                pool=dec.index[dec==d_]
                if len(pool)==0: continue
                pick+=list(rng.choice(pool,size=min(k,len(pool)),replace=False))
            if len(set(pick)&mvp)>=obs: hits+=1
        return {'n':len(mem),'obs':obs,'p':hits/n}
    fav={x:spec(sets.get(x,set())) for x in FAVOURED}
    imm={x:spec(sets.get(x,set())) for x in IMMUNE}
    print(f'\n=== precision >= {t} | proteins {len(uni)} | edges {sum(len(v) for v in adj.values())//2}',flush=True)
    print(f'  GATE PSMA1 -> {g1} proteasome partners | RPL7 -> {g2} ribosomal  => {"PASS" if gates else "FAIL"}',flush=True)
    print(f'  MVP degree: {len(mvp)}',flush=True)
    print(f'  PRIMARY MVP-PARP4: {prim["PARP4"]}   SECONDARY MVP-TEP1: {prim["TEP1"]}',flush=True)
    print(f'  named partners present: {[g for g,v in named.items() if v] or "none"}',flush=True)
    if mvp and len(mvp)<=25: print(f'  MVP partners: {sorted(mvp)}',flush=True)
    for lbl,dd in (('membrane',fav),('immune',imm)):
        for k,v in dd.items(): print(f'    {lbl:<9} {k:<42} {v}',flush=True)
    out['threshold_results'][str(t)]={'gates':bool(gates),'psma1_proteasome':g1,'rpl7_ribosomal':g2,
        'n_proteins':len(uni),'mvp_degree':len(mvp),'mvp_parp4':prim['PARP4'],'mvp_tep1':prim['TEP1'],
        'named':named,'membrane_terms':fav,'immune_terms':imm,
        'mvp_partners':sorted(mvp) if len(mvp)<=200 else f'{len(mvp)} partners'}

p=out['threshold_results']['0.5']
if not p['gates']: v='UNINFORMATIVE (gates failed)'
elif not p['mvp_parp4']: v='KILL CONDITION MET for #116 - MVP-PARP4 absent in native co-fractionation'
else:
    mem=any(x and x['p']<0.05 for x in p['membrane_terms'].values())
    imm=any(x and x['p']<0.05 for x in p['immune_terms'].values())
    v=f'MVP-PARP4 RECOVERED | membrane support: {mem} | immune support: {imm}'
out['verdict']=v
print('\nVERDICT (at precision>=0.50):',v,flush=True)
json.dump(out,open('results/cfdb.json','w'),indent=1,default=str)
