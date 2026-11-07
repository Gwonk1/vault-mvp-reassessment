# Pre-registration: does NSUN2 repress CYP3A4 in human liver?

**Date:** 2026-11-07, before any correlation computed. Tests the chain in Graham's article 2 §8:
vault RNA -> NSUN2 m5C -> DICER -> svRNAb -> represses **CYP3A4**, the largest contributor to oxidative
drug metabolism in humans. Shown in MCF7/HepG2 cell lines (Persson 2009); svRNAb was never detected in
liver tissue, which is the one place it would matter.

## Data
TCGA-LIHC, 366 primary liver tumours, already on disk (`data/processed/bulk/lihc.expr.parquet`).
**VTRNA1-1 is absent** from the mRNA quantification (it is a Pol III transcript), so this tests the
**NSUN2 -> CYP3A4 arm only**, not the vault RNA itself. That is a real limit, stated up front.

## Primary test
Partial Spearman correlation of **NSUN2 vs CYP3A4**, controlling for hepatocyte differentiation:
HNF4A, NR1I2 (PXR), NR1I3 (CAR) and ALB. Without that adjustment any correlation would just report how
differentiated the tumour is.

- **SUPPORTS REPRESSION:** partial rho significantly **negative** (p < 0.05).
- **AGAINST:** significantly positive.
- **NO RELATION:** not significant.

## Gate, before reading NSUN2
HNF4A and NR1I2 must each positively predict CYP3A4 with rho > 0.40 and p < 1e-10. If the known
regulators of CYP3A4 do not show up, the data cannot address the question and the result is uninformative.

## Specificity controls
The same partial correlation for NSUN2 against **CYP2E1** and **CYP1A2** (other hepatic P450s not
proposed as svRNAb targets) and against **ALB**. A repression specific to CYP3A4 should be absent or
weaker in these. If NSUN2 anti-correlates with every P450 equally, it is a differentiation artefact.

## Secondary
MVP and DICER1 against CYP3A4 under the same adjustment, reported for context only.

## Limits
Tumour tissue, not normal liver, and tumours lose CYP3A4 expression as they dediffentiate — the reason
the adjustment set exists. Bulk tissue mixes hepatocytes with stroma and immune cells. mRNA is a poor
proxy for CYP3A4 enzyme activity. A negative result here does not refute the cell-line mechanism; it
bounds how much it can matter at the tissue level.
