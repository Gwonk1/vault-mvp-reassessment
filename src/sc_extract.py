"""Stream Kim 2020 raw UMI text into sparse log1p(CP10K) for malignant + myeloid cells only."""
import gzip,numpy as np,pandas as pd,scipy.sparse as sp,sys,time
a=pd.read_csv('data/raw/sc/GSE131907_Lung_Cancer_cell_annotation.txt.gz',sep='\t').set_index('Index')
want=a.Cell_subtype.isin(['Malignant cells','tS1','tS2','tS3'])|(a.Cell_type=='Myeloid cells')
f=gzip.open('data/raw/sc/GSE131907_Lung_Cancer_raw_UMI_matrix.txt.gz','rt')
hdr=f.readline().rstrip('\n').split('\t')[1:]
idx=np.array([i for i,c in enumerate(hdr) if want.get(c,False)]); cells=[hdr[i] for i in idx]; print(len(hdr),len(idx),flush=True)
genes=[];R=[];C=[];V=[];t=time.time()
lib=np.zeros(len(idx))
for n,l in enumerate(f):
    g,rest=l.split('\t',1); x=np.fromstring(rest,sep='\t')[idx]; nz=np.nonzero(x)[0]
    lib+=x; genes.append(g); R.append(np.full(len(nz),n,dtype=np.int32)); C.append(nz.astype(np.int32)); V.append(x[nz].astype(np.float32))
    if n%3000==0: print(n,round(time.time()-t),flush=True)
M=sp.csr_matrix((np.concatenate(V),(np.concatenate(R),np.concatenate(C))),shape=(len(genes),len(idx)))
D=sp.diags(1e4/lib); M=(M.T.multiply(1e4/lib[:,None]) if False else (M@D)).tocsr(); M.data=np.log1p(M.data)
sp.save_npz('data/processed/kim_lognorm.npz',M); pd.DataFrame({'gene':genes}).to_parquet('data/processed/kim_genes.parquet')
a.loc[cells].assign(libsize=lib).to_parquet('data/processed/kim_cells.parquet'); print('done',M.shape,flush=True)
