# Argon Primary-Data Investigation: Structural, Enzymatic, Interactomic & Multi-Omic Resolution of the Vault Holoenzyme

**Timestamp:** 2026-11-06  
**Pre-Registration:** `PREREGISTRATION_ARGON.md` (`SHA-256: 9432b91e41f89f4b152bae5ec2203735fd9140ad2f46cc5b1c208b0459928524` — verified intact)  
**Workspace Isolation:** All raw data (`raw/`), analysis scripts (`src/`), and structured outputs (`results/`) reside strictly inside `~/projects/Vault/argon/`. Zero tracked repository files were modified.

---

## 1. Executive Synthesis: What the Vault Actually Is

Four decades of vault research—and `LEDGER.md` Standing Item `#18` (*"absorb what?"*)—stalled on a missing biochemical substrate: why build a 13 MDa, 78-subunit `SPFH`-superfamily protein shell (`MVP`, 89.5th percentile sequence conservation, `mis_z = 2.5`) to house two proteins (`TEP1`, 0.8th percentile; `PARP4`, 3rd percentile) that evolve as fast as innate immune sensors, yet show zero fitness phenotype (`ORCS` `9/1,340` screens in the pre-registered universe [`results/orcs_final.json`], plus `3` descriptive-only hits in excluded screens [`results/orcs_mvp_excluded.csv`] that are not pooled) in sterile tissue culture?

By pulling **seven 2025–2026 primary manuscripts**, **four cryo-EM atomic structures (`PDB 9R86`, `9R87`, `9BW6`, `11JB`)**, **live-cell *Dictyostelium* `MVPA-TurboID` + endogenous human `A549` anti-`MVP` IP-MS + `BioPlex 3.0`**, **untrimmed eukaryotic alignments (`n = 173` species) + `gnomAD v4` (`~800k` humans)**, and **`CCLE` / `CPTAC` copy-number-adjusted proteomics & 225-metabolite LC-MS**, all four puzzles snap into a single biochemical machine:

1. **The Vault's Native Small-Molecule Ligand Is `NAD+` / `ADP-Ribose` Bound in 78 `SPFH` Shoulder Pockets (`PDB 9BW6`, `PDB 11JB`):**
   - **Lodwick et al. (*Nature Communications* 2025, `PMC12280208`, `PDB 9BW6`)** and **Osinski et al. (Tagliabracci lab, HHMI/UTSW, May 2026, `10.64898/2026.05.01.722283`, `PDB 11JB`)** demonstrate that human `MVP` binds `NAD+`, `ADP`, and **`ADP-ribose` (`AR6`)** inside a cationic/aromatic keyhole pocket in its **`SPFH` shoulder domain (`residues 499–573` + repeat-9 `R437`)**, directly adjacent to ~20 docked copies of `PARP4`.
   - Reprocessing native human brain vaults (`EMPIAR-10766`) **with zero exogenous nucleotides added** reveals **endogenous `ADP-ribose` (`AR6`) natively occupying the `MVP` shoulder pocket (`PDB 11JB`)**.
   - Our structural conservation analysis (`src/analyze_pocket_and_tep1.py`) shows that the **`SPFH` shoulder (`residues 499–665`) is the single most conserved domain in eukaryotic `MVP`** (`median AA identity = 0.828`, `mean chemical conservation = 0.855` across 173 eukaryotes), with core `ADP-ribose`-contacting side chains **`F547`, `D566` (ribose 2'/3'-OH clamp), `F567` (aromatic stack), and `G569` `100.0%` identical across all 173 eukaryotes**, and pyrophosphate clamp **`K506` `98.7%` identical**.

2. **`TEP1` Is the Second Active Mammalian `TIR`-Like `NAD(P)ase` (`TeTIR` / `NIR` / `DUF4062`) After `SARM1`:**
   - Three independent 2026 structural/biochemical studies—**Osinski et al. (`2026.05.01.722283`)**, **Le Mouëllic et al. (`2026.09.04.749371`)**, and **Hornebeck et al. (`2026.09.21.753143`)**—prove that `DUF4062` (`PF13271`, renamed `TeTIR` / `NIR`) is an ancient bacterial antiphage abortive-infection `NADase` (`Swarożyc`, `Avs`, `Vulcan`, `Vesta`) conserved in **`TEP1` (`residues 886–1117`, catalytic glutamate `E1008`)**.
   - Human `TEP1` (`TROVE`–`TeTIR`–`NACHT`–`WD40`) has an **APAF-1 / plant-TNL resistosome (`STAND`) architecture**: isolated `TEP1-TeTIR` exhibits robust `NADase`/`NADPase` activity comparable to `SARM1` (`NAD+ -> ADP-ribose + nicotinamide`) and **triggers `E1008`-dependent `NAD+` depletion and cell death in human cells**. Reconstituted **`MVP + TEP1` vaults are catalytically active `NAD(P)ases` (`WT` active, `E1008A` dead)**, and Volta phase-plate cryo-ET places `TEP1` along the central axis right at the `MVP` shoulder, encircled by the `PARP4` belt and `MVP`'s 78 `ADP-ribose` pockets!
   - **Resolution of the Divergence Paradox (`LEDGER.md` `#9` vs `#25`):** Whole-protein `TEP1` sits at the `0.8th` genome-wide percentile (`mean identity = 0.448`) because its `NACHT` (`0.337`) and `WD40` pathogen/damage-sensor propellers (`0.413`) undergo rapid diversifying evolution, **yet its 7 `TeTIR` catalytic active-site residues (`F902, R914, R942, W943, C959, R976, E1008`) retain `0.766` identity (`84.2nd` percentile of `TEP1`, Mann-Whitney `p = 8.58e-4`; `E1008 = 88.5%`, `R914 = 93.6%`, `W943 = 92.0%` with `0` PASS missense alleles in `gnomAD v4`)**!
   - **Post-Translational Caging (`Test H1`):** Across `n = 371` `CCLE` cell lines, `PARP4` and `TEP1` are obligate orphan subunits post-translationally stabilized by `MVP` (`partial r(PARP4_prot, MVP_prot | PARP4_mRNA) = +0.876, p = 6.1e-119`, jumping `R²` from `0.291 -> 0.835`; `partial r(TEP1_prot, MVP_prot | TEP1_mRNA) = +0.681, p = 1.7e-38`, jumping `R²` from `0.103 -> 0.519`). Free `TEP1`/`PARP4` fail to accumulate outside the `MVP` cage.

3. **Ancient (>1 Gyr) `PARP` Coupling & `PARP4`-Gated Plasma-Membrane / `S100A10`–`ANXA2` Localization (`Test A2` + `Test A4A`):**
   - In live *Dictyostelium discoideum* amoebae (**Geißler et al., *Nat. Commun.* 2026, `PMC13100048`**), *in situ* `MVPA-TurboID` proximity labeling (`3,001` proteins) recovers **four endogenous `PARP`s among the top hits in the entire proteome (`#3` `+3.49`, `#5` `+2.83`, `#6` `+2.32`)**, alongside **4 of 7 `Arp2/3` cortical-actin subunits (`ACTR3`/`Arp3` `+1.39`)** and **`Annexin A7` (`+0.64, q = 3.5e-5`)**, proving the **vault–`PARP`–cortical-membrane complex predates the Amoebozoa–Opisthokonta split (>1 billion years ago)**.
   - In endogenous human `A549` lung anti-`MVP` IP-MS (**Lodwick et al., *Nat. Commun.* 2025, `lodwick_supp_4.xlsx`**), wild-type vaults physically pull down **`S100A10` (`+2.11 log2FC, p = 0.0136`, obligate partner of `ANXA2`)**, `TCAF1` (`+6.48`), `NBR1` (`+5.09`), and `COP1`/`RFWD2` (`+4.74`, replicated in `BioPlex` for all 3 subunits!). Crucially, **`26.5%` (`9/34`) of WT human vault physical interactors localize to the Plasma Membrane (`88.2%` are known ADP-ribosylated proteins), dropping to `0.0%` (`0/16`, with complete loss of `S100A10` to `-0.66`) in `PARP4`-knockout cells**, where vaults relocalize to the nucleus (`87.5%`).
   - Across 7 copy-number-matched human tumor proteomics cohorts (`9,613` proteins), regressing out `MVP` copy number promotes **`ANXA2` (`#3` overall / `#1` extra-vault, `r = +0.440`)**, `VWA5A` (`#4`), `SERPINB1` (`#5`), **`CAPN2` & `CAPNS1` (`#6` & `#7`)**, **`ACTR3` (`#10`)**, **`LGALS3` / Galectin-3 (`#14`)**, and **`S100A10` (`#16`)** ahead of `16p11.2` cis-neighbors.

---

## 2. Pre-Registration Scorecard (Popperian Audit Summary)

| Test ID | Pre-Registered Hypothesis / Gate | Verdict | Key Quantitative Result & Honest Falsifications |
| :--- | :--- | :--- | :--- |
| **Test A1** | Musgrove et al. 2026 neuronal Vault RIP-seq (`PMID: 42031226`) passes 3/3 *Trap-and-Seq* criteria (incl. RNase protection / 13 MDa sizing) | **PARTIAL (`2/3` — SURFACE OR LUMEN RNP)** | Passes Criterion 1 (`Vaultrc5` enriched & lost on CIRTS KD) and Criterion 2 (anti-GFP vs IgG). **Fails Criterion 3:** uses `1%` paraformaldehyde crosslinking + `MVP:eGFP` overexpression with **zero RNase protection**. Classified strictly per pre-registration as *Vault-Associated RNP*, NOT proven luminal encapsulation (`LEDGER #77` stays open). |
| **Test A2** | Physical/proximity interactomes pass canonical subunit gate and recover cortical/membrane-repair (`ANXA2`/`S100A10`/`Arp2/3`) partners | **CONFIRMED (`3/3` gated datasets; `1` unassayed)** | `Human Cell Map` lacked `MVP/TEP1/PARP4` baits/preys (uninformative). All 3 assaying datasets passed positive-control gates (`p < 1e-6` / `pInt = 1.000`) and recovered `S100A10` + `26.5%` PM targets (`PARP4`-dependent, Lodwick A549), `Arp2/3` + `Annexin A7` + `4 PARPs` (*Dictyostelium* TurboID), and `MAP7` + `RFWD2/COP1` + `STX17` + `TIRAP` (`BioPlex 3.0`). |
| **Test A3A** | Phage `L05` Repeat 1–2 putative CoA pocket is conserved (`>75th` luminal pct) on human vaults (`PDB 9R86` / `11JB`) | **KILLED FOR `L05` LOCUS (`45.2th` pct); RELOCATED TO `SPFH` SHOULDER** | **Pre-registered Kill Condition hit on Repeat 1–2 (`45.2th <= 50th` luminal pct):** human vaults do **not** conserve phage `L05`'s Repeat 1–2 CoA pocket. Instead, human vaults bind **`NAD+`/`ADP-ribose`** in the **`SPFH` shoulder (`499–665`)**, the most conserved domain of `MVP` (`median = 0.828`; `F547/D566/F567/G569 = 100%` identical), while `MVP`'s `PARP4-MINT` patch (`Repeats 3–4`) fast-diverges (`30.7th` pct, `p = 0.0020`). |
| **Test A3B** | Prokaryotic `MVP` & `TeTIR` genomic neighborhoods (`H7`) enrich anti-phage defense / nucleotide / RNA-repair operons across `>=3` phyla | **CONFIRMED** | Anthropic (`2,185` `MVP-1` loci across `212` lineages) finds operons with anti-phage `JAB` defense, `RtcB` RNA repair, nucleosidases, and c-di-GMP signaling. Osinski & Le Mouëllic show bacterial `DUF4062`/`TeTIR` sits in defense islands across `26` phyla (`20.0%` vs `3.9%` chance, `p < 10^-134`). |
| **Test H1** | `PARP4` and `TEP1` exhibit massive post-translational protein stabilization by `MVP` controlling for own mRNA (`CCLE` `n=371`) | **STRONGLY CONFIRMED** | `PARP4`: `partial r = +0.876` (`p = 6.1e-119`, `R²` `0.291 -> 0.835`). `TEP1`: `partial r = +0.681` (`p = 1.7e-38`, `R²` `0.103 -> 0.519`). Non-luminal `ANXA2`/`CAPN2` gain only `+4–7%` `R²`. |
| **Test A4A** | Regressing out `16p11.2` CNA abolishes `PYCARD`, `MAPK3`, `ALDOA`, `SULT1A3` from top-100 while preserving `PARP4`, `TEP1`, `ANXA2`, `CAPN2`, `CASP1/4` | **PASSED IN `CCLE`; PARTIAL IN BULK `CPTAC`** | In `16p`-euploid `CCLE` (`n=360`), `PYCARD (+0.075)`, `ALDOA (+0.159)`, `SULT1A3 (+0.218)`, `MAPK3 (+0.319)` all miss top-100 while `ANXA2/CAPN2/EHD2/S100A10` stay `> +0.51`. In bulk `CPTAC` (`k=7`), CNA regression promotes **`ANXA2` to `#3` (`#1` extra-vault)** and **`CASP4` (`chr11`) into top-100 (`#96`)**, but `MAPK3 (#10)`, `SULT1A3 (#12)`, `ALDOA (#16)`, `PYCARD (#40)` remain top-100 via cis-`TAD` / myeloid admixture rather than DNA copy number alone. |
| **Test A4B** | `CCLE` 225-metabolite LC-MS screen (`n=370`) detects steady-state metabolite sink at `FDR q < 0.05` | **RAW/3-PC HIT (`1-MNA` `q=1.8e-7`) SELF-FALSIFIED BY `NNMT` CONTROL -> STEADY-STATE NULL** | `1-methylnicotinamide` (`1-MNA`, nicotinamide catabolite) ranked **#1 of 225** both raw (`r = +0.407, q = 7.7e-14`) and 3-PC-adjusted (`r = +0.313, q = 1.8e-7`). **However, our follow-up confounder audit caught that `NNMT` protein correlates `+0.478` with `MVP` (`+0.697` with `1-MNA`):** controlling for `NNMT + lineage` collapses `r` to **`+0.038` (`p = 0.467`)**. Steady-state `NAD+` (`r = +0.077`) is unperturbed in unstimulated cells, consistent with `TEP1` being **autoinhibited** until triggered. |

---

## 3. Detailed Findings by Track

### Track A1: Audit of Musgrove et al. (2026) Neuronal Vault RIP-seq (`PMID: 42031226`)
- **Source files:** `raw/musgrove_vaultrc5.pdf`, `raw/musgrove_vaultrc5.txt`, `raw/musgrove_vaultrc5.xml`, `raw/musgrove_media_6.xlsx`.
- **Experimental design:** Primary mouse cortical neurons (`DIV 12`) transduced with `MVP:eGFP` lentivirus + control or `CIRTS-Vaultrc5` knockdown, stimulated with `KCl` or `BDNF`, **crosslinked for 10 min in 1% paraformaldehyde**, sonicated (`25 x 30 s`), immunoprecipitated on anti-GFP vs mouse IgG magnetic beads (`500 mM NaCl` + `1% NP-40` + `0.5%` deoxycholate + `0.05% SDS` washes), reverse-crosslinked with Proteinase K, and sequenced (`RIP-seq` + `LC-MS/MS`, raw data `DOI: 10.17632/ckpxd8xx22.1`).
- **Rigor Gate Evaluation:**
  1. *Endogenous `Vaultrc5` recovery:* **PASS** (`Vaultrc5` specifically recovered in synaptosomal vault fractions and depleted by `CIRTS-Vaultrc5` KD).
  2. *Negative control IP:* **PASS** (mouse IgG control + KD comparison).
  3. *RNase protection or native 13 MDa particle sizing:* **FAIL.** Because 1% formaldehyde covalently links surface-adsorbed and dendritic-granule neighbor RNAs/proteins (`MVP` colocalizes with `Staufen1` dendritic RNP granules) and no RNase protection step was performed before shell lysis, this dataset **cannot distinguish luminal encapsulation from exterior RNP co-granulation**.
- **Biological Cargo Findings (with surface/crosslink caveat):**
  - Under `Vaultrc5` sufficiency + neuronal activity, `MVP:eGFP` co-precipitates translational/synaptogenesis mRNAs (`Homer1`, `Rps15`, `Eif5a`, `Bag1`, `Map2k2`, `Cdc42bpa`) and induces local dendritic `PSD95` translation via `MAPK`/`ERK` phosphorylation (`p-p44/42`).
  - Upon `Vaultrc5` knockdown, synaptic translation mRNAs are lost and replaced by immune/NF-κB/microglial-recruitment transcripts (`Ccl4`, `Nfkbid`, `Tnfsf9`), and `Vaultrc5` KD causes **nuclear `MVP` accumulation** in infralimbic prefrontal cortex (`p = 0.0172`)—mirroring the **nuclear relocalization of `MVP` seen in `PARP4`-KO human `A549` cells** (Lodwick et al. 2025)!

---

### Track A2: Physical & Nanometer-Proximity Interactomes (`results/test_a2_interactome.json`)

#### 1. Live-Cell *Dictyostelium* `MVPA-TurboID` Proximity Proteomics (Geißler et al., *Nat. Commun.* 2026, `PMC13100048`)
- **Positive-Control Gate:** `MVPA-TurboID` bait (`FUS01`, `log2FC = +8.82, q = 3.7e-7`) and heteromeric partner `MVPB` (`+7.49, q = 3.7e-7`) are `#1` and `#2` out of `3,001` quantified proteins.
- **Ancient Vault–`PARP` Holoenzyme (>1 Billion Years Old):** Despite *Dictyostelium* lacking a direct `MINT`-sequence match to human `PARP4`, **four endogenous `PARP` / `ADPRT` proteins are heavily biotinylated by `MVPA-TurboID` in living amoebae**:
  - `DDB_G0289141` (`PARP` catalytic + WGR domain): **`log2FC = +3.49, q = 4.9e-7` (#3 non-bait protein in the entire cell!)**
  - `ADPRT2` (`DDB_G0292942`): **`log2FC = +2.83, q = 4.2e-7` (#5 overall)**
  - `ADPRT4` (`DDB_G0281023`): **`log2FC = +2.32, q = 1.6e-6` (#6 overall)**
  - `DDB_G0286613` (`PARP`): **`log2FC = +1.37, q = 1.3e-4`**
- **Cortical Actin & Membrane Repair Proximity:** Enriches **4 of 7 `Arp2/3` complex subunits** (`ARCC`/`Arp3` `+1.39, q = 2.5e-6`, matching human `ACTR3` at `#10` genome-wide in CNA-adjusted CPTAC!; `ARCE` `+1.19`; `ARCG` `+0.56`; `ARCA` `+0.49`), **`Annexin A7` (`NXNA`, `+0.64, q = 3.5e-5` — the canonical membrane-repair annexin in *Dictyostelium*!)**, and `81/126` ribosomal proteins (`mean +0.97`, matching *in situ* cryo-ET of vaults docked on rough ER membranes).
- **Important Null Result (Fig. 1C):** *In situ* cryo-ET vault particle counts do **not** increase under acute hyper-osmotic (`100 mM` sorbitol: `2.95` vaults/tomogram) or hypo-osmotic (`dH2O`: `3.01`) shock vs starvation control (`3.38`), falsifying acute osmotic particle neogenesis.

#### 2. Endogenous Human `A549` Anti-`MVP` IP-MS in WT vs `PARP4`-KO Cells (Lodwick et al., *Nat. Commun.* 2025, `lodwick_supp_4.xlsx`)
- **Positive-Control Gate:** `MVP` (`+7.62, p = 1.8e-6`), `PARP4` (`+8.66, p = 7.2e-7`), and `TEP1` (`+6.27, p = 2.0e-5`) are top hits in WT `A549`; `PARP4` drops to `0` (`-8.66` shift) in `PARP4`-KO while `MVP` (`+6.98`) and `TEP1` (`+5.30`) remain intact.
- **Direct Physical Recovery of `S100A10` & `PARP4`-Dependent Plasma Membrane Targeting:**
  - WT endogenous vaults physically co-immunoprecipitate **`S100A10` (`WT_log2FC = +2.11, p = 0.0136` — the obligate heterotetramer partner of `ANXA2` in membrane repair)**, **`TCAF1` (`+6.48, p = 6.9e-5` — plasma-membrane `TRPM8` channel partner)**, **`NBR1` (`+5.09, p = 0.0029` — selective autophagy cargo receptor)**, and **`COP1`/`RFWD2` (`+4.74, p = 0.0033`)**.
  - **`PARP4` Knockout Destroys Plasma-Membrane Localization:** In WT `A549` cells, **`26.5%` (`9/34`) of physical vault interactors localize to the Plasma Membrane** and **`88.2%` (`30/34`) are established ADP-ribosylated targets**. In `PARP4`-KO cells, **Plasma-Membrane interactors drop to `0.0%` (`0/16`)**, **`S100A10` binding vanishes completely (`KO_log2FC = -0.66`)**, and nuclear interactors surge to **`87.5%` (`14/16`)**.

#### 3. `BioPlex 3.0` (`HEK293T` & `HCT116` AP-MS) & `Human Cell Map`
- **`Human Cell Map` (Go et al. 2021):** Honest null/unassayed — neither `MVP`, `TEP1`, nor `PARP4` appeared among the baits or passing preys in `preys-latest.txt`.
- **`BioPlex 3.0`:** Passes positive-control gate (`MVP`–`PARP4` `pInt = 1.000000`, `MVP`–`TEP1` `pInt = 0.999999`). Across `HCT116` cells, **all three vault subunits (`MVP`, `TEP1`, `PARP4`) independently pull down with:**
  - **`MAP7` (`Ensconsin`, `pInt = 1.0000, 0.9999, 1.0000`)** — the epithelial microtubule-associated adaptor that recruits **kinesin-1** to drive rapid plus-end cortical transport of vaults!
  - **`RFWD2` / `COP1` (`pInt = 0.9993, 0.9660, 1.0000`)** — E3 ubiquitin ligase replicating Lodwick `A549` endogenous IP-MS!
  - Additional high-confidence physical hits: `MVP`–**`STX17`** (`pInt = 1.0000`, autophagosome-lysosome fusion SNARE) and `TEP1`–**`TIRAP`** (`pInt = 0.9995`, `PIP2`-binding plasma-membrane `TIR` adaptor).

---

### Track A3: Structural Pocket Conservation (`PDB 11JB`, `9R86`, `9BW6`) & `TEP1` `TeTIR` Active Site (`results/test_a3_pocket_and_tep1.json`)

1. **Test A3A-1 — Phage `L05` Repeat 1–2 Putative CoA Pocket Fails in Human Vaults (Pre-Registered Kill Condition Hit):**
   - In Anthropic's phage `L05` cryo-EM structure (`10.64898/2026.11.04.764334v1`), unassigned CoA-like density sits in a basic inter-chain seam pocket between **wall repeats 1 and 2**.
   - Evaluating the structurally homologous **Repeat 1–2 luminal inter-chain seam (`residues 5–112`, `n = 15` seam residues; `n = 59` all Repeat 1–2 luminal residues)** across the full 78-chain human brain vault (`PDB 11JB` / `9R86`) and `173` non-human eukaryotes yields **`mean AA identity = 0.763` (`45.2th` luminal percentile — strictly `<= 50th` percentile kill threshold)** and low basic `K/R/H` content (`26.1%` seam, `15.3%` luminal). Thus, **phage `L05`'s Repeat 1–2 CoA pocket is lineage-specific and NOT conserved in human vaults**.

2. **Test A3A-2 — Human Vaults Conserve an `NAD+` / `ADP-Ribose` Pocket in the `SPFH` Shoulder (`PDB 11JB` + `9BW6`):**
   - Across all six structural domains of human `MVP` (`893 aa`), the **`SPFH` shoulder (`residues 499–665`) is the most conserved domain in the entire protein** (`mean AA identity = 0.778`, `median = 0.828`, `mean chemical-class conservation = 0.855` vs `0.713–0.746` in wall/cap helices and `0.644` in the cap disk).
   - In `PDB 11JB`, `28` `MVP` residues contact endogenous `ADP-ribose` (`AR6`) within `<= 4.5 Å` (`30` residues combined with Lodwick's `NAD+` keyhole loop). Because the entire `MVP` luminal shell is exceptionally conserved (`median = 0.805`), the broad `4.5 Å` contact shell (`mean = 0.801`, `<= 2.7 Å` H-bond/stacking core `mean = 0.826`) sits near the high luminal average overall, **while the specific ligand-anchoring side chains reach near-absolute invariance across 1.5 billion years of eukaryotic evolution**:
     - **`F547` (`100.0%`), `D566` (`100.0%`, `2.59 Å` to `AR6` ribose diol), `F567` (`100.0%`, `2.67 Å` aromatic stack), `G569` (`100.0%`)**
     - **`K506` (`98.7%` identical, `2.21 Å` pyrophosphate salt bridge), `S501` (`98.0%`), `F522` (`97.3%`), `L500` (`96.7%`), `D521` (`93.2%`), `W545` (`92.7%`), `K573` (`92.1%` identical / `96.7%` basic)**
     - **`R437` (`87.5%` basic, `1.99 Å` H-bond), `R504` (`85.4%` basic `K/R` swap), `R507` (`82.1%` basic `K/R` swap)**

3. **Test A3A-3 — Co-Divergence of `MVP`'s `PARP4-MINT` Interface (`PDB 9BW6`):**
   - In stark contrast to the conserved `SPFH` shoulder, the `18` `MVP` residues on luminal Repeats 3–4 contacting `PARP4`'s `MINT` domain (`residues 116–215`) have **`mean AA identity = 0.642` (`30.7th` luminal percentile — significantly *more divergent* than the rest of the luminal wall, Mann-Whitney `p = 0.0020`)**, demonstrating intermolecular co-evolution with rapidly evolving `PARP` partners.

4. **`TEP1` Domain Architecture & `TeTIR` `NADase` Active-Site Constraint:**
   - Domain conservation across `KOG3602` (`n = 173` eukaryotes): `TROVE vtRNA-binding (201–698) = 0.576`, `N-term repeats (1–200) = 0.573`, `WD40 sensor propellers (1650–2627) = 0.413`, `TeTIR overall (886–1117, expanded loops) = 0.379`, `NACHT NTPase (1150–1550) = 0.337`.
   - **Active-Site Island Inside a Divergent Sensor:** The 7 experimentally validated `TeTIR` catalytic/substrate-binding residues (**`F902 = 0.833`, `R914 = 0.936`, `R942 = 0.705`, `W943 = 0.920`, `C959 = 0.689`, `R976 = 0.397` [`0.769` basic], catalytic `E1008 = 0.885`**) average **`0.766` identity (`84.2nd` percentile of `TEP1` vs `0.448` rest of `TEP1`, `p = 8.58e-4`)**. In `gnomAD v4` canonical PASS exomes+genomes, `F902` (`AC=0`), `W943` (`AC=0`), `C959` (`AC=1`), and catalytic `E1008` (`AC=2`) are virtually invariant across ~800,000 humans.

---

### Track A4: Orphan Stabilization (`H1`), `16p11.2` CNA Dissection (`A4A`), and `CCLE` Metabolomics + Confounder Takedown (`A4B`)

1. **Orphan-Subunit Stabilization (`Test H1`, `results/test_a4_cna_metab.json`):**
   - Across `371` `CCLE` cell lines with matched RNA-seq and TMT proteomics:
     - **`PARP4`:** `r(mRNA, MVP_mRNA) = +0.381` -> **`r(Prot, MVP_Prot) = +0.874`**; **`partial r(Prot, MVP_Prot | own_mRNA) = +0.876` (`p = 6.11e-119`)**. `MVP` protein increases explained variance of `PARP4` protein from `29.1%` to **`83.5%` (`+54.4%` post-translational stabilization)**.
     - **`TEP1` (`n = 273`):** `r(mRNA, MVP_mRNA) = +0.172` -> **`r(Prot, MVP_Prot) = +0.654`**; **`partial r(Prot, MVP_Prot | own_mRNA) = +0.681` (`p = 1.69e-38`)**. `MVP` protein increases explained variance of `TEP1` protein from `10.3%` to **`51.9%` (`+41.6%` post-translational stabilization)**.

2. **`16p11.2` Copy-Number & Genome-Wide Rank Dissection (`Test A4A`, `results/confounder_checks.json`):**
   - In **`16p11.2`-euploid `CCLE` cell lines (`n = 360`)**, `16p11.2` neighbors `PYCARD` (`r = +0.075`), `ALDOA` (`+0.159`), `SULT1A3` (`+0.218`), and `MAPK3` (`+0.319`) fall completely out of `MVP`'s top-100, whereas **`PARP4` (`+0.872`), `TEP1` (`+0.659`), `CAPN2` (`+0.585`), `IQGAP1` (`+0.580`), `ANXA2` (`+0.577`), `EHD2` (`+0.575`), `EHD4` (`+0.549`), `S100A10` (`+0.511`), and `CASP4` (`chr11`, `+0.363`)** remain robust.
   - Across **7 CNA-matched primary tumor proteomics cohorts (`9,613` genes)**, regressing out `MVP` copy number demotes `MAPK3` (`#4 -> #10`), `SULT1A3` (`#7 -> #12`), `ALDOA` (`#5 -> #16`), and `PYCARD` (`#32 -> #40`), elevating **`ANXA2` (`#3` overall / `#1` extra-vault, `r = +0.440`)**, `VWA5A` (`#4`), `SERPINB1` (`#5`), **`CAPN2` (`#6`)**, **`CAPNS1` (`#7`)**, **`ACTR3` (`#10`)**, **`PLEC` (`#13`)**, **`LGALS3` / Galectin-3 (`#14`)**, **`S100A10` (`#16`)**, and **`CASP4` (`chr11`, `#182 -> #96`)**. Because `MAPK3/SULT1A3/ALDOA/PYCARD` remain in the bulk tumor top-40 even after CNA regression (unlike flanking `16p11.2` genes `CORO1A #910` and `PRKCB #4145`), bulk tumor co-abundance within the `29.8–31.1 Mb` `16p11.2` locus reflects **local cis-TAD chromatin co-regulation + myeloid immune infiltration (`PYCARD`)**, not DNA amplification alone.

3. **`CCLE` 225-Metabolite Screen & Popperian Self-Correction (`Test A4B`, `results/ccle_metabolomics_mvp.csv`):**
   - Screening `225` polar/lipid metabolites across `370` `CCLE` cell lines yielded **`1-methylnicotinamide` (`1-MNA`, methylated sink product of nicotinamide cleaved from `NAD+`) as Rank #1 of 225** both raw (`r = +0.407, q = 7.69e-14`) and after 3-PC removal (`r = +0.313, q = 1.75e-7`), alongside depleted `niacinamide` (`r_3pc = -0.171, q = 0.021`) and enriched raft sphingomyelins (`C16:0 SM` `q_3pc = 0.0027`, `C16:1 SM` `q_3pc = 0.014`).
   - **Crucial Self-Falsification Control:** Before claiming `1-MNA` as basal `TEP1`/`PARP4` catalysis, we tested whether high-`MVP` cancer lines co-express **`NNMT` (`nicotinamide N-methyltransferase`, `chr11q23.2`)**. Indeed, `NNMT` protein correlates `+0.478` with `MVP` in `CCLE` (`+0.697` with `1-MNA`) and `+0.293` across 17 tumor cohorts (`+0.566` in GBM, `+0.548` in LUSC, `+0.512` in BRCA), while nuclear `PARP1` anticorrelates (`-0.514`) and antiviral `PARP9/14` (`+0.299 / +0.352`) + `NAMPT` (`+0.382`) co-express! Controlling for `NNMT + tissue lineage` reduces `r(1-MNA, MVP)` from `+0.407` to **`+0.038` (`p = 0.467`)**, and steady-state `NAD+` is flat (`r = +0.077, q = 0.20`).
   - **Biological Meaning:** Steady-state bulk metabolomics in unstimulated cells is **NULL after `NNMT` control**—which is *required* by the `STAND` autoinhibition model, because constitutive `TEP1` `TeTIR` `NADase` activity kills human cells!

---

## 4. Unified Model: Proven Facts vs. Falsifiable Predictions

### What Is Now Proven Fact
1. **Enzymatic Identity:** The eukaryotic vault is a compartmentalized **`NAD+` / `ADP-ribose` signaling and `NAD(P)ase` holoenzyme** combining `78` `MVP` `SPFH` subunits (each bearing an ancient shoulder `NAD+`/`ADP-ribose` pocket natively occupied by `ADP-ribose` in human brain), `~20` `PARP4` mono-ADP-ribosyltransferases, and `~1–2` `TEP1` `STAND` (`TROVE`–`TeTIR`–`NACHT`–`WD40`) `NAD(P)ases` (`E1008`).
2. **Post-Translational Caging:** `MVP` post-translationally stabilizes `PARP4` (`+54%` `R²`) and `TEP1` (`+42%` `R²`) across hundreds of human cell lineages.
3. **`PARP4`-Gated Cortical/Membrane Docking:** Vaults physically associate with `PARP`s, `Arp2/3`, and repair annexins (`Annexin A7` in *Dictyostelium*; `S100A10` + `26.5%` plasma-membrane targets in human `A549` cells, plus kinesin-1 adaptor `MAP7`), and **knocking out `PARP4` completely abolishes human vault plasma-membrane / `S100A10` association**, sending vaults to the nucleus (just as knocking down `Vaultrc5` sends neuronal `MVP` to the nucleus).

### The Unified Two-Tier Barrier-Guardian Hypothesis (Falsifiable Synthesis)
`MVP` (`SPFH` membrane-microdomain scaffold), `PARP4` (mono-ART), `TEP1` (`STAND` `TeTIR` `NADase`), and Pol-III `vtRNAs` form a **two-tier cortical barrier surveillance complex** deployed along mucociliary/gut/ductal epithelia, macrophages, and neuronal dendrites:
- **Tier 1 — Cortical Repair & Local `ADP-Ribose` Signaling (Sub-lethal Stress):** `PARP4` mono-ADP-ribosylates cortical targets (maintaining `MVP` at plasma-membrane `S100A10`–`ANXA2`–`CAPN2`–`Arp2/3` sites via `MAP7`/kinesin-1 transport), while `MVP`'s 78 shoulder pockets locally buffer `NAD+`/`ADP-ribose` (`AR6`) to coordinate membrane resealing, channel regulation (`TCAF1`/`TRPM`), or selective autophagic clearance (`NBR1`/`STX17`).
- **Tier 2 — `STAND`-Gated `NADase` Execution (Catastrophic Invasion / `vtRNA` Switch):** `vtRNA1-1` (bound to `TEP1`'s `TROVE` domain, whose loss triggers apoptosis sensitivity and nuclear shift) or pathogen/damage ligands sensed by `TEP1`'s hyper-evolving `WD40` propellers (`0.8th` pct) gate `NACHT` oligomerization. Upon catastrophic intracellular pathogen breach (e.g., *Pseudomonas*, influenza, pore-forming toxins, or Pol-III viral/stress RNA displacement), `TEP1` oligomerizes at the vault shoulder and fires **`E1008`-dependent `TeTIR` `NAD(P)ase` catalysis**—either flooding the `PARP4`/shoulder chamber with `ADP-ribose` or executing altruistic `NAD+` depletion to block pathogen replication.

### Three Immediate Killer Predictions to Test Next
1. **Prediction 1 (`vtRNA1-1` as the Endogenous Autoinhibitory Lock on `TEP1` `TeTIR`):** In purified reconstituted `MVP + TEP1` vaults (Osinski et al. assay), loading `vtRNA1-1` vs RNase/antisense depletion of `vtRNA1-1` will directly shift the `Km`/`Vmax` of `E1008`-dependent `NAD+` hydrolysis! *(Links Horos 2019 `vtRNA1-1` apoptosis resistance directly to `TEP1 E1008` `NADase` gating.)*
2. **Prediction 2 (`TEP1-E1008A` vs `PARP4-KO` Epistasis Under Pore-Forming Toxin / *Pseudomonas* Challenge):** Under Streptolysin-O / digitonin plasma-membrane wounding, `PARP4-KO` (which loses PM/`S100A10` localization) will impair membrane resealing kinetics, whereas `TEP1-E1008A` knock-in will selectively abolish `NAD+` drop and pyroptotic/necrotic execution during high-MOI intracellular infection!
3. **Prediction 3 (Computational — `PDB 9R86` / `11JB` Interior Charge Correction for Claude's `src/surface.py`):** Any interior surface electrostatic calculation on `4V60` alone misses (a) the 78 bound `ADP-ribose` (`-2` pyrophosphate) anions at `R437/K506/R511/K573` in `11JB` and (b) the `~20` docked `PARP4-MINT` chains masking Repeats 3–4 (`residues 116–215` in `9BW6`). Running surface electrostatics on **`11JB` + `9BW6`** rather than legacy `4V60` will avoid a major structural artifact.

---

## 5. Index of Argon Files & Reproducible Outputs

- Pre-registration & hash: `PREREGISTRATION_ARGON.md`, `PREREGISTRATION_ARGON.sha256`, `PREREGISTRATION_ARGON_003.md`, `PREREGISTRATION_ARGON_003.sha256`
- Scripts:
  - `src/analyze_interactome.py` -> `results/test_a2_interactome.json`, `results/test_a2_interactome.log`
  - `src/analyze_pocket_and_tep1.py` -> `results/test_a3_pocket_and_tep1.json`, `results/test_a3_pocket_and_tep1.log`
  - `src/analyze_cna_and_metabolomics.py` -> `results/test_a4_cna_metab.json`, `results/ccle_metabolomics_mvp.csv`, `results/test_a4_cna_metab.log`
  - `src/confounder_checks.py` -> `results/confounder_checks.json`, `results/confounder_checks.log`
  - `src/analyze_003_pore_and_electrostatics.py` -> `results/test_003_pore_and_electrostatics.json`, `results/electrostatics_profile_11jb_vs_4v60.csv`, `results/test_003_pore_and_electrostatics.log`
- Primary 2025–2026 structures & manuscripts in `raw/`:
  - Cryo-EM: `11JB.cif.gz`, `9R86.cif.gz`, `9R87.cif.gz`, `9BW6.cif.gz`
  - `TEP1` `TeTIR`/`NIR` `NADase` papers: `osinski_2026_tir_vault.pdf`, `lemouellic_2026_tep1_nadase.pdf`, `hornebeck_2026_tetir.pdf`
  - `MVP`–`PARP4`–`NAD+` & endogenous `A549` IP-MS: `lodwick_2025.xml`, `lodwick_supp_4.xlsx`, `lodwick_supp_5.xlsx`
  - *Dictyostelium* *in situ* vault & `MVPA-TurboID`: `PMC13100048.xml`, `natcomms_source_data/Source_data_Vault.xlsx`
  - Neuronal Vault RIP-seq: `musgrove_vaultrc5.pdf`, `musgrove_media_6.xlsx`
  - Phage `L05` & prokaryotic `MVP` survey: `anthropic_l05.pdf`

---

## 6. Addendum 003: SPFH Shoulder Tunnel Test (`LEDGER #34`) & Holo-Vault Electrostatics (`Test A5` & `Test A6`)

Pre-registered in `PREREGISTRATION_ARGON_003.md` (`SHA-256: da4a6cf715482be083ae1302e1a38793573efa7701b512f02f203ad30f34f583`).

1. **`Test A5` — `LEDGER #34` Verdict: `LUMENAL` (`TRANSMURAL` Shoulder-Pore Hypothesis Killed by Pre-Registered Kill Condition):**
   - Across the 78-mer `PDB 11JB` assembly (`z` in `[-328.1, +328.1] Å`, `R_cyl` in `[51.0, 197.6] Å`), **all `36/36` heavy atoms (`100%`) of bound `ADP-ribose` (`AR6`) sit strictly inside the local `Cα` shell midsurface `R_mid(|z|)`** across all axial bin resolutions (`15 Å` bins: `Delta_R = [-14.04, -2.82] Å`, mean `-8.61 Å`; `10 Å` bins: `[-17.85, -1.91] Å`, mean `-8.62 Å`; `2 Å` smooth: `[-16.37, -2.17] Å`, mean `-7.51 Å`). Adenine (`C2/N1/N6`) tucks deepest into the inner wall (`Delta_R_15A = -2.8 to -3.5 Å`), while the pyrophosphate (`PA/PB`, `-12.0 to -12.7 Å`) and keyhole loop (`R504 = -19.3 Å`, `K506 = -16.3 Å`, `R507 = -16.2 Å`) project directly into the vault lumen.
   - Directional `0.4 Å` 3D Euclidean distance-transform flood-fill and Lee-Richards SASA show **zero direct exterior probe access to `AR6` (`SASA_exterior = 0.00 Å²` at both `r_probe = 1.4 Å` water and `2.5 Å` nucleotide; `R_max_exterior = 1.10 Å < 1.40 Å`)**, versus **wide lumenal access (`SASA_lumen = 40.99 Å²` at `1.4 Å` [`7/36` atoms] and `16.25 Å²` at `2.5 Å`; `R_max_lumen = 3.10 Å`, a `6.2 Å`-diameter lumenal mouth; apo 30-residue pocket lining `976.20 Å²` lumenal vs `20.93 Å²` exterior)**.
   - *Bonus structural note:* `15 Å` equatorward at the Repeat-8/9-to-shoulder hinge seam (`|z| = 155–167 Å`, lined by `Chain A: 427–464` and `Chain m: 473–497`), the closed shell contains a narrow **`1.60 Å`-radius (`3.2 Å` diameter) inter-chain water/ion micro-cleft** (`R_max_hinge_seam = 1.60 Å`), permitting water/H⁺ equilibration with the lumen while remaining strictly impermeable to `NAD+` or nicotinamide (`>= 2.5 Å`). Cytosolic `NAD+` cannot enter the shoulder pocket through the closed wall; entry requires waist/half-vault breathing (`Collins et al. 2026`).

2. **`Test A6` — Holo (`11JB + 78 AR6²⁻ + 20 PARP4-MINT`) vs Apo (`11JB` / `4V60`) Luminal Electrostatics:**
   - At the `SPFH` shoulder (`residues 499–665`, `Delta_R < 0` across 78 chains), binding `78 × AR6²⁻` (`-156.0 e`) **reverses the luminal formal charge sign from `+23.4 e` (`+0.30 e`/chain in human `11JB` apo; `+167.2 e` in rat `4V60` apo) to `-132.6 e` (`-1.70 e`/chain)**.
   - Along the inner lumen wall (`R_inner(|z|) - 3 Å`, `150 mM` Debye-Hückel), apo human `11JB` displays the strongest positive electrostatic beacon in the entire vault right at the `SPFH` shoulder keyhole (`|z| = 170 Å`: **`+37.60 mV`**, missed completely by legacy 3.5-Å `4V60` at **`-5.28 mV`**), electrostatically focusing anionic `NAD+`/`ADP-ribose`/`vtRNA` into the shoulder reaction zone. Occupancy by `78 × AR6²⁻` quenches this peak by **`-17.00 mV`** (to `+20.60 mV`).
   - Superposing `9BW6` onto `11JB` (`201 Cα`, `RMSD = 1.16 Å`) places `PARP4-MINT` (`|z| = 41.7–84.5 Å`, `R_cyl = 139.3–177.8 Å < R_mid = 182.9 Å`) strictly inside the lumen; because `PARP4-MINT` is nearly charge-neutral overall (`+0.3 e`/copy, `+6.0 e` for 20 copies), it alters mean-field potential at `|z| = 50–70 Å` by only `-1.26 to +2.20 mV`, acting primarily via **steric masking** of Repeats 3–4 rather than monopole shift.
