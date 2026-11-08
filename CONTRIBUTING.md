# Working on this repository

This repository is the **single source of truth**. Analysis is run here and committed here.

## Local setup

Large inputs are not committed. Three paths are symlinks into a local data store and are gitignored:

```
data/raw        ->  <local store>/data/raw          public datasets (HPA, CCLE, MSigDB, GEO, PDB)
data/processed  ->  <local store>/data/processed    derived matrices (parquet)
.venv           ->  <local store>/.venv             python environment
argon/raw/*     ->  <local store>/argon/raw/*       third-party papers, see argon/raw/README.md
```

To recreate them, fetch the sources (`cd argon/raw && ./fetch.sh && sha256sum -c SHA256SUMS.txt`) and
point the symlinks at wherever you put them. `results/` is committed in full, so **every number in the
papers can be checked without any of this**; the data is only needed to recompute from scratch.

## House rules that exist because they were learned the hard way

1. **Pre-register before you look.** Write the prediction, the positive-control gate and the kill
   condition into a `*_PREREGISTRATION.md`, commit it, *then* run the test. The git timestamp is the
   evidence.
2. **A failed gate means UNINFORMATIVE.** It does not mean reinterpret. Ledger #80 records this paper
   breaking that rule in its own title and abstract — and **§62a records the same fault regressing into
   the title a day after #80 fixed it**, because every audit compared prose to data and nothing ever
   re-checked the title. **Audit the title.**
3. **Read the table, do not describe it.** Faults #59, #60, #64, #70 and #90 are all the same mistake
   (**#90 is a dangling citation — the ledger has no entry 90; the rule stands on the other four, and
   we leave the number visible rather than tidy away the provenance**):
   summarising a sorted file from memory instead of opening it. Check the top *and* the bottom.
4. **Verify a collaborator's number against their data file, not their prose.** Fault #64.
5. **Do not iterate a method until it passes.** Fault #113 is the decision to stop re-opening a finding
   after two gate failures, because adjusting until it passes destroys the value of having registered
   anything.
6. **Corrections go next to the original claim**, struck through, with the reason. Nothing is silently
   amended; `LEDGER.md` is the record of being wrong as much as of being right.

### 7. Verify a control protein is present in the instrument's universe before registering it

Learned by breaking it (#188). We registered a specificity control requiring that fewer than two of
cohesin and condensin's subunits be vault interactors. All four turned out to be absent from the IP-MS
table entirely, so the control returned PASS and the PASS meant nothing: a protein outside the universe
cannot be an interactor, so the rule had no power to fail.

The controls were well chosen in principle — abundant, nuclear, chromosomal, the right contrast for the
artefact we feared. The error was registering them without checking the instrument had detected them.

**Before a pre-registration is committed, confirm every named control protein appears in the data the
test will read.** A control that cannot fail is not a control, and it is worse than no control, because
it launders an untested claim as a checked one.

### 8. Before committing a registration, check that every registered outcome is reachable

Learned by breaking it twice in one day, in opposite directions (#188, #204).

A gate exists to make a result independent of what we hoped for. A gate with only one reachable answer
does the opposite: it launders a foregone conclusion as a checked one. We built both kinds:

- **A control that could only PASS.** The SMC5/6 specificity control required that fewer than two of
  cohesin and condensin's subunits be vault interactors. All four were absent from that instrument's
  detected proteome, so the rule could not have failed. Rule 7 came from this.
- **A kill condition that could only KILL.** The translation replication test dichotomised a continuous
  measurement at `LWTP > 1.3`. Its critical value was 12 observed against 6.94 expected, it had **19%
  power at the effect actually present**, and we recorded a kill at p = 0.195. The continuous statistic
  the cut discarded was a **+0.544 log2 shift at p = 0.004**. The signal was there the whole time.

**Three pre-flight checks, all cheap, all done before the registration is committed:**

1. **Minimum detectable effect.** Compute the effect size the test has 80% power for, and write it into
   the registration. If that number is larger than the effect you are adjudicating, you are registering
   a foregone "kill".
2. **Ceiling.** Compute the largest effect the instrument can express. Our pulldown's maximum
   fold-enrichment is 88/6.94 = **12.7x**, so the 18x co-elution figure it was supposed to adjudicate
   was never a quantity it could have returned. A test that cannot express the estimand is not a test of
   it.
3. **Don't dichotomise a continuous measurement.** If the data are continuous, the registered primary
   statistic should be continuous. Where a threshold is genuinely required, register the continuous
   statistic alongside it and report both — a disagreement between them is the finding.

And when a correction arrives in the direction you wanted, **apply it to every claim it touches,
including the ones you would rather keep.** Applying a rule in one direction only is the same error as
having no rule, and it is harder to see because each individual step looks principled.

### 9. If you change the statistic, re-run the reachability check

Learned by breaking it within hours of writing rule 8 (#218).

Rule 8 says check that every registered outcome is attainable before committing. We did that — on the
normal approximation, where the positive control's z of 6.75 gave q = 1.4e-08 and a pass looked
trivially reachable. An addendum then replaced that statistic with an empirical null, correctly, and
**nobody re-ran the check.** On the new statistic the same gate sat a factor of two above the test's
resolution floor: a 3-protein set's empirical p is bounded below by the draw count, so q < 0.01 demanded
one or fewer exceedances in 400,000 draws. We got two, the control failed, and a test we had every
reason to believe in returned no verdict at all.

**A reachability check is a property of the statistic, not of the registration.** Change the statistic —
parametric to empirical, count to mean, one threshold to another — and the check is void until repeated.

**And when a gate fails narrowly, do not buy a pass with compute.** Our control's p rested on two
events, so more draws would have tightened a Poisson-limited estimate and probably landed just inside
the gate. That is still fault #113: iterating a method until it passes. Monte Carlo precision is a fine
thing to increase, but never in response to the answer. Fix the draw count in a new registration, or
record the uninformative verdict and move on.

### 10. A refusal band can be wider than your estimator

Learned three times in one day (#188, #204, #240). Rules 8 and 9 cover whether each outcome is
*attainable*; this one covers whether your bars are *resolvable*.

Our mass test registered "confirm above 75, clear below 60" on a statistic whose estimate came in at
70.0 with a standard error near 8.5 percentile points. The confirm bar was 0.6 SE above the estimate
and the clear bar 1.2 SE below it: **the dead zone was wider than the estimator could resolve, so an
EQUIVOCAL verdict was close to pre-ordained.** A gate that mostly returns "we cannot say" manufactures
indecision exactly as a one-way gate manufactures a conclusion.

Related, from the same audit: **register the summary statistic and its weighting, not just the
threshold.** Our seven assemblies gave a seed-weighted median of 70.0 and an assembly-weighted median of
75.3 — the second clears the confirm bar the first missed. We had not said which we would use, so the
verdict was decided after the fact by an unregistered choice.

**Before committing: compute the standard error of the statistic you are about to gate on, and check
that your bars are at least ~2 SE apart from each other and not inside 1 SE of the value you expect.**
If they are not, widen the data or narrow the claim — do not register a band you cannot land in.

### 11. Mark a remediated entry `[FIXED]`, not struck

`~~strikethrough~~` was used for two different things: a claim that was **refuted**, and a claim that
was **true and acted on**. Entry #80 is the second kind — its body says "Title changed, abstract
rewritten" — but the strike made it read as disproved, so a standing warning looked like a closed error
and the fault it warned about regressed unnoticed (§62b).

**A notation that marks "this was wrong" and "this was right and we dealt with it" identically will
eventually hide a live problem.** From here, a remediated-but-true entry is marked `[FIXED]` with a
pointer to the fix. We are not retro-editing the 64 existing struck entries, because corrections in this
repository sit next to claims rather than replacing them — the convention change applies going forward
and #80 carries the annotation in place.

### 12. When you find a bug in one script, grep the idiom across all of them

Learned by missing it twice (#280). We found a frame built in GENCODE FASTA order rather than table
order in `export_test.py`, where it silently scrambled one of three matching axes. A registered gate
caught it before publication, we wrote that up approvingly, and we did not look at the other scripts
using the same idiom. One of them, `donor_and_k.py`, had already been run, so its figures went into the
ledger and stayed there — 65 cells, 189 donors, a 2.48x ratio, where the correct frame gives 35, 129
and 2.86x.

**A bug found in one file is a hypothesis about every file.** Before moving on: grep the exact
construction across `src/`, and re-run anything that shares it. The cost is one command; the cost of not
doing it was a published number and a diagnosis that pointed at the wrong cause for two sections.
