# Pre-registration: does MVP's human protein neighbourhood exist in an amoeba?

**Date:** 2026-11-07, before computing any overlap. Claude drafted; Graham stated no predictions.

## Why
My co-abundance partners (§11, §14) come from human tumours and cell lines. An independent test exists
in *Dictyostelium discoideum*, separated from humans by >1 billion years, using a completely different
method: **MVPA-TurboID proximity labelling in live cells** (Geissler et al., Nat Commun 2026;
`argon/raw/natcomms_source_data/Source_data_Vault.xlsx`, sheet `Fig. 5D`, 3,001 proteins).

If the same proteins sit near the vault in an amoeba and co-vary with it in human tumours, the
association is ancient and real. If not, mine is vertebrate-specific or an artefact of abundance
correlation.

## Data definition (fixed from the file's own legend, before any overlap)
The legend states a contrast "A vs B" returns fold changes for **B/A**. The contrast is
"cytosolic TurboID vs MVPA-TurboID", so **positive log2FC = enriched in MVPA-TurboID = vault-proximal**.
- **Vault-proximal:** `foldchange.log2 > 0` and `qvalue < 0.05`.
- Mapping is by the file's own `gene_symbols` column, which already carries human-style symbols.
- **My ranking:** the CNA-adjusted list (`data/processed/mvp_coabundance_cna.parquet`), as that is now the
  reference ranking per §14.

## Gate
The published result reports Arp2/3 subunits and multiple PARPs among the top vault-proximal hits. At
least 3 of the Arp2/3 complex (ACTR2, ACTR3, ARPC1A/1B/2/3/4/5) must be vault-proximal. If they are not,
my reading of the file's sign convention is wrong and the test is reported as uninformative.

## Primary test
Hypergeometric enrichment of **vault-proximal** proteins among my **top 100**, within the shared universe.

- **ANCIENT ASSOCIATION:** p < 0.05 with at least 5 overlapping proteins.
- **NOT CONSERVED:** otherwise.

## Secondary (reported, not decisive)
1. Spearman between my adjusted co-abundance z and the *Dictyostelium* log2FC across the shared universe.
2. Named proteins reported individually: ACTR2, ACTR3, ARPC1B, CAPNS1, IQGAP1, CAP1, CLIC1, PARP4, TEP1.
   ANXA2 and S100A10 are vertebrate-specific and are expected to be absent; their absence is **not**
   evidence against anything.

## Limits
Orthology by gene symbol is crude across a billion years. Proximity labelling tags anything within
~10 nm, so it captures neighbourhoods rather than contacts. The amoeba has two MVP genes (MVPA, MVPB)
and only MVPA was tagged. A positive result shows ancient co-localisation, not shared function.
