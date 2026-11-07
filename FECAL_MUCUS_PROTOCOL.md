# Declared protocol: is MVP reported in human stool or mucus proteomes?

**Written 2026-11-07, before reading any protein list.** This is a literature and database lookup
rather than a statistical test, so it has no null distribution — but it needs one thing a lookup is
usually not given, and that is the reason for writing it down.

## The question

#235 recorded that we could find no report of MVP in the human fecal proteome or in gut mucus, while
MVP is independently documented in exosome preparations, released from cells by a non-exosomal route,
and present in extracellular cement in the Atlantic salmon louse. Graham's export hypothesis predicts
MVP should be findable in gut lumen contents and in mucus itself.

## The gate, which is the whole point of declaring this

**"MVP was not reported" is uninformative unless the dataset could have reported it.** A stool
proteomics study that identifies 80 host proteins, all of them abundant plasma leakage markers, says
nothing about a cytoplasmic 100 kDa protein.

**For each dataset, we record first and independently of MVP:**

1. the number of **human** proteins identified;
2. whether the list contains **intracellular proteins of comparable abundance class** — we fix three
   now: `ACTB`, `GAPDH` and `HSPA8`, all cytoplasmic, all more abundant than MVP in most cells;
3. whether it contains known **secreted/lumenal** controls, e.g. `ALB`, `LTF`, `LCN2`, `MUC2`.

**A dataset qualifies as able to answer the question only if at least two of ACTB, GAPDH and HSPA8 are
present.** If the intracellular controls are absent, the dataset only sampled secreted protein and
MVP's absence is expected regardless of whether vaults are exported. Such datasets are recorded as
**UNINFORMATIVE** and are not counted as negatives.

## Datasets to check, fixed now

Human stool: **PXD000506** (Lichtman et al., *Host-centric proteomics of stool*), **PXD021424**
(dietary protein, faecal self-proteome), **PXD057120** (Crohn's/UC, ~1,250 proteins by SWATH),
**PXD001573** (Tanca et al., metaproteomics with differential centrifugation). All four are
ProteomeXchange `submissionType: PARTIAL`, so no processed identification files exist and the protein
lists must come from each paper's own tables.

Mucus: any human airway or intestinal mucus proteome we can reach. We have no accession in hand and
record that as a limit rather than substituting a related matrix.

## Outcomes, fixed now

- **MVP REPORTED** in one or more qualifying datasets: the first direct evidence that vaults or MVP
  reach the gut lumen, and a result the literature does not currently contain. We would then ask
  whether PARP4 and TEP1 appear alongside, since MVP alone could be degradation product rather than a
  particle.
- **MVP ABSENT from qualifying datasets**: recorded as a real negative, bounded by the number of
  qualifying datasets and their depth. This would **not** refute export — mucus and lumen are harsh,
  proteolytic environments and a shed particle may simply not survive — but it would remove the easy
  version of the prediction.
- **NO QUALIFYING DATASET**: the question stays open and we say the lookup failed rather than reporting
  an absence.

**Registered expectation: we expect MVP to be absent or the datasets not to qualify.** Stool
proteomics is dominated by microbial and plasma-leakage protein, host coverage is typically shallow,
and §57 has just shown us how easily we read structure into thin data. **If MVP is present in a
qualifying dataset, that is Graham's hypothesis scoring a point we did not expect it to score.**
