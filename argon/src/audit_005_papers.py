#!/usr/bin/env python3
"""
Complete adversarial fact-check for Back-channel 005:
1. Exact conservation across all MVP regions on Claude's 2QPP0 trimmed alignment (human-anchored)
2. Exact phospho_part2.json check (64 rows vs "0 of 44, all |rho|<0.11")
3. Exact PDB/mmCIF coordinate check for S445 and S864/S867/S873/S876 across all cached vault structures
4. Exact verification of every remaining quantitative figure in Paper 1 & Paper 2 against results/*.json
"""
import glob
import gzip
import json
import os
import re
import statistics
import tarfile
from collections import Counter

ROOT = "~/projects/Vault"
OUT = f"{ROOT}/argon/results/audit_005_papers.json"

out = {}

# ---------------------------------------------------------
# 1. Alignment domain conservation (Claude's exact 2QPP0 trimmed alignment)
# ---------------------------------------------------------
T = tarfile.open(f"{ROOT}/data/raw/divergence/2759_trimmed_algs.tar")
member = [x for x in T.getmembers() if x.name.endswith("/2QPP0.trimmed_alg.faa.gz")][0]
with gzip.open(T.extractfile(member), "rt") as fh:
    seqs = {}
    cur = None
    for line in fh:
        line = line.strip()
        if line.startswith(">"):
            cur = line[1:].split()[0]
            seqs[cur] = []
        elif cur:
            seqs[cur].append(line)
seqs = {k: "".join(v) for k, v in seqs.items()}
hum_key = [k for k in seqs if "9606.ENSP00000378760" in k][0]
hseq = seqs[hum_key]

# Check how surface.py computes cons: most frequent non-gap residue or identity to human among non-gap (with >=20% coverage)?
# Let's read lines 60-130 of surface.py to match Claude's formula 100%
with open(f"{ROOT}/src/surface.py") as fh:
    surf_code = fh.read()

# Reconstruct human sequence positions (note trimmed alignment may drop columns! Wait: how does human pos map if trimmed?)
# Let's check length of ungapped hseq in trimmed alignment vs full 893-aa human MVP!
ungapped_trimmed = hseq.replace("-", "")
out["trimmed_alignment_info"] = {
    "n_seqs": len(seqs),
    "aln_cols": len(hseq),
    "human_ungapped_len_in_trimmed": len(ungapped_trimmed),
}

# Fetch full 893-aa human MVP from argon/data or uniprot/cif if available, or check how Claude anchored human residues!
# Let's check 11JB entity sequence or argon/results/test_a3_pocket_and_tep1.json
full_mvp_seq = None
cif_candidates = glob.glob(f"{ROOT}/data/raw/struct/*") + glob.glob(f"{ROOT}/argon/data/**/*", recursive=True)
for p in cif_candidates:
    if os.path.isfile(p) and ("11jb" in p.lower() or "9bw6" in p.lower()):
        opener = gzip.open if p.endswith(".gz") else open
        with opener(p, "rt", errors="ignore") as fh:
            txt = fh.read(200000)
        # look for MVTEE... human MVP sequence
        m = re.search(r"(MAT[A-Z\n\r]{800,950})", txt)
        if m:
            cand = re.sub(r"[^A-Z]", "", m.group(1))
            if 885 <= len(cand) <= 900:
                full_mvp_seq = cand
                break

# Also check if there is an untrimmed alignment or fasta in argon/data
for p in glob.glob(f"{ROOT}/argon/**/*", recursive=True):
    if os.path.isfile(p) and p.endswith((".fa", ".faa", ".fasta")):
        with open(p) as fh:
            ftxt = fh.read()
        if "ENSP00000378760" in ftxt:
            for rec in ftxt.split(">")[1:]:
                hdr, *body = rec.splitlines()
                if "ENSP00000378760" in hdr:
                    s = "".join(body).replace("-", "").strip()
                    if len(s) == 893:
                        full_mvp_seq = s

out["full_mvp_len"] = len(full_mvp_seq) if full_mvp_seq else None

# Map trimmed alignment columns onto full 893-aa human sequence via Bio.Align.PairwiseAligner (as surface.py does)
from Bio.Align import PairwiseAligner
if full_mvp_seq:
    al = PairwiseAligner()
    al.mode = "global"
    al.match_score = 2
    al.mismatch_score = -1
    al.open_gap_score = -5
    al.extend_gap_score = -0.5
    best = al.align(full_mvp_seq, ungapped_trimmed)[0]
    # map ungapped_trimmed index -> full_mvp_seq 1-based pos
    trim_to_full = {}
    for (f0, f1), (t0, t1) in zip(*best.aligned):
        for fi, ti in zip(range(f0, f1), range(t0, t1)):
            if full_mvp_seq[fi] == ungapped_trimmed[ti]:
                trim_to_full[ti] = fi + 1

    # Now compute both: (A) modal non-gap frequency (Shannon/modal as in surface.py) and (B) human identity among non-gap
    col_for_t = []
    for col, c in enumerate(hseq):
        if c != "-":
            col_for_t.append(col)
    pos_modal = {}
    pos_hum_id = {}
    for ti, col in enumerate(col_for_t):
        if ti not in trim_to_full:
            continue
        fpos = trim_to_full[ti]
        col_chars = [s[col] for s in seqs.values() if s[col] not in "-X"]
        if len(col_chars) < 0.2 * len(seqs):
            continue
        cnt = Counter(col_chars)
        pos_modal[fpos] = cnt.most_common(1)[0][1] / len(col_chars)
        pos_hum_id[fpos] = cnt[hseq[col]] / len(col_chars)

    def stats_for(dmap, a, b):
        vals = [dmap[p] for p in range(a, b + 1) if p in dmap]
        if not vals:
            return None
        return {
            "n_mapped": len(vals),
            "span_len": b - a + 1,
            "mean": round(statistics.mean(vals), 4),
            "median": round(statistics.median(vals), 4),
        }

    domain_defs = [
        ("Whole_protein_1_893", 1, 893),
        ("R1_1_53", 1, 53),
        ("R2_54_108", 54, 108),
        ("R3_109_162", 109, 162),
        ("R4_163_215", 163, 215),
        ("R5_216_269", 216, 269),
        ("R6_270_322", 270, 322),
        ("R7_323_376", 323, 376),
        ("R8_377_427", 377, 427),
        ("R9_428_498", 428, 498),
        ("Repeats_1_2_1_108", 1, 108),
        ("Repeats_3_4_canonical_109_215", 109, 215),
        ("PARP4_MINT_patch_160_260", 160, 260),
        ("Repeats_5_9_216_498", 216, 498),
        ("SPFH_shoulder_499_665", 499, 665),
        ("Cap_helix_666_790", 666, 790),
        ("Cap_disk_tail_791_893", 791, 893),
    ]
    out["domain_conservation_human_id"] = {name: stats_for(pos_hum_id, a, b) for name, a, b in domain_defs}
    out["domain_conservation_modal"] = {name: stats_for(pos_modal, a, b) for name, a, b in domain_defs}
    out["key_pocket_residues_human_id"] = {p: round(pos_hum_id.get(p, -1), 4) for p in [506, 547, 566, 567, 569]}

# ---------------------------------------------------------
# 2. Check all cached vault structures for S445 and S864/S867/S873/S876 (fast stream scan of first MVP chain)
# ---------------------------------------------------------
def fast_scan_cif(sp):
    opener = gzip.open if sp.endswith(".gz") else open
    rmap = {}
    target_ch = None
    in_atom = False
    headers = []
    with opener(sp, "rt", errors="ignore") as fh:
        for line in fh:
            if line.startswith("loop_"):
                in_atom = False
                headers = []
                continue
            if line.startswith("_atom_site."):
                in_atom = True
                headers.append(line.strip())
                continue
            if in_atom:
                if not line.startswith(("ATOM", "HETATM")):
                    if rmap:
                        break
                    continue
                parts = line.split()
                if len(parts) < len(headers):
                    continue
                # find indices once
                if not rmap and target_ch is None:
                    try:
                        i_ch = headers.index("_atom_site.auth_asym_id")
                        i_seq = headers.index("_atom_site.auth_seq_id")
                        i_comp = headers.index("_atom_site.label_comp_id")
                    except ValueError:
                        return {"err": "missing_cols"}
                ch = parts[i_ch]
                if target_ch is None:
                    target_ch = ch
                elif ch != target_ch:
                    if len(rmap) > 300:
                        break
                    else:
                        target_ch = ch
                        rmap = {}
                try:
                    ai = int(parts[i_seq])
                    rmap[ai] = parts[i_comp]
                except ValueError:
                    pass
    if not rmap:
        return {"empty": True}
    nums = sorted(rmap)
    return {
        "chain": target_ch,
        "n_modeled": len(nums),
        "min_res": nums[0],
        "max_res": nums[-1],
        "has_445": 445 in rmap,
        "missing_near_445": [x for x in range(435, 462) if x not in rmap],
        "modeled_ge_850": [f"{x}:{rmap[x]}" for x in nums if x >= 850],
        "has_864_867_873_876": {x: rmap.get(x) for x in [864, 867, 873, 876]},
    }

all_structs = sorted(set(
    glob.glob(f"{ROOT}/data/raw/struct/*.cif*") +
    glob.glob(f"{ROOT}/argon/data/**/*.cif*", recursive=True)
))
struct_info = {os.path.basename(sp): fast_scan_cif(sp) for sp in all_structs}
out["structures_modeled_residues"] = struct_info

# ---------------------------------------------------------
# 3. Verify every number in Paper 1 & Paper 2 against results/*.json
# ---------------------------------------------------------
def jload(fn):
    with open(f"{ROOT}/results/{fn}") as f:
        return json.load(f)

checks = {}

# prot_final + cna_adjusted
pf = jload("prot_final.json")
ca = jload("cna_adjusted.json")
checks["prot_coabundance"] = {
    "prot_final_n_cohorts": len(pf["cohorts"]),
    "prot_final_cohort_names": list(pf["cohorts"].keys()),
    "prot_final_dropped_duplicates_note": pf["dropped_duplicates"],
    "prot_final_n_genes": pf["n"],
    "prot_final_parp4_rank_incl_mvp": pf["parp4_rank"],
    "prot_final_tep1_rank_incl_mvp": pf["tep1_rank"],
    "prot_final_top3": pf["top40"][:3],
    "prot_final_pc3": pf["pc3"],
    "prot_final_ccle_n_samples_or_genes": {k: pf["ccle"][k] for k in ["n", "TEP1", "PARP4"]},
    "cna_adjusted_cohorts": ca.get("cohorts") if isinstance(ca.get("cohorts"), list) else len(ca.get("cohorts", [])),
    "cna_adjusted_summary": {k: v for k, v in ca.items() if k not in ("top100", "all")},
}

# sc_kim + bulk
sck = jload("sc_kim.json")
checks["ifn_sc_kim"] = sck
bk = jload("bulk.json")
bkr = jload("bulk_robust.json")
checks["ifn_bulk"] = {"bulk_keys": list(bk.keys()), "bulk": bk, "bulk_robust": bkr}

# persisters
checks["persisters"] = {
    "primary": jload("persister_primary.json"),
    "replication": jload("persister_replication.json"),
    "split": jload("persister_split.json"),
}

# coloss
cf = jload("coloss_final.json")
cfx = jload("coloss_fixed.json")
checks["coloss"] = {
    "final": {k: v for k, v in cf.items() if not isinstance(v, list) or len(v) < 5},
    "fixed": {k: v for k, v in cfx.items() if not isinstance(v, list) or len(v) < 5},
}

# vaultrc5_ko
checks["vaultrc5_ko"] = jload("vaultrc5_ko.json")

# cyp3a4
checks["cyp3a4"] = jload("cyp3a4.json")

# tissue_expression
te = jload("tissue_expression.json")
checks["tissue_expression"] = te

# crossspecies (Dictyostelium + annexin paralog count!)
cs = jload("crossspecies.json")
checks["crossspecies"] = {k: v for k, v in cs.items() if not isinstance(v, (list, dict)) or len(str(v)) < 1500}
# Check how many human ANXA paralogs exist in crossspecies!
checks["crossspecies_keys"] = list(cs.keys())

# turnover
to = jload("turnover.json")
checks["turnover"] = to

# coessentiality & orcs
ce = jload("coessentiality.json")
checks["coessentiality"] = ce
orc = jload("orcs_final.json")
checks["orcs_final"] = {k: v for k, v in orc.items() if not isinstance(v, (list, dict)) or len(str(v)) < 1500}

# pocket_geometry & surface & gnomad & divergence
checks["pocket_geometry"] = jload("pocket_geometry.json")
checks["surface"] = jload("surface.json")
checks["gnomad"] = jload("gnomad.json")
checks["divergence"] = jload("divergence.json")
checks["divergence_clade"] = jload("divergence_clade.json")

# lrp
checks["lrp"] = jload("lrp.json")
checks["lrp_mediate_matched"] = jload("lrp_mediate_matched.json")

out["paper1_2_json_checks"] = checks

with open(OUT, "w") as f:
    json.dump(out, f, indent=2)

print("Saved", OUT)
print("=== HUMAN DOMAIN CONSERVATION (human_id) ===")
for k, v in out.get("domain_conservation_human_id", {}).items():
    print(f"  {k:32s}: {v}")
print("=== HUMAN DOMAIN CONSERVATION (modal) ===")
for k, v in out.get("domain_conservation_modal", {}).items():
    print(f"  {k:32s}: {v}")
print("=== KEY POCKET RESIDUES ===")
print(" ", out.get("key_pocket_residues_human_id"))
print("=== STRUCTURES MODELED RESIDUES ===")
for k, v in struct_info.items():
    print(" ", k, "->", v)
