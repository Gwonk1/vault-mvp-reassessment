# Pre-registration: is the vault near the non-classical export route, or is this another composition artefact?

**Written 2026-11-07 after the exploratory §54c scan, before any corrected or controlled test.**
Committed before running `src/export_test.py`. §54c is explicitly unregistered and promotes nothing;
this is the test that decides.

## What §54c found, and why it cannot stand as it is

Eight export- and secretion-related terms were scanned against the anti-MVP pulldown with empirical
nulls. Two cleared nominal significance — `GOBP_DETOXIFICATION` (n=15, +0.970, p=0.005) and
`GOCC_LATE_ENDOSOME` (n=13, +0.740, p=0.027) — while classical secretion machinery did not, and §49c's
degradation terms are the most depleted in the whole 1,276-term scan.

Four reasons that is not yet a result:

1. **No correction.** Crude Bonferroni across eight leaves detoxification at 0.04 and late endosome at
   0.22.
2. **No physicochemical control.** §51 destroyed an apparently strong translation finding by matching on
   length and net charge. That control has not been applied here, and **detoxification enzymes are a
   distinctive protein class** (glutathione transferases, peroxiredoxins, superoxide dismutases — small,
   abundant, often basic), which is precisely the profile that produced the §51 artefact.
3. **Small n.** 13 and 15 members, the regime where §50 showed small-*n* means are dominated by a few
   extreme values.
4. **Term selection was ours.** We chose the eight terms to match a hypothesis, which is the §31 error:
   asking only about modules we already favour.

## Method

Same table, same parse, empirical nulls throughout (no normal approximation, per §50's addendum).

1. **Physicochemical control (primary).** Re-test `GOBP_DETOXIFICATION` and `GOCC_LATE_ENDOSOME`
   against randoms matched on **length decile and net-charge decile in addition to abundance decile** —
   identical machinery to §51. **If either dies, it dies**, as translation did.
2. **Unbiased replacement for our term selection.** Rather than eight hand-picked terms, scan **every**
   term with 10-500 members in the universe on the empirical statistic, Benjamini-Hochberg corrected,
   and report where detoxification and late endosome **rank** — the §49a specificity discipline. A term
   that is 300th of 1,276 is part of the pulldown's composition, not a finding.
3. **Member-level transparency.** For anything that survives, list every member protein with its
   WT_LFC, so a reader can see whether a 15-protein mean rests on two values.

## Gates

1. **Positive control:** the vault core (MVP, PARP4, TEP1 — verified present, house rule 7) must clear
   the fully length- and charge-matched control at p < 0.05, as it did in §51 (p = 0.024). A matching
   scheme that erases the bait is over-specified and the result is UNINFORMATIVE.
2. **Negative control:** `GOCC_RIBOSOME` must **fail** under the same matched control, reproducing §51's
   p = 0.184. If the ribosome signal comes back alive, the matching has not been applied correctly and
   nothing here is interpretable.
3. **Reachability, on the deciding statistic** (house rules 8 and 9): with 200,000 draws the empirical p
   floor is 5e-6 and n = 13-15 sets have ample spread, so both outcomes are attainable; and BH across
   ~1,276 terms needs a raw p near 4e-5 for the top rank, which §54c's uncorrected 0.005 does **not**
   reach — so this test can fail, and on the current numbers it is more likely to fail than pass.

## Outcomes, fixed now

- **SURVIVES** if a term clears the length- and charge-matched control at p < 0.05 **and** ranks in the
  top 2% of the unbiased 1,276-term scan **and** both gates hold. Then the vault sits near the
  non-classical export route, and Graham's export hypothesis has its first controlled support.
- **DIES** if the matched control removes it, exactly as §51 removed translation.
- **COMPOSITION** if it survives matching but ranks outside the top 10% of the unbiased scan: real but
  unremarkable, reported as part of what this pulldown contains.

**Registered expectation: we expect detoxification to die on the physicochemical control.** Small
abundant basic enzymes are the §51 profile, and 0.005 uncorrected will not survive a 1,276-term
correction. We expect late endosome to be composition at best. **We are stating this plainly because
the hypothesis is the user's and the result would be welcome, which is exactly when a registered
expectation matters most.**

## A separate, cheaper question this does not address

The literature appears not to have asked whether MVP is present in **feces, gut lumen contents, or
mucus itself** (§54b). That is a database query against published fecal and mucus proteomics, not an
analysis of this pulldown, and it is recorded as a standing item rather than folded into this test.
