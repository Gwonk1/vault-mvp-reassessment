# Pre-registration: does the membrane-repair module replicate in independent tumour proteomics, and is it specific to MVP?

**Written 2026-11-07, before computing anything in any tumour cohort.** Committed before running
`src/module_replication.py`.

## Why this and not another EMT variant

§28 found the membrane-repair and caveolar gene sets enriched around MVP in CCLE cell lines at
matched-random specificity p = 0.000, after residualising on cytoplasmic mass and proliferation. §29's
EMT control failed its own validity gate, and **#113 committed us to stop re-running that control** —
adjusting a method until a finding passes is what pre-registration exists to prevent.

The legitimate next moves are not method variants. They are:

- **replication in independent data**, and
- **specificity against the obvious alternative explanation** — that this is a generic property of
  SPFH-domain proteins rather than anything about vaults.

Both are registered here.

## Data

Tumour proteomics cohorts already in this repository under `data/processed/prot/`, independent of CCLE
cell lines: `brain_cptac_2020`, `brca_cptac_2020`, `coad_cptac_2019`, `gbm_cptac_2021`,
`luad_cptac_2020`, `lusc_cptac_2021`, plus any other `*_cptac_*` cohort present. **Cohorts are analysed
separately and never pooled**, because pooling would reintroduce the cross-tissue composition confound
that §22 and §27 both turned on.

Minimum 50 samples and 2,000 measured proteins per cohort, the same filter used in §13.

## Method, identical to §28 except for the dataset

Per cohort: residualise every protein at sample level on the N:C proxy (mean z of cytosolic RPL/RPS
minus nuclear HNRNP/SRSF/SF3B/SMC) plus available proliferation markers, Spearman-correlate each
residualised protein against residualised MVP, and test enrichment of the **same externally defined,
unmodified MSigDB sets** among MVP's top 200, against 200 size- and abundance-matched random sets.

Gene sets are unchanged from §28: `GOBP_PLASMA_MEMBRANE_REPAIR` (primary), plus `GOCC_CAVEOLA`,
`GOBP_PLASMA_MEMBRANE_ORGANIZATION`, `GOCC_LATE_ENDOSOME`, `GOBP_ENDOSOMAL_TRANSPORT` as the registered
secondary and negative-control terms. **No set is added, removed or redefined.**

## Positive-control gates, per cohort

1. **Assembly.** PARP4 must be within MVP's top 100 residualised correlates in that cohort. TEP1 is
   **not** required, because §28 established it is sparsely measured; requiring it is what made run 1 of
   §28 uninformative on a technicality.
2. **Complex.** PSMA1 must recover at least 8 of 25 proteasome subunits in its own top 50 in that
   cohort.

A cohort failing either gate is reported **UNINFORMATIVE and excluded from the replication count**, not
silently dropped.

## Primary prediction and kill condition

Of the gate-passing cohorts, count those where `GOBP_PLASMA_MEMBRANE_REPAIR` reaches specificity
p < 0.05.

- **Replicates** if it clears 0.05 in a **majority** of gate-passing cohorts.
- **Kill condition: if it clears 0.05 in fewer than one third of gate-passing cohorts, §28 is a
  cell-line-specific result and ledger #41 is struck for the third time** — this time on independent
  data rather than on a method variant. My own favoured hypothesis goes with it.
- Between one third and one half is reported as **partial replication**, and #41 is recorded as
  unresolved rather than reversed.

## Secondary test, registered now: is this specific to MVP?

MVP's conserved shoulder is an SPFH domain. If the enrichment is a generic property of SPFH-family
proteins, it says little about vaults specifically. In CCLE, repeat the identical analysis seeding with
**FLOT1, FLOT2, STOM, PHB, PHB2, ERLIN1, ERLIN2** instead of MVP.

- **MVP-specific** if `GOBP_PLASMA_MEMBRANE_REPAIR` clears 0.05 for MVP but for **fewer than half** of
  the SPFH seeds tested.
- **Generic SPFH property** if it clears 0.05 for a majority of SPFH seeds. That would not be a null
  result — it would relocate the finding from "vaults sit in repair compartments" to "SPFH-domain
  proteins sit in repair compartments, vaults included" — but it would remove MVP's claim to be special
  and must be reported as such.

No threshold is registered for how MVP's effect size compares with the SPFH seeds; only the
clears/does-not-clear count is pre-committed.

## What this cannot do

It cannot establish physical contact; §13's IP-MS remains the only contact test and it missed at
p = 0.058. It cannot resolve the EMT question left open in #109. Tumour tissue carries stromal and
immune content that cell lines lack, so a failure to replicate is also consistent with the tumour
cohorts being noisier rather than CCLE being wrong — and that ambiguity is stated here in advance rather
than invoked afterwards if the result is unwelcome.
