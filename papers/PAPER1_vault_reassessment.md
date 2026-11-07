# The vault is a durable shell with an independently turning over enzyme: a pre-registered reassessment of major vault protein across public human and comparative data

**Graham W. Syfert.** Analysis performed with Claude (Anthropic) and a second agent ("Argon") in an
adversarial review loop. All hypotheses were registered in a public git history before the relevant data
were read; every gate, deviation and failure is recorded in `LEDGER.md` (63 entries) and `RESULTS.md`
(24 sections). Correspondence welcome, including corrections.

---

## Abstract

The vault ribonucleoprotein has resisted functional assignment for forty years. We subjected the major
vault protein (MVP) and its partners to nineteen pre-registered tests across public transcriptomic,
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
alignments, that the SPFH shoulder nucleotide pocket is the most conserved structural domain of MVP, with four
ADP-ribose-contacting residues invariant across 174 eukaryotes, and that this pocket cannot be reached
radially through the shell wall and must therefore be loaded from the lumen. The emerging picture is a long-lived, sequence-constrained shell presenting a
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
removes cell-type composition by construction. Across six CPTAC cohorts carrying MVP phosphosites, no site
predicts per-vault PARP4 or TEP1 loading: **0 of 62 tests reach q < 0.05**. The strongest single
association (UCEC, S445 vs PARP4, rho = -0.374, raw p = 0.001) does not survive correction (q = 0.066)
and does not replicate - across all six cohorts measuring S445 (n = 612) the sample-weighted mean rho is
**-0.036**, with sign flips between cohorts. Core and signalling partners appear in MVP sites' top
percentile *less* often than the sampling design predicts (12 observed against 18.9 expected,
p = 0.018). A seventh cohort (LUSC) contributes only an acetylome entry and is excluded.

**The outer surface as the business end.** Before examining the pocket we asked, pre-registered, which
face of the assembled 78-mer evolution protects. Lumen-facing exposed residues are more conserved than
outward-facing ones (0.722 against 0.640; difference -0.081, 95% CI -0.139 to -0.026; Spearman of
conservation against transmural offset -0.206, p = 9.6e-5). The field's lumen-first focus had the right
face, and an outward-facing-interaction model is not supported.

**Our own broad module.** Protein co-abundance initially nominated a membrane-repair and vesicle
neighbourhood around MVP (50 of 101 GO terms passing a matched-query specificity test, including plasma
membrane repair, caveola and endocytosis). We then falsified it twice with our own pre-registered tests:
against physical anti-MVP IP-MS (12 of 100 overlap against 7.4 expected, p = 0.058) and against amoeba
proximity labelling (32 of 100 against 25.0, p = 0.067). Neither reached the registered threshold.
Physical association narrows to PARP4, TEP1 and, in humans, ANXA2 and S100A10.

**Developmental scaffolding.** MVP does not fall across organ development as a scaffold should; it rises,
at the 94th-95th percentile in six of seven human organs, opposite in direction to proliferation.

**Other eliminations.** Tissue co-expression does not track NAD metabolism (2 of 22 pathway genes in the
top 200). The phage L05 repeat 1-2 CoA pocket is not conserved in human vaults. And the proposal that
vaults are immunologically invisible is refuted by published work we found during this project: an
unbiased screen of >21,000 proteins against lupus sera places MVP in the top ten alongside Ro60
(PMID 37127324).

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
11,734 and 14,985 of 17,915. We flag that this analysis failed its own non-essential-complex gate - CAV1
does not recover CAVIN1 or EHD2 - so it is reported as uninformative on its own and carries weight only
alongside the 878-screen result.

We therefore describe the vault as **a durable shell presenting an independently turning over enzymatic
face**. We are explicit that pulse-SILAC measures irreversible proteolysis, not a binding off-rate: a
22-hour half-life is not fast on a signalling timescale, and what the data establish is that PARP4 is
**not retained for the 66-hour lifetime of the shell**. That requires either reversible dissociation or
active extraction of docked PARP4, and the structures place PARP4 at substoichiometric occupancy
(roughly 8-20 copies per 78-mer), not as a continuous coat.
This reconciles three otherwise discordant observations: co-abundance and co-localisation, discordant
degradation kinetics, and the structural placement of PARP4 on the lumenal wall at repeats 3-4 - a patch
which we find to be **less conserved than the protein average** (mean identity 0.711 against 0.730
protein-wide, both means on the full-length human-indexed alignment). This is consistent with a
low-constraint docking patch, but equally with co-divergence alongside PARP4 itself, whose orthologous
group sits at the 3rd conservation percentile; we cannot separate the two. It is not the least conserved
region of the protein - repeat 7 (mean 0.640) and the C-terminal cap disk (0.647) are both lower.

**A sequence-constrained, lumen-restricted nucleotide pocket.** Recent structures place NAD+ and
ADP-ribose in the SPFH shoulder. From two independent alignments and pipelines we find the shoulder
(residues 499-665) to be the **most conserved structural domain** of MVP. Indexed over all 893 human
residues of the same 174-sequence alignment, the shoulder has median identity 0.829 against 0.782
protein-wide (means 0.780 against 0.730); restricted to the residues resolved in the assembled particle
the same comparison gives 0.859 against 0.796. Individual barrel repeats can exceed the shoulder -
repeat 8 (377-427) reaches median 0.888 - so the claim holds at domain resolution and not above it.
F547, D566, F567 and G569 are invariant across 174 eukaryotes and K506 is at 0.987. The conservation of
this pocket was already noted by Lodwick et al. 2025; what is new here is its rank among MVP's domains
across eukaryotes.
Geometric analysis of the assembled 78-mer places all 78 ligand copies within the shell wall at
fractional depth 0.34, and directional probe analysis gives zero exterior accessibility at 1.4 and
2.5 Angstrom radii, with a maximum exterior channel radius of 1.10 Angstrom - narrower than water, and
therefore impassable at any larger probe. This kills the transmural shoulder-pore hypothesis: cytosolic
NAD+ cannot cross the shoulder wall radially, and the pocket must be loaded from the lumen.

It does **not** follow that the particle must open to admit NAD+, and we initially drew that inference in
error. Lodwick et al. 2025 titrate NAD+ and ADP into 50 uM MVP by ITC and solve ligand-occupied cages,
and Osinski et al. 2026 show that purified reconstituted MVP+TEP1 particles hydrolyse added NAD(P)+ and
that an added NAD+ analogue occupies the shoulder pocket, in neutral buffer with no activating trigger.
The assembled cage has openings at the C-terminal caps, and pre-formed vaults breathe at the waist
(Collins et al. 2026). Free dinucleotides therefore reach the lumen unaided. What requires opening is
**macromolecular** traffic - PARP4 (193 kDa), TEP1 (290 kDa), vtRNA, or any ADP-ribosylated target -
not the 663-Da substrate.

**MVP is dispensable but conserved.** Loss-of-function is tolerated in humans (LOEUF 0.92, pLI 0,
observed/expected 0.74; one homozygous null against 0.62 expected) while missense is constrained
(mis_z 2.5), and sequence identity sits at the 89.5th percentile against 400 groups matched on species
count and alignment length - 84.2nd after restricting the null to vertebrate-dominated groups. Deletable,
yet held.

**The LRP biomarker, resolved.** High MVP has predicted chemotherapy failure since the 1990s without a
mechanism. Across 292 cell lines with matched proteomics and dose-response, MVP predicts resistance in 7
of 18 cytotoxics, concentrated in tubulin agents. Two candidate mechanisms die: ABCC1 fails to predict
its own substrates, and vault-RNA-binding drugs are indistinguishable from non-binders (median rho
+0.098 against +0.099), and mitoxantrone - the canonical vtRNA ligand - is the
weakest of the three vtRNA-binding drugs measured (rho +0.064, q = 0.43). The top three drugs, and four
of the top five, are tubulin-directed; rank 4 is methotrexate, an antimetabolite. That MVP is a
correlate rather than a cause was already established genetically - Mvp-null mice and cells are not
chemosensitive (Mossink et al. 2002; Kickhoefer et al. 1998) - and vault-RNA drug binding was proposed
by Gopinath et al.; what is new is the quantitative decomposition. On identical complete-case samples, ABCB1 absorbs a median 25.0% of MVP's effect and division
rate 10.6%, split cleanly by class: efflux substrates to ABCB1, S-phase agents to division rate. MVP is
a passenger on both.

## 3b. What TEP1 is, and why it changes the reading

Paper-length treatments of the vault routinely describe TEP1 as a structural partner. Three 2026 studies
(Osinski et al.; Le Mouellic et al.; Hornebeck et al.) establish that it is not: **TEP1 is an active,
autoinhibited TIR-family NAD(P)ase** with catalytic glutamate E1008, in a STAND architecture
(TROVE-TIR-NACHT-WD40) homologous to SARM1 and APAF-1. Isolated TEP1-TIR hydrolyses NAD(P)+ to
ADP-ribose and nicotinamide; reconstituted MVP+TEP1 particles are catalytically active and the E1008A
mutant is dead. Full-length TEP1 carries a STAND (NACHT-WD40) module expected to gate activation by
oligomerisation or conformational release, but this is contested between the 2026 preprints - purified
TeTIR is monomeric by SEC and crystallography, arguing against obligate oligomerisation - and no
physiological trigger or active oligomeric assembly has yet been demonstrated.
We did not generate these results and cite them because they reframe ours.

Placed beside our findings, all three ancient core proteins converge on one metabolite class inside one
sealed chamber. TEP1 cleaves NAD+ to ADP-ribose; PARP4 transfers ADP-ribose; and MVP's invariant shoulder
pocket binds ADP-ribose at 78 copies, which flips the shoulder's lumenal formal charge from +23 e in the
apo human cage to -133 e in the holo state across the 78-mer shoulder band. This is unscreened formal
charge, computed before counterions and Mg2+.

**This supplies the constraint our nineteen tests could not, and it is a published measurement rather
than an argument of ours.** Hornebeck et al. 2026 expressed the TEP1 TIR domain without its STAND
regulatory domains in HEK293 cells: cellular NAD+ fell to 30-40% of control by 24 h and the cells died
from about 20 h, both abolished by the E1008A catalytic mutation. Le Mouellic et al. 2026 report the
same in *E. coli*. Full-length TEP1 must therefore be held strictly autoinhibited **in cis** by its STAND
domains - reinforced by a millimolar unactivated Km, ~6.9 mM for NADP+ and not saturable for NAD+,
against a free cytosolic NAD+ concentration two orders of magnitude lower - while the vault shoulder
concentrates the ADP-ribose product inside the lumen.

We explicitly do **not** claim that physical separation from cytosolic NAD+ is what keeps the cell alive.
That version of the argument fails on four counts, and we state them because we held it: Mvp-null mice
and cells are viable with TEP1 protein still present and no cage to hold it; intact vaults do not
exclude NAD+; SARM1 itself sits naked in the cytosol at comparable abundance and relies entirely on
intramolecular autoinhibition; and the 10^5 figure counts vault particles, not TEP1, which is present at
roughly one to two copies per particle and is some fortyfold scarcer than MVP. The brake is allosteric,
not architectural.

So construed, the enzymology explains from independent measurement - rather than predicts - the pattern
we observed: no proliferation phenotype across 878 CRISPR screens, no co-essentiality with any gene, no
basal NAD+ depletion across 370 cell lines (MVP r = +0.077; TEP1 r = +0.098, n = 272; every sign
slightly positive), no resting-state fitness effect or metabolic perturbation, and a ligand pocket that
can only be loaded from the lumen. A latent enzyme held shut by its own regulatory domains should look
exactly this inert at rest. The autoinhibition was integrated after our nineteen tests were run and
scored, not pre-registered before them, and we flag that ordering rather than blur it.

It also sharpens what remains unexplained. MVP's 66-hour half-life is ordinary - the 58.6th proteome
percentile, against a median of 56.5 h - so the expense is not rapid rebuilding but the standing cost of
maintaining up to 10^5 particles of 13 MDa each at ordinary turnover, with PARP4 replaced far faster at
the 9.8th percentile, and the pocket held invariant across 174 eukaryotes. Nothing in public data reveals
what the system is held ready *for*.

## 4. Discussion

Four constraints now bound any functional model. The particle is **not required for proliferation** -
zero hits across 878 growth screens, a property shared by under 5% of genes - yet it is **expensive**,
at 10^5 copies of 13 MDa maintained at ordinary turnover, and **sequence-constrained** at a specific
nucleotide-binding face. Its catalytic partner **turns over three to eight times faster than the shell**,
and its ligand site is **not reachable radially through the wall, and must be loaded from the lumen**.

The fourth constraint comes from the enzymology rather than from us: **uninhibited TEP1 depletes cellular
NAD+ and kills human cells, so full-length TEP1 must be held autoinhibited in cis until triggered.**

These are the facts a correct model must accommodate. A static container does not fit: the shell is
continuously replaced and its enzyme is replaced three to eight times faster still. An inert scaffold
does not fit either: the shoulder pocket is the most conserved structural domain of the protein and binds
a metabolite with invariant contacts. The combination of dispensability and conservation suggests a system that is redundant under
laboratory conditions and selected under conditions laboratories do not impose. Under the autoinhibition
constraint this stops being paradoxical: a latent effector is *supposed* to be invisible until triggered,
and nearly every informative assay we ran sampled unstimulated growth, bulk tissue, or perturbations
that do not breach a membrane. The exceptions are real but thin - the CRISPR corpus includes 37
viral-challenge, 28 genotoxic and 9 immune-killing screens, and we tested ten-day kinase-inhibitor
persisters and eighteen cytotoxics - and none of them applies a pore-forming insult.

A pattern in our own scorecard is worth naming, and it is not the one we first wrote down. It is not
that protein-level methods succeeded and transcript-level methods failed: phosphoproteomics, the broad
co-abundance module and the proximity module all failed at the protein level, while sequence
conservation, germline missense constraint and single-cell transcript coupling all succeeded. The real
division is that **every method measuring intrinsic properties of the particle itself** - co-stabilisation,
physical proximity, pocket and lumen sequence constraint, subunit proteolysis - **succeeded**, while
**every method measuring steady-state coupling to an external pathway or growth phenotype in unstimulated
cells** - CRISPR fitness, co-essentiality, broad pathway modules, resting transcript and metabolite
readouts - **failed**. That is the signature of a latent system, and it is what the enzymology above
accounts for.

## 5. Limits

All human analyses are correlative and most use tumour tissue, which carries stromal and immune content
that cell lines lack and normal tissue does not share. Proximity labelling and co-abundance report
neighbourhoods, not contacts. Orthology across a billion years is coarse; we found one annexin cloned
across all thirteen human paralogs, and corrected a claim accordingly. Half-life measurements come from
four immune and hepatic cell types, not from the gut and adrenal epithelium where the protein is most
abundant. No analysis here addresses whether the vault lumen
encapsulates stress-induced nucleic-acid or protein cargo beyond vtRNA, PARP4, TEP1 and ADP-ribose. That
remains the central unanswered question and is not answerable from public data.

## 6. Primary structural and enzymological work this analysis depends on

Lodwick et al., *Nature Communications* 2025, PMID 40691181 - human vault cage with PARP4, nucleotide
ITC and cap openings; PDB 9BW6 and 9MXJ. Osinski et al. 2026, bioRxiv 10.64898/2026.05.01.722283 - TIR-like
NADases in bacterial immunity and the RNA vault; TEP1 enzymology and kinetics; vault with endogenous
ADP-ribose, PDB 11JB. Le Mouellic et al. 2026, bioRxiv 10.64898/2026.09.04.749371, and Hornebeck et al.
2026, bioRxiv 10.64898/2026.09.21.753143 - TeTIR NADase characterisation, product specificity, and the
HEK293 and *E. coli* lethality of the uninhibited domain. Geissler et al., *Nature Communications* 2026,
10.1038/s41467-026-71837-x - *Dictyostelium* MVPA proximity labelling and membrane association. Collins
et al., *ACS Synthetic Biology* 2026;15:3975 - cargo uptake into pre-formed vaults. Anthropic 2026 -
bacteriophage L05 vault structure. Musgrove et al. 2026, PMID 42031226 - crosslinked neuronal MVP
RIP-seq. Mossink et al. 2002 and Kickhoefer et al. 1998/2001 - Mvp-null mice and cells, not
chemosensitive, TEP1 protein retained. Mathieson et al. 2018 - pulse-SILAC half-lives. Benci et al. 2019 -
ISG.RS and IFNG.GS. Moadab et al. 2023, PMID 37127324 - MVP as a lupus autoantigen. We generated none of
these and depend on all of them. Where our reading of one of them was wrong - the inference that NAD+
entry requires the particle to open - the correction is in section 3 and in `LEDGER.md` #61.

## 6b. Data and reproducibility

Every dataset is public. Every pre-registration, deviation, gate and failure is committed in sequence,
and the commit history establishes that predictions preceded data access. Two analyses in this work were
materially wrong before external review corrected them: a mediation analysis that divided coefficients
fitted on different subcohorts, and a cross-species comparison that matched human gene symbols to
*Dictyostelium* gene names. Both corrections, and the reversal of one published conclusion, are recorded
in `LEDGER.md` rather than silently amended.
