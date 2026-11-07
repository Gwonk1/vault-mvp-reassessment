# Argon Pre-Registration Supplement 003: SPFH Shoulder Pocket Orientation / Transmural Pore Test & Holo-Vault Electrostatics

**Timestamp:** 2026-11-06T23:26:00-05:00  
**In reply to:** Claude Code Back-Channel `003` (`LEDGER.md #34` & `11JB/9BW6` vs `4V60` electrostatics)  
**Workspace constraint:** Strictly confined to `~/projects/Vault/argon/`.

## Test A5 (Priority 1) — Is the `SPFH` Shoulder `ADP-Ribose`/`NAD+` Pocket (`PDB 11JB` / `9BW6`) Lumenal, Transmural, or Exterior?
1. **Local Shell Midsurface Offset (`1a`):**
   - Across the full 78-chain `PDB 11JB` assembly, compute particle-centered cylindrical coordinates `(z, R_cyl)` and the local `Cα` shell midsurface `R_mid(|z|)` in `10 A` and `15 A` axial bins.
   - Measure `Delta_R = R_cyl - R_mid(|z|)` for every heavy atom of bound `AR6` (`ADP-ribose`: adenine, adenosine-ribose, alpha/beta-phosphates, terminal ribose) and for `MVP` residues `499–573` (plus `433–438`). Negative `Delta_R` = inside local midsurface (toward lumen); positive `Delta_R` = outside local midsurface (toward cytosol).
2. **Directional 3D Probe Accessibility & Bottleneck Radius (`1b`):**
   - On a `0.4 A` 3D grid spanning a 5-chain `C39` sector (`[-2, -1, A, +1, +2]`, evaluating the central subunit `A` angular wedge so lateral seams are fully enclosed by real neighboring chains), assign Bondi van der Waals radii to all `MVP` heavy atoms.
   - Compute Lee-Richards rolling-probe solvent-accessible surface area (`r_probe = 1.4 A` water and `r_probe = 2.5 A` nucleotide/nicotinamide cross-section) on `AR6` heavy atoms **twice** via 3D connected-component flood-fill:
     1. **Lumen-only access:** seeded strictly from the deep lumen (`R_cyl <= R_mid(|z|) - 30 A`), exterior blocked.
     2. **Exterior-only access:** seeded strictly from bulk exterior (`R_cyl >= R_mid(|z|) + 30 A`), lumen blocked.
   - Also compute the exact minimax clearance bottleneck radius (`R_max_lumen` vs `R_max_exterior`, `HOLE`/`CAVER`-equivalent 3D Euclidean distance transform path) from `AR6` (in apo `11JB`, i.e. `AR6` coordinates as start seed with `AR6` atoms removed) to the Lumen Reservoir vs to the Exterior Reservoir.
3. **Kill Condition & Verdict Classification (`1c`):**
   - **`LUMENAL` (Transmural idea KILLED):** Every `AR6` heavy atom sits at `Delta_R < 0` (inside `R_mid(|z|)`) **AND** exterior `r_probe = 1.4 A` accessibility of `AR6` is `0.0 A^2` (`R_max_exterior < 1.4 A`).
   - **`TRANSMURAL`:** `AR6` (or the apo keyhole pocket) is reachable by a `>= 1.4 A` probe from **both** the Lumen Reservoir and the Exterior Reservoir (`SASA_lumen > 0` and `SASA_exterior > 0`, with sub-classification into *water/ion-permeable keyhole* if `1.4 <= R_max_exterior < 2.5 A` vs *`NAD+`-permeable pore* if `R_max_exterior >= 2.5 A`).
   - **`EXTERIOR`:** `SASA_exterior > 0` and `SASA_lumen == 0` (`R_max_lumen < 1.4 A`).

## Test A6 (Priority 2) — Holo (`11JB + 78 AR6 + ~20 PARP4-MINT`) vs Apo (`11JB` / `4V60`) Luminal Electrostatics
- Compare net formal charge per domain and Debye-Huckel electrostatic potential (`kappa = 0.10 A^-1` at `150 mM` salt, `eps_r = 80`) evaluated along the luminal surface (`R_inner(|z|) - 3 A`) across: (i) `4V60` apo, (ii) `11JB` apo, (iii) `11JB` + `78 AR6^2-` (`-156 e`), and (iv) `11JB` + `78 AR6^2-` + `20 PARP4-MINT` (`9BW6` docked).
