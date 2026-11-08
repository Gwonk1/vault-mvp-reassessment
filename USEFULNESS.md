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
vaults: the **thirteen house rules and two enforced gates** in `CONTRIBUTING.md` and
`src/check_retractions.py`. One-way gates, a control with no power to fail, a refusal band wider than
its estimator, three criteria that measured the wrong quantity, a degenerate matching scheme read for
two sections, the same indexing bug three times, one correction propagated through four documents one at
a time, two gates passing vacuously on paraphrase, and the literature gate never built until five
checks had each found prior art. **Every one is a failure mode available to anyone running
pre-registered computational tests, and each is written with the number that exposed it.**

**The uncomfortable version of the answer:** the project's useful output is a list of ways to be wrong,
produced by being wrong in all of them.
