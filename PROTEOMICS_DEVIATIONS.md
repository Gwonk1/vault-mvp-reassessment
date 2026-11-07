# Deviations: protein co-abundance test

Written while data downloaded, before any protein value was read.

1. **Antibody panels excluded.** Some cBioPortal `protein_quantification` profiles are RPPA-style
   panels of a few hundred antibodies, not discovery mass spectrometry (`brca_tcga_pub2015` returns
   173 proteins). Profiles with fewer than **2,000 measured proteins** are dropped: a 173-protein
   universe cannot support a co-abundance ranking or a GO enrichment.
2. **Cell lines reported separately.** `ccle_broad_2019` is cell-line proteomics, not tumor tissue, so
   it falls outside the pre-registered sample definition. It is **not pooled** into the primary
   meta-analysis. It is reported as an independent replication, and the distinction is stated in the
   result, since cell lines carry no stroma and therefore none of the purity confound named in the
   pre-registration.
3. **Cohort list fixed by the fetch**, not chosen afterward: every qualifying profile the API returned
   is used. The list is printed in `results/fetch_prot.log`.

## Added 2026-11-06, before the analysis was run (prompted by `gemini-argon-audit.txt` §1A)

4. **Duplicate TCGA cohorts removed.** cBioPortal served both legacy and PanCanAtlas repackagings of the
   same CPTAC tumors — verified shared patients: brca 1,084, coadread 594, ov 585. Pooling both copies
   would double-count three studies, shrink the Hartung-Knapp intervals and let 2-cohort proteins pass the
   `MIN_COH = 3` rule. **The legacy `brca_tcga`, `coadread_tcga` and `ov_tcga` are dropped; the
   PanCanAtlas versions are kept** as the harmonised ones.
5. **Normal-adjacent samples now actually excluded.** The intended filter contained `and False`, so it
   never ran, and the line after it overwrote the result. TCGA sample barcodes ending `-10` or `-11` are
   normal tissue and are now removed, as the pre-registration required ("tumor samples").
6. **Three pre-registered checks implemented** that the first draft of `src/prot_coabund.py` defined but
   never called: the 200 matched random query proteins for the specificity test, the 3-principal-component
   sensitivity analysis, and the CCLE cell-line replication. **The test was not run before this was fixed**,
   so no result was produced against an unmet pre-registration.
