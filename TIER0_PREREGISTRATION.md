# Pre-registration: Tier 0 done properly

Registered before either computation was run. Tools installed for this purpose: **HMMER 3.4**,
**PAML 4.9j (`codeml`)**, **MAFFT 7.505** - the absence of which is why §79-§83 used the wrong
instruments.

---

## Correction to our own Tier 0 instruction, before using it

Paper 2's Tier 0a proposed: *"is omega elevated on the branches leading to the clades that **lost**
MVP relative to those that retained it?"*

**That test is ill-posed and we wrote it anyway.** You cannot estimate dN/dS on a branch where the gene
is absent - there is no sequence. The measurable version of the same idea is **relaxation among
retainers**: whether omega is uniform across the retained tree, or elevated in some retained lineages.
That is what is registered below. **Paper 2 will be corrected.**

---

## 0b - the paralogue question, with a profile HMM

**Source alignment, already in hand:** eggNOG orthogroup **2QPP0** (MVP's own, established in §68),
**174 sequences, 1,943 aligned columns**, at `argon/raw/eggnog_raw_alg_2QPP0.json`.

**Method.** `hmmbuild` -> profile; `hmmsearch` against the 20,429-entry reviewed human proteome
(HMMER 3.4 applies biased-composition filtering by default, which is the protection
`Bio.PairwiseAligner` lacked and which §84g identified as the reason our 28.7% hit was noise).

**Fixed in advance:**
- **Significance: full-sequence E-value <= 0.001.**
- **Coverage: the aligned envelope must span >= 50% of the profile length.** Our previous best hit
  covered 28% of MVP and we had registered no coverage requirement at all (§84g).
- **Ranked by bit score, never percent identity.**
- MVP itself is excluded from the hit list.

**POSITIVE-CONTROL GATE - both clauses must hold:**
1. **The MVP profile must recover MVP itself** at E <= 1e-50 when it is not excluded. A profile that
   cannot find its own source gene cannot be trusted to report an absence.
2. **A `jackhmmer` search of ACTB against the same proteome must recover ACTG1** at E <= 0.001 with
   >= 50% coverage. This shows the pipeline detects a real paralogue **under the same thresholds**,
   which the §84g controls did not, since they were tested only at 97-99% identity.

**DECISION, registered:**
- If one or more human proteins other than MVP clear both thresholds, **a candidate paralogue exists**
  and it is named.
- If none do and the gate passed, **MVP is single-copy in the reviewed human proteome by profile
  search.** That is a far stronger negative than §83d could support, and it is the first time this
  project would be entitled to say it.

---

## 0a - the selection estimate, with a codon model on a tree

**Species, fixed now.** Mammals: human, rat, dog, cow, sheep, horse, rabbit, opossum. Deeper retainers,
added because §84b's mammal-only panel cannot address the ~600 My the paradox asks about: chicken,
*Xenopus tropicalis*, zebrafish.

**Data.** Orthologue CDS fetched in **two steps** - gene ids first, then sequences individually - since
the one-shot homology-with-sequence endpoint is what returned HTTP 500 on 36 of 90 calls (§80b).

**Alignment.** Translate, align proteins with **MAFFT**, thread the CDS back through the protein
alignment to produce a codon alignment. Columns with a gap in any sequence are dropped.

**Tree, fixed now** (standard topology, no estimation from these data):
`(((((human,(rat,rabbit)),(dog,horse)),(cow,sheep)),opossum),(chicken,(xenopus,zebrafish)))`

**Models.** `codeml`, `seqtype = 1`, `CodonFreq = 2` (F3x4):
- **M0**, one omega for the whole tree -> the headline number.
- **Two-ratio branch model**, mammals as foreground against the deeper retainers as background,
  compared to M0 by **likelihood-ratio test on 1 df**. This is the corrected version of the branch
  test described above.

**PREDICTION, registered:** M0 omega lands **below 0.20** and **above 0.02** - that is, between the
essential-gene and relaxed-control clusters of §84b, consistent with pairwise NG86's 0.1118 but
**expected to come in lower**, because NG86 biases omega upward (§84b).

**GATE:** `codeml` must converge (non-zero likelihood, omega not pinned at a bound) **and** the M0
omega must be reproducible across two independent starting values of omega (0.05 and 0.5) to within
**0.02**. A single run that cannot be reproduced from a different start is not an estimate.

**KILL:** if omega >= 0.5, or if the two starts disagree by more than 0.02, the codon-model result is
uninformative and **§84b's pairwise 0.1118 stands alone as the project's estimate**, with its stated
limits.

**What this cannot do, stated first.** One omega averaged over sites and branches says nothing about
which residues are constrained. Site models were not registered and will not be run post hoc.
