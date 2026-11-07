# Pre-registration: does the membrane-repair / endolysosomal module survive the cytoplasmic-mass confound?

**Written 2026-11-07, before computing any residualised correlation.** Committed before running
`src/membrane_module.py`.

## Why re-open ledger #41

The broad membrane-repair neighbourhood has now been pointed at by **three independent data types**, and
not one of them cleared its own bar:

1. **§11, co-abundance GO enrichment:** 50 of 101 terms pass matched-query specificity, including
   `GOBP_PLASMA_MEMBRANE_REPAIR` (specificity 0.010), `GOCC_CAVEOLA`, `GOBP_ENDOCYTOSIS` (0.000).
   Named partners: ANXA2, S100A10, EHD2, EHD4, CAPN2, CAPNS1.
2. **§13, independent anti-MVP IP-MS:** 12 of top 100 are physical interactors against 7.4 expected,
   hypergeometric **p = 0.058**. Registered threshold was 0.05. Struck as #41.
3. **§15, *Dictyostelium* proximity labelling:** 32 of 100 against 25.0 expected, **p = 0.067**.
   Also missed.

Ledger #75 already softened #41: these are failures to clear a line, not falsifications, both point
estimates are enrichments, and CAPN2, EHD4 and IQGAP1 were **absent from the IP table entirely**, so
they were never tested rather than refuted.

A fourth line arrived today from a blind second opinion: across CCLE lineages, MVP's top covariates
include CD63 (+0.891), OPTN (+0.831), EHD4 (+0.822), VPS35 (+0.818), ANXA2 (+0.746) and IQGAP1 (+0.851).
**But §27b established that a housekeeping nuclear-to-cytoplasmic proxy alone explains R² = 0.515 of
lineage-mean MVP variance, and that cytosolic ribosomal proteins correlate +0.83 to +0.85 with it.** Any
cytoplasmic protein will covary with MVP through that confound. The fourth line is therefore worthless
as it stands, and this test is whether anything survives stripping it.

## Non-circularity requirement

The module **must not** be defined from the covariate list that prompted this test, or the test is
circular. Gene sets are taken **externally and unmodified** from MSigDB
`c5.go.bp.v2024.1.Hs.symbols.gmt` and `c5.go.cc.v2024.1.Hs.symbols.gmt`, already in this repository and
used in §11. Sets fixed here:

- **Primary:** `GOBP_PLASMA_MEMBRANE_REPAIR` — the term §11 flagged with the strongest specificity.
- **Secondary (endolysosomal, pre-specified as one pooled set):** `GOCC_LYSOSOME`, `GOCC_LATE_ENDOSOME`,
  `GOBP_ENDOSOMAL_TRANSPORT`, `GOCC_CAVEOLA`, `GOCC_MEMBRANE_RAFT`.

No gene is added or removed by hand.

## Method

CCLE protein, 375 lines. For every protein, regress out at **line level** (not lineage mean, for power):
the N:C proxy of §27b (mean z of cytosolic RPL/RPS minus nuclear HNRNP/SRSF/SF3B/SMC) and six
proliferation markers (MKI67, TOP2A, MCM2, MCM6, PCNA, MYBL2). Correlate each residualised protein with
residualised MVP by Spearman across lines.

Enrichment of each gene set among MVP's **top 200** correlates, against **200 random gene sets matched
on set size and on mean protein abundance** (deciles), reporting the empirical specificity = fraction of
matched random sets scoring at or above the real set.

## Positive-control gates, both required

1. **Assembly gate.** PARP4 and TEP1 must both remain in MVP's **top 50** residualised correlates. They
   are confirmed physical partners, so if residualisation destroys them it has destroyed real signal and
   the test is **UNINFORMATIVE**.
2. **Complex gate.** Seeding with PSMA1 must recover at least **10 of 25** proteasome subunits in its own
   top 50 after the identical residualisation.

## Primary prediction and kill condition

- **Module survives** if `GOBP_PLASMA_MEMBRANE_REPAIR` reaches empirical specificity **p < 0.05**
  against matched random sets.
- **Kill condition: if specificity p >= 0.05, ledger #41 stays struck and is strengthened from
  "failed to clear a line" to "failed under the one analysis that controls the confound."** I will stop
  re-opening it, and the membrane framing — which is also my own favoured hypothesis H2 from this
  afternoon — is withdrawn as a co-abundance claim.

## Separately, and marked as post-hoc

I will also report the Fisher combination of the two independent pre-registered tests (§13 IP-MS
p = 0.058 and §15 amoeba p = 0.067). **This was not the registered rule**, which required each test to
clear 0.05 on its own. Combining after seeing both results is precisely the flexibility
pre-registration exists to prevent, so it is reported as an observation about what a meta-analysis would
say and **explicitly not** as satisfaction of the original criterion.

## What this cannot do

It cannot establish physical contact — co-abundance is not contact, which is what §13 was for. It can
only say whether the co-abundance association survives the confound that invalidates the newest evidence.
