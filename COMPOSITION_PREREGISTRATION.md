# Pre-registration: is MVP's amino-acid composition that of a storage protein?

Written before any composition was computed. Prompted by Graham's chair/furniture line - *"if someone
is making chairs, they might eventually want to sit down... maybe they borrow raw materials... maybe
they do it because they will need them"* - and his follow-up, **what would the chemical composition be
useful for?**

## The reasoning

A protein whose job is to **bank raw material** has a composition signature. Plant seed storage
proteins and milk caseins are **nitrogen-rich** - loaded with Arg, Asn, Gln, Lys - because nitrogen is
the scarce element being stockpiled. A protein whose job is **structure** has no such bias; it is near
the proteome average, or shifted toward hydrophobics and helix-formers.

MVP is 893 residues at ~78 copies per particle, and the particle count per cell is quoted up to
100,000. **If any protein in the human proteome were a bulk amino-acid or nitrogen reserve, the
composition would show it.** This is cheap, decisive in one direction, and computable from sequence.

## Method

UniProt reviewed human proteome (Swiss-Prot) as the baseline, **downloaded, not remembered**. For each
protein, elemental composition from the standard residue formulas (C/H/N/O/S per residue, which are
definitional, not estimated), plus per-residue amino-acid frequencies. Report **side-chain nitrogen per
residue** and **sulfur per residue** as z-scores against the proteome distribution.

## PREDICTION

**If the storage reading has any support from composition, MVP's nitrogen-per-residue sits above the
proteome mean by at least 1 SD.** Registered direction: **above**.

## POSITIVE-CONTROL GATE - failable in both directions

1. **At least two of three known storage/reserve proteins** (casein CSN1S1, albumin ALB, ferritin
   light chain FTL) must come out **above** the proteome mean on nitrogen-per-residue.
2. **At least two of three known structural proteins** (clathrin CLTC, actin ACTB, tubulin TUBB) must
   come out **not above** +1 SD.
3. Both groups must be found in the downloaded proteome by accession, **with the count reported**, so a
   missing control cannot pass silently (house rule 7, broken three times this week).

If the gate fails, **UNINFORMATIVE** and MVP's composition is not interpreted.

## KILL CONDITION

**If MVP's nitrogen-per-residue is within +1 SD of the proteome mean, composition gives the storage
reading no support**, and "the vault is a raw-material reserve" stays where it is - unranked, and now
with one piece of evidence against it rather than none.

## Known limits, stated first

Composition is suggestive, not dispositive: a reserve could be stored for carbon or for specific
essential residues rather than nitrogen, and a structural protein can be incidentally N-rich. **This
test can refuse the simplest version of the storage idea. It cannot establish it**, and nothing below
will claim it does.
