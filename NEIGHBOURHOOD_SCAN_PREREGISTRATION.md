# Pre-registration: an unbiased, replication-gated scan of MVP's co-abundance neighbourhood

**Written 2026-11-07, before computing any term-level statistic.** Committed before running
`src/neighbourhood_scan.py`.

## Why unbiased, and why now

Co-abundance has now been used four times to ask whether MVP has a functional neighbourhood, each time
by nominating a module we already favoured and testing that one: §11 nominated membrane repair, §13 and
§15 failed to confirm it physically, §28 reversed it after a confound was removed, §30 killed it on
replication. **Four attempts, one of which I described to Graham as the finding of the day, and it is
gone.**

The failure mode is structural, not statistical. Selecting the module first and testing it afterwards
means every result is one degree of freedom away from a story we wanted. The honest instrument is the
reverse: **scan every gene set, require replication across independent cohorts, and let the data
nominate.** If the answer is that nothing replicates, that is a clean and useful negative — it would
mean co-abundance supports no neighbourhood for MVP beyond its two confirmed partners, and we should
stop using it on this question.

## Data

Five independent proteomic datasets already in this repository: the four CPTAC cohorts that passed
control gates in §30 (`brain_cptac_2020`, `coad_cptac_2019`, `gbm_cptac_2021`, `ucec_cptac_2020`) plus
`ccle_broad_2019`. **Analysed separately and never pooled.**

## Method

Per dataset, exactly as §28/§30: residualise every protein at sample level on the N:C proxy (mean z of
cytosolic RPL/RPS minus nuclear HNRNP/SRSF/SF3B/SMC) plus available proliferation markers; Spearman
each residualised protein against residualised MVP; take MVP's top 200.

Then test **every** MSigDB GO BP and CC term with between 10 and 500 members present in that dataset,
by hypergeometric enrichment in the top 200, Benjamini-Hochberg corrected **within** each dataset.
Gene sets are external and unmodified. **No term is chosen, excluded or redefined by us.**

## Positive-control gates

**Per dataset,** the same two as §30: PARP4 within MVP's top 100, and PSMA1 recovering at least 8 of 25
proteasome subunits in its own top 50. A dataset failing either is excluded and reported as excluded.

**For the scan design itself:** repeating the identical scan seeded with **PSMA1** instead of MVP must
return at least one proteasome term replicating in a majority of included datasets. If a scan of this
construction cannot recover the proteasome from PSMA1, it cannot detect a real complex and **the whole
analysis is reported UNINFORMATIVE** whatever MVP does.

## Primary outcome, with thresholds fixed now

For each term, count datasets where it reaches **q < 0.05**.

- **Replicating neighbourhood exists** if one or more terms reach q < 0.05 in a **majority** of included
  datasets (3 of 5, or 3 of 4 if one is excluded).
- **No replicating neighbourhood** if zero terms do.
- Terms replicating in exactly half are reported as **suggestive and unresolved**, not promoted.

## Registered prediction, so it is on the record before the result

**I predict zero or very few terms replicate in a majority.** Given that the membrane module cleared
0.05 in only 1 of 4 cohorts in §30 and that three of those returned p = 1.00, I expect MVP's
co-abundance neighbourhood beyond PARP4 and TEP1 to be dataset-specific. **If I am right, the conclusion
is that co-abundance is the wrong instrument for this question and we stop using it.** If something does
replicate, it will have nominated itself, which is worth considerably more than anything we have
proposed by hand.

## How this will be weighed

Output is a ranked table of every term by replication count, so the result is a graded
eliminate/probable list rather than a binary verdict — including the terms we have previously favoured,
whose position will be reported whether flattering or not.

## What this cannot do

Co-abundance is not physical contact and never was; §13's IP-MS remains the only contact test and it
missed at p = 0.058. A replicating term would be a reproducible association, not an interaction. This
scan also cannot address the EMT question left open in #109.
