# Pre-registration: is my co-abundance module physically vault-associated?

**Date:** 2026-11-06, committed before computing any overlap. Claude drafted; Graham stated no predictions.

## Why
`RESULTS.md` §11 found MVP protein co-varies with a plasma-membrane-repair neighbourhood (ANXA2,
S100A10, EHD2/4, CAPN2) across 13 tumour cohorts and 375 cell lines. **Co-abundance is correlation, not
interaction** — the stated limit of #26. An independent physical IP-MS of the human vault exists
(Lodwick/Zhao, Nat Commun 2025, `argon/raw/lodwick_supp_4.xlsx`, sheet `Fig. 5c-d`, 1,205 proteins,
anti-MVP IP, WT vs PARP4-depleted, two backgrounds x 3 replicates). This asks whether the two agree.

## Data definitions (fixed from column diagnostics, before any overlap was computed)
- `LWTP`, `LKDP`, `WTKD_P` are **-log10(p)** (range 0-6.5; 18.2% of rows exceed 1.3).
- **WT vault interactor:** `WT_LFC > 0` and `LWTP > 1.3` (p < 0.05).
- **PARP4-dependent interactor:** WT interactor with `WTKD_LFC > 0` and `WTKD_P > 1.3`.
- **My ranking:** `data/processed/mvp_coabundance.parquet`, MVP excluded, restricted to proteins also
  present in the 1,205-protein IP universe.

## Gate (verified before registering, stated for the record)
Vault components must be recovered as WT interactors: MVP `WT_LFC 7.62 / LWTP 3.80`, PARP4 `8.66 / 3.32`,
TEP1 `6.27 / 3.33`. All pass. PARP4 is strongly depleted in KD (`WTKD_LFC 5.51`), confirming the KD arm
targets PARP4.

## Primary test
Hypergeometric enrichment of **WT vault interactors** among my **top 100** co-abundant proteins, within
the shared universe. Reported with the exact overlap and the background rate.

- **PHYSICALLY CORROBORATED:** enrichment p < 0.05 with at least 5 overlapping proteins.
- **NOT CORROBORATED:** otherwise. **This is the kill condition for #26** — if proteins that co-vary with
  MVP across hundreds of tumours are not preferentially found in a physical vault pull-down, the module is
  an abundance artefact and #26 must be downgraded.

## Secondary (reported, not decisive)
1. Spearman correlation between my pooled co-abundance z and `WT_LFC` across the shared universe.
2. Among my top 100, how many are **PARP4-dependent**, and is that fraction higher than among WT
   interactors generally? This tests argon's Tier-1 claim (PARP4 stations vaults at the membrane) using
   my independent partner list rather than its own.
3. Named membrane-repair genes reported individually: ANXA2, S100A10, EHD2, EHD4, CAPN2, CAPNS1, IQGAP1.

## Limits
One cell line, one antibody-based IP, 1,205 proteins — a small and biased universe versus my ~10,900.
An IP recovers stable binders and misses transient ones, so absence is weak evidence. Co-abundance and
co-purification can both be driven by shared regulation rather than contact.
