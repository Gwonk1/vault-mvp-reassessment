# Amendment to SURFACE_PREREGISTRATION.md

**Date:** 2026-11-06, before the test was run. Prompted by `gemini-argon-audit.txt` §1B. The original
geometry was wrong and would have blurred or inverted the result; it is corrected here rather than after
seeing an answer.

## 1. Global median radius replaced by local transmural offset
A vault tapers from roughly 200 Å radius at the waist to ~60 Å at the cap ring, while the shell wall is
only ~15-25 Å thick. Splitting exposed residues at the **global** median radius therefore separates
**caps from belly**, not **lumen from outside**: outward-facing cap residues fall inside the global
median and would be labelled "lumen-facing", and lumen-facing residues on the barrel wall fall outside it
and would be labelled "outward-facing".

**Replacement:** for each exposed residue compute `delta_r = r_i - R(|z_i|)`, where `r_i` is its radial
distance from the symmetry axis and `R(|z|)` is the **local shell midsurface radius at that residue's own
axial height**, estimated as the median `r` of all residues in a 10 Å `|z|` window. Negative = lumen-facing,
positive = outward-facing. At the flat cap top, where the shell normal is axial rather than radial, residues
are classified by axial offset from the local midsurface instead.

## 2. Subunit interfaces become their own category
Residues buried in the 78-mer but exposed in an isolated chain are **interface** residues, not "buried".
Structural packing selection is expected to concentrate there, and leaving them in the buried pile would
hide it. Reported as a third category and excluded from the lumen-vs-outward comparison.

## 3. Full biological assembly, not the deposited asymmetric unit
`4V60` as deposited is not the whole particle, so the waist dimerisation interface would be scored as
solvent-exposed. The **biological assembly** is used for all accessibility calculations. The pre-registered
">= 30 chains" gate is replaced by: the assembly must have **at least 70 protein chains** and be closed
(no residue of the inner wall exposed to bulk solvent through a gap).

## 4. Added secondary analysis
Human missense constraint from `data/raw/gnomad/MVP.json` mapped onto the same residues, asking whether
within-human constraint concentrates on interfaces, lumen or outer face. This is **exploratory** and was
suggested by the audit; it is not part of the primary label.

Everything else in `SURFACE_PREREGISTRATION.md` stands, including the primary statistic, the labels, the
buried-residue confound and the gate on buried-versus-exposed conservation.
