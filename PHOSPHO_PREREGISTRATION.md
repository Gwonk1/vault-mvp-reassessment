# Pre-registration: do assembled vaults open in living human tissue?

**Date:** 2026-11-07, before reading any phospho value. Argon proposed the modality (back-channel 004);
design and gates below are Claude's. A modality neither agent has touched.

## The logic
A protein kinase cannot phosphorylate a residue it cannot reach: the catalytic cleft needs roughly
**5 Angstrom** of probe access to the substrate side chain. §12 established that the SPFH ligand pocket
has **0.00 square angstroms of exterior access** in the closed 78-mer. So:

**If a residue is reproducibly phosphorylated in human tumours but is inaccessible from outside the
closed particle, the particle must open in vivo.** That converts a static structure into evidence about
dynamics, using tissue from real patients rather than a dish.

## Part 1 — steric test (self-contained, run first)
- Sites: MVP phosphosites annotated in CPTAC (`generic-assay-meta`, 6 sites in LUAD).
- Structure: PDB 11JB, 78-mer, already on disk.
- For each phosphorylated residue compute, in the assembled particle: transmural offset from the local
  shell midsurface, and solvent accessibility at probe radii **1.4 A (water) and 5.0 A (kinase cleft)**,
  from the exterior side and the lumen side separately.

**SHELL MUST OPEN:** at least one reproducible site has 0.00 square angstrom exterior access at
r_probe = 5.0 A. **NO EVIDENCE:** every site is exterior-accessible at 5.0 A.

## Part 2 — stoichiometry (requires fetching phospho data)
Residualise each phosphosite on **its own gene's total protein** (`dp = phospho ⊥ total`), which removes
cell-type composition and bulk abundance by construction. Then test whether `dp_MVP` predicts per-vault
PARP4 or TEP1 loading (`PARP4_prot ⊥ MVP_prot`), pooled across cohorts with the REML estimator.

## Gates
1. **Signalling gate:** residualised MAPK1 activation-loop phosphorylation (T185/Y187) must recover at
   least 3 canonical MAPK-pathway phosphosites (MAPK3, MAP2K1/2, RPS6KA*, EGFR, BRAF) in its top 25.
2. **Coverage gate:** MVP must have at least 2 sites quantified in at least 3 cohorts.
If either fails, Part 2 is reported UNINFORMATIVE. Part 1 does not depend on either.

## Kill condition
The phospho-gated-vault idea is dead if **every** reproducibly phosphorylated MVP residue is already
exterior-accessible at 5.0 A in the closed particle **and** no `dp_MVP` site associates with per-vault
PARP4/TEP1 stoichiometry at q < 0.05.

## Limits
CPTAC site assignments come from peptide mapping and can be ambiguous between nearby S/T/Y. A solvent
probe is a crude proxy for a kinase active site. 11JB is one conformation of a dynamic particle, so
"inaccessible in this structure" is not "inaccessible always" — which is precisely the point being
tested, and means a positive result shows the closed state cannot be the only state.
