# Pre-registration: does MVP mark the non-dividing compartment inside tumors?

**Date:** 2026-11-06. Tests whether the developmental result (`results/development.json`: MVP rises as
proliferation falls, 6 of 7 organs) extends to tumors, which would tie it to the thirty-year LRP
chemoresistance association. Committed before any correlation was computed. Claude drafted it; Graham
stated no numeric predictions.

## Hypothesis under test
If MVP marks quiescent or differentiated cells rather than causing drug resistance, it should
**anti-correlate with proliferation inside tumors**, as it does across development. Chemotherapy kills
dividing cells, so a tumor richer in non-dividing cells survives it — which would explain the biomarker
without MVP acting on any drug.

## Data
The six TCGA cohorts already on disk: LUAD, LUSC, SKCM, PAAD, LIHC, THCA. Primary tumor samples, one per
patient, as in `src/models.py`.

## Statistic
Proliferation score = mean of z-scored log expression of HALLMARK_E2F_TARGETS and
HALLMARK_G2M_CHECKPOINT members, **MVP removed if present** (`src/scores.py` asserts and aborts on a leak).

Per cohort, two models for every expressed gene:
1. **Unadjusted:** Spearman rho against the proliferation score.
2. **Primary (adjusted):** the gene's coefficient on the proliferation score in
   `gene ~ proliferation + purity + myeloid + lymphoid`, the covariate set already used in §2.

The quantity reported is **MVP's percentile in that cohort's genome-wide distribution**, not the raw
coefficient, since every gene shifts with global tumor composition.

## Labels (primary, adjusted)
- **NON-DIVIDING MARKER:** MVP at or below the 10th percentile in at least 4 of 6 cohorts.
- **PROLIFERATION-ASSOCIATED:** at or above the 90th in at least 4 of 6.
- **NO RELATION:** anything else.

Unadjusted results are reported beside the primary. If the two disagree, the result is reported as
composition-driven and the adjusted model governs.

## Gate, before reading MVP
MKI67, TOP2A and CCNB1 must each sit at or above the 90th percentile in at least 4 of 6 cohorts, for at
least 2 of the 3. If proliferation genes do not track the proliferation score, the score is not
measuring proliferation and the MVP result is uninformative.

## Interpretation
- **NON-DIVIDING MARKER:** the developmental result generalises to tumors, and the LRP association gets
  an explanation that needs no mechanism — MVP marks the compartment chemotherapy cannot kill. It would
  remain a correlation, and it would not show that MVP does nothing.
- **PROLIFERATION-ASSOCIATED:** the unifying story collapses. The developmental finding would then be
  about tissue maturation specifically, not about cell division in general.
- **NO RELATION:** MVP is not tracking division state in tumors either way, and the developmental result
  stays a developmental result.

## Limits
Bulk tumor expression, so a within-tumor compartment claim is being tested with between-tumor variation —
a tumor scoring low for proliferation has more quiescent cells, but this cannot show that the MVP-high
cells *are* the quiescent ones. Single-cell data would be needed for that. TCGA has no matched chemotherapy
response, so the link to the biomarker stays indirect.
