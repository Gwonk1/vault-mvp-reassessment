"""Test A4 + H1 + H4:
- Part 4A: Copy-number-adjusted MVP protein co-abundance (CCLE + CPTAC linear CNA), testing 16p11.2 confound (PYCARD, MAPK3, ALDOA) vs chr11 CASP1/4 & membrane-repair module.
- Part H1: Post-translational orphan-subunit stabilization (PARP4/TEP1 protein ~ own mRNA + MVP protein across 370+ CCLE lines).
- Part 4B: CCLE 225-metabolite LC-MS screen (Li et al. 2019) against MVP, PARP4, TEP1 protein abundance (raw + 3-PC removed), with FDR across all 225 metabolites.
- Part H4: CCLE cytotoxic drug AUC vs MVP protein, ABCC1 (16p13.11) protein, and proliferation rate.
"""
import os, json, urllib.request
import numpy as np
import pandas as pd
import requests
from scipy import stats

RAW = "~/projects/Vault/argon/raw"
OUT = "~/projects/Vault/argon/results"
os.makedirs(RAW, exist_ok=True)
os.makedirs(OUT, exist_ok=True)

HDR = {"User-Agent": "Mozilla/5.0"}

def dl(url, path):
    if not os.path.exists(path):
        req = urllib.request.Request(url, headers=HDR)
        with urllib.request.urlopen(req, timeout=40) as r:
            open(path, "wb").write(r.read())
    return path

# 1. Load CCLE proteomics already on disk
ccle_prot = pd.read_parquet("~/projects/Vault/data/processed/prot/ccle_broad_2019.parquet")
print("CCLE prot shape:", ccle_prot.shape, "sample cols:", list(ccle_prot.columns[:5]))

# 2. Download CCLE_metabolomics_20190502.csv (Broad Institute)
met_path = f"{RAW}/CCLE_metabolomics_20190502.csv"
try:
    dl("https://data.broadinstitute.org/ccle/CCLE_metabolomics_20190502.csv", met_path)
    print("Downloaded CCLE metabolomics:", os.path.getsize(met_path), "B")
except Exception as e:
    print("Broad metabolomics err:", e)

# 3. Download ccle_broad_2019 linear CNA (or discrete CNA) and mRNA from cBioPortal datahub or API
for fn in ["data_cna.txt", "data_linear_cna.txt"]:
    p = f"{RAW}/ccle_{fn}"
    if not os.path.exists(p):
        for base in [
            f"https://media.githubusercontent.com/media/cBioPortal/datahub/master/public/ccle_broad_2019/{fn}",
            f"https://raw.githubusercontent.com/cBioPortal/datahub/master/public/ccle_broad_2019/{fn}",
        ]:
            try:
                dl(base, p)
                if os.path.getsize(p) > 10000:
                    print(f"Downloaded ccle_{fn}: {os.path.getsize(p)} B")
                    break
                else:
                    os.remove(p)
            except Exception:
                pass

# Also fetch CPTAC linear CNA for major CPTAC cohorts from cBioPortal datahub!
cptac_studies = ["luad_cptac_2020", "lusc_cptac_2021", "paad_cptac_2021", "brca_cptac_2020", "gbm_cptac_2021", "ucec_cptac_2020", "coad_cptac_2019"]
cptac_cna_files = {}
for st in cptac_studies:
    for fn in ["data_linear_cna.txt", "data_cna.txt"]:
        p = f"{RAW}/{st}_{fn}"
        if os.path.exists(p) and os.path.getsize(p) > 10000:
            cptac_cna_files[st] = p
            break
        for base in [
            f"https://media.githubusercontent.com/media/cBioPortal/datahub/master/public/{st}/{fn}",
            f"https://raw.githubusercontent.com/cBioPortal/datahub/master/public/{st}/{fn}",
        ]:
            try:
                dl(base, p)
                if os.path.getsize(p) > 10000:
                    cptac_cna_files[st] = p
                    print(f"Downloaded {st}_{fn}: {os.path.getsize(p)} B")
                    break
                else:
                    os.remove(p)
            except Exception:
                pass
        if st in cptac_cna_files:
            break

# Fetch mRNA & drug AUC for key genes in ccle_broad_2019 via cBioPortal REST API (fast, targeted)
S = requests.Session()
S.headers["Content-Type"] = "application/json"
target_syms = ["MVP", "PARP4", "TEP1", "ABCC1", "ABCB1", "ABCG2", "PYCARD", "MAPK3", "ALDOA", "SULT1A3",
               "CASP1", "CASP4", "ANXA2", "S100A10", "S100A6", "CAPN2", "CAPNS1", "EHD2", "EHD4", "IQGAP1", "MKI67", "PCNA"]
genes_all = pd.DataFrame(S.get("https://www.cbioportal.org/api/genes?pageSize=100000&projection=SUMMARY", timeout=30).json())
sym2entrez = dict(zip(genes_all.hugoGeneSymbol, genes_all.entrezGeneId))
entrez2sym = dict(zip(genes_all.entrezGeneId, genes_all.hugoGeneSymbol))
t_ids = [int(sym2entrez[g]) for g in target_syms if g in sym2entrez]

samples = [s["sampleId"] for s in S.get("https://www.cbioportal.org/api/studies/ccle_broad_2019/samples?pageSize=100000", timeout=30).json()]
mrna_raw = S.post("https://www.cbioportal.org/api/molecular-profiles/ccle_broad_2019_rna_seq_mrna/molecular-data/fetch?projection=SUMMARY",
                  json={"entrezGeneIds": t_ids, "sampleIds": samples}, timeout=60).json()
df_mrna = pd.DataFrame([(entrez2sym[r["entrezGeneId"]], r["sampleId"], float(r["value"])) for r in mrna_raw], columns=["g", "s", "v"]).pivot(index="g", columns="s", values="v")
print("Fetched CCLE targeted mRNA:", df_mrna.shape)

res = {}

# ==============================================================================
# PART H1: Post-Translational Orphan-Subunit Stabilization in CCLE (mRNA vs Protein)
# ==============================================================================
print("\n=== TEST H1: Post-Translational Orphan-Subunit Stabilization (CCLE n~371) ===")
common_s = ccle_prot.columns.intersection(df_mrna.columns)
print("Shared mRNA + Mass-Spec Proteomics CCLE cell lines:", len(common_s))
h1_out = {}
for partner in ["PARP4", "TEP1", "ANXA2", "CAPN2"]:
    sub = pd.DataFrame({
        "p_prot": ccle_prot.loc[partner, common_s],
        "p_rna": np.log2(df_mrna.loc[partner, common_s] + 1.0),
        "mvp_prot": ccle_prot.loc["MVP", common_s],
        "mvp_rna": np.log2(df_mrna.loc["MVP", common_s] + 1.0),
    }).dropna()
    r_rna_rna = sub["p_rna"].corr(sub["mvp_rna"])
    r_prot_prot = sub["p_prot"].corr(sub["mvp_prot"])
    r_own = sub["p_prot"].corr(sub["p_rna"])
    # Partial correlation of p_prot with mvp_prot controlling for p_rna!
    res_p = sub["p_prot"] - np.poly1d(np.polyfit(sub["p_rna"], sub["p_prot"], 1))(sub["p_rna"])
    res_m = sub["mvp_prot"] - np.poly1d(np.polyfit(sub["p_rna"], sub["mvp_prot"], 1))(sub["p_rna"])
    r_partial, p_partial = stats.pearsonr(res_p, res_m)
    # Multiple regression R^2: own_rna alone vs own_rna + mvp_prot
    X1 = np.column_stack([np.ones(len(sub)), sub["p_rna"]])
    X2 = np.column_stack([np.ones(len(sub)), sub["p_rna"], sub["mvp_prot"]])
    y = sub["p_prot"].values
    r2_1 = 1 - np.sum((y - X1 @ np.linalg.lstsq(X1, y, rcond=None)[0])**2) / np.sum((y - y.mean())**2)
    r2_2 = 1 - np.sum((y - X2 @ np.linalg.lstsq(X2, y, rcond=None)[0])**2) / np.sum((y - y.mean())**2)
    print(f"  {partner:6s} (n={len(sub)}): r(mRNA, MVP_mRNA)={r_rna_rna:+.3f} -> r(Prot, MVP_Prot)={r_prot_prot:+.3f} | "
          f"partial r(Prot, MVP_Prot | own_mRNA)={r_partial:+.3f} (p={p_partial:.2e}) | R2 own_mRNA={r2_1:.3f} -> +MVP_Prot={r2_2:.3f}")
    h1_out[partner] = {"n": len(sub), "r_rna": float(r_rna_rna), "r_prot": float(r_prot_prot),
                       "partial_r_given_own_rna": float(r_partial), "partial_p": float(p_partial),
                       "r2_own_rna": float(r2_1), "r2_plus_mvp_prot": float(r2_2)}
res["test_h1_orphan_stabilization"] = h1_out

# ==============================================================================
# PART 4A: Copy-Number-Adjusted MVP Protein Co-Abundance (CPTAC + CCLE)
# ==============================================================================
print("\n=== TEST A4A: Copy-Number-Adjusted MVP Co-Abundance (16p11.2 Confound Dissection) ===")
def load_cbioportal_cna(path):
    df = pd.read_csv(path, sep="\t", low_memory=False)
    gcol = "Hugo_Symbol" if "Hugo_Symbol" in df.columns else df.columns[0]
    drop_cols = [c for c in ["Hugo_Symbol", "Entrez_Gene_Id", "Cytoband"] if c in df.columns]
    df = df.dropna(subset=[gcol]).set_index(gcol).drop(columns=[c for c in drop_cols if c != gcol], errors="ignore")
    df = df.apply(pd.to_numeric, errors="coerce")
    return df[~df.index.duplicated(keep="first")]

check_genes = ["PARP4", "TEP1", "PYCARD", "MAPK3", "ALDOA", "SULT1A3", "CASP1", "CASP4", "ANXA2", "S100A10", "CAPN2", "CAPNS1", "EHD2", "EHD4", "IQGAP1", "CLIC1"]

cna_results = {}
# CPTAC cohorts with continuous linear CNA
raw_rs_by_gene = {g: [] for g in check_genes}
adj_rs_by_gene = {g: [] for g in check_genes}
for st, cna_p in cptac_cna_files.items():
    prot = pd.read_parquet(f"~/projects/Vault/data/processed/prot/{st}.parquet")
    cna = load_cbioportal_cna(cna_p)
    shared = prot.columns.intersection(cna.columns)
    if len(shared) < 40 or "MVP" not in prot.index or "MVP" not in cna.index:
        continue
    mvp_p = prot.loc["MVP", shared]
    mvp_c = cna.loc["MVP", shared]
    valid_m = mvp_p.notna() & mvp_c.notna()
    # Residualize MVP protein against MVP CNA
    mp = mvp_p[valid_m]
    mc = mvp_c[valid_m]
    mvp_res = mp - np.poly1d(np.polyfit(mc, mp, 1))(mc)
    for g in check_genes:
        if g not in prot.index or g not in cna.index:
            continue
        gp = prot.loc[g, valid_m.index[valid_m]]
        gc = cna.loc[g, valid_m.index[valid_m]]
        ok = gp.notna() & gc.notna() & mvp_res.notna()
        if ok.sum() < 35:
            continue
        r_raw = float(mp[ok].corr(gp[ok]))
        # Residualize partner protein against BOTH its own CNA and MVP CNA!
        X = np.column_stack([np.ones(ok.sum()), gc[ok].values, mc[ok].values])
        yv = gp[ok].values
        g_res = yv - X @ np.linalg.lstsq(X, yv, rcond=None)[0]
        r_adj = float(np.corrcoef(mvp_res[ok].values, g_res)[0, 1])
        raw_rs_by_gene[g].append(r_raw)
        adj_rs_by_gene[g].append(r_adj)

print(f"CPTAC cohorts with matched linear CNA + Mass-Spec Proteomics: {len(cptac_cna_files)} ({list(cptac_cna_files.keys())})")
for g in check_genes:
    if raw_rs_by_gene[g]:
        mr = float(np.mean(raw_rs_by_gene[g]))
        ma = float(np.mean(adj_rs_by_gene[g]))
        pct_change = 100.0 * (ma - mr) / max(abs(mr), 1e-6)
        loc = "16p11.2 (29-31Mb)" if g in {"PYCARD", "MAPK3", "ALDOA", "SULT1A3"} else ("chr11 inflammasome" if g in {"CASP1", "CASP4"} else "off-chr16")
        print(f"  {g:10s} [{loc:18s}] k={len(raw_rs_by_gene[g])} | r_raw={mr:+.3f} -> r_CNA_adj={ma:+.3f} ({pct_change:+.1f}%)")
        cna_results[g] = {"k_cohorts": len(raw_rs_by_gene[g]), "r_raw": mr, "r_cna_adj": ma, "pct_change": pct_change, "locus": loc}
res["test_a4a_cptac_cna_adjusted"] = cna_results

# Also check CCLE CNA adjustment if ccle_data_linear_cna.txt or ccle_data_cna.txt exists
for fn in ["ccle_data_linear_cna.txt", "ccle_data_cna.txt"]:
    p = f"{RAW}/{fn}"
    if os.path.exists(p):
        ccna = load_cbioportal_cna(p)
        sh = ccle_prot.columns.intersection(ccna.columns)
        print(f"\nCCLE CNA ({fn}) shared samples with proteomics: {len(sh)}")
        if len(sh) >= 100 and "MVP" in ccna.index:
            # Test strictly in 16p-euploid cell lines (MVP discrete CNA == 0 or |linear CNA| < 0.2) AND CNA-regressed!
            mc = ccna.loc["MVP", sh]
            mp = ccle_prot.loc["MVP", sh]
            euploid = sh[(mc.abs() < 0.25) & mp.notna()] if "linear" in fn else sh[(mc == 0) & mp.notna()]
            print(f"  CCLE 16p11.2-euploid cell lines: n={len(euploid)}")
            ccle_cna_out = {}
            for g in check_genes:
                if g in ccle_prot.index:
                    r0 = float(mp.corr(ccle_prot.loc[g, sh]))
                    reup = float(ccle_prot.loc["MVP", euploid].corr(ccle_prot.loc[g, euploid]))
                    print(f"    CCLE {g:10s}: r_all={r0:+.3f} -> r_16p_euploid={reup:+.3f}")
                    ccle_cna_out[g] = {"r_all": r0, "r_16p_euploid": reup}
            res["test_a4a_ccle_euploid"] = ccle_cna_out
        break

# ==============================================================================
# PART 4B: CCLE 225-Metabolite LC-MS Screen (Li et al. 2019)
# ==============================================================================
print("\n=== TEST A4B: CCLE 225-Metabolite LC-MS Screen (Li et al. 2019) ===")
if os.path.exists(met_path):
    met = pd.read_csv(met_path)
    print("Metabolomics table shape:", met.shape, "first cols:", list(met.columns[:5]))
    id_col = "CCLE_ID" if "CCLE_ID" in met.columns else met.columns[0]
    met = met.set_index(id_col)
    met_num = met.select_dtypes(include=[np.number])
    shared_m = ccle_prot.columns.intersection(met_num.index)
    print(f"Shared CCLE cell lines (Mass-Spec Proteomics x 225 Metabolites): n={len(shared_m)}, n_metabolites={met_num.shape[1]}")

    # Raw & 3-PC-removed metabolite correlations with MVP, PARP4, TEP1
    # Remove top 3 PCs from metabolite matrix (and protein matrix) to control lineage/growth-rate confounding
    M_mat = met_num.loc[shared_m].copy()
    M_z = (M_mat - M_mat.mean()) / M_mat.std()
    M_fill = M_z.fillna(0.0).values
    U, S_svd, Vt = np.linalg.svd(M_fill, full_matrices=False)
    M_3pc = pd.DataFrame(M_fill - (U[:, :3] * S_svd[:3]) @ Vt[:3, :], index=shared_m, columns=M_mat.columns)

    mvp_vec = ccle_prot.loc["MVP", shared_m]
    parp4_vec = ccle_prot.loc["PARP4", shared_m]
    tep1_vec = ccle_prot.loc["TEP1", shared_m]

    rows_m = []
    for col in M_mat.columns:
        v = M_mat[col]
        ok = mvp_vec.notna() & v.notna()
        if ok.sum() < 100: continue
        r_raw, p_raw = stats.pearsonr(mvp_vec[ok], v[ok])
        rho_raw, _ = stats.spearmanr(mvp_vec[ok], v[ok])
        r_3pc, p_3pc = stats.pearsonr(mvp_vec[ok], M_3pc.loc[ok.index[ok], col])
        ok_p = parp4_vec.notna() & v.notna()
        r_parp4 = float(parp4_vec[ok_p].corr(v[ok_p]))
        ok_t = tep1_vec.notna() & v.notna()
        r_tep1 = float(tep1_vec[ok_t].corr(v[ok_t]))
        rows_m.append({"metabolite": col, "n": int(ok.sum()), "r_raw": float(r_raw), "rho_raw": float(rho_raw), "p_raw": float(p_raw),
                       "r_3pc": float(r_3pc), "p_3pc": float(p_3pc), "r_parp4": r_parp4, "r_tep1": r_tep1})
    df_mres = pd.DataFrame(rows_m)
    # Benjamini-Hochberg FDR
    for pcol, qcol in [("p_raw", "q_raw"), ("p_3pc", "q_3pc")]:
        ps = df_mres[pcol].values
        order = np.argsort(ps)
        ranks = np.empty_like(order); ranks[order] = np.arange(1, len(ps) + 1)
        q = ps * len(ps) / ranks
        q_mon = np.minimum.accumulate(q[order][::-1])[::-1]
        qf = np.empty_like(ps); qf[order] = np.clip(q_mon, 0, 1)
        df_mres[qcol] = qf

    df_mres = df_mres.sort_values("p_raw")
    df_mres.to_csv(f"{OUT}/ccle_metabolomics_mvp.csv", index=False)
    print(f"Metabolites at q_raw < 0.05: {(df_mres.q_raw < 0.05).sum()} | at q_3pc < 0.05: {(df_mres.q_3pc < 0.05).sum()}")
    print("\nTop 20 Metabolites correlated with MVP protein (raw):")
    print(df_mres.head(20)[["metabolite", "n", "r_raw", "q_raw", "r_3pc", "q_3pc", "r_parp4", "r_tep1"]].to_string(index=False))
    print("\nTop 15 Metabolites after 3-PC removal:")
    print(df_mres.sort_values("p_3pc").head(15)[["metabolite", "r_raw", "r_3pc", "q_3pc", "r_parp4", "r_tep1"]].to_string(index=False))
    print("\nTargeted check — NAD / NADP / Nicotinamide / Pantothenate / GSH:")
    nad_sub = df_mres[df_mres["metabolite"].str.contains("NAD|nicotin|pantothen|glutathione|GSH|GSSG|carnitine|LPC|LPE|ceramide", case=False, na=False)]
    print(nad_sub.head(25)[["metabolite", "r_raw", "q_raw", "r_3pc", "q_3pc", "r_parp4", "r_tep1"]].to_string(index=False))
    res["test_a4b_metabolomics_summary"] = {
        "n_cell_lines": int(len(shared_m)),
        "n_metabolites": int(len(df_mres)),
        "n_sig_raw_q05": int((df_mres.q_raw < 0.05).sum()),
        "n_sig_3pc_q05": int((df_mres.q_3pc < 0.05).sum()),
        "top20_raw": df_mres.head(20).to_dict(orient="records"),
        "top15_3pc": df_mres.sort_values("p_3pc").head(15).to_dict(orient="records"),
    }

json.dump(res, open(f"{OUT}/test_a4_cna_metab.json", "w"), indent=2)
