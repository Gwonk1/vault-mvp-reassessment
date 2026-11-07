# Vault hypothesis ledger

Every idea raised, with its status, the reason, and the file holding the evidence. Struck entries are
kept, not deleted — the point is to not re-run a dead idea or re-argue a settled one.

**Discipline used throughout 2026-11-06:** each test was pre-registered in git *before* the relevant data
was read, with a gate requiring the method to recover a known positive first. Where a gate failed it is
reported as failed rather than rewritten. `git log --oneline` shows the ordering.

Status key: ~~**STRUCK**~~ eliminated · **WEAKENED** damaged but alive · **STANDING** survives ·
**PENDING** running · **UNTESTED** never examined.

---

## STRUCK

| # | Idea | Why it's out | Data |
|---|---|---|---|
| 1 | ~~MVP belongs to the chronic interferon resistance program (ISG.RS)~~ | Pre-registered prediction. Needed Δ>0 within malignant cells; got −0.11 (CI −0.18,−0.05) in lung, −0.09 (−0.22,+0.04) in melanoma. CHRONIC in no dataset, model or compartment. | `results/sc_kim.json`, `sc_jerby.json`, `bulk.json` |
| 2 | ~~Vaults suppress cytosolic sensing, so MVP should anti-correlate with interferon~~ | The containment layer's only prediction testable here. MVP *rises* with interferon in malignant cells (ρ +0.23 ISG.RS, +0.29 IFNG.GS, lung). Does not refute containment as a physical function — that needs Trap-and-Seq. | `results/sc_kim.json` |
| 3 | ~~MVP's membership in Benci's IFNG.GS tells us something about MVP~~ | IFNG.GS is exactly Hallmark IFN-γ minus ISG.RS. MVP landed in the "acute" bucket by subtraction. Nobody tested it. | `data/genesets/genesets.json` |
| 4 | ~~The contradictory MVP tumour papers resolve as positions on the acute/chronic axis~~ | Thyroid (−1.57), pancreas (−0.82), liver (−0.65) all sit on the *same* side, thyroid furthest from chronic. The contradiction is not an axis artifact. | `results/bulk.json` → `tcga` |
| 5 | ~~MVP expression predicts checkpoint-inhibitor response~~ | Pooled log odds per SD +0.04 (−0.30, +0.38), 5 cohorts. Two nominal hits in opposite directions, neither surviving correction. | `results/bulk.json` → `resp_meta` |
| 6 | ~~Mvp carries the chronic program's epigenetic memory mark~~ | Absent from Qiu's strict memory-domain list; nearest domain 730 kb away; promoter accessibility 39th pct where Oas1a is 94th; STAT1-dependence 63rd vs 100th; RNA falls ~13% on STAT1 loss vs 3–5 fold for real targets. | `results/epigenetic.md`, `epigenetic.log` |
| 7 | ~~MVP loss impairs cell growth~~ | Zero hits across 878 proliferation screens. Only ~4.8% of genes manage that; the median gene has 5. | `results/orcs_final.json` |
| 8 | ~~A coherent gene module is lost whenever MVP is lost~~ | **Re-run after fixing a taxonomic artifact the audit found** (Spiralia — *Aplysia*, *Helobdella* — both retain MVP but were swallowed into a "Protostomia lost" call; now correctly `Ecdysozoa`): best q still 0.1566, still zero significant terms. Conclusion unchanged. Note co-loss is structurally blind to partners that are themselves essential and never deleted — which is why #25/#26 found what this could not. No GO term reached q<0.05 (best 0.16) across 6,128 families / 472 species, while 45% of matched random families *did* hit something. Method recovers cilia from IFT88 and complex I from NDUFS2. | `results/coloss_final.json` |
| 9 | ~~MVP marks the drug-tolerant persister state~~ | Needed 90th percentile induction in ≥2 of 3 models; got 80.6 / 82.0 / 81.1. Reproducible but not a core persister gene, and not interferon-driven. | `results/persister_primary.json` |
| 10 | ~~MVP sequences are "all different" across animals~~ | 60.6% mean pairwise identity over 174 sequences / 134 species — **89.5th percentile** against 400 species- and length-matched groups (matched median 47%). | `results/divergence.json` |
| 11 | ~~Vaults are developmental scaffolding you build on and discard~~ | Predicted decline across development. MVP *rises*: 94–95th percentile in 6 of 7 organs. Zero organs showed the predicted decline. | `results/development.json` |
| 12 | ~~MVP is a brake that tells a cell to stop dividing~~ | A brake, deleted, should release growth. 878 growth screens, both selection directions, nothing. | `results/orcs_final.json` |
| 13a | ~~Vaults are immunologically invisible in lupus (the "autoantigen asymmetry" vs Ro60/La)~~ | **Struck by published literature, not by us.** Moadab et al., *J Rheumatol* 2023;50(9):1136 (PMID 37127324) screened >21,000 human proteins with SLE sera: Ro60 was the top hit, and **MVP was in the top 10**, validated by ELISA in two SLE cohorts (n=49, n=46). Article 5 experiment 5 pre-committed: "If anti-MVP shows up... that whole thread collapses." It showed up, three years ago. The *instinct* to put vaults and lupus in one room was right — vaults are targeted alongside Ro60, AGO1-3 and ribosomes. | PMID 37127324 / PMC10524170 |
| 13 | ~~The CoA-like pocket is a phosphopantetheine tether (a "string")~~ | A covalent arm needs a phosphopantetheinyl transferase (human: AASDHPPT) and a conserved serine; MVP is not among the few known human carrier proteins. The reported *pocket* density reads as a bound ligand, not an arm. Sink reading survives; tether does not. | reasoning from published structure description |

---

## WEAKENED

| # | Idea | What damaged it | Data |
|---|---|---|---|
| 14 | Vaults are vestigial | Three things don't fit: the cost (100,000 copies/cell), **sequence conservation at the 89.5th pct**, and missense constraint (mis_z 2.5) alongside LoF tolerance. Vestigial structures drift; this one doesn't. Losses are clean whole-clade events, not ongoing decay. | `results/divergence.json`, `gnomad.json` |
| 15 | ~~The vault is NOT regulated as one unit~~ **REVERSED** — see STANDING #25 | Four independent lines say no: TEP1/PARP4 not co-lost with MVP; they don't follow MVP across development (MVP 95th pct, TEP1 4–79th, PARP4 6–59th); their groups sit at the 0.8th and 3rd percentile of conservation while MVP is at 89.5th. Protein co-abundance pending. | `coloss_final.json`, `development.json`, `divergence.json` |
| 16 | MVP marks the non-dividing compartment inside tumours | Pre-registered rule needed 4 of 6 cohorts below the 10th pct; got 3 — but those three are at the genome *floor* (LUSC 0.0, SKCM 0.5, LUAD 0.7) while pancreas runs opposite (86.5). Gate passed cleanly. Tissue-specific, not general. | `results/proliferation.json` |
| 17 | The chassis framing | Survives every test, but flagged as **nearly unfalsifiable** — every new observation becomes "another customer". Its own prediction (shape conserved, sequence free) failed: the sequence *is* conserved. | `results/divergence.json` |

---

## STANDING

| # | Idea | What supports it | Data |
|---|---|---|---|
| 18 | **Sink / absorption, deployed on demand** — best-fitting model so far | Six independent results with no special pleading: no partner module; zero growth phenotype (nothing to absorb in clean media); rises with tissue maturation (accumulated load); interferon-coupled at the 95th pct (deploy on alarm); conserved sequence with tolerated loss (precise site, redundant system); reproducible mild rise under three unrelated drugs. Weakness: **"absorb what?" is unanswered**, and without a ligand it predicts nothing. | §§2,3,8,9,10 of `RESULTS.md` |
| 19 | MVP is unusually interferon-coupled without belonging to either program | 95th pct (ISG.RS) and 88th (IFNG.GS) in lung malignant cells; 97th/78th in melanoma. The one clearly *positive* finding of the day. | `results/sc_kim.json`, `sc_jerby.json` |
| 20 | MVP marks finished tissue rather than building tissue | 94–95th pct rise across 6 organs, opposite in direction to proliferation, so not the proliferation confound. | `results/development.json` |
| 45 | **#21 ANSWERED: the LRP biomarker is slow division plus modest multidrug resistance, with MVP a passenger on both** | 292 lines, CCLE protein x GDSC. MVP predicts resistance in 8/19 cytotoxics, concentrated in tubulin agents. **Model C dead**: vtRNA-binders +0.098 vs non-binders +0.099, and mitoxantrone is the least-associated drug tested. **Model A dead**: ABCC1 fails its own gate. **CORRECTED 2026-11-07 after external audit + my own verification: on 132 complete-case lines, ABCB1 absorbs 25.0% and division rate 10.6% — the ordering is REVERSED from my first write-up, which divided betas fitted on different subcohorts (n=190 vs n=290). Split is clean by drug class: ABCB1 dominates efflux substrates, division rate dominates S-phase agents. Also 7/18 unique drugs, not 8/19 — `Docetaxel` was duplicated in my gene list.** | `results/lrp.json`, `results/lrp_mediate.json` |
| 21 | ~~The LRP chemoresistance biomarker has no mechanism~~ RESOLVED by #45 | Not the sink model, not a knockout-visible drug mechanism, not the persister state. Thirty-year association now harder to explain, not easier. Naming the gap precisely is the result. | `orcs_final.json`, `persister_primary.json` |
| 25 | **The vault is one assembly at the protein level** | PARP4 (r 0.82) and TEP1 (r 0.52) are MVP's top 2 partners of 10,924, in 13 cohorts, after 3-PC removal, and in 375 stroma-free cell lines. Gate recovers proteasome/complex I/ribosome from single seeds. RNA and evolution say "separate" because unassembled subunits are degraded — complex membership shows at protein level, not mRNA. | `results/prot_final.json` |
| 26 | **DOWNGRADED** — MVP's co-abundance neighbourhood is mostly shared regulation, not physical association | **My own pre-registered cross-test failed.** Against an independent anti-MVP IP-MS (1,205 proteins), only 12 of my top 100 are physical interactors vs 7.4 expected, hypergeom **p = 0.058** (threshold was 0.05); global Spearman **+0.019, p = 0.52**. Gate passed (MVP/PARP4/TEP1 all recovered). **What survives:** my ranks 1 and 2 are PARP4 and TEP1, both confirmed physically, and **ANXA2 (rank 12) and S100A10 (rank 65) are genuine vault interactors** (p 0.0024, 0.002). The method works; the wider module does not replicate as contact. | `results/crosstest.json` |
| 26b | Original claim, retained for the record | 50 of 101 significant GO terms pass specificity against 200 matched random proteins; generic actin terms do *not*. `PLASMA_MEMBRANE_REPAIR` (spec 0.010), `CAVEOLA`, `PLASMA_MEMBRANE_RAFT`, `ENDOCYTOSIS` (0.000), `RESPONSE_TO_MECHANICAL_STIMULUS` (0.005). Partners ANXA2, S100A10, EHD2/4, CAPN2/CAPNS1 — the canonical membrane-repair machinery, all off chr16. Converges with Pseudomonas/Listeria pore-forming toxins and the SPFH family. | `results/prot_enrichment_full.csv`, `_ccle.csv` |
| 27 | Inflammasome association (CASP1, CASP4, PYCARD) | **Partly compromised:** PYCARD sits 2 Mb from MVP on 16p11.2, so co-amplification may drive it; CASP1/CASP4 are chr11 and survive. Notable against an unverified report, which we could not independently source, that loaded vaults are immunogenic via NLRP3. Needs copy-number adjustment. | `results/prot_final.json` |
| 22 | MVP is dispensable but conserved | Two independent scales: across species (89.5th pct identity) and within humans (mis_z 2.5, LOEUF 0.92, pLI 0). Strange, specific, and unexplained. | `divergence.json`, `gnomad.json` |

---

## THE CORE THAT SURVIVES EVERYTHING (2026-11-07)

| # | Item | Status | Evidence |
|---|---|---|---|
| 40 | **CORRECTED: a three-protein core is ancient (MVP, PARP4, TEP1); ANXA2 is human-confirmed but the amoeba evidence is family-level** | A single *Dictyostelium* annexin (P24639) maps to all 13 human annexins via one orthogroup, so ANXA2/4/7/11 in my top 100 were **one observation counted four times** (verified in my own pipeline). PARP4 and TEP1 are 1-to-1 and stand (+3.49, +1.61, q<1e-4). ANXA2 remains a confirmed *human* physical interactor (§13) but the billion-year claim applies to the annexin family, not the paralog. Original entry: | Co-abundance across 13 human cohorts puts PARP4/TEP1/ANXA2 at ranks 1/3/7 (CNA-adjusted); physical anti-MVP IP-MS confirms all three; *Dictyostelium* proximity labelling finds all three vault-proximal (PARP4 +3.49, TEP1 +1.61, ANXA2 +0.64, all q<1e-4) across >1 Gyr. S100A10 joins at 3 of 3 where it exists. | `prot_final.json`, `crosstest.json`, `crossspecies.json` |
| 41 | ~~The broad membrane-repair neighbourhood~~ | **STRUCK by two independent tests.** Physical IP-MS p = 0.058; cross-species proximity p = 0.067. Both missed my pre-registered 0.05 and neither is rescued by the CNA-adjusted ranking (p = 0.20). The wide module was shared regulation; the narrow core is real. | `crosstest.json`, `crosstest_cna.json`, `crossspecies.json` |
| 43 | ~~DepMap continuous co-essentiality rescues what binary ORCS missed~~ | **Argon's H2a premise failed its own gate.** NDUFS2 recovers 25/25 complex I, but CAV1 does not recover CAVIN1 or EHD2 (it does get CAV2 at rank 2). So the method is not reliable for the non-essential complexes this question needs, and MVP's null is UNINFORMATIVE by pre-registration. | `results/coessentiality.json` |
| 44 | **The four-protein core has no fitness coupling** | MVP's strongest genome-wide co-essentiality is r = 0.205 against 17,915 genes; PARP4 ranks 9,020, TEP1 11,734, ANXA2 14,985. 2,886 genes pass q<0.05 purely from n = 1,178. The core travels and sits together but deleting MVP does not change the consequence of deleting them. Pre-registered kill condition fired, softened by the gate failure. | `results/coessentiality.json` |
| 42 | Method note: name-matching across species is invalid | My first cross-species run matched human symbols to *Dictyostelium* gene names (Arp2 = ARPB, Arp3 = ARPC, MVP = MVPB) and produced a meaningless 62/100 overlap. The pre-registered Arp2/3 gate caught it. Rebuilt via eggNOG orthology; gate then passed 5/8. | `src/crossspecies.py` |

## NEW FROM THE ARGON CHANNEL (2026-11-06 23:20)

| # | Item | Status | Evidence |
|---|---|---|---|
| 28 | **MVP's SPFH shoulder binds NAD+ / ADP-ribose** | **VERIFIED independently by both agents.** Two different alignments (my trimmed n=174 human-anchored; argon's untrimmed n=173), zero disagreement: F547, D566, F567, G569 all exactly **1.000** conserved across eukaryotes, K506 0.987. Shoulder 499-665 is the most conserved region (median 0.839 vs 0.787 whole protein); the PARP4-MINT patch is the least (0.708). Structures: PDB 9BW6 (Lodwick 2025), 11JB (Osinski 2026, endogenous ADP-ribose in native brain vaults, no added nucleotide). **This is a candidate answer to #18's "absorb what?": NAD+ / ADP-ribose.** | `results/divergence.json` + argon `test_a3_pocket_and_tep1.json` |
| 29 | ~~The CoA pocket of phage L05 is conserved in human vaults~~ | **STRUCK by argon's pre-registered kill condition** (45.2nd luminal percentile at repeats 1-2). The human ligand site is the SPFH shoulder, not the L05 locus. Supersedes #13. | argon Test A3A |
| 30 | **TEP1 is a TIR-family NAD(P)ase (catalytic E1008), autoinhibited at rest** | CLAIM from three 2026 primary papers; argon verified the texts, I have not read them. Reconstituted MVP+TEP1 vaults are catalytically active; E1008A is dead. BB-loop autoinhibition, activation requires oligomerisation. Steady-state NAD+ is flat in 370 CCLE lines (r +0.077), consistent with autoinhibition. | argon `raw/osinski_2026_tir_vault.txt` et al. |
| 31 | **PARP4 and TEP1 are orphan subunits stabilised by MVP** | Explains why RNA/evolution said "separate" while protein said "unit". Partial r(PARP4_prot, MVP_prot given PARP4_mRNA) = **+0.876**, R² 0.29 -> 0.84; TEP1 +0.681, R² 0.10 -> 0.52, n=371 CCLE. Not independently rerun by me. | argon Test H1 |
| 32 | **My kill condition for #26 was tested and NOT met** | Argon's 16p-euploid CCLE re-analysis drops PYCARD (+0.075), ALDOA (+0.159), SULT1A3 (+0.218), MAPK3 (+0.319) out of the top 100 while ANXA2 / CAPN2 / EHD2 / S100A10 all stay above +0.51. **#26 (membrane-repair neighbourhood) survives copy-number adjustment; #27 (inflammasome) correctly downgraded** since PYCARD was carrying it. | argon Test A4A |
| 39 | Argon's Tier-1 claim (PARP4 stations vaults at membrane-wounding sites) | **Weak support at best in my hands.** PARP4-dependence is not enriched among my top co-abundant interactors (2/12 = 16.7% vs 18.5% background). S100A10 does fall +2.11 -> -0.66 on PARP4 depletion as argon reported, but that has -log10 p = 1.21 (p ~ 0.062), **not significant** - the third time its framing has outrun its statistics while its raw numbers held. | `results/crosstest.json` |
| 33 | **JOINT HYPOTHESIS, untested anywhere: membrane breach is the trigger for vault NADase** | **SPECULATION**, but assembled from two independent lines that had not met. Argon VERIFIED that none of the three 2026 TEP1 papers tests membrane wounding, Ca2+ influx or pore-forming toxins, and Osinski states the activating signal is unknown. Meanwhile MVP-null mice die of *Pseudomonas* and the *Listeria* result both involve pore-forming toxins, and #26 puts MVP among ANXA2/S100A10/EHD2/EHD4/CAPN2. **A specific, falsifiable wet-lab experiment nobody has run.** | #26 + argon item 4 |
| 35 | ~~The vault's business end is the OUTER surface~~ | **STRUCK by my own test.** On the 78-mer, lumen-facing exposed residues are more conserved than outward-facing (0.722 vs 0.640; diff -0.081, CI -0.139 to -0.026; Spearman vs transmural offset -0.206, p 9.6e-5). Gate passed. Graham's instinct was reasonable and is wrong; the field's lumen-first focus had the right face. | `results/surface.json` |
| 36 | **The ADP-ribose pocket is embedded in the shell wall, not on either surface** | 78 AR6 copies in PDB 11JB all at abs(z) 171.7 A, r 134.6 A; shell there spans 120.4-161.9 A, so fractional depth 0.34 with 26% of protein mass radially inside the ligand. Refines the published "lumenal wall" wording: it is *in* the wall, a third out from the lumen face. | `results/pocket_geometry.json` |
| 34 | ~~The shoulder pocket is a transmural pore admitting cytosolic NAD+~~ | **STRUCK. Kill condition met on both limbs** (argon Test A5, pre-registered + sha256-locked before running): 36/36 AR6 heavy atoms strictly inside the local midsurface (mean dR -8.6 A), and exterior probe accessibility **0.00 A-squared** at both 1.4 A and 2.5 A radii, with max exterior channel radius 1.10 A - below water. Its geometry agrees with mine (AR6 r 129.1-140.3 A vs my median 134.6 A). It also caught a trap: a 1.60 A hinge-seam micro-cleft at |z| 155-167 A passes water/H+ and would fake a transmural result in an unsealed flood-fill, but blocks anything >=1.7 A. **Consequence: cytosolic NAD+ cannot cross the wall; substrate must enter when the particle opens.** | argon `test_003_pore_and_electrostatics.json` |
| 37 | **My 4V60 electrostatics would have been badly wrong** | Argon's holo comparison: shoulder lumenal net charge is +167.2 e in rat apo 4V60, +23.4 e in human apo 11JB, and **-132.6 e** in human holo (+78 AR6 at -2 each). A full sign reversal. My apo rat structure misrepresents the electrostatic environment, exactly as argon warned before I ran it. PARP4-MINT acts by steric masking, not monopole shift. | argon `electrostatics_profile_11jb_vs_4v60.csv` |
| 38 | Caution on argon's precision | Cross-checking its citation of **my** file: residues 548-558 dr "+14 to +26.6 A" matches mine exactly (+13.96 to +26.61). But it described that loop's conservation as "0.079-0.215" when my values run **0.079 to 0.738, mean 0.404** - it quoted the three lowest as the range. Real values, selectively framed. Also: my per-residue geometry puts pocket residues W545 (+1.8) and F547 (+7.8) on the *outward* side of the midsurface while its ligand atoms are all inward - consistent with a pocket that **straddles** the wall, which supports #36. | `results/surface_residues.csv` |
| 34b | Open: what opens the vault to admit substrate? | Published text says **lumenal** (Lodwick: "NAD+ ... bind the lumenal wall"; PARP4 docks the same lumenal face). Neither agent has verified it geometrically. Argon notes the Lodwick "keyhole" loop (R504-R511 / P565-K573) at the inter-chain seam raises the possibility of a **transmural shoulder pore** letting cytosolic NAD+ in without opening the waist. AR6 contacts 28 MVP residues incl. 499-524 and 565-569. Now closed by #34. Remaining question: Collins et al. showed pre-formed vaults admit AAV capsids via waist breathing, so if NAD+ also requires opening, **ligand access is gated by particle opening** - which gives the "deployed on demand" reading a physical mechanism. Untested. | `results/pocket_geometry.json` |

## PENDING

| # | Idea | Test | Status |
|---|---|---|---|
| 23 | MVP protein travels with TEP1/PARP4, or with anything | Co-abundance across ~10 CPTAC mass-spec cohorts; TEP1/PARP4 rank is the "is it a unit" question with an independent molecule | fetching |
| 24 | The business end is the **outside** surface, not the lumen | Per-residue conservation mapped onto the assembled particle (PDB 4V60); lumen-facing vs outward-facing exposed residues, buried residues excluded | pre-registered `86378cc` |

---

## TESTED SINCE (2026-11-07)

| # | Item | Status | Evidence |
|---|---|---|---|
| 54 | ~~MVP's tissue distribution tracks NAD metabolism~~ | **NOT NAD-LINKED.** 2 of 22 NAD genes in the top 200 (p = 0.031 but rule required k>=3). Gate passed hard (RPL7 -> 21/25 ribosomal). What the profile tracks instead is immunoglobulin/B-cell at 70/143 Ig genes — **plasma-cell content of gut tissue, i.e. composition, not partnership.** Does not touch the structural NAD evidence in #28. | `results/tissue_coexpr.json` |
| 52 | ~~Lung is the highest-vault tissue~~ | **FALSE.** Lung is rank 5 of 51 (120 nTPM). Top four: adrenal gland 176, colon 162, small intestine 157, duodenum 146. A claim repeated through all five articles and by me all day, unchecked. The LRP name came from lung-cancer drug resistance, not tissue ranking. Real pattern: adrenal + whole GI tract. | `results/tissue_expression.json` |
| 53 | ~~Pre-eclampsia: placenta is a high-vault tissue~~ | **STRUCK by its own pre-committed criterion** (article 5 experiment 8). Placenta is rank **38 of 51**, 36 nTPM vs adrenal 176. Dead on arrival, as Graham suspected. | `results/tissue_expression.json` |
| 50 | ~~Layer 3: vault RNA availability sets p62/autophagy capacity (tissue level)~~ | **NO EFFECT.** In Vaultrc5-knockout mouse liver with the deletion confirmed (log2FC -1.37, 0.1st pct), the 17-gene autophagy/p62 program shifts -0.058, p = 0.46; Sqstm1 itself -0.09. Deleting the RNA outright does not move the program it is supposed to gate. Brain inconclusive (Vaultrc5 undetected). **Bounds the tissue-level transcriptional consequence; mRNA cannot see p62 oligomerisation, which is what the model predicts.** | `results/vaultrc5_ko.json` |
| 51 | Method fault, twice today: script stricter than pre-registration | §19 (turnover) and §20 (Vaultrc5) both printed UNINFORMATIVE because the code demanded more than the written rule did - `both` gates where the text said "where measured" / "if present". Caught and corrected both times by reading the text back. Worth fixing by writing gate logic directly from the pre-registration sentence rather than from memory. | `results/turnover.json`, `results/vaultrc5_ko.json` |
| 47 | **PARP4 turns over 3x faster than MVP — STRENGTHENED on audit** | Holds in 4 of 4 human cell types (B cells 16.0<33.5<55.9; hepatocytes 19.4<25.9<29.4; monocytes 26.0<47.5<77.0; NK cells 38.2<100.6<**310.3**, an 8x gap). The cells are **non-dividing**, so these are pure proteolysis — the division-dilution caveat I listed does not apply. Two text errors corrected: the table is 4 human types + Mouse Neurons, not 5 human. Original entry: | Half-lives: MVP 66.4 h (58.6th pct), PARP4 22.2 h (**9.8th**), TEP1 40.6 h. Triplet spread 44.2 h = 29.9th percentile of random triplets -> NOT A UNIT BY TURNOVER. Constrains argon's orphan-subunit model: PARP4 is not stable only inside the cage. Fits Lodwick (PARP4 docks on the lumenal face) and my own finding that the PARP4-MINT patch is MVP's least-conserved region (0.708). **Picture: a durable shell with a fast-exchanging enzyme on its inner face.** | `results/turnover.json` |
| 48 | MVP is not structural furniture | 66 h half-life, 58.6th percentile — mid-pack, nowhere near lamins/histones at 1,500-1,700 h. At 100,000 copies/cell the population is continuously rebuilt. Born-loaded fork stays open; turnover does not settle it. | `results/turnover.json` |
| 49 | Method note: my script was stricter than my own pre-registration | Short-lived gate controls (MYC/FOS/JUN) are absent from pulse-SILAC data entirely. Written rule said "where measured" and "if neither direction separates"; the long direction passed at the 99.9th percentile. Script coded `both` and printed UNINFORMATIVE. Rule as written applied; discrepancy recorded. | `results/turnover.json` |
| 46 | ~~NSUN2/svRNAb represses CYP3A4 at tissue level~~ | **NO RELATION** in 366 human livers. Partial rho -0.052, p = 0.33, with gate passed (HNF4A +0.48, PXR +0.53). Specificity control inverts the story: the only nominal hit is CYP2E1 (-0.125), a non-target. **Limit: VTRNA1-1 is absent from mRNA data, so only the NSUN2 arm was testable.** Bounds the cell-line mechanism rather than refuting it. | `results/cyp3a4.json` |

## UNTESTED (from the five articles — nothing today touched these)

Lupus / Ro60 autoantigen asymmetry, with La as matched control · anti-MVP serology in banked SSA sera ·
Aicardi-Goutières and TREX1 · SAVI · pre-eclampsia and placental vault levels · cystic fibrosis
modifier genetics · C9orf72 repeat RNA in vaults · tauopathy / PSP loaded vaults · Paget's disease ·
svRNAb → CYP3A4 in human liver · mitoxantrone binding to vault RNA · vault delivery vehicles ·
Trap-and-Seq (the experiment that decides containment) · TEP1 binding misfolded RNA · progeria falsifier.

**Born-loaded is not absolute.** Collins et al., *ACS Synth Biol* 2026;15:3975 (`sb6c00512.pdf`, in this directory) mixed *pre-formed* empty human vaults with INT-conjugated AAV9 capsids and packaged intact virions into ~23.7% of them, 0% without INT. Polyribosome templating governs *de novo* shell synthesis, not a permanent lock on the lumen — assembled vaults breathe at the waist. This reopens the load-on-demand branch that Article 1 §6 had closed.

**Note on the Trap-and-Seq power argument:** at 100,000 vaults per cell, even 1% carrying a non-vtRNA
cargo gives ~1,000 molecules per cell — easily detectable by modern sequencing, invisible to 1986 gels
and a 2001 Northern blot. The cargo need only be rare *per particle*, which makes a clean negative there
genuinely decisive rather than dismissable.

---

## Method notes worth keeping

- **Pre-register, then gate.** Four of today's tests returned nulls; they only mean something because
  the method first recovered a known positive (cilia from IFT88, complex I from NDUFS2, proteasome,
  proliferation genes at the 99th pct). Where a gate failed — development, persister — the formal label
  is UNINFORMATIVE and is reported that way.
- **Percentiles, not effect sizes.** Global composition shifts move every gene; MVP's rank against the
  genome is the interpretable quantity.
- **Always exclude MVP from any gene set containing it.** `src/scores.py` asserts and aborts.
- **External audit, 2026-11-06 (`gemini-argon-audit.txt`).** Every claim I could independently check verified: the Moadab citation and its content; TCGA cohort duplication (1,084 / 594 / 585 shared patients); MVP's OG being 70.1% vertebrate (94/134, 0 fungi, 0 plants); the Collins PDF. It caught three real bugs in `src/prot_coabund.py` and a geometric flaw in `SURFACE_PREREGISTRATION.md`. Its weaker sections are the post-hoc causal stories (acinar-to-ductal metaplasia for the PAAD flip; dominant-negative assembly poisoning for mis_z vs pLI) — plausible, testable, but asserted rather than demonstrated.
- **Three pre-registered checks were never implemented** in `src/prot_coabund.py`: the 200 matched random queries, the 3-PC sensitivity, and the CCLE replication. Test #23 must not be run until they are, or it will not be the test that was registered.
- **A literature gap of mine:** `LEDGER.md` listed anti-MVP serology as UNTESTED when it had been published in 2023. I never searched for it.
- **Two mistakes made and corrected:** a control group ID guessed from memory (`KOG1691` is TMED10, not
  RPL7) and two results written as prose before being written as data (gnomAD, epigenetic). Both fixed.
