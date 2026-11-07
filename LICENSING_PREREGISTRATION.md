# Pre-registration: does argon's AHR/STAT1-vs-EZH2 licensing model survive the confound argon itself found?

**Written 2026-11-07, before computing any residualised correlation for these genes.** Protein
availability was checked (counts only, no values). Committed before running `src/licensing.py`.

## The hypothesis being tested

Argon's H2 (#103), the only mechanism anyone has offered for a standing positive (#19): resting MVP
level is set by **tonic AHR plus basal STAT1/IRF1** in barrier epithelia and **silenced by EZH2/PRC2**
in haematolymphoid and neuroendocrine lineages. That would explain the paradox we recorded and never
accounted for — MVP sits at the 95th genome percentile for interferon coupling, yet blood and lymphocyte
are the two **lowest** CCLE lineages.

Its supporting correlations were lineage-mean protein: **AHR +0.542, STAT1 +0.641, TAP1 +0.820,
EZH2 −0.756.**

## Why those numbers are suspect, stated before testing

§27b established that a housekeeping nuclear-to-cytoplasmic proxy alone explains **R² ≈ 0.52** of
lineage-mean MVP variance, and that cytosolic ribosomal proteins correlate **+0.83 to +0.85** with it.
The proxy is *cytosolic minus nuclear*.

**MVP is cytoplasmic. EZH2 is nuclear.** A cytoplasmic protein and a nuclear protein will anti-correlate
through that proxy **by construction**, with no biology involved. So EZH2's −0.756 is a prime candidate
for pure artefact, and the same confound inflates any cytoplasmic covariate upward.

This is the confound argon found. Applying it to argon's own hypothesis is the point of this test.

## Method

CCLE protein, 375 lines. Residualise every protein at line level on the N:C proxy (mean z of cytosolic
RPL/RPS minus nuclear HNRNP/SRSF/SF3B/SMC) plus six proliferation markers, exactly as §28. Spearman
against residualised MVP across lines, reported with raw correlations side by side so the shift is
visible.

Covariates tested: AHR, ARNT, STAT1, STAT2, IRF9, TAP1, TAP2, B2M, SP1 (all 366-375 lines), EZH2, EED,
SUZ12 (375). IRF1 (97), CYP1A1 (36) and NLRC5 (36) are reported but carry no registered threshold
because of coverage; TIPARP and CIITA are absent.

## Positive-control gate, taken from argon's own specification

**STAT1 must track TAP1 at Spearman rho > 0.6 after residualisation.** If the interferon axis does not
hold together in the residualised data, nothing here can speak to MVP's relation to it, and the result
is **UNINFORMATIVE**.

## Primary test A: does the activating arm survive?

- **Survives** if at least two of AHR, STAT1, TAP1, IRF9 keep rho > 0.25 with MVP after residualisation.
- **Does not survive** if all fall below 0.15.

**Prediction:** the STAT1/TAP1/IRF9 interferon arm survives, because MVP is a genuinely
interferon-gamma-inducible gene and that is independent of compartment. **AHR I expect to weaken
substantially**, because its reported +0.542 has no mechanism behind it in this dataset beyond
covariation.

## Primary test B: is EZH2's negative correlation anything more than nuclear compartment?

Compare MVP's residualised rho with EZH2 against the distribution of MVP's residualised rho with **200
size-matched random proteins drawn from `GOCC_NUCLEUS`** (external, unmodified MSigDB).

- **EZH2-specific silencing supported** if EZH2 sits below the 5th percentile of that nuclear
  distribution.
- **Compartment artefact** if EZH2 sits inside the bulk of it.

**Prediction: artefact.** I expect EZH2 to be unremarkable among nuclear proteins once the proxy is
removed, and the PRC2 partners EED and SUZ12 are reported alongside as a coherence check.

## Kill condition for argon's H2

Gate passes, the activating arm fails test A, **and** EZH2 is indistinguishable from generic nuclear
proteins in test B. That would leave the licensing model with no correlational support in the one
dataset where it was proposed, and #103 would be struck.

## What this cannot do

It tests only the **correlational premise** at protein level. It cannot test causality, promoter
H3K27me3, DNA methylation, or response to EZH2 inhibition or AHR antagonism — the perturbation arms
argon specified and which need GEO/ENCODE data not held here. **A pass here is not confirmation of the
model; a fail removes its stated evidence.** Protein is also a poor readout for a transcriptional
mechanism, and that limitation is registered here rather than raised afterwards.
