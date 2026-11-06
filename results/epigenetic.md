# Epigenetic lookup (plan 3d): Qiu 2023, GSE219179

**Pre-registered positive:** gain of H3K4me1 and/or ATAC at the Mvp promoter or a linked element in
ICB-resistant vs parental cells, comparable to positive control ISGs and above random-gene background.

**Result: negative. Mvp shows no IFN-memory chromatin signature in this model.** Mouse B16/Res499 only.

| Check | Mvp | Controls |
|---|---|---|
| Strict IFN-IMD gene list (Qiu Table 3) | absent | Oas1a, Oas1g, Oas1b, Oasl2, Ifit1, Ifit3, Usp18, Cd274 present |
| Inclusive IFN-IMD list (Table 4) | present, nearest IMD peak 730 kb from TSS | also listed; list appears broad, 1,820 genes |
| Resolved-domain list (Table 5) | present, nearest resolved peak 152 kb from TSS | Oas1a, Oas1g, Mx1, Usp18, Irf7 also listed |
| IMD or resolved peak within 30 kb of Mvp | none (0 of 10 ATAC peaks) | |
| ATAC gain at promoter, Res499 vs B16 (genome percentile) | -0.02 (39th) | Oas1a 94th, Oas1g 91st, Ifit1 88th, Usp18 85th, Irf7 97th |
| STAT1-dependent ATAC at promoter, percentile | 63rd | Oas1a 100th, Oas1g 100th, Ifit1 99th, Usp18 99th |
| STAT1-dependent ATAC, best peak in locus, percentile | 17th | Oas1a/g 99.9th, Ifit1 96th, Irf7 93rd |
| H3K4me1 gain at promoter, percentile | 79th (+0.06) | Oas1g 82nd, Usp18 64th, Ifit1 38th, Irf7 94th |
| H3K4me1 STAT1 dependence at promoter, percentile | 78th | Oas1a/g 99.8+, Ifit1 98th |
| Best H3K4me1 peak gain, percentile of peaks | 92nd (+0.08, +7 kb upstream) | not STAT1 dependent (35th) |
| ATAC-RNA coupling rank (Qiu Fig 2D source data) | 18,993 of 21,069, R² 0.004 | Oas1g 1st, Oas1a 17th, Ifit3 61st, Ifit1 85th |
| RNA Res499 vs B16 | +0.08 rlog (78th) | Oas1a +0.51, Usp18 +0.60, Stat1 +0.43 |
| RNA STAT1 dependence | +0.18 rlog (92nd, but small) | Ifit3 +2.43, Stat1 +2.50, Oas1a +1.58 |

Reading: a weak H3K4me1 gain at and just upstream of the promoter is the only item leaning positive. It
is small, STAT1 independent, and is not accompanied by accessibility gain. Mvp RNA barely moves with
STAT1 loss in these cells (about 13% on the rlog scale), where true chronic-program genes lose
3- to 5-fold. Caveat: replicates are n=2 for CUT&RUN, the values are small vst differences, and this is
a single mouse melanoma line in culture, so this is context, as pre-registered, and does not override
the human verdict. Scripts: `src/epi_lookup.py`, `src/epi_rna.py`.
