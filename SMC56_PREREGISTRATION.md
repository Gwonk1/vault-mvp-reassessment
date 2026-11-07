# Pre-registration: is the SMC5/6 observation real, or an annotation coincidence?

**Written 2026-11-07, before any correction, control or second-instrument lookup.** Committed before
running `src/smc56.py`. §44a recorded the observation as a diagnostic of our own design gap; this tests
it.

## The observation

`GOCC_SMC5_SMC6_COMPLEX` has 6 members in the IP-MS universe and 4 are vault interactors — SMC6
(+6.79), NSMCE3 (+6.00), NSMCE1 (+5.79), SMC5 (+3.93), none PARP4-dependent — while NSMCE4A (LWTP 0.48)
and NSMCE2 (0.06) are not. Expected 0.44 of 6. The term was excluded from the §44 scan by our
registered 10-500 size filter, so it is untested rather than negative.

## Three threats, and a test for each

### Threat 1: multiple testing across small terms

Thirty-four excluded small terms hit three or more interactors, most of them nested metabolic
annotations recycling the same few enzymes. **Test:** BH-correct across *every* term with fewer than 10
members in the universe — the whole excluded family, not the ones that happened to hit. SMC5/6 must
reach **q < 0.05** within that family. Reporting it without this correction would be cherry-picking.

### Threat 2: nuclear contamination of a cytoplasmic pulldown

**This is the serious one.** SMC5/6 is a nuclear DNA-repair SUMO ligase complex; MVP is cytoplasmic. A
vault pulldown returning a nuclear complex is more easily explained by nuclear carry-over than by
biology, and this project has already been burned twice by compartment artefacts (#103's EZH2 limb,
#160).

**Control, the same shape as §40's SPFH-family control:** the other SMC-family complexes must **not**
be enriched. Cohesin (SMC1A, SMC3) and condensin (SMC2, SMC4) are equally nuclear, equally abundant
chromosomal ATPases. **If SMC1A, SMC2, SMC3 and SMC4 are vault interactors too, this is a nuclear or
abundance artefact and the claim dies.** If only the SMC5/6 complex comes down, the signal is specific
to one complex and not to nuclear SMC proteins generally.

Secondary on the same threat: the §44 scan found zero terms at q < 0.05 across 1,276 terms, including
nuclear ones, which already argues against general nuclear carry-over. We state the direction of that
evidence now rather than after.

### Threat 3: single instrument

**CFdb co-fractionation lookup** for MVP's edges to SMC5, SMC6, NSMCE1 and NSMCE3, with MVP-PARP4 at
its known precision 0.676 as the positive control that the lookup works.

**A CFdb negative here is weak evidence and we say so before looking.** #180 established that CFdb
scores MVP-TEP1 at 0.041, the noise floor, for a protein the pulldown confirms at LWTP 3.33 — so that
instrument demonstrably misses real vault partners. A CFdb positive would be strong; a CFdb negative
cannot kill this. Registering that asymmetry now is the point, because after a negative it would look
like an excuse.

## Outcomes, fixed now

- **SURVIVES** if q < 0.05 within the small-term family **and** fewer than two of the four
  cohesin/condensin controls are interactors. Then: the vault physically associates with one specific
  nuclear complex, which is the first positive neighbourhood result in this project and the only term
  ever to clear a gate here.
- **DIES** if q ≥ 0.05 in the corrected family, **or** if the cohesin/condensin controls come down too.
  Then it is an annotation coincidence or a compartment artefact, §44a's flag is closed, and we record
  that our design gap cost nothing.
- CFdb is reported either way and decides nothing on its own.

**Registered expectation: we expect this to die on Threat 2.** A cytoplasmic 13 MDa particle pulling
down a nuclear SUMO ligase complex is prior-implausible, nuclear carry-over is the ordinary explanation,
and this project's base rate for surviving a first specificity control is poor. If the cohesin and
condensin controls stay clean, we will have been wrong in the interesting direction for the second time
(§40 was the first).

## What this cannot do

Four proteins of one complex in one pulldown, even corrected and controlled, is a lead and not a
demonstrated interaction. SMC5/6 and the vault could meet during mitosis when the nuclear envelope
breaks down, which an unsynchronised lysate would capture as association without it being a steady-state
feature. Nothing here distinguishes direct contact from shared presence in a sub-complex.
