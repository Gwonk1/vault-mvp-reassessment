#!/usr/bin/env bash
# Fetch the third-party sources this analysis reads.
# Verify afterwards with:  sha256sum -c SHA256SUMS.txt
set -euo pipefail
cd "$(dirname "$0")"

get() { # get <url> <outfile>
  if [ -f "$2" ]; then echo "have   $2"; return; fi
  echo "fetch  $2"
  curl -fsSL --retry 3 -o "$2" "$1" || echo "FAILED $2  <- $1"
}

# --- PDB structures (public domain) ---
for id in 9BW6 11JB 9R86 9R87; do
  get "https://files.rcsb.org/download/${id}.cif.gz" "${id}.cif.gz"
  get "https://data.rcsb.org/rest/v1/core/entry/${id}" "${id}_meta.json"
done

# --- BioPlex interactomes (public) ---
get "https://bioplex.hms.harvard.edu/data/BioPlex_293T_Network_10K_Dec_2019.tsv" \
    "BioPlex_293T_Network_10K_Dec_2019.tsv"
get "https://bioplex.hms.harvard.edu/data/BioPlex_HCT116_Network_5.5K_Dec_2019.tsv" \
    "BioPlex_HCT116_Network_5.5K_Dec_2019.tsv"

# --- IntAct interaction queries (public API) ---
for g in MVP PARP4 TEP1; do
  get "https://www.ebi.ac.uk/intact/ws/interaction/findInteractions/${g}" "intact_${g}.json"
done

# --- CCLE metabolomics (public) ---
get "https://data.broadinstitute.org/ccle/CCLE_metabolomics_20190502.csv" \
    "CCLE_metabolomics_20190502.csv"

cat <<'MANUAL'

------------------------------------------------------------------
MANUAL DOWNLOADS — fetch these yourself, then re-run sha256sum -c
------------------------------------------------------------------
Licences for these are not confirmed for redistribution, so this
script will not mirror them. Each is free to read at its source.

  bioRxiv preprints (CC-BY 4.0) - download the PDF and extract text:
    osinski_2026_tir_vault      doi 10.64898/2026.05.01.722283
    lemouellic_2026_tep1_nadase doi 10.64898/2026.09.04.749371
    hornebeck_2026_tetir        doi 10.64898/2026.09.21.753143

  Publisher-hosted:
    lodwick_2025.xml, lodwick_supp_*  PMID 40691181 (Nat Commun 2025)
    PMC13100048.xml                   PMC13100048
    musgrove_vaultrc5.*, musgrove_*   PMID 42031226

  Portal exports (free account may be required):
    *_data_cna.txt, ccle_data_cna.txt   cBioPortal, per-study CNA export
    PXD071329_*.xlsx                    PRIDE PXD071329
    eggnog_raw_alg_*.json                eggNOG 5.0 orthogroup alignments
    baits-latest.txt                     BioGRID ORCS 2.0.18

See SHA256SUMS.txt for the exact bytes used.
MANUAL
