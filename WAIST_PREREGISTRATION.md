# Pre-registration: are the WAIST contact residues constrained, and how, relative to other interfaces?

Written before the conservation column was read for any waist split. This is the test **§87d refused and
§91b/house rule 16 says is owed.**

## Why it is owed

We declined it by arguing that a perfectly symmetric 39-fold ring has no designated nucleation start, so
no statistic can name which subunit fires first. **True, and it answers a different question.** Grok
audit 009: *"stochastic nucleation removes a start-site conservation test and leaves the contact test
untouched."*

## What already exists, and what it does not answer

`results/surface_residues.csv` (from `src/surface.py`, registered in `SURFACE_PREREGISTRATION.md`)
already carries per-residue `interface`, `buried`, `exposed`, axial coordinate `z`, and `cons` -
conservation from the eggNOG 2QPP0 alignment anchored on the rat sequence. **The general result is
already in the record:** interface residues are more conserved than exposed non-interface residues.

**It does not answer the waist question**, because `interface` is defined as any residue losing >20 A^2
of accessibility in context - **all** subunit-subunit contacts, lateral and cap as well as inter-half.

## The split, fixed now on geometry alone

The reference chain spans **z = -329.7 to -0.7**, i.e. one half of the particle, with **z ~ 0 the waist
end and |z| ~ 330 the cap end.** Fixed before reading any conservation value:

- **WAIST-PROXIMAL** = interface residues with **|z| <= 50 A**
- **DISTAL** = interface residues with |z| > 50 A
- **NULL** = exposed non-interface residues (any z)

## PREDICTION, with its direction and its reasoning

**Waist-proximal interface residues are LESS conserved than distal interface residues.**

Reasoning, stated so the prediction is not a free bet: **an interface that has to come apart cannot be
optimised like one that never does.** A permanent lateral contact can accumulate every stabilising
substitution available; a contact that must open under some condition is under a **two-sided**
constraint and should tolerate more variation. This is the opposite of the naive guess - that the waist
matters, so the waist is conserved - and we are registering against the naive guess on purpose.

## GATE - failable

1. **The general result must reproduce:** interface `cons` mean > exposed non-interface `cons` mean.
   If the existing column does not show that, the conservation values are not usable here.
2. **At least 15 residues in the waist-proximal bin.** Fewer is underpowered and the comparison is not
   made.
3. **Mann-Whitney U reported**, not only means, because `cons` is bounded on [0,1] and skewed.

## KILL

**If waist-proximal conservation is >= distal, the prediction is wrong and gets recorded as wrong.** The
naive reading would then be the better one, and "an interface that must open is less optimised" dies.

## What this cannot do

It cannot distinguish zipper from hinge from iris - **every opening model uses these same contacts**,
which is precisely why grok called the test informative regardless of mechanism. It also cannot
establish that the waist opens at all in a mature particle (§91c).
