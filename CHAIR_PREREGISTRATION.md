# Pre-registration: the testable claims in the chair metaphor

Written before any value was read. Graham's framing: *"if someone is making chairs, they might
eventually want to sit down... a growing cell doesn't have any, but a cell that is fully matured
produces them... maybe they do it because they will need them... maybe the same process that builds
them can undo them... or a similar inverted protein, maybe a mirror image."*

That is five claims. One is already dead, one is already constrained, three are testable tonight.

- **Raw-material reserve** - **DEAD** (§82): MVP is not nitrogen-rich and is sulfur-poor at a third of
  the proteome average, avoiding the expensive essential residues a bank would hold.
- **Reversible assembly** - **CONSTRAINED, not tested.** Mrazek et al. 2014 show vault assembly is
  **co-translational on polyribosomes**, templated rather than spontaneous. **You cannot un-translate a
  protein**, so disassembly cannot be assembly run backwards. A separate disassembly mechanism is still
  possible; symmetry is not. Recorded, not registered.
- **Timing** -> TEST A and TEST B below.
- **Mirror image / inverted protein** -> TEST C below.
- **Viral decoy** - not testable with data in hand; needs infection time courses we do not have.

---

## TEST A - does MVP rise with maturation, within organ?

**Data:** `data/raw/devel/Human.RPKM.txt`, Cardoso-Moreira E-MTAB-6814. 51,299 genes, 297 samples,
columns named `Organ.stage.replicate`, seven organs from 4 weeks post-conception to senior.

**Stage order, fixed now:** 4wpc, 5wpc, 6wpc, 7wpc, 8wpc, 9wpc, 10wpc, 11wpc, 12wpc, 13wpc, 16wpc,
18wpc, 19wpc, 20wpc, newborn, infant, toddler, school, youngTeenager, teenager, oldTeenager,
youngAdult, youngMidAge, olderMidAge, senior.

**Statistic:** Spearman rho of log1p(RPKM) against stage rank, within each organ having >= 8 distinct
stages.

**PREDICTION (Graham's, direction registered): rho > 0 for MVP in a majority of qualifying organs.**

**GATE - failable:**
1. **Proliferation markers MKI67, TOP2A, PCNA, CCNB1 must give rho < 0 in >= 5 of 7 organs.** If
   proliferation does not fall with maturation, the stage ordering or the matrix is wrong and nothing
   else is interpretable.
2. **Housekeeping ACTB and GAPDH must have |rho| below the proliferation markers' median |rho|**, so a
   positive MVP result cannot be a global drift affecting every gene.
3. Every gene above must be **found by ENSG id, with the count reported**; a missing control fails the
   gate rather than passing silently (house rule 7, broken three times this week).

**KILL:** if MVP's rho is <= 0 in a majority of qualifying organs, the timing claim is **refused** and
"built ahead of a need" loses its only measurable leg.

---

## TEST B - is MVP higher in post-mitotic than proliferative tissue?

**Data:** `data/raw/tissue/rna_tissue_consensus.tsv`, HPA consensus, 51 tissues, nTPM.

**Sets fixed now. Post-mitotic:** cerebral cortex, cerebellum, heart muscle, skeletal muscle.
**Proliferative:** bone marrow, testis, small intestine, skin.

**PREDICTION: MVP's median nTPM is higher in the post-mitotic set.**

**GATE:** MKI67 and TOP2A must both be **higher in the proliferative set**. If the sets do not separate
on proliferation markers, they are not proliferation sets and the comparison is void.

---

## TEST C - is there a human paralogue that could be the "mirror image"?

An inverted or antagonistic partner protein has to exist to do anything. **Does the human proteome
contain a second MVP-like protein at all?**

**Data:** the 20,429-entry Swiss-Prot human proteome already downloaded for §82.

**Method:** 6-mer Jaccard similarity of MVP against every human protein as a prefilter, then
Smith-Waterman-style local alignment (Biopython `PairwiseAligner`, BLOSUM62) on the top 40 candidates.
Report percent identity and aligned length for the best non-MVP hits.

**PREDICTION:** if the mirror-image idea has any footing, **a human paralogue exists at >= 20% identity
over >= 200 aligned residues.**

**GATE - failable in both directions:**
1. **Known paralogue pairs must be recovered**: ACTB must find ACTG1, and TUBB must find another
   beta-tubulin, each well above the threshold. If the method cannot find a real paralogue, it cannot
   be trusted to report an absence.
2. The search must cover **>= 20,000 proteins, count reported.**

**KILL:** if MVP's best non-self hit falls below that threshold while the controls pass, **MVP is
single-copy in human**, and the inverted-partner idea has no protein to be built from - in this
species. Note in advance: the salmon louse genome has an **expanded** vault family, so single-copy in
human would not mean single-copy everywhere.

---

## Limits, stated first

All three are **transcript-level or sequence-level**. None measures particle count, and §71 established
that **vault abundance is not one quantity** - bulk MVP mRNA is not assembled vaults. A positive TEST A
would say MVP transcription rises with maturation, **not** that mature cells hold more particles.
