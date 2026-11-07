"""Popperian Confounder & Precision Gate Checks for Test A4A & Test A4B:
1. 1-Methylnicotinamide (1-MNA) Confounder Audit:
   - Test whether MVP/PARP4/TEP1 correlation with 1-methylnicotinamide (r=+0.407, #1 of 225 metabolites)
     survives controlling for NNMT protein, NNMT mRNA, NAMPT/CD38, and tissue lineage across CCLE (n=370),
     OR whether NNMT co-expression explains the signal!
   - Also check MVP-NNMT protein co-abundance across all 11 CPTAC + CCLE cohorts on disk.
2. Genome-wide Top-100 Rank & Continuous Linear-CNA Dissection of 16p11.2 (PYCARD, MAPK3, ALDOA, SULT1A3)
   vs Vault Core (PARP4, TEP1), Inflammasome (CASP1, CASP4 on chr11), and Membrane-Repair Module (ANXA2, S100A10, CAPN2, EHD2/4, ACTR3).
"""
import glob, json, os
import numpy as np
import pandas as pd
import requests
from scipy import stats

RAW = "~/projects/Vault/argon/raw"
OUT = "~/projects/Vault/argon/results"

ccle_prot = pd.read_parquet("~/projects/Vault/data/processed/prot/ccle_broad_2019.parquet")
met = pd.read_csv(f"{RAW}/CCLE_metabolomics_20190502.csv").set_index("CCLE_ID")
met_num = met.select_dtypes(include=[np.number])
shared_m = ccle_prot.columns.intersection(met_num.index)

print("=== 1. POPPERIAN CONFOUNDER CHECK ON 1-METHYLNICOTINAMIDE (CCLE n=370) ===")
nad_enzymes = ["MVP", "PARP4", "TEP1", "NNMT", "NAMPT", "NMRK1", "NAPRT", "CD38", "BST1", "PARP1", "PARP9", "PARP14", "SARM1", "AOX1"]
present_enz = [g for g in nad_enzymes if g in ccle_prot.index]
print("Present NAD/nicotinamide enzymes in CCLE proteomics:", present_enz)

mna = met_num.loc[shared_m, "1-methylnicotinamide"]
nam = met_num.loc[shared_m, "niacinamide"]
nad = met_num.loc[shared_m, "NAD"]
ratio_mna_nam = mna - nam  # CCLE metabolomics values are log10-normalized and median-centered! Verify scale first:
print(f"1-MNA range: [{mna.min():.2f}, {mna.max():.2f}] (std={mna.std():.2f}), niacinamide range: [{nam.min():.2f}, {nam.max():.2f}]")

for g in present_enz:
    v = ccle_prot.loc[g, shared_m]
    ok = v.notna() & mna.notna()
    if ok.sum() >= 50:
        r_mna, p_mna = stats.pearsonr(v[ok], mna[ok])
        ok_mvp = v.notna() & ccle_prot.loc["MVP", shared_m].notna()
        r_mvp = float(v[ok_mvp].corr(ccle_prot.loc["MVP", shared_m][ok_mvp]))
        print(f"  {g:8s} (n={ok.sum():3d}): r(1-MNA)={r_mna:+.3f} (p={p_mna:.2e}) | r(MVP_prot)={r_mvp:+.3f}")

# Fetch NNMT mRNA from cBioPortal too (in case NNMT protein has missing values in TMT plexes!)
S = requests.Session()
S.headers["Content-Type"] = "application/json"
samples = [s["sampleId"] for s in S.get("https://www.cbioportal.org/api/studies/ccle_broad_2019/samples?pageSize=100000", timeout=30).json()]
# NNMT entrez = 4837, NAMPT = 10135, CD38 = 952, MVP = 9961
mrna_raw = S.post("https://www.cbioportal.org/api/molecular-profiles/ccle_broad_2019_rna_seq_mrna/molecular-data/fetch?projection=SUMMARY",
                  json={"entrezGeneIds": [4837, 10135, 952, 9961], "sampleIds": samples}, timeout=30).json()
id2sym = {4837: "NNMT", 10135: "NAMPT", 952: "CD38", 9961: "MVP"}
df_nad_rna = pd.DataFrame([(id2sym[r["entrezGeneId"]], r["sampleId"], np.log2(float(r["value"]) + 1.0)) for r in mrna_raw],
                          columns=["g", "s", "v"]).pivot(index="g", columns="s", values="v")

# Extract tissue lineage from CCLE_ID suffix (e.g., 22RV1_PROSTATE -> PROSTATE)
lineages = pd.Series([s.split("_", 1)[1] if "_" in s else "OTHER" for s in shared_m], index=shared_m)

df_audit = pd.DataFrame({
    "mna": mna,
    "nam": nam,
    "nad": nad,
    "mvp_prot": ccle_prot.loc["MVP", shared_m],
    "parp4_prot": ccle_prot.loc["PARP4", shared_m],
    "tep1_prot": ccle_prot.loc["TEP1", shared_m],
    "nnmt_prot": ccle_prot.loc["NNMT", shared_m] if "NNMT" in ccle_prot.index else np.nan,
    "nnmt_rna": df_nad_rna.loc["NNMT"].reindex(shared_m),
    "nampt_rna": df_nad_rna.loc["NAMPT"].reindex(shared_m),
    "cd38_rna": df_nad_rna.loc["CD38"].reindex(shared_m),
    "lineage": lineages,
})

def partial_corr(df, x, y, covars):
    sub = df[[x, y] + covars].dropna()
    X = np.column_stack([np.ones(len(sub))] + [sub[c].values for c in covars])
    rx = sub[x].values - X @ np.linalg.lstsq(X, sub[x].values, rcond=None)[0]
    ry = sub[y].values - X @ np.linalg.lstsq(X, sub[y].values, rcond=None)[0]
    r, p = stats.pearsonr(rx, ry)
    return len(sub), float(r), float(p)

print("\nPartial correlation dissection of 1-methylnicotinamide (mna) ~ MVP_prot:")
for desc, covs in [
    ("Raw (no covariates)", []),
    ("Controlling for NNMT_rna", ["nnmt_rna"]),
    ("Controlling for NNMT_prot", ["nnmt_prot"]),
    ("Controlling for NNMT_prot + NNMT_rna + NAMPT_rna + CD38_rna", ["nnmt_prot", "nnmt_rna", "nampt_rna", "cd38_rna"]),
]:
    if not covs:
        sub = df_audit[["mna", "mvp_prot"]].dropna()
        r, p = stats.pearsonr(sub["mna"], sub["mvp_prot"])
        n = len(sub)
    else:
        n, r, p = partial_corr(df_audit, "mna", "mvp_prot", covs)
    print(f"  {desc:60s}: n={n:3d} | r={r:+.4f} (p={p:.3e})")

# Also control for tissue lineage fixed effects (one-hot lineages with >=5 lines) + NNMT!
sub_lin = df_audit[["mna", "mvp_prot", "nnmt_rna", "lineage"]].dropna()
lin_dummies = pd.get_dummies(sub_lin["lineage"], drop_first=True, dtype=float)
X_lin_only = np.column_stack([np.ones(len(sub_lin)), lin_dummies.values])
rx_l = sub_lin["mna"].values - X_lin_only @ np.linalg.lstsq(X_lin_only, sub_lin["mna"].values, rcond=None)[0]
ry_l = sub_lin["mvp_prot"].values - X_lin_only @ np.linalg.lstsq(X_lin_only, sub_lin["mvp_prot"].values, rcond=None)[0]
r_lin, p_lin = stats.pearsonr(rx_l, ry_l)

X_lin_nnmt = np.column_stack([np.ones(len(sub_lin)), sub_lin["nnmt_rna"].values, lin_dummies.values])
rx_ln = sub_lin["mna"].values - X_lin_nnmt @ np.linalg.lstsq(X_lin_nnmt, sub_lin["mna"].values, rcond=None)[0]
ry_ln = sub_lin["mvp_prot"].values - X_lin_nnmt @ np.linalg.lstsq(X_lin_nnmt, sub_lin["mvp_prot"].values, rcond=None)[0]
r_lin_nnmt, p_lin_nnmt = stats.pearsonr(rx_ln, ry_ln)
print(f"  {'Controlling for Tissue Lineage fixed effects (24 lineages)':60s}: n={len(sub_lin):3d} | r={r_lin:+.4f} (p={p_lin:.3e})")
print(f"  {'Controlling for Tissue Lineage + NNMT_rna':60s}: n={len(sub_lin):3d} | r={r_lin_nnmt:+.4f} (p={p_lin_nnmt:.3e})")

# Check MVP vs NNMT protein correlation across all 11 cohorts in data/processed/prot/!
prot_files = sorted(glob.glob("~/projects/Vault/data/processed/prot/*.parquet"))
nnmt_corrs = {}
for pf in prot_files:
    st = os.path.basename(pf).replace(".parquet", "")
    pr = pd.read_parquet(pf)
    if "MVP" in pr.index and "NNMT" in pr.index:
        ok = pr.loc["MVP"].notna() & pr.loc["NNMT"].notna()
        if ok.sum() >= 30:
            nnmt_corrs[st] = float(pr.loc["MVP", ok].corr(pr.loc["NNMT", ok]))
print("\nMVP vs NNMT protein correlation across all 11 proteomics cohorts:", {k: round(v, 3) for k, v in nnmt_corrs.items()}, "mean=", round(np.mean(list(nnmt_corrs.values())), 3))

# ==============================================================================
# 2. GENOME-WIDE RANK & CONTINUOUS LINEAR-CNA DISSECTION OF 16p11.2 IN CPTAC + CCLE
# ==============================================================================
print("\n=== 2. GENOME-WIDE TOP-100 RANK & CONTINUOUS LINEAR CNA CHECK (16p11.2 vs OFF-CHR16) ===")
# Check which molecular profiles exist for CPTAC studies on cBioPortal!
cptac_names = [os.path.basename(pf).replace(".parquet", "") for pf in prot_files if "ccle" not in pf]
print("Local proteomics cohorts:", cptac_names)

# Compute genome-wide correlation of MVP with ALL proteins across:
# (a) Raw CPTAC cohorts with CNA, (b) MVP-CNA-residualized CPTAC cohorts, (c) Euploid (MVP GISTIC==0) samples!
cna_studies = {}
for st in ["luad_cptac_2020", "brca_cptac_2020", "ucec_cptac_2020", "coad_cptac_2019"]:
    p = f"{RAW}/{st}_data_cna.txt"
    if os.path.exists(p):
        df = pd.read_csv(p, sep="\t", low_memory=False)
        gcol = "Hugo_Symbol" if "Hugo_Symbol" in df.columns else df.columns[0]
        df = df.dropna(subset=[gcol]).set_index(gcol).drop(columns=[c for c in ["Hugo_Symbol", "Entrez_Gene_Id", "Cytoband"] if c in df.columns and c != gcol], errors="ignore")
        df = df.apply(pd.to_numeric, errors="coerce")
        cna_studies[st] = df[~df.index.duplicated(keep="first")]

# Also check if cBioPortal API has continuous linear_CNA molecular profiles for these CPTAC cohorts!
lin_cna_studies = {}
for st in cptac_names:
    try:
        profs = S.get(f"https://www.cbioportal.org/api/studies/{st}/molecular-profiles", timeout=10).json()
        lin_ids = [p["molecularProfileId"] for p in profs if "linear" in p["molecularProfileId"].lower() or p.get("datatype") == "CONTINUOUS" and "cna" in p["molecularProfileId"].lower()]
        if lin_ids:
            print(f"  Found continuous CNA profile on cBioPortal for {st}: {lin_ids[0]}")
            samps = [s["sampleId"] for s in S.get(f"https://www.cbioportal.org/api/studies/{st}/samples?pageSize=10000", timeout=15).json()]
            # Fetch MVP (9961) continuous CNA across all samples in this cohort!
            d = S.post(f"https://www.cbioportal.org/api/molecular-profiles/{lin_ids[0]}/molecular-data/fetch?projection=SUMMARY",
                       json={"entrezGeneIds": [9961], "sampleIds": samps}, timeout=20).json()
            if d:
                lin_cna_studies[st] = pd.Series({r["sampleId"]: float(r["value"]) for r in d})
    except Exception:
        pass

print(f"Fetched continuous MVP linear-CNA for {len(lin_cna_studies)} CPTAC cohorts: {list(lin_cna_studies.keys())}")

# Across ALL cohorts that have continuous MVP linear-CNA (or discrete CNA if not), compute genome-wide correlation with MVP before vs after regressing out MVP CNA from EVERY protein!
all_cna_vecs = dict(lin_cna_studies)
for st, cdf in cna_studies.items():
    if st not in all_cna_vecs and "MVP" in cdf.index:
        all_cna_vecs[st] = cdf.loc["MVP"]

raw_mat = {}
adj_mat = {}
eup_mat = {}
for st, mvp_cna_s in all_cna_vecs.items():
    pr_path = f"~/projects/Vault/data/processed/prot/{st}.parquet"
    if not os.path.exists(pr_path): continue
    pr = pd.read_parquet(pr_path)
    sh = pr.columns.intersection(mvp_cna_s.dropna().index)
    if len(sh) < 45 or "MVP" not in pr.index: continue
    mp = pr.loc["MVP", sh]
    mc = mvp_cna_s.loc[sh]
    ok_m = mp.notna() & mc.notna()
    sh = sh[ok_m]
    mp = mp.loc[sh].values
    mc = mc.loc[sh].values
    # Residualize EVERY protein row (with >=40 non-null) against MVP copy number mc!
    X = np.column_stack([np.ones(len(sh)), mc])
    mp_res = mp - X @ np.linalg.lstsq(X, mp, rcond=None)[0]
    r_raw_s = {}
    r_adj_s = {}
    for g, row in pr[sh].iterrows():
        v = row.values
        m = ~np.isnan(v)
        if m.sum() < 40: continue
        r_raw_s[g] = float(np.corrcoef(mp[m], v[m])[0, 1])
        Xm = X[m]
        vres = v[m] - Xm @ np.linalg.lstsq(Xm, v[m], rcond=None)[0]
        mres = mp[m] - Xm @ np.linalg.lstsq(Xm, mp[m], rcond=None)[0]
        r_adj_s[g] = float(np.corrcoef(mres, vres)[0, 1])
    raw_mat[st] = pd.Series(r_raw_s)
    adj_mat[st] = pd.Series(r_adj_s)

df_raw_gw = pd.DataFrame(raw_mat)
df_adj_gw = pd.DataFrame(adj_mat)
keep_g = df_raw_gw.notna().sum(axis=1) >= max(3, len(raw_mat) // 2)
mean_raw = df_raw_gw.loc[keep_g].mean(axis=1).sort_values(ascending=False)
mean_adj = df_adj_gw.loc[keep_g].mean(axis=1).sort_values(ascending=False)

rank_raw = mean_raw.rank(ascending=False, method="min").astype(int)
rank_adj = mean_adj.rank(ascending=False, method="min").astype(int)

watch = ["MVP", "PARP4", "TEP1", "PYCARD", "MAPK3", "ALDOA", "SULT1A3", "CORO1A", "PRKCB",
         "CASP1", "CASP4", "ANXA2", "S100A10", "CAPN2", "CAPNS1", "EHD2", "EHD4", "IQGAP1", "ACTR3", "ARPC2"]
print(f"\nGenome-wide Rank across {len(raw_mat)} CNA-matched CPTAC cohorts (n_genes={keep_g.sum()}):")
rank_rows = []
for g in watch:
    if g in mean_raw.index and g != "MVP":
        rr, ra = float(mean_raw[g]), float(mean_adj[g])
        kr, ka = int(rank_raw[g]), int(rank_adj[g])
        loc = "16p11.2" if g in {"PYCARD", "MAPK3", "ALDOA", "SULT1A3", "CORO1A", "PRKCB"} else ("chr11" if g in {"CASP1", "CASP4"} else "off-16p")
        print(f"  {g:10s} [{loc:7s}]: r_raw={rr:+.3f} (Rank #{kr:4d}) -> r_CNA_adj={ra:+.3f} (Rank #{ka:4d}) | delta_rank={ka-kr:+d}")
        rank_rows.append({"gene": g, "locus": loc, "r_raw": rr, "rank_raw": kr, "r_cna_adj": ra, "rank_cna_adj": ka, "delta_rank": ka - kr})

print("\nTop 20 genome-wide MVP protein partners AFTER continuous/GISTIC MVP-CNA regression:")
for i, (g, val) in enumerate(mean_adj.drop("MVP", errors="ignore").head(20).items(), 1):
    print(f"  #{i:2d}: {g:12s} r_CNA_adj={val:+.3f} (was r_raw={mean_raw[g]:+.3f}, Rank #{rank_raw[g]})")

json.dump({
    "mna_nnmt_confounder_audit": {
        "r_mna_mvp_raw": float(df_audit[["mna", "mvp_prot"]].dropna().corr().iloc[0, 1]),
        "r_mna_nnmt_prot": float(df_audit[["mna", "nnmt_prot"]].dropna().corr().iloc[0, 1]) if df_audit["nnmt_prot"].notna().sum() > 20 else None,
        "r_mna_nnmt_rna": float(df_audit[["mna", "nnmt_rna"]].dropna().corr().iloc[0, 1]),
        "r_mvp_nnmt_prot_ccle": float(df_audit[["mvp_prot", "nnmt_prot"]].dropna().corr().iloc[0, 1]) if df_audit["nnmt_prot"].notna().sum() > 20 else None,
        "partial_r_mna_mvp_given_nnmt_rna": partial_corr(df_audit, "mna", "mvp_prot", ["nnmt_rna"])[1],
        "partial_p_mna_mvp_given_nnmt_rna": partial_corr(df_audit, "mna", "mvp_prot", ["nnmt_rna"])[2],
        "partial_r_mna_mvp_given_nnmt_prot": partial_corr(df_audit, "mna", "mvp_prot", ["nnmt_prot"])[1],
        "partial_p_mna_mvp_given_nnmt_prot": partial_corr(df_audit, "mna", "mvp_prot", ["nnmt_prot"])[2],
        "partial_r_mna_mvp_given_lineage": float(r_lin),
        "partial_r_mna_mvp_given_lineage_and_nnmt": float(r_lin_nnmt),
        "partial_p_mna_mvp_given_lineage_and_nnmt": float(p_lin_nnmt),
        "mvp_nnmt_prot_across_11_cohorts": nnmt_corrs,
    },
    "cptac_cna_genomewide_ranks": {
        "cohorts_used": list(raw_mat.keys()),
        "n_genes_scored": int(keep_g.sum()),
        "watch_genes": rank_rows,
        "top20_after_cna_adj": [{"rank": i, "gene": g, "r_cna_adj": float(v), "r_raw": float(mean_raw[g])}
                                for i, (g, v) in enumerate(mean_adj.drop("MVP", errors="ignore").head(20).items(), 1)],
    },
}, open(f"{OUT}/confounder_checks.json", "w"), indent=2)
