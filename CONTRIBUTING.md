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
