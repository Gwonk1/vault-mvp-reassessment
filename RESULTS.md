# Results: MVP does not belong to the chronic interferon resistance program

Run 2026-11-06 on public data. Predictions committed first (`PREREGISTRATION.md`, commit 837a38c); gene
sets and acquisition code frozen second (c6a7888); deviations in `DEVIATIONS.md`.

## Verdict under the pre-registered rules

**The prediction failed.** It said MVP would track ISG.RS more than IFNG.GS within malignant cells. In no
dataset, model, or compartment did MVP come out CHRONIC.

**Which outcome obtained:** ACUTE, not specific, in lung malignant cells, the pre-registered single-cell
test. "Not specific" matters: MVP leans toward IFNG.GS at the 29th genome percentile, and the average
gene leans the same way. The better summary is that MVP is an interferon-associated gene in malignant
cells that sits on neither side of the acute/chronic split.

| Test | Label | β(ISG.RS) | β(IFNG.GS) | Δ (95% CI) | Genome percentile of Δ |
|---|---|---|---|---|---|
| Bulk ICB pool, 7 cohorts, 686 patients (screen) | ACUTE | -0.06 | +1.05 | -1.09 (-1.64, -0.54) | 7.6 |
| **Lung malignant, 21 patients, 24,784 cells (verdict)** | **ACUTE, not specific** | +0.035 | +0.17 | -0.11 (-0.18, -0.05) | 29 |
| Melanoma malignant, 14 patients, 2,018 cells (replication) | BOTH/UNRESOLVED | +0.11 | +0.20 | -0.09 (-0.22, +0.04) | 64 |
| Mouse chromatin lookup (context) | Negative | | | | |

Consequences, as committed in advance:

- **Signaling-brake layer:** the abandonment condition is met for its "member of the chronic program"
  claim. This test can only speak to that claim. Section 6 says what stays open.
- **Containment layer:** its testable prediction here, anti-correlation with both sets, failed. MVP
  rises with interferon state in malignant cells: within-patient Spearman ρ = +0.23 (ISG.RS) and +0.29
  (IFNG.GS) in lung, +0.23 and +0.28 in melanoma. This does not refute containment as a physical function.

## 1. Epigenetic lookup

Mvp has no IFN-memory signature in Qiu's B16/Res499 model. It is absent from the strict memory-domain
list. The nearest memory domain is 730 kb from its TSS, and no memory or resolved peak lies within 30 kb.
Promoter accessibility sits at the 39th percentile for gain (Oas1a 94th) and shows no STAT1 dependence
(63rd; Oas1a 100th). Mvp RNA falls about 13% with STAT1 loss, against 3- to 5-fold for true program genes.
A small H3K4me1 gain near the promoter is the only item leaning positive, and it is STAT1 independent.
Details in `results/epigenetic.md`. This was one mouse line, so it is context only.

**The plan expected this lookup could settle the question. It could not on its own, but it agrees with
the human data.**

## 2. Bulk screen

ACUTE holds under the primary model, with TMB added (5 cohorts), with ISG.RS restricted to its 24 Hallmark
genes, and with any one cohort dropped. **It is not robust to the other named checks:**

| Specification | Label | Δ (95% CI) |
|---|---|---|
| Primary | ACUTE | -1.09 (-1.64, -0.54) |
| TMB added | ACUTE | -0.97 (-1.43, -0.51) |
| ISG.RS, 24 Hallmark genes only | ACUTE | -1.00 (-1.49, -0.52) |
| No covariates | BOTH/UNRESOLVED | -0.30 (-0.63, +0.04) |
| ssGSEA scoring | BOTH/UNRESOLVED | -0.46 (-1.02, +0.11) |
| Hallmark IFN-α vs IFN-γ | NEITHER | +0.01 (-1.20, +1.22) |
| ISG.RS minus IFNG.GS as one predictor | no association | β +0.09 (-0.08, +0.25) |

**The plan says collinearity must be declared if the ratio and the adjusted model disagree. They
disagree.** VIF for IFNG.GS is 11 to 23, the ISG.RS/IFNG.GS correlation is 0.74 to 0.90, and a β above 1 is
a sign of that. The bulk ACUTE magnitude should not be believed. What holds across all specifications is
β(ISG.RS) with a CI spanning zero and no Δ significantly above zero. The tertile stratification had 0 to 4 samples per
cohort in the ISG.RS-high/IFNG.GS-low cell and is uninformative.

## 3. Single cell

Within-patient models, combined across patients. Depth-adjusted runs were added as a sensitivity check.

| Compartment | Patients | Label | Δ (95% CI) | Genome percentile |
|---|---|---|---|---|
| Lung malignant | 21 | ACUTE | -0.11 (-0.18, -0.05) | 29 |
| Lung malignant, depth adjusted | 21 | ACUTE | -0.09 (-0.14, -0.03) | 9.7 |
| Lung primary tumor, tS labels included | 13 | ACUTE | -0.10 (-0.18, -0.02) | 25 |
| Lung brain metastases | 10 | BOTH/UNRESOLVED | -0.06 (-0.13, 0.00) | 54 |
| Lung lymph node metastases | 7 | ACUTE | -0.21 (-0.38, -0.05) | 17 |
| Lung myeloid | 57 | ACUTE | -0.10 (-0.14, -0.06) | 16 |
| Melanoma malignant | 14 | BOTH/UNRESOLVED | -0.09 (-0.22, +0.04) | 64 |
| Melanoma malignant, depth adjusted | 14 | BOTH/UNRESOLVED | -0.08 (-0.21, +0.05) | 66 |
| Melanoma macrophage | 1 | UNUSABLE | | |

Calibration: Δ separates true ISG.RS from true IFNG.GS members with AUC 0.78 to 0.79 in both malignant
sets, so the test can detect a chronic gene. MVP's Δ falls at the 11th percentile of held-out ISG.RS
members in lung and the 30th in melanoma. Its Δ is below most genes the test identifies as chronic.

**One real positive:** MVP's co-variation with each program is high against the genome. In lung malignant
cells, β(ISG.RS) is at the 95th percentile and β(IFNG.GS) at the 88th; in melanoma, 97th and 78th. The
absolute effects are small. MVP is more interferon-linked than a typical gene in malignant cells, though
it is not selective between the two programs. Depth adjustment moves the lung Δ across the pre-registered
10th-percentile line, so the "not specific" qualifier on the lung verdict is sensitive to that choice.

Across patients (pseudobulk), the same pattern is underpowered: all coefficient CIs span zero.

## 4. Exploratory, not headline

**Published MVP contradictions.** The plan asked whether PAAD and LIHC (immune-evasive) versus THCA
(immune-hot) resolve as positions on the acute/chronic axis. **They do not.** All three are on the same
side, THCA furthest from chronic.

| TCGA | n | Δ | SE | Genome percentile |
|---|---|---|---|---|
| THCA | 497 | -1.57 | 0.17 | 8 |
| PAAD | 177 | -0.82 | 0.33 | 18 |
| LIHC | 366 | -0.65 | 0.23 | 18 |
| LUSC | 484 | -0.83 | 0.22 | 3 |
| LUAD | 510 | -0.24 | 0.22 | 23 |
| SKCM, primary tumors only | 76 | +0.65 | 0.66 | 72 |

**ICB response.** No pooled association: log odds ratio per SD +0.04 (-0.30, +0.38), 5 cohorts. Two
cohorts reached nominal significance for MVP beyond ISG.RS with opposite-direction response associations:
Liu (p = 0.046) and IMvigor210 (p = 0.014). Neither survives Benjamini-Hochberg across the five tests
(adjusted 0.12 and 0.07). This matches the plan's expectation of no independent signal.

## 5. Corrections to the plan

- **§6 is wrong:** MVP is in Benci's IFNG.GS. That set is Hallmark IFN-γ minus ISG.RS, so the placement
  was by construction and no one tested MVP.
- **§3c datasets are controlled access:** public substitutes were used. Kim's "malignant" labels exist
  only in advanced and metastatic samples.
- **§0's design premise is weaker than stated.** The two sets do not hold interferon induction constant
  in a clean way. Benci states they differ by compartment, and the bulk adjusted model is unstable as a
  result. The within-malignant test and the genome null are what carry the inference.

## 6. Limits, and a warning

- Correlative throughout. Transcript co-variation cannot see a protein-level action. Reported STAT1
  inhibition by MVP protein is neither supported nor refuted here.
- **The warning from plan §7 applies now.** The sentence above is the shape of a third absorption: "wrong
  readout measured." It is true, and it is also what a dying hypothesis would say. If the chronic-program
  framing survives this, it needs a new prediction that could fail, ideally the MVP-knockout
  interferon-output experiment. It should not be re-described so this result no longer counts against it.
- Lung labels are mostly stage IV, and this is not an ICB cohort. The Dubinett and Kadara datasets could
  still differ. MVP was detected in about 54% of malignant cells, and melanoma has only 14 usable patients.
- IFNG.GS was taken from patent claim text, because Table S1 could not be fetched. ISG.RS was independently
  matched at 38 of 38; IFNG.GS has only the Hallmark reconstruction as a check.
- Predictions were drafted by Claude from the plan, before data, and not stated independently by Graham.

## 7. Addendum: gnomAD v4 loss-of-function lookup (not pre-registered)

`src/gnomad.py`, run 2026-11-06. Observed/expected LoF with 90% CI upper bound (LOEUF), pLI:

| Gene | Obs/exp LoF | LOEUF | pLI | HC LoF alleles | Homozygotes |
|---|---|---|---|---|---|
| MVP | 0.74 | 0.92 | 0.00 | 1,457 | 1 (p.Arg474Ter) |
| TEP1 | 0.79 | 0.88 | 0.00 | 2,532 | 6 |
| PARP4 | 0.64 | 0.74 | 0.00 | 2,149 | 3 |
| STAT1 (intolerant reference) | 0.22 | 0.30 | 1.00 | 62 | 0 |

MVP tolerates losing one copy, with at most mild depletion. Expected homozygotes from allele frequency are
about 0.7, so one observed is unremarkable, and the test has no power to detect selection against losing
both copies. gnomAD has no phenotype data for that individual and the variant was not manually curated.

## 8. CRISPR screens: when does losing MVP matter? (pre-registered, `ORCS_PREREGISTRATION.md`)

BioGRID ORCS 2.0.18, 1,350 human loss-of-function screens from 210 papers. **Verdict: NO SIGNAL.** MVP was a
hit in 9 of 1,340 screens, 26th percentile for overall hit rate, with no condition signal in any class. 2.2% of
all genes received one. TEP1 and PARP4 also show no signal, so there is no partner agreement.

**How much the null can bear, by class.** Control genes decide this, and the rule was fixed in advance.

| Class | Papers | Control gate | MVP | What the null means |
|---|---|---|---|---|
| Virus | 37 | PASS, 3 of 3 | 1 paper, p = 0.23 | Informative: no recurring viral phenotype |
| Baseline fitness | 59 | none set | 0 of 878 screens | Informative: loss does not affect growth in culture |
| Genotoxic | 28 | FAIL, 1 of 3 | 5 papers, p = 0.049, q = 0.54 | Uninformative by the rule |
| Immune killing | 9 | FAIL, 1 of 3 | 1 paper, p = 0.80 | Uninformative by the rule |
| Bacteria | 4 | no gene in the genome signals | 0 papers | Blind |
| Interferon | 1 | not testable | | Not tested |

**Baseline:** only 4.8% of genes have zero fitness hits (median gene: 5). This is the sharpest fact here, and it
fits the knockout mice: across hundreds of cancer lines, losing MVP does not slow growth. Expression in each line
was not checked.

**Genotoxic, exploratory and not a finding.** The class is named in advance and the raw p is suggestive, so it was
read by hand. It should not be promoted:
- It does not survive correction (q = 0.54), and 35% of all genes have a raw p this low in some class.
- Dropping one screen that called 44% of its genes hits moves p from 0.049 to 0.11.
- Five different agents. Temozolomide, etoposide and AZD6738 lean toward loss sensitizing cells, 5-FU the
  other way, and cisplatin is ambiguous.
- The three genotoxic hits with one clean FDR (5-FU, cisplatin, etoposide) have FDR 0.50 to 1.0. They passed lenient author thresholds.
- The two strongest (etoposide, AZD6738) are both HEK293-A and may not be independent.
- Controls such as FANCA have 27 hits against MVP's 5.

Worth one targeted look later, specifically MVP's score across all DNA-damage screens in one line and lab, with
the expected direction stated first.

**Limits.** Pooled screens read mostly growth in proliferating cancer lines. They miss subtle or redundant roles,
primary-cell or organism-level roles, and anything non-cell-autonomous. Thresholds vary by author.

## 9. Evolutionary co-loss: what is lost when MVP is lost? (pre-registered, `COLOSS_PREREGISTRATION.md`)

eggNOG 5.0, 472 eukaryote species, 6,128 scored gene families, counted by independent loss events on the
taxonomy tree. **Verdict: NO MODULE.** No GO term passed q < 0.05 (best q = 0.16).

**The test could have found one.** Both pre-set controls passed: from IFT88 alone it recovers intraflagellar
transport (IFT52, IFT122), and from NDUFS2 alone it recovers complex I (NDUFS1, NDUFS3, NDUFS4). So, unlike the
screens, this null means something, within the limits below.

- MVP's loss events: Fungi, Viridiplantae, Protostomia, Alveolata, Bacillariophyta, Entamoeba, Cyanidiaceae, plus
  Passeriformes and Alligator, which look like assembly gaps. Removing those two leaves the label unchanged.
- 45% of matched random gene families reach a significant term, and MVP does not.
- MVP's best partners score at an ordinary level: top-20 mean 0.51, 31st percentile of matched families.
- No family was co-lost in more than 5 of the 9 events. 24 reach 5, including MICU1-3, TANGO6, CDO1 and WDR91.
  Those are not leads. The set of top names is what a lack of signal looks like.
- TEP1's family ranks 1,132 of 6,127, which is weak. PARP4 is untestable: its family also holds PARP1-3.

**Reading.** MVP is repeatedly lost without any recognizable system of genes going with it, and the lineages that
lost it include fungi, plants and insects. That fits a self-contained particle, or one that plugs into machinery
which is retained for other reasons. It does not show vaults lack partners.

**Limits.** "Protostomia" merges into one event what the literature counts as at least 6 to 7 losses within
Ecdysozoa, because sampling there is thin. Family-level OGs hide losses of single paralogs. Both controls are large
systems, and a partner set of a few genes would not enrich a GO term. Only 111 matched families existed against the
200 pre-registered, and the reporting line for the false-positive rate was corrected after freezing, with no effect
on the analysis. eggNOG 5 dates from 2019.

**Priority.** One literature search found distribution studies and no genome-wide co-loss analysis. That is not a
claim that none exists.

## 10. Persister test: is MVP a passenger marker of the drug-tolerant state? (pre-registered, `PERSISTER_PREREGISTRATION.md`)

GSE150949 (Oren et al., Watermelon), 3 usable models, 50,735 cells. Replication GSE149383 (Aissa et al.).
**Verdict: NOT A PERSISTER MARKER**, and formally UNINFORMATIVE because the pre-registered gate failed.

**The reframe failed in the form it was specified.** The threshold was the 90th percentile of genome-wide
induction in at least 2 of 3 models. MVP reached it in none.

| Model | Drug | Treated / naive | MVP pct | After interferon adjustment |
|---|---|---|---|---|
| PC9 lung | osimertinib, 10 d | 9,458 / 7,019 | 80.6 | 82.4 |
| A375 melanoma | BRAF inhibitor, 10 d | 11,869 / 2,699 | 82.0 | 81.5 |
| HT29 colorectal | kinase inhibitor, 10 d | 9,676 / 2,164 | 81.1 | 81.0 |

- **Reproducible but modest.** Three cancer types, three drug classes, MVP within 1.4 percentile points
  each time. A real small induction, not a hallmark persister gene.
- **Interferon does not explain it**, unlike the bulk tumour picture in §2. Adjusting for both Hallmark
  interferon programs (MVP excluded, assertion enforced) leaves the value unchanged.
- **Not specific to the non-cycling state.** Cycling persisters 61.3 / 82.6 / 82.3, non-cycling
  80.9 / 77.8 / 78.8 (`results/persister_split.json`). The classic quiescent persister is not where it sits.
- **Gate failed as written.** MKI67 was undetected in A375 and the rule required all three proliferation
  genes in at least 2 of 3 models; TOP2A fell to the 0.4th-3.7th percentile in all three, so the drug
  response is plainly detectable. The conclusion does not depend on the gate: at 0 of 3 above the 90th
  percentile the label is NOT A PERSISTER MARKER either way. **The gate failure is reported rather than
  rewritten.**
- **The efflux contrast could not run.** ABCB1, ABCG2 and ABCC1 were undetected in every model, so the
  pre-registered comparison against pump genes has no data behind it.
- **Replication is too shallow to count.** Drop-seq detected MVP above the 5% floor in only 1 of 3 arms
  (PC9 erlotinib D11), where it sat at the 17th percentile. The proliferation gate passed in all three arms.

**Reading.** MVP rises slightly and reproducibly in drug-surviving cells, but it is not part of the persister
program's core and does not behave like a drug-handling gene. The passenger reframe is not supported in this
form, and the thirty-year LRP chemoresistance association remains unexplained. Kinase inhibitors in cell
lines are not the cytotoxic chemotherapies the biomarker was built on, so this tests the state claim, not the
clinical association.
