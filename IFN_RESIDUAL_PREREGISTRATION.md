# Pre-registration: does anything in MVP's neighbourhood survive removing the interferon axis?

**Written 2026-11-07, before computing any STAT1/IRF9-residualised term statistic.** Committed before
running `src/ifn_residual.py`.

## Why, and whose test this is

§31 found 103 GO terms replicating around MVP, dominated by innate immunity. §35 recorded the external
reviewer's objection, which we accept: **MVP is a documented interferon-gamma-inducible gene, so its top
correlates are the interferon regulon by construction, and we never residualised on the interferon
axis.** Our response at the time — "so I deflated it to shared regulation" — was a verbal move, not a
test. The reviewer specified the test:

> *"Residualise the same five proteomic matrices on STAT1 + IRF9 and rerun the GO replication. Immune
> terms dying, and ruffle/actin surviving, is the discriminative outcome."*

That is the right test and it is not ours. It is registered here with thresholds fixed in advance.

## Method

Identical to §31 in every respect except the covariate set. Per dataset — `brain_cptac_2020`,
`coad_cptac_2019`, `gbm_cptac_2021`, `ucec_cptac_2020`, `ccle_broad_2019`, analysed separately and never
pooled — residualise every protein at sample level on:

- the N:C proxy (mean z of cytosolic RPL/RPS minus nuclear HNRNP/SRSF/SF3B/SMC),
- six proliferation markers,
- **and STAT1 + IRF9**, the interferon-axis addition.

Then rank by Spearman against residualised MVP, test all MSigDB GO BP/CC terms with 10-500 members by
hypergeometric enrichment in MVP's top 200, BH-correct within dataset, and count datasets reaching
q < 0.05. Gene sets external and unmodified. **Replication threshold unchanged: a majority of
gate-passing datasets.**

## Gates, unchanged from §31 plus one addition

1. **Per dataset:** PARP4 within MVP's top 100, and PSMA1 recovering at least 8 of 25 proteasome
   subunits in its own top 50.
2. **Design gate:** the same scan seeded with PSMA1 must still return at least one proteasome term
   replicating in a majority. Residualising on STAT1/IRF9 must not destroy the method's ability to see a
   real complex.
3. **New, and the one that makes this interpretable:** the residualisation must actually remove the
   interferon axis. **TAP1 must fall out of MVP's top 200 in at least three of the gate-passing
   datasets**, or at minimum its rank must worsen in a majority. If STAT1/IRF9 residualisation does not
   displace the canonical interferon target, it has not done its job and the result is **UNINFORMATIVE**.

## Registered predictions, both of them

**Prediction 1:** the immune block largely dies. Antigen processing, cytokine production, inflammatory
response, response to type II interferon and response to bacterium should lose majority replication. If
they do, §31's immune finding was substantially a re-description of the interferon regulon, and we will
say so.

**Prediction 2:** the cortical block survives. `GOCC_RUFFLE` and `GOBP_ACTIN_FILAMENT_ORGANIZATION`
should keep majority replication, because interferon inducibility does not predict them. **This is the
reviewer's prediction, not ours, and we are testing it rather than our own.**

## Outcomes, fixed now

- **Immune dies, cortical survives** → §31 is reframed: MVP's replicating neighbourhood is cortical
  actin/ruffle, and the immune signal was regulon. The cortical block becomes the lead and we had been
  ignoring it.
- **Both die** → MVP has no co-abundance neighbourhood independent of the interferon axis, and §31 is
  withdrawn entirely. Co-abundance is finished on this question for good.
- **Both survive** → the interferon axis does not explain the scan, and the immune block is more than
  shared regulation. This would be the strongest positive result in the project and we would distrust
  it until replicated by someone else.
- **Immune survives, cortical dies** → the opposite of the reviewer's prediction, and we report it as
  such.

## What this cannot do

STAT1 and IRF9 *protein* are imperfect proxies for interferon pathway activity, so this
**under-corrects**; terms that survive may still be regulon. It remains co-abundance, not contact. And
it cannot address the COAD counterexample (§35e), which stands regardless of the outcome here.
