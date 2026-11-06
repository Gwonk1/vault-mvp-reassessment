"""gnomAD v4 constraint and observed loss-of-function carriers for vault genes and reference genes."""
import json,time,requests
API='https://gnomad.broadinstitute.org/api'
Q='''query($s:String!){gene(gene_symbol:$s,reference_genome:GRCh38){symbol canonical_transcript_id
 gnomad_constraint{exp_lof obs_lof oe_lof oe_lof_lower oe_lof_upper pli exp_mis obs_mis oe_mis mis_z}
 variants(dataset:gnomad_r4){variant_id consequence lof lof_filter lof_flags hgvsp transcript_id
  exome{ac an homozygote_count filters} genome{ac an homozygote_count filters}}}}'''
out={}
for g in ['MVP','TEP1','PARP4','STAT1','TTN','OR4F5']:
    r=requests.post(API,json={'query':Q,'variables':{'s':g}},timeout=180,headers={'User-Agent':'vault-analysis'}).json()
    if 'errors' in r: print(g,r['errors'][:1]); time.sleep(8); continue
    d=r['data']['gene']; json.dump(d,open(f'data/raw/gnomad/{g}.json','w'))
    c=d['gnomad_constraint'] or {}
    lof=[v for v in d['variants'] if v['lof']=='LC' or v['lof']=='HC']
    hc=[v for v in lof if v['lof']=='HC' and not v['lof_flags']]
    tot=lambda v,k:sum((v[x] or {}).get(k) or 0 for x in('exome','genome'))
    hom=[(v['variant_id'],v['hgvsp'],tot(v,'ac'),tot(v,'homozygote_count')) for v in hc if tot(v,'homozygote_count')>0]
    an=max([tot(v,'an') for v in hc] or [0]); ac=sum(tot(v,'ac') for v in hc)
    print(g,{k:(round(c[k],3) if isinstance(c.get(k),float) else c.get(k)) for k in['exp_lof','obs_lof','oe_lof','oe_lof_lower','oe_lof_upper','pli','oe_mis','mis_z']})
    print('  HC LoF variants',len(hc),'carrier alleles',ac,'max AN',an,'cum AF',round(ac/an,5) if an else None,'homozygotes',sum(h[3] for h in hom))
    for h in sorted(hom,key=lambda x:-x[3])[:8]: print('   hom',h)
    time.sleep(8)
