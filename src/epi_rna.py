import gzip,re,pandas as pd
m={}
for l in gzip.open('gencode.vM25.basic.gtf.gz','rt'):
    if l[0]=='#':continue
    f=l.split('\t')
    if f[2]=='gene':
        m[re.search(r'gene_id "(ENSMUSG\d+)',f[8]).group(1)]=re.search(r'gene_name "([^"]+)"',f[8]).group(1)
d=pd.read_csv('GSE219176_rna.dat_rlog.txt.gz',sep='\t',index_col=0); d.index=[m.get(i,i) for i in d.index]; d=d[~d.index.duplicated()]
g=lambda p:[c for c in d.columns if re.match(p,c)]
D=pd.DataFrame({k:d[g(p)].mean(axis=1) for k,p in {'B16':'B16_cas','B16SKO':'B16_SKO','R499':'R499_cas','R499SKO':'R499_SKO'}.items()})
D['res_vs_b16']=D.R499-D.B16; D['stat1dep_R']=D.R499-D.R499SKO; D['stat1dep_B']=D.B16-D.B16SKO
P=D.rank(pct=True)*100
for c in ['Mvp','Oas1a','Oas1g','Ifit1','Ifit3','Usp18','Irf7','Stat1','Cd274','Tep1','Parp4','Actb']:
    print(c,D.loc[c].round(2).to_dict(),'pctiles res',round(P.res_vs_b16[c],1),'stat1R',round(P.stat1dep_R[c],1),'level',round(P.R499[c],1))
print(d.loc['Mvp'].round(2).to_dict())
