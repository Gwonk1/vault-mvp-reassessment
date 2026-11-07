# Pre-registration: does MVP's tissue distribution track NAD metabolism?

**Date:** 2026-11-07, before any correlation computed.

## Why
Two of today's results create this question. The SPFH shoulder binds **NAD+/ADP-ribose** with four
contact residues at 100% conservation across 174 eukaryotes (§12, #28). And MVP's top tissue is the
**adrenal gland** (§21), among the most NADPH-demanding tissues in the body through CYP-driven
steroidogenesis, followed by the whole GI tract. If the vault's ligand is NAD-related, its tissue
distribution might follow NAD metabolism.

## Data
HPA consensus, 15,736 expressed genes x 51 tissues, log2(nTPM+1).

## Gate
A known complex must recover itself from tissue co-expression: **RPL7 must return at least 10 ribosomal
proteins (RPL*/RPS*) in its top 25.** Tissue co-expression is coarse, so if even the ribosome does not
hold together, nothing else is interpretable.

## Primary test
Is the pre-specified **NAD metabolism set** enriched among MVP's top 200 tissue-co-expressed genes?
Set fixed now: NAMPT, NMNAT1, NMNAT2, NMNAT3, NADSYN1, NAPRT, QPRT, NADK, NADKD1, CD38, BST1, PARP1,
PARP2, SARM1, NNMT, NMRK1, NMRK2, IDO1, TDO2, ACMSD, HAAO, KYNU, AFMID, NUDT12.

Hypergeometric against all expressed genes.

- **NAD-LINKED:** p < 0.05 with at least 3 set members in the top 200.
- **NOT NAD-LINKED:** otherwise.

## Secondary
Unbiased GO enrichment of MVP's top 200 (BP + CC, 10-500 members, Benjamini-Hochberg), to see what the
tissue profile *does* track if not NAD. Reported descriptively.

## Limits
**n = 51 tissues is a small and highly structured sample**; tissue co-expression is dominated by broad
tissue-specificity rather than by functional partnership, so this is a weak design and a positive result
would be suggestive at best. Bulk tissue mixes cell types. Co-expression is not interaction. A negative
result says the NAD connection does not show at tissue resolution, not that it is absent.
