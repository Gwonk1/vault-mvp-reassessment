# Pre-registration: is MVP a passenger marker of the drug-tolerant persister state?

**Date:** 2026-11-06. Drafted by Claude at Graham's request. Graham stated no numeric predictions.
Committed before any MVP value in any persister dataset was read. Dataset structure (cell lines,
drugs, timepoints, file layout) was inspected first; no expression values were.

## Why this question

High MVP/LRP in a biopsy has predicted chemotherapy failure since the 1990s, and in thirty years no
mechanism has been demonstrated. The sink model (the barrel sequesters drug) has no regulated uptake
behind it. Two results from today make an alternative worth testing:

- MVP rises with interferon state in malignant cells but is not selective between interferon programs
  (`RESULTS.md` §3).
- Knocking MVP out does not recur as a drug-survival signal in 1,350 CRISPR screens, and it has zero
  hits in 878 growth screens (`RESULTS.md` §8).

So MVP may mark a cell **state** that survives drug rather than causing survival. Drug-tolerant
persisters are the named version of that state: slow-cycling, stress-adapted, often interferon-high.
If MVP is induced in persisters while its loss changes nothing, the thirty-year biomarker is a
passenger, and that is a different claim from anything in the vault literature.

## Data

**Primary — GSE150949** (Oren et al., Watermelon). 7 models across 4 cancer types: PC9, HCC827
(EGFR), BT474, EFM192A (HER2), A375, COLO858 (BRAF), HT29 (colorectal), each treated 10 days with a
clinically relevant kinase inhibitor. Unit of inference is the **model**, not the cell.

**Replication — GSE149383** (Aissa et al.). PC9 erlotinib time course (D0, D1, D2, D4, D9, D11, D19)
plus M14 melanoma vemurafenib (D0, D3). Different lab, different drugs, different protocol.

Cells: authors' own labels for treatment and timepoint. Normalization: log1p of CP10K per cell.

## Primary estimand

Per model: **Δ = mean log1p(CP10K) in drug-treated persisters − mean in untreated day 0**, computed
per gene, plus **MVP's percentile in that model's genome-wide Δ distribution**, over genes detected in
at least 5% of cells in that model.

Percentile is the quantity that counts, not raw Δ, because global shifts in library composition move
every gene.

## Labels (primary dataset)

- **PERSISTER MARKER:** MVP at or above the 90th percentile of Δ in at least 5 of 7 models.
- **NOT A PERSISTER MARKER:** fewer than 5 of 7, including any result where MVP falls.
- **DOWN IN PERSISTERS:** at or below the 10th percentile in at least 5 of 7 models.

Replication is reported separately and does not change the primary label.

## The interferon control (required, not optional)

Persister programs are reported to be interferon-enriched, and MVP is interferon-inducible. Without
this control a positive result is uninterpretable, the same confound as the partition test.

Per model, score each cell for HALLMARK_INTERFERON_GAMMA_RESPONSE and
HALLMARK_INTERFERON_ALPHA_RESPONSE **with MVP removed** (`src/scores.py` asserts and aborts on a leak),
then recompute Δ for every gene from the residual of a per-cell regression on both scores.

- **INTERFERON-EXPLAINED:** MVP meets PERSISTER MARKER on raw Δ but drops below the 90th percentile
  on residualized Δ.
- **INDEPENDENT OF INTERFERON:** meets it on both.

## Comparators, fixed in advance

- **Efflux contrast:** ABCB1, ABCG2, ABCC1. If MVP is a drug-handling mechanism of the kind the
  oncology literature assumes, it should behave like these. If it behaves unlike them and like the
  interferon genes instead, that is the passenger reading.
- **Interferon contrast:** IFIT1, ISG15, STAT1, B2M.
- **Named persister markers:** AXL, NGFR, ALDH1A3, KDM5A. Reported for context only; the literature
  does not promise these in every model, so they are not a gate.

## Gate (pipeline must prove it can see the persister state)

Persisters are largely non-cycling, so proliferation genes must fall. **MKI67, TOP2A and CCNB1 must
each sit at or below the 10th percentile of Δ in at least 5 of 7 models.** If that fails, the drug
response is not detectable in these labels and any MVP result here is reported as uninformative.

## The causal leg (already run, reused without refitting)

From `results/orcs_final.json`: MVP is a hit in 9 of 1,340 screens, 26th percentile overall, with no
condition signal in any class. For this question the relevant subset is screens whose condition is a
targeted kinase inhibitor matching these drug classes; MVP's hit status there is reported descriptively.
No new statistic is computed from ORCS, and its pre-registered limits stand, including that the
genotoxic and immune-killing classes failed their control gates.

## Interpretation, fixed in advance

| Expression | Causal (ORCS) | Reading |
|---|---|---|
| Induced in persisters | No recurring knockout signal | **Passenger.** Supports MVP as a marker of a surviving state rather than a cause of survival. Does not prove the sink model false; it removes its main support. |
| Induced | Knockout sensitizes in matched drugs | Real mechanism. The reframe is wrong. |
| Not induced | — | The persister framing is wrong for MVP, and the thirty-year biomarker needs some other explanation. |
| Down in persisters | — | Strongly against both the sink model and the passenger reading. |

## Limits, stated in advance

Cell lines in culture, kinase inhibitors rather than the cytotoxic chemotherapies the LRP biomarker was
built on, so this tests the state claim and not the clinical association directly. Persister definitions
differ between labs. Single-cell dropout affects a moderately expressed gene like MVP. A positive result
would be a correlation in a model system, not a demonstration that MVP does nothing in patients.
