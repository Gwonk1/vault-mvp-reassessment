# Is any of it useful to anyone? — Claude's assessment

**Written 2026-11-07 and committed before Grok was asked the same question**, so the independence is
checkable from `git log`.

**Usefulness is a different question from novelty, and the orderings barely overlap.** A finding can be
unoriginal and still save someone an experiment; it can be original and change nobody's decision. Below
is the ten ranked by *who could act on it*, with the novelty rank beside it for contrast.

> Standing qualification: every interactor number here comes from **PRIDE PXD052802** (VM1/H6 co-IP,
> wild-type versus PARP4-knockout **A549** cells) whose depositors analysed the same contrast — so these
> are readings of public data, possibly line-specific. See §71.

| useful rank | finding | who acts on it, and how | novelty rank |
|---|---|---|---|
| **1** | **CFdb misses MVP-TEP1 at the noise floor** — 0.041 against PARP4's 0.676, and any cutoff retaining TEP1 admits 1,733 partners | **Anyone drawing a negative inference from a co-fractionation resource.** This is a calibration datapoint: the resource **fails to recover a genuine stoichiometric subunit of a known complex.** If you are about to write "X does not interact with Y, no high-confidence edge", this says your false-negative rate can be high enough to miss a real subunit. **Applies far beyond vaults.** | 2 |
| **2** | **Published stool proteomics cannot recover a vault** — the canonical workflow spins at 2,500 then 35,000 x g and **discards the pellet**; the one dataset that keeps it recovers a lumenal secretome with no beta-actin, GAPDH or HSC70 | **Anyone designing a stool or gut-lumen proteomics experiment to look for a particle or a cytoplasmic protein.** Two concrete design changes: **keep the 35,000 x g pellet**, and use **targeted detection** rather than shotgun, because shotgun in that matrix cannot see cytoplasmic protein whether or not it is there. Saves a whole experiment that would read as a clean negative. | 1 |
| **3** | **The interferon co-abundance block is a STAT1/IRF9 regulon** — residualise on the regulon drivers until a canonical target (TAP1) leaves the seed's top 200, and the block collapses to CNS only | **Anyone separating co-regulation from co-complex in any co-abundance dataset.** The *technique* is the useful part: using the exit of a canonical target as the **stopping rule** for residualisation is reusable on any transcriptionally-driven block in any compendium. Nothing about this is vault-specific. | 3 |
| **4** | **"Vault abundance" is not one quantity** — adrenal ranks first for the shell alone while the armed holoenzyme peaks in gut mucosa; MVP, PARP4 and TEP1 do not co-rank across tissues | **Anyone quoting MVP tissue levels as vault levels** — which is the standard reading of the classic Izquierdo distribution. If shell and caps have different tissue profiles, an MVP measurement is not a particle measurement, and tissue comparisons built on MVP alone may be comparing different objects. | 7 |
| **5** | **The three subunit half-lives were never tested for mutual compatibility** — 22.2 / 40.6 / 66.4 h, spread at the 29.86th percentile of random triplets | **Anyone holding pulse-SILAC fits.** This comes with a named test and a power requirement: a **2-df Wald or likelihood-ratio test of k_MVP = k_TEP1 = k_PARP4 on the fit covariance**, needing a per-rate CV of 22.6% or better for 80% power on the observed MVP-PARP4 gap. **Runnable today by anyone with the replicate SEs**, and it decides a claim the field states loosely. | 8 |
| 6 | **Myoferlin is actively excluded** — depleted in the pulldown and in pre-lysis covalent proximity labelling around PARP4 | Anyone pursuing a myoferlin-vault link. Two instruments of different physics agree on **exclusion**, so a membrane-repair model built on MYOF starts from a wrong premise. Negative, specific, saves effort. | 10 |
| 7 | **The ruffle signal dies at contact** — 13 observed against 3.1 expected across three cohorts in co-abundance, flat and below its matched null in the pulldown | Anyone building on MVP migration or ruffling phenotypes. Co-abundance supports it, contact does not — which does not refute the phenotype but does say **co-abundance is not evidence for a physical ruffle association.** | 5 |
| 8 | **MVP is present in human colonic and ileal mucus** — 52 unique peptides, 94th-95th percentile | A datapoint for anyone studying mucus proteomes or vault release. **Export and leakage are not distinguished**, so it changes no decision on its own. | 4 |
| 9 | MVP's co-elution tail is translation-enriched, surviving four controls | Unpromotable with one instrument, and no CFdb-only statistic can finish it. Of interest to someone with an orthogonal instrument; useless otherwise. | 6 |
| 10 | ANXA2/S100A10 the only survivors of the classical membrane list | A549-specific and resting on the depositors' own list. Mildly useful as a prioritisation hint. | 9 |

## The answer to the question as asked

**Yes — but almost entirely as methods warnings, not as biology.** The top five are all "here is an
instrument or a design that will mislead you, and here is what to do instead." Not one of them tells
anyone what a vault does.

**And the most useful output of the project is not on this list at all**, because the list was scoped to
vaults: the **fifteen house rules and two enforced gates** in `CONTRIBUTING.md` and
`src/check_retractions.py`. One-way gates, a control with no power to fail, a refusal band wider than
its estimator, three criteria that measured the wrong quantity, a degenerate matching scheme read for
two sections, the same indexing bug three times, one correction propagated through four documents one at
a time, two gates passing vacuously on paraphrase, and the literature gate never built until five
checks had each found prior art. **Every one is a failure mode available to anyone running
pre-registered computational tests, and each is written with the number that exposed it.**

**The uncomfortable version of the answer:** the project's useful output is a list of ways to be wrong,
produced by being wrong in all of them.

---

# Grok's independent answer, and where it beats mine (§75)

Requested after the above was committed (21:36:01). **It gives six zeros where I gave none, and it wins
most of the disagreements.**

## Where we agree

**Finding 1 (CFdb MVP-TEP1) is rank 1 for both of us**, independently. And finding 3 (the interferon
regulon) is top-three for both. Those are the only two items both assessments call useful without
qualification.

## Where it beats me

**It zeros my rank 2.** I put the stool-proteomics finding second. Grok: *"Nobody running standard stool
proteomics is trying to recover vaults; they discard that pellet on purpose. Nobody running a vault lab
is handed a workable alternative dataset. No protocol change follows for either job."* **The finding has
no actor** — I assumed one existed on both sides and neither does. That is the single best correction in
the exchange.

**It zeros my rank 4** — "vault abundance is not one quantity" — with a better analysis than mine:
*"Measuring the minor subunits before calling a tissue 'vault-high' is ordinary multi-subunit practice.
Switching purification from adrenal to gut mucosa on the belief that bulk co-ranking is an armed
holoenzyme does not survive: tissue ranks do not establish co-assembly."* **The safe reading is standard
practice; the interesting reading invites a bad experiment.** I had only seen the first half.

**It catches false precision I have been repeating all day.** *"Three-decimal half-lives are false
precision against a CV bar of 22.6% (about 15 h on the MVP estimate)."* We have been quoting
**66.359 h** for a quantity whose own power calculation implies **±15 h**.

**And it wins the argument about the methods pile, which I had called the most useful output.** Grok:
*"They travel as advice the field has already been given in other words. They do not travel as an
artefact: the scripts are internal... Finding 1 is a number a stranger can put in a test harness. The
rules, as specified here, are not."* That is right. I over-valued the house rules because they were
expensive to learn here, not because they are useful elsewhere — which is the same error as valuing a
finding by how hard it was to get.

## Where it finds uses I did not

**A better generalisation of finding 1.** Not "CFdb misses a vault subunit" but: **MVP-TEP1 is a
discordant edge** — noise in co-fractionation, solid in a pulldown. *"Any integrator that treats
channels as voters, or that intersects co-fractionation with affinity data before it will call a
subunit, will systematically drop low-detectability true subunits and keep the abundant ones. The action
is to score channels as asymmetric sensors and to keep at least one discordant true edge in the
regression suite."* **MVP-TEP1 as a regression-suite test case for interactome integrators** — that
applies to every multi-subunit machine those databases cover.

**A bigger audience for finding 3 than I identified.** The canonical-target stopping rule *"ports to any
co-expression or co-abundance 'complex' that actually sits inside a regulon. The user base is WGCNA and
co-expression mining in vaccinology, interferonopathy, hypoxia, and stress responses, which is larger
than the set of people thresholding CFdb."*

**Two exports I missed entirely:**
1. **van der Post 2019's intracellular tag classifies nothing** — 79% of both proteomes carry it — so
   anyone mining that paper for secreted or mucus-core proteins must use a different column. A usable
   warning about a specific published dataset, independent of vaults.
2. **Finding 8's unrun design is the useful object**, for pulse-SILAC groups comparing subunit
   half-lives of the proteasome, ribosome or nuclear pore: a 2-df Wald test of equal rates on the fit
   covariance with a published CV bar. *"Other complex-turnover papers are using equally indirect
   functionals."*

## Its strongest argument, and the check it demanded

> *"This project's pipeline has already shipped a frame-index bug into a published ledger, run a
> specificity control that could only pass, and interpreted two sections of a matching scheme that was
> 49% singletons with the bait in its own cell... A stranger who cannot see which of the ten passed
> through the bad matcher or the bad index has a positive reason to change nothing until the figures are
> recomputed under the gates that now exist. **Usefulness of a reanalysis is zero while the numbers are
> incredible, however well aimed the conclusions are.**"*

That is the best point in six audits. **And it makes its own concession conditional and checkable:**
findings 1 and 3 survive *"if and only if those two were recomputed after the gates."*

**Checked.** Neither finding touches either contamination route:

| | 3-way decile matcher | `index=list(seq)` bug | any `qcut` matching |
|---|---|---|---|
| `smc56.py` (finding 1) | 0 | 0 | **0** |
| `mass_confound.py` (finding 1) | 0 | 0 | **0** |
| `ifn_residual.py` (finding 3) | 0 | 0 | **0** |

Both are direct score lookups and residualisations with **no matched-null machinery at all**, so the
degenerate matcher cannot reach them. The CFdb quote-parse bug — the one a registered gate caught — is
fixed in all three CFdb readers. **The condition is satisfied.**

## The joint verdict

**Two items are useful to a stranger, and both are instrument calibration rather than biology:**

1. **MVP-TEP1 as a discordant-edge test case** — refuse a global co-fractionation cutoff that cannot
   retain a true subunit without admitting 1,733 partners; keep a discordant true edge in any
   integrator's regression suite.
2. **The canonical-target stopping rule** — residualise on the regulon drivers until a pre-chosen target
   leaves the top-N, required in every dataset, before calling a co-abundance block a complex.

**Everything else is zero, or useful only to a lab already holding the specific lead.** And the thing I
nominated as most useful — the methodological record — loses to a single number that a stranger can put
in a test harness on Monday.
