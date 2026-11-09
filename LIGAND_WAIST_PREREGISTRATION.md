# Pre-registration: does the vault's waist interface differ by ligand state?

Registered before any structure beyond 4V60 and 11JB was parsed for contacts.

## The series, and why it exists

Lodwick et al. 2025 deposited a **ligand series on one species by one method from one group** - the
ideal control for asking whether anything about the particle changes with occupancy:

| PDB | contents |
|---|---|
| **9BW5** | Human Vault Cage (apo) |
| **9MXH** | + NAD+ |
| **9MXV** | + ADP |
| **9BW6** | + PARP4 |
| **9BW7** | + PARP4 and NAD+ |

## Two aims, and the second is probably foreclosed

**PRIMARY - a 5-fold replication of the contact set.** §95 established the inter-half interface as ~10
residues of the N-terminal tail in **two** structures. Five more determinations of the same interface
would pin the **consensus** contact set far better than two, which is the honest way to address §94c's
power problem: not by inventing residues but by establishing which ones are real.

**SECONDARY - the ligand comparison, registered with its own likely failure.** Grok audit 009's
reconciliation of §88b's contradiction was *"a trigger - ligand, modification or chaperone - nucleating
a homomeric opening."* The NAD+ pocket is lumen-facing and inter-subunit (§73). **If NAD+ occupancy
changed the waist, that would be a mechanical link from ligand to join.**

**We expect it not to.** All five are **closed cages reconstructed with imposed C39** - a
ligand-driven opening **would not have survived into a closed-cage reconstruction**, and the depositors
would have reported a gross difference. **This secondary test is largely foreclosed by what gets
deposited**, and is registered anyway because the primary aim requires the same parse.

## Method - identical to §94/§95, no changes

Full `-assembly1` files from RCSB. Split chains into halves on mean axial coordinate; a residue is a
waist contact if any atom comes within **4.5 A of an atom in a chain of the other half.** Contacts
restricted to within 60 A of the waist plane for tractability.

## PREDICTIONS

1. **Every structure returns a small, N-terminal-dominated contact set** - under 30 residues, with
   **>= 60% at residue <= 50.**
2. **The ligand states do not differ materially:** pairwise overlap of contact sets **>= 60%**, and
   contact counts within **+/- 8** of each other.
3. **A consensus set - residues contacting in >= 4 of the 5 - exists and is non-empty.**

## GATE

Each assembly must split into **two equal halves** (39/39, or whatever the deposited stoichiometry
dictates, reported per structure), and must return a non-empty contact set. **A structure failing
either is reported and excluded, not silently dropped.**

## KILL

**If the contact sets disagree wildly across structures that are nominally the same closed cage, the
measurement is unstable and §95's replication was luck.** That would withdraw §95c's upgraded
statement rather than extend it.

## What this cannot do

It cannot detect a seam or an open state - **every structure here is symmetry-averaged**, which §91a
establishes forecloses interface inequality. **Five symmetrised closed cages cannot answer a question
about asymmetry**, and nothing below will claim they do.
