# Pre-registration: is the MVP lineage pattern just epithelial identity?

**Written 2026-11-07, after `results/lineage_mvp.json` existed but before any class-level statistic was
computed.** The lineage z-scores are already known to me and are stated in §25; what is *not* known is
how much of their variance tissue class absorbs, which is what this tests.

## Why

§25 found MVP protein high in kidney, CNS, pancreas, gastric and colorectal lines and low in blood,
lymphocyte, uterus, bone and plasma-cell lines. Every functional story one might tell about that
ranking — and I have several — is worthless if the ranking is simply **epithelial versus
non-epithelial**, carrying no information beyond tissue class.

This must be excluded before any functional hypothesis is worth testing, including any proposed by the
second agent, who has been asked the same question blind.

## Classification, fixed here before computing anything

Assigned on standard tissue-of-origin grounds, not on MVP values:

- **epithelial** (14): kidney, pancreas, gastric, colorectal, upper_aerodigestive, skin, urinary_tract,
  lung, ovary, breast, liver, esophagus, prostate, uterus
- **haematopoietic** (3): blood, lymphocyte, plasma_cell
- **mesenchymal** (2): bone, soft_tissue
- **neural** (1): central_nervous_system

`neural` has n = 1 lineage and will not be tested as a group; it is reported descriptively because CNS
is the clearest counterexample to the epithelial reading and I want its position on the record either
way.

## Positive-control gate

The classification must be recoverable from the protein data. **EPCAM, CDH1 or KRT8** must show a mean
z in `epithelial` lineages at least **1.0 higher** than in `haematopoietic` lineages. If none does, the
classification is not resolvable in this matrix and the result is **UNINFORMATIVE**.

## Primary test and prediction

One-way comparison of mean lineage MVP z by class (epithelial vs haematopoietic vs mesenchymal),
weighted equally per lineage, reporting eta-squared.

- **H1 wins — the pattern is tissue class** if class explains **eta-squared >= 0.50** *and* the spread
  of mean MVP z **within** the 14 epithelial lineages is less than **1.0** z.
- **H1 loses — real structure survives within class** if within-epithelial spread is **>= 1.5** z,
  meaning epithelial identity cannot account for kidney (+1.22) sitting far above esophagus (-0.37)
  and prostate (-0.46).
- Intermediate outcomes are reported as partial and no functional hypothesis is promoted on them.

## Kill condition

If H1 wins, then **every functional interpretation of the tissue ranking in this project is withdrawn**,
including the sterol-microdomain and oxidative-load hypotheses I favour, and `PAPER2` experiment 9 is
demoted again to a descriptive survey rather than a test that decides anything.

## What this cannot do

It cannot explain adrenal, which has no cell lines. It cannot establish function. It can only tell us
whether the ranking contains information beyond tissue class.
