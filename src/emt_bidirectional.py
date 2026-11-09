"""Bidirectional EMT control. Implements EMT_BIDIRECTIONAL_PREREGISTRATION.md.
Do not edit thresholds after the result is known."""
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr, pearsonr

PRIMARY = "GOBP_PLASMA_MEMBRANE_REPAIR"
SECONDARY = [
    "GOCC_LYSOSOME", "GOCC_LATE_ENDOSOME", "GOBP_ENDOSOMAL_TRANSPORT",
    "GOCC_CAVEOLA", "GOCC_MEMBRANE_RAFT", "GOBP_PLASMA_MEMBRANE_ORGANIZATION",
]
PROLIF = ["MKI67", "TOP2A", "MCM2", "MCM6", "PCNA", "MYBL2"]
SCORE_MES = ["ZEB1", "ZEB2", "SNAI1", "SNAI2", "TWIST1", "PRRX1", "FOXC2", "CDH2"]
SCORE_EPI = ["ESRP1", "ESRP2", "GRHL2", "OCLN", "CLDN4", "CLDN7", "TJP3", "CRB3"]
VAL_MES = ["VIM", "FN1", "SPARC", "MMP2"]
VAL_EPI = ["CDH1", "EPCAM", "KRT8", "DSP"]
NAMED = ["PARP4", "TEP1", "ANXA2", "S100A10", "EHD2", "EHD4", "CAPN2", "MYOF", "AHNAK", "AHNAK2"]

ROOT = Path(__file__).resolve().parents[1]


def load_sets():
    sets = {}
    for name in [
        "data/raw/eggnog/c5.go.bp.v2024.1.Hs.symbols.gmt",
        "data/raw/eggnog/c5.go.cc.v2024.1.Hs.symbols.gmt",
    ]:
        for line in open(ROOT / name):
            p = line.rstrip("\n").split("\t")
            sets[p[0]] = set(p[2:])
    return sets


def main():
    sets = load_sets()
    tested = set()
    for name in [PRIMARY] + SECONDARY:
        tested |= sets.get(name, set())
    drop = tested | {"MVP", "PARP4", "TEP1"}

    M = pd.read_parquet(ROOT / "data/processed/prot/ccle_broad_2019.parquet")
    M = M[~M.index.duplicated()]
    Z = M.sub(M.mean(axis=1), axis=0).div(M.std(axis=1).replace(0, np.nan), axis=0)

    def arm(genes):
        kept, excluded = [], []
        for g in genes:
            if g in drop:
                excluded.append(g)
            elif g in Z.index:
                kept.append(g)
        return kept, excluded

    mes, mes_ex = arm(SCORE_MES)
    epi, epi_ex = arm(SCORE_EPI)
    print(f"score arms: mes {len(mes)}/{len(SCORE_MES)} epi {len(epi)}/{len(SCORE_EPI)}", flush=True)
    print(f"excluded from score: mes {mes_ex} epi {epi_ex}", flush=True)

    out = {
        "score_mes_used": mes,
        "score_epi_used": epi,
        "score_excluded": {"mes": mes_ex, "epi": epi_ex},
    }
    if len(mes) < 6 or len(epi) < 6:
        out["verdict"] = "UNINFORMATIVE (score arm under 6 genes)"
        dump(out)
        return

    score = Z.loc[mes].mean() - Z.loc[epi].mean()

    def mean_r(genes):
        rs, present = [], []
        for g in genes:
            if g not in Z.index:
                continue
            pair = pd.concat([Z.loc[g], score], axis=1).dropna()
            if len(pair) < 50:
                continue
            r, _ = pearsonr(pair.iloc[:, 0], pair.iloc[:, 1])
            rs.append(float(r))
            present.append(g)
        return present, rs

    vmes, rmes = mean_r(VAL_MES)
    vepi, repi = mean_r(VAL_EPI)
    out["validators"] = {
        "mes": dict(zip(vmes, [round(r, 4) for r in rmes])),
        "epi": dict(zip(vepi, [round(r, 4) for r in repi])),
        "mes_mean": None if not rmes else round(float(np.mean(rmes)), 4),
        "epi_mean": None if not repi else round(float(np.mean(repi)), 4),
    }
    gate3 = bool(
        len(vmes) >= 3 and len(vepi) >= 3
        and float(np.mean(rmes)) >= 0.30 and float(np.mean(repi)) <= -0.30
    )
    print(f"GATE3 validators {out['validators']} -> {'PASS' if gate3 else 'FAIL'}", flush=True)

    cyto = [g for g in Z.index if str(g).startswith(("RPL", "RPS")) and "P1" not in str(g)]
    nuc = [g for g in Z.index if str(g).startswith(("HNRNP", "SRSF", "SF3B", "SMC"))]
    nc = Z.loc[cyto].mean() - Z.loc[nuc].mean()
    C = pd.concat(
        [nc.rename("nc"), score.rename("emt")]
        + [Z.loc[g].rename(g) for g in PROLIF if g in Z.index],
        axis=1,
    ).dropna()
    Zc = Z[C.index]
    Zc = Zc.loc[Zc.notna().sum(axis=1) >= 150]
    Xfull = np.c_[np.ones(len(C)), C.values]

    def resid(row):
        m = row.notna().values
        y = row.values[m]
        b = np.linalg.lstsq(Xfull[m], y, rcond=None)[0]
        o = np.full(len(row), np.nan)
        o[m] = y - Xfull[m] @ b
        return o

    R = pd.DataFrame(
        np.vstack([resid(Zc.loc[g]) for g in Zc.index]),
        index=Zc.index, columns=C.index,
    )

    def ranked(seed):
        s = R.loc[seed].values
        vals = {}
        for g in R.index:
            if g == seed:
                continue
            o = R.loc[g].values
            m = np.isfinite(s) & np.isfinite(o)
            if m.sum() < 100:
                continue
            r, _ = spearmanr(s[m], o[m])
            if np.isfinite(r):
                vals[g] = r
        return pd.Series(vals).sort_values(ascending=False)

    mvp = ranked("MVP")
    g1 = {g: (list(mvp.index).index(g) + 1 if g in mvp.index else None) for g in ["PARP4", "TEP1"]}
    gate1 = all(v is not None and v <= 50 for v in g1.values())
    psma = ranked("PSMA1")
    subs = {g for g in R.index if str(g).startswith(("PSMA", "PSMB", "PSMC", "PSMD"))}
    rec = len(set(psma.index[:50]) & subs)
    gate2 = rec >= 10
    print(f"GATE1 {g1} -> {'PASS' if gate1 else 'FAIL'}", flush=True)
    print(f"GATE2 proteasome {rec} -> {'PASS' if gate2 else 'FAIL'}", flush=True)

    top200 = set(mvp.index[:200])
    abund = M.mean(axis=1).reindex(R.index)
    dec = pd.qcut(abund.rank(method="first"), 10, labels=False)
    rng = np.random.default_rng(0)

    def spec(gs, n=200):
        mem = sorted(g for g in gs if g in R.index)
        if len(mem) < 5:
            return None
        obs = len(set(mem) & top200)
        prof = dec.loc[mem].value_counts().sort_index()
        hits = 0
        for _ in range(n):
            pick = []
            for d, k in prof.items():
                pool = dec.index[dec == d]
                pick += list(rng.choice(pool, size=min(int(k), len(pool)), replace=False))
            if len(set(pick) & top200) >= obs:
                hits += 1
        return {"n_members": len(mem), "observed_in_top200": obs, "specificity_p": hits / n}

    prim = spec(sets.get(PRIMARY, set()))
    sec = {t: spec(sets.get(t, set())) for t in SECONDARY}
    print(f"PRIMARY {prim}", flush=True)
    for t, v in sec.items():
        print(f"  {t}: {v}", flush=True)

    if not (gate1 and gate2 and gate3):
        verdict = "UNINFORMATIVE (gate failed)"
    elif prim and prim["specificity_p"] < 0.05:
        verdict = "MODULE SURVIVES bidirectional EMT adjustment"
    else:
        verdict = "KILL: membrane-repair neighbourhood does not survive EMT adjustment"
    print("VERDICT:", verdict, flush=True)

    ranks = {g: (int(list(mvp.index).index(g) + 1) if g in mvp.index else None) for g in NAMED}
    out.update({
        "gate1_assembly": gate1, "gate1_ranks": g1,
        "gate2_proteasome": gate2, "gate2_recovered": rec,
        "gate3_score_valid": gate3,
        "verdict": verdict,
        "primary": {PRIMARY: prim},
        "secondary": sec,
        "n_proteins": int(R.shape[0]),
        "named_ranks": ranks,
        "named_rho": {g: (round(float(mvp[g]), 4) if g in mvp.index else None) for g in NAMED},
        "mvp_top30": {k: round(float(v), 4) for k, v in mvp.head(30).items()},
    })
    dump(out)


def dump(out):
    dest = ROOT / "results" / "emt_bidirectional.json"
    json.dump(out, open(dest, "w"), indent=1, default=lambda o: bool(o) if isinstance(o, np.bool_) else o)
    print(f"wrote {dest}", flush=True)


if __name__ == "__main__":
    main()
