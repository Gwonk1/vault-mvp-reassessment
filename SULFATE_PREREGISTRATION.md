# Pre-registration: does MVP's tissue distribution track steroid SULFO-conjugation, and does the placenta asymmetry exist?

**Date:** 2026-11-10, before any MVP-versus-sulfotransferase number was computed. Nothing in this
file has been run. `git log --oneline` is the record: this commit contains the registration and no
results.

## Why

Two things that are already on the record, which together make a prediction neither makes alone.

1. **The lumen is an anion trap.** Argon test A6 (`channel/to-claude/003r`, verified): apo human
   `11JB` carries **the highest positive electrostatic potential in the entire vault lumen at the
   SPFH shoulder keyhole, +37.60 mV at |z| = 170 Å** — described there as *"an electrostatic trap
   for anionic NAD+/ADP-ribose/vtRNA"* — and loading 78 AR6²⁻ flips the shoulder's luminal net
   charge from +23.4 e to −132.6 e, quenching the peak by −17.00 mV. Every published vault ligand
   is an **anion**.
2. **Argon excluded "steroidogenesis or NADPH biosynthesis *per se*" (`007r`, VERIFIED) on the
   placenta rank:** placenta is massively steroidogenic and sits at **#38/51** for MVP (§21).

The refinement being registered: **adrenal cortex is a sulfo-CONJUGATING tissue (SULT2A1; DHEA-S is
the most abundant circulating steroid in humans) while placenta is the body's DE-sulfating tissue
(steroid sulfatase, which imports DHEA-S and hydrolyses it).** A reading in which the trap's load is
an **anionic amphipathic steroid sulfate** therefore *predicts* the very observation that killed the
generic steroid reading — adrenal high, placenta low — whereas "steroidogenesis" predicts both high.
That asymmetry is the only reason this is worth an instrument rather than a sentence.

**This is also the hypothesis class this project has been wrong about most often.** It was arrived at
by reading a ranked list for a story, which is faults #59/#60/#64/#70/#90, and §22 has already shown
that *this exact instrument returns tissue composition* (70 of 143 immunoglobulin genes in MVP's top
200, because gut tissue is plasma-cell rich). The design below is therefore **asymmetric on purpose**.

## Data

`data/raw/tissue/rna_tissue_consensus.tsv` — HPA consensus, long format, 1,026,293 rows,
20,123 genes x 51 tissues, nTPM. The same file as §21 and §27a. Spearman throughout, so no
log transform is required.

## Gate (must pass before the primary is interpretable)

The file must recover the textbook tissue of each enzyme in the comparison, or it cannot speak to
their contrast:

- **SULT2A1 must place adrenal gland in its top 2 of 51 tissues.**
- **STS must place placenta in its top 5 of 51 tissues.**

File-level gates already passed on this file in §21 (ALB→liver, INS→pancreas, SFTPC→lung).
**If either enzyme gate fails, this registration is reported as GATE-FAILED and no primary is read.**

## Primary test — pre-declared as KILL-ONLY

Spearman rho of MVP against every expressed gene across the 51 tissues, then the **percentile rank**
within that genome-wide distribution for a fixed panel, named now:

**Sulfo-conjugation:** `SULT2A1`, `SULT2B1`, `SULT1A1`, `SULT1A3`, `SULT1E1`
**Sulfate donor / transport:** `PAPSS1`, `PAPSS2`, `SLC35B2`, `SLC35B3`
**De-sulfation (the contrast):** `STS`, `GNS`, `GALNS`, `ARSA`, `ARSB`

Percentile, not raw rho, because rank-1-of-N restated as a percentile is vacuous (#470) and because
the genome-wide distribution is the only available null for this instrument.

- **KILLED** if **both** `SULT2A1` and `SULT2B1` fall below the **80th percentile** of MVP's
  genome-wide co-expression distribution, **OR** if `STS` ranks above both of them.
- **NOT KILLED** otherwise.

**"NOT KILLED" is not support, and may not be written as support anywhere.** §22 established that
this instrument's output is dominated by tissue identity; a pass means the reading survived a cheap
filter and nothing more. No probability may be attached to the hypothesis on the strength of this
test, in this file or any other.

## Pre-declared confound, with its control

**MVP is a GI-and-glandular gene and the sulfotransferases are GI-and-hepatic genes, so a pass is
what pure tissue sharing predicts.** This is the §11/§22 confound class and it is named before the
run, not after.

**Control, computed in the same script:** build a GI composite (mean nTPM across colon, small
intestine, duodenum, rectum), take every gene in the **top quartile** of correlation with that
composite, and report the **distribution of MVP co-expression percentiles within that matched set.**
If `SULT2A1`'s percentile sits **inside the interquartile range** of that matched null, the pass is
tissue identity and must be reported as such **in the same sentence as the percentile**, per house
rule 19.

## Secondary — the asymmetry itself, which is the actual content

Report, as one table and with no statistic attached: the rank of **adrenal gland** and of
**placenta**, out of 51, for `MVP`, `SULT2A1`, `SULT2B1`, `STS`, `PAPSS2`.

- **The asymmetry EXISTS** if `SULT2A1` ranks adrenal above placenta and `STS` ranks placenta above
  adrenal.
- **KILL CONDITION for the whole design:** if `STS` ranks **adrenal above placenta** in this file,
  the contrast the registration rests on does not exist here and the sulfate refinement is withdrawn
  regardless of the primary.

## Limits, stated before the result is known

- **n = 51 bulk tissues**, highly structured; co-expression is not binding, and transcript is not
  enzyme activity.
- **Nothing in this design measures whether a vault binds a steroid sulfate.** It cannot: the
  measurement that would is a binding assay against purified vaults, which does not exist publicly
  and is not available to this project.
- **It cannot distinguish "steroid sulfates" from "any anionic amphiphile"** — several of which are
  also GI-and-adrenal enriched.
- **Adrenal has exactly one CCLE line and zero with proteomics** (§25), so there is no orthogonal
  instrument available for the one tissue the hypothesis is about.
- **The only thing this test can do is remove the reading.** It is registered because that is cheap
  and the reading is otherwise unfalsifiable with data in hand.

## Relationship to the stopping rule

The project STOPPED on 2026-11-09 after audit 011, on the grounds that *"everything remaining needs
data that does not exist in a usable form."* **This test does not need new data** — the file has been
on disk since 2025-11-05 and is the same one §21 and §27a used — so it is outside the class that
ruling closed. Reopened at Graham's explicit instruction, 2026-11-10. **No codeml, no EMPIAR, no
second structure**, which is what audit 011 actually forbade.
