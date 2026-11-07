"""Fast empirical audit checks for Claude Back-Channel 004 (ss13-22).
Strictly read-only outside argon/; writes summary JSON inside argon/results/audit_004_checks.json.
"""
import json, re, gzip
import numpy as np
import pandas as pd
import openpyxl
import statsmodels.api as sm
from scipy.stats import spearmanr, hypergeom

ROOT = "~/projects/Vault"
out = {}

# ==============================================================================
# CHECK 1: s17 LRP Dissection & Mediation (Unmatched-N bias, Docetaxel dup, GDSC1/2)
# ==============================================================================
print("=== CHECK 1: s17 LRP Dissection & Mediation ===")
G_list = []
for f in ["GDSC1", "GDSC2"]:
    d = pd.read_excel(f"{ROOT}/data/raw/gdsc/{f}_fitted_dose_response_27Oct23.xlsx")
    d["src"] = f
    G_list.append(d)
G = pd.concat(G_list, ignore_index=True)
G["cl"] = G.CELL_LINE_NAME.astype(str).str.upper().str.replace(r"[^A-Z0-9]", "", regex=True)
M = pd.read_parquet(f"{ROOT}/data/processed/prot/ccle_broad_2019.parquet")
clin = pd.read_parquet(f"{ROOT}/data/processed/prot/ccle_broad_2019.clin.parquet").set_index("sampleId")
key = lambda c: re.sub(r"[^A-Z0-9]", "", c.split("_")[0].upper())
M.columns = [key(c) for c in M.columns]
M = M.loc[:, ~M.columns.duplicated()]
shared = sorted(set(M.columns) & set(G.cl))
P = M[shared]
dt = pd.to_numeric(clin.DOUBLING_TIME, errors="coerce")
dt.index = [key(i) for i in clin.index]
dt = dt[~dt.index.duplicated()].reindex(shared)
prolif = P.reindex(["MKI67", "TOP2A", "MCM2"]).apply(lambda r: (r - r.mean()) / r.std(), axis=1).mean()
auc = G[G.cl.isin(shared)].pivot_table(index="DRUG_NAME", columns="cl", values="AUC", aggfunc="mean")

print(f"Matched lines: {len(shared)} | non-null MVP={int(P.loc['MVP'].notna().sum())}, ABCB1={int(P.loc['ABCB1'].notna().sum())}, ABCC1={int(P.loc['ABCC1'].notna().sum())}, dt={int(dt.notna().sum())}, prolif={int(prolif.notna().sum())}")

Z = lambda s: (s - np.nanmean(s)) / np.nanstd(s)
DRUGS = ["Vinorelbine", "Vinblastine", "Paclitaxel", "Docetaxel", "Methotrexate", "Etoposide", "Epirubicin"]
med_rows = []
for d in DRUGS:
    y = auc.loc[d]
    # Exact sample sizes in Claude's unmatched fits:
    df_all = pd.DataFrame({"y": y, "MVP": P.loc["MVP"], "ABCB1": P.loc["ABCB1"], "dt": dt, "prolif": prolif})
    n0 = int(df_all[["y", "MVP"]].dropna().shape[0])
    n1 = int(df_all[["y", "MVP", "ABCB1"]].dropna().shape[0])
    n2 = int(df_all[["y", "MVP", "dt", "prolif"]].dropna().shape[0])
    n3 = int(df_all.dropna().shape[0])

    # Common complete-case sample (exact same n3 lines for all 4 models!)
    dfc = df_all.dropna().copy()
    dfc_z = dfc.apply(Z)
    b0_c = float(sm.OLS(dfc_z["y"], sm.add_constant(dfc_z[["MVP"]])).fit().params["MVP"])
    b1_c = float(sm.OLS(dfc_z["y"], sm.add_constant(dfc_z[["MVP", "ABCB1"]])).fit().params["MVP"])
    b2_c = float(sm.OLS(dfc_z["y"], sm.add_constant(dfc_z[["MVP", "dt", "prolif"]])).fit().params["MVP"])
    f3_c = sm.OLS(dfc_z["y"], sm.add_constant(dfc_z[["MVP", "ABCB1", "dt", "prolif"]])).fit()
    b3_c, p3_c = float(f3_c.params["MVP"]), float(f3_c.pvalues["MVP"])

    # Also larger sample without dt (using prolif protein on ABCB1-non-null sample n1!)
    df_p1 = df_all[["y", "MVP", "ABCB1", "prolif"]].dropna().apply(Z)
    b0_p1 = float(sm.OLS(df_p1["y"], sm.add_constant(df_p1[["MVP"]])).fit().params["MVP"])
    b_abcb1_p1 = float(sm.OLS(df_p1["y"], sm.add_constant(df_p1[["MVP", "ABCB1"]])).fit().params["MVP"])
    b_prol_p1 = float(sm.OLS(df_p1["y"], sm.add_constant(df_p1[["MVP", "prolif"]])).fit().params["MVP"])

    # Also check beta_alone on dt-available sample (n2) vs dt-missing sample!
    df_n2 = df_all[["y", "MVP", "dt", "prolif"]].dropna().apply(Z)
    b0_n2 = float(sm.OLS(df_n2["y"], sm.add_constant(df_n2[["MVP"]])).fit().params["MVP"])
    b2_n2 = float(sm.OLS(df_n2["y"], sm.add_constant(df_n2[["MVP", "dt", "prolif"]])).fit().params["MVP"])

    med_rows.append({
        "drug": d, "n0": n0, "n1_abcb1": n1, "n2_dt": n2, "n3_common": n3,
        "b0_common": round(b0_c, 3),
        "pct_abcb1_common": round(100 * (1 - b1_c / b0_c), 1),
        "pct_prolif_dt_common": round(100 * (1 - b2_c / b0_c), 1),
        "b0_on_n2": round(b0_n2, 3),
        "pct_prolif_dt_matched_n2": round(100 * (1 - b2_n2 / b0_n2), 1),
        "pct_abcb1_on_n1": round(100 * (1 - b_abcb1_p1 / b0_p1), 1),
        "pct_prolifProt_only_on_n1": round(100 * (1 - b_prol_p1 / b0_p1), 1),
        "p3_common": round(p3_c, 4),
    })
df_med = pd.DataFrame(med_rows)
print(df_med.to_string(index=False))
print(f"COMMON-SAMPLE (n~{df_med['n3_common'].median():.0f}) medians: ABCB1 absorbs {df_med['pct_abcb1_common'].median():.1f}% | dt+prolif absorbs {df_med['pct_prolif_dt_common'].median():.1f}%")
print(f"MATCHED-N2 (n~{df_med['n2_dt'].median():.0f}) median: dt+prolif absorbs {df_med['pct_prolif_dt_matched_n2'].median():.1f}%")
print(f"MATCHED-N1 (n~{df_med['n1_abcb1'].median():.0f}, no dt drop): ABCB1 absorbs {df_med['pct_abcb1_on_n1'].median():.1f}% | prolif_protein alone absorbs {df_med['pct_prolifProt_only_on_n1'].median():.1f}%")
out["s17_mediation_recheck"] = df_med.to_dict(orient="records")

# Deduplicated 18 unique drugs BH-FDR check
lrp_j = json.load(open(f"{ROOT}/results/lrp.json"))
df_lrp = pd.DataFrame(lrp_j["results"]).drop_duplicates("drug").sort_values("p").reset_index(drop=True)
df_lrp["q_dedup"] = (df_lrp["p"] * len(df_lrp) / np.arange(1, len(df_lrp) + 1)).iloc[::-1].cummin().iloc[::-1].clip(upper=1.0)
print(f"Deduplicated LRP drugs: {len(df_lrp)} unique drugs, q<0.05 count = {int((df_lrp['q_dedup'] < 0.05).sum())} (was reported 8/19 due to duplicate Docetaxel)")
out["s17_dedup_n_drugs"] = int(len(df_lrp))
out["s17_dedup_n_sig"] = int((df_lrp["q_dedup"] < 0.05).sum())

# ==============================================================================
# CHECK 2: s19 Pulse-SILAC Turnover (Cell types, Abundance bias, Abundance-matched triplets)
# ==============================================================================
print("\n=== CHECK 2: s19 Mathieson 2018 Pulse-SILAC Turnover ===")
wb_t = openpyxl.load_workbook(f"{ROOT}/data/raw/turnover/41467_2018_3106_MOESM5_ESM.xlsx", read_only=True, data_only=True)
print("MOESM5 sheets:", wb_t.sheetnames)
rows_t = list(wb_t[wb_t.sheetnames[0]].iter_rows(values_only=True))
print("Header row 0:", rows_t[0][:25])
print("Header row 1:", rows_t[1][:25])
wb_t4 = openpyxl.load_workbook(f"{ROOT}/data/raw/turnover/41467_2018_3106_MOESM4_ESM.xlsx", read_only=True, data_only=True)
print("MOESM4 sheets:", wb_t4.sheetnames)
for sname in wb_t4.sheetnames:
    r4 = list(wb_t4[sname].iter_rows(values_only=True))[:4]
    print(f"  MOESM4[{sname}] rows 0..2:", [x[:12] for x in r4[:3]])

# ==============================================================================
# CHECK 3: s14 CNA-adjusted SULT1A3 & PYCARD check
# ==============================================================================
print("\n=== CHECK 3: s14 CNA-adjusted SULT1A3 & PYCARD ===")
import glob
cna_files = sorted(glob.glob(f"{ROOT}/data/processed/cna/*.parquet"))
sult_pres, pyc_pres, mvp_pres = [], [], []
for cf in cna_files:
    st = cf.split("/")[-1].replace(".parquet", "")
    A = pd.read_parquet(cf)
    sult_in = "SULT1A3" in A.index
    pyc_in = "PYCARD" in A.index
    sult_std = float(A.loc["SULT1A3"].std()) if sult_in and isinstance(A.loc["SULT1A3"], pd.Series) else (float(A.loc["SULT1A3"].iloc[0].std()) if sult_in else np.nan)
    sult_rows = int((A.index == "SULT1A3").sum())
    sult_pres.append((st, sult_in, sult_rows, round(sult_std, 4) if np.isfinite(sult_std) else None))
    pyc_pres.append((st, pyc_in))
print("SULT1A3 in CNA parquets (cohort, in_index, n_rows, std):", sult_pres)
print("PYCARD in CNA parquets:", pyc_pres)

# ==============================================================================
# CHECK 4: s15 Cross-species eggNOG orthology & min-q winner's curse
# ==============================================================================
print("\n=== CHECK 4: s15 Cross-species eggNOG orthology ===")
wb_d = openpyxl.load_workbook(f"{ROOT}/argon/raw/natcomms_source_data/Source_data_Vault.xlsx", read_only=True, data_only=True)
rows_d = list(wb_d["Fig. 5D"].iter_rows(values_only=True))
cols_d = list(rows_d[0])
Dd = pd.DataFrame(rows_d[1:], columns=cols_d)
fc_c = [c for c in cols_d if str(c).startswith("foldchange.log2")][0]
qv_c = [c for c in cols_d if str(c).startswith("qvalue")][0]
Dd["fc"] = pd.to_numeric(Dd[fc_c], errors="coerce")
Dd["q"] = pd.to_numeric(Dd[qv_c], errors="coerce")
Dd["acc"] = Dd.accessions.astype(str).str.split(";").str[0]

xr = pd.read_csv(f"{ROOT}/data/raw/ortho/dicty_eggnog.tsv", sep="\t").dropna(subset=["eggNOG"])
acc2og = {a: [x for x in str(e).split(";") if x] for a, e in zip(xr.Entry, xr.eggNOG)}
hum = json.load(open(f"{ROOT}/data/processed/eggnog_human.json"))
sym = {}
for l in gzip.open(f"{ROOT}/data/raw/eggnog/gencode.v25.pc_translations.fa.gz", "rt"):
    if l[0] == ">":
        p = l[1:].split("|")
        sym[p[0].split(".")[0]] = p[6]
og2sym = {og: sorted({sym[x] for x in ps if x in sym}) for og, ps in hum.items()}

rows2 = []
for _, r in Dd.iterrows():
    for og in acc2og.get(r.acc, []):
        for h in og2sym.get(og, []):
            rows2.append((h, r.acc, str(r.get("gene_names", r.get("description", ""))), og, r.fc, r.q))
O = pd.DataFrame(rows2, columns=["sym", "dicty_acc", "desc", "og", "fc", "q"])
print("ACTR3 candidate rows in O before drop_duplicates:")
print(O[O.sym == "ACTR3"].sort_values("q").head(10).to_string(index=False))

# Check how many distinct Dicty accessions generated the 32 top-100 overlaps!
O_dedup = O.sort_values("q").drop_duplicates("sym").set_index("sym")
po_cna = pd.read_parquet(f"{ROOT}/data/processed/mvp_coabundance_cna.parquet")
uni = [g for g in po_cna.index if g in O_dedup.index]
top100 = [g for g in po_cna.index if g in set(uni)][:100]
prox_dedup = O_dedup[(O_dedup.fc > 0) & (O_dedup.q < 0.05)]
hits32 = O_dedup.loc[[g for g in top100 if g in prox_dedup.index]]
print(f"Claude's 32/100 proximal human symbols come from ONLY {hits32['dicty_acc'].nunique()} distinct Dicty proteins!")
print("Dicty accessions cloned into multiple top-100 human hits:")
print(hits32.groupby("dicty_acc").apply(lambda g: list(g.index)).to_string())

# Also compute unbiased median-fc / median-p per human symbol (no min-q winner's curse!):
prox_rate_raw_dicty = float(((Dd["fc"] > 0) & (Dd["q"] < 0.05)).mean())
prox_rate_claude_hum = float(((O_dedup["fc"] > 0) & (O_dedup["q"] < 0.05)).mean())
print(f"Proximal base rate: raw Dicty proteins = {100*prox_rate_raw_dicty:.1f}% vs Claude's min-q human-projected = {100*prox_rate_claude_hum:.1f}%!")

# ==============================================================================
# CHECK 5: s22 HPA Tissue Co-Expression after removing IG/TR V(D)J gene segments
# ==============================================================================
print("\n=== CHECK 5: s22 HPA Tissue Co-Expression without germline IG/TR segments ===")
hpa = pd.read_parquet(f"{ROOT}/data/processed/hpa_tissue_log.parquet")
print("hpa_tissue_log shape:", hpa.shape)
ig_tr_pat = re.compile(r"^(IG[HKL][VDJCAEGMS]|TR[ABGD][VDJC])")
non_ig = [g for g in hpa.index if not ig_tr_pat.match(str(g))]
hpa_clean = hpa.loc[non_ig]
mvp_v = hpa_clean.loc["MVP"].values
X = hpa_clean.values
# Check whether Claude used Pearson or Spearman on hpa_tissue_log:
r_p = pd.Series([np.corrcoef(mvp_v, X[i])[0, 1] for i in range(len(hpa_clean))], index=hpa_clean.index).drop("MVP").sort_values(ascending=False)
r_s = pd.Series([spearmanr(mvp_v, X[i]).statistic for i in range(len(hpa_clean))], index=hpa_clean.index).drop("MVP").sort_values(ascending=False)
NAD_SET = {"NAMPT","NMNAT1","NMNAT2","NMNAT3","NADSYN1","NAPRT","QPRT","NADK","NADKD1","CD38","BST1","PARP1","PARP2","SARM1","NNMT","NMRK1","NMRK2","IDO1","TDO2","ACMSD","HAAO","KYNU","AFMID","NUDT12"}
nad_meas = NAD_SET & set(hpa_clean.index)
for label_m, s_corr in [("Pearson (no IG/TR)", r_p), ("Spearman (no IG/TR)", r_s)]:
    t200 = list(s_corr.index[:200])
    hits_n = sorted(set(t200) & nad_meas)
    pval_n = hypergeom.sf(len(hits_n) - 1, len(s_corr), len(nad_meas), 200)
    print(f"{label_m}: {len(hits_n)}/{len(nad_meas)} NAD genes in top 200 {hits_n}, p={pval_n:.4g} | top15={t200[:15]}")
    for g_chk in ["PARP4", "TEP1", "ANXA2", "S100A10"]:
        if g_chk in s_corr.index:
            rk = int(list(s_corr.index).index(g_chk)) + 1
            print(f"  {g_chk}: rank {rk}/{len(s_corr)} (corr={s_corr[g_chk]:.3f})")

json.dump(out, open(f"{ROOT}/argon/results/audit_004_checks.json", "w"), indent=2)
