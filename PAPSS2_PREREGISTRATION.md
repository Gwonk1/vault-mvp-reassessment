# Pre-registration: is MVP–PAPSS2 special, or is it what any gene with PAPSS2's tissue profile gets?

**Date:** 2026-11-10, after §107 and before any matched-null value was computed. Nothing in this file
has been run. This commit contains the registration and no results; `git log --oneline` is the record.

## Why

§107 killed the steroid-sulfate reading and left one number behind: **`PAPSS2` at the 99.91st
percentile of MVP's genome-wide tissue co-expression, rank 16 of 16,929, rho +0.781, and adrenal
#1 of 51 — MVP's own top tissue.** Ledger #495 parked it as unreconciled rather than promoting it,
and named the condition for ever using it: *"even 99.91 means nothing until the class control is run
against **it**."* This is that control.

**The project's own history says what happens to a number like this if the control is not run.** #480
flagged COP1 at 27-fold as *"the strongest unreconciled positive number in the project"* — parked in
the support list of a claim with no exclusion rule applied to it. A second one now exists. The point
of running this today is that an unreconciled number does not stay neutral; it becomes a belief.

**And there is already a strong prior that this is tissue, not partnership.** `PAPSS1`, the paralogue
that makes the same metabolite, sits at the **24.61st percentile** (§107). Two enzymes with the same
product cannot both bear on a ligand hypothesis while differing by 75 percentile points. The obvious
reading is that `PAPSS1` is ubiquitous and `PAPSS2` is tissue-restricted, and that MVP's rho is
measuring the restriction.

## Data

`data/raw/tissue/rna_tissue_consensus.tsv`, the same HPA consensus file and the same expressed-gene
filter as §107 (nTPM >= 1 in at least 5 of 51 tissues; 16,930 genes), reusing `src/sulfate.py`'s
definitions so the two sections are comparable.

## The procedure being tested (named before it is pointed at anything)

For a seed gene **S**:

1. Rank all expressed genes by Spearman correlation of their own 51-tissue profile against **S's**
   profile. Take the nearest **N = 200** (and **N = 500** for robustness), excluding `MVP` and `S`.
   These are genes that look like S across tissues.
2. The null is the distribution of **rho(MVP, g)** over that matched set.
3. Ask where **rho(MVP, S)** falls inside it.

This asks the only question that matters here: **is MVP's correlation with S better than MVP's
correlation with genes that merely share S's tissue pattern?**

## Gate — the procedure must recover a known partner, or it cannot speak

Run the identical procedure with **S = PARP4**, a textbook stoichiometric vault subunit.

- **GATE PASSED** if `rho(MVP, PARP4)` exceeds the **95th percentile** of its PARP4-profile-matched
  null at N = 200.
- **GATE FAILED** otherwise, and in that case **the primary is not interpreted and this registration
  is reported as GATE-FAILED.**

**Both outcomes are declared in advance as informative, and the failure branch is the one this
project should expect.** `CALIBRATION.md` finding 2 measured three standard complex signatures against
this same particle and **all three failed** — co-abundance specifically *"returns the tissue"*. If
PARP4 cannot clear a tissue-matched null, that is the same floor appearing again on a fourth
instrument, it is a result in its own right, and **it means PAPSS2's 99.91 can never be promoted on
this instrument by anybody.**

`TEP1` is run as a second, harder positive control and **reported descriptively only** — it is not
part of the gate, because the known-hard subunit failing is expected (CFdb put it at the noise floor,
§CALIBRATION 1) and would tell us nothing new.

## Primary test

**S = PAPSS2.**

- **STRUCK** if `rho(MVP, PAPSS2)` sits at or below the **75th percentile** of the PAPSS2-matched null.
  The number is then tissue-profile sharing, ledger #495 is closed, and the row is marked struck.
- **NOT STRUCK** if it exceeds the **95th percentile** of that null.
- **INDETERMINATE** between the two, reported as such, with no promotion either way.

**"NOT STRUCK" is not support and may not be written as support**, for the same reason §107's
"not killed" could not be: this instrument's ceiling is co-regulation, not co-complex. No probability
may be attached to any hypothesis on the strength of this test, and `HYPOTHESES_AND_NOVELTY.md` is
not to be edited on its outcome.

## Secondary, all pre-specified

1. **Reciprocal direction:** MVP's percentile within `PAPSS2`'s own genome-wide co-expression
   distribution. Symmetry is expected and is not evidence of anything; asymmetry would be worth a note.
2. **`PAPSS1` as the internal negative**, run through the identical matched-null procedure. If
   `PAPSS1` is also extreme against its own matched null, then the paralogue split in §107 is not what
   it looks like.
3. **The matched sets themselves**, top 15 members listed for `PAPSS2` and `PARP4`, so a reader can
   see what "looks like this gene across tissues" actually returned.

## Limits, stated before the result is known

- **`PAPSS2` was selected for being extreme.** It is the maximum of the 14-gene panel in §107, so its
  percentile is a **maximum order statistic**, and the matched null does not correct for that
  selection. This limit survives any outcome below and must travel with the number.
- **Co-expression over 51 bulk tissues cannot separate co-complex from co-regulation.** That is not a
  caveat added here, it is `CALIBRATION.md` finding 2's third face, measured on this particle.
- **Transcript, not protein; bulk tissue, not cell type.** §27b's cytoplasmic-mass-fraction confound
  does not apply to this file (it is RNA, not equal-mass TMT), but bulk tissue composition does.
- **A profile-matched null is matched on the thing being controlled for, which makes it conservative
  in one direction only:** it can show a correlation is unremarkable, and it cannot establish that a
  remarkable one is physical.
- **n = 1 seed gene.** Whatever happens, it is one number about one pair.

## Relationship to the stopping rule

Same standing as §107: no new data, a file on disk since 2025-11-05, and no codeml, no EMPIAR, no
second structure — which is what audit 011 forbade. Run at Graham's explicit instruction,
2026-11-10, to close a parked number rather than to open a lane.
