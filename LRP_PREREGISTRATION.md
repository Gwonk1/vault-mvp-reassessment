# Pre-registration: what actually explains the 30-year LRP chemoresistance biomarker?

**Date:** 2026-11-07, before any drug correlation computed. Implements argon's H4; Claude's design.
Graham stated no predictions.

## Why
High LRP/MVP in a biopsy has predicted chemotherapy failure since the 1990s with no mechanism
(`LEDGER.md` #21). §9 showed MVP is not a drug-handling gene in CRISPR screens; §10 showed it is not a
persister marker. Three competing explanations remain, and they are separable in cell lines:

- **Model A — chromosomal passenger.** `ABCC1`/MRP1, a *proven* efflux pump, sits at chr16:15.9 Mb;
  MVP at chr16:29.8 Mb. Whole-arm 16p gain co-amplifies both, so MVP may ride along with a real pump.
- **Model B — division-rate passenger.** §12 found MVP anti-correlates with proliferation at the genome
  floor in lung and melanoma. Cytotoxics kill dividing cells, so slow tumours look MVP-high and resistant.
- **Model C — vault RNA drug binding.** vtRNA1-1/1-2 bind mitoxantrone and anthracyclines directly, so
  resistance should be **drug-class specific** rather than general.

## Data
- MVP, ABCC1, ABCB1, SLFN11 protein from `data/processed/prot/ccle_broad_2019.parquet` (375 lines).
- Drug response: GDSC1 + GDSC2 fitted dose-response (release 8.5), AUC per cell line x drug.
- Copy number: `ccle_broad_2019_cna` from cBioPortal (chr16p genes).
- **Doubling time: already present** in the CCLE clinical table (`DOUBLING_TIME`).
- Proliferation protein score: mean z of MKI67, TOP2A, MCM2 where measured.
- Cell lines matched by stripping the tissue suffix from CCLE sample IDs.

## Gates, evaluated before reading MVP
1. **ABCB1 protein predicts resistance to taxanes/vinca alkaloids** (paclitaxel, docetaxel, vinblastine,
   vincristine), p < 0.001 in the expected direction.
2. **ABCC1 protein predicts resistance to etoposide and/or doxorubicin**, p < 0.01.

If neither gate passes, the drug-response matching is broken and nothing about MVP is reported.

## Primary test
Across matched lines, is **MVP protein associated with resistance (higher AUC) to cytotoxic
chemotherapeutics**? Spearman per drug, then combined across the pre-specified cytotoxic set
(anthracyclines, mitoxantrone, etoposide, cisplatin, carboplatin, oxaliplatin, gemcitabine, 5-FU,
cytarabine, vincristine, vinblastine, paclitaxel, docetaxel, irinotecan, topotecan).

- **BIOMARKER IS CELL-INTRINSIC:** MVP associates with resistance after Benjamini-Hochberg.
- **NOT CELL-INTRINSIC:** no association. **This would mean the thirty-year clinical signal is not a
  property of the tumour cell at all** — stromal, immune or compositional — which is a substantive
  answer to #21 and the single most likely outcome given §9 and §10.

## Mediator dissection (only if the primary is positive)
Nested models per drug: MVP alone; MVP + ABCC1 protein + chr16p CNA (A); MVP + doubling time +
proliferation score (B). Report how much of MVP's coefficient each absorbs. For C, compare effect sizes
in vtRNA-binding drugs (anthracyclines, mitoxantrone) against non-binders, after adjusting for A and B.

## Kill condition
If MVP protein has no association with any cytotoxic drug while ABCB1 and ABCC1 gates both pass, Models
A, B and C are all unnecessary and #21 is answered: **the biomarker is not cell-intrinsic.**

## Limits
Cell lines lack stroma and immune cells, which is precisely why a null here would implicate them. GDSC
AUC is a short-term viability readout, not clinical response. Protein coverage is 12,096 proteins over
375 lines, so some drugs will have few matched lines.
