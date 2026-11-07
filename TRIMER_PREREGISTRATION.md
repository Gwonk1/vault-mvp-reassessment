# Pre-registration: is the vault core a trimer, or an MVP-PARP4 pair with TEP1 as a variable passenger?

**Written 2026-11-07, before reading the PARP4-knockdown columns for TEP1.** Committed before running
`src/trimer.py`.

## Why this question, and why now

Everything else in this project has died. The one association surviving in both co-migration and
physical-contact instruments is MVP with PARP4 and TEP1 (#176), and we have been calling it a
three-protein core since §25. **The instruments do not actually agree about TEP1.**

| instrument | PARP4 | TEP1 |
|---|---|---|
| CFdb co-fractionation, precision | **0.676** (99.99th pct of 10,614) | **0.041** (noise floor) |
| anti-MVP IP-MS, WT_LFC / LWTP | 8.66 / 3.32 | 6.27 / 3.33 |
| CPTAC co-abundance rank, 8 cohorts | 1 of 8 cohorts at rank 1 | rank 2 raw, rank 3 after copy-number adjustment |
| pulse-SILAC half-life | 22.2 h | 40.6 h (MVP 66.4 h) |

PARP4 is dramatically tighter than TEP1 in native co-elution and comparable to it in a pulldown. That is
the signature of a protein recruited **through** another, and it is a specific claim we have never
tested despite building on the trimer for the whole project.

**The Lodwick supplementary table carries PARP4-knockdown columns** (`KD_LFC`, `LKDP`, `WTKD_LFC`,
`WTKD_P`), and §13 already used them to define PARP4-dependence. We have not asked what they say about
TEP1.

## Method

`argon/raw/lodwick_supp_4.xlsx`, sheet `Fig. 5c-d`, parsed exactly as §13 and §41 parsed it. PARP4
dependence is defined exactly as §13 defined it, with no redefinition: a WT interactor
(`WT_LFC > 0`, `LWTP > 1.3`) that additionally satisfies `WTKD_LFC > 0` and `WTKD_P > 1.3` — that is,
significantly reduced in the PARP4-knockdown pulldown relative to wild type.

## Positive-control gates, both required

1. **MVP must be a WT interactor and must NOT be PARP4-dependent.** MVP is the bait and the structural
   subunit; if knocking down PARP4 removes MVP from its own pulldown, the knockdown has destroyed the
   particle and nothing downstream is interpretable.
2. **PARP4 itself must be PARP4-dependent**, as a sanity check that the knockdown worked and the
   dependence columns mean what we think.

Failing either gives **UNINFORMATIVE**.

## Primary test and outcomes, fixed now

Is **TEP1** PARP4-dependent by that definition?

- **TEP1 is PARP4-dependent** → the core is better described as **MVP-PARP4, with TEP1 recruited
  through PARP4**. The "three-protein core" language from §25 onward is then imprecise and we will
  correct it throughout rather than leave it standing.
- **TEP1 is not PARP4-dependent** → TEP1 associates with the vault independently of PARP4, the trimer
  language stands, and CFdb's noise-floor score for TEP1 is a sensitivity failure of that instrument
  rather than a statement about stoichiometry.
- **TEP1 absent or not a WT interactor** → uninformative on this question; §41 already established TEP1
  is a WT interactor at LWTP 3.33, so we do not expect this.

**No expectation is registered.** We genuinely do not know, and the CFdb and IP-MS data point opposite
ways. Saying so is more honest than manufacturing a prediction, and unlike the last four tests there is
no favoured answer to guard against.

## Secondary, descriptive

How many of the 88 WT interactors are PARP4-dependent, and whether the previously named proteins
(ANXA2, S100A10, EHD2, EHD4, CAPN2) fall inside or outside that set. #39 already noted that PARP4
dependence was not enriched among our co-abundant interactors (2 of 12 against 18.5% background), and
this re-states it from the primary table rather than from that summary.

## What this cannot do

A knockdown reduces a protein, it does not remove it, so a negative could reflect residual PARP4. The
dependence columns are a single experiment in a single cell line. And an IP cannot distinguish direct
from indirect association either way — the question here is narrower: whether TEP1's presence in the
pulldown requires PARP4.
