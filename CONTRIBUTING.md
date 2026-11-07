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
   breaking that rule in its own title and abstract.
3. **Read the table, do not describe it.** Faults #59, #60, #64, #70, #90 are all the same mistake:
   summarising a sorted file from memory instead of opening it. Check the top *and* the bottom.
4. **Verify a collaborator's number against their data file, not their prose.** Fault #64.
5. **Do not iterate a method until it passes.** Fault #113 is the decision to stop re-opening a finding
   after two gate failures, because adjusting until it passes destroys the value of having registered
   anything.
6. **Corrections go next to the original claim**, struck through, with the reason. Nothing is silently
   amended; `LEDGER.md` is the record of being wrong as much as of being right.

## 7. Verify a control protein is present in the instrument's universe before registering it

Learned by breaking it (#188). We registered a specificity control requiring that fewer than two of
cohesin and condensin's subunits be vault interactors. All four turned out to be absent from the IP-MS
table entirely, so the control returned PASS and the PASS meant nothing: a protein outside the universe
cannot be an interactor, so the rule had no power to fail.

The controls were well chosen in principle — abundant, nuclear, chromosomal, the right contrast for the
artefact we feared. The error was registering them without checking the instrument had detected them.

**Before a pre-registration is committed, confirm every named control protein appears in the data the
test will read.** A control that cannot fail is not a control, and it is worse than no control, because
it launders an untested claim as a checked one.

## 8. Before committing a registration, check that every registered outcome is reachable

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
