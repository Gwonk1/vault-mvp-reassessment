# Pre-registration: does an EMT / adhesion axis absorb the membrane-repair module?

**Written 2026-11-07, before computing any EMT-adjusted correlation.** Committed before running
`src/emt_control.py`.

## Why

§28 reversed ledger #41: after residualising on the cytoplasmic-mass (N:C) proxy and proliferation, the
plasma-membrane-repair and caveolar gene sets are enriched around MVP at matched-random specificity
p = 0.000, with PARP4 and TEP1 as ranks 1 and 2.

**In the same section I flagged the reason that might be wrong (#109).** MVP's top-30 residualised
correlates include LMNA, FHL2, BCAR1, ITGA3, RRAS, ANLN and FOSL1, which read as an adhesion /
mesenchymal axis. EMT state is one of the largest axes of variation in CCLE, and AHNAK and myoferlin are
reported as EMT-associated. If an EMT score absorbs the signature, **#41 dies again** and the membrane
framing — my own favoured hypothesis — is withdrawn as a co-abundance claim.

## Circularity check, already performed and reported before the test

`HALLMARK_EPITHELIAL_MESENCHYMAL_TRANSITION` (200 genes) and the union of the four tested GO sets (529
genes) **overlap by only two genes: COL5A1 and RHOB.** None of ANXA2, S100A10, EHD2, MYOF, AHNAK,
AHNAK2, CAPN2, CD151, LMNA, FHL2, ITGA3 or BCAR1 is a member of HALLMARK_EMT. So residualising on an EMT
score cannot remove the module by construction. **Both overlapping genes are nonetheless excluded from
the EMT score**, as are MVP, PARP4 and TEP1.

## Method

Identical to §28 (`src/membrane_module2.py`) with one covariate added. Covariates become: the N:C proxy
(88 cytosolic RPL/RPS minus 46 nuclear HNRNP/SRSF/SF3B/SMC), six proliferation markers, **and an EMT
score** = mean z of HALLMARK_EMT members present in the matrix, excluding COL5A1, RHOB, MVP, PARP4,
TEP1. Residualise every protein at line level on all of it, then re-run the same matched-random
specificity test against the same externally defined gene sets, unmodified.

## Positive-control gates, all three required

1. **Assembly.** PARP4 and TEP1 must both remain in MVP's top 50. If adding a covariate destroys the
   confirmed physical core, the covariate is removing real signal and the result is UNINFORMATIVE.
2. **Complex.** PSMA1 must still recover at least 10 of 25 proteasome subunits in its top 50.
3. **EMT score validity.** The score must behave like EMT: VIM and FN1 must correlate positively with it
   and CDH1 negatively, each |r| >= 0.3. A score that does not separate those is not an EMT axis and the
   test says nothing.

## Primary prediction and kill condition

- **Module survives EMT adjustment** if `GOBP_PLASMA_MEMBRANE_REPAIR` keeps specificity **p < 0.05**.
- **Kill condition: if specificity p >= 0.05, ledger #41 is struck for the third time and I stop
  re-opening it.** The entry will record that the membrane neighbourhood is an EMT/adhesion correlate,
  that my own favoured hypothesis H2 from this afternoon is withdrawn, and that §28 was a confound I
  swapped for another rather than a finding.

## Secondary, reported without a registered threshold

Where PARP4, TEP1 and the named repair proteins (ANXA2, S100A10, EHD2, EHD4, CAPN2, MYOF, AHNAK) rank
before and after EMT adjustment, so the size of the shift is on the record either way.

## What this cannot do

It cannot establish contact — §13's IP-MS remains the only contact test and it missed at p = 0.058. It
tests one further confound. Others may remain, and surviving this one is not proof of anything.
