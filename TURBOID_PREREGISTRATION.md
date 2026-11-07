# Pre-registration: is the vault a PARP4-proximal assembly, and does its neighbourhood survive a contact instrument?

**Written 2026-11-07, before reading a single value from the PARP4 sheet.** Columns were inspected on
the PARP1 sheet only, deliberately, so no MVP number in the bait of interest had been seen. Committed
before running `src/turboid.py`.

## Why this dataset and not another co-abundance run

Co-abundance has failed the neighbourhood question **five times** (§11 nomination, §13 IP-MS p = 0.058,
§15 amoeba p = 0.067, §30 non-replication, §31 1-of-5 in the unbiased scan). The honest conclusion is
that it is the wrong instrument: it cannot separate physical association from shared transcriptional
regulation, which is exactly the deflation recorded in #123.

Zheng et al. 2025 (*Sci Data* 12:405, PMID 40058474, Figshare 10.6084/m9.figshare.27906234) is a
different instrument. `V5-TurboID` biotinylates neighbours **covalently, inside living cells, before
lysis**, so it does not depend on a complex surviving detergent. Critically it labels **all 17 human
PARP family members in one batch**, giving **16 matched non-vault baits as a built-in specificity
background** — a control structure nothing else available to us has.

Data: `data/raw/zheng2025/Supplementary_Table_2.xlsx`, 17 bait sheets, each with per-prey
`Log2(FoldChange)` against a TurboID-vector control and a `P.value`, from triplicates.

## Positive-control gate, required before any MVP number is interpreted

TurboID of PARP4 must recover PARP4's own known biology:

1. **Self-labelling.** `PARP4` must appear as enriched in its own sheet (`Log2(FoldChange) > 1` and
   `P.value < 0.05`), confirming the construct labels its own locus.
2. **Family specificity.** At least **12 of the 17** baits must enrich their own gene symbol by the same
   rule, confirming the batch works generally and the 16-bait background is usable.

If either fails the dataset cannot support the inference and the result is **UNINFORMATIVE**.

## Primary test and prediction

**Is MVP a PARP4-proximal protein, specifically?**

- **Enriched** if MVP has `Log2(FoldChange) > 1` and `P.value < 0.05` in the PARP4 sheet.
- **Specific** if MVP's PARP4 fold-change exceeds its fold-change in at least **14 of the 16** other
  PARP baits where it is measured.

**Prediction, committed:** I expect MVP to be enriched and specific. This is the one claim in the
project with support from co-abundance in 13 cohorts, CCLE, all 8 CPTAC cohorts, anti-MVP IP-MS and
*Dictyostelium* proximity labelling. **If MVP is not PARP4-proximal here, the single most robust finding
in this work is in serious trouble**, and that would matter far more than anything else this test could
return.

**Kill condition:** MVP absent or not enriched in the PARP4 sheet while the gates pass. That would
contradict §13, §28, §30 and #116 simultaneously and must be reported as such, not explained away.

## Secondary test, registered now: TEP1

Same rule for `TEP1`. TEP1 is sparsely measured in proteomics generally, so absence is uninformative;
only a present-and-not-enriched result counts against it.

## Tertiary test: does the membrane-repair neighbourhood appear in a contact instrument?

For the five previously favoured GO terms (`GOBP_PLASMA_MEMBRANE_REPAIR`, `GOCC_CAVEOLA`,
`GOBP_PLASMA_MEMBRANE_ORGANIZATION`, `GOCC_LATE_ENDOSOME`, `GOBP_ENDOSOMAL_TRANSPORT`) and the
innate-immune terms that replicated in §31 (`GOBP_INFLAMMATORY_RESPONSE`, `GOBP_RESPONSE_TO_BACTERIUM`,
`GOCC_RUFFLE`, `GOBP_ANTIGEN_PROCESSING_AND_PRESENTATION`), test enrichment among PARP4-proximal
proteins against **200 size- and abundance-matched random sets**, as in §28.

**This is the decisive test for both hypotheses**, because it asks about physical proximity rather than
covariation. A term failing here after failing co-abundance replication is finished. A term passing here
would be the first contact-level support any of them has had.

Named proteins reported individually whether flattering or not: ANXA2, S100A10, EHD2, EHD4, CAPN2, MYOF,
AHNAK, IQGAP1, CD63, OPTN, VPS35, FLOT1, FLOT2.

## What this cannot do

Proximity labelling reports a ~10-20 nm neighbourhood, not binary contact, and it is one cell line
(HEK293T) with modest endogenous MVP. Lumenally encapsulated PARP4 can only biotinylate neighbours
reachable from inside the particle or during assembly, so **a negative for external membrane proteins
is expected under the sealed-shell model and must not be read as refuting membrane association in
intact cells.** That asymmetry is stated here, in advance, so it cannot be invoked selectively later.
