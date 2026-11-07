# Additional Hypotheses, Verification Checks & Next-Wave Tests

**Date:** 2026-11-06 (written after `results/prot_final.json` landed at 21:30).  
**Scope:** Everything here goes *beyond* `gemini-argon-audit.txt` and `LEDGER.md` (`#1–#24`). In response to the fair methodological pushback in `LEDGER.md` line 94 ("plausible, testable, but asserted rather than demonstrated"), **every hypothesis below is stated with an explicit dataset, a pre-registrable statistic, a positive-control gate, and a kill condition.**

---

## 0. Two Immediate Verification Checks on Completed Runs (Run Before Locking `#23` & `#8`)

### Check 0.1 — Audit `PRIMARY B: MODULE LEAD` in `results/prot_final.json` Against the `3-PC` Rule
`results/prot_final.json` delivered an unambiguous **PRIMARY A: UNIT** verdict (`PARP4` rank **#2 of 10,924**, `r = 0.820`; `TEP1` rank **#3 of 10,924**, `r = 0.520` — replicated identically at **#2 and #3** after 3-PC removal and at **#2 and #3** in 375 stroma-free `CCLE` cell lines). That single result overturns `LEDGER #15` at the protein level.

However, **PRIMARY B (`MODULE LEAD`) needs two checks before promotion to `STANDING`:**
1. **Tail-term trigger:** In `results/prot_final.json`, **0 of the top 15 GO terms** passed the `< 0.05` specificity threshold (`spec` ranged from `0.060` to `0.170`, meaning 6%–17% of matched random proteins also enrich general actin terms in bulk tumors). `MODULE LEAD` fired because at least one lower-ranked GO term (`q < 0.05`, rank ≥ 16) crossed `spec < 0.05`. Print the exact term(s) with `q < 0.05` and `spec < 0.05`.
2. **Missing 3-PC & CCLE enrichment agreement (`PROTEOMICS_PREREGISTRATION.md` line 57):** The pre-registration states *"Conclusions must agree across both [raw and 3-PC]. If they disagree, the raw result is reported as composition-driven."* `src/prot_coabund.py` verified `PARP4`/`TEP1` ranks in `3-PC` and `CCLE`, **but did not run `enrich()` + specificity on the `3-PC` top-100 or `CCLE` top-100.** In bulk tumors, `ACTR2/3`, `ARPC1B`, `FPR1`, and `PSMB8` partly reflect myeloid infiltrate, whereas in `3-PC` and pure `CCLE` cell lines, a sharper **cell-intrinsic** set (`PARP4`, `TEP1`, `ANXA2`, `CAPN2`, `CAPNS1`, `S100A6`, `IQGAP1`, `EHD2`, `EHD4`, `CAP1`, `CLIC1`) stays at the top. Running `enrich()` on `3-PC` and `CCLE` (5 minutes, local data) cleanly separates stromal actin from cell-intrinsic biology.

### Check 0.2 — Fix the `Protostomia` Taxonomic-Imbalance Artifact in `src/coloss.py` (`#8`)
Inspecting `data/processed/eggnog_presence.npz` directly on `2QPP0` (`MVP`) exposes a tree-descent artifact in `src/coloss.py` (`line 57`: `if v[j] <= .1: out.append(j)`):
- `eggNOG` has **45 `Protostomia` species**: **43 Ecdysozoa** (insects + nematodes) and only **2 Spiralia/Lophotrochozoa** (`Aplysia californica` mollusk, `Helobdella robusta` annelid).
- **Both Spiralia species (`2/2 = 100%`) RETAIN `MVP`**, while Ecdysozoa is `1/43` (`2.3%`, only the centipede `Strigamia maritima`). Because `3/45 = 6.7% <= 10%`, `coloss.py` stopped at `Protostomia`, misclassifying mollusks and annelids as a loss and lumping them with insects/nematodes.
- Simultaneously, inside Stramenopiles (`18` species), **Diatoms (`0/3 = 0%`) lost `MVP`** while **Oomycetes (`11/13 = 84.6%`, `Saprolegnia`, `Pythium`, `Phytophthora`) RETAINED `MVP`**, alongside **Choanoflagellates (`2/2 = 100%`)**, **Porifera (`1/1 = 100%`)**, **Cnidaria (`2/2 = 100%`)**, and **non-vertebrate Deuterostomes (`5/5 = 100%`)**.
- **Check to run (local data, 5 min):** Fix clade-loss calling so small sister sub-clades with `100%` retention (`Spiralia`) are not swallowed by heavily sampled cousin clades (`Insects`), and inspect **gene-level** Jaccard/phylogenetic co-retention (top 50 individual OGs, not 10–500-gene GO terms, which miss 3–5-gene complexes).

---

## 1. Hypothesis H1 — Post-Translational "Orphan Subunit" Sheltering (`MVP` Barrels Control `PARP4` & `TEP1` Protein Half-Life)

### The Empirical Puzzle It Solves
Today produced an apparent contradiction between RNA (`LEDGER #15`) and protein (`prot_final.json`):
- **At the mRNA level**, `TEP1` and `PARP4` do **not** track `MVP` across organ development (`MVP` 95th pct vs `TEP1` 4–79th, `PARP4` 6–59th), tumor proliferation, or persister induction.
- **At the protein level**, `PARP4` (`r = 0.820`, **#2**) and `TEP1` (`r = 0.520`, **#3**) are `MVP`'s top two partners in the entire human proteome across 13 tumor cohorts, 3-PC residuals, and 375 pure cell lines.

**Hypothesis:** `MVP` is the **transcriptionally regulated limiting scaffold**, while `PARP4` and `TEP1` are transcribed largely constitutively and undergo **ubiquitin-proteasome "orphan subunit" degradation** whenever they fail to dock inside an assembled `MVP` barrel (the exact protein-level mirror of Kickhoefer et al. 2001, where `TEP1` loss degraded `vtRNA` without halting `vtRNA` transcription). If true, **every `MVP`-low tissue or knockout is also a functional `PARP4`/`TEP1` protein depletion**, invisible to 40 years of RNA-seq.

### Pre-Registrable Computational Tests (Zero Wet Lab)
1. **Test H1a — Directional Protein-Attenuation Residual (`CPTAC` + `CCLE` matched RNA & Protein):**
   - Pair `data/processed/prot/*.parquet` (`luad`, `lusc`, `paad`, `brca`, `coad`, `ov`, `gbm`, `ucec`, and `ccle_broad_2019`) with matched sample mRNA expression (cBioPortal / DepMap RNA).
   - Fit `R_PARP4 = PARP4_prot - E[PARP4_prot | PARP4_mRNA]` and `R_MVP = MVP_prot - E[MVP_prot | MVP_mRNA]`.
   - **Prediction:** `MVP_prot` (and `MVP_mRNA`) strongly predicts `R_PARP4` (`r > 0.50`, top 0.5% genome-wide) and `R_TEP1`, whereas **the reverse is Asymmetric** (`PARP4_mRNA` does *not* predict `R_MVP`, `|r| < 0.10`), because 78-chain `MVP` shells assemble cleanly without `PARP4` (`Stephen et al. 2001`), whereas free `PARP4` is degraded without `MVP`.
2. **Test H1b — *Trans*-Chromosomal Somatic Copy-Number Proof (`chr16p` → `chr13q` & `chr14q`):**
   - `MVP` is on **`chr16p11.2`**, `PARP4` is on **`chr13q12.12`**, and `TEP1` is on **`chr14q11.2`**.
   - Test across pooled CPTAC + CCLE whether **somatic DNA copy-number gain/deletion of `MVP` (`chr16p11.2`) shifts `PARP4` protein (`chr13`) and `TEP1` protein (`chr14`) in *trans*** while leaving `PARP4_mRNA` and `TEP1_mRNA` unchanged. Because somatic `chr16p` CNA precedes expression, a positive *trans*-pQTL effect is causal, unconfounded genetic proof in human tissue.
- **Gate:** Known scaffold→orphan attenuation pairs (`ITGB1` CNA/mRNA → `ITGA*` protein residual; `SMC3` → `RAD21` protein residual; `CD3E` → `CD3D/G` or `PSMA` proteasome attenuation) must pass directional asymmetry (`p < 1e-6`).
- **Kill Condition:** `PARP4_mRNA ~ MVP_mRNA` in the exact same samples accounts for `>= 70%` of `PARP4_prot ~ MVP_prot`, OR the `chr16p11.2` `MVP` CNA → `PARP4_prot` *trans* effect spans zero while `MVP` *cis*-pQTL passes.

---

## 2. Hypothesis H2 — Plasma/Endomembrane Breach & Pore-Tamponade Complex ("The Cortical Patch Hypothesis")

### Why `results/prot_final.json` Points Here (New Since `gemini-argon-audit.txt`)
Look at the non-vault proteins that sit at the very top of `MVP`'s co-abundance list in **both `3-PC-removed CPTAC` and stroma-free `CCLE` cell lines**:
- **`CAPN2` (#5 in CCLE, #10 CPTAC) + `CAPNS1` (#7 in 3-PC, #8 CPTAC) + `CAPN1` (#31 CPTAC):** Ca²⁺-activated Calpain protease heterodimer triggered immediately by membrane puncture / pore Ca²⁺ influx.
- **`ANXA2` (#6 in 3-PC, #11 CCLE) + `S100A6` (#6 CCLE) + `ANXA4` (#36 CPTAC):** Ca²⁺-triggered phospholipid-binding membrane-resealing plugs.
- **`EHD2` (#9 CCLE) + `EHD4` (#10 CCLE, #39 CPTAC):** Caveolae / membrane-curvature ATPases required for plasma-membrane wound repair.
- **`IQGAP1` (#7 CCLE, #14 CPTAC) + `CAP1` (#9 3-PC) + `CLIC1` (#8 3-PC):** Cortical actin wound-closure ring + oxidation-sensing membrane-inserting chloride channel.

**Hypothesis:** Vaults (`SPFH` membrane-microdomain shoulder + Ca²⁺-binding waist + low-pH disassembly + 40 nm footprint) are **pre-assembled cortical/endomembrane breach scaffolds** recruited alongside `Calpain + Annexin A2/A4 + EHD2/4` to plug or quarantine acute membrane pores (bacterial `T3SS`/pore-forming toxins like *Pseudomonas* and *Listeria* LLO, mechanical shear in lung/gut/endothelium, or ruptured phagolysosomes) and shed naked into the non-vesicular extracellular fraction (`Jeppesen et al. 2019`) as damaged membrane patches are excised.

This immediately explains **`0/878` CRISPR growth screens (`LEDGER #7`)**: canonical plasma-membrane repair proteins (`DYSF` Dysferlin, `ANXA1/2`, `EHD2/4`, `CAV1`) also have ~0 growth hits in unstressed plastic dishes!

### Pre-Registrable Computational Tests
1. **Test H2a — Continuous `DepMap Chronos` Co-Essentiality (Overcoming Binary `ORCS` Blindness):**
   - `ORCS` (`#7`) used binary author hit calls (`HIT == YES`), discarding 99% of variance for subtle/lineage-specific genes. In Broad DepMap (`CRISPRGeneEffect.csv`, ~1,100 human cell lines), non-essential complexes (`CAV1`–`CAVIN1`–`EHD2` caveolae; peroxisomes; melanosomes) still show highly significant **continuous gene-effect correlations** across 1,100 cell lines because subtle mechanical/passaging/media stresses perturb partner genes together.
   - Compute genome-wide Pearson/GLS co-essentiality of `MVP`'s continuous `Chronos` vector across ~1,100 lines. Does `MVP` cluster with `PARP4`/`TEP1`, `ANXA2`/`CAPN2`/`CAPNS1`/`EHD2/4`/`CAV1`, or endolysosomal ESCRT repair (`CHMP*`/`PDCD6IP`)?
   - **Gate:** `CAV1` (also `0` binary essentiality in most screens) must recover `CAVIN1` and `EHD2` in its top 25 co-essential partners (`q < 0.01`).
   - **Kill Condition:** `MVP`'s top continuous co-essentiality correlation across ~18,000 genes fails `FDR q < 0.05` even though `CAV1` passes.
2. **Test H2b — Chemical-Genetic Sensitivity to Membrane / Lysosomal Disruptors (`DepMap PRISM` + `GDSC`):**
   - Test `MVP` protein (`ccle_broad_2019`, on disk) and `MVP` `Chronos` score against drug response across ~4,500 compounds in PRISM Repurposing + GDSC, pre-specifying **membrane-destabilizing / lysosomotropic / ionophore / ferroptotic / statin-cholesterol** classes against nuclear DNA-damaging controls.
   - **Gate:** `GPX4`/`FSP1`(`AIFM2`) expression recovers ferroptosis inducers (`RSL3`, `erastin`, `ML210`); `ABCB1` recovers taxanes/vinca alkaloids.
   - **Kill Condition:** Pre-specified membrane/lysosomotropic compound classes show no shift (`q >= 0.05`) relative to background compounds.

---

## 3. Hypothesis H3 — The "Rigid Cell Wall / Cuticle Replacement" Macroevolutionary Law

### The Pattern Across All 472 Eukaryotes in `eggNOG`
Looking across the full taxonomic breakdown of `2QPP0` (`MVP`) in `data/processed/eggnog_presence.npz`:
- **Retained (`85%–100%`):** Unicellular naked-membrane phagotrophs (`Choanoflagellata` `2/2`), basal naked-epithelium animals (`Porifera` `1/1`, `Cnidaria` `2/2`), soft-bodied `Spiralia` (`Mollusca + Annelida` `2/2`), `Deuterostomia` (`99/109`), free-living soil amoebae exposed to osmotic shock (`Dictyostelium` `2/2`), and Stramenopiles that disperse via **wall-less, osmotically fragile motile zoospores** (`Oomycota` `11/13`, `84.6%`).
- **Deleted (`0%–2.3%`):** Every clade that encased its cells or external/gut epithelia in a **rigid cell wall, silica shell, or molted chitin/collagen cuticle**, or retreated inside an isotonic host cell: `Fungi` (`0/178`, chitin wall), `Viridiplantae` (`0/76`, cellulose wall), `Diatoms` (`0/3`, silica frustule), `Nematoda` (`0/10`, collagenous cuticle), `Insects/Crustaceans` (`0/32` in eggNOG, chitinous exoskeleton — with the famous salmon-louse exception repurposing MVP into secreted cuticle glue!), and `Entamoeba` (`0/2`, isotonic gut endoparasite).

**Hypothesis:** Vaults protect **naked, mechanically/osmotically deformable eukaryotic plasma membranes** (phagocytosis, hypotonic shock, ciliated/mucosal shear, pore-forming toxins). Whenever a lineage evolves an external rigid cell wall, mineral shell, or molted cuticle (simultaneously abandoning phagocytosis and shielding the plasma membrane from direct mechanical/toxin contact), the 100,000-copy metabolic cost of vaults ceases to pay for itself and the gene is cleanly deleted.

### Pre-Registrable Computational Test
- Code each of the 472 `eggNOG` eukaryote species on two objective textbook traits **blinded to `MVP` status**:
  1. `Rigid_Exterior` (`1` = vegetative cell wall [cellulose/chitin/peptidoglycan/theca/frustule] without naked phagotrophic/zoospore trophic dependency, OR ecdysozoan molted cuticle covering ectoderm + foregut/hindgut; `0` = naked plasma membrane / non-cuticulate epithelium / wall-less zoospore dispersal);
  2. `Obligate_Endoparasite` (`1` = obligate intracellular/isotonic lumen parasite such as *Plasmodium*, *Cryptosporidium*, *Entamoeba*, *Encephalitozoon*; `0` = free-living / extracellular).
- Fit **phylogenetic logistic regression (`phyloglm` / Pagel's 1994 correlated-evolution likelihood ratio test)** on the NCBI/TimeTree eukaryote phylogeny so shared ancestry (`Fungi` counting once, `Viridiplantae` counting once, `Ecdysozoa` counting once, `Diatoms` counting once, etc.) is strictly controlled.
- **Gate:** `Ciliary_Motility` trait must significantly predict `IFT88` retention under the exact same phylogenetic regression (`p < 1e-4`), and a housekeeping control must show no association.
- **Kill Condition:** Phylogenetic LRT `p >= 0.05` across the independent transitions, OR expanding sampling to sequenced chytrids (*Batrachochytrium*, which has wall-less zoospores), unicellular algae (*Chlamydomonas* vs naked prasinophytes), and wider Lophotrochozoa/Tardigrada contradicts the naked-membrane/zoospore prediction.

---

## 4. Hypothesis H4 — Solving the 30-Year `LRP` Chemoresistance Biomarker (`LEDGER #21`): The `chr16p` `ABCC1` (`MRP1`) Neighbor Confound vs. Slow-Division Confound vs. `vtRNA` Drug Class

### The Genomic Fact Nobody Checked Today
`LEDGER #21` notes that the 30-year clinical association between high `LRP/MVP` and poor chemotherapy outcome now has *less* explanation than this morning. Look at the chromosome map of where `LRP` (`MVP`) was discovered in multidrug-resistant lung cancer (`SW-1573/2R120`, `GLC4/ADR`; Scheffer et al., *Nat Med* 1995; Slovak et al., *Cancer Res* 1995):
- **`MVP` (`LRP`) sits at `chr16p11.2` (`29.8 Mb`).**
- **`ABCC1` (`MRP1` — Multidrug Resistance-Associated Protein 1, a proven ATP-dependent drug efflux pump!) sits on the SAME short arm of chromosome 16 at `chr16p13.11` (`16.0 Mb`)!**
- Whole-arm `chr16p` gains and amplicons in lung, ovarian, and myeloid tumors co-amplify `ABCC1` and `MVP` together. At the same time, in `LUAD`/`LUSC` (`results/proliferation.json`), high `MVP` marks **non-dividing (`0.0–0.7th` pct proliferation)** differentiated cells — and cytotoxic S/M-phase chemotherapy selectively kills dividing cells!

### Pre-Registrable Three-Way Dissection (Runnable on `ccle_broad_2019` Proteomics + `GDSC1/2` & `PRISM`)
Across the **375 cancer cell lines** already in `data/processed/prot/ccle_broad_2019.parquet` matched to `GDSC1/2` and `PRISM` drug `AUC`s (doxorubicin, mitoxantrone, etoposide, cisplatin, vincristine, paclitaxel, 5-FU, cytarabine):
1. **Raw biomarker check:** Does `MVP` *protein* correlate with cytotoxic chemo resistance (`AUC`) across cell lines (and within NSCLC / AML / ovarian subsets)?
2. **Three competing mediators tested head-to-head in nested models:**
   - **Model A (`chr16p` / `ABCC1` passenger):** Does adjusting for `ABCC1` protein + `chr16p` copy number collapse the `MVP` effect?
   - **Model B (Division-rate passenger):** Does adjusting for measured cell-line **doubling time** + proliferation protein score (`MKI67`/`TOP2A`/`MCM2`) collapse the `MVP` effect?
   - **Model C (`vtRNA`-binding drug specificity, `Article 2 §3b`):** Does `MVP` (or `TEP1`) protein specifically predict resistance to **anthracyclines / mitoxantrone** (demonstrated `vtRNA1-1/1-2` binders) significantly more than non-binding taxanes/platinums/antimetabolites *after* controlling for `ABCC1`, `ABCB1`, doubling time, and lineage?
- **Gate:** `ABCB1` protein must strongly predict paclitaxel/vinblastine resistance (`p < 1e-8`); `ABCC1` protein must predict etoposide/doxorubicin resistance; `SLFN11` protein must predict topotecan/cisplatin sensitivity (`p < 1e-8`).
- **Outcome Value:** Whichever of A, B, or C wins (or if `MVP` protein has zero cell-intrinsic association even raw across 375 lines, proving the clinical biopsy signal was stromal/macrophage infiltrate all along!), **a 30-year oncology mystery gets a concrete, quantitative answer.**

---

## 5. Hypothesis H5 — Direct Metabolomic & Lipidomic Screening of `MVP` Protein in `CCLE` (Testing `LEDGER #18`: "Absorb What?")

### Why This Directly Attacks `LEDGER #18`'s Named Weakness
`LEDGER #18` identifies *"Sink / absorption, deployed on demand"* as the best-fitting survivor of all 10 tests, with one glaring hole: **"absorb what?"** Meanwhile, `CCLE` proteomics (`prot_final.json`) placed **`MGLL` (monoacylglycerol lipase, #8 in CCLE)** and CPTAC placed **`PLIN3` (perilipin-3, #23)** and **`SQOR` (sulfide:quinone oxidoreductase, #11)** alongside `MVP`.

Broad CCLE published **quantitative LC-MS profiling of 225 intracellular polar metabolites and lipids** (`Li et al., Nature Medicine 2019`) across ~928 cell lines — **~350 of which overlap directly with `data/processed/prot/ccle_broad_2019.parquet` on disk!** Measured species include acyl-carnitines, CoA-linked intermediates, reduced/oxidized glutathione (`GSH`/`GSSG`), NAD+/NADH, nucleotides, methyl-donors (`SAM`/`SAH`), ceramides, sphingomyelins, cholesteryl esters, diacylglycerols, monoacylglycerols, and lysophospholipids (the direct products of membrane phospholipase stress!).

### Pre-Registrable Test
- Correlate `MVP` protein (raw and lineage-residualized) across the ~350 overlapping `CCLE` lines against all 225 metabolites/lipids, plus lipid-class summary scores (lysophospholipids `LPC`/`LPE` — markers of membrane repair/remodeling — vs triacylglycerols vs redox `GSH/GSSG`).
- **Gate:** `SLC7A11` / `GCLC` protein must recover `GSH` (`q < 1e-4`); `IDH1/2` hotspot or `NNMT` protein (`1-methylnicotinamide`, one of the strongest signals in Li 2019) must pass at `q < 1e-10`.
- **Kill Condition:** Zero metabolites or lipid classes pass `FDR q < 0.05` after lineage adjustment. A clean null here directly damages the small-molecule/lipid metabolic buffer version of `#18`.

---

## 6. Hypothesis H6 — Breaking the Interferon Loop via `16p11.2` Copy-Number Natural Experiment + CPTAC Phospho-Switch Mapping

### 6A. Somatic `16p11.2` Deletion/Gain vs. `STAT1` / `NF-κB` Output (`Article 1 §6` Executed Properly)
Every mRNA correlation between `MVP` and interferon (`RESULTS.md §§2–3`) is circular because `STAT1` drives the `MVP` promoter. Somatic DNA copy-number (`CNA`) loss or gain at `chr16p11.2` breaks that reverse-causation arrow: **`STAT1` cannot delete chromosome `16p11.2`.**
- **Crucial refinement nobody noted in Article 1:** The canonical `16p11.2` microdeletion interval (~600 kb) also contains **`MAPK3` (`ERK1`)**! Any `16p11.2` CNA test MUST check focal `MVP` vs `MAPK3` co-deletion (or adjust for `MAPK3` dosage / test whether `MVP` point mutations/truncations in TCGA `n ~ 10,000` shift `ISG` or `NF-κB` scores relative to wild-type within the same tumor type).
- **Gate:** Somatic `JAK1`/`JAK2` or `B2M`/`IFNGR1` deletions/truncations in TCGA must reduce `IFNG.GS`/`ISG` output; `MVP` CNA must shift `MVP` mRNA & protein (`p < 1e-10`).
- **Kill Condition:** Neither `MVP` truncating mutations nor `MVP` copy loss (controlling for purity and aneuploidy) increases `ISG` or `NF-κB` transcriptional scores (or `STAT1-pY701` in CPTAC phosphoproteomics) across tumors (`95% CI` within `[-0.10, +0.10]` SD).

### 6B. CPTAC Site-Level Phosphoproteomics — Finding the Post-Translational Trigger
Vaults translocate to lipid rafts within 15 minutes (`Kowalski 2007`) and open on electrostatic perturbation (`Anthropic 2026`). CPTAC has **site-level phosphoproteomics** (`phosphoprotein_quantification`) on the exact same cohorts already in `data/processed/prot/`.
- **Test:** Residualize each measured `MVP` phosphosite (`Y13`, `Y15`, shoulder/cap serines/threonines) on total `MVP` protein (`pSite_resid = MVP_pSite - beta * MVP_prot`) so abundance cannot confound stoichiometry. Test which upstream kinase activity / pathway (`Src/FAK` focal adhesion, `EGFR/MAPK`, `PKC` Ca²⁺ signaling, `JAK/STAT`) correlates with stoichiometric `MVP` phosphorylation across cohorts.
- **Gate:** Stoichiometric `STAT1-pY701/pS727` residualized on total `STAT1` protein must correlate with `ISG` expression (`q < 0.001`).
- **Kill Condition:** All `MVP` phosphosites scale strictly linearly with total `MVP` protein, with no reproducible cross-cohort kinase/pathway association in the residuals (`q >= 0.05`).

---

## 7. Hypothesis H7 — Prokaryotic & Bacteriophage Operon Synteny ("Guilt by Operon" on `L05` & Bacterial `MVP` Homologs)

`Article 5` Experiment 7 proposed checking the genomic neighbors of phage `L05` ("costs nothing but compute"), yet it never made it into `LEDGER.md`. **In prokaryotes and phages, operon synteny succeeds precisely where eukaryotic clade co-loss (`#8`) fails**, because co-functioning bacterial/phage genes are physically co-transcribed within `±5` ORFs.

### Pre-Registrable Three-Way Operon Test (NCBI / UniProt / Pfam, ~15 min)
Pull all bacterial and phage `MVP` homologs (`Pfam PF01505` / `InterPro IPR002504` Vault protein repeat + SPFH shoulder homologs in Myxococcota, Cyanobacteria, Planctomycetota, and Caudoviricetes/jumbo phages) and score Pfam domain enrichment within `±5` flanking ORFs against shuffled genomic windows:
1. **Viral Morphogenesis (`terminase`, `portal`, `major capsid`, `tail`, `prohead protease`)** → genuine capsid lineage;
2. **Acyl-CoA / Polyketide / Toxin Metabolism (`AMP-binding` acyl-CoA synthetase, `acyltransferase`, `CoA-transferase`, `thioesterase`, `cytochrome P450`, `ABC efflux`)** → directly validates the **`L05` CoA-pocket metabolic compartment / toxin-sink** hypothesis (`LEDGER #13/#18`)!
3. **Membrane-Envelope Stress / Anti-Phage Defense (`SPFH/HflK-C`, `FtsH` protease, `PspA` phage-shock membrane repair, `CBASS`/`Thoeris`/restriction-modification)** → validates **H2 (membrane-breach / pore defense)** back to bacteria!
- **Gate:** Bacterial `Encapsulin` (`PF04454`) flanking `±3` ORFs must enrich `DyP-type peroxidase` / `ferritin-like` cargo domains (`q < 1e-10`); `HflK` must enrich `HflC` and `FtsH`.
- **Kill Condition:** Flanking `±5` ORFs around prokaryotic/phage `MVP` homologs show no conserved Pfam family at `FDR q < 0.05`.

---

## 8. Hypothesis H8 — Testing the Untouched RNA Half of the Vault (`vtRNA` → `p62` Autophagic Flux & `NSUN2`/`svRNAb` → `CYP3A4` in Human Liver)

Every test run today (`#1–#24`) interrogated `MVP`/`TEP1`/`PARP4` and left **Layer 3 (`vtRNA1-1` → `p62`/`SQSTM1` selective autophagy buffer)** and **Layer 1c (`NSUN2` → `svRNAb` → `CYP3A4`)** completely untouched. Two tests are immediately runnable on public human cohorts:

### 8A. Proteomic Selective-Autophagy Flux Signature (`SQSTM1`/`p62` Protein-to-mRNA Accumulation Ratio in `CPTAC` + `CCLE`)
When selective autophagy runs faster, **`SQSTM1` (`p62`), `NBR1`, `TAX1BP1`, and `NCOA4` proteins are degraded in lysosomes while their mRNAs stay constant or rise** — making `SQSTM1_prot - E[SQSTM1_prot | SQSTM1_mRNA]` the established human-tissue proteomic readout of **autophagic flux blockade** (`Horos et al., Cell 2019`).
- **Test:** Across `CPTAC` (13 cohorts) and `CCLE` (375 cell lines), test whether `MVP` protein (and specifically the **`TEP1`-to-`MVP` stoichiometry**, which governs `vtRNA` stabilization per Kickhoefer 2001!) predicts `SQSTM1` / `NBR1` / `TAX1BP1` post-transcriptional protein accumulation, controlling for `NFE2L2`/`NRF2` oxidative-stress transcription.
- **Gate:** `KEAP1`/`NFE2L2` status recovers `SQSTM1` mRNA induction; known autophagy/lysosomal v-ATPase (`ATP6V*`) protein variation shifts `SQSTM1`/`NBR1`/`NCOA4` protein-to-mRNA residuals together.
- **Kill Condition:** `SQSTM1`/`NBR1`/`TAX1BP1` protein-to-mRNA residuals show zero association (`|r| < 0.05`, `CI` spanning zero) with `MVP` and `TEP1` across both `CPTAC` and `CCLE`.

### 8B. `NSUN2` × `DICER1` × `VTRNA1-1` Small-RNA Reads → `CYP3A4` in Human Liver (`TCGA-LIHC` + `CPTAC` / `GTEx`)
`Article 2 §8` highlighted `Persson et al. (Nat Cell Biol 2009)`: `NSUN2` methylates `vtRNA1-1` (`m5C`), enabling `DICER1` cleavage into `svRNAb`, which represses **`CYP3A4`** in cell lines — but rested on an old RNase-protection negative in resting liver.
- **Test:** In `TCGA-LIHC` (`n = 366` human liver tumors + `50` matched normal human livers; expression already in `data/processed/bulk/lihc.expr.parquet`, plus TCGA small-RNA sequencing alignments covering `VTRNA1-1` on `chr5q31.3`!) and `GTEx` normal adult human livers (`n > 200`):
  1. Check whether `21–24 nt` `svRNAb` reads mapping to `VTRNA1-1` are actually detectable at modern sequencing depth in normal and inflamed/stressed human liver (directly answering Persson's 2009 sensitivity limit!).
  2. Test whether `NSUN2` (and `svRNAb` read abundance where available, plus `NSUN2 × DICER1` interaction) **inversely correlates with `CYP3A4`** after controlling for hepatocyte differentiation (`HNF4A`, `NR1I2`/`PXR`, `NR1I3`/`CAR`, `ALB`), using non-target P450s or `ALB` as negative specificity controls.
- **Gate:** `HNF4A` and `NR1I2` (`PXR`) must strongly positively predict `CYP3A4` in human liver (`r > 0.50`, `p < 1e-15`).
- **Kill Condition:** `svRNAb` reads remain absent at modern depth in human liver AND `NSUN2` / `VTRNA1-1` shows non-negative or null partial correlation with `CYP3A4` after `HNF4A`/`PXR` adjustment.

---

## 9. Recommended Execution Order (Highest Signal-per-Minute First)

| Priority | Test | Needs Download? | Est. Runtime | What Question It Settles |
|---|---|---|---|---|
| **1** | **Check 0.1:** `3-PC` & `CCLE` GO enrichment + print exact `spec < 0.05` terms on `prot_final` | **No** (all on disk) | **3 min** | Whether `MODULE LEAD` is stromal actin or a true cell-intrinsic `Calpain–Annexin–EHD` module |
| **2** | **(Already pre-registered #24):** `4V60` 78-mer local-shell transmural + interface SASA + `gnomAD` missense map (`SURFACE_AMENDMENT.md`) | **No** (`4V60-assembly1.cif.gz` & `MVP.json` on disk) | **5 min** | Inside vs. outside conservation + whether `mis_z = 2.5` sits on 78-mer assembly interfaces |
| **3** | **Check 0.2 + H3:** Fix `Protostomia` (`Spiralia` vs `Ecdysozoa`) in `coloss.py` + run phylogenetic `Rigid_Wall_Or_Cuticle` test | **No** (`eggnog_presence.npz` on disk) | **10 min** | Why entire kingdoms deleted vaults while naked-membrane lineages kept them |
| **4** | **H1a + H1b + H8a:** Matched RNA + Protein + CNA in `CPTAC` & `CCLE` (`PARP4`/`TEP1` orphan stabilization, *trans*-`16p11.2` CNA, and `SQSTM1` flux ratio) | Small API fetch (`mRNA` + `CNA` for cohorts already in `prot/`) | **15 min** | Proves causal `MVP → PARP4/TEP1` protein sheltering + tests `p62` autophagy flux in humans |
| **5** | **H4 + H2b + H5:** `CCLE` `MVP` protein vs `GDSC/PRISM` drugs (`chr16p` `ABCC1` + doubling-time dissection) & `CCLE` `225` Metabolites/Lipids | Fast public CSVs (DepMap / GDSC / Li 2019 metabolomics) | **20 min** | Solves 30-year `LRP` chemoresistance confound (`#21`) & directly tests metabolic ligands (`#18`) |
| **6** | **H2a:** Continuous `DepMap Chronos` genome-wide co-essentiality (~1,100 lines) | One public CSV (`CRISPRGeneEffect.csv`) | **10 min** | Recovers subtle fitness partners that binary `ORCS` (`#7`) could never see |
| **7** | **H7:** Prokaryotic & phage `L05` operon synteny (`±5` ORFs Pfam enrichment) | NCBI / UniProt API | **15 min** | Tests Capsid vs. Acyl-CoA/Metabolic vs. Membrane-Defense operons in bacteria & phages |
| **8** | **H6 + H8b:** `16p11.2` CNA → IFN/phospho-`MVP` switch (`CPTAC`) & `NSUN2`/`svRNAb` → `CYP3A4` in `TCGA-LIHC`/`GTEx` liver | Public GDC / cBioPortal phospho & liver tables | **25 min** | Breaks IFN transcriptional circularity & tests hepatic `CYP3A4` regulation in humans |
