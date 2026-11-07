# Pre-registration: does MVP have co-essential partners?

**Date:** 2026-11-07, before any correlation computed. Claude drafted; Graham stated no predictions.
Prompted by argon's H2a, which correctly identified a blind spot in my ORCS test (§8).

## Why
`RESULTS.md` §8 used **binary** author hit-calls across 878-1,340 screens and found MVP in 9. Binary
calls discard almost all variance. DepMap's **continuous Chronos gene-effect scores** across ~1,100 cell
lines detect partners of *non-essential* complexes, because subtle variation in media, passaging and
mechanical stress perturbs partner genes together. This is the test ORCS could not be.

## Data
DepMap `CRISPRGeneEffect.csv` (figshare 51064667, 428 MB), cell lines x genes. Genes with fewer than 300
scored lines, or zero variance, are dropped.

## Statistic
Pearson correlation of MVP's Chronos vector against every other gene across shared cell lines, then rank.
Benjamini-Hochberg across the genome. Spearman reported as a robustness check.

## Gates, evaluated before reading MVP
1. **Essential-complex gate:** NDUFS2 must recover at least 5 `NDUF*` genes in its top 25.
2. **Non-essential-complex gate (argon's, and the one that matters here):** **CAV1 must recover CAVIN1
   and EHD2 within its top 25 co-essential partners.** CAV1 is near-zero essentiality in most screens, so
   this proves the method sees complexes that binary screens miss.

If gate 2 fails, a null for MVP is reported as uninformative.

## Primary test
Does MVP have **any** gene passing FDR q < 0.05?

- **HAS CO-ESSENTIAL PARTNERS:** at least one gene at q < 0.05. Report the top 25 and whether PARP4,
  TEP1, ANXA2 or S100A10 are among them.
- **NO CO-ESSENTIAL PARTNERS:** none. Given that CAV1 passes, this would mean MVP loss does not
  co-vary in fitness consequence with any gene in 1,100 genetic backgrounds — a strong null, and the
  cleanest statement yet of the dispensability in #22.

## Secondary
GO enrichment of MVP's top 100 with the same specificity logic as §11 (matched random queries), and the
ranks of the four-protein core from #40.

## Kill condition
If the four-protein core (PARP4, TEP1, ANXA2, S100A10) shows **no** co-essentiality with MVP while CAV1's
complex does, then #40's core is a *physical/abundance* association with no fitness coupling — which
would be informative rather than fatal, and must be stated plainly rather than omitted.

## Limits
Cancer cell lines in culture, the same setting that gave zero growth phenotype in §8. Co-essentiality
detects shared fitness consequence, not contact. A gene with no fitness effect in any line has no signal
to correlate, so a null here partly restates §8 rather than testing something wholly new.
