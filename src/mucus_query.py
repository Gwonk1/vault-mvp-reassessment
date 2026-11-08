"""Query the van der Post 2019 human colonic mucus tables for MVP + registered controls.
Protocol: FECAL_MUCUS_PROTOCOL.md. Gate FIRST, independently of MVP."""
import sys, openpyxl, re
CTRL_INTRA=['ACTB','GAPDH','HSPA8']
CTRL_SECR=['ALB','LTF','LCN2','MUC2']
TARGET=['MVP','LRP','Q14764']
ALL=CTRL_INTRA+CTRL_SECR+TARGET+['PARP4','TEP1']
for path in sys.argv[1:]:
    print('='*74); print(path.split('/')[-1])
    try: wb=openpyxl.load_workbook(path,read_only=True,data_only=True)
    except Exception as e: print('  cannot open:',e); continue
    for ws in wb.worksheets:
        hits={}; nrow=0; cells=0
        for row in ws.iter_rows(values_only=True):
            nrow+=1
            for v in row:
                if v is None: continue
                cells+=1
                s=str(v).strip()
                # exact token match anywhere in the cell, semicolon/space/pipe separated
                for tok in re.split(r'[;,\s|/]+',s):
                    t=tok.strip().upper()
                    if t in ALL: hits.setdefault(t,[]).append((nrow,s[:70]))
        print(f'  sheet "{ws.title}": {nrow} rows, {cells} non-empty cells')
        if hits:
            for t in ALL:
                if t in hits:
                    n=len(hits[t]); r0,s0=hits[t][0]
                    print(f'    {t:<8} FOUND {n}x  first at row {r0}: {s0}')
        else:
            print('    none of the queried identifiers found in this sheet')
