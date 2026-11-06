# Pre-registration: what does MVP protein travel with?

**Date:** 2026-11-06. Drafted by Claude at Graham's request; Graham stated no numeric predictions.
Committed before any protein value was read. Only the *list* of available profiles was inspected.

## Why

Everything run today measured RNA. MVP is a 100,000-copy protein assembly whose protein may be
long-lived, so mRNA is a poor proxy and every negative so far carries that caveat. Proteins that sit
in a complex co-vary in **protein abundance** across samples far more tightly than their transcripts
do. This asks the "is the vault a unit" question with an independent molecule and method.

It also repairs the known blind spot of the co-loss test (`RESULTS.md` §9): a partner set of three or
four proteins could never enrich a GO term, but it would show up as a tight co-abundance cluster.

## Data

cBioPortal mass-spectrometry `protein_quantification` profiles, every study with at least 50 samples.
Candidates seen in the profile listing: brain, brca, coad, gbm, luad, lusc, paad, ucec (CPTAC), ov and
brca/coadread TCGA CPTAC, mng_utoronto. One sample per patient, tumor samples.

## Statistic

Per cohort: Spearman rho between MVP and every other protein across samples. Combine across cohorts by
Fisher z and random-effects REML with Hartung-Knapp (the estimator already used in `src/models.py`).

**Universe:** proteins measured in at least 50% of samples in a cohort, and present in at least 3 cohorts.

**Primary A — is the vault a unit?** The pooled rank of **TEP1** and **PARP4** in MVP's co-abundance
ranking. These two sit physically inside the particle. The co-loss test could not resolve them because
their ortholog groups are too coarse; protein co-abundance has no such problem.

- **UNIT:** both in the top 1% of the ranking.
- **PARTIAL:** exactly one in the top 1%.
- **NOT A UNIT:** neither in the top 5%.
- **UNRESOLVED:** anything else, or either protein absent from the universe.

**Primary B — is there any coherent partner set?** MSigDB GO BP and CC enrichment of MVP's top 100
co-abundant proteins, hypergeometric, Benjamini-Hochberg, terms of 10 to 500 members.
Specificity by 200 random query proteins matched on measurement frequency (±10%) and on median
absolute correlation (±0.05): report the fraction of matched queries that also hit each term.
**MODULE LEAD** needs q < 0.05 and fewer than 5% of matched queries hitting that term; otherwise
**NON-SPECIFIC** or **NO MODULE**, as in the co-loss test.

## Gate, evaluated before reading MVP

Control proteins must recover their own complexes: **PSMA1** (proteasome), **NDUFS2** (complex I),
**RPL7** (ribosome). For at least 2 of 3, at least 5 of the top 20 co-abundant proteins must belong to
the same complex by symbol family (PSM*, NDUF*, RPL*/RPS*). If that fails, the method cannot see
complexes here and an MVP null is reported as uninformative.

## Confound, named in advance

Global technical and compositional structure (tumor purity, stromal content, batch) inflates
correlations between unrelated proteins. **Primary is raw Spearman; the named sensitivity analysis
removes the first 3 principal components of each cohort's protein matrix before correlating.**
Conclusions must agree across both. If they disagree, the raw result is reported as composition-driven.

## What each result would mean

- **UNIT:** the vault behaves as one assembly, and the §9 co-loss null is a resolution artifact.
- **NOT A UNIT:** the shell and its contents are regulated separately — the strongest evidence yet for
  the chassis reading, arrived at from protein data rather than from argument.
- **MODULE LEAD:** a specific protein neighborhood for MVP, which is the thing forty years of lumen-first
  searching has not produced. It would be a correlation in tumor tissue, not a demonstrated interaction.
- **NO MODULE:** MVP protein has no tight neighbors, consistent with a self-contained particle.

## Limits

Tumor tissue only, so normal-tissue biology is not represented. Mass spectrometry under-samples
low-abundance proteins, and TEP1 (~290 kDa, hard to detect) may simply be absent. Co-abundance is
correlation, not interaction. Cohorts differ in quantification method (ratio vs intensity), which the
per-cohort standardization and rank statistic partly absorb.
