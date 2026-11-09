# One assembly, no stoichiometric neighbourhood, and an instrument that cannot see a known subunit: a pre-registered reassessment of major vault protein across public human and comparative data

> **Title history.** The first title claimed *"three lifetimes"* (removed, §61b: compatibility
> never tested). The second claimed *"a sealed nucleotide pocket"* — removed here, because §73 found
> that pocket **published** (Lodwick et al. 2025) and **not sealed**: it is lumen-facing,
> inter-subunit, and created by assembly. **Twice the title headlined something that was not ours or
> not true.** This one headlines the well-controlled negative and the calibration finding, which are.

**Graham W. Syfert.** Analysis performed with Claude (Anthropic). Two further language-model agents
reviewed the manuscript adversarially against the committed data, in three rounds; between them they
struck or qualified more than a dozen claims made here, and those reversals are recorded in place
rather than quietly removed. All hypotheses were committed to a timestamped git history before the
relevant data were read; every gate, deviation and failure is recorded in `LEDGER.md` (415 entries, ids 1-417 with 89 and 90 unused)
and `RESULTS.md` (24 sections). **That history is currently local and has not been published**, so
the ordering it establishes is not yet independently verifiable; we state the fact rather than imply
otherwise, and the repository is available to anyone who asks. Correspondence welcome, including
corrections.

---

## Abstract

The vault ribonucleoprotein has resisted *consensus* functional assignment for forty years — a
framing we used, wrongly, as licence to assume a thin literature.
**It is not thin.** Four structure papers appeared in 2025-2026 alone, alongside a functional
literature of knockout studies running from 2019 to 2025, and an active structural group is
publishing on the same questions asked here. **All five literature checks this project eventually
ran found prior art**, including one whose answer sat unexamined in our own downloaded structure
files (§73d, §74). We subjected the major vault protein (MVP) and its partners to forty-odd
pre-registered tests across public transcriptomic, proteomic, genomic, structural and comparative
datasets, each gated on recovery of a known positive control.

**One positive measurement survived all of it.** In the lineages that retained MVP, the gene is under
**strong purifying selection**: dN/dS = **0.1118** across seven one-to-one mammalian orthologues
(0.0850-0.1244), **above every one of four essential-gene controls** (0.0031-0.0771) and **below every
one of three rapidly-evolving controls** (0.2166-0.5578). We first refused this number on a gate
technicality and an external methods audit reversed us (§84a-b, house rule 15). **It sharpens the
forty-year paradox rather than resolving it:** a gene deletable from a mouse without obvious
consequence, and discarded outright by two major clades, is **actively conserved wherever it
survives.** Something is paying to keep it, and the payment is not visible in a dish.

**One framing correction belongs at the front, because it changes what every negative result below
means.** We set out to find MVP's physical interaction neighbourhood and did not find one, by any
instrument. We then discovered a substantial published literature — knockout work across six papers whose convergence is **mostly one group's** (Jingjing Ben on five of
the six; only the influenza study is authorially independent, §76b) — establishing MVP as a **modulator
of signalling**: IKK-NF-kB in diet-induced obesity and atherosclerosis, calcineurin-NFATc1 in
osteoclastogenesis, STAT3 in lung cancer, Parkin-mediated mitophagy in endothelium, and adaptive
immunity on influenza rechallenge. **Those interactions are transient, low-stoichiometry and
regulatory — the class that co-abundance, native co-fractionation and wash-based immunoprecipitation
recover worst.** So the absence we document is not evidence against function. It is a
well-controlled demonstration that **MVP has no stoichiometric partner complex beyond PARP4 and
TEP1**, which is a real and narrower result, obtained with instruments that were wrong for the
question the field is actually asking.

**A second correction follows from the same literature.** Every published vault phenotype is
conditional: MVP-knockout mice are healthy, mice lacking all three vault proteins are phenotypically
normal, and knockout zebrafish regenerate normally — with defects appearing only under influenza
rechallenge, high-fat diet, injury, ageing, oestrogen withdrawal, or *Dictyostelium* nutrient
starvation. **Our own "no fitness coupling" came from CRISPR screens in rich medium, which is the
one condition in which every published model is also normal.** We read *no function in the single
environment we examined* as *no function*. **Eight of the twenty-eight returned a formally
uninformative verdict because a control gate failed, and we mark each one rather than promote it.**
Most standing hypotheses nonetheless failed on tests that did gate: MVP is not a member of the
chronic interferon resistance program; no gene family is co-lost with it across 472 eukaryotes;
NSUN2 does not repress CYP3A4 in human liver; and phosphorylation does not gate vault assembly or
partner exchange. Drug-tolerant persistence and tissue-level autophagy gating both pointed the same
way but failed their gates, so we report them as uninformative.

What survives is narrow. MVP, PARP4 and TEP1 are mutually closest by protein co-abundance - PARP4
and TEP1 at ranks 1 and 2 of 10,924 proteins across thirteen tumour cohorts, and PARP4 first with
TEP1 third after copy-number adjustment - and all three are vault-proximal in *Dictyostelium*. They
are not a welded complex: the ordering PARP4 < TEP1 < MVP holds in four of four non-dividing primary
human cell types, with ratios from 1.5- to 8.1-fold, though that test also failed its gate. We
resolve the thirty-year LRP chemoresistance biomarker as a passenger phenomenon carried by two
separate mechanisms, ABCB1-mediated efflux and slow division, which do not partition by drug class.
In native co-fractionation across 411 datasets, where symmetric scoring and a size axis replace
sample covariation, MVP's highest-scoring partner of 10,614 is PARP4 at the 99.99th percentile, with
a profile matching flotillin-1's obligate heterodimer rather than a multi-subunit machine; TEP1
scores at the noise floor in the same data, so sensitivity for known vault subunits there is one of
two.

**The most useful result in this work is a negative one about method, and we reached it only after
publishing three wrong versions of it.** One question - whether cytoplasmic translation machinery is
physically associated with the vault - returned a different answer from every statistical treatment
we tried. Dichotomising at a significance threshold gave a null (9 of 95 proteins against 6.94
expected, p = 0.195) and we recorded a kill. The continuous mean the cut had discarded gave a strong
positive: the 95 translation proteins detected in that pulldown average **+0.228 log2 against -0.316
for the other 1,110**, a shift at the **99.8th percentile of abundance-matched draws, p = 0.004**,
ranking **23rd of 1,276 terms**. We withdrew the kill. Then a matched control on protein **length
and net charge** returned the null again, and we withdrew the positive.

**That third control was degenerate, and we did not notice for two sections.** Matching on three
decile axes at once divides 1,166 proteins among up to 1,000 cells: **578 cells are occupied, 49% of
them hold exactly one protein, and the median is two.** The "matched random draw" was sampling pools
of one to three proteins that routinely included the term's own members. **MVP's own cell contains
MVP and one other protein**, so the control we cited as proof the matching discriminated was drawing
the test subject into its own null. Every p-value from that machinery is void. **What survives is
the one-way abundance-matched comparison, where ten cells hold about 117 proteins each** - so the
+0.544 log2 class shift stands, and never depended on the broken control.

The single clean positive exclusion in this work is **myoferlin**, depleted both in the pulldown
(-2.23) and in pre-lysis covalent proximity labelling (-3.32, p = 3.4e-4), an instrument no wash
artefact can reach - and myoferlin had been our strongest membrane-repair evidence. Cortical actin
is unresolved: our exclusion rested on a co-elution cutoff that also excludes TEP1, a real subunit
this pulldown recovers at log-p 3.33. We also withdraw two earlier readings: an enrichment test
against a partner set of size one has no power, and a container metaphor is one of six models
producing the same graph. **What survives unchanged is the particle itself** - a 78-mer shell, PARP4
and TEP1 each independently associated, and subunit half-lives of 22.2, 40.6 and 66.4 h whose
mutual compatibility we never tested and do not claim — figures whose three decimals are false
precision against their own 22.6% CV bar, about +/-15 h on the MVP estimate (§75). **The nucleotide
pocket is NOT on this list:** it is published (Lodwick et al. 2025, *Nat Commun* 16:6724) and it is
**not sealed** — lumen-facing, inter-subunit, created by assembly (§73).

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

**The gate scorecard, stated up front.** The enumeration in this section covers the first
thirty-three registered tests. A further nine were registered and run afterwards and are itemised
individually in the ledger with their own verdicts, including two that returned EQUIVOCAL or
UNINFORMATIVE on gates we had designed badly and one whose control we later invalidated ourselves;
we do not restate a running total here, because every later verdict is tabulated at its own ledger
entry and a summary figure would go stale faster than it informs. Of those first thirty-three tests,
twenty-two returned an informative verdict with their positive controls recovered; **eight carry a
formal verdict of UNINFORMATIVE in their own committed output**; and three passed partially - the
CRISPR corpus, where the genotoxic screen class failed its control while viral and immune-killing
classes passed; the LRP decomposition, where ABCC1 failed to predict its own substrates; and the
SMC5/6 test, whose primary multiple-testing arm was informative while its specificity control turned
out to have no power to fail (see below).

**Three further tests were declined before registration rather than run**, because a presence check
showed they could not discriminate: a BioPlex replication of the physical interactome (seven of
MVP's eight partners there were never detected in our IP-MS, so non-replication would have been
guaranteed by non-detection); a CRL4 assembly test for COP1 (four of six complex components
undetected); and a sequence scan of MVP for a COP1 VP degron (the motif is sequence-divergent with
no per-position consensus, and known substrates lack it entirely). We count these separately from
the thirty-three because nothing was computed.

The eight, each with the control that failed: co-essentiality (CAV1 fails to recover CAVIN1 or
EHD2); developmental trajectory (two of three stemness markers absent or above threshold);
drug-tolerant persistence (a proliferation control undetected in one model); subunit turnover
(short-lived controls absent from the pulse-SILAC table entirely); the Vaultrc5 knockout (the
transcript is undetected in brain); an epithelial-mesenchymal control (we required E-cadherin to
anti-correlate with an extracellular-matrix-dominated signature at a threshold it does not reach); a
proximity-labelling contact test (MVP is absent from the relevant bait's run, which is the
second-shallowest of seventeen); and a transcriptional-licensing test (we adopted a transcript-level
coherence threshold for protein data without checking it was reachable, and it is not reachable even
before adjustment).

**Three of those eight failed because we designed the gate badly rather than because the data were
uninformative**, and we say so because it is the largest single source of wasted effort in this
work. A fourth gate-design error is recorded in the partial column: in the SMC5/6 test we required
that fewer than two of cohesin and condensin's subunits be vault interactors, and all four turned
out to be absent from that instrument's detected proteome, so the control returned PASS and the PASS
carried no information. **A control that cannot fail is worse than no control, because it launders
an untested claim as a checked one.** The house rule added in response - confirm every named control
protein is present in the data a test will read, before committing the registration - immediately
stopped the three declined tests above.

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

**And a native instrument settles it.** Because co-abundance cannot separate physical association
from shared regulation, we turned to co-fractionation mass spectrometry: 411 harmonised native
separations across 21,703 fractions, no detergent immunoprecipitation and no wash-off step, and
critically a method in which an intact 13 MDa particle cannot co-elute with free monomers by
accident. Its controls recover 34 proteasome subunits from PSMA1 and 77 ribosomal proteins from
RPL7.

**In that resource MVP has exactly one high-confidence partner in the human proteome, and it is
PARP4. PARP4 has exactly one, and it is MVP.** The two are reciprocally exclusive. For scale, the
same data assign PARP1 133 partners and ANXA2 27 - so ANXA2 is well measured and well connected
there, and simply not connected to MVP. Every membrane and innate-immune gene set returns **zero**
MVP partners against degree-matched random sets. The one apparent exception, a single hit in
inflammatory response, is PARP4 itself, which carries that annotation while MVP does not.

This is the sixth independent instrument to recover MVP-PARP4 and the first with a size
discriminator, which makes the pair about as firmly established as anything in this work. It also
ends the broad neighbourhood as a physical claim, on a well-powered negative rather than an
ambiguous one.

**We drafted a container reading of that absence and an external reviewer killed it, correctly.** A
sealed obligate container, an inert homooligomer, an RNA-binding particle, a partially occupied
vault, a transient interactor, and a protein measured just well enough to return its one database
edge all produce an isolated dyad. Two further objections hold: co-fractionation scores are
symmetric, so "reciprocal" was free, and an enrichment test against a partner set of size one has no
power, so the membrane and immune nulls here are uninformative rather than well-powered. All three
claims are withdrawn.

**What the full score distribution does support is narrower and better controlled.** Across all
10,614 of MVP's scored pairs, PARP4 sits at the 99.99th percentile with twice the score of rank two,
then a smooth plateau - a cliff, not an artefact of where we cut. The instrument's own calibration
places that profile precisely: PSMA1 returns ten partners at precision 1.00, flotillin-1 returns its
obligate heterodimer partner flotillin-2 at 0.60 followed by a drop, and MVP returns PARP4 at 0.68
followed by a drop. **MVP-PARP4 has the signature of a binary complex rather than a multi-subunit
machine.** Against that, TEP1 - a known subunit - scores 0.04, so sensitivity for vault components
here is one of two and the absence of further partners comes from the same process that lost TEP1.

The honest statement: MVP has no detectable co-eluting neighbourhood beyond a binary-complex-grade
PARP4 edge, in an instrument that demonstrably misses one of the three subunits we already know
about. Ranks two to twelve, below our threshold and unexamined until the reviewer asked for them,
are translation and RNA-handling proteins - ZNF598, RPL8, EIF3A, UPF1, ZC3HAV1 - which is neither of
the neighbourhoods we had been arguing about and is consistent with polyribosome templating.

**We then pursued both of those leads to their ends, and the shape of both failures is the paper's
main result.**

**Cortical actin.** Removing the interferon axis from the co-abundance scan - residualising on STAT1
and IRF9 until the canonical target TAP1 is displaced out of MVP's top 200 in five of five datasets
- collapses the immune signal to the central nervous system alone and leaves membrane ruffling and
actin filament organisation standing in endometrium and in cell lines, which contain no immune
system. Those two then survive the control we expected to kill them: against 200 size- and
abundance-matched random sets, actin organisation clears in three of three
non-central-nervous-system datasets and ruffling in two plus a borderline, with ruffling at 13
observed against 3.1 expected. Mitochondrion, the largest abundant cytoplasmic compartment, is not
enriched anywhere, so this is not what abundance buys.

**And it is not physical.** In the native co-fractionation data, all twenty-five cortical actin
proteins we checked are present with partners - cofilin-1 has 170, beta-actin 128, gamma-actin 117 -
totalling 1,175 high-confidence edges, and **not one connects to MVP**. That is a well-powered
negative rather than missing data. The covariation is real and reproducible; the association is not
there.

**Translation.** MVP's sub-threshold co-elution tail is enriched eighteenfold for cytoplasmic
translation, and that enrichment is specific to MVP: at the 98th percentile of 150 comparable seed
proteins, where five abundant glycolytic enzymes span the 26th to 79th percentile and MVP's own
SPFH-family relatives - flotillin-1, flotillin-2, stomatin - sit at the 60th, 70th and 41st. We
registered the expectation that this would prove generic and were wrong on both counts.

**And it too is not physical.** An anti-MVP immunoprecipitation that recovers all three vault
subunits - MVP, PARP4 and TEP1, each at a log-p above 3.3 - shows no enrichment for translation
among its 88 interactors (9 observed against 6.94 expected, p = 0.195), nor for ribosome, actin or
mitochondrion. That test is only powered for a large effect and we say so; it is not a clean
refutation. But the registered rule was applied as written.

**And then an adversarial review took both of those conclusions apart.** The exchange is in the
repository (`grok/`), and the computation it demanded is the most consequential in this work.

**The translation question took three treatments to settle, and we published the first two.** Asked
by a reviewer for the number our hard cut had discarded, we computed the mean enrichment of *all* 95
detected translation proteins rather than counting how many crossed a line: **+0.228 log2 against
-0.316 for the other 1,110**, at the 99.8th percentile of abundance-matched draws. We withdrew the
kill. Then, reading our own unbiased scan more carefully, we found that the **mitochondrial** large
ribosomal subunit scored **+0.560** against the **cytosolic** ribosome's **+0.272**, while the
mitochondrial compartment as a whole was flat. Mitoribosomes sit behind two membranes; a cytoplasmic
13 MDa particle cannot be bound to them, so the enrichment was tracking *"is a ribosomal protein"*
rather than any location.

Ribosomal proteins are **2.6x shorter than the median detected protein (160 against 418 residues)
and 44x more basic (+130 against +2.94 charge units per 1,000 residues)** - the profile of something
that sticks to an affinity matrix. Matched on length and charge decile as well as abundance,
**cytosolic ribosome gives p = 0.309 with a matched null of +0.229 against an observed +0.272**;
cytoplasmic translation p = 0.174; ribosome p = 0.184. The matched null reproduces the observation.
**The contact corroboration is withdrawn.** What survives is §40's co-elution result, which this
does not test: MVP's sub-threshold tail at the 98th percentile of 150 comparable seeds, a
*seed-level* specificity that a promiscuous physicochemical property does not obviously explain,
since promiscuous small basic proteins should populate every seed's tail rather than MVP's
preferentially.

**One arithmetic point we had also missed:** the largest fold-enrichment this pulldown can express
is 88/6.94 = **12.7x**, so the 18x co-elution figure the kill was supposed to adjudicate was never a
quantity that test could have returned.

**We then spent two further tests trying to explain away the co-elution result and could not.**
Co-fractionation separates by apparent mass, and a 13 MDa 78-mer might share fractions with
polysomes without touching them - so we compared MVP against 35 seeds drawn from seven assemblies of
known mass.
**Mass does not order the result and is close to inverting it:** the 110 MDa nuclear pore complex
sits at the **26th** percentile and the 1.4 MDa dynein complex at the **96th**, with MVP at 98.0.
The second test asked whether a seed's own size and charge explain its tail, as they explained the
contact result. **Length does organise these tails** - Spearman ρ = **−0.294**, p = 0.0003, shorter
seeds having richer ones - **and charge, the property that killed the contact result, is irrelevant
here** (ρ = +0.077, p = 0.355). Two instruments, two different nuisance axes. Against that trend,
MVP is **893 residues, longer than 80% of eligible seeds**, and among its thirty nearest neighbours
in size-and-charge space - median length 768, median charge −17.2 - the neighbours' median fold is
**1.38x** and their best is **9.84x**, while MVP is **18.49x**. It exceeds every seed that resembles
it.

**We decline to promote it anyway, and the reason is a rule we wrote badly.** Our registered
condition for calling this result strengthened required *charge* to correlate with fold; the axis
that mattered turned out to be length, which we had not anticipated, so the registered verdict is
that nothing is promoted. Substituting the axis after the fact - immediately after a registered rule
declined to promote - is the error this work has already made twice. So the status of the one
translation result still standing is: **five specific alternatives eliminated** (degree, abundance,
family membership, apparent mass, seed length and charge), **no contact corroboration**, and a
residual lift in cytoplasmic assemblies to a median 70th percentile whose cause we cannot name. Five
eliminations and no promotion is the intended output of a method built to make promotion hard.


**The actin exclusion has no positive control.** Its load-bearing number was zero high-confidence
co-elution edges from MVP to twenty-five actin proteins. But TEP1 - a stoichiometric subunit this
same pulldown recovers at log-p 3.33 - sits at co-elution precision **0.041**, and any cutoff
retaining TEP1 retains **1,733** MVP partners, the entire noise floor. At the cutoff we used, MVP
has **zero** partners of any kind. The zero describes our threshold, not the vault. Cortical actin
is **unresolved**.

**And the length-and-charge control that appeared to settle the translation question was
degenerate.** An adversarial reviewer accepted the control in principle, on the condition that the
proteins drawn from those decile cells were not the label under another name. Testing that condition
revealed a more basic failure: the three-way decile cross divides 1,166 proteins among up to 1,000
cells, leaving **578 occupied cells at a mean of 2.02 proteins, 49% of them singletons.**
Restricting donors properly
- removing the term's own members and their annotation neighbours, and requiring thirty usable donors
per cell - returns **NON-IDENTIFIABLE for all three terms tested, with a median of zero usable
donors.** The control never had a population to draw from, and the gate we cited in its defence had
**MVP sharing a cell with exactly one other protein.** Every p-value from that analysis is
withdrawn; the one-way abundance-matched result, with about 117 proteins per cell, is unaffected.

**What survives is one exclusion, and it is a good one.** Myoferlin is depleted in the pulldown
(-2.23) *and* in pre-lysis covalent proximity labelling around PARP4 (-3.32, p = 3.4e-4), an
instrument no wash artefact can reach - and §43 establishes that PARP4 is on the particle, its
knockdown leaving MVP untouched, so proximity to PARP4 is proximity to the vault. Myoferlin was the
single most canonical membrane-repair protein that arrived unbidden in our scan, and two instruments
of different physics agree it is excluded.

**So the honest generalisation is narrower and more uncomfortable than the one we published this
morning.** It is not that co-migration was mistaken for contact three times. It is that **we twice
built a gate with only one reachable answer - a specificity control whose proteins were absent from
the instrument, and a kill condition that returned "kill" for every plausible moderate effect - on
the same day, in opposite directions, and then believed the gates over the data.** The one
association appearing in both instrument classes remains MVP with PARP4 and TEP1, which come down
together in that pulldown.

**An unbiased scan, and what it cost us.** Because every co-abundance test to this point had begun
by nominating a module we already favoured, we inverted the procedure: scan all 8,634 Gene Ontology
terms against MVP's top 200 correlates in five independent proteomic datasets, each residualised on
a nuclear-to-cytoplasmic proxy and proliferation, and require replication in a majority. We
registered a prediction that zero or very few terms would replicate. **One hundred and three did**,
and the module was innate immune - antigen processing, cytokine production, inflammatory response,
response to bacterium, membrane ruffling and actin organisation. The design gate passed: the same
scan seeded with PSMA1 recovers the proteasome.

That result then weakened substantially under external review, and the corrections matter more than
the finding. The 103 terms are overlapping branches of one ontology, approximately **two**
independent signals rather than 103. Two of the five datasets are the same tissue - brain and
glioblastoma - so the apparent four-of-five replication is central nervous system counted twice,
plus endometrium, plus cell lines. And the colorectal cohort, which we had treated as uninformative
because it returned q = 1.000 throughout, **recovers six of seven proteasome terms from a PSMA1 seed
with five at q = 0.0000**: it has ample power, it is the tissue where the vault holoenzyme is most
abundant, and it is therefore a real counterexample rather than a dead dataset. We were
cherry-picking around it.

What survives is a reproducible covariation, in cells with no immune system, between MVP abundance
and a cell-autonomous innate-immune program. Partialling on STAT1 and IRF9 removes roughly 45% of it
and leaves the rest (MVP-B2M falls from +0.426 to +0.270, MVP-TAP1 from +0.380 to +0.216, both p <
1e-4), so it is neither a pure re-description of the interferon regulon nor clearly more than one.
MVP is an interferon-gamma-inducible gene, and correlational data cannot separate effector from
co-regulated passenger. We also note, having initially set it aside because it did not fit an immune
reading, that membrane ruffling and actin organisation replicate at exactly the same bar - and that
unlike the immune terms, they are not predicted by interferon inducibility.

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

### Two standing qualifications on everything in this section

**First, the provenance of every interactor number below.** They come from one dataset: **PRIDE
PXD052802**, co-immunoprecipitation of MVP with the synthetic antigen binding reagent **VM1**
against control **H6**, in **wild-type versus PARP4-knockout A549 cells** — a lung adenocarcinoma
line, for a protein historically named lung resistance-related protein. **The deposit's own
description analyses the same WT-versus-knockout contrast we use**, so the enrichments reported here
are readings of a public dataset rather than discoveries of this work, and they may be specific to
that cell line. "Not PARP4-dependent" below should everywhere be read as **"still present when PARP4
is removed in A549"** rather than as independence in general.

**Second, what the absence of a neighbourhood does and does not mean.** The published vault function
is **signalling modulation** — IKK-NF-kB, calcineurin-NFATc1, STAT3, Parkin-mediated mitophagy,
adaptive immunity on influenza rechallenge. **The convergence is mostly one group's** — Jingjing Ben
appears on five of the six papers, and only the influenza study shares no author with any other, so
this is one programme plus one independent replication rather than six independent results (§76b).
Those interactions are **transient, low-stoichiometry and regulatory**, which is the class
co-abundance, native co-fractionation and wash-based immunoprecipitation recover worst.
**So nothing below is evidence against vault function.** What survives is the narrower and still
useful claim that
**MVP has no stoichiometric partner complex beyond PARP4 and TEP1.** Section 70 sets this out in
full; it is repeated here because a reader meeting the interactor tables for the first time needs it
at that point, not sixty sections earlier.

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

**This supplies the constraint our twenty-eight tests could not, and it is a published measurement
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
autoinhibition was integrated after our tests were run and scored, not pre-registered before them,
and we flag that ordering rather than blur it.

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
