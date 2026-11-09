# Pre-registration: a bidirectional EMT score, run by someone who did not write #41

**Written 2026-11-09, before computing any correlation of this score with MVP.** The script
`src/emt_bidirectional.py` is committed with this file and is not run until after that commit.

## Who is writing this, and what they have already seen

Ledger #113 stopped the EMT question until someone who did not write the membrane-repair hypothesis
ran it. This registration is that run. The previous HALLMARK_EMT test (§29) is already in the
repository, and it was read before this file was written: its validity gate failed because CDH1
reached only r = -0.194, and the repair enrichments in that unlicensed run did not move. This is
therefore **not blind** to that failure. What it is not allowed to do is retune a score until the
module survives. The gene lists below are standard EMT markers. They were not picked from MVP's
top correlates. If this score's own validity gate fails, the verdict is UNINFORMATIVE and **no
second score is substituted in this session**.

## Score, locked

Built on transcription-factor and junction genes. The canonical markers used as the validity check
are held out, so the gate is not true by construction.

Score mesenchymal arm: ZEB1, ZEB2, SNAI1, SNAI2, TWIST1, PRRX1, FOXC2, CDH2.

Score epithelial arm: ESRP1, ESRP2, GRHL2, OCLN, CLDN4, CLDN7, TJP3, CRB3.

Held-out mesenchymal validators: VIM, FN1, SPARC, MMP2.

Held-out epithelial validators: CDH1, EPCAM, KRT8, DSP.

The score on each cell line is the mean z of the mesenchymal-arm genes present minus the mean z of
the epithelial-arm genes present. Any score-arm gene that also sits in a GO set tested below, or
that is MVP, PARP4 or TEP1, is dropped from the score and the drop is logged. The GO sets
themselves are not edited.

## Method

Same matrix, same N:C proxy, same six proliferation markers, same pairwise-complete
residualisation, same matched-random specificity test (200 draws, seed 0, abundance deciles) as
`src/membrane_module2.py`. One covariate is added: this score.

## Gates, all required

1. **Assembly.** PARP4 and TEP1 both remain in MVP's top 50 after residualisation. If the
   covariate destroys the confirmed core, the result is UNINFORMATIVE.
2. **Complex.** PSMA1 still recovers at least 10 of its proteasome subunits in its top 50.
3. **Score validity, on held-out genes.** At least six genes of each score arm must be measured,
   and at least three held-out genes of each validator arm. The mean Pearson correlation of the
   held-out mesenchymal genes with the score must be >= +0.30, and the mean for the held-out
   epithelial genes must be <= -0.30. Otherwise the score is not an EMT axis and the test says
   nothing.

## Primary call

- **Module survives** if all three gates pass and `GOBP_PLASMA_MEMBRANE_REPAIR` keeps specificity
  p < 0.05.
- **Kill.** If all three gates pass and that specificity p >= 0.05, ledger #41 is struck: the
  membrane-repair neighbourhood is an EMT/adhesion correlate. It is not reopened from this score.
- **UNINFORMATIVE** if any gate fails. #41 is left where §28 put it. No replacement score.

## Secondary, no threshold

Ranks of PARP4, TEP1, ANXA2, S100A10, EHD2, EHD4, CAPN2, MYOF, AHNAK, AHNAK2 before and after the
score is added. The secondary cannot rescue a kill or license a failed gate.
