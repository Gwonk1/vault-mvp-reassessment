"""Does the translation enrichment replicate in a physical-contact instrument?
Pre-registered in IPMS_TRANSLATION_PREREGISTRATION.md. Same table and parse as section 13."""
import openpyxl, json, re, numpy as np, pandas as pd, warnings
warnings.filterwarnings('ignore')

TERM = 'GOBP_CYTOPLASMIC_TRANSLATION'
NRAND = 200

sets = {}
for f in ['data/raw/eggnog/c5.go.bp.v2024.1.Hs.symbols.gmt',
          'data/raw/eggnog/c5.go.cc.v2024.1.Hs.symbols.gmt']:
    for line in open(f):
        p = line.rstrip('\n').split('\t')
        sets[p[0]] = set(p[2:])

# --- identical parse to src/crosstest.py (section 13) ---
wb = openpyxl.load_workbook('argon/raw/lodwick_supp_4.xlsx', read_only=True, data_only=True)
rows = list(wb['Fig. 5c-d'].iter_rows(values_only=True))
D = pd.DataFrame(rows[1:], columns=list(rows[0])).dropna(subset=['GeneName'])
for c in D.columns[1:]:
    D[c] = pd.to_numeric(D[c], errors='coerce')
D = D.drop_duplicates('GeneName').set_index('GeneName')
print(f'IP-MS universe: {len(D)} proteins | columns: {list(D.columns)}', flush=True)

wt = set(D.index[(D.WT_LFC > 0) & (D.LWTP > 1.3)])
print(f'WT vault interactors (WT_LFC>0 & LWTP>1.3): {len(wt)}', flush=True)

# --- GATE: the pulldown must recover the vault ---
core = {}
for g in ['MVP', 'PARP4', 'TEP1']:
    if g in D.index:
        r = D.loc[g]
        core[g] = {'WT_LFC': round(float(r.WT_LFC), 3), 'LWTP': round(float(r.LWTP), 3),
                   'interactor': bool(r.WT_LFC > 0 and r.LWTP > 1.3)}
    else:
        core[g] = None
n_core = sum(1 for v in core.values() if v and v['interactor'])
gate = n_core >= 2
print(f'GATE core recovery: {core}')
print(f'  {n_core}/3 of MVP/PARP4/TEP1 meet interactor criteria -> {"PASS" if gate else "FAIL"}', flush=True)

# --- abundance proxy: a WT_LFC-independent intensity-like column if present, else row order ---
abund_col = next((c for c in D.columns if re.search(r'intens|abund|ibaq|pep', str(c), re.I)), None)
if abund_col is not None:
    ab = D[abund_col]
    print(f'abundance proxy column: {abund_col}', flush=True)
else:
    ab = pd.Series(np.arange(len(D)), index=D.index)
    print('no intensity column found; using table order as the abundance proxy', flush=True)
dec = pd.qcut(ab.rank(method='first'), 10, labels=False, duplicates='drop')

rng = np.random.default_rng(0)
def spec(gs, n=NRAND):
    mem = [g for g in gs if g in D.index]
    if len(mem) < 5: return None
    obs = len(set(mem) & wt)
    prof = dec.loc[mem].value_counts()
    hits = 0
    for _ in range(n):
        pick = []
        for d_, k in prof.items():
            pool = dec.index[dec == d_]
            if len(pool) == 0: continue
            pick += list(rng.choice(pool, size=min(k, len(pool)), replace=False))
        if len(set(pick) & wt) >= obs: hits += 1
    return {'n_in_universe': len(mem), 'obs': obs,
            'exp': round(len(mem) * len(wt) / len(D), 2), 'p': hits / n}

prim = spec(sets[TERM])
print(f'\nPRIMARY {TERM}: {prim}', flush=True)
# context terms, no registered threshold
ctx = {t: spec(sets.get(t, set())) for t in
       ['GOCC_RIBOSOME', 'GOBP_TRANSLATION', 'GOCC_RUFFLE',
        'GOBP_ACTIN_FILAMENT_ORGANIZATION', 'GOCC_MITOCHONDRION']}
print('context (no registered threshold):')
for t, v in ctx.items():
    print(f'  {t:<36} {v}', flush=True)

if not gate:
    verdict = 'UNINFORMATIVE (gate failed)'
elif prim and prim['p'] < 0.05:
    verdict = f"REPLICATES in a contact instrument (p={prim['p']})"
else:
    verdict = 'KILL CONDITION MET - does not replicate; translation tail is co-migration, not contact'
print('\nVERDICT:', verdict, flush=True)

# --- Instrument B/C: descriptive only ---
amoeba = json.load(open('argon/results/test_a2_interactome.json'))
tm = sets[TERM] | sets['GOCC_RIBOSOME']
dicty = [(r['gene_symbols_or_id'], round(r['log2fc'], 2))
         for r in amoeba['dicty_mvpa_top60']
         if re.match(r'^RP[LS]', str(r['gene_symbols_or_id']), re.I)]
bp = []
for k in ['bioplex_HEK293T', 'bioplex_HCT116']:
    for r in amoeba.get(k, []):
        for s in (r.get('SymbolA'), r.get('SymbolB')):
            if s and s != 'MVP' and s in tm: bp.append((k, s))
print(f'\nInstrument B (amoeba top60, descriptive): ribosomal entries = {dicty}')
print(f'Instrument C (BioPlex, descriptive): translation/ribosome partners = {bp or "none"}', flush=True)

json.dump({'universe': len(D), 'wt_interactors': len(wt), 'core': core,
           'gate': bool(gate), 'abundance_proxy': str(abund_col),
           'primary': {TERM: prim}, 'context': ctx, 'verdict': verdict,
           'amoeba_ribosomal': dicty, 'bioplex_translation': bp},
          open('results/ipms_translation.json', 'w'), indent=1, default=str)
