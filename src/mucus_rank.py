"""Is MVP over-represented in mucus relative to leakage expectation?
Leakage should scale with cellular abundance, and ACTB/GAPDH/HSPA8 are far more
abundant in cells than MVP. Compare their mucus intensities directly."""
import sys, openpyxl, numpy as np, warnings
warnings.filterwarnings('ignore')
PROBE=['MVP','ACTB','GAPDH','HSPA8','ANXA2','MUC2','ALB','S100A10','LGALS3']
for path in sys.argv[1:]:
    wb=openpyxl.load_workbook(path,read_only=True,data_only=True); ws=wb.worksheets[0]
    rows=list(ws.iter_rows(values_only=True))
    hdr=None; hi=None
    for i,r in enumerate(rows[:6]):
        if sum(1 for x in r if x is not None)>3: hdr=r; hi=i; break
    cols={}
    for j,h in enumerate(hdr or []):
        hs=str(h)
        if 'Gene names' in hs: cols['gene']=j
        elif hs.startswith('Annotation'): cols['ann']=j
        elif 'Core mucus' in hs: cols['core']=j
        elif 'ormali' in hs and 'intensity' in hs.lower(): cols.setdefault('int',[]).append(j)
        elif hs.startswith('Peptide counts (unique'): cols['pep']=j
    if 'gene' not in cols:   # supp003 has header split across rows
        print(f'{path.split("/")[-1]}: header layout differs, skipping'); continue
    ic_int=[]; out={}
    for r in rows[hi+1:]:
        g=r[cols['gene']]
        if g is None: continue
        g=str(g).split(';')[0].strip()
        vals=[r[j] for j in cols.get('int',[]) if isinstance(r[j],(int,float))]
        if not vals: continue
        m=float(np.median(vals))
        ann=str(r[cols['ann']]) if 'ann' in cols else '?'
        if ann=='IC': ic_int.append(m)
        if g in PROBE:
            out[g]={'median_int':m,'ann':ann,
                    'core':str(r[cols['core']]) if 'core' in cols else '?',
                    'pep':r[cols['pep']] if 'pep' in cols else '?'}
    allint=[]
    for r in rows[hi+1:]:
        vals=[r[j] for j in cols.get('int',[]) if isinstance(r[j],(int,float))]
        if vals: allint.append(float(np.median(vals)))
    allint=np.array(allint); ic=np.array(ic_int)
    print('='*78); print(f'{path.split("/")[-1]}  ({len(allint)} quantified proteins, {len(ic)} annotated IC)')
    for g in PROBE:
        if g in out:
            v=out[g]; pr=100*(allint<v['median_int']).mean(); pi=100*(ic<v['median_int']).mean()
            print(f"  {g:<9} median intensity {v['median_int']:>14,.0f}  ann={v['ann']:<3} core={v['core']:<5} "
                  f"uniq_pep={v['pep']:<4} pct_all={pr:5.1f} pct_IC={pi:5.1f}")
        else: print(f'  {g:<9} not quantified in this table')
    if 'MVP' in out and 'GAPDH' in out:
        print(f"  --> MVP / GAPDH intensity ratio = {out['MVP']['median_int']/out['GAPDH']['median_int']:.2f}")
    if 'MVP' in out and 'ACTB' in out:
        print(f"  --> MVP / ACTB  intensity ratio = {out['MVP']['median_int']/out['ACTB']['median_int']:.2f}")
