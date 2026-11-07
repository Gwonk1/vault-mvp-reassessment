# Pre-registration: redo every dichotomised contact test on the continuous measurement

**Written 2026-11-07 after the Grok audit, before computing any term statistic beyond the single
translation mean already reported in §48a.** Committed before running `src/continuous.py`.

## Why, and the bias this is designed to avoid

#203 established that our contact test destroyed a real signal by dichotomising a continuous
measurement at `LWTP > 1.3`: translation proteins average **+0.228 log2** against **−0.316** for the
rest of the detected proteome, p = 0.004, where the dichotomised test returned p = 0.195.

**That correction arrived in the direction we wanted.** Applying it only to translation would be the
exact fork Grok identified in our handling of the amoeba list — honouring a rule in one direction and
not the other. So this re-analysis is applied **uniformly to every term we previously tested on the
dichotomised interactor set, including every term we would prefer to see die**, and to the full
unbiased scan.

## Method

Same table and parse as §13, §41, §43-§46. For each GO term, the statistic is the **mean `WT_LFC` of
its members present in the 1,205-protein universe**, with no threshold anywhere. Significance is the
percentile of that mean against **2,000 random gene sets matched on set size and on the table's
abundance-proxy decile** — the same matching used in §37, §41 and §48a.

Two analyses:

1. **Targeted:** every term previously tested in a contact instrument — cytoplasmic translation,
   ribosome, translation, ruffle, actin filament organisation, mitochondrion, the SMC5/6 complex, SUMO
   ligase complex, and the three degradation terms from §46d.
2. **Unbiased:** all 1,276 terms with 10-500 members in the universe, Benjamini-Hochberg corrected —
   the continuous counterpart of §44, which found zero terms dichotomised.

## Positive-control gate

**The vault core must show a large positive shift.** MVP, PARP4 and TEP1 together must have a mean
`WT_LFC` above the 99th percentile of matched draws. These three are the bait and its two known
subunits at WT_LFC +7.62, +8.66 and +6.27, so a continuous statistic that cannot see them cannot see
anything, and the result is **UNINFORMATIVE**.

**Second gate, against the failure mode of §45b:** every protein named in that control is verified
present in the universe before this file is committed. Confirmed — MVP, PARP4 and TEP1 are all present
(house rule 7).

**Third gate, calibration:** the distribution of matched-draw percentiles across all 1,276 terms must be
approximately uniform. If it is skewed, the matching is broken and no term-level claim can be made.

## Specificity, which is the real question

A continuous statistic is more sensitive than a dichotomised one, so **more terms will reach nominal
significance, and that is not evidence for any of them.** The question §40 asked of seed proteins is the
one to ask here: **where does translation rank among all 1,276 terms?** We pre-commit to reporting
translation's percentile within the full distribution of term shifts, not merely its own p-value.

If translation is one of two hundred terms with a positive shift, the §48a result is a property of the
pulldown's general composition and the §40 convergence is weaker than it now looks. **If it is in the
top handful, the convergence across instrument classes is real.**

## Outcomes, fixed now

- **Translation's convergence is corroborated** if it sits in the top 2% of all 1,276 terms by matched
  percentile. **Weakened** if it sits outside the top 10%.
- **Cortical actin becomes a live claim** if actin filament organisation or ruffle clears the same bar
  translation clears. §48b left it unresolved; this can resolve it in either direction.
- **The SMC5/6 and degradation terms get the same chance**, and if either clears while translation does
  not, we follow the data.
- **Anything that reaches nominal significance but sits outside the top 10% of terms is reported as part
  of the pulldown's general composition**, not as a finding.

**Registered expectation:** we expect translation to clear comfortably, since its dichotomised failure
was already shown to be an artefact. We expect **actin filament organisation to clear nominal
significance and to fail the specificity bar**, because its dichotomised numbers (7 vs 4.75) were weak
in a way translation's (a +0.544 log2 shift) was not. We expect the degradation terms to stay flat,
since §46d's counts were *below* expectation rather than merely unremarkable. We have no expectation for
SMC5/6.

## What this cannot do

A mean shift across a term's members is still an aggregate: it cannot distinguish a few strongly
enriched proteins from a uniform mild shift, and we will report the member-level distribution for
anything that clears. It remains one experiment in one cell line, and an immunoprecipitation still
reports what survives a wash — the correction here is to our statistics, not to the instrument's
physics.
