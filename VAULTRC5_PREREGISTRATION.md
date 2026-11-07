# Pre-registration: does losing vault RNA break the p62 / autophagy buffer?

**Date:** 2026-11-07, before any differential expression computed. Tests **layer 3** of Graham's model
(article 1 §5, article 4): the barrel sequesters vtRNA; free vtRNA brakes p62 oligomerisation; so vault
RNA availability sets selective-autophagy capacity. A version of this model has been raised within the field but we could find no published test of it. `LEDGER.md` lists it UNTESTED.

## Data
GSE269048: total RNA-seq of **Vaultrc5-knockout vs floxed control mice**, brain and liver, 3 biological
replicates per genotype per tissue (12 samples), 7-9 week old males. Counts for 55,450 genes.

## Gate
**Vaultrc5 itself must be reduced in the knockout** if it is present in the annotation. If it is absent
(a Pol III transcript may not be quantified), the fallback gate is that knockout and control must
separate on the first two principal components within a tissue. If neither holds, nothing is reported.

## Primary test
Is the **autophagy / p62 receptor program** altered in knockout versus control? Pre-specified set, fixed
now: *Sqstm1, Nbr1, Tax1bp1, Calcoco2, Optn, Map1lc3a, Map1lc3b, Gabarap, Gabarapl1, Gabarapl2, Atg5,
Atg7, Atg12, Ctsb, Ctsd, Lamp1, Lamp2, Tfeb*.

Per tissue: differential expression knockout vs control, then test whether this set is shifted against
the genome-wide distribution (Mann-Whitney on log fold change, and the set's mean percentile).

- **BUFFER SUPPORTED:** the autophagy set shifts significantly in at least one tissue (p < 0.05),
  in a consistent direction.
- **NO EFFECT:** it does not. Given the model says vault RNA availability *sets* autophagic capacity,
  deleting the RNA outright should move this program if the model is right at the tissue level.

## Secondary (reported, not decisive)
- Interferon response genes (mouse Hallmark IFN-gamma orthologs) — tests whether vault RNA loss
  derepresses innate sensing, the containment-adjacent prediction.
- Membrane repair set: *Anxa2, S100a10, Ehd2, Ehd4, Capn2, Capns1*.
- The vault components themselves: *Mvp, Tep1, Parp4* — does losing the RNA destabilise the particle's
  transcription?

## Limits
Whole brain and whole liver, so cell-type-specific effects are diluted. mRNA abundance is a weak proxy
for autophagic flux — the model predicts a change in p62 *oligomerisation and turnover*, which is a
protein-level event this cannot see. **A null here bounds the tissue-level transcriptional consequence;
it does not refute the biochemistry.** The authors' own title says the RNA is dispensable to development,
so a large effect is not expected.
