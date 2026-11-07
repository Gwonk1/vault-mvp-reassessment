"""Is MVP's translation-rich co-elution tail explained by apparent mass?
Pre-registered in MASS_CONFOUND_PREREGISTRATION.md. Reproduces section 40's statistic exactly."""
import gzip, json, heapq, numpy as np
from collections import defaultdict

PATH='data/raw/cfdb/Homo_sapiens.tsv.gz'; TERM='GOBP_CYTOPLASMIC_TRANSLATION'
TOPN=200; NRAND=150; MIN_PARTNERS=5000
S40_NAMED=['MVP','RPL7','RPS6','PSMA1','GAPDH','ENO1','PKM','LDHA','ALDOA','FLOT1','FLOT2','STOM']
GROUPS={'nuclear pore ~110 MDa':['NUP133','NUP93','NUP205','NUP188','NUP107','NUP160','NUP214'],
 '26S proteasome ~2.5 MDa':['PSMA1','PSMD1','PSMC1'],
 'spliceosome ~1.5 MDa':['SF3B1','PRPF8','SNRNP200','EFTUD2','SF3B3'],
 'dynein ~1.4 MDa':['DYNC1H1','DCTN1','DYNC1I2','ACTR1A'],
 'condensin/cohesin ~1 MDa':['SMC1A','SMC2','SMC3','SMC4','NCAPD2'],
 'TRiC/CCT ~1 MDa':['CCT2','CCT3','CCT4','CCT5','CCT6A','CCT7','TCP1'],
 'clathrin coat':['CLTC','CLTA','AP2M1','AP2B1'],
 'small-complex negatives':['FLOT1','FLOT2','STOM','GAPDH','ENO1','PKM']}

sets={}
for f in ['data/raw/eggnog/c5.go.bp.v2024.1.Hs.symbols.gmt','data/raw/eggnog/c5.go.cc.v2024.1.Hs.symbols.gmt']:
    for line in open(f):
        p=line.rstrip('\n').split('\t'); sets[p[0]]=set(p[2:])
term=sets[TERM]

# pass 1: degrees
counts=defaultdict(int)
with gzip.open(PATH,'rt') as fh:
    next(fh)
    for line in fh:
        p=line.rstrip('\n').split('\t')
        if len(p)<4: continue
        counts[p[0].strip('"')]+=1; counts[p[1].strip('"')]+=1
eligible=sorted(g for g,n in counts.items() if n>=MIN_PARTNERS)
universe=set(counts); expected=len(term&universe)*TOPN/len(universe)
print(f'universe {len(universe)} | eligible {len(eligible)} | expected in top-{TOPN}: {expected:.3f}',flush=True)

# reproduce section 40's random draw EXACTLY (same rng, same exclusion list)
rng=np.random.default_rng(0)
pick=list(rng.choice([g for g in eligible if g not in set(S40_NAMED)],size=NRAND,replace=False))
want=set(pick)|set(S40_NAMED)|{g for gs in GROUPS.values() for g in gs}|{'RPL4','RPS3'}
want={g for g in want if counts.get(g,0)>=MIN_PARTNERS}
print(f'seeds to evaluate: {len(want)}',flush=True)

# pass 2: top-200 by score per wanted seed, via bounded heaps
heaps={g:[] for g in want}
with gzip.open(PATH,'rt') as fh:
    next(fh)
    for line in fh:
        p=line.rstrip('\n').split('\t')
        if len(p)<4: continue
        a,b=p[0].strip('"'),p[1].strip('"')
        if a not in heaps and b not in heaps: continue
        try: s=float(p[2])
        except ValueError: continue
        for x,y in ((a,b),(b,a)):
            h=heaps.get(x)
            if h is None: continue
            if len(h)<TOPN: heapq.heappush(h,(s,y))
            elif s>h[0][0]: heapq.heapreplace(h,(s,y))
print('pass 2 done',flush=True)

def fold(g):
    h=heaps.get(g)
    if not h or len(h)<TOPN: return None
    return len({y for _,y in h}&term)/expected
dist=np.array([f for f in (fold(g) for g in pick) if f is not None])
def pct(x): return float((dist<x).mean()*100)
print(f'random reference: n={len(dist)} median {np.median(dist):.2f}x 95th {np.percentile(dist,95):.2f}x max {dist.max():.2f}x',flush=True)

mvp_f=fold('MVP'); mvp_p=pct(mvp_f)
print(f'\nMVP: fold {mvp_f:.2f}x percentile {mvp_p:.1f} (section 40 reported 98.0)',flush=True)
# GATES
g1=all(pct(fold(g))>95 for g in ['RPL7','RPS6'] if fold(g) is not None)
negs=[pct(fold(g)) for g in GROUPS['small-complex negatives'] if fold(g) is not None]
g2=float(np.median(negs))<80
print(f'GATE1 RPL7/RPS6 >95th: {g1}  (RPL7 {pct(fold("RPL7")):.1f}, RPS6 {pct(fold("RPS6")):.1f})')
print(f'GATE2 small-complex negatives median {np.median(negs):.1f} < 80: {g2}',flush=True)

res={}; big=[]
print('\nby assembly:')
for lab,gs in GROUPS.items():
    ps=[]
    for g in gs:
        f=fold(g)
        if f is None: continue
        ps.append(pct(f)); res[g]={'group':lab,'fold':round(f,2),'pct':round(pct(f),1),'degree':counts[g]}
    if ps:
        print(f'  {lab:<26} n={len(ps):<2} median pct {np.median(ps):5.1f}  range {min(ps):.0f}-{max(ps):.0f}')
        if lab!='small-complex negatives': big+=ps
bigmed=float(np.median(big))
print(f'\nALL large assemblies (n={len(big)}): median percentile {bigmed:.1f}',flush=True)

if not (g1 and g2): verdict='UNINFORMATIVE (gate failed)'
elif bigmed>75 or any(np.median([res[g]["pct"] for g in gs if g in res])>mvp_p
                      for lab,gs in GROUPS.items() if lab!='small-complex negatives'):
    verdict=f'MASS CONFOUND CONFIRMED (large-assembly median {bigmed:.1f})'
elif bigmed<60 and mvp_p>95: verdict=f'MVP SURVIVES AS SPECIFIC (MVP {mvp_p:.1f} vs large-assembly median {bigmed:.1f})'
else: verdict=f'EQUIVOCAL (MVP {mvp_p:.1f}, large-assembly median {bigmed:.1f}) - promotes nothing'
print('\nVERDICT:',verdict,flush=True)
json.dump({'expected':expected,'mvp':{'fold':mvp_f,'pct':mvp_p,'degree':counts['MVP']},
           'random':{'n':len(dist),'median':float(np.median(dist)),'p95':float(np.percentile(dist,95))},
           'gate1':bool(g1),'gate2':bool(g2),'negatives_median':float(np.median(negs)),
           'seeds':res,'large_assembly_median':bigmed,'verdict':verdict},
          open('results/mass_confound.json','w'),indent=1,default=str)
