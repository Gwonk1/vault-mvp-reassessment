"""Does a seed's own length and charge explain its translation-rich co-elution tail?
Pre-registered in SEED_PROPERTY_PREREGISTRATION.md."""
import gzip, json, heapq, numpy as np
from collections import defaultdict
from scipy.stats import spearmanr

PATH='data/raw/cfdb/Homo_sapiens.tsv.gz'; TERM='GOBP_CYTOPLASMIC_TRANSLATION'
TOPN=200; NRAND=150; MIN_PARTNERS=5000; KNN=30
S40=['MVP','RPL7','RPS6','PSMA1','GAPDH','ENO1','PKM','LDHA','ALDOA','FLOT1','FLOT2','STOM']
PKA={'K':10.5,'R':12.5,'H':6.0}; NEG={'D':3.9,'E':4.3,'C':8.3,'Y':10.1}
def chgk(s):
    q=0.0
    for a,pk in PKA.items(): q+=s.count(a)/(1+10**(7.0-pk))
    for a,pk in NEG.items(): q-=s.count(a)/(1+10**(pk-7.0))
    return 1000*q/len(s)

sets={}
for f in ['data/raw/eggnog/c5.go.bp.v2024.1.Hs.symbols.gmt','data/raw/eggnog/c5.go.cc.v2024.1.Hs.symbols.gmt']:
    for line in open(f):
        p=line.rstrip('\n').split('\t'); sets[p[0]]=set(p[2:])
term=sets[TERM]
counts=defaultdict(int)
with gzip.open(PATH,'rt') as fh:
    next(fh)
    for line in fh:
        p=line.rstrip('\n').split('\t')
        if len(p)<4: continue
        counts[p[0].strip('"')]+=1; counts[p[1].strip('"')]+=1
elig=sorted(g for g,n in counts.items() if n>=MIN_PARTNERS)
universe=set(counts); expected=len(term&universe)*TOPN/len(universe)
rng=np.random.default_rng(0)
pick=list(rng.choice([g for g in elig if g not in set(S40)],size=NRAND,replace=False))
want=set(pick)|set(S40)
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
def fold(g):
    h=heaps.get(g)
    if not h or len(h)<TOPN: return None
    return len({y for _,y in h}&term)/expected

seq={}; name=None; buf=[]
with gzip.open('data/raw/eggnog/gencode.v25.pc_translations.fa.gz','rt') as fh:
    for line in fh:
        if line.startswith('>'):
            if name and name in want:
                s=''.join(buf)
                if name not in seq or len(s)>len(seq[name]): seq[name]=s
            p=line[1:].rstrip().split('|'); name=p[6] if len(p)>6 else None; buf=[]
        else: buf.append(line.strip())
    if name and name in want:
        s=''.join(buf)
        if name not in seq or len(s)>len(seq[name]): seq[name]=s

rows=[]
for g in pick:
    f=fold(g)
    if f is None or g not in seq: continue
    rows.append((g,f,len(seq[g]),chgk(seq[g])))
G=np.array([(r[1],r[2],r[3]) for r in rows]); names=[r[0] for r in rows]
print(f'seeds with fold+sequence: {len(rows)} of {NRAND}', flush=True)
dist=G[:,0]
def pct(x): return float((dist<x).mean()*100)
mvp_f=fold('MVP'); mvp_len=len(seq['MVP']); mvp_chg=chgk(seq['MVP'])
print(f'MVP fold {mvp_f:.2f}x  percentile {pct(mvp_f):.1f}  length {mvp_len}  charge/kres {mvp_chg:+.1f}', flush=True)

# GATE: the axis must be measurable
gate=True
for g in ['RPL7','RPS6']:
    f=fold(g); L=len(seq[g]); C=chgk(seq[g])
    hi_chg=C>np.percentile(G[:,2],75); lo_len=L<np.percentile(G[:,1],25); hi_f=pct(f)>95
    print(f'  GATE {g}: fold pct {pct(f):.1f} (>95: {hi_f}) | charge {C:+.1f} top quartile: {hi_chg} | length {L} bottom quartile: {lo_len}')
    gate = gate and hi_f and hi_chg and lo_len
print(f'  -> axis measurable: {gate}', flush=True)

print('\nTEST 1: correlation of translation-fold with seed properties')
rc=spearmanr(G[:,0],G[:,2]); rl=spearmanr(G[:,0],G[:,1])
print(f'  Spearman rho(fold, charge/kres) = {rc.statistic:+.3f}  p = {rc.pvalue:.4f}')
print(f'  Spearman rho(fold, length)      = {rl.statistic:+.3f}  p = {rl.pvalue:.4f}', flush=True)

print(f'\nTEST 2: MVP percentile among its {KNN} nearest neighbours in (length, charge) space')
z=(G[:,1:]-G[:,1:].mean(0))/G[:,1:].std(0)
mz=(np.array([mvp_len,mvp_chg])-G[:,1:].mean(0))/G[:,1:].std(0)
d=np.sqrt(((z-mz)**2).sum(1)); nn=np.argsort(d)[:KNN]
nnf=G[nn,0]; mvp_nn_pct=float((nnf<mvp_f).mean()*100)
print(f'  neighbours: median fold {np.median(nnf):.2f}x  max {nnf.max():.2f}x')
print(f'  their median length {np.median(G[nn,1]):.0f}  median charge/kres {np.median(G[nn,2]):+.1f}')
print(f'  MVP percentile among neighbours = {mvp_nn_pct:.1f}')
print(f'  nearest 8: {[(names[i], round(G[i,0],2)) for i in nn[:8]]}', flush=True)

if not gate: verdict='UNINFORMATIVE (axis not measurable)'
elif mvp_nn_pct<75: verdict=f'SECTION 40 EXPLAINED AND WITHDRAWN (MVP {mvp_nn_pct:.1f} among neighbours)'
elif rc.pvalue<0.05 and rc.statistic>0 and mvp_nn_pct>90:
    verdict=f'SECTION 40 STRENGTHENED (rho_charge {rc.statistic:+.3f} p {rc.pvalue:.4f}; MVP {mvp_nn_pct:.1f} among neighbours)'
else: verdict=f'NEITHER - axis is not the mechanism; one more alternative eliminated, section 40 unpromoted (MVP {mvp_nn_pct:.1f})'
print('\nVERDICT:',verdict, flush=True)
json.dump({'n_seeds':len(rows),'mvp':{'fold':mvp_f,'pct':pct(mvp_f),'length':mvp_len,'charge':mvp_chg},
           'gate':bool(gate),'rho_charge':[float(rc.statistic),float(rc.pvalue)],
           'rho_length':[float(rl.statistic),float(rl.pvalue)],'knn':KNN,
           'mvp_knn_pct':mvp_nn_pct,'knn_median_fold':float(np.median(nnf)),
           'knn_names':[names[i] for i in nn],'verdict':verdict},
          open('results/seed_property.json','w'),indent=1,default=str)
