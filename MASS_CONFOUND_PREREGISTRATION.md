# Pre-registration: is MVP's co-elution tail translation-rich because of association, or because of mass?

**Written 2026-11-07, before computing any new seed's translation-fold.** Committed before running
`src/mass_confound.py`. This tests the one translation result still standing after §51.

## The problem

§40 found MVP's top-200 co-elution partners enriched for `GOBP_CYTOPLASMIC_TRANSLATION` at the
**98.0th percentile of 150 random seeds**, with glycolytic controls at the 26th-79th and MVP's own
SPFH relatives at the 41st-70th. §51 withdrew the *contact* corroboration but explicitly did not test
this, because seed-level specificity is not obviously explained by a physicochemical property.

**But co-fractionation separates by apparent mass, and §40 controlled for degree only — by a floor of
≥5,000 scored partners, not a matched distribution — and not for mass at all.** The vault is a 78-mer
of about **13 MDa**; polysomes are also multi-megadalton. Very few things in a cell lysate are that
large, so MVP and polysomes may occupy the same fractions without touching.

This is the co-fractionation analogue of §51's length-and-charge confound: a property shared with the
term's members that the matching never removed.

## What we already know, stated before the test

Two facts in hand cut against the confound and we record them now rather than after:

1. **MVP's degree is 10,614 — only the 73.8th percentile among the 9,773 eligible seeds** (median
   9,462, max 11,803). MVP is not an unusually promiscuous co-eluter, and every large-assembly
   comparator below has a *higher* degree than MVP. So a simple degree effect cannot produce MVP's
   98th percentile.
2. **§40's own negative gate was a large assembly.** PSMA1 is a 26S proteasome subunit, roughly
   2.5 MDa assembled, and it sat at the **70th percentile** — below the bar. One multi-megadalton
   assembly has already failed to show the effect.

## Method

Reproduce §40's statistic exactly: for a seed, take its 200 highest-scoring CFdb partners and count
how many are `GOBP_CYTOPLASMIC_TRANSLATION` members, divided by the expectation from the term's share
of the scored universe. The random reference distribution is regenerated with §40's own seed list and
RNG so the percentiles are directly comparable.

Then evaluate **35 new comparator seeds drawn from seven assemblies of known mass**, all verified
present in CFdb above the ≥5,000-partner floor before this file was committed (house rule 7):

| assembly | approximate assembled mass | seeds |
|---|---|---|
| nuclear pore complex | ~110 MDa | NUP133, NUP93, NUP205, NUP188, NUP107, NUP160, NUP214 |
| 26S proteasome | ~2.5 MDa | PSMA1, PSMD1, PSMC1 |
| spliceosome | ~1.5 MDa | SF3B1, PRPF8, SNRNP200, EFTUD2, SF3B3 |
| cytoplasmic dynein | ~1.4 MDa | DYNC1H1, DCTN1, DYNC1I2, ACTR1A |
| condensin / cohesin | ~1 MDa | SMC1A, SMC2, SMC3, SMC4, NCAPD2 |
| TRiC/CCT chaperonin | ~1 MDa | CCT2, CCT3, CCT4, CCT5, CCT6A, CCT7, TCP1 |
| clathrin coat | large, polymeric | CLTC, CLTA, AP2M1, AP2B1 |
| **small-complex negatives** | < 300 kDa | FLOT1, FLOT2, STOM, GAPDH, ENO1, PKM |

## Gates

1. **Sensitivity:** RPL7 and RPS6 must exceed the 95th percentile, as in §40. A statistic that cannot
   see ribosomal proteins in their own tails cannot adjudicate anything.
2. **Specificity floor:** the six small-complex negatives must have a **median below the 80th
   percentile**. All six are verified present above the degree floor.
3. **Reachability, on the deciding statistic** (house rules 8 and 9, the omission that produced #218):
   the statistic is a percentile against 150 seeds, so values from 0 to 100 are all attainable by
   construction, and 35 comparators give a median whose standard error is roughly 3 percentile points.
   Both outcomes are reachable.

## Outcomes, fixed now

- **MASS CONFOUND CONFIRMED** if the median percentile of the 35 large-assembly seeds is **above 75**,
  or if any assembly's median exceeds MVP's 98.0. §40's result would then be a statement about
  apparent mass, the last translation finding would fall, and the whole translation thread would close
  as an artefact in both instrument classes.
- **MVP SURVIVES AS SPECIFIC** if the large-assembly median is **below 60** while MVP remains near 98
  and the gates hold. Mass would then be excluded as the explanation, and MVP's co-elution tail would
  be the one translation result left standing — single-instrument, but controlled for degree, abundance
  and now mass.
- **EQUIVOCAL** between those bars: promotes nothing, and we say the question is open rather than
  picking the reading we prefer.

**Registered expectation: we lean to MVP surviving, with a reduced margin.** PSMA1 at 2.5 MDa already
sat at the 70th percentile, and MVP's degree is unremarkable. But we expect some large assemblies —
particularly the spliceosome and TRiC, which are genuinely RNA- and nascent-chain-adjacent — to score
above the median, so we expect the large-assembly distribution to be shifted upward without reaching
MVP.

## What this cannot do

Assembled mass is itself a crude axis: these complexes differ in shape, stability through
fractionation, and whether they survive lysis intact, and a nuclear assembly is in a different
compartment from a cytoplasmic one before any mass argument applies. A surviving MVP would remain one
instrument's finding with no contact corroboration, since §51 removed that. This cannot establish
association; it can only remove or fail to remove one specific alternative explanation.
