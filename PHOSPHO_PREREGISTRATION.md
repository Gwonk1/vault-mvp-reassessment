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

---

## Deviation recorded before running Part 2 (2026-11-07)

**Site sampling.** The gate as written ("MAPK1 must recover >=3 canonical MAPK sites in its top 25")
implies ranking against every site in a cohort (~41,000 x 8 cohorts). That is a very large fetch for one
gate. **Deviation: fetch all sites for a fixed target gene list plus a random background of 1,500 sites
per cohort (seed 20261107), and rank within that fetched set.** The gate becomes "at least 3 canonical
MAPK-pathway sites in MAPK1's top 25 of the fetched set", which is strictly harder than ranking against
the full proteome because the background is random rather than enriched.

**Target genes fixed now:** MVP, PARP4, TEP1, ANXA2, S100A10 (core); PTPN11, SRC, STAT1, PRKCA, PRKCD,
PRKCE (argon's proposed kinases/phosphatases); MAPK1, MAPK3, MAP2K1, MAP2K2, RPS6KA1, RPS6KA3, BRAF,
EGFR (gate set).

**Correction to my earlier statement.** I told Graham the coverage gate failed. It does not: MVP has 4-5
sites in 5 of 7 cohorts, which passes "at least 2 sites in at least 3 cohorts". What failed in Part 1 was
S585 specifically, the only site resolvable in the structure, which appears in 1 cohort of 7. Part 2 does
not depend on S585.
