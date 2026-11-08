# Pre-registration: is MVP under purifying selection in the lineages that KEPT it?

**Written and committed before any MVP dN/dS value was computed or viewed.** This is the last test of
the project and the one open question §73 and the article series both named and neither answered.

## The question

MVP is **dispensable**: gnomAD v4.0 pLI 0, LOEUF 0.94, observed loss-of-function ~ expected; knockout
mice are healthy; **Ecdysozoa (0/42) and fungi (0) deleted it outright**. Yet it traces to the
eukaryotic ancestor and is kept across ~44% of surveyed eukaryotes.

Leonard Rome's own rubric asks a theory to account for conservation, and the article series conceded
the point in those words: *"If the thing is dispensable enough to delete, why is it conserved where
it's kept? I don't have an answer."* Neither did forty gated tests. **This is that test.**

## Two hypotheses, and what separates them

- **H1 — maintained by selection where kept.** In retaining lineages MVP is under purifying selection
  comparable to genes with established functions. Then "dispensable" is a statement about laboratory
  conditions and redundancy, **not** about absence of function, and the paradox sharpens into a
  specific question: selection for *what*, in those lineages?
- **H2 — retained by drift or inertia.** dN/dS is near 1 or indistinguishable from relaxed genes.
  Then retention is not evidence of function, and **near-neutral tolerated extravagance (currently
  0.03) and furniture (0.04) must be promoted.**

## Fixed in advance

**Species (retaining lineages only, spanning ~600 My).** Human (reference), mouse, chicken,
*Xenopus tropicalis*, zebrafish, and ***Ciona intestinalis*** — the tunicate the §68 census found
**does** carry MVP (2/2), which makes it the one non-vertebrate retainer we can reach.

**Genes.** Subject: **MVP**. Project comparators: **TEP1**, **PARP4**. Essential-gene controls
(expect strong purifying selection): **RPL7, ACTB, GAPDH, TUBB**. Relaxed / positive-selection
controls (expect markedly higher): **TRIM5, MX1, APOBEC3G**.

**Method.** Ensembl REST canonical CDS per species; protein-guided codon alignment; **NG86** pairwise
against human (Biopython 1.88; **YN00 raises `RuntimeError` in this version and LWL85 is unstable, so
NG86 is the estimator — chosen by availability, which is a limit, not a preference**).

**Saturation rule, fixed now:** any pair with **dS > 1.5** is reported but **excluded from the primary
comparison**, because NG86 saturates at deep divergence. Primary = unsaturated pairs only.

## PRIMARY PREDICTION

**MVP's median unsaturated dN/dS is below 0.15 and inside the range of the essential-gene controls.**
Stated plainly because it must be falsifiable: an 893-residue chain that maintains a 78-mer interface
is not what a drifting gene looks like. **So I expect H1, which means I expect this test to make the
conservation paradox worse rather than resolve it.**

## POSITIVE-CONTROL GATE — and it can fail

**The pipeline must separate the two control classes before MVP's number means anything:**

1. **all four** essential controls return median unsaturated dN/dS **< 0.20**, AND
2. **the lowest** relaxed control exceeds **the highest** essential control, AND
3. **at least 3 of 6** species yield an unsaturated pair for every gene reported.

**If any of the three fails, the result is UNINFORMATIVE and MVP's value is not interpreted.** Written
this way because the project's recurring fault was gates with only one reachable answer (house rules
7-9): gate 2 is a strict separation that a noisy pipeline will miss, and gate 3 can fail on orthologue
coverage alone.

## KILL CONDITION

**If MVP's median unsaturated dN/dS is >= 0.5, or is not lower than the lowest relaxed control, H1 is
dead.** Near-neutral and furniture are promoted, and the article's conservation leg is answered in the
uncomfortable direction. **No reinterpretation. A failed prediction is a failed prediction.**

## SECONDARY, registered because it tests the project's own top hypothesis

Hypothesis 1 of `HYPOTHESES_AND_NOVELTY.md` (**0.45**) says the **bare MVP shell is the functional
unit and PARP4/TEP1 are optional**. If so, **MVP should be under stronger purifying selection than
both PARP4 and TEP1.** Registered direction: **dN/dS(MVP) < dN/dS(PARP4) and dN/dS(MVP) <
dN/dS(TEP1).** If MVP is *not* lower than both, that is evidence against the shell-first reading and
it gets recorded as such.

## Reachability check (house rule 9)

dN/dS is unbounded above and bounded below by 0, so both "indistinguishable from essential" and
"indistinguishable from relaxed" are reachable for every gene. The gate's three clauses are each
independently failable. **Nothing here can pass by construction.**

## Known limits, stated before the result

NG86 assumes equal codon usage and no transition/transversion bias; it is conservative at low
divergence and biased at high. One estimator, no bootstrap over sites, pairwise rather than a codon
model on a tree. **This can distinguish "like an essential gene" from "like a drifting gene." It
cannot locate selection on particular sites or branches, and nothing below will claim it does.**

---

## Amendment, committed before the run

Two things the registration above did not specify, fixed here rather than decided after seeing numbers:

1. **Alignment source.** Ensembl Compara's homology endpoint with `sequence=cds` returns a
   **codon-aligned CDS** for both members (verified: 2,679 columns for human-mouse MVP = 893 codons,
   MVP's exact length). Compara aligns proteins and threads the CDS through, which **is** the
   protein-guided codon alignment registered above, produced by the resource rather than by us. We use
   it. `dn_ds` comes back `null`, so the estimate is ours.
2. **Orthologue tie-break.** Where a species returns more than one homology, take the
   **`ortholog_one2one`** if present; otherwise the one with the **highest `perc_id`**. Ties broken by
   the lexicographically first stable id, so the choice is deterministic and not ours to make later.
3. **Codon filtering.** Drop any codon column where either sequence has a gap, an ambiguity, or a stop.
   Report how many codons survive per pair, because a pair that keeps very few is not evidence.
