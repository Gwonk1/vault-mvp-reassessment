#!/usr/bin/env python3
"""
Pass-2 adversarial audit for Back-channel 005r:
1. Sweep every superlative/extremal/"only" claim in revised Paper 1 & Paper 2 against results/*.json
2. Search all local 2025-2026 primary texts (Lodwick, Osinski, Le Mouellic, Hornebeck, Geissler,
   Anthropic L05, Musgrove, Articles 1-5) for prior art on the 6 claimed novelties + TEP1 cellular assays
3. Quantitative test of the Keystone Argument (TEP1 stoichiometry, cellular toxicity in 2026 papers,
   and CCLE NAD+ power vs kcat).
"""
import glob
import json
import os
import re

def strip_html(h):
    h = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", h, flags=re.S | re.I)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h)).strip()

ROOT = "~/projects/Vault"
OUT = f"{ROOT}/argon/results/audit_005_pass2.json"
rep = {}

# ---------------------------------------------------------
# 1. Superlative / numerical checks in results/*.json
# ---------------------------------------------------------
with open(f"{ROOT}/results/lrp.json") as f:
    lrp = json.load(f)
# Deduplicate Docetaxel and recompute BH q-values on 18 unique drugs
seen = set()
uniq_lrp = []
for r in lrp["results"]:
    if r["drug"] not in seen:
        seen.add(r["drug"])
        uniq_lrp.append(dict(r))
uniq_sorted_p = sorted(uniq_lrp, key=lambda x: x["p"])
m_n = len(uniq_sorted_p)
for i, r in enumerate(uniq_sorted_p, 1):
    r["q_18"] = min(1.0, r["p"] * m_n / i)
# enforce monotonicity
for i in range(m_n - 2, -1, -1):
    uniq_sorted_p[i]["q_18"] = min(uniq_sorted_p[i]["q_18"], uniq_sorted_p[i + 1]["q_18"])

vtrna_drugs = [r for r in uniq_sorted_p if r["vtrna"]]
rep["lrp_full_18"] = {
    "ordered_by_rho": [
        {"rank": i + 1, "drug": r["drug"], "cls": r["cls"], "rho": round(r["rho"], 4),
         "p": round(r["p"], 5), "q_19": round(r["q"], 4), "q_18": round(r["q_18"], 4), "vtrna": r["vtrna"]}
        for i, r in enumerate(sorted(uniq_sorted_p, key=lambda x: x["rho"], reverse=True))
    ],
    "vtrna_drugs": vtrna_drugs,
}

# Check cyp3a4.json ("The only nominal association is with CYP2E1")
with open(f"{ROOT}/results/cyp3a4.json") as f:
    rep["cyp3a4"] = json.load(f)

# Check turnover.json per-cell-type half-lives (check 3x to 8x range across all cell types!)
with open(f"{ROOT}/results/turnover.json") as f:
    rep["turnover"] = json.load(f)

# Check development.json ("94th-95th percentile in six of seven human organs")
with open(f"{ROOT}/results/development.json") as f:
    rep["development"] = json.load(f)

# Check tissue_coexpr.json ("2 of 22 pathway genes in the top 200")
with open(f"{ROOT}/results/tissue_coexpr.json") as f:
    tc = json.load(f)
    rep["tissue_coexpr"] = {k: v for k, v in tc.items() if not isinstance(v, list) or len(v) < 25}

# Check sc_kim.json & sc_jerby.json
with open(f"{ROOT}/results/sc_kim.json") as f:
    sk = json.load(f)
    rep["sc_kim_keys"] = {k: v for k, v in sk.items() if not isinstance(v, (list, dict)) or len(str(v)) < 800}

# ---------------------------------------------------------
# 2. Extract and search all local 2025-2026 primary texts
# ---------------------------------------------------------
texts = {}

# Plain txt papers
for fn in ["anthropic_l05.txt", "osinski_2026_tir_vault.txt", "lemouellic_2026_tep1_nadase.txt",
           "hornebeck_2026_tetir.txt", "musgrove_vaultrc5.txt", "natcomms_supp_1.txt"]:
    p = f"{ROOT}/argon/raw/{fn}"
    if os.path.exists(p):
        with open(p, errors="ignore") as fh:
            texts[fn] = fh.read()

# Lodwick EPMC full text JSON? Check what's inside lodwick_epmc.json!
with open(f"{ROOT}/argon/raw/lodwick_epmc.json") as fh:
    lod_j = json.load(fh)
texts["lodwick_epmc.json"] = json.dumps(lod_j)

# Geissler 2026 Nat Comms HTML
with open(f"{ROOT}/argon/raw/natcomms_41467_026_71837.html", errors="ignore") as fh:
    texts["geissler_2026_natcomms.html"] = strip_html(fh.read())

# Anthropic supp HTML
if os.path.exists(f"{ROOT}/argon/raw/anthropic_supp.html"):
    with open(f"{ROOT}/argon/raw/anthropic_supp.html", errors="ignore") as fh:
        texts["anthropic_supp.html"] = strip_html(fh.read())

# Articles 1-5 (Graham's background articles!)
for i in range(1, 6):
    p = f"{ROOT}/data/raw/articles/article{i}.txt"
    if os.path.exists(p):
        with open(p, errors="ignore") as fh:
            texts[f"article{i}.txt"] = fh.read()

rep["corpus_lengths"] = {k: len(v) for k, v in texts.items()}

def search_corpus(patterns):
    hits = {}
    for doc, txt in texts.items():
        doc_hits = {}
        for label, pat in patterns.items():
            ms = list(re.finditer(pat, txt, re.I))
            if ms:
                doc_hits[label] = {
                    "count": len(ms),
                    "samples": [
                        re.sub(r"\s+", " ", txt[max(0, m.start() - 140):min(len(txt), m.end() + 220)])
                        for m in ms[:3]
                    ],
                }
        if doc_hits:
            hits[doc] = doc_hits
    return hits

novelty_queries = {
    "turnover_halflife": r"half[- ]life|Mathieson|SILAC|turnover|degrad|22\s*h|66\s*h",
    "pocket_access_pore": r"keyhole|pore|channel|solvent[- ]access|lumen[- ]only|exterior|waist|open|breath|Collins|AAV",
    "surface_conservation": r"conserved surface|lumen[- ]facing|outward[- ]facing|interior surface|ConSurf|surface conservation",
    "lrp_chemoresistance": r"ABCB1|P-glycoprotein|mitoxantrone|multidrug|chemoresist|doubling time|Gopinath",
    "cterm_tail_phospho": r"864|867|873|876|C-terminal tail|phospho|primate",
    "tep1_full_length_cells": r"full[- ]length|HEK293|293T|viability|cell death|toxic|autoinhibit|oligomer|basal NAD|kcat|turnover number",
}

rep["corpus_search"] = search_corpus(novelty_queries)

with open(OUT, "w") as f:
    json.dump(rep, f, indent=2)

print("Corpus lengths:", rep["corpus_lengths"])
print("LRP 18 ordered:", json.dumps(rep["lrp_full_18"]["ordered_by_rho"], indent=2))
print("CYP3A4:", json.dumps(rep["cyp3a4"], indent=2)[:800])
print("Development:", json.dumps(rep["development"], indent=2)[:800])
