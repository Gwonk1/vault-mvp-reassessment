"""Continuous statistic across the whole small-term family, BH-corrected.
Pre-registered in SMC56_CONTINUOUS_PREREGISTRATION.md."""
import openpyxl, json, numpy as np, pandas as pd, warnings
warnings.filterwarnings('ignore')
from scipy.stats import norm

NDRAW=4000
sets={}
for f in ['data/raw/eggnog/c5.go.bp.v2024.1.Hs.symbols.gmt','data/raw/eggnog/c5.go.cc.v2024.1.Hs.symbols.gmt']:
    for line in open(f):
        p=line.rstrip('\n').split('\t'); sets[p[0]]=set(p[2:])
wb=openpyxl.load_workbook('argon/raw/lodwick_supp_4.xlsx',read_only=True,data_only=True)
rows=list(wb['Fig. 5c-d'].iter_rows(values_only=True))
D=pd.DataFrame(rows[1:],columns=list(rows[0])).dropna(subset=['GeneName'])
for c in D.columns[1:]: D[c]=pd.to_numeric(D[c],errors='coerce')
D=D.drop_duplicates('GeneName').set_index('GeneName')
uni=set(D.index); N=len(uni); L=D['WT_LFC']
dec=pd.qcut(pd.Series(np.arange(N),index=D.index).rank(method='first'),10,labels=False,duplicates='drop')
pools={d:dec.index[dec==d] for d in dec.unique()}
rng=np.random.default_rng(0)

# one shared null per size, since matching is by decile profile we draw per-term
def zstat(mem,ndraw=NDRAW):
    obs=L.loc[mem].mean(); prof=dec.loc[mem].value_counts()
    mus=np.empty(ndraw)
    for i in range(ndraw):
        pick=[]
        for d_,k in prof.items():
            pool=pools[d_]; pick+=list(rng.choice(pool,size=min(k,len(pool)),replace=False))
        mus[i]=L.loc[pick].mean()
    sd=mus.std(ddof=1)
    z=(obs-mus.mean())/sd if sd>0 else 0.0
    return obs,mus.mean(),sd,z

fam={t:[g for g in (gs&uni)] for t,gs in sets.items()}
fam={t:m for t,m in fam.items() if 3<=len(m)<=9}
print(f'family: {len(fam)} terms with 3-9 members in the universe', flush=True)
print(f"(section 45's family used a <10 cut with no floor: {sum(1 for t,gs in sets.items() if 0<len(gs&uni)<3)} terms with 1-2 members are excluded here)", flush=True)

res={}
for t,m in fam.items():
    obs,nm,sd,z=zstat(m,ndraw=600)
    res[t]={'n':len(m),'mean':round(float(obs),4),'null':round(float(nm),4),
            'sd':round(float(sd),4),'z':round(float(z),3)}
# refine the top 40 with the full draw count
top=sorted(res,key=lambda t:-res[t]['z'])[:40]
for t in top:
    obs,nm,sd,z=zstat(fam[t],ndraw=NDRAW)
    res[t].update({'mean':round(float(obs),4),'null':round(float(nm),4),
                   'sd':round(float(sd),4),'z':round(float(z),3),'refined':True})
names=list(res); ps=np.array([norm.sf(res[t]['z']) for t in names])
o=np.argsort(ps); n=len(ps); qs=np.empty(n); prev=1.0
for i in range(n-1,-1,-1):
    prev=min(prev,ps[o[i]]*n/(i+1)); qs[o[i]]=prev
Q=pd.Series(qs,index=names)
for t in names: res[t]['q']=float(Q[t])

core=zstat(['MVP','PARP4','TEP1'])
# the core is a 3-member set: place it in the family for gating
pcore=norm.sf(core[3]); qcore=min(1.0,pcore*n/1)
print(f'\nGATE vault core (MVP/PARP4/TEP1): mean {core[0]:+.3f} null {core[1]:+.3f} sd {core[2]:.3f} z {core[3]:.2f}')
print(f'  BH-equivalent q (best-rank bound) = {qcore:.3e} -> q<0.01: {qcore<0.01}', flush=True)
gate=qcore<0.01

S=Q.sort_values()
rank_smc=int((S.index=='GOCC_SMC5_SMC6_COMPLEX').argmax())+1
print(f'\nSMC5/6: {res["GOCC_SMC5_SMC6_COMPLEX"]}')
print(f'  rank {rank_smc} of {len(S)} in the family by q', flush=True)
print('\ntop 12 of the family by q:')
for t in S.index[:12]:
    r=res[t]; print(f'  {t[:52]:<54} n={r["n"]:<3} mean={r["mean"]:+.3f} z={r["z"]:+.2f} q={r["q"]:.4f}', flush=True)

qs_ = res['GOCC_SMC5_SMC6_COMPLEX']['q']
if not gate: verdict='UNINFORMATIVE (vault-core gate failed)'
elif qs_<0.05: verdict=f'SMC5/6 SURVIVES family correction on the continuous statistic (q={qs_:.4f})'
else: verdict=f'SMC5/6 DIES for good (q={qs_:.4f}); section 45 stands on a second statistic'
print('\nVERDICT:',verdict, flush=True)
json.dump({'family_size':len(fam),'gate_core':{'mean':float(core[0]),'z':float(core[3]),'q':float(qcore)},
           'gate_pass':bool(gate),'smc56':res['GOCC_SMC5_SMC6_COMPLEX'],'smc56_rank':rank_smc,
           'top12':{t:res[t] for t in S.index[:12]},'verdict':verdict},
          open('results/smc56_continuous.json','w'),indent=1,default=str)
