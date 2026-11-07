"""Is the translation enrichment association, or just what ribosomal proteins are?
Pre-registered in RIBOSOME_PROPERTY_PREREGISTRATION.md. Empirical nulls only."""
import gzip, json, openpyxl, numpy as np, pandas as pd, warnings
warnings.filterwarnings('ignore')
NDRAW=200_000
# net charge at pH 7 from composition (Henderson-Hasselbalch, standard side-chain pKa)
PKA={'K':10.5,'R':12.5,'H':6.0}; NEG={'D':3.9,'E':4.3,'C':8.3,'Y':10.1}
def charge(s):
    q=0.0
    for a,pk in PKA.items(): q+=s.count(a)/(1+10**(7.0-pk))
    for a,pk in NEG.items(): q-=s.count(a)/(1+10**(pk-7.0))
    return q

sets={}
for f in ['data/raw/eggnog/c5.go.bp.v2024.1.Hs.symbols.gmt','data/raw/eggnog/c5.go.cc.v2024.1.Hs.symbols.gmt']:
    for line in open(f):
        p=line.rstrip('\n').split('\t'); sets[p[0]]=set(p[2:])
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
cov=len(seq)/len(uni)
print(f'GATE rule 7: sequences for {len(seq)}/{len(uni)} = {100*cov:.1f}% of the universe '
      f'-> {"PASS" if cov>=0.90 else "FAIL"}', flush=True)
if cov<0.90:
    print('ABORT: neither test runs.'); raise SystemExit(0)

G=pd.DataFrame({'WT_LFC':D['WT_LFC']})
G['len']=[len(seq[g]) if g in seq else np.nan for g in G.index]
G['chg']=[charge(seq[g]) if g in seq else np.nan for g in G.index]
G['chg_per_kres']=1000*G['chg']/G['len']
G=G.dropna()
G['ab']=pd.qcut(pd.Series(np.arange(len(G)),index=G.index).rank(method='first'),10,labels=False,duplicates='drop')
G['ld']=pd.qcut(G['len'].rank(method='first'),10,labels=False,duplicates='drop')
G['cd']=pd.qcut(G['chg_per_kres'].rank(method='first'),10,labels=False,duplicates='drop')
print(f'usable: {len(G)} proteins', flush=True)
vals=G['WT_LFC'].values; idx={g:i for i,g in enumerate(G.index)}
rng=np.random.default_rng(11)

def emp(members,keys,ndraw=NDRAW):
    mem=[g for g in members if g in idx]
    if len(mem)<3: return None
    obs=G.loc[mem,'WT_LFC'].mean()
    cells=G.loc[mem].groupby(keys).size().to_dict() if len(keys)>1 else G.loc[mem,keys[0]].value_counts().to_dict()
    pools={}
    grp=G.groupby(keys)
    for key,k in cells.items():
        try: pool=np.array([idx[g] for g in grp.get_group(key).index])
        except KeyError: pool=np.array([idx[g] for g in G.index])
        pools[key]=pool
    mus=np.zeros(ndraw)
    for key,k in cells.items():
        p=pools[key]; j=rng.integers(0,len(p),size=(ndraw,k)); mus+=vals[p[j]].sum(axis=1)
    mus/=len(mem)
    ge=int((mus>=obs).sum())
    return {'n':len(mem),'obs':round(float(obs),4),'null':round(float(mus.mean()),4),
            'sd':round(float(mus.std(ddof=1)),4),'ge':ge,'p':(ge+1)/(ndraw+1),
            'med_len':float(G.loc[mem,'len'].median()),
            'med_chg':round(float(G.loc[mem,'chg_per_kres'].median()),2)}

print(f"\nwhole-universe medians: length {G['len'].median():.0f}, charge/kres {G['chg_per_kres'].median():+.2f}")
print('\n--- TEST 1: compartment discrimination, abundance-matched only ---')
t1={}
for t in ['GOCC_CYTOSOLIC_RIBOSOME','GOCC_MITOCHONDRIAL_RIBOSOME','GOCC_ORGANELLAR_RIBOSOME',
          'GOCC_MITOCHONDRIAL_LARGE_RIBOSOMAL_SUBUNIT','GOCC_RIBOSOME','GOBP_CYTOPLASMIC_TRANSLATION']:
    r=emp(sets.get(t,set()),['ab']); t1[t]=r
    if r: print(f'  {t[:46]:<48} n={r["n"]:<4} obs={r["obs"]:+.3f} p={r["p"]:.2e} len={r["med_len"]:.0f} chg/kres={r["med_chg"]:+.1f}', flush=True)

print('\n--- GATE: vault core under length+charge+abundance matching ---')
core_ab=emp(['MVP','PARP4','TEP1'],['ab']); core_full=emp(['MVP','PARP4','TEP1'],['ab','ld','cd'])
print(f'  abundance only      : {core_ab}')
print(f'  + length + charge   : {core_full}')
gate = core_full is not None and core_full['p']<0.05
print(f'  -> core still clears p<0.05 with full matching: {gate}', flush=True)

print('\n--- TEST 2: cytosolic ribosome under length+charge+abundance matching ---')
t2={}
for t in ['GOCC_CYTOSOLIC_RIBOSOME','GOBP_CYTOPLASMIC_TRANSLATION','GOCC_RIBOSOME','GOCC_MITOCHONDRIAL_RIBOSOME']:
    r=emp(sets.get(t,set()),['ab','ld','cd']); t2[t]=r
    if r: print(f'  {t[:46]:<48} n={r["n"]:<4} obs={r["obs"]:+.3f} null={r["null"]:+.3f} ge={r["ge"]}/{NDRAW} p={r["p"]:.3e}', flush=True)

cyt=t1.get('GOCC_CYTOSOLIC_RIBOSOME'); mito=t1.get('GOCC_MITOCHONDRIAL_RIBOSOME') or t1.get('GOCC_ORGANELLAR_RIBOSOME')
cyt2=t2.get('GOCC_CYTOSOLIC_RIBOSOME')
if not gate: verdict='UNINFORMATIVE (core gate failed under full matching - matching over-specified)'
elif mito and cyt and mito['obs']>=cyt['obs']:
    verdict=('POLYSOME READING DIES: mitochondrial ribosome >= cytosolic ('
             f"{mito['obs']:+.3f} vs {cyt['obs']:+.3f}) - enrichment tracks 'is a ribosomal protein'")
elif cyt2 and cyt2['p']>=0.05:
    verdict=f"POLYSOME READING DIES: cytosolic ribosome fails length+charge matching (p={cyt2['p']:.3f})"
else:
    verdict=(f"ASSOCIATION READING SURVIVES: cytosolic ({cyt['obs']:+.3f}) > mitochondrial "
             f"({mito['obs']:+.3f}) and survives length+charge matching (p={cyt2['p']:.2e})")
print('\nVERDICT:',verdict, flush=True)
json.dump({'seq_coverage':cov,'test1':t1,'core_ab':core_ab,'core_full':core_full,
           'gate_pass':bool(gate),'test2':t2,'verdict':verdict},
          open('results/ribosome_property.json','w'),indent=1,default=str)
