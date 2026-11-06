# Pre-registration: is MVP developmental scaffolding?

**Date:** 2026-11-06. Tests Graham's "seed / scaffolding you build on and later replace" idea.
Committed before any expression value was read.

## Prediction under the theory
Scaffolding is highest when a structure is being built and falls once it is built. So MVP should
**decline across development**, from embryo toward adult, in most organs.

## Data
Cardoso-Moreira et al. 2019 (E-MTAB-6814), human bulk RNA-seq across 7 organs — brain, cerebellum,
heart, kidney, liver, ovary, testis — from Carnegie stages and early fetal weeks through adulthood.
`Human.RPKM.txt`, sample labels carry organ, stage and sex.

## Statistic
Per organ: Spearman rho between log2(RPKM+1) and developmental stage rank, over genes with RPKM > 1 in
at least a quarter of that organ's samples. Then **MVP's percentile in that organ's genome-wide rho
distribution**. Percentile, not rho, because global trends move every gene.

## Labels
- **DEVELOPMENTAL SCAFFOLD:** MVP at or below the 10th percentile (declines) in at least 5 of 7 organs.
- **RISES WITH MATURATION:** at or above the 90th in at least 5 of 7. Opposite of the theory.
- **NO DEVELOPMENTAL TREND:** anything else. The seed framing is not supported.

## The confound, named in advance
Proliferation falls steeply across development, and anything correlated with cell division will appear
to decline. **If MVP's percentile is indistinguishable from MKI67's and TOP2A's, the decline is the
proliferation program and not evidence for scaffolding.** A scaffold claim requires MVP to decline while
sitting apart from those markers, so both are reported beside it in every organ.

## Gate, before reading MVP
Canonical fetal-to-adult decliners **LIN28A, LIN28B, IGF2BP1** must each sit at or below the 10th
percentile in at least 5 of 7 organs, for at least 2 of the 3. If that fails, the developmental axis is
not being read correctly and the MVP result is uninformative.

## What each result means
- **Scaffold:** the first positive support for the seed idea, and a reason to look at early development
  rather than at disease.
- **No trend:** the scaffolding-as-development framing is wrong, though scaffolding in the physical
  sense — crowding, surface, mechanics — would be untouched, since that predicts no developmental slope.
- **Rises:** points toward a mature, differentiated-tissue role, which is the opposite of the theory.

## Limits
Bulk tissue, so composition changes with age are inseparable from per-cell changes without single-cell
data. Seven organs is a modest number for a 5-of-7 rule. Human developmental samples are precious and
sparsely sampled at the earliest stages, which is exactly where the theory makes its strongest claim.
