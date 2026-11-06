# Deviations: persister passenger test

Written after inspecting cell counts per model, before any expression value was computed.

1. **Three usable models, not seven.** GSE150949's pooled matrix holds 8 cell lines, but only
   A375_SKIN, HT29_LARGE_INTESTINE and PC9_LUNG have at least 100 cells in both the naive and the
   drug-treated arm. HCC827 has no naive cells in this matrix; BT474 (28 treated), EFM192A (19),
   MMACSF (50) and COLO829 (87) fall below the cutoff and are reported descriptively only.
2. **Majority rule restated.** The pre-registered "at least 5 of 7" becomes **at least 2 of 3**
   (two-thirds of usable models, the same proportion). The gate becomes 2 of 3 on the same rule.
   With three models the test is weaker than planned, and a 2-of-3 result is correspondingly weak.
3. **Persister definition.** `sample_type` of cycling or non-cycling at day 10 is the treated arm;
   naive is the untreated arm. Both persister classes are pooled, since the pre-registration asks
   about the drug-surviving state and not about cycling rate. Split results are reported too.
4. **Δ computed as a regression coefficient.** Raw Δ is the treatment coefficient from
   `y ~ 1 + treated`, identical to the difference in means. Residualized Δ is the treatment
   coefficient from `y ~ 1 + IFNG_score + IFNA_score + treated`, which is equivalent to the
   pre-registered residual method and numerically more stable.
5. **Replication arms** from GSE149383: PC9 D0 vs D3 erlotinib (10x), M14 D0 vs D3 vemurafenib
   (Drop-seq), and the Drop-seq PC9 time course D0 vs D11 erlotinib. These are 3-day and 11-day
   exposures, shorter than the primary's 10-day sorted persisters.
