"""Registered export test + the donor-pool check added by addendum.
Pre-registered in EXPORT_PREREGISTRATION.md."""
import gzip, json, openpyxl, numpy as np, pandas as pd, warnings
warnings.filterwarnings('ignore')
NDRAW=200_000
PRIMARY=['GOBP_DETOXIFICATION','GOCC_LATE_ENDOSOME']
ADJ={'GOBP_DETOXIFICATION':['GOBP_RESPONSE_TO_XENOBIOTIC_STIMULUS','GOBP_RESPONSE_TO_OXIDATIVE_STRESS',
      'GOBP_CELLULAR_RESPONSE_TO_CHEMICAL_STRESS','GOBP_GLUTATHIONE_METABOLIC_PROCESS'],
     'GOCC_LATE_ENDOSOME':['GOCC_ENDOSOME','GOCC_EARLY_ENDOSOME','GOCC_LYSOSOME','GOBP_VESICLE_MEDIATED_TRANSPORT']}
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
G=pd.DataFrame({'WT_LFC':[D.loc[g,'WT_LFC'] for g in seq],'len':[len(seq[g]) for g in seq],
                'chg':[chgk(seq[g]) for g in seq]},index=list(seq))
G['ab']=pd.qcut(pd.Series(np.arange(len(G)),index=G.index).rank(method='first'),10,labels=False,duplicates='drop')
G['ld']=pd.qcut(G['len'].rank(method='first'),10,labels=False,duplicates='drop')
G['cd']=pd.qcut(G['chg'].rank(method='first'),10,labels=False,duplicates='drop')
print(f'usable universe: {len(G)}',flush=True)
vals=G['WT_LFC'].values; pos={g:i for i,g in enumerate(G.index)}
grp=G.groupby(['ab','ld','cd']); rng=np.random.default_rng(23)
def emp(members,keys=('ab','ld','cd'),ndraw=NDRAW):
    mem=[g for g in members if g in G.index]
    if len(mem)<3: return None
    obs=G.loc[mem,'WT_LFC'].mean()
    cells=G.loc[mem].groupby(list(keys)).size().to_dict()
    gg=G.groupby(list(keys)); mus=np.zeros(ndraw)
    for key,k in cells.items():
        try: pool=np.array([pos[g] for g in gg.get_group(key).index])
        except KeyError: pool=np.arange(len(G))
        j=rng.integers(0,len(pool),size=(ndraw,k)); mus+=vals[pool[j]].sum(axis=1)
    mus/=len(mem); ge=int((mus>=obs).sum())
    return {'n':len(mem),'obs':round(float(obs),4),'null':round(float(mus.mean()),4),
            'ge':ge,'p':(ge+1)/(ndraw+1)}
def donor(term,adjterms):
    mem=[g for g in sets[term] if g in G.index]
    cells=G.loc[mem].groupby(['ab','ld','cd']).size()
    gg=G.groupby(['ab','ld','cd']); don=[]
    for key in cells.index:
        try: don+=list(gg.get_group(key).index)
        except KeyError: pass
    don=sorted(set(don))
    adj=set().union(*[sets[t] for t in adjterms if t in sets]) if any(t in sets for t in adjterms) else set()
    fd=len([g for g in don if g in adj])/len(don); fu=len([g for g in G.index if g in adj])/len(G)
    return {'n_donors':len(don),'frac_donor':round(fd,3),'frac_universe':round(fu,3),
            'ratio':round(fd/fu,2) if fu>0 else None,
            'terms_used':[t for t in adjterms if t in sets]}
print('\nGATES')
core=emp(['MVP','PARP4','TEP1']); print(f'  core, full matching: {core}')
g1=core and core['p']<0.05
rib=emp(sets['GOCC_RIBOSOME']); print(f'  GOCC_RIBOSOME, full matching: {rib}  (section 51 gave p=0.184)')
g2=rib and rib['p']>=0.05
print(f'  gate1 core clears: {g1} | gate2 ribosome fails: {g2}',flush=True)
print('\nPRIMARY, abundance+length+charge matched:')
res={}
for t in PRIMARY:
    r=emp(sets[t]); res[t]={'matched':r}
    print(f'  {t:<32} {r}',flush=True)
print('\nADDENDUM donor-pool check:')
for t in PRIMARY:
    d=donor(t,ADJ[t]); res[t]['donor']=d
    v=('INVALID as applied' if d['ratio'] and d['ratio']>2.0 else
       'stands' if d['ratio'] and d['ratio']<1.5 else 'PARTIAL')
    res[t]['donor_verdict']=v
    print(f'  {t:<32} {d}  -> {v}',flush=True)
print('\nMEMBER-LEVEL (registered transparency requirement):')
for t in PRIMARY:
    mem=sorted([g for g in sets[t] if g in G.index],key=lambda g:-G.loc[g,'WT_LFC'])
    print(f'  {t}:')
    print('    '+', '.join(f'{g} {G.loc[g,"WT_LFC"]:+.2f}' for g in mem),flush=True)
out={}
for t in PRIMARY:
    r=res[t]['matched']; dv=res[t]['donor_verdict']
    if not (g1 and g2): out[t]='UNINFORMATIVE (gate failed)'
    elif r['p']>=0.05: out[t]=f"DIES on the matched control (p={r['p']:.3f})"
    elif dv=='INVALID as applied': out[t]=f"UNDECIDED - clears matching (p={r['p']:.3f}) but donor pool is {res[t]['donor']['ratio']}x"
    else: out[t]=f"SURVIVES matched control (p={r['p']:.3f}), donor pool {dv}"
    print(f'\nVERDICT {t}: {out[t]}')
json.dump({'core':core,'ribosome':rib,'gate1':bool(g1),'gate2':bool(g2),
           'results':res,'verdicts':out},open('results/export_test.json','w'),indent=1,default=str)
