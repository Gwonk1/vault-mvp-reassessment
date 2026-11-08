"""Rerun of section 51's matching per Grok audit 4, deliverable 2, to its spec:
donor pool = matched decile cell with term members AND adjacents removed;
require >=30 remaining donors per cell else NON-IDENTIFIABLE; no 2.0x switch;
emit restricted-pool p and importance-weighted p for all three terms."""
import gzip, json, openpyxl, numpy as np, pandas as pd, warnings
warnings.filterwarnings('ignore')
NDRAW=200_000; MIN_DONORS=30
TERMS={
 'GOBP_CYTOPLASMIC_TRANSLATION':['GOCC_RIBOSOME','GOBP_TRANSLATION','GOCC_RIBONUCLEOPROTEIN_COMPLEX',
   'GOBP_RIBOSOME_BIOGENESIS','GOBP_TRANSLATIONAL_INITIATION','GOBP_TRANSLATIONAL_ELONGATION',
   'GOBP_RRNA_PROCESSING','GOCC_SMALL_RIBOSOMAL_SUBUNIT','GOBP_MRNA_METABOLIC_PROCESS','GOBP_RNA_PROCESSING'],
 'GOBP_DETOXIFICATION':['GOBP_RESPONSE_TO_XENOBIOTIC_STIMULUS','GOBP_RESPONSE_TO_OXIDATIVE_STRESS',
   'GOBP_CELLULAR_RESPONSE_TO_CHEMICAL_STRESS','GOBP_GLUTATHIONE_METABOLIC_PROCESS'],
 'GOCC_LATE_ENDOSOME':['GOCC_ENDOSOME','GOCC_EARLY_ENDOSOME','GOCC_LYSOSOME','GOBP_VESICLE_MEDIATED_TRANSPORT'],
}
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
wb=openpyxl.load_workbook('argon/raw/lodwick_supp_4.xlsx',read_only=True,data_only=True)
rows=list(wb['Fig. 5c-d'].iter_rows(values_only=True))
D=pd.DataFrame(rows[1:],columns=list(rows[0])).dropna(subset=['GeneName'])
for c in D.columns[1:]: D[c]=pd.to_numeric(D[c],errors='coerce')
D=D.drop_duplicates('GeneName').set_index('GeneName'); uni=set(D.index)
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
G=pd.DataFrame({'WT_LFC':D['WT_LFC']})
G['len']=[len(seq[g]) if g in seq else np.nan for g in G.index]
G['chg']=[chgk(seq[g]) if g in seq else np.nan for g in G.index]
G=G.dropna()
G['ab']=pd.qcut(pd.Series(np.arange(len(G)),index=G.index).rank(method='first'),10,labels=False,duplicates='drop')
G['ld']=pd.qcut(G['len'].rank(method='first'),10,labels=False,duplicates='drop')
G['cd']=pd.qcut(G['chg'].rank(method='first'),10,labels=False,duplicates='drop')
N=len(G); vals=G['WT_LFC'].values; pos={g:i for i,g in enumerate(G.index)}
gg=G.groupby(['ab','ld','cd'])
print(f'universe {N}; occupied cells {gg.ngroups}; mean cell size {N/gg.ngroups:.2f}\n',flush=True)
rng=np.random.default_rng(101); out={}
for term,adjterms in TERMS.items():
    adj=set().union(*[sets[t] for t in adjterms if t in sets])
    mem=[g for g in sets[term] if g in G.index]
    cells=G.loc[mem].groupby(['ab','ld','cd']).size().to_dict()
    obs=G.loc[mem,'WT_LFC'].mean()
    # --- per-cell donor census after removing members and adjacents ---
    census=[]; restricted={}; full={}
    for key,k in cells.items():
        try: pool=list(gg.get_group(key).index)
        except KeyError: pool=[]
        full[key]=pool
        keep=[g for g in pool if g not in set(mem) and g not in adj]
        restricted[key]=keep; census.append(len(keep))
    census=np.array(census)
    ok=int((census>=MIN_DONORS).sum()); tot=len(census)
    print(f'=== {term} ===')
    print(f'  members in universe {len(mem)} | occupied cells {tot} | donors/cell after removal: '
          f'median {np.median(census):.0f}, max {census.max()}, cells with >={MIN_DONORS}: {ok}/{tot}')
    if ok < tot:
        print(f'  -> NON-IDENTIFIABLE ({tot-ok} of {tot} cells have <{MIN_DONORS} usable donors; '
              f'the covariates determine the label there)',flush=True)
        out[term]={'members':len(mem),'cells':tot,'cells_ok':ok,'median_donors':float(np.median(census)),
                   'verdict':'NON-IDENTIFIABLE','obs':round(float(obs),4)}
        continue
    # (only reached if every cell is adequately populated)
    mus=np.zeros(NDRAW)
    for key,k in cells.items():
        p=np.array([pos[g] for g in restricted[key]])
        j=rng.integers(0,len(p),size=(NDRAW,k)); mus+=vals[p[j]].sum(axis=1)
    mus/=len(mem); ge=int((mus>=obs).sum())
    out[term]={'members':len(mem),'cells':tot,'cells_ok':ok,'verdict':'TESTED',
               'obs':round(float(obs),4),'null':round(float(mus.mean()),4),'p_restricted':(ge+1)/(NDRAW+1)}
    print(f'  restricted-pool p = {(ge+1)/(NDRAW+1):.4f}  (null {mus.mean():+.4f} vs obs {obs:+.4f})',flush=True)
json.dump({'min_donors':MIN_DONORS,'universe':N,'occupied_cells':gg.ngroups,'results':out},
          open('results/donor_restricted.json','w'),indent=1,default=str)
print('\nNOTE: the cell-size census above is the headline, not any p-value.')
