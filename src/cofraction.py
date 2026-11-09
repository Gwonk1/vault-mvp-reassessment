"""Co-elution test. Implements COFRACTION_PREREGISTRATION.md exactly.
Chromatograms are read only at runtime, after the registration is committed."""
import json
import re
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import pearsonr

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "raw" / "cfms"
ACC = {
    "MVP": "Q14764", "PARP4": "Q9UKK3", "TEP1": "Q99973",
    "ANXA2": "P07355", "S100A10": "P60903", "MYOF": "Q9NZM1",
    "AHNAK": "Q09666", "AHNAK2": "Q8IVF2", "EHD2": "Q9NZN4",
    "EHD4": "Q9H223", "CAPN2": "P17655", "CD151": "P48509", "CAVIN1": "Q6NZI2",
    "PSMA1": "P25786", "PSMB1": "P20618", "PSMB2": "P49721",
    "PSMB3": "P49720", "PSMC1": "P62191", "PSMD1": "Q99460",
}
GENE = {v: k for k, v in ACC.items()}
REPAIR = ["ANXA2", "S100A10", "MYOF", "AHNAK", "AHNAK2", "EHD2", "EHD4", "CAPN2", "CD151", "CAVIN1"]
PROT = ["PSMB1", "PSMB2", "PSMB3", "PSMC1", "PSMD1"]
SEC_POS = ("sec", "size exclusion", "size-exclusion", "superose", "superdex", "gel filtration", "gel-filtration")
IEX = ("iex", "ion exchange", "ion-exchange", "sax", "wax", "scx")
DENS = ("sucrose", "glycerol gradient", "density gradient", "density-gradient")
QUANT_RANK = (("ibaq", 0), ("ms1", 1), ("intensity", 1), ("spectral", 2), ("count", 2))


def tokenise(value):
    text = str(value).upper()
    parts = re.split(r"[;|\s,]+", text)
    genes = set()
    for p in parts:
        p = p.split("_")[0]
        if p in GENE:
            genes.add(GENE[p])
        if p in ACC:
            genes.add(p)
        # gene_HUMAN style already split; also "MVP" inside a longer token
        for g in ACC:
            if p == g:
                genes.add(g)
    return genes


def method_of(path: Path, meta_text: str):
    blob = (str(path).lower() + "\n" + meta_text.lower())
    iex = any(k in blob for k in IEX)
    sec = any(k in blob for k in SEC_POS)
    dens = any(k in blob for k in DENS)
    if sec and not iex:
        return "SEC"
    if dens and not sec:
        return "density"
    if iex and not sec:
        return "IEX"
    return "unlabeled"


def quant_key(path: Path):
    name = path.name.lower()
    best = 9
    for token, rank in QUANT_RANK:
        if token in name:
            best = min(best, rank)
    return best


def read_gene_table(path: Path):
    """Row index is the protein id; columns are fractions in shipped order.

    These matrices are written with the id as an unnamed first field, so
    index_col=0 is the alignment that keeps fraction 01 in column 0.
    """
    try:
        df = pd.read_csv(path, sep="\t", index_col=0)
    except Exception:
        return None
    if df.shape[1] < 8 or df.shape[0] < 20:
        return None
    rows = {}
    for idx, rec in df.iterrows():
        genes = tokenise(idx)
        if not genes:
            continue
        vals = pd.to_numeric(rec, errors="coerce").astype(float).values
        for g in genes:
            if g not in rows:
                rows[g] = vals
    if "MVP" not in rows:
        return None
    return pd.DataFrame(rows).T


def profile_r(a, b):
    m = np.isfinite(a) & np.isfinite(b)
    if m.sum() < 8:
        return None
    if np.nanstd(a[m]) == 0 or np.nanstd(b[m]) == 0:
        return None
    r, _ = pearsonr(a[m], b[m])
    return float(r) if np.isfinite(r) else None


def analyse_experiment(table: pd.DataFrame):
    mvp = table.loc["MVP"].values.astype(float)
    finite = np.isfinite(mvp)
    if finite.sum() < 8:
        return None
    # peak on finite values; NaN is not a peak
    peak = int(np.nanargmax(mvp))
    n = len(mvp)
    early = ((peak + 1) / n) <= 0.20
    window = set(range(max(0, peak - 1), min(n, peak + 2)))

    def coelutes(gene):
        if gene not in table.index:
            return False, None, None
        vec = table.loc[gene].values.astype(float)
        r = profile_r(mvp, vec)
        if not np.isfinite(vec).any():
            return False, r, None
        gp = int(np.nanargmax(vec))
        ok = (r is not None and r >= 0.50) or (gp in window)
        return ok, r, gp

    partners = {}
    for g in ("PARP4", "TEP1"):
        ok, r, gp = coelutes(g)
        partners[g] = {"coelutes": ok, "r": None if r is None else round(r, 4), "peak": gp}
    both = partners["PARP4"]["coelutes"] and partners["TEP1"]["coelutes"]
    repair = {}
    for g in REPAIR:
        if g not in table.index:
            repair[g] = None
            continue
        vec = table.loc[g].values.astype(float)
        r = profile_r(mvp, vec)
        finite_n = int(np.isfinite(vec).sum())
        gp = int(np.nanargmax(vec)) if finite_n else None
        repair[g] = {
            "r": None if r is None else round(r, 4),
            "n_finite": finite_n,
            "peak_in_window": gp in window if gp is not None else None,
        }
    # all-protein correlations for the null, only if this experiment is a candidate
    corrs = {}
    finite_counts = {}
    if early and both:
        for g in table.index:
            vec = table.loc[g].values.astype(float)
            r = profile_r(mvp, vec)
            if r is None:
                continue
            corrs[g] = r
            finite_counts[g] = int(np.isfinite(vec).sum())
    proteasome = []
    if "PSMA1" in table.index:
        a = table.loc["PSMA1"].values.astype(float)
        for g in PROT:
            if g in table.index:
                r = profile_r(a, table.loc[g].values.astype(float))
                if r is not None:
                    proteasome.append(r)
    return {
        "n_fractions": n,
        "mvp_peak_1based": peak + 1,
        "early": bool(early),
        "both_partners": bool(both),
        "partners": partners,
        "repair": repair,
        "corrs": corrs,
        "finite_counts": finite_counts,
        "proteasome_mean_r": None if not proteasome else round(float(np.mean(proteasome)), 4),
    }


def main():
    # One sample directory is one experiment. The archive stores iBAQ, MS1,
    # LFQ and spectral counts side by side; the registration takes the first
    # of iBAQ, MS1/intensity, spectral counts. Method comes from the path,
    # because the file named metadata.tsv.gz is a MaxQuant protein table and
    # not a method record. That was checked from filenames and a header, not
    # from any vault elution profile.
    dirs = {}
    for p in DATA.rglob("*"):
        if not p.is_file():
            continue
        if quant_key(p) >= 9:
            continue
        dirs.setdefault(p.parent, []).append(p)
    experiments = []
    skipped = {"no_matrix": 0, "no_mvp": 0, "not_sec": 0}
    method_census = {}
    for directory, paths in sorted(dirs.items(), key=lambda kv: str(kv[0])):
        label = method_of(directory, "")
        method_census[label] = method_census.get(label, 0) + 1
        if label != "SEC":
            skipped["not_sec"] += 1
            continue
        chosen = None
        table = None
        for p in sorted(paths, key=quant_key):
            table = read_gene_table(p)
            if table is not None:
                chosen = p
                break
        if chosen is None:
            skipped["no_matrix"] += 1
            continue
        info = analyse_experiment(table)
        if info is None:
            skipped["no_mvp"] += 1
            continue
        info["path"] = str(chosen.relative_to(DATA))
        info["method"] = label
        info["quant_file"] = chosen.name
        experiments.append(info)
        print(f"{info['method']:10} early={info['early']} both={info['both_partners']} peak={info['mvp_peak_1based']}/{info['n_fractions']} {info['path']}", flush=True)

    sec_early = [e for e in experiments if e["method"] == "SEC" and e["early"]]
    analysis = [e for e in sec_early if e["both_partners"]]
    gate = len(analysis) >= 1

    # mean r per gene across analysis experiments
    def mean_r(gene, exps):
        rs, ns = [], []
        for e in exps:
            rec = e["corrs"].get(gene)
            if rec is None:
                continue
            rs.append(rec)
            ns.append(e["finite_counts"].get(gene, 0))
        if not rs:
            return None
        return float(np.mean(rs)), int(np.median(ns)), len(rs)

    repair_stats = {}
    for g in REPAIR:
        repair_stats[g] = mean_r(g, analysis)
    quantified = {g: v for g, v in repair_stats.items() if v is not None}
    observed = float(np.mean([v[0] for v in quantified.values()])) if quantified else None

    # null pool from the union of correlations. A protein's mean r and its median finite count.
    pool = {}
    for e in analysis:
        for g, r in e["corrs"].items():
            if g in REPAIR or g in ("MVP", "PARP4", "TEP1"):
                continue
            pool.setdefault(g, {"rs": [], "ns": []})
            pool[g]["rs"].append(r)
            pool[g]["ns"].append(e["finite_counts"].get(g, 0))
    pool_rows = []
    for g, d in pool.items():
        pool_rows.append((g, float(np.mean(d["rs"])), int(np.median(d["ns"])), len(d["rs"])))

    rng = np.random.default_rng(0)
    null_means = []
    if gate and len(quantified) >= 5 and pool_rows:
        for _ in range(1000):
            draw = []
            for g, (r, nmed, nexp) in quantified.items():
                cands = [
                    row for row in pool_rows
                    if abs(row[3] - nexp) <= 1 and (nmed == 0 or abs(row[2] - nmed) / nmed <= 0.25)
                ]
                if not cands:
                    cands = pool_rows
                pick = cands[int(rng.integers(0, len(cands)))]
                draw.append(pick[1])
            null_means.append(float(np.mean(draw)))
        p = (1 + sum(1 for m in null_means if m >= observed)) / 1001
    else:
        p = None

    if not gate:
        verdict = "UNINFORMATIVE (vault core not visible in an early SEC fraction)"
    elif len(quantified) < 5:
        verdict = "UNINFORMATIVE (fewer than 5 repair genes quantified)"
    elif p is not None and p < 0.05:
        verdict = "PHYSICAL CO-ELUTION SURVIVES"
    elif p is not None:
        verdict = "KILL: repair set does not co-elute with the vault above the null"
    else:
        verdict = "UNINFORMATIVE (null could not be built)"

    # window occupancy, secondary
    window_hits = {}
    for g in REPAIR:
        flags = []
        for e in analysis:
            rec = e["repair"].get(g)
            if rec and rec["peak_in_window"] is not None:
                flags.append(bool(rec["peak_in_window"]))
        window_hits[g] = None if not flags else round(sum(flags) / len(flags), 3)

    proteasome_rs = [e["proteasome_mean_r"] for e in analysis if e["proteasome_mean_r"] is not None]
    summary = {
        "n_sample_directories": len(dirs),
        "n_sec_with_mvp": len(experiments),
        "skipped": skipped,
        "method_counts": method_census,
        "n_sec_early": len(sec_early),
        "n_gate_experiments": len(analysis),
        "gate_pass": gate,
        "repair_mean_r": {g: (None if v is None else round(v[0], 4)) for g, v in repair_stats.items()},
        "repair_n_experiments": {g: (None if v is None else v[2]) for g, v in repair_stats.items()},
        "observed_mean_r": None if observed is None else round(observed, 4),
        "null_p": None if p is None else round(p, 4),
        "null_mean_of_means": None if not null_means else round(float(np.mean(null_means)), 4),
        "peak_in_window_rate": window_hits,
        "proteasome_diagnostic_mean_r": None if not proteasome_rs else round(float(np.mean(proteasome_rs)), 4),
        "verdict": verdict,
        "gate_experiments": [
            {"path": e["path"], "peak": e["mvp_peak_1based"], "n": e["n_fractions"], "partners": e["partners"]}
            for e in analysis
        ],
    }
    # drop corrs before writing the per-experiment log
    slim = []
    for e in experiments:
        slim.append({k: v for k, v in e.items() if k not in {"corrs", "finite_counts"}})
    dest = ROOT / "results" / "cofraction.json"
    json.dump({"summary": summary, "experiments": slim}, open(dest, "w"), indent=1)
    print("VERDICT:", verdict, flush=True)
    print(f"wrote {dest}", flush=True)


if __name__ == "__main__":
    main()
