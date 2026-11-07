# Pre-registration: is MVP's sub-threshold co-elution neighbourhood translation machinery?

**Written 2026-11-07, before computing any enrichment statistic on this ranking.** Committed before
running `src/cfdb_subthreshold.py`.

## Why this test and not another co-abundance test

#165 records the project-level finding: co-abundance has been run eight times on the neighbourhood
question and **never once been corroborated by a contact instrument**. MVP's co-abundance correlates
report cellular state. Running a ninth co-abundance test would repeat the error.

This test uses the instrument that **does** report association — native co-fractionation — and asks
about material we discarded. §33 thresholded CFdb at precision >= 0.50, which left MVP with one partner.
§35d reported that MVP's ranks 2-12 by score are **ZNF598, RPL8, RPL30, EIF3A, EIF3C, UPF1, GIGYF2,
FAM120A, ZC3HAV1** at precision 0.30-0.38 — translation, ribosome-quality-control and RNA-handling
proteins, none of them hypothesised by us.

It matters that this is independent of the lesson in #165: it is co-elution data, so a positive here
would be the first contact-instrument support for any neighbourhood in this project.

## Full disclosure of what has already been seen

**We have seen eleven gene names from ranks 2-12 and their scores. We have not computed any enrichment
statistic on this ranking.** That is the honest state, and it is why the test below is specified over
MVP's top 200 by score rather than over the eleven names, and why translation terms are tested alongside
pre-committed comparators rather than alone.

## Method

From `data/raw/cfdb/Homo_sapiens.tsv.gz`, take MVP's **top 200 partners by score** regardless of
precision, from its 10,614 scored pairs. Test GO enrichment against **200 random sets matched on CFdb
degree decile and on set size**, degree being the right matching variable in a graph.

## Term panel, fixed here

- **Under test (translation/RNA):** `GOBP_TRANSLATION`, `GOCC_RIBOSOME`,
  `GOBP_CYTOPLASMIC_TRANSLATION`, `GOCC_RIBONUCLEOPROTEIN_COMPLEX`, `GOBP_RNA_CATABOLIC_PROCESS`
- **Comparators, pre-committed (the three hypotheses that died):** `GOBP_ACTIN_FILAMENT_ORGANIZATION`,
  `GOCC_RUFFLE`, `GOBP_PLASMA_MEMBRANE_REPAIR`, `GOBP_INFLAMMATORY_RESPONSE`
- **Negative control:** `GOCC_MITOCHONDRION` — abundant, large, and not expected

## Positive-control gate

The identical procedure seeded with **PSMA1** must enrich `GOCC_PROTEASOME_COMPLEX` at specificity
p < 0.05, and seeded with **RPL7** must enrich `GOCC_RIBOSOME`. Both are run on their own top 200 by
score with the same degree matching. If a known complex does not come back, sub-threshold CFdb ranking
carries no usable signal and the result is **UNINFORMATIVE**.

## Primary prediction and outcomes, fixed now

**Prediction: translation and RNA terms clear p < 0.05 and the three dead hypotheses do not.** If so,
MVP's co-elution neighbourhood below the reporting threshold is translation machinery, which would be
the first neighbourhood in this project supported by a contact instrument, and it would align with the
published observation that vaults are assembled on polyribosomes and carry a small RNA.

- **Kill condition:** no translation or RNA term clears while the gates pass. The §35d observation is
  then eleven gene names at the top of a long tail with no statistical support, and we drop it rather
  than carry it as a lead.
- **If the actin or immune comparators also clear**, the result is not specific and we report it as a
  generic property of MVP's score tail rather than as a translation finding.
- **If `GOCC_MITOCHONDRION` clears**, the degree matching is inadequate and the whole panel is
  uninterpretable.

## What this cannot do

Precision 0.30-0.38 is below the level at which CFdb's authors report interactions, so these are not
high-confidence edges and we will not describe them as interactions. Co-elution at equal size is not
contact. And ribosomal and translation proteins are abundant and numerous, which is why matching is on
degree and why the mitochondrion control is included.
