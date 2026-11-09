# Vault function: ten hypotheses, and ten candidate novel findings

> **STANDING (added §84b; number superseded §90, cut to one significant figure §102b):** the one
> positive measurement in this project is that **MVP is under strong purifying selection where it is
> retained** - a codon-model (`codeml` M0) **omega of 0.06 across 11 vertebrates**, with an
> essential-gene control at **0.05** and a relaxed control at **0.4** - MVP at **1.2x** the essential
> control and about **one-seventh** of the relaxed one, stated as ratios because a row of three figures
> performs the retracted equality (§103). The earlier pairwise NG86
> figure of 0.1118 **understated** it. **Two limits travel with the number:** there is **no interval
> on any of these estimates**, so no equality with the essential control is claimed; and the panel is
> **keeper-only by construction**, since only retained orthologues remain alignable. It **constrains**
> this list rather than picking a winner: it refuses the two nulls, and it is neutral between every
> hypothesis that requires the protein to do something.


**Consolidated 2026-11-07.** The original lists were written at 20:24:07 and committed before Grok was
asked the same two questions (`git log` is the record); five rounds of correction followed. This file
now leads with the final rankings. The record of what changed sits at the end rather than as stacked
addenda — nothing is deleted, but the current state should be readable first.

> ### Two standing qualifications
>
> **Provenance.** Every interactor number here — `WT_LFC`, `LWTP`, `WTKD_*` — comes from one dataset:
> **PRIDE PXD052802**, co-IP of MVP with the synthetic antigen binding reagent VM1 against control H6,
> in **wild-type versus PARP4-knockout A549 cells**, a lung adenocarcinoma line. **The deposit's own
> description analyses the same contrast we used**, so these are readings of public data, not
> discoveries of this work, and may be line-specific. **"Not PARP4-dependent" everywhere means "still
> present when PARP4 is removed in A549."** We did not establish the cell line until §71.
>
> **The published function.** Knockout work establishes MVP as a **signalling modulator** — but the
> convergence is **mostly one group's**: Jingjing Ben appears on 5 of the 6 papers and only the
> influenza study shares no author with any other (§76b). Read it as **one programme plus one
> independent replication**, not six independent results —
> IKK-NF-kB, calcineurin-NFATc1, STAT3, Parkin-mediated mitophagy, adaptive immunity on influenza
> rechallenge — and **every published phenotype is conditional**, absent at baseline. Those
> interactions are transient and low-stoichiometry: what co-abundance, co-fractionation and wash-based
> IP recover worst. **So no negative in this project is evidence against vault function.** §70.

---

## Part A — Ten hypotheses for what vaults are for, ranked

Probabilities are my judgement that each is substantially correct. **A signalling-modulator hypothesis
is deliberately absent: it is not untested, it is established** (see the standing qualification above).
What remains untested is which mechanism, and whether it is the shell's or the caps'.

| # | hypothesis | P | strongest point for | strongest point against | decided by |
|---|---|---|---|---|---|
| **1** | **The bare MVP shell is the functional unit**; PARP4 and TEP1 are optional, independently docked passengers | **0.45** | **MVP binds NAD+ with PARP4 unnecessary for the interaction, structurally resolved (§73b)** — a published function of the shell itself; adrenal ranks first for the shell alone while the armed holoenzyme peaks in gut mucosa; MVP transcript at the 96th-97th percentile against PARP4's 78-89 and TEP1's 58-85; MVP alone forms vaults in Sf9 cells | "what the cell invests in" relocates the question rather than answering it | cap occupancy per particle by cryo-ET, adrenal vs gut mucosa |
| **2** | **The published signalling function is the shell's, not the caps'** | **0.30** | every published functional result uses MVP knockout, which removes shell and particle together, so none separates them | no direct evidence either way yet | Experiment 15: PARP4/TEP1 double-null retains a bare shell |
| 3 | **Multi-client sequestration cage**, free COP1 the one supported client | 0.24 | COP1 at +4.74 (~27-fold), not PARP4-dependent; 0 of 1,276 GO terms enriched is what unrelated clients look like | one instrument class; DDB1 detected and not an interactor | MVP point mutant losing COP1, with in-cell crosslinking |
| 4 | **TEP1 is an oligomerisation-activated TIR NAD(P)ase** (E1008) | **0.25** | TIR fold with the catalytic glutamate; NAD(P) consumption is itself a signalling mechanism, which fits the published pathway work | no activity measurement exists; most shells lack the enzyme | NAD+ consumption, monomer vs forced oligomer, E1008 control |
| ~~5~~ | ~~**Nucleotide-sequestering buffer** — 78 sealed SPFH-shoulder pockets~~ **WITHDRAWN, §73** | ~~0.20~~ | — | **the pocket is published (Lodwick et al., *Nat Commun* 2025, PMID 40691181, NAD+ and ADP modelled in 9MXH/9MXV) and "sealed" is contradicted: it is lumen-facing, read as solvent-accessible, and formed *between* two monomers, so assembly creates it rather than closing it** | already done |
| 6 | Polyribosome assembly or quality-control platform | 0.15 | co-elution tail translation-enriched at the 98.0th percentile of 150 seeds, surviving degree, abundance, family and mass controls | no CFdb-only statistic separates this from a shared hydrodynamic window | Experiment 14: puromycin dissociation |
| 7 | ANXA2-S100A10 heterotetramer membrane dock | 0.12 | an obligate heterotetramer is harder to dismiss than either hit alone; ATP7A points the same way | the surrounding membrane module is positively absent | S100A10 knockout then MVP-ANXA2 crosslinking |
| ~~8~~ | ~~The sealed pocket is a ligand-gated latch for waist opening~~ **WITHDRAWN, §73** | ~~0.12~~ | — | same grounds; the published **keyhole-loop gating** is a real adjacent mechanism, but it is loop gating, not shell sealing | — |
| 9 | Cargo turnover rather than transport | 0.12 | PARP4 at 22.2 h against the shell's 66.4 h | a substoichiometric protein has an expected free pool that can dominate | 2-df Wald test on pulse-SILAC fit covariance |
| 10 | vtRNA chaperone — the shell exists for the RNA | 0.08 | vtRNAs are otherwise hard to account for; a 13 MDa shell is a plausible RNase shelter | never tested; §20's transcript-level test found nothing | vtRNA stability in MVP-null cells |

**Below the line:** mechanical/crowding buffer 0.06 · export with altered cargo 0.06 · multidrug
sequestration 0.05 · tissue pattern tracks xenobiotic flux 0.05 · ~~**furniture with no acute function
0.04**~~ **-> 0.01** · ~~**near-neutral tolerated extravagance 0.03**~~ **-> 0.01**.

> **Both nulls are downgraded on a measurement, not a judgement (§84b, now §90).** MVP's codon-model
> omega across **11 vertebrate orthologues is 0.06** - near an essential-gene control at 0.05 and far
> from a relaxed control at 0.4. A gene that is drifting, or tolerated as inert extravagance, does
> not look like that. **The downgrade does not depend on the third digit or on the superseded pairwise
> value**, which is why it survived both audits. **They are no longer merely
> unsupported; they are contradicted.** They stay on the list at 0.01 rather than being deleted,
> because a ranking that erases its own null is dishonest - and because selection is not proof of a
> *current* function in humans; it is proof that something, somewhere in these lineages, is paying.

---

## Part B — Ten candidate novel findings, with check status

**Five literature checks have been run and all five found prior art** — the fifth inside our own
`data/raw/struct/` directory (§73d). These are **candidates, not
findings**. A probability on an unchecked row is an opinion about data, not a claim about the
literature, and the base rate says expect attrition.

| # | candidate | P | checked | type |
|---|---|---|---|---|
| **1** | **Published stool proteomics cannot see a vault** — the canonical workflow discards the 35,000 x g pellet, the range vaults are purified in; and the one dataset retaining it recovers a lumenal secretome with no beta-actin, GAPDH or HSC70 | ~~0.65~~ **0.35** | **yes — splits** | **the general principle is published** (see below); the vault application is not |
| 2 | **CFdb scores MVP-TEP1 at the noise floor** (0.041 against PARP4's 0.676) — a sensitivity failure of a public resource on a known subunit; any cutoff retaining TEP1 admits 1,733 partners | 0.60 | no | new observation |
| 3 | **The interferon co-abundance block is a STAT1/IRF9 regulon** — residualising until TAP1 leaves MVP's top 200 collapses it to CNS only | 0.60 | no | new reading |
| 4 | **MVP is present in human colonic and ileal mucus** — 52 unique peptides, 94.4th and 94.8th percentiles | 0.55 | no | new reading |
| 5 | **The ruffle signal dies at contact** — 13 observed against 3.1 expected across three cohorts in co-abundance, flat and below its matched null in the pulldown | 0.55 | no | new observation |
| 6 | MVP's co-elution tail is specifically translation-enriched, surviving four controls | 0.50 | no | new observation |
| 7 | **Adrenal ranks first for the shell only**; the armed holoenzyme peaks in gut mucosa, so "vault abundance" is not one quantity | 0.45 | no | new reading |
| 8 | The three subunit half-lives were never tested for mutual compatibility — spread at the 29.86th percentile of random triplets | 0.40 | no | new reading |
| 9 | ANXA2 and S100A10 are the only confirmed survivors of the classical membrane list, and the shape of that list matters | 0.30 | partial | new reading |
| 10 | Myoferlin is actively excluded — depleted in the pulldown and in pre-lysis covalent proximity labelling | 0.25 | partial | new reading |

**#1 splits on checking.** The general methods principle is published: a 2021 *J. Proteomics* study is
titled around the finding that *"metaproteomic sample preparation methods bias the recovery of host and
microbial proteins according to taxa and **cellular compartment**"*, and Tanca et al. 2015 — whose
companion paper is called *"Enrichment or depletion? The impact of stool pretreatment on metaproteomic
characterization of the human gut microbiota"* — established that differential centrifugation
significantly changes what is recovered. **What we could not find published is any source quantifying
the loss of host *cytoplasmic* protein to lumen degradation, or applying the bias to a megadalton
particle.** So the methods insight is known and the vault application is ours, which is a narrower
claim than we made.

**The pattern is the most useful row in the table: every candidate that reads a published interactor
list has fallen, and every candidate resting on a methods argument or an unremarked row in someone
else's table still stands.** #1 is best-standing precisely because it is about other people's
protocols rather than a careful read of their data.

---

## What changed, and why

| claim | was | now | killed by |
|---|---|---|---|
| TEP1 binds the vault independently of PARP4 | 0.75, ranked **first** | **0.08** | ~25-year literature: MVP-only Sf9 vaults, TEP1-KO vaults intact, caps incorporate into preformed shells — plus the dataset's own PARP4-KO analysis (§66b, §71c) |
| MVP ancestral in eukaryotes, lost in fungi/plants/Ecdysozoa | presented as a finding | **withdrawn** | Daly et al. 2013 reached it verbatim (§69a); and we had censused VIT-domain groups, not MVP's own orthogroup (§68) |
| Degradation machinery most depleted of 1,276 terms | 0.65 | 0.25 | dataset provenance (§71c) |
| Near-neutral "tolerated extravagance" | 0.14 | **0.01** (was 0.03; §84b) | *Dictyostelium* MVP knockouts have reduced survival under nutrient stress; five systems show conditional phenotypes (§69c, §70) |
| Furniture with no acute function | 0.12 | **0.01** (was 0.04; §84b) | same |
| Our "no fitness coupling" | read as "no function" | **read as "no function in rich medium"** | every published model is also normal at baseline (§70b) |
| The bare shell hypothesis | absent from our list | **ranked first** | Grok's independent list; we held every component and never assembled it (§66a) |

**Three further hypotheses we omitted and Grok supplied:** the bare shell (now #1), the ANXA2-S100A10
dock (#7), and multidrug sequestration taken seriously on the grounds that **nothing in this project
measures a drug**, so none of its forty tests contradicts it.

**Two novelty candidates we omitted and Grok supplied:** the interferon regulon (#3 above) and the
ruffle collapse (#5) — the first being the cleanest piece of negative work in the project, left off our
own list of unremarked findings.
