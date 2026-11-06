# Pre-registration: does MVP partition with the chronic interferon program?

**Date:** 2026-11-06. Committed to git before any MVP expression value, in any dataset, was viewed.

**Authorship disclosure:** drafted by Claude (Opus 5.5) on Graham's behalf, deriving the hypothesis
and outcome table from `vault-partition-analysis-plan.md` §1. Graham did not separately state these
numbers. He may add a dated dissent below the line at the end, but nothing above it changes.

## The §1 block

```
Date: 2026-11-06
Primary prediction: within malignant cells, MVP co-varies with the chronic set (ISG.RS)
  more than with the acute set (IFNG.GS), after adjustment for each other.
Predicted sign and relative magnitude of β(ISG.RS) vs β(IFNG.GS):
  β(ISG.RS) > 0, β(IFNG.GS) ≈ 0 or smaller, Δ = β(ISG.RS) − β(IFNG.GS) ≥ +0.10 (standardized).
What result would make me abandon the containment layer:
  Its only prediction testable here is anti-correlation with both sets (vaults suppressing
  sensing). That prediction is abandoned if single-cell outcome is CHRONIC or ACUTE, i.e. MVP
  rises with an interferon program within malignant cells. This does not refute containment as a
  physical function. The plan §6 limit stands: this test cannot address containment directly.
What result would make me abandon the signaling-brake layer:
  Single-cell outcome of ACUTE, NEITHER, or ANTI. Also: CHRONIC in bulk but not in single cell.
Decision rule for "no effect":
  |β| < 0.10 standardized, or the 95% CI includes 0.
```

## Primary estimand (bulk screen)

Per cohort, pre-treatment samples only, one sample per patient:

`z(MVP) ~ z(ISG.RS) + z(IFNG.GS) + purity_proxy + myeloid + lymphoid`

- All signature scores exclude MVP. Enforced by an assertion that aborts the run.
- Score = mean of z-scored log2(TPM+1) (or the cohort's closest available unit) across members.
- Pooled across ICB cohorts by random-effects meta-analysis (REML with Hartung-Knapp CIs).
- The primary quantity is **Δ = β(ISG.RS) − β(IFNG.GS)** with its 95% CI, using the within-model
  covariance of the two coefficients.

## Outcome labels

Applied identically to the bulk pool and to the single-cell test.

| Label | Rule |
|---|---|
| CHRONIC | β(ISG.RS) ≥ +0.10 with CI excluding 0, **and** Δ CI excludes 0 with Δ > 0 |
| ACUTE | β(IFNG.GS) ≥ +0.10 with CI excluding 0, **and** Δ CI excludes 0 with Δ < 0 |
| ANTI | both β ≤ −0.10, both CIs excluding 0 |
| NEITHER | both β fail the no-effect rule above |
| BOTH/UNRESOLVED | anything else, including positive on both with Δ CI spanning 0 |

## Calibration controls (added to the plan; the plan had none)

Both signatures are interferon-driven but differ in compartment: IFNG.GS is expected to be more
immune-derived than ISG.RS. So a generic tumor-expressed gene could read as "chronic" for reasons
that have nothing to do with MVP. A raw Δ cannot distinguish these, hence:

1. **Genome-wide null.** Fit the identical model to every expressed gene, per cohort. Report MVP's
   percentile in the genome-wide Δ distribution. Interpreted as specific only at ≥ 90th percentile
   (or ≤ 10th for ACUTE).
2. **Held-out members.** Each signature member, scored against its signature with itself removed,
   gives the Δ distribution a true chronic gene and a true acute gene produce. Report where MVP
   falls relative to both.

A CHRONIC label that misses the 90th percentile is reported as "CHRONIC, not specific."

## Single-cell test (what makes the claim)

- Datasets: Yanagawa/Dubinett pulmonary nodules and Sinjab/Kadara multiregion LUAD if publicly
  obtainable. If one is not, substitute the largest public LUAD scRNA-seq set with malignant-cell
  labels, and say so.
- Compartment: malignant epithelial cells per the authors' labels. Myeloid analyzed separately and
  never pooled with malignant.
- Signature genes not detected in ≥ 1% of malignant cells are dropped from that compartment's score,
  and the kept and dropped lists are reported. This is necessary because IFNG.GS holds lymphocyte
  genes that malignant cells do not express.
- Unit of inference: **patient**. Within-patient correlation of MVP against each score is computed
  on normalized expression, then combined across patients by random-effects meta-analysis. Cells are
  never treated as independent samples. Patient-level pseudobulk is reported as the second view.
- Patients with fewer than 50 malignant cells are excluded.
- The genome-wide null applies here too, against the malignant-expressed gene universe.

## Decision hierarchy

1. Bulk label is the screen. Single-cell label is the verdict.
2. Bulk CHRONIC and single-cell CHRONIC, specific: "MVP belongs to the chronic program."
3. Bulk CHRONIC, single-cell anything else: not a finding of membership. Bulk signal attributed to
   composition.
4. Single-cell data unusable: "suggestive, unresolved," whatever the bulk says.

## Epigenetic check

Qiu 2023 lookup, if data is deposited. Positive = gain of H3K4me1 and/or ATAC signal at the Mvp
promoter or a linked element in ICB-resistant vs. parental cells, comparable to positive control
ISGs (Oas1 family, Ifit family) and above a random-gene background. Its model is mouse, so this is
reported as supporting context and does not override the human single-cell verdict in either direction.

## Everything else is exploratory

ICB response association, likelihood-ratio test of MVP beyond ISG.RS, ISG.RS/IFNG.GS ratio, tertile
stratification, TCGA tumor types (LUAD, LUSC, SKCM, PAAD, LIHC, THCA), ssGSEA robustness. Labeled as
exploratory, Benjamini-Hochberg across the set, and not promoted to the headline. Exception: the ratio
and ssGSEA are named checks on the primary. If they disagree with it, the write-up says so.

## Change log rule

Deviations forced by data (a missing cohort, a missing covariate) go in `DEVIATIONS.md` with the date
and the reason, written before the affected result is viewed wherever possible. The file above the
line below is frozen.

---
