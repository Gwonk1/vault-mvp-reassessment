# Pre-registration: what is lost when MVP is lost? (evolutionary co-loss)

**Date:** 2026-11-06. Drafted by Claude at Graham's request. Graham stated no numeric predictions.
**Already seen before freezing:** MVP's own presence/absence per clade (to validate against literature), and which
OGs hold MVP, TEP1, PARP4 and IFT88. **Not seen:** any gene's co-loss score against MVP.

## Question
Across eukaryotes, which gene families are independently lost in the same lineages as MVP, more specifically than
chance, and do they form a recognizable biological module?

## Prior
No pathway is predicted. Expected outcome: no specific module, since few independent losses are available and the
ortholog groups are coarse. **Cilia is a named confound:** fungi and flowering plants lost cilia too, so a cilium
hit is suspect unless it passes the specificity test below.

## Data
eggNOG 5.0 eukaryote-level (2759) orthologous groups, 477 species; NCBI taxonomy as the tree, without branch lengths.
Species with fewer than 2,500 OGs are dropped as incomplete or extremely reduced.

## Method (`src/coloss.py`)
**Loss event:** for each OG, walk down from the lowest node holding at least 90% of its presences. An event is a
maximal clade of at least 2 species with presence at or below 10%. Single-species absences are ignored as likely
assembly gaps. Events are counted once however many species they contain, so a 179-species clade counts as 1.

**Score for gene g against query q:** co / (co + q_only + g_only), where
- co = q's events in which g is also absent (≤10%) and retained (≥50%) in the sister species,
- q_only = q's events without that,
- g_only = g's events inside which q is mostly present (>50%).
Rank by score, ties by higher co, then lower g_only.

**Module test:** top 100 OGs with a human member (one count per OG), hypergeometric against all scored OGs with a
human member, MSigDB 2024.1 GO BP and CC (10 to 500 OGs in universe), Benjamini-Hochberg.

**Specificity:** 200 random query OGs matched on event count (±1) and presence fraction (±0.10). For each term hit by
MVP, the fraction of matched queries also hitting that term at q < 0.05.

## Labels
- **MODULE LEAD:** at least one GO term with q < 0.05 hit by fewer than 5% of matched queries.
- **NON-SPECIFIC:** terms pass q < 0.05, but none pass specificity. Reads as a shared pattern of big ancient losses.
- **NO MODULE:** no term passes q < 0.05.

The top-ranked genes are reported in every case as hypotheses and never as findings.

## Gates, evaluated before reading MVP
IFT88 must recover GOCC_INTRACILIARY_TRANSPORT_PARTICLE or GOCC_CILIUM at q < 0.05. NDUFS2 must recover
GOCC_NADH_DEHYDROGENASE_COMPLEX or GOCC_RESPIRASOME at q < 0.05. If either fails, the pipeline is reported as
unable to detect real modules, and a NO MODULE result for MVP is uninformative.

## Partners
TEP1 and PARP4 ranks are reported. **PARP4 is uninformative by construction**, because its OG also holds PARP1, 2
and 3. TEP1's OG holds NWD1 and NWD2, so its rank is weak evidence in either direction.

## What each result would mean
- **MODULE LEAD:** a specific pathway to bring to someone with a lab. It shows evolutionary association only.
- **NON-SPECIFIC or NO MODULE:** no recognizable partner system at this resolution. It does not show vaults lack
  partners: coarse OGs hide paralog-level losses, and small complexes may not enrich a GO term.

## Limits
Taxonomy polytomies blur event placement. Sampling is uneven. eggNOG 5 dates from 2019. OG absence can reflect
annotation or clustering. MVP has a limited number of events, which caps resolution.
