# A pre-registered reassessment of the vault particle (major vault protein)

Nineteen pre-registered computational tests of standing hypotheses about the vault
ribonucleoprotein and major vault protein (MVP), run against public transcriptomic,
proteomic, genomic, structural and comparative data. Each test carried a
positive-control gate and an explicit kill condition written down before the
relevant data were read.

**Most of the hypotheses failed, including ours.** That is the result.

## Start here

| File | What it is |
|---|---|
| [`papers/PAPER1_vault_reassessment.md`](papers/PAPER1_vault_reassessment.md) | The reassessment: what survived, what did not, and the gate scorecard |
| [`papers/PAPER2_bench_experiments.md`](papers/PAPER2_bench_experiments.md) | Eleven wet-lab experiments, ranked by what they decide |
| [`LEDGER.md`](LEDGER.md) | Every idea raised, struck, or still standing — 91 entries, with the reason and the file that settled it |
| [`RESULTS.md`](RESULTS.md) | Full per-test results and corrections |
| `*_PREREGISTRATION.md` | The predictions, gates and kill conditions, as written before the data |

## What this repository is honest about

The ledger is the point of the project. Roughly twenty of its entries are the
authors catching themselves — a mediation analysis that divided coefficients fitted
on different subcohorts and reversed a conclusion, a cross-species comparison that
matched human gene symbols to amoeba gene names, a result described from the bottom
slice of a sorted table, a claim that the paper's own committed JSON contradicted on
the facing page. Each correction sits next to the original claim rather than
replacing it.

Two further language-model agents reviewed the manuscripts adversarially against the
committed data, over three rounds. Between them they struck or qualified more than a
dozen claims. The review correspondence is in `channel/` and `argon/`.

**On pre-registration.** The full development history is published here, 62 commits
with their original timestamps, so the ordering is checkable rather than merely
asserted. `git log --reverse` shows each prediction committed before the data it
tested were read.

Three redactions were made to that history, deliberately, and the final commit
records them: references sourcing a hypothesis and an NLRP3 immunogenicity report to
private correspondence are replaced with neutral phrasing and now marked as claims we
could not independently source; the filenames of gitignored source transcripts are
generalised; and local filesystem paths are made relative. Published citations are
untouched. Nothing else about the development record has been altered, including the
parts where we were wrong.

**Five of the nineteen tests are formally uninformative** because a control gate
failed, and they are marked as such rather than promoted. The scorecard is in the
introduction of paper 1.

## Reproducing it

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt   # if present
cd argon/raw && ./fetch.sh && sha256sum -c SHA256SUMS.txt            # third-party sources
```

`results/` is committed in full, so every number in the papers can be checked without
refetching anything. `argon/raw/` is only needed to recompute from scratch; it is
excluded because several files are publisher-hosted with licences we did not verify.
See [`argon/raw/README.md`](argon/raw/README.md).

Analysis scripts are in `src/` (and `argon/src/` for the second agent's tests).

## Licence

Dual-licensed: prose, papers and results under **CC BY 4.0**, code under **MIT**.
See [`LICENSE`](LICENSE) for which applies to what, and for the citation. Third-party
material read by this project is not relicensed — see [`argon/raw/README.md`](argon/raw/README.md).

## Status

Not peer reviewed. Not submitted. Corrections are welcome and will be recorded in the
ledger like every other correction.
