# Pre-registration: the donor list, and varying k

**Written 2026-11-07 after Grok audit 3, before computing either quantity.** Committed before running
`src/donor_and_k.py`. These are the two specific gaps the audit named.

## Test 1: the donor list — is length-and-charge matching a recoding of the label?

Grok accepted the §51 control as legitimate (length and net charge are pre-treatment sequence features,
not on the causal path) **with one condition**:

> *"The match is the wrong control only when the proteins actually drawn from those decile cells are
> ribosomal under another name (translation factors, RBPs, ribosome-biogenesis proteins), i.e. when
> charge/length is a recoding of the label rather than an independent cause of WT_LFC... the donor list
> is the missing number."*

With a 44x charge gap (+130 vs +2.94 per 1,000 residues) and a 2.6x length gap (160 vs 418), the cells
`GOBP_CYTOPLASMIC_TRANSLATION` occupies are a sparse corner of the universe, so the concern is live.

**Method.** For the exact (length decile, charge decile) cells that `GOBP_CYTOPLASMIC_TRANSLATION`'s 95
members occupy, enumerate every protein available as a donor, and compute what fraction belongs to a
**pre-specified "translation-adjacent" set**: the union of `GOCC_RIBOSOME`, `GOBP_TRANSLATION`,
`GOCC_RIBONUCLEOPROTEIN_COMPLEX`, `GOBP_RIBOSOME_BIOGENESIS`, `GOBP_TRANSLATIONAL_INITIATION`,
`GOBP_TRANSLATIONAL_ELONGATION`, `GOBP_RRNA_PROCESSING`, `GOCC_SMALL_RIBOSOMAL_SUBUNIT`,
`GOBP_MRNA_METABOLIC_PROCESS` and `GOBP_RNA_PROCESSING` — all verified present with 12 to 261 members
(house rule 7). The set is fixed here and not adjusted afterwards.

**Reference.** The same fraction computed over the whole 1,166-protein sequenced universe. The donor
pool's enrichment over that baseline is the quantity in question.

**Outcomes, fixed now.**
- **§51's control is INVALID as applied** if the donor pool is **more than 2-fold enriched** for
  translation-adjacent proteins relative to the universe baseline. The matching would then be partly
  regressing the label on itself, the +0.070 residual would be an underestimate by construction, and
  §51 loses its force even as a sensitivity analysis.
- **§51's control STANDS as a sensitivity analysis** if the donor pool is **less than 1.5-fold**
  enriched.
- **PARTIAL** between 1.5x and 2x: the control is weakened and we report the residual with that
  caveat attached rather than as a bound.

**Registered expectation: we expect 1.5x to 2.5x enrichment and therefore PARTIAL or INVALID.** Short
basic proteins in a proteomics universe are disproportionately ribosomal and RNA-binding; that is why
the gaps are so large. If so, **§51 weakens and the class shift gets correspondingly stronger**, which
is a result against our own most recent position.

## Test 2: varying k — does the enrichment behave like a complex or like a window?

Grok: *"The top-200 cutoff magnifies it. No control matched on elution-profile correlation or varied
k."* We cannot match on elution profiles — CFdb distributes scored pairs, not fraction-level profiles —
and we say so rather than approximating it badly. **Varying k we can do.**

**The discriminating prediction, stated before computing.** For a genuine co-complex, the true partners
are the highest-scoring, so enrichment should be **maximal at small k and decay as k grows** and dilutes
them. For a shared-elution-window artefact, the window's occupants are spread through the seed's
high-scoring neighbourhood, so enrichment should be **flat or rising with k**.

**Method.** Recompute §40's statistic at k = 25, 50, 100, 200, 400, 800 for MVP and for the same 150
random seeds, reporting MVP's fold and percentile at each k. Gates at every k: RPL7 and RPS6 above the
95th percentile (a true ribosomal seed must stay high), and the small-complex negatives' median below
the 80th.

**Outcomes, fixed now.**
- **COMPLEX-LIKE** if MVP's fold is highest at k ≤ 50 and declines monotonically, with its percentile
  staying above 95 at small k.
- **WINDOW-LIKE** if MVP's fold is flat or rises with k, or if its percentile is **below 95 at k ≤ 50**
  — the regime where a real co-complex should be most visible.
- **MIXED** otherwise, which promotes nothing.

**Registered expectation: window-like.** Grok's account explains MVP sitting just below RPL7/RPS6 and
inside the dynein/proteasome/condensin cluster, and we have no mechanism to offer against it. **If MVP
is complex-like at small k, that would be the first evidence for §40 that is not a percentile among
seeds**, and we would say so.

## Reachability, per house rules 8, 9 and 10

Both outcomes are attainable on the deciding statistics, and the bars are resolvable: the donor fraction
is a proportion over hundreds of proteins (SE under 0.03), so 1.5x and 2x are far apart relative to it;
and MVP's percentile at each k is a rank among 150 seeds, resolvable to 0.7 points, with the 95 bar well
inside range. **Rule 10 check: the donor-list bars are ~17 SE apart, and the k bars are decided by
monotonic direction rather than a band.**
