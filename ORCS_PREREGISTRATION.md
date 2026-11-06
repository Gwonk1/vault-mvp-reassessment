# Pre-registration: when does losing MVP matter? (BioGRID ORCS)

**Date:** 2026-11-06. Committed before any MVP, TEP1 or PARP4 row in ORCS was read. Only the screen index
(no gene data) was examined. Drafted by Claude at Graham's request. Graham stated no numeric predictions.

## Question

Across published CRISPR loss-of-function screens, is there a class of conditions where losing MVP
changes cell fitness or phenotype more than expected for a gene with its overall hit rate?

## Prior

Expected outcome: NO SIGNAL. Vault-knockout mice are viable and earlier work reports little in-culture
phenotype. Classes the vault framework names in advance: **genotoxic, virus, bacteria, toxin,
immune_killing, oxidative_mito**. A hit in any other class is still reported, labeled as unpredicted.

## Data

BioGRID ORCS 2.0.18, human. Universe: Knockout or Inhibition libraries, high throughput, at least 10,000
genes scored, at least one hit (`src/orcs_classes.py`). Activation screens are excluded because they ask a
different question. Hits-only screens are excluded because a missing gene there cannot count as a non-hit.
Any MVP row in an excluded screen is listed descriptively, outside all statistics.

**Hit** = the authors' `HIT=YES`. A gene absent from a screen is untested for that screen.

## Statistic

1. Paper is the unit, because one paper can contribute dozens of related screens. Per paper within a class,
   take the fraction of tested screens in which the gene is a hit.
2. Class score = mean of those fractions across the class's papers.
3. Rest score = the same quantity using all screens outside that class.
4. Empirical p = position of the gene's class score among the 1,000 genes nearest in rest score, as
   (1 + number with score at or above the gene's) / 1001. This controls for genes that hit everywhere.
5. Benjamini-Hochberg across the gene's testable classes. A class is testable with at least 3 papers.

## Labels

- **CONDITION SIGNAL:** adjusted p < 0.05, plus hits in at least 3 papers and at least 2 cell lines.
- **FREQUENT FLIER:** at or above the 95th genome percentile for overall hit rate and no condition signal.
  Reads as generic screen noise or generic fitness.
- **NO SIGNAL:** neither of those.

## Gates

**Pipeline controls, evaluated before reading MVP.** At least 2 of 3 known genes must give a condition signal
in each class: genotoxic FANCD2, FANCA, XRCC1; virus ACE2, SLC35B2, EXT1; immune_killing JAK1, IFNGR1, B2M. If
a class fails, an MVP null in that class is reported as uninformative.

**False-positive rate.** Report the fraction of all genes that receive a condition signal. An MVP signal is
judged against that base rate.

**Partners.** TEP1 and PARP4, the other vault proteins, run through the same test. A vault function should
show agreement, though both have non-vault roles. Disagreement is reported.

## What each result would mean

- **CONDITION SIGNAL in a named class:** a lead for a specific stress to test in a lab, with direction read
  from the individual screens afterward. Correlates nothing with mechanism, and it does not establish function.
- **Unpredicted class signal:** a lead with lower prior.
- **NO SIGNAL:** MVP loss is not a strong, recurring cell-autonomous phenotype in pooled screens of mostly
  proliferating cancer lines. Adds modest support to "dispensable under these conditions." It cannot exclude
  subtle effects, redundancy, primary-cell or organism-level roles, or phenotypes that pooled growth readouts miss.

## Known limits, stated in advance

Interferon has 1 paper and proteotoxic 2, so **this database cannot directly test interferon**. Hit direction
is not coded uniformly and is read by hand after the verdict. Thresholds vary by author. No check is made that
MVP is expressed in each line.
