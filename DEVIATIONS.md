# Deviations from the plan and pre-registration

Each entry was written before the affected human expression result was viewed. Entry 7 records a
result already obtained (the Qiu lookup) because the plan ordered it first.

1. **IFNG.GS source.** Benci 2019 Table S1 could not be fetched (cell.com 403, PMC interstitial).
   Lists come from the claim text of US12662705B2 (Minn, University of Pennsylvania, the same group).
   ISG.RS there matches Qiu 2023 Fig 1E source data exactly (38 of 38), an independent check. IFNG.GS
   has no second independent check beyond Hallmark. A person with a browser should compare against
   Table S1.
2. **Plan §6 is wrong on one point.** It says MVP is not in Benci's named sets. MVP *is* in IFNG.GS.
   But IFNG.GS (176 genes) is exactly Hallmark IFN-γ (200) minus the 24 genes also in ISG.RS, apart
   from symbol renames. So the placement is by default and no one tested MVP. It does not settle the
   question. It does make the exclusion assertion essential: MVP is always removed from IFNG.GS and
   Hallmark IFN-γ before scoring.
3. **Single-cell substitution.** The plan's datasets are controlled access: Yanagawa (dbGaP
   phs002371), Sinjab (EGA EGAS00001005021). Per the pre-registered fallback, the lung test uses
   Kim 2020 GSE131907 (LUAD, authors' cell labels). Jerby-Arnon 2018 GSE115978 (melanoma, malignant
   labels, ICB-naive and post-ICB) is added as a second independent test, because the bulk cohorts are
   mostly melanoma. Controlled-access data remains the better test if Graham wants to apply for it.
4. **Bulk data source.** cBioPortal iAtlas-harmonized versions where available (Riaz, Hugo, Liu, Gide,
   IMvigor210), cBioPortal for Van Allen, GEO GSE135222 for Jung.
5. **Definitions the pre-registration left open.**
   - Pre-treatment: `SAMPLE_TREATMENT` indicating pre-treatment. Where a study lacks the field, every
     sample is used and the fact is printed. First sample per patient.
   - Expressed gene (null universe): nonzero in ≥ 50% of a cohort's samples and in at least 3 cohorts.
   - Covariates: purity_proxy = ESTIMATE score (Yoshihara sets, via tidyestimate). myeloid = MCP-counter
     Monocytic lineage. lymphoid = MCP-counter T, CD8 T, cytotoxic, NK and B lineage union. Any
     covariate gene also in ISG.RS, IFNG.GS or MVP is removed from the covariate.
   - Null estimator: per-gene OLS, then per-gene REML with Hartung-Knapp, the same as MVP.
   - Single-cell expression: log1p of CP10K, computed on all genes per cell. Per-patient Spearman of
     MVP against each score, plus a per-patient partial regression giving β and Δ; Fisher z or the
     regression estimates are then combined by REML with Hartung-Knapp.
6. **Named sensitivity analyses (exploratory, added now).** Unadjusted model; Hallmark IFN-α/γ as
   coarse controls; ISG.RS restricted to the 24 genes in Hallmark IFN-γ; dropping any cohort in turn.
   Reason: ISG.RS contains non-ISG genes (ROBO1, SLC6A15, CA2, HSD17B1, CCNA1) that may carry compartment
   signal unrelated to interferon. The adjusted β(IFNG.GS) may also be attenuated, since it overlaps the
   immune covariates. This is why the genome-wide null is the interpretive standard.
7. **Epigenetic lookup ran first, as the plan directs** (`results/epigenetic.md`).
