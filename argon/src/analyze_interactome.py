"""Test A2: Physical & Nanometer-Proximity Interactomes:
1. Geissler et al. (Nat Comms 2026) Dictyostelium in situ MVPA-TurboID vs cytosolic TurboID + osmotic stress tomograms.
2. Lodwick et al. (Nat Comms 2025) endogenous human A549 anti-MVP sAB IP-MS (WT vs control sAB & PARP4-KO).
3. Go et al. (Nature 2021) Human Cell Map 192-compartment BioID proximity map.
4. BioPlex 3.0 (HEK293T & HCT116 AP-MS) + EBI IntAct physical interactome.
"""
import json, zipfile, os, re
import xml.etree.ElementTree as ET
import numpy as np
import pandas as pd

RAW = "~/projects/Vault/argon/raw"
OUT = "~/projects/Vault/argon/results"
os.makedirs(OUT, exist_ok=True)

def read_xlsx_sheet(path, sheet_name):
    ns = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    with zipfile.ZipFile(path) as z:
        wb = ET.fromstring(z.read("xl/workbook.xml"))
        sheets = [s.attrib["name"] for s in wb.findall(".//m:sheet", ns)]
        idx = sheets.index(sheet_name) + 1
        sst = []
        if "xl/sharedStrings.xml" in z.namelist():
            sroot = ET.fromstring(z.read("xl/sharedStrings.xml"))
            sst = ["".join(si.itertext()) for si in sroot.findall(".//m:si", ns)]
        w = ET.fromstring(z.read(f"xl/worksheets/sheet{idx}.xml"))
        rows = []
        for r in w.findall(".//m:row", ns):
            row_dict = {}
            for c in r.findall("m:c", ns):
                ref = c.attrib.get("r", "")
                col_letters = "".join(ch for ch in ref if ch.isalpha())
                col_idx = 0
                for ch in col_letters:
                    col_idx = col_idx * 26 + (ord(ch) - ord("A") + 1)
                t = c.attrib.get("t")
                v = c.findtext("m:v", default="", namespaces=ns)
                if t == "s" and v.isdigit():
                    v = sst[int(v)]
                elif t == "inlineStr":
                    v = "".join(c.itertext())
                row_dict[col_idx - 1] = v
            if row_dict:
                max_c = max(row_dict.keys())
                rows.append([row_dict.get(i, "") for i in range(max_c + 1)])
        return rows

res = {}

mvp_coab = pd.read_parquet("~/projects/Vault/data/processed/mvp_coabundance.parquet")
top100_coab = set(mvp_coab.head(101).index) - {"MVP"}
top250_coab = set(mvp_coab.head(251).index) - {"MVP"}

# 1. Dictyostelium in situ MVPA-TurboID
xlsx = f"{RAW}/natcomms_source_data/Source_data_Vault.xlsx"
rows_5d = read_xlsx_sheet(xlsx, "Fig. 5D")
hdr_5d = [f"col_{i}" if not h else h for i, h in enumerate(rows_5d[0])]
df_5d = pd.DataFrame(rows_5d[1:], columns=hdr_5d)
fc_col = [c for c in df_5d.columns if "foldchange.log2" in c][0]
q_col = [c for c in df_5d.columns if "qvalue" in c.lower()][0]
df_5d["log2fc"] = pd.to_numeric(df_5d[fc_col], errors="coerce")
df_5d["qval"] = pd.to_numeric(df_5d[q_col], errors="coerce")

fus_fc = float(df_5d.loc[df_5d["gene_symbols_or_id"] == "FUS01", "log2fc"].iloc[0])
mvpb_fc = float(df_5d.loc[df_5d["gene_symbols_or_id"] == "MVPB", "log2fc"].iloc[0])
assert fus_fc > 5.0 and mvpb_fc > 5.0
mvpa_hits = df_5d[(df_5d["qval"] < 0.01) & (df_5d["log2fc"] > 1.0)].sort_values("log2fc", ascending=False)

# Search Dictyostelium TurboID specifically for PARP, TEP1, Arp2/3, Annexin, EHD, Calpain, SPFH/Flotillin/Prohibitin
print("=== Dictyostelium TurboID: Targeted Family Check ===")
for kw in ["Poly \\[ADP-ribose\\]", "telomerase|TEP", "Actin-related protein 2/3|Arp2|Arp3|ARCC", "annexin|copine", "calpain", "prohibitin|stomatin|flotillin|hfl", "ribosom"]:
    m = df_5d[df_5d["fasta_headers"].str.contains(kw, case=False, na=False)].sort_values("log2fc", ascending=False)
    sig_m = m[(m["qval"] < 0.05) & (m["log2fc"] > 0.5)]
    print(f"  [{kw}]: total={len(m)}, MVPA-enriched(q<.05, log2FC>0.5)={len(sig_m)}")
    for _, r in sig_m.head(6).iterrows():
        desc = re.sub(r"^>[^\s]+\s+", "", str(r["fasta_headers"])).split(" OS=")[0][:65]
        print(f"     {str(r['gene_symbols_or_id']):14s} log2FC={r['log2fc']:+6.2f} q={r['qval']:.2e} | {desc}")

# 2. Lodwick et al. 2025 Human A549 Endogenous Anti-MVP sAB IP-MS (Fig 5c-d & Fig 5g)
print("\n=== Lodwick et al. 2025 (Nat Comms) Human A549 Endogenous Anti-MVP IP-MS ===")
r_lod = read_xlsx_sheet(f"{RAW}/lodwick_supp_4.xlsx", "Fig. 5c-d")
print("Fig 5c-d header:", r_lod[0])
df_lod = pd.DataFrame(r_lod[1:], columns=[f"c_{i}" if not h else h for i, h in enumerate(r_lod[0])])
for c in df_lod.columns[1:]:
    df_lod[c] = pd.to_numeric(df_lod[c], errors="coerce")
print("Fig 5c-d shape:", df_lod.shape, "cols:", list(df_lod.columns))
# Check MVP, PARP4, TEP1 in Lodwick IP-MS!
print(df_lod[df_lod["GeneName"].isin(["MVP", "PARP4", "TEP1"])].to_string(index=False))

# Compute WT VM1 (anti-MVP) vs WT H6 (control sAB) log2FC & t-test, and KD (PARP4-KO) VM1 vs KD H6
wt_vm1 = np.log2(df_lod[["WT-VM1-1", "WT-VM1-2", "WT-VM1-3"]].replace(0, np.nan))
wt_h6  = np.log2(df_lod[["WT-H6-1", "WT-H6-2", "WT-H6-3"]].replace(0, np.nan))
kd_vm1 = np.log2(df_lod[["KD-VM1-1", "KD-VM1-2", "KD-VM1-3"]].replace(0, np.nan))
kd_h6  = np.log2(df_lod[["KD-H6-1", "KD-H6-2", "KD-H6-3"]].replace(0, np.nan))

from scipy import stats
df_lod["wt_log2fc"] = wt_vm1.mean(axis=1) - wt_h6.mean(axis=1)
df_lod["wt_p"] = [stats.ttest_ind(wt_vm1.iloc[i].dropna(), wt_h6.iloc[i].dropna(), equal_var=True).pvalue
                  if wt_vm1.iloc[i].notna().sum()>=2 and wt_h6.iloc[i].notna().sum()>=2 else np.nan for i in range(len(df_lod))]
df_lod["kd_log2fc"] = kd_vm1.mean(axis=1) - kd_h6.mean(axis=1)
df_lod["kd_p"] = [stats.ttest_ind(kd_vm1.iloc[i].dropna(), kd_h6.iloc[i].dropna(), equal_var=True).pvalue
                  if kd_vm1.iloc[i].notna().sum()>=2 and kd_h6.iloc[i].notna().sum()>=2 else np.nan for i in range(len(df_lod))]

# If Lodwick sheet already has precomputed log2FC / p-value columns beyond col 12, print them too!
if len(df_lod.columns) > 13:
    print("Extra precomputed columns in Fig 5c-d:", list(df_lod.columns[13:]))

wt_ip_hits = df_lod[(df_lod["wt_log2fc"] > 1.0) & (df_lod["wt_p"] < 0.05)].sort_values("wt_log2fc", ascending=False)
kd_ip_hits = df_lod[(df_lod["kd_log2fc"] > 1.0) & (df_lod["kd_p"] < 0.05)].sort_values("kd_log2fc", ascending=False)
print(f"\nLodwick WT A549 native vault IP hits (log2FC>1, p<.05): {len(wt_ip_hits)}")
for _, r in wt_ip_hits.head(40).iterrows():
    tag = " [CPTAC TOP-100]" if r["GeneName"] in top100_coab else (" [CPTAC TOP-250]" if r["GeneName"] in top250_coab else "")
    coab_r = f" (coab r={mvp_coab.loc[r['GeneName'], 'r']:.2f})" if r["GeneName"] in mvp_coab.index else ""
    print(f"  {str(r['GeneName']):12s} WT_log2FC={r['wt_log2fc']:+5.2f} (p={r['wt_p']:.4f}) | PARP4KO_log2FC={r['kd_log2fc']:+5.2f}{coab_r}{tag}")

print("\nLodwick Fig 5g summary table:")
for r in read_xlsx_sheet(f"{RAW}/lodwick_supp_4.xlsx", "Fig. 5g"):
    if any(r): print(" ", r)

# 3. Human Cell Map (Go et al. Nature 2021)
preys = pd.read_csv(f"{RAW}/preys-latest.txt", sep="\t")
baits = pd.read_csv(f"{RAW}/baits-latest.txt", sep="\t")
print("\n=== Human Cell Map (192-compartment BioID) ===")
print("Sample preys symbols:", list(preys["symbol"].head(10)))
print("Preys match:", preys[preys["symbol"].astype(str).str.upper().isin(["MVP", "TEP1", "PARP4"])].to_string(index=False))
print("Baits cols:", list(baits.columns))
b_col = baits.columns[0]
print("Baits match:", baits[baits.astype(str).apply(lambda col: col.str.upper().isin(["MVP", "TEP1", "PARP4"])).any(axis=1)].to_string(index=False))

# 4. BioPlex 3.0 (HEK293T & HCT116 AP-MS)
for cell, fn in [("HEK293T", "BioPlex_293T_Network_10K_Dec_2019.tsv"), ("HCT116", "BioPlex_HCT116_Network_5.5K_Dec_2019.tsv")]:
    bp = pd.read_csv(f"{RAW}/{fn}", sep="\t")
    sub = bp[(bp["SymbolA"].isin(["MVP", "TEP1", "PARP4"])) | (bp["SymbolB"].isin(["MVP", "TEP1", "PARP4"]))].sort_values("pInt", ascending=False)
    print(f"\n=== BioPlex 3.0 {cell} (n_edges={len(sub)}) ===")
    print(sub.to_string(index=False))
    res[f"bioplex_{cell}"] = sub.to_dict(orient="records")

# 5. EBI IntAct physical interactions
print("\n=== EBI IntAct Physical Interactomes ===")
intact_sets = {}
for sym in ["MVP", "TEP1", "PARP4"]:
    d = json.load(open(f"{RAW}/intact_{sym}.json"))
    partners = {}
    for row in d.get("content", []):
        # Check human-human or all physical edges
        na = str(row.get("interactorNameA") or row.get("geneNameA") or row.get("moleculeA") or row.get("idA") or "")
        nb = str(row.get("interactorNameB") or row.get("geneNameB") or row.get("moleculeB") or row.get("idB") or "")
        # inspect all string fields if na/nb empty
        if not na or not nb:
            pass
        partners.setdefault((na, nb), []).append(row)
    if d.get("content") and sym == "MVP":
        print("IntAct MVP raw row[0]:", d["content"][0])

res["dicty_mvpa_top60"] = mvpa_hits[["protein_id", "gene_symbols_or_id", "log2fc", "qval", "fasta_headers"]].head(60).to_dict(orient="records")
res["lodwick_wt_hits"] = wt_ip_hits[["GeneName", "wt_log2fc", "wt_p", "kd_log2fc", "kd_p"]].to_dict(orient="records")
res["lodwick_kd_hits"] = kd_ip_hits[["GeneName", "wt_log2fc", "wt_p", "kd_log2fc", "kd_p"]].to_dict(orient="records")
json.dump(res, open(f"{OUT}/test_a2_interactome.json", "w"), indent=2)
