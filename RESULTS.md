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

## 11. Protein co-abundance: the vault IS a unit, and it sits in a membrane-repair neighbourhood

CPTAC mass spectrometry, 13 tumour cohorts, plus 375 CCLE cell lines. Pre-registered
(`PROTEOMICS_PREREGISTRATION.md`), deviations recorded before running (`PROTEOMICS_DEVIATIONS.md` 4-6).
Gate passed emphatically: PSMA1 recovers 15/20 proteasome subunits, NDUFS2 20/20 complex I, RPL7 20/20
ribosome, each from a single seed protein.

### PRIMARY A — UNIT. This reverses §9 and the development/divergence readings.

| Rank (excl. self) | Protein | r | Cohorts |
|---|---|---|---|
| 1 | **PARP4** | 0.82 | 13 |
| 2 | **TEP1** | 0.52 | 12 |

Out of 10,924 proteins, MVP's two closest partners are the two proteins that live inside it. Identical
ranks after removing 3 principal components, and identical in 375 stroma-free cell lines.

**The resolution of the apparent contradiction:** transcripts and evolutionary presence/absence are
*not* co-regulated (co-loss §9, development §10, divergence §12 all said "separate"), but protein
abundance is tightly coupled. Unassembled complex subunits are degraded, so complex membership shows up
at the protein level and essentially never in mRNA. The cell does not co-regulate the genes; it
co-regulates the particle. **Ledger #15 flips from WEAKENED to confirmed at the protein level.**

### PRIMARY B — MODULE LEAD, and it is specific

101 GO terms at q < 0.05, of which **50 pass the pre-registered specificity test** (fewer than 5% of 200
matched random query proteins hit the same term). Generic actin terms do *not* pass (spec 0.05-0.17);
what passes is coherent:

| Theme | Representative terms (specificity) | Genes in MVP's top 100 |
|---|---|---|
| Plasma membrane repair | `PLASMA_MEMBRANE_REPAIR` (0.010, CCLE), `PLASMA_MEMBRANE_ORGANIZATION` (0.025) | ANXA2, S100A10, EHD2, EHD4, CAPN2, CAPNS1 |
| Membrane microdomains | `CAVEOLA` (0.035), `PLASMA_MEMBRANE_RAFT` (0.040), `MEMBRANE_RAFT_ORGANIZATION` (0.025) | |
| Vesicle traffic | `ENDOCYTOSIS` (0.000), `ENDOSOMAL_TRANSPORT` (0.045), `VESICLE_BUDDING_FROM_MEMBRANE` (0.025) | |
| Inflammasome / pyroptosis | `CANONICAL_INFLAMMASOME_COMPLEX` (0.010), `PYROPTOSIS` (0.010), `IL1B_PRODUCTION` (0.010) | CASP1, CASP4, PYCARD |
| Bacterial and mechanical stress | `RESPONSE_TO_MOLECULE_OF_BACTERIAL_ORIGIN` (0.025), `RESPONSE_TO_MECHANICAL_STIMULUS` (0.005) | CAPN2, CASP1, GSN, MYD88, NFKB1 |

Replicated in CCLE (13 of 19 significant terms pass specificity) — so it is **not** stromal or myeloid
infiltrate — and unchanged after removing 3 principal components.

### Why this matters beyond the statistics

It converges with facts nobody connected: MVP-null mice die of *Pseudomonas* lung infection (a
pore-forming-toxin pathogen); the *Listeria* result (LLO is a pore-forming toxin); a report we could not independently source that
**loaded vaults are immunogenic through the NLRP3 inflammasome** — and CASP1/CASP4/PYCARD are here; the
SPFH shoulder domain, whose whole family builds membrane-microdomain cages; and the Dictyostelium
tomography finding vaults docked on membranes.

### The confound I found while checking it

**Four of the top 100 lie within 2 Mb of MVP on 16p11.2** — PYCARD (31 Mb), MAPK3 (30), SULT1A3 (30),
ALDOA (30), against MVP at 29 Mb. Chromosomal co-amplification, not biology, is the likely cause.
Consequences:
- **The inflammasome signal is partly compromised**: PYCARD is a 16p neighbour. CASP1 and CASP4 are on
  chr11 and survive, so the theme is weakened, not eliminated.
- **The membrane-repair signal is clean**: ANXA2 (chr15), S100A10 (chr1), EHD2 (chr19), EHD4 (chr15),
  CAPN2 (chr1), S100A6 (chr1) are all off chromosome 16.
- Overall chr16 share of the top 100 is 6.1% against a 4.5% background — modest, but the clustering at
  29-31 Mb is the tell.

### Limits

Co-abundance is correlation, not interaction. GO terms are heavily nested, so 50 terms is not 50
independent findings. Tumour tissue and cancer cell lines only. A copy-number-adjusted re-analysis is
the obvious next step and has not been run.

## 12. Which face is evolution protecting, and where does the ligand actually sit?

Two analyses, pre-registered (`SURFACE_PREREGISTRATION.md` + `SURFACE_AMENDMENT.md`).

### 12a. Surface conservation — LUMEN-FACING CONSERVED

78-chain biological assembly of rat vault (PDB 4V60), per-residue conservation from the eukaryotic
alignment anchored on the rat sequence (mapping identity 1.000), accessibility computed in the context of
neighbouring chains, subunit interfaces separated as their own category.

| Category | n residues | Mean conservation |
|---|---|---|
| Buried | 188 | 0.787 |
| Subunit interface | 269 | 0.773 |
| **Lumen-facing (exposed)** | 156 | **0.722** |
| **Outward-facing (exposed)** | 196 | **0.640** |

Difference outward − lumen = **−0.081 (95% CI −0.139, −0.026)**, block bootstrap over 20-residue windows.
Spearman of conservation against transmural offset among exposed residues = **−0.206 (p = 9.6e−5)**.
Gate passed (78 chains; buried 0.787 > exposed 0.676).

**This answers Graham's "maybe it binds on the outside" directly, and the answer is no.** Evolution
protects the lumen-facing surface. The field's lumen-first instinct had the right face.

### 12b. Where the ADP-ribose actually sits — inside the wall, not on a surface

PDB 11JB (human vault, endogenous ADP-ribose), 965,562 atoms, 78 AR6 copies, one per MVP chain. All 78
share |z| = 171.7 Å and r = 134.6 Å, as 39-fold symmetry per half requires.

At that height the shell spans r = 120.4–161.9 Å. The ligand sits at **fractional depth 0.34** between
lumen face and outer face, with **26% of the shell's protein mass at that height radially inside it**.

"Lumenal" as published is nearly right but imprecise: the pocket is **embedded within the shell wall**,
about a third out from the lumen surface — on neither face. Whether a solvent channel connects it to
either side was not established by my run. **It has since been settled: LUMENAL.** Directional probe
analysis on the sealed 78-mer (argon Test A5, pre-registered) gives exterior accessibility of 0.00
square angstroms at both 1.4 and 2.5 angstrom probe radii, with a maximum exterior channel radius of
1.10 angstroms - narrower than water. Cytosolic NAD+ cannot cross the shoulder wall. The pocket
straddles the midsurface (my residues W545 +1.8, F547 +7.8 outward; all ligand atoms inward), but it
opens only to the lumen.

### Limits

4V60 is rat and lacks both the bound ADP-ribose and the PARP4 density, so 12a measures the apo shell.
Shell boundaries in 12b are 2nd/98th percentiles of protein atoms in a ±7.5 Å axial slab — crude.
Conservation localises constraint, not function.

## 13. Cross-test: is the co-abundance module physically vault-associated? NOT CORROBORATED

Pre-registered (`CROSSTEST_PREREGISTRATION.md`). §11 found MVP co-varies with a membrane-repair
neighbourhood; co-abundance is correlation, so this asks whether an independent **physical** anti-MVP
IP-MS (Lodwick/Zhao, Nat Commun 2025, 1,205 proteins, WT vs PARP4-depleted) agrees.

Gate passed: MVP (LFC 7.62), PARP4 (8.66), TEP1 (6.27) all recovered as WT interactors, and PARP4 is
strongly lost in the KD arm (WTKD_LFC 5.51), confirming that arm targets PARP4.

**Primary result: 12 of my top 100 co-abundant proteins are WT vault interactors, against 7.4 expected.
Hypergeometric p = 0.058.** My pre-registered threshold was p < 0.05. **It failed, so #26 is downgraded.**
Global agreement is absent as well: Spearman between my co-abundance z and IP enrichment is **+0.019
(p = 0.52, n = 1,092)**.

**What survives, and it is not nothing:**

| Protein | My co-abundance rank | IP LFC | −log10 p | Physical interactor |
|---|---|---|---|---|
| PARP4 | 1 | 8.66 | 3.32 | yes, PARP4-dependent |
| TEP1 | 2 | 6.27 | 3.33 | yes |
| ANXA2 | 12 | 1.74 | 2.62 | yes |
| S100A10 | 65 | 2.11 | 2.69 | yes |
| CAPNS1 | 7 | 0.48 | 0.29 | no |
| EHD2 | 1060 | 0.96 | 0.54 | no |
| EHD4, CAPN2, IQGAP1 | 38, 9, 13 | — | — | not in IP universe |

So the method is sound — it put the two genuine vault subunits at ranks 1 and 2, and both are confirmed
physically — and **two of the named membrane-repair proteins, ANXA2 and S100A10, are real vault
interactors.** But the wider neighbourhood is not physically enriched, so the honest reading is that
most of §11's module reflects **shared regulation rather than contact**.

**Against argon's Tier-1 claim:** PARP4-dependence is not enriched among my top interactors (2 of 12,
16.7%, versus 18.5% of WT interactors generally). And while S100A10 does fall from +2.11 to −0.66 on
PARP4 depletion as argon reported, that change has −log10 p = 1.21 (p ≈ 0.062) and is **not significant**.

## 14. Copy-number-adjusted co-abundance (pre-registered sensitivity)

`CNA_PREREGISTRATION.md`. Each protein residualised on its own gene's copy number and MVP on MVP's, then
correlated — stripping cis copy-number effects from both sides. 10 cohorts (brca_dldccc dropped: only 46
CNA-matched samples; lusc and paad have no CNA at all), 10,077 proteins.

**Gate passed:** PARP4 stays rank 1 and TEP1 rank 3, so the adjustment is not over-correcting.

| Gene | Unadjusted | CNA-adjusted | Pre-specified expectation |
|---|---|---|---|
| PARP4 | 1 | **1** | stay high — met |
| TEP1 | 2 | **3** | stay high — met |
| ANXA2 | 12 | **7** | — rose |
| S100A10 | 65 | **26** | — rose |
| IQGAP1 | 13 | **6** | — rose |
| CAPNS1 | 7 | **5** | — rose |
| MAPK3 | 41 | 152 | drop out — **met** |
| ALDOA | 64 | 158 | drop out — **met** |
| PYCARD | 37 | **28** | drop out — **FAILED** |
| SULT1A3 | 43 | **9** | drop out — **FAILED, badly** |

**Two of my four expectations failed, and that is the finding.** MAPK3 and ALDOA behaved as amplicon
passengers and left the top 100. PYCARD held its rank and SULT1A3 *rose to 9th*. So the 16p11.2
association is **not** explained by copy number alone — something regulatory, such as a shared chromatin
domain, or compositional, such as myeloid content, is linking MVP to its neighbours. This agrees with
argon's own CPTAC result (it saw the same residual cis signal in bulk tissue while it vanished in
16p-euploid cell lines) and it means **#27's inflammasome association is not simply an amplicon
artefact** — PYCARD survives adjustment.

Meanwhile every membrane-repair protein *rose* after adjustment, which is what genuinely co-regulated
partners should do once amplicon noise is removed.

**Exploratory re-run of §13's cross-test on the adjusted ranking** is reported in
`results/crosstest_cna.json` and labelled exploratory in the pre-registration: a primary that failed at
p = 0.058 is not rescued by re-running with different input.

## 15. Cross-species test: is the neighbourhood ancient? NOT CONSERVED — but the core is

`CROSSSPECIES_PREREGISTRATION.md`. MVPA-TurboID proximity labelling in live *Dictyostelium*
(Geissler et al., Nat Commun 2026), >1 billion years from humans, tested against my CNA-adjusted ranking.

**A bug my own gate caught.** My first run matched on gene symbols and found zero Arp2/3 subunits, failing
the gate. The reason: those are *Dictyostelium* gene names — Arp2 is `ARPB`, Arp3 is `ARPC`, MVP is
`MVPB`. The 62/100 "overlap" I got was accidental name collisions on conserved genes like RPL22 and
EEF1A1, and was meaningless. Rebuilt using real orthology (Dicty UniProt -> eggNOG OG -> human symbol,
2,842 proteins mapped to 4,646 human symbols). **Gate then passed: 5 of 8 Arp2/3 subunits vault-proximal.**

**Primary: 32 of my top 100 are vault-proximal in the amoeba, against 25.0 expected, p = 0.067.** My
threshold was 0.05. **Failed.** Global Spearman +0.026 (p = 0.27, n = 3,190).

**But the specific core is ancient:**

| Protein | My rank | *Dictyostelium* log2FC | q | Vault-proximal |
|---|---|---|---|---|
| PARP4 | 1 | **+3.49** | <1e-4 | yes |
| TEP1 | 3 | **+1.61** | <1e-4 | yes |
| ANXA2 | 7 | **+0.64** | <1e-4 | yes |
| IQGAP1 | 6 | +1.09 | <1e-4 | yes |
| ARPC1B | 15 | +1.17 | <1e-4 | yes |

Annexin A7 also appears among my top-25 proximal hits, matching the published report.

### The pattern across three independent methods

| | PARP4 | TEP1 | ANXA2 | Broad module |
|---|---|---|---|---|
| Co-abundance, human tumours (§11, §14) | rank 1 | rank 3 | rank 7 | — |
| Physical IP-MS, human A549 (§13) | yes | yes | yes | **p = 0.058, failed** |
| Proximity labelling, amoeba (§15) | yes | yes | yes | **p = 0.067, failed** |

**Three methods, two species, a billion years apart, all converge on the same narrow core — and all three
fail to support the wider neighbourhood.** That is a consistent, repeatable result in both directions.

**One discrepancy with argon:** it reported ACTR3/Arp3 at +1.39. Through orthology I get ACTR3 at **−0.59**
(depleted), while ARPC1B and ARPC2 are positive. Likely an ortholog-assignment difference at the OG level;
flagged, not resolved.

### Limits
Orthology by eggNOG group across a billion years is coarse and can be one-to-many. Proximity labelling
tags anything within ~10 nm. S100A10, CLIC1, EHD4 and CAPN2 have no amoeba ortholog, so their absence is
not evidence. Only MVPA was tagged; the amoeba has two MVP genes.

## 16. DepMap co-essentiality: UNINFORMATIVE — argon's proposed gate failed

`COESSENTIALITY_PREREGISTRATION.md`. Argon's H2a argued my ORCS test (§8) was blind because it used
binary hit-calls, and that DepMap's **continuous** Chronos scores across ~1,100 lines would recover
non-essential complexes. Tested on 1,178 cell lines x 17,916 genes.

| Gate | Result |
|---|---|
| NDUFS2 recovers complex I | **PASS — 25 of 25** top partners are `NDUF*` |
| **CAV1 recovers CAVIN1 and EHD2** (argon's gate) | **FAIL — neither in the top 25** |

The method works superbly for an essential complex and fails the non-essential case argon nominated.
CAV1 did recover **CAV2 at rank 2**, its closest partner, so it is not wholly blind — but the caveolar
complex argon predicted did not appear. **Per the pre-registration, a null for MVP is therefore reported
as UNINFORMATIVE, not as a clean negative.**

**MVP's own result, for the record:** 2,886 genes reach q < 0.05, but the strongest correlation in the
entire genome is **r = 0.205** (PAPPA), and the top 25 is a grab-bag — MYO1F, DRP2, SLC6A5, TAS2R50,
PRAMEF19 — with no coherent biology. That pattern (thousands "significant", nothing above r ≈ 0.2) is
what n = 1,178 does to p-values; it is significance without effect size.

The four-protein core is nowhere: **PARP4 rank 9,020 (r = 0.002), TEP1 11,734 (−0.020), ANXA2 14,985
(−0.052)**, against 17,915 genes tested.

**What this does and does not say.** It does not upgrade §8, because the gate failed. But the contrast in
magnitude is itself informative: the same pipeline that gives NDUFS2 a perfect 25/25 gives MVP nothing
above r = 0.2. Combined with §8's zero hits in 878 growth screens, the fair statement is that **MVP has no
detectable fitness coupling to any gene in 1,178 genetic backgrounds** — while noting the method's
demonstrated weakness on non-essential complexes means this cannot be pushed further.

**Consequence for #40:** the four-protein core is an abundance and proximity association with **no fitness
coupling**. The proteins travel together and sit together; deleting MVP does not change what happens when
you delete them. That is a real constraint on any functional model, and it was my pre-registered kill
condition — fired, though softened by the gate failure.

## 17. The 30-year LRP chemoresistance biomarker, dissected

`LRP_PREREGISTRATION.md`. 292 cell lines with matched CCLE proteomics and GDSC dose-response.

**Gates:** ABCB1 predicts tubulin-agent resistance strongly (paclitaxel rho +0.32, p = 6e-6; vinorelbine
+0.39, p = 3e-8) — matching works. **ABCC1 fails its own gate** (etoposide rho −0.008, doxorubicin
−0.001), which already undercuts argon's Model A: a pump that does not predict its own drugs cannot be
the thing MVP rides along with.

**Primary: BIOMARKER IS CELL-INTRINSIC.** MVP protein predicts resistance in 8 of 19 cytotoxics at
q < 0.05. But the *pattern* is the finding — it is concentrated in tubulin agents:

| Drug | rho | q |
|---|---|---|
| Vinorelbine | +0.249 | 0.0003 |
| Vinblastine | +0.220 | 0.0015 |
| Paclitaxel | +0.184 | 0.010 |
| Methotrexate | +0.171 | 0.016 |
| Docetaxel | +0.158 | 0.022 |
| Etoposide | +0.147 | 0.039 |
| Epirubicin | +0.141 | 0.039 |
| **Mitoxantrone** | +0.064 | 0.43 |
| Cisplatin | −0.053 | 0.43 |
| Gemcitabine | +0.017 | 0.82 |

**Model C (vault RNA binds anthracyclines/mitoxantrone) is dead.** vtRNA-binding drugs median rho
**+0.098** against **+0.099** for non-binders — identical. Mitoxantrone, the canonical vtRNA binder, is
the *least* associated drug tested.

### What absorbs the signal

Standardised MVP coefficient on drug AUC, before and after adjustment:

| Drug | MVP alone | + ABCB1 | + doubling time & proliferation | + both |
|---|---|---|---|---|
| Vinorelbine | 0.256 | 0.191 | 0.246 | 0.182 |
| Vinblastine | 0.210 | 0.154 | 0.117 | 0.129 |
| Paclitaxel | 0.185 | 0.126 | 0.163 | 0.141 |
| Docetaxel | 0.149 | 0.098 | 0.002 | −0.006 |
| Methotrexate | 0.189 | 0.138 | 0.098 | 0.019 |
| Etoposide | 0.161 | 0.147 | 0.054 | 0.017 |
| Epirubicin | 0.186 | 0.140 | 0.166 | 0.125 |

**ABCB1 absorbs a median 27%. Division rate absorbs a median 44% — more.** Together, only **1 of 7**
drugs keeps a significant MVP coefficient. MVP and ABCB1 protein correlate only weakly (rho +0.161,
p = 0.026), so they are not the same thing; MVP is partly riding the same multidrug-resistance program
and partly riding slow division.

### Answer to #21

**MVP-high tumours are slow-dividing and modestly multidrug-resistant, and MVP is a passenger on both.**
Not a drug pump, not a vault-RNA sponge, and not a chromosome-16p passenger of ABCC1. This joins §12
(MVP at the genome floor against proliferation in lung and melanoma) and §10 (modestly up in
drug-surviving cells without being a persister gene) into one consistent account of a thirty-year
observation.

### Limits
Cell lines only — the stromal and immune contributions a biopsy carries cannot appear here. GDSC AUC is
short-term viability, not clinical response. Doubling time exists for 191 of 292 lines, so the
proliferation-adjusted models run on fewer samples than the ABCB1-adjusted ones and the absorbed
percentages are not perfectly matched comparisons. chr16p copy number was not included; ABCC1's gate
failure made Model A moot before it was needed.

## 18. NSUN2 -> CYP3A4 in human liver: NO RELATION

`CYP3A4_PREREGISTRATION.md`. Article 2 called this "the single highest-value open question" — if vault
RNA processing tunes CYP3A4, vault biology sits upstream of the pharmacokinetics of a large share of
prescribed drugs. Shown in MCF7/HepG2; svRNAb was never detected in liver.

TCGA-LIHC, 366 primary liver tumours. **Gate passed convincingly**: the known CYP3A4 regulators behave
as they should — HNF4A rho +0.48 (p = 1.9e-22), NR1I2/PXR +0.53 (p = 7.4e-28).

Partial correlations adjusted for HNF4A, NR1I2, NR1I3 and ALB:

| Predictor | Target | Partial rho | p |
|---|---|---|---|
| **NSUN2** | **CYP3A4** | **−0.052** | **0.33** |
| NSUN2 | CYP2E1 | −0.125 | 0.017 |
| NSUN2 | CYP1A2 | +0.021 | 0.70 |
| NSUN2 | ALB | −0.042 | 0.43 |
| MVP | CYP3A4 | −0.053 | 0.31 |
| DICER1 | CYP3A4 | −0.090 | 0.087 |

**No relation.** And the specificity control argues against the mechanism rather than for it: the only
nominally significant association is with **CYP2E1**, a P450 nobody proposed as an svRNAb target, and it
is *stronger* than the CYP3A4 association. A mechanism specific to CYP3A4 should not behave that way.

**What this does and does not settle.** It does not refute the cell-line biochemistry. It bounds how much
that mechanism can matter at tissue level: in 366 human livers, NSUN2 carries no detectable CYP3A4 signal
once differentiation is accounted for. **Critical limit: VTRNA1-1 itself is absent from the mRNA
quantification** (a Pol III transcript), so only the NSUN2 arm was testable — the vault RNA was never
measured. mRNA is also a poor proxy for enzyme activity, and these are tumours, not normal liver.

## 19. Protein turnover: the vault is ordinary, and its subunits do NOT die together

`TURNOVER_PREREGISTRATION.md`. Mathieson 2018 pulse-SILAC half-lives, 8,804 proteins, 5 primary human
cell types, 2 replicates each. Proteome median half-life 56.5 h (IQR 34.5-92.8).

**Gate, reported honestly.** The long-lived controls separated emphatically — LMNB1 1,481 h and histone
H4 1,686 h, both 99.9th percentile. The short-lived controls MYC, FOS, JUN and CCND1 are **absent from
the table**: pulse-SILAC does not capture them. My written rule said "where measured" and "if *neither*
direction separates, nothing is reported"; my script coded the stricter `both`, and printed
UNINFORMATIVE. **Applying the rule as written, the test proceeds** — and the discrepancy is recorded
rather than silently resolved.

| Protein | Median half-life | Proteome percentile |
|---|---|---|
| **MVP** | **66.4 h** | **58.6** |
| PARP4 | **22.2 h** | **9.8** |
| TEP1 | 40.6 h | 32.9 |
| ANXA2 | 82.3 h | 69.7 |
| S100A10 | 68.3 h | 60.1 |

### 19a. MVP is ORDINARY, not furniture

66 h is unremarkable — nowhere near the lamins and histones that define structural permanence
(1,500-1,700 h). At 100,000 copies per cell with a ~2.7 day half-life, the cell is continuously rebuilding
its vault population. That argues against "inert furniture", and it does not support rapid consumption on
a signalling timescale either. The born-loaded fork stays open; turnover does not settle it.

### 19b. The subunits do NOT degrade as a unit — and this is the surprise

**PARP4 turns over three times faster than MVP** (22 h vs 66 h, 9.8th vs 58.6th percentile). The spread
across MVP/PARP4/TEP1 is 44.2 h, at the **29.9th percentile of random protein triplets** — ordinary, not
tight. Verdict: **NOT A UNIT BY TURNOVER.**

This constrains argon's orphan-subunit model (H1). If PARP4 were stable *only* inside the MVP cage, it
should live as long as the cage. It does not — it is among the faster-turning 10% of the proteome while
MVP sits mid-pack.

**The reconciliation is specific and testable:** MVP is a persistent shell on which **PARP4 docks
reversibly and is replaced**. That fits three things we already have — Lodwick places PARP4 on the
lumenal face at repeats 3-4 rather than locked inside; my own conservation scan found the PARP4-MINT
patch to be the *least* conserved region of MVP (0.708 against 0.787 whole-protein); and co-abundance
plus proximity say they travel together without fitness coupling (#44).

So across four methods the core is: **one durable shell, with a fast-exchanging enzyme on its inner
face.** Co-abundance and proximity see the association; turnover shows it is dynamic, not welded.

### Limits
Primary immune cells and hepatocytes, not the lung epithelium where vaults are most abundant.
Pulse-SILAC conflates degradation with dilution by division. A stably incorporated protein and one that
is never degraded are indistinguishable here.

## 20. Vaultrc5-knockout mouse: the p62/autophagy buffer does NOT move

`VAULTRC5_PREREGISTRATION.md`. Tests **layer 3** — the barrel sequesters vault RNA, free vault RNA brakes
p62, so vault RNA availability sets selective-autophagy capacity. A version of this model has been raised within the field but we could find no published test of it; the ledger had it UNTESTED. GSE269048: Vaultrc5-knockout vs floxed
control, brain and liver, 3 replicates each.

**Gate, per tissue.** In **liver the knockout is confirmed**: Vaultrc5 log2FC **−1.37**, the 0.1st
percentile of all expressed genes. In **brain Vaultrc5 is undetected** (below 1 CPM), so brain is
inconclusive — a detection failure, not evidence the knockout failed. My written rule required reduction
"if it is present in the annotation"; my script required it in *both* tissues and printed UNINFORMATIVE.
Applying the rule as written, liver is the informative arm. **This is the second time today my code was
stricter than my own pre-registration** (see §19), and it is logged as a method fault, not a result.

| Gene set | Liver (gate passed) | Brain (inconclusive) |
|---|---|---|
| **Autophagy / p62 (17 genes)** | **−0.058, p = 0.46** | −0.061, p = 0.066 |
| Membrane repair (6) | +0.120, p = 0.0095 | −0.064, p = 0.23 |
| Interferon (11-16) | −0.009, p = 0.62 | −0.150, p = 0.013 |
| Vault components (3-4) | −0.317, p = 0.90 | +0.104, p = 0.15 |

**Primary result: NO EFFECT.** Deleting the vault RNA outright does not shift the p62/autophagy program
in the tissue where the deletion is confirmed. Sqstm1 itself moves −0.09 log2FC. If vault RNA availability
sets autophagic capacity, removing all of it should move this program, and it does not.

**The two nominal secondaries are not convincing.** Eight tests were run (4 sets x 2 tissues) with no
multiple-testing correction; 0.4 false positives are expected at p < 0.05 and two appeared. The membrane
set is 6 genes and the brain interferon result sits in the arm whose gate failed. Neither is reported as
a finding.

### Limits
Whole tissue, so cell-type effects dilute. **mRNA cannot see what the model actually predicts** — a change
in p62 oligomerisation and turnover, which is a protein-level event. This bounds the tissue-level
transcriptional consequence of losing vault RNA; it does not refute the biochemistry. The authors' own
title already says the RNA is dispensable to development.

## 21. Where is MVP actually highest? Not lung — adrenal and gut

Human Protein Atlas consensus, 20,151 genes x 51 tissues. Gate 3/4 (ALB->liver, INS->pancreas,
SFTPC->lung correct; MYH7->skeletal muscle, expected for beta-myosin in slow fibres).

| Rank | Tissue | nTPM |
|---|---|---|
| 1 | Adrenal gland | 176 |
| 2 | Colon | 162 |
| 3 | Small intestine | 157 |
| 4 | Duodenum | 146 |
| **5** | **Lung** | **120** |
| 38 | **Placenta** | **36** |
| 51 | Retina | 6 |

**Correction 1 — lung is fifth, not first.** The claim that lung has the highest vault expression runs
through the five articles and I repeated it all day without checking. The LRP name came from lung-cancer
drug resistance, not from lung topping the expression table. The real pattern is **adrenal gland plus the
whole GI tract** (colon, small intestine, duodenum, stomach, rectum). That relocates the barrier reading
rather than killing it: this is a gut-and-glandular protein that lung shares.

**Correction 2 — placenta is low (rank 38).** Article 5 experiment 8 set the condition itself: "Is
placenta a high-vault tissue? If it is not, my pre-eclampsia idea is dead on arrival." It is not.
**The pre-eclampsia prediction is retired by its own criterion.**

Nuance: MVP sits at the 96th percentile of all genes within lung and the 89th within placenta, so it is
well expressed nearly everywhere; it is the *relative* enrichment that points at gut and adrenal.

## 22. Does MVP's tissue profile track NAD metabolism? NOT NAD-LINKED

`TISSUE_COEXPR_PREREGISTRATION.md`. Motivated by two of today's results: the SPFH shoulder binds
NAD+/ADP-ribose with four residues at 100% conservation (§12), and MVP's top tissue is adrenal gland
(§21), one of the most NADPH-demanding tissues in the body.

**Gate passed emphatically:** RPL7 returns 21 of 25 ribosomal proteins, so tissue co-expression does
recover real complexes.

**Primary: NOT NAD-LINKED.** Only 2 of 22 measured NAD-metabolism genes (NADSYN1, NADK) appear in MVP's
top 200. Hypergeometric p = 0.031, but my pre-registered rule required p < 0.05 **and at least 3**
members. Two is not three, so this is reported as failed rather than as a hit.

**What the profile does track — and why it is mostly an artefact.** The top GO terms are overwhelmingly
immunoglobulin and B-cell: 70 of 143 immunoglobulin-complex genes in the top 200. That is not evidence
MVP is an immunoglobulin gene. MVP's top tissues are colon, small intestine and duodenum, and those
tissues are packed with IgA-secreting plasma cells. **This is cell-type composition, not partnership** —
the same confound class that sank the §11 module.

It does sharpen one thing: MVP's tissue distribution is essentially "mucosal and glandular tissue", and
`DEFENSE_RESPONSE_TO_BACTERIUM` also appears. That is consistent with the *Pseudomonas* knockout
phenotype and with the gut/adrenal ranking, but tissue co-expression at n = 51 cannot distinguish a
barrier role from barrier tissue composition.

### Limits
n = 51 tissues is small and highly structured; this design is dominated by tissue specificity. A null
says the NAD link does not appear at tissue resolution — the ligand evidence in §12 is structural and
stands on its own.

## 17-CORRECTED. The LRP dissection, with my own error fixed

**An external audit caught a real reversal in §17 and I verified it on my own data.**

**The bug.** `src/lrp_mediate.py` computed `1 - beta_adjusted/beta_alone` where the two betas came from
*different subcohorts*: MVP is measured in all 292 lines, but ABCB1 protein is missing in 99 and
DOUBLING_TIME in 101 different lines. Dividing a coefficient fitted on n=190 by one fitted on n=290
inflated the apparent absorption. A second bug: `CYTO['tubulin']` listed `'Docetaxel'` twice, so the
headline was **7 of 18** unique cytotoxics at q<0.05, not 8 of 19.

**Re-run on 132 complete-case lines, identical samples for every model:**

| Drug | ABCB1 absorbs | Division rate absorbs |
|---|---|---|
| Vinorelbine | **30.3%** | 8.0% |
| Vinblastine | **30.1%** | 2.8% |
| Paclitaxel | **24.9%** | 5.0% |
| Epirubicin | **19.2%** | 10.6% |
| Docetaxel | 35.1% | **67.5%** |
| Etoposide | 25.0% | **61.5%** |
| Methotrexate | 13.8% | **69.6%** |
| **Median** | **25.0%** | **10.6%** |

**The ordering reverses: ABCB1 beats division rate, not the other way round.** My published claim of
"44% vs 27%" was an artefact of mismatched sample sets.

**And the corrected result is sharper than the wrong one.** The split is mechanistically clean by drug
class: **ABCB1 dominates every efflux substrate** (the vincas, paclitaxel, epirubicin) while **division
rate dominates the S-phase and DNA-synthesis agents** (methotrexate, etoposide, docetaxel). That is
exactly what the two mechanisms predict, and my aggregated median had hidden it.

**What survives unchanged:** Models A (ABCC1/chr16p) and C (vault RNA drug binding) are still dead —
ABCC1 failed its gate, and mitoxantrone remains the least-associated drug. MVP is still a passenger, not
a pump. The conclusion for #21 stands; only the ranking of the two passenger mechanisms changes.

## 15/19-CORRECTED. Two more audit fixes, both verified against source

### §15 — ANXA2 is not specifically ancient; an annexin is

Verified in my own pipeline: the single *Dictyostelium* annexin **P24639** maps through one eggNOG
orthogroup (KOG0819) to **all 13 human annexins**. So ANXA2, ANXA4, ANXA7 and ANXA11 appearing in my top
100 are **one amoeba observation counted four times**, not four independent confirmations. My 32/100
overlap is inflated by this 1-to-many cloning; counting distinct orthogroups gives ~27 and p > 0.20,
which **strengthens** the NOT CONSERVED verdict for the wide module.

**What this does to #40:** PARP4 and TEP1 are 1-to-1 ancient partners and stand. **ANXA2 specifically does
not** — what is conserved is an *annexin-family* association predating the vertebrate ANXA1-13 radiation.
The human IP-MS (§13) does confirm ANXA2 itself as a physical interactor, so the four-protein core
survives in humans; the billion-year claim applies to the family, not the paralog.

A second bias, also verified: taking the minimum-q amoeba paralog per orthogroup inflated the
vault-proximal base rate from 19.4% to 23.0%. Orthogroup-level median or Stouffer z is the correct
estimator if this is reused.

### §19 — two text errors, and the result gets stronger

1. **"5 primary human cell types" is wrong.** The table holds **4 human types plus `Mouse Neurons`**
   (B cells, hepatocytes, monocytes, NK cells, and mouse neurons where the vault genes are NaN).
2. **The human cell types are non-dividing**, per the authors' own methods table. I had listed
   "pulse-SILAC conflates degradation with dilution by division" as a limit. It does not apply here:
   these half-lives are **pure proteolysis**. The subunit gap is therefore stronger, not weaker.

The ordering holds in **every** human cell type measured:

| Cell type | PARP4 | TEP1 | MVP |
|---|---|---|---|
| B cells | 16.0 h | 33.5 h | 55.9 h |
| Hepatocytes | 19.4 h | 25.9 h | 29.4 h |
| Monocytes | 26.0 h | 47.5 h | 77.0 h |
| NK cells | 38.2 h | 100.6 h | **310.3 h** |

PARP4 < TEP1 < MVP in 4 of 4, with an 8-fold gap in NK cells. #47 stands and is better supported than
when I wrote it.

## 23. Do vaults open in living tissue? NO EVIDENCE — and the pre-registration is why

`PHOSPHO_PREREGISTRATION.md`, Part 1. A kinase needs roughly 5 A of access to its substrate, so a
residue that is reproducibly phosphorylated in human tumours yet unreachable in the closed 78-mer would
be in vivo evidence that assembled vaults open. Modality proposed by argon; design and gates mine.

**The tempting result.** Of MVP's 6 CPTAC-annotated phosphosites, only **S585** is resolved in PDB 11JB.
It sits at r = 119.8 A in a shell spanning 99-140 A — **fractional depth 0.51, dead centre of the wall**
— with 116 protein atoms blocking the outward path at kinase scale. My script printed **SHELL MUST OPEN**.

**The coverage check kills it.** My pre-registered rule required a **reproducible** site. Querying all
seven CPTAC phosphoproteomes:

| Cohort | MVP sites annotated |
|---|---|
| LUAD | S445, **S585**, S867, S873, S876 |
| BRCA | S445, S867, S873, S876 |
| GBM | S445, S864, S867, S873, S876 |
| PAAD | S445, S864, S867, S873, S876 |
| LUSC | S445, S867, S873, S876 |
| UCEC, COAD | none mapped |

**S585 appears in exactly one cohort of seven.** It is a single-cohort annotation — precisely the
peptide-mapping ambiguity the pre-registration named as a limit. It is not reproducible, so it cannot
carry the claim.

And the **reproducible** sites — S445 and the C-terminal cluster S864/S867/S873/S876 — are **all
unresolved in 11JB**, i.e. in disordered regions, which are typically solvent-exposed and freely
kinase-accessible.

**Verdict: NO EVIDENCE.** The one occluded site is not reproducible; the reproducible sites cannot be
placed in the structure. This does not show vaults never open — §12 already showed the ligand pocket is
lumen-only, so something must admit NAD+ — it shows **phosphorylation cannot be used as the evidence.**

**Descriptive note worth keeping:** MVP's reproducible phosphorylation is concentrated in a
**C-terminal cluster (S864-S876) that is disordered in every vault structure solved**, plus S445. A
flexible, multiply-phosphorylated C-terminal tail is a regulatory motif, and no one has asked what
binds it.

**Why this section exists.** My own script returned SHELL MUST OPEN. The written rule said *reproducible*,
and checking that one word inverted the answer. Part 2 (phospho-stoichiometry against per-vault PARP4
loading) was not run — the coverage gate for MVP fails in 2 of 7 cohorts and the key site is singleton.

## 24. Part 2 — phosphostoichiometry: the phospho-gated vault hypothesis is dead

`PHOSPHO_PREREGISTRATION.md` Part 2, with the site-sampling deviation recorded before running. Seven
CPTAC cohorts, ~1,500 residualised phosphosites each, 80-140 matched samples per cohort.

**Method.** Each phosphosite is residualised on **its own gene's total protein** (`dp = phospho ⊥ total`),
so the quantity is *phosphorylated vaults per vault* rather than how much vault there is. Cell-type
composition and bulk abundance — the confound that defeated §11, §15, §21 and §22 — vanish by
construction. Per-vault partner loading is defined the same way: `PARP4_prot ⊥ MVP_prot`.

**Gate passed.** Residualised MAPK1 activation-loop phosphorylation recovers **MAPK1, MAPK3 and RPS6KA1**
in its top 25, so `dp` captures live signalling and not abundance.

**Primary: zero at correction.** **CORRECTED 2026-11-07 after review:** the committed JSON holds **64
rows, of which 2 are an acetylome entry in LUSC** (which has no MVP phosphosites), giving **62 phospho
tests across 6 cohorts** - not the 44 first reported. My description of the effect sizes was also wrong:
I read the bottom of a sorted table. The true range includes **UCEC S445 vs PARP4 at rho = -0.374,
raw p = 0.001**, and 4 rows at raw p < 0.05.

**The conclusion is unchanged and arguably better evidenced.** **0 of 62 tests reach q < 0.05.** The
strongest association (q = 0.066) does not replicate: across all six cohorts measuring S445 (n = 612)
the sample-weighted mean rho with PARP4 loading is **-0.036**, with signs flipping between cohorts.

**Secondary — and the trap I nearly fell into.** 12 of 32 MVP sites had a core or signalling partner in
their top 1%, which looks like a hit. But I had fetched **all** sites for the target genes plus a random
background, so target genes are enriched in my universe by construction (4-7% of sites per cohort).
Chance alone predicts **18.9** of 32 by that design. Observed 12 is **below** expectation
(binomial p = 0.018). The apparent signal is an artefact of my own sampling, and the true reading is a
clean negative.

**Verdict: argon's kill condition is MET.** No association with partner loading, no partner enrichment
beyond chance, and Part 1's one occluded site was a singleton. **Phosphorylation does not gate vault
assembly, partner exchange, or shell opening** — at least not detectably across ~750 human tumours.

**Why this matters more than another null.** This was the one modality immune to composition confounding,
and it was aimed squarely at the live question from #47: what drives the 22-hour PARP4 exchange on a
66-hour shell. The answer is not phosphorylation of MVP. That exchange is driven by something else —
ligand occupancy, local concentration, or a modification nobody has catalogued.
