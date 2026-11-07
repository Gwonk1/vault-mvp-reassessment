# Pre-registration: copy-number-adjusted co-abundance

**Date:** 2026-11-06, before any adjusted correlation was computed. Sensitivity analysis on `RESULTS.md`
§11, prompted by my own finding that 4 of MVP's top 100 partners (PYCARD, MAPK3, SULT1A3, ALDOA) sit
within 2 Mb of MVP on 16p11.2.

## Question
How much of MVP's protein co-abundance ranking is driven by shared somatic copy number rather than by
shared biology?

## Data
The 13 primary CPTAC-style cohorts from §11. **11 have copy-number data** on cBioPortal; `lusc_cptac_2021`
and `paad_cptac_2021` have none and are dropped from this analysis only. Continuous `log2CNA` preferred;
`gistic` discrete used where that is all that exists (luad, ucec). CCLE reported separately.

## Method
Per cohort, per protein: residualise protein abundance on **its own gene's copy number**, residualise MVP
on **MVP's copy number**, then correlate the residuals (Spearman on ranks, as in §11). Proteins or samples
lacking CNA are dropped pairwise. Pooling across cohorts by the same vectorised random-effects estimator.

This removes cis copy-number effects on **both** sides, which is what is needed to kill 16p11.2
co-amplification.

## Pre-specified expectations
- **Should fall out of the top 100:** PYCARD, MAPK3, SULT1A3, ALDOA (16p11.2 cis-neighbours).
- **Should remain high:** PARP4 (chr13) and TEP1 (chr14) — they are trans and physically confirmed, so if
  CNA adjustment demotes them the method is over-correcting and the whole analysis is suspect.

## Gate
PARP4 and TEP1 must remain in the top 1% after adjustment. If they do not, report as OVER-CORRECTED and
draw no conclusions about other proteins.

## What it decides
- If the 16p cluster drops and PARP4/TEP1/ANXA2/S100A10 stay, §11's ranking is biology, not amplicon, and
  the adjusted list becomes the reference ranking.
- If much of the top 100 collapses, §11's ranking was substantially copy-number driven and must be
  re-described.

## Note on the cross-test
§13's cross-test against physical IP-MS used the **unadjusted** ranking and failed (p = 0.058). Re-running
it on the adjusted ranking is **exploratory and labelled as such** — a failed primary cannot be rescued by
re-running with a different input, and any result there is reported as a secondary observation only.
