"""Is the vault core a trimer, or MVP-PARP4 with TEP1 recruited through PARP4?
Pre-registered in TRIMER_PREREGISTRATION.md. Same table and parse as sections 13 and 41."""
import openpyxl, json, pandas as pd, warnings
warnings.filterwarnings('ignore')

NAMED = ['ANXA2', 'S100A10', 'EHD2', 'EHD4', 'CAPN2', 'IQGAP1', 'MYOF', 'AHNAK']

wb = openpyxl.load_workbook('argon/raw/lodwick_supp_4.xlsx', read_only=True, data_only=True)
rows = list(wb['Fig. 5c-d'].iter_rows(values_only=True))
D = pd.DataFrame(rows[1:], columns=list(rows[0])).dropna(subset=['GeneName'])
for c in D.columns[1:]:
    D[c] = pd.to_numeric(D[c], errors='coerce')
D = D.drop_duplicates('GeneName').set_index('GeneName')

def status(g):
    if g not in D.index: return None
    r = D.loc[g]
    wt = bool(r.WT_LFC > 0 and r.LWTP > 1.3)
    dep = bool(wt and r.WTKD_LFC > 0 and r.WTKD_P > 1.3)
    return {'WT_LFC': round(float(r.WT_LFC), 3), 'LWTP': round(float(r.LWTP), 3),
            'WTKD_LFC': round(float(r.WTKD_LFC), 3), 'WTKD_P': round(float(r.WTKD_P), 3),
            'wt_interactor': wt, 'parp4_dependent': dep}

core = {g: status(g) for g in ['MVP', 'PARP4', 'TEP1']}
print('core proteins:')
for g, v in core.items():
    print(f'  {g:<7} {v}', flush=True)

g1 = core['MVP'] and core['MVP']['wt_interactor'] and not core['MVP']['parp4_dependent']
g2 = core['PARP4'] and core['PARP4']['parp4_dependent']
gate = bool(g1 and g2)
print(f"\nGATE1 MVP is a WT interactor and NOT PARP4-dependent: {g1}")
print(f"GATE2 PARP4 is itself PARP4-dependent: {g2}")
print(f"  => {'PASS' if gate else 'FAIL'}", flush=True)

t = core['TEP1']
if not gate:                       verdict = 'UNINFORMATIVE (gate failed)'
elif not (t and t['wt_interactor']): verdict = 'UNINFORMATIVE (TEP1 not a WT interactor)'
elif t['parp4_dependent']:         verdict = 'TEP1 IS PARP4-DEPENDENT - core is MVP-PARP4, TEP1 recruited through PARP4'
else:                              verdict = 'TEP1 is NOT PARP4-dependent - trimer language stands'
print('\nVERDICT:', verdict, flush=True)

wt = D[(D.WT_LFC > 0) & (D.LWTP > 1.3)]
dep = wt[(wt.WTKD_LFC > 0) & (wt.WTKD_P > 1.3)]
print(f'\nsecondary: {len(dep)} of {len(wt)} WT interactors are PARP4-dependent '
      f'({100*len(dep)/len(wt):.1f}%)', flush=True)
named = {g: status(g) for g in NAMED}
print('previously named proteins:')
for g, v in named.items():
    if v is None:
        print(f'  {g:<9} absent from table', flush=True)
    else:
        tag = 'PARP4-dep' if v['parp4_dependent'] else ('WT interactor' if v['wt_interactor'] else 'not an interactor')
        print(f'  {g:<9} {tag:<17} WT_LFC {v["WT_LFC"]:+.2f} LWTP {v["LWTP"]:.2f}', flush=True)

json.dump({'core': core, 'gate1_mvp': bool(g1), 'gate2_parp4': bool(g2), 'gate': gate,
           'verdict': verdict, 'n_wt_interactors': int(len(wt)),
           'n_parp4_dependent': int(len(dep)), 'named': named},
          open('results/trimer.json', 'w'), indent=1, default=str)
