"""Gene set scoring. MVP can never enter a score: scoring aborts if it does."""
import json
import numpy as np, pandas as pd

TARGET_ALIASES = {'MVP', 'LRP', 'VAULT1', 'LRP/MVP'}
RENAMES = {'DDX58': 'RIGI', 'FTSJD2': 'CMTR1', 'MARCH1': 'MARCHF1', 'METTL7B': 'TMT1B', 'PRIC285': 'HELZ2', 'WARS': 'WARS1'}


def assert_no_target(genes, label=''):
    bad = TARGET_ALIASES & set(genes)
    if bad:
        raise AssertionError(f'MVP LEAK: {bad} in gene set {label}; correlating MVP with itself')


def load_sets(path='data/genesets/genesets.json'):
    d = json.load(open(path))
    sets = {k: [g for g in d[k] if g not in TARGET_ALIASES] for k in ['ISG_RS', 'IFNG_GS', 'HALLMARK_IFNG', 'HALLMARK_IFNA']}
    for k, v in sets.items():
        assert_no_target(v, k)
    return sets


def resolve(genes, index):
    """Map set members onto a matrix's symbols, trying the old/new symbol pair."""
    rev = {v: k for k, v in RENAMES.items()}
    out = []
    for g in genes:
        for c in (g, RENAMES.get(g), rev.get(g)):
            if c is not None and c in index:
                out.append(c); break
    return sorted(set(out))


def to_log(m):
    """log2(x+1) when the matrix is on a linear scale. Returns matrix and a unit note."""
    v = m.values[np.isfinite(m.values)]
    if np.nanquantile(v, .999) > 40:
        return np.log2(m.clip(lower=0) + 1), 'linear->log2(x+1)'
    return m, 'already log'


def zgenes(m):
    s = m.std(axis=1, ddof=1)
    return m.sub(m.mean(axis=1), axis=0).div(s.where(s > 0), axis=0)


def score(z, genes, label=''):
    assert_no_target(genes, label)
    g = resolve(genes, z.index)
    assert_no_target(g, label)
    return z.loc[g].mean(axis=0), g


if __name__ == '__main__':
    # The assertion must fail loudly. Prove it does.
    d = json.load(open('data/genesets/genesets.json'))
    assert 'MVP' in d['IFNG_GS'] and 'MVP' in d['HALLMARK_IFNG'], 'source lists changed'
    s = load_sets()
    assert 'MVP' not in s['IFNG_GS'] and 'MVP' not in s['HALLMARK_IFNG']
    try:
        assert_no_target(d['IFNG_GS'], 'raw IFNG_GS')
    except AssertionError as e:
        print('assertion fires on raw list, as required:', e)
    else:
        raise SystemExit('assertion failed to fire')
    print({k: len(v) for k, v in s.items()})
