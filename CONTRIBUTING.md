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
   (**#90 is a dangling citation — the ledger has no entry 90, and none has 89 either; the rule stands on the other four, and
   we leave the number visible rather than tidy away the provenance. The ledger has two id gaps in all:
   89-90 and 391-394. Verified #464: nothing in the repository cites 391-394, so unlike #90 these are
   unused numbers rather than dangling citations. The gaps stay; renumbering 450+ rows to close them
   would invalidate every citation in the file**):
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

### 13. Recover the literature before believing the finding is yours

Learned by not doing it forty times (#306, #316). Every test in this project was gated on recovering a
known positive control before the result was believed. **No test was ever gated on recovering the
existing literature before the result was called new.**

Three checks were eventually run and **all three found prior art**: a top-ranked novelty claim turned
out to be twenty-five years old; an entire phylogenetic argument reproduced a 2013 paper's conclusion;
and the pulldown we had analysed all day turned out to be a public deposit whose own description
analyses the same comparison we used. We also discovered, only at that point, a substantial published
functional literature on the protein — knockout work in five systems — that none of our forty tests had
touched, and which reframed our central negative result.

**A novelty claim needs a literature check registered as its own gate, with the same standing as a
positive control.** Before ranking anything as unremarked:

1. **Search for the claim itself**, not just the topic.
2. **Establish the provenance of every dataset you used** — who deposited it, under what accession,
   with what analysis already described, in what cell line. We analysed a lung-cancer line for a day
   without knowing it was one.
3. **Ask what the field's established view is**, so a hypothesis list is not written in ignorance of
   the tested hypotheses.
4. **Record the check status beside the claim**, so an unchecked claim cannot be read as a ranked one.

The cheapest version of this rule is one search per claim. We ran forty tests and avoided that search,
and it cost four withdrawn claims and one reframed paper.

## 14. A gate's instrument class must match the file class it is pointed at

The retraction gate is a **prose** instrument: its patterns are bare decimals and short phrases, which
discriminate in documents because documents contain few numbers. Pointed at `results/*.log`, the same
patterns scored **three genuine void values and three coincidences** out of six hits - a `null_sd` that
happened to equal `0.174`, a model CI bound of `0.0526`, and the prefix of a Spearman rho.

**And tightening it inverts the outcome.** Adding `(?!\d)` to stop a pattern matching the prefix of a
longer float suppresses the two genuine hits (`p=0.18352908…`, `p=0.05261473…`) while keeping both
coincidental short floats.

So: **do not extend a gate to a new file class by widening its patterns.** Gate the new class on a
property that is actually decidable there. For logs that is a banner - `SUPERSEDED_LOGS` in
`src/check_retractions.py` lists each superseded log and the check asserts the file says so at the top.

**Enumerate the cases before shipping the tightening.** We would have shipped `(?!\d)` as an
improvement otherwise. See §77.

## 15. A gate binds inference only when the failed clause is about that estimator

The dN/dS gate had four clauses. Clauses 1 and 2 tested whether the instrument could separate an
essential gene from a drifting one - **validity conditions**. Clause 3 was a different gene's pair
count and clause 4 was a tally of HTTP timeouts. **Neither enters the sampling distribution of the
subject's estimate.**

We treated all four as equally binding and refused a result that two passing validity clauses had
earned (§81d, reversed in §84b). **That was not rigour. It was a category error that happened to point
the same way rigour usually points**, which is exactly why it felt virtuous.

**The rule has a sharp edge and it cuts both ways.** Overriding a *met* threshold because the threshold
sits inside the null is correct (§84g: a 20%-identity floor over 200 residues is noise for an 893-aa
query against 20,211 proteins). Overriding a *failed* clause because you dislike the answer is the §41
fault. **The test is not "did a clause fail" but "does the failed clause describe the estimator I am
about to quote."** Write gates so that question has an obvious answer: separate the clauses that
establish validity from the clauses that establish coverage, and say which is which **in the
registration**.

## 16. Rule 15 applies to a decision NOT to run a test

Rule 15 says a gate binds inference only when the failed clause is about that estimator. **The mirror
case is refusing to measure something.** In §87d we declined a waist-residue conservation test by
arguing that a perfectly symmetric ring has no designated start, so no statistic could name which
subunit fires first. True - and it answers a **different question** from the one the test would have
asked.

> *"Stochastic nucleation removes a start-site conservation test and leaves the contact test
> untouched… 'uninformative by construction' conflates 'which copy fires first' with 'are the contact
> residues constrained.'"*

**A refusal to test is an inference and needs the same paperwork as a result.** Before declining, write
down **the statistic you are not computing** and **the outcome that would have been informative**. If
you cannot state both, you are not refusing a test - you are substituting a narrative for one. It is
the cheaper failure mode, because nothing goes in the ledger to contradict later.

## 17. Intersection first, forks second, the adjective only if both survive

**The error this exists for** (Grok audit 010): *"You counted containers, then described the count as
agreement."* It has two subtypes. **Type I** - the containers are copies of one production, so the
sample size is the number of **production events**, not of files. **Type II** - the containers hold the
same **label**, not the same measurement, and you counted labels.

The class: **a count of bearers of a label, written down as if it were the number of independent
productions of a measurement.** It has now happened twice in unrelated domains (six papers that were
one lab, §76; seven structures whose forks are unverified, §99d) and **a third time inside the
correction written to fix the second** (§99c).

> **You may not write "independent", and you may not use a count of objects as evidence, until two
> lines are already on the page:**
> 1. **Intersection** - the values common to **every** member. Residues, authors, starting-model PDB
>    ids. **Not "members that returned something."**
> 2. **Forks** - for each element of that intersection, the most recent cause shared with another
>    member. **Collapse those; what remains is the sample size.**
>
> **If the intersection is empty, or a singleton you would not have bet on, there is no replicated
> result. Order is the rule.**

**"Independent" is a property of the errors, not of the nouns.** Two observations are independent
evidence only when **the ways they could be wrong do not move together.** Species and method are nouns.
Shared software, shared starting coordinates, a shared threshold, and the same person choosing it are
forks.

**And a fork you cannot find is a fork.** §99d: the depositions' `_refine.pdbx_starting_model` fields
are unpopulated, so the sample size is **1** until the primary methods are read - not 7.

## 18. Read what your own tools printed. There is now a check for it.

**Every other gate here compares a claim to data. None asked whether the tool had already told us we
were wrong.** §101a: codeml printed `This is a rooted tree.  Please check!` and `lnL(ntime: 24 ...)` -
where an unrooted 13-taxon tree has 23 branches - **in a file we never opened**, and an external auditor
found the fault from **arithmetic alone**, with no access to it.

`src/check_tool_warnings.py` scans every `.log`, `.txt` and `.out` under `results/` and the working
scratch for the strings a tool uses when it is telling you something: *please check*, WARNING, ERROR,
FAIL, `rooted tree`, convergence failures, singular/unidentifiable, Traceback, NaN, deprecated,
truncated, skipped.

**It is deliberately noisy.** First run: **47 lines across 21 files.** Most are registered gate failures
we recorded on purpose. **One mattered** - the rooted tree, present in *every* codeml run including the
§90 controls. **It was fatal to the branch test (§98c) and did not reach the M0 bracket:** rooting moved
a likelihood ratio by 12 points while the M0 estimates moved under 3%, because M0 is a tree-wide average
and is insensitive to branch assignment. **That asymmetry runs both ways - the M0 check does not vouch
for any likelihood-ratio statistic either** (§102b). **One needed three minutes to clear** - a real
`ValueError` traceback in `results/phospho_part2.log`, which turned out to be a **later aborted re-run**:
the complete JSON is timestamped 08:37 and the crash log 09:04, so §24 rests on the successful run.

> **What this check is worth, assessed by grok audit 011 (§102d) rather than by us.** The **scientific**
> yield of clearing all 47 was **one sentence**: §10's scope limit. One hit was the rooted-tree line
> **already found by arithmetic** without reading the file; one was the aborted re-run; the rest were
> gates we had recorded deliberately. **And the clearance path is itself unreliable** - an ERE `\|`
> once searched for a literal backslash, and our own `READ (2):` annotation missed the marker
> vocabulary. **A 45-of-47 annotation load with a false-negative path like that will decay into
> stamps.** Keep the check; **it is a tool, not a finding**, and it was ruled out of `CALIBRATION.md`
> for that reason.

**Two scope faults in this check, both found by what it failed to catch (#468).** It originally scanned
`results/` and the working scratch, **not the repository root** - and its filter required a `.log`,
`.txt` or `.out` extension, while **PAML writes its default outputs with no extension at all** (`mlc`,
`rst`, `rst1`, `rub`, `lnf`). Six codeml output files therefore sat in the repository root for a day
without this check ever reading one of them, for two independent reasons. Both are fixed, and the
general lesson is in the code comment: **a tool-output filter that assumes an extension is a filter
that misses every tool whose convention is a bare name.**

**To clear a file**, add a line containing `READ:` (or EXPECTED / benign / VOID / `see RESULTS`) saying
what the warning means and why it is acceptable. **A judged warning is annotated. An unjudged warning is
a pending fault.** Do not widen the exclusion list to make the check quiet.

## 19. A repair is not real until the old sentence's JOB is withdrawn

**Grok audit 012. This is the class under all the others, and it took twelve audits to see.**

Every rule above was written after an error, and every one of those errors got a local fix: the word
was replaced, a caveat was added, a strikethrough went in, a scope note was appended. **And in almost
every case the sentence kept its post.** The claim that was criticised went on doing the same
inferential work in the document, wearing the repair.

The auditor's own list, which is checkable against this repository's history:

| what was criticised | what came back |
|---|---|
| "indistinguishable from a housekeeping gene" | the same comparison as a **one-significant-figure juxtaposition**: "0.06, with controls at 0.05 and 0.42" |
| the dismissal of co-fractionation | "**cannot retain a real subunit**" — while the table showed a length-1 list containing the true top subunit |
| the need for a transferable method | a "**stopping rule**" whose own text calls it a heuristic and whose depth is fitted to its control |
| the need for a biological contribution | the no-further-partner headline, **with a qualification beside it that removes the content** |
| the structural result | p = 0.008, **relabelled "underpowered"** and left on the live list |
| the need for a leading idea | a weight of **0.25 called "the top hypothesis"** |

**The shape: the caveat is stored in a scope that does not edit the sentence that gets exported.**
Disclosure *beside* a claim leaves the claim at its old strength. A reader meets the headline; the
qualification is in a banner, a footnote, a limits subsection, or two hundred sections later.

### The test, which takes one minute

**Write the inferential job of the old sentence in one line. Write the job of the repaired sentence in
one line. If they match, nothing was repaired** — the criticised token was swapped and the claim kept
its post.

### What this rule forbids

- **Adding a caveat instead of weakening the claim.** If the caveat is true, the claim is smaller: say
  the smaller thing in the sentence a reader meets first.
- **Relabelling a statistic instead of retiring it.** Calling p = 0.008 "underpowered" and leaving it
  in the results is not a correction; "underpowered" describes a test that returns a *large* p when an
  effect is real, and so was also the wrong word (§103e).
- **Rounding two numbers to one significant figure so that they read as equal.** That is the retracted
  equality, re-executed by typography.
- **Standing banners doing the work of a rewrite.** This repository has four places where a correction
  was appended at the end while the claims it qualifies stayed live where a reader meets them (#262,
  #283, #319, and the RESULTS.md head banner). **The banner was the fourth instance of the fault, not
  the fix for it.**

## 20. A number written in prose must be computed, not maintained

**Ledger #358 corrected a count that had been "incremented instead of counted." #482 found the same
fault again, in five places at once** - the README claiming **264** ledger entries and **63** RESULTS
sections against an actual **482** and **104**, "the ten house rules" when there were nineteen, and
Paper 1's front matter still citing **452 entries, ids 1-454** and **"RESULTS.md (24 sections)"**.

**Care does not fix this.** A number typed beside a file that grows will drift, and it drifts silently,
because nothing in a document disagrees with it. Within ten minutes of *writing #482 down*, the row
describing the fault had itself made §104c's count wrong.

**So counts are computed. `src/check_counts.py` (check 5, in the pre-commit hook) recomputes every
count in the repository and fails on any prose figure that no longer matches.** It is wired to 17
claim sites across four files.

**Two things it taught immediately:**

- **"Number of rows" and "number of ids" were being conflated.** The ledger has **482 rows**, of which
  **479 carry numeric ids** (1-485, with 89-90 and 391-394 unused) and **3 are letter-suffixed**
  (13a, 26b, 34b). Both of the figures previously quoted were wrong, in opposite directions.
- **When the check fails, do not just edit the number.** If the count is stated somewhere new, add the
  site to `CLAIMS` so it is checked from now on. Editing the figure and moving on is how it drifted
  the previous two times.
