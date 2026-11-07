# Pre-registration: is the cortical-actin neighbourhood just protein abundance?

**Written 2026-11-07, before computing any abundance-matched statistic.** Committed before running
`src/cyto_composition.py`.

## The concern, which is ours and was named in §36d before anyone raised it

#155 holds that after removing the interferon axis, `GOCC_RUFFLE` and `GOBP_ACTIN_FILAMENT_ORGANIZATION`
replicate around MVP in endometrium and in cell lines. #157 names the control that would kill it: MVP is
an abundant cytoplasmic protein, the actin cortex is the most abundant cytoplasmic structure, and
residualising on a nuclear-to-cytoplasmic ratio removes nothing about composition *within* the cytoplasm.

**Two design facts, established before registering and both of which matter.**

First, the obvious control is circular and is therefore excluded. Of 17 core actin-machinery genes
(ACTB, ACTG1, ACTR2/3, ARPC1A-5, CFL1, PFN1, TMSB4X/10, CAPZA1/2, CAPZB), **16 are members of the tested
sets themselves** — only ACTB is disjoint. Residualising on a core-actin score would remove the signal
being tested by construction, so that arm is not run.

Second, and this is the actual gap: **§31 and §36 used plain hypergeometric enrichment with
Benjamini-Hochberg correction and no abundance matching.** §28 used 200 size- and abundance-matched
random sets; the scan did not. Abundant, well-measured proteins are more likely to enter any top-200
correlate list, and actin-cortex proteins are among the most abundant in the cell. **The scan's
enrichment statistic cannot presently distinguish "associated with MVP" from "abundant".**

## Method

In the §36 framework exactly — residualised on the N:C proxy, six proliferation markers, STAT1 and IRF9
— recompute enrichment in MVP's top 200 for a fixed panel of terms, but against **200 random gene sets
matched on measured-abundance decile and on set size**, the §28 procedure.

Datasets: the three non-CNS sets that decide #155 (`coad_cptac_2019`, `ucec_cptac_2020`,
`ccle_broad_2019`), with the two CNS sets reported for completeness and excluded from the verdict.

## Term panel, fixed here

- **Under test:** `GOCC_RUFFLE`, `GOBP_ACTIN_FILAMENT_ORGANIZATION`
- **Also under test, since it survived §36 against prediction:** `GOBP_INFLAMMATORY_RESPONSE`
- **Negative controls, expected to stay dead:** `GOBP_ANTIGEN_PROCESSING_AND_PRESENTATION`,
  `GOBP_RESPONSE_TO_TYPE_II_INTERFERON` — both 0 of 3 non-CNS in §36. If abundance matching *resurrects*
  these, the matching is broken.
- **Abundance reference, no registered threshold:** `GOCC_MITOCHONDRION`, `GOCC_GOLGI_APPARATUS`,
  `GOCC_ENDOSOME` are each >1,000 members and outside the scan's 10-500 window, so they are reported
  descriptively as a check on whether MVP's top 200 is enriched for every abundant compartment.

## Positive-control gate

PSMA1-seeded proteasome terms must still clear specificity p < 0.05 under abundance matching in at least
two of the three non-CNS datasets. Proteasome subunits are abundant, so if abundance matching destroys
the proteasome it is over-matching and the result is **UNINFORMATIVE**.

## Primary prediction and kill condition

- **#155 survives** if `GOCC_RUFFLE` **or** `GOBP_ACTIN_FILAMENT_ORGANIZATION` clears specificity
  p < 0.05 in **both** `ucec_cptac_2020` and `ccle_broad_2019` — the two datasets that carried it in §36.
- **Kill condition: if neither clears in both, #155 is struck and the cortical neighbourhood is recorded
  as a protein-abundance artefact.** That would leave the §31/§36 scan with no surviving neighbourhood
  term at all, co-abundance would be finished on this question for the second time, and the only
  standing association in this project would be MVP-PARP4.

**We expect it to die.** The same abundance logic that makes the actin cortex a plausible artefact also
explains why it beat every hypothesis we proposed: it is the largest cytoplasmic protein mass in the
cell. Registering that expectation so a survival counts for something.

## What this cannot do

It cannot make co-abundance into contact; CFdb found no cortical neighbourhood at all (§33) and that
disagreement stands either way. It does not address the COAD counterexample. And abundance matching on
measured intensity is itself imperfect, since detection and true abundance are not the same thing.
