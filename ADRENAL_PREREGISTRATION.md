# Pre-registration: is MVP's immunoglobulin co-expression caused by plasma cells being MVP-rich?

**Written 2026-11-07, before any MVP value in this stratification was read.** Committed before running
`src/lineage_mvp.py`.

## Why

`RESULTS.md` section 22 found that MVP's abundance across 51 tissues is dominated by plasma-cell and
immunoglobulin genes (`GOCC_IMMUNOGLOBULIN_COMPLEX`, 70 of 143, p = 9.3e-98). Section 21 found MVP's
top tissues are adrenal gland (176 nTPM) and the colon-small intestine-duodenum axis, with lung only
fifth of 51. Ledger #89 reads those together and proposes that the gut rankings are plasma-cell
**infiltrate**, leaving adrenal as the unexplained residual.

That proposal has two possible causes and we have not distinguished them:

- **(a) Infiltrate.** Plasma cells are intrinsically MVP-rich, so tissues holding more plasma cells
  measure more MVP. This would make the gut ranking a composition artefact.
- **(b) Coincidence.** MVP and immunoglobulin genes are high in the same tissues for unrelated reasons,
  and plasma cells are not themselves MVP-rich. This would leave the gut ranking standing as epithelial
  and would remove the main reason to treat adrenal as special.

Cell lines carry no immune infiltrate by construction, so lineage-stratified cell-line protein is the
clean discriminator.

## Data

`data/processed/prot/ccle_broad_2019.parquet` (CCLE, 12,096 proteins x 375 lines) with
`ccle_broad_2019.clin.parquet` for `LINEAGE`. Already in this repository and used in sections 13 and 18.

**Power is weak and stated in advance: only 6 of the 375 proteomics lines are `plasma_cell`.** A large
effect is detectable; a small one is not. A null here is weak evidence and will be reported as weak.
There is exactly **1 `adrenal_cortex` line in all 1,739 CCLE lines and 0 with proteomics**, so this
test cannot address adrenal directly and makes no attempt to.

## Positive-control gate

Plasma-cell identity must be recoverable from the protein data before any MVP number is interpreted.
Of the plasma-cell markers **MZB1, XBP1, SDC1, PRDM1, DERL3**, at least one must place `plasma_cell`
**first among all lineages with n >= 5** by mean z-score. If none does, the lineage labels are not
resolvable at protein level in this matrix and the result is reported **UNINFORMATIVE** regardless of
what MVP does.

## Primary test and prediction

MVP protein z-scored across lines; mean per lineage; lineages restricted to n >= 5.

- **Cause (a) is supported** if `plasma_cell` ranks in the **top 3** lineages for mean MVP z.
- **Cause (a) is not supported** if `plasma_cell` falls at or below the **median** lineage.
- Anything between is reported as equivocal, not as support for either.

## Kill condition

If `plasma_cell` sits at or below the median lineage for MVP while the gate passes, then **ledger #89's
infiltrate explanation loses its mechanism**, the gut tissue ranking is not explained by plasma cells,
and adrenal stops being a distinguished residual. We would then be obliged to withdraw the framing we
published this morning in `PAPER2` experiment 9, and we will.

## Secondary, descriptive only, no prediction registered

The full lineage ranking of mean MVP z, reported for orientation. `colorectal` (n = 30) and `lung`
(n = 79) are of interest because they are the tissues whose bulk rankings are in question, but no
threshold is set for them and nothing will be concluded from their position.

## What this cannot do

It cannot explain adrenal. It cannot establish what vaults are for. It tests one confound in one
direction, and that is all it is offered as.
