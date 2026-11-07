# Pre-registration: how long does a vault live, and do its subunits die together?

**Date:** 2026-11-07, before reading any half-life value. Claude drafted; Graham stated no predictions.

## Why
Article 1 §6 calls born-loaded-versus-loaded-on-demand "the central fork, and it decides everything".
Protein half-life is a direct readout: a particle that is built once, carries something, and is consumed
must turn over on the timescale of that cargo flux. A particle that is furniture does not.

Second question, sharper: **if MVP post-translationally stabilises PARP4 and TEP1 as orphan subunits**
(argon's H1: partial r 0.876 and 0.681 controlling for own mRNA), then all three should share a
half-life, because an assembled subunit lives as long as its particle and an unassembled one is degraded.

## Data
Mathieson et al. 2018, *Nat Commun* (PMC5814408), proteome-wide pulse-SILAC half-lives in **five primary
human cell types**, 2 replicates each; 8,805 proteins in the high-quality set. Half-life per protein per
cell type per replicate.

## Gates, before reading MVP
1. **Short-lived controls** MYC, FOS, JUN must sit in the bottom 25% of half-lives where measured.
2. **Long-lived controls** histones (H3, H4 family) or LMNB1 must sit in the top 25%.
If neither direction separates, the table is not being read correctly and nothing is reported.

## Primary test
MVP's **median half-life across cell types** and its **percentile in the proteome-wide distribution**.

- **LONG-LIVED (structural):** at or above the 75th percentile.
- **SHORT-LIVED (consumed):** at or below the 25th percentile.
- **ORDINARY:** between.

## Secondary — do the subunits die together?
Compare MVP, PARP4 and TEP1 half-lives. Under the orphan-subunit model their half-lives should be
similar, and the spread among them should be **smaller** than for random protein triplets matched on
abundance. Report the three values and the rank of their spread against 10,000 random triplets.

- **DEGRADE AS A UNIT:** spread below the 5th percentile of random triplets.
- **NOT A UNIT BY TURNOVER:** otherwise.

## What it decides
A long half-life argues against single-use born-loaded particles consumed on a signalling timescale and
for furniture, which fits #44 (no fitness coupling). A short half-life would make consumption plausible
and reopen the fork. Matched subunit half-lives would be a third independent line for #40.

## Limits
Primary immune cells, not the lung epithelium where vaults are most abundant. Pulse-SILAC half-lives
conflate degradation with dilution by division. A protein incorporated into a stable complex and one
that is simply never degraded look identical here.
