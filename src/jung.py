"""GSE135222 Jung 2019 NSCLC anti-PD1: pre-treatment by study design. Map Ensembl to symbols."""
import gzip,re,pandas as pd,os
m={}
for l in gzip.open('data/raw/cov/gencode.v19.gtf.gz','rt'):
    if l[0]=='#':continue
    f=l.split('\t')
    if f[2]=='gene' and 'gene_type "protein_coding"' in f[8]:
        m[re.search(r'gene_id "(ENSGR?\d+)',f[8]).group(1)]=re.search(r'gene_name "([^"]+)"',f[8]).group(1)
d=pd.read_csv('data/raw/cov/jung.tsv.gz',sep='\t',index_col=0)
d.index=[m.get(i.split(".")[0]) for i in d.index]; d=d[d.index.notna()].groupby(level=0).sum()
d.columns=d.columns.astype(str); d.to_parquet('data/processed/bulk/jung.expr.parquet'); print('jung',d.shape)
