# What a wet lab should do next with vaults: fourteen experiments, ranked by what they decide

**Graham W. Syfert**, with Claude (Anthropic) and two independent reviewing agents. Companion to
`PAPER1_vault_reassessment.md`. Written for a group with a working vault purification pipeline.

**Why this document exists.** We ran twenty-eight pre-registered computational tests against every
public dataset we could reach. Eighteen returned an informative verdict with their positive controls
recovered, eight are formally uninformative because a control gate failed, and two passed partially;
the companion paper names each one, including the three where the gate was badly designed rather
than the data uninformative. Between them they eliminated most standing hypotheses and left four
constraints that no public dataset can resolve further. Everything below requires a bench. Each
entry states what it decides, the minimal design, the positive control, and the result that would
kill the idea - including ours.

**The four constraints any experiment should respect:**
1. The nucleotide pocket in the SPFH shoulder **cannot be reached radially through the shell wall**
and must be loaded from the lumen (zero exterior probe access at 1.4 and 2.5 Angstrom in the
assembled 78-mer; maximum exterior channel radius 1.10 Angstrom, narrower than water). This does
**not** mean the particle must open to admit NAD+: published ITC and soaking experiments show free
dinucleotides reaching the pocket of intact cages in neutral buffer, via the C-terminal cap openings
and waist breathing. Opening is required for **macromolecular** traffic - PARP4, TEP1, vtRNA,
ADP-ribosylated targets - not for the 663-Da substrate. We held the stronger claim and were wrong.
2. **PARP4 turns over faster than the shell in four of four non-dividing primary human cell types**,
by 1.5-fold in hepatocytes up to 8.1-fold in NK cells, so these are pure proteolysis rates. The
often-quoted pair 22.2 h against 66.4 h is the proteome-table summary, not any one cell type's
measurement. Two cautions carry over from the companion paper: this test failed its own gate - the
short-lived positive controls are absent from the pulse-SILAC table - and pulse-SILAC measures
degradation, not off-rate, so a free cytoplasmic pool may dominate the number while docked molecules
persist. Experiment 4 below is what would settle it.
3. The particle is **dispensable for proliferation** (zero hits in 878 growth screens) yet
**sequence-constrained** at the pocket (four residues invariant across 174 eukaryotes). Whatever
selects it does not operate in a dish.
4. **TEP1 is a latent, autoinhibited TIR-family NAD(P)ase (E1008), and the uninhibited domain is
lethal in human cells** - expressed without its STAND regulatory domains it drops cellular NAD+ to
30-40% of control and kills HEK293 cells, both abolished by E1008A. The brake is **in cis**,
allosteric, reinforced by a millimolar unactivated Km; it is not the cage. The 10^5 figure counts
vault particles, not TEP1 molecules; a per-particle TEP1 stoichiometry is not established in the
texts we rely on, and the conclusion does not need one. Nearly every assay in our computational work
sampled unstimulated growth or bulk tissue, which is precisely when a latent effector is designed to
be invisible. **The experiments below are therefore ordered by how directly they perturb the system
out of that resting state.**

---

## Tier 1 - decides the most, costs the least
*(Order revised after adversarial review: perturbation experiments first, since the resting state is
uninformative by design. Experiment numbers are retained as stable identifiers; the sequence below
is the recommended running order.)*
### 2. Does membrane breach trigger TEP1 NADase activity?
**Decides:** our single most specific joint hypothesis, assembled from two literatures that had not
met.
**The convergence:** TEP1 is an autoinhibited TIR-family NAD(P)ase (E1008 catalytic) whose STAND
module is expected to gate activation, though obligate oligomerisation is contested between the 2026
preprints and no physiological trigger has been demonstrated. The published work notes that vaults
confer resistance to *Pseudomonas aeruginosa* and influenza A and speculates that TEP1 may be an
innate-immune executioner, but no study connects that to pore-forming toxins or to membrane-wound
repair.

**We must be accurate about how weak the priors actually are, because we previously overstated them
both.** Kowalski et al. (*Science* 2007;317:130) did not show that MVP-null mice "die of
*Pseudomonas*": after an experimental intranasal inoculum, nulls carried roughly 3.5-fold more lung
bacteria and had a hazard ratio for death of 2.96 (n = 15 null against 17 wild type, 96 h), and the
mechanism they proposed was failed epithelial internalisation following CFTR-dependent raft
recruitment. The mice are healthy in ordinary housing. Nor is the *Listeria* link a pore-forming
one: InlK, the listerial protein that binds MVP, is a surface protein that coats the bacterium to
evade autophagy, and it is **not** listeriolysin O. Writing "both pore-forming toxins" conflated an
organism with a toxin and InlK with LLO.

What genuinely remains is thinner and still worth a bench: MVP is implicated in two
bacterial-defence settings by independent groups, its co-abundant neighbours include ANXA2 and
S100A10 - the canonical membrane-wound-repair heterotetramer - and nobody has tested a pore-forming
insult against TEP1 at all. The experiment is motivated by the untested gap, not by a published
convergence.
**Design:** sterile streptolysin-O versus live *Pseudomonas*, in wild-type, **MVP-null**,
PARP4-knockout and TEP1-E1008A knock-in cells. Targeted LC-MS/MS over 0-120 min against authentic
standards, monitoring **NAD+, NADP+, linear ADP-ribose, 2'-phospho-ADP-ribose, nicotinamide, and
cyclic ADPR**.
**A product-panel warning that would otherwise cause a false negative.** TIR NADases differ in what
they make. The published characterisations report TEP1 generating **linear ADP-ribose and
nicotinamide** (and 2'-phospho-ADPR from NADP+), whereas **SARM1
- the obvious positive control - does generate cyclic ADPR**. Monitoring cADPR alone would therefore
miss TEP1 entirely while lighting up the control, and injury itself activates SARM1 and CD38.
Monitor the full panel and include a SARM1 inhibitor or knockout arm so the two enzymes can be
separated. The cADPR-negative result for TEP1 is verbatim in the primary text and independently
stated by a second group.
**Positive control:** SARM1 activation by vacor or CZ-48 in the same assay, read on the same panel.
**The discriminating signature:** TEP1 activation predicts a rise in **linear ADPR + 2'-P-ADPR +
nicotinamide with no cADPR rise**, abolished in TEP1-E1008A.
**Kill condition:** NAD+ is unperturbed by membrane wounding in wild-type cells while the SARM1
control depletes normally. That kills the breach-trigger model cleanly.

### 3. What opens the shell?
**Decides:** constraint 1 above, and the born-loaded versus loaded-on-demand fork.
**Why now:** free NAD+ *does* reach the pocket of intact cages - that is constraint 1, and it is why
this experiment is no longer about admitting NAD+. What is unknown is the **door and the traffic
rule**. Published work shows access under the conditions it tested, not the route: the
single-particle maps never resolved the opening that nucleotides use, and a 663-Da metabolite
entering unaided says nothing about whether PARP4, TEP1 or vtRNA can follow. Pre-formed vaults do
take up intact AAV capsids, which is macromolecular traffic and is the size class this experiment is
about; we previously cited that result as evidence for small-molecule entry, which mixes the two
classes the constraint exists to separate. The open question is what governs macromolecular exchange
and whether pocket occupancy turns over at all.
**Design:** low-pH opening is already published, so test **physiological** triggers: pH 6.0-7.4,
Ca2+ 0.1-100 uM with and without ANXA2/S100A10, vtRNA, mechanical shear, pore-forming toxin. Do
**not** read this out as labelled-NAD+ uptake: free NAD+ already reaches the pocket of intact cages
at baseline, so that assay is saturated before the experiment starts. Read out **macromolecular**
traffic instead - uptake of labelled PARP4-MINT or of exogenous vtRNA into pre-formed cages - and,
in parallel, the **off-rate of pre-bound ADP-ribose from native holo-vaults**, which reports pocket
exchange rather than pocket filling. Use wild-type against pocket mutants (F547A/D566A) rather than
a bulky lumenal sensor that would itself change lumenal crowding. Pair with cryo-EM or HS-AFM on the
same conditions.
**Positive control:** low pH, where opening is already published, must produce the macromolecular
uptake the physiological conditions are being tested for - otherwise a null across the physiological
panel is uninterpretable.
**Kill condition:** no physiological condition increases macromolecular occupancy above baseline and
no condition accelerates ADP-ribose release, with the pocket mutant indistinguishable from
wild-type.

### 1. Stressed Trap-and-Seq: what is actually inside a vault?
**Decides:** the containment hypothesis, and roughly half the candidate disease list.
**Why now:** the claim that vaults contain a single small RNA rests on a 1986 gel and a 2001
Northern blot on unstressed mouse liver, and a Northern blot cannot discover an unknown RNA. The one
modern attempt - Musgrove et al. 2026 neuronal MVP:eGFP RIP-seq - recovered Vaultrc5 plus hundreds
of mRNAs but used 1% formaldehyde crosslinking **without a nuclease shave**, so exterior
ribonucleoprotein sticking cannot be distinguished from sealed lumenal cargo. That is exactly the
gap this design closes.
**Design:** cells with high native vault expression, wild-type and MVP-null in parallel. Block
autophagic turnover (bafilomycin A1, 2 h). Four arms: vehicle; a genotoxic agent; UV-C or etoposide;
transfected nuclear-targeted synthetic dsRNA. 60-120 min, short of death. **Do not crosslink whole
cells first** - formaldehyde tethers cytosolic RNA to the barrel exterior and blocks complete
digestion, recreating the artefact above. Lyse gently in cold isotonic buffer, isolate intact native
particles, **nuclease-shave the uncrosslinked shells** with benzonase/RNase/DNase, then lyse the
shaved vaults. Rapid size-exclusion plus anti-MVP capture. Sequence small RNA and DNA at modern
depth.
**Power argument that has not been made:** at 10^5 vaults per cell, even 1% carrying a non-vtRNA
cargo yields ~10^3 molecules per cell - comparable to a moderately expressed mRNA, and trivially
detectable now. The cargo need only be rare **per particle**.
**Positive control:** spiked exogenous RNA must be destroyed by >=99.9% while endogenous vtRNA1-1
survives the same shave. That single control is what separates cargo from passengers.
**Kill condition:** a clean nuclease-protected profile under stress, at modern depth, with nothing
but vtRNA. That would close a question open since 1986 and is publishable as such.

---

## Tier 2 - resolves a specific published contradiction
### 4. What drives PARP4 exchange?
**Decides:** the mechanism behind constraint 2, which we could not touch computationally.
**What we ruled out:** MVP phosphorylation. Across six phospho-bearing CPTAC cohorts, no MVP
phosphosite predicts per-vault PARP4 loading: 0 of 62 tests reach q < 0.05, and the strongest raw
association (rho = -0.374, p = 0.001) fails to replicate across the six cohorts measuring that site.
**Design:** pulse-chase PARP4 on assembled vaults while varying lumenal ligand occupancy (NAD+,
ADP-ribose, non-hydrolysable analogues), ionic strength and MVP abundance. Does ligand occupancy set
residence time?
**Positive control:** the free and particle-associated PARP4 pools must separate cleanly on the same
gradient, and a subunit of known permanent residence - MVP itself - must show no exchange in the
same chase. Without that separation this assay cannot distinguish pool turnover from docked
exchange, which is exactly the ambiguity it exists to resolve.
**Kill condition:** PARP4 residence is invariant to lumenal occupancy.

### 5. Does TEP1 bind misfolded noncoding RNA, as its only paralog does?
**Decides:** whether the TROVE domain means anything functional, and the Ro60 comparison.
**Design:** express the TROVE-vWA fragment rather than full-length TEP1 (the p80 homology region
suffices for vtRNA and particle association). EMSA against vtRNA (positive), Y RNA, correctly folded
5S rRNA, and misfolded 5S precursor - Ro60's known substrate. Competition: does vtRNA block access
as Y RNA does for Ro60?
**The addition that makes this worth doing now:** generic TEP1 RNA-binding EMSA was partly done in
2002. What is new is (i) misfolded pre-5S rRNA against native 5S, which is Ro60's actual
quality-control substrate, and (ii) **whether vtRNA or misfolded RNA allosterically gates TEP1 E1008
NAD(P)ase catalysis in reconstituted MVP+TEP1 particles.** Run the NADase readout alongside the
binding assay; RNA-gated activation would connect the TROVE domain to the enzymology directly.
**Positive control:** Ro60 run alongside must bind misfolded pre-5S and be competed by Y RNA, as
published; if the reference TROVE protein fails, the assay says nothing about TEP1's.
**Kill condition:** binding is restricted to vtRNA *and* no RNA species modulates NADase rate. Note
that restricted binding alone *supports* the buffer model, so the experiment advances either way -
which is precisely why it should be run by someone with no stake.

### 7. Autophagic flux in the right genotype
**Decides:** the vtRNA-p62 buffer model, properly.
**Correction to the obvious design:** TEP1-null is the wrong animal - losing TEP1 *degrades* vault
RNA rather than freeing it. **MVP-null is the right genotype**, where vtRNA has no barrel but TEP1
is intact. We showed the Vaultrc5 knockout leaves the p62 transcriptional program unmoved, but
transcript abundance cannot see oligomerisation.
**Design:** MVP-null versus wild-type. Fractionate free versus particle-associated vtRNA first, to
confirm the premise. Then p62 oligomerisation by native gel or crosslinking, LC3-II flux with and
without bafilomycin, and aggregate clearance after puromycin.
**Positive control:** bafilomycin must raise LC3-II and puromycin must drive measurable p62
oligomerisation in wild-type cells, or the flux assay is not reporting flux.
**Kill condition:** p62 oligomerisation is unchanged in MVP-null cells.

### 11. MVP-null interferon output under stress
**Decides:** the signalling-brake layer, which our expression work could weaken but not test.
**Why computational work cannot settle it:** MVP sits downstream of STAT1, so every expression
correlation is circular. We found no support for membership in the chronic interferon program, but
that is a different claim from MVP *modulating* interferon output.
**Design:** MVP-null versus wild-type under defined stimulation (IFN-gamma, poly(I:C), live
pathogen). Measure STAT1 phosphorylation and ISG output directly rather than inferring from
steady-state expression.
**Positive control:** a JAK inhibitor must collapse ISG output in both genotypes, and STAT1-null
cells must fail to respond at all; without both the assay cannot report a modifier effect.
**Kill condition:** ISG output and STAT1 phosphorylation are indistinguishable between genotypes at
every stimulus and timepoint. That retires the signalling-brake layer.

---

## Tier 3 - cheap, and each closes a loop
*(Experiment 10 is strictly conditional on experiment 1 returning positive; experiment 6 is last.)*

### 9. Where the vault actually sits, by cell type
**Decides:** which cell type carries the vault load in the tissues that rank highest, and whether
the adrenal gland - the top tissue of 51 - is cortical, medullary, or neither.
**Why now.** Whole-organ expression puts adrenal gland (176 nTPM) and the colon-small
intestine-duodenum axis (162/157/146) above lung (120, rank 5 of 51). We tested and rejected the
obvious objection to that ranking: because MVP's cross-tissue profile is dominated by plasma-cell
immunoglobulin genes (70 of 143, p = 9.3e-98), we proposed the gut signal might be immune infiltrate
rather than epithelium. It is not. In cell lines, which carry no infiltrate, **plasma cells are
MVP-poor** - rank 15 of 20 lineages, z = -0.45, consistent across 40 immune-lineage lines - while
colorectal, gastric, pancreatic and kidney lines all run above average. The bulk ranking is
corroborated, not undermined, and is most simply read as parenchymal. **What remains unknown, and
why the experiment is still worth an afternoon.** Cell lines cannot settle adrenal: there is exactly
one adrenal cortical line in all 1,739 CCLE lines and none with proteomics. No hypothesis we tested
explains why adrenal tops the table - NAD metabolism failed its registered threshold despite adrenal
cortex running enormous NADPH flux, and no steroid, cytochrome-P450 or xenobiotic term reached
significance. Bulk tissue also cannot distinguish adrenal cortex from medulla, or bronchial
epithelium from alveolar parenchyma. Nobody has looked at vaults with cell-type resolution in the
tissues that actually carry the most of them.
**Design:** cell-type-resolved MVP by quantitative imaging or single-cell proteomics in **adrenal**
(cortex scored by zone - glomerulosa, fasciculata, reticularis - against medulla), **colonic
mucosa** (epithelium against lamina propria), and **airway** (bronchial epithelium against alveolar
parenchyma). Co-stain CD138 or MZB1 so the plasma-cell contribution is measured rather than assumed,
even though the cell-line result predicts it will be small.
**Positive control:** proteins of known cell-type restriction in the same sections - chromogranin A
for adrenal medulla, CYP11B1 for the cortex, villin for enterocytes, CD138 for plasma cells - must
each resolve to the expected compartment before any MVP number is read.
**Kill condition:** MVP is uniform across cell types within each organ. That would mean the tissue
ranking reflects nothing about cellular specialisation and would retire tissue-level reasoning about
vaults as a source of hypotheses, ours included.
**What a positive result buys:** a cell type to study. Every functional experiment in this document
is easier if it can be run in the cell that actually makes 10^5 of these particles, and right now
nobody knows which cell that is.

### 8. Anti-MVP serology with La as internal control
**Decides:** whether anti-MVP autoreactivity tracks anything mechanistic, now that its existence is
settled.
**Status change:** we found this partially answered in the literature - Moadab et al. 2023 screened
>21,000 proteins with lupus sera and **MVP was a top-ten hit alongside Ro60**. The asymmetry
argument is dead; the interesting question inverted.
**Design:** is anti-MVP reactivity associated with vault burden, UV exposure or disease activity?
Banked SSA-positive, SSB-positive and control sera; La as the matched non-vault control.
**Positive control:** anti-Ro60 titres must reproduce their established association with disease
activity in the same sera, or the panel is not measuring what it claims.
**Kill condition:** anti-MVP reactivity is present but associated with nothing - not burden, not UV,
not activity - which makes it a bystander consequence of cell death rather than a driver.

### 10. The progeria falsifier
**Precondition: do not run this unless experiment 1 returns positive.** It tests the specificity of
a containment function, so it is uninterpretable until containment itself is established; a negative
here with a negative experiment 1 means nothing.
**Decides:** whether a containment function, if established, is specific to the lesion type the
model predicts.
**Design:** progeria fibroblasts with documented envelope rupture and cGAS-STING activation;
overexpress MVP; measure interferon output, against TREX1-null as the clearance-failure comparison.
**Positive control:** TREX1-null cells must respond to MVP overexpression, establishing that the
overexpression is doing something measurable at all.
**Kill condition:** MVP overexpression calms progeria inflammation. That would mean the lesion
specificity of the model is wrong, and we would rather learn it here than defend it.

### 6. The C-terminal phosphorylation cluster - DEMOTED, and here is why
**Status: we talked ourselves out of this one.** We verified in our own alignment that the entire
human 862-893 tail is **absent in mouse, rat, chicken, zebrafish and *Dictyostelium*** (0%
occupancy) and present only in primates (100% in macaque and chimp; S876 is proline even in
macaque). A primate-restricted, disordered, proline-directed tail that scored 0 of 62 in our own
phospho test is a poor bet, and it cannot be modelled in rodents. Listed last, and reasonably
dropped.
**If run anyway, it decides:** whether a primate-specific regulatory element exists.
**New observation from this work:** MVP's reproducible phosphorylation concentrates in a C-terminal
cluster (S864, S867, S873, S876) present in five of six phospho-bearing CPTAC cohorts and
**disordered in every vault structure solved** - the segment Lodwick et al. 2025 named the "human
knob extension". A flexible, multiply phosphorylated tail is a canonical interaction motif.
**Design:** phospho-specific pulldown from the tail; identify the kinase by inhibitor panel; test
phosphomimetic and phospho-dead mutants for assembly, trafficking and PARP4 occupancy.
**Positive control:** a known proline-directed phosphosite on an unrelated bait must pull down its
established 14-3-3 or WW-domain partner from the same lysate.
**Kill condition:** no interactor, no kinase assignment, no phenotype.

---

### 12. Is MVP a COP1 substrate, or is COP1 a passenger?

**Decides:** whether the best-replicated non-subunit vault partner is there as a ubiquitin ligase
acting on the vault, or is present for some other reason.
**The replication is narrower than we first claimed:** #194 called it three independent instruments,
and #206 corrected that - the anti-MVP IP-MS, BioPlex AP-MS and a 2014 TAP are three *datasets* but
**one instrument class**, all lysis plus affinity matrix plus MS, so dataset independence is real
and method independence is absent. What stands is COP1 at **WT_LFC +4.74, about 27-fold, LWTP 2.59,
and not PARP4-dependent** in the pulldown, with the supporting IntAct evidence at chance once PARP4
is set aside (#206). An orthogonal instrument - pre-lysis covalent labelling, crosslinking or
reconstitution - has never been applied to this pair, which is part of what makes the bench the
right next step. We cannot interpret it computationally (§47), and §48c records why DDB1's absence
(present in the universe, not an interactor at LWTP 0.71) is positive evidence for free COP1 over an
assembled CRL4 holocomplex.

**Design:** co-immunoprecipitate COP1 and MVP reciprocally in a cell line where both are expressed,
then (a) ask whether endogenous MVP carries ubiquitin by immunoblot after COP1 knockdown versus
control, and (b) measure MVP's half-life by cycloheximide chase in COP1-knockdown versus control
cells. MVP's baseline half-life is ~66 h, so run the chase to 96 h; a ligase-substrate relationship
predicts stabilisation. Probe the same lysates for DET1, DDB1 and CUL4A/B to establish whether an
assembled CRL4 is present at all — the question §47b could not answer because four of six components
were never detected in the available IP-MS.

**Positive control:** a known COP1 substrate in the same lysate — ETV4, ETV5 or ACC1 — must show the
expected stabilisation on COP1 knockdown. Without it, a null on MVP means the knockdown failed, not
that MVP is not a substrate.

**Kill condition:** if MVP's ubiquitination and half-life are unchanged by COP1 knockdown while the
positive-control substrate stabilises, COP1 is not acting as a ligase on MVP. The association would
then need explaining some other way — COP1 as cargo, or as a shared binding partner of something
else — and the "degradation" reading dies, which §46d already shows has no module-level support.

**Why not a VP-degron prediction first:** §47a declines that. COP1's VP motifs are
sequence-divergent with no per-position consensus, a bare VP dipeptide is uninformative in a
893-residue protein, and known substrates including CEBPA and GATA2 are recognised without a
canonical motif. The scan cannot discriminate in either direction.

### 13. Is there a vault in stool, mucus, or culture supernatant - and is it loaded?

**Decides:** whether vaults leave cells intact, which is the premise of the export reading and is
not answered by any reanalysis we can do. Also the cheapest unasked question we found: a literature
search turned up **no report of MVP in the human fecal proteome or in gut mucus**, while MVP is
independently documented in exosome preparations, released from cells by a non-exosomal route, and -
in the Atlantic salmon louse - present in extracellular cement.

**Design, with the one point that decides the whole experiment: interrogate the 35,000 x g PELLET,
not the supernatant.** Section 58a establishes that the canonical host-centric stool proteomics
workflow (Lichtman et al., PMID 23982161) spins stool at 2,500 x g and then 35,000 x g, **discards
the pellet**, and analyses only soluble secreted protein - and a 13 MDa 78-mer sediments in exactly
that range, since differential centrifugation there is how vaults are purified. **Every published
stool proteome we could reach throws away the fraction this experiment needs**, which is the
likeliest reason the literature is silent. So run immunoblot and targeted MS for MVP, PARP4 and TEP1
on **both fractions separately** in (a) conditioned medium from a high-vault epithelial line,
cleared of cells and debris, (b) human stool, and (c) airway or intestinal mucus. Compare
particle-containing fractions from a sucrose cushion against the soluble fraction, so that intact
vaults are distinguished from free MVP monomer. Where a vault is recovered, sequence its contents -
vtRNA by RT-PCR, protein by MS - and ask whether what is inside differs from vaults purified from
the same cells' cytoplasm.

**Use targeted detection, not a shotgun survey.** Section 60 shows why: the one public stool dataset
that retains the pellet *and* searched a human database recovered 232 human proteins that are a
lumenal and brush-border secretome with **no beta-actin, no GAPDH and no HSC70** - so shotgun stool
proteomics cannot see cytoplasmic protein at all, and could not see a vault whether or not one is
there. Immunoblot and targeted MS against MVP, PARP4 and TEP1 are therefore the methods, and a
shotgun result would be uninterpretable.

**Positive control:** a known secreted protein in each matrix, and cytoplasmic vaults from the same
cells as the particle standard. **The three subunits must co-sediment**; MVP alone could be
degradation product rather than a particle.

**Kill condition:** if no MVP is recoverable from any of the three matrices while the secreted
control is, vaults do not leave cells in quantity and the export reading loses its premise. **If MVP
is recovered but as monomer without PARP4 and TEP1, that is also a kill** for the particle-export
version, though not for MVP release.

**Why this and not more computation:** §57 shows the control needed to test export computationally
is unusable at the relevant term size, and the two candidate signals rest on three proteins each,
two of which we already knew. **ATP7A**, a copper-transporting ATPase at +2.38 and the only efflux
pump in either list, is worth probing alongside - but as one protein, not a module.

### 14. Can a specific association be separated from the co-migration envelope it sits inside?

**Decides:** the one question §40 cannot answer with any amount of reanalysis. Six registered
alternatives have been eliminated or left live, and §56c shows why that cannot finish: MVP's
translation-rich co-elution tail shows **both** a sharp top-of-list signal the negatives entirely
lack (12 hits at k=25 against 0.32 expected) **and** continued accumulation to 93 hits at k=800 that
looks like a shared elution window. One instrument cannot separate them.

**Design:** purify vaults from a high-expressing line and ask directly whether ribosomal protein or
rRNA co-purifies through two orthogonal separations - a sucrose gradient and size-exclusion - then
repeat after puromycin or EDTA treatment to dissociate polysomes. A specific association survives
polysome dissociation; a shared-window artefact does not.

**Positive control:** PARP4 and TEP1 must co-purify through both separations and survive both
treatments, since they are the particle.

**Kill condition:** if ribosomal signal disappears on polysome dissociation while PARP4 and TEP1
persist, §40 is the co-migration artefact grok's audit describes, and the translation thread closes
for good.

## What a home run looks like

Experiment 1 returning **nucleotide-protected, stress-induced cargo other than vtRNA** would reopen
the containment model with direct evidence and make roughly half the candidate disease list testable
again. Experiment 2 returning **NAD+ depletion on membrane wounding, abolished in TEP1-E1008A**,
would give the particle its first demonstrated trigger and connect a 2026 enzymology result to a
2007 infection phenotype.

Either outcome would be the first *positive* functional assignment the field has had. We think the
honest prior is that both return negative - but both are cheap, both are decisive, and a clean
negative on experiment 1 closes a question that has been open since 1986.

**A note on who should run these.** We have no laboratory and no stake in the outcome. The analysis
behind this document is public, pre-registered, and includes the two occasions on which our own
conclusions were reversed. We would rather these experiments were run by people who can do them
properly than be right about which way they come out.
