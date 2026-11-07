# Pre-registration: which face of the vault is evolution protecting?

**Date:** 2026-11-06. Tests Graham's "maybe it binds on the outside" idea against the field's
lumen-first assumption. Committed before any conservation value was mapped to any structure.

## Question
Within MVP, is sequence conservation concentrated on the **lumen-facing** surface or the
**outward-facing** surface of the assembled particle?

## Why it is answerable now
MVP is unusually conserved for its phylogenetic reach (89.5th percentile, `results/divergence.json`),
so there is real signal to localise. Forty years of searching the lumen for cargo is an assumption about
which face matters; this measures it.

## Data
- **Structure:** PDB 4V60, rat liver vault, 3.5 Å, the assembled particle.
- **Conservation:** the eggNOG 2759 alignment of MVP's orthologous group `2QPP0`, 174 sequences,
  1,202 columns. The rat sequence in that alignment anchors the mapping, so no cross-species step is needed.

## Method
1. Per-residue conservation = fraction of aligned sequences carrying the rat residue at that column,
   over columns where at least half the sequences are ungapped.
2. Solvent accessibility computed **in the context of the assembled particle**, so that subunit
   interfaces count as buried.
3. Each residue is classified by accessibility and by radial distance from the particle's symmetry axis
   (its principal axis of inertia):
   - **buried** — relative accessibility below 15%, excluded from the primary comparison;
   - **lumen-facing** — exposed and inside the median radius of exposed residues;
   - **outward-facing** — exposed and outside it.

## Primary statistic
Difference in mean conservation between outward-facing and lumen-facing exposed residues, with a
**block bootstrap over 20-residue windows** (2,000 resamples) because neighbouring residues are not
independent.

- **OUTWARD-FACING CONSERVED:** outward mean exceeds lumen mean, bootstrap CI excluding zero.
- **LUMEN-FACING CONSERVED:** the reverse.
- **NO DIFFERENCE:** CI includes zero.

Secondary, reported alongside: Spearman correlation of conservation against radial distance among
exposed residues, and mean conservation per annotated domain (wall repeats, shoulder/SPFH, cap helix,
cap ring) from UniProt Q14764.

## The confound that would otherwise sink this
**Buried residues are conserved for folding reasons, not functional ones**, and the barrel wall has more
buried volume than the caps. Restricting the comparison to solvent-exposed residues is what makes the
question about function rather than about packing. Buried-residue conservation is reported separately as
a check that it is high, which would confirm the measure behaves as expected.

## Gate, before reading the comparison
The structure must behave like a vault: at least 30 protein chains, and exposed residues must span a wide
radial range rather than a single shell. Mean conservation of buried residues must exceed that of exposed
residues overall — the standard pattern for any folded protein. If that fails, the conservation mapping is
wrong and the result is uninformative.

## Limits
A rat structure with conservation measured across eukaryotes; the particle is conformationally dynamic and
one crystal form may not represent the docked or open states. "Lumen-facing" by radius is a geometric
proxy, not a chemical one. Conservation localises constraint, not function — a conserved outer face does
not show what binds there.
