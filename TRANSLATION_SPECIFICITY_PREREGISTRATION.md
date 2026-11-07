# Pre-registration: is MVP's translation-enriched co-elution tail specific to MVP?

**Written 2026-11-07, before computing any seed distribution.** Committed before running
`src/translation_specificity.py`.

## Why

§39 found MVP's sub-threshold CFdb tail enriched 18-fold for `GOBP_CYTOPLASMIC_TRANSLATION`, and
registered the verdict **NOT SPECIFIC** because cortical actin terms also cleared. #168 then noted that
this supplies a competing explanation for #155: if MVP co-elutes with translation machinery, a
cytoskeletal association could follow from **where the particle is synthesised** rather than from what it
does — and the published claim that vaults are assembled on polyribosomes makes that more than idle.

**But #168 rests on an untested premise.** Translation machinery is the most abundant and most strongly
co-eluting material in any lysate. If *every* abundant cytoplasmic protein's score tail is
translation-enriched, then MVP's 18-fold tells us nothing about vaults, and #168 loses its basis.

This is not a method variant of §39 (which #113 forbids). It is the specificity question §39's verdict
left open, asked of the same instrument with a different comparison.

## Method

From `data/raw/cfdb/Homo_sapiens.tsv.gz`, for each seed protein take its **top 200 partners by score**
regardless of precision — identical to §39 — and compute the hypergeometric enrichment of
`GOBP_CYTOPLASMIC_TRANSLATION` (external, unmodified MSigDB) among them, as a fold-enrichment over
expectation.

**Reference distribution:** 150 seed proteins drawn at random from those with at least 5,000 scored
partners, so every seed has a comparable tail to rank. MVP's fold-enrichment is reported as a percentile
of that distribution.

**Named comparators, fixed here:**
- *Expected high:* `RPL7`, `RPS6` — ribosomal proteins, which should be extreme by construction
- *Abundant cytoplasmic, no polyribosome story:* `GAPDH`, `ENO1`, `PKM`, `LDHA`, `ALDOA`
- *SPFH family:* `FLOT1`, `FLOT2`, `STOM` — MVP's own domain family
- *Known complex, non-translational:* `PSMA1`

## Positive-control gates, both required

1. **`RPL7` and `RPS6` must each exceed the 95th percentile** of the random distribution. A ribosomal
   protein whose tail is not translation-enriched would mean the measure does not work.
2. **`PSMA1` must fall below the 90th percentile.** A proteasome seed should not look like a ribosome
   seed; if everything is extreme, the measure has no discrimination and the result is
   **UNINFORMATIVE**.

## Primary prediction and kill condition

- **MVP-specific** if MVP exceeds the **95th percentile** of the 150 random seeds.
- **Kill condition: if MVP falls below the 75th percentile, the translation tail is a generic property of
  abundant cytoplasmic proteins in co-fractionation data, #168 is struck, and §39's observation is
  withdrawn entirely rather than carried as a competing explanation.**
- Between the 75th and 95th is reported as equivocal and promotes nothing.

**Our expectation, registered: we think MVP will be high but not extreme, and that the glycolytic
comparators will also be elevated.** Translation machinery dominates co-fractionation profiles generally.
If that is what we see, the honest conclusion is that #168's mechanism is unsupported even though §39's
numbers were real.

## Secondary, descriptive only

Where the three SPFH-family proteins fall. If MVP is extreme and FLOT1/FLOT2/STOM are not, that is a
point about vaults; if the family behaves alike, it is a point about SPFH proteins. No threshold is
registered.

## What this cannot do

Precision 0.30-0.38 is below the level CFdb's authors report interactions at, so nothing here is called
an interaction. It cannot establish that polyribosome templating causes the tail, only whether the tail
distinguishes MVP from comparable proteins. And a positive result would still be co-elution, which §38
established is not the same as contact.
