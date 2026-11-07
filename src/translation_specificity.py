"""Is MVP's translation-enriched co-elution tail specific to MVP?
Pre-registered in TRANSLATION_SPECIFICITY_PREREGISTRATION.md."""
import gzip, json, numpy as np, pandas as pd
from collections import defaultdict

PATH = 'data/raw/cfdb/Homo_sapiens.tsv.gz'
TERM = 'GOBP_CYTOPLASMIC_TRANSLATION'
TOPN = 200
NRAND = 150
MIN_PARTNERS = 5000
NAMED = {
    'MVP': 'under test',
    'RPL7': 'gate: expect high', 'RPS6': 'gate: expect high',
    'PSMA1': 'gate: expect low',
    'GAPDH': 'abundant cytoplasmic', 'ENO1': 'abundant cytoplasmic',
    'PKM': 'abundant cytoplasmic', 'LDHA': 'abundant cytoplasmic',
    'ALDOA': 'abundant cytoplasmic',
    'FLOT1': 'SPFH family', 'FLOT2': 'SPFH family', 'STOM': 'SPFH family',
}

sets = {}
for f in ['data/raw/eggnog/c5.go.bp.v2024.1.Hs.symbols.gmt',
          'data/raw/eggnog/c5.go.cc.v2024.1.Hs.symbols.gmt']:
    for line in open(f):
        p = line.rstrip('\n').split('\t')
        sets[p[0]] = set(p[2:])
term_members = sets[TERM]
print(f'{TERM}: {len(term_members)} members', flush=True)

# one pass: per-protein top-N partner sets by score, plus partner counts
scores = defaultdict(list)
with gzip.open(PATH, 'rt') as fh:
    next(fh)
    for line in fh:
        p = line.rstrip('\n').split('\t')
        if len(p) < 4: continue
        a, b = p[0].strip('"'), p[1].strip('"')
        try: s = float(p[2])
        except ValueError: continue
        scores[a].append((s, b)); scores[b].append((s, a))
counts = {g: len(v) for g, v in scores.items()}
print(f'proteins with scored partners: {len(counts)}', flush=True)

eligible = sorted(g for g, n in counts.items() if n >= MIN_PARTNERS)
print(f'eligible seeds (>={MIN_PARTNERS} partners): {len(eligible)}', flush=True)
universe = set(counts)
in_term = len(term_members & universe)
expected = in_term * TOPN / len(universe)
print(f'term members in universe: {in_term} | expected in a top-{TOPN}: {expected:.2f}', flush=True)

def fold(seed):
    v = scores.get(seed)
    if not v or len(v) < MIN_PARTNERS: return None
    top = {g for _, g in sorted(v, key=lambda x: -x[0])[:TOPN]}
    return len(top & term_members) / expected

rng = np.random.default_rng(0)
pick = rng.choice([g for g in eligible if g not in NAMED], size=NRAND, replace=False)
dist = np.array([f for f in (fold(g) for g in pick) if f is not None])
print(f'\nrandom distribution over {len(dist)} seeds: '
      f'median {np.median(dist):.2f}x  75th {np.percentile(dist,75):.2f}x  '
      f'95th {np.percentile(dist,95):.2f}x  max {dist.max():.2f}x', flush=True)

def pct(x): return float((dist < x).mean() * 100)
res = {}
print('\nnamed seeds:')
for g, role in NAMED.items():
    f = fold(g)
    res[g] = {'role': role, 'fold': round(f, 2) if f else None,
              'percentile': round(pct(f), 1) if f else None,
              'n_partners': counts.get(g)}
    print(f"  {g:<7} {role:<22} fold {str(res[g]['fold']):<7} "
          f"percentile {res[g]['percentile']}", flush=True)

g1 = all(res[g]['percentile'] is not None and res[g]['percentile'] > 95 for g in ['RPL7','RPS6'])
g2 = res['PSMA1']['percentile'] is not None and res['PSMA1']['percentile'] < 90
gate = g1 and g2
print(f"\nGATE1 RPL7/RPS6 > 95th: {g1} | GATE2 PSMA1 < 90th: {g2} -> {'PASS' if gate else 'FAIL'}",
      flush=True)

mp = res['MVP']['percentile']
if not gate:      verdict = 'UNINFORMATIVE (gate failed)'
elif mp > 95:     verdict = f'MVP-SPECIFIC (percentile {mp})'
elif mp < 75:     verdict = f'KILL CONDITION MET - generic property; #168 struck (percentile {mp})'
else:             verdict = f'EQUIVOCAL (percentile {mp}) - promotes nothing'
print('VERDICT:', verdict, flush=True)

json.dump({'term': TERM, 'expected_in_top200': round(expected, 3),
           'random': {'n': len(dist), 'median': round(float(np.median(dist)), 3),
                      'p75': round(float(np.percentile(dist, 75)), 3),
                      'p95': round(float(np.percentile(dist, 95)), 3),
                      'max': round(float(dist.max()), 3)},
           'named': res, 'gate1_ribosomal': bool(g1), 'gate2_proteasome': bool(g2),
           'verdict': verdict},
          open('results/translation_specificity.json', 'w'), indent=1)
