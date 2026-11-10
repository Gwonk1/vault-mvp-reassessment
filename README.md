# A pre-registered reassessment of the vault particle (major vault protein)

Forty-odd pre-registered computational tests of standing hypotheses about the vault
ribonucleoprotein and major vault protein (MVP), run against public transcriptomic,
proteomic, genomic, structural and comparative data. Each test carried a positive-control
gate and an explicit kill condition written down and committed before the relevant data
were read.

**Most of the hypotheses failed, including ours. That is the result.** Of **493** ledger
rows, **69 carry a strikethrough** — claims withdrawn, usually by us, often by an
adversarial reviewer. **Twelve audit rounds** are recorded verbatim in `grok/`; the last one
rewrote the file this README points you at first.

## The most useful thing here is not about vaults

It is a worked record of **how pre-registered gates fail**. We built, and then had to
diagnose, four distinct failure modes in a single two-day run:

| failure | what happened |
|---|---|
| **a control that could only pass** | A specificity control required fewer than two of cohesin/condensin's subunits to be vault interactors. All four were absent from the instrument's detected proteome, so the rule could not have failed. |
| **a kill condition that could only kill** | A replication test dichotomised a continuous measurement at a significance threshold, had 19% power at the effect actually present, and returned "kill" at p = 0.195. The continuous statistic it discarded was a +0.544 log2 shift at p = 0.004. |
| **a refusal band wider than its estimator** | A gate registered "confirm above 75, clear below 60" on a statistic that landed at 70.0 with an SE near 8.5, making EQUIVOCAL close to pre-ordained. |
| **the wrong statistic entirely** | Three registered criteria were reachable and resolvable but did not discriminate what they were written to discriminate — one named charge when the axis was length; one reported a percentile that was 55% likely by construction; one used fold-decline to separate a complex from a co-migration window, when the quantity that separates them is whether hit counts saturate. |

The 20 house rules in [`CONTRIBUTING.md`](CONTRIBUTING.md) exist because we broke each
of them. Four were written on the second day, each after breaking the one before.

One sequence is worth reading end to end as a cautionary tale: **the same question, on
the same data, returned three different answers depending only on the statistical
treatment** — a dichotomised null (we recorded a kill), a continuous positive (we
upgraded it), and a physicochemically-matched null (we withdrew it) — before a donor-pool
check invalidated the third control as well. The biology never changed. RESULTS §41,
§49, §51, §55, §56.

## Start here

| File | What it is |
|---|---|
| [`papers/PAPER1_vault_reassessment.md`](papers/PAPER1_vault_reassessment.md) | The reassessment: what survived, what did not, and the gate scorecard |
| [`papers/PAPER2_bench_experiments.md`](papers/PAPER2_bench_experiments.md) | **Fifteen** wet-lab experiments plus **Tier 0** (two free computations to run first), ranked by what they decide, each with a positive control and a kill condition |
| [`LEDGER.md`](LEDGER.md) | Every idea raised, struck, or still standing — **493 rows** (490 numeric ids 1-496, with 89-90 and 391-394 unused, plus 3 letter-suffixed; house rule 3), with the reason and the file that settled it |
| [`RESULTS.md`](RESULTS.md) | Full per-test results and corrections — **107 numbered sections** |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | The **20 house rules**, and the fault that produced each. **Rule 19 is the one that matters most** — a repair is not real until the old sentence's job is withdrawn |
| `*_PREREGISTRATION.md` | **52 files**: the predictions, gates and kill conditions, as written before the data |
| `grok/`, `argon/`, `channel/` | Adversarial review correspondence, verbatim |

## The correction that reframes everything below

We set out to find MVP's physical interaction neighbourhood and did not find one, by any instrument,
across forty-odd gated tests. We then found a substantial published literature establishing MVP as a **signalling modulator**:
IKK-NF-kB, calcineurin-NFATc1, STAT3, Parkin-mediated mitophagy, and adaptive immunity on influenza
rechallenge. **But that convergence is mostly one group's:** Jingjing Ben appears on five of the six
papers and only the influenza study shares no author with any other, so it is one programme plus one
independent replication rather than six independent results (§76b). **And those interactions are
transient and low-stoichiometry — exactly what our instruments recover worst.** The absence we document is therefore not evidence against function; it shows MVP has
**no stoichiometric partner complex beyond PARP4 and TEP1**, which is narrower and still useful.

**And every published vault phenotype is conditional** — knockout mice healthy, triple-knockout mice
normal, knockout zebrafish regenerating — with defects only under challenge. **Our "no fitness
coupling" came from CRISPR screens in rich medium, the one condition where every published model is
also normal.** See RESULTS §70.

## If you only read one file

**[`CALIBRATION.md`](CALIBRATION.md)** — the two findings here that are useful to someone who does not
work on vaults. Both are instrument calibration rather than biology.

**1. A sensitivity floor.** Three standard complex-detection signatures, measured against a particle
whose membership has not been in dispute for decades — ~100,000 copies per cell, three agreed members,
established by pulldown, knockout mice and structure. **All three fail, in three different ways:**
co-elution is **precise but incomplete** (the top subunit comes back in a list of one; both known
subunits cost 1,733 names), shared-turnover concordance **does not discriminate** (the *true* triplet
sits at the 29.86th percentile of abundance-matched random triplets), and regulon-residualised
co-abundance **returns the tissue** rather than the complex.

**2. The completeness split in detail** — the MVP–TEP1 discordant edge, one of that floor's three
faces. **[`calibration_edges.tsv`](calibration_edges.tsv)** holds the test case in machine-readable
form.

> **Both of these were corrected late and hard** (§103). Finding 1's original headline — *"no cutoff
> both retains a true subunit and returns a followable list"* — was **false on our own results file**,
> which prints a length-1 list containing PARP4. And the floor itself had been written down in three
> separate places **as caveats on a biological negative** before an external audit pointed out that
> read forward they are one measurement. A **pre-registerable stopping rule** was the second finding
> until the same audit removed it: *"residualise **until** a canonical target leaves the top-N"* fits
> the regression depth to its own control. It is now a demoted lab note at the foot of that file, with
> the three conditions that would make it a rule.

## Provenance, and what five literature checks found

**Every interactor claim below comes from one public dataset, not from us.** The anti-MVP pulldown is
**PRIDE PXD052802** — co-IP with the synthetic antigen binding reagent VM1 against control H6, in
**wild-type versus PARP4-knockout A549 cells**, a lung adenocarcinoma line — and the deposit's own
description analyses the same contrast we used. So these are readings of public data, possibly
line-specific. **"Independent of PARP4" means "still present when PARP4 is removed in A549."** We did
not establish the cell line until late in the work.

**Five literature checks were run on our ten candidate novel findings. All five found prior art:**

| checked claim | outcome |
|---|---|
| TEP1 associates independently of PARP4 | **~25 years old** — MVP alone forms vaults in Sf9 cells, TEP1-knockout vaults stay intact, and caps incorporate into preformed shells |
| MVP ancestral in eukaryotes, lost in fungi/plants/Ecdysozoa | **Daly et al. 2013 reached it verbatim**; we had also censused the wrong orthogroups (VIT-domain, not MVP's) |
| the interactor readings generally | the pulldown is a **public deposit with its own analysis** of our comparison |
| stool proteomics cannot recover a vault | **the methods principle is published** — prep bias by cellular compartment, and Tanca 2015 on differential centrifugation; only the vault application is ours |
| ~~**a sealed nucleotide pocket in MVP's SPFH shoulder**~~ **WITHDRAWN §73** — the foundation of our top-ranked hypothesis | **the SPFH assignment is Tanaka et al., *Science* 2009 (PDB 4V60); the pocket is Lodwick et al., *Nat Commun* 2025 with NAD+ and ADP in deposited coordinates — and "sealed" is contradicted, since the site is lumen-facing and formed *between* two monomers, so assembly creates it rather than closing it.** The answer sat in our own `data/raw/struct/`, including a file titled *"RNA Vault with ADPR bound"* |

**One misjudgement produced all five hits.** This work assumed the vault literature was thin because
consensus on function is absent. **It is not thin:** four structure papers appeared in 2025-2026
alone, an active structural group is publishing on the same questions asked here, and a functional
knockout literature runs from 2019 to 2025. We treated the absence of consensus as licence to stop
looking.

**So the honest description of the contribution is narrow.** In every check, the general version of
the observation was already known and only the **vault-specific application** was new. **The six
unchecked candidates in [`HYPOTHESES_AND_NOVELTY.md`](HYPOTHESES_AND_NOVELTY.md) should be read as
probably-known rather than provisional** — on a five-for-five base rate, that is the correct prior.

> **Two counts appear in this repository and they count different things.** **Five** is the number of
> *formal literature checks* run on candidate novel findings; all five found prior art. **Six** is the
> number of times we *presented something as new without checking at all* (§85, §5435) - the sixth was
> caught not by a literature check but by the user, in one sentence, about a result we had already
> known was known. **Neither number is a typo for the other**, and the second is the worse one.

~~**What was produced rather than rediscovered is one well-controlled negative:** MVP has no
stoichiometric partner complex beyond PARP4 and TEP1, across every instrument available, with
calibration gates passing. No literature check has touched it.~~

**WITHDRAWN, §103e.** That sentence reduces to: **one PRIDE deposit (PXD052802), on a contrast the
depositors themselves analysed, recovers the known particle and does not produce a second one.**
"Every instrument" was **labels on one production** - all 75 interactor terms across eight sections
come from that deposit. Co-fractionation **failed its own positive control** on TEP1, so it cannot
contribute to a negative; the half-life statistic **does not recognise the true triplet** (29.86th
percentile), so it cannot corroborate the absence of others. And "no literature check has touched it"
sat next to "the depositors analysed the same contrast."

**What was actually produced is a sensitivity floor**, and it is in
[`CALIBRATION.md`](CALIBRATION.md) finding 2: **three standard complex-detection signatures, measured
against a particle whose membership has not been in dispute for decades, all three failing in
different ways.** That measurement was in hand the whole time, written down in three places as excuses
for a negative result (§103g).

## What survives

A short list, deliberately — and **shorter after §103**, which reinterpreted three of its items:

- the **MVP-PARP4-TEP1 trimer**, with TEP1 present in a PARP4-knockout line. **This is the textbook
  composition of the particle**, re-read in one deposit; it is not a contribution of this work.
- **ANXA2 and S100A10** as the only non-subunit interactors of the old membrane list to survive. Note
  they are an **abundant heterotetramer**, the prey class pulldowns retain by mass.
- **COP1 at 27-fold in one instrument class.** Flagged in §103e as **the strongest unreconciled
  positive number in the project** — an enrichment parked in the support list of a no-further-partner
  claim, with no exclusion rule ever applied to it. **Not resolved, and not promoted.**
- ~~**myoferlin actively excluded**, in a wash-based pulldown and in pre-lysis covalent proximity
  labelling~~ — **WITHDRAWN, §103e.** *"Actively excluded"* describes a **depletion** as an action,
  and the two arms are **two assays inside one production**, not two instruments. Surviving statement:
  **myoferlin is depleted, not enriched, in these data.**
- **degradation machinery the most depleted annotation of 1,276** in an anti-MVP pulldown —
  **flagged, §103e.** That is **the minimum of 1,276 categories**; every ranked list has one, and no
  effect size or null was attached. The direction is measured; its distinction from the extreme of
  1,276 draws is not.
- subunit half-lives whose spread sits at the **29.86th percentile** of random triplets. **This one
  has changed sides.** It was listed here as support for a negative; §103g reads it forward as part of
  the sensitivity floor — **a concordance statistic that does not recognise the true particle cannot
  corroborate the absence of further ones.**

**One positive measurement survived everything, and got sharper by being cut down.** Among extant
orthologues that remain alignable, MVP is under **strong purifying selection** - a codon-model
(`codeml` M0) **omega of 0.06 across 11 vertebrates** - **1.2x the essential-gene control and about
one-seventh of the relaxed control** (GAPDH 0.05, CD4 0.4 at the same one significant figure, §90).
**The ratios are given rather than the three numbers side by side, because printing "0.06, 0.05, 0.42"
performs the retracted equality by typography** (§103, house rule 19) - and 0.4304 to one significant
figure is 0.4, so the old "0.42" was not even consistent with its own rounding. **We refused this number on a gate technicality and an external
methods audit reversed us** (§84, house rule 15); a second audit then cut it down to **one significant
figure**, because our own reruns disagree about the third digit (§102b).

**What it is not:** it is **not** an equality with a housekeeping gene (no standard error, no test of
equality, an 18% gap - withdrawn, §102b); the panel is **vertebrate, not chordate**, and it is
**keeper-only by construction**, since every sequence in it comes from a lineage that retained the gene
(§102e). A pairwise NG86 estimate of 0.1118 (§84b) **understated** the constraint and is superseded by
the codon model. It **sharpens** the paradox: deletable from a mouse, discarded by two major clades,
and actively conserved wherever it survives.

One observation has survived six registered attacks and is **still not promoted**: MVP's
sub-threshold co-elution tail is translation-enriched at the 98th percentile of 150
comparable seeds, and not explained by degree, abundance, family membership, apparent mass,
or seed length and charge. It stays unpromoted because one instrument cannot separate a
specific association from the co-migration envelope it sits inside. That is what Paper 2's
Experiment 14 is for.

## What this repository is honest about

Roughly a quarter of the ledger is the authors catching themselves — a mediation analysis
that divided coefficients fitted on different subcohorts, a cross-species comparison that
matched human gene symbols to amoeba gene names, a result described from the bottom slice
of a sorted table, a claim the project's own committed JSON contradicted on the facing
page, a frame indexed in the wrong order so that one matching axis was silently scrambled.
Each correction sits next to the original claim rather than replacing it, and superseded
entries are struck with a pointer to what overturned them.

Three language-model agents reviewed the manuscripts adversarially against the committed
data, over six rounds. Between them they struck or qualified more than twenty claims. The
sharpest single intervention asked for one number the authors' own threshold had discarded,
and overturned the largest claim of that day.

**On pre-registration.** The full development history is published, 130 commits with their
original timestamps, so the ordering is checkable rather than merely asserted.
`git log --reverse` shows each prediction committed before the data it tested were read.

Redactions were made to that history, deliberately, and are recorded: references sourcing a
hypothesis and an NLRP3 immunogenicity report to private correspondence are replaced with
neutral phrasing and marked as claims we could not independently source; the filenames of
gitignored source transcripts are generalised; and local filesystem paths are made
relative. Published citations are untouched. Nothing else has been altered, including the
parts where we were wrong.

**Formally uninformative results are marked, not promoted.** Several tests failed their own
gates, including two we had designed badly enough that the gate could only return one
answer. They are reported as uninformative with the control that failed named.

## Reproducing it

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt   # if present
cd argon/raw && ./fetch.sh && sha256sum -c SHA256SUMS.txt            # third-party sources
```

`results/` is committed in full, so every number in the papers can be checked without
refetching anything. `argon/raw/` is only needed to recompute from scratch; it is excluded
because several files are publisher-hosted with licences we did not verify. See
[`argon/raw/README.md`](argon/raw/README.md).

Analysis scripts are in `src/` — 73 of them — and `argon/src/` for the second agent's tests.

## Licence

Dual-licensed: prose, papers and results under **CC BY 4.0**, code under **MIT**. See
[`LICENSE`](LICENSE) for which applies to what, and for the citation. Third-party material
read by this project is not relicensed — see [`argon/raw/README.md`](argon/raw/README.md).

## Status

Not peer reviewed. Not submitted. No wet-lab work has been done; Paper 2 is a proposal, and
the two experiments added last exist specifically because reanalysis provably cannot answer
them. Corrections are welcome and will be recorded in the ledger like every other
correction.
