# What a wet lab should do next with vaults: eleven experiments, ranked by what they decide

**Graham W. Syfert**, with Claude (Anthropic) and a second review agent. Companion to
`PAPER1_vault_reassessment.md`. Written for a group with a working vault purification pipeline.

**Why this document exists.** We ran eighteen pre-registered computational tests against every public
dataset we could reach. They eliminated most standing hypotheses and produced three hard constraints
that no public dataset can resolve further. Everything below requires a bench. Each entry states what it
decides, the minimal design, the positive control, and the result that would kill the idea - including
ours.

**The three constraints any experiment should respect:**
1. The nucleotide pocket in the SPFH shoulder is reachable **only from the lumen** (zero exterior probe
   access at 1.4 and 5.0 Angstrom in the assembled 78-mer). Something must open the particle.
2. **PARP4 exchanges three to eightfold faster than the shell** (22.2 h vs 66.4 h, four of four
   non-dividing human cell types). The enzyme is not locked in.
3. The particle is **dispensable for proliferation** (zero hits in 878 growth screens) yet
   **sequence-constrained** at the pocket (four residues invariant across 174 eukaryotes). Whatever
   selects it does not operate in a dish.

---

## Tier 1 - decides the most, costs the least

### 1. Stressed Trap-and-Seq: what is actually inside a vault?
**Decides:** the containment hypothesis, and roughly half the candidate disease list.
**Why now:** the claim that vaults contain a single small RNA rests on a 1986 gel and a 2001 Northern
blot on unstressed mouse liver. A Northern blot cannot discover an unknown RNA.
**Design:** cells with high native vault expression, wild-type and MVP-null in parallel. Block
autophagic turnover (bafilomycin A1, 2 h). Four arms: vehicle; a genotoxic agent; UV-C or etoposide;
transfected nuclear-targeted synthetic dsRNA. 60-120 min, short of death. Reversibly crosslink, lyse,
then **nuclease-shave with benzonase/RNase/DNase** so only sealed cargo survives. Rapid size-exclusion
plus anti-MVP capture. Sequence small RNA and DNA at modern depth.
**Power argument that has not been made:** at 10^5 vaults per cell, even 1% carrying a non-vtRNA cargo
yields ~10^3 molecules per cell - comparable to a moderately expressed mRNA, and trivially detectable
now. The cargo need only be rare **per particle**.
**Positive control:** vtRNA1-1 must be recovered and must survive the nuclease shave.
**Kill condition:** a clean nuclease-protected profile under stress, at modern depth, with nothing but
vtRNA. That would close a question open since 1986 and is publishable as such.

### 2. Does membrane breach trigger TEP1 NADase activity?
**Decides:** our single most specific joint hypothesis, assembled from two literatures that had not met.
**The convergence:** TEP1 is an autoinhibited TIR-family NAD(P)ase requiring oligomerisation (E1008
catalytic); no published study tests what activates it in cells. Independently, MVP-null mice die of
*Pseudomonas aeruginosa* and the *Listeria* InlK result involves listeriolysin O - **both pore-forming
toxins** - and MVP co-abundance places it near ANXA2 and S100A10, the canonical membrane-repair
heterotetramer.
**Design:** sterile streptolysin-O versus live *Pseudomonas*, in wild-type, PARP4-knockout and
TEP1-E1008A knock-in cells. Read NAD+ by LC-MS over 0-120 min, with cADPR and nicotinamide as products.
**Positive control:** SARM1 activation by vacor or CZ-48 in the same assay.
**Kill condition:** NAD+ is unperturbed by membrane wounding in wild-type cells while the SARM1 control
depletes normally. That kills the breach-trigger model cleanly.

### 3. What opens the shell?
**Decides:** constraint 1 above, and the born-loaded versus loaded-on-demand fork.
**Why now:** cytosolic NAD+ cannot reach the pocket in the closed particle, yet endogenous ADP-ribose is
present in vaults purified from brain. Something admits it. Separately, pre-formed vaults have been
shown to take up intact AAV capsids, so the waist does breathe.
**Design:** reconstituted vaults with a lumenal FRET or fluorogenic NAD+ sensor; titrate pH, calcium,
ionic strength, mechanical shear and pore-forming toxin. Measure occupancy kinetics. Pair with
cryo-EM or HS-AFM on the same conditions.
**Kill condition:** no tested condition increases lumenal occupancy above baseline exchange.

---

## Tier 2 - resolves a specific published contradiction

### 4. What drives PARP4 exchange?
**Decides:** the mechanism behind constraint 2, which we could not touch computationally.
**What we ruled out:** MVP phosphorylation. Across seven tumour cohorts, no MVP phosphosite predicts
per-vault PARP4 loading (0 of 44 tests, all |rho| < 0.11).
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
**Kill condition:** binding is restricted to vtRNA. Note this outcome *supports* the buffer model, so
the experiment advances either way - which is precisely why it should be run by someone with no stake.

### 6. The C-terminal phosphorylation cluster
**Decides:** a regulatory element nobody has characterised.
**New observation from this work:** MVP's reproducible phosphorylation concentrates in a C-terminal
cluster (S864, S867, S873, S876) present in five of seven CPTAC cohorts and **disordered in every vault
structure solved**. A flexible, multiply phosphorylated tail is a canonical interaction motif.
**Design:** phospho-specific pulldown from the tail; identify the kinase by inhibitor panel; test
phosphomimetic and phospho-dead mutants for assembly, trafficking and PARP4 occupancy.
**Kill condition:** no interactor, no kinase assignment, no phenotype.

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

---

## Tier 3 - cheap, and each closes a loop

### 8. Anti-MVP serology with La as internal control
**Status change:** we found this partially answered in the literature - Moadab et al. 2023 screened
>21,000 proteins with lupus sera and **MVP was a top-ten hit alongside Ro60**. The asymmetry argument is
dead; the interesting question inverted.
**Remaining design:** is anti-MVP reactivity associated with vault burden, UV exposure or disease
activity? Banked SSA-positive, SSB-positive and control sera; La as the matched non-vault control.

### 9. Where the vault actually sits, by cell type
**Why:** whole-organ expression put adrenal gland and the colon-duodenum axis above lung, contradicting
a widely repeated claim. Bulk tissue cannot separate bronchial epithelium from alveolar parenchyma.
**Design:** quantitative imaging or single-cell proteomics across adrenal cortex, intestinal epithelium
and airway, to establish which cell type carries the 10^5 copies.

### 10. The progeria falsifier
**Keep it on the record.** If containment is correct, vaults should be useless against a ruptured
nuclear envelope. Progeria fibroblasts with documented rupture and cGAS-STING activation; overexpress
MVP; measure interferon output, against TREX1-null as the clearance-failure comparison.
**Predicted:** progeria refractory, TREX1-null responsive. If MVP overexpression calms progeria
inflammation, the pore-docking specificity of the model is wrong.

### 11. MVP-null interferon output under stress
**Decides:** the signalling-brake layer, which our expression work could weaken but not test.
**Why computational work cannot settle it:** MVP sits downstream of STAT1, so every expression
correlation is circular. We found no support for membership in the chronic interferon program, but that
is a different claim from MVP *modulating* interferon output.
**Design:** MVP-null versus wild-type under defined stimulation (IFN-gamma, poly(I:C), live pathogen).
Measure STAT1 phosphorylation and ISG output directly rather than inferring from steady-state expression.

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
