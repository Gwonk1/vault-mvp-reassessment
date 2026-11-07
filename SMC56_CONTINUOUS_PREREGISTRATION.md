# Pre-registration: the continuous statistic across the whole small-term family

**Written 2026-11-07, before running the continuous statistic on any small term other than the four
already reported (SMC5/6, SUMO ligase complex, and the vault core gate).** Committed before running
`src/smc56_continuous.py`.

## Why this exists

§49d found `GOCC_SMC5_SMC6_COMPLEX` at mean WT_LFC **+3.976** against a matched null of +0.035 (sd
0.80) — about five sigma. §45 had killed the same complex at **q = 0.4199** across 4,527 small terms
using the dichotomised 4-of-6 count.

**These are not in conflict; they are two statistics, one of which has been family-corrected and one of
which has not.** Reporting the continuous figure as a revival would be exactly the selective
application #203 and house rule 8 warn against: taking the new statistic where it helps and the old
correction where that helps.

## Method

Compute the continuous statistic — mean `WT_LFC` of a term's members present in the 1,205-protein
universe, against size- and abundance-matched draws — for **every** term with 3 to 9 members in the
universe, the same family §45 corrected across. Benjamini-Hochberg across that whole family. Terms with
fewer than 3 members are excluded because a 2-protein mean is not estimable; §45's family used a
<10-member cut with no floor, so **we state this difference now** and report how many terms it changes.

Because the empirical percentile saturates at 100 with a finite draw count, significance is computed
parametrically from the matched-draw mean and standard deviation (z, one-sided), not from the
percentile, with 4,000 draws per term to stabilise the standard deviation.

## Positive-control gate

The vault core — MVP, PARP4, TEP1, a 3-member set, all verified present in the universe (house rule 7)
— must reach **q < 0.01** within this family. It is the bait and its two known subunits at +7.62, +8.66
and +6.27, so a family-corrected test that cannot recover it has no power for any small complex.

## Reachability check, per house rule 8

Both outcomes must be attainable before we commit. **They are:** with roughly 4,500 terms, BH at q =
0.05 requires a raw p of about 1.1e-5 for the single best term, which corresponds to about 4.2 sigma.
SMC5/6's observed z is near 4.9 and the vault core's is far larger, so a pass is reachable; and the
great majority of small terms sit near zero shift, so a fail is reachable. **Neither outcome is
foregone.**

## Outcomes, fixed now

- **SMC5/6 survives** if q < 0.05 within the family **and** the vault-core gate clears q < 0.01. Then
  §45's kill was a power failure of the dichotomised count, not a multiple-testing verdict, and the
  complex becomes the project's second positive contact finding after translation.
- **SMC5/6 dies for good** if q ≥ 0.05. §45's verdict then stands on a second and more sensitive
  statistic, and we close it permanently rather than returning to it.
- **Uninformative** if the vault-core gate fails.

We also pre-commit to reporting **SMC5/6's rank within the family**, not only its q, for the same
specificity reason as §49a: in a family this size, a small set of extreme-valued proteins can carry a
mean, and rank among comparable terms is the honest context.

**Registered expectation: we expect it to survive.** The z is large, the family correction at ~4,500
terms demands roughly 4.2 sigma and the observation is near 4.9, and the complex is internally coherent
— four subunits in, two specifically out (NSMCE2 at WT_LFC +0.27, NSMCE4A at +1.08). We state this
expectation knowing it inverts §45's published verdict, and if the test fails we will record that our
expectation was wrong rather than appeal to the z.

## What this cannot do

Four proteins of one complex in one pulldown remains one instrument, whatever the statistic. The nuclear
contamination question §45 tried and failed to control for is **still uncontrolled** — cohesin and
condensin are absent from this instrument's detected proteome, so the specificity control that would
distinguish "SMC5/6 specifically" from "nuclear carry-over generally" cannot be built here at all. A
surviving result would therefore be a lead requiring a different instrument, not a demonstrated
interaction.
