# Pre-registration: do the repair neighbours co-elute with the vault, or only co-vary across cell lines?

**Written 2026-11-09, before any co-fractionation chromatogram was opened.** UniProt accessions
below were confirmed against the reviewed human proteome on this date, which is an identifier
check and not a look at elution profiles. `src/cofraction.py` is committed with this file and is
not run until after that commit.

## Why this is the test that #41 does not have

§28 reversed #41 on co-abundance in 375 cell lines, after a cytoplasmic-mass adjustment. §13's
anti-MVP IP-MS missed its contact bar at p = 0.058. Co-abundance across cell lines cannot tell a
particle from a shared regulatory program. Intact vaults are about 13 MDa. On a size-exclusion
column they have to emerge at the high-molecular-weight end, and a soluble repair protein that is
not on the particle cannot follow them there. That is the distinction this test makes.

## Data, locked

Skinnider, Akinlaja and Foster, the processed chromatogram release on Zenodo record 4106578
(`Chromatograms.zip` only). This is the 206-experiment chromatogram matrix from the 2021
meta-analysis. It is not the 411-experiment CFdb expansion of 2023, which publishes pairwise
feature tables and raw MaxQuant output rather than a chromatogram matrix of this size. The 2023
matrix is not swapped in after these profiles have been seen.

One quantification file per experiment directory, in this order: a file whose name contains
`ibaq`, else `ms1` or `intensity`, else `spectral` or `count`. The choice is logged. Protein
identifiers may be gene symbols or UniProt accessions. The locked map is:

| gene | accession |
|---|---|
| MVP | Q14764 |
| PARP4 | Q9UKK3 |
| TEP1 | Q99973 |
| ANXA2 | P07355 |
| S100A10 | P60903 |
| MYOF | Q9NZM1 |
| AHNAK | Q09666 |
| AHNAK2 | Q8IVF2 |
| EHD2 | Q9NZN4 |
| EHD4 | Q9H223 |
| CAPN2 | P17655 |
| CD151 | P48509 |
| CAVIN1 | Q6NZI2 |

## Which experiments count

An experiment is size-exclusion only if its path or its own metadata says SEC, size exclusion,
Superose, Superdex or gel filtration, and does not name ion exchange (IEX, SAX, WAX) as the
method. Density-gradient experiments are reported separately and are not in the primary. An
experiment with no method label is excluded and counted. Fraction order is the column order as
shipped. No experiment is reordered by hand after the profiles are seen.

MVP is usable in an experiment when it has at least 8 finite fraction values. Its peak is the
fraction of maximum signal. The peak is early when its 1-based index divided by the number of
fractions is <= 0.20. The vault window is that fraction plus or minus one.

## Gate

Among early size-exclusion experiments, the gate passes only if at least one experiment shows
**both** PARP4 and TEP1 co-eluting with MVP, where co-eluting means Pearson r >= 0.50 across the
fractions (at least 8 pairwise-finite points) **or** that protein's own peak inside the vault
window. If the core particle is not visible, the repair test is UNINFORMATIVE. A proteasome
self-correlation (PSMA1 against PSMB1, PSMB2, PSMB3, PSMC1, PSMD1, where measured) is reported as
a chromatogram-quality diagnostic and is **not** a gate: a weak proteasome cannot be used to
discard an inconvenient vault result.

## Primary

The analysis set is the experiments that individually satisfy the gate. For every protein
quantified in at least 8 fractions, compute Pearson r with MVP. Each repair gene contributes its
mean r across the analysis experiments in which it is quantified. At least 5 of the 10 repair
genes must be quantified in at least one analysis experiment, or the test is UNINFORMATIVE.

Null: 1000 draws, seed 0. Each draw replaces every quantified repair gene with a random protein
whose count of finite fractions is within 25% of that gene's median and which is quantified in a
number of analysis experiments within ±1 of that gene. p = (1 + number of null means >= the
observed mean) / 1001.

- **Physical co-elution survives** if the gate passes and p < 0.05.
- **Kill.** If the gate passes and p >= 0.05, the physical-particle reading of the membrane-repair
  neighbourhood is struck. The cell-line co-abundance result can remain, labelled as co-abundance.
- The fraction of repair genes whose own peak falls in the vault window is reported with no
  threshold and cannot rescue a kill.
