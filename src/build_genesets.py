"""Build frozen gene sets from source files. Run once; output is committed."""
import json,re,hashlib,sys
root='data/raw/genesets/'
html=open(root+'patent.html',errors='ignore').read()
t=re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',html))
i=t.index('the ISG.RS metagene comprises'); seg=t[i:i+4000]
m=re.search(r'the ISG\.RS metagene comprises (.*?); and the IFNG\.GS metagene comprises (.*?)\. \d',seg)
parse=lambda s:[g.strip() for g in re.sub(r'\band\b',',',s).split(',') if g.strip()]
isg,ifng=parse(m.group(1)),parse(m.group(2))
hall={l.split('\t')[0]:l.strip().split('\t')[2:] for l in open(root+'h.all.gmt')}
H=set(hall['HALLMARK_INTERFERON_GAMMA_RESPONSE']);A=set(hall['HALLMARK_INTERFERON_ALPHA_RESPONSE'])
import openpyxl
q=[r[0] for r in openpyxl.load_workbook('data/raw/qiu/moesm4.xlsx',read_only=True,data_only=True)['Fig. 1E'].iter_rows(min_row=2,values_only=True)]
print('ISG.RS patent',len(isg),'| Qiu Fig1E',len(q),'| symmetric diff',set(isg)^set(q))
print('IFNG.GS patent',len(ifng),'| dup',len(ifng)-len(set(ifng)))
print('overlap ISG/IFNG',set(isg)&set(ifng))
print('IFNG.GS not in Hallmark:',sorted(set(ifng)-H))
print('Hallmark not in ISG.RS or IFNG.GS:',sorted(H-set(ifng)-set(isg)))
print('ISG.RS in Hallmark IFNG:',len(set(isg)&H),'of',len(isg))
print('MVP: in ISG.RS',('MVP' in isg),' in IFNG.GS',('MVP' in ifng),' position',ifng.index('MVP') if 'MVP' in ifng else None,' in Hallmark IFNG',('MVP' in H),' Hallmark IFNA',('MVP' in A))
fix={'CIS':'C1S'}  # patent OCR of C1S; verified by Hallmark membership below
ifng=[fix.get(g,g) for g in ifng]
assert 'C1S' in H
out=dict(meta=dict(ISG_RS='US12662705 claim text; identical set to Qiu 2023 Fig 1E source data',IFNG_GS='US12662705 claim text (Minn lab patent); Benci 2019 Table S1 PDF could not be fetched',hallmark='MSigDB 2024.1.Hs',note='MVP retained here as published. scores.py removes it before any scoring.'),
 ISG_RS=isg,IFNG_GS=ifng,HALLMARK_IFNG=sorted(H),HALLMARK_IFNA=sorted(A))
json.dump(out,open('data/genesets/genesets.json','w'),indent=1)
print('sha256',hashlib.sha256(open('data/genesets/genesets.json','rb').read()).hexdigest())
