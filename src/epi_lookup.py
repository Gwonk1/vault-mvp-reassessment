"""Run with cwd data/raw/qiu. Plan 3d lookup: chromatin at Mvp vs ISG controls and genome background."""
import gzip,re,numpy as np,pandas as pd,openpyxl
# TSS table
rows=[]
for l in gzip.open('gencode.vM25.basic.gtf.gz','rt'):
    if l[0]=='#':continue
    f=l.split('\t')
    if f[2]!='gene' or 'gene_type "protein_coding"' not in f[8]:continue
    n=re.search(r'gene_name "([^"]+)"',f[8]).group(1)
    s,e=int(f[3]),int(f[4]); rows.append((n,f[0],s,e,f[6],s if f[6]=='+' else e))
G=pd.DataFrame(rows,columns='gene chrom start end strand tss'.split()).drop_duplicates('gene').set_index('gene')
print('Mvp',G.loc['Mvp'].to_dict())
def load(fn):
    d=pd.read_csv(fn,sep='\t',index_col=0)
    p=d.index.to_series().str.extract(r'(chr\w+)_(\d+)_(\d+)'); d['chrom']=p[0];d['s']=p[1].astype(int);d['e']=p[2].astype(int);return d
A={'ATAC':'GSE219175_ATAC_revisions_consensus_mat_tn5_insertion_counts_IDR_vst.txt.gz','H3K4me1':'GSE219178_H3K4me1_consensus_mat_insertion_counts_WT_pooled_vst.txt.gz','H3K27ac':'GSE219178_H3K27Ac_consensus_mat_insertion_counts_WT_pooled_vst.txt.gz','H3K4me3':'GSE219178_H3K4me3_consensus_mat_insertion_counts_WT_pooled_vst.txt.gz'}
ctl=['Mvp','Oas1a','Oas1g','Oasl2','Ifit1','Ifit3','Usp18','Cd274','Stat1','Irf7','Actb','Gapdh']
wb=openpyxl.load_workbook('moesm3.xlsx',read_only=True,data_only=True)
imd=[r[3] for r in wb['Table 1. IFN-IMD bed'].iter_rows(min_row=2,values_only=True)]
res=[r[3] for r in wb['Table 2. IFN Resolved Dom bed'].iter_rows(min_row=2,values_only=True)]
imd=set(imd);res=set(res)
pc=G[G.chrom.str.match(r'chr[0-9XY]+$')]
out=[]
for k,fn in A.items():
    d=load(fn); cols=[c for c in d.columns if c not in('chrom','s','e')]
    grp=lambda pat:[c for c in cols if re.match(pat,c)]
    d['res_vs_b16']=d[grp('R499_WT')].mean(axis=1)-d[grp('B16_WT')].mean(axis=1)
    d['stat1_dep']=d[grp('R499_WT')].mean(axis=1)-d[grp('R499_SKO')].mean(axis=1)
    d['b16_stat1dep']=d[grp('B16_WT')].mean(axis=1)-d[grp('B16_SKO')].mean(axis=1)
    pk=d[['chrom','s','e','res_vs_b16','stat1_dep','b16_stat1dep']].copy(); pk['mid']=(pk.s+pk.e)//2
    bychr={c:x.sort_values('mid') for c,x in pk.groupby('chrom')}
    # gene-level: peaks within TSS +/- 2kb (promoter) and within gene +/- 20kb (locus)
    rec=[]
    for g,r in pc.iterrows():
        x=bychr.get(r.chrom)
        if x is None: continue
        m=x.mid.values
        for name,(a,b) in {'promoter':(r.tss-2000,r.tss+2000),'locus':(r.start-20000,r.end+20000)}.items():
            i,j=np.searchsorted(m,[a,b])
            if j>i:
                sub=x.iloc[i:j]; t=sub.loc[sub.res_vs_b16.abs().idxmax()]
                rec.append((g,name,len(sub),sub.res_vs_b16.max(),sub.res_vs_b16.mean(),t.stat1_dep,sub.stat1_dep.max()))
    R=pd.DataFrame(rec,columns='gene win npk maxgain meangain topstat1 maxstat1'.split())
    for name,x in R.groupby('win'):
        x=x.set_index('gene'); pct=x.rank(pct=True)
        for c in ctl:
            if c in x.index: out.append((k,name,c,int(x.npk[c]),round(x.maxgain[c],3),round(100*pct.maxgain[c],1),round(x.meangain[c],3),round(100*pct.meangain[c],1),round(x.maxstat1[c],3),round(100*pct.maxstat1[c],1)))
    # peaks at Mvp
    r=G.loc['Mvp']; x=pk[(pk.chrom==r.chrom)&(pk.e>r.start-30000)&(pk.s<r.end+30000)].copy()
    x['pct_gain']=[100*(pk.res_vs_b16<v).mean() for v in x.res_vs_b16]; x['pct_stat1']=[100*(pk.stat1_dep<v).mean() for v in x.stat1_dep]
    x['IMD']=[i in imd for i in x.index]; x['Resolved']=[i in res for i in x.index]
    print('\n',k,'peaks genome',len(pk),'in IMD',pk.index.isin(imd).sum(),'in Res',pk.index.isin(res).sum()); print(x[['res_vs_b16','pct_gain','stat1_dep','pct_stat1','b16_stat1dep','IMD','Resolved']].round(2).to_string())
pd.set_option('display.width',200)
print(pd.DataFrame(out,columns='assay win gene npk maxgain pct_max meangain pct_mean maxSTAT1dep pct_stat1'.split()).to_string())
# nearest domains
def near(s,lab):
    r=G.loc['Mvp']; a=[]
    for p in s:
        c,a0,b0=p.rsplit('_',2); 
        if c==r.chrom: a.append((min(abs(int(a0)-r.tss),abs(int(b0)-r.tss)),p))
    print(lab,sorted(a)[:3])
near(imd,'IMD');near(res,'Res')
