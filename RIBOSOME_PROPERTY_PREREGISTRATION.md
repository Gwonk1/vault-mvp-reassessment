# Pre-registration: is the translation enrichment association, or just what ribosomal proteins are?

**Written 2026-11-07, before any physicochemical matching or formal compartment test.** Committed
before running `src/ribosome_property.py`. We found this problem in our own §49a output rather than
having it pointed out, and it threatens the one module-level finding we upgraded today.

## The problem

§49a upgraded cytoplasmic translation to probable on the strength of a coherent ribosomal family at the
top of an unbiased 1,276-term scan. Reading our own output more carefully:

| term | n | mean WT_LFC |
|---|---|---|
| `GOCC_MITOCHONDRIAL_LARGE_RIBOSOMAL_SUBUNIT` | 23 | **+0.560** |
| `GOCC_ORGANELLAR_RIBOSOME` | 45 | **+0.382** |
| `GOCC_RIBOSOME` | 134 | +0.314 |
| `GOCC_CYTOSOLIC_RIBOSOME` | 82 | **+0.272** |
| `GOCC_MITOCHONDRION` (whole compartment) | 191 | **−0.145** |
| whole universe | 1,205 | −0.273 |

**The mitochondrial ribosome is more enriched than the cytosolic ribosome**, while the mitochondrial
compartment as a whole is not enriched at all. Mitoribosomes sit inside mitochondria behind two
membranes; **a cytoplasmic 13 MDa particle cannot be bound to them.**

So the enrichment tracks *"is a ribosomal protein"* rather than *"is in the cytosol"* or *"is
mitochondrial"*. That is the signature of a shared physical property — ribosomal proteins are small,
strongly basic and abundant — rather than of polysome association. Grok's audit named the adjacent
version of this for the amoeba list: *"ribosomal proteins are also the standard lysine-rich TurboID
contaminant class."* The same logic applies to an affinity matrix.

## Tests

### 1. Compartment discrimination (primary)

Compare `GOCC_CYTOSOLIC_RIBOSOME` against `GOCC_MITOCHONDRIAL_RIBOSOME` / `GOCC_ORGANELLAR_RIBOSOME`
using the empirical matched-draw statistic of §50 (no normal approximation, per house rule 8's third
check and the §50 addendum).

**If the mitochondrial ribosome is enriched at or above the cytosolic ribosome, the polysome-association
reading dies** and the §40/§49a convergence is reinterpreted as a property of ribosomal proteins that
both instruments share.

### 2. Physicochemical matching (primary)

Recover sequences for the IP-MS universe from GENCODE v25 (gene name is pipe-field index **6**, which we
got wrong on the first attempt and state here). For each protein compute **length** and **net charge at
pH 7** from residue composition. Then re-test `GOCC_CYTOSOLIC_RIBOSOME` against random sets matched on
**length decile and charge decile in addition to abundance decile**.

**If cytosolic ribosome no longer clears, the enrichment is explained by what these proteins are.**

### 3. Gates

- **Rule 7:** sequences must be recovered for **at least 90%** of the 1,205-protein universe, or neither
  test runs. We have not yet run the corrected parse, so this is a genuine gate and not a formality.
- **Positive control:** the vault core (MVP 893 aa, PARP4, TEP1 — large, not basic) must still clear the
  length- and charge-matched control. If physicochemical matching erases the bait and its own subunits,
  the matching is over-specified and the result is UNINFORMATIVE.

### 4. Reachability, per house rules 8 and 9

Both outcomes are attainable on the statistic that will decide this. The empirical p floor at 200,000
draws is 5e-6, and cytosolic ribosome has n = 82 — far from the small-*n* resolution problem that broke
§50's 3-protein gate. A pass requires the matched draws to stay below +0.272 and a fail requires them to
reach it; neither is excluded by construction. **This check is run on the empirical statistic, which is
the statistic that decides — the omission that produced #218.**

## Registered expectation

**We expect the polysome-association reading to die.** The mitochondrial figure is already higher than
the cytosolic one in data we have published, the mitochondrial compartment as a whole is flat, and a
shared physicochemical property explains all three observations at once. We are stating this before
running because it reverses a finding we upgraded to probable hours ago, and because §40's seed-level
specificity — which remains unexplained by this hypothesis — is the one thing that might save it.

**What would save it:** if the cytosolic ribosome clearly exceeds the mitochondrial ribosome once both
are matched, and if cytosolic ribosome survives length- and charge-matching, then the association
reading stands and the mitochondrial signal is a smaller separate artefact.

## What this cannot do

Net charge from residue composition is a crude proxy for behaviour on an affinity matrix, and length and
charge do not exhaust the relevant properties. A surviving result would not prove association; a dying
one would not prove the ribosome is absent from vaults, only that this instrument cannot distinguish
association from composition. §40's co-elution result is a different instrument and is not tested here.
