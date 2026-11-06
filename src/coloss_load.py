"""Build species x OG presence and the taxonomy tree. Reads only OG membership, computes no gene-vs-gene scores."""
import gzip,numpy as np,pandas as pd,re,json
R='data/raw/eggnog/'
tax=pd.read_csv(R+'e5.taxid_info.tsv',sep='\t',dtype=str); tax.columns=['taxid','name','rank','lineage_names','lineage']
tax=tax.set_index('taxid')
ogs={}; hum={}
for l in gzip.open(R+'2759_members.tsv.gz','rt'):
    p=l.rstrip('\n').split('\t'); og=p[1]; sp=set(p[5].split(',')) if len(p)>5 else set(x.split('.')[0] for x in p[4].split(','))
    ogs[og]=sp; hum[og]=[x.split('.',1)[1] for x in p[4].split(',') if x.startswith('9606.')]
species=sorted(set().union(*ogs.values())); ix={s:i for i,s in enumerate(species)}
print('OGs',len(ogs),'species',len(species))
np.savez_compressed('data/processed/eggnog_presence.npz',M=np.array([np.isin(np.arange(len(species)),[ix[s] for s in v]) for v in ogs.values()],dtype=bool),ogs=np.array(list(ogs)),species=np.array(species))
json.dump(hum,open('data/processed/eggnog_human.json','w'))
