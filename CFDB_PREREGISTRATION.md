# Pre-registration: does the vault appear as a native co-eluting assembly, and does its neighbourhood?

**Written 2026-11-07 while the data downloaded, before any value was read.** Committed before running
`src/cfdb.py`.

## Why this instrument

Co-abundance has failed the neighbourhood question five times and cannot distinguish physical
association from shared transcription (#123). The TurboID attempt (§32) was voided because MVP was
absent from a shallow run — a gate argon specified and we demoted (#130).

CFdb (Skinnider, Akinlaja & Foster, *Nat Commun* 2023, PMID 38102123; Zenodo 10.5281/zenodo.10038713)
is a harmonised meta-analysis of **411 co-fractionation MS datasets**, 21,703 fractions, giving a scored
human interactome from **native separations with no detergent IP and no wash-off step**.

Its decisive property for this question is **size**. An intact vault is ~13 MDa. Soluble monomers such
as CAPN2 (80 kDa), EHD4 (61 kDa) or IQGAP1 (189 kDa) cannot migrate into megadalton fractions on their
own. **Co-elution with the MVP peak therefore carries size information that co-abundance across samples
never did.**

Data: `data/raw/cfdb/Homo_sapiens.tsv.gz`, the predicted human interactome.

## Positive-control gate, required before any MVP result is interpreted

CFdb must recover complexes we know exist, using the same scoring column and threshold applied to MVP:

1. **Proteasome.** `PSMA1` must have at least **5** other proteasome subunits (`PSMA*`/`PSMB*`/`PSMC*`/
   `PSMD*`) among its scored partners above threshold.
2. **Ribosome.** `RPL7` must have at least **5** `RPL*`/`RPS*` partners above threshold.

If either fails, the resource as we are reading it cannot detect a real complex and the result is
**UNINFORMATIVE** whatever MVP does.

## Primary test and prediction

**Is MVP-PARP4 present as a scored native interaction?**

**Prediction, committed:** yes. PARP4 is MVP's rank-1 partner in 13 co-abundance cohorts, CCLE, all 8
CPTAC cohorts, anti-MVP IP-MS and *Dictyostelium* proximity labelling (#116). If a native
co-fractionation meta-analysis of 411 datasets does **not** recover MVP-PARP4 while its gates pass,
**the most robust finding in this project is in real trouble** and that is the headline, not anything
else here.

**Kill condition for #116:** gates pass and MVP-PARP4 is absent or scores below threshold.

## Secondary: TEP1

Same test for MVP-TEP1. TEP1 is sparsely measured in proteomics, so absence is weak evidence; only
present-and-low counts against it.

## Tertiary: the neighbourhood, which is the point

For MVP's scored partners, test enrichment of the previously favoured membrane terms
(`GOBP_PLASMA_MEMBRANE_REPAIR`, `GOCC_CAVEOLA`, `GOBP_PLASMA_MEMBRANE_ORGANIZATION`,
`GOCC_LATE_ENDOSOME`) and the innate-immune terms that replicated in §31
(`GOBP_INFLAMMATORY_RESPONSE`, `GOBP_RESPONSE_TO_BACTERIUM`, `GOCC_RUFFLE`,
`GOBP_ANTIGEN_PROCESSING_AND_PRESENTATION`) against **200 size- and degree-matched random protein sets**.

Named proteins reported individually whether flattering or not: ANXA2, S100A10, EHD2, EHD4, CAPN2, MYOF,
AHNAK, IQGAP1, CD63, OPTN, VPS35, FLOT1, FLOT2, CAVIN1.

- **Membrane module gets its first contact-level support** if a membrane term clears p < 0.05.
- **Innate-immune module gets contact-level support** if an immune term clears p < 0.05.
- **Both finished** if neither clears while the gates pass. After five co-abundance failures and one
  void contact test, a null in a native size-resolved instrument with working gates is the end of the
  line for both as physical-association claims, and we will say so.

## What this cannot do

CFdb scores are predictions from elution-profile similarity, not direct binding measurements, and
co-elution at equal size is not contact. Fraction resolution in most CF-MS runs will not isolate a
13 MDa particle cleanly. **We are not treating a positive as proof of interaction**, only as evidence
from an instrument whose failure mode differs from co-abundance — which is the entire reason for using
it.
