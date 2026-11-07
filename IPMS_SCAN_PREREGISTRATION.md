# Pre-registration: unbiased scan of the vault's physical interactome

**Written 2026-11-07, before computing any term statistic on the IP-MS interactor set.** Committed
before running `src/ipms_scan.py`.

## Why

§41 tested five hypotheses against the anti-MVP pulldown one at a time — translation, ribosome, ruffle,
actin, mitochondrion — and found nothing enriched. But that repeats the structural error §31 was built
to avoid: **we only ever asked the contact instrument about modules we already favoured.** We have never
asked it what the vault's physical neighbourhood actually contains.

This is the contact-instrument counterpart of the §31 scan, and the last obvious question we can put to
data already in hand. The instruments have been exhausted (§42); the hypotheses have not.

## Method

`argon/raw/lodwick_supp_4.xlsx`, sheet `Fig. 5c-d`, parsed exactly as §13, §41 and §43 parsed it.
Universe: the 1,205 proteins in the table. Target set: the **88 WT vault interactors**, defined as §13
defined them (`WT_LFC > 0`, `LWTP > 1.3`) with no redefinition.

Scan **every** MSigDB GO BP and CC term with between 10 and 500 members present in the universe, by
hypergeometric enrichment among the 88, Benjamini-Hochberg corrected across the scan. Any term reaching
q < 0.05 is then re-tested against **200 random gene sets matched on set size and on the table's own
abundance-proxy decile**, as §37 and §41 did, and only terms clearing both are reported.

## Power, stated before the result

**88 interactors in a 1,205-protein universe is a small target set.** A term with 30 members in the
universe expects 2.2 hits; detecting enrichment needs roughly a doubling or more. **This scan can find
a large, concentrated physical neighbourhood and cannot find a diffuse one.** We state that now so that
a null is read correctly, and so we cannot later present a null as stronger than it is.

## Calibration gate, which replaces a positive control

There is no good positive control here: the vault's only known physical components are MVP, PARP4 and
TEP1, and three proteins cannot calibrate a term-level scan. So we calibrate on the null instead.

**Twenty random 88-protein subsets of the same universe must produce a median of zero terms at
q < 0.05.** If random subsets of this table generate spurious enrichments, the scan is miscalibrated and
the result is **UNINFORMATIVE** whatever MVP's interactors do. The observed count for the real
interactor set is reported against that random distribution, not only against the q threshold.

## Outcomes, fixed now

- **A physical neighbourhood exists** if one or more terms clear q < 0.05 *and* matched-random
  specificity p < 0.05, with the real count exceeding the 95th percentile of the random subsets.
- **No detectable physical neighbourhood** if zero terms clear. Given everything else in this project,
  this would be the expected and the most informative outcome: it would mean the vault's physical
  interactome, as measured by the one instrument that recovers all three of its subunits, consists of
  its subunits plus a short list of individual proteins and **no functional module at all**.
- Terms clearing q but failing matched-random specificity are reported as abundance artefacts, not
  findings.

**Registered expectation: we expect zero terms.** Three hypothesised modules have already died in this
instrument class, the 88-protein target set is small, and ANXA2 and S100A10 — the only non-subunit
survivors (#182) — are two proteins, not a module. If something does clear, it will not be anything we
proposed, and that is the only circumstance in which it would be worth much.

## Secondary, descriptive

The 88 interactors listed in full, with WT_LFC and PARP4-dependence, so the physical interactome is on
the record as a list regardless of whether any term describes it. This is the thing we should arguably
have published in §13 and did not.

## What this cannot do

An IP reports what survives a wash, so transient and weak association is absent by construction, and a
null here does not mean the vault touches nothing in a cell. It is a single experiment in a single cell
line. And enrichment among 88 proteins cannot distinguish a real small module from a coincidence of
three or four co-annotated proteins — which is why matched-random specificity is required on top of q.
