# One assembly, three lifetimes, and a sealed nucleotide pocket: a pre-registered reassessment of major vault protein across public human and comparative data

**Graham W. Syfert.** Analysis performed with Claude (Anthropic). Two further language-model agents
reviewed the manuscript adversarially against the committed data, in three rounds; between them they
struck or qualified more than a dozen claims made here, and those reversals are recorded in place
rather than quietly removed. All hypotheses were committed to a timestamped git history before the
relevant data were read; every gate, deviation and failure is recorded in `LEDGER.md` (119 entries)
and `RESULTS.md` (24 sections). **That history is currently local and has not been published**, so
the ordering it establishes is not yet independently verifiable; we state the fact rather than imply
otherwise, and the repository is available to anyone who asks. Correspondence welcome, including
corrections.

---

## Abstract

The vault ribonucleoprotein has resisted functional assignment for forty years. We subjected the
major vault protein (MVP) and its partners to nineteen pre-registered tests across public
transcriptomic, proteomic, genomic, structural and comparative datasets, each gated on recovery of a
known positive control. **Five of the nineteen returned a formally uninformative verdict because a
control gate failed, and we mark each one rather than promote it.** Most standing hypotheses
nonetheless failed on tests that did gate: MVP is not a member of the chronic interferon resistance
program; no gene family is co-lost with it across 472 eukaryotes; NSUN2 does not repress CYP3A4 in
human liver; and phosphorylation does not gate vault assembly or partner exchange. Drug-tolerant
persistence and tissue-level autophagy gating both pointed the same way but failed their gates, so
we report them as uninformative.

What survives is narrow. MVP, PARP4 and TEP1 are mutually closest by protein co-abundance - PARP4
and TEP1 at ranks 1 and 2 of 10,924 proteins across thirteen tumour cohorts, and PARP4 first with
TEP1 third after copy-number adjustment - and all three are vault-proximal in *Dictyostelium*. They
are not a welded complex: the ordering PARP4 < TEP1 < MVP holds in four of four non-dividing primary
human cell types, with ratios from 1.5- to 8.1-fold, though that test also failed its gate. We
resolve the thirty-year LRP chemoresistance biomarker as a passenger phenomenon carried by two
separate mechanisms, ABCB1-mediated efflux and slow division, which do not partition by drug class.
We confirm, from two independent alignments, that the SPFH shoulder nucleotide pocket is the most
conserved structural domain of MVP, with four ADP-ribose-contacting residues invariant across 174
eukaryotes, and that this pocket cannot be reached radially through the shell wall and must
therefore be loaded from the lumen. The emerging picture is a long-lived shell presenting a
dynamically occupied enzymatic face, dispensable for proliferation while retaining a
sequence-constrained ligand site. We note that our own registered rule scored MVP's overall
conservation as *typical* rather than unusual, and we do not claim otherwise.

---

## 1. Introduction

The vault particle is among the largest known cytoplasmic ribonucleoprotein complexes: approximately
13 MDa, assembled from 78 copies of MVP, present at up to 10^5 copies per cell, and conserved across
the eukaryotic crown. Its persistence is matched only by the absence of an accepted function. Murine
Mvp nulls are viable and fertile; whole kingdoms, including Fungi and Viridiplantae, have deleted
the gene outright.

The modern literature has accumulated candidate roles faster than it has eliminated them: multidrug
resistance, interferon signalling, innate immune sensing, autophagy regulation, nucleocytoplasmic
transport, and nanoparticle engineering. These hypotheses are rarely tested against one another, and
almost never against a stated falsification criterion.

We took the opposite approach. Each hypothesis was converted into a pre-registered statistical test
with a positive-control gate and an explicit kill condition, committed to version control before the
relevant data were examined. Where a gate failed, the result is reported as uninformative rather
than reinterpreted. Where our own analysis was wrong, the correction is recorded alongside the
original.

**The gate scorecard, stated up front.** Of nineteen tests, twelve returned an informative verdict
with their positive controls recovered; **five carry a formal verdict of UNINFORMATIVE in their own
committed output** - co-essentiality (CAV1 fails to recover CAVIN1 or EHD2), developmental
trajectory (two of three stemness markers absent or above threshold), drug-tolerant persistence (a
proliferation control undetected in one model), subunit turnover (short-lived controls absent from
the pulse-SILAC table entirely) and the Vaultrc5 knockout (the transcript is undetected in brain);
and two passed partially - the CRISPR corpus, where the genotoxic screen class failed its control
while viral and immune-killing classes passed, and the LRP decomposition, where ABCC1 failed to
predict its own substrates.

We say this in the introduction because an earlier draft of this paper asserted four of those five
in its title and abstract as though they were findings, which is precisely the failure the gate was
meant to prevent. Where an uninformative test and an informative one point the same way we say so
and lean on the informative one; where an uninformative test stands alone, it supports nothing.

## 2. What does not survive

**The chronic interferon resistance program.** MVP is an interferon-gamma-inducible gene, and the
published MVP-immune literature is self-contradictory. Benci and colleagues partitioned interferon-
stimulated genes into an acute immune signature (IFNG.GS) and a chronic resistance signature
(ISG.RS). We tested whether MVP partitions with the chronic set within malignant cells. It does not.
In single-cell data from lung adenocarcinoma (21 patients, 24,784 malignant cells) MVP sits at the
29th genome percentile on the acute-chronic axis; in melanoma the result is unresolved. That
percentile is sensitive to one preprocessing choice we should disclose rather than bury: adjusting
for sequencing depth moves it to the **9.7th**, which crosses the 10th-percentile line we use
elsewhere for a specific call. Either way it is on the acute side and nowhere near chronic, which is
what the test was about, but the specificity of the assignment depends on the adjustment. Bulk
checkpoint-inhibitor cohorts gave an apparently strong acute assignment, but collinearity between
the two signatures (VIF 11-23) destabilised it, and the result did not survive ssGSEA scoring or the
ratio formulation. MVP's membership in IFNG.GS is an artefact of set construction: that signature is
Hallmark interferon-gamma minus ISG.RS, so MVP was assigned by subtraction and never tested.

The single reproducible positive is that MVP is unusually interferon-coupled without belonging to
either program: 95th and 88th genome percentile for the two signatures in malignant lung cells.

**Drug tolerance and persistence.** Across three cancer lineages and three kinase inhibitors, MVP is
induced in drug-tolerant persisters at the 80.6th, 82.0th and 81.1st percentile - strikingly
reproducible, but below the 90th-percentile threshold registered in advance, and no stronger in
quiescent than cycling persisters. MVP marks neither state selectively. This test also failed its
gate - a proliferation control was undetected in one model - so its formal label is uninformative;
the three percentiles sit below the registered bar either way.

**Co-loss across eukaryotes.** Using orthologous group presence across 472 eukaryotes and an
event-based loss model, no gene family is co-lost with MVP at q < 0.05 (best q = 0.157), while the
same pipeline recovers intraflagellar transport from IFT88 and respiratory complex I from NDUFS2,
and 45% of matched random queries return a significant term. A taxonomic artefact identified in
review - Spiralia retain MVP but were absorbed into an Ecdysozoa-wide loss call - was corrected
without changing the conclusion. The method is structurally blind to partners that are themselves
essential, which motivated the proteomic approach below.

**Vault RNA and autophagy.** In Vaultrc5-knockout mice with the deletion confirmed in liver (log2FC
-1.37, 0.1st percentile), a seventeen-gene p62/autophagy receptor program is unmoved (-0.058, p =
0.46); Sqstm1 itself shifts -0.09. Transcript abundance cannot report p62 oligomerisation, which is
what the buffer model predicts, so this bounds the tissue-level consequence rather than refuting the
biochemistry.

**Vault RNA and drug metabolism.** In 366 human liver tumours, with HNF4A and PXR recovering CYP3A4
as expected (rho +0.48 and +0.53), NSUN2 shows no partial association with CYP3A4 (rho -0.052, p =
0.33). The only nominal association is with CYP2E1, a non-target, which argues differentiation
residue rather than specific repression.

**Phosphorylation as a regulatory gate.** Residualising each phosphosite on its own gene's total
protein removes cell-type composition by construction. Across six CPTAC cohorts carrying MVP
phosphosites, no site predicts per-vault PARP4 or TEP1 loading: **0 of 62 tests reach q < 0.05**.
The strongest single association (UCEC, S445 vs PARP4, rho = -0.374, raw p = 0.001) does not survive
correction (q = 0.066) and does not replicate - across all six cohorts measuring S445 (n = 612) the
sample-weighted mean rho is **-0.036**, with sign flips between cohorts. Core and signalling
partners appear in MVP sites' top percentile *less* often than the sampling design predicts (12
observed against 18.9 expected, p = 0.018). A seventh cohort (LUSC) contributes only an acetylome
entry and is excluded.

**The outer surface as the business end.** Before examining the pocket we asked, pre-registered,
which face of the assembled 78-mer evolution protects. Lumen-facing exposed residues are more
conserved than outward-facing ones (0.722 against 0.640; difference -0.081, 95% CI -0.139 to -0.026;
Spearman of conservation against transmural offset -0.206, p = 9.6e-5). The field's lumen-first
focus had the right face, and an outward-facing-interaction model is not supported.

**Our own broad module.** Protein co-abundance initially nominated a membrane-repair and vesicle
neighbourhood around MVP (50 of 101 GO terms passing a matched-query specificity test, including
plasma membrane repair, caveola and endocytosis). We then tested it twice with our own
pre-registered tests, and it failed both: against physical anti-MVP IP-MS (12 of 100 overlap against
7.4 expected, p = 0.058) and against amoeba proximity labelling (32 of 100 against 25.0, p = 0.067);
the orthogroup correction pushes the second above 0.20. We state plainly what this is and is not:
both are **failures to clear a pre-registered 0.05 line, not falsifications**, and both point
estimates are enrichments. The broad module is unsupported at the threshold we set, not disproved.
Nor is the narrow list a corrected call: ANXA2 and S100A10 have nominal IP-MS p-values near 0.002
without correction over 1,205 proteins, and CAPN2, EHD4 and IQGAP1 are absent from the IP table
altogether, so they were never tested. What we can say is that PARP4 and TEP1 are confirmed
physically and that ANXA2 and S100A10 are the strongest additional human candidates.

**We then reversed that, and then reversed it back, and both moves are instructive.** A blind review
identified a confound we had not considered: equal-protein-mass proteomics mechanically penalises a
strictly cytoplasmic complex in nucleus-dominated cells, and a housekeeping nuclear-to-cytoplasmic
proxy alone explains R-squared = 0.52 of between-lineage MVP variance. Removing it sharpened the
signal dramatically - plasma membrane repair, caveola and membrane organisation each beat all 200
size- and abundance-matched random sets (p = 0.000) while generic endosomal transport did not (p =
0.49), with PARP4 and TEP1 as ranks 1 and 2 of 8,982 proteins, and with myoferlin and the AHNAK
scaffold appearing unbidden. We recorded that as a reversal.

**It does not replicate.** Across eight independent tumour proteomic cohorts analysed separately,
the same test with the same unmodified gene sets clears 0.05 in **one of four** cohorts whose
control gates passed, with three returning p = 1.00. The pre-registered kill condition fired and the
reversal is withdrawn. One cohort reached p = 0.00 but missed its complex gate by a single
proteasome subunit, which would have moved the verdict to partial replication; we honour the gate as
written and state the closeness rather than bury it. A registered specificity test confirms the
cell-line enrichment was MVP-specific rather than a generic property of SPFH-domain proteins
(clearing for one of six other SPFH seeds), which makes it a precise result about a non-replicating
one.

**What replicates instead is the pair, not the neighbourhood.** PARP4 is MVP's rank-one correlate in
**all eight cohorts** - brain, breast, colon, glioblastoma, lung, pancreas and endometrium - after
the same residualisation, in addition to cell lines and to the original thirteen-cohort analysis.
That is the most robust quantitative finding in this work. The broad membrane neighbourhood around
it is not supported by co-abundance data, and the hypothesis one of us favoured is withdrawn with
it. Nothing here disproves a membrane association as biology: the SPFH domain, the *Dictyostelium*
tomography placing vaults on membranes, ANXA2 and S100A10 as confirmed interactors, and the
published CFTR-raft knockout phenotype all stand. What is dead is the inference from co-abundance.

**Developmental scaffolding - reported as uninformative.** This test **failed its own gate** and we
report it accordingly, because our stated rule is that a failed gate is not reinterpreted. The
pre-registration required LIN28A, LIN28B and IGF2BP1 each at or below the 10th percentile in at
least 5 of 7 organs, for at least 2 of the 3; only IGF2BP1 cleared it (LIN28A is absent from the
filtered matrix in five organs and above the 10th in both where it is measured; LIN28B clears
three). The underlying numbers do point one way - MVP rises to the 94th-95th percentile in six of
seven organs, opposite in direction to proliferation - but by our own decision rule they do not
retire the scaffold hypothesis, and we do not claim they do.

**Other eliminations.** Tissue co-expression does not track NAD metabolism (2 of 22 pathway genes in
the top 200). The phage L05 repeat 1-2 CoA pocket is not conserved in human vaults. And the proposal
that vaults are immunologically invisible is refuted by published work we found during this project:
an unbiased screen of >21,000 proteins against lupus sera places MVP in the top ten alongside Ro60
(PMID 37127324).

**Tissue and disease predictions.** Lung is not the highest-MVP tissue; it ranks fifth of 51, behind
adrenal gland and the colon-small intestine-duodenum axis. Placenta ranks 38th, retiring a
pre-eclampsia prediction by its originator's own stated criterion.

## 3. What survives

**One assembly by abundance and proximity; not by turnover or fitness.** Across thirteen
mass-spectrometry cohorts, MVP's two closest co-abundant proteins out of 10,924 are PARP4 (r = 0.82)
and TEP1 (r = 0.52). PARP4 and TEP1 stay first and second after removal of three principal
components and in 375 stroma-free cell lines. **Copy-number adjustment does not preserve the pair**,
and we previously reported that it did: on the 10 cohorts with usable copy-number data (10,077
proteins), PARP4 holds rank 1, ACTR3 takes rank 2 and TEP1 falls to rank 3. TEP1's lead was thin to
begin with - r = 0.520 against ACTR3 at 0.512 unadjusted - so the honest statement is that PARP4 is
robustly first and TEP1 is in the top three under every adjustment, not that the two are uniquely
closest. ANXA2 improves from 12 to 7 under the same adjustment, and S100A10 from 65 to 26. The same
pipeline recovers the proteasome, complex I and the ribosome from single seeds. In *Dictyostelium*,
MVPA proximity labelling places PARP4 and TEP1 orthologs among vault-proximal proteins (log2FC +3.49
and +1.61, q < 10^-4) across more than a billion years.

The association is nonetheless not a welded complex. In four of four non-dividing primary human cell
types - where pulse-SILAC half-life is pure proteolysis - **the ordering PARP4 < TEP1 < MVP holds in
every one**, though the ratio varies widely: 3.5-fold in B cells (16.0 against 55.9 h), 1.5-fold in
hepatocytes (19.4 against 29.4), 3.0-fold in monocytes (26.0 against 77.0) and 8.1-fold in NK cells
(38.2 against 310.3). The headline pair, PARP4 at 22.2 h against MVP at 66.4 h (9.8th and 58.6th
proteome percentiles), is the **proteome-table summary and not the measurement in any single cell
type**; we previously wrote it as though it were. The script's own verdict on this test is
uninformative, because the short-lived positive controls are absent from the pulse-SILAC table
entirely; the rule as written allowed the long direction to proceed, and we record the conflict
rather than resolve it silently. And across 1,178 cell lines, MVP's strongest genome-wide
co-essentiality is r = 0.205, with PARP4, TEP1 and ANXA2 ranked 9,020, 11,734 and 14,985 of 17,915.
We flag that this analysis failed its own non-essential-complex gate - CAV1 does not recover CAVIN1
or EHD2 - so it is reported as uninformative on its own and carries weight only alongside the
878-screen result.

We therefore describe the vault as **a long-lived shell whose enzymatic subunits have their own,
shorter lifetimes** - and we hold that description loosely, because the test it rests on failed its
gate. We are explicit that pulse-SILAC measures irreversible proteolysis, not a binding off-rate: a
22-hour half-life is not fast on a signalling timescale, and what the data establish is that the
PARP4 **population** does not persist for the 66-hour lifetime of the shell. This does **not**
establish that docked PARP4 leaves the shell, and we drew that inference too quickly: PARP4 is
substoichiometric on the particle, so a free cytoplasmic pool is expected, and that pool can
dominate the measured half-life while docked molecules stay for the life of the cage. Distinguishing
the two needs a pulse-chase on assembled particles, which is experiment 4 of the companion paper. On
occupancy, the published figure we can cite is an average of about 20 PARP4 molecules per
reconstituted vault, from an overexpression assembly; substoichiometric, but not a continuous coat.
This reconciles three otherwise discordant observations: co-abundance and co-localisation,
discordant degradation kinetics, and the structural placement of PARP4 on the lumenal wall at
repeats 3-4 - a patch which we find to be **less conserved than the protein average** (mean identity
0.711 against 0.730 protein-wide, both means on the full-length human-indexed alignment). This is
consistent with a low-constraint docking patch, but equally with co-divergence alongside PARP4
itself, whose orthologous group sits at the 3rd conservation percentile; we cannot separate the two.
It is not the least conserved region of the protein - repeat 7 (mean 0.640) and the C-terminal cap
disk (0.647) are both lower.

**A sequence-constrained, lumen-restricted nucleotide pocket.** Recent structures place NAD+ and
ADP-ribose in the SPFH shoulder. From two independent alignments and pipelines we find the shoulder
(residues 499-665) to be the **most conserved structural domain** of MVP. Indexed over all 893 human
residues of the same 174-sequence alignment, the shoulder has median identity 0.829 against 0.782
protein-wide (means 0.780 against 0.730); restricted to the residues resolved in the assembled
particle the same comparison gives 0.859 against 0.796. Individual barrel repeats can exceed the
shoulder - repeat 8 (377-427) reaches median 0.888 - so the claim holds at domain resolution and not
above it. F547, D566, F567 and G569 are invariant across 174 eukaryotes and K506 is at 0.987. The
conservation of this pocket was already noted by Lodwick et al. 2025; what is new here is its rank
among MVP's domains across eukaryotes. Geometric analysis of the assembled 78-mer places all 78
ligand copies within the shell wall at fractional depth 0.34, and directional probe analysis gives
zero exterior accessibility at 1.4 and 2.5 Angstrom radii, with a maximum exterior channel radius of
1.10 Angstrom - narrower than water, and therefore impassable at any larger probe. One adjacent
figure belongs in the record: in the *apo* state the 30-residue pocket does present 20.93 square
Angstroms of exterior surface at a 1.4 Angstrom probe, across six atoms. The bound ligand is sealed
from the outside; the empty pocket mouth is not quite. With a maximum exterior channel radius of
1.10 Angstrom nothing larger than a water molecule passes either way, so the conclusion stands -
this kills the transmural shoulder-pore hypothesis, cytosolic NAD+ cannot cross the shoulder wall
radially, and the pocket is loaded from the lumen - but the wall is not a perfect dielectric
boundary.

It does **not** follow that the particle must open to admit NAD+, and we initially drew that
inference in error. Lodwick et al. 2025 titrate NAD+ and ADP into 50 uM MVP by ITC and solve
ligand-occupied cages, and Osinski et al. 2026 show that purified reconstituted MVP+TEP1 particles
hydrolyse added NAD(P)+ and that an added NAD+ analogue occupies the shoulder pocket, in neutral
buffer with no activating trigger. The assembled cage has openings at the C-terminal caps, and
pre-formed vaults breathe at the waist (Collins et al. 2026). Free dinucleotides therefore reach the
lumen unaided. What requires opening is **macromolecular** traffic - PARP4 (193 kDa), TEP1 (290
kDa), vtRNA, or any ADP-ribosylated target - not the 663-Da substrate.

**MVP is dispensable, and its conservation is ordinary by our own bar.** Loss-of-function is
tolerated in humans (LOEUF 0.92, pLI 0, observed/expected 0.74; one homozygous null against 0.62
expected) while missense is mildly depleted (mis_z 2.5). Cross-species identity sits at the 89.5th
percentile against 400 groups matched on species count and alignment length, and at the **84.2nd**
against the fairer vertebrate-restricted null of 253 groups - 70% of MVP's orthologous sequences are
vertebrate. **Our pre-registered rule called "unusually conserved" at or above the 90th percentile,
so the registered verdict on this test is TYPICAL, and we report it as such.** Two things
nevertheless remain odd and are not graded by that rule: the *pocket* is invariant where the protein
is not, and whole kingdoms delete the gene cleanly rather than letting it decay. Deletable, and not
decaying.

**The LRP biomarker, resolved.** High MVP has predicted chemotherapy failure since the 1990s without
a mechanism. Across 292 cell lines with matched proteomics and dose-response, MVP predicts
resistance in 7 of 18 cytotoxics, concentrated in tubulin agents. Two candidate mechanisms die:
ABCC1 fails to predict its own substrates, and vault-RNA-binding drugs are indistinguishable from
non-binders - median rho +0.098 for the three binders against **+0.089** for the fifteen non-binders
over the deduplicated eighteen-drug list (the +0.099 we published earlier was computed on the table
that listed docetaxel twice). Mitoxantrone, the canonical vtRNA ligand, is the weakest of the three
binders measured (rho +0.064, q = 0.43). The top three drugs, and four of the top five, are
tubulin-directed; rank 4 is methotrexate, an antimetabolite. That MVP is a correlate rather than a
cause was already established genetically - Mvp-null mice and cells are not chemosensitive (Mossink
et al. 2002; Kickhoefer et al. 1998) - and vault-RNA drug binding was proposed by Gopinath et al.;
what is new is the quantitative decomposition. Across the seven drugs with matched covariates, ABCB1
absorbs a median 25.0% of MVP's coefficient and division rate 10.6%. Three precisions matter. The
samples are near-matched rather than identical - per-drug n runs 120 to 132 against 132 complete
cases, with etoposide the outlier - so we no longer describe them as identical. The two absorptions
come from **separate models**, so they are not shares of one effect and can sum past 100%. And the
apportionment is **bimodal rather than cleanly split by class**: division rate dominates for
docetaxel (67.5%), methotrexate (69.6%) and etoposide (61.5%), while ABCB1 dominates for
vinorelbine, vinblastine, paclitaxel and epirubicin. Docetaxel and paclitaxel are both taxanes and
fall on opposite sides, so the tidy "efflux substrates to ABCB1, S-phase agents to division rate"
reading we published does not survive its own data. What survives is that two passenger mechanisms,
not one, carry the biomarker, and that MVP is a passenger on both.

## 4. What TEP1 is, and why it changes the reading

Paper-length treatments of the vault routinely describe TEP1 as a structural partner. Three 2026
studies (Osinski et al.; Le Mouellic et al.; Hornebeck et al.) establish that it is not: **TEP1 is
an active, autoinhibited TIR-family NAD(P)ase** with catalytic glutamate E1008, in a STAND
architecture (TROVE-TIR-NACHT-WD40) homologous to SARM1 and APAF-1. Isolated TEP1-TIR hydrolyses
NAD(P)+ to ADP-ribose and nicotinamide; reconstituted MVP+TEP1 particles are catalytically active
and the E1008A mutant is dead. Full-length TEP1 carries a STAND (NACHT-WD40) module expected to gate
activation by oligomerisation or conformational release, but this is contested between the 2026
preprints - purified TeTIR is monomeric by SEC and crystallography, arguing against obligate
oligomerisation - and no physiological trigger or active oligomeric assembly has yet been
demonstrated. We did not generate these results and cite them because they reframe ours.

Placed beside our findings, all three ancient core proteins converge on one metabolite class inside
one sealed chamber. TEP1 cleaves NAD+ to ADP-ribose; PARP4 transfers ADP-ribose; and MVP's invariant
shoulder pocket binds ADP-ribose at 78 copies, which flips the shoulder's lumenal formal charge from
+23 e in the apo human cage to -133 e in the holo state across the 78-mer shoulder band. This is
unscreened formal charge, computed before counterions and Mg2+.

**This supplies the constraint our nineteen tests could not, and it is a published measurement
rather than an argument of ours.** Hornebeck et al. 2026 expressed the TEP1 TIR domain without its
STAND regulatory domains in HEK293 cells: cellular NAD+ fell to 30-40% of control by 24 h and the
cells died from about 20 h, both abolished by the E1008A catalytic mutation. Le Mouellic et al. 2026
report the same in *E. coli*. Full-length TEP1 must therefore be held strictly autoinhibited **in
cis** by its STAND domains - reinforced by a millimolar unactivated Km, ~6.9 mM for NADP+ and not
saturable for NAD+, against a free cytosolic NAD+ concentration two orders of magnitude lower -
while the vault shoulder concentrates the ADP-ribose product inside the lumen. One caveat on the
metabolomics, since we cite the flat NAD+ correlation: the same CCLE screen's top MVP-associated
metabolite was 1-methylnicotinamide at r = +0.41, which collapsed to a partial r of +0.038 (p =
0.47) once NNMT expression and lineage were adjusted for. The metabolomics were not uniformly null
before that confounder check, and a reader should know which result had to be discarded. Note also
that a flat bulk NAD+ correlation excludes catalysis at the scale of the uninhibited domain but
cannot exclude a slow intraluminal trickle buffered by salvage synthesis - and native brain vaults
do carry bound ADP-ribose, so some local product accumulation plainly occurs without bulk depletion.

We explicitly do **not** claim that physical separation from cytosolic NAD+ is what keeps the cell
alive. That version of the argument fails on four counts, and we state them because we held it:
Mvp-null mice and cells are viable with TEP1 protein still present and no cage to hold it; intact
vaults do not exclude NAD+; SARM1 itself sits naked in the cytosol at comparable abundance and
relies entirely on intramolecular autoinhibition; and the 10^5 figure counts vault **particles**,
not TEP1 molecules, so assigning MVP's copy number to the enzyme was a category error of ours. We
deliberately do not substitute a number: a per-particle TEP1 stoichiometry is not established in the
texts we rely on - the single-particle maps could not resolve TEP1 at all - and the figures we
circulated earlier ("one to two per particle", "fortyfold scarcer") trace to no measurement and are
withdrawn. The brake is allosteric, not architectural, and the abundance premise was never needed
for that conclusion.

So construed, the enzymology explains from independent measurement - rather than predicts - the
pattern we observed: no proliferation phenotype across 878 CRISPR screens, no basal NAD+ depletion
across 370 cell lines (MVP r = +0.077; TEP1 r = +0.098, n = 272; every sign slightly positive), **no
fitness coupling between MVP and its own partners** - PARP4, TEP1 and ANXA2 at ranks 9,020, 11,734
and 14,985 - and a ligand pocket that can only be loaded from the lumen. We correct an earlier
phrasing here: "no co-essentiality with any gene" was wrong, and contradicted by the number on the
previous page. 2,886 of 17,916 genes pass q < 0.05 against MVP, driven by n = 1,178; the defensible
claim is about the partners, not the genome. That test also failed its own gate, as noted above. A
latent enzyme held shut by its own regulatory domains should look exactly this inert at rest. The
autoinhibition was integrated after our nineteen tests were run and scored, not pre-registered
before them, and we flag that ordering rather than blur it.

It also sharpens what remains unexplained. MVP's 66-hour half-life is ordinary - the 58.6th proteome
percentile, against a median of 56.5 h - so the expense is not rapid rebuilding but the standing
cost of maintaining up to 10^5 particles of 13 MDa each at ordinary turnover, with PARP4 replaced
far faster at the 9.8th percentile, and the pocket held invariant across 174 eukaryotes. Nothing in
public data reveals what the system is held ready *for*.

## 5. Discussion

Four constraints now bound any functional model. The particle is **not required for proliferation**
- zero hits across 878 growth screens, a property shared by under 5% of genes - yet it is
**expensive**, at 10^5 copies of 13 MDa maintained at ordinary turnover, and **sequence-constrained
at a specific nucleotide-binding face** even though its overall conservation scored typical against
matched nulls. Its catalytic partner **turns over 1.5 to 8.1 times faster than the shell, depending
on cell type**, and its ligand site is **not reachable radially through the wall, and must be loaded
from the lumen**.

The fourth constraint comes from the enzymology rather than from us: **uninhibited TEP1 depletes
cellular NAD+ and kills human cells, so full-length TEP1 must be held autoinhibited in cis until
triggered.**

These are the facts a correct model must accommodate. A static container does not fit: the shell is
continuously replaced and its enzyme is replaced faster still in every cell type measured. An inert
scaffold does not fit either: the shoulder pocket is the most conserved structural domain of the
protein and binds a metabolite with invariant contacts. The combination of dispensability and
conservation suggests a system that is redundant under laboratory conditions and selected under
conditions laboratories do not impose. Under the autoinhibition constraint this stops being
paradoxical: a latent effector is *supposed* to be invisible until triggered, and nearly every
informative assay we ran sampled unstimulated growth, bulk tissue, or perturbations that do not
breach a membrane. The exceptions are real but thin - the CRISPR corpus includes 37 viral-challenge,
28 genotoxic and 9 immune-killing screens, and we tested ten-day kinase-inhibitor persisters and
eighteen cytotoxics - and none of them applies a pore-forming insult.

A pattern in our own scorecard is worth naming, and it is not the one we first wrote down. It is not
that protein-level methods succeeded and transcript-level methods failed: phosphoproteomics, the
broad co-abundance module and the proximity module all failed at the protein level, while sequence
conservation and germline missense constraint succeeded. The division we drew next - intrinsic
properties succeed, external-pathway coupling fails - also does not hold as stated, and we withdraw
the word "every" from both halves. MVP's single-cell interferon coupling at the 95th and 88th
percentiles *is* steady-state coupling to an external pathway, and it succeeded; so would the
developmental rise if its gate had passed.

The surviving generalisation is narrower and worth having anyway: **measurements of the particle's
own composition, kinetics and sequence constraint were informative, while every measurement of a
*functional consequence* in unstimulated cells was not** - CRISPR fitness, partner co-essentiality,
phospho-gated loading, bulk metabolite levels, and tissue-level autophagy and drug-metabolism
output. Abundance couples to interferon and to differentiation; consequence couples to nothing we
could measure at rest. That is the signature of a latent system.

We are careful about what the enzymology then explains. Autoinhibition accounts for the viable
knockouts, the absent growth phenotype and the flat bulk NAD+. It says nothing about the co-loss
null, the phosphorylation null, the CYP3A4 null, the tissue ranking, the LRP decomposition, or which
face of the shell is conserved. Those stand on their own, and the enzyme does not speak to them.

## 6. Limits

All human analyses are correlative and most use tumour tissue, which carries stromal and immune
content that cell lines lack and normal tissue does not share. Proximity labelling and co-abundance
report neighbourhoods, not contacts. Orthology across a billion years is coarse; we found one
annexin cloned across all thirteen human paralogs, and corrected a claim accordingly. Half-life
measurements come from four immune and hepatic cell types, not from the gut and adrenal epithelium
where the protein is most abundant. No analysis here addresses whether the vault lumen encapsulates
stress-induced nucleic-acid or protein cargo beyond vtRNA, PARP4, TEP1 and ADP-ribose. That remains
the central unanswered question and is not answerable from public data.

## 7. Primary structural and enzymological work this analysis depends on

Lodwick et al., *Nature Communications* 2025, PMID 40691181 - human vault cage with PARP4,
nucleotide ITC and cap openings; PDB 9BW6 and 9MXJ. Osinski et al. 2026, bioRxiv
10.64898/2026.05.01.722283 - TIR-like NADases in bacterial immunity and the RNA vault; TEP1
enzymology and kinetics; vault with endogenous ADP-ribose, PDB 11JB. Le Mouellic et al. 2026,
bioRxiv 10.64898/2026.09.04.749371, and Hornebeck et al. 2026, bioRxiv 10.64898/2026.09.21.753143 -
TeTIR NADase characterisation, product specificity, and the HEK293 and *E. coli* lethality of the
uninhibited domain. Geissler et al., *Nature Communications* 2026, 10.1038/s41467-026-71837-x -
*Dictyostelium* MVPA proximity labelling and membrane association. Collins et al., *ACS Synthetic
Biology* 2026;15:3975 - cargo uptake into pre-formed vaults. Anthropic 2026 - bacteriophage L05
vault structure. Musgrove et al. 2026, PMID 42031226 - crosslinked neuronal MVP RIP-seq. Mossink et
al. 2002 and Kickhoefer et al. 1998/2001 - Mvp-null mice and cells, not chemosensitive, TEP1 protein
retained. Mathieson et al. 2018 - pulse-SILAC half-lives. Benci et al. 2019 - ISG.RS and IFNG.GS.
Moadab et al. 2023, PMID 37127324 - MVP as a lupus autoantigen. We generated none of these and
depend on all of them. Where our reading of one of them was wrong - the inference that NAD+ entry
requires the particle to open - the correction is in section 3 and in `LEDGER.md` #61.

## 8. Data and reproducibility

Every dataset is public. Every pre-registration, deviation, gate and failure is committed in
sequence, and the commit history establishes that predictions preceded data access.

This paper has been wrong in public more than once, and we list the errors rather than count them
vaguely. Before review: a mediation analysis that divided coefficients fitted on different
subcohorts, reversing the ordering of two mechanisms; a cross-species comparison that matched human
gene symbols to *Dictyostelium* gene names; and an annexin orthogroup that counted one amoeba
protein as four human paralogs. Found in the first review round: a phosphoproteomics result
described from the bottom slice of a sorted table (64 rows, not 44; maximum |rho| 0.374, not below
0.11). Found by us after that round: a superlative claiming mitoxantrone was the least-associated
drug tested when it ranks fourteenth of nineteen. Found in the second review round: the inference
that NAD+ entry requires the particle to open, refuted by published ITC and soaking experiments; a
copy-number premise that assigned the vault particle's abundance to TEP1; and two conservation
figures copied from a collaborator's prose without being checked against that collaborator's own
data file. Found in the third: a claim that copy-number adjustment left PARP4 and TEP1 as the top
two partners when it moves TEP1 to third; a failed-gate developmental result reported as a finding;
a non-binder median still computed on a table with a duplicated row; "no co-essentiality with any
gene" contradicted by our own file on the facing page; and a clean drug-class split that does not
survive docetaxel. Every one is in `LEDGER.md` at the entry it belongs to, beside the original
claim, rather than silently amended. The recurring failure mode is specific and worth naming:
**describing a table instead of reading it.**
