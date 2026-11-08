# Untested functional hypotheses, and what we learned that appears unnoted

**Claude's lists, written 2026-11-07 and committed before Grok was asked the same two questions**, so
the independence is checkable from `git log` rather than asserted. Grok's answers go in
`grok/from-grok/005r-*` and the comparison follows in RESULTS §66.

Ratings are **my** probability that the hypothesis is substantially correct, or that the observation is
both true and genuinely unremarked. They are judgements, not computed values, and several are low on
purpose — a top-ten list of untested ideas should contain ideas I expect to be wrong.

---

## Part A — Top 10 untested hypotheses for vault function

### A1. The vault is a nucleotide-sequestering buffer. **~20%**
The strongest thing in this project's structural work is a **sealed nucleotide pocket in the SPFH
shoulder**, found in two independent alignments. A 78-mer presents 78 such pockets; at ~100,000
particles per cell that is a large, addressable nucleotide pool. **For:** the pocket is conserved and
sealed, which is an odd thing to maintain for nothing. **Against:** we never showed anything binds it,
and "sealed" is as compatible with a vestige as with a buffer. **Decides it:** ITC or a nucleotide-
competition assay on purified shell against the E1008 mutant.

### A2. TEP1 is a latent TIR-family NAD(P)ase that fires on membrane breach. **~18%**
TEP1 carries a TIR-family fold with the catalytic glutamate at **E1008**, and TIR NADases are
autoinhibited until oligomerised. **For:** the architecture is right, and §43 shows TEP1 binds the
particle independently of PARP4, so it is not a passenger. **Against:** we have no activity
measurement at all, and the membrane-breach trigger comes from a module (membrane repair) that died
six times in this project. **Decides it:** NAD+ consumption by purified TEP1, wild-type against
E1008A, with and without forced oligomerisation.

### A3. The vault is an assembly or quality-control platform on polyribosomes. **~15%**
MVP's co-elution tail is translation-enriched at the **98.0th percentile of 150 comparable seeds**,
surviving controls for degree, abundance, family membership and apparent mass. **For:** four
alternatives eliminated; vaults are reported to assemble on polyribosomes. **Against:** §63's rerun
voided the contact-instrument arm entirely, and Grok showed no CFdb-only statistic can separate this
from a shared hydrodynamic window. **Decides it:** Paper 2 Experiment 14 — puromycin dissociation.

### A4. The vault's job is turnover of its own cargo, not transport of it. **~12%**
PARP4 turns over at **22.2 h** against MVP's **66.4 h**, and PARP4 is substoichiometric. If the shell
outlives its catalytic subunit threefold, the particle may be a slowly-replaced housing that cycles
contents through. **For:** the half-life ordering is real on point estimates. **Against:** #76 already
struck the strong version — a substoichiometric protein has an expected free pool that can dominate
the measurement — and §61 shows the three rates were never tested for compatibility. **Decides it:**
the 2-df Wald test Grok specified, on pulse-SILAC fit covariance.

### A5. The vault is furniture: an abundant structural protein with no acute function. **~12%**
The least interesting hypothesis and not the least likely. **For:** no fitness coupling in CRISPR
screens; MVP sits mid-pack in turnover at the 58.6th percentile; this project eliminated every
functional neighbourhood it tested. **Against:** furniture is usually long-lived, and 66.4 h with
continuous rebuilding at 100,000 copies per cell is expensive for nothing; and the conserved sealed
pocket argues against pure inertness. **Decides it:** nothing cheap. This is the null that survives by
default, which is exactly why it needs stating.

### A6. COP1 ubiquitinates MVP, making vault abundance a regulated quantity. **~10%**
COP1 is at **+4.74 (≈27-fold), LWTP 2.59, not PARP4-dependent**, with independent 2014 TAP support.
**For:** best-measured non-subunit partner in the project. **Against:** one instrument *class*;
**DDB1 is present in the universe and is not an interactor**, which is positive evidence for free COP1
over an assembled CRL4; and §49c shows degradation machinery is the **most depleted annotation of
1,276**. **Decides it:** Paper 2 Experiment 12.

### A7. The vault is a vtRNA chaperone, and the protein shell exists to protect the RNA. **~8%**
Inverts the usual framing: the particle is for the vtRNA, not the reverse. **For:** vtRNAs are
otherwise hard to account for, and a 13 MDa shell is a plausible RNase shelter. **Against:** we never
tested it; §20's transcript-level test of the vtRNA-p62 axis found nothing. **Decides it:** vtRNA
stability in MVP-null cells by Northern or RT-qPCR with a spike-in.

### A8. The vault is a mechanical element — a pressure or crowding buffer. **~6%**
A 13 MDa hollow barrel at high copy number is a large excluded volume. **For:** explains abundance
without requiring chemistry, and explains the absence of any detectable partner module. **Against:**
no evidence of any kind, and it is close to unfalsifiable with current tools. **Decides it:** cell
stiffness or crowding-sensor readouts in MVP-null versus wild type.

### A9. The vault is an unconventional export vehicle whose cargo differs when exported. **~6%**
Graham's hypothesis, and the sharpest version is the cargo clause rather than the export clause.
**For:** MVP-dependent miR-193a loading into exosomes is published as a disposal route; MVP is
released non-exosomally; §49c shows the particle is *anti*-associated with intracellular degradation
machinery. **Against:** §59 found MVP in mucus at a level that does not distinguish export from
leakage; PARP4 and TEP1 are absent there. **Decides it:** Paper 2 Experiment 13, on the 35,000 × g
pellet.

### A10. The vault's tissue distribution reflects xenobiotic flux, not cell type. **~5%**
MVP is high in gut epithelium, lung and adrenal. **For:** matches the LRP drug-resistance literature,
and adrenal has unusual steroid and xenobiotic traffic. **Against:** §97 showed adrenal is #1 for the
**shell only** while the armed holoenzyme peaks in gut mucosa, so "the vault" is not one thing across
tissues; and Izquierdo 1996 mapped this distribution thirty years ago. **Decides it:** holoenzyme
versus shell ratio against measured xenobiotic exposure per tissue.

---

## Part B — Top 10 things we learned about vaults that appear unnoted elsewhere

Each carries what kind of claim it is: **[new observation]** (we measured something nobody has),
**[new reading]** (the data are published, the observation is not), or **[uncertain novelty]**.

### B1. TEP1 binds the vault independently of PARP4. ~~**~75%**~~ **DEMOTED to ~20% — see §66b** — [new reading]

> **[The conclusion is published and has been for ~25 years.** Grok declined to rank this and was
> right. MVP-only recombinant vaults assemble in Sf9 insect cells from ~96 copies of a single protein;
> TEP1-knockout mice contain structurally intact vault-like particles with reduced cap density;
> VPARP/PARP4-knockout mice are viable without major phenotype; and **"VPARP and TEP1 are able to
> incorporate into vaults even after the formation of the MVP vault particle shell is complete"** —
> independent incorporation, explicitly in print. What survives is only the quantitative human-cell
> demonstration below. **I ranked this first of ten.]**
PARP4 knockdown leaves TEP1 untouched (**WTKD_LFC 0.154, WTKD_P 0.020**) while PARP4 itself is
strongly dependent (5.51, 2.85), and MVP is unaffected, so the particle survives the knockdown. Both
registered gates passed. The knockdown columns are published; this reading of them is not one I can
find. **Why it matters:** the trimer is three independent associations, not a pair plus a passenger.

### B2. Myoferlin is actively excluded from the vault's vicinity. **~70%** — [new **reading**, corrected §66b]
**−2.23** in the anti-MVP pulldown and **−3.32 (p = 3.4e-4)** in pre-lysis covalent proximity
labelling around PARP4 — two instruments of different physics agreeing on a depletion. Negative
results of this specificity are rarely published, and MYOF had been this project's strongest
membrane-repair evidence.

### B3. Degradation machinery is the most depleted annotation in an anti-MVP pulldown. **~65%** — [new **reading**, corrected §66b]
Proteasomal protein catabolism at mean **−1.066**, the **0.0 percentile of 1,276 terms**; protein
catabolic process −0.839; macroautophagy −1.163. **Anti-associated, not merely absent.** Constrains
every disposal model, including A6 and A9.

### B4. Published stool proteomics cannot see a vault, for two independent reasons. **~65%** — [new reading]
The canonical workflow spins at 2,500 × g then **35,000 × g and discards the pellet** — the range in
which vaults are *purified*. And the one dataset that retains the pellet and searched a human database
recovers a lumenal secretome with **no beta-actin, no GAPDH, no HSC70**, so cytoplasmic protein does
not survive the colon. Explains an absence everyone would otherwise read as biological.

### B5. CFdb scores MVP-TEP1 at the noise floor while MVP-PARP4 is at the 99.99th percentile. **~60%** — [new observation]
**0.041 against 0.676.** TEP1 is a genuine PARP4-independent interactor (B1), so this is a
**sensitivity failure of a major co-fractionation resource on a known subunit** — and any
high-confidence cutoff that retains TEP1 admits 1,733 MVP partners.

### B6. MVP is present in human colonic and ileal mucus. **~55%** — [new reading]
**52 unique peptides**, 94.4th percentile of 853 proteins in colon and 94.8th of 1,457 in ileum, in
van der Post 2019. The table is published; nobody appears to have remarked on it. **Export and leakage
are not distinguished** (§63d), and PARP4 and TEP1 are absent.

### B7. MVP's co-elution tail is specifically translation-enriched. **~50%** — [new observation]
**18.49x at the 98.0th percentile of 150 degree-eligible seeds**, with glycolytic controls at the
26th-79th and MVP's own SPFH relatives at the 41st-70th, surviving controls for degree, abundance,
family and apparent mass. Unpromoted because one instrument cannot separate it from a shared
hydrodynamic window — but the observation is solid and, I believe, unreported.

### B8. The adrenal gland is top-ranked for the vault shell only; the armed holoenzyme peaks in gut mucosa. **~45%** — [new reading]
MVP, PARP4 and TEP1 do not co-rank across tissues, so **"vault abundance" is not one quantity**. This
reframes a distribution that has been in the literature since 1996 and is routinely quoted as if the
particle were uniform.

### B9. ANXA2 and S100A10 are the only confirmed non-subunit interactors of the classical membrane list. **~40%** — [new **reading**, corrected §66b]
ANXA2 **+1.74 (LWTP 2.62)** and S100A10 **+2.11 (2.69)**, neither PARP4-dependent, surviving every
instrument applied — while EHD2, AHNAK and MYOF fail and EHD4, CAPN2 and IQGAP1 were never tested at
all. The *shape* of the list matters as much as its members.

### B10. MVP's half-life is ordinary, and the subunits' mutual compatibility has never been tested. **~35%** — [new reading]
**66.4 h, 58.6th percentile of 8,804 proteins**, proteome median 56.5 h, against lamins and histones
at 1,500-1,700 h. So MVP is **not structural furniture** in the turnover sense. And the three subunit
half-lives (22.2 / 40.6 / 66.4 h) sit at the **29.86th percentile of random triplets** — less
dispersed than 70% of them — so the widely-implied "distinct lifetimes" reading has no support, and
equality was never tested either.

---

## What is deliberately absent

The methodological findings — degenerate matching, one-way gates, the three-answer sequence — are the
most transferable things this project produced and are **not** on either list, because the question was
about vaults. They are in `CONTRIBUTING.md` and RESULTS §41-§65.

---

## Addendum — A11, added after a user remark, and it outranks three of the original ten

Graham, on hearing that furniture is "usually long-lived" and "expensive": *"maybe it makes furniture
for the same reason that humans fart around - like Vonnegut. Maybe it just wants something else to do.
Doubtful, but maybe."*

That is **not** A5. Furniture implies a structural role. What this describes is **near-neutrality** —
constructive neutral evolution, a spandrel, something the cell keeps building because nothing stops
it. It is a distinct hypothesis and it deserved a test rather than a nod. Two were available in data
already here.

### Test 1 — the cost, which argues against it

MVP transcript abundance, HPA consensus, 20,162 genes across 51 tissues:

| tissue | MVP nTPM | percentile | PARP4 | TEP1 |
|---|---|---|---|---|
| adrenal gland | 176.2 | **97.5th** | 78.5th | 57.7th |
| duodenum | 145.6 | **97.3rd** | 88.8th | 84.5th |
| small intestine | 156.7 | **97.0th** | 86.2nd | 68.3rd |
| colon | 161.7 | **96.6th** | 84.2nd | 69.0th |
| lung | 119.8 | **96.3rd** | 82.5th | 62.5th |

**MVP is in the top 3-4% of all transcripts wherever vaults matter.** Pure drift does not usually
sustain that. Note also that **the shell is the expensive part and the catalytic subunits are not** —
PARP4 and TEP1 sit 10-40 percentile points lower throughout.

### Test 2 — the dispensability, which argues strongly for it

eggNOG v5 eukaryotes, the five orthogroups carrying a vault inter-alpha-trypsin domain:

| present | absent |
|---|---|
| human, mouse, chicken, *Xenopus*, zebrafish | ***Drosophila melanogaster*** |
| ***Dictyostelium discoideum*** | ***Caenorhabditis elegans*** |
| *Daphnia pulex*, *Nematostella vectensis* | *Saccharomyces cerevisiae*, *Arabidopsis thaliana* |
| | *Plasmodium falciparum*, *Leishmania major*, ***Ciona intestinalis*** |

**The pattern is repeated independent loss, which is the signature of a gene you can live without:**

- Present in *Dictyostelium* **and** animals, so it predates their divergence — the gene is ancient.
- **Crustaceans keep it (*Daphnia*) while insects lost it (*Drosophila*)** — lost within arthropods.
- ***Ciona*, a chordate, lacks it while every vertebrate checked has it** — lost within chordates.
- Absent from fungi, land plants and apicomplexans entirely.

An essential machine does not get discarded independently by insects, nematodes and tunicates.

**One caveat, stated because the raw number is the weak part:** only 210 of 5,090 eggNOG eukaryote
species carry the domain, which is **4.1%** — but genome databases are heavily over-weighted toward
fungi, all of which lack it, so that percentage is mostly a sampling artefact. **The reference-organism
loss pattern is the real evidence; the 4.1% is not.**

### A11. The vault is a tolerated extravagance — near-neutral, not functional. **~14%**

Ranked above A5 (furniture, 12%), A6 (COP1, 10%), A7 (vtRNA chaperone, 8%), A8 (mechanical, 6%),
A9 (export, 6%) and A10 (xenobiotic flux, 5%).

**For:** repeated independent loss by whole phyla; no fitness coupling in CRISPR screens; and the
single largest result of this project — ~40 registered tests finding **no functional neighbourhood of
any kind** — is exactly what near-neutrality predicts and what every functional hypothesis has failed
to deliver.

**Against:** the 96-97th percentile expression. Constructive neutral evolution explains *retention*
cheaply but explains *high expression* poorly; drift does not usually hold a gene in the top 3% of the
transcriptome across five tissues.

**What would decide it:** dN/dS across the lineages that retained it, against paralogues and against
genes of matched expression. Near-neutrality predicts dN/dS approaching 1 and no detectable purifying
selection on the SPFH pocket; a quantitative function predicts strong purifying selection on the
pocket specifically while the shell's bulk drifts. **That is a computable test on sequence data and it
has not been run here.**

**Why it ranks where it does:** the loss pattern is strong evidence and the expression level is strong
counter-evidence, and they do not cancel — they point at a third possibility, that the vault is under
selection for *capacity* rather than *activity*, which is A1's buffer hypothesis arriving from the
other direction. **A1 and A11 are the two hypotheses this project's evidence actually favours, and
both predict exactly the absence of partners that we spent forty tests confirming.**


---

## Addendum 2 — three hypotheses I missed, added after Grok's independent list (§66a)

**A12. The bare MVP shell is what the cell invests in; PARP4 and TEP1 are optional, independently
docked passengers. ~35%** — Grok's top item at 0.40, and **it would now rank first on my list too.**
I held every piece and never assembled it: adrenal ranks first for the shell alone, the holoenzyme
peaks in gut mucosa, TEP1 is PARP4-independent, CFdb splits them, and **my own A11 test found MVP's
transcript at the 96-97th percentile while PARP4 sits at 78-89 and TEP1 at 58-85.** The literature
checked in §66b supports it further: MVP alone forms the shell, and caps add afterwards. I rate it
slightly below Grok because "what the cell invests in" is not yet a function — it relocates the
question to the shell rather than answering it. **Decides it:** cap occupancy per particle by cryo-ET,
adrenal versus gut mucosa; under 10% in both keeps the bare shell as the object of investment.

**A13. ANXA2-S100A10 heterotetramer as a membrane dock. ~12%** — I had both in the novelty list and
never made them a hypothesis. They are an obligate heterotetramer, which is harder to dismiss than
either hit alone, and ATP7A at +2.38 points the same way. **Against:** the surrounding membrane module
is positively absent — MYOF excluded twice, EHD2 and AHNAK failing, ruffle below its matched null.
**Decides it:** S100A10 knockout, then in-cell crosslinking of MVP to ANXA2; dies if the crosslink
survives S100A10 loss, and dies if it appears only after lysis.

**A14. Multidrug sequestration, taken seriously rather than dismissed. ~5%** — I had folded this into
a tissue-flux framing (A10) and missed Grok's sharper point: **nothing in this project measures a
drug**, so a small-molecule sequestration model leaves no proteomic trace and **none of our forty
tests contradicts it.** Against it: lung is 5th of 51 despite the protein's name, no xenobiotic
transporter is among the 88 interactors, and MVP-null mice are viable without a clean drug-sensitivity
phenotype. **Decides it:** steady-state doxorubicin, nuclear versus vault-associated, MVP-null against
wild type at matched uptake.
