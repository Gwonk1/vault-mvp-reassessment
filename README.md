# A pre-registered reassessment of the vault particle (major vault protein)

Forty-odd pre-registered computational tests of standing hypotheses about the vault
ribonucleoprotein and major vault protein (MVP), run against public transcriptomic,
proteomic, genomic, structural and comparative data. Each test carried a positive-control
gate and an explicit kill condition written down and committed before the relevant data
were read.

**Most of the hypotheses failed, including ours. That is the result.** Of 264 ledger
entries, **64 are struck through** — claims withdrawn, usually by us, sometimes by an
adversarial reviewer.

## The most useful thing here is not about vaults

It is a worked record of **how pre-registered gates fail**. We built, and then had to
diagnose, four distinct failure modes in a single two-day run:

| failure | what happened |
|---|---|
| **a control that could only pass** | A specificity control required fewer than two of cohesin/condensin's subunits to be vault interactors. All four were absent from the instrument's detected proteome, so the rule could not have failed. |
| **a kill condition that could only kill** | A replication test dichotomised a continuous measurement at a significance threshold, had 19% power at the effect actually present, and returned "kill" at p = 0.195. The continuous statistic it discarded was a +0.544 log2 shift at p = 0.004. |
| **a refusal band wider than its estimator** | A gate registered "confirm above 75, clear below 60" on a statistic that landed at 70.0 with an SE near 8.5, making EQUIVOCAL close to pre-ordained. |
| **the wrong statistic entirely** | Three registered criteria were reachable and resolvable but did not discriminate what they were written to discriminate — one named charge when the axis was length; one reported a percentile that was 55% likely by construction; one used fold-decline to separate a complex from a co-migration window, when the quantity that separates them is whether hit counts saturate. |

The ten house rules in [`CONTRIBUTING.md`](CONTRIBUTING.md) exist because we broke each
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
| [`papers/PAPER2_bench_experiments.md`](papers/PAPER2_bench_experiments.md) | **Fourteen** wet-lab experiments, ranked by what they decide, each with a positive control and a kill condition |
| [`LEDGER.md`](LEDGER.md) | Every idea raised, struck, or still standing — **264 entries**, with the reason and the file that settled it |
| [`RESULTS.md`](RESULTS.md) | Full per-test results and corrections — 63 sections |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | The ten house rules, and the fault that produced each |
| `*_PREREGISTRATION.md` | 44 files: the predictions, gates and kill conditions, as written before the data |
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
work on vaults. Both are instrument calibration: native co-fractionation cannot retain a known
stoichiometric subunit without admitting 1,733 partners, and there is a pre-registerable stopping rule
for telling co-regulation from co-complex in any co-abundance dataset. Two independent assessments,
each written before seeing the other, ranked these the same two out of ten candidates and zeroed most
of the rest. **[`calibration_edges.tsv`](calibration_edges.tsv)** holds the test case in
machine-readable form.

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

**What was produced rather than rediscovered is one well-controlled negative:** MVP has no
stoichiometric partner complex beyond PARP4 and TEP1, across every instrument available, with
calibration gates passing. No literature check has touched it.

## What survives

A short list, deliberately: the **MVP-PARP4-TEP1 trimer**, with TEP1 shown independent of
PARP4 by knockdown; **ANXA2 and S100A10** as the only confirmed non-subunit interactors of
the old membrane list; **COP1** at 27-fold in one instrument class; **myoferlin actively
excluded**, in a wash-based pulldown and in pre-lysis covalent proximity labelling;
**degradation machinery the most depleted annotation of 1,276** in an anti-MVP pulldown;
and subunit half-lives whose spread sits at only the 29.86th percentile of random triplets.

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
