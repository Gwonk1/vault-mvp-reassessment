# Pre-registration: does a seed's own length and charge explain its translation-rich co-elution tail?

**Written 2026-11-07, before computing any correlation or matched percentile.** Committed before
running `src/seed_property.py`. This applies §51's successful method to the other instrument, which is
the uniform-application discipline #203 and house rule 8 demand.

## First, a test we are declining and why

§52b named an untested hypothesis — that the residual lift in large cytoplasmic assemblies reflects
**compartment** rather than mass. We tried to build it and **house rule 7 stopped it.** The MSigDB
collection in this repository is a filtered subset in which the root compartment terms are absent:
`GOCC_CYTOSOL`, `GOCC_CYTOPLASM`, `GOCC_NUCLEUS`, `GOCC_NUCLEOPLASM`, `GOCC_NUCLEAR_LUMEN` and
`GOCC_CHROMOSOME` all return nothing. The available proxies are asymmetric — nuclear terms cover 1,314
/ 859 / 415 proteins against 309 / 20 for cytoplasmic ones — so a classifier built from them would label
far more seeds nuclear than cytoplasmic and leave many unlabelled. **A compartment test needs full GO
annotations we do not have locally, and we are not running it on a lopsided proxy.** It stays an
untested hypothesis, as §52b recorded.

## The test we are running

§51 killed the contact-instrument translation result by showing that **length and net charge** account
for it: ribosomal proteins are 2.6x shorter and 44x more basic than the median detected protein. The
same property could in principle drive co-elution scores, since like-behaving proteins co-migrate.

**But MVP's own profile is the opposite of a ribosomal protein's**, and we record the numbers before the
test:

| protein | length | charge per 1,000 residues |
|---|---|---|
| **MVP** | **893** (80.1st percentile of seeds) | **−28.5** (16.4th percentile) |
| RPL7 | 248 | +162.6 |
| RPS6 | 249 | +169.3 |
| 150 random seeds, median | 452 | −2.5 |

So MVP is **longer than 80% of eligible seeds and more acidic than 84% of them.** If a like-binds-like
physicochemical mechanism produced ribosome-rich tails, MVP should be among the *least* likely seeds to
have one — and it is at the 98.0th percentile.

Sequence coverage, checked before committing (house rule 7): **146 of 150 random seeds, 97.3%**, and all
twelve named seeds.

## Method

For each of the 146 random seeds with a recovered sequence, compute length and net charge at pH 7 from
residue composition, exactly as §51 did, and pair it with that seed's §40 translation-fold.

1. **Correlation (primary):** Spearman ρ of translation-fold against charge, and against length, across
   the 146 seeds.
2. **Matched percentile (primary):** MVP's translation-fold percentile among the **30 seeds nearest to
   MVP in standardised (length, charge) space**. This is the direct analogue of §51's matched null —
   if MVP's tail is explained by what MVP is, matching on what MVP is should erase its lead.

## Gates

1. **The axis must be measurable:** RPL7 and RPS6 must both be above the 95th percentile for fold
   *and* in the top quartile for charge and the bottom quartile for length. Verified true above, so
   this gate is already known to pass and we say so rather than pretending otherwise.
2. **Reachability, on the deciding statistic** (house rules 8 and 9): MVP's percentile among 30
   neighbours can take any value from 0 to 100 in steps of about 3.3, so both outcomes are attainable;
   and Spearman ρ over 146 points has a two-sided 0.05 threshold near |ρ| = 0.16, well inside the
   achievable range.

## Outcomes, fixed now

- **§40 STRENGTHENED** if ρ with charge is positive and significant — meaning basic seeds do have
  ribosome-rich tails — **while MVP stays above the 90th percentile among its 30 physicochemical
  neighbours.** MVP would then be producing a ribosome-rich tail *against* the trend its own
  composition predicts, which is harder to explain as an artefact than the raw 98th percentile was.
- **§40 EXPLAINED AND WITHDRAWN** if MVP falls below the 75th percentile among its neighbours. The tail
  would then be a property of seeds like MVP, and the last translation result closes.
- **NEITHER** if there is no correlation and MVP stays high: the physicochemical axis is simply not the
  mechanism, one more alternative is eliminated, and §40 remains unpromoted exactly as §52c left it.

**Registered expectation: we expect the third outcome.** MVP's profile is so far from ribosomal that we
doubt this axis organises the tails at all, and the 30 nearest neighbours in (length, charge) space will
mostly be ordinary large acidic proteins with unremarkable tails. We note that this expectation, if
borne out, **promotes nothing** — it eliminates a candidate and leaves §40 where it was.

## What this cannot do

Length and net charge from composition do not capture shape, post-translational modification, or
assembly state, and a seed's monomer properties are a poor proxy for the behaviour of the particle it
belongs to — MVP's 893-residue monomer says little about how a 13 MDa 78-mer migrates. A null here
removes one mechanism, not the class of mechanisms.
