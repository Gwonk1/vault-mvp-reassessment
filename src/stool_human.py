import sys, openpyxl, re, warnings
warnings.filterwarnings('ignore')
wb=openpyxl.load_workbook(sys.argv[1],read_only=True,data_only=True)
ws=wb.worksheets[0]; rows=list(ws.iter_rows(values_only=True))
hdr=rows[0]
print('columns:',[str(x) for x in hdr if x is not None][:12])
hum=[r for r in rows if any(x is not None and '_HUMAN' in str(x) for x in r)]
print(f'\n{len(hum)} human rows. Listing accession + description + unique peptides:\n')
# find column indices
ia=0; idx_desc=1
iu=next((i for i,h in enumerate(hdr) if h and 'Unique Peptides' in str(h)), None)
ic=next((i for i,h in enumerate(hdr) if h and 'Coverage' in str(h)), None)
out=[]
for r in hum:
    acc=str(r[ia]); desc=str(r[idx_desc])[:78]
    up=r[iu] if iu is not None else '?'
    cov=r[ic] if ic is not None else '?'
    out.append((up if isinstance(up,(int,float)) else 0,acc,desc,up,cov))
out.sort(key=lambda x:-x[0])
for _,acc,desc,up,cov in out[:45]:
    print(f'  {acc:<22} uniq={str(up):<5} cov={str(cov)[:5]:<6} {desc}')
print(f'\n  ... {len(out)} total human rows')
print('\n=== explicit search for vault / MVP across ALL rows ===')
for r in rows:
    j=' '.join(str(x) for x in r if x is not None)
    if re.search(r'\bMVP\b|MVP_HUMAN|vault|Q14764',j,re.I):
        print('  HIT:',j[:200])
print('  (no output above means absent)')
