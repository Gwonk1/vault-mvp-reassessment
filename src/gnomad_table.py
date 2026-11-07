"""Derive constraint + LoF carrier table from saved gnomAD responses, with canonical+PASS filtering."""
import json,glob,os
out={}
for f in sorted(glob.glob('data/raw/gnomad/*.json')):
    g=os.path.basename(f)[:-5]; d=json.load(open(f)); c=d.get('gnomad_constraint') or {}
    can=d.get('canonical_transcript_id')
    def tot(v,k): return sum((v[x] or {}).get(k) or 0 for x in ('exome','genome'))
    def passed(v):
        ok=False
        for x in ('exome','genome'):
            s=v[x]
            if s and (s.get('ac') or 0)>0:
                if s.get('filters'): return False
                ok=True
        return ok
    hc=[v for v in d['variants'] if v['lof']=='HC' and not v['lof_flags']]
    strict=[v for v in hc if v.get('transcript_id')==can and passed(v)]
    an=max([tot(v,'an') for v in strict] or [0]); ac=sum(tot(v,'ac') for v in strict)
    hom=sum(tot(v,'homozygote_count') for v in strict)
    out[g]=dict(canonical_transcript=can,exp_lof=c.get('exp_lof'),obs_lof=c.get('obs_lof'),
        oe_lof=c.get('oe_lof'),loeuf=c.get('oe_lof_upper'),pli=c.get('pli'),oe_mis=c.get('oe_mis'),mis_z=c.get('mis_z'),
        hc_lof_all=len(hc),hc_lof_canonical_pass=len(strict),carrier_alleles=ac,max_an=an,
        cum_af=(ac/an if an else None),homozygotes=hom,expected_homozygotes=((ac/an)**2*an/2 if an else None),
        hom_variants=[(v['variant_id'],v.get('hgvsp'),tot(v,'ac'),tot(v,'homozygote_count')) for v in strict if tot(v,'homozygote_count')>0])
json.dump(out,open('results/gnomad.json','w'),indent=1,default=float)
for g,v in out.items():
    print(g,'| obs_lof(official)',v['obs_lof'],'| my HC all',v['hc_lof_all'],'-> canonical+PASS',v['hc_lof_canonical_pass'],
          '| hom',v['homozygotes'],'exp',None if v['expected_homozygotes'] is None else round(v['expected_homozygotes'],2))
print('\nMVP homozygous LoF variants:',out['MVP']['hom_variants'])
