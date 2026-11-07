# `argon/raw/` — third-party source files, not redistributed

This directory is intentionally empty in the published repository. It holds 62 files
(~251 MB) of third-party material that the analysis reads but that we do not
redistribute, because licences differ and several are publisher-hosted:

| Source | Licence | Redistributable |
|---|---|---|
| bioRxiv preprints (Osinski 2026, Le Mouellic 2026, Hornebeck 2026) | CC-BY 4.0 | yes, but fetched for consistency |
| PDB structure files (9BW6, 11JB, 9R86, 9R87) | public domain | yes, but fetched for size |
| cBioPortal / CCLE / BioPlex / IntAct / eggNOG extracts | public, per-source terms | yes, but fetched for size |
| *Nature Communications* XML and supplements (Lodwick 2025) | **unverified** | not assumed |
| PMC XML, Musgrove 2026 HTML and supplements | **unverified** | not assumed |

`SHA256SUMS.txt` pins the exact bytes every result in this repository was computed
from. Anyone re-running the analysis should fetch the sources themselves and verify
against it:

```bash
cd argon/raw
./fetch.sh                      # downloads what can be fetched automatically
sha256sum -c SHA256SUMS.txt     # verify; manual downloads are listed below
```

Files `fetch.sh` cannot retrieve without a publisher session are listed in its
`MANUAL` block, with the DOI or accession to fetch each one from by hand.

**Why this matters for reproducibility.** Every number in `RESULTS.md` traces to a
file in `results/`, which is committed in full. This directory is only needed to
*recompute* those numbers from scratch, not to check them.
