"""Grok audit 3's two named gaps: the donor list, and varying k.
Pre-registered in DONOR_AND_K_PREREGISTRATION.md."""
import gzip, json, heapq, openpyxl, numpy as np, pandas as pd, warnings
warnings.filterwarnings('ignore')
from collections import defaultdict

ADJ=['GOCC_RIBOSOME','GOBP_TRANSLATION','GOCC_RIBONUCLEOPROTEIN_COMPLEX','GOBP_RIBOSOME_BIOGENESIS',
     'GOBP_TRANSLATIONAL_INITIATION','GOBP_TRANSLATIONAL_ELONGATION','GOBP_RRNA_PROCESSING',
     'GOCC_SMALL_RIBOSOMAL_SUBUNIT','GOBP_MRNA_METABOLIC_PROCESS','GOBP_RNA_PROCESSING']
TERM='GOBP_CYTOPLASMIC_TRANSLATION'
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
adj=set().union(*[sets[t] for t in ADJ])

# ---------- TEST 1: the donor list ----------
wb=openpyxl.load_workbook('argon/raw/lodwick_supp_4.xlsx',read_only=True,data_only=True)
rows=list(wb['Fig. 5c-d'].iter_rows(values_only=True))
D=pd.DataFrame(rows[1:],columns=list(rows[0])).dropna(subset=['GeneName'])
for c in D.columns[1:]: D[c]=pd.to_numeric(D[c],errors='coerce')
D=D.drop_duplicates('GeneName').set_index('GeneName')
uni=set(D.index)
seq={}; name=None; buf=[]
with gzip.open('data/raw/eggnog/gencode.v25.pc_translations.fa.gz','rt') as fh:
    for line in fh:
        if line.startswith('>'):
            if name and name in uni:
                s=''.join(buf)
                if name not in seq or len(s)>len(seq[name]): seq[name]=s
            p=line[1:].rstrip().split('|'); name=p[6] if len(p)>6 else None; buf=[]
        else: buf.append(line.strip())
    if name and name in uni:
        s=''.join(buf)
        if name not in seq or len(s)>len(seq[name]): seq[name]=s
G=pd.DataFrame({'len':[len(seq[g]) for g in seq],'chg':[chgk(seq[g]) for g in seq]},index=list(seq))
G['ab']=pd.qcut(pd.Series(np.arange(len(G)),index=G.index).rank(method='first'),10,labels=False,duplicates='drop')
G['ld']=pd.qcut(G['len'].rank(method='first'),10,labels=False,duplicates='drop')
G['cd']=pd.qcut(G['chg'].rank(method='first'),10,labels=False,duplicates='drop')
mem=[g for g in sets[TERM] if g in G.index]
cells=G.loc[mem].groupby(['ab','ld','cd']).size()
donors=[]
grp=G.groupby(['ab','ld','cd'])
for key in cells.index:
    try: donors+=list(grp.get_group(key).index)
    except KeyError: pass
donors=sorted(set(donors))
f_don=len([g for g in donors if g in adj])/len(donors)
f_uni=len([g for g in G.index if g in adj])/len(G)
ratio=f_don/f_uni
print(f'TEST 1 donor list, for {TERM} (n={len(mem)} members, {len(cells)} occupied cells)')
print(f'  donor pool size: {len(donors)} proteins')
print(f'  translation-adjacent in donor pool : {f_don:.3f}')
print(f'  translation-adjacent in universe   : {f_uni:.3f}  (n={len(G)})')
print(f'  ENRICHMENT RATIO = {ratio:.2f}x', flush=True)
v1=('INVALID as applied' if ratio>2.0 else 'STANDS as a sensitivity analysis' if ratio<1.5 else 'PARTIAL')
print(f'  -> section 51 control: {v1}', flush=True)

# ---------- TEST 2: varying k ----------
PATH='data/raw/cfdb/Homo_sapiens.tsv.gz'
S40=['MVP','RPL7','RPS6','PSMA1','GAPDH','ENO1','PKM','LDHA','ALDOA','FLOT1','FLOT2','STOM']
NEGS=['FLOT1','FLOT2','STOM','GAPDH','ENO1','PKM']
KS=[25,50,100,200,400,800]
counts=defaultdict(int)
with gzip.open(PATH,'rt') as fh:
    next(fh)
    for line in fh:
        p=line.rstrip('\n').split('\t')
        if len(p)<4: continue
        counts[p[0].strip('"')]+=1; counts[p[1].strip('"')]+=1
elig=sorted(g for g,n in counts.items() if n>=5000)
cfuni=set(counts); term=sets[TERM]
rng=np.random.default_rng(0)
pick=list(rng.choice([g for g in elig if g not in set(S40)],size=150,replace=False))
want=set(pick)|set(S40)
KMAX=max(KS)
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
            if len(h)<KMAX: heapq.heappush(h,(s,y))
            elif s>h[0][0]: heapq.heapreplace(h,(s,y))
print(f'\nTEST 2 varying k  (expected = |term in CFdb universe| * k / |universe|)')
tab={}
for k in KS:
    exp=len(term&cfuni)*k/len(cfuni)
    def fold(g):
        h=heaps.get(g)
        if not h: return None
        top={y for _,y in heapq.nlargest(k,h)}
        return len(top&term)/exp
    dist=np.array([f for f in (fold(g) for g in pick) if f is not None])
    def pct(x): return float((dist<x).mean()*100)
    mf=fold('MVP'); mp=pct(mf)
    g1=all(pct(fold(g))>95 for g in ['RPL7','RPS6'])
    negmed=float(np.median([pct(fold(g)) for g in NEGS]))
    tab[k]={'mvp_fold':round(mf,2),'mvp_pct':round(mp,1),'rpl7':round(pct(fold('RPL7')),1),
            'rps6':round(pct(fold('RPS6')),1),'neg_median':round(negmed,1),
            'gate':bool(g1 and negmed<80),'rand_median':round(float(np.median(dist)),2)}
    print(f'  k={k:<4} MVP fold {mf:6.2f}x  pct {mp:5.1f} | RPL7 {pct(fold("RPL7")):5.1f} RPS6 {pct(fold("RPS6")):5.1f} | negs med {negmed:5.1f} | gate {"PASS" if g1 and negmed<80 else "FAIL"}', flush=True)
folds=[tab[k]['mvp_fold'] for k in KS]
small=[tab[k]['mvp_pct'] for k in KS if k<=50]
peak_small = folds.index(max(folds))<=1
mono = all(folds[i]>=folds[i+1] for i in range(len(folds)-1))
if folds[-1]>=folds[0] or min(small)<95: v2='WINDOW-LIKE'
elif peak_small and mono: v2='COMPLEX-LIKE'
else: v2='MIXED - promotes nothing'
print(f'\n  folds across k: {folds}')
print(f'  -> {v2}', flush=True)
print(f'\nVERDICT  test1: {v1}  |  test2: {v2}')
json.dump({'donor':{'n_members':len(mem),'n_cells':int(len(cells)),'n_donors':len(donors),
           'frac_donor':f_don,'frac_universe':f_uni,'ratio':ratio,'verdict':v1},
           'k':tab,'k_verdict':v2},open('results/donor_and_k.json','w'),indent=1,default=str)
