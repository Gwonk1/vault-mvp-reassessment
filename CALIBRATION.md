# Two calibration findings for interaction-proteomics pipelines

> **Read the second one first if you only have a minute.** It is the sensitivity floor: three standard
> complex-detection signatures, measured against a particle whose membership has not been in dispute
> for decades, all three failing in different ways. The first finding is one of its three faces, in
> full detail.

**This is the only part of this project we think is useful to someone who does not work on vaults.**
It is short on purpose. Both findings say an instrument fails in a specific, predictable direction, and
both are actionable without believing anything about vault biology.

Two independent assessments — ours and an adversarial reviewer's, each written before seeing the other
— ranked these the same two findings, out of ten candidates, and **zeroed most of the rest**. See
`USEFULNESS.md` for that comparison and `RESULTS.md` §75 for the disagreements.

---

## 1. Native co-fractionation recovers this complex precisely, and completely only at an unfollowable cutoff

### The observation

In **CFdb** (Skinnider & Foster co-fractionation compendium; 411 datasets, ~47.5M scored human pairs),
for seed protein **MVP** across its 10,614 scored partners:

| edge | precision | rank | status |
|---|---|---|---|
| **MVP–PARP4** | **0.6757** | **1 of 10,614** | true subunit, cleanly recovered |
| **MVP–TEP1** | **0.0407** | noise floor | **true subunit, missed** |

**PARP4 is not merely first, it is first by a cliff:** score **0.2722** against rank 2 (ZNF598) at
**0.1378** — **1.98x** — and then a smooth plateau. *(The earlier version of this table said "99.99th
percentile" instead. That number is **1 − 1/10,614 = 0.99991**, i.e. it is **rank 1 restated**, and
would be true of whichever partner came first. The 2x gap to rank 2 is the content; the percentile was
not. Withdrawn.)*

MVP's partner count as a function of the precision cutoff, **computed at full precision**:

| cutoff | MVP partners retained | PARP4 in? | TEP1 in? |
|---|---|---|---|
| ≥ 0.70 | 0 | no | no |
| **≥ 0.5** | **1** | **yes** | no |
| ≥ 0.25 | 29 | yes | no |
| ≥ 0.1 | 357 | yes | no |
| **≥ 0.0407** | **1,733** | yes | **yes** |

> **A row has been removed from this table and the reason matters more than the row.** It read
> `≥ 0.676 → 0`, and was quoted as showing that *even at PARP4's own precision, nothing survives.*
> **It was a rounding artefact.** PARP4's precision is **0.675679**; I rounded it to 0.676 for display
> and then **used the rounded value as the cutoff**, which excludes the very edge it was rounding.
> TEP1's 0.0407108 was displayed as 0.041 but applied at full precision, so **the two calibrator edges
> in one table were rounded in opposite directions.** Both numbers were printed to full precision in my
> own log file.

**TEP1 is a genuine stoichiometric member of the vault particle** — recovered in an anti-MVP pulldown,
and TEP1-knockout mice contain vault particles with reduced cap density. It is not a borderline
assignment.

### The useful statement

> **This claim was wrong in its first published form and the correction narrows it.** It read: *"there
> is no threshold on this resource that both retains a known stoichiometric subunit and returns a
> followable list."* **That is false on the table above.** At ≥ 0.5 the list has **length 1 and that one
> entry is PARP4, a true subunit.** A list of one is followable. The row saying so was in my own
> results file, which prints `mvp_partners = ['PARP4']`.

**The statement that matches the data: no cutoff on this resource retains BOTH known subunits inside a
followable list.** The top subunit is recoverable cheaply and precisely — at ≥ 0.5 you get PARP4 and
nothing else. **What costs 1,733 names is completeness.** You can have the best-behaved member of a
complex, or you can have all of its known members, and the gap between those two is **four orders of
magnitude in list length** (1 to 1,733).

**So this is a sensitivity statement about complex COMPLETENESS, not about whether the resource works.**
For a method whose output is "the complex", that distinction is the whole thing: a pipeline tuned until
it looks precise will return the subunit you already knew about.

### Why it is diagnostic rather than a complaint

**MVP–PARP4 at 0.676 in the same database** proves CFdb *can* rank a true vault subunit far above
noise. So the failure is not "this seed has no signal" and not "vaults do not co-fractionate" — it is
**subunit-specific**. The confirming evidence comes from different physics (affinity pulldown), which
is what a calibration pair requires: you are not validating co-fractionation with co-fractionation.

### The mechanism sentence is withdrawn

The first version of this file read: *"TEP1 is substoichiometric and large. Low copy number gives fewer
peptides, a noisier elution profile, worse profile correlation. So the bias has a direction:
**co-fractionation recall falls with subunit abundance.**"* **Withdrawn, and it should not have been
written.**

- **The positive control in the same table contradicts it.** PARP4 is **1,724 residues** and also
  substoichiometric relative to MVP's 893-residue, high-copy shell — and PARP4 is the edge that was
  **recovered at rank 1.** Size and sub-stoichiometry cannot explain a split whose recovered side
  shares both properties.
- **n = 1 missed subunit cannot support a slope.** Two ordered points always define "a direction";
  that is arithmetic, not a measurement.
- **And there is a property specific to TEP1 that predicts this exact contrast without any abundance
  story: TEP1 is also a telomerase subunit.** Its elution profile is therefore a **mixture over two
  different particles**, at any copy number. PARP4 has no such second residence. A co-fractionation
  method models one profile per protein, so a genuinely bimodal protein is penalised by the method's
  own assumption.

**What a reuser should take is the measured split, not either explanation.** If you want the cause,
the test is a panel of complexes with shared-subunit and exclusive-subunit members matched for
abundance — which is exactly the regression suite recommended below, and which this project did not
run.

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

## 2. Three standard ways of calling a complex, measured against a complex whose composition was already known

**This is the finding this project did not realise it had**, and it took an external audit to point at
it. Each of the three numbers below was first written down as a **caveat on a biological negative**.
Read forward rather than apologetically, they are one measurement: **a sensitivity floor for
complex-detection methods, calibrated on a gold-standard particle.**

The vault is unusually good for this purpose. Its composition is **not in dispute** — MVP, PARP4 and
TEP1 — established by pulldown, by knockout mice and by structure, decades before any of these
resources existed. So when a method fails to recover it, that is **the method's floor**, not an open
biological question.

### The three results

| signature | method | result on a known-composition particle |
|---|---|---|
| **Co-elution** | CFdb co-fractionation, 411 datasets | **Precise but incomplete.** PARP4 recovered at list length **1**; retaining both known subunits costs **1,733** names (finding 1) |
| **Shared turnover** | half-life concordance against 10,000 abundance-matched random triplets | **Does not discriminate.** The true triplet sits at the **29.86th percentile** — it fails a 5th-percentile unity bar, and is less dispersed than only 70% of random triples |
| **Co-abundance** | co-expression after residualising the driving regulon | **Returns the tissue.** What remained after removing the interferon regulon was a single tissue class (CNS) — what tissue covariance looks like, not a complex |

### The useful statement

**On a particle whose membership is textbook, all three of the commonest complex signatures fail — and
they fail in three different ways.** Co-elution is precise but incomplete; turnover concordance does
not discriminate at all; co-abundance returns the tissue rather than the complex.

**Why this is worth a stranger's time.** These three are the standard evidence classes behind "this is
a complex" claims. A method that cannot recover the vault — not a borderline assembly, not a transient
interaction, but a particle present at ~100,000 copies per cell with three agreed members — is
reporting **its own floor** whenever it returns a negative on something harder.

### What to do with it

1. **Put a known-composition complex in your regression suite, and require the COMPLETE membership,
   not the top edge.** Recovering the best-behaved subunit is cheap and says nothing about
   completeness. The discordant edge is in `calibration_edges.tsv`.
2. **Do not treat turnover concordance as corroboration.** On a true triplet it returned the 29.86th
   percentile. A statistic that does not flag a known complex cannot support a proposed one.
3. **If a co-abundance module survives regulon removal, check that it is not a tissue** before
   designing anything on it.
4. **State which of the three your claim rests on.** They are not interchangeable instruments and they
   do not fail the same way.

### Honest limits

**Each of the three is n = 1 particle.** This is a floor demonstrated on one complex, not an estimated
error rate, and the vault may be unusual in ways that matter: unusually abundant, unusually rigid, and
with one member (TEP1) that is **also a telomerase subunit** and therefore genuinely bimodal in any
profile-based method.

**Two of the three rest on single resources** (CFdb; one half-life dataset). The co-abundance result is
**five slices of one resource, which is one production and not five replications.**

**And the three failures are not three independent votes.** Co-elution and co-abundance are both
profile-correlation methods, on different axes; a protein that is bimodal for one underlying reason can
fail both. Treat this as one floor with three faces, not as triangulation.

---

## What came out of this file, and what it would take to put it back

**A "stopping rule for separating co-regulation from co-complex" was the second finding here until an
external audit removed it.** It is kept on record because the reasoning is the transferable part.

The rule was: identify the regulon's drivers (STAT1, IRF9); pre-select a canonical target of that
regulon which is **not** a plausible physical partner of the seed (TAP1); **residualise the seed's
co-abundance profile on the drivers until the canonical target is displaced out of the seed's top N**
(N = 200); require it in every dataset; then read what remains.

**Why it is not a rule.** The word doing the work is *"until"* — **the depth of the regression is
fitted to the control.** So *"it held in 5 of 5 datasets"* reports that a target was met by a procedure
adjusted toward meeting it. Worse, **it states only a disappear condition**: nothing in the five steps
forbids the same regression from also ejecting PARP4 or TEP1, so **the procedure has no false-negative
bound** — the exact defect this project kept finding in other people's gates (house rule 7). And
TAP1's rank *before* residualisation was never recorded, so the distance the *"until"* had to travel is
invisible.

**What would make it a rule, written so someone else can do it properly:**

1. **Freeze the regression in advance** — name the covariates and the estimator, fix the depth, then
   **record** where the canonical target lands. A measured rank is a result; a target reached by
   adjustment is not.
2. **Add a retain condition.** Require a **known true partner** of the seed to **survive** the same
   residualisation. Without it the procedure is only tested in the direction it was built to succeed
   in.
3. **Report the pre-residualisation rank** of the canonical target, so the depth is auditable.

Until those three are in place it is a lab note, and it belongs in this section rather than above it.

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

---

## What this file deliberately does not contain

**This file holds two findings, and neither is about process.** That is a deliberate restriction, and it
has been tested twice against an external methods auditor.

Over this project's eleven audit rounds the most *transferable*-feeling output was procedural: a rule
about the order in which to write a comparison, a gate that greps your own tool output for the warnings
it already printed. Both came out of real errors, and the temptation to promote them into this file was
strong on exactly that basis. **Both were ruled out** (`RESULTS.md` §102d, and §72's earlier ruling on
an annotation finding), for two reasons worth stating because they apply to anyone writing something
like this:

1. **A stranger gains nothing from a slogan they would not have from ordinary practice.** A rule that
   encodes *our* sequence of mistakes reads, to someone who did not make them, as a platitude. It
   lowers the file it sits in.
2. **The cost of learning something is not evidence of its value.** Two days of expensive error makes a
   lesson feel like a finding. It is the single most reliable way to inflate a results file, and the
   auditor named it as a recurring failure of ours before we committed it again.

The working rules themselves live in `CONTRIBUTING.md`, where they belong, and the checks live in
`src/`. **If you are deciding what goes in a file like this, the test we settled on is: would this have
prevented a false result for someone who never met us?** Both findings above clear it. Neither rule did.
