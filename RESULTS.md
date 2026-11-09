# Results: MVP does not belong to the chronic interferon resistance program

> ### Two standing notes that qualify every pulldown section in this file
>
> **Provenance (established late, in §71).** Every `WT_LFC`, `LWTP` and `WTKD_*` number in §13 and
> §41-§57 — 75 interactor terms across eight sections — comes from **one dataset: PRIDE PXD052802**,
> co-IP of MVP with the synthetic antigen binding reagent **VM1** against control **H6**, in
> **wild-type versus PARP4-knockout A549 cells**, a lung adenocarcinoma line. **The deposit's own
> description analyses the same WT-versus-knockout contrast we use**, so these are readings of public
> data rather than discoveries of this work, and may be specific to that line. Everywhere below, **"not
> PARP4-dependent" means "still present when PARP4 is removed in A549"**, not independence in general.
> We did not establish the cell line until §71, having analysed it for a full session.
>
> **Relocation (established in §70).** The published vault function is **signalling modulation** —
> IKK-NF-kB, calcineurin-NFATc1, STAT3, Parkin-mediated mitophagy, adaptive immunity on influenza
> rechallenge. **The convergence is mostly one group's** (Ben on 5 of 6 papers; only the influenza
> study is authorially independent — §76b), and **five of six** published phenotypes are
> **conditional**, absent
> at baseline. Those interactions are transient and low-stoichiometry: the class these instruments
> recover worst. **So no negative result in this file is evidence against vault function.** What the
> negatives establish is narrower and still useful: **MVP has no stoichiometric partner complex beyond
> PARP4 and TEP1.**
>
> Both notes are repeated here because this file is read in fragments and the sections they qualify were
> written before either was known. This is the fourth place the same failure was found — a correction
> appended at the end while the claims it qualifies stay live where a reader meets them (#262, #283,
> #319, here).

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

**CORRECTED 2026-11-07 (ledger #66).** Two of the "facts" below were overstated, and the overstatement
was load-bearing. Kowalski 2007 reports that MVP-null mice carry ~3.5x more lung bacteria and a hazard
ratio of 2.96 after an *experimental* intranasal *Pseudomonas* inoculum (n = 15 vs 17) - not that they
die of *Pseudomonas*; the proposed mechanism was failed epithelial internalisation after CFTR-dependent
raft recruitment. And the listerial protein that binds MVP is **InlK, a surface protein that evades
autophagy - not listeriolysin O**. Calling both "pore-forming toxin" links conflated an organism with a
toxin and InlK with LLO. The convergence as originally written:

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

**Correction, 2026-11-07 (ledger #61).** I went one step further than this and inferred that the
particle must therefore *open* to admit NAD+. That inference is wrong, and the test could not have
supported it: Test A5 sealed the z-ends of the shoulder band, so it measured radial wall crossing only.
The assembled cage has openings at its C-terminal caps (Lodwick 2025 Supp. Fig. 4a) and breathes at the
waist (Collins 2026), and published ITC and soaking experiments put free NAD+ and an NAD+ analogue in
the shoulder pocket of intact cages in neutral buffer with no trigger, with purified MVP+TEP1 vaults
hydrolysing added NAD(P)+ (Osinski 2026 Fig. 5G, 6A). **The result here is that the transmural
shoulder-pore hypothesis is dead and the pocket is lumen-loaded. Particle opening gates macromolecular
traffic - PARP4, TEP1, vtRNA, ADP-ribosylated targets - not the 663-Da substrate.**

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
q < 0.05 (**corrected below to 7 of 18 unique drugs — `Docetaxel` was duplicated in the gene list; see §18**). But the *pattern* is the finding — it is concentrated in tubulin agents:

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
the weakest of the three vtRNA-binding drugs measured (+0.064, q 0.43) while the top of the ranking is
pure tubulin. **Corrected 2026-11-07:** it is *not* the least-associated drug overall — cisplatin is
lowest (−0.053) and five drugs rank below mitoxantrone. The Model C refutation rests on the
binder-vs-non-binder medians being identical, which is unaffected.

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
ABCC1 failed its gate, and mitoxantrone remains the weakest vtRNA-binding drug (rank 14 of 19 overall). MVP is still a passenger, not
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

## 25. Is the immunoglobulin co-expression caused by plasma cells? NO — and this reverses §22's reading

`ADRENAL_PREREGISTRATION.md`, committed at `64f8ce8` before any stratified MVP value was read.

§22 found MVP's cross-tissue profile dominated by plasma-cell immunoglobulin (70 of 143,
p = 9.3e-98). Ledger #89, written this morning, read that together with §21's tissue ranking and
concluded the gut rankings were plasma-cell **infiltrate**, leaving adrenal as the one unexplained
residual. That reading had two possible causes and I had not separated them: plasma cells being
intrinsically MVP-rich, or MVP and immunoglobulin merely being high in the same tissues for unrelated
reasons. Cell lines carry no infiltrate, so lineage-stratified protein discriminates.

**Gate passed emphatically.** Three of four plasma-cell markers put `plasma_cell` first of 20 lineages:
MZB1 (z = +3.51), SDC1 (+1.00), PRDM1 (+1.48). Lineage identity is fully resolvable at protein level.

**Primary: INFILTRATE NOT SUPPORTED. The pre-registered kill condition fired.** MVP in `plasma_cell`
lines ranks **15th of 20** lineages at z = **−0.454**, below the median rank of 10.5. All six lines are
measured, none imputed, and all six are canonical myeloma lines.

The direction is consistent across far more than the six lines the registration worried about —
**40 immune-lineage lines all point the same way**, while epithelial and glandular lineages run high:

| Lineage | n | mean MVP z |
|---|---|---|
| kidney | 12 | **+1.22** |
| central nervous system | 14 | +0.78 |
| pancreas | 20 | +0.72 |
| gastric | 14 | +0.53 |
| colorectal | 30 | +0.32 |
| lung | 79 | +0.04 |
| **plasma cell** | 6 | **−0.45** |
| lymphocyte | 11 | −0.85 |
| blood | 23 | **−1.21** |

**What this means, and it is the opposite of what I published this morning.** Plasma cells are
MVP-*poor*. The immunoglobulin correlation in §22 is a tissue-level coincidence — gut tissue is both
MVP-rich and plasma-cell-rich, for unrelated reasons — not evidence that the MVP signal comes from the
plasma cells. **The gut tissue ranking is therefore not an infiltrate artefact, and is most simply read
as epithelial.** Colorectal, gastric and pancreatic lines are all positive, which independently
corroborates the bulk ranking rather than undermining it.

**Consequences I am obliged to accept.** Ledger #89's infiltrate framing is withdrawn, and with it the
claim that adrenal is a distinguished residual: if the whole ranking is parenchymal, adrenal is simply
the top of a coherent glandular-and-GI series rather than an anomaly needing its own explanation. The
`PAPER2` experiment 9 rewrite I pushed this morning was built on the infiltrate premise and has been
corrected. The experiment survives, for a weaker and more honest reason.

**What is still open.** This says nothing about adrenal directly and does not pretend to: there is
exactly **one** `adrenal_cortex` line in all 1,739 CCLE lines and **zero** with proteomics, which was
stated in the registration before the test ran. Why adrenal tops 51 tissues remains unexplained, and
the NAD hypothesis that would have explained it failed in §22. I am not proposing a replacement story;
kidney at rank 1 among lineages and CNS at rank 2 do not fit a tidy barrier reading, and inventing one
here would repeat faults #59, #60, #64, #70 and #90.

## 26. Is the lineage pattern just epithelial identity? NO — structure survives within epithelium

`LINEAGE_CLASS_PREREGISTRATION.md`, with the tissue classification fixed before any class statistic was
computed. This is a confound check, not a hypothesis test: every functional reading of §25's ranking is
worthless if the ranking is merely epithelial versus not.

**Gate passed.** CDH1 separates epithelial from haematopoietic lineages by +1.13 z and KRT8 by +1.05,
both clearing the registered 1.0 bar (EPCAM +0.88).

**Primary: H1 LOSES.** Tissue class explains **eta-squared = 0.338** of the between-lineage variance —
below the registered 0.50 — and the spread *within* the 14 epithelial lineages is **2.15 z**, far above
the 1.5 threshold set for rejecting the confound. Class means: epithelial +0.079, mesenchymal −0.217,
haematopoietic −0.838.

So epithelial identity accounts for roughly a third of the pattern, mostly by placing the three
haematopoietic lineages at the bottom. It cannot account for kidney (+1.22) sitting 2.15 z above uterus
(−0.93) when both are epithelial, and it is directly contradicted by CNS at **+0.78**, which is not
epithelial at all.

| epithelial lineage | z | | epithelial lineage | z |
|---|---|---|---|---|
| kidney | **+1.22** | | ovary | −0.09 |
| pancreas | +0.72 | | breast | −0.19 |
| gastric | +0.53 | | liver | −0.20 |
| colorectal | +0.32 | | esophagus | −0.37 |
| upper aerodigestive | +0.28 | | prostate | −0.46 |
| skin | +0.20 | | uterus | **−0.93** |
| urinary tract | +0.05 | | | |
| lung | +0.04 | | | |

**Consequence: functional hypotheses about the ranking remain worth testing.** The kill condition would
have withdrawn them and did not fire.

**One observation, offered as an observation and not a theory.** Among epithelia the high end is
digestive, renal and barrier — kidney, pancreas, stomach, colon, upper aerodigestive, skin — and the low
end is dominated by **hormone-responsive reproductive** epithelium: uterus, prostate, breast, ovary.
Adrenal, the top tissue overall, is hormone-*producing* rather than hormone-*target*. I am recording
that because it is a pattern in the ranked list and recording it is cheaper than re-deriving it later,
**not** because I have tested it. Reading a ranked list for a story I like is fault #59/#60/#64/#70/#90,
and liver at −0.20 already embarrasses the obvious detoxification reading it might suggest.

## 27. Two corrections from a blind second opinion, both of which cost us

Argon was given §25's and §26's observations with **none** of my hypotheses attached, and asked what
unifies the pattern. It attested to answering before reading any of today's commits. Two of its findings
are verified here independently and both damage conclusions I published today.

### 27a. Adrenal is #1 for the *shell* only. The armed holoenzyme peaks in gut.

Reproduced exactly from `data/raw/tissue/rna_tissue_consensus.tsv`. Adrenal gland ranks **1st of 51 for
MVP, 16th for PARP4 and 21st for TEP1**. The MVP:TEP1 ratio is **23.5 in adrenal against 5.5 in
duodenum**. Ranking tissues by the three-subunit geometric mean:

| rank | tissue | MVP | PARP4 | TEP1 | holo |
|---|---|---|---|---|---|
| 1 | duodenum | 145.6 | 36.6 | 26.3 | **51.9** |
| 2 | colon | 161.7 | 36.3 | 16.3 | 45.7 |
| 3 | small intestine | 156.7 | 36.8 | 14.5 | 43.7 |
| 4 | rectum | 90.6 | 37.1 | 16.8 | 38.4 |
| 5 | spleen | 111.9 | 24.8 | 14.2 | 34.0 |
| 6 | lung | 119.8 | 27.1 | 10.3 | 32.2 |
| 7 | stomach | 101.7 | 32.6 | 9.0 | 31.0 |
| **8** | **adrenal gland** | **176.2** | 21.6 | 7.5 | **30.6** |

**This dissolves the question we spent the afternoon on.** We treated "why adrenal?" as the anomaly
demanding explanation, having never once stratified the tissue ranking by the other two subunits. The
catalytic MVP-PARP4-TEP1 particle concentrates in **gastrointestinal mucosa**, which is where Graham's
original barrier intuition put it. Adrenal carries an extreme excess of unarmed shell.

### 27b. A cytoplasmic-mass-fraction confound we never considered, and it is larger than the one we did

CCLE proteomics is equal-protein-mass TMT, which mechanically penalises a strictly cytoplasmic complex
in small nucleus-dominated suspension cells and inflates it in giant-cytoplasm clear-cell renal lines.
Defining a housekeeping nuclear-to-cytoplasmic proxy as mean z of 88 cytosolic RPL/RPS proteins minus 46
nuclear HNRNP/SRSF/SF3B/SMC proteins, **that proxy alone explains R² = 0.515 of lineage-mean MVP
variance** (r = +0.718, p = 3.7e-4; argon's slightly different gene lists give 0.642). At line level
R² = 0.197 over 375 lines.

For comparison, the epithelial-class confound we *did* pre-register explains η² = 0.338. **We tested the
smaller confound and missed the larger one.**

Residualising MVP on that proxy at lineage level:

- **kidney collapses from +1.22 to +0.26** — our top lineage was substantially a cytoplasmic-volume
  artefact of clear-cell histology
- **skin flips** +0.20 to −0.32; **esophagus flips** −0.37 to +0.19; **bone flips** −0.48 to +0.19
- **pancreas becomes first** (+0.83), with upper aerodigestive and CNS next
- **blood (−1.21) and lymphocyte (−0.58) stay firmly lowest**, so that part of the pattern is not the
  confound

### 27c. Consequences for §25 and §26, stated plainly

**§25 weakens.** `plasma_cell` moves from **−0.454, rank 15 of 20** to **+0.124, rank 8 of 20** — from
below the median to above it. **The pre-registered kill condition would not have fired on adjusted
values.** It fired as written on the registered metric, and the registration did not anticipate this
confound.

What survives: plasma cells are still not MVP-*rich*, and the infiltrate hypothesis needs them to be
rich to explain gut, so #89's withdrawal stands in substance. What does not survive is my positive claim
that **plasma cells are MVP-poor**. They are unremarkable. §25's conclusion should have been "no
evidence plasma cells are MVP-rich", not "plasma cells are MVP-poor".

**§26 weakens further.** Within-epithelial spread falls from **2.152 z to 1.149 z**, which lands inside
my own pre-registered **"PARTIAL — no functional hypothesis promoted"** band rather than the "H1 loses"
band. Class η² barely moves (0.338 to 0.324), so tissue class never explained much either way. The
honest verdict on §26 is partial, not a clean rejection of the confound.

### 27d. The literature answer to the question I called unexplained

**Izquierdo et al., *Am J Pathol* 1996;148(3):877-887 (PMID 8774142)** — "Broad distribution of the
multidrug resistance-related vault lung resistance protein in normal human tissues and tumors" —
reported high LRP by immunohistochemistry in **bronchus, digestive tract, renal proximal tubules,
keratinocytes, macrophages and adrenal cortex**. Verified against the published abstract. It is the same
paper that identified LRP as the major vault protein.

**The tissue distribution we spent the afternoon rediscovering is that paper's result list, at protein
level, from 1996.** Sugawara et al. 1997 (*Cancer Lett*) reports adrenal independently. This also
further undercuts the "nobody checked lung" framing already retracted in #60: the 1996 atlas never
claimed lung was uniquely highest, and listed adrenal cortex alongside it.

## 28. Ledger #41 re-opened and REVERSED: the membrane-repair module survives the confound

`MEMBRANE_MODULE_PREREGISTRATION.md`, with gene sets taken externally and unmodified from MSigDB so the
test is not circular with the covariate list that prompted it.

### 28a. Transparency about two runs

**Run 1 (`src/membrane_module.py`) formally returned UNINFORMATIVE.** Gate 1 required PARP4 *and* TEP1 to
stay in MVP's top 50 after residualisation. PARP4 came first; TEP1 was absent entirely — because a
no-NaN mask had cut the matrix from 12,096 x 375 to 5,063 x 330, and **TEP1 is measured in only 277 of
375 lines**. The gate failed on a coding choice, not on destroyed signal.

**Run 2 (`src/membrane_module2.py`) fixes that with pairwise-complete handling**, retaining 8,982
proteins including TEP1. **The gene sets, thresholds, gates and kill condition are identical to the
registered text; only the missing-data handling changed.** A sceptic may still call this a second bite,
so both runs and both logs are committed.

### 28b. Result

Residualising every protein on the §27b N:C proxy plus six proliferation markers, at line level:

**Both gates pass.** PARP4 ranks **1st (+0.839)** and TEP1 **2nd (+0.581)** among 8,982 residualised
correlates — the confirmed physical core survives emphatically. PSMA1 still recovers 20 of 25 proteasome
subunits.

| gene set (external, unmodified) | members | in MVP top 200 | specificity p |
|---|---|---|---|
| `GOBP_PLASMA_MEMBRANE_REPAIR` | 24 | 5 | **0.000** |
| `GOCC_CAVEOLA` | 52 | 7 | **0.000** |
| `GOBP_PLASMA_MEMBRANE_ORGANIZATION` | 87 | 9 | **0.000** |
| `GOCC_LATE_ENDOSOME` | 210 | 11 | **0.005** |
| `GOBP_ENDOSOMAL_TRANSPORT` | 243 | 6 | 0.49 |

**The last row is the important one.** Generic endosomal transport is *not* enriched while plasma
membrane repair, caveola and membrane organisation sit at zero of 200 matched-random sets. This is not
"any cytoplasmic membrane protein covaries with MVP" — that was the confound, and it has been removed.
It is specifically the repair and caveolar compartment.

### 28c. The module recruits canonical repair proteins we never named

MVP's top 30 residualised correlates include the §11 list — **ANXA2 +0.516, S100A10 +0.516, EHD2 +0.504,
CAPN2 +0.441, EHD4 +0.438** — and adds proteins absent from our original nomination that are more
canonical still:

- **MYOF (myoferlin) +0.475** — ferlin family, with dysferlin the defining Ca²⁺-dependent
  membrane-resealing proteins
- **AHNAK +0.458 and AHNAK2 +0.485** — the AHNAK scaffold that partners dysferlin in sarcolemmal repair
- **CD151 +0.443** (tetraspanin), **S100A6 +0.463**, **CAVIN1** (caveolar coat, top 25 in run 1)

We did not propose any of these. They arrived from an externally defined analysis after the confound was
stripped.

### 28d. Status of #41, and what would still kill it

**#41 is reversed as a co-abundance claim.** The broad membrane-repair neighbourhood is enriched around
MVP with matched-random specificity, after removing the confound that invalidated the newest evidence,
with the particle's two confirmed partners as the top two hits.

Three limits, all real:

1. **This is co-abundance, not contact.** §13's anti-MVP IP-MS was the contact test and it missed its
   bar at p = 0.058. Surviving a confound does not convert co-abundance into physical association. #26's
   downgrade stands.
2. **A further confound is plainly visible in the top 30 and is the obvious next control.** LMNA, FHL2,
   BCAR1, ITGA3, RRAS, ANLN and FOSL1 read as an adhesion / mesenchymal-EMT axis, which is one of the
   largest axes of variation in CCLE. AHNAK and MYOF are themselves EMT-associated. **If an EMT score
   absorbs this signature, #41 dies again**, and that test should be pre-registered next.
3. **Post-hoc, and declared as such in advance:** Fisher's combination of the two earlier independent
   tests (§13 p = 0.058, amoeba §15 p = 0.067) gives X² = 11.10, **p = 0.0255**. This was **not** the
   registered rule, which required each to clear 0.05 alone. Combining after seeing both is the
   flexibility pre-registration exists to prevent, and it is reported as what a meta-analysis would say,
   not as satisfaction of the original criterion.

## 29. The EMT control is UNINFORMATIVE — its own validity gate failed, so #109 stays open

`EMT_PREREGISTRATION.md`. This was the control I flagged in §28d as able to kill #41 a third time.

**Formal verdict: UNINFORMATIVE. Gate 3 failed.** The registered validity gate required the EMT score to
behave like an EMT axis, with VIM, FN1 and CDH1 each at |r| >= 0.3. VIM (+0.595) and FN1 (+0.691) passed
easily; **CDH1 reached only −0.194**. By the rule as written the score is not a validated EMT axis and
the test says nothing, so it is reported that way.

In hindsight the gate was badly chosen rather than the data being at fault. `HALLMARK_EMT` is dominated
by extracellular-matrix and mesenchymal genes, and CDH1 loss is not a reliable *linear* correlate of
pan-cancer EMT score — many epithelial lines retain CDH1 while scoring mesenchymal. Requiring a
symmetric epithelial arm from an asymmetric signature was a design error of mine. **That is a lesson
about gate design, not about vaults.**

**The substantive numbers, reported because the gate failure does not entitle us to hide them, and
explicitly not as a result:**

| gene set | §28 (N:C + proliferation) | §29 (+ EMT score) |
|---|---|---|
| `GOBP_PLASMA_MEMBRANE_REPAIR` | 0.000 | **0.000** |
| `GOCC_CAVEOLA` | 0.000 | **0.000** |
| `GOBP_PLASMA_MEMBRANE_ORGANIZATION` | 0.000 | **0.000** |
| `GOCC_LATE_ENDOSOME` | 0.005 | **0.095** |
| `GOBP_ENDOSOMAL_TRANSPORT` | 0.49 | 0.115 |

Gates 1 and 2 both passed: PARP4 remains rank 1 (+0.816) and TEP1 rank 2 (+0.583); PSMA1 still recovers
20 of 25 proteasome subunits. The named repair proteins all **drop substantially in rank but stay
positive**: S100A10 13th, ANXA2 19th, AHNAK2 24th, MYOF 27th, CAPN2 45th, AHNAK 52nd, EHD4 55th, EHD2
56th.

So the EMT axis plausibly absorbs *some* of the signal — the rank drops are real and the late-endosome
term loses significance — while the repair, caveola and membrane-organisation enrichments do not move
from zero of 200 matched-random sets. **But none of that is licensed, because the score failed its own
validity check.**

### Where this leaves #41, and why we stop here

**§28's reversal stands on its own gates**, which passed. **#109's EMT concern is neither confirmed nor
refuted — it remains open and untested.** The correct next step would be a validated bidirectional EMT
signature with separate epithelial and mesenchymal arms rather than `HALLMARK_EMT`.

**We are not running it.** This test has now been attempted twice with a gate failure each time for
different mechanical reasons, and continuing to adjust the method until the module passes is exactly the
behaviour the pre-registration discipline exists to prevent. The honest state of the evidence is:

- The module survives the one confound we have properly controlled (cytoplasmic mass and proliferation).
- Whether it survives an adhesion/EMT axis is **unknown**, and we flagged it ourselves rather than
  waiting for a reviewer to.
- It remains co-abundance, not contact.

That is where it should sit until someone runs it who did not write the hypothesis.

## 30. The membrane-repair module does NOT replicate in independent tumour proteomics

`MODULE_REPLICATION_PREREGISTRATION.md`. The registered kill condition fired, and §28's reversal of
ledger #41 is withdrawn.

### 30a. Replication

Eight CPTAC cohorts, analysed separately and never pooled. Same method as §28, same externally defined
gene sets, unmodified.

| cohort | n | PARP4 rank | proteasome | gate | `PLASMA_MEMBRANE_REPAIR` p |
|---|---|---|---|---|---|
| brain_cptac_2020 | 218 | **1** | 24/25 | pass | 0.60 |
| coad_cptac_2019 | 97 | **1** | 11/25 | pass | 1.00 |
| gbm_cptac_2021 | 99 | **1** | 14/25 | pass | **0.00** |
| ucec_cptac_2020 | 95 | **1** | 12/25 | pass | 1.00 |
| brca_cptac_2020 | 122 | 1 | 0/25 | **fail** | (0.06) |
| luad_cptac_2020 | 110 | 1 | 0/25 | **fail** | (1.00) |
| paad_cptac_2021 | 124 | 1 | 7/25 | **fail** | (0.00) |
| lusc_cptac_2021 | 35 | — | — | excluded | — |

**1 of 4 gate-passing cohorts clears p < 0.05.** That is 0.25, below the registered one-third threshold,
so the verdict is **DOES NOT REPLICATE**.

**The borderline, stated rather than buried.** `paad_cptac_2021` reached p = 0.00 but failed its
complex gate by a single subunit (7 of 25 against a registered 8). Had it passed, the count would be 2
of 5 = 0.40, which falls in the **partial replication** band. The verdict therefore turns on one
proteasome subunit in one cohort. We are honouring the gate as written — that is the rule that made
§28's run 1 uninformative too — but a reader should know the result is not far from partial.

**The pre-stated caveat, which we are not leaning on.** The registration said in advance that a failure
to replicate is also consistent with tumour cohorts being noisier than cell lines, since they carry
stromal and immune content. That was written down precisely so it could not be invoked selectively now.
We note it and do not rest on it: three cohorts returned p = 1.00, which is not noise around a real
effect.

### 30b. What replicates perfectly, and it is not the module

**PARP4 is MVP's rank-1 residualised correlate in all eight cohorts**, gate-passing or not, across
brain, breast, colon, glioblastoma, lung, pancreas and endometrium. The MVP-PARP4 association is the
most robust quantitative finding in this entire project. The *broad neighbourhood* around it is not.

### 30c. The module was MVP-specific, for whatever that is now worth

Secondary registered test, seeding CCLE with other SPFH-domain proteins: `GOBP_PLASMA_MEMBRANE_REPAIR`
clears 0.05 for MVP (0.000) and for **1 of 6** SPFH seeds tested — FLOT1 at 0.035, which is coherent
since flotillin-1 is a canonical lipid-raft protein. FLOT2, STOM, PHB2, ERLIN1 and ERLIN2 do not clear.

By the registered rule that is **MVP-specific**, not a generic SPFH artefact. But it is specificity about
a cell-line-only result, so it rescues nothing.

### 30d. Ledger #41, final

**Struck for the third time.** The sequence, with nothing hidden:

1. §11 nominated it from co-abundance GO enrichment with matched-query specificity.
2. §13 physical IP-MS missed at p = 0.058; §15 amoeba proximity missed at p = 0.067. Struck as #41.
3. §28 reversed it after removing a cytoplasmic-mass confound: repair and caveolar sets at p = 0.000,
   with PARP4 and TEP1 as ranks 1 and 2.
4. §29's EMT control failed its own validity gate and resolved nothing.
5. **§30: it does not replicate in independent tumour proteomics.**

**My own favoured hypothesis from this afternoon — H2, vaults as sterol-rich membrane-microdomain
residents — goes with it as a co-abundance claim**, exactly as the registration required. What survives
is narrower and was never in dispute: MVP and PARP4 travel together, everywhere we look.

The membrane idea is not disproven as *biology* — the SPFH domain is real, the amoeba tomography showing
vaults on membranes is real, ANXA2 and S100A10 are confirmed physical interactors, and Kowalski's
CFTR-raft phenotype is published. What is dead is the claim that **co-abundance data supports a broad
membrane-repair neighbourhood.** Four tests, one dataset in its favour, and it does not survive contact
with another.

## 31. Unbiased neighbourhood scan: my prediction was wrong, and the replicating module is innate immune

`NEIGHBOURHOOD_SCAN_PREREGISTRATION.md`. Every GO BP and CC term (8,634 loaded, 10-500 members),
scanned against MVP's top 200 residualised correlates in five independent datasets, BH-corrected within
each, replication required in a majority. No term chosen by hand.

**I registered the prediction that zero or very few terms would replicate. That was wrong.** All five
datasets passed their gates — PARP4 is rank 1 in every one — the scan design gate passed (6 proteasome
terms replicate from a PSMA1 seed), and **103 terms replicate in 3 or more of 5 datasets.**

### 31a. What replicates

| term | datasets |
|---|---|
| `GOBP_ANTIGEN_PROCESSING_AND_PRESENTATION` | 4 |
| `GOBP_CYTOKINE_PRODUCTION` | 4 |
| `GOBP_INFLAMMATORY_RESPONSE` | 4 |
| `GOBP_RESPONSE_TO_BACTERIUM` | 4 |
| `GOBP_POSITIVE_REGULATION_OF_DEFENSE_RESPONSE` | 4 |
| `GOCC_RUFFLE` | 4 |
| `GOBP_ACTIN_FILAMENT_ORGANIZATION` | 4 |
| `GOBP_CYTOKINE_MEDIATED_SIGNALING_PATHWAY` | 4 |
| `GOBP_RESPONSE_TO_TYPE_II_INTERFERON` | 3 |
| `GOBP_MYELOID_LEUKOCYTE_ACTIVATION` | 3 |
| `GOBP_INTEGRIN_MEDIATED_SIGNALING_PATHWAY` | 3 |
| `GOCC_EXTERNAL_SIDE_OF_PLASMA_MEMBRANE` | 3 |

The module is **innate immune defence, inflammatory signalling, antigen presentation, interferon-gamma
response, and actin-ruffle membrane dynamics.** `coad_cptac_2019` is the consistent outlier at q = 1.000
for nearly everything — the same cohort that returned p = 1.00 throughout §30.

### 31b. It is not immune infiltrate, and the internal control is what shows that

Tumour tissue contains immune cells, so an immune signature across CPTAC cohorts is exactly what
infiltrate would produce — the same confound class that sank §22's immunoglobulin finding. **CCLE is in
the included set and is cell lines, with no immune cells at all.** Per-dataset q values:

| term | brain | coad | gbm | ucec | **CCLE** |
|---|---|---|---|---|---|
| `INFLAMMATORY_RESPONSE` | 0.000 | 1.000 | 0.000 | 0.000 | **0.000** |
| `RESPONSE_TO_BACTERIUM` | 0.002 | 1.000 | 0.000 | 0.010 | **0.002** |
| `CYTOKINE_PRODUCTION` | 0.000 | 1.000 | 0.000 | 0.001 | **0.006** |
| `GOCC_RUFFLE` | 0.001 | 1.000 | 0.012 | 0.032 | **0.010** |
| `RESPONSE_TO_TYPE_II_INTERFERON` | 0.000 | 1.000 | 0.013 | 0.083 | **0.017** |
| `ACTIN_FILAMENT_ORGANIZATION` | 0.000 | 0.451 | 0.000 | 0.014 | **0.016** |
| `MYELOID_LEUKOCYTE_ACTIVATION` | 0.000 | — | 0.000 | 0.003 | 0.082 |
| `ADAPTIVE_IMMUNE_RESPONSE` | 0.000 | — | 0.000 | 0.038 | 0.269 |

**The two terms that require actual immune cells — myeloid leukocyte activation and adaptive immune
response — are the two that fail in cell lines**, while every cell-autonomous defence and inflammatory
term holds. That is the pattern a genuine cell-intrinsic signal produces and an infiltrate artefact
cannot. We did not design that control; it fell out of including CCLE.

### 31c. The honest deflation: this may be shared regulation, not partnership

**MVP is an interferon-gamma-inducible gene.** Co-abundance with other interferon-stimulated and
inflammatory proteins is therefore partly expected from **shared transcriptional control**, not shared
function — the identical objection that downgraded #26. What this scan may be detecting is the
regulatory program that *sets MVP's level*, which is precisely the AHR/STAT1-IRF1 licensing model argon
proposed as its H2 and which we had no counterpart for.

So the result is better read as: **MVP's abundance is governed by, and co-varies with, a cell-autonomous
innate-immune program, reproducibly, across five datasets and in cells with no immune system.** That is
a real and replicating fact. It is not evidence of a functional module, and we are not calling it one.

### 31d. The membrane hypothesis dies a fifth time, including in the unbiased scan

| previously favoured term | replicates in |
|---|---|
| `GOBP_PLASMA_MEMBRANE_REPAIR` | **1 of 5** (CCLE only) |
| `GOCC_CAVEOLA` | 1 of 5 |
| `GOBP_PLASMA_MEMBRANE_ORGANIZATION` | 1 of 5 |
| `GOCC_LATE_ENDOSOME` | 0 of 5 |
| `GOBP_ENDOSOMAL_TRANSPORT` | 0 of 5 |

The one dataset where plasma membrane repair clears is CCLE — exactly as §30 concluded, it is a
cell-line-specific result. **Note that a different membrane-adjacent program does replicate:** ruffle
and actin filament organisation, in 4 of 5 including CCLE. Ruffles are macropinocytic structures. That
is not the repair/caveolar compartment we proposed and we are not claiming it as a rescue.

### 31e. Four unused interactome datasets, and one crosslink already in our own files

Argon was asked the single question of whether a physical-interaction dataset exists that we have not
used, since co-abundance has now failed this question five times and is plainly the wrong instrument.
Its answer, with the local 2025-26 corpus checked and nothing additional found there:

1. **Zheng et al., *Sci Data* 2025, PMID 40058474** (PRIDE PXD052745; Figshare
   10.6084/m9.figshare.27906234) — `V5-TurboID` proximity labelling across **all 17 human PARP family
   members including PARP4**, in HEK293T. Covalent in-cell labelling before lysis, and **16 matched
   non-vault PARP baits in the same batch as a built-in specificity background.** This is the best
   available instrument for the neighbourhood question.
2. **CFdb — Skinnider et al., *Nat Commun* 2023, PMID 38102123** — 411 harmonised native
   co-fractionation MS datasets, no detergent wash-off. The argument is sharp: an intact 13 MDa vault
   elutes in megadalton fractions where soluble monomers like CAPN2, EHD4 and IQGAP1 cannot migrate
   alone, so **co-elution with the MVP-PARP4-TEP1 peak is a direct test of native physical
   association.**
3. **OpenCell — Cho et al., *Science* 2022, PMID 35271311** — endogenous knock-in IP-MS under mild
   digitonin, which preserves peripheral membrane assemblies that NP-40 lysis in BioPlex strips.
4. **Kurusu et al., *Dev Cell* 2023, PMID 37192622** — particle-sorted p62-body proteomics identifying
   intact vaults as selective autophagy cargo.

**Two negatives it checked so we do not waste effort.** In the Human Cell Map (Go et al. 2021, 192
compartment BioID baits), **EHD4, IQGAP1 and MYOF are high-confidence endosome and plasma-membrane
preys while MVP, PARP4 and TEP1 are completely absent at BFDR <= 0.01.** That is an independent negative
against the membrane neighbourhood and worth more than another co-abundance run.

**And one we already owned without noticing:** Fasci et al. 2018 proteome-wide crosslinking MS
(PMID 30021884), already inside our own `intact_MVP.json`, contains an **in-situ MVP-FLOT2 crosslink**.
Flotillin-2 is an SPFH-family protein. We had that file on disk throughout and never read it — the third
literature gap of the session after Moadab and Izquierdo.

## 32. The TurboID contact test is UNINFORMATIVE, for a reason argon predicted and we failed to gate on

`TURBOID_PREREGISTRATION.md`. Zheng et al. 2025 (PMID 40058474), `V5-TurboID` across all 17 human PARP
family members in HEK293T, with 16 matched non-vault baits as specificity background.

**The dataset is excellent and both gates passed emphatically.** PARP4 self-labels at log2 fold-change
**7.30**, p = 3.2e-4, and **17 of 17 baits enrich their own gene symbol**. There is nothing wrong with
the experiment.

**MVP is absent from the PARP4 sheet, and the reason is depth.**

| | preys measured | MVP detected |
|---|---|---|
| PARP1 | 4,297 | no |
| **PARP4** | **4,829** | **no** |
| PARP5B | 5,086 | yes |
| PARP2, PARP3, PARP9 | 5,502-5,605 | no |
| PARP11 … PARP8 | 6,100-8,779 | mostly yes |

**PARP4's run is the second-shallowest of seventeen.** MVP is missing from essentially every shallow
run and appears once depth passes about 5,000 proteins; it is detected in 9 of 17 baits overall. This is
ordinary data-dependent-acquisition missingness, not evidence about vaults.

By the registered rule, absence is **uninformative on presence** rather than the kill condition, which
required MVP present-and-not-enriched. The primary test therefore returns no answer.

**For the record, MVP's behaviour where it was measured:** enriched in only 2 of 9 baits (PARP11 fc
+2.13, p = 0.002; PARP15 +1.59, p = 0.009) and significantly *depleted* in PARP12 (−1.95, p = 0.004).
So MVP is not generically biotinylated by any cytoplasmic bait, which is mildly reassuring about the
assay but says nothing about PARP4.

### 32a. The tertiary test is void, and we are not reporting its negatives as findings

The tertiary test asked whether the membrane and immune modules appear among PARP4-proximal proteins. It
returned null for everything — plasma membrane repair 0 observed against 2.3 expected (p = 1.0), caveola
p = 0.71, late endosome p = 0.57, endosomal transport p = 0.675, inflammatory response p = 0.31, ruffle
p = 0.575, antigen processing p = 0.94, with response to bacterium alone borderline at p = 0.05.

**We are not calling that a sixth death of the membrane hypothesis, because the premise is unverified.**
If the PARP4 run is too shallow to detect MVP, we cannot confirm that this `V5-TurboID-PARP4` construct
was incorporated into vaults at all — and if it was not, its neighbourhood is PARP4's, not the vault's.
Reporting these nulls as contact-level refutation would be overclaiming in the direction that happens to
suit us, which is the same error as overclaiming in the other direction.

**One observation recorded without interpretation:** several proteins we championed are not merely
absent from PARP4's neighbourhood but significantly *depleted* from it — MYOF −3.32 (p = 3.4e-4),
IQGAP1 −2.82 (p = 1.0e-4), FLOT1 −2.16 (p = 1.2e-4), with AHNAK, S100A10 and CAPN2 negative at marginal
p. Real numbers in a gate-passing dataset, uninterpretable without MVP present.

### 32b. Argon specified the correct gate and we demoted it to an outcome

Its message read: *"Require MVP to be a top-ranked `V5-TurboID-PARP4` prey first (HEK293T has modest
endogenous MVP, and lumenally encapsulated PARP4 will only biotinylate external/membrane neighbors via
open/waisted particles, assembly intermediates, or exchangeable PARP4)."*

**That is exactly the gate this test needed, and we made it the primary test instead.** Had MVP's
presence been a gate, the analysis would have aborted before producing seven nulls we now cannot
interpret. The pre-registered sealed-shell asymmetry — that a negative for external membrane proteins is
expected and must not be read as refutation — was written down in advance and is being honoured, but it
is secondary to the simpler point that the construct's vault membership is unverified.

**What would make this work:** the same analysis on a bait with deeper coverage, or MVP-TurboID rather
than PARP4-TurboID, or CFdb native co-fractionation (PMID 38102123), where a 13 MDa particle elutes in
megadalton fractions that soluble monomers cannot reach. That remains the best untried instrument.

## 33. CFdb native co-fractionation: MVP and PARP4 are a reciprocal exclusive pair, and nothing else is there

`CFDB_PREREGISTRATION.md`, threshold in `CFDB_DEVIATIONS.md`. Skinnider, Akinlaja & Foster,
*Nat Commun* 2023 (PMID 38102123): 411 harmonised co-fractionation MS datasets, 21,703 fractions,
47,455,274 scored human pairs. Native separations, no detergent IP, no wash-off. 69,120 pairs at the
conventional precision >= 0.50.

**Gates pass emphatically.** PSMA1 returns **34** proteasome partners and RPL7 returns **77** ribosomal
partners at precision >= 0.50, and the gates hold at 0.75 and 0.90. The instrument detects real
complexes.

### 33a. The primary result

**MVP has exactly one high-confidence partner in the entire human proteome, and it is PARP4.**
**PARP4 has exactly one, and it is MVP.** A reciprocal exclusive pair.

| protein | CFdb degree at precision >= 0.50 |
|---|---|
| **MVP** | **1** (PARP4) |
| **PARP4** | **1** (MVP) |
| TEP1 | 0 |
| PARP1 | **133** |
| ANXA2 | **27** |
| FLOT1 | 1 |
| CD63 | 0 |

The two comparisons that matter are in that table. **PARP1 has 133 partners**, so the method is not
simply failing on PARP-family proteins. **ANXA2 has 27 partners**, so ANXA2 is well measured and well
connected in this resource — it is simply **not connected to MVP**. That is a well-powered negative, not
an absence of data.

This is the sixth independent instrument to recover MVP-PARP4: co-abundance across 13 cohorts, CCLE,
all 8 CPTAC cohorts after confound removal, anti-MVP IP-MS, *Dictyostelium* proximity labelling, and now
native co-fractionation. **And this one carries size information the others did not** — an intact 13 MDa
particle cannot co-elute with free monomers by accident.

**Honest caveat on strength:** the MVP-PARP4 edge sits between precision 0.50 and 0.75. At >= 0.75 and
>= 0.90 MVP drops out entirely (degree 0). So it is high-confidence by the conventional threshold and
not top-tier. TEP1 has degree 0 at every threshold, which the registration declared uninformative in
advance given how sparsely TEP1 is measured.

### 33b. Both neighbourhoods get zero contact-level support

Against 200 degree-matched random sets, among MVP's partners:

| term | members in CFdb | observed | p |
|---|---|---|---|
| `GOBP_PLASMA_MEMBRANE_REPAIR` | 12 | **0** | 1.0 |
| `GOCC_CAVEOLA` | 19 | **0** | 1.0 |
| `GOBP_PLASMA_MEMBRANE_ORGANIZATION` | 46 | **0** | 1.0 |
| `GOCC_LATE_ENDOSOME` | 90 | **0** | 1.0 |
| `GOBP_RESPONSE_TO_BACTERIUM` | 154 | **0** | 1.0 |
| `GOCC_RUFFLE` | 73 | **0** | 1.0 |
| `GOBP_ANTIGEN_PROCESSING_AND_PRESENTATION` | 37 | **0** | 1.0 |
| `GOBP_INFLAMMATORY_RESPONSE` | 160 | 1 | 0.05 |

**The single observation in inflammatory response is PARP4 itself**, which is annotated to that term
(verified: PARP4 is a member, MVP is not). So the nominal p = 0.05 is an artefact of PARP4's own GO
annotation and there is **zero independent support** for the immune neighbourhood here.

### 33c. Where this leaves both hypotheses

The registration committed in advance: *"Both finished if neither clears while the gates pass. After
five co-abundance failures and one void contact test, a null in a native size-resolved instrument with
working gates is the end of the line for both as physical-association claims, and we will say so."*

**We say so.**

- **The membrane-repair neighbourhood is finished as a physical-association claim.** Sixth test, and the
  first where the negative is well-powered rather than ambiguous: ANXA2 has 27 partners in this resource
  and MVP is not among them.
- **The innate-immune neighbourhood from §31 is also finished as a physical claim.** It survives only
  as what §31c already said it was — a reproducible covariation with a cell-autonomous innate-immune
  program, most plausibly shared transcriptional regulation of an interferon-inducible gene, not a
  complex.
- **MVP-PARP4 is as close to established as anything in this work gets.** Six instruments, including one
  with a size discriminator, and in the native data it is exclusive on both sides.

**The positive reading of the whole arc.** A particle whose only stable partner is its own internal
enzyme, in an instrument that happily assigns PARP1 133 partners and ANXA2 27, is behaving exactly like
a **sealed compartment**. That is consistent with §12's geometry — a wall that admits nothing larger
than water radially — and with the absence of any broad neighbourhood in five instruments. The vault may
have no neighbourhood because it is a container, and containers do not have one.

## 34. Argon's licensing model: UNINFORMATIVE on a mis-specified gate, with both predictions confirmed anyway

`LICENSING_PREREGISTRATION.md`, deviation in `LICENSING_DEVIATIONS.md`. Tests argon's H2 (#103) — the
only mechanism anyone has offered for #19, MVP at the 95th interferon percentile while blood and
lymphocyte are the lowest lineages — against the N:C confound argon itself found.

**Formal verdict: UNINFORMATIVE. The gate failed.** Argon's own specification required STAT1 to track
TAP1 at Spearman rho > 0.6. After residualisation it is **0.369**.

**The gate was never achievable, and that is my error not the data's.** STAT1-TAP1 is **0.42 on raw,
unresidualised protein** — below the threshold before anything was removed. Argon proposed that gate for
transcript-level data, where interferon-axis correlations are tighter; I applied it to proteomics without
checking it was reachable. A correctly chosen control for this axis was sitting in the same matrix:
**TAP1-TAP2 at 0.957** (an obligate heterodimer) and TAP1-B2M at 0.613. The antigen-presentation axis is
perfectly coherent here. The gate simply asked the wrong pair.

### 34a. What the numbers show, reported but not licensed

| protein | raw rho vs MVP | residualised |
|---|---|---|
| B2M | +0.325 | **+0.426** |
| TAP1 | +0.423 | **+0.380** |
| TAP2 | +0.428 | **+0.359** |
| STAT1 | +0.452 | **+0.351** |
| IRF9 | +0.288 | **+0.351** |
| AHR | +0.465 | +0.279 |
| STAT2 | +0.317 | +0.183 |
| SP1 | −0.458 | −0.168 |
| **ARNT** | −0.191 | **−0.021** |
| EZH2 | −0.498 | −0.256 |
| EED | −0.332 | −0.180 |
| SUZ12 | −0.360 | −0.260 |

**Both registered predictions were confirmed.**

**The interferon arm is robust to the confound.** STAT1, IRF9, TAP1, TAP2 and B2M all sit at +0.35 to
+0.43 after residualisation, and B2M and IRF9 *strengthen*. This is the expected behaviour of a genuinely
interferon-inducible gene and it is independent of compartment.

**The AHR arm is weak and has an internal problem.** AHR drops from +0.465 to +0.279, and **ARNT — AHR's
obligate dimerisation partner — goes to −0.021.** If AHR were acting as a transcription factor on MVP,
ARNT should track with it. It does not. That is a specific argument against the AHR limb that we did not
register and are reporting because it cuts against the hypothesis.

### 34b. The EZH2 limb is a compartment artefact, as predicted before testing

The registration stated the reason in advance: the N:C proxy is *cytosolic minus nuclear*, MVP is
cytoplasmic and EZH2 is nuclear, so the two anti-correlate through it by construction.

Argon's reported **−0.756** becomes **−0.256** after residualisation. Against 200 random
`GOCC_NUCLEAR_BODY` proteins, whose residualised correlations with MVP have mean −0.073 and 5th
percentile −0.302, **EZH2 sits at the 11.5th percentile — inside the bulk of the nuclear distribution,
not below it.** Its PRC2 partners behave identically (EED −0.180, SUZ12 −0.260).

**EZH2 is unremarkable among nuclear proteins.** There is no EZH2-specific silencing signal here, only
the compartment effect.

### 34c. Status of #103

Not struck, because the kill condition required the activating arm to fail *and* EZH2 to be an artefact,
and only the second happened. Not supported either, because the gate failed. **#103 remains open with
its evidence rebalanced:** the interferon/antigen-presentation limb has real correlational support that
survives the confound, the EZH2/PRC2 limb has none, and the AHR limb is weak and contradicted by its own
dimerisation partner.

What would decide it is the perturbation arm argon specified and we cannot reach from here: promoter
H3K27me3 and methylation at the MVP TSS across lineages, MVP response to EZH2 inhibition, and MVP
response to AHR antagonism. Those need GEO and ENCODE data not held locally.

### 34d. Third gate-design error of the session

This is a pattern worth naming. §29's EMT control failed because I required CDH1 at |r| >= 0.3 from an
asymmetric signature where that is not expected. §32's TurboID test was voided because I took a
prerequisite argon stated plainly and made it the primary test instead of a gate. §34 failed because I
adopted a threshold specified for transcript data and applied it to protein without checking it was
reachable — when a better control for the same axis, TAP1-TAP2 at 0.957, was in the same file.

**Gates have to be chosen from the data's own achievable range, not from the hypothesis or from
memory.** Three tests this session returned no answer for that reason, which is a larger toll than any
single wrong result.

## 35. Grok audit of §31-34: the container reading dies, the dyad survives reframed, and COAD is a real counterexample

`grok/to-grok/001-*.md` and `grok/from-grok/001r-*.md`. Grok was given the numbers inline with no file
or tool access, so the exchange is reproducible and it could not touch the repository. It was asked to
attack two claims. Both verdicts came back **SURVIVES WEAKENED**, and the reasoning cost us more than
either verdict.

### 35a. Three withdrawals on §33, all correct

1. **"Reciprocal exclusive pair" is a free claim.** CFdb scores are symmetric, so every edge is
   reciprocal by construction and the assay cannot fail that test. MVP degree 1 and PARP4 degree 1 are
   **one isolated dyad**, not two independent observations. Withdrawn.
2. **The GO enrichment at n = 1 had no power.** With MVP having exactly one partner, "0 observed,
   p = 1.0" is the null output of a one-sided test, not evidence of depletion — the test was only ever
   asking whether PARP4 carries the annotation. **§33's "well-powered negative" claim is withdrawn.**
   The ANXA2-has-27-partners observation remains relevant to coverage but does not make the enrichment
   test powered.
3. **TEP1's absence is a false negative inside the particle itself.** We now have the number:
   **precision(MVP-TEP1) = 0.041**, score 0.0125 — at the noise floor, not just below the cut. So
   sensitivity for known vault subunits in this instrument is **1 of 2**, and "no other neighbours" is
   produced by the same process that lost TEP1.

### 35b. But the decisive test grok specified comes back a cliff, not a threshold artefact

It identified that thresholding at 0.50 destroyed the only contrast that could separate three worlds,
and that the diagnostic was the shape of MVP's full precision list. Run on all 10,614 of MVP's scored
pairs:

| rank | MVP partner | score | precision |
|---|---|---|---|
| **1** | **PARP4** | **0.2722** | **0.676** |
| 2 | ZNF598 | 0.1378 | 0.382 |
| 3 | RPL8 | 0.1179 | 0.329 |
| 4 | ZC3HAV1 | 0.1161 | 0.324 |
| 5 | EIF3A | 0.1148 | 0.320 |

**PARP4 sits at the 99.99th percentile of MVP's 10,614 scores, with twice the score of rank 2 and then
a smooth plateau.** That is the cliff, and it excludes grok's ramp and flat worlds.

**And the right control was in the same file.** FLOT1, a known obligate heterodimer partner of FLOT2:
FLOT2 at precision 0.599, then a drop to 0.258. **Identical shape to MVP-PARP4.** Meanwhile PSMA1 has
ten partners at precision 1.000 with scores of 0.93-0.97.

So the instrument distinguishes three regimes, and MVP is clearly in the second: **a large obligate
machine (PSMA1), a binary complex (FLOT1-FLOT2, MVP-PARP4), and noise.** MVP-PARP4 behaves like a
binary complex by this instrument's own standard.

### 35c. The container reading is killed

Grok's closing argument is right and we accept it: a sealed obligate container, an inert homooligomer,
an RNA-binding particle, a partially occupied vault, a transient interactor, and a protein measured just
well enough to return its one database edge all produce this graph. The vault loses its only edge one
threshold up and fails to recover TEP1, which is the wrong shape for the analogy.

**#135 is struck.** What stands is narrower: *MVP has no co-eluting neighbourhood above precision 0.50
except a mid-precision PARP4 edge, and that edge has the profile of a binary complex rather than a
multi-subunit machine.*

### 35d. New observation we had thresholded away

MVP's ranks 2-12 are **translation and RNA machinery**: ZNF598 (ribosome quality control), RPL8, RPL30,
EIF3A, EIF3C, UPF1 (nonsense-mediated decay), GIGYF2, FAM120A, ZC3HAV1 (ZAP). All at precision
0.30-0.38, below our cut, never seen until grok asked for the list.

Not membrane. Not immune. **Consistent with MVP being templated on polyribosomes and binding vault
RNA** — a connection the published literature makes and our analysis never touched. Recorded as an
observation; it has had no test.

### 35e. §31 weakens badly, and COAD is the reason

**brain_cptac and gbm_cptac are both central nervous system.** So the headline "4 of 5 datasets" is
really **CNS counted twice, plus UCEC, plus cell lines**, with colorectal null. Grok caught this; we
had treated five datasets as five tissue contexts.

**And COAD is not a dead dataset.** Grok specified the test: seed COAD with PSMA1 and see whether the
proteasome replicates there. It does — **6 of 7 proteasome terms at q < 0.05, five at q = 0.0000.** The
method has ample power in COAD and returns **q = 1.000 for every immune term**. Colorectal is also one
of the tissues where the vault holoenzyme is most abundant (§27a).

**So COAD is a real counterexample and cannot be set aside.** Effective replication is two tissue
contexts plus cell lines positive, one tissue context with demonstrated power negative.

**Also conceded:** 103 replicating terms are overlapping DAG slices, roughly **two independent
signals** — an interferon/MHC-I block and a cortical actin block — not 103 results.

### 35f. The test we should have run, and what it shows

Grok: *"'so I deflated it to shared regulation' is not a test. Partial r(MVP, TAP1 | STAT1, IRF9) is the
test, and it is in the matrices you have."* Correct. Run on CCLE, n = 330, all controlled for N:C and
proliferation:

| pair | residualised | partial on STAT1 + IRF9 |
|---|---|---|
| MVP-B2M | +0.426 | **+0.270** (p < 1e-4) |
| MVP-AHR | +0.279 | **+0.231** (p < 1e-4) |
| MVP-TAP1 | +0.380 | **+0.216** (p = 1e-4) |
| MVP-TAP2 | +0.359 | **+0.204** (p = 2e-4) |

**Neither collapse nor clean survival: roughly 45% of the association is STAT1/IRF9-mediated and the
remainder is not.** By grok's own framing that makes it partly regulon re-description and partly
something else. We add the caveat it did not: STAT1 and IRF9 *protein* are imperfect proxies for pathway
activity, so this under-corrects and the residual 0.20-0.27 may still be regulon.

### 35g. Two further corrections we accept

**The ruffle/actin cluster was selective attention.** `GOCC_RUFFLE` replicates at the same bar as
inflammatory response (0.001 / 1.000 / 0.012 / 0.032 / 0.010, 4 of 5 including CCLE) and actin filament
organisation likewise. We set them aside because they did not fit an immune sentence. They are reported
at equal standing from here, and grok's point stands that the cortical block is the half of the scan
that interferon inducibility does **not** predict.

**The EZH2 statistic was mis-stated.** 11.5th percentile of 200 nuclear proteins means about 23 are more
negative, an empirical one-sided p of roughly 0.12. That is the **left tail**, so "inside the bulk of
the nuclear distribution" was wrong. The correct statement: EZH2 is modestly more negative than typical
nuclear proteins but nowhere near the 5th percentile registered for a specific-silencing call. Too weak
to support PRC2 silencing, and not the clean artefact we described.

## 36. Removing the interferon axis: the reviewer's prediction was right, and what survives is cortical actin

`IFN_RESIDUAL_PREREGISTRATION.md`. The test grok specified and we registered under its prediction, not
ours: residualise all five matrices on **STAT1 + IRF9** in addition to the N:C proxy and proliferation,
then rerun the §31 scan unchanged.

**All three gates pass, including the one that makes it interpretable.** PARP4 remains MVP's rank-1
correlate in all five datasets; PSMA1 still recovers 12-25 of 25 proteasome subunits and six proteasome
terms still replicate; and **TAP1 is displaced out of MVP's top 200 in 5 of 5 datasets** — to ranks 558,
806, 1342, 4238 and 7042. The interferon axis really was removed.

**103 replicating terms fall to 52.** But the count is not the result; the composition is.

### 36a. Disaggregated by tissue, because the raw count repeats the error grok caught

Two of the five datasets are central nervous system (brain and glioblastoma), so we report how many of
the **three non-CNS datasets** — colorectal, endometrium and cell lines — support each term:

| term | brain | coad | gbm | ucec | **CCLE** | non-CNS |
|---|---|---|---|---|---|---|
| `GOCC_RUFFLE` | 0.001 | 0.971 | 0.042 | 0.003 | **0.004** | **2/3** |
| `GOBP_ACTIN_FILAMENT_ORGANIZATION` | 0.000 | 0.663 | 0.000 | 0.003 | **0.001** | **2/3** |
| `GOBP_INFLAMMATORY_RESPONSE` | 0.000 | 1.000 | 0.000 | 0.000 | **0.000** | **2/3** |
| `GOCC_LAMELLIPODIUM` | 0.004 | 1.000 | 0.030 | 0.332 | 0.045 | 1/3 |
| `GOCC_CELL_LEADING_EDGE` | 0.000 | 1.000 | 0.002 | 0.077 | 0.001 | 1/3 |
| `GOBP_WOUND_HEALING` | 0.000 | 1.000 | 0.000 | 0.428 | 0.000 | 1/3 |
| `GOBP_CELL_SUBSTRATE_ADHESION` | 0.003 | 1.000 | 0.001 | 0.889 | 0.000 | 1/3 |
| `GOBP_RESPONSE_TO_BACTERIUM` | 0.028 | 1.000 | 0.001 | 0.003 | 0.114 | 1/3 |
| **`GOBP_ANTIGEN_PROCESSING_AND_PRESENTATION`** | 0.000 | 1.000 | 0.000 | 0.596 | **0.617** | **0/3** |
| **`GOBP_RESPONSE_TO_TYPE_II_INTERFERON`** | 0.000 | 1.000 | 0.019 | 0.219 | **0.476** | **0/3** |

### 36b. The prediction was right, and it was not ours

**The interferon-specific terms are now CNS-only.** Antigen processing and presentation and response to
type II interferon each hold in brain and glioblastoma and in **neither** colorectal, endometrium nor
cell lines. Removing STAT1 and IRF9 removed them everywhere it mattered. **§31's interferon and
antigen-presentation signal was substantially a re-description of the interferon regulon**, exactly as
grok argued and we had only asserted.

**And the cortical block survives with non-CNS support.** Membrane ruffling and actin filament
organisation each hold in endometrium *and* cell lines after the axis is gone — and cell lines contain
no immune system, so neither infiltrate nor interferon tone explains them. They were in §31 at the same
bar as the immune terms and we set them aside because they did not fit the story we were telling.

### 36c. Where the prediction was only half right

`GOBP_INFLAMMATORY_RESPONSE` also survives at 2 of 3 non-CNS, at q = 0.000 in both endometrium and cell
lines. So "the immune block dies" is too strong: **the interferon-specific part dies and the broader
inflammatory part does not.** Inflammatory response is a wider set than the interferon axis and is not
removed by residualising STAT1 and IRF9. We report that against the registered prediction rather than
rounding it to a clean win.

### 36d. What this licenses, and the four things it does not

**Licensed:** after removing the interferon axis, MVP's only co-abundance neighbourhood terms with
support in more than one non-CNS dataset are **membrane ruffling, actin filament organisation and
inflammatory response.** Everything interferon-specific is confined to one tissue.

**Not licensed, and each of these is live:**

1. **This is co-abundance, not contact.** CFdb found nothing resembling a cortical actin neighbourhood
   around MVP — MVP's only native co-eluting partner is PARP4. §33 and §36 are measuring different
   things and only one of them reports physical association.
2. **COAD is null for every term in the table.** It passed its gates with 12 of 25 proteasome subunits
   recovered, so this is not a power problem. The colorectal counterexample from §35e stands unchanged.
3. **The correction under-corrects.** STAT1 and IRF9 *protein* are imperfect proxies for pathway
   activity, so surviving terms may still be partly regulon.
4. **A cytoskeletal-abundance confound is untested.** MVP is an abundant cytoplasmic protein and the
   actin cortex is the most abundant cytoplasmic structure; residualising on a nuclear-to-cytoplasmic
   ratio does not remove within-cytoplasm composition. **That is the obvious next control and we have
   not run it**, so the cortical result should be read as the best-surviving candidate rather than as
   established.

## 37. The abundance control fails to kill the cortical result, and strengthens it

`CYTO_COMPOSITION_PREREGISTRATION.md`. We expected this to kill #155 and registered that expectation.
**It did not.**

**Gate passed in 3 of 3 non-CNS datasets:** PSMA1-seeded proteasome terms clear abundance-matched
specificity at p = 0.000 everywhere, so the matching does not over-correct.

### 37a. Result

Specificity against 200 size- and abundance-matched random sets, in the §36 residualisation
(N:C + proliferation + STAT1 + IRF9):

| term | coad | ucec | CCLE | non-CNS |
|---|---|---|---|---|
| `GOBP_ACTIN_FILAMENT_ORGANIZATION` | **0.015** | **0.000** | **0.000** | **3/3** |
| `GOCC_RUFFLE` | 0.050 | **0.000** | **0.000** | 2/3 clear + 1 borderline |
| `GOBP_INFLAMMATORY_RESPONSE` | 0.855 | **0.000** | **0.000** | 2/3 |
| *neg control:* antigen processing | 0.715 | 0.385 | 0.435 | **0/3** |
| *neg control:* response to type II interferon | 0.585 | 0.035 | 0.080 | **1/3** |

Observed against expected is not marginal: ruffle gives 13 observed against 3.1 expected in endometrium
and 12 against 3.2 in cell lines; actin filament organisation gives 21 against 7.1 in both.

**The negative controls behaved.** Antigen processing and type II interferon stay dead across all three
non-CNS datasets — and both are p = 0.000 in brain and glioblastoma, exactly reproducing §36's finding
that they are CNS-only. Abundance matching did not resurrect them, so the matching is working.

### 37b. The specificity argument that makes this more than abundance

If MVP's top 200 were simply enriched for abundant cytoplasmic proteins, the largest abundant
cytoplasmic compartment should light up. **`GOCC_MITOCHONDRION` (1,086-1,328 members) is not enriched in
any dataset** — p = 0.465, 0.88, 1.0 across the three non-CNS sets, and 0.985 and 0.495 in the two CNS
sets. Golgi and endosome are mixed and inconsistent.

So the result is not "MVP correlates with whatever is abundant." It is specific to the actin cortex
among abundant compartments, which is the discrimination #157 said was missing.

### 37c. COAD, and an honest note about why it changed

**The colorectal cohort — the counterexample from §35e, null for every term in §36 — clears actin
filament organisation at p = 0.015 and sits exactly on 0.05 for ruffle**, while still rejecting
inflammatory response at p = 0.855.

**We are not claiming COAD "now supports" the result in the same sense, because this is a different
statistic.** §36 was a genome-wide scan of 8,634 terms with Benjamini-Hochberg correction across all of
them; §37 is a focused, pre-specified test of five terms with abundance-matched permutation. The focused
test has far more power and carries no correction burden across the ontology. Both results are correct
for what they are, and the difference is power, not biology.

What is fair to say: **under a properly abundance-matched test of pre-specified terms, the actin result
holds in all three non-CNS datasets including the one that rejected everything else, while the immune
terms do not.** That is a cleaner separation than §36 produced.

### 37d. What now stands, and the four things still against it

**#155 survives and is upgraded.** After removing the interferon axis and matching on abundance, MVP's
co-abundance neighbourhood contains cortical actin organisation in 3 of 3 non-CNS datasets and membrane
ruffling in 2 of 3 plus a borderline, with mitochondrion as a negative specificity control and the
interferon terms as negative replication controls. **This is now the best-supported neighbourhood claim
in the project — and it is one we dismissed in §31 and set aside again in §36 because it did not fit the
story we were telling.**

Standing objections, none of which this test addresses:

1. **CFdb found no cortical neighbourhood at all.** MVP's only native co-eluting partner is PARP4, and
   actin proteins are not among its scored partners above threshold. **Co-abundance and native
   co-elution disagree, and only co-elution reports physical association.** This is the single largest
   problem with #155 and it is unresolved.
2. **The circular control could not be run.** Sixteen of seventeen core actin genes are inside the
   tested sets, so we cannot residualise on actin machinery to ask whether the signal is specific to
   the cortex versus the whole actin system.
3. **Still co-abundance.** It reports covariation of abundance across samples, not contact. The vault is
   reported to be assembled on polyribosomes, and §35d's unexamined ranks 2-12 were translation and RNA
   machinery, so a cytoskeletal association could be a consequence of where the particle is synthesised
   rather than what it does.
4. **We expected this to die and said so in advance.** A survival against a registered expectation is
   worth more than a confirmation, but it is one test in one direction and we have reversed ourselves
   six times today.

## 38. The disagreement resolved: cortical actin is co-regulation, and definitely not contact

§37 upgraded #155 on co-abundance. §33 found nothing cortical in native co-fractionation. Those
instruments flatly contradict each other, and §37d named that as the result's largest problem. This is
the check that decides whether the co-elution negative is real or a coverage failure.

**CFdb degree at precision >= 0.50 for the cortical actin machinery:**

| protein | degree | MVP-linked |
|---|---|---|
| CFL1 | **170** | no |
| ACTB | **128** | no |
| ACTG1 | **117** | no |
| MYH9 | 90 | no |
| VCL | 85 | no |
| TLN1 | 80 | no |
| MSN | 58 | no |
| EZR | 46 | no |
| PFN1 | 42 | no |
| ACTR3 | 38 | no |
| RDX | 35 | no |
| ACTR2 | 32 | no |
| CORO1C | 29 | no |
| ARPC4 | 27 | no |
| FLNA | 26 | no |
| ARPC2 | 25 | no |
| ARPC1B, ARPC3 | 24 | no |
| ARPC5, ARPC1A, IQGAP1 | 18-19 | no |
| MYL6, CAPZB | 15-16 | no |
| WASF2, TMSB4X | 6-7 | no |

**All 25 of 25 are present with partners. Their degrees total 1,175 edges. Not one connects to MVP.**

For scale: MVP has 1, PARP4 has 1, ANXA2 27, PSMA1 34, PARP1 133.

**This is not a coverage failure.** The cortical actin machinery is among the best-covered material in
native co-fractionation — CFL1 alone has 170 high-confidence partners. If MVP physically associated with
the actin cortex at a level this instrument can see, there were 1,175 opportunities for it to show and it
took none of them. That is the well-powered negative we claimed for the membrane module in §33 and did
not actually have (#143); here we do.

### 38a. What that leaves

Two gated, replicated results that cannot both be describing contact:

- **Co-abundance** (5 datasets, interferon axis removed, abundance-matched): cortical actin organisation
  enriched around MVP in 3 of 3 non-CNS datasets, 13 observed against 3.1 expected for ruffling, with
  mitochondrion as a negative specificity control.
- **Native co-fractionation** (411 datasets): zero of 1,175 cortical actin edges touch MVP.

**The parsimonious reading, and the one we adopt: the cortical signal is co-regulation, not
association.** MVP abundance and actin-cortex abundance covary across samples because both track some
shared cellular state — adhesion, spreading, mechanical or cytoskeletal tone — without the proteins
being in contact. That is precisely the conclusion #26 reached for the membrane module, arrived at again
by a different route.

**#155 is therefore downgraded in kind, not in strength.** The covariation is real, replicated, specific
among abundant compartments and survives removal of the interferon axis. It is **not** evidence of a
physical neighbourhood, and we withdraw the word "neighbourhood" for it. The defensible claim is: *MVP
abundance co-varies with cortical actin and adhesion programs across tumours and cell lines,
independently of interferon tone and of protein abundance, and the two do not physically co-elute.*

### 38b. The consequence for the whole project

Three separate hypotheses have now produced the same pattern — membrane repair (§13, §30, §33), innate
immunity (§31, §36) and cortical actin (§37, §38): **a reproducible co-abundance signal with no
corresponding co-elution.** Co-abundance has been run eight times on the neighbourhood question and has
never once been corroborated by a contact instrument.

The honest generalisation is not about vaults. It is that **MVP's co-abundance correlates report cellular
state, and this project has repeatedly mistaken state for structure.** The only association that appears
in both kinds of instrument is MVP-PARP4.

## 39. MVP's sub-threshold co-elution tail: translation dominates, but the result is NOT SPECIFIC

`CFDB_SUBTHRESHOLD_PREREGISTRATION.md`. The one lead in this project that came from a contact instrument
rather than from co-abundance (#165), and the only one we never hypothesised: §35d reported that MVP's
CFdb ranks 2-12 by score are translation, ribosome-quality-control and RNA-handling proteins at precision
0.30-0.38, below the threshold §33 used.

**Both design gates passed emphatically.** On its own top 200 by score with the same degree matching,
PSMA1 recovers **42 of 59** proteasome-complex members against 1.0 expected, and RPL7 recovers **77 of
223** ribosomal proteins against 3.8. Sub-threshold CFdb ranking carries real complex signal.

**Result against 200 degree-matched random sets, MVP's top 200 by score:**

| term | observed | expected | p | fold |
|---|---|---|---|---|
| `GOBP_CYTOPLASMIC_TRANSLATION` | 47 | 2.6 | **0.000** | **18x** |
| `GOBP_TRANSLATION` | 67 | 9.4 | **0.000** | 7.1x |
| `GOCC_RIBOSOME` | 41 | 3.8 | **0.000** | 10.8x |
| `GOCC_RIBONUCLEOPROTEIN_COMPLEX` | 59 | 10.8 | **0.000** | 5.5x |
| `GOBP_RNA_CATABOLIC_PROCESS` | 12 | 4.1 | 0.055 | 2.9x |
| `GOCC_RUFFLE` | 9 | 2.5 | **0.000** | 3.6x |
| `GOBP_ACTIN_FILAMENT_ORGANIZATION` | 12 | 6.0 | 0.030 | 2.0x |
| `GOBP_PLASMA_MEMBRANE_REPAIR` | 2 | 0.4 | 0.075 | — |
| `GOBP_INFLAMMATORY_RESPONSE` | 4 | 7.8 | 0.710 | depleted |
| *negative control:* `GOCC_MITOCHONDRION` | 7 | 22.4 | 1.000 | **depleted** |

### 39a. The registered verdict is NOT SPECIFIC, and we report it as registered

The pre-registration fixed this outcome in advance: *"If the actin or immune comparators also clear, the
result is not specific and we report it as a generic property of MVP's score tail rather than as a
translation finding."* Ruffle clears at 0.000 and actin organisation at 0.030. **So this is a property of
the tail, not a translation finding, and the §35d observation does not graduate to a lead.**

### 39b. What is nonetheless true inside that verdict

The tail is **not** indiscriminate, and two numbers show it. `GOCC_MITOCHONDRION` — 1,313 members, the
largest abundant cytoplasmic compartment — is **depleted** (7 against 22.4 expected, p = 1.0), as is
inflammatory response. And the effect sizes are not comparable: **cytoplasmic translation is 18-fold
enriched** against 2.0-fold for actin organisation and 3.6-fold for ruffling.

So an honest description of MVP's sub-threshold co-elution tail is: heavily enriched for ribosomes and
translation machinery, mildly enriched for cortical actin, and depleted for mitochondria and
inflammation. **An order-of-magnitude difference between two things that both cleared is not what we
registered a threshold on, so it stays an observation.**

### 39c. Why it is worth recording anyway

It aligns with the one thing the vault literature is confident about and our analysis never touched:
**vaults are assembled on polyribosomes and carry a small RNA.** ZNF598 (ribosome quality control), RPL8,
RPL30, EIF3A, EIF3C, UPF1 (nonsense-mediated decay), GIGYF2 and ZC3HAV1 are the specific proteins at the
top of that tail.

It also supplies the alternative reading flagged in §38 for the cortical-actin result: if MVP co-elutes
with translation machinery, a cytoskeletal association may follow from **where the particle is
synthesised** rather than from what it does. That is now a competing explanation with data behind it
rather than a bare possibility — though it is itself sub-threshold, and CFdb's authors do not report
interactions at this precision. We do not call these interactions.

## 40. The translation tail IS specific to MVP, against our registered expectation

`TRANSLATION_SPECIFICITY_PREREGISTRATION.md`. We registered the expectation that MVP would be "high but
not extreme" and that the glycolytic comparators would "also be elevated", with a kill condition below
the 75th percentile. **Both halves of that expectation were wrong.**

**Both gates passed.** Ribosomal seeds are extreme as they must be — RPL7 at 30.3x (98.7th percentile),
RPS6 at 31.9x (98.7th) — and PSMA1 sits at 2.75x (70th), so the measure discriminates rather than
calling everything extreme.

Random reference distribution over 150 seed proteins with at least 5,000 scored partners each:
**median 1.57x, 75th percentile 2.75x, 95th percentile 8.09x, maximum 31.87x.**

| seed | role | fold | percentile |
|---|---|---|---|
| RPS6 | gate: expect high | 31.9x | 98.7 |
| RPL7 | gate: expect high | 30.3x | 98.7 |
| **MVP** | **under test** | **18.5x** | **98.0** |
| PKM | abundant cytoplasmic | 3.5x | 79.3 |
| ALDOA | abundant cytoplasmic | 3.2x | 75.3 |
| PSMA1 | gate: expect low | 2.8x | 70.0 |
| GAPDH | abundant cytoplasmic | 2.8x | 70.0 |
| FLOT2 | SPFH family | 2.8x | 70.0 |
| FLOT1 | SPFH family | 2.4x | 60.0 |
| ENO1 | abundant cytoplasmic | 2.0x | 52.0 |
| STOM | SPFH family | 1.6x | 41.3 |
| LDHA | abundant cytoplasmic | 1.2x | 26.0 |

**Verdict: MVP-SPECIFIC at the 98.0th percentile.**

### 40a. Why the comparators matter more than MVP's number

The premise we set out to test was that translation machinery dominates every abundant cytoplasmic
protein's co-elution tail. **It does not.** Five abundant glycolytic enzymes span the 26th to 79th
percentile — GAPDH and ENO1, two of the most abundant proteins in the cytoplasm, sit at 70th and 52nd.
So a translation-enriched tail is not what abundance buys you in this instrument.

**Nor is it an SPFH-family property.** FLOT1, FLOT2 and STOM land at the 60th, 70th and 41st percentiles.
MVP's own domain family does not do this, which is the same discrimination §30 found for the membrane
module and in the same direction: whatever this is, it is about the vault and not about SPFH proteins.

MVP sits with the ribosomal proteins — 18.5x against RPL7's 30.3x and RPS6's 31.9x — and clear of every
non-translational comparator.

### 40b. This does not overturn §39, and the distinction is worth stating precisely

§39 registered the verdict **NOT SPECIFIC** and that verdict stands. The two tests ask different
specificity questions:

- **§39, across terms:** within MVP's tail, is translation enriched *and other things not*? Answer: no —
  ruffle and actin organisation also cleared, so the tail is not exclusively translational.
- **§40, across seeds:** among comparable proteins, is MVP's translation enrichment unusual? Answer:
  yes — 98th percentile, with abundant and SPFH controls unremarkable.

Both are true. The tail contains more than translation, **and** the translation component is specific to
MVP. §39's effect-size observation — 18-fold for translation against 2.0-fold for actin — now has the
comparison behind it that we said it lacked, and it is the across-seed comparison that supplies it.

### 40c. What it supports, and the four limits that remain

**#168 survives and strengthens.** The competing explanation for #155 — that MVP's cortical-actin
covariation may follow from where the particle is synthesised rather than from what it does — now rests
on a specific, gated, control-bearing result rather than on a raw fold-enrichment.

It also aligns with the published claim this project never tested: **vaults are assembled on
polyribosomes.** We did not discover that. What is new is that it is visible in native co-fractionation
of 411 datasets, in a measure where MVP sits beside ribosomal proteins and clear of its own domain
family.

Limits, all live:

1. **Precision 0.30-0.38 is below the level CFdb's authors report interactions at.** These are not
   interactions and we do not call them that.
2. **Co-elution is not contact** (§38). A 13 MDa particle assembled on a polyribosome would co-elute with
   ribosomal material for reasons of shared sedimentation and synthesis, which is a different claim from
   physical association.
3. **This is one instrument.** Everything that died tonight died on replication or on a second
   instrument, and this result has had neither.
4. **Our expectation was wrong twice over**, which is the correct reason to trust the result more and our
   judgement about it less. The registered prediction said MVP would be unremarkable and the glycolytic
   controls elevated; the data said the reverse on both counts.

## 41. The translation result does NOT replicate in the contact instrument — and the temptation to rescue it is the finding

`IPMS_TRANSLATION_PREREGISTRATION.md`. The registered kill condition fired.

**The gate passed emphatically.** The anti-MVP pulldown recovers all three vault components, not two:
MVP (WT_LFC 7.62, LWTP 3.80), PARP4 (8.66, 3.32), TEP1 (6.27, 3.33). This experiment unambiguously
captures the particle.

**Primary: no translation enrichment.** Among the 88 WT vault interactors of 1,205 proteins, against 200
size- and abundance-matched random sets drawn from the IP-MS universe itself:

| term | in universe | observed | expected | p |
|---|---|---|---|---|
| `GOBP_CYTOPLASMIC_TRANSLATION` | 95 | 9 | 6.94 | **0.195** |
| `GOCC_RIBOSOME` | 134 | 11 | 9.79 | 0.545 |
| `GOBP_TRANSLATION` | 191 | 15 | 13.95 | 0.530 |
| `GOCC_RUFFLE` | 27 | 1 | 1.97 | 0.850 |
| `GOBP_ACTIN_FILAMENT_ORGANIZATION` | 65 | 7 | 4.75 | 0.195 |
| `GOCC_MITOCHONDRION` | 191 | 17 | 13.95 | 0.275 |

**Nothing is enriched** — not translation, not actin, not mitochondria. Per the registration, §40's
result is therefore recorded as a **co-migration property, not evidence of physical association**:
consistent with a 13 MDa particle assembled on and sedimenting with polyribosomes, which is a different
claim from being attached to them. #168 and #172 are amended accordingly.

### 41a. The power caveat was wrong, and the null is stronger than we said

We originally wrote here that the test "could not have detected a modest enrichment; it is only powered
for a large one." **We computed the power and that was wrong in the direction generous to the dead
hypothesis.** `src/power41.py`:

With N = 1,205, K = 88 interactors and M = 95 term members, the critical value at α = 0.05 is **12
observed (1.73x)**, and the test had:

| true enrichment | expected obs | power |
|---|---|---|
| 1.5x | 10.4 | 0.34 |
| **2.09x** | **14.5** | **0.80** |
| 2.5x | 17.3 | 0.95 |
| 3.0x | 20.8 | **0.99** |
| 4.0x | 27.8 | 1.00 |

**80% power at 2.09x, and essentially certain detection at 3x and above.** 2.09x is a modest effect, not
a large one, so the original caveat understated the test. The observed 9 is 1.30x — below even the
critical value.

One honest qualification: §40's "18x" is an enrichment within a co-elution tail *ranking*, which is not
the same quantity as a hypergeometric fold-enrichment in an interactor set, so the two numbers are not
directly comparable and we do not claim 18x against 2.09x as a like-for-like contrast. What we can say
is that **the replication test was well powered for any ordinary physical association**, and a null here
is a real negative rather than a shrug. The registered kill condition was therefore not merely applied
as a rule — it was applied to an adequately powered test.

(The exact hypergeometric p for 9 of 95 is 0.251; the registered permutation test gave 0.195. Both are
correct for what they measure — the permutation version is abundance-matched and is the registered one.)

### 41b. The amoeba observation, and why we are not using it

Instrument B was registered as **descriptive only, with no statistic to be computed**, because n = 60
and because #42 records this project producing a meaningless result by matching gene symbols across
species. Having committed to that, here is what the list contains:

**Eleven of the 60 top MVPA-proximal proteins in *Dictyostelium* are ribosomal** — RPL38 (+1.88),
RPL10A (+1.73), RPL14 (+1.51), RPL21 (+1.50), RPLP2 (+1.48), RPS10 (+1.41), RPL12 (+1.38), RPL30
(+1.37), RPS29 (+1.37), RPS4 (+1.34), RPL35 (+1.30).

**That is 18% of the list, and it is exactly what we would want to see.** It is also from a covalent
in-cell proximity label applied before lysis, which captures associations that an IP wash removes — a
mechanistically real difference, and one §32's registration already noted for a different purpose.

**We are not using it, and naming why is the point of this section.** We pre-committed not to test that
list because we judged in advance that we could not interpret it. The primary instrument then failed,
and the amoeba list now looks supportive. Reaching for it at this moment — after the registered test
returned the unwelcome answer — would be precisely the behaviour the pre-registration exists to prevent,
and it would be the fourth time tonight we were tempted to promote something because it fit
(#152, #157, #110, and now this). **The observation is recorded, unregistered and uninterpreted, for
someone else to test properly with orthology rather than symbol matching.**

Instrument C (BioPlex AP-MS) contains **no** translation or ribosome partners. Descriptive, and with
these counts it means little either way.

**Correction, made in §46 while re-reading the primary file.** This section originally said "15 HEK293T
and 28 HCT116 MVP interactions", taken from the row counts of a collaborator's `bioplex_*` arrays.
Those arrays hold edges for **all three vault proteins as baits**, not MVP alone. Parsing the BioPlex
network files directly, **MVP has 8 partners in 293T and 4 in HCT116**; the remaining 7 and 24 rows are
PARP4 and TEP1 edges. The conclusion of this paragraph is unchanged — there are no translation partners
either way — but the counts were wrong and overstated. This is the same error as #64: a container's
label and length were read as its contents without opening it.

### 41c. Where the translation lead now stands

- **§40 stands as measured:** MVP's co-elution tail is specifically translation-enriched at the 98th
  percentile among 150 comparable seeds, with abundant and SPFH controls unremarkable. That number is
  not in question.
- **§41 bounds what it means:** the association does not appear in a wash-based pulldown that
  successfully recovers all three vault subunits, so it is not demonstrated contact.
- **The honest synthesis is the same one §38 forced on cortical actin**, and it is now the third time:
  a real, specific, replicable co-migration signal with no corresponding physical association.
  Co-abundance, co-fractionation and co-elution tails all report where things are and how they move,
  not what holds them together. **Only MVP-PARP4-TEP1 appears in both kinds of instrument** — and in
  this IP-MS all three come down together at LWTP > 3.3.

## 42. OpenCell is not applicable: MVP is not one of its targets

Recorded because the negative saves effort, and because an external reviewer's advice is what produced
it cheaply. Grok's recommendation on OpenCell (Cho et al., *Science* 2022, PMID 35271311) was explicit:
*"Query the published OpenCell prey table before designing anything; do not make it the next
analysis."*

We queried. **MVP, PARP4 and TEP1 are not among OpenCell's 1,310 CRISPR-tagged target lines.** There is
no bait-side vault experiment in that resource to analyse. Only 54 of the 1,310 lines expose a saved
interaction network through the public API, and the pulldown and interaction endpoints we probed return
404, so there is no prey-side query either. Reaching MVP as a prey would require processing the raw
mass-spectrometry deposits (PRIDE PXD024909 / PXD029191), which is a different order of work from a
table query and is not justified by the prior.

**OpenCell is therefore struck from the instrument list rather than attempted.** It was the last
readily-available contact instrument we had not used, and it does not contain the protein.

### 42a. Instruments used, for the record

| instrument | kind | status |
|---|---|---|
| CPTAC / CCLE co-abundance | covariation | used extensively |
| CFdb native co-fractionation (411 datasets) | co-migration | used (§33, §38, §39, §40) |
| anti-MVP IP-MS, Lodwick | physical, wash-based | used (§13, §41) |
| *Dictyostelium* MVPA TurboID | physical, covalent in-cell | used descriptively |
| BioPlex AP-MS | physical | used descriptively |
| IntAct aggregate | mixed | used |
| Zheng PARP4 TurboID (17 PARPs) | physical, covalent | **voided** - MVP absent from a shallow run (§32) |
| OpenCell endogenous IP-MS | physical, digitonin | **not applicable** - MVP not a target |

Two contact instruments remain unexhausted and both need new data acquisition: the raw OpenCell deposits,
and Kurusu et al. 2023 (PMID 37192622) particle-sorted p62-body proteomics, which bears on vault *fate*
rather than vault neighbourhood and connects to the autophagy thread §20 tested at transcript level.

## 43. The trimer language stands: TEP1 does not need PARP4

`TRIMER_PREREGISTRATION.md`. No expectation was registered, because the instruments pointed opposite
ways and we did not know.

**Both gates passed.** MVP is a WT interactor (LWTP 3.80) and is **not** PARP4-dependent
(WTKD_LFC 0.005, WTKD_P 0.069) — so knocking down PARP4 does not dismantle the particle, and anything
downstream is interpretable. PARP4 **is** PARP4-dependent (WTKD_LFC 5.51, WTKD_P 2.85) — so the
knockdown worked and the dependence columns mean what we took them to mean.

| protein | WT_LFC | LWTP | WTKD_LFC | WTKD_P | PARP4-dependent |
|---|---|---|---|---|---|
| MVP | 7.62 | 3.80 | 0.005 | 0.069 | no (gate) |
| PARP4 | 8.66 | 3.32 | 5.51 | 2.85 | **yes** (gate) |
| **TEP1** | **6.27** | **3.33** | **0.154** | **0.020** | **no** |

**TEP1's vault association is unchanged by PARP4 knockdown.** It is not recruited through PARP4.

### 43a. What this settles, and what it says about CFdb

The trimer language used since §25 is correct: **MVP, PARP4 and TEP1 are three proteins each
independently associated with the particle**, not a pair plus a passenger. The specific alternative we
registered — that PARP4's dramatically tighter co-elution score meant TEP1 was recruited through it — is
wrong.

It also resolves the instrument disagreement in CFdb's disfavour. CFdb scored MVP-TEP1 at precision
**0.041**, the noise floor, while the same resource gave MVP-PARP4 **0.676**. The pulldown says TEP1 is
a genuine, PARP4-independent vault interactor at LWTP 3.33. **So CFdb's TEP1 score is a sensitivity
failure of that instrument, not a statement about the vault** — which is the reading #144 proposed and
this test confirms, and it strengthens the caution in §33 that sensitivity for known vault subunits
there is one of two.

### 43b. MYOF is actively excluded, and two instruments now agree

The secondary analysis re-states #39's background from the primary table: **17 of 88 WT interactors
(19.3%) are PARP4-dependent**, matching the 18.5% figure quoted there.

Among the proteins this project nominated and later withdrew:

- **ANXA2 (+1.74, LWTP 2.62) and S100A10 (+2.11, LWTP 2.69) are confirmed WT vault interactors**, and
  neither is PARP4-dependent. These two have now survived every instrument we have applied and remain
  the only members of the old membrane list with any support.
- **EHD2 is not an interactor** (LWTP 0.54). **AHNAK is not** (LWTP 0.05). **EHD4, CAPN2 and IQGAP1 are
  absent from the table entirely**, which is the point #75 made: they were never tested rather than
  refuted.
- **MYOF is depleted from the vault pulldown: WT_LFC −2.23.** §32 independently found MYOF at **−3.32**
  (p = 3.4e-4) in the PARP4 TurboID neighbourhood. **Two instruments of different design now agree that
  myoferlin is actively excluded from the vault's vicinity** — and myoferlin was the single most
  canonical membrane-repair protein that arrived unbidden in §28 and which we treated as the strongest
  evidence for that module. It is the opposite of a vault partner.

## 44. Unbiased scan of the physical interactome: zero terms, and the registered expectation held

`IPMS_SCAN_PREREGISTRATION.md`. Registered expectation was zero terms, and that is the result.

**The calibration gate passed cleanly.** Twenty random 88-protein subsets of the same universe produced
**median 0, mean 0.00, maximum 0** terms at q < 0.05 across 1,276 tested terms. The scan generates no
false positives on this table, so a null is a real null and not a thresholding artefact.

**The real interactor set: 0 terms at q < 0.05.**

So the vault's physical interactome, in the one instrument that recovers all three of its subunits,
**is describable by no functional module at all.** This is the fourth and most direct statement of the
same result: there is no vault neighbourhood, and the thing we spent most of this project chasing does
not exist at the resolution any available instrument can see.

### 44a. The power limit we registered, now with a specific instance

The registration said: *"This scan can find a large, concentrated physical neighbourhood and cannot
find a diffuse one."* It turns out the registered design has a second blind spot we did not anticipate,
and it is worth stating plainly because it changes what the null covers.

**The scan tested only terms with 10 to 500 members present in the universe.** That filter excludes
small defined protein complexes. Inspecting the excluded terms afterwards — a diagnostic, not a test —
**`GOCC_SMC5_SMC6_COMPLEX` has 6 members in the universe and 4 of them are vault interactors:**

| protein | WT_LFC | LWTP | interactor | PARP4-dependent |
|---|---|---|---|---|
| SMC6 | +6.79 | 1.39 | yes | no |
| NSMCE3 | +6.00 | 2.31 | yes | no |
| NSMCE1 | +5.79 | 3.02 | yes | no |
| SMC5 | +3.93 | 2.98 | yes | no |
| NSMCE4A | +1.08 | 0.48 | **no** | — |
| NSMCE2 | +0.27 | 0.06 | **no** | — |

Expected is 0.44 of 6; observed is 4. `GOCC_SUMO_LIGASE_COMPLEX` is the same four proteins under a
second name, and three further small terms that hit — mitotic recombination, telomere maintenance via
recombination, chromatin looping — are **the SMC5/6 complex's own functions**, so this is one coherent
complex rather than scattered annotation.

**This is untested, not a finding, and emphatically not a result of this section.** Thirty-four
excluded small terms hit three or more interactors, and most are clearly nested metabolic annotations
recycling the same three or four enzymes. Any claim about SMC5/6 requires correction across that whole
family and a second instrument, which §45 registers before looking. **We are flagging a gap in our own
registered design, not rescuing a failed test** — the registered test returned exactly what we
predicted, and this does not change it.

### 44b. The physical interactome as a list, and what it kills

`results/ipms_interactome.csv` holds all 88 with WT_LFC and PARP4-dependence. Top entries by WT_LFC:
**TRO** (+8.68, PARP4-dependent), PARP4, RALGAPB, **MVP**, SMC6, **TCAF1** (+6.48, PARP4-dependent),
TEP1, NSMCE3, LMTK2, NSMCE1, DARS2, WDR11, **NBR1** (+5.09), COP1, IPO7, RACK1, GMPPA (LWTP 6.53, the
highest confidence in the table), ACAD11, HNRNPDL, SMC5.

**This kills the p62-body lead before we spent anything on it.** §42 named Kurusu's p62-body proteomics
as remaining work on vault *fate*. In this pulldown:

- **NBR1 is a vault interactor** (+5.09, LWTP 2.36)
- **SQSTM1 — p62 itself — is not** (LWTP 0.48)
- CALCOCO2 is not (0.38), TAX1BP1 is not (0.09)

So one selective-autophagy receptor associates with the vault and its three closest relatives,
**including p62, do not**. That is a single protein, not an autophagy module, and it is the same shape
as everything else here. It does not support a p62-body model and we are not pursuing one.

## 45. SMC5/6 dies on multiple testing, and our specificity control was vacuous

`SMC56_PREREGISTRATION.md`. Registered expectation was that this would die on Threat 2, nuclear
contamination. **It died on Threat 1 instead** — right outcome, wrong mechanism.

### 45a. Threat 1, multiple testing: the claim dies here

BH-corrected across **every** term with fewer than 10 members in the universe — 4,527 of them, not just
the ones that happened to hit:

**`GOCC_SMC5_SMC6_COMPLEX`: raw p = 3.567e-04, q = 0.4199.** Not significant.

And the manner of failure is as informative as the fact. The top of that corrected family is a dead
heat, every term at the identical q = 0.4199:

| term | hits | q |
|---|---|---|
| `GOCC_SMC5_SMC6_COMPLEX` | 4/6 | 0.4199 |
| `GOCC_SUMO_LIGASE_COMPLEX` | 4/6 | 0.4199 |
| `GOBP_TERTIARY_ALCOHOL_METABOLIC_PROCESS` | 3/4 | 0.4199 |
| `GOBP_TELOMERE_MAINTENANCE_VIA_RECOMBINATION` | 3/4 | 0.4199 |
| `GOBP_RETINOL_METABOLIC_PROCESS` | 3/4 | 0.4199 |

**SMC5/6 is tied with tertiary alcohol metabolism.** When 4,527 small terms are tested, a 4-of-6 hit is
exactly as surprising as a 3-of-4 hit on an alcohol-metabolism annotation, which is the cleanest
available demonstration that the observation was not special. §44a's flag is closed: **our registered
design gap cost nothing**, because the thing it excluded does not survive being included.

### 45b. Threat 2: the control passed, and passing meant nothing

This is the part worth recording. The registered rule was that fewer than two of SMC1A, SMC3, SMC2 and
SMC4 may be interactors. The result was **0 of 4, and the rule therefore recorded PASS.**

**All four are absent from the IP-MS table entirely.** They are not present-and-unenriched; they were
never detected. A protein that is not in the universe cannot be an interactor, so the control could only
ever have returned PASS. **It had no power to fail, and a control that cannot fail is not a control.**
This is the fifth error in the #140 family and the first where the flaw was invisible until the data
came back — the control proteins were chosen for being abundant, nuclear and chromosomal, which is
exactly right in principle, without checking that the instrument had detected them.

We note, without using it, that detecting four SMC5/6 members while detecting no cohesin or condensin
subunit is an odd asymmetry, since cohesin is by far the more abundant complex. **That asymmetry would
need its own test with its own controls, and Threat 1 has already settled the claim**, so we are not
pursuing it. Recording it is not reviving it.

### 45c. Threat 3, CFdb: no support, and the gate earned its keep

The lookup worked only after a parse fix, and **the positive control is what caught the error.** The
first run reported no MVP-PARP4 edge at all — an impossible result for a 0.676 edge — which flagged a
quoting bug in the parse rather than a biological negative. Had the gate not been registered, "no CFdb
edges to SMC5/6" would have read as clean confirmation of a null.

After the fix, with MVP-PARP4 at precision **0.6757** as expected:

| edge | precision | |
|---|---|---|
| MVP-PARP4 | **0.676** | gate, passes |
| MVP-SMC2 | 0.177 | *control*, noise floor |
| MVP-SMC4 | 0.142 | *control*, noise floor |
| MVP-SMC1A | 0.141 | *control*, noise floor |
| MVP-SMC3 | 0.051 | *control*, noise floor |
| MVP-SMC5 | 0.042 | noise floor |
| MVP-TEP1 | 0.041 | noise floor — the known sensitivity failure (#180) |
| MVP-SMC6 | 0.011 | noise floor |
| MVP-NSMCE1 | 0.010 | noise floor |
| MVP-NSMCE3 | — | no edge |

CFdb gives no support. **And cohesin and condensin members score slightly higher there than the SMC5/6
members do**, so that instrument does not even rank SMC5/6 above the controls. Per the registration this
decides nothing on its own — a CFdb negative is weak evidence, and MVP-TEP1 at 0.041 for a protein the
pulldown confirms at LWTP 3.33 is the standing reason why.

## 46. COP1 is the only non-subunit vault partner with three independent instruments

Began as a list-level replication test — do any of the 88 physical interactors appear as MVP partners
elsewhere? — and **house rule 7 stopped it before it was registered.**

### 46a. The test had no power, and the reason is a finding

Rule 7 (added hours ago after #188) requires confirming a control or comparison protein is present in
the data a test will read, before registering. Applied to BioPlex: **of MVP's 8 BioPlex 293T partners,
exactly 1 is present in the IP-MS universe at all.** GOPC, GOT1, HCN1, HIST1H4F, PPP2R2B, RCOR3 and
STX17 were never detected in the IP-MS run, so non-replication would have been guaranteed by
non-detection rather than by disagreement.

**The two instruments sample nearly disjoint proteomes.** Cross-instrument replication between them is
impossible in principle for seven of eight partners, which also retroactively bounds §41's use of
BioPlex as a descriptive check: it was never capable of confirming or denying anything about the IP-MS
interactome. **The rule earned its keep on first use**, and would have saved the §45b error had it
existed a day earlier.

### 46b. The #42 synonym error, again

The first pass recorded BioPlex HCT116's partner `RFWD2` as absent from the IP-MS universe. **RFWD2 is
COP1** — the IP-MS table uses the current symbol, BioPlex the former one. This is the same
symbol-matching failure as #42, hit for the second time, now within a single analysis. The real overlap
was larger than naive matching showed.

### 46c. Provenance decides it, and it splits the two candidates apart

IntAct holds **75 distinct human MVP partners, 16 of them detectable in the IP-MS universe**, so unlike
BioPlex it has real power. Three of those 16 are IP-MS interactors: **PARP4, COP1 and MAP7**.

But IntAct **aggregates published interactions**, so "a third instrument" may be a second copy of the
first. Checking the record provenance:

| record | source | independent of BioPlex? |
|---|---|---|
| MVP-MAP7 | Huttlin 2021, PMID 33961781 | **no — that paper *is* BioPlex 3.0** |
| MVP-COP1 | Huttlin 2021, PMID 33961781 | no |
| **MVP-COP1** | **Lu G. et al. 2014, PMID 25117710, TAP** | **yes** |
| MVP-PARP4 | Huttlin 2017 + Huttlin 2021 | no (both BioPlex) |

So:

- **COP1 has three genuinely independent physical instruments** — **[SUPERSEDED, see §55c: these are
  three datasets but ONE instrument class, since TAP, BioPlex AP-MS and this IP-MS are all lysis plus
  affinity matrix plus MS]** — the anti-MVP IP-MS (WT_LFC +4.74,
  LWTP 2.59, not PARP4-dependent), BioPlex AP-MS, and a 2014 tandem-affinity purification. **It is the
  only non-subunit protein in this entire project with that much cross-instrument support.**
- **MAP7 does not.** Its IntAct record is the BioPlex record, so it has two instruments, not three — and
  its IP-MS evidence is marginal at **LWTP 1.319 against a 1.3 threshold**. We are not carrying it as a
  finding.
- IntAct adds no independent support for PARP4 either, though PARP4 does not need it (CFdb 0.676, IP-MS
  LWTP 3.32, co-abundance rank 1 in eight cohorts).

**Caveat on all of them: every IntAct record above is "spoke expansion"** — a binary pair inferred from
a multi-protein pulldown, not a demonstrated binary contact.

### 46d. And there is still no module, including the tempting one

COP1 is an E3 ubiquitin ligase; NBR1, also an interactor (+5.09), is a selective-autophagy receptor. Two
degradation-pathway proteins on a particle with a 66-hour half-life is an inviting story about vault
disposal, and **§44 already excluded it before it could be told.** Those terms were inside the scanned
window and are flat or below chance:

| term | in universe | hits | expected |
|---|---|---|---|
| `GOBP_PROTEASOMAL_PROTEIN_CATABOLIC_PROCESS` | 75 | 4 | 5.48 |
| `GOBP_PROTEIN_CATABOLIC_PROCESS` | 111 | 7 | 8.11 |
| `GOBP_MACROAUTOPHAGY` | 31 | 2 | 2.26 |

**Below expectation, not merely unsupported.** COP1 and NBR1 are two individual proteins that happen to
share an annotation, which is exactly the pattern this project has mistaken for a module five times. The
finding is COP1, singular, and nothing larger.

## 47. Two COP1 follow-ups declined, and the reasons are the content

COP1 is the project's newest survivor (§46c — **corrected in §55c: three datasets but one instrument
class, not three independent instruments**), so the mechanistic question
is obvious: **is MVP a COP1 substrate?** Two tests suggested themselves and **neither was run.** Both
declines are recorded because the reasoning is reusable and the alternative was a number that
discriminated nothing.

### 47a. Declined: scanning MVP for a COP1 VP degron

COP1 recognises substrates through a short valine-proline "VP degron", which would make a sequence scan
of MVP an attractive orthogonal test — independent of every proteomics instrument used here. The
literature does not support the test:

- **The motif is explicitly sequence-divergent.** Lau et al. describe COP1-interacting partners as
  harbouring *"sequence-divergent Val-Pro (VP) peptide motifs"*, and the structural work (Uljon et al.
  2016, PMID 27041596) establishes an extended-conformation binding mode on the WD40 top face rather
  than a per-position consensus. There is no residue-frequency pattern to search for.
- **A bare VP dipeptide is far too common** to carry information in a 893-residue protein.
- **Known substrates lack the motif.** CEBPA is ubiquitinated by COP1 via TRIB1 without a canonical
  COP1-binding motif, and GATA2 uses a reported non-VP recognition surface. So absence would not
  exclude substrate status either.

**Both error directions are expected, so the scan cannot discriminate.** Running it would have produced
a motif count and an implied verdict with no power behind it — the shape of error this project has
logged five times. Not run.

### 47b. Declined on rule 7: whether COP1 is present as an assembled ligase

The better-posed question is whether COP1 sits on the vault *as a functioning CRL4 ligase*. If so, its
obligate partners should come down too. Checking presence first, per house rule 7:

| CRL4-COP1-DET1 component | in IP-MS universe? |
|---|---|
| COP1 | **present**, interactor (LWTP 2.59) |
| DDB1 | **present**, *not* an interactor (WT_LFC −0.53, LWTP 0.71) |
| DET1 | absent — never detected |
| CUL4A | absent |
| CUL4B | absent |
| RBX1 | absent |

**Four of six were never detected, so the assembly test has no power** and was not registered. Of ten
known COP1 substrates, only ACACA is in the universe (and is not an interactor, LWTP 0.87) — so no
substrate-presence test either.

### 47c. What the instrument can say, weighted as the one protein it is

**DDB1 — the CRL4 scaffold — is detectable and is not a vault interactor** (LWTP 0.71). PSMA1 (−0.86)
and PSMD1 (LWTP 0.50) are likewise detectable and not interactors, consistent with §44 and §46d.

So the single testable component of the machinery points **away** from COP1 being present as an
assembled ligase. That is one protein and we weight it as one protein: suggestive, not decisive, and
nowhere near the standard the trimer (#179) or COP1's own replication (#194) met.

**COP1's presence on the vault is well-replicated and mechanistically uninterpretable from available
data.** Its role needs an experiment, not another reanalysis, and it is added to Paper 2 as
Experiment 12. This is the honest terminus of the computational thread: the instruments can establish
that COP1 is there and cannot establish what it is doing.

## 48. Grok's audit reverses §41: the translation kill was a dichotomisation artefact

Second Grok audit (`grok/to-grok/002-*`, `grok/from-grok/002r-*`), which named one decisive computation.
We ran it. **It overturns the largest claim we made tonight.**

### 48a. Translation IS in the contact instrument. We threw it away with a threshold.

Grok's deliverable 5: *"The number already sitting in the IP-MS table that would decide the biology,
and that the hard cut discarded, is the mean WT_LFC of all 95 GOBP_CYTOPLASMIC_TRANSLATION proteins in
the universe... A systematic positive shift of a few tenths of a log2 across 95 detected proteins would
show the dichotomization manufactured the mechanism."*

`src/grok_audit_checks.py`:

| set | n | mean WT_LFC | median |
|---|---|---|---|
| `GOBP_CYTOPLASMIC_TRANSLATION` in universe | 95 | **+0.2284** | +0.2624 |
| all other detected proteins | 1,110 | **−0.3157** | −0.1135 |
| **difference** | | **+0.5441 log2** | |

Against 2,000 abundance-matched draws (null mean −0.1187, sd 0.1215), the observed mean sits at the
**99.8th percentile, two-sided p = 0.004**.

**Translation proteins are systematically enriched in the anti-MVP pulldown.** The signal is continuous
and strong; our registered test dichotomised it at `LWTP > 1.3` and found 9 of 95 against 6.94 expected,
p = 0.195. **The hard cut discarded the effect it was built to detect.**

So §41's verdict is withdrawn. **The translation association appears in both instrument classes** — at
the 98.0th percentile of 150 seeds in co-elution, and at p = 0.004 as a continuous shift in physical
contact. #173's "kill condition fired" was a thresholding artefact, not a biological null.

Grok also identified the structural defect before we computed anything: *"A gate whose plausible
mild-to-moderate alternatives mostly return 'kill' is a one-way gate. They already logged one of
those."* That is #188's vacuous control in mirror image — a gate with only one reachable answer — and we
committed both on the same day, in opposite directions. The additional ceiling argument is also correct:
**the maximum fold this IP can express is 88/6.94 = 12.7x**, so §40's 18x *"was not a number §41 could
have returned."*

### 48b. The actin exclusion has no positive control either

The load-bearing number for the cortical-actin exclusion was *"0 of 1,175 high-confidence co-elution
edges among 25 actin proteins reach MVP."* Grok: TEP1 is a stoichiometric subunit, recovered in this IP
at LWTP 3.33, and sits at CFdb precision **0.0407** — the same floor as MVP-SMC5 at 0.042. So:

| cutoff | MVP's CFdb degree | TEP1 retained? |
|---|---|---|
| ≥0.676 | **0** | no |
| ≥0.5 | 1 | no |
| ≥0.25 | 29 | no |
| ≥0.1 | 357 | no |
| ≥0.0407 | **1,733** | **yes** |

**Any cutoff that retains a known vault subunit retains 1,733 partners — the entire noise floor.** The
actin zero is therefore **not a powered negative**: it is a statement about a cutoff that excludes TEP1.
And the IP half never carried the leg either — ruffle 1 vs 1.97 (below the null), actin filament
organisation 7 vs 4.75 at the same p = 0.195, with 80% power only near 2.4x.

**Cortical actin is unresolved, not excluded.** Its co-abundance evidence (ruffling 13 vs 3.1, ≈4.2x,
three independent cohorts, surviving interferon-axis removal and abundance matching) still does not
establish complex membership — but we no longer claim a contact instrument refuted it.

### 48c. COP1 is one instrument class counted three times

Grok turns our own taxonomy against the claim: *"TAP, BioPlex AP-MS, and this anti-MVP IP-MS are one
instrument class — lysis, affinity matrix, MS. In the taxonomy of this project... these three are one
class counted three times."* Correct. **Dataset independence is real; method independence is absent.**
An orthogonal instrument would be pre-lysis covalent labelling, crosslinking or reconstitution, and
none is in the COP1 claim. #194 is corrected accordingly.

Two further corrections to our own argument:

- **IntAct is at chance once PARP4 is set aside.** 15 non-PARP4 detectable partners, expected
  15 × 87/1204 = **1.08**, observed 2 (COP1 + MAP7), P(X≥2) ≈ 0.30. After MAP7's demotion: one hit
  against one expected.
- **We used "spoke expansion" as a stronger insult than it is.** It undermines MVP-COP1 only if the bait
  was a third protein or the score never cleared the study's cutoff, and we never established Lu 2014's
  bait or score. Our independence claim was incomplete in both directions.

**What survives is the in-house enrichment**: COP1 at WT_LFC +4.74 — **27-fold** — and LWTP 2.59, not a
threshold scrape. That is one well-measured observation in one instrument class.

**And DDB1 should carry more weight than we gave it.** DDB1 is *present* in the universe, so rule 7's
vacuity does not apply, and it is not an interactor (LWTP 0.71) while COP1 is at 27-fold. DDB1 is the
obligate adaptor of CRL4-COP1. **That pair is positive evidence for free COP1 and against the assembled
holocomplex.** Citing DET1, CUL4A/B and RBX1 absences, as §47b did, repeats gate-design error five.

### 48d. Where Grok is wrong, and it matters

Grok inferred that COP1 cannot be a BioPlex MVP partner: *"Of MVP's 8 BioPlex 293T partners, only PARP4
is present in the 1,205-protein universe. COP1 is present in that universe. Therefore COP1 is not among
the 8."* The inference is sound but **it conflates two cell lines.**

**COP1 (as RFWD2) is a BioPlex MVP partner in HCT116, not 293T.** Verified: 293T partners are GOPC,
GOT1, HCN1, HIST1H4F, PARP4, PPP2R2B, RCOR3, STX17; HCT116 partners are COL8A2, COLQ, MAP7, **RFWD2**.

**But the conclusion survives on different grounds, and worse ones.** The vault-recovery gate passes in
293T (PARP4 present) and **fails in HCT116** (neither PARP4 nor TEP1 among its four partners). So the
BioPlex leg of the COP1 claim comes from **the one cell line that does not recover the vault at all**.
Grok reached the right verdict by the wrong route, and the right route is more damaging.

### 48e. The amoeba decline: right call, wrong reasons

Grok: *"Refusing to promote 11/60 to a confirmatory p-value is the correct half. Keeping it out of the
evidence that constrains the kill sentence is the bias... Applying the commitment in only that direction
is a second fork."* Granted — and §48a now makes it moot, since the kill sentence is withdrawn.

More useful, Grok supplied three reasons to discount that list which are better than the one we used:

1. **No denominator.** We never established the ribosomal base rate in the TurboID proteome, so 18% is
   unloaded — it could neither reinstate §40 nor be treated as checked and found null.
2. **RPL/RPS symbols are exactly the names that survive a bad orthology join**, so an 11-name list
   drawn from that join is enriched for the ribosome's mapping success before any biology. This is #42's
   failure mode predicting its own recurrence.
3. **Ribosomal proteins are a standard lysine-rich TurboID contaminant class.**

*"'We pre-registered descriptive-only' does not [belong in the decline]."* Accepted. The decline stands
on 1-3; the procedural reason was the weakest one available.

### 48f. What is left of the headline

The generalisation we promoted to Paper 1's abstract hours ago — *three candidate neighbourhoods each
survived their controls and then vanished in a contact instrument* — **does not survive this audit.**

| module | co-abundance / co-elution | contact instrument | status now |
|---|---|---|---|
| **MYOF** | — | **−2.23 in IP; −3.32 (p=3.4e-4) in pre-lysis covalent TurboID** | **excluded, and the wash objection cannot reach it** |
| translation | 98.0th pct of 150 seeds | **+0.544 log2, p = 0.004** | **corroborated, not refuted** |
| cortical actin | ruffling 13 vs 3.1, 3 cohorts | IP underpowered; co-elution cutoff excludes TEP1 | **unresolved** |
| membrane repair | died six times | ANXA2/S100A10 confirmed; MYOF excluded | mixed, as before |

**"Three times" is unsupported. One exclusion is solid (MYOF), one claim is now corroborated across
both classes (translation), and one is unresolved (actin).**

The methodological lesson is still there and it is sharper than the one we claimed: **we dichotomised a
continuous contact measurement at a significance threshold and destroyed a real signal, then promoted
the resulting null to a mechanism and from there to a headline.** The error was not mistaking
co-migration for contact. It was building a gate with one reachable answer — twice in one day, in
opposite directions — and then trusting the gate more than the data.

## 49. Continuous re-analysis: translation corroborated, ruffling dead, degradation actively excluded

`CONTINUOUS_PREREGISTRATION.md`. Applied uniformly to every term previously tested on the dichotomised
set, including the ones we would have preferred to see die.

**Both gates passed.** The vault core (MVP, PARP4, TEP1) has mean WT_LFC **+7.516** against a matched
null of +0.017 — the **100th percentile**, so the statistic sees the bait and its two known subunits.
The matched-percentile distribution across 1,276 terms has deciles 4.8 / 20.3 / **48.3** / 75.8 / 92.7,
approximately uniform, so the matching is sound.

### 49a. Translation clears the registered specificity bar, and not alone

| term | n | mean WT_LFC | matched pct | rank of 1,276 |
|---|---|---|---|---|
| `GOCC_RIBOSOME` | 134 | **+0.314** | 100.0 | **14 (top 1.10%)** |
| `GOBP_TRANSLATION` | 191 | **+0.280** | 100.0 | **14 (top 1.10%)** |
| `GOBP_CYTOPLASMIC_TRANSLATION` | 95 | **+0.228** | 99.85 | **23 (top 1.80%)** |

The registered bar was the top 2%. Translation clears it at **1.80%** — narrowly, and we say so.

**What makes it convincing is not that one term squeaked in, but that the top of the scan is one
coherent family.** Eight of the top fifteen terms are ribosomal or translational: ribosomal subunit
(+0.314), ribosome (+0.314), ribonucleoprotein complex (+0.116), large ribosomal subunit (+0.255),
mitochondrial large ribosomal subunit (+0.560), cytosolic ribosome (+0.272), cytosolic small ribosomal
subunit (+0.486), translation (+0.280). A thresholding artefact does not produce a nested family of
eight related annotations at the top of an unbiased 1,276-term scan.

**[SUPERSEDED - see §51, §55b and §56a. The contact half of this convergence was withdrawn, restated
as a residual bound, and that bound then invalidated because the matching donor pool is 77%
translation-adjacent. The co-elution result stands alone.]** ~~So the convergence across instrument
classes is real~~: translation is enriched at the 98.0th
percentile of 150 seeds in native co-elution (§40) and in the top 1.8% of all terms in physical contact.
§41's kill is formally withdrawn.

### 49b. Our registered prediction about actin was right, and it resolves nothing

We registered: *"We expect actin filament organisation to clear nominal significance and to fail the
specificity bar."* It did exactly that — `GOBP_ACTIN_FILAMENT_ORGANIZATION` mean +0.168, p = 0.059,
**rank 80 of 1,276 = top 6.27%**. That falls between the registered bars (top 2% corroborates, outside
top 10% weakens), so **cortical actin is formally intermediate and remains unresolved.**

**But ruffling is dead.** `GOCC_RUFFLE` has mean **−0.0709**, below the matched null, **rank 497 of
1,276 = top 38.95%**, p = 0.791. Membrane ruffling was the *strongest* co-abundance signal in this
entire project — 13 observed against 3.1 expected, ≈4.2x, replicating across three independent cohorts
after interferon-axis removal and abundance matching. **In the contact instrument it is flat.** The
continuous statistic that rescued translation does not rescue ruffling, which is the cleanest
demonstration available that §48a's correction was not a universal solvent.

`GOCC_MITOCHONDRION` sits at top 24.76%, p = 0.491 — the abundance control behaves.

### 49c. Degradation machinery is actively excluded, and we were wrong about how

We registered that the degradation terms would "stay flat, since §46d's counts were below expectation
rather than merely unremarkable." **They are not flat. They are the most depleted terms in the entire
scan.**

| term | n | mean WT_LFC | matched null | pct | rank |
|---|---|---|---|---|---|
| `GOBP_PROTEASOMAL_PROTEIN_CATABOLIC_PROCESS` | 75 | **−1.066** | −0.364 | **0.0** | **1,276 of 1,276** |
| `GOBP_PROTEIN_CATABOLIC_PROCESS` | 111 | **−0.839** | −0.346 | 0.3 | 1,276 of 1,276 |
| `GOBP_MACROAUTOPHAGY` | 31 | **−1.163** | −0.276 | 0.8 | 1,216 of 1,276 |

**Proteasomal protein catabolism is the single most depleted annotation of 1,276 in an anti-MVP
pulldown.** That is a stronger statement than §46d's "at or below chance", and it kills the vault-disposal
reading far more decisively than the counts did: the machinery is not merely absent, it is
anti-associated. COP1 (+4.74) and NBR1 (+5.09) are individual proteins standing against the trend of
their own annotation class, which makes the "two degradation proteins therefore a disposal module"
inference worse than we already judged it.

### 49d. SMC5/6 reappears, and we are not claiming it

`GOCC_SMC5_SMC6_COMPLEX` has mean WT_LFC **+3.976** against a matched null of +0.035, sd 0.80 — roughly
five sigma, and the 100th percentile of 2,000 draws. `GOCC_SUMO_LIGASE_COMPLEX`, the same six proteins,
gives the identical figure.

**This is the same 4-of-6 observation restated with a more sensitive statistic, and the more sensitive
statistic does not fix the multiple-testing problem that killed it.** §45 killed SMC5/6 at q = 0.4199
across 4,527 small terms using the dichotomised count. The continuous statistic has not been run across
that family, so **SMC5/6's apparent strength here is uncorrected and means nothing yet.**

Claiming it now would be precisely the selective application #203 warns against — using the new
statistic where it helps and the old family correction where that helps. **The consistent move is to run
the continuous statistic across all 4,527 small terms with the same correction**, which is registered
separately in `SMC56_CONTINUOUS_PREREGISTRATION.md` before being run.

## 50. SMC5/6: the normal approximation was doing the work, and then our own gate failed

`SMC56_CONTINUOUS_PREREGISTRATION.md` plus the addendum written while the test was running and before
any result was seen. **Registered verdict: UNINFORMATIVE.** We expected survival and did not get a
verdict at all.

### 50a. The addendum was right, by two orders of magnitude

The normal approximation reported SMC5/6 at **q = 0.0003**, rank 2 of 1,849, which under the main
pre-registration alone would have been a pass. The addendum refused that figure and required an
empirical null from at least 200,000 matched draws. We ran 400,000:

| | observed mean | raw count of null draws ≥ observed | empirical p | normal-approx p | discrepancy |
|---|---|---|---|---|---|
| vault core (n=3) | +7.516 | **2 of 400,000** | 7.50e-06 | 1.28e-11 | **586,825x** |
| `GOCC_SMC5_SMC6_COMPLEX` (n=6) | +3.976 | **15 of 400,000** | 4.00e-05 | 3.02e-07 | **132x** |

The underlying cause, quantified: the `WT_LFC` distribution has **skew −0.87 and excess kurtosis 6.00**,
so the null of a small-*n* mean is not Gaussian — the empirical nulls carry positive skew (+0.45 at
n = 3, +0.30 at n = 6). **A z of 5.0 is worth p ≈ 4e-05 here, not 3e-07.** Had we accepted the normal
figure we would have published a result inflated 132-fold.

### 50b. And then our own positive control failed

The registered gate required the vault core at **q < 0.01**. On the empirical statistic:

**q_core = 7.50e-06 × 1,849 = 0.0139.** The gate fails. **Per the registration the result is
UNINFORMATIVE, whatever SMC5/6 did** — and what it did was q_empirical = **0.0370**, which would have
cleared its own q < 0.05 bar.

So the honest position is that **SMC5/6 is neither alive nor dead.** It passed its own bar in a test
whose positive control did not pass, and a result whose gate failed is not a result. §45's kill no
longer stands on a second statistic, but nothing replaces it.

### 50c. Why the gate failed, and the sixth gate-design lesson

Not because the vault core is weakly enriched — it is the bait plus its two subunits at mean +7.52 with
**2 exceedances in 400,000 draws.** It failed because **a 3-protein set's empirical p is floored by the
draw count.** With 400,000 draws the smallest achievable p is 2.5e-06 and the smallest achievable
q_core is 0.0046, so q < 0.01 required **one or fewer exceedances out of 400,000.** We got two.

Our house rule 8 reachability check was performed on the *normal* statistic, where the core's z = 6.75
gave q = 1.4e-08 and a pass looked trivially reachable. On the statistic the addendum then mandated, the
same gate sat **a factor of two above the test's resolution floor.**

**Sixth gate-design lesson: a gate threshold must be checked against the resolution of the statistic
that will decide it, not against the statistic you first wrote down.** Rule 8 told us to check that both
outcomes were attainable; it did not tell us to re-check after changing the statistic, and changing the
statistic is exactly what the addendum did.

### 50d. What we are not going to do

The core's empirical p rests on **2 events**, so its Poisson 95% interval is roughly 0.9e-06 to 27e-06,
which puts **q_core anywhere in [0.0017, 0.050]** — straddling our threshold. Four million draws would
tighten that estimate and, on the point estimate, would likely land near q ≈ 0.0093, just inside the
gate.

**We are not running them.** Increasing precision *because the gate failed*, and stopping when it
passes, is fault #113 — iterating a method until it passes — and it is a standing house rule. Monte
Carlo precision is a defensible thing to increase, but not in response to the answer. If this is to be
resolved it requires a **new registration that fixes the draw count in advance**, and we are recording
the UNINFORMATIVE verdict rather than buying a pass with compute.

### 50e. One more thing to be honest about

The top of that 1,849-term family is coherent — SUMO ligase complex, SMC5/6 complex, mitotic
recombination, telomere maintenance via recombination and chromatin looping occupy ranks 1 to 5. **That
coherence is mostly redundancy, not corroboration.** All five annotations describe the same four to six
proteins; it is one complex appearing under its aliases and its functions, which is a different thing
from §49a's ribosomal family, where eight terms drew on 95 to 261 distinct detected proteins.

Also recorded: this family has **1,849 terms against §45's 4,527**, because §45 used a <10-member cut
with no floor and we excluded the **2,678 terms with 1-2 members** as not estimable. We flagged that
difference in the registration before running. It makes this correction *less* stringent than §45's by a
factor of 2.4 — and even so, the family-size difference does not explain the reversal, since
q = 0.0370 × 2.4 = 0.089 would still have beaten q = 0.4199. **The statistic, not the family, is what
changed.**

## 51. The translation enrichment is what ribosomal proteins are, not what they bind

`RIBOSOME_PROPERTY_PREREGISTRATION.md`. **Registered expectation was that the polysome reading would
die. It died, on both tests independently.** §49a's upgrade is withdrawn.

### 51a. Compartment discrimination

Mitoribosomes sit inside mitochondria behind two membranes. A cytoplasmic 13 MDa particle cannot be
bound to them.

| term | n | mean WT_LFC | p (abundance-matched) | median length | charge per 1,000 residues |
|---|---|---|---|---|---|
| `GOCC_MITOCHONDRIAL_LARGE_RIBOSOMAL_SUBUNIT` | 23 | **+0.560** | 1.4e-02 | 198 | +54.4 |
| `GOCC_ORGANELLAR_RIBOSOME` | 45 | **+0.382** | 7.6e-03 | 198 | +54.5 |
| `GOCC_RIBOSOME` | 134 | +0.314 | 1.1e-04 | 184 | +100.2 |
| `GOCC_CYTOSOLIC_RIBOSOME` | 82 | **+0.272** | 3.5e-03 | 160 | +130.2 |
| `GOBP_CYTOPLASMIC_TRANSLATION` | 95 | +0.228 | 3.3e-03 | 179 | +108.1 |
| whole universe | 1,166 | −0.273 | — | **418** | **+2.94** |

**The mitochondrial ribosome is more enriched than the cytosolic one**, while §49b showed the
mitochondrial compartment as a whole is flat (−0.145). The enrichment tracks *"is a ribosomal protein"*
and nothing else.

### 51b. Length and charge matching erases it completely

Ribosomal proteins are **2.6x shorter than the median detected protein (160 vs 418 residues) and 44x
more basic (+130 vs +2.94 charge units per 1,000 residues)**. That is the profile of a protein that
sticks to an affinity matrix. Re-testing against randoms matched on length decile and charge decile in
addition to abundance:

> **[VOID — see §63. Every p-value in this section comes from the three-way length x charge x
> abundance matching, which is degenerate: 1,166 proteins over up to 1,000 cells, 49% of occupied
> cells holding one protein, and MVP's own cell holding MVP plus one other. The null was drawing the
> test subject. The one-way abundance-matched result is unaffected.]**


| term | n | observed | matched null | draws ≥ obs | p |
|---|---|---|---|---|---|
| `GOCC_CYTOSOLIC_RIBOSOME` | 82 | +0.272 | **+0.229** | 61,764 / 200,000 | **0.309** |
| `GOBP_CYTOPLASMIC_TRANSLATION` | 95 | +0.228 | **+0.158** | 34,706 / 200,000 | **0.174** |
| `GOCC_RIBOSOME` | 134 | +0.314 | **+0.256** | 36,886 / 200,000 | **0.184** |

**The matched null essentially reproduces the observation.** Length and charge account for the entire
effect.

### 51c. The gate passed, which is what makes this readable

A control that erased everything would prove nothing. The vault core — MVP, PARP4, TEP1, **median
length 1,724 residues, charge −28.5**, the opposite profile — **still clears the fully matched control
at p = 0.024** (it was 5e-06 on abundance alone, and the matched null rises from −0.29 to +2.00, so the
matching is doing real work). **The same control that destroys the ribosome signal spares the bait and
its two known subunits.** That is a discriminating control rather than an over-specified one, and it is
the reason we treat this as an answer.

### 51d. What this leaves, and the uncomfortable part

**Translation returns to where it was before §48a: a single-instrument finding.** §40's co-elution
result — MVP's sub-threshold tail at the 98.0th percentile of 150 comparable seeds, with glycolytic
controls at the 26th-79th and MVP's own SPFH relatives at the 41st-70th — **is not tested here and still
stands.** It is seed-level specificity, which a generic ribosomal property does not obviously explain:
if small basic proteins co-migrate promiscuously they should appear in every seed's tail, not MVP's
preferentially. That remains open and is the right target for the next test.

**But the contact corroboration is gone, and the honest summary of this whole arc is unflattering.**
The same question, on the same data, has now returned three different answers depending only on the
statistical treatment:

| treatment | result | §  |
|---|---|---|
| dichotomised count at `LWTP > 1.3` | null, p = 0.195 → we recorded a kill | §41 |
| continuous mean, abundance-matched | positive, top 1.8% of 1,276 terms → we upgraded it | §49a |
| continuous mean, length- and charge-matched | **null, p = 0.174** → withdrawn | §51b |

**The biology never changed. Each reversal was a methodological choice we had not interrogated, and in
each case we published the answer before interrogating it.** The first was ours, the second came from an
adversarial reviewer, and the third we found in our own output — which is the only encouraging thing
here. The rule that would have prevented all three is the one we keep arriving at from different
directions: **before reporting an enrichment, ask what property other than the one you are naming could
produce it, and match on that.**

## 52. Mass is not the explanation for §40, and §40 is still not promoted

`MASS_CONFOUND_PREREGISTRATION.md`. **Registered verdict: EQUIVOCAL.** Our registered expectation was
that MVP would survive with a reduced margin; it did not, and we report the bar we actually hit.

**The reproduction is exact**, which validates the pipeline before anything is read from it: MVP at
**fold 18.49x, percentile 98.0** — §40 reported 98.0 — with gates passing identically (RPL7 **98.7**,
RPS6 **98.7**, small-complex negatives median **65.0** < 80).

### 52a. Mass does not predict the score. It is close to anti-correlated.

| assembly | approx. assembled mass | n | median percentile | range |
|---|---|---|---|---|
| **nuclear pore complex** | **~110 MDa** | 7 | **26.0** | 6-52 |
| spliceosome | ~1.5 MDa | 5 | **26.0** | 26-41 |
| small-complex negatives | < 300 kDa | 6 | 65.0 | 41-79 |
| clathrin coat | polymeric | 4 | 72.7 | 41-98 |
| TRiC/CCT chaperonin | ~1 MDa | 7 | 75.3 | 60-81 |
| condensin / cohesin | ~1 MDa | 5 | 91.3 | 6-94 |
| 26S proteasome | ~2.5 MDa | 3 | 92.7 | 70-94 |
| **cytoplasmic dynein** | **~1.4 MDa** | 4 | **96.0** | 93-98 |
| **MVP** | **~13 MDa** | 1 | **98.0** | — |

**The largest assembly tested, the 110 MDa nuclear pore, sits at the 26th percentile. The 1.4 MDa
dynein complex sits at the 96th.** Across the seven groups, apparent mass and translation-fold are if
anything inversely related. **The mass confound is refuted as a mechanism** — which is what this test
was built to decide, and it decided it.

### 52b. But something still shifts the large assemblies upward, and we do not know what

The 35 large-assembly seeds have a **median percentile of 70.0** against a random-seed median of 50.
That is why the registered verdict is equivocal rather than a pass: our bars were >75 confirms the
confound, <60 clears MVP, and 70.0 sits between them. **No assembly's median reaches MVP's 98.0** — the
closest is dynein at 96.0 — so the confound is not confirmed either.

The residual pattern **looks** like compartment rather than mass: the two lowest groups, nuclear pore
(26.0) and spliceosome (26.0), are nuclear, while proteasome (92.7), dynein (96.0), TRiC (75.3) and
clathrin (72.7) are cytoplasmic, as MVP is. **Condensin and cohesin contradict it** at a median of 91.3
despite being chromosomal — and with a range of 6-94 across five seeds, that group is too noisy to
carry either reading. Group sizes are 3 to 7. **We are naming this as an untested hypothesis, not
adopting it**, because adopting a post-hoc axis that two of our own groups violate is the error §48e
caught us in.

### 52c. Where this leaves the translation thread

| claim | status |
|---|---|
| contact-instrument enrichment (§48a, §49a) | **withdrawn** — explained by length and charge (§51) |
| co-elution tail enriched 18.49x, MVP at the 98.0th percentile of 150 degree-eligible seeds | **stands, reproduced exactly** |
| ...not explained by MVP's degree | **established** — MVP is only the 73.8th percentile for degree, below every comparator used here |
| ...not explained by abundance | established in §40 (glycolytic controls 26th-79th) |
| ...not explained by family membership | established in §40 (SPFH relatives 41st-70th) |
| ...**not explained by apparent mass** | **established here** |
| ...explained by something else that also lifts cytoplasmic assemblies | **open** |

So the honest position after four controls: **§40's result survives every specific alternative we have
been able to construct, and we still decline to promote it**, because the large-assembly distribution
is shifted enough to show there is a mechanism we have not named. Three seeds out of 150 reach above
the 95th percentile without being ribosomal, and we cannot say why.

**This is what "eliminate or mark as probable and weigh" looks like when it works.** We eliminated mass.
We did not buy a promotion with it.

## 53. Seed properties do not explain §40, and our registered rule named the wrong axis

`SEED_PROPERTY_PREREGISTRATION.md`. **Registered verdict: NEITHER** — one more alternative eliminated,
§40 unpromoted. That was our registered expectation. **But the registered verdict understates the
numbers, for a reason that is our own fault, and we report both.**

Gate passed: RPL7 (fold pct 98.6, charge top quartile, length bottom quartile) and RPS6 (98.6, same) —
the axis is measurable. MVP reproduces at fold **18.49x, percentile 97.9** on 146 seeds.

### 53a. Length matters, charge does not

| correlate | Spearman ρ | p |
|---|---|---|
| translation-fold vs **charge** per 1,000 residues | +0.077 | **0.355** |
| translation-fold vs **length** | **−0.294** | **0.0003** |

**Shorter seeds genuinely do have more translation-rich co-elution tails**, and charge — the property
that killed the contact result in §51 — is irrelevant here. Two instruments, two different nuisance
axes.

### 53b. MVP beats every seed that resembles it

MVP's 30 nearest neighbours in standardised (length, charge) space have **median length 768 and median
charge −17.2**, closely matching MVP's 893 and −28.5, so the matching worked. Their folds:

- **neighbour median fold: 1.38x**
- **neighbour maximum fold: 9.84x**
- **MVP: 18.49x — the 100.0th percentile of its own look-alikes** **[but see §55c: conditional on MVP
  already being the 98.0th percentile of 150 seeds, 0.98^30 = 0.545, so a pre-chosen 98th-percentile
  seed tops all 30 of a random 30-set 55% of the time. This number is nearly uninformative and we led
  with it.]**

Nearest eight by profile: STAT2 (1.18x), INPP4B (0.79x), ITGB3 (0.39x), DIEXF (1.18x), CTAGE4 (1.18x),
RABL6 (1.57x), SSH1 (1.57x), LLGL1 (1.97x).

MVP is longer than 80% of seeds, length anti-correlates with fold at p = 0.0003, and **MVP nonetheless
has a tail 13x richer than the median seed of comparable size and charge, and nearly twice the richest
of them.** The registered withdrawal bar was MVP below the 75th percentile among neighbours; it is at
100.

### 53c. Why we are not calling this strengthening

Our registered condition for STRENGTHENED was that **charge** correlate positively *and* MVP stay above
the 90th percentile among neighbours. The second half is met at 100.0. **The first half named the wrong
property** — the axis that organises these tails is length, which we did not anticipate, so the rule
fell through to NEITHER.

Substantively this is the pattern we described in the registration as strengthening: *"MVP would then be
producing a ribosome-rich tail against the trend its own composition predicts, which is harder to
explain as an artefact than the raw 98th percentile was."* That is exactly what happened, on length
rather than charge.

**We are not promoting §40 on it.** Promoting a finding on an axis we did not register, immediately
after the registered rule declined to promote it, is the post-hoc substitution this project has been
caught at twice today (#209, and the selective-statistic fork in §49d). **The registered verdict governs:
one more alternative eliminated, nothing promoted.** The length result is recorded as what it is — an
unregistered observation pointing the same way — and if it is to count, it counts in a future test
registered on that axis and preferably in another dataset.

### 53d. The running tally on §40

§40's co-elution result now survives **five** specific alternatives: **degree** (MVP at the 73.8th
percentile, below every large-assembly comparator), **abundance** (glycolytic seeds 26th-79th), **family
membership** (SPFH relatives 41st-70th), **apparent mass** (110 MDa nuclear pore at the 26th percentile,
1.4 MDa dynein at the 96th), and now **seed length and charge** (MVP at the 100th percentile of its own
physicochemical neighbours).

It remains **unpromoted and single-instrument**, because the mechanism that lifts cytoplasmic assemblies
to a median of 70 (§52b) is still unnamed, and because the one contact instrument that could corroborate
it does not (§51). **Five eliminations and no promotion is the correct outcome of a method designed to
make promotion hard**, and it is worth saying plainly that this is what the project looks like when it
is working rather than when it is stuck.

## 54. The export hypothesis (Graham's), exploratory — and a question the literature has not asked

**This section is EXPLORATORY and unregistered. Nothing in it is promoted.** It is recorded because the
hypothesis is specific, it makes a prediction testable in data already in hand, and the pattern that
came back is closer to the prediction than we expected.

### 54a. The hypothesis

If the vault is an export device — if it exists to carry something out of the cell — then a healthy cell
should not hold loaded vaults, and a loaded one should be got rid of promptly. That predicts vaults in
secretions and in the gut lumen, and it predicts **disposal by export rather than by degradation**.

### 54b. What the published literature already says

Partly published, and more directly than we expected:

- **MVP loads RNA into exosomes.** Silencing MVP reduces total exosomal RNA, and biotinylated MVP
  partitions to exosomes.
- **MVP-dependent loading of the tumour-suppressor miR-193a into exosomes is described as a way cancer
  cells get rid of it** — knocking out MVP makes miR-193a accumulate in the donor cell and inhibits
  tumour progression. That is the export-as-disposal model, already in print.
- **Rome's group reports that human cells release Argonaute 1-4 and MVP independently of exosomes**, so
  the release route is not the classical exosome pathway.
- **But a 2025 *Journal of Extracellular Vesicles* study found most vtRNA and MVP in differential-
  centrifugation pellets are *not* membrane-enclosed or protected** — consistent with free vault
  particles being co-isolated rather than packaged as vesicle cargo. For this hypothesis that is a
  point in favour: whole particles appear to get out.
- **In the Atlantic salmon louse, MVP is a component of extracellular cement material** — a precedent
  for MVP functioning outside the cell in another animal.
- Gene annotation places MVP in the **secretory granule lumen**, though by traceable author statement
  rather than direct measurement, and records high LRP expression in **epithelial cells of the digestive
  tract**, matching the tissue pattern.

**On the specific question — vaults in feces, gut lumen, or mucus itself — we found nothing.** No study
reporting MVP in the human fecal proteome or in gut mucus secretions. The nearest result is a 2023
preprint reporting **MVP genes in bacteriophages from the human gut microbiome**, which concerns phage
genes rather than host protein in stool. **This appears to be a genuinely unasked question**, and a
cheap one: published fecal and mucus proteomics datasets exist and could simply be queried for MVP.

### 54c. What our own data says, with its caveats stated first

Caveats, before the numbers: **8 terms, no pre-registration, no multiple-testing correction, two of the
hits have n = 13 and n = 15, and the length-and-charge control that destroyed the translation finding in
§51 has not been applied here.** Empirical nulls, 200,000 draws, vault-core gate passed (2 of 200,000).

| term | n | observed | matched null | percentile | p |
|---|---|---|---|---|---|
| **`GOBP_DETOXIFICATION`** | 15 | **+0.970** | −0.284 | **99.5** | **0.005** |
| **`GOCC_LATE_ENDOSOME`** | 13 | **+0.740** | −0.276 | **97.3** | **0.027** |
| `GOBP_EXPORT_FROM_CELL` | 37 | +0.068 | −0.264 | 86.6 | 0.134 |
| `GOBP_EXOCYTOSIS` | 17 | +0.090 | −0.195 | 75.0 | 0.250 |
| `GOCC_SECRETORY_GRANULE` | 107 | −0.213 | −0.299 | 68.0 | 0.320 |
| `GOCC_SECRETORY_VESICLE` | 114 | −0.255 | −0.286 | 56.4 | 0.437 |
| `GOBP_VESICLE_MEDIATED_TRANSPORT` | 100 | −0.327 | −0.230 | 29.6 | 0.703 |
| `GOBP_RESPONSE_TO_XENOBIOTIC_STIMULUS` | 30 | −0.583 | −0.247 | 16.4 | 0.836 |

Under a crude Bonferroni across the eight, **detoxification survives (0.005 × 8 = 0.04) and late
endosome does not (0.22).**

**The shape of the result is what makes it interesting rather than either hit on its own.** Set beside
§49c's reference points:

- **classical secretion machinery is not near the vault** — secretory granule, secretory vesicle,
  exocytosis and vesicle-mediated transport all unremarkable or below the null
- **the late endosome is** (+0.740) — the multivesicular-body route, which is the non-classical exit
- **detoxification enzymes are** (+0.970), the strongest hit in the set
- **degradation machinery is the most depleted thing in the entire 1,276-term scan** — proteasomal
  catabolism −1.066 at the 0.2nd percentile, macroautophagy −1.163 at the 0.8th

So: not degraded, not classically secreted, but sitting near the non-classical exit route and near
detoxification chemistry. **That is the hypothesis's prediction, arrived at from the other direction.**
It is also exactly the kind of coherent story this project has been wrong about five times today, which
is why §55 registers the real test instead of claiming this one.

One tension worth naming: **`GOBP_RESPONSE_TO_XENOBIOTIC_STIMULUS` is the *lowest* term in the set**
(16.4th percentile, −0.583) while `GOBP_DETOXIFICATION` is the highest. Those two should move together
under any simple reading of a drug-efflux role, and they do not. Fifteen proteins against thirty, so
this may be noise — but it is the first thing a reviewer should attack.

## 55. Third audit: our kill was a sensitivity analysis, and its justification was noise

Grok audit 3 (`grok/to-grok/003-*`, `grok/from-grok/003r-*`). **Its central charge is correct and we
accept it**: we promoted §51's length-and-charge null *"from a sensitivity analysis to the official
kill, on the authority of the mitoribosome contrast"* — and that contrast is noise. We verified its
arithmetic before writing (`results/grok3_checks.log`).

### 55a. The mitoribosome argument fails twice over

We justified applying the physicochemical control by observing that
`GOCC_MITOCHONDRIAL_LARGE_RIBOSOMAL_SUBUNIT` (+0.560) exceeds `GOCC_CYTOSOLIC_RIBOSOME` (+0.272),
reasoning that mitoribosomes are unreachable behind two membranes.

**Statistically it is nothing.** The difference is +0.288 on n = 23 against n = 82:

| dispersion used | SE | 95% CI | two-sided p |
|---|---|---|---|
| σ = 1.951, implied by our own normal-approximation p-values | 0.460 | **[−0.61, +1.19]** | **0.53** |
| σ ≈ 0.75, from the 200,000-draw matched nulls | 0.177 | [−0.06, +0.63] | 0.104 |

Excluding zero at two-sided 95% would need σ ≤ 0.62, below both estimates. **And we quoted the more
extreme of the two mitochondrial terms** — `GOCC_ORGANELLAR_RIBOSOME` gives a gap of only **+0.110** —
having picked it out of a 1,276-term scan.

**Logically it is worse.** Grok: *"The 23 mt-LSU rows are in the IP-MS matrix, so in this assay they
were in the tube. Two membranes describe the intact cell. A lysate IP cannot use them as an unreachable
negative."* That is plainly right, and it is a basic error: lysis destroys the compartment boundary the
whole argument rested on. **The mitoribosome justification is withdrawn.**

### 55b. What §51 actually established, stated correctly this time

The control itself is legitimate — length and net charge are **pre-treatment sequence features**, so
they are not on the causal path from contact to enrichment, and "a bound ribosome would still be small
and basic" does not make the matching illegal. But it answers a **different estimand** than the class
shift, and both are true at once:

> **[VOID — see §63. Every p-value in this section comes from the three-way length x charge x
> abundance matching, which is degenerate: 1,166 proteins over up to 1,000 cells, 49% of occupied
> cells holding one protein, and MVP's own cell holding MVP plus one other. The null was drawing the
> test subject. The one-way abundance-matched result is unaffected.]**


| estimand | value | status |
|---|---|---|
| abundance-matched class shift: translation +0.2284 vs −0.3157 for the other 1,110 | **+0.544, p = 0.004, rank 23 of 1,276** | **stands** |
| residual beyond length and charge: cytosolic ribosome | +0.043, CI [−0.13, +0.21], p = 0.309 | bounded near zero |
| residual beyond length and charge: cytoplasmic translation | +0.070, CI [−0.08, +0.22], p = 0.174 | bounded near zero |
| residual beyond length and charge: ribosome | +0.058, CI [−0.07, +0.19], p = 0.184 | bounded near zero |

Those upper bounds are about **1.16x**. So the correct statement is not "withdrawn" but: **the class
shift is real and has been decomposed; essentially all of it is accounted for by length and charge, and
any residual contact-specific component is bounded below ~1.16x.** The same procedure spares the core
(residual +5.5, p = 0.024), so the control discriminates. **Contact corroboration beyond the
physicochemical profile stays withdrawn; the class shift does not.** §51's headline overstated this and
is corrected.

Grok also names the condition under which the matching *would* be wrong, and the number we are missing:
it fails if the proteins drawn from those sparse decile cells are themselves ribosomal under another
name — translation factors, RBPs, ribosome-biogenesis proteins — making charge and length a recoding of
the label. With a 44x charge gap and 2.6x length gap the occupied cells are a sparse corner, so this is
plausible. **The donor list is the missing number and we have not computed it.**

### 55c. §53's best number is 55% likely by construction

We reported MVP at the **100.0th percentile of its 30 nearest look-alikes** as the strongest surviving
argument for §40. Conditional on MVP already being the 98.0th percentile of 150 seeds,
**0.98³⁰ = 0.545** — so **a pre-chosen 98th-percentile seed tops all 30 of any random 30-set 55% of the
time.** Verified. That statistic is very nearly uninformative, and we presented it as the headline.

Worse, grok argues the matching object is wrong: MVP's neighbours were matched on **monomer** length and
charge, but *"the 30 neighbours do not share a 13 MDa elution peak."* Matching monomer sequence features
cannot control for particle-scale co-elution. And length's correlation, while real at p = 0.0003, has
**r² = 0.086** — far too small to generate an 18.49x tail.

### 55d. The artefact none of our five controls touches

**Polysome-window co-elution.** CFdb top-200 lists fill with whichever complex dominates peptide mass in
the shared heavy fractions, and in a cytoplasmic lysate that complex is the ribosome. MVP at the 98.0th
percentile sits just under RPL7 and RPS6 at 98.7. Grok's summary is the sharpest sentence in the audit:

> *"A vault that co-elutes like a ribosomal protein and co-precipitates translation proteins at a
> residual +0.070 log2 (p = 0.174), against a core of +7.516, is co-fractionation without a
> co-complex."

**[The quoted residual and its p = 0.174 are VOID — §63 shows they came from the degenerate three-way
matching. Grok's point about co-fractionation versus co-complex does not depend on them; the numbers
it was handed do.]**"*

And MVP's 98 sits exactly in the high cluster — dynein 96.0, proteasome 92.7, condensin/cohesin 91.3 —
*"which is where a polysome-overlapping cytoplasmic profile lands."* **Two controls we never ran:
matching on elution-profile correlation, and varying k, the top-200 cutoff that magnifies the effect.**

### 55e. Our mass gate had a dead zone wider than its own estimator

A third one-way gate, after #188 and #204. The large-assembly median was **70.0** against a random
median of 50 — that is 2.4 SE, two-sided **p ≈ 0.018**, a real shift. But our confirm bar at 75 sat
**0.6 SE above** the estimate and our clear bar at 60 sat **1.2 SE below** it: **the pre-registered
refusal band was wider than the estimator could resolve**, so EQUIVOCAL was close to pre-ordained.

Two further corrections:

- **Weighting decides the verdict.** Equal weight per assembly on the seven medians (26, 26, 72.7, 75.3,
  91.3, 92.7, 96) gives **75.3 — which clears our >75 confirm bar.** Seed-weighting let NPC (n=7) and
  the spliceosome (n=5) pull it down. We did not register the weighting.
- **Mass is exonerated regardless, and more cleanly than we argued.** The informative contrast is
  large-assembly 70.0 against our own small-complex negatives at **65.0** — a **5-point gap**. We
  reached the right conclusion by the wrong comparison.
- **The median was the wrong summary.** Within-assembly ranges (condensin/cohesin 6-94, clathrin 41-98,
  NPC 6-52) describe a two-cluster distribution, not a central tendency.
- **We over-applied rule 7 on the compartment test.** We declined it for lack of GO compartment terms —
  but **assembly identity already labels all 35 seeds**, and condensin/cohesin at a median of 91.3 on
  n = 5 means at least three of its seeds are ≥ 91, so it genuinely does break a pure cytoplasm rule.
  Declining to *adopt* compartment was right; declining to *test* it was unnecessary.

### 55f. The SMC5/6 gate failure was a one-count artefact

| exceedances k | add-one p | q (BH × 1,849) |
|---|---|---|
| 1 | 5.00e-06 | **0.00924** |
| **2 (observed)** | 7.50e-06 | **0.01387** |
| MLE at k=2 | 2/400,000 | 0.00924 |

**Our 0.01 bar sits in the gap between k=1 and k=2.** The miss is the 50% add-one penalty at two
counts, not a property of the data. Garwood's 95% interval on 2 events gives q ∈ **[0.0011, 0.033]** —
our quoted [0.0017, 0.050] was too wide on top — and 0.01 is inside either interval, so *"unresolved"*
survives while our upper endpoint does not.

Grok's charge of manufactured indecision lands: **SMC5/6 is the better-measured quantity**, 15 counts at
26% relative Poisson error against the control's 2 counts at 71%, and **q_empirical = 0.037 meets 0.05
on its own.** *"Voiding a 15-count q because a 2-count positive control missed by the continuity
correction is the manufactured half."* The core, at mean +7.516 with 2 exceedances, is a **detected**
positive control whose q is merely unidentified — not a failed one.

**But refusing the 4M draws was right**, and grok agrees for a better reason than ours: at the current
rate 4M draws expect 20 counts, pass about **60%** of the time, and leave SE(q) ≈ 0.002 still straddling
0.01. *"'Likely just inside' is a coin flip."* Resolving it to 3 SE would take on the order of **3×10⁸
draws.**

### 55g. What we are changing, and what we are not

Changed: §51's headline (a sensitivity analysis, not a kill), the mitoribosome justification
(withdrawn), §53's look-alike percentile (55% by construction), §52's gate design (dead zone wider than
the estimator; weighting unregistered), and §50's verdict framing (the control was detected, not
failed).

**Not changed: no claim is promoted.** SMC5/6 at q = 0.037 is better measured than we said, and it is
still one instrument, with a nuclear-contamination control that cannot be built in this assay (#217).
§40 still has the polysome-window artefact unaddressed, which is a *new* alternative, not an eliminated
one — so the honest count is **five eliminated and one newly identified**, not six eliminated.

## 56. The donor list invalidates §51's control; k behaves ambiguously and our criterion missed it

`DONOR_AND_K_PREREGISTRATION.md`. Both tests Grok named. **Test 1 met our registered expectation.
Test 2 contradicted it, and then we found our own criterion was the wrong one.**

### 56a. §51's control is INVALID as applied

Grok's condition was that length-and-charge matching fails if the donors drawn from those decile cells
are *"ribosomal under another name."* Enumerating the actual donor pool for
`GOBP_CYTOPLASMIC_TRANSLATION`'s 95 members across their 65 occupied cells:

| | value |
|---|---|
| donor pool size | **189 proteins** |
| translation-adjacent fraction, donor pool | **0.772** |
| translation-adjacent fraction, whole universe (n=1,166) | 0.311 |
| **enrichment ratio** | **2.48x** — *wrong; the correct frame gives 2.86x, see §64b* |

Registered bars: invalid above 2.0x, stands below 1.5x. **2.48x — invalid as applied.**

**The matched draws were comparing translation proteins against a pool that is 77% translation-adjacent.**
Length and charge are, in this universe, substantially a recoding of the label. So §51's residual of
+0.070 log2 (upper bound ~1.16x) is **an underestimate by construction**, and the bound we reported in
§55b cannot stand.

**What this does and does not do.** It does not restore the contact corroboration — it **reopens** the
question. The abundance-matched class shift (+0.544, p = 0.004, rank 23 of 1,276) is now the
better-supported statement, since the decomposition that explained it away is invalid. We have no valid
estimate of the contact-specific residual, and constructing one needs a donor pool that is not already
the label, which this universe may not contain.

### 56b. k declines monotonically — our registered criterion says complex-like

Gates passed at every k (RPL7 and RPS6 at 98.7-100.0; small-complex negatives' median 0.0-65.0):

| k | MVP fold | MVP percentile | hits | hits/k |
|---|---|---|---|---|
| **25** | **37.78x** | **99.3** | 12 | 0.480 |
| 50 | 31.48x | 98.0 | 20 | 0.400 |
| 100 | 28.33x | 98.0 | 36 | 0.360 |
| 200 | 18.49x | 98.0 | 47 | 0.235 |
| 400 | 13.97x | 98.7 | 71 | 0.177 |
| 800 | 9.15x | 98.7 | 93 | 0.116 |

Our registered rule — *"maximal at small k and declining monotonically, percentile above 95 at small
k"* — is satisfied exactly: **the effect is strongest at k = 25 (37.78x, 99.3rd percentile)**, where a
real co-complex should be most visible, and the percentile is stable at 98-99 throughout. At k = 25 all
six small-complex negatives have **zero** translation partners, so the statistic discriminates sharply
there.

**This also removes the polysome-window alternative (#239) on its own terms**: a window artefact was
registered to produce flat or rising fold, and fold falls 4.1x.

### 56c. But we pre-specified the wrong discriminator, and the right one is ambiguous

**Declining fold is the arithmetic consequence of any finite partner set**, because expectation grows
linearly in k. The quantity that actually separates a complex from a window is **whether the hit count
saturates** — and we did not pre-specify it.

**It does not saturate.** k grows **32x** (25 → 800), fold falls only **4.1x**, and **hits grow 7.8x,
from 12 to 93.** A complex with N true partners would plateau at N with fold falling as fast as k rises.
Translation proteins keep accumulating through MVP's entire top-800.

So the honest reading is **mixed, and our registered verdict of COMPLEX-LIKE is not wrong so much as
answering a weaker question than we thought it was.** The 12 hits at k = 25 against 0.32 expected are a
real, sharp, top-of-list signal that the negatives entirely lack. The continued accumulation to 93 hits
at k = 800 is what a shared elution window looks like. **Both are present**, which is consistent with a
small specific association sitting inside a broad co-migration envelope — and we cannot separate them
with this instrument.

**This is the third time today a registered criterion has failed to capture what it was written to
capture** (#231 named charge instead of length; #238's look-alike percentile was 55% likely by
construction; now this). It is becoming the project's characteristic failure, and it is a different
error from the one-way gate: the bars were reachable and resolvable, but **the statistic was not the one
that discriminates.**

### 56d. Net effect on §40

| alternative | status |
|---|---|
| degree | eliminated |
| abundance | eliminated |
| family membership | eliminated |
| apparent mass | eliminated |
| seed length and charge | eliminated, though #238 shows our headline number for it was weak |
| **polysome-window co-elution** | **eliminated on the registered criterion, but the unregistered saturation test leaves it live** |

And the contact-instrument question, which §51 appeared to close and §55b restated as a bound, is
**reopened** by §56a with no valid estimate available.

**Still unpromoted.** But §40 is now the most-attacked surviving observation in this project — six
registered alternatives, five cleanly eliminated — and the reason it stays unpromoted is no longer that
we expect it to fail. It is that one instrument cannot separate a specific association from the
co-migration envelope it sits inside, and the experiment that could is a bench experiment, not a
reanalysis.

## 57. The export test: both terms undecided, and the length-charge control is unusable for small terms

`EXPORT_PREREGISTRATION.md` plus its pre-result addendum. **Registered outcome for both terms:
UNDECIDED.** Our registered expectation was that detoxification would die on the matched control; it
effectively did, but on a control the addendum then showed cannot be trusted in either direction.

### 57a. A bug our own gate caught

The first run failed gate 1: the vault core gave **p = 0.125** where §51 gave 0.024. That was not a
finding, it was our error — we built the analysis frame indexed in **GENCODE file order** while the
abundance proxy is **table order** (§41 established there is no intensity column), silently scrambling
one of the three matching axes. Rebuilt in table order, the gates reproduce §51 exactly: **core
p = 0.0240** (§51: 0.024) and **`GOCC_RIBOSOME` p = 0.1835** (§51: 0.184). Recorded because the
positive control did its job: a gate we registered for a different purpose caught an indexing bug that
would otherwise have read as a biological null.

### 57b. The results, and why neither counts

> **[VOID — see §63. Every p-value in this section comes from the three-way length x charge x
> abundance matching, which is degenerate: 1,166 proteins over up to 1,000 cells, 49% of occupied
> cells holding one protein, and MVP's own cell holding MVP plus one other. The null was drawing the
> test subject. The one-way abundance-matched result is unaffected.]**


| term | n | observed | matched null | p (matched) | donor-pool ratio | verdict |
|---|---|---|---|---|---|---|
| `GOBP_DETOXIFICATION` | 15 | +0.970 | +0.426 | **0.0526** | **4.07x** | UNDECIDED |
| `GOCC_LATE_ENDOSOME` | 13 | +0.740 | −0.207 | **0.0101** | **5.54x** | UNDECIDED |

Late endosome **clears** the matched control at p = 0.010; detoxification **just misses** at p = 0.053.
But the addendum's donor check disqualifies both: the donor pools are **4.07x and 5.54x** enriched for
their own term's adjacency sets, far above the 2.0x invalidity bar.

**And we extend the addendum's rule symmetrically, which it did not state.** It said a term clearing an
invalid control is undecided rather than a survivor. The same must hold in reverse: **a control that
cannot validly support a survival cannot validly support a death either.** So detoxification's
p = 0.053 is not a kill, and late endosome's p = 0.010 is not a finding. Both undecided.

### 57c. The real result is methodological: this control does not work for small specialised terms

Three independent applications now:

| term | donor-pool enrichment |
|---|---|
| `GOBP_CYTOPLASMIC_TRANSLATION` (§56a) | 2.48x (**corrected to 2.86x**, §64b) |
| `GOBP_DETOXIFICATION` | **4.07x** |
| `GOCC_LATE_ENDOSOME` | **5.54x** |

**Small specialised terms occupy sparse corners of length-charge space, and the only proteins available
as donors in those corners are the term's own relatives.** The matching therefore regresses the label
partly on itself, and the effect gets worse as the term gets more specialised. §51's method is sound in
principle and **unusable in practice for any term small and distinctive enough to be interesting here.**
That retrospectively weakens every use we made of it, which is #237 generalised from one case to the
technique.

### 57d. What the member lists show, which is the most useful thing here

The registered transparency requirement earns its place:

**`GOCC_LATE_ENDOSOME`** — NBR1 **+5.09**, ATP7A +2.38, ANXA2 +1.74, FYCO1 +0.97, SQSTM1 +0.33,
VPS29 +0.25, MCOLN2 +0.19, then MAGI2 −0.00, HSPA8 −0.10, VAC14 −0.13, MYO5A −0.18, CHMP2A −0.20,
GRN −0.74.

**The +0.740 mean is carried by three proteins, and two of them we already knew individually** — NBR1
(§44b, the one autophagy receptor present while p62 is not) and ANXA2 (#182, a confirmed interactor
surviving every instrument). Ten of thirteen members sit at or below zero. **This is not a late-endosome
module; it is two known interactors plus ATP7A, re-annotated.**

**`GOBP_DETOXIFICATION`** — TXN +3.62, ALDH1A1 +3.16, ATP7A +2.38, HBD +1.67, PRDX1 +1.52, S100A9
+1.48, MT1G +1.37, GSTP1 +0.87, then ALB +0.48, TXNRD1 +0.35, NQO1 +0.19, AIFM2 +0.16, AKR1B10 −0.18,
LANCL1 −0.81, PRDX3 −1.73. Carried by the top three of fifteen.

**`ATP7A` appears in both lists** — a copper-transporting ATPase, at +2.38. One protein, not a module,
and we are not building anything on it. But it is the single protein in this analysis that is itself an
efflux pump, so it is the one name worth carrying forward to the bench experiment rather than another
reanalysis.

### 57e. Status of the export hypothesis

**Unchanged from §54: exploratory, nothing promoted.** The shape that made it interesting is intact —
degradation machinery is the most depleted thing in the pulldown (§49c), classical secretion is absent,
and the two terms nearest the non-classical exit route are the two that came up. But the control that
would have tested it does not work at this term size, the two means are carried by three proteins each,
and two of those are already-known individual interactors. **The hypothesis is not supported and not
refuted by this analysis, and the honest next step is the bench, not another matching scheme.**

## 58. Why the literature is silent on vaults in stool: the standard workflow discards them

`FECAL_MUCUS_PROTOCOL.md`. **Registered outcome: NO QUALIFYING DATASET.** The question stays open, and
per the protocol we report that the lookup failed rather than reporting an absence. But the reason it
failed is informative, and it is not about MVP.

### 58a. The canonical stool-proteome workflow is blind to vaults by construction

Lichtman, Marcobal, Sonnenburg & Elias, *"Host-centric Proteomics of Stool"*, Mol Cell Proteomics 2013;
**PMID 23982161, PMC3820941, DOI 10.1074/mcp.M113.029967**. The paper's own deposit identifier is
**PXD000240**, not the PXD000506 we had listed (#235 is corrected accordingly; 506 is the companion).

Its method, quoted from the paper: stool is centrifuged at **2,500 × g and then 35,000 × g**, the
pellet is **discarded**, and the soluble supernatant is analysed — *"we partitioned microbe-bound
proteins from the secreted soluble host proteins on which our analysis focused."* Host identifications
from the supernatant were enriched for *secreted* annotations; the pellet fraction they set aside was
enriched for *"methylation, acetylation and filament."*

**A 13 MDa 78-mer particle sediments at 35,000 × g.** Differential centrifugation in that range is how
vaults are *purified*. So the fraction this workflow throws away is precisely the fraction where an
intact exported vault would be.

**That is a structural answer to the question, and a better one than a protein list.** The silence we
recorded in #235 is not evidence that vaults are absent from stool; it is what a secretome-focused
preparation guarantees. By the protocol's gate, the dataset cannot speak to MVP, and we determined that
from the **methods** rather than from the identification table — a more fundamental disqualification
than the ACTB/GAPDH check we had registered.

Depth compounds it: the human arm identified **234 host proteins** (the text says 234, the Figure 4
legend says 244 — an internal inconsistency we could not resolve), with a **core proteome of 57
proteins** shared across three donors. Even ignoring centrifugation, 234 proteins is far too shallow to
make an absence meaningful.

### 58b. What we could not reach, stated plainly

The human identification table (Supplemental Table S5) is **not retrievable by automated fetch**. PMC
serves a bot interstitial in place of the supplementary `.xlsx` files; Europe PMC's supplementary-files
API returns *"Article with id PMC3820941 is not open access one"*; the publisher copy returns HTTP 403.
The PRIDE project pages for **PXD021424** and **PXD057120** are JavaScript shells that return a
44-character document, so their linked publications were not reached either.

**So we have not checked whether MVP, ACTB, GAPDH or HSPA8 appear in any stool protein list.** We are
recording that as a failure to look, not as a look that found nothing. The distinction is the whole
reason the protocol separated the two.

### 58c. What this changes

- **#235 stands and is strengthened**: nobody has reported MVP in stool, and we can now say *why* the
  standard method would not have found it. That makes the question more worth asking, not less.
- **Our registered expectation was "MVP absent or datasets fail to qualify."** The datasets failed to
  qualify, for a reason we had not anticipated and which no protein list would have revealed.
- **Paper 2's Experiment 13 is wrong as written and is corrected**: it must interrogate the
  **35,000 × g pellet**, not the supernatant. Every published host-centric stool proteome we found
  discards exactly the material the experiment needs. That is now the experiment's single most
  important design point, and it is the kind of detail that decides whether a negative means anything.
- **Mucus remains entirely unexamined.** We have no accession and found no human mucus proteome with a
  protein list, and we are not substituting a related matrix for it.

## 59. MVP *is* in human gut mucus — and it is exactly where cell leakage would put it

`FECAL_MUCUS_PROTOCOL.md`. **Registered outcome: MVP REPORTED in qualifying datasets.** Our registered
expectation was that MVP would be absent or that the datasets would fail to qualify. **That was wrong,
and #235 is corrected: the mucus half of our literature claim was simply mistaken.**

Source: van der Post et al., *"Structural weakening of the colonic mucus barrier is an early event in
ulcerative colitis pathogenesis"*, **Gut 2019; PMID 30914450, PMC6872445, DOI
10.1136/gutjnl-2018-317571**, PRIDE PXD012632. Open access, supplementary tables retrieved via Europe
PMC's `supplementaryFiles` API — the route that failed for the stool paper.

### 59a. The identification is solid

| | colon mucus (Table S5) | ileal mucus (Table S6) |
|---|---|---|
| UniProt | Q14764, "Major vault protein" | Q14764 |
| **unique peptides** | **52** | **52** |
| median normalised intensity | 1.02e8 | 3.71e9 |
| **percentile of all quantified proteins** | **94.4** (of 853) | **94.8** (of 1,457) |

**Fifty-two unique peptides** for an 893-residue protein is deep coverage, and MVP sits in the **top 6%
of the mucus proteome by intensity in both tissues.** This is not a trace hit. Gate passed in all three
tables (colon: GAPDH + HSPA8; ileum: ACTB + GAPDH + HSPA8; secreted controls ALB, LTF, MUC2 present).

### 59b. And the comparison that matters says leakage

Leakage of cytoplasmic protein into mucus should scale with cellular abundance, and ACTB, GAPDH and
HSPA8 are all far more abundant in cells than MVP. So if MVP were being *exported* rather than spilled,
it should stand **above** them. It does not:

| protein | colon pct | ileum pct | MVP ratio (ileum) | authors' annotation |
|---|---|---|---|---|
| GAPDH | 96.0 | 98.0 | **MVP/GAPDH = 0.32** | IC |
| HSPA8 | 96.4 | 97.5 | — | IC |
| ACTB | — | 94.4 | **MVP/ACTB = 1.08** | IC |
| **MVP** | **94.4** | **94.8** | — | **IC** |
| ANXA2 | 97.2 | 98.1 | — | **S**, core=Yes |
| MUC2 | 97.9 | 99.7 | — | **S**, core=Yes |

Four things point the same way:

1. **MVP is below GAPDH and HSPA8 and level with ACTB** — precisely the ordering cellular abundance
   predicts, with no excess.
2. **The authors annotate MVP as `IC` (intracellular)**, not `S` (secreted) or `P` (plasma).
3. **MVP is not in their "core mucus proteome"** — ANXA2, MUC2 and LGALS3 carry `core=Yes`; MVP's field
   is empty.
4. **672 of 853 colon proteins and 1,143 of 1,457 ileal proteins are annotated `IC`.** Roughly 79% of
   these mucus proteomes is intracellular protein, so the dataset as a whole is dominated by shed and
   lysed cells. MVP's presence is unremarkable within that.

**And PARP4 and TEP1 are absent from all three tables**, so there is no evidence of an intact particle —
only of MVP. That is weak evidence against a particle, since both are substoichiometric and far harder
to detect than a protein contributing ~75% of vault mass, but it is the evidence available.

### 59c. What this does to the export hypothesis

**It is found and it does not support the hypothesis.** MVP reaches gut mucus in quantity, which the
literature already records and we had wrongly said it did not. But the hypothesis predicted MVP would
be *exported* — and in the one dataset able to test it, MVP's abundance is what spillage from dying
epithelium predicts, it is classified intracellular by the people who generated it, it is excluded from
their core secreted set, and it sits in a proteome that is four-fifths intracellular protein.

**This is the cleanest possible outcome for the question as asked.** The prediction was specific, the
data existed, we found it, and the answer is no — not "underpowered", not "uninformative", not
"equivocal". After a day of gates that could only say one thing, a test that simply answers is worth
noting.

Two things it does **not** settle:

- **Stool is still unexamined** (§58): the one workflow we could evaluate discards the fraction a vault
  would sediment into, so nothing here speaks to the lumen.
- **A loaded-versus-empty question is untouched.** Graham's hypothesis was not only that vaults get out
  but that *what is inside them* differs when they do. Nothing in a bulk mucus proteome addresses
  cargo, and Paper 2's Experiment 13 remains the way to ask it.

## 60. Stool: MVP is absent, and the gate says that means nothing — for a deeper reason than §58

`FECAL_MUCUS_PROTOCOL.md`. **Registered outcome for stool: NO QUALIFYING DATASET.** Both candidate
studies fail, for different reasons, and the second reason is more fundamental than the first.

### 60a. The dataset that should have worked

Tanca et al., *"A human gut metaproteomic dataset from stool samples pretreated or not by differential
centrifugation"*, Data in Brief 2015; **PMID 26306325, PMC4536287, DOI 10.1016/j.dib.2015.07.014**,
PRIDE **PXD001573**. This addresses §58's objection directly:

- **Five of its ten aliquots are NOT pretreated by differential centrifugation** — whole stool, pellet
  included, so the fraction a 13 MDa particle sediments into is retained.
- **The search database included human sequences**: *"sequences from 298 detected microbial genera ...
  were appended to the Homo sapiens sequences retrieved from SwissProt"*, a 5,990,075-sequence
  host-microbiome database.
- Over 5,800 proteins identified, with the paper advertising *"deep information about gut microbiota and
  host proteins in the same experiment."*

And unlike every other dataset in this search, **its processed identification table is public**:
`DC_5repl_vs_NC_5repl_host-microbiome_identified_proteins.xlsx`, 2.4 MB, downloaded from the PRIDE FTP
archive. 5,859 rows, of which **232 carry human identifiers.**

### 60b. MVP is absent, and the gate fails 0 of 3

Searching all 5,859 rows for `MVP`, `MVP_HUMAN`, `Q14764` or "vault": **nothing.**

But the registered gate — at least two of ACTB, GAPDH, HSPA8 — returns **0 of 3**. None of the three is
present. Nor are ALB, LTF, LCN2 or MUC2 by symbol. **So the dataset does not qualify and MVP's absence
is uninformative**, which is precisely the determination the gate existed to make.

### 60c. Why, and it is a better answer than §58's

The reason is visible in the 232 human proteins. The top of that list by unique peptides:

FCGBP (57), maltase-glucoamylase (49), myosin-7 (24), alpha-1-antitrypsin (23), cytosol aminopeptidase
(21), NAALADL (20), serpin B6 (19), CLCA1 (17), CDHR2 (17), DMBT1 (16), DPP4 (16), meprin A alpha (15),
elastase 3A (14), intelectin-2 (14), chymotrypsin-C (14), meprin A beta (14), polymeric Ig receptor
(14), transthyretin (13), pancreatic lipase (13), dipeptidase 1 (13), neprilysin (13), intestinal
alkaline phosphatase (12), ZG16, intelectins, enteropeptidase, sucrase-isomaltase...

**That is a lumenal and brush-border secretome, essentially without cytoplasm.** Digestive proteases,
glycosidases, peptidases, mucus and barrier proteins, serpins. **No beta-actin, no GAPDH, no HSC70** —
the three most abundant cytoplasmic proteins in most cells. The one actin present is **ACTA1, skeletal
muscle actin**, which alongside titin, myosin-1, myosin-7, muscle glycogen phosphorylase and myosin
light chain is far more likely **dietary** than host (the study ran a separate food database for exactly
this reason).

So §58 concluded the stool workflow *discards* vaults by centrifugation. **This is stronger: even when
nothing is discarded, cytoplasmic protein does not survive the colon.** The lumen is a proteolytic
environment, and shotgun stool proteomics recovers what is built to survive it. A 13 MDa cytoplasmic
particle would have to survive both the gut and the sample prep to appear here, and the absence of
GAPDH says the first hurdle alone is enough.

### 60d. Closing the protocol

| matrix | outcome | basis |
|---|---|---|
| **gut mucus** | **MVP PRESENT** (§59) — 52 unique peptides, 94th-95th percentile — **but at cell-leakage level**, annotated `IC`, not in the core mucus proteome | van der Post 2019, qualifying |
| **stool** | **NO QUALIFYING DATASET** | Lichtman discards the pellet (§58); Tanca retains it but recovers no cytoplasmic protein at all |

**The registered expectation for stool — "MVP absent or the datasets fail to qualify" — is met, by the
second clause.** We will not be answering the stool question from public proteomics, and we now have a
specific reason rather than a shrug: **shotgun stool proteomics cannot see cytoplasmic protein, so it
cannot see a vault whether or not one is there.** Paper 2's Experiment 13 therefore needs targeted
detection — immunoblot and targeted MS against MVP, PARP4 and TEP1 — rather than a shotgun survey, and
that is now also stated in the experiment.

## 61. The paper's own title overstated a result, and the gate it rests on failed

Found by auditing the title against the scorecard rather than against the prose. **Two separate
problems, and we are fixing the one that is ours to fix.**

### 61a. The turnover test's committed verdict is UNINFORMATIVE, and we are keeping it

`results/turnover.json` records `"gate_short": false, "gate_long": true, "verdict": "UNINFORMATIVE"`.
The short-lived controls (MYC, FOS, JUN) are absent from pulse-SILAC data entirely; the long-lived
controls separated.

The registered text says: *"**If neither direction separates**, the table is not being read correctly
and nothing is reported."* One direction did separate. **So the registered rule would have passed this
test, and the script that printed UNINFORMATIVE imposed `both` where the registration said `neither`** —
which is exactly what #49 and #51 recorded at the time, as a code fault rather than a data problem.

**We are not reclassifying it.** House rule 2 says a failed gate means UNINFORMATIVE and does not mean
reinterpret, and a committed output file saying UNINFORMATIVE is the kind of thing this project treats
as binding even when a later reading of our own registration is more permissive. Rescuing a verdict by
re-reading our own rule, a day later, in the direction that helps, is the move we have refused four
times today. The conservative label stands.

### 61b. But the title asserted what the secondary test denied

The registered secondary test was explicit:

> **DEGRADE AS A UNIT:** spread below the 5th percentile of random triplets.
> **NOT A UNIT BY TURNOVER:** otherwise.

Observed: MVP **66.4 h** (58.6th percentile), TEP1 **40.6 h** (32.9th), PARP4 **22.2 h** (9.8th), spread
44.2 h at the **29.86th percentile of 10,000 abundance-matched random triplets.** The script applied the
registered bar correctly and returned `"NOT A UNIT BY TURNOVER"`.

**And that 29.86 is the number the title ignored.** The three subunits are **less dispersed than 70% of
random protein triples.** They fail the demanding 5th-percentile bar for unity, but they are nowhere
near unusually spread either. *"Three lifetimes"* asserts a distinctness that the dispersion statistic
does not support — three values that differ, drawn from a spread that is unremarkable.

**The title is corrected.** It was changed here to *"One assembly, a sealed nucleotide pocket, and one
question that gave three answers"* - **and changed again at §78d, because "sealed" was itself withdrawn
at §73 and we had not registered it.** The current title is *"One assembly, no stoichiometric
neighbourhood, and an instrument that cannot see a known subunit."* The three half-lives remain
reported, with their percentile against random triplets alongside them, which is how they should have
appeared from the start - though §75 notes their three decimals are false precision against a 22.6% CV
bar, roughly +/-15 h on the MVP estimate.

### 61c. What still stands from the turnover work

- **MVP is not structural furniture.** 66.4 h, 58.6th percentile of 8,804 proteins, median proteome
  half-life 56.5 h — mid-pack, and nowhere near lamins and histones at 1,500-1,700 h. At ~100,000
  copies per cell the population is continuously rebuilt. That was the registered primary outcome
  (**ORDINARY**, between the 25th and 75th percentiles) and it is unaffected by either problem above.
- **PARP4 is the fastest-turning-over subunit** at 22.2 h, 9.8th percentile, and #47 records this
  holding in 4 of 4 human cell types. But #70 already flagged that the headline 22.2-against-66.4 pair
  comes from the **proteome-table summary**, not the per-cell-type measure, and #76 struck the inference
  that a fast PARP4 requires active extraction, since a substoichiometric protein has an expected free
  cytoplasmic pool that can dominate the measurement.
- **ANXA2 at 82.3 h (69.7th) and S100A10 at 68.3 h (60.1st)** sit above MVP, which is worth noting
  only because they are the two confirmed non-subunit interactors.

**The lesson is narrow and worth stating: we audited the prose against the data repeatedly today and
never once audited the title.** It had carried an overstatement through every revision, including three
rewrites of the abstract directly beneath it.

## 62. §61 rediscovered a fault the ledger had already recorded and fixed

Auditing `CONTRIBUTING.md`'s own citations — the last un-audited surface — turned up the most
uncomfortable finding of the day. It is about the record-keeping system, which is this project's main
artefact.

### 62a. The title fault is a repeat, not a discovery

Ledger **#80** reads, in part:

> *"Four conclusions asserted in the title and abstract were backed by tests whose own verdict is
> UNINFORMATIVE... `turnover.json` verdict UNINFORMATIVE... yet the **title** asserted 'an independently
> turning over enzyme'... **The paper violated its own central methodological promise in its first
> sentence.** Title changed, abstract rewritten, and a gate scorecard added."*

**That is §61.** Same test, same file, same failure: a title asserting a turnover result whose committed
verdict is UNINFORMATIVE. It was found, the title was changed, a scorecard was added — and then a
turnover claim went back into the title as *"three lifetimes"*, survived every subsequent revision, and
was rediscovered from scratch a day later.

**So §61 was not a new finding. It was a regression.** We had a house rule (2), a ledger entry
documenting the violation, and a fix, and the fault returned anyway. That is worse than a first
occurrence, and the reason is visible: **nothing in the workflow re-checked the title.** Every audit we
ran compared prose to data. The title is prose that no section owns.

### 62b. The ledger's strikethrough notation is ambiguous, and it hid this

`~~strikethrough~~` is used for two different things across 64 struck entries:

- **refuted** — 23 say "STRUCK", 10 say "WITHDRAWN" or "SUPERSEDED"
- **remediated** — at least #80, where the body says *"Title changed, abstract rewritten"*. The claim
  was **true and acted on**, not refuted.

Reading #80 today, the strikethrough made it look like a claim that had been disproved. It had not — it
had been *fixed*, and the strike recorded the fixing. **A notation that marks "this was wrong" and "this
was right and we dealt with it" identically will eventually hide a live problem**, and here it did:
had #80 read as a standing warning, the title would have been on the audit list.

Unresolved on purpose: we are **not** retro-editing 64 entries to split the notation. That would be a
large rewrite of a historical record for a readability gain, and this repository's whole premise is that
corrections sit next to claims rather than replacing them. Instead the convention is stated here and in
`CONTRIBUTING.md`: **from now on a remediated-but-true entry is marked `[FIXED]` rather than struck**,
and #80 gets that annotation in place.

### 62c. House rule 3 cites a ledger entry that does not exist

> *"3. Read the table, do not describe it. Faults #59, #60, #64, #70, **#90** are all the same
> mistake."*

**There is no #90.** The ledger numbering runs ...#88, then jumps to #91. Confirmed by enumerating every
id: the only other gaps are the deliberate sub-entries (13→13a, 26→26b, 34→34b), and 268 entries carry a
maximum id of 267, so the count is otherwise consistent.

So one of the five citations backing a house rule points at nothing. The other four exist and say what
the rule claims. **We are leaving the number in place and annotating it as dangling**, because deleting
it would make the rule look cleaner than its provenance actually is — and the rule stands on four
verified instances without it.

### 62d. What this says about the project

Today produced five consecutive findings that were **not about vaults**: a stale README, a title
overstating a denied result, a bench experiment premised on a retraction, three ledger entries
asserting superseded claims, and now a fixed fault that regressed plus a house rule citing a
nonexistent entry.

**The analysis is finished and the documentation is now the failure surface.** That is a normal place
for a project this size to arrive, but it is worth naming rather than discovering a sixth time: the
remaining risk in this repository is not that a number is wrong. It is that a true number sits beside a
sentence that no longer follows from it.

## 63. The length-charge matching was degenerate from the start, and the rerun shows why

Grok audit 4 (`grok/from-grok/004r-*`) ordered one rerun with a specific donor-pool spec. We ran it, and
it found something worse and simpler than the adjacency contamination either of us was arguing about.

### 63a. The rerun: all three terms NON-IDENTIFIABLE, by a factor of ten

Grok's spec: restrict donors to the matched decile cell with term members **and** adjacents removed;
require **≥30 remaining donors per cell** or emit NON-IDENTIFIABLE; delete the 2.0x switch.
`src/donor_restricted.py`:

| term | members | occupied cells | median usable donors/cell | max | cells with ≥30 |
|---|---|---|---|---|---|
| `GOBP_CYTOPLASMIC_TRANSLATION` | 95 | 35 | **0** | 3 | **0 / 35** |
| `GOBP_DETOXIFICATION` | 15 | 15 | 2 | 5 | **0 / 15** |
| `GOCC_LATE_ENDOSOME` | 13 | 13 | **0** | 6 | **0 / 13** |

No p-value was computed, because none is computable.

### 63b. The actual defect: the cells are almost empty

**The universe is 1,166 proteins and the three-way decile cross has up to 1,000 cells.** That is 1.17
proteins per cell by construction:

- **578 occupied cells, mean size 2.02**
- **49% of occupied cells contain exactly one protein**
- median 2, 90th percentile 4, 99th percentile 7, max 24

So the "matched random draw" was sampling from pools of one to three proteins, which routinely **included
the term's own members**. That is not a null distribution.

**And it invalidates the gate we leaned on hardest.** §51's control was that the vault core still clears
full matching at p = 0.024, which we described as proof the matching "discriminates rather than
destroys". Looking at the actual cells:

| protein | its cell | cell size | donors other than itself |
|---|---|---|---|
| **MVP** | (5, 8, 1) | **2** | **1 — `PAXBP1`** |
| PARP4 | (5, 9, 1) | 7 | 6 — MYH1, MYH10, MYH11, MYH14, MYH9, NEURL4 |
| TEP1 | (8, 9, 5) | 3 | 2 — SIPA1L3, SPEG |

**MVP's matched null was drawn from a two-protein pool containing MVP.** The null mean rose from the
universe's −0.27 to +2.01 precisely because the draws kept returning the test subject. The gate
"passed" while being self-contaminated, which is the worst way for a gate to pass.

### 63c. What this retracts, and what it leaves standing

**Retracted: every p-value from the three-way length x charge x abundance matching.** That is §51's
0.309 / 0.174 / 0.184, §57's 0.0526 and 0.0101, and the 0.024 gate in both. Not because the donor pools
were adjacency-contaminated at 2.48x-5.54x — that was a symptom we measured while missing the disease —
but because **the design never had enough donors to match against.** #250's generalisation ("unusable
for any small specialised term") was also wrong in its diagnosis: grok is right that smallness is not
the confounder, and the true limit is cell sparsity, which afflicts terms of any size in a
1,166-protein universe.

**Standing, and now more securely: the one-way abundance-matched results.** §48a and §49a matched on the
abundance decile alone — **10 cells over 1,166 proteins, about 117 per cell** — which is well populated
and non-degenerate. So the class shift stands exactly as grok said it does: translation
**+0.2284 against −0.3157**, a +0.544 log2 shift at **p = 0.004**, rank **23 of 1,276**. That result
never depended on the broken machinery.

**The asymmetry is the lesson: one-way matching here has ~117 donors per cell and three-way matching has
~2.** We added axes to make a control stricter and made it degenerate instead, then read its output for
two full sections without once checking how many proteins were in a cell.

### 63d. Grok's other four corrections, accepted

1. **Delete the symmetry sentence.** *"A control that cannot validly support a survival cannot validly
   support a death"* is **sign-wrong on the survival half**: contaminated donors inflate the null,
   suppress survivals and manufacture deaths, so a survival is a **lower bound** on the evidence.
   `GOCC_LATE_ENDOSOME` at p = 0.0101 beat a null weighted ~12x against it and we recorded it UNDECIDED
   — we under-called the most contaminated of the three. It is now moot, since §63a voids the p
   entirely, but the reasoning error is logged rather than quietly dropped.
2. **The saturation argument was the fold curve counted twice.** `(hits/k) / fold = 0.01271 at every
   single k`, because the background was estimated once and fold is just hit-rate rescaled by that
   constant — and `32/7.75 = 4.13 = 37.78/9.15`. Our "self-criticism" of the registered rule was
   correct but its replacement identified nothing. Correct label: **NON-IDENTIFYING**, not "mixed", and
   §40's script now emits that on a monotonic fold decline. Grok: no CFdb-only statistic can separate a
   specific association from a narrow hydrodynamic window, because such a window **is itself a clique**
   in co-fractionation.
3. **The mucus mechanistic sentence is withdrawn.** Length runs the wrong way for us: MVP is 893
   residues against GAPDH's 335, so the per-residue proxy is 0.32 x 335/893 = **0.120**, making MVP
   *lower* relative to GAPDH, not higher — the correction cannot hide an export excess. Both 0.32 and
   1.08 sit inside ordinary tenfold ionisation variation, and ACTB is quantified on **2 unique peptides**
   against MVP's 52. Cross-tissue intensity comparison is void (3.71e9 / 1.02e8 = 36.4 while the
   percentiles match). The `IC` tag covers **78.8% and 78.4%** of the two proteomes and is assigned from
   prior cytosolic annotation, so using it to conclude "intracellular leakage" is circular. **What
   survives: MVP is present in both mucus preparations, carries the authors' intracellular tag along
   with four proteins in five, and sits outside their core mucus set. Export and leakage are not
   distinguished.** §59's verdict over-called against the hypothesis and is corrected.
4. **The turnover title change stands, for a different reason than we gave.** The 29.86th percentile is
   precise, not noisy — Monte Carlo SE is **0.46 percentile points** at 10,000 triplets, and these three
   subunits *are* the whole population, so "a 3-point spread has enormous sampling variance" aimed at
   the wrong variance. But *"less dispersed than 70% of triplets, therefore not distinct lifetimes"*
   **overreaches**: 29.86 does not show the three rates are statistically compatible, and compatibility
   was never tested. The deletion is correct because an affirmative kinetic-separation claim landed in
   the body of the null, not because the data show equality. **The test that would decide it: a 2-df
   Wald or likelihood-ratio test of k_MVP = k_TEP1 = k_PARP4 on the pulse-SILAC fit covariance**,
   needing a per-rate CV ≤ 22.6% to have 80% power on the observed MVP-PARP4 gap of 0.0208 h⁻¹. More
   random triplets do nothing. Also: **keeping UNINFORMATIVE was right** — *"if neither direction
   separates"* is sufficient for silence, not an iff, and must-clause 1 is unmet because absent controls
   do not sit in the bottom 25%.

## 64. The same indexing bug, a third time — and this one was published

Following §63's retraction, we audited every script for multi-axis matching. Four use the three-way
decile cross; fifteen use the single abundance axis alone and are unaffected. **But two of the four
built their analysis frame in the wrong order, and one of those numbers is in the published ledger.**

### 64a. The audit

| script | section | matching axes | frame order | status |
|---|---|---|---|---|
| `ribosome_property.py` | §51 | ab × ld × cd | **table (correct)** | p-values void by degeneracy (§63) |
| `export_test.py` | §57 | ab × ld × cd | **was GENCODE — caught before publishing** | p-values void by degeneracy (§63) |
| `donor_and_k.py` | §56a | ab × ld × cd | **GENCODE — PUBLISHED as #243** | **figures wrong, corrected below** |
| `donor_restricted.py` | §63 | ab × ld × cd | table (correct) | the rerun; correctly NON-IDENTIFIABLE |
| 15 others | — | `ab` only | — | **unaffected; ~117 proteins per cell** |

The bug is always the same line: building the frame with `index=list(seq)`, which is **GENCODE FASTA
file order**, when §41 established that the abundance proxy **is table order** because the IP-MS table
has no intensity column. It silently scrambles one of three matching axes.

### 64b. #243's figures were all wrong, and the correct ones are worse for us

Recomputed on both orderings for `GOBP_CYTOPLASMIC_TRANSLATION`:

| | cells | donors | adjacent fraction | universe | **ratio** |
|---|---|---|---|---|---|
| GENCODE order — **what #243 published** | 65 | 189 | 0.772 | 0.311 | **2.48x** |
| table order — **correct** | **35** | **129** | **0.891** | 0.311 | **2.86x** |

Fewer cells, fewer donors, **89.1% of available donors translation-adjacent rather than 77.2%**, and a
higher ratio. **The direction of #243's conclusion was right and every number in it was wrong.**

It also explains §63 exactly: 129 donors across 35 cells is 3.7 per cell, and at 89.1% adjacency that
leaves roughly **0.4 non-adjacent donors per cell** — which is why the restricted rerun found a median
of **zero**.

### 64c. Why this one stings

This is the **third** appearance of one bug. We found it in `export_test.py` before publishing, said so
in §57a, and praised the gate for catching it — and then did not check the other scripts that shared
the idiom. The script carrying it into the ledger had already been written and run **before** we found
the bug elsewhere, so the fix went forward and never went back.

**House rule 12: when a bug is found in one script, grep the idiom across all of them before moving
on.** The gate caught it once. Nothing caught it twice, because we treated a class of error as an
incident.

Three corrections stand regardless of the arithmetic: §63's degeneracy finding (which rests on the
correctly-ordered `donor_restricted.py`), the retraction of every three-way-matched p-value, and the
one-way abundance-matched class shift at p = 0.004 (ten cells, ~117 proteins each, and no sequence
axis at all, so untouched by any of this).

### 64d. Rule 12 applied immediately, and the damage is bounded

Having written house rule 12, we applied it to its own bug class rather than only recording it. Three
checks across all 73 scripts in `src/`:

1. **Every abundance-decile construction** (10 scripts) indexes on `D.index` — table order — or on a
   `G` frame built from `D.index`. The four `G`-building scripts were each inspected individually:
   `ribosome_property.py` and `donor_restricted.py` were correct, `export_test.py` was fixed before
   publication, `donor_and_k.py` is fixed now.
2. **No remaining `index=list(...)` construction anywhere**, except the comment recording the fix.
3. **No script reorders `D` before computing its decile.** Thirty-five scripts contain a sort, reindex
   or sort_values, and in the ten that also build an abundance decile, every one of those operations
   acts on an *output* object — a q-value series, a ranked term list, a display table — never on the
   frame whose row order carries the abundance proxy.

**So the bug class is contained to the two scripts already named.** That is a more useful statement
than "we fixed two instances", because it is the difference between a repair and a bound. It took one
command, which is the point rule 12 is making.

## 65. A mechanism instead of a thirteenth house rule

Three occurrences of one documentation failure — a retraction appended at the end while the original
number stays stated as live where a reader meets it (#262, then #283 on the very retraction that
diagnosed it) — is enough to establish that writing the lesson down does not install it. So this one
gets a mechanism.

`RETRACTIONS.tsv` lists every retracted claim as a literal pattern, what retracted it, and why.
`src/check_retractions.py` fails if any pattern appears in `RESULTS.md`, `LEDGER.md`, `README.md` or
either paper **without a retraction marker within six lines.**

**It found two violations on its first run**, which is the only honest advertisement a checker needs:

1. **A false positive** — §53b's look-alike figure *does* carry an inline note, but the note's wording
   (*"but see §55c"*, *"nearly uninformative"*, *"by construction"*) was absent from the marker
   vocabulary. The marker list was the thing at fault, and it is extended.
2. **A genuine miss** — §55d quotes Grok's sharpest sentence, which contains *"a residual +0.070 log2
   (p = 0.174)"*. That p is void by §63, and a reader meets it inside a quotation presented
   approvingly. **Grok's argument about co-fractionation versus co-complex does not depend on the
   number; the number it was handed does.** Annotated.

The checker now reports `OK: 13 retracted claims checked across 5 documents`.

**What this is and is not.** It cannot tell whether a claim *should* be retracted — that judgement stays
with the ledger. It only enforces that a retraction, once made, is visible wherever the retracted figure
appears. That is the narrow failure this project kept repeating, and it is the kind of failure a grep can
hold and a house rule cannot: rules 1-12 all describe judgement, and judgement is what degrades at the
end of a long session, whereas a script that exits non-zero does not get tired.

Run it before any commit touching those five files. Twelve rules and one check is a better ratio than
thirteen rules.

### 65a. The mechanism is shipped but not installed, and that is a real gap

§65 built the checker and then told the reader to *"run it before any commit touching those five
files"* — which is a house rule about remembering to run the mechanism, and therefore the same
judgement-dependence §65 was written to remove. A mechanism that needs remembering is not installed.

`hooks/pre-commit` is committed: it fires only when `RESULTS.md`, `LEDGER.md`, `README.md`,
`RETRACTIONS.tsv` or a paper is staged, runs the checker, and blocks the commit with the reason and an
explicit `--no-verify` override. **Self-tested both ways** without installing it — a planted
`p = 0.309` is caught at the line it was planted on, and the restored tree reports OK.

**It is deliberately not installed.** Installing a git hook means writing an automatically-executing
script into `.git/hooks`, and this session's permission classifier declined that as unauthorised
persistence — correctly, on the general principle rather than anything about this script. So the hook
sits in the repository where it can be read before it is trusted, and installing it is one command,
recorded here and in the file's own header:

```bash
ln -sf ../../hooks/pre-commit .git/hooks/pre-commit
```

**Until someone runs that, the gate is advisory and the failure mode remains live.** That was the honest
state when this section was written: §65's argument is that judgement degrades and scripts do not, and
the project had an uninstalled script and a twelve-rule list, one step short of its own point.
**[CLOSED — the hook was installed by the user; verified end to end in §65c.]**

### 65b. The checker fired on §65a, and we committed anyway

Immediately after writing §65a — the section arguing that an advisory gate is not a gate — **the
checker failed, and the commit went through.** The flagged line was §65a's own description of the
self-test: *"a planted `p = 0.309` is caught at the line it was planted on"*. The checker was right
that a retracted figure appeared without a marker, and wrong only in that the sentence was never a
claim about the vault.

Two things happened at once, and both are worth recording:

1. **A real false-positive class.** Documentation *about* retraction machinery necessarily quotes the
   patterns that machinery watches for. The marker vocabulary now includes `planted`, `self-test`,
   `RETRACTIONS.tsv`, `check_retractions` and `caught at the line`, and the script's docstring records
   why the exemption exists.
2. **The gate being advisory is not a hypothetical.** The checker ran, printed FAIL, and the output
   scrolled past inside a longer command while the commit proceeded — because nothing was enforcing
   it. **§65a predicted this in the abstract and then demonstrated it in the same commit**, which is
   the most direct evidence available that the uninstalled hook is a live gap rather than a tidy
   footnote.

The checker now reports OK. **And the hook is installed as of this commit**, so the gap §65a and §65b
described is closed — see §65c.

### 65c. Installed, and verified in both directions

The hook is installed — `.git/hooks/pre-commit -> ../../hooks/pre-commit` — and tested through the
installed path rather than by running the checker directly:

| test | staged | result |
|---|---|---|
| **A** | clean tree, a watched document staged | **exit 0** — passes, does not obstruct ordinary work |
| **B** | a planted `p = 0.0101` presented as a finding | **exit 1**, with the reason, the three prior occurrences, and the `--no-verify` override |
| **restore** | violation reverted | **exit 0**, working tree matches HEAD |

Test B is the one that matters: the planted line said *"the residual was p = 0.0101 and we treat it as
a finding"* — the exact sentence shape of the error this project committed three times — and the commit
path refused it.

**So the sequence closes properly.** §62 diagnosed the failure and wrote a rule. §63-§64 committed it
again anyway, on the retraction that diagnosed it. §65 replaced the rule with a script. §65a admitted
the script was not installed and therefore not a mechanism. §65b watched that admission come true one
commit later. **§65c is the first point at which the thing is actually load-bearing**, and it took a
human running one command, because the session's own permission boundary correctly would not let an
agent install a self-executing hook on its own authority.

That boundary is worth recording as a feature rather than an obstacle: the gate now exists because
someone who could evaluate it chose to turn it on.

## 66. The two independent top-ten lists, compared — and my top novelty claim does not survive

Claude's lists were committed at **20:24:07** (`HYPOTHESES_AND_NOVELTY.md`, commit `005f309`); Grok's
were requested afterwards with the evidence and none of the rankings
(`grok/to-grok/005-*`, `grok/from-grok/006r-*`). The independence is checkable from `git log`.

### 66a. The hypothesis lists barely overlap at the top

| rank | **Claude** | P | **Grok** | P |
|---|---|---|---|---|
| 1 | nucleotide-sequestering buffer | 0.20 | **bare MVP shell is the investment; caps optional** | **0.40** |
| 2 | TEP1 latent TIR NAD(P)ase | 0.18 | multi-client sequestration cage, free COP1 the one client | 0.24 |
| 3 | polyribosome assembly platform | 0.15 | **ANXA2-S100A10 heterotetramer membrane dock** | 0.14 |
| 4 | **near-neutral tolerated extravagance** | **0.14** | ~~sealed pocket as ligand-gated waist latch~~ **WITHDRAWN §73** | ~~0.12~~ |
| 5 | cargo turnover, not transport | 0.12 | cap chemistry: TEP1 NADase on the shell platform | 0.10 |
| 6 | **furniture, no acute function** | **0.12** | ribosome-adjacent translation buffer | 0.09 |
| 7 | COP1 makes abundance regulated | 0.10 | extracellular deployment of shells | 0.07 |
| 8 | vtRNA chaperone | 0.08 | multidrug sequestration (LRP model) | 0.05 |
| 9 | mechanical/crowding buffer | 0.06 | innate-immune sensor | 0.05 |
| 10 | export with altered cargo | 0.06 | NBR1-selective autophagy adaptor | 0.04 |

**Three things I missed entirely**, and the first is the one that matters:

- **Grok's #1 at P = 0.40 — "the bare MVP shell is what cells invest in; PARP4 and TEP1 are optional,
  independently docked passengers, and the armed triple particle is a minor state."** I had every
  component of that argument — adrenal ranks first for the shell only, the holoenzyme peaks in gut
  mucosa, TEP1 is PARP4-independent, CFdb splits them, and my own A11 test found **MVP's transcript at
  the 96-97th percentile while PARP4 sits at 78-89 and TEP1 at 58-85** — and never assembled them into
  a hypothesis. Grok rates it double my top item. Its experiment is the right one: count cap occupancy
  per particle by cryo-ET in adrenal versus gut.
- **ANXA2-S100A10 as a membrane dock (0.14).** I had both proteins in my *novelty* list and never
  turned them into a function. They are a known obligate heterotetramer, which is harder to dismiss
  than either hit alone.
- **Innate-immune (0.05) and NBR1 autophagy (0.04).** I had written both off; Grok ranks them low but
  gives each a real kill experiment, which is more useful than omission.

**And one thing Grok missed.** Its ten are all functional. **Neither near-neutrality nor furniture
appears anywhere on its list** — the Vonnegut hypothesis is absent. Given repeated phylum-level loss,
I think that is a gap in its list rather than mine, and I am keeping A11 at 0.14.

Where we agree, Grok is consistently harsher and usually right: on translation it notes **1.4 MDa
dynein sits at the 96th percentile, two points below MVP**, so a large cytoplasmic particle reproduces
the enrichment — a sharper kill than anything I had.

### 66b. My top novelty claim is not novel, and the literature says so

Grok declined to rank one item and explained why: *"An MVP shell can exist without TEP1 or PARP4...
The independence claim survives. Its novelty does not."* I checked rather than take it on faith, and
**it is right**:

- **MVP-only recombinant vaults assemble in Sf9 insect cells** — ~96 copies of a single protein are
  *"sufficient to form the minimal structure and entire exterior shell."*
- **TEP1-knockout mice contain structurally intact vault-like particles** with reduced cap density.
- **VPARP (= PARP4) knockout mice are viable with no major phenotypic alterations.**
- Decisively: **"VPARP and TEP1 are able to incorporate into vaults even after the formation of the MVP
  vault particle shell is complete."** Independent incorporation is *explicitly published*.

**So B1 drops from P = 0.75 to about 0.20.** What survives is narrow: the quantitative demonstration in
a human-cell pulldown (TEP1 at WTKD_P **0.020** while PARP4 is at **2.85**, with the particle intact)
may be unreported, but **the conclusion it supports has been in print for roughly twenty-five years.**
I ranked it first of ten.

**And it corrects my labels.** I marked B2, B3 and B9 **[new observation]**. They rest on the published
Lodwick IP-MS and Zheng TurboID tables. **They are new readings, not new measurements** — Grok flagged
the same risk about its own #4 (*"assuming this IP-MS is unpublished... if this pulldown is already in
a preprint, the novelty call is wrong"*). It is published. Every claim of mine that rests on it is a
reading.

### 66c. Where Grok's novelty list beats mine

| Grok | P | my treatment |
|---|---|---|
| turnover triplet test never run | **0.76** | I had it **last at 0.35** |
| CFdb MVP-TEP1 is noise | 0.74 | mine at 0.60 |
| **the immune block is a STAT1/IRF9 regulon** | **0.72** | **absent from my list** |
| no enriched function + degradation most depleted | 0.70 | mine at 0.65 |
| MYOF excluded by two physical methods | 0.68 | mine at 0.70 — agreement |
| COP1 is free, not CRL4 | 0.64 | folded into my #5, under-weighted |
| three subunits do not co-rank across tissues | 0.60 | mine at 0.45 |
| **ruffle signal dies at contact** | **0.58** | **absent from my list** |
| mucus cannot be read as secretion | 0.55 | mine at 0.55 — exact agreement |
| TEP1 TIR/E1008 + ~~sealed pocket~~ (**WITHDRAWN §73**) | 0.42 | **I built hypothesis A1 on it without questioning novelty** |

Two misses of mine worth naming: **the interferon regulon** — the single cleanest piece of negative
work in this project, and I left it off a list of unremarked findings — and **the ruffle collapse**,
which I treated as a defeat rather than a result.

And Grok's #10 is the warning I needed: it suspects **the SPFH shoulder assignment is already in the
structural literature** and could name no paper for the TEP1 TIR glutamate either way. **My top-ranked
hypothesis A1 rests on that pocket**, so its novelty, and part of its force, is less secure than I
presented.

### 66d. What this exchange cost and bought

**Cost:** my first-ranked novelty claim, demoted from 0.75 to 0.20 by twenty-five-year-old literature;
three mislabelled claim types; and the admission that the hypothesis I ranked first rests on a
structural call Grok thinks is probably published.

**Bought:** a hypothesis at P = 0.40 that is better supported than anything on my list and which my own
A11 test supplied the evidence for; two novelty items I had omitted; and confirmation on the one place
we agreed exactly — the mucus reading, independently at 0.55 both times.

**The pattern across five audits is stable and worth stating plainly: Grok is better than me at
noticing when a result is already known, and better at refusing to let a negative become a story. I am
better at finding the negatives in the first place.** Four of today's twelve house rules came from it.

## 67. The phylogenetic argument, done properly — and my 4.1% was wrong by an order of magnitude

Graham asked two questions about §66's addendum: what do insects, nematodes and tunicates share, and
**could plants, fungi and apicomplexans never have had vaults rather than having discarded them?** The
second is the rigorous one, and answering it exposed a mistake of mine first.

### 67a. My own denominator was wrong

I reported *"210 of 5,090 eggNOG eukaryote species = 4.1%"*. **The 5,090 was every taxon in the file,
bacteria included.** The eukaryote count in this release is **477**. So the real figure is
**210 / 477 = 44%**, not 4.1% — wrong by a factor of ten, and wrong in the direction that made my
"repeated loss" story look stronger than the data supported. I flagged the percentage as the weak part
of that argument; I did not notice it was also arithmetically wrong.

### 67b. The clade distribution answers Graham's question, and reverses it

| clade | carry | total | % |
|---|---|---|---|
| **Vertebrata** | **104** | **104** | **100%** |
| Metazoa overall | 114 | 161 | 71% |
| **Fungi** | **83** | **179** | **46%** |
| Amoebozoa | 4 | 4 | 100% |
| Alveolata | 2 | 20 | 10% |
| Viridiplantae | 2 | 76 | 3% |
| Stramenopiles | 0 | 18 | 0% |

**So the answer to the question as asked is no — they did not fail to acquire it, they lost it.** The
domain is present in Amoebozoa, Metazoa, Fungi, Alveolata (ciliates), Rhizaria, Viridiplantae (moss and
*Chlamydomonas*) and **Parabasalia (*Trichomonas vaginalis*)**. That spans essentially the whole
eukaryote tree, including lineages outside Amorphea, which means the domain is most parsimoniously
**ancestral to eukaryotes** and the pattern is pervasive loss.

**And it corrects two things I told you.** Yeast is not representative: **46% of sampled fungi carry
the domain**, so "absent from fungi entirely" was wrong, drawn from *S. cerevisiae* alone. Land plants
mostly lost it rather than never having it — a moss and a green alga retain it.

### 67c. But the domain is not vault-specific, which weakens all of this

The five orthogroups are annotated **"Vault protein inter-alpha-trypsin domain"** — the **VIT domain**,
which MVP shares with the **inter-alpha-trypsin inhibitor (ITIH) family**. A VIT hit is therefore *not*
evidence of a vault.

That almost certainly explains the scattered presences: 46% of fungi, two ciliates, a moss and
*Trichomonas* are far more likely to be **ITIH-like VIT proteins than vault particles**, and the
established vault literature places vaults in animals, *Dictyostelium* and some protists, not in fungi
or plants. **So §66's phylogenetic argument rests on a domain census that cannot distinguish MVP from
its relatives, and the A11 near-neutrality case is correspondingly weaker than I presented it.**

**What survives the confound** — because absence of even the shared domain is a stronger signal than
presence of it:

- **Insecta: 0 of 30 genomes.** Thirty independent insect genomes, not one carrying even a VIT domain.
- **Nematoda: 0 of 10.**
- **Arachnida 0/1, Tunicata 0/2, Placozoa 0/1, Mollusca 0/1.**
- Against **Vertebrata 104/104**, and retention in Crustacea, Cephalochordata, Annelida, Porifera,
  Echinodermata, Platyhelminthes and Cnidaria.

Those zeros in well-sampled clades are real.

### 67d. What insects, nematodes and tunicates share — the honest answer

**Two of the three are Ecdysozoa**, and the losses cluster there: insects 0/30, arachnids 0/1,
nematodes 0/10. **Crustaceans break it** at 1/1 — and since crustaceans and insects are both
Pancrustacea, the loss is in **Hexapoda specifically, after their split from crustaceans.** Tunicates
are chordates and sit outside that story entirely.

So the clean statement is: **the losses are Ecdysozoa-heavy with crustaceans excepted, plus an
independent tunicate loss.** That is a clade pattern rather than a random assortment, which is worth
something.

**What I will not do is name a shared environment or mechanism.** Graham's instinct — *"my heart says
there's some benefit to dropping it in certain conditions, environmental"* — is a real hypothesis, and
this dataset cannot test it: the retainers and losers do not separate by habitat (soil nematode lost,
soil amoeba retained; marine tunicate lost, marine cnidarian retained), several groups rest on a single
genome, and the VIT confound sits over all of it. **A correlation I could draw from n=1 clades against a
non-specific domain would be exactly the kind of story this project has spent two days learning not to
tell.**

**The test that would settle it:** build proper MVP orthologs — reciprocal best hits plus the
MVP-specific shoulder and cap domains, not the shared VIT domain — across the sequenced Pancrustacea,
then ask whether loss coincides with any ecological variable. Hexapoda against Crustacea is the natural
contrast and both are densely sequenced.

## 68. The real MVP orthogroup: the loss is Ecdysozoa, and tunicates never lost it

§67 flagged that the five "vault protein inter-alpha-trypsin domain" orthogroups censused the **VIT
domain**, shared between MVP and the inter-alpha-trypsin inhibitor family, and that the analysis was
correspondingly weak. **It was worse than weak: those were the wrong orthogroups entirely.**

Locating human MVP's own protein IDs in GENCODE and finding which eggNOG group contains them returns
**exactly one: OG 2QPP0 — and it is none of the five.** The five were ITIH-family groups. MVP's
orthogroup was never examined.

### 68a. Within animals, the loss is a single clade

| clade | carry | total | |
|---|---|---|---|
| Vertebrata | 94 | 104 | 90% |
| **Tunicata** | **2** | **2** | **100%** |
| Cephalochordata | 1 | 1 | 100% |
| Platyhelminthes | 2 | 2 | 100% |
| Mollusca, Annelida, Porifera, Echinodermata, Placozoa | 1 each | 1 each | 100% |
| Cnidaria | 2 | 2 | 100% |
| **Insecta** | **0** | **30** | **0%** |
| **Nematoda** | **0** | **10** | **0%** |
| **Crustacea** | **0** | **1** | **0%** |
| **Arachnida** | **0** | **1** | **0%** |

**The losers are Ecdysozoa — 0 of 42 sampled genomes — and nothing else.** Every other animal phylum
sampled retains it, including sponges and placozoans at the base of the tree.

**Both of my previous claims were wrong.** *Ciona* does have MVP: **Tunicata is 2/2, not 0/2**, so
tunicates are not losers at all. And **crustaceans are 0/1, not 1/1** — so §67d's "the loss is in
Hexapoda specifically, after the split from crustaceans" is wrong. There is no split to explain. The
loss is **one event at the base of Ecdysozoa**, covering insects, crustaceans, arachnids and nematodes
together.

**So the answer to "what do insects, nematodes and tunicates have in common" is that the premise was
mine and it was false.** Insects and nematodes share Ecdysozoa. Tunicates were never in the set.

### 68b. And it is unambiguously loss, not failure to acquire

The 25 non-metazoan carriers span nearly every eukaryotic supergroup:

- **Amoebozoa** — *Dictyostelium discoideum*, *D. purpureum*
- **Stramenopiles** — eleven oomycetes: *Phytophthora* ×5, *Pythium* ×4, *Saprolegnia diclina*,
  *Aphanomyces invadans*
- **Euglenozoa** — *Trypanosoma brucei*, *T. cruzi*, *Leishmania* ×3
- **Opisthokonta outside animals** — *Monosiga brevicollis*, *Salpingoeca rosetta* (choanoflagellates),
  *Capsaspora owczarzaki*, *Fonticula alba*
- **Heterolobosea** — *Naegleria gruberi*
- **Alveolata** — *Paramecium tetraurelia*
- **Apusozoa** — *Thecamonas trahens*

**That distribution puts MVP in the last eukaryotic common ancestor**, and makes every absence a loss:
Ecdysozoa, land plants, apicomplexans — and **fungi, which carry zero**. My "46% of fungi" in §67b was
the ITIH confound precisely as suspected, and it is now withdrawn: **no fungus in this release carries
MVP.** *Capsaspora*, *Fonticula* and the choanoflagellates are Opisthokonta but not fungi, so the
fungal loss happened after their divergence.

### 68c. What this does to A11

**It strengthens the dispensability half and sharpens it.** A single basal loss across Ecdysozoa — the
most speciose animal clade on Earth, including every insect — plus independent losses in fungi, plants
and apicomplexans, is a gene that whole kingdoms discard. **And the loss is clean:** 0 of 42
ecdysozoans, not a patchy scatter that might be annotation failure.

**But it also undercuts the Vonnegut reading.** A protein retained from LECA through *Dictyostelium*,
oomycetes, trypanosomes, choanoflagellates, sponges, cnidarians, flatworms, molluscs, echinoderms,
amphioxus, tunicates and vertebrates — and sitting at the 96th-97th percentile of transcripts where
retained — is not drifting. **Near-neutral genes do not survive a billion years of purifying selection
in a dozen lineages and then sit in the top 3% of expression.** A11 stays on the list, but the
distribution reads much more like **a real function that Ecdysozoa, fungi and plants each found a way
to do without** than like a tolerated extravagance.

**The Vertebrata figure of 90% rather than 100% is most likely annotation gaps** in ten draft genomes
rather than ten real losses, and we are not reading anything into it.

### 68d. One observation we are deliberately not building on

The non-animal retainers are heavily weighted toward **pathogens and parasites**: eleven oomycetes
(*Phytophthora*, the potato-blight genus), five kinetoplastids (*Trypanosoma*, *Leishmania*),
*Naegleria*, *Aphanomyces*. That is a striking list and it is exactly the kind of pattern this project
has been wrong about repeatedly. **Oomycetes and kinetoplastids are also simply well-sequenced because
they are pathogens**, which is sufficient to produce the appearance without any biology. Recorded as an
observation with an obvious confound, not a lead.

## 69. §68 is a rediscovery of Daly 2013, and the literature corrects it in three ways

Before treating §68 as a finding we checked whether it was known. **It is**, and checking also found
three errors in it plus one piece of functional evidence that changes two hypothesis ratings.

### 69a. The core conclusion is published

**Daly et al. 2013, *"In silico resurrection of the major vault protein suggests it is ancestral in
modern eukaryotes"*** reconstructed ancestral MVP sequences to search across eukaryotes and concluded
**MVP was present in the last eukaryotic common ancestor with later loss in some lineages.** A
commentary on that work states the losses as *"at least in fungi, plants, and Ecdysozoa."*

**That is §68a and §68b verbatim.** Our clade census reproduced a twelve-year-old result. The census is
correct and it is not news — and this is the **second time today**: #289 demoted our top novelty claim
to twenty-five-year-old literature on the same grounds.

### 69b. Three corrections to §68 from the literature

1. **"0 of 42 Ecdysozoa" is too strong.** The commentary records that **one arthropod is known to carry
   MVP — the velvet spider *Stegodyphus*.** Our Arachnida cell was 0/1 and it was the wrong arachnid.
   A documented retention inside the lost clade matters: it weakens "one clean basal loss event" and
   raises either patchy loss or a regain.
2. **There is a competing hypothesis we did not mention.** A thesis on MVP distribution argues for **an
   independent horizontal gene transfer into eukaryotes**, noting that **only lophotrochozoan
   protostomes carry MVP among protostomes.** That conflicts with ancestral origin, so the field has
   **two live hypotheses** and §68b asserted one as settled. Our own data cannot separate them.
3. **MVP has bacterial and viral homologs.** A 2023 preprint reports the **first viral MVPs, in human
   gut bacteriophages, closely related to bacterial MVP homologs.** We had the phage result in #234 as
   a curiosity about the gut; it is in fact direct evidence bearing on the HGT hypothesis, and we
   filed it under the wrong question.

### 69c. The functional evidence that changes two ratings

The same search surfaced something no amount of reanalysis here would have produced:
***Dictyostelium* MVP knockouts show reduced survival under stressful nutrient conditions.**

**That is direct functional evidence, from a knockout, in a retaining organism** — and it is the
strongest single argument against the two non-functional hypotheses on our list:

- **A5 (furniture, no acute function): 0.12 → 0.07.** A knockout with a conditional survival defect is
  not furniture.
- **A11 (near-neutral tolerated extravagance): 0.14 → 0.06.** Near-neutrality predicts no phenotype in
  any condition. A nutrient-stress phenotype is what a real function looks like when the assay finally
  matches the condition.

**Graham's Vonnegut hypothesis therefore does worse on the literature than it did on our data**, and the
reason is instructive: our CRISPR-screen null came from rich-medium cancer lines. **The *Dictyostelium*
result says the phenotype appears under nutrient stress** — a condition no screen in our evidence base
tested. We read "no fitness coupling" as "no function" when it was "no function in the one environment
we looked at."

A12 (bare shell is the investment) and A1 (nucleotide buffer) are now the top two unchallenged, and
both are compatible with a conditional stress phenotype.

### 69d. The pattern worth naming

**Twice today a clean result of ours turned out to be published**, once at twenty-five years and once at
twelve. Both times it was Grok's habit — check whether it is known before ranking it — that caught the
first and prompted the check that caught the second.

**Vault biology is a small, old field with a long literature and few workers**, which makes it unusually
easy to rediscover. For a project whose whole method is registered tests against public data, the
missing gate is obvious in hindsight and is now stated: **a novelty claim needs a literature check
registered as its own gate, with the same standing as a positive control.** We ran forty tests against
data and none against the literature until an external reviewer made us.

## 70. The published functional literature, which this project never engaged — and which reframes its central negative

Applying §69d's gate properly meant asking what the field actually claims about vault function before
ranking hypotheses against it. **The answer invalidates the framing of §66's hypothesis list.**

### 70a. What is established, from knockouts, in good journals

| finding | model |
|---|---|
| **MVP knockout mice are healthy; mice lacking all three vault proteins are phenotypically normal** with subtle immune issues | mouse, triple KO |
| **MVP KO mice: attenuated antibody responses and reduced survival after influenza A rechallenge** | mouse, 2024 |
| **Global and myeloid MVP KO aggravates high-fat-diet obesity, insulin resistance, hepatic steatosis and atherosclerosis** — via IKK-NF-κB | mouse, *Nat Commun* 2019 |
| **MVP negatively regulates osteoclastogenesis via calcineurin-NFATc1**; KO inhibits osteoclast apoptosis, contributing to age- and OVX-related bone loss | mouse, 2021/2023 |
| **Endothelial MVP promotes Parkin-mediated mitophagy**, alleviating vascular remodelling | mouse, *Nat Commun* 2025 |
| **MVP suppresses lung cancer proliferation by inhibiting STAT3** | cell |
| **MVP KO zebrafish: organ regeneration preserved, but cell death enhanced after injury** | zebrafish, 22 kb coding deletion |

**There is a substantial published literature treating MVP as a signalling modulator** — NF-κB, STAT3,
NFATc1, Fas/apoptosis, mitophagy — with knockout support across four independent systems and multiple
*Nature Communications* papers. **None of it appears anywhere in this project's forty tests, and none of
my ten hypotheses was "MVP modulates signalling."**

### 70b. The pattern across every knockout is the one §69c found

**Baseline: normal. Under challenge: phenotype.** Healthy mice, normal triple-knockouts, preserved
zebrafish regeneration — but defects on **influenza rechallenge, high-fat diet, injury, ageing and
oestrogen withdrawal**, plus the *Dictyostelium* nutrient-stress survival defect from §69c. **Five
independent systems, same shape.**

That is exactly the error §69c diagnosed, now confirmed at scale: our "no fitness coupling" came from
**CRISPR screens in rich medium**, which is the one condition in which every published model is also
normal.

### 70c. It reframes this project's central negative result

Forty registered tests found **no physical interaction neighbourhood around MVP by any instrument**. I
have been treating that as the project's main finding and as evidence against function.

**The published function is signalling modulation.** NF-κB, STAT3 and NFATc1 interactions are
**transient, low-stoichiometry and regulatory** — precisely the class that co-abundance, co-elution and
wash-based immunoprecipitation are worst at recovering. **So the absence of a stable neighbourhood is
consistent with the published function rather than evidence against it**, and the instruments were
wrong for the question the field is actually asking.

That does not retract any of the forty tests. **It relocates them**: they are a well-controlled
demonstration that MVP has no **stoichiometric partner complex** beyond PARP4 and TEP1 — which is a
real and useful negative — and they say nothing about transient regulatory interaction, which is where
the published evidence sits.

### 70d. And it corrects my immune dismissal

§36 concluded the immune co-abundance block is a **STAT1/IRF9 regulon, not a physical neighbourhood**,
and Grok ranked that observation at 0.72 as likely unremarked. **The observation stands. The inference
I drew from it does not.** I treated "the co-abundance signature is transcriptional" as "there is no
immune function" — and MVP KO mice have attenuated antibody responses and reduced influenza survival.

**Two different claims, and I collapsed them.** A transcriptionally-driven co-abundance block is not
evidence against an immune role; it is evidence that co-abundance was the wrong instrument to find one.

### 70e. What this does to the hypothesis list

**The list was built in ignorance of the tested hypotheses, which makes its ratings unreliable.** A
signalling-modulator hypothesis belongs at the top of any ranking of what vaults are *for* — and it
does not belong on a list of **untested** hypotheses, because it has knockout support across six
papers — though §76b shows that support is **one group's programme plus one independent replication**,
not six independent results.
Graham asked for untested ideas; I supplied ten without establishing what was already tested.

The ratings that move:

- **A5 (furniture) → ~0.04** and **A11 (near-neutral) → ~0.03.** Five systems with conditional
  phenotypes, and a documented NF-κB mechanism, leave very little room.
- **A1 (nucleotide buffer, 0.20) and A12 (bare shell, 0.35) survive best**, because both are agnostic
  about what the shell then does and are compatible with signalling modulation.
- **A2 (TEP1 NADase) gains**, since NAD(P) consumption is a signalling mechanism and would sit
  naturally beside the published pathway work.
- **The innate-immune hypothesis, which I omitted entirely and Grok ranked at 0.05, should have been
  near the top.** It has direct knockout evidence and I dismissed it on a co-abundance artefact.

## 71. The pulldown is a deposited dataset with its own PARP4-knockout analysis, and four novelty claims fall

Applying §69d's literature gate to the remaining novelty claims produced one search that settles most
of them, and not in our favour.

### 71a. It is PXD052802, and the match is exact

A PRIDE deposit describes **co-immunoprecipitation of human MVP using a synthetic antigen binding
reagent (sAB) called VM1, with a control reagent called H6, comparing wild-type against PARP4-knockout
A549 cells**, reporting that *"PARP4, as well as a number of other proteins, were significantly
enriched in the experimental co-IP from the WT versus PARP4 KO cells."*

**That is the dataset we have been analysing all day.** Our table's columns are literally `WT-H6-1/2/3`,
`WT-VM1-1/2/3`, `KD-H6-*` and `KD-VM1-*`. **VM1 and H6 are the reagent names; WT and KD are the
genotypes.** We had been treating this as a generic human anti-MVP IP-MS and never established the cell
line: **it is A549, a lung adenocarcinoma line** — which is worth knowing given that this protein's other
name is lung resistance-related protein, and which we should have known before drawing a single tissue
inference from it.

### 71b. Grok predicted this exact failure

In audit 3 it wrote, of its own equivalent claim: *"New observation, **assuming this IP-MS is
unpublished**... **If this pulldown is already in a preprint, the novelty call is wrong.**"* We quoted
that caveat approvingly in §63d and **did not then go and check.** The deposit exists, with a described
analysis of the same WT-versus-PARP4-KO contrast we used.

### 71c. The claims that fall

**Four of ten novelty claims rest on this dataset, and a paper depositing it would have analysed its own
interactor list.** We cannot verify publication status from the deposit alone, and we are not going to
assert it either way — but a described analysis of the identical comparison is enough that these
probabilities cannot stand:

| claim | was | now | why |
|---|---|---|---|
| **B1** TEP1 PARP4-independent | 0.75 → 0.20 (#289) | **→ 0.08** | the depositors ran WT vs PARP4-KO; TEP1's behaviour in that contrast is the first thing their analysis would show |
| **B2** MYOF actively excluded | 0.70 | **→ 0.25** | depletion in their own WT-vs-KO comparison; survives partly because the TurboID arm is a second dataset |
| **B3** degradation most depleted | 0.65 | **→ 0.25** | a term-level read of their interactor list |
| **B7** translation-enriched co-elution tail | 0.50 | **0.50, unchanged** | rests on CFdb, not on this pulldown |

**B5 (CFdb noise floor) and B6 (mucus) are unaffected** — different datasets. **B4 (stool workflows
cannot see a vault) is unaffected** and is now our best-standing novelty claim, because it is a
methodological argument about other people's protocols rather than a reading of anyone's table.

### 71d. The honest tally on novelty

**Three literature checks, three prior-art hits:** B1 at twenty-five years (#289), the whole
phylogenetic argument at twelve (§69a), and now the pulldown's own provenance. **Every check we have
run has found something**, which is the strongest possible argument that the eight unchecked claims
should be read as provisional rather than ranked.

**What survives best is what rests on nobody's table:** B4, a methods argument about stool
proteomics; B5, a sensitivity failure of a public resource; B6, an unremarked row in a published mucus
table; B7, a co-elution statistic on CFdb. **What falls is everything that reads a single published
interactor list more carefully than its depositors did** — which was, in hindsight, always the weakest
kind of novelty to claim.

**And the sharpest lesson of the two days is in §70 and here together.** We ran forty registered tests
against data and none against the literature, then ranked ten findings for novelty without checking any
of them. The gate we built for everything else — *recover a known positive control before believing the
result* — has an exact analogue we never built: **recover the existing literature before believing the
finding is yours.**

## 72. A mechanism for the failure that happened four times

#262, #283, #319 and #320 are one error in four documents: **a correction landing in one place while
every other document asserting what it changed stays unqualified.** Three of the four were found only
because the previous one had just been found, which is not a learning curve — it is the same error
propagating one document at a time, because each fix was scoped to the file in front of us rather than
to the class.

The preventive step is obvious in hindsight: **when a reframe lands, ask which documents assert what it
changed, and fix all of them in one pass.** We had the grep for that — written for the retraction
checker — and used it once, on the narrow case, instead of on the reframe.

### 72a. Qualifications, as distinct from retractions

`src/check_retractions.py` now runs a second check against `QUALIFICATIONS.tsv`. The distinction
matters:

- a **retraction** must be marked **at the line**, because the claim is dead and a reader meeting it
  needs to know immediately. Window: six lines.
- a **qualification** qualifies a **whole document**, so a standing banner anywhere in the file
  satisfies it. The claim is still true; it needs context.

Five qualifications are registered: `WT_LFC`, `LWTP` and `not PARP4-dependent` each require
**PXD052802 or A549** somewhere in any file that uses them; `no stoichiometric partner` requires the
**signalling-modulation** context from §70; `no fitness coupling` requires the **conditional
phenotype** context.

### 72b. Tested both ways

Clean tree: **`OK: 5 qualified claims checked; every document asserting one carries its standing
context.`**

Planting a stray line — *"ANXA2 at WT_LFC +1.74, not PARP4-dependent"* — into a file with no
provenance is caught on **three patterns at once**, each naming what the document needs and which
section established it, and the checker **exits 1**. Restored, it exits 0.

### 72c. What this does and does not fix

It cannot tell that a reframe has happened, or decide what context a claim needs — both are judgement,
and both stay with the ledger. **It enforces that once a qualification is registered, no document can
assert the claim without it.** That is precisely the step that failed four times: not the thinking, but
the propagation.

Two mechanisms now, against twelve rules of judgement: one that a retraction stays visible at the line,
one that a qualification reaches every document. **Both exist because the same failure recurred after we
wrote the rule for it.**

## 73. The nucleotide pocket is published, it is not sealed, and the answer was in our own data directory

An agent was asked whether the SPFH-shoulder assignment and the ~~sealed~~ nucleotide pocket (**the
"sealed" characterisation is WITHDRAWN** - see 73b) are already
published. **Both halves of hypothesis A1 fall, and the fifth literature check is the worst of the
five.**

### 73a. The SPFH assignment: published in 2009, and we had the structure

**Tanaka et al., "The structure of rat liver vault at 3.5 angstrom resolution", *Science* 2009,
PMID 19150846 — PDB 4V60.** It reports the shoulder domain as structurally similar to the SPFH domain,
with DALI hits to **stomatin** and the **flotillin-2 band-7 domain**. **Our relatives list —
flotillin-1, flotillin-2, stomatin — reproduces the published DALI hits exactly.**

It is also a live database annotation on **UniProt Q14764**: a *"MVP shoulder"* domain feature at
residues 519-646, cross-referenced to **InterPro IPR036013 "Band 7/SPFH domain superfamily"**, **CATH
G3DSA:3.30.479.30 "Band 7 domain"** and **NCBI CDD cl19107 "SPFH_like"** at 480-604. Four 2025-2026
structure papers use "MVP's SPFH domain" as routine nomenclature. Grok's suspicion in audit 4 — that
the SPFH label was probably already in the structural literature — was correct.

One real distinction the agent drew: the homology is **structural (DALI/CATH), not sequence-detectable**
in human MVP. The single published attempt on sequence grounds (a 2019 bioRxiv preprint) found the
Band-7 signal in *bacterial* MVPs and reported **its absence in eukaryotic ones.**

### 73b. The pocket: published July 2025, by the authors of the dataset we spent the day on

**Lodwick JE, Shen R, Erramilli S, Xie Y, Roganowicz K, Ritchey S, Kossiakoff AA, Zhao M. "Structural
insights into the roles of PARP4 and NAD+ binding in the human vault cage." *Nature Communications*
2025;16:6724. PMID 40691181.**

Abstract: *"The structures reveal atomic-level details of the protein-binding interface, as well as
**unexpected binding sites for NAD+ and related nucleotides within the interior of the vault cage**."*
The pocket sits in MVP's SPFH domain behind a *"keyhole loop"*, is formed **between the SPFH domains of
two adjacent MVP monomers**, and **NAD+ and ADP are modelled in deposited coordinates** (9MXH, 9MXV).
Pocket residues are named: R504, K506, P508, H509, R511, L517, F522, P565, R437.

**This is the same group whose supplementary table we have been analysing all day** — the VM1/H6
synthetic antigen binding reagents of PXD052802 (§71). So the interactome we read and the structure we
hypothesised about are **one published paper**.

### 73c. "Sealed" is not just unpublished, it is contradicted

The agent searched Europe PMC and grep'd the full texts of five recent vault structure papers for
*occluded, sealed, buried, enclosed, inaccessible, cryptic* and **found no source describing the pocket
as sealed.** Three published statements run the other way:

1. It **opens into the lumen** — *"the binding site of NAD+ is a recessed pocket lined by basic
   residues"* on the interior wall.
2. A second group reads it as **solvent-accessible**: *"consistent with the idea that vault-associated
   components may require solvent access for activity."*
3. **The directionality is inverted.** An inter-subunit pocket between two MVP monomers **exists
   because the shell is assembled** — it is created by assembly, not sealed by it.

The nearest published occlusion element is **loop gating, not shell sealing**: NAD+ sits "behind the
keyhole loop", which is displaced on binding.

### 73d. The answer was in `data/raw/struct/` the whole time

| file | title in the mmCIF | deposited |
|---|---|---|
| `4V60.cif.gz` | *"The structure of rat liver vault at 3.5 angstrom resolution"* | **2008-10-24** |
| `9BW6.cif.gz` | *"Human Vault Cage in complex with PARP4"* | **2024-05-20** |
| **`11JB.cif.gz`** | ***"RNA Vault with ADPR bound (MVP/PARP4/TEP1 NADP sample)"*** | **2026-02-26** |

**4V60 is the Tanaka structure that established the SPFH assignment. 9BW6 is one of the Lodwick 2025
structures. And 11JB is a vault with ADP-ribose bound — 4,446 `AR6` HETATM records in the file.**

**We hypothesised an undiscovered nucleotide pocket while holding a nucleotide-bound vault structure
whose own title says so.** Every literature gate this project built looks for a control in the data;
the one check never run was reading the titles of the files already downloaded.

### 73e. What this does to the hypothesis list

- **A1 (nucleotide-sequestering buffer, 0.20) is withdrawn.** The pocket is published and the "sealed"
  premise is contradicted. What survives is **not a hypothesis but a published fact**: MVP binds NAD+,
  and *"PARP4 is not necessary for the interaction."*
- **A8 (sealed pocket as a ligand-gated waist latch, 0.12) is withdrawn** on the same grounds, though
  the published keyhole-loop gating is a real and adjacent mechanism.
- **A12 (the bare shell is the functional unit) is strengthened to ~0.45 and is now the clear leader.**
  The shell binds NAD+ **without PARP4** — a published, structurally-resolved function of MVP itself,
  which is precisely what A12 predicts and the strongest single piece of evidence for it.
- **A2 (TEP1 as a TIR NAD(P)ase) gains context rather than losing it.** The vault demonstrably
  concentrates NAD+ in its lumen; an NAD(P)-consuming enzyme on the same particle is a more coherent
  proposition with a published NAD+ reservoir than without one. Raised to ~0.25.
- **Five literature checks, five prior-art hits**, and this one found the prior art **inside our own
  `data/raw/` directory.**

## 74. Five checks, five hits: the project's founding premise was wrong

**Every literature check this project ran found prior art.** Not "most" — all five, and the ones we
were most confident about failed hardest:

| check | our claim | what was already there |
|---|---|---|
| 1 | TEP1 associates independently of PARP4 — **our top novelty item at 0.75** | ~25 years: MVP-only Sf9 vaults, TEP1-KO vaults intact, caps joining preformed shells |
| 2 | MVP ancestral in eukaryotes, lost in fungi/plants/Ecdysozoa | **Daly et al. 2013**, verbatim |
| 3 | the interactor readings | the pulldown is a **public deposit with its own analysis** of our comparison |
| 4 | stool proteomics cannot recover a vault — **our best-standing claim at 0.65** | the methods principle is published; only the vault application is ours |
| 5 | a sealed SPFH nucleotide pocket — **the foundation of our top-ranked hypothesis** | **Tanaka 2009** for SPFH, **Lodwick 2025** for the pocket, and the premise "sealed" is contradicted |

### 74a. The premise was the error, not the individual claims

Paper 1 opens: *"The vault ribonucleoprotein has resisted functional assignment for forty years."* We
built forty registered tests on the assumption that we were working a neglected problem with a thin
literature.

**The literature is not thin.** In the last two years alone the agent surfaced **four 2025-2026
structure papers** — Lodwick's PARP4/NAD+ cryo-EM series, a membrane-association cryo-ET study, a
flexibility study with MD, and a *Sci Adv* paper on the cap — plus a vault structure from human brain,
and a functional literature running from *Nat Commun* 2019 on obesity through 2024 influenza work to
*Nat Commun* 2025 on mitophagy. **An active structural group is publishing on exactly the questions we
were asking, in exactly the window we were asking them.**

So the forty-year framing is true about *consensus* and false about *activity*, and we used it as
licence to stop looking. **Every one of the five hits follows from that single misjudgement**, which is
a more useful diagnosis than five separate oversights.

### 74b. What the honest contribution looks like

Of the five checked claims, the surviving fragments share a shape: **the general principle was always
already known, and only the vault-specific application was new.** Stool-prep bias by cellular
compartment is published; nobody applied it to a megadalton particle. Co-fractionation sensitivity
limits are known; the MVP-TEP1 noise-floor comparison may not be. That is a real but modest kind of
contribution, and it is the accurate description of what two days of reanalysis against an active
forty-year literature can produce.

**The six unchecked candidates should now be read as probably-known rather than provisional.** On a
five-for-five base rate that is the correct prior, and stating it is more useful than leaving ten
numbers in a table.

### 74c. What survives all of it

The methodological record. **Thirteen house rules and two enforced mechanisms, every one of them
written because the project broke the thing it describes** — one-way gates, a control with no power to
fail, a refusal band wider than its estimator, three criteria that measured the wrong quantity, a
degenerate matching scheme read for two sections, the same indexing bug three times, one correction
propagated through four documents one at a time, and two gates that passed vacuously on paraphrase.

**And one well-controlled negative that no literature check has touched:** MVP has no stoichiometric
partner complex beyond PARP4 and TEP1, across every instrument available, with calibration gates
passing. §70 relocated what that means — it is consistent with the published transient-signalling
function rather than evidence against function — but the result itself still stands, and it is the one
piece of biology here that was produced rather than rediscovered.

## 75. Usefulness to a stranger: ours against Grok's, and Grok wins most of it

**This section lives in [`USEFULNESS.md`](USEFULNESS.md), not here.** It was written there and numbered
§75 in the ledger (#336-340) and cited as "RESULTS.md §75" from `CALIBRATION.md`, which left **§75 as
the only hole in this file's numbering** and nine dangling references pointing into it. The stub exists
so the numbering is contiguous and the citations resolve.

**What is there, in one paragraph.** Both assessments were written independently, ours committed at
21:36:01 before Grok was asked. **Finding 1 (CFdb MVP-TEP1) is rank 1 for both; the interferon regulon
is top-three for both; those are the only two items both call useful unqualified.** Grok returned **six
zeros**, including our rank 2 (stool proteomics - *"nobody running standard stool proteomics is trying
to recover vaults; they discard that pellet on purpose"*, i.e. **the finding has no actor**) and our
rank 4 (whose safe reading is ordinary multi-subunit practice and whose interesting reading invites a
tissue swap that co-ranking cannot license). It caught that **three-decimal half-lives are false
precision against a 22.6% CV bar**, about +/-15 h on the MVP estimate. It **won the argument we most
wanted to win** - the house rules are not the most useful output, because *"finding 1 is a number a
stranger can put in a test harness; the rules, as specified here, are not."* It found two exports we
missed (van der Post's intracellular tag classifies nothing at 79% of both proteomes; the unrun 2-df
Wald design ports to proteasome, ribosome and nuclear-pore turnover groups) and a better generalisation
of finding 1 as a **discordant edge** for interactome integrators. Its strongest argument was that
**usefulness of a reanalysis is zero while the numbers are incredible** - conceded conditionally on
findings 1 and 3 having been computed after the gates, which was checked and holds.

## 76. The "signalling modulator" evidence is one group's programme, not convergent independent work

Verified citations were fetched for the six papers behind E1. **Both of our framings of that evidence
were wrong, and the authorship count is the reason.**

### 76a. Verified citations

| mechanism | citation |
|---|---|
| IKK-NF-kB, obesity & atherosclerosis | **Ben J, Jiang B, Wang D, … Wiemer EAC, Xu Y, Chen Q.** *Nat Commun* 2019;**10**(1):1801. PMID 30996248 · PMC6470148 · 10.1038/s41467-019-09588-x |
| calcineurin-NFATc1, osteoclastogenesis | **Yuan L, Zhao N, Wang J, … Wiemer EAC, Chen Q, Mao Y, Ben J, Ma J.** *Theranostics* 2021;**11**(15):7247-7261. PMID 34158848 · PMC8210610 · 10.7150/thno.58468 |
| Fas-mediated apoptosis, bone loss | **Wang R, Yang Y, Zhang Z, Zhao N, Wiemer EAC, Ben J, Ma J, Yuan L.** *Cell Death Dis* 2023;**14**(9):604. PMID 37704623 · PMC10500014 · 10.1038/s41419-023-05928-4 |
| **adaptive immunity, influenza A** | **Ma C, Luo C, Deng F, … Zeng X, Zhu Y, Liu S.** *Biochim Biophys Acta Mol Basis Dis* 2024;**1870**(7):167441. PMID 39069011 · **no PMCID** · 10.1016/j.bbadis.2024.167441 |
| Parkin-mediated mitophagy, vascular | **Jiang B, Bai F, Hu Y, … Yang Q, Ben J, Chen Q.** *Nat Commun* 2025;**16**(1):4365. PMID 40348769 · PMC12065841 · 10.1038/s41467-025-59644-y |
| STAT3, lung cancer | **Bai H, Wang C, Qi Y, … Xu Y, Ben J, Chen Q.** *BMC Cancer* 2019;**19**(1):454. PMID 31092229 · PMC6521381 · 10.1186/s12885-019-5665-6 |

### 76b. It is one group, not six

Counting shared authorship across the six:

| author | papers |
|---|---|
| **Jingjing Ben** | **5 of 6** |
| Junqing Ma | 4 of 6 |
| Qi Chen | 4 of 6 |
| Qing Yang, **Erik A C Wiemer**, Hanwen Zhang, Xiaoyu Li, Bin Jiang, Xudong Zhu, Hui Bai | 3 of 6 each |

Pairwise overlap is extreme: *Nat Commun* 2019 and *BMC Cancer* 2019 share **twelve** authors;
*Nat Commun* 2019 and *Nat Commun* 2025 share **nine**; *Nat Commun* 2025 and *BMC Cancer* 2019 share
**eight**; *Theranostics* 2021 and *Cell Death Dis* 2023 share **five**.

**Exactly one paper shares no author with any other: the influenza study** (Ma, …, Liu — a different
institution entirely).

**So E1 rests on one research programme spanning five papers — metabolism, bone twice, vascular, lung
cancer — plus one genuinely independent replication in a sixth tissue.** Erik Wiemer, a long-standing
vault researcher, appears on three as a collaborator.

**This retracts a claim we made explicitly**: that the evidence was *"six-plus independent groups…
harder to dismiss than one result."* It is not. **One group's multi-tissue programme can share a mouse
line** — `Mvp-/-` and `Mvp f/f Lyz2-Cre` recur across the papers — **reagents, antibodies, analytical
habits, and a systematic error.** The convergence we were impressed by is largely internal.

**What survives:** the influenza paper is an independent group reaching a compatible conclusion in an
unrelated tissue, which is real but is **one replication, not five.**

### 76c. And "every phenotype is conditional" has a counterexample

The agent flagged it rather than letting it pass. ***Theranostics* 2021 reports an osteoporosis-like
phenotype in unchallenged knockouts**: *"Mvp-/- and Mvp f/f Lyz2-Cre mice both exhibited
osteoporosis-like phenotypes."* The challenge models in that paper — ovariectomy and calvaria-adjacent
LPS — are used for the **overexpression** arm, not the knockout.

So the correct statement is **five of six, not all six.** And whether the bone phenotype is genuinely
unconditional turns on the age at which the baseline micro-CT was done, which needs the figures rather
than the abstract.

**One further distinction:** the lung-cancer paper is **shRNA knockdown plus xenograft**, not a knockout
mouse — *"knockdown of MVP in LLC cells promoted xenografted lung cancer formation"* — so it is a
different class of evidence from papers 1-5 and should not be counted alongside them.

### 76d. What this does to E1

**Downgraded from "established by convergent independent evidence" to "one group's programme with one
independent replication."** That is still real evidence — five papers in *Nat Commun*, *Theranostics*,
*Cell Death Dis* and *BMC Cancer* are not nothing — but it is a different epistemic object, and anyone
citing "MVP is established as a signalling modulator" should know the convergence is mostly one lab's.

**And the error is ours in a familiar shape.** We asserted independence without checking authorship —
the same move as asserting novelty without checking the literature, five times. **The check costs one
author-list fetch.**

## 77. The retraction gate did not cover `results/`, and the obvious fix inverts the outcome

Reading four stored logs surfaced **`ENRICHMENT RATIO = 2.48x`** in `results/donor_and_k.log` - a
**registered retraction pattern** (§64b: buggy frame order, correct value 2.86x). The gate scans five
documents. It never looked at `results/*.log`, which are **in the public repository**.

### 77a. Six hits, three of them real

Running the registered patterns over `results/` by hand:

| file:line | pattern | verdict |
|---|---|---|
| `donor_and_k.log:5` | `2.48x` | **GENUINE** - the pre-fix TEST 1 value |
| `export_test.log:5` | `0.184` | **GENUINE** - `GOCC_RIBOSOME, full matching, p=0.1835`, which the line itself cross-checks against "§51 gave p=0.184" |
| `export_test.log:9` | `0.0526` | **GENUINE** - under the header `PRIMARY, abundance+length+charge matched`, i.e. the degenerate matcher |
| `continuous.log:16` | `0.174` | coincidence - a `null_sd` that happens to equal 0.174 |
| `models.log:29` | `0.0526` | coincidence - a confidence bound in a model coefficient array |
| `sc_kim.log:38` | `0.184` | coincidence - the prefix of a Spearman rho, `0.1842505648549325` |

**Half the hits are noise**, because the patterns are bare decimals and logs are dense with unrelated
floats.

### 77b. The obvious fix makes it worse, and this is the point

Add `(?!\d)` so a pattern stops matching the prefix of a longer float. Then:

- `0.184` no longer matches `0.1842505…` — **kills the coincidence**, good;
- but `0.0526` no longer matches `p=0.05261473…` — **kills a GENUINE hit**;
- and `0.0526` still matches `[…, 0.0526, 6]` — **keeps the other coincidence**.

**The tightening inverts the outcome: it suppresses the real violations and retains the false ones.**
A prose instrument does not become a numeric instrument by tightening it, and we would have shipped the
change believing it an improvement had we not enumerated the six cases first.

### 77c. What we did instead

**The two superseded logs are stamped**, originals preserved verbatim below the banner - 19 and 24
lines intact, `ENRICHMENT RATIO = 2.48x` still on the page at its new line 28. `donor_and_k.log` names
all four corrected figures (65→35 cells, 189→129 donors, 0.772→0.891, 2.48x→2.86x) and records that
**TEST 1's verdict survives the correction while TEST 2's does not** - the bias is larger, not smaller,
so §51's control is still invalid, but the `COMPLEX-LIKE` call dies to §64c's `(hits/k)/fold`
constancy. `export_test.log` names the three voided p-values **and the gate on its own line 6**, the
positive control that could not have failed because the same degenerate scheme computed it.

**And the gate now checks a tractable property instead of an intractable one:** a log known to be
superseded must say so at the top (`SUPERSEDED_LOGS` → banner). **Self-tested both ways** - strip the
banner, exit 1; name a log that does not exist, exit 1.

**One further note on the testing.** The first negative test read `$?` after piping to `tail`, so it
reported `tail`'s status and printed `exit=0` for a run that had crashed with a `NameError`. **That is
the vacuous-pass shape occurring inside the test of a gate built to catch vacuous passes** - caught only
because the traceback was visible above it.

## 78. The sweep that followed §77 found the worst-placed error in the repository

Having stamped two logs, the obvious next question was whether other file classes carried retracted
values. Sweeping **every tracked non-document file** returned **145 hits** - and the distribution is
§77b's prediction confirmed at scale.

### 78a. 145 hits, four real

**Nearly all are coincidence.** `results/surface_residues.csv` matched four times on solvent-accessible
fractions; `prot_enrichment_*.csv` and `coloss_mvp_enrichment.csv` on other GO terms' q-values;
`ccle_metabolomics_mvp.csv` on metabolite correlations; `kim_*.csv` on per-patient fractions. **The
funniest false positive is `src/check_retractions.py` itself**, whose new comment explaining that
`0.184`, `0.0526` and `0.174` collide in numeric files **contains those three literals and matches its
own patterns** - as does house rule 14's text in `CONTRIBUTING.md`.

**And a large class is legitimately immutable.** `grok/` and `channel/` transcripts carry retracted
values because that is **where they were retracted**; the two pre-registrations carry them because a
pre-registration written before the data **must not be edited afterwards**. Annotating either would
falsify the record.

**Confirming rule 14 from the other side:** a sweep of 145 hits yielded **four** actionable items. Had
we extended the gate to these files, it would have fired constantly and been switched off.

### 78b. The two machine-readable twins

`results/donor_and_k.json` holds `"ratio": 2.481321147987815`, `"n_cells": 65`, `"n_donors": 189` -
the pre-fix values in machine-readable form, **and the `2.48x` pattern never matched it because JSON
has no `x` suffix.** `results/export_test.json` holds `"p": 0.18352908235458823` and `"gate1": true`,
the latter being the control that could not have failed. **We stamped the logs and left their twins**,
which is the propagation failure one file over. Both now carry a `_superseded` key, and the check
covers all four files, self-tested by deletion.

### 78c. The `LICENSE` suggested citation carried two withdrawn claims

> *Syfert, G. W. (2026).* **One assembly, three lifetimes, and a sealed nucleotide pocket:** *a
> pre-registered reassessment…*

**"Three lifetimes"** was retracted at §61b - the compatibility was never tested - and the paper's own
title was corrected for it. **"Sealed"** was contradicted at §73 - the pocket is lumen-facing,
inter-subunit, and created by assembly. **The `LICENSE` was never updated for either**, so the single
most copy-pasted line in the repository carried both.

### 78d. And `sealed` was never registered, so it survived in the paper's own title

§73 withdrew hypotheses A1 and A8 on the ground that the pocket **is not sealed**, and **never added
`sealed` to `RETRACTIONS.tsv`** (the file had zero matches for it). The word therefore survived in:

- **the title of Paper 1** - *"One assembly, a sealed nucleotide pocket, and one question…"*;
- **Paper 1's "what survives unchanged" list**, the strongest claim-position in the paper;
- the README's findings list;
- three RESULTS tables and the README's prior-art table, **unmarked**.

Both patterns are now registered, and the title is changed a second time:

> **One assembly, no stoichiometric neighbourhood, and an instrument that cannot see a known subunit**

**Twice the title headlined something that was either not ours or not true** - "three lifetimes"
(untested) and "a sealed nucleotide pocket" (published by Lodwick 2025, and not sealed). This one
headlines the well-controlled negative and the calibration finding, **which are both ours and both
survive.** Paper 1 now carries a standing "Title history" note saying exactly that, and the `LICENSE`
citation matches.

### 78e. A tight marker vocabulary fails safe; a loose one fails open

Registering `sealed` made the gate fire on **four occurrences whose surrounding text genuinely does
retract it** - §73's own opening sentence, two ranking tables, and the README's prior-art row whose
adjacent cell reads *"the SPFH assignment is Tanaka et al., Science 2009."* None used vocabulary in
`MARKERS`.

**The fix was to annotate the four, not to broaden `MARKERS`** - and that choice is the whole lesson.
**Broadening the marker list makes every future bare claim easier to excuse**, which is the
vacuous-pass direction (#325, #327). **A narrow marker list produces false alarms you fix by
annotating, which is safe.** Prefer the gate that cries wolf.

## 79. The last test produced exactly the number predicted, and the gate forbids using it

The dN/dS test registered at commit `e8997c8` (22:32:04, before any value existed) **failed its own
positive-control gate.** Per the registration, *"if any of the three fails, the result is UNINFORMATIVE
and MVP's value is not interpreted."*

### 79a. The gate, evaluated mechanically

| clause | result | detail |
|---|---|---|
| 1. all four essential controls median dN/dS < 0.20 | **FAIL** | **RPL7 returned no unsaturated pair at all**, so it has no median to test |
| 2. lowest relaxed control > highest essential control | PASS | relaxed min **0.2398** (MX1) vs essential max **0.0740** (GAPDH) |
| 3. >= 3 unsaturated pairs for every gene reported | **FAIL** | **eight of ten genes fell short**; TEP1 and APOBEC3G returned nothing |

### 79b. And this is the part that matters

**MVP was the only gene in the panel that satisfied clause 3.** Three of three pairs unsaturated -
mouse (dS 0.586), chicken (dS 1.141), *Xenopus* (dS 1.457) - with a median

**dN/dS = 0.1431**

The registered primary prediction was *"below 0.15 and inside the range of the essential-gene
controls."* **0.1431 is below 0.15.** It is the cleanest-looking number the project has produced, it
lands inside the prediction written before the data existed, and it is the one result we were most
hoping for.

**It is uninformative and we are not interpreting it.** The controls that would tell us whether the
pipeline can distinguish an essential gene from a drifting one **did not return enough data to say**,
and a subject value is worth nothing without them. A number that agrees with your prediction while its
controls are missing is **exactly** the situation every rule in `CONTRIBUTING.md` exists to govern.

### 79c. Why it failed - diagnosis, not interpretation

Three distinct causes, none of them about MVP:

- **16 "no orthologue".** *Ciona* accounts for 10 - **it is served by Ensembl Metazoa, not the main
  REST endpoint we queried**, so the one non-vertebrate retainer in the design returned nothing for any
  gene. A registry error, ours. **APOBEC3G accounts for 5, and that one is real biology**: APOBEC3G is
  primate-restricted, so there is no mouse, chicken or fish orthologue to find. **We registered a
  control that cannot exist in the species set** - which is house rule 7, the vacuous control, committed
  again in the very registration that cites the rule.
- **9 "dS unusable"** - NG86 returns -1 where it cannot solve, at the deep pairs.
- **5 timeouts** - transient, recoverable.

### 79d. The design fault underneath

**The species set was too deep for the control genes.** At mouse distance every gene computed cleanly
(dS 0.45-0.92, all unsaturated). The controls are short - RPL7 246 codons, GAPDH 333, TUBB 445 - and
short genes saturate at synonymous sites by chicken and *Xenopus*, while **MVP at 861 codons did not**.

So the registration chose a depth that answers the question we care about ("the lineages that kept it",
~600 My) and a saturation rule honest enough to refuse saturated pairs, **and those two choices are
incompatible for short genes.** Nothing noticed until the gate was evaluated. The question survives;
this instrument, as specified, cannot reach it.

### 79e. What this costs, stated now

**MVP's value has been seen.** Any repair run is therefore **not blind**, and must be labelled that way
permanently, however the numbers land. House rule 5 forbids iterating a method until it passes; fixing
orthologue coverage is not the same as tuning a result, but **the distinction does not restore
blindness**, and no later run gets to be described as a registered test of a prediction whose answer
was already on the screen.

### 79f. Correction to 79c: the diagnosis was itself unverified

Ensembl began returning **503 Service Unavailable** when the failures were being diagnosed - the API
rate-limits under sustained load, and the run had just made fifty calls. That matters backwards:
**`src/dnds.py` recorded any response lacking the expected structure as `"no orthologue"`**, which
**conflates a true biological absence with a server that did not answer.**

So §79c's breakdown - *"Ciona accounts for 10, a registry error of ours"* - is **asserted, not
established.** The APOBEC3G claim stands on independent grounds (it is primate-restricted as a matter
of published biology, which needs no API call). The *Ciona* claim and the sixteen-count do not: both
are consistent with a rate-limited endpoint, and **the instrument that produced the diagnosis cannot
tell the two apart.**

**This is the fourth time in this project that an error-handling branch quietly merged two outcomes**
and the merged category was then read as the informative one. The repair below classifies HTTP status,
empty-but-valid responses, and true absences separately, because a diagnosis that cannot fail is not a
diagnosis.

## 80. The repair failed too, on four clauses, and two of the causes were mine again

| clause | result |
|---|---|
| 1. four essential controls, >=3 pairs, median < 0.20 | **FAIL** - GAPDH had 2 mammal pairs |
| 2. three relaxed controls, >=3 pairs, lowest > highest essential | **FAIL** - ZP3 returned nothing at all |
| 3. every gene >= 3 unsaturated mammal pairs | **FAIL** - MVP, TEP1, PARP4, GAPDH, ZP3 short |
| 4. no absence inferred from a non-200 | **FAIL** - **MVP lost rat, dog, cow, macaque, opossum and chicken to HTTP errors** |

### 80a. Clause 4 earned its place

It was added in the repair after §79f found the first script merging server failures into
`"no orthologue"`. It immediately caught **36 HTTP failures across 90 calls** - and every one of MVP's
missing mammals was one of them. **Without clause 4 this run would have reported MVP as absent from
five mammals and been believed.**

### 80b. All 36 were HTTP 500, and the retry logic skipped exactly that code

`src/dnds2.py` retried on `(429, 503, 504)`. **Every failure was a 500**, which fell through to an
immediate give-up with **no retry at all**. So the run that was built to survive throttling was felled
by a code it did not list, and the sleep-and-backoff machinery never fired once.

### 80c. And TRIM5 was a second vacuous control

The valid-but-empty results - the ones clause 4 certifies as genuine absences - include **TRIM5 absent
from dog, opossum, chicken, *Xenopus* and zebrafish.** That is correct biology: TRIM5alpha is
primate-restricted. **Having dropped APOBEC3G for exactly this reason (#360), we replaced it with
another primate-restricted gene and did not check.** House rule 7, third occurrence, in consecutive
registrations.

Two genuine absences are worth keeping, since clause 4 vouches for them: **TEP1 has no one-to-one
mouse orthologue in Compara**, and **RPL7 none in mouse or rat** - which is why RPL7 failed clause 1 in
the first run. Those are facts about the resource, not about vaults.

## 81. Three runs, three gate failures. The question is recorded as unreachable and we stop.

The third attempt was capped in advance: *"If the gate fails again, the question is recorded as
UNREACHABLE WITH THIS INSTRUMENT and the project stops asking it."* **It failed. We stop.**

### 81a. Two clauses passed decisively, two failed

| clause | result |
|---|---|
| 1. four essential controls, >=3 pairs, median < 0.20 | **PASS** - RPL7 0.0449, ACTB 0.0073, GAPDH 0.0771, TUBB 0.0031 |
| 2. three relaxed controls, >=3 pairs, lowest > highest essential | **PASS** - **0.2166 > 0.0771**, clean separation |
| 3. **every** reported gene >= 3 unsaturated mammal pairs | **FAIL** - TEP1 returned 2 |
| 4. no absence inferred from a non-200 | **FAIL** - 14 errored calls |

**The one thing that is now established, and it is about the controls, not about MVP:** NG86 on
Compara CDS alignments **does** separate essential genes from rapidly evolving ones across mammals -
**0.003 to 0.077** for ACTB, TUBB, RPL7, GAPDH against **0.217 to 0.558** for MX1, CD4, FCGR2B. The
instrument works. That is a statement about ten control pairs and it stands on its own.

### 81b. What failed, precisely

**Clause 3 failed on TEP1 alone.** TEP1 is a 290 kDa protein, and the Compara `sequence=cds` query for
it **failed on 11 of 13 species** - seven timeouts, one 503, two 500s. A large CDS appears to exceed
what that endpoint will serve. Not biology; an endpoint limit.

**Clause 4 failed on 14 errored calls**, 11 of them TEP1's and **3 of them MVP's** (mouse, macaque,
pig - all timeouts).

### 81c. The number, recorded and not interpreted

MVP returned **7 unsaturated mammal pairs, every one `ortholog_one2one`**, 839-890 codons each:

| species | dN | dS | dN/dS |
|---|---|---|---|
| rat | 0.0512 | 0.6025 | 0.0850 |
| rabbit | 0.0523 | 0.5007 | 0.1045 |
| dog | 0.0492 | 0.4569 | 0.1077 |
| opossum | 0.1285 | 1.1489 | 0.1118 |
| horse | 0.0441 | 0.3690 | 0.1195 |
| sheep | 0.0571 | 0.4714 | 0.1211 |
| cow | 0.0581 | 0.4671 | 0.1244 |

**Median 0.1118, range 0.0850-0.1244.** Seven species, one-to-one orthologues, a spread of 0.04.

**It is not interpreted. It does not enter the hypothesis ranking. Nothing above it changes.**

### 81d. Why we are refusing a number this clean, stated plainly because it is the whole point

**Strip TEP1 out and the gate passes.** The two clauses that test whether the instrument can tell an
essential gene from a drifting one **both passed**. MVP's own seven pairs are one-to-one, long, and
tight. Clause 3 failed on a different gene's server errors, and clause 4 counted errored calls rather
than actual inferred absences - and we are not, in fact, inferring that MVP is absent from mouse.

~~**A reasonable person would report 0.1118 with caveats. That is exactly what house rule 5 forbids.**~~
**REVERSED, §84b.** Grok audit 008: *"a gate binds inference only when the failed clause is about
that estimator."* Clauses 3 and 4 were TEP1's pair count and a tally of HTTP timeouts - **neither
enters the sampling distribution of MVP's omega.** 0.1118 stands as strong purifying selection. The
reasoning below is preserved because the *shape* of it is still right; it was **applied to the wrong
clauses.** HOUSE RULE 15.

The clause was written by us, the check was implemented by us, and the check says FAIL. Arguing *now*
that clause 4 "really meant" something narrower - having seen which clauses failed and having seen that
the subject's number looks good - is **the same move as §41's reinterpretation of a failed kill**, which
cost this project a withdrawn section and a house rule. **A gate you renegotiate after reading the
result is not a gate.** Three runs were registered, three failed, the cap was set before the third, and
the honest outcome is that **we do not get to know this.**

### 81e. What a real version of this test needs

Stated so the next person does not repeat it: a **local Ensembl/Compara dump or mirror**, because the
public endpoint will not serve a large CDS reliably; **TEP1's CDS fetched directly** rather than through
homology-with-sequence; and for the question that actually matters - selection across the ~600 My of
lineages that kept MVP - **a codon model on a phylogeny, not pairwise NG86**, which saturates exactly
where the interesting comparisons live.

~~**The conservation paradox is where the article series left it.**~~ **SUPERSEDED, §84b: it has an
answer, and it is the uncomfortable one we predicted - where MVP is kept, it is kept under strong
purifying selection.** Forty-odd gated tests, three
registered attempts at the one question both Rome's rubric and the series named, and the answer is still
*"I don't have an answer."*

## 82. MVP is not built to be banked. It is built to be opened and not to rust.

Registered at `25c270b` before any value existed, prompted by Graham's chair/furniture line and his
question **what would the chemical composition be useful for?**

### 82a. The gate passed, and the prediction died

| | |
|---|---|
| clause 1: >=2 of 3 reserve proteins above the proteome mean on N/residue | **PASS** - CSN1S1 +0.83, FTL +0.29 (ALB -0.35) |
| clause 2: >=2 of 3 structural proteins not above +1 SD | **PASS** - all three (CLTC -0.09, ACTB -0.83, TUBB -0.56) |
| clause 3: every control found by name, counts reported | **PASS** - 20,129 proteins >=50 aa from 20,429 Swiss-Prot entries |

**MVP nitrogen/residue z = +0.29.** Registered prediction was **>= +1 SD**. **NOT MET. Kill condition
fires.** The simplest version of the raw-material-reserve idea gets **no support from composition**, and
it is the first gate this project has passed on the first attempt.

### 82b. And the composition argues the other way, not merely weakly

**MVP is sulfur-poor: z(S) = -1.20.** 0.0157 S atoms per residue against a proteome mean of 0.0483 -
roughly **one third**. Cysteine z = **-0.76**, methionine z = **-1.18**, both among its five most
depleted residues.

That matters for the storage reading specifically. ~~**Met is essential and both Met and Cys are among the most metabolically expensive residues to
make.** A protein banking scarce material would *include* them. MVP avoids them. So composition does
not just fail to support storage - **it points away from it.**~~ **WITHDRAWN, §84c.** Grok: *"low
Met/Cys is what casein-like storage looks like, and you never showed the reserve controls are
sulfur-rich."* **We invented a second hypothesis after the fact and scored it against controls never
tested for it.** The depletion is real and **understated** (0.33x the mean sulfur density, z near -2 in
a long-protein bin); only the *inference* is void.

### 82c. What the composition does look built for

Two signatures, both consistent with things already established about the particle:

> **Better statistic available, §85a.** The z-scores below are superseded by direct counts and a
> within-particle contrast that needs no sd: **MVP has 5 Cys in 893 residues (0.56%) against a proteome
> median of 2.05%, while TEP1 (2.13%) and PARP4 (2.15%) are proteome-typical.** The depletion is
> specific to the shell subunit, with the caps as the closest available comparison.

**Cysteine- and methionine-poor.** A 78-mer that must open and close at a waist **cannot afford
disulfide cross-links**, and a particle that leaves the cell as a free, unwrapped object in an
oxidizing extracellular environment - which Jeppesen et al. 2019 showed it does - would be at risk of
random disulfide formation and methionine oxidation if it were sulfur-rich. **Redox-inert, reversibly
openable.**

**Valine-enriched at z = +2.16**, the single largest deviation in the protein and far beyond anything
else. Val is beta-branched and beta-sheet-favouring, and MVP's wall is built from repeated beta-sheet
repeats. **This is what a beta-rich structural shell looks like.**

### 82d. The novelty question, asked this time instead of assumed

**The Cys/Met-poor reading is NOT claimed as new.** Five novelty claims in this project produced five
prior-art hits (§74), and the lesson was that an absence of consensus is not a thin literature. A
compositional observation about a protein solved four times by cryo-EM is **exactly** the kind of thing
a structural paper says in passing. **It needs a literature check before anyone repeats it**, and that
check is logged as outstanding rather than performed and forgotten.

### 82e. Where this leaves the chair

Graham's framing was that a cell making chairs might eventually want to sit down - that the vault could
be built ahead of a need, its material borrowed back later. **Composition refuses the material half of
that.** The shell is not a nitrogen bank and not a sulfur bank, and it is built out of the cheap
residues rather than the dear ones.

**It does not touch the timing half.** "A growing cell doesn't have any; a matured cell produces them"
is a claim about expression against differentiation state, it is **testable with data already in
`data/raw/devel` and `data/raw/tissue`**, and it is untested here.

## 83. The chair gets built as the organ matures. The timing claim is confirmed; two others are not.

Registered at `7c82d9c` before any value was read.

### 83a. TEST A - gate PASSED, prediction MET in all seven organs

Spearman rho of log1p(RPKM) against developmental stage rank, Cardoso-Moreira E-MTAB-6814, 297 samples:

| gene | Brain | Cerebellum | Heart | Kidney | Liver | Ovary | Testis | neg |
|---|---|---|---|---|---|---|---|---|
| MKI67 | -0.931 | -0.925 | -0.693 | -0.826 | -0.283 | -0.657 | -0.726 | 7/7 |
| TOP2A | -0.948 | -0.924 | -0.592 | -0.781 | -0.401 | -0.196 | -0.550 | 7/7 |
| PCNA | -0.845 | -0.585 | -0.604 | -0.685 | -0.266 | -0.041 | -0.626 | 7/7 |
| CCNB1 | -0.812 | -0.880 | -0.760 | -0.843 | -0.369 | +0.229 | -0.813 | 6/7 |
| **MVP** | **+0.829** | **+0.848** | **+0.649** | **+0.789** | **+0.663** | **+0.760** | **+0.470** | **0/7** |
| TEP1 | -0.641 | +0.580 | -0.546 | -0.358 | -0.309 | -0.797 | -0.535 | 6/7 |
| PARP4 | -0.718 | -0.843 | -0.227 | +0.087 | -0.117 | +0.000 | -0.442 | 5/7 |

> **Note on one number in that table.** TEP1's Liver value is **-0.309**, which collides with a
> registered retraction pattern (§63's void three-way matched residual). **It is a coincidence** - this
> is a Spearman rho against developmental stage, computed by `src/chair.py`, unrelated to the degenerate
> matcher. The gate flagged it and **we annotated rather than loosening the pattern**, which is house
> rule 14 and §78e: prefer the gate that cries wolf.

**Gate: all three clauses PASS.** Proliferation markers fall in 6-7 of 7 organs; housekeeping |rho|
(ACTB 0.678, GAPDH 0.271) sits below the proliferation median of 0.689; all nine genes resolved by ENSG
and found.

**MVP rises in 7 of 7 organs, median rho +0.760.** It is **the only gene in the panel positive in every
organ.** Graham's prediction - *"a growing cell doesn't have any, but a cell that is fully matured
produces them"* - **is confirmed at the transcript level, on a registered direction, under a passing
gate.** The first positive prediction this project has confirmed this way.

**Caveat that strengthens it rather than weakening it:** ACTB also declines in 7/7 at |rho| 0.678, so
this dataset carries a broad downward drift. MVP moves **against** that drift, not with it. GAPDH at
0.271 shows the drift is not uniform.

### 83b. The thing nobody asked about: the shell rises while the caps fall

**MVP is positive in 7/7. TEP1 is negative in 6/7. PARP4 is negative in 5/7.**

Under a single program for a single particle, the three subunits should track. **They move in opposite
directions across development in nearly every organ.** ~~That is independent transcript-level evidence for the project's top-ranked hypothesis (**0.45**: the
bare shell is the functional unit and the caps are optional), and it was not what the test was designed
to find.~~ **WITHDRAWN, §84f.** TEP1 is **reversed in cerebellum (+0.58)**, and PARP4's "5/7" counted
kidney +0.087, liver -0.117 and ovary 0.000 as directional; **at |rho| > 0.3, PARP4 keeps three of
seven.** What survives is weaker: MVP and TEP1 have opposite signs in most organs, which no global
scale factor can produce - but which is also what class membership looks like when thousands of genes
fall and the complement rises.

### 83c. TEST B - gate PASSED, prediction REFUSED

HPA consensus, median nTPM. Gate passes: MKI67 0.1 vs 5.8 and TOP2A 0.7 vs 27.8, both far higher in the
proliferative set, so the sets separate on proliferation as required.

**MVP: post-mitotic 34.0 vs proliferative 51.2.** **Higher in proliferative tissue. Prediction NOT
MET.**

**The two tests disagree and both gates passed, so the disagreement is real.** They are different
contrasts: **A is within-organ across developmental time**, **B is between-tissue in adults.** MVP
rises as a given organ matures, and separately, adult high-turnover tissues carry more of it than
post-mitotic ones. Note that B's proliferative set - bone marrow, testis, small intestine, skin - are
also the **barrier and immune-rich** tissues, and MVP is interferon-inducible, so B may be reading
immune or epithelial content rather than proliferation. **Not resolved here.**

So: **"matured cells produce them" is right about developmental time and wrong about adult tissue
type.**

### 83d. TEST C - gate passed after a ranking bug, and the threshold I registered was wrong

The first run failed gate C1 because local alignment returned **6- to 8-residue perfect matches** that
outranked the true paralogue - ACTG1 at 98.9% over 375 aa came **second** to VKORC1 at 100% over 6 aa.
A sorting fault, mine. **The gate aborted before MVP's result printed, so the repair was still blind
for the subject**, which is recorded because §79e established that a repair after seeing the subject's
value is not.

Fixed: controls now pass decisively - **ACTB -> ACTG1 98.9% / 375 aa**, **TUBB -> TUBB4B 97.7% / 443
aa**.

**MVP's only above-threshold hit: GAS2L1, 28.7% identity over 251 aligned residues.**

Formally the registered prediction (>=20% over >=200 aa) is **MET**. **Substantively the threshold was
badly chosen, and the controls prove it:** real paralogues in this method score **97-99%**. MVP's best
is **28.7%**, against a cytoskeletal crosslinker with no structural relationship to a vault. And
TEP1's best hits - CIAO1, SEC13, GOLGA2, SPAG5, all **WD40-repeat proteins**, which TEP1 also has -
show exactly what this method returns at that level: **domain-level coincidence, not paralogy.**

**So TEST C is uninformative about the mirror-image idea**, not because the data refused it but because
**we set a floor that admits twilight-zone noise.** The honest statement is that the test as registered
cannot distinguish a paralogue from a coincidence, and the 70-point gap between the controls and MVP's
best hit is the evidence for that. **We are not converting it into "MVP is single-copy"** - that would
be reading a conclusion out of a test we have just declared unfit.

### 83e. Where the chair stands

| claim | status |
|---|---|
| raw-material reserve | **DEAD** (§82) - not N-rich, sulfur-poor, avoids the expensive essential residues |
| **"matured cells produce them"** | **CONFIRMED** for developmental time, 7/7 organs, gate passed |
| same claim, adult tissue type | **REFUSED** - higher in proliferative tissue, gate passed |
| reversible assembly | **CONSTRAINED** - co-translational templating means disassembly cannot be assembly reversed |
| mirror-image partner | **UNTESTED** - our threshold was unfit; needs a proper profile search |
| viral decoy | **UNTESTED** - needs infection time courses we do not have |

**Standing caveat (§71):** all of this is transcript level. **Vault abundance is not one quantity**, and
MVP mRNA rising with maturation is not the same claim as a mature cell holding more particles.

### 83f. Correction from Graham: the timing result was already known

On being shown §83a, Graham's response was *"we knew that it was built as the organ matures - so we
already knew that."*

**He is right, and the framing in §83a was wrong.** We called it *"the first positive prediction this
project has confirmed under a passing gate"* - true as a statement about our gate, and **misleading as
a statement about knowledge.** A registered confirmation of something the field already holds is a
**pipeline validation**, not a finding. The correct reading of §83a is that **our instrument reproduced
known developmental biology**, which is reassuring about the instrument and uninformative about vaults.

**This is the sixth time in this project that we presented something as new without checking** (§74
diagnosed the first five). The pattern survived every rule written to stop it, and this time the check
came from the user in one sentence rather than from us.

**What may still be unchecked, flagged rather than claimed:** the **shell/cap dissociation** of §83b -
MVP up in 7/7 organs while TEP1 falls in 6/7 and PARP4 in 5/7. That was not the test's purpose and is
a different claim from the timing itself. **It is NOT asserted as novel.** It needs a literature check
against the developmental and vault-assembly literature, and that check is **outstanding, not
performed.**

## 84. Grok methods audit: one refusal reversed, one inference withdrawn, one gate declared not a gate

Audit 008 (`grok/from-grok/008r-20261108-2045-grok.md`), requested as a **calculations** audit of the
four tests. It is the sharpest of the six. **It reverses one of our refusals, withdraws one of our
inferences, and supplies a principle we did not have.**

### 84a. The principle we were missing - HOUSE RULE 15

> *"The two overrides are different kinds of decision. Test 4 overrode a met threshold because the
> threshold sits inside the null. That is the right scientific move. Test 2 honoured two failed clauses
> that are not validity conditions of the MVP estimator.* **A gate binds inference only when the failed
> clause is about that estimator.**"

We treated all four dN/dS clauses as equally binding. **They are not the same kind of object.** Clauses
1 and 2 test whether the instrument can separate an essential gene from a drifting one - those are
validity conditions. **Clause 3 is TEP1's pair count and clause 4 is a tally of HTTP timeouts. Neither
enters the sampling distribution of MVP's omega.** Honouring them was not rigour; it was a category
error pointing the same direction rigour usually points, which is why it felt right.

### 84b. REVERSED: MVP's dN/dS of 0.1118 stands, and it means strong purifying selection

**§81d's refusal is withdrawn.** The correct handling is a **protocol deviation on the bundle**, MVP
interpreted against the controls that cleared, and TEP1 left uninterpreted at n=2.

**Placement:** (0.1118 - 0.0771) / (0.2166 - 0.0771) = **0.25** - one quarter of the way from GAPDH to
MX1. **Above every essential control** (all <= 0.0771) **and below every relaxed control** (all >=
0.2166). That is **strong purifying selection, roughly 90% of amino-acid substitutions removed**, and it
is **outside the essential envelope**.

Four corrections to how we reported it:
- **Cow and sheep are one clade.** Collapsing them gives median **0.110**. Effective independent clades
  are **4-5, not 7**; no iid standard error or t-test applies.
- **NG86 biases omega upward**, since dS is the saturated class and Jukes-Cantor under-corrects it. A
  codon model would move these pairs **down together, not reorder them** - toward GAPDH, not toward
  MX1. **The rank is trustworthy; the absolute value is a little high.**
- **The third digit is decorative.** Sampling SE of one pairwise omega is about **0.02**.
- **`dS > 1.5` is lenient**; 1.0 is the defensible cut. **Internal check that saturation is not
  manufacturing the result: opossum is the deepest pair and its omega is mid-pack, not the maximum.**
  Saturation inflation would have put opossum on top. Dropping distant pairs moves the median *down*,
  toward rat's 0.0850 - i.e. more constrained, not less.

**So the conservation paradox has an answer after all, and it is the uncomfortable one we predicted:
where MVP is kept, it is kept under strong purifying selection.** §81e's *"we do not get to know this"*
was wrong - we did know it, and refused to look.

### 84c. WITHDRAWN: sulfur as evidence against storage

§82b argued that MVP's sulfur depletion **argues against** storage because Met is essential and
Met/Cys are expensive, so a bank would hold them. **Grok refuses this and is right:**

> *"Low Met/Cys is what casein-like storage looks like, and you never showed the reserve controls are
> sulfur-rich. 'A bank would hold every expensive amino acid' is a different hypothesis from the one you
> registered."*

**We invented a second hypothesis after the fact and scored it against controls never tested for it.**
The depletion is real - and **understated**: the published sd of 0.0272 matches binomial noise at L~60,
so a z against it compresses the low end, and the distribution is bounded at 0. The length-invariant
statement is **0.0157 / 0.0483 = 0.33x the mean sulfur density, about 14 Cys+Met in 893 residues
against ~43 expected**; in a long-protein bin the z is plausibly **near -2**. §82c's reading - that
Cys/Met-poor fits a particle that must open and must not crosslink - **is unaffected, because it never
depended on the storage comparison.**

**Label hazard in our own output:** `S -1.40` in §82c's residue list is **serine**; `S z = -1.20` is
**sulfur**. Two different things one line apart.

### 84d. §82's gate was non-diagnostic, and the bar was above the only valid control

**FTL stores iron. ALB is a carrier. Neither is an amino-acid nitrogen bank** - two of three "reserve"
controls were the wrong class. The only real one, **CSN1S1 at +0.83, fails the +1.0 bar we imposed on
MVP.** *">= 2 of 3 reserves above the mean" is a coin flip; ">= 2 of 3 structural below +1 sd" is the
default for almost any protein.* **The gate passing did not mean the assay could detect storage.**

The kill still stands: length-stratification lifts MVP from +0.29 to roughly **+0.35 to +0.50**, still
ordinary, and MVP sits about **a third of the way from the mean to casein** (0.29/0.83). **A bar at
casein's own level would also have killed it.** And **residue-pooling is the wrong fix** - the sequence
is fully observed, so the unit is the protein; stratify by length instead.

**Val z = +2.16 is the largest of 20 correlated residue tests, where the maximum of 20 lands near 2
under a null. It is a description, not a second hit.**

### 84e. §83's "prediction met" - restated after running grok's prescribed check

Grok's threat model: RPKM fixes the length-weighted sum, so if a large declining class loses read mass,
every remaining gene is multiplied by a shared k(stage) > 1, and **Spearman scores that inflation as a
strong rise even for a gene at 1.3x, because rho cannot see magnitude.**

We ran its prescription - stage medians, per-gene fold, MVP's percentile in the gene-wise distribution,
and a residual against the cross-gene median trajectory. **`src/chair_repair.py`, 22,879-26,390 genes
per organ.**

| check | result |
|---|---|
| **was the 7/7 sign test mis-centred?** | **No.** Fraction of all genes with rho>0 is **0.486** median (0.387-0.501). The null is centred. |
| MVP fold percentile | 86.3, 91.1, 95.3, 95.4, 89.3, 91.9, 85.0 - **top decile, but >= 95th in only 2 of 7** |
| **residual rho after removing the bulk trajectory** | **0.837, 0.844, 0.791, 0.831, 0.720, 0.790, 0.439 - above 0.5 in 6 of 7** |
| MVP log2 fold | **+4.17 Kidney, +3.10 Ovary, +2.70 Testis, +1.97 Liver** - 4x to 18x, not a coasting 1.3x |
| ACTB / GAPDH | now plainly **inside the declining class** (ACTB 1.4th-45.5th percentile) |

**So MVP's rise is gene-specific, not a normalisation artefact.** The null is correctly centred, the
residual survives removal of the bulk trajectory in 6 of 7 organs, and the fold changes are large.
**But it does not clear grok's stated 95th-percentile bar in 5 of 7 organs**, so **"extreme" overstates
it; "top decile" is the honest word.** And `log1p` was pointless - **Spearman sees only ranks**, so
those rho values are identical to Spearman on raw RPKM.

**Gate clause 2 is recorded as FAILED.** ACTB passed at |rho| 0.678 against a proliferation median of
0.689 - **a margin of 0.011** - and the clause used `|rho|`, discarding the fact that **ACTB is signed
*with* the proliferation markers in 7/7 organs**. 13 of 28 proliferation |rho| values sit below ACTB's.
**ACTB is a failure that an inequality converted into a pass.** GAPDH at 0.271 is a real pass.

**And "pipeline validated" is only true for declines**: there was **no positive control known to rise**,
so the rising side of the instrument is unvalidated.

### 84f. WITHDRAWN: the shell/cap dissociation

§83b claimed MVP up 7/7 while TEP1 down 6/7 and PARP4 down 5/7 supports the shell-first hypothesis.
**Not supported.** TEP1 is **reversed in cerebellum (+0.58)**, and PARP4's 5/7 counts **kidney +0.087,
liver -0.117 and ovary 0.000** as directional. **Require |rho| > 0.3 and PARP4 keeps three of seven.**
The repair run confirms it: PARP4 is **+0.168 Kidney, +0.133 Ovary, -0.270 Liver, -0.518 Testis** -
mixed and small.

**What survives is exploratory and weaker:** MVP and TEP1 have opposite signs in most organs; PARP4 is
mixed. A global scale factor cannot produce opposite signs, so that much is real - but it is also what
class membership looks like when thousands of genes fall and the complement rises.

### 84g. Test 4 - the refusal was right, and the reasoning should be sharper

Grok upholds it and supplies the arithmetic we should have used: **an exact hexamer match at identity p
has probability ~p^6 - about 0.53 at 90% identity, 0.016 at 50%, and 7x10^-4 at 30%.** So **a diverged
paralogue never enters the top 40**, and the prefilter keeps recent duplicates and compositional
accidents. TEP1's WD40 hits passed only because exact short motifs survived - a special case, not a
remote-homology search.

Also: **the floor sits inside the null.** The best local alignment of an 893-residue Val/Glu-rich query
against 20,211 proteins routinely clears 20% over 200 aa; we applied **no correction for 20,211
searches**, and `PairwiseAligner` applies neither SEG nor composition-based statistics. **GAS2L1's 251
aligned residues are 28% of MVP's length** - even a real domain hit would not make it a paralogue of
the protein.

**What should have been run:** a profile HMM from the mammal alignment we already had, searched with
`hmmsearch`/`jackhmmer` at a pre-registered E-value with composition-based statistics on; or a
structure search of the vault fold (Foldseek, DALI, HHpred). **Rank by bit score, never by percent
identity**, and require coverage of a large fraction of the query.

## 85. The outstanding literature check, performed - and the sharper version of the observation

§82d logged the Cys/Met reading as *"an outstanding literature check rather than performed and
forgotten."* Leaving it outstanding after six novelty failures was not defensible. Performed here.

### 85a. The precise numbers, counted rather than z-scored

| | length | Cys | Met | Cys+Met |
|---|---|---|---|---|
| **MVP** | 893 | **5 (0.56%)** | **9 (1.01%)** | **14** |
| TEP1 | 2627 | 56 (2.13%) | 40 (1.52%) | 96 |
| PARP4 | 1724 | 37 (2.15%) | 36 (2.09%) | 73 |
| proteome median | - | **2.05%** | **2.14%** | - |

**MVP carries about one quarter the median cysteine density and half the median methionine density.**
Its five cysteines sit at **59, 182, 282, 515, 572** - spread, not paired.

**And the contrast §82 missed: TEP1 and PARP4 are both proteome-typical.** The depletion is **specific
to the subunit that forms the 78-mer shell**, not a property of the particle's proteins generally. That
is a far better observation than MVP-against-the-proteome, because the caps are the closest available
comparison: same particle, same cell, same expression program, **and no cysteine depletion at all.**

This also supersedes the scaling complaint in §84c. Grok was right that a z against a binomial-inflated
sd is the wrong statistic; **the raw percentages and the within-particle contrast need no sd at all.**

### 85b. What the literature check found, and what it did not settle

**It did not establish that this is unpublished, and it did not establish that it is published.**
Searching for a native MVP cysteine count or a published remark on its depletion returned no such
statement.

**What it did return is directly relevant and better than either answer.** The 9-angstrom vault shell
crystal structure was solved not from native MVP but from **`cpMVP`, an engineered construct carrying
an N-terminal cysteine-peptide insertion**, and in that structure **the introduced cysteines
disulfide-bridge nonequivalent chains across the upper and lower vault halves**
([PLoS Biology 2007](https://journals.plos.org/plosbiology/article?id=10.1371%2Fjournal.pbio.0050318);
[PMC2229873](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2229873/)). Vault engineering patents
describe the same cysteine-rich-peptide fusion
([US 9181312](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/9181312)), and
derivatives are used to tune molecular release
([Sci Rep 2017](https://www.nature.com/articles/s41598-017-12870-x)).

**So the field has been exploiting the absence for nearly twenty years without, as far as this check
can tell, naming it as a feature.** You add cysteines to MVP **because native MVP will not crosslink
its own halves**. That is the mechanistic reading of §82c arrived at from the opposite direction - by
engineers who needed the bridge and had to build it.

**Status: UNRESOLVED, and explicitly not claimed as novel.** At six for six the prior is that a
structural paper says it in passing. What is now defensible is narrower and does not depend on
novelty: **the numbers above are correct, the within-particle contrast is real, and the engineering
literature is consistent with the functional reading.**

## 86. Tier 0b, run properly: MVP is single-copy in the reviewed human proteome

Registered at `06dd589`. Tools installed for the purpose: **HMMER 3.4**.

### 86a. Both gates passed, and gate 2 is the one that earns the negative

**Profile:** `hmmbuild` on eggNOG orthogroup **2QPP0** - 174 sequences, 1,943 aligned columns,
**904 consensus positions**.

| gate | result |
|---|---|
| **1.** the profile must recover MVP itself at E <= 1e-50 | **PASS** - MVP at **E = 0, bit score 1625.6, 98.8% coverage** |
| **2.** `jackhmmer` ACTB must recover ACTG1 at E <= 0.001 and >= 50% coverage | **PASS** - ACTG1 at **E = 9.3e-200, 663.0 bits, 100% coverage** |

> **GO, §88b.** Grok audit 009: *"jackhmmer is iterative and builds bridges through the paralogues it
> is trying to find; the MVP result came from a static hmmsearch."* **Our gate ran a different
> algorithm from our test**, and ACTB/ACTG1 at ~99% identity is the easy case at a new E-value.
> **"Pre-registering a weak event and then passing it is house rule 15 in form only."** The negative
> stands on the **130.4-bit gap** of §89a, not on this gate.

~~**Gate 2 matters more than gate 1.**~~ §84g's objection to the old search was that its controls were
tested **only at 97-99% identity**, so they never showed the method could work in the regime the
question lives in. Under the registered thresholds this pipeline returns **30 genuine actin-family
paralogues** - ACTG1, ACTC1, ACTA2, ACTA1, ACTG2, the POTE family - all at 100% coverage. **The
instrument detects paralogues. That is now demonstrated rather than assumed.**

### 86b. The result

**Non-MVP human proteins clearing E <= 0.001 with >= 50% envelope coverage: ZERO.**

The only other hit at any threshold is **MRFAP1L2 at 10.2 bits, E = 0.14, 10% coverage** - noise.

**Registered decision, fired:** **MVP is single-copy in the reviewed human proteome by profile
search.** §83d's `UNINFORMATIVE` is resolved, and this is the **first time this project has been
entitled to say it.**

Note what changed and what did not. §83d's 6-mer prefilter returned **GAS2L1 at 28.7% over 251
residues**; the profile search's only noise hit is a **different protein entirely**. **Two methods, two
unrelated best-noise hits - which is what noise does**, and it confirms GAS2L1 was never a candidate.

### 86c. What it means for the chair, and the two limits

**The mirror-image hypothesis has no protein to be built from in human.** Graham's *"a similar inverted
protein, maybe a mirror image"* required a paralogue to exist; there isn't one. ~~**Reversible assembly must run through a non-paralogous mechanism** - a chaperone, a protease, a
post-translational modification - not an inverted twin.~~ **WITHDRAWN, §88b:** it **omits the homomeric
path** - the same MVP chain changing conformation, which is §87's entire content - so **our two new
conclusions excluded each other.** Reconciliation: **a trigger nucleating a homomeric opening.** And
§89b shows paralogues **do** exist in 23 of 134 taxa, so the idea is **relocated, not refuted.**

**Two limits, stated rather than buried:**
1. **This is the reviewed proteome** (Swiss-Prot, 20,429). A paralogue annotated only in TrEMBL, or
   missed by annotation entirely, would not appear. The search should be repeated against the full
   proteome and the genome before anyone calls it final.
2. **Human only.** The salmon louse carries an **expanded** vault family, so single-copy here is not
   single-copy everywhere - and the louse is exactly the lineage where a second vault protein was
   repurposed into cement.

## 87. The zipper: not unsupported, unobservable. No test was run, and here is why.

Graham: *"what if the hinge is a zipper?"* **This section runs no test. It is a structural-logic
argument about why no test can currently be run, and it is the most useful thing we can say about the
idea.**

### 87a. "Hinge" may be the wrong mechanical word, and the field's own structures say so

A **hinge** is a localised pivot: two rigid bodies, one axis, one concerted rotation. **The vault's
waist is not that.** It is a **continuous ring of 39 identical inter-half interfaces** (78-mer = 2 x
39). A ring of identical contacts has only two ways to come apart:

- **concertedly** - all 39 break together, which is a very high barrier; or
- **progressively** - one breaks, which strains and then releases its neighbour, propagating around the
  circumference. **That is a zipper.**

Three published observations fit propagation better than rotation, and we had all three on file without
assembling them:

1. **Mrazek et al. 2014's waist mutants produce "continuous symmetric rolls that cannot pinch off."**
   A broken *hinge* would fail to close. A broken *zipper* **keeps adding units** - which is what a
   roll is. The mutation did not remove the pivot; it removed the **stop**.
2. **The L05 shell was flipped into an open rosette by changing one amino acid near the cap.** One
   residue controlling a whole-particle transition is a **nucleation** signature, not a hinge property.
3. **HflK/C, MVP's SPFH relative, opens into a "nautilus"** under antibiotic stress - a **spiral**,
   which is what a partially-propagated ring looks like, not a clamshell.

### 87b. Why no test can be run on deposited data: symmetry imposition erases the signal

**Every deposited vault structure was reconstructed with imposed point symmetry:**

| structure | imposed symmetry |
|---|---|
| **4V60** (Tanaka 2009, rat liver, 3.5 A) | *"exhibiting **39-fold dihedral symmetry**"* (D39) |
| **9BW6** (Lodwick 2025, human + PARP4) | `_pdbx_point_symmetry.circular_symmetry 39` - a 156-meric *"complete point assembly"* built by applying 39 operations |
| **11JB** (78-mer, ADPR-bound) | `_em_3d_reconstruction.symmetry_type POINT`, 16,218 particles |

**A zipper's entire signature is a broken symmetry** - one interface unlike the other 38, a seam, a
partially-propagated intermediate. **Imposing C39 or D39 during reconstruction averages all 39
interfaces into one by construction.** Whatever asymmetry a zipper would produce is **removed before
the map exists.**

~~**So the absence of evidence for progressive opening in the vault literature is not evidence of
absence. It is a property of the reconstruction protocol.**~~ **GO, §91a.** What stands is narrower: **a
rare, randomly phased seam mixes 38:1 into every interface - a 2.6% alternate conformer - so a C39
consensus map is not evidence against a zipper.** Several traces **do** survive symmetrisation and we
checked none of them (NCS local resolution; **2D classes, which precede any point-group symmetry**).
And "the vault literature" was a **widening** - crosslinking and exchange experiments are not
symmetrised at all. The question has not been answered; **it
has not been askable.**

A further consequence worth stating: in a **perfectly symmetric** ring, a zipper has **no designated
start** - nucleation is stochastic, anywhere. So there is also **no conservation test**: there is no
privileged "first" residue for selection to have marked. ~~We considered one and it is uninformative by construction.~~ **GO, §91b - HOUSE RULE 16.** That
argument answers a **different** question: *"stochastic nucleation removes a start-site conservation
test and leaves the contact test untouched."* Whether the **39 waist contact residues** are constrained
relative to non-contact surface residues is cheap, uses the alignment we already hold, and is
informative under every opening model. **Outstanding and owed.**

### 87c. The experiment, which is cheap and uses data that may already exist

**C1 reconstruction with 3D classification.** Reprocess vault particles **without imposed symmetry**,
then classify in 3D for states that are **not** 39-fold symmetric: a seam, a locally separated waist, a
partially opened ring.

- **11JB used 16,218 particles** - ample for C1 classification. **Symmetry expansion followed by
  focused classification on a single waist interface** is the standard modern approach to exactly this
  question, and it is routine in other fields.
- Check **EMPIAR** for the deposited raw particle stacks of 4V60, 9BW6, 11JB and the 2025 PSP-brain
  vault structure before collecting anything new.
- **Prediction, if the zipper is right:** a minority class with **one or a few waist interfaces
  separated while the rest remain closed**. Under a concerted hinge, intermediates should be absent and
  particles should partition cleanly into closed and fully open.
- The PSP-brain structure's incidental observation that **"many vaults contained internal density
  while others were empty"** is exactly the kind of particle-to-particle heterogeneity that symmetry
  imposition hides, and nobody followed it up.

### 87d. Status

**Not claimed as novel.** Symmetry-expansion and focused classification are standard practice, so the
idea that vault asymmetry is unexamined may well have been said in print; at six for six the prior is
that it has. **Not tested** - we ran nothing here. **What is established above is narrow and checkable:
all three deposited structures imposed point symmetry, the field's "hinge" language describes a 39-fold
ring, and the experiment that would separate hinge from zipper has not been done on any deposited
vault dataset.**

**And an incidental find, since we were in the file:** 11JB is titled *"RNA Vault with ADPR bound
(MVP/PARP4/TEP1 NADP sample)"* but **models exactly one protein** - `1 polymer 'Major vault protein'
x78`. PARP4 and TEP1 were in the sample and are not in the model. **Anyone reading that title as a
three-protein structure, as we nearly did in §73, would be wrong.**

## 88. Grok audit 009: the single-copy claim survives, its stated reasons do not, and my two new conclusions contradicted each other

`grok/from-grok/009r-20261108-2154-grok.md`. Requested as an audit of §86 (Tier 0b) and §87 (the
zipper). **The most damaging of the seven**, and it reverses a decision *not* to run a test.

### 88a. What stands

**"No second reviewed-human protein matches the 2QPP0 profile over a substantial fraction of its
length at E <= 0.001" - STANDS.** Grok's reason is better than ours: **the empty tail and the score
gap**, not the thresholds. Self-hit 1625.6 bits at 1.80 bits per consensus column; next hit 10.2 bits
at the noise floor; **nothing in between.** *"A second full-length MVP-like protein would have landed
hundreds of bits above that floor."*

### 88b. What goes - and the first one is structural

**The actin gate does not certify the MVP search. GO.**

> *"jackhmmer is iterative and builds bridges through the paralogues it is trying to find; the MVP
> result came from a static hmmsearch of a prebuilt orthogroup profile. **A pass on the more sensitive
> algorithm does not certify the search that returned zero.**"*

**Our gate ran a different algorithm from our test.** And ACTB/ACTG1 are ~99% identical, so 663 bits at
100% coverage is *"the easy case run at a new E-value"*; the 30-paralogue count is inflated by recent
high-identity duplications. We reported identity, bits, E and coverage only for ACTG1 - **never for the
worst hit in that list**, which is the only number that would have shown the control leaving the
high-identity regime. ***"Pre-registering a weak event and then passing it is house rule 15 in form
only."***

**The 50% coverage bar as the reason for the zero. GO.** Nothing existed between the 10% noise envelope
and 50%, so the bar was not load-bearing - and §89a shows it was actively **wrong**.

**"Therefore disassembly must run through a chaperone, protease or modification." GO.**

> *"It omits the homomeric path: the same MVP chain changing conformation, which is the entire content
> of NEW 2."*

**Our two new conclusions excluded each other** and neither section noticed. The reconciliation grok
supplies: **a trigger - ligand, modification or chaperone - nucleating a homomeric opening.**

### 88c. The blindness, demonstrated in our own output

> *"You treat HflK/C as MVP's SPFH relative, and the human SPFH proteins are in the reviewed proteome;
> none of them cleared E <= 0.001. **This profile does not see its own accepted superfamily.**"*

So the zero's actual scope: **it excludes a mirror-shell protein at 25-40% identity over most of ~900
columns. It says nothing about a one-domain relative at SPFH-like divergence.** The main hole is
**remoteness past this orthogroup**, not TrEMBL and not the coverage bar.

## 89. Two things we were holding and had not reported

### 89a. The empirical detection floor, which inverts our own coverage logic

Grok: *"the sensitivity calibration you already hold and did not report is the score distribution of the
in-profile sequences."* Run on all 174:

| | bits | E | coverage |
|---|---|---|---|
| self-hit (human MVP) | 1625.6 | 0 | 98.8% |
| median in-profile member | 1427.7 | - | - |
| **weakest TRUE member** | **140.6** | **4.6e-43** | **18.0%** |
| next four weakest | 181.3, 197.9, 200.3, 204.5 | ~1e-55..1e-62 | **13.6, 13.9, 12.8, 13.2%** |
| **MRFAP1L2** (only non-MVP human hit) | **10.2** | 0.14 | 10.0% |

**The gap between a genuine remote vault relative and the human noise floor is 130.4 bits.** That is a
far stronger negative than any threshold argument.

**And it shows our registered coverage bar was wrong in substance, not merely inert:** the five weakest
true members cover **12.8-23.7%** of the profile. **A 50% coverage requirement would have discarded
every one of them.** The criterion that works is **bit score**; coverage was the wrong axis and we
registered it as a safeguard.

### 89b. MVP paralogues exist in nature - inside the very orthogroup we built the profile from

| copies per taxon | taxa |
|---|---|
| 1 | 111 |
| 2 | 12 |
| 3 | 7 |
| 4 | 3 |
| **6** | **1** |

**23 of 134 taxa carry more than one MVP in OG 2QPP0** - including *Dictyostelium discoideum* (3),
*Nematostella vectensis* (4), *Aplysia californica* (4) and one taxon with **six**.

**So "single-copy" is a statement about the human lineage, not about the protein family.** Vault
proteins duplicate readily across eukaryotes. **Graham's inverted-partner idea is not refuted - it is
relocated:** the place to look for a second vault protein is a genome that has one.

**And grok's hypothesised blindness is partly confirmed:** the salmon louse (taxid 72036), the one
lineage published as having an **expanded** vault family, is **absent from OG 2QPP0 entirely** - so
eggNOG did not place those copies here, and the profile was never trained on them.

## 90. TIER 0a RUN PROPERLY: under a codon model, MVP's constraint is at housekeeping-gene level

Registered at `06dd589`. `codeml` 4.9j, M0 (one omega), F3x4 codon frequencies, MAFFT protein alignment
threaded to codons, gap-free columns only, fixed topology, **two starting omegas as the registered
reproducibility gate**.

### 90a. The gate, and the number

| gene | class | **omega** | start 0.05 | start 0.5 | taxa | codons | lnL | kappa |
|---|---|---|---|---|---|---|---|---|
| GAPDH | essential control | **0.0516** | 0.05165 | 0.05165 | 9 | 333 | -4011.44 | 1.32 |
| **MVP** | **subject** | **0.0635** | 0.06350 | 0.06350 | 11 | 786 | -14149.21 | 2.44 |
| CD4 | relaxed control | **0.4304** | 0.43041 | 0.43041 | 11 | 386 | -11801.00 | 2.14 |

**GATE PASS.** Registered tolerance between starting values was 0.02; all three genes agree to **five
decimal places**, and MVP's two runs give identical likelihoods to six.

**PREDICTION MET.** Registered: *"omega lands below 0.20 and above 0.02… expected to come in lower than
pairwise NG86's 0.1118, because NG86 biases omega upward."* **0.0635 is in range and is lower.**

### 90b. And the placement changed, which is the substantive result

The whole reason for running this was grok's warning that **a codeml omega cannot be placed against
NG86 pairwise control values** (§84b). So the controls were rerun under the same model, same pipeline,
same topology.

| | essential control | MVP | relaxed control | MVP's position |
|---|---|---|---|---|
| **NG86 pairwise** (§84b) | 0.0771 (GAPDH) | **0.1118** | 0.2166 (MX1) | **25% of the way to relaxed** |
| **codeml M0** (here) | 0.0516 (GAPDH) | **0.0635** | 0.4304 (CD4) | **3.1% of the way to relaxed** |

**Under the proper model MVP is not intermediate between the clusters. It sits essentially on top of the
housekeeping control** - 0.0119 above GAPDH against a 0.3788 span to CD4.

**So §84b understated the constraint.** The reversal grok forced there - that MVP is under strong
purifying selection - **holds and gets stronger**: the honest statement is now that **MVP's selective
constraint is not distinguishable from a housekeeping gene's** on this panel.

**This sharpens the paradox as far as it can be sharpened by sequence alone.** A gene that is deletable
from a mouse with no obvious phenotype, discarded outright by two major clades, and absent from
proliferation screens in 878 cell lines, is **as constrained as GAPDH** wherever it is retained.

### 90c. Limits, stated rather than buried

- **One essential and one relaxed control, not four and three.** §84b's broader panel was NG86 and
  cannot be mixed in.
- **Unequal panels:** GAPDH lost rat (a 618-nt fragmentary transcript, dropped by the filter added in
  §90d) and has no opossum orthologue in the dump, so it ran on 9 taxa and 333 codons against MVP's 11
  and 786.
- **M0 averages one omega over all sites and all branches.** It says nothing about which residues are
  constrained, and site models were not registered and were not run.
- **The topology groups Cetartiodactyla outside the dog/horse clade**, making Laurasiatheria
  paraphyletic. It was fixed in advance and left alone; M0 is robust to this, but it is wrong.
- **Transcript choice was "longest CDS carrying the gene symbol"**, which for human MVP selected a
  **917-codon isoform** rather than the 893-residue canonical. Different isoforms across species add
  gaps rather than bias omega, but the choice was not orthology-aware.
- **The registered extension beyond mammals is only partly delivered**: chicken, *Xenopus* and
  zebrafish are in, but the ~600 My question wants the tunicates, and *Ciona* is not in these dumps
  under this gene symbol.

### 90d. Two faults in our own pipeline, found by their symptoms

**The tree pruner produced single-child nodes.** Dropping a taxon by regex turned `),opossum)` into
`))`, leaving a node with one child, which **codeml rejects silently - GAPDH simply returned no
omega.** Replaced with a real Newick parse that collapses single-child nodes on removal.

**And nothing checked for fragmentary transcripts.** Rat's GAPDH came back at **618 nt against a
~1,002 nt median**, and the resulting alignment retained only **203 gap-free codons** instead of 333.
A median-relative length filter now drops any sequence under 70% of the set's median, and says so.
**Both faults were invisible until a control failed to produce a number at all** - the gate caught
them, which is what it is for.

## 91. Grok audit 009 on the zipper: most of it goes, and it caught us refusing a test on bad reasoning

### 91a. Verdicts, item by item

**(a) the concerted-or-progressive dichotomy - GO.** *"Copy count does not set a barrier."* Thirty-nine
interfaces at 1 kT each is ~23 kcal/mol and slow; at 0.3 kT each it is crossable; if the closed ring is
strained the net barrier can be small. ***"The sign of the coupling is doing all the work and is
undefended."*** Worse, the coupling can run the other way: **strain relief after one break stabilises
the remaining 38 - an anti-zipper - and a ring under tension does that by default.** Independent
interfaces give a binomial scatter of open contacts with **no front at all.** And the modes symmetric
capsids actually use - **axial separation, iris dilation, a global subunit switch** - keep every
interface equivalent throughout and are **neither hinge nor zipper.** **What survives:** a C39 ring
gives selection no geometric reason to mark a single hinge axis, so **a localised pivot is an extra
assumption rather than the default.**

**(b) the three observations as evidence for propagation - GO.** All three are **end states** and two
are **assembly phenotypes.** Mrazek's rolls: every subunit carries the same mutation, so it changes a
**distributed angular parameter**, and a symmetric roll is what a **symmetry-preserving failure to
close** looks like. *"'Removed the stop, not the pivot' discriminates nothing, because a uniformly
weakened contact and a changed dihedral angle both keep adding units."* ***"A zipper-specific
prediction would be an excess of incomplete arcs with a free end. The phenotype as described is the
observation you get when that prediction is not met."*** L05 is **read backwards**: one residue
flipping a particle is what a **cooperative two-state system** does, haemoglobin included, and a
symmetric rosette is an end state of an iris as easily as of a completed zipper. HflK/C's nautilus is
a **static spiral in a relative**, producible by a wedge defect plus curvature with **no time-ordered
front.**

**(c) SPLITS.** **STANDS, in these words:** *a rare, randomly phased seam is invisible in a C39/D39
consensus map, so those maps are not evidence against a zipper* - a seam mixes **38:1 into every
interface, a 2.6% alternate conformer.** **GO:** "unobservable" and "a property of the protocol, not a
finding." Several traces **do** survive, and we did not look at any of them:
- **39-fold is NCS, not a crystallographic axis**, so 4V60's 3.5 A is reached **only where the copies
  agree.** A well-resolved waist is **positive evidence the crystallised molecules were closed.**
  **Waist-versus-cap local resolution is available in the deposited maps and we never compared it.**
- **A large opening is sorted into discarded 2D/3D classes rather than blurred in place**, because
  alignment of a ~13 MDa particle is dominated by the intact shell.
- ***"2D classes are computed before any point-group symmetry.*** A gap large enough to see in
  projection would be there, **and you have not looked.**"
- Per-particle B-factors are one global number and record nothing about which interface failed; local
  resolution stays flat for a randomly phased seam, so **absence of a cold spot is the expected outcome
  under our own model**, not evidence.
- The metadata tags are **weaker than the use we made of them** - a genuinely symmetric particle
  carries the same tags. **One part does stand alone: 9BW6's 156/39 = 4 chains expanded by 39
  operators, so that deposited model has zero power to show inequality.**
- And we **widened a map limitation into "the vault literature"**: crosslinking, exchange and
  subunit-exchange experiments are not symmetrised by C39, and their silence is not explained by the
  reconstruction protocol.

**(d) SPLITS.** **STANDS, and §88 makes it stronger:** there is **one MVP gene**, so all 39 chains are
the same polypeptide and **no conservation statistic can name a start subunit the gene does not
distinguish.** An asymmetric cue does not restore it - an **on-axis** cue (cap, TEP1, a membrane
facing one pole) picks a **pole, not one of 39 longitudes**; an off-axis cargo picks a longitude
**epigenetically**, and that chain is still the same sequence as the other 38.

### 91b. HOUSE RULE 16 - rule 15 applies to a decision NOT to run a test

**GO: "a waist-residue conservation test is therefore uninformative and correctly refused."**

> ***"Stochastic nucleation removes a start-site conservation test and leaves the contact test
> untouched.*** Every opening model, zipper included, uses the same 39 waist contacts, and those
> columns can be conserved, or not, in the 174-sequence alignment you already built. 'Uninformative by
> construction' conflates **'which copy fires first'** with **'are the contact residues
> constrained.'** … **House rule 15 applies to a decision not to run a test: the statistic and the
> informative outcome have to be written down, and here the narrative replaced them.**"

We refused a cheap, informative test by arguing against a **different** test. The question *"are the
waist contact residues under constraint relative to non-contact surface residues"* is ordinary, has a
clean null, uses an alignment we already hold, **and is informative under every opening model.**
**Outstanding and owed.**

### 91c. The hole under both sections

> *"Zipper and hinge are being treated as alternative mechanisms when **a partial ring opening is a
> hinge either way**, and this whole kinetic distinction is being asked of equilibrium maps."*

**Once a contiguous arc is open and the rest is shut, the closed remainder IS the pivot.** That
intermediate is what a stalled zipper, an asynchronous concerted opening, and a damaged barrel all look
like. **Path-independence:** the net free energy of separating all 39 contacts is the same however they
are ordered - **a zipper only changes the shape of the barrier**, and only if the coupling is positive
and something pays the energy.

**And nothing in (a)-(d) establishes that mature vaults open at the waist at all**, as opposed to
failing to close during assembly: **Mrazek is an assembly phenotype; L05 and the nautilus are
alternative oligomers.** If intact half-vaults are the dissociation product, the stable unit is a
39-mer and the coordinate is **axial separation of two rigid halves** - concerted as easily as
zippered.

### 91d. The experiment, rebuilt

**GO as specified, including "16,218 particles should suffice."** Those are the particles that
**survived picking and 2D as intact vaults** - *"the set least likely to contain halves, nautiluses and
open arcs."* Power: expansion gives 16,218 x 39 = **632,502 interface views**, and a one-seam particle
contributes one open view, so an intermediate fraction f yields **f/39 of the expanded stack** - at
f = 0.10 that is **0.26%**, at f = 0.01 it is 162 images. ***"Focused classification on a small mask
finds a minority 'open' class on purely symmetric noise. Running it once, with this prediction, would
manufacture the zipper."***

**The rebuilt design:**
1. **A control mask on a region that must stay closed**, which must come back empty.
2. **The discarded 2D and 3D classes**, which is where a real opening would have gone.
3. **The zipper-specific observable is spatial, not a class count:** open interfaces should form
   **contiguous arcs**, with a **neighbour-correlation length longer than a binomial draw at the same
   occupancy** - and that length should **grow under a triggered-opening condition and shrink under a
   stabilising one.**
4. **A second biochemical state.** ADPR-bound 11JB is one arm only if apo, or another ligand state, is
   classified identically. *"An equilibrium snapshot cannot establish a kinetic path."*

### 91e. The two cheap measurements we declined or skipped

Both are informative **under either kinetic model**, and neither was run:
1. **Conservation of the 39 waist contact residues** against the 174-sequence alignment, with
   non-contact surface residues as the null (§91b).
2. **Waist-versus-cap local resolution** in 4V60 and 11JB, which is in the deposited maps.

## 92. The owed waist test, run: my prediction was wrong, the kill fired, and the contacts are constrained anyway

Registered at `045473f` before the conservation column was read for any waist split. This is the test
**§87d refused**, §91b called owed, and **house rule 16 exists because of.**

### 92a. The gate passed on all three clauses

| clause | result |
|---|---|
| 1. interface `cons` > exposed non-interface `cons` (the existing result must reproduce) | **PASS** - 0.7727 vs 0.6764 |
| 2. >= 15 residues in the waist-proximal bin | **PASS** - n = 18 |
| 3. Mann-Whitney U reported, not means alone | **PASS** - U = 2431.0 |

### 92b. The result, and my prediction is dead

| | n | mean `cons` | median |
|---|---|---|---|
| **WAIST-PROXIMAL** (interface, \|z\| <= 50 A) | **18** | **0.8187** | 0.8397 |
| DISTAL interface (\|z\| > 50 A) | 251 | 0.7694 | 0.8311 |
| NULL - exposed non-interface | 352 | 0.6764 | 0.7288 |

~~**Registered prediction: waist < distal. NOT MET. The kill condition fired.**~~ **KILL WITHDRAWN,
§94b:** the by-chain waist definition §91e asked for gives **the opposite direction and the prediction
MET at p = 0.0076.** This geometric bin **contained mostly residues that are not inter-half contacts at
all.** I argued that *"an
interface that has to come apart cannot be optimised like one that never does"*, registered it
explicitly against the naive guess, and **the direction went the other way.** That reasoning is
recorded as wrong.

**But the comparison it was about is underpowered and settles nothing:** waist versus distal gives
**p = 0.5906** at n = 18. **So the naive reading is not confirmed either** - it is merely not refuted.
Both "the waist is specially conserved" and "the waist is specially relaxed" are outside what 18
residues can decide.

### 92c. What the test does establish, which is what Grok said it would

**Waist contacts versus non-contact exposed surface: 0.8187 vs 0.6764, p = 0.01767.**

**The waist contact residues are under constraint.** That is the question §91b said was *"ordinary and
cheap"* and informative *"under every opening model"*, and the answer is yes. It discriminates nothing
about mechanism - zipper, hinge and iris all use these contacts - and it was never going to.

### 92d. The part that is actually embarrassing

**Every input to this test was already in `results/surface_residues.csv`** - per-residue `interface`,
the axial coordinate `z`, and `cons` from the eggNOG 2QPP0 alignment - generated by `src/surface.py`
under its own earlier pre-registration. **We wrote "uninformative by construction" about a test whose
data was sitting in our own results directory**, computed by our own script, in a project whose entire
method is reading the table instead of describing it (house rule 3).

Grok had to tell us the test was separable from the one we had refuted. **The data never needed
fetching.**

### 92e. Limits

**n = 18.** The waist-proximal bin is small because the `|z| <= 50 A` cut was fixed on geometry before
the split was run, and we are not moving it now. **A properly powered version needs the inter-half
contacts identified by chain in the full assembly**, rather than approximated by axial position in a
single reference chain - which is the measurement §91e still lists as outstanding.

## 93. Waist-versus-cap order: wrong prediction, consistent answer, and the one result that leans toward heterogeneity

Registered at `e316176`, including the note that **a pass would have argued against our own zipper
interest.** It did not pass.

### 93a. Both structures, same direction

| | CA atoms | B range | **waist median B** | **cap median B** | ratio |
|---|---|---|---|---|---|
| **11JB** (78-mer, cryo-EM, `symmetry_type POINT`) | 60,450 | 14.3-109.4 | **63.52** | **51.63** | **1.23x** |
| **4V60** (rat liver, crystallographic, D39) | 63,336 | 6.6-300.0 | **166.62** | **97.52** | **1.71x** |

**Gate passed** on both (IQR 28.0 and 64.3; >= 200 residues per bin, actual n ~9,100-9,500).

**Registered prediction - waist better ordered than cap, i.e. LOWER B - NOT MET in either structure.**
In both, **the waist is the least well-ordered part of the particle**, and in the crystal structure it
is 71% worse than the caps.

### 93b. What that does and does not mean

Grok audit 009 set the interpretation in advance, which is why this was worth running:

> *"A well-resolved waist under that averaging is positive evidence that the crystallized molecules
> were closed and similar; a high open-occupancy would have cost waist resolution relative to the cap."*

**We got the second branch.** Waist disorder survived into both models. That is **consistent with** a
mixed population at the waist - which is what a partially-open subpopulation would produce under
symmetry averaging - and it is the **only measurement in this project that leans that way rather than
away.**

**It is not evidence for a zipper, or for opening at all.** Four reasons, stated before anyone quotes
the ratio:
1. **B-factors absorb far more than local resolution** - model error, genuine flexibility, occupancy,
   and in a crystal structure real thermal motion. 4V60's ceiling of exactly 300.00 is a refinement
   cap, which means the worst regions are **censored, not measured.**
2. **The waist being the most flexible part of a permanently closed particle predicts the same thing.**
   A pinched junction between two 39-mers is where a closed barrel would flex regardless of whether it
   ever opens.
3. **p ~ 0 is an artefact of n.** With ~9,000 residues per bin, any real difference is "significant";
   the effect sizes (1.23x and 1.71x) are the only numbers worth reading.
4. **Our waist bin is geometric** - the 15% of residues nearest the particle's median z - not the
   inter-half contact set identified by chain. §91e's measurement is still the one that would settle it.

### 93c. What is worth keeping

**The direction is consistent across two independent structures determined by different methods**
- cryo-EM with imposed point symmetry, and crystallography with 39-fold NCS - **and it is the opposite
of what we predicted.** That combination is the only thing here resistant to our own enthusiasm: we
registered the comfortable outcome, the data refused it, and the refusal points at the uncomfortable
reading.

**Net: one weak, confounded, consistent signal that the vault waist is where the particle's
heterogeneity lives.** It earns the §91d experiment. It does not substitute for it.

## 94. The by-chain waist: 12 residues, the prediction revives, and the gate's power clause fails

Registered at `e93ab2a` as **a re-test of a dead prediction, not a new bet** - the better waist
definition §91e asked for, specified before it was run.

### 94a. The true inter-half interface is tiny, and it is the N-terminus

Loading **4V60-assembly1** (78 chains, split 39/39 by the `-2` dihedral suffix - **GATE 1 PASS**) and
calling a residue a waist contact when any of its atoms comes within **4.5 A of an atom in a chain of
the other half**:

**12 residues: 1, 2, 3, 4, 6, 21, 42, 43, 44, 45, 46, 47.**

**Twelve, out of 845 modelled.** The entire inter-half interface of a 13 MDa particle is the
**N-terminal ~47 residues**, and almost all of it is the first six. That is a structural fact
independent of anything below, and **it bears directly on §91a's energetics**: grok's objection that
*"copy count does not set a barrier"* is strengthened by how little contact each of the 39 interfaces
actually makes. A 12-residue footprint per interface is not a high concerted barrier.

### 94b. The prediction revives - and the proxy had it backwards

| | n | mean `cons` | median |
|---|---|---|---|
| **TRUE waist contacts** (by chain, 4.5 A) | **10** | **0.5889** | 0.6854 |
| other interface residues | 269 | 0.7727 | 0.8311 |
| null - exposed non-interface | 352 | 0.6764 | 0.7288 |

**Registered prediction - waist contacts LESS conserved than other interfaces - MET, p = 0.0076.**

The §92b proxy version gave **the opposite**: waist 0.8187 vs distal 0.7694, p = 0.5906, and we recorded
the kill as fired. **That kill was an artefact of a bad waist definition.** The geometric bin - the 15%
of residues nearest the waist plane in one reference chain - **contained mostly residues that are not
inter-half contacts at all**, and it reported the wrong direction.

So the reasoning registered in `WAIST_PREREGISTRATION.md` - *"an interface that has to come apart cannot
be optimised like one that never does"* - **survives its proper test**, having died on the proxy.

### 94c. GATE 2 FAILED, and that governs how this may be read

Registered: *"at least 40 true waist-contact residues, or the comparison is still underpowered and is
reported as such."* **We got 10.** Reported as such:

- **n = 10 against 269.** p = 0.0076 is real for a Mann-Whitney at that imbalance, but **ten residues
  is ten residues.**
- **Waist versus the non-contact null is NOT significant** - 0.5889 vs 0.6764, **p = 0.1674**. So the
  waist contacts are **not** demonstrably less conserved than ordinary exposed surface; they are only
  less conserved than *other interfaces*.
- **One structure, one species.** 4V60 is rat, and the contact set is defined on a D39-averaged model -
  the very averaging §91a says cannot show interface inequality. **A seam, if it exists, is not in this
  contact list by construction.**
- The two definitions disagreeing means **at least one of them is measuring the wrong thing**, and the
  by-chain version is only better on argument, not on power.

### 94d. What stands

**Solid:** the inter-half interface of the vault is **12 residues, essentially the N-terminal tail**, and
that is a direct geometric measurement on the deposited assembly.

**Supported but underpowered:** those contacts are less conserved than the particle's other interfaces
(p = 0.0076, n = 10), which is what we registered and what the proxy denied.

**Not supported:** that they are less conserved than ordinary surface (p = 0.17).

**And §92b's recorded kill is withdrawn** - not because we dislike it, but because the test that
produced it used a waist definition the structure does not support.
