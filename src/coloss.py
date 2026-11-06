"""Event-based co-loss per COLOSS_PREREGISTRATION.md. Usage: coloss.py controls | final"""
import gzip, json, sys, numpy as np, pandas as pd
from scipy.stats import hypergeom
R = 'data/raw/eggnog/'
BLIND = {'MVP', 'TEP1', 'PARP4'}
z = np.load('data/processed/eggnog_presence.npz'); M0, OG, SP = z['M'], z['ogs'], z['species']
keep_sp = M0.sum(axis=0) >= 2500
M0 = M0[:, keep_sp]; SP = SP[keep_sp]
tax = pd.read_csv(R + 'e5.taxid_info.tsv', sep='\t', dtype=str); tax.columns = ['taxid', 'name', 'rank', 'names', 'lineage']; tax = tax.set_index('taxid')
hum = json.load(open('data/processed/eggnog_human.json'))
sym = {}
for l in gzip.open(R + 'gencode.v25.pc_translations.fa.gz', 'rt'):
    if l[0] == '>':
        p = l[1:].split('|'); sym[p[0].split('.')[0]] = p[6]
HS = {o: sorted({sym[x] for x in hum.get(o, []) if x in sym}) for o in OG.tolist()}
# tree
kids, under, names = {}, {}, {}
for i, s in enumerate(SP):
    lin = tax.lineage[s].split(','); nm = tax.names[s].split(',')
    for a, b in zip(lin[:-1], lin[1:]): kids.setdefault(a, set()).add(b)
    for x, n in zip(lin, nm): under.setdefault(x, set()).add(i); names[x] = n
def collapse(n):
    while len(kids.get(n, ())) == 1 and len(under[next(iter(kids[n]))]) == len(under[n]): n = next(iter(kids[n]))
    return n
ROOT = collapse('1')
nodes, ch, par = [], {}, {}
def walk(n):
    nodes.append(n); cs = [collapse(c) for c in kids.get(n, ())]
    ch[n] = cs
    for c in cs: par[c] = n; walk(c)
walk(ROOT)
ni = {n: i for i, n in enumerate(nodes)}
NM = np.zeros((len(nodes), len(SP)), dtype=bool)
for n in nodes: NM[ni[n], list(under[n])] = True
sz = NM.sum(axis=1)
pres = M0.sum(axis=1)
use = pres >= 10
M = M0[use]; OGS = OG[use]; idx = {o: i for i, o in enumerate(OGS.tolist())}
F = (M.astype(np.float32) @ NM.T.astype(np.float32)) / sz            # OG x node presence fraction
P = np.array([ni[par[n]] if n in par else -1 for n in nodes])
Sib = np.zeros((M.shape[0], len(nodes)), dtype=np.float32)            # presence in the sister species of each node
for j, n in enumerate(nodes):
    if P[j] >= 0:
        o = NM[P[j]] & ~NM[j]
        Sib[:, j] = M[:, o].mean(axis=1) if o.any() else 0
def events(g):
    v = F[g]; tot = M[g].sum(); n = ROOT
    while True:
        nx = [c for c in ch[n] if (M[g] & NM[ni[c]]).sum() >= .9 * tot]
        if not nx: break
        n = nx[0]
    out = []
    def go(x):
        for c in ch[x]:
            j = ni[c]
            if sz[j] < 2: continue
            if v[j] <= .1: out.append(j)
            else: go(c)
    go(n)
    return out
Ev = np.zeros((M.shape[0], len(nodes)), dtype=bool)
for g in range(M.shape[0]):
    Ev[g, events(g)] = True
nev = Ev.sum(axis=1); frac = M.mean(axis=1)
has_h = np.array([bool(HS[o]) for o in OGS.tolist()])
scored = np.where(has_h & (nev >= 1))[0]
def score(q):
    L = np.where(Ev[q])[0]
    co = ((F[:, L] <= .1) & (Sib[:, L] >= .5)).sum(axis=1)
    qon = F[q] > .5
    go = (Ev[:, qon]).sum(axis=1)
    s = co / np.maximum(co + (len(L) - co) + go, 1)
    d = pd.DataFrame({'og': OGS, 's': s, 'co': co, 'g_only': go, 'nev': nev})
    d = d.iloc[scored]; d = d[d.og != OGS[q]]
    return d.sort_values(['s', 'co', 'g_only'], ascending=[False, False, True]), L
SETS = {}
for f in ['c5.go.bp.v2024.1.Hs.symbols.gmt', 'c5.go.cc.v2024.1.Hs.symbols.gmt']:
    for l in open(R + f):
        p = l.rstrip('\n').split('\t'); SETS[p[0]] = set(p[2:])
UNI = OGS[scored].tolist()
ANN = {}
for t, gs in SETS.items():
    m = {o for o in UNI if gs & set(HS[o])}
    if 10 <= len(m) <= 500: ANN[t] = m
print('species', len(SP), 'nodes', len(nodes), 'scored OGs', len(UNI), 'terms', len(ANN), flush=True)
def enrich(top):
    T = set(top); rows = []
    for t, m in ANN.items():
        k = len(T & m)
        if k: rows.append((t, k, len(m), hypergeom.sf(k - 1, len(UNI), len(m), len(T))))
    r = pd.DataFrame(rows, columns=['term', 'k', 'K', 'p']).sort_values('p').reset_index(drop=True)
    if len(r):
        n = len(ANN); r['q'] = (r.p * n / (r.index + 1)).iloc[::-1].cummin().iloc[::-1].clip(upper=1)
    return r
def og_of(s):
    c = [o for o in OGS.tolist() if s in HS[o]]
    return sorted(c, key=lambda o: len(HS[o]))[0]
def query(s):
    q = idx[og_of(s)]; d, L = score(q)
    return q, d, L, enrich(d[d.co >= 1].og.head(100).tolist())
mode = sys.argv[1]; out = {}
gate = {}
for s, want in (('IFT88', ['GOCC_INTRACILIARY_TRANSPORT_PARTICLE', 'GOCC_CILIUM']), ('NDUFS2', ['GOCC_NADH_DEHYDROGENASE_COMPLEX', 'GOCC_RESPIRASOME'])):
    q, d, L, e = query(s)
    hit = e[e.term.isin(want)]
    gate[s] = bool((hit.q < .05).any())
    print(f'\nCONTROL {s} OG {OGS[q]} events {len(L)} gate', 'PASS' if gate[s] else 'FAIL'); print(hit.round(5).to_string()); print(e.head(8).round(5).to_string(max_colwidth=60))
    print(' top', [HS[o][:2] for o in d.og.head(14)])
out['gate'] = gate
if mode == 'final':
    q, d, L, e = query('MVP')
    print('\nMVP OG', OGS[q], 'events', len(L), [(names[nodes[j]], int(sz[j])) for j in L], 'presence', round(float(frac[q]), 3))
    rng = np.random.default_rng(20261106)
    cand = scored[(np.abs(nev[scored] - len(L)) <= 1) & (np.abs(frac[scored] - frac[q]) <= .1) & (scored != q)]
    print('matched candidates', len(cand))
    ch_q = rng.choice(cand, size=min(200, len(cand)), replace=False)
    hits = {}; anyhit = 0
    for r in ch_q:
        dr, _ = score(r); er = enrich(dr[dr.co >= 1].og.head(100).tolist())
        anyhit += int((er.q < .05).any())
        for t in er[er.q < .05].term: hits[t] = hits.get(t, 0) + 1
    e['spec'] = e.term.map(lambda t: hits.get(t, 0) / len(ch_q))
    sig = e[e.q < .05]
    lab = 'MODULE LEAD' if (sig.spec < .05).any() else ('NON-SPECIFIC' if len(sig) else 'NO MODULE')
    print('\nLABEL', lab, '| matched queries', len(ch_q), '| fraction of matched queries with any q<.05 term', round(anyhit/len(ch_q),3))
    print(e.head(25).round(5).to_string(max_colwidth=70))
    top = d.head(60).assign(genes=lambda x: [','.join(HS[o][:4]) for o in x.og])
    print(top[['genes', 's', 'co', 'g_only', 'nev']].round(3).to_string(max_colwidth=50))
    print('score distribution', d.s.describe().round(3).to_dict(), 'co', d.co.value_counts().sort_index().to_dict())
    for s in ['TEP1', 'PARP4']:
        for o in [x for x in OGS.tolist() if s in HS[x]]:
            r = list(d.og).index(o) + 1 if o in set(d.og) else None
            print(s, o, HS[o][:6], 'rank', r, 'of', len(d), 'events', int(nev[idx[o]]), d[d.og == o][['s', 'co', 'g_only']].round(3).to_dict('records'))
    e.to_csv('results/coloss_mvp_enrichment.csv', index=False); top.to_csv('results/coloss_mvp_top.csv', index=False)
    out.update(label=lab, events=[(names[nodes[j]], int(sz[j])) for j in L], matched=len(ch_q), top_terms=e.head(20).to_dict('records'))
json.dump(out, open(f'results/coloss_{mode}.json', 'w'), indent=1, default=float)
