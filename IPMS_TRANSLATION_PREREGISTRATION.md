# Pre-registration: does the translation enrichment replicate in a physical-contact instrument?

**Written 2026-11-07, before computing any enrichment on the IP-MS table.** Committed before running
`src/ipms_translation.py`.

## Why

§40 found MVP's co-elution tail specifically enriched for cytoplasmic translation at the 98th percentile
of 150 comparable seeds, with abundant glycolytic and SPFH-family controls unremarkable. #172 recorded
four limits, and this test addresses the one that matters most:

> *"This is one instrument. Everything that died tonight died on replication or on a second instrument,
> and this result has had neither."*

Co-fractionation and co-abundance both measure co-migration or covariation. **Anti-MVP
immunoprecipitation measures what comes down with the particle.** If the translation association is
physical, it should appear there. If it does not, §40 is a property of how vaults sediment, not of what
they are attached to — which is exactly the distinction §38 forced on us for cortical actin.

## Instrument A, primary: human anti-MVP IP-MS

`argon/raw/lodwick_supp_4.xlsx`, sheet `Fig. 5c-d` — the same table and the same parse §13 used, so the
comparison is like for like. Vault interactors are defined exactly as §13 defined them, with no
redefinition: `WT_LFC > 0` and `LWTP > 1.3`.

**Test:** among the WT vault interactors, is `GOBP_CYTOPLASMIC_TRANSLATION` (external, unmodified
MSigDB) enriched against **200 random gene sets matched on set size and on the table's own
`WT_LFC`-independent abundance proxy decile**, drawn from the IP-MS universe rather than from the
genome? Matching inside the instrument's own universe is the point: the question is whether translation
proteins are enriched *among things this experiment could have detected*.

## Positive-control gate

The IP-MS must recover the vault itself. **At least two of MVP, PARP4 and TEP1 must be present in the
table and meet the interactor criteria.** An anti-MVP pulldown that does not return its own bait and at
least one known partner cannot speak to anything else, and the result is **UNINFORMATIVE**.

## Primary prediction and kill condition

- **Replicates** if `GOBP_CYTOPLASMIC_TRANSLATION` reaches specificity p < 0.05 among WT interactors.
- **Kill condition: if it does not, §40 does not replicate in a contact instrument.** We will then record
  that the translation tail is a co-migration property — consistent with a 13 MDa particle assembled on
  and sedimenting with polyribosomes — and **not** evidence of physical association, and #168 and #172
  will be amended to say so.

**Registered expectation: we do not know.** Unlike the last three tests we are not predicting a
direction, and we say so rather than inventing one. A particle synthesised on polyribosomes could
plausibly either retain ribosomal contacts into a pulldown or not, and the IP wash would remove
loosely-associated material either way.

## Instrument B, secondary and descriptive only, no threshold

*Dictyostelium* MVPA TurboID top 60 (`argon/results/test_a2_interactome.json`). **RPL38 sits at rank 9
(log2FC +1.88)**, which we noticed before registering and state here. With n = 60 and cross-species
orthology — where #42 records us producing a meaningless result by matching gene symbols across species
— **no enrichment statistic on this list would be interpretable, and we will not compute one.** Reported
as a single observation.

## Instrument C, secondary and descriptive only, no threshold

BioPlex AP-MS MVP interactions: 15 in HEK293T, 28 in HCT116. We will report how many are cytoplasmic
translation members. With n = 15 and 28 these counts are reported, not tested.

## What this cannot do

An IP cannot distinguish a direct contact from a shared complex, and a wash step removes weak or
transient association regardless of whether it is real in the cell. A negative here therefore bounds the
claim rather than refuting polyribosome association as biology — the published claim that vaults are
assembled on polyribosomes stands either way, since it rests on evidence we have not examined.
