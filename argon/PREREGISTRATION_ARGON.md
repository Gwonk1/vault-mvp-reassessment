# Argon Pre-Registration: Primary 2024–2026 Datasets, Physical/BioID Interactomes, Pocket & Operon Tests

**Timestamp:** 2026-11-06T22:44:00-05:00  
**Workspace isolation:** All files, raw downloads, scripts, and outputs are strictly confined to `~/projects/Vault/argon/` so tracked repository files remain untouched while Claude runs `src/surface.py`.

This document freezes predictions, positive-control gates, and kill conditions **before** inspecting the contents/tables of:
1. Musgrove et al. (`bioRxiv 10.1101/2025.05.16.654162v2` / `PMID: 42031226`) neuronal Vault RIP-seq & Vidigal et al. (`PMC11482604` / `PRJNA1120017`) `Vaultrc5-/-` mouse data.
2. *Dictyostelium* *in situ* vault proximity-labeling proteomics (`PMC13100048` / `PRIDE PXD071329`) and human physical/proximity interactomes (`Human Cell Map` BioID, `BioPlex 3.0`, `OpenCell`, `EBI IntAct`).
3. Anthropic's prokaryotic/phage `L05` vault preprint (`bioRxiv 10.64898/2026.11.04.764334v1`) + Human Brain Vault cryo-EM structures (`PDB 9R86` / `9R87`, Lövestam & Scheres 2025).
4. `DepMap` `CCLE` copy-number-adjusted co-abundance + 225-metabolite LC-MS screen + `Replogle 2022` Perturb-seq knockdown readouts (if accessible).

---

## Test A1 — Methodological & Cargo Audit of 2026 Neuronal Vault RIP-seq ("Trap-and-Seq")
- **Target:** Musgrove et al. (`10.1101/2025.05.16.654162v2` / `PMID: 42031226`).
- **Gate ( Biochemical Rigor Gate ):** For a Vault RIP-seq dataset to count as genuine *Trap-and-Seq* (luminal encapsulation or specific vault RNP cargo rather than bead/IgG background), it must pass at least **2 of 3 biochemical specificity criteria**:
  1. Positive recovery of endogenous vault RNA (`Vaultrc5` in mouse/rat) strongly enriched over Input / IgG control.
  2. Explicit negative control IP (isotype IgG, bead-only, or `Mvp`-knockdown/KO background subtraction) with quantitative fold-enrichment + FDR threshold.
  3. Nuclease protection (RNase treatment prior to shell lysis) **or** biochemical purification separating intact ~13 MDa vault particles from free soluble RNPs. *(Note: if #1 and #2 pass without #3, cargo is classified as **VAULT-ASSOCIATED RNP (SURFACE OR LUMEN)** rather than proven luminal encapsulation.)*
- **Pre-registered Questions:**
  - Does `MVP` IP enrich retrotransposons / Pol III RNAs / viral-mimic dsRNAs (Article 1 containment prediction), or specific mRNAs?
  - Which exact "immune surveillance" transcripts shift into vaults upon `Vaultrc5` knockdown, and do they overlap the interferon/inflammasome/membrane-repair pathways in `LEDGER.md` (`#19`, `#26`, `#27`)?

---

## Test A2 — Physical & Nanometer-Proximity Interactome Convergence (`PXD071329` + Human AP-MS / BioID)
- **Targets:**
  - *Dictyostelium* live-cell proximity-labeling mass-spec (`PMC13100048` supplementary tables / `PRIDE PXD071329`).
  - Human AP-MS & BioID (`BioPlex 3.0`, `OpenCell`, `Human Cell Map` 192-compartment BioID, `IntAct` / `BioGRID` physical).
- **Positive-Control Gate:** Human physical interaction datasets that assay `MVP`, `TEP1`, or `PARP4` must recover at least one canonical intra-vault partner (`MVP`–`PARP4` or `MVP`–`TEP1`) at passing FDR/score before extra-vault preys are interpreted.
- **Primary Prediction (`MEMBRANE-REPAIR / CORTICAL CONTACT`):*
  - If Standing `#26` (bulk/CCLE co-abundance with `ANXA2`, `S100A10`, `EHD2/4`, `CAPN2/CAPNS1`, caveolae/rafts) reflects physical colocalization rather than co-regulated cell state, human BioID (`Human Cell Map`) and/or AP-MS (`BioPlex`/`OpenCell`/`IntAct`) should place `MVP` at **plasma-membrane / cell-junction / cortical actin / endosomal-recycling** compartments or recover direct physical interactors in those families.
  - **Kill Condition:** If high-confidence BioID / AP-MS places `MVP` exclusively in soluble cytosol or nuclear pore / ER-ribosome fractions with **zero** plasma-membrane/cortical/annexin/EHD/calpain proximity partners across both human and *Dictyostelium*, then Standing `#26` is a **co-regulated cell-state module, not a stable physical complex**.

---

## Test A3 — `L05` vs. Human Brain Vault (`PDB 9R86` / `9R87`) Pocket Conservation & Prokaryotic Operon Synteny
- **Part 3A (The Putative CoA-like Inner-Wall Pocket):**
  - Extract the exact domain/residue coordinates of the unassigned inner-wall pocket density reported in Anthropic's `L05` preprint (`10.64898/2026.11.04.764334v1`).
  - Structurally align `L05` to the **actual human brain vault cryo-EM structure (`PDB 9R86`)** and score residue conservation across the eukaryotic `MVP` alignment (`data/raw/divergence/`).
  - **Prediction (`CONSERVED LIGAND POCKET`):** Structurally equivalent pocket-lining side chains exist on the luminal face of human `9R86` and exhibit mean conservation strictly above the luminal-surface median (>75th percentile of luminal exposed residues), preserving compatible chemical polarity (e.g., cationic Arg/Lys phosphate clamp + hydrophobic/aromatic adenine/acyl cradle for CoA-like ligands).
  - **Kill Condition (`PHAGE-SPECIFIC POCKET`):** If the pocket in `L05` is occluded in human `9R86`, maps to a non-homologous insertion, or its lining residues in eukaryotes sit <=50th percentile of luminal conservation with non-conservative charge flips, **Ledger #18's "conserved small-molecule sink at the L05 pocket" is struck for human vaults**.
- **Part 3B (Prokaryotic / Phage `MVP` Genomic Neighborhood — `H7`):**
  - Across non-redundant bacterial/archaeal/phage contigs encoding the `MVP` homologs in `10.64898/2026.11.04.764334v1` (+/- 10 flanking CDSs):
  - **Prediction:** Significant recurrence (>=3 independent phyla/genera and hypergeometric enrichment q < 0.05 or clear domain-family clustering) of either **(i) mobile anti-phage / nucleic-acid defense systems** (RM, CRISPR, CBASS, Thoeris, Viperin, `Ro60`/`rtcB`, endonucleases) or **(ii) membrane-stress / SPFH / `HflK-C` / AAA+ protease (`FtsH`) / CoA-lipid enzymes**.
  - **Kill Condition:** Flanking genes are random core/housekeeping genes with no shared functional theme across >=3 non-redundant lineages.

---

## Test A4 — Copy-Number-Adjusted Co-Abundance (`chr16p` Dissection) & `CCLE` 225-Metabolite Screen
- **Part 4A (`16p11.2` CNA Adjustment):** Regressing out gene-level copy number (or testing strictly in `16p`-euploid samples across `CCLE` / `CPTAC`) will **abolish** `PYCARD`, `MAPK3`, `ALDOA`, `SULT1A3` from `MVP`'s top-100 partners while **preserving** `PARP4`, `TEP1`, `ANXA2`, `CAPN2/CAPNS1`, `EHD2/4`, and testing whether `CASP1`/`CASP4` (`chr11`) genuinely survive (`r` attenuation < 25%).
- **Part 4B (`CCLE` 225-Metabolite LC-MS Screen):** Correlate `MVP` protein abundance (`ccle_broad_2019`, `n ~ 375`) against all 225 intracellular polar metabolites and lipids (`CCLE` metabolomics), both raw and after 3-PC / lineage adjustment.
  - **Gate / Threshold:** Any candidate metabolite class (CoA/pantothenate/acyl-carnitines vs. membrane-repair lysophospholipids/ceramides/plasmalogens) must reach **FDR q < 0.05** across all 225 metabolites. If best `q >= 0.05`, the steady-state bulk metabolite sink screen is **NULL**.
