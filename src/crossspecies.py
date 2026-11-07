"""Cross-species test per CROSSSPECIES_PREREGISTRATION.md."""
import openpyxl,json,numpy as np,pandas as pd
from scipy.stats import hypergeom,spearmanr
wb=openpyxl.load_workbook('argon/raw/natcomms_source_data/Source_data_Vault.xlsx',read_only=True,data_only=True)
rows=list(wb['Fig. 5D'].iter_rows(values_only=True))
cols=list(rows[0]); D=pd.DataFrame(rows[1:],columns=cols)
fc=[c for c in cols if str(c).startswith('foldchange.log2')][0]
qv=[c for c in cols if str(c).startswith('qvalue')][0]
D['fc']=pd.to_numeric(D[fc],errors='coerce'); D['q']=pd.to_numeric(D[qv],errors='coerce')
# ORTHOLOGY, not name matching: Dicty UniProt -> eggNOG OG -> human symbol
import gzip,json as _j
xr=pd.read_csv('data/raw/ortho/dicty_eggnog.tsv',sep='\t').dropna(subset=['eggNOG'])
acc2og={a:[x for x in str(e).split(';') if x] for a,e in zip(xr.Entry,xr.eggNOG)}
hum=_j.load(open('data/processed/eggnog_human.json'))
sym={}
for l in gzip.open('data/raw/eggnog/gencode.v25.pc_translations.fa.gz','rt'):
    if l[0]=='>':
        p=l[1:].split('|'); sym[p[0].split('.')[0]]=p[6]
og2sym={og:sorted({sym[x] for x in ps if x in sym}) for og,ps in hum.items()}
D['acc']=D.accessions.astype(str).str.split(';').str[0]
rows2=[]
for _,r in D.iterrows():
    for og in acc2og.get(r.acc,[]):
        for h in og2sym.get(og,[]):
            rows2.append((h,r.fc,r.q))
O=pd.DataFrame(rows2,columns=['sym','fc','q'])
print('Dicty proteins with eggNOG OG:',D.acc.isin(acc2og).sum(),'| human symbols reached:',O.sym.nunique(),flush=True)
D=O.sort_values('q').drop_duplicates('sym').set_index('sym')
prox=set(D.index[(D.fc>0)&(D.q<.05)])
print(f'Dictyostelium proteins {len(D)} | vault-proximal (log2FC>0, q<0.05): {len(prox)} ({100*len(prox)/len(D):.1f}%)',flush=True)
arp=['ACTR2','ACTR3','ARPC1A','ARPC1B','ARPC2','ARPC3','ARPC4','ARPC5']
hit=[g for g in arp if g in prox]
gate=len(hit)>=3
print(f'GATE Arp2/3 vault-proximal: {len(hit)}/8 {hit} ->','PASS' if gate else 'FAIL',flush=True)
po=pd.read_parquet('data/processed/mvp_coabundance_cna.parquet')
uni=[g for g in po.index if g in D.index]
top=[g for g in po.index if g in set(uni)][:100]
k=len(set(top)&prox); exp=len(top)*len(prox&set(uni))/len(uni)
p=hypergeom.sf(k-1,len(uni),len(prox&set(uni)),len(top))
rho=spearmanr(po.loc[uni].z.values,D.loc[uni].fc.values,nan_policy='omit')
lab=('ANCIENT ASSOCIATION' if (p<.05 and k>=5) else 'NOT CONSERVED') if gate else 'UNINFORMATIVE'
print(f'\nshared universe {len(uni)} | vault-proximal within it {len(prox&set(uni))}',flush=True)
print(f'PRIMARY: {k}/100 of my top partners are vault-proximal in Dictyostelium (expected {exp:.1f}) | p = {p:.4g}',flush=True)
print('VERDICT:',lab,flush=True)
print(f'Secondary: Spearman(my adjusted z, Dicty log2FC) = {rho.statistic:+.3f} (p={rho.pvalue:.2g}, n={len(uni)})',flush=True)
named=['ACTR2','ACTR3','ARPC1B','CAPNS1','IQGAP1','CAP1','CLIC1','PARP4','TEP1','ANXA2','S100A10','EHD4','CAPN2']
out=[]
for g in named:
    r=int(list(po.index).index(g))+1 if g in po.index else None
    if g in D.index:
        out.append(dict(gene=g,my_rank=r,dicty_log2FC=round(float(D.fc[g]),2),q=round(float(D.q[g]),4),proximal=g in prox))
    else: out.append(dict(gene=g,my_rank=r,dicty_log2FC=None,q=None,proximal='absent in amoeba'))
T=pd.DataFrame(out); print('\n',T.to_string(index=False),flush=True)
print('\nmy top-25 that are vault-proximal in the amoeba:',[g for g in top[:25] if g in prox],flush=True)
json.dump(dict(verdict=lab,gate=bool(gate),arp_hits=hit,shared=len(uni),proximal=len(prox&set(uni)),
  overlap=k,expected=float(exp),p=float(p),spearman=float(rho.statistic),spearman_p=float(rho.pvalue),
  named=T.to_dict('records')),open('results/crossspecies.json','w'),indent=1,default=float)
