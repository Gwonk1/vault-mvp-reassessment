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

---

# Addendum: waist-versus-cap order from deposited B-factors

Registered before any B-factor was read. §91e lists **waist-versus-cap local resolution** as one of two
cheap measurements we skipped. The deposited maps are not local; **the coordinate files are**, and in a
cryo-EM model the per-atom `B_iso_or_equiv` is fitted against local map quality, so it is a usable
proxy - **a weaker one than the map, and labelled as such.**

## Why the direction matters

Grok audit 009: *"39-fold is NCS... a well-resolved waist under that averaging is positive evidence
that the crystallized molecules were closed and similar; a high open-occupancy would have cost waist
resolution relative to the cap."*

So the two outcomes mean opposite things:
- **waist better ordered than cap** (lower B) -> the particles that entered the average were closed and
  mutually consistent at the waist. **Evidence against a substantial open population in that dataset.**
- **waist worse ordered than cap** (higher B) -> waist heterogeneity survived into the model.
  **Consistent with, though not evidence for, a mixed population.**

## Method, fixed now

CA atoms only, from **11JB** (78-mer, `symmetry_type POINT`) and **4V60-assembly1** (D39). Parse the
`_atom_site` loop header for column indices rather than assuming them - **the assumption is what broke
the first attempt at this.** Waist and cap defined on the axial coordinate by the same geometry as
above: **waist = the 15% of residues nearest the waist plane, cap = the 15% furthest.** Report median B
for each and a Mann-Whitney U.

## PREDICTION

**The waist is better ordered than the cap - median B lower at the waist.** Reasoning: these are
purified, closed particles selected for intactness through picking and 2D, and the waist is the most
constrained part of such a particle; the caps carry PARP4/TEP1 density and flexible termini. **This
prediction, if met, is evidence AGAINST our own zipper interest** - it says the deposited datasets were
closed, which is what grok said a well-resolved waist would mean.

## GATE

Per-residue B must actually **vary** - if the deposited B-factors are constant or near-constant (some
cryo-EM depositions set them uniformly), the proxy carries no information and **the test is void**.
Require **interquartile range > 0** and at least 200 residues per bin.
