# Two calibration findings for interaction-proteomics pipelines

**This is the only part of this project we think is useful to someone who does not work on vaults.**
It is short on purpose. Both findings say an instrument fails in a specific, predictable direction, and
both are actionable without believing anything about vault biology.

Two independent assessments — ours and an adversarial reviewer's, each written before seeing the other
— ranked these the same two findings, out of ten candidates, and **zeroed most of the rest**. See
`USEFULNESS.md` for that comparison and `RESULTS.md` §75 for the disagreements.

---

## 1. Native co-fractionation cannot retain a real subunit without drowning you

### The observation

In **CFdb** (Skinnider & Foster co-fractionation compendium; 411 datasets, ~47.5M scored human pairs),
for seed protein **MVP** across its 10,614 scored partners:

| edge | precision | status |
|---|---|---|
| **MVP–PARP4** | **0.676** — 99.99th percentile | true subunit, cleanly recovered |
| **MVP–TEP1** | **0.041** — noise floor | **true subunit, missed** |

MVP's partner count as a function of the precision cutoff:

| cutoff | MVP partners retained | TEP1 retained? |
|---|---|---|
| ≥ 0.676 | **0** | no |
| ≥ 0.5 | 1 | no |
| ≥ 0.25 | 29 | no |
| ≥ 0.1 | 357 | no |
| **≥ 0.041** | **1,733** | **yes** |

**TEP1 is a genuine stoichiometric member of the vault particle** — recovered in an anti-MVP pulldown,
and TEP1-knockout mice contain vault particles with reduced cap density. It is not a borderline
assignment.

### The useful statement

**There is no threshold on this resource that both retains a known stoichiometric subunit and returns a
followable list.** You lose TEP1, or you inherit 1,733 candidates. This is not a tuning problem.

### Why it is diagnostic rather than a complaint

**MVP–PARP4 at 0.676 in the same database** proves CFdb *can* rank a true vault subunit far above
noise. So the failure is not "this seed has no signal" and not "vaults do not co-fractionate" — it is
**subunit-specific**. The confirming evidence comes from different physics (affinity pulldown), which
is what a calibration pair requires: you are not validating co-fractionation with co-fractionation.

**The mechanism is predictable.** TEP1 is substoichiometric and large. Low copy number gives fewer
peptides, a noisier elution profile, and worse profile correlation. So the bias has a direction:
**co-fractionation recall falls with subunit abundance.** It is not random noise.

### What to do with it

**If you are writing a negative from co-fractionation** — *"X and Y are not in a complex, no
high-confidence co-elution edge"* — this is a counterexample where that inference was wrong for a real
subunit of a well-characterised complex.

**If you are building or using an interactome integrator**, this is the larger use. Integrators combine
channels (co-fractionation, AP-MS, co-expression, literature), and many treat them as **voters**,
requiring two or more to agree before calling an interaction. MVP–TEP1 shows co-fractionation
systematically misses **low-detectability true subunits** — so a voting scheme drops exactly the
hardest-to-detect members and keeps the abundant ones. **That is a systematic bias toward abundant
complex members, not a random error rate.**

Two concrete changes:

1. **Score channels as asymmetric sensors.** Co-fractionation is high-precision, low-recall for
   low-abundance subunits. Weighting it as an equal vote imports the bias.
2. **Keep a discordant true edge in your regression suite.** `calibration_edges.tsv` in this directory
   holds MVP–TEP1 and MVP–PARP4 in machine-readable form. **If your pipeline drops MVP–TEP1, your
   recall problem is live and you now know it.**

### Honest limit

**This is one pair.** It establishes that the failure mode exists and gives you a test case. It does
**not** quantify a false-negative rate. The study that would is a survey of known-complex subunits
against their co-fractionation scores, **stratified by subunit abundance** — which, as far as we found,
nobody has published.

---

## 2. A stopping rule for separating co-regulation from co-complex

### The problem

Co-abundance and co-expression confound two different things. If a transcription-factor pair drives a
program, every gene in that program co-varies across samples **whether or not the proteins ever touch**.
Guilt-by-association then reports a "module" that is a regulon.

Residualising on the drivers is the obvious fix and it has no natural stopping point. Too little and
the regulon survives; too much and you remove real signal. In practice this is where the analysis
stops being falsifiable.

### The rule

1. **Identify the regulon's drivers.** In our case STAT1 and IRF9.
2. **Pre-select a canonical target** of that regulon — unambiguously a transcriptional target,
   unambiguously **not** a plausible physical partner of your seed. We used **TAP1**, a textbook
   interferon-stimulated gene.
3. **Residualise the seed's co-abundance profile on the drivers until the canonical target is displaced
   out of the seed's top N** (we used N = 200). At that point you have, by construction, removed enough
   to eliminate regulon-driven covariance.
4. **Require it in every dataset, not on average.** Ours held in five of five.
5. **Then look at what remains.**

### Why it is useful

It converts a judgement call into a **pre-registerable, reader-checkable criterion**. The alternatives
are: do not residualise (overclaim), residualise by eye (unfalsifiable), or remove an arbitrary number
of principal components (unjustified).

**The audience is wide.** It applies to any co-expression or co-abundance module that might sit inside a
regulon — WGCNA modules in vaccinology, where interferon modules are ubiquitous; interferonopathy;
hypoxia and HIF; ATF4 and heat-shock stress programs; NF-kB. And it costs nothing: you need the driver
TFs, one canonical target, and data you already have.

### Honest limits

**It is a heuristic with a defensible logic, not a theorem.** Choice of canonical target and of N both
matter, and both must be fixed in advance.

**And the residue is not a finding.** In our case the block collapsed to a single tissue class
(central nervous system). **That is what tissue-identity covariance looks like after a regulon is
removed** — it does not license an experiment on the residue. **The rule travels; the leftover does
not.**

---

## Provenance and credibility

The interactor numbers cited here come from **PRIDE PXD052802** — co-IP of MVP with synthetic antigen
binding reagent VM1 against control H6, in wild-type versus PARP4-knockout **A549** cells — whose
depositors analysed the same contrast (Lodwick et al., *Nat Commun* 2025, PMID 40691181). They are
readings of public data.

**This project shipped real analysis bugs**, documented in `LEDGER.md`: a degenerate three-way matching
scheme read for two sections, a frame-indexing error that reached the published ledger, and a
specificity control with no power to fail. A reader is entitled to ask whether these two findings came
through any of that. **They did not, and it is checkable:**

```
$ grep -c "'ld'\|'cd'\|index=list(seq)\|qcut" src/smc56.py src/mass_confound.py src/ifn_residual.py
```

All three return **0**. Both findings are direct score lookups and residualisations with **no
matched-null machinery at all**, so the degenerate matcher cannot reach them. The one CFdb parsing bug
that did occur was caught by a registered positive control before any result was read, and the fix is
present in all three CFdb readers.
