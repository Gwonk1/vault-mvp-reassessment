# Pre-registration: is MVP unusually divergent for its phylogenetic reach?

**Date:** 2026-11-06. Drafted by Claude; Graham's claim under test is his own ("line up the vault
proteins of different animals and they're all different; I think that's unique"). Committed before any
alignment was scored.

## Question
Across eukaryotes, is MVP's sequence less conserved than other proteins that span the same evolutionary
distance? A chassis — constrained in shape but not in sequence — should sit at the divergent end.

## Prior
Against the claim, weakly. MVP falls into a single eukaryote-level orthologous group spanning 134
species, which means it stays recognisably itself over roughly 1.5 billion years. Recognisable and
well-conserved are different things, so the question is real.

## Data
eggNOG 5.0 eukaryote level (2759) trimmed alignments, one per orthologous group. MVP = `2QPP0`.

## Statistic
Mean pairwise percent identity over aligned columns, computed on a capped random sample of 300 sequence
pairs per group (seed 20261106) so large groups do not dominate the cost. Columns where either sequence
has a gap are skipped; pairs with fewer than 50 shared ungapped columns are discarded.

## Matched comparison
Groups matched to MVP on **number of species (±15%)** and **alignment length (±30%)**, at least 200 of
them. MVP's percentile within that matched distribution is the result.

- **UNUSUALLY DIVERGENT:** at or below the 10th percentile of identity. Supports the chassis reading —
  shape conserved, sequence free.
- **TYPICAL:** between the 10th and 90th. The uniqueness claim does not hold.
- **UNUSUALLY CONSERVED:** at or above the 90th. Argues something about the sequence itself is under
  selection, which would cut against both the chassis and the vestigial readings.

## Gate, before reading MVP
Two controls must land where known biology puts them: a histone (**H3-3A/H3F3A**) or a core ribosomal
protein must be at or above the 75th percentile of identity, and a rapidly evolving group must be below
the 25th. If the method cannot separate those, the MVP figure is reported as uninformative.

## Also reported
TEP1 and PARP4 group identities, for context only. Their groups are mixed (NWD1/NWD2 and PARP1-3), so
they cannot carry weight.

## Limits
Trimmed alignments discard poorly aligned regions, which compresses apparent divergence and does so for
every group alike. Percent identity ignores branch lengths, so a group sampled in fast-evolving lineages
looks divergent for reasons unrelated to constraint; species-count matching only partly controls this.
This measures sequence conservation, not structural conservation, and the chassis claim is about shape.
