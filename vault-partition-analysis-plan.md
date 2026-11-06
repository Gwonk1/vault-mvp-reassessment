# Analysis Plan: Does MVP Belong to the Chronic Interferon Resistance Program?

**Prepared 2026-11-06 for execution in Claude Code.** This is a computational plan only — public
data, no wet lab, no new samples.

---

## 0. Why this analysis and not the obvious one

The naive test — correlate MVP expression against an interferon signature in tumor data — is
circular. MVP is itself IFN-γ-inducible through a STAT1 site in its promoter, so it sits
*downstream* of any interferon signature. Any inflamed tumor reads MVP-high regardless of what
MVP does. That confound is why the published MVP/immune-correlation literature contradicts
itself (pancreatic and hepatocellular results say immune-evasive; papillary thyroid and
pan-cancer say immune-hot).

**The design fix:** compare MVP against *two different interferon-driven gene sets* rather than
against interferon in general. Both comparison sets are IFN-induced, so interferon induction is
held constant and cancels out. The question becomes which subset MVP partitions with — not
whether it responds to interferon at all.

The two subsets come from the acute-versus-chronic distinction:

- **Acute IFN-γ response** — immune recognition and effector function. Intact in immune control,
  impaired during progression (Krysan/Tran/Dubinett: progressive premalignant lesions show
  decreased interferon signaling and antigen presentation).
- **Chronic interferon resistance program** — prolonged signaling produces STAT1/IRF3-maintained
  epigenetic changes, a restricted subset of ISGs, checkpoint-ligand upregulation, and T cell
  dysfunction (Benci et al., *Cell* 2016; Qiu et al., *Nat Cancer* 2023). In Qiu's model one
  member is the RNA sensor OAS1, which amplifies type I interferon while immune-inhibitory genes
  rise alongside it.

MVP's reported behavior — induced by IFN-γ, then *inhibits* STAT1, while *inducing* type I
interferon through IRF7, and driving M2 macrophage polarization through STAT6 — is structurally
the same profile OAS1 has in that model. That is the hypothesis to test.

---

## 1. Pre-registration (complete BEFORE running anything)

Fill this in, commit it, and do not edit it afterward. The whole value of this analysis is that
it can come out against the hypothesis.

```
Date:
Primary prediction:
Predicted sign and relative magnitude of β(ISG.RS) vs β(IFNG.GS):
What result would make me abandon the containment layer:
What result would make me abandon the signaling-brake layer:
Decision rule for "no effect":
```

Stated predictions:

| Outcome | Interpretation |
|---|---|
| MVP tracks chronic set after adjustment, within malignant cells | MVP is a member of the chronic resistance program. Supports the signaling-brake layer. **Argues against containment as the primary function.** |
| MVP tracks acute IFN-γ set | MVP is an ordinary acute ISG. The brake story weakens; the interferon angle becomes uninteresting. |
| MVP tracks neither | ISG framing is wrong for MVP. The confound worry was overstated. Containment survives but gains nothing. |
| MVP anti-correlates with both after adjustment | This is the containment prediction — vaults suppressing sensing. Most interesting possible result. |

All four are publishable as a short note. That is the point of choosing this test.

---

## 2. Gene sets

**Do not type these from memory. Pull them from source and record versions.**

1. **ISG.RS** (interferon-stimulated gene resistance signature) and **IFNG.GS** (IFN-γ gene
   signature) — the formal acute/chronic pair. Defined in Benci et al., *Cell* 2019, "Opposing
   functions of interferon coordinate adaptive and innate immune responses to cancer immune
   checkpoint blockade." **Verify the exact member lists from that paper's supplementary tables.**
   The 2016 paper's headline genes (IFIT1, IFIT3, MX1, OAS1) are a subset, not the signature.
2. **HALLMARK_INTERFERON_GAMMA_RESPONSE** and **HALLMARK_INTERFERON_ALPHA_RESPONSE** from MSigDB,
   as coarse controls. Record MSigDB release.
3. **Qiu 2023 inflammatory-memory ISG subset** — extract from that paper's supplement if listed.

### Critical trap

**Check whether MVP is itself a member of any of these sets and remove it before scoring.** MVP is
an IFN-γ-inducible gene and may well appear in HALLMARK_INTERFERON_GAMMA_RESPONSE. If it is left
in, you will be correlating MVP with a score that contains MVP, and the result is guaranteed and
meaningless. Assert this programmatically with a test that fails loudly, not a comment.

Gene symbol: **MVP**. Ensembl: **ENSG00000013364**. UniProt: **Q14764**. Aliases to catch in older
annotations: **LRP**, **LRP/MVP**, **VAULT1**.

---

## 3. Data

### 3a. Primary — ICB-treated cohorts with RNA-seq plus response

Verify availability and access terms for each before writing acquisition code. Do not assume.

- Melanoma: Hugo 2016, Van Allen 2015, Riaz 2017, Gide 2019, Liu 2019
- Bladder: IMvigor210 (atezolizumab; distributed as an R data package)
- NSCLC: Jung 2019 and any NSCLC ICB cohorts with RNA-seq that are currently public

Several of these are aggregated in TIDE and in published re-analysis repositories, which is
usually faster than assembling from GEO one at a time. Record provenance per cohort.

### 3b. Secondary — TCGA, for the treatment-independent structural question

LUAD, LUSC, SKCM, plus **PAAD, LIHC, THCA** specifically. Those last three are where the published
MVP contradictions live, so include them to test whether the contradiction resolves as different
positions on the acute/chronic axis rather than as conflicting findings.

### 3c. The test that actually matters — single cell

Bulk correlation can be driven entirely by immune infiltration, because MVP is expressed in
macrophages and dendritic cells and the ISG sets are partly immune-derived in bulk tissue. So:

- Yanagawa / Tran / Salehi-Rad / Lim / Dubinett, single-cell characterization of pulmonary nodules
  across early lung adenocarcinoma
- Sinjab / Kadara, multiregion single-cell sequencing of lung adenocarcinoma (*Cancer Discov* 2021)

Ask whether MVP and the chronic set co-vary **within the malignant epithelial compartment**, with
myeloid cells analyzed separately. **Treat bulk as the screen and single-cell as the test.** A bulk
result with no single-cell confirmation is not a finding.

### 3d. Epigenetic check — the sharpest single lookup

Qiu's model says chronic-program ISGs carry H3K4me1-marked accessible chromatin. If that paper
deposited ChIP-seq/ATAC in GEO, **query the MVP locus directly in their inflammatory-memory
domains.** This is a lookup in an existing deposited dataset and could settle the question faster
than everything above. Do this first if the data exists.

---

## 4. Statistics

### Core model, per cohort

1. Score each sample for ISG.RS and IFNG.GS. Use z-scored mean of log-transformed member genes;
   repeat with ssGSEA or GSVA as a robustness check. Agreement between methods is a sanity gate.
2. Fit `MVP ~ ISG.RS + IFNG.GS` and report standardized coefficients with CIs.
   **The test is which signature survives adjustment for the other.**
3. Report **VIF**. ISG.RS and IFNG.GS are strongly collinear by construction and will inflate
   standard errors. Because of that, also run the non-collinear version: compute the
   **ISG.RS / IFNG.GS ratio** (Benci's own framing) and test MVP against it. Both analyses should
   agree; if they don't, the collinearity is eating the result and you say so.
4. Stratify: is MVP elevated in ISG.RS-high / IFNG.GS-low samples specifically?

### Required covariates

- Tumor purity (ESTIMATE or ABSOLUTE)
- Myeloid and lymphoid fractions (CIBERSORTx or equivalent) — non-negotiable, since MVP is
  myeloid-expressed
- Tumor type / cohort as a random effect in any pooled model
- Mutational burden where available

### Secondary endpoint

In ICB cohorts, test whether MVP associates with response, and whether it adds information beyond
ISG.RS via a likelihood-ratio test on nested models. Expect it not to. If MVP is simply a member
of the program, it should carry no independent signal — and that negative result is itself
informative, because independent signal would suggest MVP does something the rest of the program
doesn't.

### Multiple comparisons

Pre-specify the primary test (step 2, in the pooled ICB cohorts) as the one that counts. Everything
else is exploratory and labeled as such. Benjamini-Hochberg across the exploratory set. Do not
promote an exploratory hit to the headline.

---

## 5. Deliverables

1. `data/` acquisition scripts with provenance and checksums per cohort
2. `scores.py` / `scores.R` — gene set scoring with the MVP-exclusion assertion
3. `models.*` — the fits, with VIF and diagnostics printed
4. Three figures: MVP vs each signature; forest plot of adjusted coefficients across cohorts;
   single-cell MVP-versus-chronic-set within the malignant compartment
5. `RESULTS.md` — the pre-registered predictions, what came out, and which of the four outcomes in
   §1 obtained. Written to be readable by someone who will disagree with it.

---

## 6. Honest limits, to be stated in any write-up

- MVP does not appear in Dubinett's published work, nor — as far as searching has shown — in
  Benci's or Qiu's named gene sets. **This is a placement hypothesis, not a reported finding.**
- The whole analysis is correlative. Partitioning with the chronic set would show MVP *belongs to*
  the program, not that it *maintains* it. Causal claims need the knockout and IFN-readout
  experiment, not this.
- Bulk transcriptomics cannot separate tumor-intrinsic from infiltrate-driven signal. The
  single-cell step is what makes the claim, and if that data turns out to be unusable, the honest
  conclusion is "suggestive, unresolved."
- This test cannot address the containment layer directly. It can only make containment less
  necessary as an explanation by showing the signaling-brake layer accounts for the interferon
  observations on its own.

---

## 7. One caution about the project this belongs to

Two disconfirmations have now been absorbed into this hypothesis in a single day: the 2002 MVP
knockout showing no hypersensitivity to cytostatics (absorbed as "wrong endpoint measured") and
the interferon-direction contradiction (absorbed as "wrong axis compared"). Both absorptions are
defensible — acute versus chronic is independently established, and the knockout genuinely did
measure cytotoxicity rather than interferon output. But the pattern is the failure mode to watch.
Complete §1 before running anything, and let the pre-registration decide what the result means
rather than deciding afterward.
