# What a wet lab should do next with vaults: eleven experiments, ranked by what they decide

**Graham W. Syfert**, with Claude (Anthropic) and a second review agent. Companion to
`PAPER1_vault_reassessment.md`. Written for a group with a working vault purification pipeline.

**Why this document exists.** We ran nineteen pre-registered computational tests against every public
dataset we could reach. They eliminated most standing hypotheses and produced four hard constraints
that no public dataset can resolve further. Everything below requires a bench. Each entry states what it
decides, the minimal design, the positive control, and the result that would kill the idea - including
ours.

**The four constraints any experiment should respect:**
1. The nucleotide pocket in the SPFH shoulder **cannot be reached radially through the shell wall** and
   must be loaded from the lumen (zero exterior probe access at 1.4 and 2.5 Angstrom in the assembled
   78-mer; maximum exterior channel radius 1.10 Angstrom, narrower than water). This does **not** mean
   the particle must open to admit NAD+: published ITC and soaking experiments show free dinucleotides
   reaching the pocket of intact cages in neutral buffer, via the C-terminal cap openings and waist
   breathing. Opening is required for **macromolecular** traffic - PARP4, TEP1, vtRNA, ADP-ribosylated
   targets - not for the 663-Da substrate. We held the stronger claim and were wrong.
2. **PARP4 turns over three to eightfold faster than the shell** (22.2 h vs 66.4 h, four of four
   non-dividing human cell types, so pure proteolysis). The enzyme is not a permanent fixture, though
   pulse-SILAC measures degradation and not off-rate.
3. The particle is **dispensable for proliferation** (zero hits in 878 growth screens) yet
   **sequence-constrained** at the pocket (four residues invariant across 174 eukaryotes). Whatever
   selects it does not operate in a dish.
4. **TEP1 is a latent, autoinhibited TIR-family NAD(P)ase (E1008), and the uninhibited domain is lethal
   in human cells** - expressed without its STAND regulatory domains it drops cellular NAD+ to 30-40% of
   control and kills HEK293 cells, both abolished by E1008A. The brake is **in cis**, allosteric,
   reinforced by a millimolar unactivated Km; it is not the cage. The 10^5 figure counts vault particles,
   not TEP1, which sits at roughly one to two copies per particle. Nearly every assay in our
   computational work sampled unstimulated growth or bulk tissue, which is precisely when a latent
   effector is designed to be invisible. **The experiments below are therefore ordered by how directly
   they perturb the system out of that resting state.**

---

## Tier 1 - decides the most, costs the least
*(Order revised after adversarial review: perturbation experiments first, since the resting state is
uninformative by design. Experiment numbers are retained as stable identifiers; the sequence below is
the recommended running order.)*
### 2. Does membrane breach trigger TEP1 NADase activity?
**Decides:** our single most specific joint hypothesis, assembled from two literatures that had not met.
**The convergence:** TEP1 is an autoinhibited TIR-family NAD(P)ase (E1008 catalytic) whose STAND module
is expected to gate activation, though obligate oligomerisation is contested between the 2026 preprints
and no physiological trigger has been demonstrated. The published work notes that vaults confer
resistance to *Pseudomonas aeruginosa* and influenza A and speculates that TEP1 may be an innate-immune
executioner, but no study connects that to pore-forming toxins or to membrane-wound repair. Independently, MVP-null mice die of
*Pseudomonas aeruginosa* and the *Listeria* InlK result involves listeriolysin O - **both pore-forming
toxins** - and MVP co-abundance places it near ANXA2 and S100A10, the canonical membrane-repair
heterotetramer.
**Design:** sterile streptolysin-O versus live *Pseudomonas*, in wild-type, **MVP-null**,
PARP4-knockout and TEP1-E1008A knock-in cells. Targeted LC-MS/MS over 0-120 min against authentic
standards, monitoring **NAD+, NADP+, linear ADP-ribose, 2'-phospho-ADP-ribose, nicotinamide, and cyclic
ADPR**.
**A product-panel warning that would otherwise cause a false negative.** TIR NADases differ in what they
make. The published characterisations report TEP1 generating **linear ADP-ribose and nicotinamide** (and
2'-phospho-ADPR from NADP+), whereas **SARM1 - the obvious positive control - does generate cyclic
ADPR**. Monitoring cADPR alone would therefore miss TEP1 entirely while lighting up the control, and
injury itself activates SARM1 and CD38. Monitor the full panel and include a SARM1 inhibitor or knockout
arm so the two enzymes can be separated. The cADPR-negative result for TEP1 is verbatim in the primary
text and independently stated by a second group.
**Positive control:** SARM1 activation by vacor or CZ-48 in the same assay, read on the same panel.
**The discriminating signature:** TEP1 activation predicts a rise in **linear ADPR + 2'-P-ADPR +
nicotinamide with no cADPR rise**, abolished in TEP1-E1008A.
**Kill condition:** NAD+ is unperturbed by membrane wounding in wild-type cells while the SARM1 control
depletes normally. That kills the breach-trigger model cleanly.

### 3. What opens the shell?
**Decides:** constraint 1 above, and the born-loaded versus loaded-on-demand fork.
**Why now:** cytosolic NAD+ cannot reach the pocket in the closed particle, yet endogenous ADP-ribose is
present in vaults purified from brain. Something admits it. Separately, pre-formed vaults have been
shown to take up intact AAV capsids, so the waist does breathe.
**Design:** low-pH opening is already published, so test **physiological** triggers: pH 6.0-7.4,
Ca2+ 0.1-100 uM with and without ANXA2/S100A10, vtRNA, mechanical shear, pore-forming toxin. Do **not**
read this out as labelled-NAD+ uptake: free NAD+ already reaches the pocket of intact cages at baseline,
so that assay is saturated before the experiment starts. Read out **macromolecular** traffic instead -
uptake of labelled PARP4-MINT or of exogenous vtRNA into pre-formed cages - and, in parallel, the
**off-rate of pre-bound ADP-ribose from native holo-vaults**, which reports pocket exchange rather than
pocket filling. Use wild-type against pocket mutants (F547A/D566A) rather than a bulky lumenal sensor
that would itself change lumenal crowding. Pair with cryo-EM or HS-AFM on the same conditions.
**Kill condition:** no physiological condition increases macromolecular occupancy above baseline and no
condition accelerates ADP-ribose release, with the pocket mutant indistinguishable from wild-type.

### 1. Stressed Trap-and-Seq: what is actually inside a vault?
**Decides:** the containment hypothesis, and roughly half the candidate disease list.
**Why now:** the claim that vaults contain a single small RNA rests on a 1986 gel and a 2001 Northern
blot on unstressed mouse liver, and a Northern blot cannot discover an unknown RNA. The one modern
attempt - Musgrove et al. 2026 neuronal MVP:eGFP RIP-seq - recovered Vaultrc5 plus hundreds of mRNAs but
used 1% formaldehyde crosslinking **without a nuclease shave**, so exterior ribonucleoprotein sticking
cannot be distinguished from sealed lumenal cargo. That is exactly the gap this design closes.
**Design:** cells with high native vault expression, wild-type and MVP-null in parallel. Block
autophagic turnover (bafilomycin A1, 2 h). Four arms: vehicle; a genotoxic agent; UV-C or etoposide;
transfected nuclear-targeted synthetic dsRNA. 60-120 min, short of death. **Do not crosslink whole cells first** - formaldehyde
tethers cytosolic RNA to the barrel exterior and blocks complete digestion, recreating the artefact
above. Lyse gently in cold isotonic buffer, isolate intact native particles, **nuclease-shave the
uncrosslinked shells** with benzonase/RNase/DNase, then lyse the shaved vaults. Rapid size-exclusion plus
anti-MVP capture. Sequence small RNA and DNA at modern depth.
**Power argument that has not been made:** at 10^5 vaults per cell, even 1% carrying a non-vtRNA cargo
yields ~10^3 molecules per cell - comparable to a moderately expressed mRNA, and trivially detectable
now. The cargo need only be rare **per particle**.
**Positive control:** spiked exogenous RNA must be destroyed by >=99.9% while endogenous vtRNA1-1
survives the same shave. That single control is what separates cargo from passengers.
**Kill condition:** a clean nuclease-protected profile under stress, at modern depth, with nothing but
vtRNA. That would close a question open since 1986 and is publishable as such.

---

## Tier 2 - resolves a specific published contradiction
### 4. What drives PARP4 exchange?
**Decides:** the mechanism behind constraint 2, which we could not touch computationally.
**What we ruled out:** MVP phosphorylation. Across six phospho-bearing CPTAC cohorts, no MVP phosphosite
predicts per-vault PARP4 loading: 0 of 62 tests reach q < 0.05, and the strongest raw association
(rho = -0.374, p = 0.001) fails to replicate across the six cohorts measuring that site.
**Design:** pulse-chase PARP4 on assembled vaults while varying lumenal ligand occupancy (NAD+,
ADP-ribose, non-hydrolysable analogues), ionic strength and MVP abundance. Does ligand occupancy set
residence time?
**Kill condition:** PARP4 residence is invariant to lumenal occupancy.

### 5. Does TEP1 bind misfolded noncoding RNA, as its only paralog does?
**Decides:** whether the TROVE domain means anything functional, and the Ro60 comparison.
**Design:** express the TROVE-vWA fragment rather than full-length TEP1 (the p80 homology region
suffices for vtRNA and particle association). EMSA against vtRNA (positive), Y RNA, correctly folded 5S
rRNA, and misfolded 5S precursor - Ro60's known substrate. Competition: does vtRNA block access as Y RNA
does for Ro60?
**The addition that makes this worth doing now:** generic TEP1 RNA-binding EMSA was partly done in 2002.
What is new is (i) misfolded pre-5S rRNA against native 5S, which is Ro60's actual quality-control
substrate, and (ii) **whether vtRNA or misfolded RNA allosterically gates TEP1 E1008 NAD(P)ase catalysis
in reconstituted MVP+TEP1 particles.** Run the NADase readout alongside the binding assay; RNA-gated
activation would connect the TROVE domain to the enzymology directly.
**Kill condition:** binding is restricted to vtRNA *and* no RNA species modulates NADase rate. Note that
restricted binding alone *supports* the buffer model, so the experiment advances either way - which is
precisely why it should be run by someone with no stake.

### 7. Autophagic flux in the right genotype
**Decides:** the vtRNA-p62 buffer model, properly.
**Correction to the obvious design:** TEP1-null is the wrong animal - losing TEP1 *degrades* vault RNA
rather than freeing it. **MVP-null is the right genotype**, where vtRNA has no barrel but TEP1 is intact.
We showed the Vaultrc5 knockout leaves the p62 transcriptional program unmoved, but transcript abundance
cannot see oligomerisation.
**Design:** MVP-null versus wild-type. Fractionate free versus particle-associated vtRNA first, to
confirm the premise. Then p62 oligomerisation by native gel or crosslinking, LC3-II flux with and
without bafilomycin, and aggregate clearance after puromycin.
**Kill condition:** p62 oligomerisation is unchanged in MVP-null cells.

### 11. MVP-null interferon output under stress
**Decides:** the signalling-brake layer, which our expression work could weaken but not test.
**Why computational work cannot settle it:** MVP sits downstream of STAT1, so every expression
correlation is circular. We found no support for membership in the chronic interferon program, but that
is a different claim from MVP *modulating* interferon output.
**Design:** MVP-null versus wild-type under defined stimulation (IFN-gamma, poly(I:C), live pathogen).
Measure STAT1 phosphorylation and ISG output directly rather than inferring from steady-state expression.

---

## Tier 3 - cheap, and each closes a loop
*(Experiment 10 is strictly conditional on experiment 1 returning positive; experiment 6 is last.)*

### 9. Where the vault actually sits, by cell type
**Why:** whole-organ expression put adrenal gland and the colon-duodenum axis above lung, contradicting
a widely repeated claim. Bulk tissue cannot separate bronchial epithelium from alveolar parenchyma.
**Design:** quantitative imaging or single-cell proteomics across adrenal cortex, intestinal epithelium
and airway, to establish which cell type carries the 10^5 copies.

### 8. Anti-MVP serology with La as internal control
**Status change:** we found this partially answered in the literature - Moadab et al. 2023 screened
>21,000 proteins with lupus sera and **MVP was a top-ten hit alongside Ro60**. The asymmetry argument is
dead; the interesting question inverted.
**Remaining design:** is anti-MVP reactivity associated with vault burden, UV exposure or disease
activity? Banked SSA-positive, SSB-positive and control sera; La as the matched non-vault control.

### 10. The progeria falsifier
**Precondition: do not run this unless experiment 1 returns positive.** It tests the specificity of a
containment function, so it is uninterpretable until containment itself is established; a negative here
with a negative experiment 1 means nothing.
**Keep it on the record.** If containment is correct, vaults should be useless against a ruptured
nuclear envelope. Progeria fibroblasts with documented rupture and cGAS-STING activation; overexpress
MVP; measure interferon output, against TREX1-null as the clearance-failure comparison.
**Predicted:** progeria refractory, TREX1-null responsive. If MVP overexpression calms progeria
inflammation, the pore-docking specificity of the model is wrong.

### 6. The C-terminal phosphorylation cluster - DEMOTED, and here is why
**Status: we talked ourselves out of this one.** We verified in our own alignment that the entire human
862-893 tail is **absent in mouse, rat, chicken, zebrafish and *Dictyostelium*** (0% occupancy) and
present only in primates (100% in macaque and chimp; S876 is proline even in macaque). A
primate-restricted, disordered, proline-directed tail that scored 0 of 62 in our own phospho test is a
poor bet, and it cannot be modelled in rodents. Listed last, and reasonably dropped.
**If run anyway, it decides:** whether a primate-specific regulatory element exists.
**New observation from this work:** MVP's reproducible phosphorylation concentrates in a C-terminal
cluster (S864, S867, S873, S876) present in five of six phospho-bearing CPTAC cohorts and **disordered
in every vault structure solved** - the segment Lodwick et al. 2025 named the "human knob extension".
A flexible, multiply phosphorylated tail is a canonical interaction motif.
**Design:** phospho-specific pulldown from the tail; identify the kinase by inhibitor panel; test
phosphomimetic and phospho-dead mutants for assembly, trafficking and PARP4 occupancy.
**Kill condition:** no interactor, no kinase assignment, no phenotype.

---

## What a home run looks like

Experiment 1 returning **nucleotide-protected, stress-induced cargo other than vtRNA** would reopen the
containment model with direct evidence and make roughly half the candidate disease list testable again.
Experiment 2 returning **NAD+ depletion on membrane wounding, abolished in TEP1-E1008A**, would give the
particle its first demonstrated trigger and connect a 2026 enzymology result to a 2007 infection
phenotype.

Either outcome would be the first *positive* functional assignment the field has had. We think the
honest prior is that both return negative - but both are cheap, both are decisive, and a clean negative
on experiment 1 closes a question that has been open since 1986.

**A note on who should run these.** We have no laboratory and no stake in the outcome. The analysis
behind this document is public, pre-registered, and includes the two occasions on which our own
conclusions were reversed. We would rather these experiments were run by people who can do them properly
than be right about which way they come out.
