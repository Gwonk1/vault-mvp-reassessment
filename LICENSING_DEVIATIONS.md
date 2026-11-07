# Deviation: nuclear reference set for test B

**Written before seeing any test B result** — the first run crashed on an empty set, so no value was
produced.

`LICENSING_PREREGISTRATION.md` specified 200 random proteins drawn from **`GOCC_NUCLEUS`**. That term
does not exist in `c5.go.cc.v2024.1.Hs.symbols.gmt`; neither does `GOCC_NUCLEOPLASM` or
`GOCC_NUCLEAR_LUMEN`. The term was named from memory and not checked against the file.

**Substituted: `GOCC_NUCLEAR_BODY` (859 members)**, the largest unambiguously nuclear cellular-component
term present in the release. External and unmodified, as registered. Everything else about test B is
unchanged: 200 random draws, residualised Spearman against MVP, EZH2 judged against the 5th percentile
of that background.

This is the same fault class as #64 — a gene or term identifier taken from memory rather than read from
the file. Logged rather than quietly fixed.
