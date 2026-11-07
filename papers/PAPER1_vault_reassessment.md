# The vault is a durable shell with a rapidly exchanging enzyme: a pre-registered reassessment of major vault protein across public human and comparative data

**Graham W. Syfert.** Analysis performed with Claude (Anthropic) and a second agent ("Argon") in an
adversarial review loop. All hypotheses were registered in a public git history before the relevant data
were read; every gate, deviation and failure is recorded in `LEDGER.md` (61 entries) and `RESULTS.md`
(24 sections). Correspondence welcome, including corrections.

---

## Abstract

The vault ribonucleoprotein has resisted functional assignment for forty years. We subjected the major
vault protein (MVP) and its partners to eighteen pre-registered tests across public transcriptomic,
proteomic, genomic, structural and comparative datasets, each gated on recovery of a known positive
control. Most standing hypotheses failed. MVP is not a member of the chronic interferon resistance
program; it is not a drug-tolerant persister marker; no gene module is co-lost with it across 472
eukaryotes; vault RNA does not detectably gate selective autophagy at tissue level; NSUN2 does not
repress CYP3A4 in human liver; and phosphorylation does not gate vault assembly or partner exchange.
What survives is narrow and reproducible. MVP, PARP4 and TEP1 form a single assembly detectable by
protein co-abundance (PARP4 and TEP1 ranked 1 and 2 of 10,924 proteins across thirteen tumour cohorts)
and by proximity labelling in *Dictyostelium*, yet they share neither fitness coupling nor degradation
kinetics: PARP4 turns over threefold faster than MVP (22.2 h versus 66.4 h) in four of four non-dividing
primary human cell types. We resolve the thirty-year LRP chemoresistance biomarker as a passenger
phenomenon split between ABCB1-mediated efflux and slow division. We confirm, from two independent
alignments, that the SPFH shoulder nucleotide pocket is the most conserved region of MVP, with four
ADP-ribose-contacting residues invariant across 174 eukaryotes, and that this pocket is accessible only
from the lumen. The emerging picture is a long-lived, sequence-constrained shell presenting a
dynamically occupied enzymatic face, dispensable for proliferation yet held under purifying selection.

---

## 1. Introduction

The vault particle is among the largest known cytoplasmic ribonucleoprotein complexes: approximately 13
MDa, assembled from 78 copies of MVP, present at up to 10^5 copies per cell, and conserved across the
eukaryotic crown. Its persistence is matched only by the absence of an accepted function. Murine Mvp
nulls are viable and fertile; whole kingdoms, including Fungi and Viridiplantae, have deleted the gene
outright.

The modern literature has accumulated candidate roles faster than it has eliminated them: multidrug
resistance, interferon signalling, innate immune sensing, autophagy regulation, nucleocytoplasmic
transport, and nanoparticle engineering. These hypotheses are rarely tested against one another, and
almost never against a stated falsification criterion.

We took the opposite approach. Each hypothesis was converted into a pre-registered statistical test with
a positive-control gate and an explicit kill condition, committed to version control before the relevant
data were examined. Where a gate failed, the result is reported as uninformative rather than
reinterpreted. Where our own analysis was wrong, the correction is recorded alongside the original.

## 2. What does not survive

**The chronic interferon resistance program.** MVP is an interferon-gamma-inducible gene, and the
published MVP-immune literature is self-contradictory. Benci and colleagues partitioned interferon-
stimulated genes into an acute immune signature (IFNG.GS) and a chronic resistance signature (ISG.RS).
We tested whether MVP partitions with the chronic set within malignant cells. It does not. In single-cell
data from lung adenocarcinoma (21 patients, 24,784 malignant cells) MVP sits at the 29th genome
percentile on the acute-chronic axis; in melanoma the result is unresolved. Bulk checkpoint-inhibitor
cohorts gave an apparently strong acute assignment, but collinearity between the two signatures (VIF
11-23) destabilised it, and the result did not survive ssGSEA scoring or the ratio formulation. MVP's
membership in IFNG.GS is an artefact of set construction: that signature is Hallmark interferon-gamma
minus ISG.RS, so MVP was assigned by subtraction and never tested.

The single reproducible positive is that MVP is unusually interferon-coupled without belonging to either
program: 95th and 88th genome percentile for the two signatures in malignant lung cells.

**Drug tolerance and persistence.** Across three cancer lineages and three kinase inhibitors, MVP is
induced in drug-tolerant persisters at the 80.6th, 82.0th and 81.1st percentile - strikingly reproducible,
but below the 90th-percentile threshold registered in advance, and no stronger in quiescent than cycling
persisters. MVP marks neither state selectively.

**Co-loss across eukaryotes.** Using orthologous group presence across 472 eukaryotes and an
event-based loss model, no gene family is co-lost with MVP at q < 0.05 (best q = 0.157), while the same
pipeline recovers intraflagellar transport from IFT88 and respiratory complex I from NDUFS2, and 45% of
matched random queries return a significant term. A taxonomic artefact identified in review - Spiralia
retain MVP but were absorbed into an Ecdysozoa-wide loss call - was corrected without changing the
conclusion. The method is structurally blind to partners that are themselves essential, which motivated
the proteomic approach below.

**Vault RNA and autophagy.** In Vaultrc5-knockout mice with the deletion confirmed in liver
(log2FC -1.37, 0.1st percentile), a seventeen-gene p62/autophagy receptor program is unmoved
(-0.058, p = 0.46); Sqstm1 itself shifts -0.09. Transcript abundance cannot report p62 oligomerisation,
which is what the buffer model predicts, so this bounds the tissue-level consequence rather than
refuting the biochemistry.

**Vault RNA and drug metabolism.** In 366 human liver tumours, with HNF4A and PXR recovering CYP3A4 as
expected (rho +0.48 and +0.53), NSUN2 shows no partial association with CYP3A4 (rho -0.052, p = 0.33).
The only nominal association is with CYP2E1, a non-target, which argues differentiation residue rather
than specific repression.

**Phosphorylation as a regulatory gate.** Residualising each phosphosite on its own gene's total protein
removes cell-type composition by construction. Across seven CPTAC cohorts, no MVP phosphosite predicts
per-vault PARP4 or TEP1 loading (0 of 44 tests at q < 0.05, all |rho| < 0.11), and core or signalling
partners appear in MVP sites' top percentile *less* often than the sampling design predicts (12 observed
against 18.9 expected, p = 0.018).

**Tissue and disease predictions.** Lung is not the highest-MVP tissue; it ranks fifth of 51, behind
adrenal gland and the colon-small intestine-duodenum axis. Placenta ranks 38th, retiring a
pre-eclampsia prediction by its originator's own stated criterion.

## 3. What survives

**One assembly by abundance and proximity; not by turnover or fitness.** Across thirteen
mass-spectrometry cohorts, MVP's two closest co-abundant proteins out of 10,924 are PARP4 (r = 0.82) and
TEP1 (r = 0.52), unchanged after removal of three principal components, in 375 stroma-free cell lines,
and after per-gene copy-number adjustment. The same pipeline recovers the proteasome, complex I and the
ribosome from single seeds. In *Dictyostelium*, MVPA proximity labelling places PARP4 and TEP1 orthologs
among vault-proximal proteins (log2FC +3.49 and +1.61, q < 10^-4) across more than a billion years.

The association is nonetheless not a welded complex. In four of four non-dividing primary human cell
types - where pulse-SILAC half-life is pure proteolysis - the ordering PARP4 < TEP1 < MVP holds, with
PARP4 at 22.2 h against MVP at 66.4 h and an eightfold gap in NK cells. And across 1,178 cell lines,
MVP's strongest genome-wide co-essentiality is r = 0.205, with PARP4, TEP1 and ANXA2 ranked 9,020,
11,734 and 14,985 of 17,915.

We therefore describe the vault as **a durable shell presenting a rapidly exchanging enzymatic face**.
This reconciles three otherwise discordant observations: co-abundance and co-localisation, discordant
degradation kinetics, and the structural placement of PARP4 on the lumenal wall at repeats 3-4 - a patch
which we find to be the *least* conserved region of MVP (0.708 against 0.787 protein-wide), as a
reversible docking site should be.

**A sequence-constrained, lumen-restricted nucleotide pocket.** Recent structures place NAD+ and
ADP-ribose in the SPFH shoulder. From two independent alignments and pipelines we find the shoulder
(residues 499-665) to be the most conserved region of MVP (median identity 0.839 against 0.787
protein-wide), with F547, D566, F567 and G569 invariant across 174 eukaryotes and K506 at 0.987.
Geometric analysis of the assembled 78-mer places all 78 ligand copies within the shell wall at
fractional depth 0.34, and directional probe analysis gives zero exterior accessibility at both 1.4 and
5.0 Angstrom radii. Cytosolic NAD+ cannot cross the shoulder wall; substrate access requires the
particle to open.

**MVP is dispensable but conserved.** Loss-of-function is tolerated in humans (LOEUF 0.92, pLI 0,
observed/expected 0.74; one homozygous null against 0.66 expected) while missense is constrained
(mis_z 2.5), and sequence identity sits at the 89.5th percentile against 400 groups matched on species
count and alignment length - 84.2nd after restricting the null to vertebrate-dominated groups. Deletable,
yet held.

**The LRP biomarker, resolved.** High MVP has predicted chemotherapy failure since the 1990s without a
mechanism. Across 292 cell lines with matched proteomics and dose-response, MVP predicts resistance in 7
of 18 cytotoxics, concentrated in tubulin agents. Two candidate mechanisms die: ABCC1 fails to predict
its own substrates, and vault-RNA-binding drugs are indistinguishable from non-binders (median rho
+0.098 against +0.099), with mitoxantrone - the canonical vtRNA ligand - the least associated drug
tested. On identical complete-case samples, ABCB1 absorbs a median 25.0% of MVP's effect and division
rate 10.6%, split cleanly by class: efflux substrates to ABCB1, S-phase agents to division rate. MVP is
a passenger on both.

## 4. Discussion

Three constraints now bound any functional model. The particle is **not required for proliferation** -
zero hits across 878 growth screens, a property shared by under 5% of genes - yet it is **expensive**,
at 10^5 copies with a 66-hour half-life, and **sequence-constrained** at a specific nucleotide-binding
face. Its catalytic partner **exchanges three to eight times faster than the shell**, and its ligand
site is **reachable only from the lumen**.

These are the facts a correct model must accommodate. A static container does not fit: the shell is
rebuilt continuously and its enzyme is replaced faster still. An inert scaffold does not fit either: the
shoulder pocket is the most conserved part of the protein and binds a metabolite with invariant
contacts. The combination of dispensability and conservation suggests a system that is redundant under
laboratory conditions and selected under conditions laboratories do not impose.

We note that every method which succeeded here measured **protein**, and every method which failed
measured **transcript or presence/absence**. Co-abundance recovers the complex; mRNA correlation,
evolutionary co-loss and knockout transcriptomics do not. For a long-lived structural protein whose
partners are post-translationally stabilised, this is expected, and it may explain why four decades of
expression-based inference produced a contradictory literature.

## 5. Limits

All human analyses are correlative and most use tumour tissue, which carries stromal and immune content
that cell lines lack and normal tissue does not share. Proximity labelling and co-abundance report
neighbourhoods, not contacts. Orthology across a billion years is coarse; we found one annexin cloned
across all thirteen human paralogs, and corrected a claim accordingly. Half-life measurements come from
four immune and hepatic cell types, not from the gut and adrenal epithelium where the protein is most
abundant. No analysis here addresses what the vault lumen contains, which remains the central unanswered
question and is not answerable from public data.

## 6. Data and reproducibility

Every dataset is public. Every pre-registration, deviation, gate and failure is committed in sequence,
and the commit history establishes that predictions preceded data access. Two analyses in this work were
materially wrong before external review corrected them: a mediation analysis that divided coefficients
fitted on different subcohorts, and a cross-species comparison that matched human gene symbols to
*Dictyostelium* gene names. Both corrections, and the reversal of one published conclusion, are recorded
in `LEDGER.md` rather than silently amended.
